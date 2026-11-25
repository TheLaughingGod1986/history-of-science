"""HOS 011 Anaesthesia pass-1 Flow mint runner & v04 plan tests (J3736).

All tests run offline against local fixtures. They never open Chrome/CDP,
never click Create on a real page, and spend 0 credits (£0).
"""
from __future__ import annotations

import ast
import importlib.util
import inspect
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
EDIT = ROOT / "02_Video-Projects/011_Surgery-Before-Anaesthesia/07_Edit-Project"
SCRIPT = EDIT / "_mint_flow_v01_pass1.py"
BUILDER = EDIT / "_build_picture_plan_v04.py"
RUNNER_013_PATH = ROOT / "02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project/_mint_flow_v01_pass1.py"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


RUNNER = _load("hos011_pass1_runner", SCRIPT)
BUILD = _load("hos011_plan_v04_builder", BUILDER)
RUNNER_013 = _load("hos013_pass1_ref_for_011", RUNNER_013_PATH)


def make_png(dest: Path, *, width: int = 1280, height: int = 720, color: str = "0x335577") -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-i", f"color=c={color}:s={width}x{height}",
            "-frames:v", "1", str(dest),
        ],
        check=True,
    )
    return dest


def make_silent_mp4(dest: Path, *, width: int = 1280, height: int = 720, duration: int = 8) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-i", f"color=c=0x224466:s={width}x{height}:d={duration}:r=25",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", str(dest),
        ],
        check=True,
    )
    return dest


class PlanAndPromptAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = json.loads((EDIT / "PICTURE_PLAN_v04.json").read_text())
        cls.scope = json.loads((EDIT / "PASS1_SCOPE_J3736.json").read_text())
        cls.audit = json.loads((EDIT / "PROMPT_AUDIT_v04.json").read_text())
        cls.rows = RUNNER.load_scope(ROOT)

    def test_exact_93_rows_67_mint_26_free_zero_overlap_and_zero_consecutive_graphics(self):
        rows = self.plan["rows"]
        self.assertEqual(len(rows), 93)
        self.assertEqual(self.plan["totals"]["mint_rows"], 67)
        self.assertEqual(self.plan["totals"]["mint_quality"], 67)
        self.assertEqual(self.plan["totals"]["mint_fast"], 0)
        self.assertEqual(self.plan["totals"]["code_graphic"], 13)
        self.assertEqual(self.plan["totals"]["free_archive"], 13)
        self.assertEqual(self.plan["totals"]["existing_plate_reuse"], 0)
        self.assertEqual(self.plan["totals"]["flow_credits_try1"], 6700)
        self.assertEqual(self.plan["totals"]["post_cutover_hybrid_try1"], 886)
        self.assertEqual(self.plan["totals"]["post_cutover_lp_hybrid_try1"], 696)
        self.assertFalse(self.plan["generation_authorized"])
        self.assertFalse(self.scope["generation_authorized"])
        self.assertTrue(all(r["generation_authorized"] is False for r in rows))

        # Verify P5:16b is a dedicated moving plate between P5:16a and P5:17_cream_end_card.
        self.assertEqual(rows[-3]["row_id"], "P5:16a")
        self.assertEqual(rows[-3]["source_kind"], "code_graphic")
        self.assertEqual(rows[-2]["row_id"], "P5:16b_closing_watch_and_globe")
        self.assertEqual(rows[-2]["source_kind"], "mint_quality")
        self.assertIsNone(rows[-2]["reuses_row"])
        self.assertEqual(rows[-2]["duration_s"], 4.52)
        self.assertEqual(rows[-1]["row_id"], "P5:17_cream_end_card")
        self.assertEqual(rows[-1]["source_kind"], "code_graphic")

        # Continuous timeline and zero consecutive full-frame graphics.
        for prev, nxt in zip(rows, rows[1:]):
            self.assertAlmostEqual(prev["out_s"], nxt["in_s"], places=6)
            self.assertFalse(
                prev["source_kind"] in ("code_graphic", "free_archive")
                and nxt["source_kind"] in ("code_graphic", "free_archive"),
                f"consecutive full-frame graphics: {prev['row_id']} -> {nxt['row_id']}",
            )

    def test_all_67_prompts_pass_name_dna_text_and_stage_direction_checks(self):
        self.assertEqual(len(self.rows), 67)
        self.assertEqual(self.audit["summary"]["mint_rows_audited"], 67)
        self.assertEqual(self.audit["summary"]["real_person_name_hits"], 0)
        self.assertEqual(self.audit["summary"]["forbidden_dna_hits"], 0)
        self.assertEqual(self.audit["summary"]["text_request_hits"], 0)
        self.assertEqual(self.audit["summary"]["leaked_stage_direction_hits"], 0)
        self.assertEqual(self.audit["summary"]["cleanups_applied_from_v03"], 6)
        for row in self.rows:
            res = BUILD.audit_prompt(row.row_id, row.prompt)
            self.assertTrue(res["ok"], f"prompt audit failed on {row.row_id}: {res}")
        # Confirm P1:01b no longer contains the leaked 'Why?' quote.
        p1_01b = next(r for r in self.rows if r.row_id == "P1:01b")
        self.assertNotIn("Why?", p1_01b.prompt)
        self.assertNotIn("Title question", p1_01b.prompt)

    def test_scope_order_and_batches(self):
        self.assertEqual(self.rows[0].row_id, "P1:01a")
        self.assertEqual(self.rows[-1].row_id, "P5:16b_closing_watch_and_globe")
        batches = RUNNER.batch_rows(self.rows)
        self.assertEqual(len(batches), 14)
        self.assertEqual([len(b) for b in batches], [5] * 13 + [2])
        self.assertEqual(sum(sum(r.try1_credits for r in b) for b in batches), 6700)

    def test_v03_remains_valid_and_immutable(self):
        res = subprocess.run(
            [sys.executable, str(EDIT / "validate_retime_v03.py")],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("PASS:", res.stdout)


class RunnerGuardTests(unittest.TestCase):
    def test_fast_refused_everywhere(self):
        for bad in ("Fast", "Veo 3.1 - Fast", "Veo 3.1 Fast"):
            with self.assertRaisesRegex(RUNNER.GuardError, "Fast is refused"):
                RUNNER.expected_model_for(bad)
            with self.assertRaisesRegex(RUNNER.GuardError, "Fast is refused"):
                RUNNER.expected_credits_for(bad)

    def test_retired_quality_refused_on_or_after_5_dec_2026(self):
        RUNNER.assert_model_not_retired("Veo 3.1 - Quality", today=date(2026, 12, 4))
        with self.assertRaisesRegex(RUNNER.GuardError, "retired on 2026-12-05"):
            RUNNER.assert_model_not_retired("Veo 3.1 - Quality", today=date(2026, 12, 5))

    def test_headroom_and_floor_3000(self):
        # Live balance 23,450 - 800 liability - 6,700 cap = 15,950 >= 3,000 -> PASS.
        left = RUNNER.headroom(23450, spent=0, pending=0, other=800, floor=3000)
        self.assertEqual(left, 15950)
        # Insufficient balance below floor 3000 -> REFUSED.
        with self.assertRaisesRegex(RUNNER.GuardError, "headroom"):
            RUNNER.headroom(9600, spent=0, pending=0, other=800, floor=3000)

    def test_writer_lock_refuses_concurrent_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            lock_path = Path(tmp) / "writer.lock"
            with RUNNER.WriterLock(lock_path):
                with self.assertRaisesRegex(RUNNER.GuardError, "writer lock held"):
                    with RUNNER.WriterLock(lock_path):
                        pass

    def test_shared_accounting_reserve_intent_resolve_posted_and_floor(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "shared"
            with RUNNER.SharedFlowAccounting(state) as acct:
                # 23450 - 6700 = 16750 >= 3000 -> allowed
                acct.reserve("HOS011_PASS1", "HOS:011", 6700, live=23450, floor=3000)
                acct.intent("HOS:011:P01:01a:t1", "HOS011_PASS1", 100, live=23450, floor=3000)
                acct.resolve("HOS:011:P01:01a:t1", submitted=True, evidence={"ui": {"balances": [23450]}})
                acct.reconcile_posted("HOS:011:P01:01a:t1", evidence={"after": 23350, "delta": 100})
                snap = acct.snapshot()
                self.assertEqual(snap["remaining_reservations"], 6600)
                self.assertEqual(snap["unposted"], 0)
                self.assertFalse(snap["pending"])
                # Low balance below floor 3000 -> refused
                with self.assertRaisesRegex(RUNNER.GuardError, "headroom"):
                    acct.intent("HOS:011:P01:01b:t1", "HOS011_PASS1", 100, live=9000, floor=3000)

    def test_unarmed_submit_and_generation_authorized_false_refused(self):
        # 1) CLI submit without env var -> refused
        env = {k: v for k, v in os.environ.items() if k != RUNNER.SUBMIT_ENV}
        res = subprocess.run(
            [sys.executable, str(SCRIPT), "submit"],
            capture_output=True, text=True, env=env, check=False,
        )
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("not armed", res.stderr)

        # 2) Even with HOS011_PASS1_SUBMIT=1, generation_authorized=false in scope -> refused!
        env_armed = {**env, RUNNER.SUBMIT_ENV: "1"}
        res2 = subprocess.run(
            [sys.executable, str(SCRIPT), "submit", "--repo", str(ROOT), "--other-reservations", "0", "--media", "/tmp"],
            capture_output=True, text=True, env=env_armed, check=False,
        )
        self.assertNotEqual(res2.returncode, 0)
        self.assertIn("generation_authorized is false", res2.stderr)

        # 3) Direct helpers refuse when unarmed
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop(RUNNER.SUBMIT_ENV, None)
            with self.assertRaisesRegex(RUNNER.GuardError, "not armed"):
                RUNNER.live_batch_price_reader()
            row0 = RUNNER.load_scope(ROOT)[0]
            with self.assertRaisesRegex(RUNNER.GuardError, "not armed"):
                RUNNER.live_still_maker(row0, Path("/tmp/x.png"), repo=ROOT, media=Path("/tmp"))
            with self.assertRaisesRegex(RUNNER.GuardError, "not armed"):
                RUNNER.live_video_submit(
                    row0, Path("/tmp/x.mp4"), Path("/tmp/x.png"),
                    accounting=RUNNER.SharedFlowAccounting(Path("/tmp/none")),
                    reservation="HOS011_PASS1", charge="c1", evidence_path=Path("/tmp/ev.json"),
                )

    def test_live_balance_verification(self):
        class FakePage:
            def __init__(self, payload):
                self.payload = payload
            def evaluate(self, _js, _arg):
                return self.payload

        # Wrong host rejected
        with self.assertRaisesRegex(RUNNER.GuardError, "ULTRA"):
            RUNNER.read_live_balance(FakePage({"host": "evil.example", "accounts": [], "balances": [23450], "ultra": True}), open_overlay=False)
        # Valid studio digest accepted via accept_account
        now = datetime.now(timezone.utc)
        got = RUNNER.accept_account(RUNNER.REQUIRED_ACCOUNT_SHA256, now.isoformat(timespec="seconds"), now=now)
        self.assertEqual(got, RUNNER.REQUIRED_ACCOUNT_SHA256)
        with self.assertRaisesRegex(RUNNER.GuardError, "studio Ultra account"):
            RUNNER.accept_account(RUNNER.FORBIDDEN_ACCOUNT_SHA256, now.isoformat(timespec="seconds"), now=now)

    def test_scope_drift_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "AGENTS.md").write_text("# test\n")
            edit = repo / RUNNER.EDIT_REL
            (edit / "parts").mkdir(parents=True)
            shutil.copy2(EDIT / "PICTURE_PLAN_v04.json", edit / "PICTURE_PLAN_v04.json")
            shutil.copy2(EDIT / "PASS1_SCOPE_J3736.json", edit / "PASS1_SCOPE_J3736.json")
            for p in range(1, 6):
                shutil.copy2(EDIT / "parts" / f"part-0{p}_plates_v04.json", edit / "parts" / f"part-0{p}_plates_v04.json")
            # Tamper with one prompt on part 1 board
            b1_path = edit / "parts/part-01_plates_v04.json"
            b1 = json.loads(b1_path.read_text())
            b1["plates"][0]["prompt"] += " tampered"
            b1_path.write_text(json.dumps(b1))
            with self.assertRaisesRegex(RUNNER.GuardError, "hash mismatch"):
                RUNNER.load_scope(repo)

    def test_cli_plan_outputs_67_rows_and_zero_spend(self):
        res = subprocess.run(
            [sys.executable, str(SCRIPT), "plan", "--repo", str(ROOT)],
            capture_output=True, text=True, check=True,
        )
        data = json.loads(res.stdout)
        self.assertEqual(data["film"], "HOS:011")
        self.assertEqual(data["row_count"], 67)
        self.assertEqual(data["quality_count"], 67)
        self.assertEqual(data["fast_count"], 0)
        self.assertEqual(data["submissions"], 0)
        self.assertEqual(data["create_clicks"], 0)
        self.assertEqual(data["credits_spent"], 0)
        self.assertFalse(data["generation_authorized"])
        self.assertEqual(data["caps"]["floor"], 3000)
        self.assertEqual(len(data["batches"]), 14)

    def test_spend_destination_boundary_matches_013(self):
        for fn in ("active_spend_repository", "require_active_spend_destination", "canonical_spend_ledger"):
            src_011 = ast.dump(ast.parse(inspect.getsource(getattr(RUNNER, fn))))
            src_013 = ast.dump(ast.parse(inspect.getsource(getattr(RUNNER_013, fn))))
            self.assertEqual(src_011, src_013, f"{fn} drifted from HOS 013 spend boundary")


if __name__ == "__main__":
    unittest.main()
