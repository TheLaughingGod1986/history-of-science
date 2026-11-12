"""Measure candidate clean-source frame mappings, never approve or render a master.

Compare a text-free upper picture band. Mapping confidence is evidence only:
ambiguous frames require review before reconstruction, never a silent CFR guess.
"""
import argparse
import json
import subprocess
from pathlib import Path
import numpy as np
import _build_rough_v13_recipe as recipe

W,H=192,72
FILTER='scale=1920:1080:flags=lanczos,crop=1920:720:0:0,scale=192:72:flags=area,format=gray'

def thumbnails(path, selection=None):
    filters=(selection+',' if selection else '')+FILTER
    raw=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-xerror',
                                 '-i',str(path),'-an','-vf',filters,
                                 '-fps_mode','passthrough','-pix_fmt','gray','-f','rawvideo','-'])
    if len(raw)%(W*H): raise ValueError('Truncated thumbnail decode')
    return np.frombuffer(raw,dtype=np.uint8).reshape(-1,H*W)

def measure(master, source):
    if not len(master) or not len(source):raise ValueError('Missing decoded comparison frames')
    mapped=[]; errors=[]; margins=[]
    source=source.astype(np.float32)
    for image in master:
        mse=np.mean((source-image.astype(np.float32))**2,axis=1)
        order=np.argsort(mse,kind='stable')
        best=int(order[0]); mapped.append(best);errors.append(float(mse[best]))
        margins.append(float(mse[order[1]]-mse[best]) if len(order)>1 else 0.)
    return dict(source_frame_indices=mapped,maximum_mse=max(errors),
                minimum_runner_up_mse_margin=min(margins),per_frame_mse=errors,
                per_frame_runner_up_margin=margins,
                nonmonotonic_steps=[i for i in range(1,len(mapped)) if mapped[i]<mapped[i-1]],
                ambiguous_local_frames=[i for i,m in enumerate(margins) if m<0.1],
                poor_match_local_frames=[i for i,e in enumerate(errors) if e>9.0])

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--master',type=Path,default=recipe.DEFAULT_MASTER)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args()
    recipe.require_hash(a.master,recipe.MASTER_SHA,recipe.MASTER_BYTES)
    manifest=recipe.load_manifest()
    cuts_path=recipe.EDIT_DIR/'_desk/008/rough_v12/cuts_rough_v12.json'
    cuts=json.loads(cuts_path.read_text())
    labels=manifest['caption_treatment']['labels']
    if len(labels)!=27:raise ValueError('Expected complete 27-row caption inventory')
    selected=[]
    for lab in labels:
        lo,hi=lab['master_frames']; selected.append(f'between(n,{lo},{hi})')
    master=thumbnails(a.master,"select='"+'+'.join(selected)+"'")
    expected=sum(b-a+1 for a,b in (lab['master_frames'] for lab in labels))
    if len(master)!=expected:raise ValueError('Master selection count differs')
    offset=0;results=[]
    for lab in labels:
        rows=[c for c in cuts if c['row']==lab['row'] and c.get('side_label')==lab['label']]
        if len(rows)!=1:raise ValueError('Ambiguous source inventory row')
        row=rows[0];path=Path(row['source_path']);sha=row['source_sha256']
        if row['framing']!={'offset':0.0}:raise ValueError('Reframe requires explicit matching transform')
        recipe.require_hash(path,sha)
        source=thumbnails(path)
        lo,hi=lab['master_frames'];count=hi-lo+1
        measured=measure(master[offset:offset+count],source);offset+=count
        recipe.require_hash(path,sha)
        results.append(dict(row=lab['row'],timeline_frames=[lo,hi],source_path=str(path),
                            source_sha256=sha,decoded_source_frames=len(source),**measured))
        print(lab['row'], 'max MSE',round(measured['maximum_mse'],3),
              'ambiguous',len(measured['ambiguous_local_frames']),flush=True)
    recipe.require_hash(a.master,recipe.MASTER_SHA,recipe.MASTER_BYTES)
    recipe.write_new(a.out,dict(job='J2242',status='CANDIDATE_SOURCE_MAPPING_ONLY',
                              master_sha256=recipe.MASTER_SHA,
                              cuts_sha256=recipe.sha256_file(cuts_path),
                              comparison_filter=FILTER,frames_measured=expected,rows=results,
                              confidence_thresholds=dict(max_mse=9.0,min_runner_up_margin=0.1),
                              limitations='Low-resolution upper-band matching. Not full-frame identity, source reconstruction, motion perception, approval or final-film gate.',
                              master_created=False,final_film_approval=False))

if __name__=='__main__':main()
