import json,pathlib,subprocess,concurrent.futures
P=pathlib.Path(__file__).parent
vs=[v for v in json.load(open(P/'inventory_api.json'))['videos'] if 'M' in v['contentDetails']['duration'] and (v['status']['privacyStatus']=='public' or v['status'].get('publishAt'))]
def search(v):
 r=subprocess.run(['yt-dlp','--flat-playlist','--dump-json','--skip-download','--no-warnings','ytsearch5:'+v['snippet']['title']],capture_output=True,text=True,timeout=60)
 return {'hosVideo':v['id'],'query':v['snippet']['title'],'results':[json.loads(l) for l in r.stdout.splitlines() if l.startswith('{')],'exit':r.returncode}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(search,vs))
(P/'search_neighbours.json').write_text(json.dumps(rows,indent=2));print('Searches',len(rows))
