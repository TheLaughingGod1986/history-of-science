#!/usr/bin/env python3
"""J0716: re-letter existing HOS key art; no generation or Studio writes."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('house', HERE / '_compose_hos_001_thumb_B_unseen_pond_microbes_v07.py')
house = importlib.util.module_from_spec(spec)
spec.loader.exec_module(house)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--out-dir', type=Path, required=True)
    args = p.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    source = Image.open(args.source).convert('RGB')
    if source.size != (1280, 720):
        raise SystemExit('Expected the existing 1280x720 flask key art')
    # Existing compositor restores the bookcase behind its lettering band.
    base = house.wipe_old_lettering(source).convert('RGBA')
    boxes = []
    for word, y, fill, highlight in [('DUST', 65, house.CREAM, house.CREAM_HI),
                                     ('TRAP', 187, house.GOLD, house.GOLD_HI)]:
        layer = house.render_word(word, 122, fill, highlight)
        x = round(285 - layer.width / 2)
        base.alpha_composite(layer, (x, y))
        boxes.append([x, y, x + layer.width, y + layer.height])
    assert all(b[0] >= 50 and b[2] <= 522 and b[3] <= 318 for b in boxes), boxes
    out = args.out_dir / 'hos_001_thumb_B_dust_trap_v08.jpg'
    base.convert('RGB').save(out, quality=94, subsampling=0)
    info = {'job':'J0716','film':'HOS:001','video':'_C92tIJCk8A',
            'maker':'codex','hook':'DUST TRAP','status':'candidate; parked for Chief review',
            'source':str(args.source),'source_sha256':hashlib.sha256(args.source.read_bytes()).hexdigest(),
            'file':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
            'bytes':out.stat().st_size,'size':[1280,720],'lettering_boxes':boxes,
            'spend':0,'studio_changed':False,
            'method':'Existing v06 painted flask art, same house compositor and serif lettering; no hero changes',
            'claim_basis':'01_Script/part04_proof_in_a_flask_v01.md: dust and microbes settle in the curve',
            'test_eligibility':'No 001 test in shared ledger at 2026-10-20; live Studio must be rechecked before arming'}
    (args.out_dir / 'manifest.json').write_text(json.dumps(info, indent=2)+'\n')
    print(json.dumps(info,indent=2))

if __name__ == '__main__':
    main()
