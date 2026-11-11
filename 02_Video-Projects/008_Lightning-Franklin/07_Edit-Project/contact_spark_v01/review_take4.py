"""Reproducible J2613 still review; never writes a take or final film."""
import argparse
import json
from pathlib import Path
import subprocess
import numpy as np
from PIL import Image, ImageDraw
from render import BLOOM_PEAK, BLOOM_RADIUS, spark, sha

# f029 pre-glow, f030 peak, f031 half bloom. Core stays on f030 and f031 only.
FLASH = {
    29: dict(phase=0, bloom_scale=0.25, core=False),
    30: dict(phase=0, bloom_scale=1.0, core=True),
    31: dict(phase=1, bloom_scale=0.5, core=True),
}

EXPECTED = '82eb0d10c57a9ddfabd10aed92d158be726ad57f987d0c35e7ecdd7422993ad5'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--take', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    if sha(a.take) != EXPECTED:
        p.error('Wrong take: SHA256 does not match the restricted approved source')
    a.out.mkdir(parents=True, exist_ok=False)
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(a.take), '-vf', r'select=between(n\,29\,31)',
                    '-fps_mode', 'vfr', '-frames:v', '3', str(a.out/'source_%02d.png')], check=True)
    rod, knuckle = (945., 333.), (933., 340.5)  # exact 1.5x of Gemini 720p edges
    phone_w, phone_h = 390, round(1080 * 390 / 1920)
    sheet = Image.new('RGB', (1920, 3*1120), '#201a16')
    # 160px window at 4x nearest, so a 60px bloom fades inside the frame.
    crop_sheet = Image.new('RGB', (1920, 1340), '#201a16')
    draw = ImageDraw.Draw(crop_sheet)
    draw.text((20, 12), 'J2613 bloom | f029 25% pre-glow, f030 peak, f031 half | 4x nearest, falloff inside the crop', fill='white')
    phones = {}
    source_1080 = None
    for i, frame in enumerate((29, 30, 31)):
        native = Image.open(a.out/f'source_{i+1:02}.png').convert('RGBA')
        if native.size != (1280, 720):
            raise ValueError('Unexpected take dimensions')
        bg = native.resize((1920,1080), Image.Resampling.LANCZOS)
        spec = FLASH[frame]
        overlay = spark(bg.size, rod, knuckle, spec['phase'], frames=2,
                        bloom_scale=spec['bloom_scale'], core=spec['core'])
        composite = Image.alpha_composite(bg, overlay).convert('RGB')
        composite.save(a.out/f'review_f{frame:03}_1080.png')
        phone = composite.resize((phone_w, phone_h), Image.Resampling.LANCZOS)
        phone.save(a.out/f'review_f{frame:03}_phone390.png')
        phones[frame] = phone
        if frame == 29:
            source_1080 = bg.convert('RGB')
            source_1080.save(a.out/'review_f029_source_1080.png')
            source_1080.resize((phone_w, phone_h), Image.Resampling.LANCZOS).save(a.out/'review_f029_source_phone390.png')
        native_overlay = spark(native.size, (630, 222), (622, 227), spec['phase'], frames=2,
                               bloom_scale=spec['bloom_scale'], core=spec['core'])
        Image.alpha_composite(native, native_overlay).convert('RGB').save(a.out/f'review_f{frame:03}_720.png')
        overlay.save(a.out/f'overlay_f{frame:03}.png')
        sheet.paste(composite, (0, i*1120+40))
        ImageDraw.Draw(sheet).text((20, i*1120+12), f'f{frame:03} | {frame/24:.3f}s | 1920x1080 delivery (source 1280x720)', fill='white')
        box = (939-80, 337-80, 939+80, 337+80)
        for j, im in enumerate((bg.convert('RGB'), composite)):
            crop = im.crop(box).resize((640, 640), Image.Resampling.NEAREST)
            crop_sheet.paste(crop, (i*640, 50+j*640))
        label = {29: 'f029 pre-glow 25%', 30: 'f030 peak bloom', 31: 'f031 half bloom'}[frame]
        draw.text((i*640+10, 32), f'{label} | original above / spark below', fill='white')
    sheet.save(a.out/'review_sheet_1080.jpg', quality=97, subsampling=0)
    crop_sheet.save(a.out/'review_crop_4x.png')
    source_phone = Image.open(a.out/'review_f029_source_phone390.png')
    # PASS sheet. Each frame is exactly 390px wide. Nothing here is enlarged.
    pair = Image.new('RGB', (phone_w * 2 + 8, phone_h + 22), '#201a16')
    ImageDraw.Draw(pair).text((8, 4), '1:1 phone 390px, no enlargement | left f029 source | right f030', fill='white')
    pair.paste(source_phone, (0, 22))
    pair.paste(phones[30], (phone_w + 8, 22))
    pair.save(a.out/'review_phone390_pair_1to1.png')
    bare = Image.new('RGB', (phone_w * 2, phone_h))
    bare.paste(source_phone, (0, 0))
    bare.paste(phones[30], (phone_w, 0))
    bare.save(a.out/'review_phone390_pair_bare.png')
    phone_sheet = Image.new('RGB', (phone_w * 4 + 12, phone_h + 22), '#201a16')
    ImageDraw.Draw(phone_sheet).text((8, 4), '1:1 390px | f029 source | f029 pre-glow | f030 peak | f031 half', fill='white')
    for i, im in enumerate((source_phone, phones[29], phones[30], phones[31])):
        phone_sheet.paste(im, (i * (phone_w + 4), 22))
    phone_sheet.save(a.out/'review_phone390_sheet.jpg', quality=95, subsampling=0)
    # Enlarged gap is a pixel proof only. The glance test is the 1:1 pair.
    gap_sheet = Image.new('RGB', (1040, 230), '#201a16')
    ImageDraw.Draw(gap_sheet).text((8, 4), 'phone 390px gap, 7x nearest | source / pre-glow / peak / half (zoom, not the glance test)', fill='white')
    cx, cy = 939.0 * phone_w / 1920, 336.75 * phone_h / 1080
    gbox = (int(cx - 18), int(cy - 14), int(cx + 18), int(cy + 14))
    for i, im in enumerate((source_phone, phones[29], phones[30], phones[31])):
        gap_sheet.paste(im.crop(gbox).resize((252, 196), Image.Resampling.NEAREST), (i * 260, 26))
    gap_sheet.save(a.out/'review_phone390_gap_nearest.png')
    src_a = np.array(source_phone)
    peak_a = np.array(phones[30])
    ix, iy = int(cx), int(cy)
    win = np.abs(peak_a[iy-12:iy+13, ix-12:ix+13].astype(int) - src_a[iy-12:iy+13, ix-12:ix+13].astype(int))
    phone_gap_max_delta = int(win.max())
    phone_gap_mean_delta = round(float(win.mean()), 2)
    # Four-phase generic design proof, separate from the take flash.
    swatch = Image.new('RGB', (1200, 280), '#201a16')
    for phase in range(4):
        overlay = spark((1920, 1080), rod, knuckle, phase, frames=4)
        bg = Image.open(a.out/'source_02.png').convert('RGBA').resize((1920, 1080), Image.Resampling.LANCZOS)
        im = Image.alpha_composite(bg, overlay).crop((869, 267, 1009, 407)).resize((280, 240), Image.Resampling.NEAREST)
        swatch.paste(im, (phase*300, 30))
        ImageDraw.Draw(swatch).text((phase*300+10, 8), f'Design phase +{phase} (not take timing)', fill='white')
    swatch.save(a.out/'design_four_phases_4x.png')
    f029_src = np.array(source_1080)
    f029 = np.array(Image.open(a.out/'review_f029_1080.png'))
    manifest=dict(job='J2613',preview_only=True,source=str(a.take),source_sha256=EXPECTED,
        source_size=[1280,720],delivery_size=[1920,1080],fps=24,
        extracted_frames=[29,30,31],allowed_source_frames_inclusive=[0,60],
        placement_job='J2592',video_take_modified=False,rod_720=[630,222],knuckle_720=[622,227],
        rod_1080=list(rod),knuckle_1080=list(knuckle),proposed_overlay_frames=[29,30,31],
        timing_note='Desk 6797257524: the flash runs f029-f031. f029 is a 25% pre-glow with no streak. f030 is the peak. f031 is the half-strength streak plus half bloom. Nothing past f060.',
        size_revision='Desk 6797257524: core stays about 3.8px FWHM. f030 bloom is warm white, peak alpha 190, radius 60px at 1080, centred on the gap. f031 bloom is half. f029 bloom is 25%, no core. The streak lower end stops at the skin edge (along < 0). Phone PASS is the untouched f029 source beside f030 at 390px, 1:1.',
        bloom=dict(peak_alpha=BLOOM_PEAK, radius_px_at_1080=BLOOM_RADIUS, f029=0.25, f030=1.0, f031=0.5),
        phone_gap_max_delta=phone_gap_max_delta, phone_gap_mean_delta=phone_gap_mean_delta,
        checks={'source_hash_matches':True,'only_frames_29_30_31_extracted':True,
                'f029_source_saved':True,
                'f029_preglow_changes_frame':bool(not np.array_equal(f029, f029_src)),
                'phone_pair_bare_is_390_times_two':list(Image.open(a.out/'review_phone390_pair_bare.png').size)==[phone_w*2, phone_h],
                'phone_gap_max_delta':phone_gap_max_delta},
        files={f.name:sha(f) for f in sorted(a.out.iterdir()) if f.is_file()})
    (a.out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest['checks']))

if __name__=='__main__':
    main()
