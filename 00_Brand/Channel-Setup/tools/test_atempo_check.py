#!/usr/bin/env python3
"""Tests for atempo_check: what counts as speeding the voice above 1.06."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import atempo_check  # noqa: E402


class Py(unittest.TestCase):
    def values(self, src: str):
        return [v for _, v in atempo_check.scan_py(src)]

    def test_constant_over_cap(self):
        # 007 s04 v02, 26 Oct 2026: ATEMPO = 1.08 passed every gate
        self.assertEqual(self.values("ATEMPO = 1.08\n"), [1.08])

    def test_constant_fed_into_filter(self):
        # 002 four elements v02, 25 Oct 2026: OPEN_RATE = 1.40 fed into atempo={OPEN_RATE}
        src = 'OPEN_RATE = 1.40         # note\nf"atempo={OPEN_RATE:.5f}"\n'
        self.assertEqual(self.values(src), [1.4])

    def test_literal_in_filter_string(self):
        self.assertEqual(self.values('af = "atrim=0:2,atempo=1.12"\n'), [1.12])

    def test_dict_key_in_meta(self):
        self.assertEqual(self.values('meta = {"open_atempo": 1.4}\n'), [1.4])

    def test_at_or_under_cap_passes(self):
        self.assertEqual(self.values("ATEMPO = 1.06\nATEMPO_B = 1.00\n'atempo=1.05'\n"), [])

    def test_unrelated_constant_ignored(self):
        self.assertEqual(self.values("SCALE = 1.40\nf'scale={SCALE}'\n"), [])


class Json(unittest.TestCase):
    def test_nested_key_over_cap(self):
        self.assertEqual([v for _, v in atempo_check.scan_json('{"vo": {"atempo": 1.07}}')], [1.07])

    def test_under_cap_and_bad_json(self):
        self.assertEqual(atempo_check.scan_json('{"atempo": 1.03}'), [])
        self.assertEqual(atempo_check.scan_json("not json"), [])


if __name__ == "__main__":
    unittest.main()
