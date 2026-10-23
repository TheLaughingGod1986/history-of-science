#!/usr/bin/env python3
"""HOS standalone Shorts S1-S4: purpose-built 9:16 still plates on Vertex gemini-2.5-flash-image (J0203).

Chief ruling (HOS #180 re 6131173528): option (a), stills only, no Flow, no Veo. Assembly moves them
with a gentle push. Uses 006's Vertex client (project gen-lang-client-0538779324, ADC). Tokens are
never printed. Media stays out of git (jpg is gitignored); the log and prompts are tracked.

  ~/.venvs/hos-vertex/bin/python docs/STANDALONE_SHORTS_TEST_2026-10/_mint_plates_v01.py --budget-gbp 0.90 [--only s1] [--dry-run]

--budget-gbp is the lag-aware usable figure from 006 `_vertex_credit_v01.py` minus any margin; the run
refuses any still that would take logged spend past it.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OUT = HERE / "plates_v01"
LOG = HERE / "PLATES_MINT_LOG_v01.json"
MINT_006 = REPO / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/_mint_vertex_v01.py"
STYLE_REF = REPO.parent / ("hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/"
                           "04_Generated-Clips/part01/refs/v02_vertex_stills/03_band_tightens_v02.jpg")
USD_PER_STILL = 0.039
GBP_PER_USD = 0.80

STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon, finished materials, "
    "warm cinematic light. Not photoreal, not flat 2D. Vertical 9:16 frame with the key subject "
    "in the centre band. No text, letters, numbers, labels, captions, signs, logos or UI anywhere. "
    "No orange robot. No boy explorer character. No DNA helix. No gore."
)

PLATES = {
    "s1": [
        ("01_beyond_red", "A glass thermometer with a blackened bulb lying on a wooden table in the dark "
         "just beyond the red edge of a rainbow spectrum, its red liquid column rising. Mysterious, "
         "the hook frame."),
        ("02_prism_window", "William Herschel, an 18th-century astronomer in a powdered wig and dark coat, "
         "in his English study in 1800, holding a glass prism in a beam of sunlight from a shuttered "
         "window; a bright rainbow spectrum falls across his table."),
        ("03_thermometers_colours", "Close on a wooden table: a vivid rainbow spectrum from a prism, with "
         "three glass thermometers laid in the violet, green and red bands, red liquid columns at "
         "different heights."),
        ("04_past_the_red", "Herschel's hand sliding one thermometer off the red end of the spectrum into "
         "the dark part of the table, leaning in closely, candle-free study lit only by the sunbeam."),
        ("05_invisible_glow", "The same table in the dark beyond the red band, shown with a soft warm "
         "invisible-heat shimmer rising past the red, the thermometer column at its highest. Wonder."),
    ],
    "s2": [
        ("01_glowing_flask", "A glass flask in a dark 17th-century alchemist's workshop, holding a white "
         "substance glowing pale green-white, lighting the room. The hook frame."),
        ("02_hamburg_lab", "Hennig Brand, a 17th-century Hamburg alchemist with a beard and a leather "
         "apron, in his cluttered stone workshop in 1669, large copper vats steaming over a furnace."),
        ("03_black_sludge", "Close on a glass retort over coals, boiled down to thick black sludge, "
         "smoke curling, Brand peering in hopefully."),
        ("04_no_gold", "Brand holding up an empty iron crucible by the furnace, disappointed: no gold, "
         "only dull residue."),
        ("05_first_glow", "In the dark workshop, a white waxy substance in a glass dish glowing eerie "
         "green-white, Brand's astonished face lit by its glow."),
    ],
    "s3": [
        ("01_broad_street_pump", "A black cast-iron Victorian street water pump with a long handle on a "
         "misty cobbled London street in 1854, ominous, the hook frame."),
        ("02_soho_1854", "A crowded Soho street in 1854, Victorian Londoners in shawls and top hats, "
         "worried faces, foggy air, brick terraces."),
        ("03_snow_tracking", "Dr John Snow, a Victorian physician with sideburns and a dark frock coat, "
         "walking a Soho street with a notebook, looking at house doors."),
        ("04_map_bars", "A hand-drawn Victorian street map on a desk, with small black bars clustered "
         "around one pump symbol in the middle; no lettering or numbers on the map at all."),
        ("05_handle_off", "The cast-iron street pump with its handle removed, Dr John Snow standing beside "
         "it holding the detached handle, a calm Soho street."),
    ],
    "s4": [
        ("01_lead_box", "An open lead-lined box in a quiet archive, holding a stack of old 1890s "
         "laboratory notebooks with worn covers, a faint eerie blue-green glow. The hook frame."),
        ("02_shed_lab", "Marie Curie and Pierre Curie in 1898 in their cramped wooden shed laboratory in "
         "Paris, glass beakers and an iron cauldron, working side by side."),
        ("03_glowing_vials", "Small glass vials on a wooden bench in the dark, glowing faint blue-green "
         "with radium, softly lighting the lab."),
        ("04_bare_hands", "Marie Curie at her bench holding a glowing glass vial in her bare hands, no "
         "gloves, calm and absorbed, warm lab light."),
        ("05_paris_archive", "A grand Paris library archive with rows of lead-lined boxes on shelves, a "
         "reader in protective gloves lifting a notebook. Quiet, awe."),
    ],
    # J0214: S5-S8 from SCRIPTS_v01 picture notes as amended by SCRIPTS_v02 (S5 VO kept "blamed on pigeons").
    # S7 and S8 run 4 plates and loop to 01 (Vertex trial balance £0.70 at 22:23Z; 18 stills keeps ≥ £0.10).
    "s5": [
        ("01_pigeons_horn", "Two grey pigeons flapping out of the open mouth of a huge horn-shaped metal "
         "radio antenna on a grassy New Jersey hill in 1964, the horn like a giant square ear trumpet on a "
         "rotating mount. The hook frame."),
        ("02_receiver_needle", "Two 1960s radio astronomers in shirt sleeves, Arno Penzias with dark hair and "
         "glasses and Robert Wilson, tall and lean, at a bank of receiver equipment with glowing valve "
         "panels, watching an analogue needle tremble on a dial with a blank face. Puzzled."),
        ("03_nests_inside", "Inside the giant metal horn antenna, looking down its tapering throat: twigs of "
         "pigeon nests and white droppings on the riveted aluminium floor, one pigeon perched. Soft daylight."),
        ("04_still_noise", "The same two radio astronomers at the receiver, the analogue needle still "
         "trembling on its blank dial, both leaning in, baffled, a broom propped against the rack."),
        ("05_every_direction", "The giant horn antenna on its hill at night, turned up to a starry sky; the "
         "whole sky glows with a faint, even, warm microwave haze from every direction. Wonder."),
    ],
    "s6": [
        ("01_mouldy_dish", "A cluttered 1920s laboratory bench with stacks of round glass culture dishes, "
         "one dish on top with a fuzzy blue-green mould spreading across it. The hook frame."),
        ("02_back_from_holiday", "Alexander Fleming, a 1920s Scottish scientist with a bow tie and white lab "
         "coat over a suit, back from holiday in his small London lab, sorting through a pile of old glass "
         "culture dishes by the window."),
        ("03_fuzzy_mould", "Close on one round glass culture dish held up to window light: a fuzzy "
         "blue-green mould colony on pale yellow bacteria."),
        ("04_clear_ring", "Close on the glass culture dish: a clear empty ring all around the fuzzy mould "
         "where the yellow bacteria colonies have vanished, the rest of the dish dotted with colonies."),
        ("05_medicine_bottles", "Rows of small 1940s glass medicine vials with plain blank labels on a "
         "pharmacy shelf in warm light, hopeful."),
    ],
    "s7": [
        ("01_candle_jar", "A candle flame shrinking to almost nothing inside an upturned glass jar standing "
         "in a dish of water on an 18th-century wooden bench, a wisp of smoke curling. The hook frame."),
        ("02_priestley_jar", "Joseph Priestley, an 18th-century English minister and scientist in a "
         "powdered wig and dark coat, at his wooden bench in 1771 lowering an upturned glass jar over a "
         "lit candle standing in a dish of water."),
        ("03_mint_sprig", "Priestley's hands slipping a fresh green sprig of mint under the rim of the "
         "upturned glass jar standing in water, the candle inside burnt out."),
        ("04_candle_bright", "A fresh candle burning bright and tall inside the upturned glass jar beside a "
         "healthy green sprig of mint, standing in water on the wooden bench. Quiet triumph."),
    ],
    "s8": [
        ("01_tall_tube", "A very tall upright glass tube against a weathered wooden barn wall in the "
         "18th century, a red column already rising high inside it. The hook frame. No blood outside the tube."),
        ("02_hales_sketch", "Stephen Hales, an 18th-century English country vicar in a black clerical coat, "
         "white bands at the collar and a short grey wig, at a desk by a window sketching a heart with a "
         "quill. No writing visible."),
        ("03_calm_mare", "A calm chestnut mare standing in a straw-filled barn, a thin brass pipe joined to "
         "a very tall glass tube rising up the barn wall beside her. No wound, no procedure, no blood visible."),
        ("04_taller_than_man", "Stephen Hales, a country vicar in a black clerical coat and short grey wig, "
         "standing in the barn looking up in wonder at the very tall glass tube whose red column rises "
         "well above his head. No blood outside the tube."),
    ],
}

# J0214 face lock: a later plate takes the named earlier plate (same Short, this run's version) as Image 2.
LOCKS = {
    ("s5", "04_still_noise"): ("02_receiver_needle", "Arno Penzias and Robert Wilson"),
    ("s6", "03_fuzzy_mould"): ("02_back_from_holiday", "Alexander Fleming"),
    ("s7", "03_mint_sprig"): ("02_priestley_jar", "Joseph Priestley"),
    ("s8", "04_taller_than_man"): ("02_hales_sketch", "Stephen Hales"),
}

# Chief FAIL retakes (HOS #180 6131411243): one v02 each. Brand plates take S2-02 as the face/wardrobe lock.
BRAND_REF = OUT / "s2" / "02_hamburg_lab_v01.jpg"
BRAND_LOCK = ("Hennig Brand must be the SAME man as in Image 2: the same bearded face, age and hair, the same "
              "brown leather apron and clothes, no glasses. ")
RETAKES = {
    "s1": [
        ("05_invisible_glow", "The same wooden table in the dark just beyond the red edge of a rainbow "
         "spectrum, the thermometer's red column at its highest. The invisible heat is shown only as a "
         "very soft warm glow and a faint clear air shimmer over the dark strip. No smoke, no trails, no "
         "embers, no sparks, no flame. Quiet wonder."),
    ],
    "s2": [
        ("03_black_sludge", BRAND_LOCK + "Close on a glass retort over glowing coals, boiled down to thick "
         "black sludge, Brand leaning in behind it, peering hopefully."),
        ("04_no_gold", BRAND_LOCK + "Brand by his furnace holding up an empty iron crucible, disappointed: "
         "no gold, only dull residue."),
        ("05_first_glow", BRAND_LOCK + "In the dark workshop, a white waxy substance in a glass dish "
         "glowing eerie green-white, Brand's astonished face lit from below by its glow."),
    ],
    "s3": [
        ("05_handle_off", "A black cast-iron Victorian street water pump on a calm Soho street in 1854 with "
         "its handle completely removed: the pump body has only a bare stub where the handle was, nothing "
         "attached. Dr John Snow, Victorian physician with sideburns and a dark frock coat, stands beside "
         "it holding the long detached iron handle in both hands. Only one handle in the picture."),
    ],
    # Chief AMEND after watch (HOS #180 6132241581): v01 had malformed gloved hands; no people at all.
    "s4": [
        ("05_paris_archive", "A grand, quiet Paris library archive with tall wooden shelves of dark "
         "lead-lined boxes receding down a long vaulted aisle, one box on a reading table in the foreground "
         "with an old 1890s laboratory notebook lying closed beside it, a faint blue-green glow at its edges. "
         "No people, no hands, no gloves, no figures anywhere in the frame. Soft warm light. Quiet, awe."),
    ],
    # Chief FAIL (HOS #180 22:34Z): v01 kept the candle lit and copied 02's framing (J0215).
    "s7": [
        ("03_mint_sprig", "Tight close-up at bench height, not a wide shot: Joseph Priestley's hands in dark "
         "coat cuffs slipping a fresh green sprig of mint under the rim of an upturned glass jar that stands "
         "in a shallow dish of water. Inside the jar the candle has burnt OUT: a short stub with a black, "
         "unlit wick and one thin wisp of grey smoke. NO flame, no glow, no fire anywhere in the frame. "
         "Priestley's face only partly in soft focus above. Quiet, curious."),
    ],
}

# Chief's last-take ruling (HOS #180 6131594106): bare pump only, no person, nothing held.
RETAKES_V03 = {
    "s3": [
        ("05_handle_off", "A black cast-iron Victorian street water pump standing alone on wet cobbles on a "
         "calm, empty Soho street in 1854. The pump has NO handle at all: on its side there is only a short "
         "bare iron stub with a bolt hole where the handle used to be. No person in the frame, no hands, "
         "nothing held, no loose handle anywhere. Soft morning light, quiet relief."),
    ],
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_006():
    spec = importlib.util.spec_from_file_location("mint006", MINT_006)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_log() -> dict:
    if LOG.exists():
        return json.loads(LOG.read_text())
    return {"job": "J0203", "model": "gemini-2.5-flash-image", "usd_per_still": USD_PER_STILL,
            "gbp_per_usd": GBP_PER_USD, "stills": []}


def to_vertical(data: bytes, dest: Path) -> None:
    tmp = dest.with_suffix(".bin")
    tmp.write_bytes(data)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(tmp),
                    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                    "-frames:v", "1", "-q:v", "2", str(dest)], check=True)
    tmp.unlink(missing_ok=True)


def prompt_for(desc: str) -> str:
    return f"Finished 3D cartoon still for a vertical history-of-science Short. {desc} {STYLE}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget-gbp", type=float, required=True)
    ap.add_argument("--only", choices=sorted(PLATES))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--retake", action="store_true", help="mint Chief's FAIL retakes as _v02")
    ap.add_argument("--retake-v03", action="store_true", help="mint Chief's last-take ruling as _v03")
    a = ap.parse_args()

    log = load_log()
    ver = "v03" if a.retake_v03 else "v02" if a.retake else "v01"
    table = RETAKES_V03 if a.retake_v03 else RETAKES if a.retake else PLATES
    done = {(s["short"], s["plate"]) for s in log["stills"] if s.get("ok") and s.get("ver", "v01") == ver}
    todo = [(k, pid, d) for k, rows in table.items() if not a.only or k == a.only
            for pid, d in rows if (k, pid) not in done]
    run_gbp = 0.0
    per = USD_PER_STILL * GBP_PER_USD
    print(f"{len(todo)} stills to mint, ~£{len(todo) * per:.2f}; budget £{a.budget_gbp:.2f}")
    if a.dry_run:
        for k, pid, d in todo:
            print(f"  {k}/{pid}: {prompt_for(d)[:110]}…")
        return 0

    m = load_006()
    from google.genai import types
    c = m.client()
    ref = m.img_part(STYLE_REF) if STYLE_REF.exists() else None
    for k, pid, d in todo:
        if run_gbp + per > a.budget_gbp:
            print(f"STOP: next still would pass the £{a.budget_gbp:.2f} budget (run £{run_gbp:.2f})")
            break
        dest = OUT / k / f"{pid}_{ver}.jpg"
        dest.parent.mkdir(parents=True, exist_ok=True)
        text = prompt_for(d)
        parts = []
        if ref:
            parts.append(ref)
            text = ("Image 1 shows this channel's locked look only: match its 3D cartoon material, finish "
                    "and warm light. Do NOT copy its room, people, objects or any text. " + text)
        if a.retake and k == "s2" and BRAND_REF.exists():
            parts.append(m.img_part(BRAND_REF))
            text = ("Image 2 is the character lock for Hennig Brand only (face, beard, age, apron). " + text)
        lock = LOCKS.get((k, pid))
        lock_ref = OUT / k / f"{lock[0]}_{ver}.jpg" if lock else None
        if lock_ref and not lock_ref.exists():
            lock_ref = OUT / k / f"{lock[0]}_v01.jpg"
        if lock and lock_ref.exists():
            parts.append(m.img_part(lock_ref))
            text = (f"Image 2 is the character lock for {lock[1]}: the SAME face, hair, age and clothes as in "
                    "Image 2. Do not copy its framing. " + text)
        parts.append(text)
        print(f"STILL {k}/{pid} {ver}", flush=True)
        entry = {"short": k, "plate": pid, "ver": ver, "at": now(), "prompt": text, "cost_usd": USD_PER_STILL,
                 "job": "J0215" if a.retake and k == "s7" else "J0214" if k in ("s5", "s6", "s7", "s8")
                 else log.get("job", "J0203")}
        try:
            r = m.with_retry(lambda: c.models.generate_content(
                model="gemini-2.5-flash-image", contents=parts,
                config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                                                   image_config=types.ImageConfig(aspect_ratio="9:16"))),
                f"{k}/{pid}")
        except Exception as e:  # noqa: BLE001
            entry.update(ok=False, error=str(e)[:200])
            log["stills"].append(entry)
            LOG.write_text(json.dumps(log, indent=2) + "\n")
            print(f"  FAIL {str(e)[:160]}")
            continue
        run_gbp += per
        data = None
        for cand in r.candidates or []:
            for part in (cand.content.parts if cand.content else []) or []:
                if part.inline_data and part.inline_data.data:
                    data = part.inline_data.data
        if not data:
            entry.update(ok=False, error="no image returned (billed)")
        else:
            to_vertical(data, dest)
            entry.update(ok=True, file=str(dest.relative_to(REPO)))
        log["stills"].append(entry)
        LOG.write_text(json.dumps(log, indent=2) + "\n")
    billed = sum(s["cost_usd"] for s in log["stills"] if s.get("ok") or "billed" in s.get("error", ""))
    print(f"run £{run_gbp:.2f}; job total ${billed:.3f} (≈£{billed * GBP_PER_USD:.2f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
