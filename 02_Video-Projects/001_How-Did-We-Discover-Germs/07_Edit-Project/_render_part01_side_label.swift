import AppKit

// Usage: render TEXT OUT.png [left|right]
// Elegant Didot italic, upper-right by default; left = dark negative space.
// Never dead-center.
let text = CommandLine.arguments[1]
let out = URL(fileURLWithPath: CommandLine.arguments[2])
let side = CommandLine.arguments.count > 3 ? CommandLine.arguments[3] : "right"
let w = 1280.0
let h = 720.0
let img = NSImage(size: NSSize(width: w, height: h))
img.lockFocus()
NSColor.clear.setFill()
NSBezierPath.fill(NSRect(x: 0, y: 0, width: w, height: h))
let font =
    NSFont(name: "Didot-Italic", size: 46)
    ?? NSFont(name: "HoeflerText-Italic", size: 46)
    ?? NSFont.systemFont(ofSize: 46, weight: .regular)
let stroke: [NSAttributedString.Key: Any] = [
    .font: font,
    .foregroundColor: NSColor.black,
    .strokeColor: NSColor.black,
    .strokeWidth: 5.5,
]
let fill: [NSAttributedString.Key: Any] = [
    .font: font,
    .foregroundColor: NSColor.white,
    .strokeWidth: 0,
]
let sStroke = NSAttributedString(string: text, attributes: stroke)
let sFill = NSAttributedString(string: text, attributes: fill)
let sz = sFill.size()
let padR = 56.0
let padT = 78.0
let origin = side == "left"
    ? NSPoint(x: padR, y: h - padT - sz.height)
    : NSPoint(x: w - padR - sz.width, y: h - padT - sz.height)
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
fputs("WROTE \(out.path) \(text)\n", stderr)
