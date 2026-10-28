"""Read-only HOS inventory and Analytics availability probe. No credentials persisted."""
import json, pathlib, urllib.request, urllib.parse, urllib.error, datetime, hashlib, concurrent.futures
ROOT=pathlib.Path('/Users/benjaminoats/YouTube/orbit-with-ben')
OUT=pathlib.Path(__file__).parent
MEDIA=pathlib.Path('/Users/benjaminoats/_desk/J1107/2026-10-28');MEDIA.mkdir(parents=True,exist_ok=True)
def request(url, data=None, token=None):
 h={'User-Agent':'Mozilla/5.0'}
 if token:h['Authorization']='Bearer '+token
 try:
  with urllib.request.urlopen(urllib.request.Request(url,data=data,headers=h),timeout=40) as r:return json.load(r)
 except urllib.error.HTTPError as e:
  body=json.load(e);return {'http_status':e.code,'error':body.get('error',{}).get('message','request rejected') if isinstance(body.get('error'),dict) else 'request rejected'}
env={}
for line in (ROOT/'07_Content-Ops/.env').read_text().splitlines():
 if '=' in line and not line.lstrip().startswith('#'):
  k,v=line.split('=',1);env[k.strip()]=v.strip().strip('\"\'')
a=request('https://oauth2.googleapis.com/token',urllib.parse.urlencode({'client_id':env['GOOGLE_CLIENT_ID'],'client_secret':env['GOOGLE_CLIENT_SECRET'],'refresh_token':env['YT_ANALYTICS_REFRESH_TOKEN_HOS'],'grant_type':'refresh_token'}).encode())
token=a.get('access_token');assert token,'Read-only token refresh failed'
def get(endpoint,params):return request(endpoint+'?'+urllib.parse.urlencode(params),token=token)
api='https://www.googleapis.com/youtube/v3/'
mine=get(api+'channels',{'part':'id,contentDetails','mine':'true'})
assert mine['items'][0]['id']=='UCXp7HkBIl1LgaznXuZHJyRg','Wrong channel'
ids={v['id'] for v in json.load(open(ROOT/'05_Analytics/hos/snapshots/2026-10-28.json'))['videos']}
pl=mine['items'][0]['contentDetails']['relatedPlaylists']['uploads'];page=''
while True:
 r=get(api+'playlistItems',{'part':'contentDetails','playlistId':pl,'maxResults':50,'pageToken':page})
 ids.update(v['contentDetails']['videoId'] for v in r.get('items',[]));page=r.get('nextPageToken')
 if not page:break
videos=[]
for start in range(0,len(ids),50):
 r=get(api+'videos',{'part':'snippet,status,contentDetails,statistics','id':','.join(sorted(ids)[start:start+50])});videos+=r.get('items',[])
(OUT/'inventory_api.json').write_text(json.dumps({'collectedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'videos':videos},indent=2))
reports={}
for metrics in ['views','videoThumbnailImpressions,videoThumbnailImpressionsClickRate','impressions,impressionsCtr']:
 reports[metrics]=get('https://youtubeanalytics.googleapis.com/v2/reports',{'ids':'channel==MINE','startDate':'2026-09-29','endDate':'2026-10-26','dimensions':'video','metrics':metrics,'sort':'-views' if metrics=='views' else '-videoThumbnailImpressions','maxResults':200})
(OUT/'analytics_probe.json').write_text(json.dumps(reports,indent=2))
def download(v):
 s=v['status']
 if s['privacyStatus']!='public' and not s.get('publishAt'):return None
 thumbs=v['snippet']['thumbnails'];t=next(thumbs[k] for k in ['maxres','standard','high','medium','default'] if k in thumbs)
 p=MEDIA/(v['id']+'.jpg')
 try:
  with urllib.request.urlopen(t['url'],timeout=30) as r: b=r.read()
  p.write_bytes(b)
  return {'id':v['id'],'url':t['url'],'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
 except Exception as e:return {'id':v['id'],'error':type(e).__name__}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:manifest=[x for x in ex.map(download,videos) if x]
(OUT/'thumbnail_manifest.json').write_text(json.dumps(manifest,indent=2))
print('Inventory:',len(videos),'Public/scheduled thumbnails:',len(manifest))
print('Analytics probes:',json.dumps({k: v.get('error','OK') for k,v in reports.items()}))
