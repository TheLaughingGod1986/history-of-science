"""Two cached archive composites for J2563. No network, no spend, no film-stage approval.

P4:03a uses the already downloaded 1854 certified copy of US patent 4,848.
P4:08b uses the already downloaded CC0 Ether Monument photograph DSC04197.
The photograph shows the Good Samaritan group and column capital. It does not
contain the inscription base, so the tilt stays inside the file.
"""
import argparse, hashlib, json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import Quartz
from Cocoa import NSURL, NSBitmapImageRep, NSCalibratedRGBColorSpace, NSPNGFileType, NSGraphicsContext
from io import BytesIO
from render_free_graphics_v02 import anchor, sha

HERE = Path(__file__).resolve().parent
FONT = '/System/Library/Fonts/Supplemental/Didot.ttc'
W, H, FPS = 1920, 1080, 30
PAPER = (53, 34, 24)
CREAM = (245, 234, 209)
INK = (92, 58, 28)
GOLD = (195, 146, 60)


def font(size):
    return ImageFont.truetype(FONT, size, index=1)


def pdf_page(path, index, scale=4):
    doc = Quartz.PDFDocument.alloc().initWithURL_(NSURL.fileURLWithPath_(str(path)))
    page = doc.pageAtIndex_(index)
    rect = page.boundsForBox_(Quartz.kPDFDisplayBoxMediaBox)
    pw, ph = float(rect.size.width), float(rect.size.height)
    w, h = int(pw * scale), int(ph * scale)
    rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
        None, w, h, 8, 4, True, False, NSCalibratedRGBColorSpace, 0, 0)
    ctx = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.setCurrentContext_(ctx)
    cg = ctx.CGContext()
    Quartz.CGContextSetRGBFillColor(cg, 1, 1, 1, 1)
    Quartz.CGContextFillRect(cg, Quartz.CGRectMake(0, 0, w, h))
    Quartz.CGContextScaleCTM(cg, scale, scale)
    page.drawWithBox_(Quartz.kPDFDisplayBoxMediaBox)
    NSGraphicsContext.restoreGraphicsState()
    data = rep.representationUsingType_properties_(NSPNGFileType, None)
    im = Image.open(BytesIO(bytes(data))).convert('RGB')
    return im, pw, ph


def crop_resize(im, pdf_box, page_h, scale, out_w, out_h):
    x0, y0, x1, y1 = pdf_box
    left, right = int(x0 * scale), int(x1 * scale)
    top, bottom = int((page_h - y1) * scale), int((page_h - y0) * scale)
    crop = im.crop((left, top, right, bottom))
    return crop.resize((out_w, out_h), Image.Resampling.LANCZOS)


def pdf_to_display(pdf_xywh, pdf_box, page_h, scale, crop_size, display_origin, display_size):
    x, y, bw, bh = pdf_xywh
    x0, y0, x1, y1 = pdf_box
    crop_w = (x1 - x0) * scale
    crop_h = (y1 - y0) * scale
    rel_x = (x - x0) * scale
    rel_y = (y1 - (y + bh)) * scale
    sx = display_size[0] / crop_w
    sy = display_size[1] / crop_h
    return (display_origin[0] + rel_x * sx, display_origin[1] + rel_y * sy,
            bw * scale * sx, bh * scale * sy)


def luma_ok(im):
    small = im.resize((96, 54)).convert('L')
    vals = sorted(small.getdata())
    mean = sum(vals) / len(vals)
    p95 = vals[int(len(vals) * 0.95) - 1]
    return mean >= 28 or p95 >= 50, mean, p95


def paste_mat(canvas, im, origin):
    d = ImageDraw.Draw(canvas)
    x, y = origin
    d.rectangle((x - 14, y - 14, x + im.width + 14, y + im.height + 14), fill=(224, 207, 173))
    canvas.paste(im, (x, y))


def draw_credit(d, text, y=1012):
    f = font(28)
    d.text((48, y), text, font=f, fill=CREAM)


def draw_label(d, text):
    f = font(58)
    box = d.textbbox((0, 0), text, font=f)
    d.text(((W - box[2]) / 2, 918), text, font=f, fill=CREAM)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sources', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=False)
    plan = json.loads((HERE / 'PICTURE_PLAN_v03.json').read_text())
    raw = json.loads((HERE.parent / plan['vo_lock']['stt_raw']).read_text())
    words = [dict(w, raw_index=i) for i, w in enumerate(raw['words']) if w['type'] == 'word']
    rows = {r['row_id']: r for r in plan['rows']}
    patent_pdf = a.sources / 'P4_03a_patent.pdf'
    monument_jpg = a.sources / 'P4_08b_ether_monument.jpg'
    page3, pw, ph = pdf_page(patent_pdf, 2, 4)
    page4, _, _ = pdf_page(patent_pdf, 3, 4)
    box3 = (28, 250, 338, 575)
    box4 = (24, 360, 340, 545)
    plate_size = (1100, 820)
    plate3 = crop_resize(page3, box3, ph, 4, *plate_size)
    plate4 = crop_resize(page4, box4, ph, 4, *plate_size)
    # PDF selection bounds measured on the downloaded file, page index 2 and 3.
    num_box = (151.5, 517.6, 37.7, 8.1)
    ether_box = (31.5, 434.2, 59.3, 8.8)
    monument = Image.open(monument_jpg).convert('RGB')
    result = {
        'job': 'J2563', 'film_stage_approved': False, 'motion_review': False, 'audio_review': False,
        'spend_gbp': 0, 'credits_used': 0, 'plan_sha256': sha(HERE / 'PICTURE_PLAN_v03.json'),
        'network': 'No requests in this render. Sources were saved before the later HTTP 429.',
        'rows': [],
    }
    specs = [
        {
            'row_id': 'P4:03a_arch_letheon_patent',
            'credit': 'US Patent No. 4,848 (12 Nov 1846), NLM / USPTO',
            'label': 'PATENT', 'phrase': 'patent',
            'source_file': patent_pdf,
            'source_url': 'https://commons.wikimedia.org/wiki/File:Copy_of_letters_patent_granted_to_W.T.G._Morton,_M.D._-_for_the_discovery_of_etherization,_together_with_the_specification_on_which_the_patent_issued_(IA_0313207.nlm.nih.gov).pdf',
            'licence': 'Public domain. 1854 certified copy of Letters Patent No. 4,848, granted 12 November 1846.',
            'reconciliation': 'Page 3 shows No. 4848 and the written date twelfth of November, eighteen hundred and forty-six. Page 4 shows the words sulphuric ether. The scan is the 1854 certified copy, not a new drawing.',
        },
        {
            'row_id': 'P4:08b_arch_ether_monument',
            'credit': 'Ether Monument (1868), Boston Public Garden / CC0',
            'label': 'MONUMENT', 'phrase': 'monument',
            'source_file': monument_jpg,
            'source_url': 'https://commons.wikimedia.org/wiki/File:Ether_Monument_-_Boston_Public_Garden_-_Boston,_MA_-_DSC04197.jpg',
            'licence': 'CC0. Photograph DSC04197 by Daderot.',
            'reconciliation': 'DSC04197 shows the Good Samaritan group and the column capital. The inscription base is not in this file, so the downward move stays inside the photograph.',
        },
    ]
    for spec in specs:
        r = rows[spec['row_id']]
        cue = anchor(words, spec['phrase'], r['in_s'], r['out_s'])
        cue.update(text=spec['label'], kind='label', out_s=min(cue['in_s'] + 1.5, r['out_s']))
        assert cue['in_s'] == words[cue['word_indices'][-1]]['start']
        frames = round(r['duration_s'] * FPS)
        target = a.out / (r['row_id'].replace(':', '_') + '.mp4')
        proc = subprocess.Popen(
            ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
             '-s', '1920x1080', '-r', '30', '-i', '-', '-an', '-c:v', 'libx264', '-preset', 'veryfast',
             '-crf', '18', '-pix_fmt', 'yuv420p', str(target)], stdin=subprocess.PIPE)
        credit_spans = []
        cursor = r['in_s']
        if cue['in_s'] > cursor:
            credit_spans.append((cursor, cue['in_s']))
        if cue['out_s'] < r['out_s']:
            credit_spans.append((cue['out_s'], r['out_s']))
        checks = []
        for n in range(frames):
            t = n / FPS
            absolute = r['in_s'] + t
            canvas = Image.new('RGB', (W, H), PAPER)
            d = ImageDraw.Draw(canvas)
            drift = round(6 * math.sin(t * 0.7))
            if spec['row_id'].startswith('P4:03a'):
                fade = max(0, min(1, (t - 2.05) / 0.7))
                plate = Image.blend(plate3, plate4, fade) if fade else plate3
                origin = (80 + drift, 70)
                paste_mat(canvas, plate, origin)
                shown = num_box if fade < 0.5 else ether_box
                box = box3 if fade < 0.5 else box4
                grow = min(1, max(0, (t - (0.35 if fade < 0.5 else 2.85)) / 0.45))
                dx, dy, dw, dh = pdf_to_display(shown, box, ph, 4, plate_size, origin, plate_size)
                if grow > 0:
                    d.rectangle((dx - 6, dy - 6, dx - 6 + (dw + 12) * grow, dy + dh + 6), outline=GOLD, width=3)
            else:
                sw, sh = monument.size
                view_h = int(sw * 900 / 1760)
                travel = sh - view_h
                top = int(travel * (t / r['duration_s']))
                crop = monument.crop((0, top, sw, top + view_h)).resize((1760, 900), Image.Resampling.LANCZOS)
                paste_mat(canvas, crop, (80, 48))
            active = cue['in_s'] <= absolute < cue['out_s']
            if active:
                draw_label(d, spec['label'])
            elif any(b <= absolute < e for b, e in credit_spans):
                draw_credit(d, spec['credit'])
            ok, mean, p95 = luma_ok(canvas)
            checks.append((ok, mean, p95))
            if n == frames // 2:
                canvas.save(a.out / (target.stem + '_layout.jpg'))
            proc.stdin.write(canvas.tobytes())
        proc.stdin.close()
        assert proc.wait() == 0
        assert all(ok for ok, _, _ in checks), checks[0]
        probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', str(target)]))['streams'][0]
        assert (probe['width'], probe['height'], probe['avg_frame_rate'], int(probe['nb_frames'])) == (1920, 1080, '30/1', frames)
        assert abs(float(probe['duration']) - r['duration_s']) < 1 / 60 + 0.00001
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(target), '-f', 'null', '-'], check=True)
        credits = [{'kind': 'archive_credit', 'text': spec['credit'], 'in_s': b, 'out_s': e, 'word_indices': [],
                    'reason': 'Credit stays off while the spoken label is on screen'} for b, e in credit_spans if e > b]
        for c in credits:
            assert c['out_s'] <= cue['in_s'] or cue['out_s'] <= c['in_s']
        result['rows'].append({
            'row_id': r['row_id'], 'path': str(target), 'sha256': sha(target),
            'source_sha256': sha(spec['source_file']), 'source_url': spec['source_url'],
            'licence': spec['licence'], 'frames': frames, 'duration_s': float(probe['duration']),
            'plan_in_s': r['in_s'], 'plan_out_s': r['out_s'], 'cues': [cue], 'credit_cues': credits,
            'luma_mean_min': min(m for _, m, _ in checks), 'luma_p95_min': min(p for _, _, p in checks),
            'review_status': 'preliminary: still layout inspected; capable motion review required',
            'reconciliation': spec['reconciliation'],
        })
        print(r['row_id'], 'rendered', flush=True)
    (a.out / 'ARCHIVE_COMPOSITES_v08.json').write_text(json.dumps(result, indent=2) + '\n')
    print('PASS render checks')


if __name__ == '__main__':
    main()
