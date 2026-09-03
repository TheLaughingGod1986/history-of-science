import AVFoundation
import Foundation

/// Original underscore: slow Cmaj7–Am7–Fmaj7–Gsus on Apple DLS warm pad + sparse piano.
/// Licensed GM samples (gs_instruments.dls). Not a ripped song.

let dls = URL(
    fileURLWithPath:
        "/System/Library/Components/CoreAudio.component/Contents/Resources/gs_instruments.dls"
)
let outURL = URL(fileURLWithPath: CommandLine.arguments[1])
let durationSec = Double(CommandLine.arguments.count > 2 ? CommandLine.arguments[2] : "80") ?? 80

let sr: Double = 48000
let format = AVAudioFormat(standardFormatWithSampleRate: sr, channels: 2)!
let engine = AVAudioEngine()
let pad = AVAudioUnitSampler()
let piano = AVAudioUnitSampler()
engine.attach(pad)
engine.attach(piano)
engine.connect(pad, to: engine.mainMixerNode, format: nil)
engine.connect(piano, to: engine.mainMixerNode, format: nil)
engine.mainMixerNode.outputVolume = 0.55

do {
    try pad.loadInstrument(at: dls)
    try piano.loadInstrument(at: dls)
} catch {
    fputs("DLS load failed: \(error)\n", stderr)
    exit(1)
}

// GM: bankMSB 0x79 = melodic. 89 = Pad 2 (warm). 0 = Acoustic Grand.
pad.sendProgramChange(89, bankMSB: 0x79, bankLSB: 0, onChannel: 0)
piano.sendProgramChange(0, bankMSB: 0x79, bankLSB: 0, onChannel: 0)

do {
    try engine.enableManualRenderingMode(.offline, format: format, maximumFrameCount: 4096)
    try engine.start()
} catch {
    fputs("engine: \(error)\n", stderr)
    exit(1)
}

struct Hit {
    let t: Double
    let notes: [UInt8]
    let vel: UInt8
    let dur: Double
    let unit: AVAudioUnitSampler
}

let chords: [[UInt8]] = [
    [48, 55, 64, 71], // Cmaj7
    [45, 52, 60, 67], // Am7
    [41, 48, 57, 64], // Fmaj7
    [43, 50, 57, 62], // Gsus
]
var hits: [Hit] = []
var t = 0.0
let bar = 8.0
while t < durationSec {
    let chord = chords[Int(t / bar) % chords.count]
    let hold = min(bar, durationSec - t + 0.8)
    hits.append(Hit(t: t, notes: chord, vel: 42, dur: hold, unit: pad))
    hits.append(Hit(t: t, notes: [chord[0]], vel: 28, dur: 1.6, unit: piano))
    t += bar
}

var onI = 0
var off: [(Double, UInt8, AVAudioUnitSampler)] = []
let framesTotal = AVAudioFramePosition(durationSec * sr)
var pos: AVAudioFramePosition = 0
guard let buf = AVAudioPCMBuffer(pcmFormat: format, frameCapacity: 4096) else {
    fputs("buffer alloc failed\n", stderr)
    exit(1)
}

var pcm = [Float]()
pcm.reserveCapacity(Int(framesTotal) * 2)

while pos < framesTotal {
    let now = Double(pos) / sr
    while onI < hits.count && hits[onI].t <= now + 0.002 {
        let h = hits[onI]
        for n in h.notes {
            h.unit.startNote(n, withVelocity: h.vel, onChannel: 0)
            off.append((h.t + h.dur, n, h.unit))
        }
        onI += 1
    }
    off.sort { $0.0 < $1.0 }
    while let first = off.first, first.0 <= now {
        first.2.stopNote(first.1, onChannel: 0)
        off.removeFirst()
    }
    let n = min(AVAudioFrameCount(4096), AVAudioFrameCount(framesTotal - pos))
    buf.frameLength = n
    do {
        try engine.renderOffline(n, to: buf)
    } catch {
        fputs("render: \(error)\n", stderr)
        exit(1)
    }
    let ch0 = buf.floatChannelData![0]
    let ch1 = buf.floatChannelData![1]
    for i in 0..<Int(n) {
        pcm.append(ch0[i])
        pcm.append(ch1[i])
    }
    pos += AVAudioFramePosition(n)
}

for o in off {
    o.2.stopNote(o.1, onChannel: 0)
}
engine.stop()

func writeWav(_ url: URL, samples: [Float], sampleRate: Double) throws {
    var header = Data()
    let dataBytes = samples.count * 2
    func u16(_ v: UInt16) { var x = v.littleEndian; header.append(Data(bytes: &x, count: 2)) }
    func u32(_ v: UInt32) { var x = v.littleEndian; header.append(Data(bytes: &x, count: 4)) }
    header.append(contentsOf: Array("RIFF".utf8))
    u32(UInt32(36 + dataBytes))
    header.append(contentsOf: Array("WAVEfmt ".utf8))
    u32(16)
    u16(1)
    u16(2)
    u32(UInt32(sampleRate))
    u32(UInt32(sampleRate * 4))
    u16(4)
    u16(16)
    header.append(contentsOf: Array("data".utf8))
    u32(UInt32(dataBytes))
    var body = Data(capacity: dataBytes)
    for s in samples {
        var v = Int16(max(-1, min(1, s)) * 32767).littleEndian
        body.append(Data(bytes: &v, count: 2))
    }
    try (header + body).write(to: url)
}

do {
    try writeWav(outURL, samples: pcm, sampleRate: sr)
    fputs("WROTE \(outURL.path) \(pcm.count / 2) samples\n", stderr)
} catch {
    fputs("write: \(error)\n", stderr)
    exit(1)
}
