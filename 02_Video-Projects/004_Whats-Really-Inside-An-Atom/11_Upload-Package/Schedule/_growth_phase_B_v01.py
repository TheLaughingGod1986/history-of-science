#!/usr/bin/env python3
"""Ben growth Phase B — long GHZDsiH7L7A Studio finish (wrapper)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MOD = HERE / "_growth_settings_ben_2003_v01.py"


def main() -> None:
    spec = importlib.util.spec_from_file_location("growth_ben_2003", MOD)
    m = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(m)
    sys.argv = [str(MOD), "--phase", "B"]
    m.main()


if __name__ == "__main__":
    main()
