# vo_check_py312 — Mini pin (4 Oct 2026)

## Problem
Default `python3` on the Mac mini is **3.14**. With **PyAV 19**, `faster_whisper` crashes:

`TypeError: open() got an unexpected keyword argument 'metadata_errors'`

## Fix (this branch)
1. Homebrew `python@3.12`
2. Venv: `History Of Science/.venv_vo_check_py312` (local; not committed)
3. Pins: `faster-whisper` + **`av==13.1.0`**
4. Wrapper: `00_Brand/Channel-Setup/tools/vo_check_py312.sh` → runs `vo_check.py` on that venv

## Run
```bash
"./00_Brand/Channel-Setup/tools/vo_check_py312.sh" <audio.mp3> --script <script.md> [--part N] [--json]
```

## Out of scope
- Do not merge without Claude PASS
- Do not edit AGENTS.md / playbook / Never list from this stand-in PR
- Optional follow-up: guard in `vo_check.py` if TypeError mentions `metadata_errors`

## Desk note
`~/_desk/handoff/vo_check_py312_pin_20261004.md`
