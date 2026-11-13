"""Five remaining J2563 archive composites. No generation and no spend.

Sources are the five files downloaded after the Wikimedia hold cleared.
P5:07a uses Wellcome L0058154, the Snow-type inhaler photograph.
Its corner credit stays off screen because a name card already occupies the row.
"""
import argparse, hashlib, json, subprocess
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFont
import Quartz
from Cocoa import NSURL, NSBitmapImageRep, NSCalibratedRGBColorSpace, NSPNGFileType, NSGraphicsContext

HERE = Path(__file__).resolve().parent
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
W, H, FPS = 1920, 1080, 30
PAPER = (53, 34, 24)
CREAM = (245, 234, 209)
GOLD = (195, 146, 60)
MAT = (224, 207, 173)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def font(size):
    return ImageFont.truetype(FONT, size, index=1)


def frames_for(row):
    start = round(row["in_s"] * FPS)
    end = round(row["out_s"] * FPS)
    return end - start


def pdf_page(path, index, scale=4):
    doc = Quartz.PDFDocument.alloc().initWithURL_(NSURL.fileURLWithPath_(str(path)))
    page = doc.pageAtIndex_(index)
    rect = page.boundsForBox_(Quartz.kPDFDisplayBoxMediaBox)
    pw, ph = int(rect.size.width * scale), int(rect.size.height * scale)
    rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
        None, pw, ph, 8, 4, True, False, NSCalibratedRGBColorSpace, 0, 0)
    ctx = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.setCurrentContext_(ctx)
    cg = ctx.CGContext()
    Quartz.CGContextSetRGBFillColor(cg, 1, 1, 1, 1)
    Quartz.CGContextFillRect(cg, Quartz.CGRectMake(0, 0, pw, ph))
    Quartz.CGContextScaleCTM(cg, scale, scale)
    page.drawWithBox_(Quartz.kPDFDisplayBoxMediaBox)
    NSGraphicsContext.restoreGraphicsState()
    data = rep.representationUsingType_properties_(NSPNGFileType, None)
    return Image.open(BytesIO(bytes(data))).convert("RGB")


def crop_frac(im, box):
    w, h = im.size
    l, t, r, b = box
    return im.crop((int(l * w), int(t * h), int(r * w), int(b * h)))


def expand(box, amount):
    l, t, r, b = box
    return (max(0, l - amount), max(0, t - amount), min(1, r + amount), min(1, b + amount))


def lerp_box(start, end, phase):
    return tuple(a + (b - a) * phase for a, b in zip(start, end))


def luma_ok(im):
    vals = sorted(im.resize((96, 54)).convert("L").getdata())
    mean = sum(vals) / len(vals)
    p95 = vals[int(len(vals) * 0.95) - 1]
    return mean >= 28 or p95 >= 50, mean, p95


def fit(im, box):
    plate = crop_frac(im, box)
    plate.thumbnail((1680, 900), Image.Resampling.LANCZOS)
    return plate


def draw_credit(canvas, text, alpha):
    if alpha <= 0:
        return
    layer = Image.new("RGBA", canvas.size)
    draw = ImageDraw.Draw(layer)
    face = font(28)
    while draw.textbbox((0, 0), text, font=face)[2] > 1760 and face.size > 18:
        face = font(face.size - 2)
    draw.text((48, 1010), text, font=face, fill=(*CREAM, int(255 * alpha)))
    canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), layer).convert("RGB"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    plan = json.loads((HERE / "PICTURE_PLAN_v03.json").read_text())
    rows = {row["row_id"]: row for row in plan["rows"]}
    sources = {
        "P5:03a_arch_squire_inhaler_1846": args.sources / "P5_03a_squire_L0057829.jpg",
        "P5:04a": args.sources / "P5_04a_liston_M0005603.jpg",
        "P5:06a_arch_simpson_1847": args.sources / "P5_06a_simpson_66950610.pdf",
        "P5:07a_arch_snow_chloroform_1858": args.sources / "P5_07a_snow_L0058154.jpg",
        "P5:14a": args.sources / "P5_14a_lister_M0003436.jpg",
    }
    expected = {
        "P5_03a_squire_L0057829.jpg": 520680,
        "P5_04a_liston_M0005603.jpg": 7519367,
        "P5_06a_simpson_66950610.pdf": 1640119,
        "P5_07a_snow_L0058154.jpg": 1503513,
        "P5_14a_lister_M0003436.jpg": 5169472,
    }
    for path in sources.values():
        size = path.stat().st_size
        if size != expected[path.name]:
            raise SystemExit(f"{path.name} is {size} bytes, expected {expected[path.name]}")
    specs = [
        {
            "row_id": "P5:03a_arch_squire_inhaler_1846",
            "credit": "Squire Ether Inhaler (1846), Wellcome / CC BY 4.0",
            "show_credit": True,
            "end": (0.10, 0.02, 0.90, 0.96),
            "page_url": "https://commons.wikimedia.org/wiki/File:Copy_of_the_Squire-type_ether_inhaler_first_used_in_1846_Wellcome_L0057829.jpg",
            "licence": "CC BY 4.0. Wellcome Collection photograph L0057829.",
            "reconciliation": "Photograph of a Squire-type copy, Wellcome L0057829. Not an 1846 engraving.",
        },
        {
            "row_id": "P5:04a",
            "credit": "E. Board, Liston Operating (1846), Wellcome / CC BY 4.0",
            "show_credit": True,
            "end": (0.04, 0.02, 0.98, 0.98),
            "page_url": "https://commons.wikimedia.org/wiki/File:Robert_Liston_operating._Wellcome_M0005603.jpg",
            "licence": "CC BY 4.0. Wellcome Collection M0005603, Ernest Board.",
            "reconciliation": "Wellcome M0005603, Ernest Board's painting of Liston operating. The approved credit line is on screen for 3.5 s.",
        },
        {
            "row_id": "P5:06a_arch_simpson_1847",
            "credit": "Simpson, Account of a New Anaesthetic Agent (1847)",
            "show_credit": True,
            "end": (0.08, 0.04, 0.92, 0.78),
            "page_url": "https://commons.wikimedia.org/wiki/File:An_account_of_a_new_anaesthetic_agent_as_a_substitute_for_sulphuric_ether_in_surgery_and_midwifery_(IA_66950610R.nlm.nih.gov).pdf",
            "licence": "Public domain. NLM scan 66950610R.",
            "reconciliation": "Title page is the 1848 New York third American edition. It prints the Edinburgh communication of 10 November 1847. The gold line grows under NEW ANAESTHETIC AGENT.",
            "underline": 0.40,
        },
        {
            "row_id": "P5:07a_arch_snow_chloroform_1858",
            "credit": "Snow-type chloroform inhaler (1848-1870), Wellcome L0058154 / CC BY 4.0",
            "show_credit": False,
            "end": (0.06, 0.06, 0.94, 0.94),
            "page_url": "https://commons.wikimedia.org/wiki/File:Snow-type_chloroform_inhaler,_London,_England,_1848-1870_Wellcome_L0058154.jpg",
            "licence": "CC BY 4.0. Wellcome Collection photograph L0058154.",
            "reconciliation": "JSON alternate L0058154, not the Snow book PDF. Corner credit stays off because the John Snow name card occupies this row.",
        },
        {
            "row_id": "P5:14a",
            "credit": "Cheyne, Antiseptic Surgery (1882), Wellcome / CC BY 4.0",
            "show_credit": True,
            "end": (0.02, 0.02, 0.98, 0.74),
            "page_url": "https://commons.wikimedia.org/wiki/File:Use_of_the_Lister_carbolic_spray,_Antiseptic_surgery,_1882._Wellcome_M0003436.jpg",
            "licence": "CC BY 4.0. Wellcome Collection M0003436.",
            "reconciliation": "Wellcome M0003436. The frame holds the operating scene and leaves the long caption below the crop.",
        },
    ]
    images = {}
    for spec in specs:
        path = sources[spec["row_id"]]
        if path.suffix == ".pdf":
            images[spec["row_id"]] = pdf_page(path, 4, 4)
        else:
            images[spec["row_id"]] = Image.open(path).convert("RGB")
    result = {
        "job": "J2563",
        "film_stage_approved": False,
        "motion_review": False,
        "audio_review": False,
        "spend_gbp": 0,
        "credits_used": 0,
        "rows": [],
    }
    for spec in specs:
        row = rows[spec["row_id"]]
        frames = frames_for(row)
        if frames <= 0 or frames > 240:
            raise SystemExit(f"{spec['row_id']} is {frames} frames")
        source = images[spec["row_id"]]
        sample = fit(source, spec["end"])
        canvas = Image.new("RGB", (W, H), PAPER)
        canvas.paste(sample, ((W - sample.width) // 2, 80))
        ok, mean, p95 = luma_ok(canvas)
        lift = 1.0
        if not ok:
            lift = 1.25
            source = ImageEnhance.Brightness(source).enhance(lift)
            images[spec["row_id"]] = source
        target = args.out / (spec["row_id"].replace(":", "_") + ".mp4")
        proc = subprocess.Popen(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
             "-s", "1920x1080", "-r", "30", "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast",
             "-crf", "18", "-pix_fmt", "yuv420p", str(target)], stdin=subprocess.PIPE)
        checks = []
        start_box = expand(spec["end"], 0.04)
        for n in range(frames):
            phase = n / max(1, frames - 1)
            plate = fit(source, lerp_box(start_box, spec["end"], phase))
            frame = Image.new("RGB", (W, H), PAPER)
            x = (W - plate.width) // 2 + round(10 * (phase - 0.5))
            y = 70
            draw = ImageDraw.Draw(frame)
            draw.rectangle((x - 14, y - 14, x + plate.width + 14, y + plate.height + 14), fill=MAT)
            frame.paste(plate, (x, y))
            if spec.get("underline") is not None:
                grow = min(1, n / (FPS * 1.4))
                line_y = y + int(plate.height * spec["underline"])
                line_w = int(plate.width * 0.62 * grow)
                line_x = x + (plate.width - int(plate.width * 0.62)) // 2
                if grow > 0:
                    draw.line((line_x, line_y, line_x + line_w, line_y), fill=GOLD, width=4)
            if spec["show_credit"]:
                fade = min(1, n / (FPS * 0.35))
                if n < int(3.5 * FPS):
                    draw_credit(frame, spec["credit"], fade)
            ok, mean, p95 = luma_ok(frame)
            checks.append((ok, mean, p95))
            if n == frames // 2:
                frame.save(args.out / (target.stem + "_layout.jpg"), quality=85)
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise SystemExit(f"ffmpeg failed for {spec['row_id']}")
        if not all(item[0] for item in checks):
            raise SystemExit(f"near-black frame in {spec['row_id']}")
        probe = json.loads(subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(target)]))["streams"][0]
        if (int(probe["width"]), int(probe["height"]), probe["avg_frame_rate"], int(probe["nb_frames"])) != (1920, 1080, "30/1", frames):
            raise SystemExit(f"{spec['row_id']} probe {probe['width']}x{probe['height']} {probe['nb_frames']} != {frames}")
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(target), "-f", "null", "-"], check=True)
        result["rows"].append({
            "row_id": spec["row_id"],
            "path": str(target),
            "sha256": sha(target),
            "source_file": sources[spec["row_id"]].name,
            "source_sha256": sha(sources[spec["row_id"]]),
            "source_bytes": sources[spec["row_id"]].stat().st_size,
            "source_url": spec["page_url"],
            "licence": spec["licence"],
            "credit": spec["credit"],
            "credit_on_screen": spec["show_credit"],
            "credit_seconds": 3.5 if spec["show_credit"] else 0,
            "frames": frames,
            "plan_in_s": row["in_s"],
            "plan_out_s": row["out_s"],
            "brightness_lift": lift,
            "luma_mean_min": round(min(item[1] for item in checks), 2),
            "luma_p95_min": round(min(item[2] for item in checks), 2),
            "review_status": "preliminary: still layout inspected; capable motion review required",
            "reconciliation": spec["reconciliation"],
        })
        print(spec["row_id"], frames, "rendered", flush=True)
    (args.out / "ARCHIVE_COMPOSITES_v09.json").write_text(json.dumps(result, indent=2) + "\n")
    print("PASS five archive composites")


if __name__ == "__main__":
    main()
