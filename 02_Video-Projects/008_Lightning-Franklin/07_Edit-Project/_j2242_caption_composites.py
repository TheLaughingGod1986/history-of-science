"""Render caption-row intermediates from unambiguous monotonic clean-source maps.

Skipped rows stay outstanding. No master assembly, audio or film approval.
"""
import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path
import _build_rough_v13_recipe as recipe
from _j2242_caption_layers import clock_expression
from _j2242_salon_patch import pixel_hashes


def eligible(row):
    indices=row['source_frame_indices']
    return bool(indices) and not any(row[k] for k in ('poor_match_local_frames','ambiguous_local_frames','nonmonotonic_steps')) and all(isinstance(i,int) and not isinstance(i,bool) and i>=0 for i in indices) and all(b>=a for a,b in zip(indices,indices[1:]))


def source_runs(indices):
    """Partition the measured schedule without guessing over repeats or jumps."""
    if not indices or any(type(i) is not int or i<0 for i in indices):
        raise ValueError('Invalid source schedule')
    if any(b<a for a,b in zip(indices,indices[1:])):
        raise ValueError('Backward source schedule')
    runs=[]; first=previous=indices[0]
    for index in indices[1:]:
        if index!=previous+1:
            runs.append((first,previous+1));first=index
        previous=index
    runs.append((first,previous+1))
    return runs


def source_graph(indices):
    runs=source_runs(indices)
    if len(runs)==1:
        first,end=runs[0]
        return f'[0:v]trim=start_frame={first}:end_frame={end},setpts=PTS-STARTPTS[ordered]'
    graph=['[0:v]split='+str(len(runs))+''.join(f'[s{i}]' for i in range(len(runs)))]
    for i,(first,end) in enumerate(runs):
        graph.append(f'[s{i}]trim=start_frame={first}:end_frame={end},setpts=PTS-STARTPTS[r{i}]')
    graph.append(''.join(f'[r{i}]' for i in range(len(runs)))+f'concat=n={len(runs)}:v=1:a=0[ordered]')
    return ';'.join(graph)


def row_clock(timeline,row):
    lo,hi=row['timeline_frames'];frames=timeline['frames'][lo:hi+1]
    if timeline['time_base']!='1/12288' or len(frames)!=hi-lo+1:
        raise ValueError('Missing original row clock')
    if any(f['index']!=lo+i for i,f in enumerate(frames)):
        raise ValueError('Original frame indices changed')
    if len(frames)!=len(row['source_frame_indices']):raise ValueError('Map/clock count differs')
    return frames


def render(row,timeline,cards,out):
    frames=row_clock(timeline,row);count=len(frames)
    source=Path(row['source_path']);recipe.require_hash(source,row['source_sha256'])
    selected=[c for c in cards if c['row']==row['row']]
    if not selected:raise ValueError('Missing row caption layers')
    indices=row['source_frame_indices'];first=indices[0]
    # Independent native source timing validation before using candidate mapping.
    native=recipe.probe_video(source);tb=Fraction(native['time_base'])
    source_runs(indices)
    if max(indices)>=len(native['frames']):raise ValueError('Source map exceeds decoded source')
    fs=[native['frames'][i] for i in indices]
    if any(f['pts']*tb!=Fraction(i,24) or f['duration']*tb!=Fraction(1,24) for i,f in zip(indices,fs)):
        raise ValueError('Selected source is not native 24fps')
    out.mkdir(exist_ok=False)
    inputs=['-i',str(source)]
    base='scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p'
    graph=[source_graph(indices),f"[ordered]{base},settb=1/12288,setpts='{clock_expression(frames)}'[base]"]
    previous='base'
    for i,c in enumerate(selected,1):
        if c['frame_in']<frames[0]['index'] or c['frame_last']>frames[-1]['index']:
            raise ValueError('Layer outside reconstruction window')
        recipe.require_hash(c['layer_path'],c['layer_sha256'])
        recipe.require_hash(c['original_clock_path'],c['original_clock_sha256'])
        inputs+=['-i',c['layer_path']]
        current=f'c{i}'
        graph.append(f'[{previous}][{i}:v]overlay=x=0:y=720:eof_action=pass:repeatlast=0:format=yuv420[{current}]')
        previous=current
    video=out/'caption_composite.nut'
    subprocess.run(['ffmpeg','-nostdin','-v','error','-xerror','-copyts',*inputs,
                    '-filter_complex',';'.join(graph),'-map',f'[{previous}]','-an',
                    '-c:v','ffv1','-level','3','-threads','4','-fps_mode','passthrough',
                    '-enc_time_base','1/12288','-avoid_negative_ts','disabled','-n',str(video)],check=True)
    actual=recipe.probe_video(video,count);ratio=Fraction(actual['time_base'])/Fraction('1/12288')
    if [f['pts']*ratio for f in actual['frames']]!=[f['pts'] for f in frames]:
        raise ValueError('Composite changed original PTS')
    duration_match=[f['duration']*ratio for f in actual['frames']]==[f['duration'] for f in frames]
    all_source=pixel_hashes(source,base)
    expected=[all_source[i] for i in indices];measured=pixel_hashes(video)
    if len(expected)!=count:raise ValueError('Source pixel count differs')
    last_caption=max(c['frame_last'] for c in selected)-frames[0]['index']
    if measured[last_caption+1:]!=expected[last_caption+1:]:
        raise ValueError('Caption leaks into clear remainder')
    upper_source=pixel_hashes(source,base+',crop=1920:720:0:0')
    if pixel_hashes(video,'crop=1920:720:0:0')!=[upper_source[i] for i in indices]:
        raise ValueError('Picture above caption band differs')
    for c in selected:
        peak=(c['frame_in']+c['frame_last'])//2-frames[0]['index']
        if measured[peak]==expected[peak]:raise ValueError('Caption absent at midpoint')
        recipe.require_hash(c['layer_path'],c['layer_sha256'])
    recipe.require_hash(source,row['source_sha256'])
    clock=out/'original_clock.json';recipe.write_new(clock,dict(time_base='1/12288',frames=frames))
    result=dict(row=row['row'],path=str(video),sha256=recipe.sha256_file(video),
                timeline_frames=row['timeline_frames'],source_frame_indices=indices,source_runs=source_runs(indices),
                source_sha256=row['source_sha256'],frame_count=count,caption_count=len(selected),
                original_pts_match=True,original_durations_preserved_in_intermediate=duration_match,
                original_clock_path=str(clock),original_clock_sha256=recipe.sha256_file(clock),
                clear_tail_frames=count-last_caption-1,clear_tail_pixel_hashes_match=True,
                above_caption_band_pixel_hashes_match=True,caption_midpoints_present=True,
                source_mapping_evidence='Low-resolution candidate matching; final in-context review outstanding',
                final_mux_duration_verification='OUTSTANDING',final_film_approval=False)
    recipe.write_new(out/'RESULT.json',result)
    print(row['row'],count,'frames verified',flush=True)
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rows',nargs='+',help='Render only these named rows; rejects missing or ineligible names')
    ap.add_argument('--mapping',type=Path,required=True)
    ap.add_argument('--timeline',type=Path,required=True)
    ap.add_argument('--out-dir',type=Path,required=True)
    a=ap.parse_args()
    root=recipe.EDIT_DIR.parents[2]/'jobs/reviews/J2242'
    evidence=json.loads((root/'SOURCE_PREFLIGHT.json').read_text())
    clock_sha=evidence['evidence_files']['source_timeline.json']['sha256']
    recipe.require_hash(a.timeline,clock_sha)
    timeline=json.loads(a.timeline.read_text());mapping=json.loads(a.mapping.read_text())
    mapping_sha=recipe.sha256_file(a.mapping)
    batch=json.loads((root/'CAPTION_LAYERS.json').read_text())
    if mapping['master_sha256']!=recipe.MASTER_SHA:raise ValueError('Wrong mapped master')
    # Pin source rows and hashes to the historical cut inventory, not supplied map values.
    cuts_path=recipe.EDIT_DIR/'_desk/008/rough_v12/cuts_rough_v12.json'
    recipe.require_hash(cuts_path,mapping['cuts_sha256'])
    cuts=json.loads(cuts_path.read_text())
    labels=recipe.load_manifest()['caption_treatment']['labels']
    if len(mapping['rows']) != 27 or len({r['row'] for r in mapping['rows']}) != 27:
        raise ValueError('Incomplete or duplicated source mapping inventory')
    for row in mapping['rows']:
        if not any(lab['row']==row['row'] and lab['master_frames']==row['timeline_frames'] for lab in labels):
            raise ValueError('Mapped window differs from approved caption inventory')
        if not any(c['row']==row['row'] and c['source_path']==row['source_path'] and c['source_sha256']==row['source_sha256'] for c in cuts):
            raise ValueError('Mapping source is absent from historical inventory')
    chosen=[r for r in mapping['rows'] if eligible(r) and (not a.rows or r['row'] in a.rows)]
    if a.rows and (len(set(a.rows))!=len(a.rows) or {r['row'] for r in chosen}!=set(a.rows)):
        raise ValueError('Requested rows absent or unsafe')
    a.out_dir.mkdir(exist_ok=False)
    results=[render(r,timeline,batch['cards'],a.out_dir/r['row']) for r in chosen]
    recipe.require_hash(a.mapping,mapping_sha);recipe.require_hash(a.timeline,clock_sha)
    recipe.write_new(a.out_dir/'RESULT.json',dict(job='J2242',status='CAPTION_COMPOSITE_INTERMEDIATES_ONLY',
        mapping_sha256=mapping_sha,rows=results,
        skipped_rows=[r['row'] for r in mapping['rows'] if not eligible(r)],
        master_created=False,final_film_approval=False))

if __name__=='__main__':main()
