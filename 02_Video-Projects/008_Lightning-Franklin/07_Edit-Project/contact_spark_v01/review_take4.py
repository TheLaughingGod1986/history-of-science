"""Reproducible J2613 still review; never writes a take or final film."""
import argparse
import json
from pathlib import Path
import subprocess
import numpy as np
from PIL import Image, ImageDraw
from render import spark, sha

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
    sheet = Image.new('RGB', (1920, 3*1120), '#201a16')
    crop_sheet = Image.new('RGB', (1200, 770), '#201a16')
    draw = ImageDraw.Draw(crop_sheet)
    draw.text((20, 12), 'J2613 | take 4 | f029 unchanged, f030 bright streak, f031 half strength | 4x DELIVERY crop', fill='white')
    for i, frame in enumerate((29, 30, 31)):
        native = Image.open(a.out/f'source_{i+1:02}.png').convert('RGBA')
        if native.size != (1280, 720):
            raise ValueError('Unexpected take dimensions')
        bg = native.resize((1920,1080), Image.Resampling.LANCZOS)
        overlay = spark(bg.size, rod, knuckle, frame-30, frames=2)
        composite = Image.alpha_composite(bg, overlay).convert('RGB')
        composite.save(a.out/f'review_f{frame:03}_1080.png')
        # Native-size source evidence beside delivery rendering, no artificial detail.
        native_overlay = spark(native.size, (630,222), (622,227), frame-30, frames=2)
        Image.alpha_composite(native,native_overlay).convert('RGB').save(a.out/f'review_f{frame:03}_720.png')
        overlay.save(a.out/f'overlay_f{frame:03}.png')
        sheet.paste(composite,(0,i*1120+40))
        ImageDraw.Draw(sheet).text((20,i*1120+12),f'f{frame:03} | {frame/24:.3f}s | 1920x1080 delivery (source 1280x720)',fill='white')
        box=(885,285,985,375)
        for j,im in enumerate((bg.convert('RGB'),composite)):
            crop=im.crop(box).resize((400,360),Image.Resampling.NEAREST)
            crop_sheet.paste(crop,(i*400,50+j*360))
        draw.text((i*400+10,33),f'f{frame:03} | original above / spark below',fill='white')
    sheet.save(a.out/'review_sheet_1080.jpg',quality=97,subsampling=0)
    crop_sheet.save(a.out/'review_crop_4x.png')
    # Four-phase generic design proof, separate from the 2-frame take placement proposal.
    swatch = Image.new('RGB',(1200,250),'#201a16')
    for phase in range(4):
        overlay=spark((1920,1080),rod,knuckle,phase,frames=4)
        bg=Image.open(a.out/'source_02.png').convert('RGBA').resize((1920,1080),Image.Resampling.LANCZOS)
        im=Image.alpha_composite(bg,overlay).crop((910,315,970,365)).resize((240,200),Image.Resampling.NEAREST)
        swatch.paste(im,(phase*300,40))
        ImageDraw.Draw(swatch).text((phase*300+10,10),f'Design phase +{phase} (not take timing)',fill='white')
    swatch.save(a.out/'design_four_phases_4x.png')
    manifest=dict(job='J2613',preview_only=True,source=str(a.take),source_sha256=EXPECTED,
        source_size=[1280,720],delivery_size=[1920,1080],fps=24,
        extracted_frames=[29,30,31],allowed_source_frames_inclusive=[0,60],
        placement_job='J2592',video_take_modified=False,rod_720=[630,222],knuckle_720=[622,227],
        rod_1080=rod,knuckle_1080=knuckle,proposed_overlay_frames=[30,31],
        timing_note='Later placement ruling limits take flick to 2–3 frames around f030; use 2 frames, peak f030 and half-strength f031. Generic optional +2/+3 tails shown separately, not placed on take.',
        checks={'source_hash_matches':True,'only_frames_29_30_31_extracted':True,
                'review_f029_unchanged':bool(np.array_equal(np.array(Image.open(a.out/'review_f029_1080.png')),np.array(Image.open(a.out/'source_01.png').convert('RGB').resize((1920,1080),Image.Resampling.LANCZOS)) ))},
        files={f.name:sha(f) for f in sorted(a.out.iterdir()) if f.is_file()})
    (a.out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest['checks']))

if __name__=='__main__':
    main()
