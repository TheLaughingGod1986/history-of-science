#!/usr/bin/env python3
"""Native Gemini Veo API generator for JWST Orbit clips.

Uses shared helper: 04_Audio/tools/orbit_gemini_veo.py

ElevenLabs Image & Video (Omni/Veo) is LEGACY. Native Gemini Veo is the default CG path.
VO remains ElevenLabs Ben Orbit Narrator.

Auth: GEMINI_API_KEY in env or Edit-Project/.env

Examples:
  export GEMINI_API_KEY=...
  python _generate_veo_gemini_api_v01.py --probe
  python _generate_veo_gemini_api_v01.py --from-reject
  python _generate_veo_gemini_api_v01.py --pass p4 --scene 07 --beat C
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "004_JWST-Discoveries-That-Change-Everything"
)
EDIT = ROOT / "07_Edit-Project"
RAW = ROOT / "04_Generated-Clips/01_Raw"
REJECTED = ROOT / "04_Generated-Clips/_Rejected/orbit-gemini-api-preregen"
QA_REJECT = EDIT / "ORBIT_CHARACTER_QA_REJECT.json"
LOG = ROOT / "03_Animation-Prompts/03_Generation-Logs/jwst_veo_gemini_api_v01.jsonl"
ENV_FILE = EDIT / ".env"
OMNI = EDIT / "_generate_omni_v01.py"

TOOLS = Path("/Users/ben/code/Orbit-YouTube/04_Audio/tools")
sys.path.insert(0, str(TOOLS))
import orbit_gemini_veo as veo  # noqa: E402


def load_omni():
    spec = importlib.util.spec_from_file_location("omni_v01", OMNI)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def dest_for(pass_id: str, scene: str, beat: str, slug: str) -> Path:
    if pass_id == "p0":
        return RAW / f"scene-{scene}" / f"p0_{beat}_{slug}_gemini-omni-flash_v01_raw.mp4"
    return RAW / f"scene-{scene}" / f"{pass_id}_{beat}_{slug}_gemini-omni-flash_v02_raw.mp4"


def beat_prompt_map(omni) -> dict[tuple[str, str], tuple[str, str]]:
    out = {}
    for scene, beat, slug, prompt in omni.load_beats():
        out[(scene, beat)] = (slug, prompt)
    return out


def quarantine(path: Path) -> Path | None:
    if not path.exists():
        return None
    REJECTED.mkdir(parents=True, exist_ok=True)
    dest = REJECTED / f"{path.stem}__{int(time.time())}{path.suffix}"
    shutil.move(str(path), str(dest))
    print(f"quarantined → {dest.name}", flush=True)
    return dest


def log_rec(rec: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps(rec) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--from-reject", action="store_true")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--pass", dest="pass_id", default="")
    ap.add_argument("--scene", default="")
    ap.add_argument("--beat", default="")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--skip-existing", action="store_true")
    ap.add_argument("--no-quarantine", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    omni = load_omni()
    prompts = beat_prompt_map(omni)

    if args.probe:
        targets = [("p0", "03", "C", "push-into-webb-window")]
    elif args.from_reject:
        data = json.loads(QA_REJECT.read_text())
        targets = [
            (row["pass"], row["scene"], row["beat"], row["slug"])
            for row in (data.get("reject") or [])
        ]
    elif args.pass_id and args.scene and args.beat:
        slug = prompts[(args.scene, args.beat)][0]
        targets = [(args.pass_id, args.scene, args.beat, slug)]
    else:
        ap.error("Use --probe, --from-reject, or --pass/--scene/--beat")

    if args.limit > 0:
        targets = targets[: args.limit]

    queue = []
    for pass_id, scene, beat, slug in targets:
        key = (scene, beat)
        if key not in prompts:
            print(f"SKIP unknown beat {scene}{beat}", flush=True)
            continue
        real_slug, base = prompts[key]
        slug = real_slug
        dest = dest_for(pass_id, scene, beat, slug)
        prompt = veo.build_prompt(base, pass_id=pass_id)
        queue.append((pass_id, scene, beat, slug, prompt, dest))

    print(f"queue {len(queue)} clips · model={veo.DEFAULT_MODEL}", flush=True)
    print(f"Orbit start+ASSET ref: {veo.ORBIT_REF.name}", flush=True)
    if args.dry_run:
        for pass_id, scene, beat, slug, prompt, dest in queue:
            print(f"  {pass_id} {scene}{beat} {slug} → {dest.name} ({len(prompt)} chars)")
        return

    client = veo.make_client(ENV_FILE)
    ok = fail = 0
    for i, (pass_id, scene, beat, slug, prompt, dest) in enumerate(queue, 1):
        print(f"\n=== [{i}/{len(queue)}] {pass_id} scene-{scene} {beat} {slug} ===", flush=True)
        if args.skip_existing and veo.already_done(dest):
            print("SKIP existing", flush=True)
            ok += 1
            continue
        if not args.no_quarantine:
            quarantine(dest)
        try:
            meta = veo.generate_clip(client, prompt, dest)
            eiffel = omni.reject_eiffel_startframe(dest)
            if eiffel:
                raise RuntimeError(f"Eiffel QA: {eiffel}")
            rec = {
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "pass": pass_id,
                "scene": scene,
                "beat": beat,
                "slug": slug,
                "file": str(dest),
                **meta,
            }
            log_rec(rec)
            print(f"SAVED {dest.name} ({meta['bytes']}) in {meta['seconds']}s", flush=True)
            ok += 1
        except Exception as e:
            fail += 1
            print(f"FAIL {pass_id} {scene}{beat}: {e}", flush=True)
            log_rec(
                {
                    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "pass": pass_id,
                    "scene": scene,
                    "beat": beat,
                    "slug": slug,
                    "error": str(e),
                    "engine": "gemini-api-veo",
                }
            )
            if fail >= 3:
                print("ABORT: 3 failures", flush=True)
                break

    print(f"\ndone ok={ok} fail={fail} log→{LOG}", flush=True)
    if fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
