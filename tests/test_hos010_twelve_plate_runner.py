"""HOS 010 Alvarez clay line twelve-plate Flow adapter tests (J2268).

All tests run offline against local fixtures and Node DOM harnesses. They never
open Chrome/CDP, never click Create on a real page, never modify NAS media, and
spend 0 credits (£0).
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
from types import ModuleType
from unittest.mock import MagicMock, Mock, patch

ROOT = Path(__file__).resolve().parents[1]
FILM_DIR = ROOT / "02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs"
EDIT_DIR = FILM_DIR / "07_Edit-Project"
SHORTS_DIR = FILM_DIR / "10_Shorts"
SCRIPT = EDIT_DIR / "_mint_flow_twelve_plates_j2268.py"
TRANCHE2_SCRIPT = ROOT / "02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/_mint_flow_v05_tranche2.py"
CAPTURE_PATH = ROOT / "jobs/reviews/J2033/LIVE_DOM_CAPTURE_2026-11-10.json"

# Construct synthetic test account tokens at runtime without embedding literal email strings.
AT_SIGN = chr(64)
TEST_STUDIO_ACCOUNT = f"studio-ultra{AT_SIGN}example.invalid"
TEST_FORBIDDEN_ACCOUNT = f"wrong-channel{AT_SIGN}example.invalid"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


RUNNER = _load_module("hos010_twelve_plate_runner", SCRIPT)
TRANCHE2 = _load_module("hos009_tranche2_ref_for_010", TRANCHE2_SCRIPT)


def make_price(
    quality: str = "Quality",
    *,
    credits: int = 100,
    model: str = "Veo 3.1 - Quality",
    outputs: str = "x1",
    aspect: str = "16:9",
    duration: str = "8s",
    line: str | None = None,
    read_at: str | None = None,
):
    return RUNNER.PriceEvidence(
        quality=quality,
        model=model,
        outputs=outputs,
        aspect=aspect,
        duration=duration,
        credits=credits,
        generate_line=line if line is not None else f"Generating will use {credits} credits",
        read_at=read_at if read_at is not None else datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )


def make_batch_prices(**overrides) -> dict[str, object]:
    out: dict[str, object] = {"Quality": make_price("Quality")}
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


def make_temp_010_repo(test_case: unittest.TestCase) -> Path:
    """Copy only the lightweight JSON/ref manifests of HOS 010 into a temp directory for mutation tests."""
    tmp = tempfile.TemporaryDirectory()
    test_case.addCleanup(tmp.cleanup)
    repo = Path(tmp.name)
    (repo / "AGENTS.md").write_text("# test\n")
    for rel in (
        RUNNER.SCOPE_REL,
        RUNNER.RECONCILIATION_REL,
        RUNNER.SHORTS_PLAN_REL,
        RUNNER.LONG_PLAN_REL,
        RUNNER.VO_KEEP_REL,
        RUNNER.EXPLORER_REF_REL,
        Path("02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/07_Edit-Project/parts/part-01_plates_v03.json"),
        Path("02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/07_Edit-Project/parts/part-02_plates_v03.json"),
        Path("02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/07_Edit-Project/parts/part-03_plates_v03.json"),
        Path("02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/07_Edit-Project/parts/part-04_plates_v03.json"),
        Path("02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/07_Edit-Project/parts/part-05_plates_v04.json"),
    ):
        dst = repo / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    return repo


def write_auth_file(
    dest: Path,
    *,
    repo: Path = ROOT,
    cap: int = 3600,
    floor: int = 3000,
    j2033_done: bool = True,
    authorized: bool = True,
    job: str = "J2269",
    film: str = "HOS:010",
    scope_sha256: str | None = None,
) -> Path:
    payload = {
        "job": job,
        "film": film,
        "generation_authorized": authorized,
        "j2033_done": j2033_done,
        "scope_sha256": scope_sha256 or RUNNER.sha256_file(repo / RUNNER.SCOPE_REL),
        "authorized_cap_credits": cap,
        "minimum_headroom_floor": floor,
    }
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2) + "\n")
    return dest


class ScopeVoAndAuthorizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = RUNNER.load_scope(ROOT)

    def test_exact_12_quality_rows_order_and_5_5_2_batches(self):
        self.assertEqual(len(self.rows), 12)
        self.assertEqual(tuple(r.row_id for r in self.rows), RUNNER.EXPECTED_ROW_IDS)
        self.assertTrue(all(r.quality == "Quality" and r.flow_model == "Veo 3.1 - Quality" for r in self.rows))
        self.assertTrue(all(r.flow_clip_s == 8 and r.try1_credits == 100 and r.max_takes == 3 for r in self.rows))
        self.assertEqual(sum(r.try1_credits for r in self.rows), 1200)
        self.assertEqual(sum(r.planning_cap for r in self.rows), 3600)

        shared_rows = [r for r in self.rows if not r.shorts_only]
        shorts_only_rows = [r for r in self.rows if r.shorts_only]
        self.assertEqual(len(shared_rows), 10)
        self.assertTrue(all(r.t_s is not None for r in shared_rows))
        self.assertEqual([r.row_id for r in shorts_only_rows], ["P5:09a_pigeon_pavement", "P5:13a_gull_seaside"])
        self.assertTrue(all(r.t_s is None for r in shorts_only_rows))

        exp_rows = [r for r in self.rows if r.explorer]
        self.assertEqual([r.row_id for r in exp_rows], ["P5:10_explorer_robin"])
        self.assertEqual(exp_rows[0].reference, "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg")
        for use in exp_rows[0].uses:
            self.assertNotEqual(use["id"], "S01")
            self.assertGreater(use["t_start_s"], 0.0)

        ordered = RUNNER.order_rows(list(reversed(self.rows)))
        self.assertEqual([r.row_id for r in ordered], list(RUNNER.EXPECTED_ROW_IDS))

        batches = RUNNER.batch_rows(self.rows)
        self.assertEqual([len(b) for b in batches], [5, 5, 2])
        self.assertEqual([sum(r.try1_credits for r in b) for b in batches], [500, 500, 200])
        self.assertEqual([sum(r.planning_cap for r in b) for b in batches], [1500, 1500, 600])

        # >5 rows or >1500 credits or out-of-order batch refused.
        with self.assertRaisesRegex(RUNNER.GuardError, "MAX_BATCH_ROWS"):
            RUNNER.assert_batch_limits(self.rows[:6])
        with self.assertRaisesRegex(RUNNER.GuardError, "canonical row order"):
            RUNNER.assert_batch_limits([self.rows[1], self.rows[0]])
        with patch.object(RUNNER, "MAX_BATCH_ROWS", 10):
            with self.assertRaisesRegex(RUNNER.GuardError, "batch cap"):
                RUNNER.assert_batch_limits(self.rows[:6])

    def test_no_auto_keep_no_legacy_runner_and_no_emails_in_source(self):
        email_pattern = rf"[A-Za-z0-9._%+-]+{AT_SIGN}[A-Za-z0-9.-]+\.[A-Za-z]{{2,}}"
        src = SCRIPT.read_text()
        test_src = Path(__file__).read_text()
        self.assertNotRegex(src, email_pattern)
        self.assertNotRegex(test_src, email_pattern)
        self.assertNotRegex(src, r"(import|spec_from_file_location|load_mod).*tranche1")
        self.assertNotRegex(src, r"['\"]status['\"]\s*:\s*['\"]KEEP['\"]")
        self.assertIn("reuse_page", src)

    def test_vo_and_option_a1_verification_catches_drift_and_corrupt_audio(self):
        report = RUNNER.verify_vo_and_option_a1(ROOT)
        self.assertTrue(report["option_a1_verified"])
        self.assertAlmostEqual(report["option_a1_silence_sum_s"], 0.26, places=6)

        # 1. Tamper Option A1 hook speed > 1.06 in SHORTS_PICTURE_PLAN_v03.json -> refused.
        repo1 = make_temp_010_repo(self)
        sp_path = repo1 / RUNNER.SHORTS_PLAN_REL
        sp = json.loads(sp_path.read_text())
        sp["shorts"][0]["assembly_audio_recipe"]["hook_atempo"] = 1.08
        sp_path.write_text(json.dumps(sp))
        with self.assertRaisesRegex(RUNNER.GuardError, "Option A1"):
            RUNNER.verify_vo_and_option_a1(repo1)

        # 2. Tamper Option A1 silence interval -> refused.
        repo2 = make_temp_010_repo(self)
        sp2_path = repo2 / RUNNER.SHORTS_PLAN_REL
        sp2 = json.loads(sp2_path.read_text())
        sp2["shorts"][0]["assembly_audio_recipe"]["silence_removals_s"][0] = [0.0, 0.12]
        sp2_path.write_text(json.dumps(sp2))
        with self.assertRaisesRegex(RUNNER.GuardError, "silence"):
            RUNNER.verify_vo_and_option_a1(repo2)

        # 3. Tamper Short_C VO sha256 on disk in media -> refused.
        with tempfile.TemporaryDirectory() as media_tmp:
            media = Path(media_tmp)
            bad_mp3 = media / "10_Shorts/vo_v02/hos_010_short_C_v02.mp3"
            bad_mp3.parent.mkdir(parents=True, exist_ok=True)
            bad_mp3.write_bytes(b"corrupted-vo-bytes")
            with self.assertRaisesRegex(RUNNER.GuardError, "Short VO sha256 mismatch"):
                RUNNER.verify_vo_and_option_a1(ROOT, media)

        # 4. Require audio files when media lacks them -> refused.
        repo3 = make_temp_010_repo(self)
        with tempfile.TemporaryDirectory() as empty_media:
            with self.assertRaisesRegex(RUNNER.GuardError, "missing required accepted Short VO"):
                RUNNER.verify_vo_and_option_a1(repo3, Path(empty_media), require_audio_files=True)

    def test_scope_drift_refused_across_plans_boards_prompts_explorer_and_shorts_only(self):
        # 1. Board sha256 mismatch
        repo = make_temp_010_repo(self)
        sc = json.loads((repo / RUNNER.SCOPE_REL).read_text())
        sc["rows"][0]["source_board_sha256"] = "0" * 64
        (repo / RUNNER.SCOPE_REL).write_text(json.dumps(sc))
        with self.assertRaisesRegex(RUNNER.GuardError, "sha256 mismatch"):
            RUNNER.load_scope(repo)

        # 2. Prompt edited on board (even if board sha256 updated in reconciliation + scope)
        repo = make_temp_010_repo(self)
        b1_rel = Path("02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/07_Edit-Project/parts/part-01_plates_v03.json")
        b1 = json.loads((repo / b1_rel).read_text())
        b1["plates"][0]["prompt"] += " Extra unapproved words."
        (repo / b1_rel).write_text(json.dumps(b1))
        new_sha = RUNNER.sha256_file(repo / b1_rel)
        recon = json.loads((repo / RUNNER.RECONCILIATION_REL).read_text())
        recon["parts"][0]["sha256"] = new_sha
        (repo / RUNNER.RECONCILIATION_REL).write_text(json.dumps(recon))
        sc = json.loads((repo / RUNNER.SCOPE_REL).read_text())
        sc["rows"][0]["source_board_sha256"] = new_sha
        (repo / RUNNER.SCOPE_REL).write_text(json.dumps(sc))
        with self.assertRaisesRegex(RUNNER.GuardError, "prompt mismatch"):
            RUNNER.load_scope(repo)

        # 3. Missing row (11 instead of 12)
        repo = make_temp_010_repo(self)
        sc = json.loads((repo / RUNNER.SCOPE_REL).read_text())
        sc["rows"].pop()
        (repo / RUNNER.SCOPE_REL).write_text(json.dumps(sc))
        with self.assertRaisesRegex(RUNNER.GuardError, "expected 12"):
            RUNNER.load_scope(repo)

        # 4. Explorer moved onto Short frame 0 -> hard fail
        repo = make_temp_010_repo(self)
        sp = json.loads((repo / RUNNER.SHORTS_PLAN_REL).read_text())
        sp["shorts"][1]["rows"][6]["id"] = "S01"
        sp["shorts"][1]["rows"][6]["t_start_s"] = 0.0
        (repo / RUNNER.SHORTS_PLAN_REL).write_text(json.dumps(sp))
        recon = json.loads((repo / RUNNER.RECONCILIATION_REL).read_text())
        recon["shorts_plan_sha256"] = RUNNER.sha256_file(repo / RUNNER.SHORTS_PLAN_REL)
        (repo / RUNNER.RECONCILIATION_REL).write_text(json.dumps(recon))
        sc = json.loads((repo / RUNNER.SCOPE_REL).read_text())
        for r in sc["rows"]:
            if r["identity"] == "P5:10_explorer_robin":
                r["uses"][0]["id"] = "S01"
                r["uses"][0]["t_start_s"] = 0.0
        (repo / RUNNER.SCOPE_REL).write_text(json.dumps(sc))
        with self.assertRaisesRegex(RUNNER.GuardError, "frame 0"):
            RUNNER.load_scope(repo)

        # 5. Shorts-only row polluted with long timeline t_s -> refused
        repo = make_temp_010_repo(self)
        b5_rel = Path("02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/07_Edit-Project/parts/part-05_plates_v04.json")
        b5 = json.loads((repo / b5_rel).read_text())
        for pl in b5["plates"]:
            if pl["id"] == "09a_pigeon_pavement":
                pl["t_s"] = 512.0
        (repo / b5_rel).write_text(json.dumps(b5))
        new_b5_sha = RUNNER.sha256_file(repo / b5_rel)
        recon = json.loads((repo / RUNNER.RECONCILIATION_REL).read_text())
        recon["parts"][4]["sha256"] = new_b5_sha
        (repo / RUNNER.RECONCILIATION_REL).write_text(json.dumps(recon))
        sc = json.loads((repo / RUNNER.SCOPE_REL).read_text())
        for r in sc["rows"]:
            if r["source_board"].endswith("part-05_plates_v04.json"):
                r["source_board_sha256"] = new_b5_sha
        (repo / RUNNER.SCOPE_REL).write_text(json.dumps(sc))
        with self.assertRaisesRegex(RUNNER.GuardError, "long timeline"):
            RUNNER.load_scope(repo)

    def test_self_authorization_refused_even_when_submit_env_is_set(self):
        # On current main, generation_authorized is false -> armed submit still refuses!
        with self.assertRaisesRegex(RUNNER.GuardError, "NOT authorized"):
            RUNNER.require_generation_authorization(ROOT)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.dict(os.environ, {RUNNER.SUBMIT_ENV: "1"}):
                with self.assertRaisesRegex(RUNNER.GuardError, "NOT authorized"):
                    RUNNER.cmd_submit(
                        ROOT,
                        other=6000,
                        media=root / "media",
                        ledger_path=root / "ledger.jsonl",
                        lock_path=root / "writer.lock",
                        pid_path=root / "runner.pid",
                        done_path=root / "runner.done",
                        archive_dir=root / "archive",
                        test_archive=True,
                    )

            # Invalid authorization payloads fail closed.
            bad_auths = [
                dict(j2033_done=False),
                dict(authorized=False),
                dict(cap=3601),
                dict(cap=0),
                dict(floor=2999),
                dict(job="J2268"),
                dict(film="HOS:009"),
                dict(scope_sha256="f" * 64),
            ]
            for idx, kwargs in enumerate(bad_auths):
                with self.subTest(case=idx):
                    af = write_auth_file(root / f"bad_{idx}.json", **kwargs)
                    with self.assertRaises(RUNNER.GuardError):
                        RUNNER.require_generation_authorization(ROOT, af)

            # Valid J2269 authorization with bounded cap (e.g. 2400 <= 3600) succeeds.
            good_af = write_auth_file(root / "j2269_ok.json", cap=2400, floor=3000)
            auth = RUNNER.require_generation_authorization(ROOT, good_af)
            self.assertEqual(auth.authorized_cap_credits, 2400)
            self.assertEqual(auth.minimum_headroom_floor, 3000)
            self.assertTrue(auth.j2033_done)


class PriceAccountCapDoubleCountAndRefTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = RUNNER.load_scope(ROOT)
        cls.row0 = cls.rows[0]

    def test_wrong_account_wrong_model_x2_aspect_duration_and_stale_price_refused(self):
        self.assertEqual(RUNNER.account_sha256(TRANCHE2.REQUIRED_ACCOUNT), RUNNER.REQUIRED_ACCOUNT_SHA256)
        self.assertEqual(RUNNER.account_sha256(TRANCHE2.FORBIDDEN_ACCOUNT), RUNNER.FORBIDDEN_ACCOUNT_SHA256)

        now = datetime.now(timezone.utc)
        self.assertEqual(
            RUNNER.accept_account(TRANCHE2.REQUIRED_ACCOUNT, now.isoformat(), now=now),
            RUNNER.REQUIRED_ACCOUNT_SHA256,
        )
        for bad_acct in (TRANCHE2.FORBIDDEN_ACCOUNT, TEST_FORBIDDEN_ACCOUNT, "", None):
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.accept_account(bad_acct, now.isoformat(), now=now)
        with self.assertRaisesRegex(RUNNER.GuardError, "not fresh"):
            RUNNER.accept_account(
                RUNNER.REQUIRED_ACCOUNT_SHA256, (now - timedelta(minutes=20)).isoformat(), now=now
            )

        self.assertEqual(RUNNER.accept_price(make_price("Quality"), now=now), 100)
        self.assertEqual(RUNNER.accept_batch_prices(make_batch_prices(), now=now), {"Quality": 100})

        bad_prices = [
            make_price(model="Veo 3.1 - Fast", credits=10, line="Generating will use 10 credits"),
            make_price(model="Omni"),
            make_price(outputs="x2", credits=200, line="Generating will use 200 credits"),
            make_price(outputs="x2"),
            make_price(aspect="9:16"),
            make_price(duration="4s"),
            make_price(credits=101, line="Generating will use 101 credits"),
            make_price(line="Generating will use 200 credits"),
            make_price(read_at=(now - timedelta(minutes=25)).isoformat()),
        ]
        for idx, ev in enumerate(bad_prices):
            with self.subTest(case=idx):
                with self.assertRaises(RUNNER.GuardError):
                    RUNNER.accept_price(ev, now=now)

        with self.assertRaises(RUNNER.GuardError):
            RUNNER.accept_batch_prices({"Quality": make_price(), "Fast": make_price(quality="Fast")}, now=now)
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.accept_zero_still_price({"displayed_credits": 10, "model": "Nano Banana 2.1"})
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.accept_zero_still_price({"displayed_credits": 0, "model": "Imagen 3"})
        self.assertEqual(
            RUNNER.accept_zero_still_price(
                {"displayed_credits": 0, "model": "Nano Banana 2.1", "outputs": "x1", "aspect": "16:9"},
                now=now,
            ),
            0,
        )

    def test_low_balance_3000_floor_and_3_take_3600_caps(self):
        # With 3,600 cap + 6,000 J2033 reservation + 3,000 floor = 12,600 minimum live balance.
        self.assertEqual(RUNNER.headroom(12600, 0, 0, 6000), 3000)
        with self.assertRaisesRegex(RUNNER.GuardError, "headroom 2999 < 3000"):
            RUNNER.headroom(12599, 0, 0, 6000)

        # Takes 1, 2, 3 permitted; take 4 refused.
        for done in (0, 1, 2):
            self.assertEqual(
                RUNNER.can_take(
                    row=self.row0,
                    live=12600,
                    spent=done * 100,
                    pending=0,
                    other=6000,
                    takes_done=done,
                    unknown_pending=False,
                    cost=100,
                ),
                3000,
            )
        with self.assertRaisesRegex(RUNNER.GuardError, "cap is 3"):
            RUNNER.can_take(
                row=self.row0,
                live=12600,
                spent=300,
                pending=0,
                other=6000,
                takes_done=3,
                unknown_pending=False,
                cost=100,
            )

        # Total cap 3,600 exhausted -> 37th take refused even if row only has 1 take.
        with self.assertRaisesRegex(RUNNER.GuardError, "cap 3600"):
            RUNNER.can_take(
                row=self.row0,
                live=20000,
                spent=3600,
                pending=0,
                other=0,
                takes_done=0,
                unknown_pending=False,
                cost=100,
            )

        # Lower J2269 authorized cap (e.g. 1200 try-1 only) enforced.
        with self.assertRaisesRegex(RUNNER.GuardError, "cap 1200"):
            RUNNER.can_take(
                row=self.row0,
                live=20000,
                spent=1200,
                pending=0,
                other=0,
                takes_done=1,
                unknown_pending=False,
                cost=100,
                cap=1200,
            )

        # Disk next_version allows t1..t3 and refuses t4.
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp)
            for expected_take in (1, 2, 3):
                take, dest = RUNNER.next_version(media, 1, "01_clay_line")
                self.assertEqual(take, expected_take)
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(b"mp4")
            with self.assertRaisesRegex(RUNNER.GuardError, "refuses take 4"):
                RUNNER.next_version(media, 1, "01_clay_line")

    def test_reservation_double_counting_prevented_in_headroom_and_shared_accounting(self):
        # 1. Inside headroom(): 200 spent (unposted) + 100 pending inside 3600 cap = 3600 liability, NOT 3900.
        self.assertEqual(RUNNER.headroom(6600, spent=200, pending=100, other=0, posted=0, cap=3600, floor=3000), 3000)
        # Once 200 is reconciled as posted on a live balance that dropped by 200 (6400), headroom stays 3000!
        self.assertEqual(RUNNER.headroom(6400, spent=200, pending=100, other=0, posted=200, cap=3600, floor=3000), 3000)

        # 2. Inside SharedFlowAccounting + resolve_external_reservations:
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            with RUNNER.SharedFlowAccounting(state) as acc:
                acc.reserve("J2033", "HOS:009", 6000, live=14890, floor=0)
                acc.reserve(RUNNER.DEFAULT_RESERVATION, "HOS:010", 3600, live=12600, floor=3000)
                snap0 = acc.snapshot()
                self.assertEqual(snap0["liability"], 9600)

                # Charge 100 on HOS:010 -> unposted=100, remaining_reservations=6000+3500=9500 -> liability STILL 9600!
                acc.intent("HOS:010:P01:01_clay_line:t1", RUNNER.DEFAULT_RESERVATION, 100, live=12600, floor=3000)
                acc.resolve("HOS:010:P01:01_clay_line:t1", submitted=True, evidence={"ui": {"balances": [12600]}})
                snap1 = acc.snapshot()
                self.assertEqual(snap1["unposted"], 100)
                self.assertEqual(snap1["remaining_reservations"], 9500)
                self.assertEqual(snap1["liability"], 9600)

                # Passing external={"J2033": 6000, "OWB_HOLD": 400} deduplicates J2033 (already in snap1) -> only 400!
                dedup = RUNNER.resolve_external_reservations(snap1, {"J2033": 6000, "OWB_HOLD": 400})
                self.assertEqual(dedup, 400)

                # Passing external > recorded cap for J2033 fails closed.
                with self.assertRaisesRegex(RUNNER.GuardError, "exceeds active shared ledger cap"):
                    RUNNER.resolve_external_reservations(snap1, {"J2033": 6500})

                # Passing own HOS:010 reservation or active film ID in external fails closed.
                with self.assertRaisesRegex(RUNNER.GuardError, "double-count own"):
                    RUNNER.resolve_external_reservations(snap1, {RUNNER.DEFAULT_RESERVATION: 3600})
                with self.assertRaisesRegex(RUNNER.GuardError, "already has an active reservation"):
                    RUNNER.resolve_external_reservations(snap1, {"HOS:009": 6000})

                # Passing stale PICTURE_PLAN_v04 reserved_flow_expected dict fails closed!
                stale_plan = json.loads((ROOT / RUNNER.LONG_PLAN_REL).read_text())
                with self.assertRaisesRegex(RUNNER.GuardError, "stale expected reservation"):
                    RUNNER.resolve_external_reservations(snap1, stale_plan["reserved_flow_expected"])

                # Reconciling the posted 100-credit drop reduces liability from 9600 -> 9500.
                acc.reconcile_posted(
                    "HOS:010:P01:01_clay_line:t1",
                    evidence={"before": 12600, "after": 12500, "delta": 100},
                )
                self.assertEqual(acc.snapshot()["liability"], 9500)

    def test_missing_corrupt_or_drifted_explorer_and_house_style_refs_refused(self):
        # Real Explorer ref in repo passes SHA-256 verification.
        exp_ok = RUNNER.verify_explorer_reference(ROOT, self.rows, check_hash=True)
        self.assertEqual(exp_ok["sha256"], RUNNER.EXPLORER_REF_SHA256)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            media = root / "media"

            # Missing media / house style_refs refused.
            with self.assertRaisesRegex(RUNNER.GuardError, "missing"):
                RUNNER.verify_style_references(ROOT, media, self.rows, check_hashes=False)

            media.mkdir()
            with self.assertRaisesRegex(RUNNER.GuardError, "missing style reference"):
                RUNNER.verify_style_references(ROOT, media, self.rows, check_hashes=False)

            # Synthetic 16:9 house style_refs pass with check_hashes=False, fail hash check with check_hashes=True.
            populate_media_style_refs(media)
            verified = RUNNER.verify_style_references(ROOT, media, self.rows, check_hashes=False)
            self.assertEqual(len(verified["house"]), 2)
            with self.assertRaisesRegex(RUNNER.GuardError, "sha256 drift"):
                RUNNER.verify_style_references(ROOT, media, self.rows, check_hashes=True)

            # Portrait or corrupt house style_ref refused.
            bad_house = media / "04_Generated-Clips/_style_refs/04_sunny_window_v01.jpg"
            make_png(bad_house, width=720, height=1280)
            with self.assertRaisesRegex(RUNNER.GuardError, "not 16:9"):
                RUNNER.verify_style_references(ROOT, media, self.rows, check_hashes=False)
            bad_house.write_bytes(b"not-an-image")
            with self.assertRaisesRegex(RUNNER.GuardError, "corrupt"):
                RUNNER.verify_style_references(ROOT, media, self.rows, check_hashes=False)

            # Missing or tampered Explorer ref refused.
            populate_media_style_refs(media)
            fake_repo = make_temp_010_repo(self)
            exp_file = fake_repo / RUNNER.EXPLORER_REF_REL
            make_png(exp_file, width=1024, height=1024, color="0x112233")
            with self.assertRaisesRegex(RUNNER.GuardError, "Explorer reference sha256 drift"):
                RUNNER.verify_explorer_reference(fake_repo, self.rows, check_hash=True)
            exp_file.unlink()
            with self.assertRaisesRegex(RUNNER.GuardError, "missing Explorer style reference"):
                RUNNER.verify_style_references(fake_repo, media, self.rows, check_hashes=False)

            # Flow Nano Banana 2.1 1376x768 16:9 start still passes verify_still_inventory.
            still0 = RUNNER.still_path(media, self.row0.part, self.row0.plate_id)
            make_png(still0, width=1376, height=768, color="0x335577")
            inv = RUNNER.verify_still_inventory([self.row0], media)
            self.assertEqual(inv[0]["width"], 1376)
            self.assertEqual(inv[0]["height"], 768)


class LockDuplicateProcessAndBatchExecutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = RUNNER.load_scope(ROOT)
        cls.batches = RUNNER.batch_rows(cls.rows)

    def test_writer_lock_two_process_headroom_race_and_duplicate_pid_refusal(self):
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

            # Two processes competing for 3,600 credits at live=6,600 with floor=3,000 -> one wins, one refused.
            state = root / "shared"
            race_code = (
                "import importlib.util,sys,time\n"
                f"s=importlib.util.spec_from_file_location('r',{str(SCRIPT)!r})\n"
                "m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)\n"
                "from pathlib import Path\n"
                f"state=Path({str(state)!r})\n"
                "try:\n"
                " with m.SharedFlowAccounting(state) as a:\n"
                "  a.reserve(sys.argv[1],sys.argv[2],3600,live=6600,floor=3000)\n"
                "  time.sleep(0.15)\n"
                "except m.GuardError:\n"
                " raise SystemExit(75)\n"
            )
            procs = [
                subprocess.Popen([sys.executable, "-c", race_code, key, film])
                for key, film in [("r1", "HOS:010"), ("r2", "HOS:009")]
            ]
            self.assertEqual(sorted(p.wait(timeout=5) for p in procs), [0, 75])

            # Live PID blocks duplicate launch even if stale .done exists.
            sleeper = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
            try:
                pid_path = root / "runner.pid"
                done_path = root / "runner.done"
                pid_path.write_text(str(sleeper.pid))
                done_path.write_text("0\n")
                with self.assertRaisesRegex(RUNNER.GuardError, "runner already live"):
                    RUNNER.refuse_duplicate(pid_path, done_path)
            finally:
                sleeper.kill()
                sleeper.wait(timeout=5)

    def test_killed_launch_once_owner_leaves_live_child_blocking_duplicate(self):
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

    def test_authorized_batches_save_generated_pending_review_never_keep_and_advance_5_5_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            media = root / "media"
            archive = root / "archive"
            archive.mkdir()
            populate_media_style_refs(media)
            sample_mp4 = make_silent_mp4(root / "fixture.mp4")
            auth_file = write_auth_file(root / "j2269_auth.json", cap=3600, floor=3000)

            def fake_still_maker(
                row, dest, *, repo, media, accounting, reservation, evidence_path, other=0, cap=3600, floor=3000
            ):
                accounting._assert_held()
                make_png(dest, width=1280, height=720, color=f"0x{row.index:02x}5577")
                RUNNER.immutable_bytes(
                    evidence_path,
                    (json.dumps({"row_id": row.row_id, "credits": 0, "ui": {"balances": [14890]}}) + "\n").encode(),
                )
                return dest

            def fake_submitter(
                row, dest, frame, *, accounting, reservation, charge, evidence_path, other=0, cap=3600, floor=3000
            ):
                self.assertTrue(frame.is_file())
                page = LiveDomAndCliTests.MockPage(
                    LiveDomAndCliTests.video_evidence(account=TRANCHE2.REQUIRED_ACCOUNT, balance=14890)
                )
                accounting.reserve(reservation, RUNNER.FILM_ID, cap, live=14890, floor=floor + other)
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

            batch_sizes = []
            with patch.dict(os.environ, {RUNNER.SUBMIT_ENV: "1"}):
                for expected_len in (5, 5, 2, 0):
                    written = RUNNER.cmd_submit(
                        ROOT,
                        other=6000,
                        media=media,
                        ledger_path=root / "ledger.jsonl",
                        lock_path=root / "writer.lock",
                        pid_path=root / "runner.pid",
                        done_path=root / "runner.done",
                        archive_dir=archive,
                        authorization_file=auth_file,
                        accounting_state=root / "shared",
                        spend_ledger=root / "ai_spend.jsonl",
                        batch_price_reader=make_batch_prices,
                        submitter=fake_submitter,
                        still_maker=fake_still_maker,
                        test_archive=True,
                    )
                    self.assertEqual(len(written), expected_len)
                    batch_sizes.append(len(written))
                    for entry in written:
                        self.assertEqual(entry["status"], "PENDING_REVIEW")
                        self.assertEqual(entry["file_state"], "GENERATED")
                        self.assertEqual(entry["review"], "PENDING_REVIEW")
                        self.assertIs(entry["keep"], False)
                        self.assertTrue(RUNNER.verified_output(entry))
                        self.assertNotIn("accounts", entry["create_evidence"]["ui"])

            self.assertEqual(batch_sizes, [5, 5, 2, 0])
            snap = RUNNER.SharedFlowAccounting.peek_readonly(root / "shared")
            self.assertEqual(sum(c["amount"] for c in snap["charges"].values()), 1200)
            self.assertEqual(snap["liability"], 3600)  # 1200 unposted + 2400 remaining reservation = 3600!


class LiveDomAndCliTests(unittest.TestCase):
    @staticmethod
    def video_evidence(*, account: str = TEST_STUDIO_ACCOUNT, balance: int = 14890) -> dict:
        return dict(
            host=RUNNER.FLOW_HOST,
            models=["Veo 3.1 - Quality"],
            outputs=["x1"],
            aspects=["16:9"],
            durations=["8s"],
            accounts=[account],
            prices=["Generating will use 100 credits"],
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

            outer = self

            class Mouse:
                @staticmethod
                def click(x: float, y: float) -> None:
                    if outer.on_mouse_click:
                        outer.on_mouse_click(x, y)
                    outer.clicks += 1

            self.mouse = Mouse()

        def evaluate(self, _js: str, expected):
            if expected is None:
                return dict(self.evidence)
            if self.before_click:
                self.before_click()
            if self.evidence != expected:
                return dict(ready=False, reason="live UI changed", evidence=self.evidence)
            return dict(ready=True, target=dict(x=1000.0, y=844.0), evidence=self.evidence)

    def test_guarded_create_rejects_fast_x2_low_balance_and_ui_drift_with_zero_clicks(self):
        row = RUNNER.load_scope(ROOT)[0]
        with patch.object(RUNNER, "REQUIRED_ACCOUNT_SHA256", RUNNER.account_sha256(TEST_STUDIO_ACCOUNT)), \
             patch.object(RUNNER, "FORBIDDEN_ACCOUNT_SHA256", RUNNER.account_sha256(TEST_FORBIDDEN_ACCOUNT)):
            with tempfile.TemporaryDirectory() as tmp:
                state = Path(tmp)
                with RUNNER.SharedFlowAccounting(state) as acc:
                    acc.reserve(RUNNER.DEFAULT_RESERVATION, "HOS:010", 3600, live=14890, floor=3000)

                    # Fast model, x2 outputs, wrong account, or low balance (< 3600 + 3000 = 6600) -> 0 clicks!
                    bad_uis = [
                        {**self.video_evidence(), "models": ["Veo 3.1 - Fast"], "prices": ["Generating will use 10 credits"]},
                        {**self.video_evidence(), "outputs": ["x2"], "prices": ["Generating will use 200 credits"]},
                        {**self.video_evidence(account=TEST_FORBIDDEN_ACCOUNT)},
                        {**self.video_evidence(balance=6599)},
                    ]
                    for idx, bad_ui in enumerate(bad_uis):
                        page = self.MockPage(bad_ui)
                        with self.assertRaises(RUNNER.GuardError):
                            RUNNER.guarded_create(
                                page,
                                acc,
                                row=row,
                                reservation=RUNNER.DEFAULT_RESERVATION,
                                charge=f"bad-{idx}",
                                evidence_path=state / f"bad_{idx}.json",
                                floor=3000,
                            )
                        self.assertEqual(page.clicks, 0)
                    self.assertFalse(acc.snapshot()["charges"])

                    # UI drift between precheck and click -> resolves NOT_SUBMITTED, 0 clicks.
                    drift_page = self.MockPage(self.video_evidence())
                    drift_page.before_click = lambda: drift_page.evidence.update(outputs=["x2"])
                    with self.assertRaisesRegex(RUNNER.GuardError, "live UI drift"):
                        RUNNER.guarded_create(
                            drift_page,
                            acc,
                            row=row,
                            reservation=RUNNER.DEFAULT_RESERVATION,
                            charge="drift-1",
                            evidence_path=state / "drift.json",
                            floor=3000,
                        )
                    self.assertEqual(drift_page.clicks, 0)
                    self.assertEqual(acc.snapshot()["charges"]["drift-1"]["status"], "NOT_SUBMITTED")

    def test_captured_10nov_dom_for_balance_quality_and_still_never_clicks_dom(self):
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
            res_bal = subprocess.run(
                ["node", "-e", dom_harness],
                input=json.dumps(
                    {
                        "js": RUNNER.BALANCE_EVIDENCE_JS,
                        "controls": [account_ctrl],
                        "bodyLines": capture["account_details_popup"]["body_lines"],
                    }
                ),
                text=True,
                capture_output=True,
                check=True,
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

            base_video = capture["video_mode_veo31_quality_settings_open"]
            ctrls = [account_ctrl]
            for c in base_video["visible_controls"]:
                copy = dict(c)
                if "Start generation" in (copy.get("ariaLabel") or copy.get("text") or ""):
                    copy["disabled"] = False
                    copy["isCreate"] = True
                ctrls.append(copy)
            res_vid = subprocess.run(
                ["node", "-e", dom_harness],
                input=json.dumps(
                    {
                        "js": RUNNER.CREATE_EVIDENCE_JS,
                        "controls": ctrls,
                        "bodyLines": base_video["body_lines"],
                        "verifyTarget": True,
                    }
                ),
                text=True,
                capture_output=True,
                check=True,
            )
            vid_data = json.loads(res_vid.stdout)
            self.assertEqual(vid_data["domClicks"], 0)
            self.assertTrue(vid_data["out"]["ready"])
            validated = RUNNER.read_live_evidence(
                type("P", (), {"evaluate": lambda _s, _j, _a=None: vid_data["ev"]})(),
                balance=14890,
            )
            self.assertEqual(validated["models"], ["Veo 3.1 - Quality"])
            self.assertEqual(validated["prices"], ["Generating will use 100 credits"])
            self.assertNotIn("accounts", validated)

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
                input=json.dumps(
                    {
                        "js": RUNNER.STILL_EVIDENCE_JS,
                        "controls": still_ctrls,
                        "bodyLines": still_state["body_lines"],
                        "verifyTarget": True,
                    }
                ),
                text=True,
                capture_output=True,
                check=True,
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

    def test_cli_plan_detach_unarmed_and_unauthorized_submit_spend_nothing(self):
        env = os.environ.copy()
        env.pop(RUNNER.SUBMIT_ENV, None)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan_out = root / "plan.json"
            proc_plan = subprocess.run(
                [sys.executable, str(SCRIPT), "plan", "--repo", str(ROOT), "--out", str(plan_out)],
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertEqual(proc_plan.returncode, 0, proc_plan.stderr)
            plan = json.loads(plan_out.read_text())
            self.assertEqual(plan["row_count"], 12)
            self.assertEqual(plan["submissions"], 0)
            self.assertEqual(plan["create_clicks"], 0)
            self.assertIs(plan["keep"], False)
            self.assertIs(plan["generation_authorized"], False)

            # Unarmed submit refused.
            proc_unarmed = subprocess.run(
                [sys.executable, str(SCRIPT), "submit", "--repo", str(ROOT)],
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertNotEqual(proc_unarmed.returncode, 0)
            self.assertIn("refusing submit", proc_unarmed.stderr + proc_unarmed.stdout)

            # Armed submit WITHOUT J2269 authorization also refused before CDP!
            armed_env = {**env, RUNNER.SUBMIT_ENV: "1"}
            proc_unauth = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "submit",
                    "--repo",
                    str(ROOT),
                    "--media",
                    str(root),
                    "--other-reservations",
                    "6000",
                ],
                capture_output=True,
                text=True,
                env=armed_env,
            )
            self.assertEqual(proc_unauth.returncode, 2)
            self.assertIn("NOT authorized", proc_unauth.stderr)
            self.assertNotIn("connect_over_cdp", proc_unauth.stderr + proc_unauth.stdout)

            # detach-command prints tmux command without creating log or done files.
            cmd = RUNNER.detached_command(
                SCRIPT,
                root / "run.log",
                root / "run.done",
                repo=ROOT,
                media=root,
                archive=root,
                other=6000,
                ledger=root / "ledger.jsonl",
                lock=root / "writer.lock",
                pid=root / "runner.pid",
            )
            self.assertEqual(cmd[:4], ["tmux", "new", "-d", "-s"])
            parsed = shlex.split(cmd[-1])
            self.assertEqual(parsed[2], "launch-worker")
            self.assertFalse((root / "run.log").exists())
            self.assertFalse((root / "run.done").exists())


if __name__ == "__main__":
    unittest.main()
