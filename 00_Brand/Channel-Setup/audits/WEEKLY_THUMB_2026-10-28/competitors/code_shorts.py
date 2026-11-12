"""Manual thumbnail observations; API-served Shorts images are not proven feed openings."""
import json, hashlib, re
from pathlib import Path
from PIL import Image, ImageStat
ROOT=Path(__file__).parent; ASSETS=Path('/Users/benjaminoats/_desk/J1107/competitors')
# Explicitly mark unreadable transcript fragments; do not invent words from OCR.
NOTES={
'veritasium': '''[no readable hook]|none|runner in park|everyday activity opens physiological question|heart
[no readable hook]|none|hand holding textured model|concrete demonstration of technical concept|dislocation
[no readable hook]|none|Einstein portrait|recognisable scientist anchors speed-limit question|faster
Rome’s Escalator Disaster|small white serif central|escalator/industrial scene|specific incident and danger|Dangerous
[small dialogue; not fully legible]|small yellow caption|two people handling phone|theft challenge proved physically|$10,000
If you defecate|small white caption|host with microphone outdoors|unexpected physical route of weight loss|weight
[no readable hook]|none|fork held over pan|familiar object linked to safety question|Dangerous
$10K Physics Bet|small white serif|wind-powered vehicle|challenge with monetary stakes|Bet
[no readable hook]|none|host holding two balloons|visible experiment with expected outcome withheld|balloons
Scariest Chart In Engineering|small white serif lower|host close-up in wire-grid scene|extreme claim about technical object|Scariest
[no readable hook]|none|identical twins side by side|identity puzzle tied to crime|perfect
[no readable hook]|none|host with orange balls on table|surprising physical action|Squeezing
[question marks]|small yellow symbols|map on dark field|location puzzle|submarines
[no readable hook]|none|dim painting of seated thinker|counterintuitive impossibility|impossible''',
'bigthink': '''and it’s using good debate|tiny white on black subtitle|single speaker close-up|practical interpersonal problem|stupid
and that’s an example|tiny white on black subtitle|single speaker close-up|numbered explanation of behaviour|3
500 times|small white on black subtitle|microbe illustrations|scientific origin question|life
against the door|tiny white on black subtitle|single speaker seated|hidden emotional cost|hidden
but|tiny white on black subtitle|brain silhouette with cosmic inset on black|origin mystery|3
like some big reptile|tiny white on black subtitle|single speaker seated|revision of familiar dinosaur image|feathers
that’s what|tiny white on black subtitle|single speaker seated|power of naming feelings|powerful
or someone you care about|tiny white on black subtitle|single speaker seated|familiar habit reframed as trap|hidden
why the arms were so small|tiny white on black subtitle|single speaker seated|odd physical feature|pathetic
How to embrace stress / Don’t be afraid of it / Protect recovery / Enjoy your recovery.|small white list on black|full text card|practical list; visual differs from talk footage|3
[small dialogue; not fully legible]|tiny white on black subtitle|two remote interview panes|social problem|conversations
an American citizen|tiny white on black subtitle|two remote interview panes|political behaviour|hypocrisy
because you promised|tiny white on black subtitle|two remote interview panes|high-stakes election claim|important
are nuanced like this|tiny white on black subtitle|single speaker seated|definition of familiar emotional term|vulnerable
RICHARD KELLY / DONNIE DARKO DIRECTOR / progress|small white name card and subtitle|interview clip with black bars|film-maker on current technology|AI
It’s made of atoms.|tiny white on black subtitle|single speaker close-up|basic physical measurement question|temperature
RICHARD KELLY / DONNIE DARKO DIRECTOR / you know|small white name card and subtitle|interview clip with black bars|storytelling medium|story
what we’ve learned|tiny white on black subtitle|single speaker close-up|practical communication improvement|supercommunicator
just using energy|tiny white on black subtitle|single speaker seated|misconception about strength|mistake
and the same thing is true|tiny white on black subtitle|single speaker close-up|new planetary finding|planets''',
'kingsandgenerals': '''Why Britain Was Expendable|small white serif on red top band|Roman figure over warm background|reversal of expected imperial value|Rome
The Sultan’s Child Levy|small white serif on red top band|map with markers|concrete extraction ratio in title|1
Rome’s Most Militarized Province|small white serif on red top band|Britain map with military markers|extreme concentration of troops|30,000
Anglo-Saxon Warriors in Exile|small white serif on red top band|map and illustration|unexpected cross-culture role|Bodyguards
The War That Bankrupted England|small white serif on red top band|map of England and France|financial consequence of war|Bankrupted
Who Are the Gurkhas?|small white serif on red top band|India/Nepal map|identity behind famous claim|Gurkha
The Plague That Transformed Europe|small white serif on red top band|two medieval figures|unexpected dress prohibition; thumbnail-title mismatch worth checking|Banned
Evolution of the Roman Legions|small white serif on red top band|three soldiers side by side|internal threat behind familiar army|Threat
Pompey Desecrates the Temple|small white serif on red top band|silhouette in doorway|forbidden room and expectation reversal|Empty
Native Pride Disrespected|small white serif on red top band|historical portrait|small insult creates large consequence|Insult
The Symbol of Norse Kings|small white serif on red top band|burning ship on muted sea|burial ritual explained|Buried
The Symbol of Norse Kings|small white serif on red top band|same burning-ship composition|burial belief questioned|Funerals
Medieval Christianity in Africa|small white serif on red top band|small figure by pale building|unexpected geography of religion|Hidden
The Beacon That Made History|small white serif on red top band|figures in dark interior|communication affects revolution|Slow
Life on Hadrian’s Wall|small white serif on red top band|Roman Britain map|harsh everyday conditions|Disease
Overlooked in Medieval Africa|small white serif on red top band|two illustrated figures on parchment|unexpected political power|Women
Death by Lacrosse|small white serif on red top band|soldiers with sporting stick|game becomes military turning point|Destroyed
Cults & Religion in Roman Britain|small white serif on red top band|portrait beside artefact/inscription|hidden religious life|Secret
The Norman Conquest|small white serif on red top band|map and medieval scene|familiar turning point and date|1066
The Bogeymen of Rome|small white serif on red top band|Gallic warrior and blades on blue|ancient fear surrounding named group|Nightmare'''
}
d=json.loads((ROOT/'cohorts.json').read_text());out=[]
for g in d['groups']:
 if g['tab']!='shorts' or not g['all_90d']:continue
 ids=list(dict.fromkeys(g['fast_ids']+g['slow_ids']));notes=NOTES[g['channel']].splitlines();assert len(ids)==len(notes),(g['channel'],len(ids),len(notes));rows={r['id']:r for r in g['all_90d']}
 for vid,note in zip(ids,notes):
  words,treatment,composition,gap,hook=note.split('|');r=rows[vid];im=Image.open(ASSETS/'thumbs'/f'{vid}.jpg').convert('L');s=ImageStat.Stat(im);h=im.histogram();title=r['title'];shape='what-happens-if' if title.lower().startswith('what happens if') else 'question' if title.endswith('?') or re.match(r'^(How|Why|What|Who|When|Where|Is|Are|Did|Do|Could|Can)\b',title) else 'number' if re.match(r'^\d',title) else 'statement'
  out.append({'id':vid,'channel':g['channel'],'format':'short','url':r['url'],'title':title,'published':r['published'],'views_per_day':r['views_per_day'],'fast':vid in g['fast_ids'],'slow':vid in g['slow_ids'],'thumbnail_words':words,'text_size_colour':treatment,'subject_and_composition':composition+'; portrait centre with dim side fill in served image','curiosity_gap':gap,'hook_word':hook,'title_shape':shape,'title_characters':len(title),'mean_luma':round(s.mean[0],2),'luma_std_contrast':round(s.stddev[0],2),'near_black_percent_luma_lt_20':round(sum(h[:20])/sum(h)*100,2),'sha256':hashlib.sha256((ASSETS/'thumbs'/f'{vid}.jpg').read_bytes()).hexdigest(),'caveat':'served thumbnail only; not verified selected cover or frame zero. Small text not always fully readable at sheet size; no feed-performance inference.'})
(ROOT/'short_visual_coding.json').write_text(json.dumps(out,indent=2)+'\n');print(len(out),'Short thumbnail observations')
