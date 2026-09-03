import AppKit

let out = URL(fileURLWithPath: CommandLine.arguments[1])
let w = 1280.0
let h = 720.0
let img = NSImage(size: NSSize(width: w, height: h))
img.lockFocus()
NSColor.clear.setFill()
NSBezierPath.fill(NSRect(x: 0, y: 0, width: w, height: h))
let font =
    NSFont(name: "DINCondensed-Bold", size: 108)
    ?? NSFont.systemFont(ofSize: 108, weight: .heavy)
let stroke: [NSAttributedString.Key: Any] = [
    .font: font,
    .foregroundColor: NSColor.black,
    .strokeColor: NSColor.black,
    .strokeWidth: 12.0,
]
let fill: [NSAttributedString.Key: Any] = [
    .font: font,
    .foregroundColor: NSColor.white,
    .strokeWidth: 0,
]
let text = "A LIVING CLOUD"
let sStroke = NSAttributedString(string: text, attributes: stroke)
let sFill = NSAttributedString(string: text, attributes: fill)
let sz = sFill.size()
let origin = NSPoint(x: (w - sz.width) / 2, y: (h - sz.height) / 2)
sStroke.draw(at: origin)
sFill.draw(at: origin)
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
