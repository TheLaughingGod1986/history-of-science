import AppKit
import Foundation

// Cream-on-brown HOS thumbs from film frames. No Orbit robot.

let args = CommandLine.arguments
guard args.count >= 4 else {
    fputs("usage: compose in.jpg out.png TITLE\n", stderr)
    exit(1)
}
let srcURL = URL(fileURLWithPath: args[1])
let outURL = URL(fileURLWithPath: args[2])
let line = args[3]
guard let src = NSImage(contentsOf: srcURL) else {
    fputs("bad image \(srcURL.path)\n", stderr)
    exit(1)
}

let w = 1280.0
let h = 720.0
let img = NSImage(size: NSSize(width: w, height: h))
img.lockFocus()
let dst = NSRect(x: 0, y: 0, width: w, height: h)
src.draw(in: dst, from: .zero, operation: .copy, fraction: 1)

let brown = NSColor(srgbRed: 0.24, green: 0.16, blue: 0.11, alpha: 1)
let cream = NSColor(srgbRed: 0.961, green: 0.910, blue: 0.824, alpha: 1)
let fade = NSGradient(colors: [
    NSColor(srgbRed: 0.24, green: 0.16, blue: 0.11, alpha: 0),
    NSColor(srgbRed: 0.24, green: 0.16, blue: 0.11, alpha: 0.88),
    brown,
])
fade?.draw(in: NSRect(x: 0, y: 0, width: w, height: 210), angle: 90)

let bar = NSRect(x: 36, y: 28, width: w - 72, height: 78)
brown.setFill()
NSBezierPath(roundedRect: bar, xRadius: 10, yRadius: 10).fill()
cream.setStroke()
let stroke = NSBezierPath(roundedRect: bar.insetBy(dx: 1.5, dy: 1.5), xRadius: 9, yRadius: 9)
stroke.lineWidth = 1.6
stroke.stroke()

let font =
    NSFont(name: "Didot-Italic", size: 36)
    ?? NSFont(name: "HoeflerText-Italic", size: 36)
    ?? NSFont.systemFont(ofSize: 34, weight: .regular)
let text = NSAttributedString(
    string: line,
    attributes: [.font: font, .foregroundColor: cream]
)
let tsz = text.size()
text.draw(at: NSPoint(
    x: bar.midX - tsz.width / 2,
    y: bar.midY - tsz.height / 2
))
img.unlockFocus()

guard let tiff = img.tiffRepresentation,
      let rep = NSBitmapImageRep(data: tiff),
      let png = rep.representation(using: .png, properties: [:])
else {
    fputs("png fail\n", stderr)
    exit(1)
}
try png.write(to: outURL)
fputs("WROTE \(outURL.path)\n", stderr)
