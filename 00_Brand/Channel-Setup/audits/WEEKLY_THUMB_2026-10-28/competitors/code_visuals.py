"""J1107 visual observations from review_sheets, 28 Oct 2026. No generation or API calls."""
import json, hashlib, re
from pathlib import Path
from PIL import Image, ImageStat
ROOT=Path(__file__).parent
ASSETS=Path('/Users/benjaminoats/_desk/J1107/competitors')
# Order: unique fast IDs followed by unique slow IDs, exactly as review_sheets.
# words | text treatment | subject/composition | curiosity mechanism | title hook
NOTES={
'veritasium': '''[none]|none|device right; silhouette left; blue light on black|unfamiliar apparatus makes the Einstein challenge tangible|wrong
How?|large white serif upper left|finger and green fibre diagonal on black|simple object with unexplained mechanism|Insane
We cracked it|large white serif right; red underline|large Enigma machine left; small person for scale|solved puzzle shown as a physical machine|Enigma
We tested it|large white serif top; red underline|hand and spider web fill frame|promised physical test of familiar claim|stronger
[none]|none|single glowing bulb centred on blue-black|announcement visual gives little specific story information|new
We filmed it.|large white serif top|eclipse above horizon; camera below; white arrow|proof captured by the camera|space''',
'realengineering': '''SKUNK WORKS’ NEWEST CREATION|large lime sans top left on black|large aircraft diagonal across landscape|novel engineering design|38%
ROMAN vs HUBBLE|large white sans top band|telescope and cosmic background; comparison in words|familiar versus new telescope|Monster
EARTH / 20% Lightspeed|large white sans left; yellow arrow|planet left; sail right; beam connects them|extreme speed and scale|20
RUTHLESS HUNTERS / Give it back! / AI|mixed small white/red labels|busy illustrated collage with embedded comment|controversy rather than engineering object|Insane
1926 / 2026|medium black numerals top|split before-after architecture; blue/red highlights|century of visible change|Documentary''',
'scishow': '''YOU CAN’T TOUCH THIS! / 10,000,000°|large white sans upper left; tiny number|host right holding glowing sphere; black background|physical impossibility and extreme heat|10,000,000
THERE’S A REASON?|large white sans diagonal bottom|jar and cannabis close-up|explains uneven familiar effect|Why
DYATLOV PASS|small black map label|host left; green map right; snowflakes|unresolved historical mystery|Finally
58|huge white number upper left|repeated host recedes into distance|count implies cloning limit|Clone
WHICH ONE?|large black sans right|host left over map with markers|contest between locations|First
THIS COLOR|large white sans upper left|almost solid mauve field and white arrow|unexpected medical consequence of colour|Saved
IT’S THE HEXAGONS|large white sans upper right|host left; giant gold texture|specific mechanism answers material question|Tarnish
WE HAVE NO IDEA WHAT THIS IS|large white sans upper left|host right; strange animal left|unidentified concrete specimen|Monster
[none]|none|moth left; mothballs right; prohibition symbol|recognisable object with forbidden-use symbol|Anymore
[none]|none|large eye implant and tool over face|surprising physical invention|Crash
FIELD TRIPS|small logo lettering|small central programme logo amid collage|series announcement rather than concrete question|Trailer
IN / THE / LIVER?|small red lettering on candy hearts|three pastel hearts on white|unexpected bodily location|Love
SPIDER VISION|large white sans top and bottom|spider centred in wireframe room|viewpoint of another creature|VR
[none]|none|penguin right; weather map behind|animal linked to unexpected large effect|Weather
MEDITERRANEAN DIET|large white sans centred|food collage across frame|familiar named subject; little added surprise|Best
[none]|none|hand holding pale rock against dark field|odd specimen with scale from hand|Aliens
Subway|medium white station-sign lettering|dense microbes surrounding subway sign|hidden life in familiar place|Living
[none]|none|monkey left; host right in green scene|host reaction and unusual animal behaviour|Weird
THE REAL DEAL|large white sans right; arrow|cork textures side by side|authentic material comparison|Artificial
[none]|none|gloved hands and syringe; white arrow; Field Trips logo|medical procedure indicated by arrow|Secret''',
'bigthink': '''SENSORY SURRENDER|large white sans bottom|illustrated people in busy dim scene|unusual phrase reframes doing nothing|nothing
SIMPLER THAN YOU THINK|large white sans right|seated expert left on white cutout over equations|promise to simplify intimidating maths|greatest
REALITY’S TRUE COLORS|large white sans centre|large multicoloured human silhouette|perception is constructed|power
PSEUDO SELF|large white sans top|small seated expert on white over collage of faces|hidden authentic identity|selfhood
UNLEARNING URKEL|large white sans centre|split archival character and adult interviewee|personal change from famous identity|outgrew
REALITY NEEDS YOU|large white sans bottom|eye fills backdrop with small person silhouette|viewer implicated in reality|answer
LIBERALISM, EXPLAINED|large white sans top|seated expert amid five portraits on black|familiar ideology explained|changed
Evil God Challenge|large white serif top|seated expert on white over fire/landscape|provocative thought experiment|God
THE FIRST COMPUTERS|large white sans right|seated expert left; organic patterns behind|reframes life's origins as computation|origin
1-MINUTE HABITS|large white sans upper left|growth stages of flower; seated expert right|small action promises lasting change|happiness
Conditions for Brilliance|medium white serif right|seated expert left in blue field with small figures|condition for high performance|20%
THE WANDERING MIND|large white sans right|seated expert left over green landscape|benefit in apparently idle state|bored
The History of Menstruation|medium black serif top|seated woman amid illustrated anatomy on pink|historical explanation of familiar biology|myths
THE RUMINATION TRAP|large black sans top|seated woman amid two thinker drawings|harm hidden in familiar habit|cost
How Relationships Die|medium white serif upper left|two interviewees flank broken heart|relationship risk visualised|5:1
5 BODY LESSONS|large black sans top|seated woman among anatomy drawings|numbered useful lessons|hidden
ARGUE BETTER|large white sans top|seated expert centred between old portraits|practical improvement|constructive''',
'kingsandgenerals': '''FRANCO’S COUP BEGINS / SPANISH CIVIL WAR|large white sans lower left; red band|portrait right over map|named decisive action starts a conflict|Collapsed
FROM CIVIL WAR TO SUPERPOWER|large white sans bottom|sultan right over Ottoman map|dramatic change in status|Superpower
RUSSO-JAPANESE WAR OF 1905 / MUKDEN 1905|large white serif/sans bottom|soldiers left; campaign map right|named battle and date|Largest
1857 INDIAN REBELLION|large white sans lower right|soldier left and coloured map|named historical event|Biggest
CONQUERING THE NORTH|large black sans upper left|warrior right over map|action-oriented territorial conquest|Forgotten
RUSSIAN INVASION OF UKRAINE SEPT 1–30 2026 / OPERATION VIVALDI|large white sans bottom band|leader left over campaign map|named secret operation|Secret
SIEGE OF KHORRAMSHAHR / IRAN-IRAQ WAR|large white sans bottom|leader right with firearm over map|named conflict with expectation reversal in title|Quick
THE ANARCHY|large yellow serif centre|map with central heraldic motif|succession crisis named|Tore
War of the Spanish Succession / 1701 / 1714|large white serif top|king and crown centred; flags/maps flank|date-bounded complete account|ALL
RISE OF MILOŠEVIĆ / YUGOSLAV WARS|large white sans bottom|leader centred over map|named leader's rise|Collapsed
AUSTRALIA’S NEW GUINEA CAMPAIGN|large white sans bottom|war scene and portrait; dark olive palette|named campaign|Broke
Mehmed’s Elite Guards|large white serif top|soldiers across dark orange scene|elite military unit|Elite
OTTOMANS IN WORLD WAR I / FALL OF JERUSALEM 1917|large white serif bottom|crowded historical group and city|turning-point loss and date|Fall
HOLY ROMAN WAR MACHINE|large white serif bottom|army before castle|metaphor turns empire into machine|Hidden
Unification of England / BRUNANBURH 937|large white serif bottom|crowded battle; banner top|named battle/date|Forgotten
RUSSIAN INVASION OF UKRAINE JUL 1–31 2026 / ECONOMIC STRUGGLE OF RUSSIA|large white sans bottom band|explosion over industrial landscape|current conflict stakes|Finally
Last Great Ruler of Iran / NADER SHAH / AFSHARID EMPIRE|large cream serif bottom; smaller map text|rider left over map|famous-person analogy in title|Napoleon
ROME vs DACIA|large white serif bottom|two groups of fighters fill frame|clear opposing sides|Richest
ROME’S STRUGGLE IN JUDEA|large cream serif top|warm cityscape at sunset|named struggle|Resistance
WERE GREEKS SEA PEOPLE?|large white serif bottom|map and directional arrows|identity question|Sea'''
}
d=json.loads((ROOT/'cohorts.json').read_text());coded=[]
for g in d['groups']:
 if g['tab']!='videos': continue
 ids=list(dict.fromkeys(g['fast_ids']+g['slow_ids'])); notes=NOTES[g['channel']].splitlines();assert len(ids)==len(notes),(g['channel'],len(ids),len(notes))
 rows={r['id']:r for r in g['all_90d']}
 for vid,note in zip(ids,notes):
  words,treatment,composition,gap,hook=note.split('|');r=rows[vid];im=Image.open(ASSETS/'thumbs'/f'{vid}.jpg').convert('L');s=ImageStat.Stat(im); hist=im.histogram();title=r['title'];shape='what-happens-if' if title.lower().startswith('what happens if') else 'question' if title.endswith('?') or re.match(r'^(How|Why|What|Who|When|Where|Is|Are|Did|Do|Could|Can)\b',title) else 'number' if re.match(r'^\d',title) else 'statement'
  coded.append({'id':vid,'channel':g['channel'],'format':'long','url':r['url'],'title':title,'published':r['published'],'views':r['views'],'views_per_day':r['views_per_day'],'fast':vid in g['fast_ids'],'slow':vid in g['slow_ids'],'title_shape':shape,'title_characters':len(title),'hook_word':hook,'thumbnail_words':words,'text_size_colour':treatment,'subject_and_composition':composition,'curiosity_gap':gap,'mean_luma':round(s.mean[0],2),'luma_std_contrast':round(s.stddev[0],2),'near_black_percent_luma_lt_20':round(sum(hist[:20])/sum(hist)*100,2),'visual_source':str(ASSETS/'review_sheets'/f'{g["channel"]}_videos.jpg'),'sha256':hashlib.sha256((ASSETS/'thumbs'/f'{vid}.jpg').read_bytes()).hexdigest(),'judgement':'worker visual observations; not causal CTR evidence'})
(ROOT/'long_visual_coding.json').write_text(json.dumps(coded,indent=2)+'\n');print(len(coded),'long thumbnails coded')
