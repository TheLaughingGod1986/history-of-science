#!/usr/bin/env python3
"""HOS 005 Short B v03 VO fix (pale -> cold): re-voice one sentence (Ben's OK, 2 Oct 12:56) in the house voice.
Same voice/model/settings as 005 VO v01 (04_Audio/tools/orbit_voice.py: Ben Orbit Narrator, eleven_v3,
settings_for_part(1)). Auth: ELEVENLABS_API_KEY from HOS's own .env (the one the 005 VO generator loads:
History Of Science/.../001.../07_Edit-Project/.env). API key only, never printed; no browser tokens.
The sentence is voiced in context (previous + next sentence) and cut out using the timestamps."""
import base64, json, os, subprocess, sys
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

TEXT = ("William Harvey tied it tight round a man's arm. "
        "The hand went cold. "
        "No blood was getting in.")
token, mode = load_token(prefer_api_key=True)
assert mode == "api_key"
vs = settings_for_part(1)
print(f"voice={VOICE_NAME} {VOICE_ID} model={MODEL_ID} settings={vs}")
here = Path(__file__).parent
for take in sys.argv[1:]:
    out = here / f"s02_line_v03_ctx_{take}.mp3"
    if out.exists():
        print("exists", out.name); continue
    code, body, _ = request("POST", f"/v1/text-to-speech/{VOICE_ID}/with-timestamps", token, mode,
                            data={"text": TEXT, "model_id": MODEL_ID, "voice_settings": vs},
                            query="output_format=mp3_44100_128", accept="application/json", timeout=300)
    if code != 200:
        raise SystemExit(f"TTS failed {code}: {body[:300]!r}")
    p = json.loads(body.decode())
    out.write_bytes(base64.b64decode(p["audio_base64"]))
    (here / f"s02_line_v03_ctx_{take}_align.json").write_text(json.dumps(p.get("alignment") or {}))
    print("SAVED", out.name)
