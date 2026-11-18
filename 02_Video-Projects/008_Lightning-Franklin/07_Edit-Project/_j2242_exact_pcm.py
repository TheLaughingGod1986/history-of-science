"""Exact High-profile pictures for the four blocked Franklin runs.

x264 will not encode lossless High profile, and a 4:4:4 lossless patch
broke later copied packets. These runs still have to match the master
frame hashes. An I_PCM picture is legal inside High profile: the samples
are the pixels, and deblocking is switched off so the filter cannot
change them.

The four runs are the ones the reference check blocked. Frame 2869, frame
3259, frames 4130-4138 and frames 11118-11245. This writes a silent clip.
It is not hos_008_master_v04.mp4, and it does not touch the master.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

BLOCKED = ((2869, 2869), (3259, 3259), (4130, 4138), (11118, 11245))
MASTER_SPS = bytes.fromhex('67640028acd940780227e584000003000400000300c03c60c658')
CODED_HEIGHT = 1088
VISIBLE = (1920, 1080)
FRAME_BYTES = 1920 * 1080 * 3 // 2


class Writer:
    def __init__(self):
        self.buf = bytearray()
        self.acc = 0
        self.n = 0

    def u(self, value, count):
        if count < 0 or value < 0 or value >= (1 << count):
            raise ValueError(f'Bit field {value} does not fit in {count} bits')
        for shift in range(count - 1, -1, -1):
            self.acc = (self.acc << 1) | ((value >> shift) & 1)
            self.n += 1
            if self.n == 8:
                self.buf.append(self.acc)
                self.acc = 0
                self.n = 0

    def ue(self, value):
        if value < 0:
            raise ValueError('Unsigned Exp-Golomb cannot be negative')
        code = value + 1
        width = code.bit_length() - 1
        self.u(0, width)
        self.u(code, width + 1)

    def se(self, value):
        mapped = 2 * value - 1 if value > 0 else -2 * value
        self.ue(mapped)

    def align(self):
        if self.n:
            self.u(0, 8 - self.n)

    def trailing(self):
        self.u(1, 1)
        self.align()

    def bytes(self):
        if self.n:
            raise ValueError('Bitstream ended mid-byte')
        return bytes(self.buf)


def rbsp_to_nal(header, rbsp):
    """Annex B payload with emulation-prevention bytes."""
    if not 0 <= header <= 255:
        raise ValueError('NAL header is one byte')
    out = bytearray([header])
    zeros = 0
    for byte in rbsp:
        if zeros >= 2 and byte <= 3:
            out.append(3)
            zeros = 0
        out.append(byte)
        zeros = zeros + 1 if byte == 0 else 0
    return bytes(out)


def annexb(*payloads):
    return b''.join(b'\x00\x00\x00\x01' + payload for payload in payloads)


def tiny_sps():
    """16x16 High profile, used only to prove the sample order."""
    w = Writer()
    w.u(100, 8)
    w.u(0, 8)
    w.u(31, 8)
    w.ue(0)
    w.ue(1)
    w.ue(0)
    w.ue(0)
    w.u(0, 1)
    w.u(0, 1)
    w.ue(0)
    w.ue(0)
    w.ue(2)
    w.ue(1)
    w.u(0, 1)
    w.ue(0)
    w.ue(0)
    w.u(1, 1)
    w.u(1, 1)
    w.u(0, 1)
    w.u(0, 1)
    w.trailing()
    return rbsp_to_nal(0x67, w.bytes())


def cavlc_pps(pps_id=0):
    """Same shape as the master PPS, with CABAC off and deblocking present."""
    if pps_id < 0:
        raise ValueError('PPS id cannot be negative')
    w = Writer()
    w.ue(pps_id)
    w.ue(0)
    w.u(0, 1)
    w.u(0, 1)
    w.ue(0)
    w.ue(0)
    w.ue(0)
    w.u(0, 1)
    w.u(0, 2)
    w.se(0)
    w.se(0)
    w.se(0)
    w.u(1, 1)
    w.u(0, 1)
    w.u(0, 1)
    w.u(0, 1)
    w.u(0, 1)
    w.se(0)
    w.trailing()
    return rbsp_to_nal(0x68, w.bytes())


def require_blocked(first, last):
    if (first, last) not in BLOCKED:
        raise ValueError(f'Frames {first}-{last} are not a blocked exact run')
    return first, last


def refuse_master_name(path):
    path = Path(path)
    if 'master_v04' in path.name or path.suffix.lower() not in {'.h264', '.mp4'}:
        raise ValueError('Exact clip must not be named as the v04 master')
    return path


def _planes(frame, width, height):
    if len(frame) != width * height * 3 // 2:
        raise ValueError('Frame is not yuv420p of the expected size')
    y_size = width * height
    c_size = (width // 2) * (height // 2)
    y = frame[:y_size]
    u = frame[y_size:y_size + c_size]
    v = frame[y_size + c_size:]
    return y, u, v


def _pad(frame, width, height, coded_height):
    if coded_height < height or coded_height % 16 or width % 16:
        raise ValueError('Coded size is not a whole macroblock frame')
    y, u, v = _planes(frame, width, height)
    pad_y = coded_height - height
    pad_c = pad_y // 2
    y += bytes(width * pad_y)
    u += bytes((width // 2) * pad_c)
    v += bytes((width // 2) * pad_c)
    return y, u, v, coded_height


def _mb(y, u, v, width, mb_x, mb_y):
    luma = bytearray()
    y0 = mb_y * 16
    x0 = mb_x * 16
    for row in range(16):
        start = (y0 + row) * width + x0
        luma += y[start:start + 16]
    chroma = bytearray()
    c_width = width // 2
    cy = mb_y * 8
    cx = mb_x * 8
    for plane in (u, v):
        for row in range(8):
            start = (cy + row) * c_width + cx
            chroma += plane[start:start + 8]
    if len(luma) != 256 or len(chroma) != 128:
        raise ValueError('Macroblock is not 4:2:0')
    return bytes(luma) + bytes(chroma)


def ipcm_idr(frame, width, height, coded_height, pps_id, idr_id):
    """One IDR access unit whose visible pixels are the frame."""
    if idr_id < 0 or idr_id > 65535:
        raise ValueError('IDR id is out of range')
    y, u, v, coded = _pad(frame, width, height, coded_height)
    w = Writer()
    w.ue(0)
    w.ue(2)
    w.ue(pps_id)
    w.u(0, 4)
    w.ue(idr_id)
    w.u((idr_id * 2) & 63, 6)
    w.u(0, 1)
    w.u(0, 1)
    w.se(0)
    w.ue(1)
    mb_w = width // 16
    mb_h = coded // 16
    for mb_y in range(mb_h):
        for mb_x in range(mb_w):
            w.ue(25)
            w.align()
            w.buf += _mb(y, u, v, width, mb_x, mb_y)
            if w.n:
                raise ValueError('PCM samples left the bitstream mid-byte')
    w.trailing()
    return rbsp_to_nal(0x65, w.bytes())


def access_unit(frame, width, height, coded_height, sps, pps_id, idr_id):
    return annexb(sps, cavlc_pps(pps_id), ipcm_idr(
        frame, width, height, coded_height, pps_id, idr_id))


def deblocking_disabled(slice_payload):
    """The slice asks for deblocking off. A filter would change exact pixels."""
    from _j2242_ref_check import Bits

    rbsp = bytearray()
    raw = slice_payload[1:]
    i = 0
    while i < len(raw):
        if i + 2 < len(raw) and raw[i] == 0 and raw[i + 1] == 0 and raw[i + 2] == 3:
            rbsp += bytes(raw[i:i + 2])
            i += 3
        else:
            rbsp.append(raw[i])
            i += 1
    bits = Bits(bytes(rbsp))
    bits.ue()
    if bits.ue() != 2:
        raise ValueError('Exact picture is not an I slice')
    bits.ue()
    bits.u(4)
    bits.ue()
    bits.u(6)
    bits.u(1)
    bits.u(1)
    bits.se()
    return bits.ue() == 1


def decode_annexb(path, width, height):
    raw = subprocess.run(
        ['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(path),
         '-an', '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-'],
        check=True, capture_output=True).stdout
    size = width * height * 3 // 2
    if len(raw) % size:
        raise ValueError('Decoded size is not a whole number of frames')
    return [raw[i:i + size] for i in range(0, len(raw), size)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--first', type=int, required=True)
    parser.add_argument('--last', type=int, required=True)
    parser.add_argument('--yuv', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    first, last = require_blocked(args.first, args.last)
    out = refuse_master_name(args.out)
    blob = args.yuv.read_bytes()
    count = last - first + 1
    if len(blob) != count * FRAME_BYTES:
        raise ValueError(f'YUV has {len(blob)} bytes, not {count} master frames')
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        raise ValueError('Exact clip already exists')
    parts = []
    for index in range(count):
        frame = blob[index * FRAME_BYTES:(index + 1) * FRAME_BYTES]
        parts.append(access_unit(
            frame, VISIBLE[0], VISIBLE[1], CODED_HEIGHT, MASTER_SPS, 1, index))
    out.write_bytes(b''.join(parts))
    decoded = decode_annexb(out, VISIBLE[0], VISIBLE[1])
    if decoded != [blob[i:i + FRAME_BYTES] for i in range(0, len(blob), FRAME_BYTES)]:
        raise ValueError('Decoded pictures do not match the master pixels')
    report = {
        'job': 'J2242',
        'status': 'EXACT_PCM_CLIP',
        'first': first,
        'last': last,
        'frames': count,
        'path': str(out),
        'sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
        'bytes': out.stat().st_size,
        'profile': 'High',
        'pix_fmt': 'yuv420p',
        'deblocking': 'off',
        'pixels_match': True,
        'audio': False,
        'finished_master': False,
        'approval': False,
        'spend_gbp': 0,
    }
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
