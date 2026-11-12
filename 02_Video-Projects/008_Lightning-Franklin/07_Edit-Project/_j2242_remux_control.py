"""Diagnostic identity remux only: no edited pixels, approval or master."""
import argparse
import json
from pathlib import Path
import _build_rough_v13_recipe as recipe


def main():
    import av
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out-dir', type=Path, required=True)
    a = ap.parse_args()
    recipe.require_hash(recipe.DEFAULT_MASTER, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    a.out_dir.mkdir(parents=True, exist_ok=False)
    with av.open(str(recipe.DEFAULT_MASTER)) as source:
        with av.open(str(a.out_dir / 'identity_remux.mp4'), 'w', options={
                'avoid_negative_ts': 'disabled', 'video_track_timescale': '12288'}) as out:
            mapping = {s.index: out.add_stream_from_template(s) for s in source.streams
                       if s.type in ('video', 'audio')}
            for p in source.demux():
                if p.size and p.stream.index in mapping:
                    p.stream = mapping[p.stream.index]
                    out.mux(p)
    recipe.require_hash(recipe.DEFAULT_MASTER, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    (a.out_dir / 'contract.json').write_text(json.dumps({
        'modified_frames': [], 'encoded_envelopes': []}) + '\n')


if __name__ == '__main__':
    main()
