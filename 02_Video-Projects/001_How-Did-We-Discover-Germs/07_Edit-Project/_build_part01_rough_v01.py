#!/usr/bin/env python3
"""History of Science Episode 001 — Part 01 rough (cold open + Invisible Enemy).

Animistry-class 3D cartoon · Explorer sparse (1 of ~10 plates).
Requires GEMINI_API_KEY + ELEVENLABS_API_KEY in .env (gitignored).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

from orbit_gemini_veo import (  # noqa: E402
    DEFAULT_MODEL,
    already_done,
    load_dotenv,
    make_client,
    strip_audio,
)
from orbit_voice import (  # noqa: E402
    CG_SILENT_AUDIO_BLOCK,
    MODEL_ID,
    VOICE_ID,
    VOICE_SETTINGS,
)

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips" / "part01" / "raw"
VO_PATH = PROJ / "02_Voiceover" / "part01_invisible_enemy_v01.mp3"
REF = REPO / "01_Character" / "05_Generation-References" / "hos-explorer-reference-v01.jpg"
MICROBE_REF = PROJ / "04_Generated-Clips" / "part01" / "refs" / "faceless_microbes_ref_v01.jpg"
META_PATH = PROJ / "07_Edit-Project" / "part01_gen_meta_v04.json"
PLATES_JSON = PROJ / "07_Edit-Project" / "parts" / "part-01_omni_plates_v04.json"
REJECTED = PROJ / "04_Generated-Clips" / "part01" / "_rejected_smiling_v01"
OUT = PROJ / "09_Final-Export" / "hos_001_part01_rough_v04.mp4"

CLIP_USE_S = 7.2
XFADE = 0.4

EXPLORER_LOCK = (
    "CRITICAL CHARACTER IDENTITY — match the attached reference exactly: "
    "young boy Explorer, messy wavy brown hair, round thin gold wire-rim glasses, "
    "teal-blue long overcoat with gold atom lapel pin, tan waistcoat, white shirt, "
    "dark brown floppy bow tie, brown trousers rolled at cuffs, cream socks, "
    "sturdy brown lace-up boots, brown leather satchel with brass compass, "
    "rolled parchment map in coat pocket. Premium 3D cartoon feature-animation "
    "polish, soft cinematic light, stylised materials — NOT photoreal, NOT flat 2D cel."
)

NEGATIVE = (
    "Orbit orange robot, floating robot, black visor mascot, Eiffel Tower, Paris, "
    "photoreal live action, horror, gore, blood, open wounds, readable UI chrome, "
    "watermark, logo overlay, dialogue, speech, talking, narrator, lip sync, "
    "twin Explorers, clone, duplicate boy, second explorer, text on screen, "
    "smiling germs, winking microbes, cute faces on bacteria, anthropomorphic germs, "
    "cartoon eyes on microbes, friendly mascot germs, kawaii germs, "
    "swarm of hundreds of germs, thick cloud of microbes filling the whole frame"
)

STYLE = (
    "Premium 3D cartoon animated film style like high-end feature animation, "
    "warm scholarly Victorian hospital palette, soft cinematic light, continuous "
    "camera motion through the final frame. " + CG_SILENT_AUDIO_BLOCK
)

# Ben lock 26 Aug 2026: germs are the enemy — wondrous science forms, never cute faces.
# Early Part 01: HUMAN WARD FIRST — few/no germs until the “invisible enemy” line.
MICROBE_LOCK = (
    "MICROBE VISUAL LOCK (HARD): blank scientific rods and spheres only — translucent "
    "teal/amber glass-like forms. NO faces, NO eyes, NO mouths, NO smiles. "
    "SPARSE: only a few microbes (about 3–8), not a room-filling swarm. "
    "Slightly ominous invisible enemy."
)

PATIENT_LOCK = (
    "Two patients maximum in frame, tasteful 3D cartoon illness — pale faces, tired "
    "eyes, feverish stillness under white sheets. NO gore, NO blood, NO open wounds, "
    "NO corpses. Family-friendly but clearly sick and ill."
)

VO_TEXT = (
    "What if the cleanest hospital corridor still killed you? "
    "Soft lamps. White sheets. Order everywhere — and still, people die in the beds "
    "behind the curtains. "
    "What if the air itself were crowded with invisible life — and nobody in the room "
    "could see it? "
    "Would you trust a doctor who washed nothing between patients? Would you survive "
    "a surgery that looked successful on paper, then turned septic by morning? "
    "What happens when medicine looks civilised… and still loses? "
    "We climb inside the moment science invented a new enemy: germs. Not ghosts. "
    "Not curses. Tiny living things — and the stubborn proof that flipped medicine forever. "
    "The smell is soap and sweat and fear. Doctors move with confidence. Hands that have "
    "just left one body arrive at the next. Instruments shine — and still, fever rises. "
    "Why does order fail? Because the danger is not the dirt you can see. It is a living "
    "cloud too small for the naked eye — microbes sharing your atmosphere, riding breath, "
    "cloth, fingers, knives. "
    "So how do you fight an enemy that does not cast a shadow? First, someone has to "
    "prove it exists."
)

# Ben 26 Aug 2026: fewer germs in first minutes; Explorer walks past sick patients in beds.
PLATES = [
    {
        "id": "01_ward_open_patients",
        "explorer": False,
        "force": True,
        "prompt": (
            f"{STYLE} {PATIENT_LOCK} Strange cold-open: Victorian hospital ward, soft lamps, "
            "brass beds — TWO sick patients resting ill in bed (pale, feverish, still). "
            "NO microbes visible yet. Human stakes first. Continuous slow push into the ward."
        ),
    },
    {
        "id": "02_clean_corridor",
        "explorer": False,
        "prompt": (
            f"{STYLE} Long clean Victorian hospital corridor, polished wood floor, soft "
            "wall lamps, white curtains in the distance, orderly and peaceful. No people. "
            "No microbes. Continuous slow dolly down the corridor toward the light."
        ),
    },
    {
        "id": "03_two_ill_patients",
        "explorer": False,
        "force": True,
        "prompt": (
            f"{STYLE} {PATIENT_LOCK} Medium shot along a row of brass beds: exactly two "
            "patients looking sick and ill under white sheets — one restless with fever, "
            "one very still and pale. Curtains, warm lamps. NO microbes. NO gore. "
            "Continuous gentle camera drift past the beds."
        ),
    },
    {
        "id": "04_explorer_walks_past_beds",
        "explorer": True,
        "force": True,
        "optional": True,
        "prompt": (
            f"{STYLE} {EXPLORER_LOCK} {PATIENT_LOCK} The Explorer walks slowly past brass "
            "hospital beds, satchel at his side, glancing with quiet concern at TWO sick "
            "patients in bed — then continues down the aisle so the ward stays the story. "
            "Single Explorer only. NO microbes. Continuous walking motion."
        ),
    },
    {
        "id": "05_doctor_hands_instruments",
        "explorer": False,
        "prompt": (
            f"{STYLE} Close cinematic 3D cartoon shot of Victorian doctor hands and "
            "gleaming metal surgical instruments on a tray under warm lamp light — "
            "confident, polished, slightly ominous. No microbes. Continuous "
            "subtle orbit of the tray."
        ),
    },
    {
        "id": "06_fever_patient",
        "explorer": False,
        "force": True,
        "prompt": (
            f"{STYLE} {PATIENT_LOCK} One ill patient in bed — soft red-orange fever glow "
            "under white sheets, thermometer on a side table, worried stillness. "
            "Tasteful cartoon illness only. NO microbes. NO gore. Continuous slow push-in."
        ),
    },
    {
        "id": "07_sparse_microbes_hint",
        "explorer": False,
        "force": True,
        "microbe_ref": True,
        "prompt": (
            f"{STYLE} {MICROBE_LOCK} Late reveal: over an empty patch of ward air, only a "
            "HANDFUL (about 5) of faceless glowing microbial rods/spheres drift like "
            "dangerous dust — sparse, not a swarm. Background ward soft. Continuous motion."
        ),
    },
    {
        "id": "08_hands_between_patients",
        "explorer": False,
        "force": True,
        "prompt": (
            f"{STYLE} {PATIENT_LOCK} Victorian doctor hands leave one curtained bed with a "
            "sick patient and move toward a second ill patient nearby — no washing bowl. "
            "Human transmission beat. NO microbe swarm; at most a tiny faceless sparkle "
            "or none. Continuous tracking with the hands."
        ),
    },
    {
        "id": "09_sparse_microbes_close",
        "explorer": False,
        "force": True,
        "microbe_ref": True,
        "prompt": (
            f"{STYLE} {MICROBE_LOCK} Macro of a FEW (3–6) faceless scientific rods and "
            "spheres tumbling slowly — educational, slightly ominous, never cute. "
            "Not a packed galaxy of germs. Continuous gentle tumble."
        ),
    },
    {
        "id": "10_ward_hold_patients",
        "explorer": False,
        "force": True,
        "prompt": (
            f"{STYLE} {PATIENT_LOCK} Wide hold on the Victorian ward: lamps, curtains, "
            "TWO ill patients still in bed — quiet question hanging. NO microbe swarm. "
            "Continuous slow pull-back."
        ),
    },
]


def resolve_keys() -> None:
    for p in (
        REPO / "04_Audio" / "tools" / ".env",
        PROJ / "07_Edit-Project" / ".env",
        REPO / ".env",
    ):
        load_dotenv(p)


def _is_quota(err: Exception) -> bool:
    s = str(err)
    return "429" in s or "RESOURCE_EXHAUSTED" in s or "quota" in s.lower()


def gen_plate(client, plate: dict, dest: Path, model: str, *, retries: int = 3) -> dict:
    from google.genai import types

    if already_done(dest):
        print(f"  skip existing {dest.name}", flush=True)
        return {"skipped": True, "bytes": dest.stat().st_size}

    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            img = None
            if plate.get("explorer"):
                img = types.Image.from_file(location=str(REF))
            elif plate.get("microbe_ref") and MICROBE_REF.exists():
                # Start from faceless still so Veo doesn't invent cute smiles.
                img = types.Image.from_file(location=str(MICROBE_REF))
            config = types.GenerateVideosConfig(
                number_of_videos=1,
                duration_seconds=8,
                aspect_ratio="16:9",
                resolution="720p",
                negative_prompt=NEGATIVE,
            )
            print(
                f"  submit {plate['id']} explorer={plate.get('explorer')} "
                f"microbe_ref={bool(plate.get('microbe_ref') and MICROBE_REF.exists())} "
                f"attempt={attempt}/{retries}",
                flush=True,
            )
            t0 = time.time()
            kwargs = dict(model=model, prompt=plate["prompt"], config=config)
            if img is not None:
                kwargs["image"] = img
            operation = client.models.generate_videos(**kwargs)
            while not operation.done:
                time.sleep(12)
                operation = client.operations.get(operation)
                print(f"  poll {plate['id']} … {int(time.time() - t0)}s", flush=True)
            if operation.error:
                raise RuntimeError(operation.error)
            response = operation.response
            if not response or not response.generated_videos:
                raise RuntimeError(f"no video for {plate['id']}")
            video = response.generated_videos[0]
            dest.parent.mkdir(parents=True, exist_ok=True)
            client.files.download(file=video.video)
            video.video.save(str(dest))
            strip_audio(dest)
            return {
                "seconds": round(time.time() - t0, 1),
                "bytes": dest.stat().st_size,
                "attempt": attempt,
            }
        except Exception as e:
            last_err = e
            print(f"  FAIL {plate['id']} attempt={attempt}: {e}", flush=True)
            sleep_s = (90 * attempt) if _is_quota(e) else (20 * attempt)
            print(f"  backoff {sleep_s}s…", flush=True)
            time.sleep(sleep_s)
    raise RuntimeError(f"{plate['id']} failed after {retries} attempts: {last_err}")


def maybe_vo() -> Path | None:
    token = os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVEN_API_KEY")
    if not token:
        print("No ELEVENLABS_API_KEY — assembling picture-only.", flush=True)
        return None
    VO_PATH.parent.mkdir(parents=True, exist_ok=True)
    if VO_PATH.exists() and VO_PATH.stat().st_size > 10_000:
        print(f"VO exists {VO_PATH}", flush=True)
        return VO_PATH
    payload = {
        "text": VO_TEXT,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS,
    }
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        data=json.dumps(payload).encode(),
        headers={
            "xi-api-key": token,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        VO_PATH.write_bytes(r.read())
    print(f"VO saved {VO_PATH} ({VO_PATH.stat().st_size} bytes)", flush=True)
    return VO_PATH


def assemble(clips: list[Path], vo: Path | None) -> None:
    n = len(clips)
    if n < 2:
        raise SystemExit("need ≥2 clips")
    inputs: list[str] = []
    for c in clips:
        inputs += ["-i", str(c)]
    if vo:
        inputs += ["-i", str(vo)]

    parts = []
    for i in range(n):
        parts.append(
            f"[{i}:v]trim=0:{CLIP_USE_S},setpts=PTS-STARTPTS,"
            f"scale=1280:720:force_original_aspect_ratio=decrease,"
            f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p[v{i}]"
        )
    vprev = "v0"
    offset = CLIP_USE_S - XFADE
    for i in range(1, n):
        out = f"vx{i}"
        parts.append(
            f"[{vprev}][v{i}]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}[{out}]"
        )
        vprev = out
        offset += CLIP_USE_S - XFADE

    pic_dur = n * CLIP_USE_S - (n - 1) * XFADE
    filter_complex = ";".join(parts)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", filter_complex]
    if vo:
        afilter = (
            f"[{n}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
            f"atrim=0:{pic_dur:.3f},apad=whole_dur={pic_dur:.3f}[a]"
        )
        cmd[-1] = filter_complex + ";" + afilter
        cmd += [
            "-map", f"[{vprev}]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-shortest",
            "-movflags", "+faststart", str(OUT),
        ]
    else:
        cmd += [
            "-map", f"[{vprev}]", "-an",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-movflags", "+faststart", str(OUT),
        ]
    print("ffmpeg assemble…", flush=True)
    subprocess.run(cmd, check=True)
    print(f"SAVED {OUT} ({OUT.stat().st_size} bytes) ~{pic_dur:.1f}s", flush=True)


def main() -> None:
    resolve_keys()
    if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
        raise SystemExit("Missing GEMINI_API_KEY")
    if not REF.exists():
        raise SystemExit(f"Missing Explorer ref: {REF}")

    PLATES_JSON.parent.mkdir(parents=True, exist_ok=True)
    PLATES_JSON.write_text(json.dumps(PLATES, indent=2))

    model = os.environ.get("ORBIT_VEO_MODEL", DEFAULT_MODEL)
    client = make_client()
    meta = {"model": model, "plates": [], "part": "01"}
    paths: list[Path] = []
    RAW.mkdir(parents=True, exist_ok=True)

    vo = maybe_vo()
    REJECTED.mkdir(parents=True, exist_ok=True)

    for plate in PLATES:
        ver = "v04" if plate.get("force") else "v01"
        dest = RAW / f"{plate['id']}_{ver}.mp4"
        try:
            info = gen_plate(client, plate, dest, model)
            meta["plates"].append({"id": plate["id"], "ver": ver, **info, "path": str(dest)})
            paths.append(dest)
        except Exception as e:
            if plate.get("optional") or plate.get("force"):
                print(f"  SKIP {plate['id']}: {e}", flush=True)
                meta["plates"].append({"id": plate["id"], "skipped": True, "error": str(e)})
                # Fallback: keep prior corridor/hands plates if named the same id+v01
                fallback = RAW / f"{plate['id']}_v01.mp4"
                if fallback.exists():
                    paths.append(fallback)
                continue
            raise

    # Assemble in narrative id order (Explorer mid-act), not generation order.
    def plate_sort_key(p: Path) -> str:
        name = p.stem
        for suffix in ("_v04", "_v03_stillbridge", "_v03", "_v02", "_v01"):
            if name.endswith(suffix):
                return name[: -len(suffix)]
        return name

    # Prefer highest version per id
    best: dict[str, Path] = {}
    rank = {"v04": 4, "v03_stillbridge": 3, "v03": 3, "v02": 2, "v01": 1}
    for p in paths:
        key = plate_sort_key(p)
        suf = p.stem[len(key) + 1 :] if p.stem.startswith(key + "_") else "v01"
        if key not in best or rank.get(suf, 0) >= rank.get(best[key].stem[len(key) + 1 :], 0):
            best[key] = p
    paths = [best[i] for i in sorted(best.keys())]

    if len(paths) < 2:
        raise SystemExit(f"Need ≥2 plates to assemble; only have {len(paths)}")

    assemble(paths, vo)
    meta["out"] = str(OUT)
    meta["vo"] = str(vo) if vo else None
    META_PATH.write_text(json.dumps(meta, indent=2))
    # copy artifact for easy review
    art = Path("/opt/cursor/artifacts")
    art.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        subprocess.run(["cp", "-f", str(OUT), str(art / OUT.name)], check=False)
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
