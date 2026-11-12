"""J2563 source-precedence checkpoint. No generation, render or narration changes.

Run with --out outside git. Metadata/download mode is opt-in and resumable.
"""
import argparse, copy, hashlib, json, pathlib, re, subprocess, urllib.error, urllib.parse, urllib.request
HERE = pathlib.Path(__file__).resolve().parent
RULING = 'https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6810336587'

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

def save(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')

def manifest():
    plan=json.loads((HERE/'PICTURE_PLAN_v03.json').read_text())
    brief=json.loads((HERE/'ARCHIVE_SOURCES_BRIEF_v01.json').read_text())
    records=[]
    for kind,key,urlkey in [('archive','archive_rows','archive_url'),('portrait','who_portraits','commons_url')]:
        for source in brief[key]:
            records.append({'asset_id':kind+'_'+source['row_id'].replace(':','_'),'row_id':source['row_id'],'role':kind,'page_url':source[urlkey], 'licence_from_brief':source['page_stated_licence'],'credit':source.get('archive_credit'),'status':'not_fetched','source_brief_record':copy.deepcopy(source)})
    overrides={
        'archive_P1_09b':('Hand_coloured_illustration_of_surgical_instruments_Wellcome_L0041135.jpg','Paré instruments, Wellcome / CC BY 4.0'),
        'portrait_P2_02a':('Sir_Humphry_Davy._Stipple_engraving_by_W._Walker,_1830,_afte_Wellcome_V0006497.jpg','H. Davy, engr. W. Walker (1830), Wellcome / CC BY 4.0'),
        'portrait_P2_07a':('Portrait_of_Crawford_Williamson_Long._Wellcome_M0003193.jpg','C. W. Long, Wellcome / CC BY 4.0'),
        'archive_P3_05b':("Anaesthetics;_Morton%27s_Ether_Inhaler_Wellcome_L0018234.jpg",'Morton inhaler replica, Wellcome / CC BY 4.0'),
        'archive_P3_09a_arch_ether_dome_1847':('Southworth_%26_Hawes_(American,_active_1844_-_1862)_-_Use_of_Ether_for_Anesthesia_-_Google_Art_Project.jpg','Southworth & Hawes (1847), Getty / Commons')}
    for r in records:
        if r['asset_id'] in overrides:
            name,r['credit']=overrides[r['asset_id']]
            r['page_url']='https://commons.wikimedia.org/wiki/File:'+name
            r['override_ref']=RULING
            r['licence_from_brief']='Public domain' if 'Google_Art' in name else 'CC BY 4.0'
        if r['asset_id']=='portrait_P1_03a':r['credit']='Portrait: C. Turner (1840), Wellcome / CC BY 4.0'
        if r['asset_id']=='archive_P3_05b':r['depicts']='Morton ether inhaler replica, circa 1945; own-drawn airflow required'
        if r['asset_id']=='archive_P5_03a_arch_squire_inhaler_1846':r['depicts']='Photograph of a Squire-type copy; not an 1846 engraving'
        if r['asset_id']=='archive_P2_05a_arch_laughing_gas_broadside':r['own_drawn_component']='1844 Hartford broadside; preserve distinction from Gillray 1802 source'
        if r['asset_id']=='archive_P5_07a_arch_snow_chloroform_1858':r['alternate_url']=r['source_brief_record']['alternate_url'];r['alternate_precedence']='JSON alternate; do not substitute Markdown alternate'
        if r['credit'] is None:r['credit_status']='Needs exact credit derived from actual metadata before use'
    rows=[{'row_id':r['row_id'],'in_s':r['in_s'],'out_s':r['out_s'],'duration_s':r['duration_s'],'build_type':('dependency_slate' if r['source_kind'].startswith('mint_') or r['source_kind']=='existing_plate_reuse' else r['source_kind'])} for r in plan['rows']]
    return {'job':'J2563','status':'source_precedence_checkpoint_not_render_authority','generation_authorized':False,'spend_gbp':0,'credits_used':0,'precedence':[RULING,'ARCHIVE_SOURCES_BRIEF_v01.json','PICTURE_PLAN_v03.json timing only'],'input_hashes':{n:sha(HERE/n) for n in ['PICTURE_PLAN_v02.json','PICTURE_PLAN_v03.json','ARCHIVE_SOURCES_BRIEF_v01.json']},'stt_sha256':sha(HERE.parent/plan['vo_lock']['stt_raw']),'vo_lock':plan['vo_lock'],'assets':records,'rows':rows,'reuse':{'row_id':'P5:16b','status':'dependency_slate','source_row':'P1:07b','source_available':False,'required_first_use_s':6.61,'required_callback_s':4.52,'minimum_disjoint_source_s':11.13,'hypothetical_8s_overlap_s':3.13,'actual_source_duration_s':None,'actual_in_out':None,'note':'No actual generated file exists/was examined; overlap is arithmetic only. Chief finding required before replacement.'}}

def fetch(m,out):
    assets=out/'archive_sources_v01';assets.mkdir(exist_ok=True)
    for r in m['assets']:
        print(r['asset_id'],flush=True)
        evidence=assets/(r['asset_id']+'_metadata.json')
        try:
            if evidence.exists(): data=json.loads(evidence.read_text())
            else:
                title=urllib.parse.unquote(r['page_url'].split('/wiki/')[1])
                url='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'action':'query','format':'json','titles':title,'prop':'imageinfo','iiprop':'url|size|extmetadata','redirects':1})
                req=urllib.request.Request(url,headers={'User-Agent':'OrbitStudio/1.0 (J2563 source verification)'})
                with urllib.request.urlopen(req,timeout=40) as response:data=json.load(response)
                save(evidence,data)
            pages=data['query']['pages'];page=next(iter(pages.values()));info=page['imageinfo'][0]
            r['metadata_file']=str(evidence);r['metadata_sha256']=sha(evidence)
            r['live_metadata']={k:info.get(k) for k in ['url','width','height','size','extmetadata']}
            ext=info.get('extmetadata',{});r['observed_licence']={k:ext.get(k,{}).get('value') for k in ['LicenseShortName','LicenseUrl','UsageTerms','AttributionRequired','Copyrighted','Credit','Artist','ImageDescription']}
            r['status']='metadata_fetched_requires_visual_and_licence_review'
            if urllib.parse.urlparse(info['url']).path.lower().endswith('.pdf'):
                r['download_note']='Full book deliberately not downloaded; locate approved printed page and verify page identity before rendering.'
            else:
                suffix=pathlib.Path(urllib.parse.urlparse(info['url']).path).suffix
                target=assets/(r['asset_id']+suffix)
                if not target.exists():
                    if info.get('size',0)>60*1024*1024:raise ValueError('Source exceeds bounded 60 MiB download')
                    req=urllib.request.Request(info['url'],headers={'User-Agent':'OrbitStudio/1.0 (J2563 source verification)'})
                    with urllib.request.urlopen(req,timeout=60) as response, target.with_suffix(suffix+'.partial').open('wb') as f:
                        total=0
                        while True:
                            chunk=response.read(1024*1024)
                            if not chunk:break
                            total+=len(chunk)
                            if total>60*1024*1024:raise ValueError('Download exceeds 60 MiB cap')
                            f.write(chunk)
                    target.with_suffix(suffix+'.partial').rename(target)
                if info.get('size') and target.stat().st_size!=info['size']:raise ValueError('Source byte-size mismatch')
                probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(target)]))
                stream=probe['streams'][0]
                if (stream['width'],stream['height'])!=(info['width'],info['height']):raise ValueError('Decoded image dimensions differ from metadata')
                r['decoded_dimensions']=[stream['width'],stream['height']]
                r['local_file']=str(target);r['file_sha256']=sha(target);r['file_bytes']=target.stat().st_size
        except urllib.error.HTTPError as e:
            r['status']='fetch_failed';r['error']='HTTP '+str(e.code)
            if e.code==429:
                m['network_hold']='Wikimedia HTTP 429; no further requests in this run. Respect Retry-After or wait before a separately bounded retry.'
                save(out/'ASSEMBLY_SOURCES_v01.json',m)
                break
        except Exception as e:r['status']='fetch_failed';r['error']=re.sub(r'[\w.+-]+@[\w.-]+', '[redacted contact]', str(e))
        save(out/'ASSEMBLY_SOURCES_v01.json',m)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=pathlib.Path,required=True);ap.add_argument('--fetch',action='store_true');args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    dest=args.out/'ASSEMBLY_SOURCES_v01.json'
    m=json.loads(dest.read_text()) if dest.exists() else manifest()
    save(dest,m)  # corrected source authority is written before any request/download
    if args.fetch:
        if m.get('network_hold'):raise SystemExit('Network hold recorded; inspect it before scheduling a later retry.')
        fetch(m,args.out)
    print('Source manifest saved; no row rendering, stage approval or media QA performed.')
if __name__=='__main__':main()
