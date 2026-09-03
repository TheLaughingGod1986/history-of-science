import AppKit
import Foundation

// 9:16 cream-on-brown HOS Short cover. Picture-first. No Orbit robot.

let args = CommandLine.arguments
guard args.count >= 4 else {
    fputs("usage: compose in.jpg out.png TITLE\n", stderr)
    exit(1)
}
guard let src = NSImage(contentsOf: URL(fileURLWithPath: args[1])) else {
    fputs("bad image\n", stderr)
    exit(1)
}

let w = 1080.0
let h = 1920.0
let img = NSImage(size: NSSize(width: w, height: h))
img.lockFocus()
src.draw(in: NSRect(x: 0, y: 0, width: w, height: h), from: .zero, operation: .copy, fraction: 1)

let brown = NSColor(srgbRed: 0.24, green: 0.16, blue: 0.11, alpha: 1)
let cream = NSColor(srgbRed: 0.961, green: 0.910, blue: 0.824, alpha: 1)
let gold = NSColor(srgbRed: 0.93, green: 0.78, blue: 0.32, alpha: 1)
let fade = NSGradient(colors: [
    NSColor(srgbRed: 0.24, green: 0.16, blue: 0.11, alpha: 0),
    NSColor(srgbRed: 0.24, green: 0.16, blue: 0.11, alpha: 0.90),
    brown,
])
fade?.draw(in: NSRect(x: 0, y: 0, width: w, height: 320), angle: 90)

let bar = NSRect(x: 48, y: 56, width: w - 96, height: 168)
brown.setFill()
NSBezierPath(roundedRect: bar, xRadius: 14, yRadius: 14).fill()
gold.setStroke()
let stroke = NSBezierPath(roundedRect: bar.insetBy(dx: 2, dy: 2), xRadius: 12, yRadius: 12)
stroke.lineWidth = 3
stroke.stroke()

let font =
    NSFont(name: "Didot-Italic", size: 42)
    ?? NSFont(name: "HoeflerText-Italic", size: 40)
    ?? NSFont.systemFont(ofSize: 38, weight: .regular)
let para = NSMutableParagraphStyle()
para.alignment = .center
para.lineBreakMode = .byWordWrapping
let text = NSAttributedString(
    string: args[3],
    attributes: [
        .font: font,
        .foregroundColor: cream,
        .paragraphStyle: para,
    ]
)
let box = bar.insetBy(dx: 20, dy: 16)
text.draw(in: box)
img.unlockFocus()

guard let tiff = img.tiffRepresentation,
      let rep = NSBitmapImageRep(data: tiff),
      let png = rep.representation(using: .png, properties: [:])
else {
    fputs("png fail\n", stderr)
    exit(1)
}
try png.write(to: URL(fileURLWithPath: args[2]))
fputs("WROTE \(args[2])\n", stderr)
