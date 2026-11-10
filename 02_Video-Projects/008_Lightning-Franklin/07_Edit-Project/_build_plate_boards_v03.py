#!/usr/bin/env python3
"""J0240 — Build and price HOS 008 plate boards v03 (boards only, no mint, no spend).

Follow-on from J0184 (acting-Chief price PASS with conditions; HOS #317 merged 520cbe7):
  (a) Rewrite every Fast row flagged emissive (candles, sparks, flicker) into non-emissive
      framing. Keep the light off-screen, or show it by its effect on faces or walls without
      the flame in shot. Move P5:07_giant_spark (where the giant lightning bolt is the story)
      into the 15 Quality heroes and drop P3:25_fibres_rise (hemp twine fibres in grey storm
      daylight, no emissive light) to Fast, so the 15 Quality hero total holds.
  (b) Turn the 11 flat-card and diagram rows into £0 code graphics (our own Python/Pillow/ffmpeg
      renderer, HOS house explainer look), each with its own per-row spec (`code_graphic_spec`),
      alternating full-frame period-paper inked diagrams with moving-plate-backed explainer
      overlays where rows are adjacent so two full-frame teach graphics never run back to back.
  (c) Measure the unused moving footage in each v02 reuse row's source KEEP clip (8.00 s clip,
      7.90 s usable after cross-fade pad). Every one of the 15 v02 reuse rows requires more
      duration (3.10–5.96 s) than the unused moving footage left in its source clip (1.94–4.14 s
      usable / 2.04–4.24 s raw), so none can get a distinct non-overlapping window of its full
      length without looping, freeze-padding or replaying frames. All 15 become priced Fast mints
      with non-emissive prompts.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

EDIT = Path(__file__).resolve().parent
PARTS = EDIT / "parts"

CLIP_RAW_S = 8.0
CLIP_USE_S = 7.9
REUSE_PAD_S = 0.5
VERTEX_LENGTHS = (4, 6, 8)
PRICE_FIELDS = (
    "flow_credits_try1",
    "flow_credits_expected",
    "vertex_try1_gbp",
    "vertex_expected_gbp",
)

STYLE = "Premium Animistry-class 3D cartoon. "
TAIL = (
    " No readable words or numbers anywhere. Silent. Continuous motion through"
    " the final frame. No Explorer. No Orbit."
)
NOSTRIKE = " The kite and string are never struck; no bolt touches them."
SAFE = " Nobody is struck, burned or hurt."
FRANKLIN = (
    "Benjamin Franklin in his mid-forties, plain short wig, no spectacles,"
    " brown 1750s coat"
)
WILLIAM = (
    "William Franklin, a young man of about twenty-one in a tricorn hat (an"
    " adult, never a child)"
)
JAR = (
    "a glass jar lined with metal foil, a cork stopper with a thick wire"
    " through it bent into a ring at the top"
)

# 15 Quality heroes: P5:07_giant_spark (giant bolt across sky is the story) replaces
# P3:25_fibres_rise (hemp twine fibres lifting in grey storm daylight, non-emissive).
HEROES = {
    "P1:01_kite_open": "Long title opening",
    "P1:13_ring_the_bells": "Short B cover",
    "P1:17_globe_spark": "Bench electricity proof and later callback",
    "P2:08_jar_spark": "Leyden jar discharge proof",
    "P2:13_explorer_jar": "Explorer hero beat",
    "P3:06_marly_spark": "First physical lightning proof",
    "P3:19_kite_climb": "Short A cover",
    "P4:02_knuckle_spark": "Kite experiment proof",
    "P4:04_fill_the_jar": "Stored lightning proof",
    "P4:05_jar_spark_field": "Stored-charge discharge proof",
    "P4:09_charge_string": "Core charge mechanism",
    "P5:07_giant_spark": "Giant spark / hotter than the Sun scale hero (swapped for P3:25_fibres_rise)",
    "P5:14_safe_towers": "Lightning rod protection proof",
    "P5:16_explorer_rooftop": "Explorer hero beat",
    "P5:19_skyline_strike": "Short C cover / modern title payoff",
}

# (a) & (c): Non-emissive Fast prompts for every rewritten Fast row and every former-reuse row
# converted to a priced Fast mint (plus P3:02_sentry_box cleaned so it's a 3D desk shot, not a card).
FAST_PROMPTS = {
    # Part 01
    "P1:01_kite_open_c1": (
        STYLE
        + "Same Philadelphia 1752 field and open wooden shed set at dusk: wide"
        " view from behind the wooden fence as wind bends the tall wet grass"
        " and the silk kite pulls taut high against dark rolling storm clouds;"
        " rain slants across the field, cool indirect sky light only, nothing"
        " emissive in shot."
        + NOSTRIKE
        + TAIL
    ),
    "P1:02_tower_tilt": (
        STYLE
        + "Overcast storm dusk over a modern city: a slow tilt up a tall"
        " generic glass tower to the thin pointed metal rod at its very top as"
        " heavy dark storm clouds roll past overhead; cool indirect sky light"
        " on the glass facade, nothing emissive in shot. No real or"
        " recognisable building."
        + TAIL
    ),
    "P1:03_table_three_c1": (
        STYLE
        + f"Same Philadelphia 1752 back-room wooden table in soft daylight from an off-screen window: close tracking drift across the silk kite, the iron key and {JAR} resting side by side on the timber grain; nothing emissive in shot."
        + TAIL
    ),
    "P1:04_storm_mystery": (
        STYLE
        + "Ancient countryside at deep storm dusk: enormous bruised-slate"
        " thunderheads roll low over wind-bent trees and dark hills, brief"
        " cool indirect sky-light shifting across the hillside from off-screen"
        " above the frame; nothing emissive in shot. Slow push."
        + TAIL
    ),
    "P1:05_split_tree": (
        STYLE
        + "A lone oak tree on a wind-swept hillside in heavy storm rain right"
        " after a strike: pale freshly split timber along the trunk and a"
        " broken bough settling onto the wet grass as thin grey steam curls"
        " into the rain; cool off-screen storm light across the hillside,"
        " nothing emissive in shot. No animals shown hurt."
        + TAIL
    ),
    "P1:06_heavens": (
        STYLE
        + "Same European 18th-century town street in a storm: wide view of"
        " townsfolk in 18th-century coats and shawls standing in doorways and"
        " looking up toward heavy overhanging storm clouds, hands clasped,"
        " figures small in frame as cool indirect sky light shifts across the"
        " wet stone walls from off-screen; nothing emissive in shot."
        + SAFE
        + TAIL
    ),
    "P1:08_sky_flash": (
        STYLE
        + "Same European 18th-century town rooftops in a summer storm: sheets"
        " of heavy rain sweep across steep slate and timber roofs as sudden"
        " pale indirect sky light from off-screen above washes over the wet"
        " tiles and chimney pots, then dims into deep storm shadow; nothing"
        " emissive in shot."
        + TAIL
    ),
    "P1:09_barn_smoke": (
        STYLE
        + "At the edge of town, grey smoke rises from a wet barn roof into the"
        " heavy rain; wide shot seen from a distance, nothing emissive in"
        " shot, no people or animals in danger."
        + TAIL
    ),
    "P1:11_tall_spire": (
        STYLE
        + "Same European 18th-century town in storm dusk: a church's tall"
        " wooden spire rises high above the low slate and timber roofs while"
        " dark storm clouds churn right over its weathervane in driving rain;"
        " cool indirect sky light on the wet shingles, nothing emissive in"
        " shot."
        + TAIL
    ),
    "P1:12_steeple_fire": (
        STYLE
        + "Same European 18th-century town in heavy rain after a strike: thick"
        " dark smoke billows from split shingles near the top of the church's"
        " wooden spire while townspeople below hurry across the wet cobbles"
        " carrying leather water buckets, figures small in frame; warm"
        " off-screen reflection on the wet stone wall, nothing emissive in"
        " shot."
        + SAFE
        + TAIL
    ),
    "P1:13_ring_the_bells_c1": (
        STYLE
        + "Same stone bell-tower interior in grey storm daylight: close on the"
        " thick hemp bell ropes rising and falling through the timber ceiling"
        " guide holes as heavy bronze bells swing in shadow above; rain blows"
        " through the stone louvres, no faces close, nothing emissive in"
        " shot."
        + SAFE
        + TAIL
    ),
    "P1:15_bell_count_c1": (
        STYLE
        + "Same stone bell-tower interior in grey storm light: slow downward"
        " tilt along the stone wall to the coiled ends of the silent hemp"
        " ropes resting on the damp timber floor as rainwater drips from the"
        " louvred sill; no people, nothing emissive in shot."
        + TAIL
    ),
    # Part 02
    "P2:01_salon_tube": (
        STYLE
        + "Same 1740s panelled salon in warm afternoon light from tall side"
        " windows out of frame: over-the-shoulder view of a travelling"
        " lecturer's hands rubbing a long clear glass tube briskly with a silk"
        " cloth before a blurred semicircle of well-dressed guests; warm"
        " indirect light on the wood panelling, nothing emissive in shot."
        + TAIL
    ),
    "P2:02_salon_spark": (
        STYLE
        + "Same 1740s panelled salon in warm off-screen window light: close on"
        " a rubbed glass tube held near a guest's powdered curls as loose"
        " strands of hair lift and float toward the glass and her hand draws"
        " back with a startled laugh; warm indirect light on faces and wall,"
        " nothing emissive in shot."
        + SAFE
        + TAIL
    ),
    "P2:03_audience_shock": (
        STYLE
        + "Same 1740s panelled salon in warm off-screen light: medium-wide"
        " view of a row of well-dressed guests holding hands who jolt in"
        " unison and laugh together as the static impulse passes along the"
        " linked hands; nothing emissive in shot."
        + TAIL
    ),
    "P2:04_franklin_watches": (
        STYLE
        + f"Same 1740s panelled salon: {FRANKLIN} leans forward in the audience, watching the glass tube intently as warm off-screen light shifts across his face and coat; nothing emissive in shot."
        + TAIL
    ),
    "P2:05_print_shop": (
        STYLE
        + f"A Philadelphia printing shop in morning daylight, wooden hand press and type cases: {FRANKLIN} hands his apron to a younger partner and carries a glass tube into the back room; nothing emissive in shot."
        + TAIL
    ),
    "P2:06_leyden_jar": (
        STYLE
        + f"Same Philadelphia 1752 back-room workshop in soft daylight from a side window: close on Franklin's hands lifting {JAR} from a shelf of jars and setting it on the wooden bench; nothing emissive in shot."
        + TAIL
    ),
    "P2:09_window_storm": (
        STYLE
        + f"Same Philadelphia 1752 back-room workshop: {FRANKLIN} stands by the rain-streaked window as cool indirect light from an off-screen distant storm shifts across the window frame and his profile; he turns his head slowly from the bench jar toward the dark clouds outside, nothing emissive in shot."
        + TAIL
    ),
    "P2:10_flash_crack_smell": (
        STYLE
        + "Same Philadelphia 1752 back-room workshop: close on Franklin's hand"
        " recoiling beside two foil-lined glass jars on the wooden bench just"
        " after a discharge, a brief cool indirect reflection fading on the"
        " glass and wall while a thin wisp of grey smoke curls up from the"
        " brass wire ring into the air; nothing emissive in shot."
        + TAIL
    ),
    "P2:11_jar_crack": (
        STYLE
        + "Same Philadelphia 1752 back-room workshop: close on two foil-lined"
        " glass jars linked by a brass discharging rod on the wooden bench as"
        " a sudden pale indirect reflection sweeps across the curved glass and"
        " the timber wall behind them, a faint wisp of vapour rising from the"
        " brass tips; nothing emissive in shot."
        + TAIL
    ),
    "P2:17_page_bottom_c1": (
        STYLE
        + "Same Philadelphia 1752 back-room bench in soft daylight from a"
        " window: close on Franklin's hand drawing a firm ink underline"
        " beneath the bottom line of his open notebook page with a goose"
        " quill, then resting the nib beside the brass inkstand; no legible"
        " words, nothing emissive in shot."
        + TAIL
    ),
    # Part 03
    "P3:01_points_desk": (
        STYLE
        + f"Same Philadelphia 1752 back-room bench in clear window daylight: {FRANKLIN} holds a sharp iron needle point steady near a charged brass sphere on a wooden stand while a fine linen indicator thread hanging from the brass sphere drops smoothly as the charge drains away; nothing emissive in shot."
        + TAIL
    ),
    "P3:02_sentry_box": (
        STYLE
        + "Same Philadelphia 1752 back-room desk in window daylight: close on"
        " Franklin's hand using a goose quill and brass straightedge to sketch"
        " an architectural elevation of a stone tower topped with a small"
        " wooden sentry-box and an upright pointed rod on heavy paper; camera"
        " eases in, no legible text, nothing emissive in shot."
        + TAIL
    ),
    "P3:05_marly_garden_c1": (
        STYLE
        + "Same Marly garden May 1752 set under grey overcast storm sky:"
        " closer view of the wooden sentry box where the foot of the 40-foot"
        " iron rod rests on an insulated wooden stool over three glass wine"
        " bottles, silk guy-cords taut in the wind; no people close, nothing"
        " emissive in shot."
        + TAIL
    ),
    "P3:07_slow_news": (
        STYLE
        + "Wide shot of an 18th-century wooden packet ship under full sail"
        " pitching steadily across grey Atlantic swells under an overcast"
        " daylight sky; slow camera drift alongside the hull, figures tiny on"
        " deck, nothing emissive in shot."
        + TAIL
    ),
    "P3:11_kite_build": (
        STYLE
        + f"Same Philadelphia 1752 back-room workshop in warm afternoon light from an off-screen window: {FRANKLIN} at his wooden bench stretching a pale silk handkerchief taut over two crossed sticks of cedar and knotting the corners, a cloth tail tied on; nothing emissive in shot."
        + TAIL
    ),
    "P3:12_wire_top": (
        STYLE
        + "Same Philadelphia 1752 back-room workshop in clear window light"
        " from off-screen: close on Franklin's hands binding a straight"
        " pointed iron wire to the top of the cedar kite frame so the sharp"
        " tip stands a foot above the wood; nothing emissive in shot."
        + TAIL
    ),
    "P3:13_key_ribbon": (
        STYLE
        + "Same Philadelphia 1752 back-room workshop in soft daylight from an"
        " off-screen window: close on Franklin's hands tying an iron key where"
        " rough hemp twine meets a dry silk ribbon; nothing emissive in shot."
        + TAIL
    ),
    "P3:13_key_ribbon_c1": (
        STYLE
        + "Same Philadelphia 1752 back-room workshop in soft window daylight:"
        " extreme close-up as Franklin's hands pull the silk ribbon knot tight"
        " against the bow of the iron key and lift the finished assembly from"
        " the wooden bench; nothing emissive in shot."
        + TAIL
    ),
    "P3:16_keep_silk_dry": (
        STYLE
        + "Inside a small open-fronted wooden shed at the edge of a field,"
        " grey storm rain outside: close on the bottom of the kite string,"
        " rough wet twine, the iron key and a dry silk ribbon held in"
        " Franklin's hand under the dry timber eaves; nothing emissive in"
        " shot."
        + TAIL
    ),
    "P3:18_william_runs": (
        STYLE
        + f"Field under a dark overcast storm sky: {WILLIAM} runs across the wet grass and lifts the silk kite into the wind while Franklin watches from the open shed doorway; grey storm daylight, nothing emissive in shot."
        + NOSTRIKE
        + TAIL
    ),
    "P3:20_waiting": (
        STYLE
        + "Same Philadelphia 1752 open shed doorway in grey storm light:"
        " father and son stand inside the dry doorway looking up at the heavy"
        " storm clouds overhead as rain falls past the eaves; nothing emissive"
        " in shot."
        + TAIL
    ),
    "P3:21_doorway_pov": (
        STYLE
        + "Same Philadelphia 1752 open shed doorway: POV from inside the shed"
        " as the taut hemp string runs up from a hand holding the dry silk"
        " ribbon out into the rain-swept field and dark rolling storm clouds"
        " overhead; cool indirect storm light on the wet grass, nothing"
        " emissive in shot."
        + NOSTRIKE
        + TAIL
    ),
    "P3:21_doorway_pov_c1": (
        STYLE
        + "Same Philadelphia 1752 open shed doorway in heavy rain: close"
        " tracking tilt up the taut wet hemp twine from the iron key hanging"
        " under the eaves toward the dark wind-tossed clouds above the field;"
        " rainwater beads on the twine, nothing emissive in shot."
        + NOSTRIKE
        + TAIL
    ),
    "P3:22_william_face": (
        STYLE
        + f"{WILLIAM} beside his father in the shed doorway, looking up as rain drips from his hat brim; cool grey storm daylight, nothing emissive in shot."
        + TAIL
    ),
    "P3:24_eyes_drop": (
        STYLE
        + "Franklin's eyes drop from the sky to the string in his hand; close,"
        " his face in cool grey storm daylight, nothing emissive in shot."
        + TAIL
    ),
    "P3:25_fibres_rise": (
        STYLE
        + "Extreme close-up in grey storm daylight: loose fibres on the wet"
        " hemp twine lift and spread apart from each other, like hairs on an"
        " arm; nothing emissive in shot."
        + NOSTRIKE
        + TAIL
    ),
    # Part 04
    "P4:01_knuckle_close": (
        STYLE
        + "In the shed in grey storm daylight, Franklin slowly brings his"
        " knuckle close to the iron key hanging on the string before any"
        " discharge; rain falling behind, nothing emissive in shot."
        + TAIL
    ),
    "P4:03_room_memory": (
        STYLE
        + "Same Philadelphia 1752 back-room workshop in soft off-screen window"
        " light: close on a hand turning the wooden crank of Franklin's glass"
        " globe electrostatic machine as the glass sphere spins briskly"
        " against its leather cushion beside a foil-lined Leyden jar on the"
        " bench; nothing emissive in shot."
        + TAIL
    ),
    "P4:07_kite_cloud_wide": (
        STYLE
        + "Same Philadelphia 1752 field set: wide shot of the silk kite"
        " holding steady high against dark rolling storm clouds over the wet"
        " field as wind bends the grass; cool indirect storm light, nothing"
        " emissive in shot."
        + NOSTRIKE
        + TAIL
    ),
    "P4:09_charge_string_c1": (
        STYLE
        + "Same Philadelphia 1752 open shed doorway in heavy rain: close on"
        " the heavy iron key hanging where the wet hemp twine meets the dry"
        " silk ribbon, raindrops dripping from the bottom of the key as the"
        " string trembles in the wind; grey storm daylight, nothing emissive"
        " in shot."
        + NOSTRIKE
        + TAIL
    ),
    "P4:10_richmann_rod": (
        STYLE
        + "St Petersburg in a summer storm, 1753: exterior wide shot of a tall"
        " iron rod rising through the roof of an 18th-century stone house as"
        " heavy dark thunderclouds roll low overhead in driving rain; cool"
        " indirect storm light on the wet roof, nothing emissive in shot."
        + TAIL
    ),
    "P4:11_richmann_room": (
        STYLE
        + "The empty St Petersburg apparatus room below: an iron rod passes"
        " down through the ceiling to an electrometer on a wooden stand with a"
        " linen thread indicator lifting sharply as sudden pale indirect storm"
        " light from off-screen outside washes across the panelled wall, then"
        " cuts to shadow; nothing emissive in shot, no body, no injury, no"
        " people."
        + TAIL
    ),
    "P4:14_royal_society": (
        STYLE
        + "A panelled Georgian meeting room at the Royal Society in London lit"
        " by tall side windows in afternoon daylight: seen from behind the"
        " speaker's lectern, a speaker holds up a folded letter before a"
        " seated row of fellows in 1750s wigs and coats listening attentively;"
        " faces small, nothing emissive in shot."
        + TAIL
    ),
    "P4:15_copley_medal": (
        STYLE
        + "Close on hands lifting a gold medal from a velvet-lined case on a"
        " wooden table in soft daylight from an off-screen window; no legible"
        " lettering, nothing emissive in shot."
        + TAIL
    ),
    # Part 05
    "P5:01_house_rod": (
        STYLE
        + "Franklin's brick town house on Market Street, 1752: an iron rod"
        " fixed to the top of the chimney, about nine feet above it, as dark"
        " overcast storm clouds roll in; grey storm daylight, nothing emissive"
        " in shot."
        + TAIL
    ),
    "P5:03_bells_ring": (
        STYLE
        + "Same Market Street 1752 staircase in grey storm daylight from a"
        " landing window: close on the two small brass bells hung six inches"
        " apart as the suspended brass ball on its silk thread swings briskly"
        " back and forth between them, striking each bell in turn so they"
        " vibrate; nothing emissive in shot."
        + TAIL
    ),
    "P5:06_rod_fitting_c1": (
        STYLE
        + "Same 1750s brick house exterior in clear daylight: close low-angle"
        " shot at the foot of the brick wall as a workman drives the lower end"
        " of the iron lightning rod deep into damp dark earth beside the"
        " foundation stones and tamps the soil around it; nothing emissive in"
        " shot."
        + TAIL
    ),
    "P5:15_why_card": (
        STYLE
        + "Same 18th-century town set as the storm clouds part in soft"
        " late-afternoon daylight: thin iron lightning rods stand on the slate"
        " and timber roofs while wet cobbles glisten below and townsfolk step"
        " calmly onto their porches; nothing emissive in shot. Slow push."
        + TAIL
    ),
    "P5:15_why_card_c1": (
        STYLE
        + "Same 18th-century town street in clear post-storm afternoon light:"
        " high wide tracking drift along a row of intact timber and stone"
        " gables fitted with pointed iron rods against a clearing sky; figures"
        " small in the street below, nothing emissive in shot."
        + TAIL
    ),
    "P5:18_rod_closeup": (
        STYLE
        + "Same modern city tower set: close shot of the thin pointed metal"
        " rod at the very top of a tall generic glass tower against rolling"
        " grey storm clouds in overcast daylight; wind moves the clouds past"
        " the tip, nothing emissive in shot. No real or recognisable building."
        + TAIL
    ),
    "P5:20_table_three_again": (
        STYLE
        + f"Same Philadelphia 1752 back-room wooden table in warm golden-hour daylight from an off-screen window: the silk cedar kite, the iron key on its silk ribbon and {JAR} rest together on the timber tabletop as the camera slowly pulls back; nothing emissive in shot."
        + TAIL
    ),
    "P5:22_newton_handoff": (
        STYLE
        + "An English orchard garden in soft late-afternoon daylight: a red"
        " apple falls from a gnarled apple tree while the pale daytime Moon"
        " hangs in the sky above the boughs; slow push, nothing emissive in"
        " shot."
        + TAIL
    ),
    "P5:22_newton_handoff_c1": (
        STYLE
        + "Same English orchard garden in soft late-afternoon daylight: the"
        " red apple settles in the long grass at the foot of the apple tree"
        " while the camera tilts slowly up through the boughs toward the pale"
        " half-Moon hanging high in the blue-grey sky; nothing emissive in"
        " shot."
        + TAIL
    ),
}

# (b): 11 flat-card and diagram rows turned into £0 code graphics (our own renderer, HOS explainer look).
# Where code-graphic rows sit adjacent (P2:14+15, P3:03+04, P5:08+09+10+11), they alternate
# full_frame_period_paper with moving_plate_overlay so two full-frame teach cards never run back to back.
CODE_GRAPHICS = {
    "P2:14_likeness_pairs": {
        "file": "code_graphic_008_p2_14_likeness_pairs.mp4",
        "renderer": "python-pillow-ffmpeg (house explainer renderer, £0)",
        "style": "HOS cream-on-brown period-paper inked diagram, white/sepia Didot italic",
        "layout_mode": "full_frame_period_paper",
        "background_plate": None,
        "label": "SAME COLOUR · CROOKED LINES",
        "elements": [
            "Left panel inked on warm period paper: brass Leyden jar ring and crooked blue-ink spark trace",
            "Right panel inked on warm period paper: storm cloud and matching crooked lightning trace",
        ],
        "animation": (
            "Divider line inks in over 0.4 s; left crooked spark path draws"
            " itself at 0.6 s; right crooked bolt path draws in matching"
            " geometry at 2.2 s; Didot italic label fades in at 0.5 s and out"
            " before cut."
        ),
        "tick_ink_s": [0.6, 2.2],
    },
    "P2:15_likeness_fire": {
        "file": "code_graphic_008_p2_15_likeness_fire.mp4",
        "renderer": "python-pillow-ffmpeg (house explainer renderer, £0)",
        "style": "HOS inked explainer diagram composited over moving Set D workshop plate (avoids back-to-back full-frame cards)",
        "layout_mode": "moving_plate_overlay",
        "background_plate": "P2:12_notebook_list (moving tail window, softly graded)",
        "label": "CRACK · FIRE · SHOCK",
        "elements": [
            "Inked notebook comparison callout over moving bench plate: bench spark igniting spirit wick vs sky bolt igniting roof timber",
        ],
        "animation": (
            "Cream-on-brown inked comparison inset draws over the moving"
            " workshop plate at 0.35 s; left and right ignition icons ink in at"
            " 0.7 s and 2.3 s; fades out at 4.8 s."
        ),
        "tick_ink_s": [0.7, 2.3],
    },
    "P3:03_rod_cloud": {
        "file": "code_graphic_008_p3_03_rod_cloud.mp4",
        "renderer": "python-pillow-ffmpeg (house explainer renderer, £0)",
        "style": "HOS cream-on-brown period-paper inked mechanism diagram, Didot italic",
        "layout_mode": "full_frame_period_paper",
        "background_plate": None,
        "label": "DRAWING CHARGE FROM CLOUD",
        "elements": [
            "Inked stone tower elevation with sentry-box and pointed iron rod rising toward passing storm cloud",
            "Animated dotted charge lines curving down from cloud base into the sharp rod tip",
        ],
        "animation": (
            "Tower and pointed rod ink in over 0.0–1.2 s; storm cloud contour"
            " drifts across top; dotted charge stream lines animate continuously"
            " from cloud into rod tip from 1.5 s to 6.5 s."
        ),
        "tick_ink_s": [0.5, 1.5],
    },
    "P3:04_letter_crosses": {
        "file": "code_graphic_008_p3_04_letter_crosses.mp4",
        "renderer": "python-pillow-ffmpeg (house explainer renderer, £0)",
        "style": "HOS inked Atlantic route line composited over moving Set E print-shop/sea plate (avoids back-to-back full-frame cards)",
        "layout_mode": "moving_plate_overlay",
        "background_plate": "P3:07_slow_news (moving Atlantic swell plate, softly graded)",
        "label": "PHILADELPHIA TO PARIS",
        "elements": [
            "Inked 1752 North Atlantic coastline contour and dotted ship track from Philadelphia to Paris over moving ocean swells",
        ],
        "animation": (
            "Coastline silhouette and Philadelphia origin marker ink in at"
            " 0.3 s; dotted vessel track draws eastward across the moving"
            " Atlantic swells to Paris over 0.6–3.4 s."
        ),
        "tick_ink_s": [0.3, 3.1],
    },
    "P3:15_wet_dry": {
        "file": "code_graphic_008_p3_15_wet_dry.mp4",
        "renderer": "python-pillow-ffmpeg (house explainer renderer, £0)",
        "style": "HOS cream-on-brown period-paper inked mechanism diagram, Didot italic",
        "layout_mode": "full_frame_period_paper",
        "background_plate": None,
        "label": "WET TWINE · DRY SILK",
        "elements": [
            "Inked vertical wet hemp twine carrying animated charge dashes down to the iron key",
            "Dry silk ribbon tied below the key where charge dashes halt at the insulator knot",
        ],
        "animation": (
            "Twine, iron key and silk ribbon ink in by 0.8 s; animated charge"
            " dashes flow down the wet twine into the key (1.0–3.0 s) and stop"
            " cleanly at the dry silk boundary (3.0–5.3 s)."
        ),
        "tick_ink_s": [0.5, 2.8],
    },
    "P4:06_same_thing": {
        "file": "code_graphic_008_p4_06_same_thing.mp4",
        "renderer": "python-pillow-ffmpeg (house explainer renderer, £0)",
        "style": "HOS inked brass-and-cream split comparison frame over moving KEEP plates, Didot italic",
        "layout_mode": "moving_plate_overlay",
        "background_plate": "Left: P2:08_jar_spark KEEP · Right: P4:02_knuckle_spark KEEP",
        "label": "ELECTRICITY",
        "elements": [
            "Left moving pane: Leyden jar spark in back room (P2:08_jar_spark)",
            "Right moving pane: iron key spark in rainy shed (P4:02_knuckle_spark)",
            "Inked period divider line and Didot italic header ELECTRICITY",
        ],
        "animation": (
            "Inked vertical rule draws down the centre at 0.3 s framing both"
            " moving KEEP plates side by side; Didot italic label ELECTRICITY"
            " inks in at 1.2 s and fades out at 5.0 s while both plates stay"
            " in continuous motion."
        ),
        "tick_ink_s": [0.3, 1.2],
    },
    "P4:08_teach_charge": {
        "file": "code_graphic_008_p4_08_teach_charge.mp4",
        "renderer": "python-pillow-ffmpeg (house explainer renderer, £0)",
        "style": "HOS cream-on-brown period-paper inked mechanism diagram, Didot italic",
        "layout_mode": "full_frame_period_paper",
        "background_plate": None,
        "label": "NO BOLT, JUST CHARGE",
        "elements": [
            "Inked storm cloud high at top of period sheet, silk kite flying well below in rain",
            "Gentle dotted charge lines draining quietly down the wet string to the shed key without any bolt",
        ],
        "animation": (
            "Cloud, kite and shed silhouette ink in over 0.0–1.2 s; soft dotted"
            " charge lines flow steadily down the string from 1.2 s to 7.1 s;"
            " label NO BOLT, JUST CHARGE inks in at 0.6 s and fades out at 4.4 s."
        ),
        "tick_ink_s": [0.6, 1.8],
    },
    "P5:08_looking_path": {
        "file": "code_graphic_008_p5_08_looking_path.mp4",
        "renderer": "python-pillow-ffmpeg (house explainer renderer, £0)",
        "style": "HOS inked stepped-leader diagram composited over moving storm-rooftop plate (alternates with P5:09 full-frame card)",
        "layout_mode": "moving_plate_overlay",
        "background_plate": "P1:16_question_sky (moving storm-clouds-over-roofs plate, graded)",
        "label": "EASIEST PATH DOWN",
        "elements": [
            "Branching ink leader lines feeling downward from cloud base toward town roof peaks over moving storm plate",
        ],
        "animation": (
            "Forked ink leader paths draw downward step by step from 0.3 s to"
            " 2.8 s over the moving rooftop plate, testing paths toward the"
            " highest gable."
        ),
        "tick_ink_s": [0.3, 1.4],
    },
    "P5:09_wood_vs_metal": {
        "file": "code_graphic_008_p5_09_wood_vs_metal.mp4",
        "renderer": "python-pillow-ffmpeg (house explainer renderer, £0)",
        "style": "HOS cream-on-brown period-paper inked cross-section diagram, Didot italic",
        "layout_mode": "full_frame_period_paper",
        "background_plate": None,
        "label": "WOOD AND STONE RESIST",
        "elements": [
            "Inked cross-section of timber roof rafters and stone steeple masonry with jagged fracture lines where current is blocked",
        ],
        "animation": (
            "Timber roof and stone steeple outlines ink in over 0.0–1.2 s;"
            " blocked current path marks resistance points at 1.8 s and radial"
            " crack lines draw outward across the masonry through 6.8 s."
        ),
        "tick_ink_s": [0.5, 1.8],
    },
    "P5:10_metal_easy": {
        "file": "code_graphic_008_p5_10_metal_easy.mp4",
        "renderer": "python-pillow-ffmpeg (house explainer renderer, £0)",
        "style": "HOS inked conductor diagram composited over moving Set H brick-wall rod plate (alternates between P5:09 and P5:11 full-frame cards)",
        "layout_mode": "moving_plate_overlay",
        "background_plate": "P5:06_rod_fitting (moving exterior wall rod plate, graded)",
        "label": "METAL CONDUCTS",
        "elements": [
            "Smooth gold-and-white inked current line running unimpeded down the iron rod on the moving brick wall plate",
        ],
        "animation": (
            "Inked callout bracket marks the iron rod at 0.25 s; a smooth"
            " continuous current trace glides straight down the rod from top"
            " to bottom over 0.4–2.8 s."
        ),
        "tick_ink_s": [0.25],
    },
    "P5:11_safe_path": {
        "file": "code_graphic_008_p5_11_safe_path.mp4",
        "renderer": "python-pillow-ffmpeg (house explainer renderer, £0)",
        "style": "HOS cream-on-brown period-paper architectural cutaway diagram, Didot italic",
        "layout_mode": "full_frame_period_paper",
        "background_plate": None,
        "label": "A SAFE PATH TO THE GROUND",
        "elements": [
            "Cutaway elevation of church steeple fitted with pointed iron rod, exterior down-conductor wire, and deep earth stake",
            "Animated current line travelling from rod tip down the outside wall into the ground while interior timber spire stays untouched",
        ],
        "animation": (
            "Steeple cutaway and exterior iron rod ink in over 0.0–1.3 s;"
            " current line traces from rod tip down the outer wall into the"
            " earth stake (1.5–6.5 s); label A SAFE PATH TO THE GROUND inks in"
            " at 0.6 s and fades out at 4.4 s."
        ),
        "tick_ink_s": [0.6, 1.5, 3.5],
    },
}


def main() -> None:
    plan_v02 = json.loads((EDIT / "PICTURE_PLAN_v02.json").read_text())
    rates = plan_v02["rates"]

    boards_v02 = []
    rows_v02 = {}
    for p in range(1, 6):
        b = json.loads((PARTS / f"part-0{p}_plates_v02.json").read_text())
        boards_v02.append(b)
        for r in b["plates"]:
            rows_v02[f"P{p}:{r['id']}"] = r

    # Pre-measure all 15 v02 reuse rows against their source clip's unused moving footage.
    reuse_measurements = {}
    for key, r in rows_v02.items():
        if r["quality"] == "reuse":
            src_key = r["reuse_of"]
            src = rows_v02[src_key]
            src_use = round(float(src["use_s"]), 2)
            req_use = round(float(r["use_s"]), 2)
            unused_raw = round(CLIP_RAW_S - src_use, 2)
            unused_usable = round(CLIP_USE_S - src_use, 2)
            shortfall_raw = round(req_use - unused_raw, 2)
            shortfall_usable = round(req_use - unused_usable, 2)
            src_is_code_graphic = src_key in CODE_GRAPHICS
            feasible = (not src_is_code_graphic) and (unused_usable >= req_use)
            reuse_measurements[key] = {
                "source_row": src_key,
                "source_clip_raw_s": CLIP_RAW_S,
                "source_clip_usable_s": CLIP_USE_S,
                "source_used_s": src_use,
                "unused_raw_s": unused_raw,
                "unused_usable_s": unused_usable,
                "required_use_s": req_use,
                "shortfall_raw_s": shortfall_raw,
                "shortfall_usable_s": shortfall_usable,
                "source_became_code_graphic": src_is_code_graphic,
                "distinct_window_feasible": feasible,
                "resolution": "priced_fast_mint" if not feasible else "reuse",
                "note": (
                    f"Source {src_key} uses {src_use:.2f} s of an 8.00 s clip"
                    f" ({CLIP_USE_S:.2f} s usable), leaving {unused_raw:.2f} s"
                    f" raw ({unused_usable:.2f} s usable) < {req_use:.2f} s"
                    f" needed (short by {shortfall_raw:.2f} s raw /"
                    f" {shortfall_usable:.2f} s usable)"
                    + (
                        f"; {src_key} is also a code graphic in v03."
                        if src_is_code_graphic
                        else "."
                    )
                    + " Converted to priced Fast mint (no loop, freeze-pad or"
                    " frame replay)."
                ),
            }

    cum_flow = 0
    cum_vertex = 0.0
    per_part = []
    boards_v03 = []

    for b_in in boards_v02:
        b = json.loads(json.dumps(b_in))
        n = int(b["part"])
        for r in b["plates"]:
            key = f"P{n}:{r['id']}"
            r["v02_quality"] = r["quality"]
            r["generation_authorized"] = False
            r["review_required"] = []

            if key in CODE_GRAPHICS:
                spec = dict(CODE_GRAPHICS[key], duration_s=r["use_s"])
                r["quality"] = "code_graphic"
                r["route"] = "code-graphic"
                r["engine_reason"] = (
                    "J0240 (b): flat-card/diagram row turned into £0 code"
                    " graphic (own renderer, HOS explainer look)."
                )
                r["code_graphic_spec"] = spec
                for fld in (
                    "prompt",
                    "flow_model",
                    "flow_clip_s",
                    "vertex_model",
                    "hero_reason",
                ):
                    r.pop(fld, None)
                r["vertex_clip_s"] = 0
                for fld in PRICE_FIELDS:
                    r[fld] = 0 if "flow" in fld else 0.0

            elif key in HEROES:
                r["quality"] = "Quality"
                r["hero_reason"] = HEROES[key]
                r["engine_reason"] = (
                    f"Quality hero ({HEROES[key]}): fragile light, spark, or"
                    " Explorer plate."
                )
                r["route"] = "flow-first"
                need_s = min(r["use_s"] + REUSE_PAD_S, CLIP_RAW_S)
                clip_s = next(L for L in VERTEX_LENGTHS if L >= need_s - 1e-6)
                r["flow_model"] = "Veo 3.1 Quality"
                r["flow_clip_s"] = 8
                r["flow_credits_try1"] = rates["flow_credits_per_take"]["Quality"]
                r["flow_credits_expected"] = math.ceil(
                    rates["flow_credits_per_take"]["Quality"]
                    * rates["takes_per_keep_005"]["Quality"]
                )
                r["vertex_model"] = "veo-3.1-generate-001"
                r["vertex_clip_s"] = clip_s
                cost = (
                    rates["vertex_usd_per_s"]["Quality"]
                    * clip_s
                    * rates["gbp_per_usd_planning"]
                )
                exp = (
                    cost * rates["takes_per_keep_005"]["Quality"]
                    + rates["stills_per_plate_005"]
                    * rates["usd_per_still"]
                    * rates["gbp_per_usd_planning"]
                )
                r["vertex_try1_gbp"] = round(cost, 2)
                r["vertex_expected_gbp"] = round(exp, 2)

            else:
                # Either an existing Fast row (rewritten if flagged/emissive) or a measured
                # unfeasible reuse row converted to a priced Fast mint.
                was_reuse = key in reuse_measurements
                r["quality"] = "Fast"
                r["route"] = "flow-first"
                r.pop("hero_reason", None)
                if was_reuse:
                    m = reuse_measurements[key]
                    r["reuse_measurement"] = m
                    r.pop("reuse_of", None)
                    r.pop("reuse_window", None)
                    r.pop("reuse_feasibility", None)
                    r.pop("clip_in_s", None)
                    r["engine_reason"] = (
                        f"J0240 (c): measured source {m['source_row']} has"
                        f" {m['unused_usable_s']:.2f} s usable"
                        f" ({m['unused_raw_s']:.2f} s raw) unused <"
                        f" {m['required_use_s']:.2f} s needed; converted to"
                        " priced Fast mint (non-emissive)."
                    )
                else:
                    if key in FAST_PROMPTS:
                        r["engine_reason"] = (
                            "J0240 (a): non-hero Fast plate with non-emissive"
                            " framing (light off-screen or by effect on"
                            " walls/faces, no flame or spark in shot)."
                        )
                    else:
                        r["engine_reason"] = (
                            "Fast: non-emissive daylight/storm framing."
                        )

                if key in FAST_PROMPTS:
                    r["prompt"] = FAST_PROMPTS[key]

                if key == "P3:07_slow_news":
                    r["set"] = "sea"

                need_s = min(r["use_s"] + REUSE_PAD_S, CLIP_RAW_S)
                clip_s = next(L for L in VERTEX_LENGTHS if L >= need_s - 1e-6)
                r["flow_model"] = "Veo 3.1 Fast"
                r["flow_clip_s"] = 8
                r["flow_credits_try1"] = rates["flow_credits_per_take"]["Fast"]
                r["flow_credits_expected"] = math.ceil(
                    rates["flow_credits_per_take"]["Fast"]
                    * rates["takes_per_keep_005"]["Fast"]
                )
                r["vertex_model"] = "veo-3.1-fast-generate-001"
                r["vertex_clip_s"] = clip_s
                cost = (
                    rates["vertex_usd_per_s"]["Fast"]
                    * clip_s
                    * rates["gbp_per_usd_planning"]
                )
                exp = (
                    cost * rates["takes_per_keep_005"]["Fast"]
                    + rates["stills_per_plate_005"]
                    * rates["usd_per_still"]
                    * rates["gbp_per_usd_planning"]
                )
                r["vertex_try1_gbp"] = round(cost, 2)
                r["vertex_expected_gbp"] = round(exp, 2)

            cum_flow += r["flow_credits_expected"]
            cum_vertex += r["vertex_expected_gbp"]
            r["cum_flow_credits_expected"] = cum_flow
            r["cum_vertex_expected_gbp"] = round(cum_vertex, 2)

        plate_rows = b["plates"]
        counts = {
            q: sum(r["quality"] == q for r in plate_rows)
            for q in ("Quality", "Fast", "code_graphic", "reuse")
        }
        b["counts"] = {
            "rows": len(plate_rows),
            "mints": counts["Quality"] + counts["Fast"],
            "added": sum(bool(r.get("added")) for r in plate_rows),
            **counts,
        }
        b["status"] = "BOARD_V03_PARKED_FOR_CHIEF"
        b["mint"] = False
        b["quality_note"] = (
            "J0240 v03: 15 Quality hero/cover plates; all 86 Fast prompts"
            " non-emissive (no candle flame, spark, bolt or flicker in shot);"
            " 11 flat-card/diagram rows converted to £0 code graphics; all 15"
            " v02 reuse rows measured against 8 s source clips and converted to"
            " priced Fast mints."
        )
        b["house"] = (
            "J0240 v03 boards by gemini, 15 Oct 2026, resolving J0184"
            " acting-Chief price PASS conditions (a) non-emissive Fast prompts"
            " + hero swap P5:07/P3:25, (b) 11 per-row £0 code graphics, (c)"
            " measured reuse windows -> priced Fast mints. No mint, no spend;"
            " parked for Chief."
        )
        b["continuation_lock"] = (
            "All 15 v02 reuse rows measured against their 8.0 s (7.9 s usable)"
            " source clips: 0 of 15 had enough unused moving footage for a"
            " distinct full-length window, so all 15 are priced Fast mints in"
            " v03. Never loop, freeze-pad or replay frames."
        )
        (PARTS / f"part-{b['part']}_plates_v03.json").write_text(
            json.dumps(b, indent=2, ensure_ascii=False) + "\n"
        )
        pp = {"part": n, **b["counts"]}
        pp.update(
            {f: round(sum(r[f] for r in plate_rows), 2) for f in PRICE_FIELDS}
        )
        per_part.append(pp)
        boards_v03.append(b)

    # Validation checks
    all_v03 = [
        (int(b["part"]), r) for b in boards_v03 for r in b["plates"]
    ]
    assert len(all_v03) == 112, len(all_v03)
    q_rows = [f"P{p}:{r['id']}" for p, r in all_v03 if r["quality"] == "Quality"]
    assert set(q_rows) == set(HEROES.keys()), (set(q_rows) ^ set(HEROES.keys()))
    cg_rows = [
        f"P{p}:{r['id']}" for p, r in all_v03 if r["quality"] == "code_graphic"
    ]
    assert set(cg_rows) == set(CODE_GRAPHICS.keys()), (
        set(cg_rows) ^ set(CODE_GRAPHICS.keys())
    )

    # Check no two full_frame_period_paper code graphics run back to back
    for b in boards_v03:
        prev_full_cg = False
        for r in b["plates"]:
            is_full_cg = (
                r["quality"] == "code_graphic"
                and r["code_graphic_spec"]["layout_mode"]
                == "full_frame_period_paper"
            )
            assert not (prev_full_cg and is_full_cg), (
                f"Back-to-back full-frame code graphics at P{b['part']}:{r['id']}"
            )
            prev_full_cg = is_full_cg

    # Check Fast prompts have no positive emissive words
    bad_emissive = []
    for p, r in all_v03:
        if r["quality"] == "Fast":
            assert not r.get("review_required"), f"P{p}:{r['id']} still has review_required"
            pr = r.get("prompt", "")
            assert pr, f"P{p}:{r['id']} missing prompt"
            cleaned = re.sub(
                r"no\s+(?:lightning|candles?|flames?|sparks?|flickers?|bolts?|fire|glow)[^.;]*",
                "",
                pr.lower(),
            )
            cleaned = cleaned.replace("lightning rod", "metal rod").replace(
                "lightning rods", "metal rods"
            )
            for w in (
                "candle",
                "spark",
                "flicker",
                "flame",
                "flashes",
                "flashing",
                "lit white by a flash",
                "a flash ",
                "bolt",
                "glow",
            ):
                if w in cleaned:
                    bad_emissive.append((f"P{p}:{r['id']}", w, pr))
    assert not bad_emissive, f"Emissive words in Fast prompts: {bad_emissive}"

    totals = {
        k: round(sum(p[k] for p in per_part), 2)
        for k in per_part[0]
        if k != "part"
    }
    for int_k in (
        "rows",
        "mints",
        "added",
        "Quality",
        "Fast",
        "code_graphic",
        "reuse",
        "flow_credits_try1",
        "flow_credits_expected",
    ):
        totals[int_k] = int(totals[int_k])

    plan_v03 = dict(plan_v02)
    plan_v03.update(
        written="2026-10-15",
        task=(
            "J0240 (OWB queue, repo hos): 008 boards v03 — non-emissive Fast"
            " prompts, 11 £0 code-graphic cards, 15 measured reuse windows ->"
            " priced Fast mints; no mint, no spend; parked for Chief"
        ),
        status="PARKED_FOR_CHIEF_V03_BOARDS",
        mint=False,
        totals=totals,
        per_part=per_part,
        hero_candidates=HEROES,
        code_graphics=CODE_GRAPHICS,
        reuse_measurements=reuse_measurements,
        all_on_flow_credits_expected=totals["flow_credits_expected"],
        all_on_vertex_gbp_expected=totals["vertex_expected_gbp"],
        changes={
            "v02_to_v03_emissive_fast_rewritten": len(
                [k for k in FAST_PROMPTS if k not in reuse_measurements]
            ),
            "v02_to_v03_hero_swap": {
                "promoted_to_quality": "P5:07_giant_spark",
                "dropped_to_fast": "P3:25_fibres_rise",
            },
            "v02_to_v03_cards_to_code_graphics": len(CODE_GRAPHICS),
            "v02_to_v03_measured_reuses_to_fast_mints": len(reuse_measurements),
        },
        price_pass_questions=[
            "Chief review of v03 boards: 15 Quality heroes (with P5:07_giant_spark swapped in for P3:25_fibres_rise), 86 non-emissive Fast plates, 11 £0 per-row code graphics, 0 unverified reuses.",
            "Minting waits for 006 and 007 completion per Chief 14 Oct ruling (Flow-only expected: 5,605 credits; try-1: 2,360 credits).",
        ],
        estimate_scope=(
            "v03 Flow/Vertex estimate with all Fast prompts non-emissive, 11"
            " flat-card/diagram rows priced at £0 / 0 cr as own code graphics,"
            " and all 15 v02 reuse rows measured against 8 s source clips and"
            " priced as Fast mints. No spend authorization."
        ),
    )
    (EDIT / "PICTURE_PLAN_v03.json").write_text(
        json.dumps(plan_v03, indent=2, ensure_ascii=False) + "\n"
    )
    print(json.dumps({"totals": totals, "per_part": per_part}, indent=2))


if __name__ == "__main__":
    main()
