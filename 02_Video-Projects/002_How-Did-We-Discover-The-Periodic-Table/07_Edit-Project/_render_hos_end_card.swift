import AppKit

// Cream-on-brown HOS end card. No subscribe, URL, Orbit, Oppti.
let out = URL(fileURLWithPath: CommandLine.arguments[1])
let w = 1280.0
let h = 720.0
let img = NSImage(size: NSSize(width: w, height: h))
img.lockFocus()
NSColor(srgbRed: 0.24, green: 0.16, blue: 0.11, alpha: 1).setFill()
NSBezierPath.fill(NSRect(x: 0, y: 0, width: w, height: h))
let cream = NSColor(srgbRed: 0.961, green: 0.910, blue: 0.824, alpha: 1)
let titleFont =
    NSFont(name: "Didot-Italic", size: 52)
    ?? NSFont(name: "HoeflerText-Italic", size: 52)
    ?? NSFont.systemFont(ofSize: 52, weight: .regular)
let lineFont =
    NSFont(name: "Didot", size: 22)
    ?? NSFont(name: "HoeflerText-Regular", size: 22)
    ?? NSFont.systemFont(ofSize: 22, weight: .regular)
let title = NSAttributedString(
    string: "History of Science",
    attributes: [.font: titleFont, .foregroundColor: cream]
)
let line = NSAttributedString(
    string: "DISCOVERY.  WONDER.  PROOF.",
    attributes: [
        .font: lineFont,
        .foregroundColor: cream,
        .kern: 3.2,
    ]
)
let tsz = title.size()
let lsz = line.size()
let gap = 22.0
let block = tsz.height + gap + lsz.height
let y0 = (h - block) / 2
title.draw(at: NSPoint(x: (w - tsz.width) / 2, y: y0 + lsz.height + gap))
line.draw(at: NSPoint(x: (w - lsz.width) / 2, y: y0))
img.unlockFocus()
guard let tiff = img.tiffRepresentation,
      let rep = NSBitmapImageRep(data: tiff),
      let png = rep.representation(using: .png, properties: [:])
else {
    fputs("png fail\n", stderr)
    exit(1)
}
try png.write(to: out)
fputs("WROTE \(out.path)\n", stderr)
