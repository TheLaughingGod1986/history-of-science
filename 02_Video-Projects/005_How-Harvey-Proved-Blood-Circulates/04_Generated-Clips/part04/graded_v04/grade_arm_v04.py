#!/usr/bin/env python3
"""HOS 005 Part 04 arm grade v04 (desk 5952762841 / 5953047660, 3 Oct 2026).
Takes the grey/blue cast off the forearm and hand below the band on plates 03/04/05 so the hand keeps a
natural skin tone (Willis tr. ch. 11: 'retains its natural colour'). Keeps the glowing blue veins, the red
above the band, the linen band, wood and wall untouched. Pixel grade only: no remint, no Vertex spend.
Mask = low-chroma, cool-or-neutral, mid-luminance pixels (the grey arm); vivid blue (veins) and warm pixels
(wood, linen, wall, red sleeve) are excluded. Luminance is kept and lifted slightly; chroma becomes skin.
  ~/.venvs/hos-vo/bin/python grade_arm_v04.py <in.mp4> <out.mp4|out.jpg>"""
import subprocess, sys
import numpy as np
SKIN = np.array([1.27, 0.96, 0.64])   # skin chroma at equal luminance (matched to plate 06 / graded v03)
LIFT = 1.18
def mask(f):
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    c = f.max(2) - f.min(2)
    br = b - r
    warm = -br / np.maximum(lum, 1)   # wood ~0.8, linen/wall ~0.45, grey arm ~0.2, cool arm < 0
    w = (np.clip((95 - c) / 25, 0, 1) * np.clip((0.34 - warm) / 0.1, 0, 1) * np.clip((lum - 30) / 20, 0, 1)
         * np.clip((222 - lum) / 15, 0, 1) * np.clip((100 - br) / 25, 0, 1))
    # soften: 8x8 box blur via down/up sample
    h, wd = w.shape
    k = 8
    s = w[: h // k * k, : wd // k * k].reshape(h // k, k, wd // k, k).mean((1, 3))
    s = np.repeat(np.repeat(s, k, 0), k, 1)
    out = np.zeros_like(w); out[: s.shape[0], : s.shape[1]] = s
    out[s.shape[0]:, :] = out[s.shape[0] - 1: s.shape[0], :]
    return np.minimum(w, out) * 0.5 + w * 0.5, lum
def grade(f):
    w, lum = mask(f)
    skin = np.clip(lum[..., None] * LIFT * SKIN, 0, 255)
    return np.clip(f * (1 - w[..., None]) + skin * w[..., None], 0, 255)
def main():
    src, dst = sys.argv[1:3]
    pr = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                  "stream=width,height,r_frame_rate", "-of", "csv=p=0", src], text=True).strip()
    W, H, fr = pr.split(","); W, H = int(W), int(H)
    still = dst.endswith(".jpg")
    dec = subprocess.Popen(["ffmpeg", "-v", "error", *(["-ss", "3"] if still else []), "-i", src,
                            *(["-frames:v", "1"] if still else []), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", fr, "-i", "-",
                            *(["-q:v", "3"] if still else ["-c:v", "libx264", "-preset", "medium", "-crf", "14",
                                                            "-pix_fmt", "yuv420p"]), dst], stdin=subprocess.PIPE)
    n = W * H * 3
    while True:
        buf = dec.stdout.read(n)
        if len(buf) < n: break
        f = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32)
        enc.stdin.write(grade(f).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()
    print("wrote", dst)
if __name__ == "__main__":
    main()
