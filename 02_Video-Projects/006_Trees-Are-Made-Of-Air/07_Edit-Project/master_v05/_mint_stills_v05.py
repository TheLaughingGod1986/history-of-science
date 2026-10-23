#!/usr/bin/env python3
"""J0886: four fresh Flow Nano Banana start frames, zero-credit guarded."""
import importlib.util
from pathlib import Path
SHARED=Path('/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project')
spec=importlib.util.spec_from_file_location('mint_v04',SHARED/'master_v04/_mint_stills_v04.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.OUT_DIR=Path(__file__).resolve().parent
m.STILLS_DIR=m.OUT_DIR/'stills'
m.still_tool.MEDIA_CLIPS=m.STILLS_DIR
m.STILLS=[
 {'id':'02_balance_trunk_v05','part':'01','core': 'Wide three-quarter view of a giant brass two-pan balance scale standing in a sunlit Flemish meadow. A whole small mature willow tree with a compact dense root ball rests INSIDE the deep LEFT weighing pan. The entire root mass and the base of the trunk are firmly seated down in the bowl of the pan, visibly supported by its brass bottom. No roots hang outside the pan, no gap beneath the roots, no floating. The tree canopy fits in frame. On the right weighing pan rests a mound of dark soil. Clear physical contact between roots and pan. Stable planted composition, no loose airborne soil.'},
 {'id':'05_pure_water_v05','part':'02','core': '1640s Flemish brick courtyard. Medium wide view showing the ENTIRE large terracotta pot and a small young willow tree whose trunk grows directly from dark soil at the CENTER INSIDE that pot. All the roots are buried in that pot. The pot is in the middle of the courtyard well away from every background tree. A flat perforated tin lid fits around the small trunk on the pot rim. Jan Baptist van Helmont in black doublet, white linen collar, dark shoulder-length hair and neat beard stands at the right, his full torso and both arms visible, gently watering the soil through the lid using a copper watering can. No tree behind or beside the pot, no detached trunk.'},
 {'id':'17_notebook_tick_v05','part':'03','core': '1771 English study, warm window light, medium wide view of Joseph Priestley seated at his oak desk. Show his head, shoulders, chest and BOTH full forearms continuously connected to his body. 18th century dark clerical coat and white collar. His right hand holds a quill over an open unmarked cream notebook, left hand resting on desk. A clear glass bell jar stands on a tray on the desk to his left. Whole person above waist, no detached or floating hand, no wrist cut off within frame, no writing or symbols on the paper.'},
 {'id':'10_only_green_v05','part':'04','core': 'Close eye-level shot of three separate clear hand-blown glass jars on a sunny 1779 English laboratory windowsill, all jars fully visible. Each jar is filled four-fifths with clear water, with a clear flat visible horizontal WATER SURFACE well below the rim. Left jar has a submerged pale root, middle jar has a submerged red flower, right jar has a submerged green leaf. Only the right green leaf has a few tiny silver oxygen bubbles clinging to its submerged surface. All leaves and objects lie completely UNDER the water surface. All air above the water surface and outside the jars is entirely clean and empty. Absolutely no bubbles or droplets in air, no spray, no effervescence plume, no steam, no sparkling dust or floating particles.'}
]
if __name__=='__main__':
 import json
 result=m.main()
 old=m.OUT_DIR/'FLOW_STILLS_LOG_v04.json'
 if old.exists():
  doc=json.loads(old.read_text());doc['job']='J0886'
  (m.OUT_DIR/'FLOW_STILLS_LOG_v05.json').write_text(json.dumps(doc,indent=2)+'\n')
 raise SystemExit(result)
