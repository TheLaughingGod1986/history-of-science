"""Reconstruct the opening caption over its clean KEEP plate, including clear tail.

Bounded to f0..141: no master mux, audio, other rows, or final-film approval.
"""
import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path
import _build_rough_v13_recipe as recipe
from _j2242_salon_patch import pixel_hashes

SOURCE_SHA = '0c07f6cfcf75985f3d6f9824666387ecf6a70000f553485f1ede4ef371c5d839'

def validate_clock(timeline, layer):
    frames = timeline['frames'][:142]
    if timeline['time_base'] != '1/12288' or len(frames) != 142:
        raise ValueError('Opening requires complete original clock')
    if any(f['index'] != i or f['pts'] != 1536+i*512 or f['duration'] != 512
           for i, f in enumerate(frames)):
        raise ValueError('Original opening clock changed')
    expected = dict(row='01_kite_open', frame_in=0, frame_last=95,
                    frame_count=96, pts_in=1536, pts_end=50688,
                    label='PHILADELPHIA 1752', overlay_position=[0,720])
    if any(layer.get(k) != v for k,v in expected.items()):
        raise ValueError('Unexpected opening caption layer scope')
    return frames

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--timeline',type=Path,required=True)
    ap.add_argument('--layer-record',type=Path,required=True)
    ap.add_argument('--out-dir',type=Path,required=True)
    a=ap.parse_args()
    evidence=json.loads((recipe.EDIT_DIR.parents[2]/'jobs/reviews/J2242/SOURCE_PREFLIGHT.json').read_text())
    clock_sha=evidence['evidence_files']['source_timeline.json']['sha256']
    layers=json.loads((recipe.EDIT_DIR.parents[2]/'jobs/reviews/J2242/CAPTION_LAYERS.json').read_text())
    # The individual record must agree with the already reviewed batch inventory.
    layer=json.loads(a.layer_record.read_text())
    if layer not in layers['cards']:
        raise ValueError('Layer record absent from pinned batch inventory')
    frames=validate_clock(json.loads(a.timeline.read_text()),layer)
    inputs={a.source:SOURCE_SHA,a.timeline:clock_sha,
            Path(layer['layer_path']):layer['layer_sha256'],
            Path(layer['original_clock_path']):layer['original_clock_sha256']}
    for path,sha in inputs.items(): recipe.require_hash(path,sha)
    native=recipe.probe_video(a.source)['frames'][:142]
    tb=Fraction(recipe.probe_video(a.source)['time_base'])
    if len(native)!=142 or any(f['pts']*tb!=Fraction(i,24) or f['duration']*tb!=Fraction(1,24)
                               for i,f in enumerate(native)):
        raise ValueError('Clean source lacks native opening frame schedule')
    a.out_dir.mkdir(parents=True,exist_ok=False)
    output=a.out_dir/'opening_caption.nut'
    base='trim=end_frame=142,scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p'
    graph=(f'[0:v]{base},settb=1/12288,setpts=PTS+1536[b];'
           '[b][1:v]overlay=x=0:y=720:eof_action=pass:repeatlast=0:format=yuv420[v]')
    subprocess.run(['ffmpeg','-nostdin','-v','error','-xerror','-copyts','-i',str(a.source),
                    '-i',layer['layer_path'],'-filter_complex',graph,'-map','[v]',
                    '-an','-c:v','ffv1','-level','3','-threads','4',
                    '-fps_mode','passthrough','-enc_time_base','1/12288',
                    '-avoid_negative_ts','disabled','-n',str(output)],check=True)
    actual=recipe.probe_video(output,142)
    ratio=Fraction(actual['time_base'])/Fraction('1/12288')
    if [(f['pts']*ratio,f['duration']*ratio) for f in actual['frames']] != [(f['pts'],f['duration']) for f in frames]:
        raise ValueError('Composite changed original opening clock')
    expected=pixel_hashes(a.source,base)
    measured=pixel_hashes(output)
    if len(expected)!=142 or measured[96:]!=expected[96:] or measured[0]!=expected[0]:
        raise ValueError('Caption leaked into clear remainder or zero-alpha frame')
    if measured[48]==expected[48]: raise ValueError('Caption missing at full opacity')
    if pixel_hashes(output,'crop=1920:720:0:0') != pixel_hashes(a.source,base+',crop=1920:720:0:0'):
        raise ValueError('Composite changed picture above caption band')
    for path,sha in inputs.items(): recipe.require_hash(path,sha)
    clock=a.out_dir/'original_clock.json'
    recipe.write_new(clock,dict(time_base='1/12288',frames=frames))
    result=dict(job='J2242',status='OPENING_COMPOSITE_INTERMEDIATE_ONLY',path=str(output),
                sha256=recipe.sha256_file(output),source_sha256=SOURCE_SHA,
                layer_sha256=layer['layer_sha256'],timeline_frames=[0,141],
                source_frames=[0,141],frame_count=142,original_pts_and_duration_match=True,
                clear_tail_frames=[96,141],clear_tail_pixel_hashes_match=True,
                picture_above_caption_band_hashes_match=True,caption_peak_present=True,
                original_clock_path=str(clock),original_clock_sha256=recipe.sha256_file(clock),
                master_created=False,final_film_approval=False,visual_review='OUTSTANDING')
    recipe.write_new(a.out_dir/'RESULT.json',result)
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
