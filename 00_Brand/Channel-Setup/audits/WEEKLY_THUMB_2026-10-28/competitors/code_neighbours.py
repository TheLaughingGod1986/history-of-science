import json,hashlib,re
from pathlib import Path
from PIL import Image,ImageStat
root=Path(__file__).resolve().parent.parent
# Manual observations from every saved fast/slow contact sheet, 28 Oct 2026.
# Each row is text | colour/type | subject/composition | curiosity device.
raw={
'RationalThinker118/videos': '''He Ne Ar Xe|multicolour handwritten symbols|two scientist portraits flanking apparatus, black background|discovery people and chemical symbols
INSIDE THE PROTON?|large white condensed|portraits flanking coloured proton diagram|hidden interior question
INVERSE SQUARE LAW?|large white condensed|portraits flanking force diagram|mechanism question
HOW BIG IS IT?|large white condensed|solar system with portrait right|scale question''',
'HistoryoftheUniverse/videos': '''EINSTEIN HATED THIS IDEA.|white outlined strip|Einstein eyes below connected glowing particles|famous scientist opposition''',
'pbsorigins/videos': '''NATIVE? or BLACK?|large cream bold|two archival portraits on warm textured background|identity choice
FEMALE FROLIC?|large white and red italic|woman portrait against historical collage|unexpected historical phrase
CRISPUS ATTUCKS|large white bold|monochrome portrait with red historical collage|named historical figure''',
'pbsorigins/shorts': '''Africatown, Alabama / Founded by survivors of one of the last legal slave ships|small dark text on parchment|archival group photo, central narrow frame|historical location context
He was a fool!|small white in blue box|monochrome face centre|provocative quotation
Before we had a rainbow, we had a garden|small white subtitle|man in floral painted scene|unexpected analogy
BRITISH RULE????????|small white in blue box|historical battle painting|counterfactual
I WANT YOU / NATIVE LAND|red and black poster lettering|Uncle Sam poster centre|familiar poster reversal
Real Voices of Formerly Enslaved People, Pt. II|small dark text on parchment|archival portrait collage|authentic recorded voices''',
'crashcourse/videos': '''INSIDE U.S. Elections|large white with red accent|ballot machinery and blue field|inside view
Electoral College EXPLAINED|large dark and white red-accented|red blue US map|mechanism explanation
Mining for Minerals!|large cream and yellow serif|open pit mine|process
To Vote or Not to Vote|large dark/red|face left ballot right|binary decision
Harnessing Earth's Energy|large cream and yellow serif|steam and geothermal landscape|useful mechanism
Who actually pays for this?|large cream|money bags and red blue silhouettes|hidden funding
ASTRONOMY MARATHON|cream green logo|bright galaxy central logo|collection label
Only two?|large cream|face between party icons|number puzzle
Why Are U.S. Politics So Divisive?|large cream|red blue columns|explanation question
Should We Worry?|large cream serif|asteroid over Earth|threat question
Disappearing Glacier?|large yellow serif|mountain glacier|change question
U.S. Government|large yellow|face beside capitol illustration|catalogue label
4 Billion Years?|large cream serif|early Earth render|scale question
Fossils!|large yellow serif|museum skeleton|object label
A Billion Years Gone?|large cream serif|host over canyon|missing time
Earthquake Preparedness|large cream yellow serif|host in room|practical promise
EARTHQUAKE!|large cream serif|host in rubble scene|event''',
'crashcourse/shorts': '''EARTHQUAKE RESISTANT BUILDINGS|small cream in red box|host below skyscrapers central vertical|engineering solution
WILL THE YELLOWSTONE VOLCANO ERUPT AGAIN?|small cream in red box|blue geothermal vertical plate|eruption question
NATURE STRATIGRAPHY FIELD TRIP|cream on tilted teal box|outdoor smiling host|trip invitation
OCEAN FOSSILS ON MT. EVEREST?!|small cream in red box|host and fossil illustration|location mismatch
PLATE TECTONICS|small cream in red box|host under map|topic label''',
'HumanProgressOrg/videos': '''MARTIN SELIGMAN|small dark uppercase|drawn portrait over yellow sky blue clouds|person name
JONATHAN ALPERT|small dark uppercase|drawn portrait over yellow sky blue clouds|person name
KEVIN CORINTH|small dark uppercase|portrait and banknotes on yellow blue|money debate
WALKER WRIGHT|small dark uppercase|portrait with ship on yellow blue|markets story
BRIAN ALBRECHT|small dark uppercase|portrait and coin stacks on yellow blue|prices story
SCOTT WINSHIP|small dark uppercase|portrait and coin stacks on yellow blue|poverty story''',
'HumanProgressOrg/shorts': '''last meals|tiny white subtitle|historical execution illustration vertical|historical shock
in Europe|tiny white subtitle|dark medieval street illustration|historical setting
reform legislation|tiny white subtitle|talking head vertical|policy discussion
to Chat|tiny white subtitle|older man talking head vertical|interview excerpt
the first hand|tiny white subtitle|warm painted bedside death scene|historical intimacy
This was not a|tiny white subtitle|woman at podcast microphone|interview excerpt
is a good thing|tiny white subtitle|man talking with hand gesture|interview excerpt
unreadable at phone size|tiny white subtitle|man on video call|interview excerpt
Because you can|tiny white subtitle|man talking head|interview excerpt
for your plastic|tiny white subtitle|man podcast interview|interview excerpt
that governments|tiny white subtitle|woman podcast interview|interview excerpt
is|tiny white subtitle|man talking head|interview excerpt
sorts of stuff|tiny white subtitle|man podcast interview|interview excerpt
What I said to|tiny white subtitle|man podcast interview|interview excerpt
unreadable at phone size|tiny white subtitle|man in purple room|interview excerpt
at the table in these games|tiny white subtitle|same man in purple room|interview excerpt
of whatever many of these|tiny white subtitle|same man in purple room|interview excerpt''',
'TEDEd/videos': '''A TED-ED HALLOWEEN SPECIAL|large red hand-lettered|green cartoon cemetery|seasonal collection
CAN'T FOCUS? WATCH THIS|large navy bold|purple bored character on cyan|viewer problem
THE BEST WAY TO USE A CREDIT CARD|large black bold|character on heap of money cyan background|practical promise
DON'T FALL FOR THESE 5 TRICKS|large black condensed|sale price tag on cyan|number warning
WHY DON'T HYDRAS AGE?|large black condensed|cartoon hydra at desk on yellow|biology puzzle
BUYING vs. RENTING|large dark bold|two buildings green purple split|binary choice
ALWAYS GETTING LOST? WATCH THIS|large black condensed|driver in car warm yellow|viewer problem
THE AI DATA CENTER CRISIS|large cream bold|man holding small Earth purple|timely resource problem
HISTORY vs. QUEEN VICTORIA|large navy serif|queen and Union Jack|historical conflict
3 WAYS TO PRESENT YOUR IDEAS|large white bold|red hand against black teal|practical numbered promise
THE BEST WAY TO EXPLAIN COMPLEX IDEAS|large white bold|blue dots black ground|practical promise
HOW ARE MAGNETS MADE?|large red italic|red blue magnet on yellow|mechanism question
HOW TARIFFS WORK|large red bold|cartoon coins border grey|mechanism explanation
WHY ARE BIRDS ALWAYS SICK?|large black condensed|cartoon bird and cough warm grey|biology question
6 WAYS TO BE MORE PERSUASIVE|large white|white speech bubbles red field|practical numbered promise
HOW TO TELL GREAT STORIES|large navy bold|pink branching tree on cream|practical promise
PLATO'S WARNING|large yellow condensed|painted philosopher on ship|historical warning
WHY IS PLANE BOARDING SO SLOW?|large red condensed|sketch of queue grey|everyday frustration
HOW DO MAGLEV TRAINS WORK?|large dark italic|purple train diagonal|mechanism question
THE GREEK MYTH OF APOLLO'S CURSE|large black condensed|yellow eyes above neon yellow text band|myth reveal'''
}
manifest={x['id']:x for x in json.load(open(root/'recovered/neighbour_thumbnail_manifest.json'))}
out=[]; coverage=[]
for s in json.load(open(root/'recovered/neighbour_competitors.json'))['samples']:
 rows=list({v['id']:v for v in s['fast']+s['slow']}.values()); key=s['channel']+'/'+s['format']
 obs=[x.split('|') for x in raw.get(key,'').splitlines()]; assert len(rows)==len(obs),(key,len(rows),len(obs))
 fast={v['id'] for v in s['fast']};slow={v['id'] for v in s['slow']}
 coverage.append({'channel':s['channel'],'format':s['format'],'eligible':s['eligible_count'],'coded':len(rows),'tail_overlap':len(fast&slow),'coverage':s['coverage']})
 for v,o in zip(rows,obs):
  m=manifest[v['id']];p=Path(m['path']);h=hashlib.sha256(p.read_bytes()).hexdigest();assert h==m['sha256'],p
  im=Image.open(p).convert('RGB');w,hh=im.size
  # hqdefault 4:3 files letterbox a 16:9 thumbnail; exclude padded rows from numerical diagnostics.
  crop=(hh-round(w*9/16))//2 if abs(w/hh-4/3)<.02 else 0
  if crop:im=im.crop((0,crop,w,hh-crop))
  lum=im.convert('L');stat=ImageStat.Stat(lum);hist=lum.histogram()
  title=v['title']; shape='what-happens-if' if title.lower().startswith('what happens if') else 'question' if '?' in title or re.match(r'^(How|Why|What|Who|Is|Do|Which)\b',title) else 'number' if re.match(r'^\d',title) else 'statement'
  out.append({'id':v['id'],'url':'https://www.youtube.com/watch?v='+v['id'],'channel':s['channel'],'format':s['format'],'title':title,'title_shape':shape,'title_length':len(title),'title_hook':title.split(' - ')[0].split(' | ')[0].split(': Crash Course')[0],'publishedAt':v['publishedAt'],'viewsPerDay':v['viewsPerDay'],'cohorts':(['fast'] if v['id'] in fast else [])+(['slow'] if v['id'] in slow else []),'thumbnail_text':o[0],'text_style':o[1],'subject_composition':o[2],'curiosity_gap':o[3],'mean_luma':round(stat.mean[0],2),'luma_stddev':round(stat.stddev[0],2),'near_black_fraction':round(sum(hist[:20])/sum(hist),4),'image':m,'method':'Manual visual observation of saved contact sheet; numerical diagnostics exclude hqdefault letterbox. Short API image is not verified chosen cover or frame 0.'})
(root/'competitors/neighbour_visual_coding.json').write_text(json.dumps(out,indent=2)+'\n')
(root/'competitors/neighbour_coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
print('Coded and hash-verified',len(out),'unique images');print(json.dumps(coverage,indent=2))
