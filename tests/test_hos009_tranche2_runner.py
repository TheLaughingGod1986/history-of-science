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
                still.write_bytes(b"still")
            (root / "archive").mkdir()
            now = datetime.now(timezone.utc)
            written = RUNNER.execute_batch(
                parents, media=media, ledger_path=root / "ledger.jsonl", lock_path=root / "writer.lock",
                live=15430, other=0, price=price(), account=RUNNER.REQUIRED_ACCOUNT,
                read_at=now.isoformat(), now=now, submitter=submitter,
                archive_dir=root / "archive", receipt_path=root / "receipt.json",
            )
            self.assertEqual([item[0] for item in calls], ["10_how_high", "07_ball_to_moon"])
            self.assertTrue(all(item[1] for item in calls))
            self.assertTrue(all(entry["status"] == "PENDING_REVIEW" and entry["keep"] is False
                                and entry["generated"] is True and entry["file_state"] == "GENERATED"
                                for entry in written))
            ledger = RUNNER.read_ledger(root / "ledger.jsonl")
            self.assertNotIn("KEEP", {entry["status"] for entry in ledger})
            archived = list((root / "archive").glob("part*/*.mp4"))
            self.assertEqual(len(archived), 2)
            sums = "".join(p.read_text() for p in (root / "archive").glob("part*/SHA256SUMS.txt"))
            self.assertIn(RUNNER.sha256_file(archived[0]), sums)
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
        command = RUNNER.detached_command(SCRIPT, Path("/tmp/j2200.log"), Path("/tmp/j2200.done"),
                                          media=ROOT, archive=ROOT, ledger=Path("/tmp/ledger"),
                                          lock=Path("/tmp/lock"), pid=Path("/tmp/pid"), other=0, repo=ROOT)
        self.assertEqual(command[:4], ["tmux", "new", "-d", "-s"])
        self.assertIn("/tmp/j2200.log", command[-1])
        self.assertIn("/tmp/j2200.done", command[-1])
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


class RepairRegressionTests(unittest.TestCase):
    def test_full_reservation_includes_impending_take(self):
        for live in (8900, 8999):
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.can_take(live=live, spent=0, pending=0, other=0,
                                takes_done=0, unknown_pending=False)
        self.assertEqual(RUNNER.can_take(live=9000, spent=0, pending=0, other=0,
                                        takes_done=0, unknown_pending=False), 3000)

    def test_delayed_deductions_do_not_release_reservations(self):
        for spent, pending in ((0, 100), (100, 0), (300, 200), (5900, 0)):
            self.assertEqual(RUNNER.headroom(10000, spent, pending, 1000), 3000)
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.headroom(9999, spent, pending, 1000)
        with self.assertRaises(RUNNER.GuardError):
            RUNNER.headroom(20000, 5900, 200, 0)

    def test_archive_collision_preserves_existing_bytes_and_retry_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src, dest = root / "src", root / "archive" / "clip"
            src.write_bytes(b"approved bytes")
            first = RUNNER.archive_verified(src, dest)
            self.assertEqual(RUNNER.archive_verified(src, dest), first)
            src.write_bytes(b"different bytes")
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.archive_verified(src, dest)
            self.assertEqual(dest.read_bytes(), b"approved bytes")

    def test_receipts_are_immutable(self):
        with tempfile.TemporaryDirectory() as tmp:
            receipt = Path(tmp) / "receipt.json"
            RUNNER.write_receipt(receipt, ["parent"], [{"hash": "abc"}])
            original = receipt.read_bytes()
            RUNNER.write_receipt(receipt, ["parent"], [{"hash": "abc"}])
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.write_receipt(receipt, ["parent"], [{"hash": "different"}])
            self.assertEqual(receipt.read_bytes(), original)

    def test_missing_archive_stops_before_submit(self):
        rows = RUNNER.order_rows(RUNNER.load_scope(ROOT))
        now = datetime.now(timezone.utc)
        calls = []
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.execute_batch(rows[:1], media=root, ledger_path=root / "ledger",
                                     lock_path=root / "lock", live=20000, other=0,
                                     price=price(), account=RUNNER.REQUIRED_ACCOUNT,
                                     read_at=now.isoformat(), now=now,
                                     submitter=lambda *a: calls.append(a))
        self.assertEqual(calls, [])

    def test_technical_guard_requires_hd_eight_second_decodable_video(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            good = silent_mp4(root)
            self.assertTrue(RUNNER.technical_report(good)["ok"])
            for name, spec in (("short", "1280x720:d=1"), ("small", "160x90:d=8"),
                               ("portrait", "720x1280:d=8")):
                bad = root / (name + ".mp4")
                subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                                "color=c=blue:s=" + spec + ":r=25", "-c:v", "libx264",
                                "-pix_fmt", "yuv420p", "-an", str(bad)], check=True)
                self.assertFalse(RUNNER.technical_report(bad)["ok"], name)
            broken = root / "broken.mp4"
            broken.write_bytes(b"not video" * 100)
            self.assertFalse(RUNNER.technical_report(broken)["ok"])

    def test_failed_output_is_archived_but_does_not_advance_or_become_parent(self):
        parents = RUNNER.order_rows(RUNNER.load_scope(ROOT))[:2]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "archive"
            archive.mkdir()
            row = parents[0]
            still = RUNNER.still_path(root, row.part, row.plate_id)
            still.parent.mkdir(parents=True)
            still.write_bytes(b"test input")
            def bad_submit(row, dest, frame):
                dest.write_bytes(b"invalid output")
            now = datetime.now(timezone.utc)
            # Invalid media is preserved, charged and refused as a parent.
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.execute_batch(parents[:1], media=root, ledger_path=root / "ledger",
                                     lock_path=root / "lock", live=20000, other=0,
                                     price=price(), account=RUNNER.REQUIRED_ACCOUNT,
                                     read_at=now.isoformat(), now=now, submitter=bad_submit,
                                     archive_dir=archive)
            ledger = RUNNER.read_ledger(root / "ledger")
            self.assertEqual(ledger[-1]["status"], "FAILED")
            self.assertTrue(ledger[-1]["archive"]["verified"])
            self.assertEqual(RUNNER.next_batch(RUNNER.load_scope(ROOT), ledger)[0].key, row.key)
            parent = RUNNER.ParentRef(row.part, row.plate_id, "test")
            self.assertIsNone(RUNNER.resolve_parent_clip(root, parent, in_scope=True, ledger=ledger))

    def test_verified_parent_version_and_hash_are_required(self):
        row = RUNNER.order_rows(RUNNER.load_scope(ROOT))[0]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            clip = silent_mp4(root)
            archive = RUNNER.archive_verified(clip, root / "archive" / "parent.mp4")
            good = RUNNER.review_record(row.plate_id, row.part, 2, clip, RUNNER.technical_report(clip))
            good["archive"] = archive
            failed = dict(good, take=1, technical={"ok": False})
            parent = RUNNER.ParentRef(row.part, row.plate_id, "test")
            self.assertEqual(RUNNER.resolve_parent_clip(root, parent, in_scope=True,
                                                       ledger=[failed, good]), clip)
            self.assertIsNone(RUNNER.resolve_parent_clip(root, parent, in_scope=True, ledger=[failed]))
            clip.write_bytes(b"changed")
            self.assertIsNone(RUNNER.resolve_parent_clip(root, parent, in_scope=True, ledger=[good]))

    def test_live_pid_wins_over_stale_done(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            child = subprocess.Popen(["sleep", "30"])
            try:
                (root / "pid").write_text(str(child.pid))
                (root / "done").write_text("0")
                with self.assertRaises(RUNNER.GuardError):
                    RUNNER.refuse_duplicate(root / "pid", root / "done")
            finally:
                child.kill()
                child.wait()

    def test_detached_command_propagates_arguments_to_fake_entrypoint(self):
        with tempfile.TemporaryDirectory(prefix="j2275 args ") as tmp:
            root = Path(tmp)
            script = root / "fake entry.py"
            script.write_text("import json,sys;from pathlib import Path;"
                              "Path(__file__).with_suffix('.json').write_text(json.dumps(sys.argv[1:]))")
            command = RUNNER.detached_command(script, root / "log", root / "done",
                                              media=root, archive=root, ledger=root / "ledger",
                                              lock=root / "lock", pid=root / "pid", other=123, repo=ROOT)
            result = subprocess.run(["/bin/sh", "-c", command[-1]], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            argv = json.loads(script.with_suffix('.json').read_text())
            for arg, value in (("--media", root), ("--archive", root), ("--ledger", root / "ledger"),
                               ("--lock", root / "lock"), ("--pid", root / "pid"),
                               ("--other-reservations", 123), ("--repo", ROOT)):
                self.assertEqual(argv[argv.index(arg) + 1], str(value))
            done = Path(argv[argv.index("--done") + 1])
            self.assertEqual(done.read_text().strip(), "0")

    def test_incomplete_repair_cannot_reach_browser_even_when_armed(self):
        from unittest.mock import patch
        with patch.dict(os.environ, {RUNNER.SUBMIT_ENV: "1"}):
            with self.assertRaisesRegex(RUNNER.GuardError, "J2275 incomplete"):
                RUNNER.cmd_submit(ROOT, other=0, media=ROOT, ledger_path=ROOT / "unused",
                                  lock_path=ROOT / "unused", pid_path=Path(tempfile.gettempdir()) / "j2275-test.pid",
                                  done_path=ROOT / "unused", archive_dir=ROOT)


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


if __name__ == "__main__":
    unittest.main()


class SharedAccountingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def state(self):
        return RUNNER.SharedFlowState(self.root / 'state', self.root / 'writer.lock')

    def test_full_cap_boundary_and_other_channel_reservations(self):
        with self.state() as state:
            state.reserve('HOS:009', 6000)
            with self.assertRaises(RUNNER.GuardError):
                state.begin('HOS:009', 'take1', 8900, {'ui': 'proof'})
            self.assertEqual(state.state['takes'], {})
            state.reserve('OWB:031', 500)
            with self.assertRaises(RUNNER.GuardError):
                state.begin('HOS:009', 'take1', 9000, {'ui': 'proof'})
            state.begin('HOS:009', 'take1', 9500, {'ui': 'proof'})
            self.assertEqual(state.liabilities('HOS:009'), (5900, 500, 100))

    def test_crash_preserves_uncertain_create_and_refuses_retry(self):
        with self.state() as state:
            state.reserve('HOS:009', 6000)
            state.begin('HOS:009', 'uncertain', 9000, {'ui': 'proof'})
        with self.state() as recovered:
            for take_id in ('uncertain', 'new-id'):
                with self.assertRaises(RUNNER.GuardError):
                    recovered.begin('HOS:009', take_id, 10000, {'ui': 'proof'})
            with self.assertRaises(RUNNER.GuardError):
                recovered.reconcile_posted('uncertain', {
                    'external_charge_id': 'bill1', 'balance_read_at': 'now'})

    def test_pending_charge_remains_liability_until_explicit_reconciliation(self):
        with self.state() as state:
            state.reserve('HOS:009', 6000)
            state.begin('HOS:009', 'one', 9000, {'ui': 'proof'})
            state.complete('one', {'sha256': 'fixture'})
            self.assertEqual(state.liabilities('HOS:009'), (5900, 0, 100))
            with self.assertRaises(RUNNER.GuardError):
                state.begin('HOS:009', 'two', 8900, {'ui': 'proof'})
            proof = {'external_charge_id': 'bill1', 'balance_read_at': 'now'}
            state.reconcile_posted('one', proof)
            state.reconcile_posted('one', proof)
            self.assertEqual(state.liabilities('HOS:009'), (5900, 0, 0))
            state.begin('HOS:009', 'two', 8900, {'ui': 'proof'})
            state.complete('two', {'failed': True}, failed=True)
            with self.assertRaises(RUNNER.GuardError):
                state.reconcile_posted('two', proof)
            self.assertEqual(state.spend_receipt('one'), state.spend_receipt('one'))

    def test_separate_process_cannot_write_through_held_lock(self):
        with self.state():
            code = '''import importlib.util,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('runner',sys.argv[1])
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
try:
    with m.SharedFlowState(Path(sys.argv[2]),Path(sys.argv[3])): pass
except m.GuardError:
    sys.exit(17)
sys.exit(1)
'''
            result = subprocess.run([sys.executable, '-c', code, str(SCRIPT),
                                     str(self.root / 'state'), str(self.root / 'writer.lock')],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 17, result.stderr)

    def test_default_paths_ignore_checkout_and_repo_override(self):
        from unittest.mock import patch
        with patch.dict(os.environ, {'HOS_REPO': '/other/worktree', 'OWB_REPO': '/other/channel'}):
            state = RUNNER.SharedFlowState()
        self.assertEqual(state.root, Path.home() / '_desk/state/flow')
        self.assertEqual(state.lock_path, Path.home() / '_desk/locks/flow-generation.lock')

    def test_corrupt_journal_fails_closed_then_releases_lock(self):
        (self.root / 'state').mkdir()
        journal = self.root / 'state/state.json'
        journal.write_text('{broken')
        with self.assertRaises(json.JSONDecodeError):
            with self.state():
                pass
        journal.write_text('{"schema":1,"takes":{},"reservations":{}}')
        with self.state() as state:
            state.reserve('HOS:009', 6000)
        self.assertEqual(json.loads(journal.read_text())['reservations'], {'HOS:009': 6000})


class StillInventoryTests(unittest.TestCase):
    def test_missing_corrupt_small_and_valid_inventory(self):
        rows = [row for row in RUNNER.load_scope(ROOT) if row.parent is None][:1]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp)
            path = RUNNER.still_path(media, row.part, row.plate_id)
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.verify_still_inventory(rows, media)
            path.parent.mkdir(parents=True)
            path.write_bytes(b'not an image')
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.verify_still_inventory(rows, media)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
                            'color=s=640x360', '-frames:v', '1', str(path)], check=True)
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.verify_still_inventory(rows, media)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
                            'color=s=1280x720', '-frames:v', '1', str(path)], check=True)
            inventory = RUNNER.verify_still_inventory(rows, media)
            self.assertEqual(inventory[0]['sha256'], RUNNER.sha256_file(path))
            self.assertEqual(inventory[0]['path'], str(path.resolve()))
