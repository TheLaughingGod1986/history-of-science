#!/usr/bin/env python3
"""HOS 005 v02 'pale' fix (desk 5952762841, Ben 2 Oct 14:05): re-voice ONE sentence in context, house voice.
Same voice/model as 005 VO v01 (04_Audio/tools/orbit_voice.py, eleven_v3, Ben Orbit Narrator).
Auth: ELEVENLABS_API_KEY from HOS's own .env; never printed.
  python gen_line_v02.py <outdir> <prefix> <settings_part> "<context text>" a b c"""
import base64, json, os, sys
from pathlib import Path
REPO = Path.home() / "YouTube/hos-005-blood"
sys.path.insert(0, str(REPO / "04_Audio/tools"))
HOS_ENV = Path.home() / "YouTube/History Of Science/02_Video-Projects/001_How-Did-We-Discover-Germs/07_Edit-Project/.env"
for line in HOS_ENV.read_text().splitlines():
    if line.startswith("ELEVENLABS_API_KEY="):
        os.environ["ELEVENLABS_API_KEY"] = line.split("=", 1)[1].strip().strip('"').strip("'")
from el_auth import load_token
from el_client import request
from orbit_voice import MODEL_ID, VOICE_ID, VOICE_NAME, settings_for_part
outdir, prefix, part, TEXT, *takes = sys.argv[1:]
outdir = Path(outdir)
token, mode = load_token(prefer_api_key=True)
assert mode == "api_key"
vs = settings_for_part(int(part))
print(f"voice={VOICE_NAME} {VOICE_ID} model={MODEL_ID} settings={vs}")
for take in takes:
    out = outdir / f"{prefix}_{take}.mp3"
    if out.exists():
        print("exists", out.name); continue
    code, body, _ = request("POST", f"/v1/text-to-speech/{VOICE_ID}/with-timestamps", token, mode,
                            data={"text": TEXT, "model_id": MODEL_ID, "voice_settings": vs},
                            query="output_format=mp3_44100_128", accept="application/json", timeout=300)
    if code != 200:
        raise SystemExit(f"TTS failed {code}: {body[:300]!r}")
    p = json.loads(body.decode())
    out.write_bytes(base64.b64decode(p["audio_base64"]))
    (outdir / f"{prefix}_{take}_align.json").write_text(json.dumps(p.get("alignment") or {}))
    print("SAVED", out.name)
