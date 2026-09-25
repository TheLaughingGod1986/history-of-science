#!/usr/bin/env python3
import faulthandler, os, sys, traceback
from pathlib import Path
faulthandler.enable(all_threads=True)
log = Path(__file__).resolve().parent / "logs" / "mint_part04_v06_desk_wrap.log"
log.parent.mkdir(exist_ok=True)
# truncate
log.write_text("")
class Tee:
    def __init__(self, path):
        self.f = open(path, "a", buffering=1)
        self.out = sys.__stdout__
    def write(self, s):
        self.out.write(s); self.out.flush(); self.f.write(s); self.f.flush()
        return len(s)
    def flush(self):
        self.out.flush(); self.f.flush()
sys.stdout = Tee(log)
sys.stderr = sys.stdout
print("WRAP start pid", os.getpid(), flush=True)
try:
    import runpy
    sys.argv = ["_mint_part04_flow_v06.py", "02b_cards_sixty_three"]
    runpy.run_path(str(Path(__file__).resolve().parent / "_mint_part04_flow_v06.py"), run_name="__main__")
    print("WRAP exit ok", flush=True)
except SystemExit as e:
    print("WRAP SystemExit", e.code, flush=True)
    raise
except BaseException:
    traceback.print_exc()
    print("WRAP crash", flush=True)
    raise
