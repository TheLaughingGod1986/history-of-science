"""HOS 013 Darwin & Wallace pass-1 Flow mint runner tests (J2499).

All tests run offline against local fixtures and Node DOM harnesses. They never
open Chrome/CDP, never click Create on a real page, and spend 0 credits (£0).
"""
from __future__ import annotations

import importlib.util
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

ROOT = Path(__file__).resolve().parents[1]
EDIT = ROOT / "02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project"
SCRIPT = EDIT / "_mint_flow_v01_pass1.py"
TRANCHE2_SCRIPT = ROOT / "02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/_mint_flow_v05_tranche2.py"
CAPTURE_PATH = ROOT / "jobs/reviews/J2033/LIVE_DOM_CAPTURE_2026-11-10.json"

TEST_STUDIO_ACCOUNT = "studio-ultra@example.com"
TEST_FORBIDDEN_ACCOUNT = "wrong-channel@example.com"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


RUNNER = _load_module("hos013_pass1_runner", SCRIPT)
TRANCHE2 = _load_module("hos009_tranche2_ref", TRANCHE2_SCRIPT)


def make_price(
    quality: str = "Quality",
    *,
    credits: int | None = None,
    model: str | None = None,
    outputs: str = "x1",
    aspect: str = "16:9",
    duration: str = "8s",
    line: str | None = None,
    read_at: str | None = None,
):
    actual_credits = (100 if quality == "Quality" else 10) if credits is None else credits
    actual_model = RUNNER.MODEL_BY_QUALITY.get(quality, "Veo 3.1 - Quality") if model is None else model
    return RUNNER.PriceEvidence(
        quality=quality,
        model=actual_model,
        outputs=outputs,
        aspect=aspect,
        duration=duration,
        credits=actual_credits,
        generate_line=line if line is not None else f"Generating will use {actual_credits} credits",
        read_at=read_at if read_at is not None else datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )


def make_batch_prices(**overrides) -> dict[str, object]:
    out = {
        "Quality": make_price("Quality"),
    }
    out.update(overrides)
    return out


def make_png(dest: Path, *, width: int = 1280, height: int = 720, color: str = "0x335577") -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-f",
            "lavfi",
            "-i",
            f"color=c={color}:s={width}x{height}",
            "-frames:v",
            "1",
            str(dest),
        ],
        check=True,
    )
    return dest


def make_silent_mp4(dest: Path, *, width: int = 1280, height: int = 720, duration: int = 8) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-f",
            "lavfi",
            "-i",
            f"color=c=0x224466:s={width}x{height}:d={duration}:r=25",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-an",
            str(dest),
        ],
        check=True,
    )
    return dest


def populate_media_style_refs(media: Path) -> None:
    make_png(media / "04_Generated-Clips/_style_refs/04_sunny_window_v01.jpg", width=1920, height=1080, color="0x446688")
    make_png(media / "04_Generated-Clips/_style_refs/10_mint_jar_v01.jpg", width=1920, height=1080, color="0x668844")


class ScopeOrderAndBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = RUNNER.load_scope(ROOT)

    def test_exact_66_rows_66_quality_0_fast_6600_credits(self):
        self.assertEqual(len(self.rows), 66)
        q_rows = [r for r in self.rows if r.quality == "Quality"]
        f_rows = [r for r in self.rows if r.quality == "Fast"]
        self.assertEqual(len(q_rows), 66)
        self.assertEqual(len(f_rows), 0)
        self.assertTrue(all(r.flow_model == "Veo 3.1 - Quality" and r.try1_credits == 100 for r in q_rows))
        self.assertTrue(all(r.flow_clip_s == 8 and r.max_takes == 1 for r in self.rows))
        self.assertEqual(sum(r.try1_credits for r in self.rows), 6600)
        self.assertEqual(sum(1 for r in self.rows if r.explorer), 2)

        # Cross-check against PICTURE_PLAN_v02.json totals and all 6 part boards.
        plan_path = EDIT / "PICTURE_PLAN_v02.json"
        plan = json.loads(plan_path.read_text())
        plan_digest = RUNNER.sha256_file(plan_path)
        scope_doc = json.loads((EDIT / "PASS1_SCOPE_J2499.json").read_text())
        mint_plan_doc = json.loads((EDIT / "PASS1_MINT_PLAN_J2499.json").read_text())
        self.assertEqual(scope_doc["plan_sha256"], plan_digest)
        self.assertEqual(mint_plan_doc["plan_sha256"], plan_digest)
        self.assertEqual(plan["totals"]["mint_rows"], 66)
        self.assertEqual(plan["totals"]["Quality"], 66)
        self.assertEqual(plan["totals"]["Fast"], 0)
        self.assertEqual(plan["totals"]["flow_credits_try1"], 6600)
        expected_ids = []
        for p in range(1, 7):
            board = json.loads((EDIT / "parts" / f"part-0{p}_plates_v02.json").read_text())
            for pl in board["plates"]:
                self.assertNotIn(pl["quality"], ("Fast", "Veo 3.1 - Fast"))
                if pl["route"] == "flow-first":
                    expected_ids.append(f"P{p}:{pl['id']}")
        self.assertEqual([r.row_id for r in self.rows], expected_ids)

    def test_fast_rows_and_fast_models_are_refused(self):
        self.assertNotIn("Fast", RUNNER.MODEL_BY_QUALITY)
        self.assertNotIn("Fast", RUNNER.PRICE_BY_QUALITY)
        for bad_q in ("Fast", "Veo 3.1 - Fast", "Veo 3.1 Fast"):
            with self.assertRaisesRegex(RUNNER.GuardError, "Fast is refused"):
                RUNNER.expected_model_for(bad_q)
            with self.assertRaisesRegex(RUNNER.GuardError, "Fast is refused"):
                RUNNER.expected_credits_for(bad_q)

        # Verify FAST_ROW_CHANGE_v02.json documents all 23 former Fast rows (5 free + 18 Quality) with archive sources/licences.
        change_doc = json.loads((EDIT / "FAST_ROW_CHANGE_v02.json").read_text())
        self.assertEqual(change_doc["summary"]["fast_rows_in_v01"], 23)
        self.assertEqual(change_doc["summary"]["fast_rows_in_v02"], 0)
        self.assertEqual(change_doc["summary"]["fast_swapped_to_free"], 5)
        self.assertEqual(change_doc["summary"]["fast_swapped_to_archive"], 2)
        self.assertEqual(change_doc["summary"]["fast_swapped_to_code_graphic"], 3)
        self.assertEqual(change_doc["summary"]["fast_upgraded_to_quality"], 18)
        self.assertEqual(len(change_doc["rows"]), 23)
        by_row = {entry["row_id"]: entry for entry in change_doc["rows"]}
        self.assertEqual(by_row["P4:07b_packet_to_mailbag"]["new"]["quality"], "code_graphic")
        self.assertEqual(by_row["P4:07b_packet_to_mailbag"]["new"]["route"], "code-graphic")
        self.assertIn("Ternate (early 1858)", by_row["P4:07b_packet_to_mailbag"]["new"]["shot_description"])
        self.assertIn("Down House (arrived 18 June 1858)", by_row["P4:07b_packet_to_mailbag"]["new"]["shot_description"])
        for entry in change_doc["rows"]:
            self.assertEqual(entry["old"]["quality"], "Fast")
            self.assertIn(entry["new"]["quality"], ("Quality", "archive", "code_graphic"))
            if entry["new"]["quality"] == "archive":
                arch = entry["new"]["archive_source"]
                self.assertTrue(arch["local_raw"])
                self.assertTrue(arch["commons_page"].startswith("https://commons.wikimedia.org/"))
                self.assertEqual(arch["licence"], "Public domain")
                self.assertEqual(len(arch["sha256"]), 64)

        # Verify load_scope refuses any Fast row in scope, on a board, in plan totals, or in scope caps.
        base_scope = json.loads((EDIT / "PASS1_SCOPE_J2499.json").read_text())

        def make_temp_repo(mutator) -> Path:
            tmp = tempfile.TemporaryDirectory()
            self.addCleanup(tmp.cleanup)
            repo = Path(tmp.name)
            (repo / "AGENTS.md").write_text("# test\n")
            edit = repo / RUNNER.EDIT_REL
            edit.mkdir(parents=True)
            shutil.copy2(EDIT / "PICTURE_PLAN_v02.json", edit / "PICTURE_PLAN_v02.json")
            (edit / "parts").mkdir()
            for p in range(1, 7):
                shutil.copy2(EDIT / "parts" / f"part-0{p}_plates_v02.json", edit / "parts" / f"part-0{p}_plates_v02.json")
            scope = json.loads(json.dumps(base_scope))
            mutator(repo, edit, scope)
            (edit / "PASS1_SCOPE_J2499.json").write_text(json.dumps(scope))
            return repo

        def mut_scope_row_fast(_r: Path, _e: Path, scope: dict) -> None:
            scope["rows"][2]["quality"] = "Fast"

        def mut_scope_row_model_fast(_r: Path, _e: Path, scope: dict) -> None:
            scope["rows"][2]["flow_model"] = "Veo 3.1 - Fast"

        def mut_scope_caps_fast(_r: Path, _e: Path, scope: dict) -> None:
            scope["caps"]["models"]["Fast"] = "Veo 3.1 - Fast"

        def mut_board_row_fast(_r: Path, edit: Path, scope: dict) -> None:
            b1_path = edit / "parts/part-01_plates_v02.json"
            b1 = json.loads(b1_path.read_text())
            b1["plates"][2]["quality"] = "Fast"
            b1["plates"][2]["flow_model"] = "Veo 3.1 Fast"
            b1_path.write_text(json.dumps(b1))
            new_hash = RUNNER.sha256_file(b1_path)
            scope["boards"]["1"]["sha256"] = new_hash
            for r in scope["rows"]:
                if r["part"] == 1:
                    r["board_sha256"] = new_hash

        for mut in (mut_scope_row_fast, mut_scope_row_model_fast, mut_scope_caps_fast, mut_board_row_fast):
            repo = make_temp_repo(mut)
            with self.assertRaisesRegex(RUNNER.GuardError, "Fast"):
                RUNNER.load_scope(repo)

    def test_order_part01_first_then_parts_02_to_06(self):
        ordered = RUNNER.order_rows(list(reversed(self.rows)))
        self.assertEqual([r.row_id for r in ordered], [r.row_id for r in self.rows])
        self.assertEqual(ordered[0].part, 1)
        self.assertEqual(ordered[0].row_id, "P1:01_study_beaks")
        self.assertEqual(ordered[-1].part, 6)
        self.assertEqual(ordered[-1].row_id, "P6:08b_darwin_mendel_synthesis")
        parts = [r.part for r in ordered]
        self.assertEqual(parts, sorted(parts))
        self.assertEqual([parts.count(p) for p in range(1, 7)], [12, 11, 14, 12, 9, 8])

        # Refuses a pass that does not start with Part 01.
        non_p1 = [r for r in self.rows if r.part >= 2]
        with self.assertRaisesRegex(RUNNER.GuardError, "Part 01"):
            RUNNER.order_rows(non_p1)

    def test_batches_respect_5_rows_and_1000_credits(self):
        batches = RUNNER.batch_rows(self.rows)
        self.assertEqual(len(batches), 14)
        self.assertEqual([len(b) for b in batches], [5] * 13 + [1])
        self.assertEqual(sum(len(b) for b in batches), 66)
        self.assertEqual(sum(sum(r.try1_credits for r in b) for b in batches), 6600)
        for batch in batches:
            self.assertLessEqual(len(batch), 5)
            self.assertLessEqual(RUNNER.assert_batch_limits(batch), 1000)

        # 6 rows = 600 credits (<1000) still refused by the 5-row cap.
        six_rows = self.rows[:6]
        self.assertEqual(len(six_rows), 6)
        with self.assertRaisesRegex(RUNNER.GuardError, "MAX_BATCH_ROWS"):
            RUNNER.assert_batch_limits(six_rows)

        # Out-of-order batch (Part 02 before Part 01) refused.
        p2_first = [next(r for r in self.rows if r.part == 2), self.rows[0]]
        with self.assertRaisesRegex(RUNNER.GuardError, "Part 01 -> Part 06 order"):
            RUNNER.assert_batch_limits(p2_first)

        # Credit cap > 1000 refused even if MAX_BATCH_ROWS were higher.
        with patch.object(RUNNER, "MAX_BATCH_ROWS", 12):
            eleven_quality = [r for r in self.rows if r.quality == "Quality"][:11]
            with self.assertRaisesRegex(RUNNER.GuardError, "exceeds 1000 credits"):
                RUNNER.assert_batch_limits(eleven_quality)

    def test_scope_drift_refused_across_plan_board_prompt_and_membership(self):
        base_scope = json.loads((EDIT / "PASS1_SCOPE_J2499.json").read_text())

        def make_temp_repo(mutator) -> Path:
            tmp = tempfile.TemporaryDirectory()
            self.addCleanup(tmp.cleanup)
            repo = Path(tmp.name)
            (repo / "AGENTS.md").write_text("# test\n")
            edit = repo / RUNNER.EDIT_REL
            edit.mkdir(parents=True)
            shutil.copy2(EDIT / "PICTURE_PLAN_v02.json", edit / "PICTURE_PLAN_v02.json")
            (edit / "parts").mkdir()
            for p in range(1, 7):
                shutil.copy2(EDIT / "parts" / f"part-0{p}_plates_v02.json", edit / "parts" / f"part-0{p}_plates_v02.json")
            scope = json.loads(json.dumps(base_scope))
            mutator(repo, edit, scope)
            (edit / "PASS1_SCOPE_J2499.json").write_text(json.dumps(scope))
            return repo

        mutations = [
            lambda _r, _e, s: s.__setitem__("plan_sha256", "0" * 64),
            lambda _r, _e, s: s["boards"]["1"].__setitem__("sha256", "f" * 64),
            lambda _r, _e, s: s["rows"][0].__setitem__("prompt_sha256", "a" * 64),
            lambda _r, _e, s: s["rows"][0].__setitem__("normalized_prompt_sha256", "b" * 64),
            lambda _r, _e, s: s["rows"][0].__setitem__("row_id", "P1:wrong_id"),
            lambda _r, _e, s: s["rows"].pop(),
            lambda _r, _e, s: s["caps"].__setitem__("max_total_credits", 6000),
            lambda _r, _e, s: s["caps"].__setitem__("max_takes_per_row", 2),
        ]
        for idx, mut in enumerate(mutations):
            with self.subTest(case=idx):
                repo = make_temp_repo(mut)
                with self.assertRaises(RUNNER.GuardError):
                    RUNNER.load_scope(repo)

        # Prompt text edited on disk after scope lock also fails closed (even if board hash were updated).
        def mutate_prompt_on_board(_repo: Path, edit: Path, scope: dict) -> None:
            b1_path = edit / "parts/part-01_plates_v02.json"
            b1 = json.loads(b1_path.read_text())
            for pl in b1["plates"]:
                if pl["id"] == "01_study_beaks":
                    pl["prompt"] = pl["prompt"] + " Extra unauthorized text."
            b1_path.write_text(json.dumps(b1))
            new_hash = RUNNER.sha256_file(b1_path)
            scope["boards"]["1"]["sha256"] = new_hash
            for r in scope["rows"]:
                if r["part"] == 1:
                    r["board_sha256"] = new_hash

        repo = make_temp_repo(mutate_prompt_on_board)
        with self.assertRaisesRegex(RUNNER.GuardError, "prompt hash mismatch"):
            RUNNER.load_scope(repo)

    def test_no_keep_or_legacy_auto_keep_imports_in_runner(self):
        src = SCRIPT.read_text()
        self.assertNotRegex(src, r"(import|spec_from_file_location|load_mod).*tranche1")
        self.assertNotRegex(src, r"['\"]status['\"]\s*:\s*['\"]KEEP['\"]")
        self.assertIn("reuse_page", src)


class PriceAccountStyleAndCapGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = RUNNER.load_scope(ROOT)
        cls.q_row = next(r for r in cls.rows if r.quality == "Quality")

    def test_account_digests_match_studio_ultra_without_storing_emails(self):
        self.assertEqual(RUNNER.account_sha256(TRANCHE2.REQUIRED_ACCOUNT), RUNNER.REQUIRED_ACCOUNT_SHA256)
        self.assertEqual(RUNNER.account_sha256(TRANCHE2.FORBIDDEN_ACCOUNT), RUNNER.FORBIDDEN_ACCOUNT_SHA256)
        now = datetime.now(timezone.utc)
        self.assertEqual(
            RUNNER.accept_account(TRANCHE2.REQUIRED_ACCOUNT, now.isoformat(), now=now),
            RUNNER.REQUIRED_ACCOUNT_SHA256,
        )
        self.assertEqual(
            RUNNER.accept_account(RUNNER.REQUIRED_ACCOUNT_SHA256, now.isoformat(), now=now),
            RUNNER.REQUIRED_ACCOUNT_SHA256,
        )
        for bad in (TRANCHE2.FORBIDDEN_ACCOUNT, RUNNER.FORBIDDEN_ACCOUNT_SHA256, TEST_FORBIDDEN_ACCOUNT, "", None):
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.accept_account(bad, now.isoformat(), now=now)
        stale = (now - timedelta(hours=1)).isoformat()
        with self.assertRaisesRegex(RUNNER.GuardError, "not fresh"):
            RUNNER.accept_account(RUNNER.REQUIRED_ACCOUNT_SHA256, stale, now=now)

    def test_price_guards_for_quality_100_and_fast_refused(self):
        now = datetime.now(timezone.utc)
        self.assertEqual(RUNNER.accept_price(make_price("Quality"), quality="Quality", now=now), 100)
        self.assertEqual(RUNNER.accept_batch_prices(make_batch_prices(), now=now), {"Quality": 100})

        # Fast price evidence is refused both directly and in pre-batch readings.
        with self.assertRaisesRegex(RUNNER.GuardError, "Fast is refused"):
            RUNNER.accept_price(make_price("Fast", model="Veo 3.1 - Fast", credits=10), quality="Fast", now=now)
        with self.assertRaisesRegex(RUNNER.GuardError, "Fast is refused"):
            RUNNER.accept_batch_prices(
                {"Quality": make_price("Quality"), "Fast": make_price("Fast", model="Veo 3.1 - Fast", credits=10)},
                now=now,
            )

        # Mismatched model, credits, duration, aspect, outputs, or missing Quality fail closed.
        bad_cases = [
            ("Quality", make_price("Quality", credits=101, line="Generating will use 101 credits")),
            ("Quality", make_price("Quality", model="Veo 3.1 - Fast")),
            ("Quality", make_price("Quality", duration="4s")),
            ("Quality", make_price("Quality", aspect="9:16")),
            ("Quality", make_price("Quality", outputs="x2")),
            ("Quality", make_price("Quality", read_at=(now - timedelta(minutes=30)).isoformat())),
        ]
        for q, ev in bad_cases:
            with self.subTest(quality=q, ev=ev):
                with self.assertRaises(RUNNER.GuardError):
                    RUNNER.accept_price(ev, quality=q, now=now)

        with self.assertRaisesRegex(RUNNER.GuardError, "missing pre-batch live price reading for Quality"):
            RUNNER.accept_batch_prices({}, now=now)

    def test_headroom_reservations_6600_cap_and_single_take_per_row(self):
        # Recorded balance 14,890 with HOS 009 J2033 reserving 6,000 leaves 2,290 after 013's 6,600 cap.
        self.assertEqual(RUNNER.headroom(14890, 0, 0, 6000), 2290)
        self.assertEqual(
            RUNNER.can_take(
                row=self.q_row, live=14890, spent=0, pending=0, other=6000,
                takes_done=0, unknown_pending=False, cost=100,
            ),
            2290,
        )
        # Boundary: 6,000 + 6,600 = 12,600 minimum live balance required.
        self.assertEqual(RUNNER.headroom(12600, 0, 0, 6000), 0)
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.headroom(12599, 0, 0, 6000)

        # Refuse 2nd take on any row in pass 1.
        with self.assertRaisesRegex(RUNNER.GuardError, "pass-1 cap is 1"):
            RUNNER.can_take(
                row=self.q_row, live=14890, spent=100, pending=0, other=0,
                takes_done=1, unknown_pending=False, cost=100,
            )
        # Refuse wrong cost for row quality (10 on Quality).
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.can_take(
                row=self.q_row, live=14890, spent=0, pending=0, other=0,
                takes_done=0, unknown_pending=False, cost=10,
            )
        # Refuse exceeding 6,600 total cap.
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.can_take(
                row=self.q_row, live=14890, spent=6550, pending=0, other=0,
                takes_done=0, unknown_pending=False, cost=100,
            )
        # Refuse unknown pending charge.
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.can_take(
                row=self.q_row, live=14890, spent=0, pending=0, other=0,
                takes_done=0, unknown_pending=True, cost=100,
            )

    def test_next_version_refuses_second_take_and_ledger_rejects_keep(self):
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp)
            take, dest = RUNNER.next_version(media, 1, "01_study_beaks")
            self.assertEqual(take, 1)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(b"take-1")
            with self.assertRaisesRegex(RUNNER.GuardError, "refuses a second take"):
                RUNNER.next_version(media, 1, "01_study_beaks")

            ledger_file = media / "ledger.jsonl"
            with self.assertRaisesRegex(RUNNER.GuardError, "KEEP"):
                RUNNER.append_ledger(ledger_file, {"row_id": "P1:01_study_beaks", "take": 1, "status": "KEEP"})
            with self.assertRaisesRegex(RUNNER.GuardError, "KEEP"):
                RUNNER.ledger_totals([{"row_id": "P1:01_study_beaks", "take": 1, "status": "PENDING_REVIEW", "keep": True}])
            with self.assertRaisesRegex(RUNNER.GuardError, "MAX_TAKES_PER_ROW=1"):
                RUNNER.ledger_totals([
                    {"row_id": "P1:01_study_beaks", "take": 1, "status": "PENDING_REVIEW", "credits_used": 100, "keep": False},
                    {"row_id": "P1:01_study_beaks", "take": 2, "status": "PENDING_REVIEW", "credits_used": 100, "keep": False},
                ])

    def test_missing_corrupt_or_drifted_style_references_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            media = root / "media"
            # Missing house style refs on media volume fails closed.
            with self.assertRaisesRegex(RUNNER.GuardError, "style reference"):
                RUNNER.verify_style_references(ROOT, media, self.rows, check_scope_hashes=False)

            # Valid 16:9 house style refs pass when scope hash pinning is disabled for synthetic fixtures.
            populate_media_style_refs(media)
            verified = RUNNER.verify_style_references(ROOT, media, self.rows, check_scope_hashes=False)
            self.assertEqual(len(verified["house"]), 2)
            self.assertIsNotNone(verified["explorer"])

            # Scope hash drift on house style refs fails closed in production mode.
            with self.assertRaisesRegex(RUNNER.GuardError, "sha256 drift"):
                RUNNER.verify_style_references(ROOT, media, self.rows, check_scope_hashes=True)

            # Corrupt or non-16:9 house style ref fails closed.
            bad_ref = media / "04_Generated-Clips/_style_refs/10_mint_jar_v01.jpg"
            make_png(bad_ref, width=1080, height=1920)
            with self.assertRaisesRegex(RUNNER.GuardError, "not 16:9"):
                RUNNER.verify_style_references(ROOT, media, self.rows, check_scope_hashes=False)

            bad_ref.write_bytes(b"corrupt-bytes")
            with self.assertRaisesRegex(RUNNER.GuardError, "corrupt"):
                RUNNER.verify_style_references(ROOT, media, self.rows, check_scope_hashes=False)

            # Missing Explorer reference fails closed when any Explorer row is in scope.
            populate_media_style_refs(media)
            fake_repo = root / "repo"
            (fake_repo / RUNNER.EDIT_REL).mkdir(parents=True)
            shutil.copy2(EDIT / "PICTURE_PLAN_v02.json", fake_repo / RUNNER.EDIT_REL / "PICTURE_PLAN_v02.json")
            with self.assertRaisesRegex(RUNNER.GuardError, "missing Explorer style reference"):
                RUNNER.verify_style_references(fake_repo, media, self.rows, check_scope_hashes=False)

        # Real studio-live NAS media passes full scope hash verification if mounted.
        if RUNNER.DEFAULT_NAS_MEDIA.is_dir():
            real_verified = RUNNER.verify_style_references(ROOT, RUNNER.DEFAULT_NAS_MEDIA, self.rows, check_scope_hashes=True)
            self.assertEqual(len(real_verified["house"]), 2)
            self.assertIsNotNone(real_verified["explorer"])


class SharedAccountingLockAndDuplicateProcessTests(unittest.TestCase):
    def test_shared_accounting_reservations_pending_and_reconciliation(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            with RUNNER.SharedFlowAccounting(state) as account:
                # HOS 009 holds 6,000; HOS 013 reserves 6,600 -> total liability 12,600.
                account.reserve("J2033", "HOS:009", 6000, live=14890)
                with self.assertRaises(RUNNER.GuardError):
                    account.reserve("HOS013_PASS1", "HOS:013", 6600, live=12599)
                account.reserve("HOS013_PASS1", "HOS:013", 6600, live=14890)
                account.reserve("HOS013_PASS1", "HOS:013", 6600, live=14890)  # idempotent
                self.assertEqual(account.snapshot()["liability"], 12600)

                # Pending charge blocks retry and cross-channel reserve/intent.
                account.intent("HOS:013:P01:01_study_beaks:t1", "HOS013_PASS1", 100, live=14890)
                self.assertTrue(account.snapshot()["pending"])
                with self.assertRaises(RUNNER.GuardError):
                    account.intent("HOS:013:P01:02_drawer_lock:t1", "HOS013_PASS1", 100, live=14890)
                with self.assertRaises(RUNNER.GuardError):
                    account.reserve("OWB-032", "OWB:032", 100, live=20000)

                # Resolve submitted -> unposted charge stays in liability until explicit posted evidence.
                account.resolve("HOS:013:P01:01_study_beaks:t1", submitted=True, evidence={"ui": {"balances": [14890]}})
                self.assertFalse(account.snapshot()["pending"])
                self.assertEqual(account.snapshot()["liability"], 12600)
                account.reconcile_posted("HOS:013:P01:01_study_beaks:t1", evidence={"before": 14890, "after": 14790, "delta": 100})
                self.assertEqual(account.snapshot()["liability"], 12500)

    def test_writer_lock_and_two_process_accounting_competition(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lock_path = root / "writer.lock"
            with RUNNER.WriterLock(lock_path):
                probe = subprocess.run(
                    [
                        sys.executable,
                        "-c",
                        "import importlib.util,sys\n"
                        f"s=importlib.util.spec_from_file_location('r',{str(SCRIPT)!r})\n"
                        "m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)\n"
                        "from pathlib import Path\n"
                        f"try:\n m.WriterLock(Path({str(lock_path)!r})).__enter__()\n"
                        "except m.GuardError:\n raise SystemExit(0)\n"
                        "raise SystemExit(1)\n",
                    ],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(probe.returncode, 0, probe.stderr)

            # Two processes competing for the last 6,600 credits: exactly one wins.
            state = root / "shared"
            code = (
                "import importlib.util,sys,time\n"
                f"s=importlib.util.spec_from_file_location('r',{str(SCRIPT)!r})\n"
                "m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)\n"
                "from pathlib import Path\n"
                f"state=Path({str(state)!r})\n"
                "try:\n"
                " with m.SharedFlowAccounting(state) as a:\n"
                "  a.reserve(sys.argv[1],sys.argv[2],6600,live=7000)\n"
                "  time.sleep(0.15)\n"
                "except m.GuardError:\n"
                " raise SystemExit(75)\n"
            )
            procs = [
                subprocess.Popen([sys.executable, "-c", code, key, film])
                for key, film in [("p1", "HOS:013"), ("p2", "OWB:032")]
            ]
            self.assertEqual(sorted(p.wait(timeout=5) for p in procs), [0, 75])

    def test_second_process_and_killed_owner_live_child_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sleeper = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
            try:
                pid_path = root / "runner.pid"
                done_path = root / "runner.done"
                pid_path.write_text(str(sleeper.pid))
                done_path.write_text("0\n")  # Stale done must never override a live PID.
                with self.assertRaisesRegex(RUNNER.GuardError, "runner already live"):
                    RUNNER.refuse_duplicate(pid_path, done_path)
            finally:
                sleeper.kill()
                sleeper.wait(timeout=5)

        # Killed launch_once owner leaves live child whose PID blocks a second launch.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            owner = root / "owner.py"
            owner.write_text(
                "import importlib.util,sys\n"
                f"s=importlib.util.spec_from_file_location('r',{str(SCRIPT)!r})\n"
                "m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)\n"
                "from pathlib import Path\n"
                f"root=Path({str(root)!r})\n"
                "cmd=[sys.executable,'-c',\"from pathlib import Path;import time;Path(\"+repr(str(root/'started'))+\").touch();time.sleep(30)\"]\n"
                "m.launch_once(cmd,ownership=root/'owner.lock',pid=root/'runner.pid',log=root/'1.log',done=root/'1.done')\n"
            )
            parent = subprocess.Popen([sys.executable, str(owner)])
            child_pid = None
            try:
                deadline = time.monotonic() + 5
                while not (root / "started").exists() and time.monotonic() < deadline:
                    time.sleep(0.02)
                self.assertTrue((root / "started").exists())
                child_pid = int((root / "runner.pid").read_text())
                parent.kill()
                parent.wait(timeout=5)
                self.assertTrue(RUNNER.process_alive(child_pid))
                with self.assertRaisesRegex(RUNNER.GuardError, "runner already live"):
                    RUNNER.launch_once(
                        ["unreachable"],
                        ownership=root / "owner.lock",
                        pid=root / "runner.pid",
                        log=root / "2.log",
                        done=root / "2.done",
                    )
                self.assertFalse((root / "2.log").exists())
            finally:
                if parent.poll() is None:
                    parent.kill()
                    parent.wait()
                if child_pid and RUNNER.process_alive(child_pid):
                    os.kill(child_pid, 15)


class BatchExecutionArchiveAndReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = RUNNER.load_scope(ROOT)
        cls.batch1 = RUNNER.batch_rows(cls.rows)[0]

    def test_quality_batch_saves_generated_pending_review_and_nas_sha256(self):
        # Batch 1 has 5 Quality (500) = 5 rows, 500 credits (0 Fast).
        self.assertEqual([r.quality for r in self.batch1], ["Quality"] * 5)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            media = root / "media"
            archive = root / "archive"
            archive.mkdir()
            populate_media_style_refs(media)
            sample_mp4 = make_silent_mp4(root / "fixture.mp4")

            stills_called: list[str] = []
            price_reads = {"count": 0}

            def fake_price_reader():
                price_reads["count"] += 1
                return make_batch_prices()

            def fake_still_maker(row, dest, *, repo, media, accounting, reservation, evidence_path, other=0, floor=0):
                accounting._assert_held()
                stills_called.append(row.row_id)
                make_png(dest, width=1280, height=720, color=f"0x{row.index:02x}4466")
                RUNNER.immutable_bytes(
                    evidence_path,
                    (json.dumps({"row_id": row.row_id, "credits": 0, "ui": {"balances": [14890]}}) + "\n").encode(),
                )
                return dest

            def fake_submitter(row, dest, frame, *, accounting, reservation, charge, evidence_path, other=0, floor=0):
                self.assertTrue(frame.is_file())
                page = LiveDomAndTrustedClickTests.MockPage(
                    LiveDomAndTrustedClickTests.video_evidence(quality=row.quality, account=TRANCHE2.REQUIRED_ACCOUNT, balance=14890)
                )
                accounting.reserve(reservation, RUNNER.FILM_ID, RUNNER.MAX_TOTAL_CREDITS, live=14890, floor=floor + other)
                ev = RUNNER.guarded_create(
                    page,
                    accounting,
                    row=row,
                    reservation=reservation,
                    charge=charge,
                    evidence_path=evidence_path,
                    floor=floor + other,
                )
                shutil.copy2(sample_mp4, dest)
                return ev

            with patch.dict(os.environ, {RUNNER.SUBMIT_ENV: "1"}):
                written = RUNNER.cmd_submit(
                    ROOT,
                    other=6000,
                    media=media,
                    ledger_path=root / "ledger.jsonl",
                    lock_path=root / "writer.lock",
                    pid_path=root / "runner.pid",
                    done_path=root / "runner.done",
                    archive_dir=archive,
                    accounting_state=root / "shared",
                    spend_ledger=root / "ai_spend.jsonl",
                    batch_price_reader=fake_price_reader,
                    submitter=fake_submitter,
                    still_maker=fake_still_maker,
                    test_archive=True,
                )

            self.assertEqual(price_reads["count"], 1)
            self.assertEqual(len(written), 5)
            self.assertEqual(stills_called, [r.row_id for r in self.batch1])
            self.assertEqual([e["credits_used"] for e in written], [100] * 5)
            for entry in written:
                self.assertEqual(entry["status"], "PENDING_REVIEW")
                self.assertEqual(entry["file_state"], "GENERATED")
                self.assertEqual(entry["review"], "PENDING_REVIEW")
                self.assertIs(entry["keep"], False)
                self.assertIs(entry["generated"], True)
                self.assertTrue(RUNNER.verified_output(entry))
                # No personal email leaked into persisted create_evidence.
                self.assertNotIn("accounts", entry["create_evidence"]["ui"])
                self.assertEqual(entry["create_evidence"]["ui"]["account_sha256"], RUNNER.REQUIRED_ACCOUNT_SHA256)

            # Archive holds 5 mp4s, 5 sha256 sidecars, 5 per-take receipts, and 1 batch receipt.
            archived_mp4s = sorted(archive.glob("*.mp4"))
            self.assertEqual(len(archived_mp4s), 5)
            for mp4 in archived_mp4s:
                proof = json.loads(mp4.with_suffix(".mp4.sha256.json").read_text())
                self.assertEqual(proof["sha256"], RUNNER.sha256_file(mp4))
                receipt = json.loads(mp4.with_suffix(".mp4.receipt.json").read_text())
                self.assertIs(receipt["keep"], False)
                self.assertEqual(receipt["file_state"], "GENERATED")
                self.assertEqual(receipt["review"], "PENDING_REVIEW")

            # Shared accounting recorded 500 credits across 5 takes (5*100) and exported ai_spend.
            snap = RUNNER.SharedFlowAccounting.peek_readonly(root / "shared")
            self.assertEqual(sum(c["amount"] for c in snap["charges"].values()), 500)
            spend_rows = [json.loads(line) for line in (root / "ai_spend.jsonl").read_text().splitlines()]
            self.assertEqual(
                [r["amount"] for r in spend_rows if r["kind"] == "spend"],
                [100] * 5,
            )

            # Next batch advances cleanly to Batch 2 without repeating Batch 1 rows.
            ledger = RUNNER.read_ledger(root / "ledger.jsonl")
            batch2 = RUNNER.next_batch(self.rows, ledger)
            self.assertEqual([r.row_id for r in batch2], [r.row_id for r in RUNNER.batch_rows(self.rows)[1]])

    def test_bad_batch_price_or_unresolved_local_submitting_calls_zero_submits(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            media = root / "media"
            archive = root / "archive"
            archive.mkdir()
            populate_media_style_refs(media)
            submits = []

            # Bad Quality price (101 instead of 100) or any Fast price stops batch before still_maker or submitter.
            with self.assertRaisesRegex(RUNNER.GuardError, "price 101 is not 100"):
                RUNNER.execute_shared_batch(
                    self.batch1[:2],
                    repo=ROOT,
                    media=media,
                    ledger_path=root / "ledger.jsonl",
                    archive_dir=archive,
                    accounting_state=root / "shared",
                    batch_price_reader=lambda: make_batch_prices(
                        Quality=make_price("Quality", credits=101, line="Generating will use 101 credits")
                    ),
                    submitter=lambda *a, **k: submits.append(1),
                    test_archive=True,
                    inventory_rows=self.rows,
                )
            with self.assertRaisesRegex(RUNNER.GuardError, "Fast is refused"):
                RUNNER.execute_shared_batch(
                    self.batch1[:2],
                    repo=ROOT,
                    media=media,
                    ledger_path=root / "ledger.jsonl",
                    archive_dir=archive,
                    accounting_state=root / "shared",
                    batch_price_reader=lambda: make_batch_prices(
                        Fast=make_price("Fast", model="Veo 3.1 - Fast", credits=10, line="Generating will use 10 credits")
                    ),
                    submitter=lambda *a, **k: submits.append(1),
                    test_archive=True,
                    inventory_rows=self.rows,
                )
            self.assertEqual(submits, [])

            # Unresolved local SUBMITTING stops before batch_price_reader is even called.
            price_calls = []
            RUNNER.append_ledger(
                root / "ledger2.jsonl",
                {"row_id": self.batch1[0].row_id, "part": 1, "plate_id": self.batch1[0].plate_id, "take": 1,
                 "status": "SUBMITTING", "credits_reserved": 100, "keep": False},
            )
            with self.assertRaisesRegex(RUNNER.GuardError, "unresolved local SUBMITTING"):
                RUNNER.execute_shared_batch(
                    self.batch1[:1],
                    repo=ROOT,
                    media=media,
                    ledger_path=root / "ledger2.jsonl",
                    archive_dir=archive,
                    accounting_state=root / "shared2",
                    batch_price_reader=lambda: price_calls.append(1),
                    submitter=lambda *a, **k: submits.append(1),
                    test_archive=True,
                    inventory_rows=self.rows,
                )
            self.assertEqual(price_calls, [])
            self.assertEqual(submits, [])

    def test_production_archive_must_be_on_mounted_nas_and_scope_cannot_inject_extra_row(self):
        base = "/tmp" if Path("/tmp").is_dir() else None
        with tempfile.TemporaryDirectory(dir=base) as tmp:
            root = Path(tmp)
            for candidate in (None, root, root / "missing"):
                with self.assertRaises(RUNNER.GuardError):
                    RUNNER.require_archive(candidate, nas=True)

            # Out-of-scope or Fast row is rejected before any submission.
            fake_row = RUNNER.Row(
                index=999, row_id="P1:99_out_of_scope", part=1, plate_id="99_out_of_scope",
                board="x", quality="Quality", flow_model="Veo 3.1 - Quality", max_takes=1,
                try1_credits=100, flow_clip_s=8, t_s=999.0, t_end_s=1003.0, use_s=4.0,
                explorer=False, prompt="x", prompt_sha256="0" * 64, normalized_prompt_sha256="0" * 64,
            )
            (root / "archive").mkdir()
            with self.assertRaisesRegex(RUNNER.GuardError, "outside the locked 66-row scope"):
                RUNNER.execute_shared_batch(
                    [fake_row],
                    repo=ROOT,
                    media=root / "media",
                    ledger_path=root / "ledger.jsonl",
                    archive_dir=root / "archive",
                    accounting_state=root / "shared",
                    test_archive=True,
                    inventory_rows=self.rows,
                )


class LiveDomAndTrustedClickTests(unittest.TestCase):
    @staticmethod
    def video_evidence(*, quality: str = "Quality", account: str = TEST_STUDIO_ACCOUNT, balance: int = 14890,
                       model: str | None = None, cost: int | None = None) -> dict:
        if model is None:
            model = "Veo 3.1 - Fast" if quality == "Fast" else RUNNER.expected_model_for(quality)
        if cost is None:
            cost = 10 if quality == "Fast" else RUNNER.expected_credits_for(quality)
        return dict(
            host=RUNNER.FLOW_HOST,
            models=[model],
            outputs=["x1"],
            aspects=["16:9"],
            durations=["8s"],
            accounts=[account],
            prices=[f"Generating will use {cost} credits"],
            balances=[balance],
            ultra=True,
            create_count=1,
        )

    @staticmethod
    def still_evidence(*, account: str = TEST_STUDIO_ACCOUNT, balance: int = 14890) -> dict:
        return dict(
            host=RUNNER.FLOW_HOST,
            models=[RUNNER.REQUIRED_STILL_MODEL],
            outputs=["x1"],
            aspects=["16:9"],
            accounts=[account],
            prices=["Generating will use 0 credits"],
            balances=[balance],
            ultra=True,
            create_count=1,
        )

    class MockPage:
        def __init__(self, evidence: dict, *, before_click=None, on_mouse_click=None):
            self.evidence = evidence
            self.before_click = before_click
            self.on_mouse_click = on_mouse_click
            self.clicks = 0
            self.mouse_coords: list[tuple[float, float]] = []
            outer = self

            class Mouse:
                @staticmethod
                def click(x: float, y: float) -> None:
                    if outer.on_mouse_click:
                        outer.on_mouse_click(x, y)
                    outer.clicks += 1
                    outer.mouse_coords.append((x, y))

            self.mouse = Mouse()

        def evaluate(self, _js: str, expected):
            if expected is None:
                return dict(self.evidence)
            if self.before_click:
                self.before_click()
            if self.evidence != expected:
                return dict(ready=False, reason="live UI changed", evidence=self.evidence)
            return dict(ready=True, target=dict(x=1000.0, y=844.0), evidence=self.evidence)

    def test_guarded_create_validates_quality_rows_and_refuses_fast_row_or_fast_ui(self):
        rows = RUNNER.load_scope(ROOT)
        q_row = next(r for r in rows if r.quality == "Quality")
        synthetic_fast_row = RUNNER.Row(
            index=99, row_id="P1:99_fast_refused", part=1, plate_id="99_fast_refused",
            board=q_row.board, quality="Fast", flow_model="Veo 3.1 - Fast", max_takes=1,
            try1_credits=10, flow_clip_s=8, t_s=1.0, t_end_s=5.0, use_s=4.0,
            explorer=False, prompt=q_row.prompt, prompt_sha256=q_row.prompt_sha256,
            normalized_prompt_sha256=q_row.normalized_prompt_sha256,
        )

        with patch.object(RUNNER, "REQUIRED_ACCOUNT_SHA256", RUNNER.account_sha256(TEST_STUDIO_ACCOUNT)), \
             patch.object(RUNNER, "FORBIDDEN_ACCOUNT_SHA256", RUNNER.account_sha256(TEST_FORBIDDEN_ACCOUNT)):
            # Quality row rejects Fast UI; synthetic Fast row is refused immediately before reading DOM.
            with tempfile.TemporaryDirectory() as tmp:
                state = Path(tmp)
                with RUNNER.SharedFlowAccounting(state) as account:
                    account.reserve("HOS013_PASS1", "HOS:013", 6600, live=14890)
                    fast_page = self.MockPage(self.video_evidence(quality="Fast"))
                    with self.assertRaises(RUNNER.GuardError):
                        RUNNER.guarded_create(
                            fast_page, account, row=q_row, reservation="HOS013_PASS1",
                            charge="q-on-fast", evidence_path=state / "q_bad.json",
                        )
                    self.assertEqual(fast_page.clicks, 0)

                    qual_page = self.MockPage(self.video_evidence(quality="Quality"))
                    with self.assertRaisesRegex(RUNNER.GuardError, "Fast is refused"):
                        RUNNER.guarded_create(
                            qual_page, account, row=synthetic_fast_row, reservation="HOS013_PASS1",
                            charge="f-on-qual", evidence_path=state / "f_bad.json",
                        )
                    self.assertEqual(qual_page.clicks, 0)
                    self.assertFalse(account.snapshot()["charges"])

                    # Matching Quality (100) row succeeds via trusted mouse.click.
                    RUNNER.guarded_create(
                        qual_page, account, row=q_row, reservation="HOS013_PASS1",
                        charge="q-ok", evidence_path=state / "q_ok.json",
                    )
                    self.assertEqual(qual_page.clicks, 1)
                    charges = account.snapshot()["charges"]
                    self.assertEqual(charges["q-ok"]["amount"], 100)

            # UI drift right before click resolves NOT_SUBMITTED without clicking.
            with tempfile.TemporaryDirectory() as tmp:
                state = Path(tmp)
                with RUNNER.SharedFlowAccounting(state) as account:
                    account.reserve("HOS013_PASS1", "HOS:013", 6600, live=14890)
                    page = self.MockPage(self.video_evidence(quality="Quality"))
                    page.before_click = lambda: page.evidence.update(durations=["4s"])
                    with self.assertRaisesRegex(RUNNER.GuardError, "live UI drift"):
                        RUNNER.guarded_create(
                            page, account, row=q_row, reservation="HOS013_PASS1",
                            charge="drift", evidence_path=state / "drift.json",
                        )
                    self.assertEqual(page.clicks, 0)
                    self.assertEqual(account.snapshot()["charges"]["drift"]["status"], "NOT_SUBMITTED")

            # Browser disconnect during mouse.click leaves charge PENDING, blocking cross-channel spend.
            with tempfile.TemporaryDirectory() as tmp:
                state = Path(tmp)
                with RUNNER.SharedFlowAccounting(state) as account:
                    account.reserve("HOS013_PASS1", "HOS:013", 6600, live=14890)
                    page = self.MockPage(
                        self.video_evidence(quality="Quality"),
                        on_mouse_click=lambda *_: (_ for _ in ()).throw(ConnectionError("cdp dropped")),
                    )
                    with self.assertRaises(ConnectionError):
                        RUNNER.guarded_create(
                            page, account, row=q_row, reservation="HOS013_PASS1",
                            charge="drop", evidence_path=state / "drop.json",
                        )
                with RUNNER.SharedFlowAccounting(state) as account:
                    self.assertTrue(account.snapshot()["pending"])

    def test_read_live_batch_prices_on_page_reads_quality_100_without_clicking_create(self):
        with patch.object(RUNNER, "REQUIRED_ACCOUNT_SHA256", RUNNER.account_sha256(TEST_STUDIO_ACCOUNT)):
            configured_models: list[str] = []

            class PricePage:
                def __init__(self):
                    self.current_model = "Veo 3.1 - Quality"
                    self.clicks = 0

                def evaluate(self, js, _arg=None):
                    if "models" not in js:
                        return {
                            "host": "flow.google.com",
                            "accounts": [TEST_STUDIO_ACCOUNT],
                            "balances": [14890],
                            "ultra": True,
                        }
                    cost = 100 if "Quality" in self.current_model else 10
                    return {
                        "host": "flow.google.com",
                        "models": [self.current_model],
                        "outputs": ["x1"],
                        "aspects": ["16:9"],
                        "durations": ["8s"],
                        "accounts": [TEST_STUDIO_ACCOUNT],
                        "prices": [f"Generating will use {cost} credits"],
                        "balances": [],
                        "ultra": True,
                        "create_count": 0,  # Empty prompt box has disabled Create; price read still works!
                    }

                class keyboard:
                    @staticmethod
                    def press(_k):
                        pass

                def wait_for_timeout(self, _ms):
                    pass

            page = PricePage()

            def configure(p, model):
                configured_models.append(model)
                p.current_model = model

            prices = RUNNER.read_live_batch_prices_on_page(page, configure_model=configure)
            self.assertEqual(configured_models, ["Veo 3.1 - Quality"])
            self.assertEqual(prices["Quality"].credits, 100)
            self.assertNotIn("Fast", prices)
            self.assertEqual(page.clicks, 0)

    def test_create_button_labels_match_the_009_runner_on_both_paths(self):
        # 10 Nov 2026 (history-of-science #480): the 009 runner learned that the video Create button can read
        # "Start generation". The still path here already knew; the video path did not, and would have stopped the
        # first paid take of pass 1 with "Create button is missing". Exactly one such button is still required.
        labels = "t === 'Create' || t === 'Start generation' || t === 'arrow_forward'"
        self.assertIn(labels, RUNNER.CREATE_EVIDENCE_JS)
        self.assertIn(labels, RUNNER.STILL_EVIDENCE_JS)
        tranche2 = (SCRIPT.parents[2] / "009_The-Falling-Moon-Gravity" / "07_Edit-Project" /
                    "_mint_flow_v05_tranche2.py").read_text()
        self.assertEqual(tranche2.count(labels), 2)
        self.assertIn("if (buttons.length !== 1) return {ready: false, reason: 'Create not unique', evidence};",
                      RUNNER.CREATE_EVIDENCE_JS)

    def test_captured_10nov_dom_for_balance_quality_fast_and_still_never_clicks_dom(self):
        raw_capture = CAPTURE_PATH.read_text().replace("<REQUIRED_HOS_ULTRA_ACCOUNT>", TEST_STUDIO_ACCOUNT)
        capture = json.loads(raw_capture)

        dom_harness = r"""
const fs = require('fs');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
let domClicks = 0;
const iconHit = {};
const makeNode = (ctrl) => ({
  innerText: ctrl.text || '',
  disabled: Boolean(ctrl.disabled),
  getAttribute: (k) => {
    if (k === 'aria-label') return ctrl.ariaLabel || null;
    if (k === 'aria-checked') return ctrl.ariaChecked || null;
    if (k === 'aria-selected') return ctrl.ariaSelected || null;
    if (k === 'aria-pressed') return ctrl.ariaPressed || null;
    if (k === 'role') return ctrl.role || null;
    return null;
  },
  contains: (other) => Boolean(ctrl.isCreate && other === iconHit),
  getBoundingClientRect: () => ({ left: 984, top: 828, width: ctrl.hidden ? 0 : 32, height: ctrl.hidden ? 0 : 32 }),
  click: () => { domClicks++; },
});
const controls = (input.controls || []).map(makeNode);
global.innerWidth = 1440;
global.innerHeight = 900;
global.location = { hostname: 'flow.google.com' };
global.getComputedStyle = () => ({ visibility: 'visible', display: 'block' });
global.document = {
  body: { innerText: (input.bodyLines || []).join('\n') },
  elementFromPoint: () => input.obstructed ? {} : iconHit,
  querySelectorAll: (q) => {
    if (q.includes('[aria-selected="true"]')) {
      return controls.filter(n =>
        n.getAttribute('aria-selected') === 'true' ||
        n.getAttribute('aria-checked') === 'true' ||
        n.getAttribute('aria-pressed') === 'true'
      );
    }
    if (q === 'button') return controls.filter(n => !n.getAttribute('role') || n.getAttribute('role') === 'button');
    if (q === '[aria-label]') return controls.filter(n => Boolean(n.getAttribute('aria-label')));
    return [];
  },
};
const fn = eval('(' + input.js + ')');
const ev = fn(null);
const out = input.verifyTarget ? fn(ev) : null;
process.stdout.write(JSON.stringify({ ev, out, domClicks }));
"""
        account_ctrl = {
            "role": None,
            "ariaLabel": f"Account details: Studio ({TEST_STUDIO_ACCOUNT})",
            "disabled": False,
            "text": "",
        }
        with patch.object(RUNNER, "REQUIRED_ACCOUNT_SHA256", RUNNER.account_sha256(TEST_STUDIO_ACCOUNT)):
            # 1. Balance popup
            res_bal = subprocess.run(
                ["node", "-e", dom_harness],
                input=json.dumps({
                    "js": RUNNER.BALANCE_EVIDENCE_JS,
                    "controls": [account_ctrl],
                    "bodyLines": capture["account_details_popup"]["body_lines"],
                }),
                text=True, capture_output=True, check=True,
            )
            bal_data = json.loads(res_bal.stdout)
            self.assertEqual(bal_data["domClicks"], 0)
            self.assertEqual(
                RUNNER.read_live_balance(
                    type("P", (), {"evaluate": lambda _s, _j, _a=None: bal_data["ev"]})(),
                    open_overlay=False,
                ),
                14890,
            )

            # 2. Video Quality (100) accepted and Fast (10) refused on 10 Nov DOM
            base_video = capture["video_mode_veo31_quality_settings_open"]
            for quality, model_text, price_line in (
                ("Quality", "Veo 3.1 - Quality\narrow_drop_down", "Generating will use 100 credits"),
                ("Fast", "Veo 3.1 - Fast\narrow_drop_down", "Generating will use 10 credits"),
            ):
                ctrls = [account_ctrl]
                for c in base_video["visible_controls"]:
                    copy = dict(c)
                    if copy.get("ariaLabel") == "Select model family":
                        copy["text"] = model_text
                    if "Start generation" in (copy.get("ariaLabel") or copy.get("text") or ""):
                        copy["disabled"] = False
                        copy["isCreate"] = True
                    ctrls.append(copy)
                lines = [
                    price_line if line.startswith("Generating will use ") else line
                    for line in base_video["body_lines"]
                ]
                res_vid = subprocess.run(
                    ["node", "-e", dom_harness],
                    input=json.dumps({
                        "js": RUNNER.CREATE_EVIDENCE_JS,
                        "controls": ctrls,
                        "bodyLines": lines,
                        "verifyTarget": True,
                    }),
                    text=True, capture_output=True, check=True,
                )
                vid_data = json.loads(res_vid.stdout)
                self.assertEqual(vid_data["domClicks"], 0)
                self.assertTrue(vid_data["out"]["ready"])
                self.assertEqual(vid_data["out"]["target"], {"x": 1000, "y": 844})
                page_obj = type("P", (), {"evaluate": lambda _s, _j, _a=None, d=vid_data["ev"]: d})()
                if quality == "Quality":
                    validated = RUNNER.read_live_evidence(
                        page_obj,
                        quality="Quality",
                        balance=14890,
                    )
                    self.assertEqual(validated["models"], ["Veo 3.1 - Quality"])
                    self.assertEqual(validated["prices"], [price_line])
                    self.assertNotIn("accounts", validated)
                else:
                    with self.assertRaisesRegex(RUNNER.GuardError, "Fast is refused"):
                        RUNNER.read_live_evidence(page_obj, quality="Fast", balance=14890)
                    with self.assertRaises(RUNNER.GuardError):
                        RUNNER.read_live_evidence(page_obj, quality="Quality", balance=14890)

            # 3. Still Nano Banana 2.1 @ 0 credits on 10 Nov DOM
            still_state = capture["still_mode_settings_open"]
            still_ctrls = [account_ctrl]
            for c in still_state["visible_controls"]:
                copy = dict(c)
                if "Start generation" in (copy.get("ariaLabel") or copy.get("text") or ""):
                    copy["disabled"] = False
                    copy["isCreate"] = True
                still_ctrls.append(copy)
            res_still = subprocess.run(
                ["node", "-e", dom_harness],
                input=json.dumps({
                    "js": RUNNER.STILL_EVIDENCE_JS,
                    "controls": still_ctrls,
                    "bodyLines": still_state["body_lines"],
                    "verifyTarget": True,
                }),
                text=True, capture_output=True, check=True,
            )
            still_data = json.loads(res_still.stdout)
            self.assertEqual(still_data["domClicks"], 0)
            self.assertTrue(still_data["out"]["ready"])
            validated_still = RUNNER.read_live_still_evidence(
                type("P", (), {"evaluate": lambda _s, _j, _a=None: still_data["ev"]})(),
                balance=14890,
            )
            self.assertEqual(validated_still["models"], ["Nano Banana 2.1"])
            self.assertEqual(validated_still["prices"], ["Generating will use 0 credits"])

    def test_cli_plan_dry_run_detach_and_unarmed_submit_spend_nothing(self):
        env = os.environ.copy()
        env.pop(RUNNER.SUBMIT_ENV, None)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan_out = root / "plan.json"
            proc_plan = subprocess.run(
                [sys.executable, str(SCRIPT), "plan", "--repo", str(ROOT), "--out", str(plan_out)],
                capture_output=True, text=True, env=env,
            )
            self.assertEqual(proc_plan.returncode, 0, proc_plan.stderr)
            plan = json.loads(plan_out.read_text())
            self.assertEqual(plan["row_count"], 66)
            self.assertEqual(plan["quality_count"], 66)
            self.assertEqual(plan["fast_count"], 0)
            self.assertEqual(plan["submissions"], 0)
            self.assertEqual(plan["create_clicks"], 0)
            self.assertIs(plan["keep"], False)

            # Unarmed submit exits non-zero before touching CDP or Playwright.
            proc_sub = subprocess.run(
                [sys.executable, str(SCRIPT), "submit", "--repo", str(ROOT)],
                capture_output=True, text=True, env=env,
            )
            self.assertNotEqual(proc_sub.returncode, 0)
            self.assertIn("refusing submit", proc_sub.stderr + proc_sub.stdout)
            self.assertNotIn("connect_over_cdp", proc_sub.stderr + proc_sub.stdout)

            # detach-command prints tmux command without starting anything.
            cmd = RUNNER.detached_command(
                SCRIPT, root / "run.log", root / "run.done",
                repo=ROOT, media=root, archive=root, other=6000,
                ledger=root / "ledger.jsonl", lock=root / "writer.lock", pid=root / "runner.pid",
            )
            self.assertEqual(cmd[:4], ["tmux", "new", "-d", "-s"])
            parsed = shlex.split(cmd[-1])
            self.assertEqual(parsed[2], "launch-worker")
            self.assertFalse((root / "run.log").exists())
            self.assertFalse((root / "run.done").exists())

    def test_live_adapters_unarmed_refusal_and_shared_reservation_boundary(self):
        from types import ModuleType

        rows = RUNNER.load_scope(ROOT)
        q_row = next(r for r in rows if r.quality == "Quality")

        env = os.environ.copy()
        env.pop(RUNNER.SUBMIT_ENV, None)
        with patch.dict(os.environ, env, clear=True):
            with self.assertRaisesRegex(RUNNER.GuardError, "not armed"):
                RUNNER.live_batch_price_reader()
            with self.assertRaisesRegex(RUNNER.GuardError, "not armed"):
                RUNNER.live_still_maker(q_row, Path("/tmp/x.png"), repo=ROOT, media=Path("/tmp"))
            with tempfile.TemporaryDirectory() as tmp:
                with RUNNER.SharedFlowAccounting(Path(tmp)) as acc:
                    with self.assertRaisesRegex(RUNNER.GuardError, "not armed"):
                        RUNNER.live_video_submit(
                            q_row, Path(tmp) / "out.mp4", Path(tmp) / "frame.png",
                            accounting=acc, reservation="HOS013_PASS1", charge="c1",
                            evidence_path=Path(tmp) / "ev.json",
                        )

        # Armed live_video_submit exercises create_guard, trusted click, and post-take balance delta check.
        with patch.object(RUNNER, "REQUIRED_ACCOUNT_SHA256", RUNNER.account_sha256(TEST_STUDIO_ACCOUNT)):
            for row, drop, should_pass in ((q_row, 100, True), (q_row, 200, False)):
                with self.subTest(row=row.row_id, drop=drop), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    frame = make_png(root / "frame.png")
                    out_mp4 = root / "out.mp4"
                    ev_data = self.video_evidence(quality=row.quality, account=TEST_STUDIO_ACCOUNT, balance=14890)
                    page = self.MockPage(
                        ev_data,
                        on_mouse_click=lambda *_: ev_data.update(balances=[14890 - drop]),
                    )

                    fake_flow = ModuleType("orbit_flow_veo_ui")
                    fake_flow.FLOW_HOME = "https://flow.google.com/"

                    def fake_generate_clip(p, prompt, dest, *, model, timeout_s, start_frame, attempts, reuse_project, create_guard):
                        self.assertEqual(attempts, 1)
                        self.assertEqual(model, RUNNER.expected_model_for(row))
                        create_guard(p)
                        dest.write_bytes(b"video")
                        return {"ok": True}

                    fake_flow.generate_clip = fake_generate_clip
                    fake_pw = ModuleType("playwright.sync_api")
                    ctx = MagicMock()
                    ctx.__enter__.return_value.chromium.connect_over_cdp.return_value = Mock()
                    fake_pw.sync_playwright = lambda: ctx

                    with RUNNER.SharedFlowAccounting(root / "state") as acc, \
                         patch.dict(os.environ, {RUNNER.SUBMIT_ENV: "1"}), \
                         patch.dict(sys.modules, {"orbit_flow_veo_ui": fake_flow, "playwright.sync_api": fake_pw}), \
                         patch.object(RUNNER, "open_flow_page", return_value=page):
                        if should_pass:
                            ev = RUNNER.live_video_submit(
                                row, out_mp4, frame, accounting=acc,
                                reservation="HOS013_PASS1", charge="chg",
                                evidence_path=root / "create.json", other=6000,
                            )
                            self.assertEqual(page.clicks, 1)
                            self.assertEqual(ev["charge"], "chg")
                            self.assertTrue(acc.snapshot()["charges"]["chg"]["posted"])
                        else:
                            with self.assertRaisesRegex(RUNNER.GuardError, "dropped by 200"):
                                RUNNER.live_video_submit(
                                    row, out_mp4, frame, accounting=acc,
                                    reservation="HOS013_PASS1", charge="chg",
                                    evidence_path=root / "create.json", other=6000,
                                )



class DetachedFloorTests(unittest.TestCase):
    def test_floor_survives_printed_command_and_launch_worker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cli = ["detach-command", "--repo", str(ROOT), "--media", str(root),
                   "--archive", str(root), "--other-reservations", "0",
                   "--ledger", str(root / "ledger.jsonl"),
                   "--lock", str(root / "writer.lock"),
                   "--pid", str(root / "runner.pid"),
                   "--log", str(root / "run.log"), "--done", str(root / "run.done")]
            for explicit in ([], ["--floor", "3000"], ["--floor", "3500"]):
                expected = explicit[-1] if explicit else "3000"
                with self.subTest(floor=expected):
                    from io import StringIO
                    output = StringIO()
                    with patch("sys.stdout", output), patch.object(RUNNER, "runner_state_dir", return_value=root):
                        self.assertEqual(RUNNER.main(cli + explicit), 0)
                    launch = shlex.split(json.loads(output.getvalue())[-1])
                    self.assertEqual(launch[launch.index("--floor") + 1], expected)
                    with patch.object(RUNNER, "runner_state_dir", return_value=root), patch.object(RUNNER, "launch_once", return_value=0) as owner:
                        self.assertEqual(RUNNER.main(launch[2:]), 0)
                    child = owner.call_args.args[0]
                    self.assertEqual(child[2], "submit")
                    self.assertEqual(child[child.index("--floor") + 1], expected)
                    self.assertNotIn("--log", child)
            self.assertEqual(list(root.iterdir()), [])

    def test_detached_floor_rejects_insufficient_reservation_and_accepts_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            command = RUNNER.detached_command(
                SCRIPT, root / "run.log", root / "run.done", repo=ROOT,
                media=root, archive=root, other=0, floor=3000,
                ledger=root / "ledger.jsonl", lock=root / "writer.lock", pid=root / "runner.pid")
            args = shlex.split(command[-1])
            floor = int(args[args.index("--floor") + 1])
            with RUNNER.SharedFlowAccounting(root / "accounting") as account:
                before = account.snapshot()
                with self.assertRaisesRegex(RUNNER.GuardError, "insufficient shared Flow headroom"):
                    account.reserve("test", RUNNER.FILM_ID, 6600, live=9599, floor=floor)
                self.assertEqual(account.snapshot(), before)
                account.reserve("test", RUNNER.FILM_ID, 6600, live=9600, floor=floor)
                self.assertEqual(account.snapshot()["liability"], 6600)
                with self.assertRaisesRegex(RUNNER.GuardError, "insufficient shared Flow headroom"):
                    account.reserve("test", RUNNER.FILM_ID, 6600, live=9599, floor=floor)

    def test_armed_submit_without_floor_refuses_reservation_under_3000(self):
        """Direct armed `submit` (no --floor) keeps the 3,000 headroom, same as detach."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seen = {}

            def fake_execute(batch, **kwargs):
                seen["floor"] = kwargs["floor"]
                with RUNNER.SharedFlowAccounting(root / "accounting") as account:
                    before = account.snapshot()
                    try:
                        account.reserve(
                            "direct-submit",
                            RUNNER.FILM_ID,
                            RUNNER.MAX_TOTAL_CREDITS,
                            live=9599,
                            floor=kwargs["floor"],
                        )
                    except RUNNER.GuardError:
                        seen["unchanged"] = account.snapshot() == before
                        raise
                return []

            argv = [
                "submit",
                "--repo", str(ROOT),
                "--media", str(root),
                "--other-reservations", "0",
                "--ledger", str(root / "ledger.jsonl"),
                "--lock", str(root / "writer.lock"),
                "--pid", str(root / "runner.pid"),
                "--done", str(root / "runner.done"),
            ]
            self.assertNotIn("--floor", argv)
            with patch.dict(os.environ, {RUNNER.SUBMIT_ENV: "1"}), \
                 patch.object(RUNNER, "execute_shared_batch", side_effect=fake_execute):
                with self.assertRaisesRegex(RUNNER.GuardError, "insufficient shared Flow headroom"):
                    RUNNER.main(argv)
            self.assertEqual(seen["floor"], RUNNER.DETACHED_HEADROOM_FLOOR)
            self.assertTrue(seen["unchanged"])

    def test_armed_submit_refuses_floor_below_3000_and_holds_9599_9600_boundary(self):
        """An explicit floor under 3,000 never reserves. Floor 3,000 refuses 9,599 and accepts 9,600."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = [
                "submit",
                "--repo", str(ROOT),
                "--media", str(root),
                "--other-reservations", "0",
                "--ledger", str(root / "ledger.jsonl"),
                "--lock", str(root / "writer.lock"),
                "--pid", str(root / "runner.pid"),
                "--done", str(root / "runner.done"),
            ]
            with patch.object(RUNNER, "execute_shared_batch") as execute:
                with patch.dict(os.environ, {RUNNER.SUBMIT_ENV: "0"}, clear=False):
                    with self.assertRaises(SystemExit) as unarmed:
                        RUNNER.main(base + ["--floor", "0"])
                self.assertIn("not armed", str(unarmed.exception))
                with patch.dict(os.environ, {RUNNER.SUBMIT_ENV: "1"}):
                    for low in ("0", "2999"):
                        with self.subTest(floor=low):
                            with self.assertRaisesRegex(RUNNER.GuardError, "armed submit floor below 3000"):
                                RUNNER.main(base + ["--floor", low])
                execute.assert_not_called()
            self.assertEqual(list(root.iterdir()), [])

            seen = []

            def fake_execute(batch, **kwargs):
                floor = kwargs["floor"]
                seen.append(floor)
                with RUNNER.SharedFlowAccounting(root / f"accounting-{len(seen)}") as account:
                    before = account.snapshot()
                    with self.assertRaisesRegex(RUNNER.GuardError, "insufficient shared Flow headroom"):
                        account.reserve(
                            "direct-submit", RUNNER.FILM_ID, RUNNER.MAX_TOTAL_CREDITS,
                            live=9599, floor=floor)
                    self.assertEqual(account.snapshot(), before)
                    account.reserve(
                        "direct-submit", RUNNER.FILM_ID, RUNNER.MAX_TOTAL_CREDITS,
                        live=9600, floor=floor)
                    self.assertEqual(account.snapshot()["liability"], RUNNER.MAX_TOTAL_CREDITS)
                return []

            with patch.dict(os.environ, {RUNNER.SUBMIT_ENV: "1"}), \
                 patch.object(RUNNER, "execute_shared_batch", side_effect=fake_execute):
                self.assertEqual(RUNNER.main(base), 0)
                self.assertEqual(RUNNER.main(base + ["--floor", "3000"]), 0)
            self.assertEqual(seen, [RUNNER.DETACHED_HEADROOM_FLOOR, RUNNER.DETACHED_HEADROOM_FLOOR])

    def test_dry_run_floor_stays_at_zero(self):
        captured = {}

        def fake_dry_run(repo, *, media, archive_dir, other, floor, out):
            captured["floor"] = floor
            return {}

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.object(RUNNER, "cmd_dry_run", side_effect=fake_dry_run):
                self.assertEqual(RUNNER.main([
                    "dry-run", "--repo", str(ROOT), "--media", str(root), "--archive", str(root),
                ]), 0)
        self.assertEqual(captured["floor"], 0)
        self.assertIs(captured["floor"], RUNNER.HEADROOM_FLOOR)

    def test_negative_detached_floor_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaisesRegex(RUNNER.GuardError, "invalid detached floor"):
                RUNNER.detached_command(
                    SCRIPT, root / "run.log", root / "run.done", repo=ROOT,
                    media=root, archive=root, other=0, floor=-1,
                    ledger=root / "ledger.jsonl", lock=root / "writer.lock", pid=root / "runner.pid")


class PolicyRefusalTests(unittest.TestCase):
    """A take Flow refuses under its content policy costs nothing, and pass 1 goes on without the row.

    Chief ruling, desk 6785808071 item 4: 013 gets the same handling as 009 before its first submit.
    Pass 1 allows one take per row, so a refused row is set aside for the picture review.
    """

    EVIDENCE = {"desk": "HOS #180 6785808071", "balance_before": 13490, "balance_live": 13490, "outputs": 0}

    @classmethod
    def setUpClass(cls):
        cls.rows = RUNNER.load_scope(ROOT)
        cls.batch1 = RUNNER.batch_rows(cls.rows)[0]
        cls.first = cls.batch1[0]
        cls.key = f"{RUNNER.FILM_ID}:P{cls.first.part:02d}:{cls.first.plate_id}:t1"

    def refused_state(self, root: Path) -> tuple[Path, Path]:
        """A pass ledger and a shared ledger in which the first row's take was clicked and then refused."""
        ledger, state = root / "ledger.jsonl", root / "shared"
        waiting = RUNNER.submitting_record(self.first, 1, root / "media" / "t1.mp4")
        waiting["shared_charge"] = self.key
        RUNNER.append_ledger(ledger, waiting)
        with RUNNER.SharedFlowAccounting(state) as account:
            account.reserve(RUNNER.DEFAULT_RESERVATION, RUNNER.FILM_ID, RUNNER.MAX_TOTAL_CREDITS, live=14890)
            account.intent(self.key, RUNNER.DEFAULT_RESERVATION, self.first.try1_credits, live=14890)
            account.resolve(self.key, submitted=True, evidence={"ui": {"balances": [14890]}})
        return ledger, state

    def reconcile(self, root: Path, ledger: Path, state: Path, **over):
        args = dict(accounting_state=state, ledger_path=ledger, lock_path=root / "writer.lock", key=self.key,
                    plate_id=self.first.plate_id, part=self.first.part, take=1,
                    reason="Flow policy: prominent people", evidence=self.EVIDENCE)
        args.update(over)
        return RUNNER.reconcile_policy_refusal(**args)

    def test_a_refused_take_costs_nothing_and_uses_the_rows_one_take(self):
        waiting = RUNNER.submitting_record(self.first, 1, Path("x.mp4"))
        closed = RUNNER.policy_refusal_record(self.first.row_id, self.first.plate_id, self.first.part, 1,
                                              reason="Flow policy: prominent people", evidence=self.EVIDENCE)
        spent, pending, unknown, takes = RUNNER.ledger_totals([waiting, closed])
        self.assertEqual((spent, pending, unknown), (0, 0, False))
        self.assertEqual(takes[self.first.row_id], RUNNER.MAX_TAKES_PER_ROW)
        for bad in ({"credits_used": 100}, {"credits_used": None}, {"credits_used": False}, {"reason": " "}):
            with self.subTest(bad=bad), self.assertRaises(RUNNER.GuardError):
                RUNNER.ledger_totals([{**closed, **bad}])
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.policy_refusal_record(self.first.row_id, self.first.plate_id, self.first.part, 1,
                                         reason="", evidence=self.EVIDENCE)

    def test_reconcile_closes_both_ledgers_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger, state = self.refused_state(root)
            before = ((state / "account.jsonl").read_bytes(), ledger.read_bytes())
            self.assertEqual(self.reconcile(root, ledger, state),
                             {"shared_appended": True, "pass_appended": True, "refused_rows": [self.first.row_id]})
            once = ((state / "account.jsonl").read_bytes(), ledger.read_bytes())
            self.assertEqual(self.reconcile(root, ledger, state),
                             {"shared_appended": False, "pass_appended": False, "refused_rows": [self.first.row_id]})
            self.assertEqual(((state / "account.jsonl").read_bytes(), ledger.read_bytes()), once)
            # History is added to, never written over.
            self.assertTrue(once[0].startswith(before[0]))
            self.assertTrue(once[1].startswith(before[1]))
            entries = RUNNER.read_ledger(ledger)
            self.assertEqual([e["status"] for e in entries], ["SUBMITTING", "FAILED_POLICY"])
            self.assertEqual(entries[-1]["shared_charge"], self.key)
            self.assertEqual(RUNNER.ledger_totals(entries)[:3], (0, 0, False))
            snap = RUNNER.SharedFlowAccounting.peek_readonly(state)
            self.assertEqual((snap["charges"][self.key]["status"], snap["charges"][self.key]["amount"]),
                             ("POLICY_REFUSED", 0))
            self.assertFalse(snap["pending"])

    def test_reconcile_refuses_the_wrong_take_or_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger, state = self.refused_state(root)
            before = ((state / "account.jsonl").read_bytes(), ledger.read_bytes())
            second = self.batch1[1]
            for over in ({"key": self.key.replace(":t1", ":t2")},                       # not this take's charge
                         {"plate_id": second.plate_id, "part": second.part},            # another row
                         {"take": 2},
                         {"evidence": {}}):
                with self.subTest(over=over), self.assertRaises(RUNNER.GuardError):
                    self.reconcile(root, ledger, state, **over)
            self.assertEqual(((state / "account.jsonl").read_bytes(), ledger.read_bytes()), before)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger, state = self.refused_state(root)
            delivered = RUNNER.submitting_record(self.first, 1, root / "x.mp4")
            delivered.update(status="PENDING_REVIEW", file_state="GENERATED", credits_used=self.first.try1_credits)
            RUNNER.append_ledger(ledger, delivered)
            with self.assertRaises(RUNNER.GuardError):
                self.reconcile(root, ledger, state)                                      # a delivered take
            snap = RUNNER.SharedFlowAccounting.peek_readonly(state)
            self.assertEqual(snap["charges"][self.key]["status"], "CHARGED")

    def test_a_refused_take_number_is_never_used_again(self):
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp)
            entries = [RUNNER.submitting_record(self.first, 1, media / "x.mp4")]
            self.assertEqual(RUNNER.takes_recorded(entries, self.first.row_id), {1})
            self.assertEqual(RUNNER.takes_recorded(entries, self.batch1[1].row_id), set())
            # Going by files alone the row would be numbered take 1 again; the ledger says it is used.
            self.assertEqual(RUNNER.next_version(media, self.first.part, self.first.plate_id)[0], 1)
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.next_version(media, self.first.part, self.first.plate_id, {1})

    def test_next_batch_sets_a_refused_row_aside_and_goes_on(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger, state = self.refused_state(root)
            ordered = RUNNER.order_rows(self.rows)
            # Until it is reconciled the row is still first in line (and the batch guard stops on it).
            self.assertEqual(RUNNER.next_batch(self.rows, RUNNER.read_ledger(ledger))[0].row_id, self.first.row_id)
            self.reconcile(root, ledger, state)
            entries = RUNNER.read_ledger(ledger)
            self.assertEqual(RUNNER.refused_rows(entries), [self.first.row_id])
            batch = RUNNER.next_batch(self.rows, entries)
            self.assertNotIn(self.first.row_id, [r.row_id for r in batch])
            self.assertEqual(batch[0].row_id, ordered[1].row_id)
            RUNNER.assert_batch_limits(batch)

    def test_the_batch_after_a_refusal_runs_and_leaves_the_refused_row_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            media, archive = root / "media", root / "archive"
            archive.mkdir()
            populate_media_style_refs(media)
            sample_mp4 = make_silent_mp4(root / "fixture.mp4")
            ledger, state = self.refused_state(root)
            self.reconcile(root, ledger, state)
            charges = []

            def fake_still_maker(row, dest, *, repo, media, accounting, reservation, evidence_path, other=0, floor=0):
                make_png(dest, width=1280, height=720, color=f"0x{row.index:02x}4466")
                RUNNER.immutable_bytes(
                    evidence_path,
                    (json.dumps({"row_id": row.row_id, "credits": 0, "ui": {"balances": [14890]}}) + "\n").encode())
                return dest

            def fake_submitter(row, dest, frame, *, accounting, reservation, charge, evidence_path, other=0, floor=0):
                charges.append(charge)
                page = LiveDomAndTrustedClickTests.MockPage(
                    LiveDomAndTrustedClickTests.video_evidence(quality=row.quality, account=TRANCHE2.REQUIRED_ACCOUNT, balance=14890))
                accounting.reserve(reservation, RUNNER.FILM_ID, RUNNER.MAX_TOTAL_CREDITS, live=14890, floor=floor + other)
                ev = RUNNER.guarded_create(page, accounting, row=row, reservation=reservation, charge=charge,
                                           evidence_path=evidence_path, floor=floor + other)
                shutil.copy2(sample_mp4, dest)
                return ev

            with patch.dict(os.environ, {RUNNER.SUBMIT_ENV: "1"}):
                written = RUNNER.cmd_submit(
                    ROOT, other=0, media=media, ledger_path=ledger, lock_path=root / "writer.lock",
                    pid_path=root / "runner.pid", done_path=root / "runner.done", archive_dir=archive,
                    accounting_state=state, spend_ledger=root / "ai_spend.jsonl",
                    batch_price_reader=make_batch_prices, submitter=fake_submitter,
                    still_maker=fake_still_maker, test_archive=True)

            expected = [r.row_id for r in RUNNER.next_batch(self.rows, RUNNER.read_ledger(ledger)[:2])]
            self.assertEqual([e["row_id"] for e in written], expected)
            self.assertNotIn(self.first.row_id, expected)
            self.assertNotIn(self.key, charges)
            self.assertTrue(all(c.endswith(":t1") for c in charges))
            latest = {(e["row_id"], e["take"]): e["status"] for e in RUNNER.read_ledger(ledger)}
            self.assertEqual(latest[(self.first.row_id, 1)], "FAILED_POLICY")        # the refusal still stands
            self.assertEqual(RUNNER.refused_rows(RUNNER.read_ledger(ledger)), [self.first.row_id])
            # The refused take is not in the spend report: it was never exported, so nothing is taken back.
            spends = [json.loads(l) for l in (root / "ai_spend.jsonl").read_text().splitlines()]
            self.assertEqual(sum(r["amount"] for r in spends if r["kind"] == "spend"),
                             sum(e["credits_used"] for e in written))
            self.assertFalse(any(self.key in json.dumps(r) for r in spends))

    def test_the_command_closes_a_refused_take(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger, state = self.refused_state(root)
            evidence = root / "evidence.json"
            evidence.write_text(json.dumps(self.EVIDENCE))
            code = RUNNER.main(["reconcile-policy-refusal", "--key", self.key, "--plate", self.first.plate_id,
                                "--part", str(self.first.part), "--reason", "Flow policy: prominent people",
                                "--evidence", str(evidence), "--accounting-state", str(state),
                                "--ledger", str(ledger), "--lock", str(root / "writer.lock")])
            self.assertEqual(code, 0)
            self.assertEqual(RUNNER.read_ledger(ledger)[-1]["status"], "FAILED_POLICY")


class NoNameWordingTests(unittest.TestCase):
    """Chief ruling, desk 6785808071 item 4: no prompt sent to Flow names a real person."""

    RECORD = ROOT / "jobs/reviews/J2529/PROMPT_CHANGE_2026-11-11.json"
    # Later changes to the same prompts, in order. Each one's `old` is the wording the one before left.
    LATER = [ROOT / "jobs/reviews/J2529/PROMPT_CHANGE_2026-11-11_beard.json"]
    NAMES = ("Darwin", "Wallace", "Lawson", "Gould", "Lyell", "Hooker", "Murray", "Jenkin", "Mendel", "Charles",
             "Emma", "Alfred", "Russel", "Nicholas", "Joseph", "Fleeming", "Gregor", "FitzRoy", "Malthus", "Huxley",
             "Owen", "Henslow")

    @classmethod
    def setUpClass(cls):
        cls.rows = RUNNER.load_scope(ROOT)
        cls.record = json.loads(cls.RECORD.read_text())
        cls.later = [json.loads(path.read_text()) for path in cls.LATER]
        # The wording each changed row should hold now: the newest record that touches it.
        cls.current = {}
        for record in [cls.record] + cls.later:
            for change in record["rows"]:
                cls.current[change["row_id"]] = change["new"]

    def test_no_prompt_of_the_71_names_a_real_person(self):
        import re
        self.assertEqual(len(self.rows), RUNNER.EXPECTED_ROW_COUNT)
        for row in self.rows:
            with self.subTest(row=row.row_id):
                for name in self.NAMES:
                    self.assertIsNone(re.search(rf"\b{name}\b", row.prompt), name)

    def test_the_record_matches_the_boards_and_only_those_rows_changed(self):
        prompts = {row.row_id: row.prompt for row in self.rows}
        self.assertEqual(len(self.record["rows"]), self.record["rows_changed"])
        self.assertEqual(self.record["rows_total"], 71)
        self.assertEqual(len(self.rows), RUNNER.EXPECTED_ROW_COUNT)
        for change in self.record["rows"]:
            with self.subTest(row=change["row_id"]):
                self.assertEqual(prompts[change["row_id"]], self.current[change["row_id"]])
                self.assertNotEqual(change["old"], change["new"])
                # The fixed opening and closing of the prompt are untouched.
                self.assertEqual(change["old"][:36], change["new"][:36])
                self.assertEqual(change["old"][-80:], change["new"][-80:])
        # Each later record starts from the wording the one before left, and the newest pins the boards as they are.
        left = {change["row_id"]: change["new"] for change in self.record["rows"]}
        boards = dict(self.record["boards"])
        for record in self.later:
            for change in record["rows"]:
                with self.subTest(later=record["ruling"], row=change["row_id"]):
                    self.assertEqual(change["old"], left[change["row_id"]])
                    self.assertEqual(change["old"][:36], change["new"][:36])
                    self.assertEqual(change["old"][-80:], change["new"][-80:])
                    left[change["row_id"]] = change["new"]
            for part, meta in record["boards"].items():
                self.assertEqual(meta["sha256_old"], boards[part]["sha256_new"], part)
                boards[part] = meta
        for part, meta in boards.items():
            self.assertEqual(RUNNER.sha256_file(ROOT / meta["path"]), meta["sha256_new"], part)

    def test_before_1862_the_naturalist_of_down_house_is_not_bearded(self):
        # Chief ruling, desk 6786709657 item 1. With the name out of the prompt the description is the likeness.
        prompts = {row.row_id: row.prompt for row in self.rows}
        for row_id in ("P4:08_midpoint_twist_packet", "P4:09a_darwin_reads_wallace", "P5:05a_darwin_writes_origin"):
            with self.subTest(row=row_id):
                self.assertNotIn("bearded", prompts[row_id])
                self.assertIn("clean-shaven with long greying side whiskers", prompts[row_id])
        split = prompts["P1:09_wallace_hut_split"]
        left, right = split.split("; on the right, ")
        self.assertIn("clean-shaven with long greying side whiskers", left)     # Down House, June 1858
        self.assertNotIn("bearded", left)
        self.assertIn("bearded field naturalist", right)                        # the other man, in the hut
        # After 1866 he was bearded: the row with the uncut 1866 journal on the shelf keeps it.
        self.assertIn("older bearded English naturalist", prompts["P5:10_darwin_worried_shelf"])

    def test_the_builder_holds_the_same_wording(self):
        # The boards are written by the builder. If it kept the old wording, the next rebuild would
        # bring the names back (and the scope would refuse the boards).
        for builder_name in ("_build_picture_plan_v01.py", "_build_picture_plan_v02.py"):
            source = (EDIT / builder_name).read_text()
            for record in [self.record] + self.later:
                for change in record["rows"]:
                    with self.subTest(builder=builder_name, row=change["row_id"]):
                        self.assertIn(json.dumps(self.current[change["row_id"]], ensure_ascii=False), source)
                        self.assertNotIn(json.dumps(change["old"], ensure_ascii=False), source)


if __name__ == "__main__":
    unittest.main()
