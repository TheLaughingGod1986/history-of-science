"""Public metadata sample; only API GETs and public yt-dlp listings, no video downloads."""
import importlib.util,json,pathlib,subprocess,concurrent.futures,datetime
P=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('collect',P/'collect.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
channels=['veritasium','SciShow','bigthink','RealEngineering','KingsandGenerals']
def listing(pair):
 ch,fmt=pair
 r=subprocess.run(['yt-dlp','--flat-playlist','--playlist-end','200','--dump-json','--skip-download','--no-warnings',f'https://www.youtube.com/@{ch}/{fmt}'],capture_output=True,text=True,timeout=120)
 return ch,fmt,[json.loads(l) for l in r.stdout.splitlines() if l.startswith('{')],r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:lists=list(ex.map(listing,[(ch,fmt) for ch in channels for fmt in ['videos','shorts']]))
ids=list({v['id'] for _,_,vs,_ in lists for v in vs});meta={}
for i in range(0,len(ids),50):
 r=c.get(c.api+'videos',{'part':'snippet,statistics,contentDetails','id':','.join(ids[i:i+50])})
 meta.update({v['id']:v for v in r.get('items',[])})
(P/'competitor_metadata.json').write_text(json.dumps(meta,indent=2))
now=datetime.datetime.now(datetime.timezone.utc);cut=now-datetime.timedelta(days=90);out=[]
for ch,fmt,vs,code in lists:
 eligible=[]
 for v in vs:
  m=meta.get(v['id'])
  if not m or 'viewCount' not in m.get('statistics',{}):continue
  dt=datetime.datetime.fromisoformat(m['snippet']['publishedAt'].replace('Z','+00:00'))
  if dt<cut:continue
  age=max((now-dt).total_seconds()/86400,1);views=int(m['statistics'].get('viewCount',0))
  eligible.append({'id':v['id'],'title':m['snippet']['title'],'publishedAt':m['snippet']['publishedAt'],'views':views,'ageDays':round(age,3),'viewsPerDay':round(views/age,2),'thumbnails':m['snippet']['thumbnails']})
 eligible.sort(key=lambda x:x['viewsPerDay'],reverse=True)
 out.append({'channel':ch,'format':fmt,'listing_count':len(vs),'listing_exit':code,'eligible_count':len(eligible),'oldestFetched':min((meta[v['id']]['snippet']['publishedAt'] for v in vs if v['id'] in meta),default=None),'excludedMissingViews':sum(1 for v in vs if v['id'] in meta and 'viewCount' not in meta[v['id']].get('statistics',{})),'coverage':'200-listing cap; compare oldestFetched with cutoff' if len(vs)==200 else 'all returned listings','fast':eligible[:10],'slow':eligible[-10:],'all90days':eligible})
(P/'competitors.json').write_text(json.dumps({'at':now.isoformat(),'cutoff':cut.isoformat(),'samples':out},indent=2))
print([(r['channel'],r['format'],r['eligible_count']) for r in out])
