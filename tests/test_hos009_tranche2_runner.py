"""Tranche-2 runner tests. They never arm Flow and never submit a real take."""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/_mint_flow_v05_tranche2.py"
TRANCHE1 = ROOT / "02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/_mint_flow_v04_tranche1.py"
EDIT = ROOT / "02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project"


def load_runner():
    spec = importlib.util.spec_from_file_location("hos009_tranche2_runner", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


RUNNER = load_runner()


def price(credits=100, outputs="x1", model=None, line=None):
    return RUNNER.PriceEvidence(
        model=model or RUNNER.REQUIRED_MODEL,
        outputs=outputs,
        credits=credits,
        generate_line=line or f"Generating will use {credits} credits",
        read_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )


def silent_mp4(directory: Path) -> Path:
    dest = directory / "silent.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=0x224466:s=1280x720:d=8:r=25",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", str(dest)],
        check=True,
    )
    return dest


class ScopeAndOrderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = RUNNER.load_scope(ROOT)

    def test_exact_twenty_v05_rows(self):
        self.assertEqual(len(self.rows), 20)
        self.assertTrue(all(row.quality == "Quality" and row.try1_credits == 100 for row in self.rows))
        self.assertTrue(all("v05" in row.board for row in self.rows))

    def test_parents_first_and_continuations_follow_named_clips(self):
        ordered = RUNNER.order_rows(self.rows)
        self.assertEqual([row.plate_id for row in ordered[:2]], ["10_how_high", "07_ball_to_moon"])
        position = {row.plate_id: index for index, row in enumerate(ordered)}
        for row in ordered:
            if row.parent and (row.parent.part, row.parent.plate_id) in {item.key for item in self.rows}:
                self.assertLess(position[row.parent.plate_id], position[row.plate_id])
        self.assertLess(position["05_shot_orbit_c1"], position["05_shot_orbit_c2"])
        self.assertLess(position["05_iss_orbit_c1"], position["05_iss_orbit_c2"])

    def test_batches_respect_caps(self):
        batches = RUNNER.batch_rows(RUNNER.order_rows(self.rows))
        sizes = [len(batch) for batch in batches]
        self.assertEqual(sizes, [2, 5, 5, 5, 3])
        self.assertEqual([row.plate_id for row in batches[0]], ["10_how_high", "07_ball_to_moon"])
        for batch in batches:
            self.assertLessEqual(len(batch), 5)
            self.assertLessEqual(len(batch) * 100, 1500)

    def test_plan_submits_nothing_and_never_keeps(self):
        plan = RUNNER.build_plan(self.rows)
        self.assertEqual(plan["submissions"], 0)
        self.assertIs(plan["keep"], False)
        self.assertEqual(plan["review"], "PENDING_REVIEW")
        self.assertEqual(plan["file_state_when_written"], "GENERATED")
        self.assertEqual(plan["order"][0]["kind"], "existing_still_or_zero_price")
        self.assertEqual(plan["order"][2]["kind"], "parent_last_frame")
        before = (EDIT / "TRANCHE2_SCOPE_J2026.json").read_bytes()
        RUNNER.cmd_plan(ROOT, None)
        self.assertEqual((EDIT / "TRANCHE2_SCOPE_J2026.json").read_bytes(), before)

    def test_bad_board_hash_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            edit = repo / "02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project"
            edit.mkdir(parents=True)
            os.symlink(EDIT / "parts", edit / "parts")
            scope = json.loads((EDIT / "TRANCHE2_SCOPE_J2026.json").read_text())
            scope["rows"][0]["board_sha256"] = "0" * 64
            (edit / "TRANCHE2_SCOPE_J2026.json").write_text(json.dumps(scope))
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.load_scope(repo)

    def test_runner_does_not_touch_tranche1_or_assign_keep(self):
        text = SCRIPT.read_text()
        self.assertNotRegex(text, r"(import|spec_from_file_location|load_mod).*tranche1")
        self.assertNotRegex(text, r"status\s*=\s*['\"]KEEP['\"]")
        self.assertIn("reuse_page", text)
        self.assertTrue(TRANCHE1.exists())


class GuardTests(unittest.TestCase):
    def test_price_must_be_quality_x1_100(self):
        self.assertEqual(RUNNER.accept_price(price()), 100)
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.accept_price(price(credits=101, line="Generating will use 101 credits"))
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.accept_price(price(outputs="x2"))
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.accept_price(price(model="Veo 3.1 - Fast"))
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.accept_price(price(line="Generating will use 100 credits, maybe"))

    def test_account_must_be_fresh_hos_ultra(self):
        now = datetime.now(timezone.utc)
        RUNNER.accept_account(RUNNER.REQUIRED_ACCOUNT, now.isoformat(), now=now)
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.accept_account(RUNNER.FORBIDDEN_ACCOUNT, now.isoformat(), now=now)
        stale = (now - timedelta(hours=2)).isoformat()
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.accept_account(RUNNER.REQUIRED_ACCOUNT, stale, now=now)

    def test_headroom_reserves_remaining_cap(self):
        self.assertEqual(RUNNER.headroom(15430, 0, 0, 0), 9430)
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.headroom(8999, 0, 0, 0)
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.headroom(15430, 0, 0, 6431)
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.can_take(live=15430, spent=5900, pending=100, other=0, takes_done=0, unknown_pending=False)
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.can_take(live=15430, spent=0, pending=0, other=0, takes_done=3, unknown_pending=False)
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.can_take(live=15430, spent=0, pending=0, other=0, takes_done=0, unknown_pending=True)

    def test_pending_line_then_review_counts_once(self):
        entries = [
            {"plate_id": "10_how_high", "take": 1, "status": "SUBMITTING", "credits_reserved": 100, "keep": False},
            {"plate_id": "10_how_high", "take": 1, "status": "PENDING_REVIEW", "credits_used": 100, "keep": False},
        ]
        spent, pending, unknown, takes = RUNNER.ledger_totals(entries)
        self.assertEqual((spent, pending, unknown, takes["10_how_high"]), (100, 0, False, 1))

    def test_keep_and_unknown_pending_stop(self):
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.ledger_totals([{"plate_id": "x", "take": 1, "status": "KEEP", "keep": True}])
        spent, pending, unknown, _takes = RUNNER.ledger_totals([
            {"plate_id": "x", "take": 1, "status": "SUBMITTING", "credits_reserved": None, "keep": False},
        ])
        self.assertTrue(unknown)
        self.assertEqual(pending, 0)
        self.assertEqual(spent, 0)

    def test_batch_over_five_rows_is_refused(self):
        rows = RUNNER.load_scope(ROOT)[:6]
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.assert_batch_limits(rows)


class ExecuteAndProcessTests(unittest.TestCase):
    def test_fake_batch_is_pending_review_and_does_not_import_playwright_submit(self):
        rows = RUNNER.order_rows(RUNNER.load_scope(ROOT))
        parents = rows[:2]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            media = root / "media"
            clip = silent_mp4(root)
            calls = []

            def submitter(row, dest, frame):
                calls.append((row.plate_id, Path(frame).exists()))
                shutil.copy(clip, dest)

            for row in parents:
                still = RUNNER.still_path(media, row.part, row.plate_id)
                still.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(["ffmpeg", "-v", "error", "-i", str(clip), "-frames:v", "1", str(still)], check=True)
            now = datetime.now(timezone.utc)
            (root / "archive").mkdir()
            written = RUNNER.execute_batch(
                parents, media=media, ledger_path=root / "ledger.jsonl", lock_path=root / "writer.lock",
                live=15430, other=0, price=price(), account=RUNNER.REQUIRED_ACCOUNT,
                read_at=now.isoformat(), now=now, submitter=submitter,
                archive_dir=root / "archive", receipt_path=root / "receipt.json", test_archive=True,
            )
            self.assertEqual([item[0] for item in calls], ["10_how_high", "07_ball_to_moon"])
            self.assertTrue(all(item[1] for item in calls))
            self.assertTrue(all(entry["status"] == "PENDING_REVIEW" and entry["keep"] is False
                                and entry["generated"] is True and entry["file_state"] == "GENERATED"
                                for entry in written))
            ledger = RUNNER.read_ledger(root / "ledger.jsonl")
            self.assertNotIn("KEEP", {entry["status"] for entry in ledger})
            archived = list((root / "archive").glob("*.mp4"))
            self.assertEqual(len(archived), 2)
            proof = json.loads(archived[0].with_suffix(".mp4.sha256.json").read_text())
            self.assertEqual(RUNNER.sha256_file(archived[0]), proof["sha256"])
            again = RUNNER.next_batch(rows, ledger)
            self.assertNotIn("10_how_high", [row.plate_id for row in again])
            self.assertNotIn("07_ball_to_moon", [row.plate_id for row in again])

    def test_unresolved_submit_does_not_call_submitter(self):
        rows = RUNNER.order_rows(RUNNER.load_scope(ROOT))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger = root / "ledger.jsonl"
            RUNNER.append_ledger(ledger, {
                "plate_id": "10_how_high", "part": 2, "take": 1, "status": "SUBMITTING",
                "credits_reserved": 100, "keep": False,
            })
            calls = []
            now = datetime.now(timezone.utc)
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.execute_batch(
                    rows[:1], media=root / "media", ledger_path=ledger, lock_path=root / "writer.lock",
                    live=15430, other=0, price=price(), account=RUNNER.REQUIRED_ACCOUNT,
                    read_at=now.isoformat(), now=now, submitter=lambda *args: calls.append(args),
                )
            self.assertEqual(calls, [])

    def test_low_balance_submits_nothing(self):
        rows = RUNNER.order_rows(RUNNER.load_scope(ROOT))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            now = datetime.now(timezone.utc)
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.execute_batch(
                    rows[:2], media=root / "media", ledger_path=root / "ledger.jsonl",
                    lock_path=root / "writer.lock", live=8999, other=0, price=price(),
                    account=RUNNER.REQUIRED_ACCOUNT, read_at=now.isoformat(), now=now,
                    submitter=lambda *args: (_ for _ in ()).throw(AssertionError("submitted")),
                )

    def test_versioned_files_are_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp)
            first = RUNNER.versioned_output(media, 2, "10_how_high", 1)
            first.parent.mkdir(parents=True)
            first.write_bytes(b"keep-me")
            take, dest = RUNNER.next_version(media, 2, "10_how_high")
            self.assertEqual(take, 2)
            self.assertNotEqual(dest, first)
            self.assertEqual(first.read_bytes(), b"keep-me")

    def test_parent_frame_comes_from_the_named_clip(self):
        rows = {row.plate_id: row for row in RUNNER.load_scope(ROOT)}
        row = rows["05_heavens_map_c1"]
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp)
            clip = silent_mp4(media)
            parent = row.parent
            dest = RUNNER.parent_clip_candidates(media, parent, in_scope=False)[-1]
            dest.parent.mkdir(parents=True)
            shutil.copy(clip, dest)
            frame = RUNNER.prepare_start_frame(row, media, in_scope_keys=set(), still_price=None, still_maker=None)
            self.assertTrue(frame.exists() and frame.stat().st_size > 100)
            self.assertIn(parent.plate_id, frame.name)

    def test_archive_mismatch_is_not_kept_as_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "src.bin"
            src.write_bytes(b"abc")
            original = RUNNER.sha256_file
            state = {"n": 0}

            def flip(path):
                state["n"] += 1
                if state["n"] == 1:
                    return "a" * 64
                return "b" * 64

            RUNNER.sha256_file = flip
            try:
                with self.assertRaises(RUNNER.GuardError):
                    RUNNER.archive_verified(src, root / "nas-like" / "src.bin")
                self.assertTrue((root / "nas-like" / "src.bin").exists())
            finally:
                RUNNER.sha256_file = original

    def test_writer_lock_blocks_another_process(self):
        with tempfile.TemporaryDirectory() as tmp:
            lock = Path(tmp) / "writer.lock"
            held = RUNNER.WriterLock(lock)
            held.__enter__()
            try:
                probe = subprocess.run(
                    [sys.executable, "-c",
                     "import importlib.util,sys\n"
                     f"s=importlib.util.spec_from_file_location('r',{str(SCRIPT)!r})\n"
                     "m=importlib.util.module_from_spec(s)\n"
                     "sys.modules[s.name]=m\n"
                     "s.loader.exec_module(m)\n"
                     f"lock={str(lock)!r}\n"
                     "try:\n"
                     "    m.WriterLock(lock).__enter__()\n"
                     "except m.GuardError:\n"
                     "    raise SystemExit(0)\n"
                     "raise SystemExit(1)\n"],
                    capture_output=True, text=True,
                )
                self.assertEqual(probe.returncode, 0, probe.stderr)
            finally:
                held.__exit__(None, None, None)

    def test_duplicate_live_pid_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sleeper = subprocess.Popen(["sleep", "30"])
            pid_path = root / "runner.pid"
            done = root / "runner.done"
            pid_path.write_text(str(sleeper.pid))
            try:
                with self.assertRaises(RUNNER.GuardError):
                    RUNNER.refuse_duplicate(pid_path, done)
            finally:
                sleeper.kill()
                sleeper.wait(timeout=5)
            done.write_text("0\n")
            RUNNER.refuse_duplicate(pid_path, done)

    def test_detached_command_records_log_and_done_and_starts_nothing(self):
        import shlex
        with tempfile.TemporaryDirectory(prefix="launch spaces ") as tmp:
            root = Path(tmp)
            command = RUNNER.detached_command(
                SCRIPT, root / "run.log", root / "run.done", repo=ROOT,
                media=root, archive=root, other=42, ledger=root / "shared.jsonl",
                lock=root / "writer.lock", pid=root / "runner.pid")
            self.assertEqual(command[:4], ["tmux", "new", "-d", "-s"])
            args = shlex.split(command[-1])
            self.assertEqual(args[2], "launch-worker")
            for flag, value in (("--repo", ROOT), ("--media", root),
                                ("--archive", root), ("--other-reservations", 42),
                                ("--ledger", root / "shared.jsonl"),
                                ("--lock", root / "writer.lock"),
                                ("--pid", root / "runner.pid"),
                                ("--log", root / "run.log"), ("--done", root / "run.done")):
                self.assertEqual(args[args.index(flag) + 1], str(value))
            self.assertFalse((root / "run.log").exists())
            self.assertFalse((root / "run.done").exists())
            self.assertNotIn(RUNNER.SUBMIT_ENV, os.environ)

    def test_cli_plan_and_unarmed_submit(self):
        env = os.environ.copy()
        env.pop(RUNNER.SUBMIT_ENV, None)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "plan.json"
            plan_run = subprocess.run(
                [sys.executable, str(SCRIPT), "plan", "--repo", str(ROOT), "--out", str(out)],
                capture_output=True, text=True, env=env,
            )
            self.assertEqual(plan_run.returncode, 0, plan_run.stderr)
            plan = json.loads(out.read_text())
            self.assertEqual(plan["submissions"], 0)
            self.assertEqual(plan["row_count"], 20)
            submit_run = subprocess.run(
                [sys.executable, str(SCRIPT), "submit", "--repo", str(ROOT)],
                capture_output=True, text=True, env=env,
            )
            self.assertNotEqual(submit_run.returncode, 0)
            self.assertIn("refusing submit", submit_run.stderr + submit_run.stdout)
            self.assertNotIn("connect_over_cdp", submit_run.stderr + submit_run.stdout)


class SafetyRegressionTests(unittest.TestCase):
    def test_full_reservation_boundary_includes_impending_charge(self):
        for live in (8900, 8999):
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.can_take(live=live, spent=0, pending=0, other=0,
                                takes_done=0, unknown_pending=False)
        self.assertEqual(RUNNER.can_take(live=9000, spent=0, pending=0, other=0,
                                        takes_done=0, unknown_pending=False), 3000)

    def test_delayed_deductions_do_not_release_reservation(self):
        for spent, pending in ((0, 100), (100, 0), (200, 100)):
            self.assertEqual(RUNNER.headroom(9000, spent, pending, 0), 3000)
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.headroom(8999, spent, pending, 0)
        self.assertEqual(RUNNER.headroom(8900, 100, 0, 0, posted=100), 3000)
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.headroom(9000, 100, 0, 1)
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.headroom(9000, 0, 0, 0, posted=100)

    def test_archive_collision_preserves_old_bytes_and_same_hash_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src, dest = root / "src", root / "archive"
            src.write_bytes(b"first")
            first = RUNNER.archive_verified(src, dest)
            self.assertEqual(RUNNER.archive_verified(src, dest), first)
            src.write_bytes(b"different")
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.archive_verified(src, dest)
            self.assertEqual(dest.read_bytes(), b"first")
            self.assertEqual(json.loads(dest.with_suffix(".sha256.json").read_text())["sha256"],
                             first["sha256"])

    def test_receipts_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "receipt.json"
            RUNNER.write_receipt(path, ["a"], [])
            RUNNER.write_receipt(path, ["a"], [])
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.write_receipt(path, ["b"], [])

    def test_production_requires_mounted_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            for path in (None, Path(tmp), Path(tmp) / "absent"):
                with self.assertRaises(RUNNER.GuardError):
                    RUNNER.require_archive(path)

    def test_technical_checks_duration_dimensions_and_decode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            good = silent_mp4(root)
            self.assertTrue(RUNNER.technical_report(good)["ok"])
            self.assertFalse(RUNNER.technical_report(good, required_s=9)["ok"])
            small = root / "small.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-i", str(good), "-vf", "scale=160:90",
                            str(small)], check=True)
            self.assertFalse(RUNNER.technical_report(small)["ok"])
            small.write_bytes(b"invalid" * 100)
            self.assertFalse(RUNNER.technical_report(small)["ok"])

    def test_failed_or_missing_output_never_advances(self):
        rows = RUNNER.order_rows(RUNNER.load_scope(ROOT))
        entry = {"plate_id": rows[0].plate_id, "part": rows[0].part, "take": 1,
                 "status": "PENDING_REVIEW", "generated": True, "keep": False,
                 "technical": {"ok": False}}
        self.assertEqual(RUNNER.next_batch(rows, [entry]), rows[:2])
        entry["technical"]["ok"] = True
        entry["archive"] = {"verified": True, "dest": "/absent", "sha256": "x"}
        entry["file"] = "/absent"
        self.assertFalse(RUNNER.verified_output(entry))

    def test_verified_parent_selects_later_take_and_rechecks_hash(self):
        rows = {r.plate_id: r for r in RUNNER.load_scope(ROOT)}
        row = rows["08_halley_visit_c1"]
        self.assertIsNotNone(row.parent)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            clip = silent_mp4(root)
            archive = RUNNER.archive_verified(clip, root / "saved.mp4")
            entry = RUNNER.review_record(row.parent.plate_id, row.parent.part, 2, clip,
                                         RUNNER.technical_report(clip))
            entry["archive"] = archive
            frame = RUNNER.prepare_start_frame(row, root, in_scope_keys={row.parent.key},
                                                still_price=None, still_maker=None, ledger=[entry])
            self.assertTrue(frame.exists())
            clip.write_bytes(b"changed")
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.prepare_start_frame(row, root, in_scope_keys={row.parent.key},
                                           still_price=None, still_maker=None, ledger=[entry])

    def test_stale_done_never_hides_live_process(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sleeper = subprocess.Popen(["sleep", "30"])
            try:
                (root / "pid").write_text(str(sleeper.pid))
                (root / "done").write_text("0")
                with self.assertRaises(RUNNER.GuardError):
                    RUNNER.refuse_duplicate(root / "pid", root / "done")
            finally:
                sleeper.kill()
                sleeper.wait()

    def test_cmd_submit_requires_archive_and_executes_guarded_first_batch(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.dict(os.environ, {RUNNER.SUBMIT_ENV: "1"}):
                with self.assertRaisesRegex(RUNNER.GuardError, "verified archive is mandatory"):
                    RUNNER.cmd_submit(
                        ROOT, other=0, media=root / "media",
                        ledger_path=root / "ledger.jsonl", lock_path=root / "writer.lock",
                        pid_path=root / "runner.pid", done_path=root / "runner.done",
                        archive_dir=None,
                    )
                archive = root / "archive"
                archive.mkdir()
                stills_made = []
                def fake_still_maker(row, dest, *, accounting, reservation, evidence_path, other=0):
                    accounting._assert_held()
                    stills_made.append(row.plate_id)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    subprocess.run(
                        ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                         "color=s=1280x720", "-frames:v", "1", str(dest)],
                        check=True,
                    )
                    RUNNER.immutable_bytes(
                        evidence_path,
                        b'{"credits":0,"ui":{"balances":[10000]}}\n',
                    )
                    return dest
                def fake_submitter(row, dest, frame, *, accounting, reservation, charge, evidence_path, other=0):
                    page = LiveCreateAdapterTests.Page(LiveCreateAdapterTests().evidence())
                    accounting.reserve(reservation, "HOS:009", RUNNER.MAX_TOTAL_CREDITS,
                                       live=10000, floor=RUNNER.HEADROOM_FLOOR + other)
                    ev = RUNNER.guarded_create(
                        page, accounting, reservation=reservation,
                        charge=charge, evidence_path=evidence_path,
                        floor=RUNNER.HEADROOM_FLOOR + other,
                    )
                    dest.write_bytes(b"fake video fixture")
                    return ev
                with patch.object(RUNNER, "strip_audio"), \
                     patch.object(RUNNER, "technical_report",
                                  side_effect=lambda p, **kw: {"ok": True, "sha256": RUNNER.sha256_file(p)}):
                    written = RUNNER.cmd_submit(
                        ROOT, other=500, media=root / "media",
                        ledger_path=root / "ledger.jsonl", lock_path=root / "writer.lock",
                        pid_path=root / "runner.pid", done_path=root / "runner.done",
                        archive_dir=archive, accounting_state=root / "shared",
                        spend_ledger=root / "spend.jsonl", submitter=fake_submitter,
                        still_maker=fake_still_maker, test_archive=True,
                    )
                self.assertEqual([e["plate_id"] for e in written], ["10_how_high", "07_ball_to_moon"])
                self.assertEqual(stills_made, ["10_how_high", "07_ball_to_moon"])
                self.assertTrue((archive / "10_how_high_t1.png").is_file())
                self.assertTrue((archive / "07_ball_to_moon_t1.png").is_file())
                self.assertEqual((root / "runner.pid").read_text().strip(), str(os.getpid()))


class DetachedSafetyTests(unittest.TestCase):
    def launch(self, root, command, **overrides):
        args = dict(ownership=root / "owner.lock", pid=root / "runner.pid",
                    log=root / "run.log", done=root / "run.done")
        args.update(overrides)
        return RUNNER.launch_once(command, **args)

    def test_fake_child_exit_and_output_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            code = self.launch(root, [sys.executable, "-c", "print('fake submit'); raise SystemExit(7)"])
            self.assertEqual(code, 7)
            self.assertEqual((root / "run.done").read_text(), "7\n")
            self.assertEqual((root / "run.log").read_text(), "fake submit\n")
            # Existing output is immutable even if the old pid has exited.
            with self.assertRaises(RUNNER.GuardError):
                self.launch(root, [sys.executable, "-c", "raise SystemExit(0)"])
            self.assertEqual((root / "run.done").read_text(), "7\n")

    def test_live_owner_blocks_even_with_stale_done_and_different_pid_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "run.done").write_text("0\n")
            with RUNNER.WriterLock(root / "owner.lock"):
                with self.assertRaises(RUNNER.GuardError):
                    self.launch(root, ["unreachable"], pid=root / "different.pid")
            self.assertFalse((root / "run.log").exists())

    def test_live_or_unreadable_child_pid_blocks_after_owner_crash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sleeper = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
            try:
                (root / "runner.pid").write_text(str(sleeper.pid))
                with self.assertRaises(RUNNER.GuardError):
                    self.launch(root, ["unreachable"])
                (root / "runner.pid").write_text("torn-pid")
                with self.assertRaises(RUNNER.GuardError):
                    self.launch(root, ["unreachable"])
            finally:
                sleeper.terminate()
                sleeper.wait()
            self.assertFalse((root / "run.log").exists())

    def test_killed_owner_leaves_live_child_that_blocks_restart(self):
        import time
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            owner = root / "crash-owner.py"
            owner.write_text(
                "import importlib.util,sys\n"
                f"s=importlib.util.spec_from_file_location('r',{str(SCRIPT)!r})\n"
                "m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m)\n"
                "from pathlib import Path\n"
                f"root=Path({str(root)!r})\n"
                "command=[sys.executable,'-c',\"from pathlib import Path; import time; Path(\"+repr(str(root/'started'))+\").touch(); time.sleep(30)\"]\n"
                "m.launch_once(command,ownership=root/'owner.lock',pid=root/'runner.pid',log=root/'first.log',done=root/'first.done')\n")
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
                self.assertFalse((root / "first.done").exists())
                self.assertTrue(RUNNER.process_alive(child_pid))
                # The kernel released the owner's flock. Durable child identity
                # must still stop a second child, even with a new log/done pair.
                with self.assertRaisesRegex(RUNNER.GuardError, "runner already live"):
                    self.launch(root, ["unreachable"], log=root / "second.log", done=root / "second.done")
                self.assertFalse((root / "second.log").exists())
            finally:
                if parent.poll() is None:
                    parent.kill()
                    parent.wait()
                if child_pid and RUNNER.process_alive(child_pid):
                    import signal
                    os.kill(child_pid, signal.SIGTERM)

    def test_pid_record_failure_cannot_start_child_work(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            marker = root / "must-not-exist"
            with patch.object(RUNNER, "claim_pid", side_effect=RUNNER.GuardError("pid persistence failed")):
                with self.assertRaises(RUNNER.GuardError):
                    self.launch(root, [sys.executable, "-c", f"from pathlib import Path; Path({str(marker)!r}).touch()"])
            # stdin EOF releases the unsignalled child without executing its command.
            self.assertFalse(marker.exists())

    def test_same_log_collision_never_starts_child(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "run.log").write_text("preserve")
            with self.assertRaises(FileExistsError):
                self.launch(root, ["unreachable"])
            self.assertEqual((root / "run.log").read_text(), "preserve")
            self.assertFalse((root / "runner.pid").exists())

    def test_emitted_command_runs_real_launch_with_fake_submit_entry(self):
        import shlex
        with tempfile.TemporaryDirectory(prefix="launch integration ") as tmp:
            root = Path(tmp)
            fake = root / "fake runner.py"
            # Exercise the real CLI and launch owner, replacing ONLY the final
            # submit function. There is no Flow import or browser in this fake.
            fake.write_text(
                "import importlib.util,sys,json,os\n"
                f"spec=importlib.util.spec_from_file_location('runner',{str(SCRIPT)!r})\n"
                "m=importlib.util.module_from_spec(spec); sys.modules[spec.name]=m; spec.loader.exec_module(m)\n"
                "from pathlib import Path\n"
                f"m.runner_state_dir=lambda: Path({str(root)!r})\n"
                f"m.__file__={str(fake)!r}\n"
                "m.cmd_submit=lambda repo,**kw: print(json.dumps(dict(repo=str(repo), **{k:str(v) for k,v in kw.items()}),sort_keys=True))\n"
                "os.environ[m.SUBMIT_ENV]='1'\n"
                "raise SystemExit(m.main())\n")
            command = RUNNER.detached_command(
                fake, root / "run.log", root / "run.done", repo=ROOT,
                media=root, archive=root, other=321, ledger=root / "ledger.jsonl",
                lock=root / "writer.lock", pid=root / "runner.pid")
            result = subprocess.run(shlex.split(command[-1]), capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            received = json.loads((root / "run.log").read_text())
            self.assertEqual(received["media"], str(root))
            self.assertEqual(received["archive_dir"], str(root))
            self.assertEqual(received["ledger_path"], str(root / "ledger.jsonl"))
            self.assertEqual(received["lock_path"], str(root / "writer.lock"))
            self.assertEqual(received["pid_path"], str(root / "runner.pid"))
            self.assertEqual(received["done_path"], str(root / "run.done"))
            self.assertEqual(received["other"], "321")
            self.assertEqual((root / "run.done").read_text(), "0\n")

    def test_two_launch_processes_start_only_one_fake_child(self):
        import time
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            owner = root / "owner.py"
            owner.write_text(
                "import importlib.util,sys\n"
                f"s=importlib.util.spec_from_file_location('r',{str(SCRIPT)!r})\n"
                "m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m)\n"
                "from pathlib import Path\n"
                f"root=Path({str(root)!r})\n"
                "tag=sys.argv[1]\n"
                "command=[sys.executable,'-c',\"from pathlib import Path; import time; Path(\"+repr(str(root/'started'))+\").touch(); time.sleep(1)\"]\n"
                "raise SystemExit(m.launch_once(command,ownership=root/'shared.lock',pid=root/'runner.pid',log=root/(tag+'.log'),done=root/(tag+'.done')))\n")
            first = subprocess.Popen([sys.executable, str(owner), "first"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                deadline = time.monotonic() + 5
                while not (root / "started").exists() and time.monotonic() < deadline:
                    time.sleep(0.02)
                self.assertTrue((root / "started").exists())
                second = subprocess.run([sys.executable, str(owner), "second"], capture_output=True, text=True)
                self.assertNotEqual(second.returncode, 0)
                self.assertIn("writer lock held", second.stderr)
                self.assertFalse((root / "second.log").exists())
                stdout, stderr = first.communicate(timeout=5)
                self.assertEqual(first.returncode, 0, stderr)
            finally:
                if first.poll() is None:
                    first.terminate()
                    first.communicate()

    def test_invalid_launch_paths_or_reservations_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            defaults = dict(repo=ROOT, media=root, archive=root, other=0,
                            ledger=root / "ledger", lock=root / "lock", pid=root / "pid")
            for change in ({"other": -1}, {"media": root / "absent"},
                           {"ledger": Path("relative")}, {"lock": root / "pid"}):
                with self.assertRaises(RUNNER.GuardError):
                    RUNNER.detached_command(SCRIPT, root / "log", root / "done", **(defaults | change))
            (root / "done").write_text("0")
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.detached_command(SCRIPT, root / "log", root / "done", **defaults)


class SharedAccountingTests(unittest.TestCase):
    def test_floor_and_cross_channel_reservations(self):
        with tempfile.TemporaryDirectory() as tmp:
            with RUNNER.SharedFlowAccounting(Path(tmp)) as account:
                for live in (8900, 8999):
                    with self.assertRaises(RUNNER.GuardError):
                        account.reserve('J2033', 'HOS:009', 6000, live=live)
                account.reserve('J2033', 'HOS:009', 6000, live=9000)
                account.reserve('J2033', 'HOS:009', 6000, live=9000)  # idempotent
                with self.assertRaises(RUNNER.GuardError):
                    account.reserve('OWB-job', 'OWB:032', 1, live=9000)
                with self.assertRaises(RUNNER.GuardError):
                    account.reserve('J2033', 'OWB:032', 6000, live=20000)
                self.assertEqual(account.snapshot()['liability'], 6000)

    def test_crashed_pending_intent_blocks_other_channel_and_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            with RUNNER.SharedFlowAccounting(state) as account:
                account.reserve('hos', 'HOS:009', 6000, live=20000)
                account.reserve('owb', 'OWB:032', 100, live=20000)
                account.intent('take1', 'hos', 100, live=20000)
            # A new process/session must see the durable intent even with a high balance.
            with RUNNER.SharedFlowAccounting(state) as account:
                self.assertTrue(account.snapshot()['pending'])
                for key, reservation in [('take1', 'hos'), ('take2', 'owb')]:
                    with self.assertRaises(RUNNER.GuardError):
                        account.intent(key, reservation, 100, live=20000)
                with self.assertRaises(RUNNER.GuardError):
                    account.release('hos')
                with self.assertRaises(RUNNER.GuardError):
                    account.reserve('third', 'OWB:031', 100, live=20000)

    def test_unposted_charges_survive_release_and_only_evidence_reconciles(self):
        with tempfile.TemporaryDirectory() as tmp:
            with RUNNER.SharedFlowAccounting(Path(tmp)) as account:
                account.reserve('hos', 'HOS:009', 6000, live=9000)
                account.intent('take1', 'hos', 100, live=9000)
                self.assertEqual(account.snapshot()['liability'], 6000)
                account.resolve('take1', submitted=True, evidence={'receipt': 'fake-create-1'})
                self.assertEqual(account.snapshot()['liability'], 6000)
                # Delayed UI deduction cannot be treated as posted automatically.
                with self.assertRaises(RUNNER.GuardError):
                    account.intent('take2', 'hos', 100, live=8900)
                with self.assertRaises(RUNNER.GuardError):
                    account.reconcile_posted('take1', evidence={})
                account.reconcile_posted('take1', evidence={'transaction': 'fake-confirmed-1'})
                self.assertEqual(account.snapshot()['liability'], 5900)
                account.intent('take2', 'hos', 100, live=8900)
                account.resolve('take2', submitted=True, evidence={'receipt': 'fake-create-2'})
                account.release('hos')
                self.assertEqual(account.snapshot()['liability'], 100)
                with self.assertRaises(RUNNER.GuardError):
                    account.reconcile_posted('take1', evidence={'transaction': 'repeat'})

    def test_confirmed_non_submission_restores_capacity_but_identity_cannot_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            with RUNNER.SharedFlowAccounting(Path(tmp)) as account:
                account.reserve('job', 'HOS:009', 100, live=3100)
                account.intent('take1', 'job', 100, live=3100)
                account.resolve('take1', submitted=False, evidence={'guard': 'never-clicked'})
                self.assertEqual(account.snapshot()['liability'], 100)
                with self.assertRaises(RUNNER.GuardError):
                    account.intent('take1', 'job', 100, live=3100)
                account.intent('take2', 'job', 100, live=3100)
                account.resolve('take2', submitted=True, evidence={'receipt': 'fake'})
                with self.assertRaises(RUNNER.GuardError):
                    account.intent('take3', 'job', 100, live=10000)

    def test_torn_or_invalid_ledger_fails_closed_and_releases_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            for data in (b'{"kind":"reserve"}', b'not-json\n', b'[]\n', b'null\n',
                         b'{"kind":"unknown","id":"x"}\n'):
                (state / 'account.jsonl').write_bytes(data)
                for _ in range(2):
                    with self.assertRaises(RUNNER.GuardError):
                        with RUNNER.SharedFlowAccounting(state):
                            self.fail('invalid ledger accepted')
            # Failed validation must not leave the OS lock held.
            (state / 'account.jsonl').write_bytes(b'')
            with RUNNER.SharedFlowAccounting(state) as account:
                self.assertEqual(account.snapshot()['liability'], 0)

    def test_mutation_requires_context_and_invalid_amounts_do_not_append(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            account = RUNNER.SharedFlowAccounting(state)
            with self.assertRaises(RUNNER.GuardError):
                account.reserve('x', 'HOS:009', 100, live=5000)
            with account:
                for amount in (-1, True, 1.5, '100'):
                    with self.assertRaises(RUNNER.GuardError):
                        account.reserve('x', 'HOS:009', amount, live=5000)
                self.assertFalse(account.path.exists())

    def test_real_two_process_competition_only_one_can_reserve_floor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            code = (
                "import importlib.util,sys,time\n"
                f"s=importlib.util.spec_from_file_location('r',{str(SCRIPT)!r})\n"
                "m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)\n"
                "from pathlib import Path\n"
                f"state=Path({str(root)!r})\n"
                "try:\n"
                " with m.SharedFlowAccounting(state) as a:\n"
                "  a.reserve(sys.argv[1],sys.argv[2],6000,live=9000)\n"
                "  time.sleep(0.2)\n"
                "except m.GuardError:\n"
                " raise SystemExit(75)\n")
            processes = [subprocess.Popen([sys.executable, '-c', code, key, film])
                         for key, film in [('hos', 'HOS:009'), ('owb', 'OWB:032')]]
            self.assertEqual(sorted(p.wait(timeout=5) for p in processes), [0, 75])
            with RUNNER.SharedFlowAccounting(root) as account:
                self.assertEqual(len(account.snapshot()['reservations']), 1)
                self.assertEqual(account.snapshot()['liability'], 6000)

    def test_killed_writer_preserves_intent_and_os_lock_recovers(self):
        import time
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            code = (
                "import importlib.util,sys,time\n"
                f"s=importlib.util.spec_from_file_location('r',{str(SCRIPT)!r})\n"
                "m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)\n"
                "from pathlib import Path\n"
                f"root=Path({str(root)!r})\n"
                "with m.SharedFlowAccounting(root) as a:\n"
                " a.reserve('hos','HOS:009',6000,live=9000)\n"
                " a.intent('take','hos',100,live=9000)\n"
                " (root/'persisted').touch()\n"
                " time.sleep(30)\n")
            writer = subprocess.Popen([sys.executable, '-c', code])
            try:
                deadline = time.monotonic() + 5
                while not (root / 'persisted').exists() and time.monotonic() < deadline:
                    time.sleep(0.02)
                self.assertTrue((root / 'persisted').exists())
                writer.kill()
                writer.wait(timeout=5)
                with RUNNER.SharedFlowAccounting(root) as recovered:
                    self.assertTrue(recovered.snapshot()['pending'])
                    self.assertEqual(recovered.snapshot()['liability'], 6000)
                    with self.assertRaises(RUNNER.GuardError):
                        recovered.intent('retry', 'hos', 100, live=20000)
            finally:
                if writer.poll() is None:
                    writer.kill()
                    writer.wait()

    def test_pending_write_is_fsynced_before_return(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            with RUNNER.SharedFlowAccounting(Path(tmp)) as account:
                account.reserve('job', 'HOS:009', 100, live=3100)
                with patch.object(RUNNER.os, 'fsync', wraps=os.fsync) as sync:
                    account.intent('take', 'job', 100, live=3100)
                    self.assertGreaterEqual(sync.call_count, 1)
                self.assertTrue(account.snapshot()['pending'])


class FlowPageTests(unittest.TestCase):
    def test_reuses_shared_helper(self):
        class Page:
            def __init__(self, url, closed=False):
                self.url, self.closed, self.visits = url, closed, []
            def is_closed(self):
                return self.closed
            def bring_to_front(self):
                pass
            def goto(self, url, **kwargs):
                self.url = url
                self.visits.append(url)

        class Context:
            def __init__(self, pages):
                self.pages = pages
            def new_page(self):
                page = Page("about:blank")
                self.pages.append(page)
                return page

        project = Page("https://flow.google.com/project/current")
        browser = type("B", (), {"contexts": [Context([project])]})()
        chosen = RUNNER.open_flow_page(browser, "https://flow.google.com/", lambda page, url: page.goto(url))
        self.assertIs(chosen, project)
        self.assertEqual(project.visits, [])

        about = Page("https://flow.google.com/about")
        browser = type("B", (), {"contexts": [Context([about])]})()
        chosen = RUNNER.open_flow_page(browser, "https://flow.google.com/", lambda page, url: page.goto(url))
        self.assertIs(chosen, about)
        self.assertEqual(about.visits, ["https://flow.google.com/"])


class LiveCreateAdapterTests(unittest.TestCase):
    def evidence(self):
        return dict(host=RUNNER.FLOW_HOST, models=[RUNNER.REQUIRED_MODEL], outputs=['x1'],
                    aspects=['16:9'], durations=['8s'], accounts=[RUNNER.REQUIRED_ACCOUNT],
                    prices=['Generating will use 100 credits'], balances=[10000],
                    ultra=True, create_count=1)

    class Page:
        def __init__(self, evidence, before_click=None):
            self.evidence, self.before_click = evidence, before_click
            self.clicks = 0
        def evaluate(self, js, expected):
            if expected is None:
                return dict(self.evidence)
            if self.before_click:
                self.before_click()
            if self.evidence != expected:
                return dict(clicked=False, reason='live UI changed', evidence=self.evidence)
            self.clicks += 1
            return dict(clicked=True, evidence=self.evidence)

    def test_rejects_each_drift_without_create_or_intent(self):
        for field, value in dict(host='example.com', models=['Veo 3.1 - Fast'], outputs=['x2'],
                                 aspects=['9:16'], durations=['4s'], accounts=[RUNNER.FORBIDDEN_ACCOUNT],
                                 prices=['Generating will use 200 credits'], balances=[],
                                 ultra=False, create_count=2).items():
            with self.subTest(field=field), tempfile.TemporaryDirectory() as tmp:
                state = Path(tmp)
                with RUNNER.SharedFlowAccounting(state) as account:
                    account.reserve('job', 'HOS:009', 6000, live=10000)
                    evidence = self.evidence(); evidence[field] = value
                    page = self.Page(evidence)
                    with self.assertRaises(RUNNER.GuardError):
                        RUNNER.guarded_create(page, account, reservation='job', charge='take',
                                              evidence_path=state/'evidence.json')
                    self.assertEqual(page.clicks, 0)
                    self.assertFalse(account.snapshot()['charges'])

    def test_intent_and_evidence_exist_before_click(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            with RUNNER.SharedFlowAccounting(state) as account:
                account.reserve('job', 'HOS:009', 6000, live=10000)
                def check():
                    self.assertTrue(account.snapshot()['pending'])
                    self.assertTrue((state/'evidence.json').is_file())
                page = self.Page(self.evidence(), check)
                RUNNER.guarded_create(page, account, reservation='job', charge='take',
                                      evidence_path=state/'evidence.json')
                self.assertEqual(page.clicks, 1)
                self.assertEqual(account.snapshot()['charges']['take']['status'], 'CHARGED')
                # Same take cannot click twice, even with a different evidence file.
                with self.assertRaises(RUNNER.GuardError):
                    RUNNER.guarded_create(page, account, reservation='job', charge='take',
                                          evidence_path=state/'retry.json')
                self.assertEqual(page.clicks, 1)

    def test_last_moment_drift_resolves_only_explicit_no_click(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            with RUNNER.SharedFlowAccounting(state) as account:
                account.reserve('job', 'HOS:009', 6000, live=10000)
                page = self.Page(self.evidence())
                page.before_click = lambda: page.evidence.update(outputs=['x4'])
                with self.assertRaises(RUNNER.GuardError):
                    RUNNER.guarded_create(page, account, reservation='job', charge='take',
                                          evidence_path=state/'evidence.json')
                self.assertEqual(page.clicks, 0)
                self.assertEqual(account.snapshot()['charges']['take']['status'], 'NOT_SUBMITTED')

    def test_browser_disconnect_preserves_pending_and_blocks_other_channel(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            with RUNNER.SharedFlowAccounting(state) as account:
                account.reserve('job', 'HOS:009', 6000, live=10000)
                def disconnect():
                    raise ConnectionError('fake browser disconnected around click')
                page = self.Page(self.evidence(), disconnect)
                with self.assertRaises(ConnectionError):
                    RUNNER.guarded_create(page, account, reservation='job', charge='take',
                                          evidence_path=state/'evidence.json')
            with RUNNER.SharedFlowAccounting(state) as account:
                self.assertTrue(account.snapshot()['pending'])
                with self.assertRaises(RUNNER.GuardError):
                    account.reserve('other', 'OWB:032', 100, live=10000)

    def test_adapter_requires_shared_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp); page = self.Page(self.evidence())
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.guarded_create(page, RUNNER.SharedFlowAccounting(state),
                                      reservation='job', charge='take', evidence_path=state/'e.json')
            self.assertEqual(page.clicks, 0)

    def test_actual_dom_script_rejects_unselected_menu_and_atomic_drift(self):
        # Execute the production JavaScript against a small DOM browser fixture,
        # rather than allowing the Python fake to stand in for selector behavior.
        harness = r"""
const fs = require('fs'); const input = JSON.parse(fs.readFileSync(0,'utf8'));
let clicks=0;
const node = (t, attrs={}) => ({innerText:t, disabled:false,
 getAttribute:k=>attrs[k] || null,
 getBoundingClientRect:()=>({width:100,height:20}), click:()=>{clicks++;}});
let selected = [node('Veo 3.1 - Quality'),node('x1'),node('16:9'),node('8s')];
const account = node('', {'aria-label':'Google Account: '+input.account});
const create = node('arrow_forward');
global.location={hostname:'flow.google.com'};
global.getComputedStyle=()=>({visibility:'visible',display:'block'});
global.document={body:{innerText:'ULTRA\n10,000 AI credits\nGenerating will use 100 credits'},
 querySelectorAll:q=>q==='button' ? [create] : q==='[aria-label]' ? [account] : selected};
const fn = eval('('+input.js+')'); const evidence=fn(null);
if (input.menuOnly) selected=selected.filter(n=>n.innerText!=='x1');
if (input.drift) selected[1]=node('x4');
const outcome=fn(input.menuOnly ? null : evidence);
process.stdout.write(JSON.stringify({evidence,outcome,clicks}));
"""
        for drift, menu in [(False,False),(True,False),(False,True)]:
            result = subprocess.run(['node','-e',harness], input=json.dumps(dict(
                js=RUNNER.CREATE_EVIDENCE_JS, account=RUNNER.REQUIRED_ACCOUNT,
                drift=drift, menuOnly=menu)), text=True, capture_output=True, check=True)
            data=json.loads(result.stdout)
            self.assertEqual(data['evidence'], self.evidence())
            self.assertEqual(data['clicks'], 0 if drift or menu else 1)
            if menu:
                self.assertEqual(data['outcome']['outputs'], [])

    def still_evidence(self):
        return dict(host=RUNNER.FLOW_HOST, models=[RUNNER.REQUIRED_STILL_MODEL], outputs=['x1'],
                    aspects=['16:9'], accounts=[RUNNER.REQUIRED_ACCOUNT],
                    prices=['Generating will use 0 credits'], balances=[10000],
                    ultra=True, create_count=1)

    def test_still_guard_rejects_nonzero_price_drift_and_low_headroom(self):
        for field, value in dict(host='example.com', models=['Veo 3.1 - Fast'], outputs=['x2'],
                                 aspects=['9:16'], accounts=[RUNNER.FORBIDDEN_ACCOUNT],
                                 prices=['Generating will use 10 credits'], balances=[8900],
                                 ultra=False, create_count=2).items():
            with self.subTest(field=field), tempfile.TemporaryDirectory() as tmp:
                state = Path(tmp)
                with RUNNER.SharedFlowAccounting(state) as account:
                    account.reserve('job', 'HOS:009', 6000, live=10000)
                    evidence = self.still_evidence()
                    evidence[field] = value
                    page = self.Page(evidence)
                    with self.assertRaises(RUNNER.GuardError):
                        RUNNER.guarded_still_create(
                            page, account, reservation='job', plate_id='10_how_high',
                            evidence_path=state / 'still.json')
                    self.assertEqual(page.clicks, 0)

    def test_still_dom_script_verifies_zero_price_and_clicks_once(self):
        harness = r"""
const fs = require('fs'); const input = JSON.parse(fs.readFileSync(0,'utf8'));
let clicks=0;
const node = (t, attrs={}) => ({innerText:t, disabled:false,
 getAttribute:k=>attrs[k] || null,
 getBoundingClientRect:()=>({width:100,height:20}), click:()=>{clicks++;}});
let selected = [node('Nano Banana 2'),node('x1'),node('16:9')];
const account = node('', {'aria-label':'Google Account: '+input.account});
const create = node('Start generation');
global.location={hostname:'flow.google.com'};
global.getComputedStyle=()=>({visibility:'visible',display:'block'});
global.document={body:{innerText:'ULTRA\n10,000 AI credits\nGenerating will use 0 credits'},
 querySelectorAll:q=>q==='button' ? [create] : q==='[aria-label]' ? [account] : selected};
const fn = eval('('+input.js+')'); const evidence=fn(null);
if (input.drift) selected[2]=node('9:16');
const outcome=fn(evidence);
process.stdout.write(JSON.stringify({evidence,outcome,clicks}));
"""
        for drift in (False, True):
            result = subprocess.run(
                ['node', '-e', harness],
                input=json.dumps(dict(js=RUNNER.STILL_EVIDENCE_JS,
                                      account=RUNNER.REQUIRED_ACCOUNT, drift=drift)),
                text=True, capture_output=True, check=True,
            )
            data = json.loads(result.stdout)
            self.assertEqual(data['evidence'], self.still_evidence())
            self.assertEqual(data['clicks'], 0 if drift else 1)


if __name__ == "__main__":
    unittest.main()
