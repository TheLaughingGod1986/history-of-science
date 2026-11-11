"""Film 009, the last remade shot: `05_minute_second_c2` (J2630 builds the path, J2586 makes the take, J2587 checks it).

Chief rulings on the desk (6792980991, 6798955014 point 2, 6799526318): c2 gets its own 100 credits, only after the
third take of the shot it continues, `05_minute_second_c1`, is KEEP on its half-second sheet. The runner path
`--retakes-j2630` is merged ahead of that check so no time is lost, and it is shut until the KEEP is written into its
scope file by a reviewed change. These tests read files and use fakes. They never arm Flow and never submit a take.
"""
import copy
import hashlib
import importlib.util
import json
import os
import shlex
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
EDIT = ROOT / "02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project"
SCRIPT = EDIT / "_mint_flow_v05_tranche2.py"
SCOPE_FILE = EDIT / "TRANCHE2_RETAKES_J2630.json"
C1, C2 = (4, "05_minute_second_c1"), (4, "05_minute_second_c2")
KEPT = "c" * 64                      # stands for the sha256 of c1 take 3
RULING = "history-of-science#180 comment 0000000000"


def load_runner():
    name = "c2_path_runner_009"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


RUNNER = load_runner()


def ledger(c1=(1, 2, 3), c2=(1,), c1_sha=KEPT, **last_c2):
    """Ledger lines: c1 on these takes (its highest carries `c1_sha`), c2 on these takes."""
    entries = [{"part": 4, "plate_id": C1[1], "take": n, "status": "PENDING_REVIEW",
                "sha256": c1_sha if n == c1[-1] else f"{n}" * 64} for n in c1]
    for n in c2:
        entry = {"part": 4, "plate_id": C2[1], "take": n, "status": "PENDING_REVIEW"}
        if n == c2[-1]:
            entry.update(last_c2)
        entries.append(entry)
    return entries


def keep(**change):
    record = {"part": 4, "id": C1[1], "take": 3, "sha256": KEPT, "ruling": RULING}
    record.update(change)
    return record


def scope_with(parent_keep, **change):
    """The scope file as it is, with a KEEP recorded (as the later reviewed change will) and any other edit."""
    scope = json.loads(SCOPE_FILE.read_text())
    scope["parent_keep"] = parent_keep
    scope.update(change)
    return patch.object(RUNNER.json, "loads", return_value=scope)


class TheScope(unittest.TestCase):
    def setUp(self):
        self.scope = json.loads(SCOPE_FILE.read_text())

    def test_one_row_c2_one_second_take(self):
        rows = self.scope["rows"]
        self.assertEqual([(r["part"], r["id"], r["take"], r["order"]) for r in rows], [(4, "05_minute_second_c2", 2, 1)])
        self.assertEqual(tuple((r["part"], r["id"]) for r in rows), RUNNER.J2630_KEYS)
        self.assertEqual((self.scope["job"], self.scope["take_made_by_job"], self.scope["takes_per_row"]), ("J2630", "J2586", 1))
        self.assertIn("TAKE 3", rows[0]["start_frame"])
        self.assertIn("never take 1's or take 2's", rows[0]["start_frame"])
        self.assertIn("05_minute_second_c1 take 3 is KEEP", rows[0]["only_after"])

    def test_the_money_is_the_last_of_the_ceiling_and_no_cash(self):
        s = self.scope
        self.assertEqual((s["spent_before_by_j2583"], s["spent_before_by_j2626"], s["reservation_cap"]), (300, 200, 100))
        self.assertEqual(s["spent_before_by_j2583"] + s["spent_before_by_j2626"] + s["reservation_cap"], s["max_total_credits"])
        self.assertEqual((s["max_total_credits"], s["max_credits_per_take"], s["cash_gbp"]), (600, 100, 0))
        self.assertEqual((RUNNER.J2630_RESERVE_CAP, RUNNER.J2630_CEILING), (100, 600))
        self.assertEqual(RUNNER.J2583_RESERVE_CAP + RUNNER.J2626_RESERVE_CAP + RUNNER.J2630_RESERVE_CAP, RUNNER.J2630_CEILING)

    def test_it_pins_the_board_as_it_is_with_the_ball_line_already_out(self):
        row = self.scope["rows"][0]
        self.assertEqual(row["board_sha256"], RUNNER.sha256_file(ROOT / row["board"]))
        tranche = json.loads((EDIT / "TRANCHE2_SCOPE_J2026.json").read_text())
        pinned = next(r for r in tranche["rows"] if (int(r["part"]), r["id"]) == C2)
        self.assertEqual((row["board"], row["board_sha256"]), (pinned["board"], pinned["board_sha256"]))
        prompt = next(r for r in RUNNER.load_scope(ROOT) if r.key == C2).prompt
        self.assertIn("both apples lie still on the table beside the ruler for the entire shot and never move", prompt)
        self.assertNotIn("ball or path", prompt)                              # taken out in #528 (desk 6799192880)

    def test_as_merged_no_keep_is_recorded(self):
        self.assertIsNone(self.scope["parent_keep"])
        self.assertIn("refuses until it is set", self.scope["parent_keep_how"])
        self.assertIn("never used", self.scope["if_c1_fails"])


class ShutUntilTheKeepIsRecorded(unittest.TestCase):
    def setUp(self):
        self.rows = RUNNER.load_scope(ROOT)

    def batch(self, entries, media="/unused"):
        return RUNNER.retake_batch(ROOT, self.rows, entries, Path(media), "J2630")

    def test_as_merged_the_path_refuses_even_when_every_take_is_in_place(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(RUNNER, "verified_output", return_value=True):
            with self.assertRaisesRegex(RUNNER.GuardError, "05_minute_second_c1 take 3 is not recorded KEEP"):
                self.batch(ledger(), tmp)

    def test_with_the_keep_recorded_it_makes_c2_and_only_c2(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(RUNNER, "verified_output", return_value=True), \
                scope_with(keep()):
            batch = self.batch(ledger(), tmp)
        self.assertEqual([r.key for r in batch], [C2])
        self.assertEqual((batch[0].parent.part, batch[0].parent.plate_id), C1)   # it continues from c1

    def test_a_keep_that_is_not_c1_take_three_with_its_ruling_is_refused(self):
        bad = (keep(take=2), keep(take=1), keep(id="05_minute_second_c2"), keep(id="08_the_apple_c1", part=2),
               keep(part=3), keep(ruling=""), keep(ruling="  "))
        with tempfile.TemporaryDirectory() as tmp, patch.object(RUNNER, "verified_output", return_value=True):
            for record in bad:
                with self.subTest(record=record), scope_with(record):
                    with self.assertRaisesRegex(RUNNER.GuardError, "the KEEP on record is not 05_minute_second_c1 take 3"):
                        self.batch(ledger(), tmp)
            for record in (keep(sha256="xyz"), keep(sha256=None), keep(sha256=KEPT.upper()), {}, "yes", True, [keep()]):
                with self.subTest(record=record), scope_with(record):
                    with self.assertRaisesRegex(RUNNER.GuardError, "is not recorded KEEP"):
                        self.batch(ledger(), tmp)

    def test_the_keep_must_be_the_very_take_the_ledger_holds(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(RUNNER, "verified_output", return_value=True), \
                scope_with(keep()):
            with self.assertRaisesRegex(RUNNER.GuardError, "is not the 05_minute_second_c1 take 3 the ledger holds"):
                self.batch(ledger(c1_sha="d" * 64), tmp)

    def test_c1_must_be_on_takes_one_to_three_with_take_three_finished(self):
        with tempfile.TemporaryDirectory() as tmp, scope_with(keep()):
            with patch.object(RUNNER, "verified_output", return_value=True):
                for c1 in ((1, 2), (1,), (), (1, 3), (2, 3)):
                    with self.subTest(c1=c1):
                        with self.assertRaisesRegex(RUNNER.GuardError, "requires 05_minute_second_c1 on takes 1 to 3 only"):
                            self.batch(ledger(c1=c1), tmp)
            # c2's own take 1 is fine, but c1's take 3 is not a finished, archived output
            with patch.object(RUNNER, "verified_output", side_effect=lambda e: e["plate_id"] == C2[1]):
                with self.assertRaisesRegex(RUNNER.GuardError, "with take 3 verified"):
                    self.batch(ledger(), tmp)

    def test_c2_must_hold_take_one_only_and_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp, scope_with(keep()):
            with patch.object(RUNNER, "verified_output", return_value=True):
                for status in ("SUBMITTING", "FAILED", "FAILED_POLICY", "PENDING_REVIEW"):
                    with self.assertRaisesRegex(RUNNER.GuardError, "J2630 requires verified take 1 only"):
                        self.batch(ledger(c2=(1, 2), status=status), tmp)
                with self.assertRaisesRegex(RUNNER.GuardError, "J2630 requires verified take 1 only"):
                    self.batch(ledger(c2=()), tmp)
                dest = RUNNER.versioned_output(Path(tmp), *C2, 2)
                dest.parent.mkdir(parents=True)
                dest.write_bytes(b"preserve")
                with self.assertRaisesRegex(RUNNER.GuardError, "J2630 must write take 2 without overwriting any output"):
                    self.batch(ledger(), tmp)
                self.assertEqual(dest.read_bytes(), b"preserve")
            with patch.object(RUNNER, "verified_output", side_effect=lambda e: e["plate_id"] == C1[1]):
                with self.assertRaisesRegex(RUNNER.GuardError, "J2630 requires verified take 1 only"):
                    self.batch(ledger(), tmp)

    def test_every_other_row_is_refused(self):
        by_key = {r.key: r for r in self.rows}
        c1, c2 = by_key[C1], by_key[C2]
        with tempfile.TemporaryDirectory() as tmp:
            for batch in ([c1], [c2, c1], [c1, c2], [c2, c2], [by_key[(2, "08_the_apple_c1")]], self.rows[:1], self.rows, []):
                with self.assertRaisesRegex(RUNNER.GuardError, "J2630 permits only c2, never another row"):
                    RUNNER.validate_retakes(batch, ledger(), Path(tmp), "J2630")

    def test_a_changed_scope_file_is_refused(self):
        changes = [("max_total_credits", 700), ("max_total_credits", 100), ("takes_per_row", 2), ("max_credits_per_take", 200),
                   ("reservation_cap", 200), ("spent_before_by_j2583", 0), ("spent_before_by_j2626", 0), ("job", "J2626")]
        with patch.object(RUNNER, "verified_output", return_value=True):
            for field, value in changes:
                with self.subTest(field=field, value=value), scope_with(keep(), **{field: value}):
                    with self.assertRaisesRegex(RUNNER.GuardError, "differs from the approved one second take of c2"):
                        self.batch(ledger())
            original = json.loads(SCOPE_FILE.read_text())

            def rows(edit):
                changed = copy.deepcopy(original["rows"])
                edit(changed)
                return changed
            for changed in (rows(lambda r: r[0].update(take=3)), rows(lambda r: r[0].update(id="05_minute_second_c1")),
                            rows(lambda r: r.append(dict(r[0], id="05_minute_second_c1"))), rows(lambda r: r.clear())):
                with scope_with(keep(), rows=changed):
                    with self.assertRaisesRegex(RUNNER.GuardError, "differs from the approved one second take of c2"):
                        self.batch(ledger())
            with scope_with(keep(), rows=rows(lambda r: r[0].update(board_sha256="0" * 64))):
                with self.assertRaisesRegex(RUNNER.GuardError, "J2630 retake board hash mismatch"):
                    self.batch(ledger())


class TheStartFrame(unittest.TestCase):
    """c2 starts from the last frame of c1's third take, never from take 1's or take 2's."""

    def test_the_runner_takes_the_last_frame_of_the_highest_verified_take_of_c1(self):
        rows = RUNNER.load_scope(ROOT)
        c2 = next(r for r in rows if r.key == C2)
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp)
            entries = []
            for n in (1, 2, 3):
                clip = media / f"c1_t{n}.mp4"
                clip.write_bytes(f"take {n}".encode())
                entries.append({"part": 4, "plate_id": C1[1], "take": n, "file": str(clip)})
            used = []

            def extract(src, dest):
                used.append(Path(src).name)
                return dest
            with patch.object(RUNNER, "verified_output", return_value=True), \
                    patch.object(RUNNER, "extract_last_frame", side_effect=extract):
                RUNNER.prepare_start_frame(c2, media, in_scope_keys={r.key for r in rows}, still_price=None,
                                           still_maker=None, ledger=entries)
            self.assertEqual(used, ["c1_t3.mp4"])

    def test_the_path_insists_take_three_is_that_highest_verified_take(self):
        # prepare_start_frame falls back to a lower take when the highest is not verified. This path refuses first.
        rows = RUNNER.load_scope(ROOT)
        with tempfile.TemporaryDirectory() as tmp, scope_with(keep()), \
                patch.object(RUNNER, "verified_output", side_effect=lambda e: e.get("take") != 3):
            with self.assertRaisesRegex(RUNNER.GuardError, "with take 3 verified"):
                RUNNER.retake_batch(ROOT, rows, ledger(), Path(tmp), "J2630")


class TheReservation(unittest.TestCase):
    """Its own identity at 100, written before any local line, released after the one row."""

    def test_the_ceiling_is_600_and_the_three_reservations_fill_it(self):
        self.assertEqual(RUNNER.retake_credit_cap(ROOT, "J2630"), 600)
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            dest = repo / RUNNER.EDIT_REL
            dest.mkdir(parents=True)
            scope = json.loads(SCOPE_FILE.read_text())
            for ceiling, message in ((700, "approved 600"), (500, "approved 600"), (50, "exceeds the approved ceiling")):
                scope["max_total_credits"] = ceiling
                (dest / "TRANCHE2_RETAKES_J2630.json").write_text(json.dumps(scope))
                with self.assertRaisesRegex(RUNNER.GuardError, message):
                    RUNNER.retake_credit_cap(repo, "J2630")
            with self.assertRaisesRegex(RUNNER.GuardError, "J2630 retake cap file is missing or invalid"):
                RUNNER.retake_credit_cap(Path(tmp) / "nowhere", "J2630")
        with patch.object(RUNNER, "J2626_RESERVE_CAP", 300):
            with self.assertRaisesRegex(RUNNER.GuardError, "J2630 reservation goes over the approved ceiling"):
                RUNNER.retake_credit_cap(ROOT, "J2630")

    def test_cmd_submit_reserves_j2630_at_100_and_only_for_its_flag(self):
        row = next(r for r in RUNNER.load_scope(ROOT) if r.key == C2)
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {RUNNER.SUBMIT_ENV: "1"}):
            root = Path(tmp)
            (root / "archive").mkdir()
            common = dict(other=0, media=root / "media", ledger_path=root / "ledger.jsonl", lock_path=root / "writer.lock",
                          pid_path=root / "runner.pid", done_path=root / "runner.done", archive_dir=root / "archive",
                          test_archive=True)
            with patch.object(RUNNER, "retake_batch", return_value=[row]) as chosen, \
                    patch.object(RUNNER, "execute_shared_batch", return_value=[]) as run:
                RUNNER.cmd_submit(ROOT, retakes_j2630=True, **common)
            self.assertEqual(chosen.call_args.args[-1], "J2630")
            self.assertEqual((run.call_args.kwargs["reservation"], run.call_args.kwargs["reservation_cap"]), ("J2630", 100))
            self.assertTrue(run.call_args.kwargs["retakes_j2630"])
            self.assertNotIn("retakes_j2626", run.call_args.kwargs)
            for pair in (dict(retakes_j2583=True, retakes_j2630=True), dict(retakes_j2626=True, retakes_j2630=True),
                         dict(retakes_j2583=True, retakes_j2626=True, retakes_j2630=True)):
                with self.assertRaisesRegex(RUNNER.GuardError, "one retake job a run"):
                    RUNNER.cmd_submit(ROOT, **pair, **common)
            self.assertFalse((root / "ledger.jsonl").exists())

    def test_the_batch_refuses_another_identity_or_another_amount(self):
        row = next(r for r in RUNNER.load_scope(ROOT) if r.key == C2)
        for reservation, cap in (("J2626", 200), ("J2630", 200), ("J2583", 300), ("J2033", 6000)):
            with tempfile.TemporaryDirectory() as tmp, self.subTest(reservation=reservation, cap=cap):
                root = Path(tmp)
                (root / "archive").mkdir()
                with self.assertRaisesRegex(RUNNER.GuardError, "J2630 retakes reserve identity J2630 at 100 credits"):
                    RUNNER.execute_shared_batch(
                        [row], media=root, ledger_path=root / "ledger.jsonl", archive_dir=root / "archive",
                        accounting_state=root / "shared", reservation=reservation, reservation_cap=cap,
                        submitter=lambda *a, **k: None, still_maker=None, test_archive=True, inventory_rows=[row],
                        retakes_j2630=True, in_scope_keys={row.key})

    def test_one_take_reserves_100_before_the_local_line_and_releases_after_it(self):
        row = next(r for r in RUNNER.load_scope(ROOT) if r.key == C2)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive, shared, ledger_path, media = root / "archive", root / "shared", root / "ledger.jsonl", root / "media"
            archive.mkdir()
            media.mkdir()
            for entry in ledger():
                RUNNER.append_ledger(ledger_path, dict(entry, keep=False, generated=True))
            # The Mini's state by then: the tranche identity closed, J2583 and J2626 spent and released.
            with RUNNER.SharedFlowAccounting(shared) as account:
                for identity, cap in (("J2033", 6000), ("J2583", 300), ("J2626", 200)):
                    account.reserve(identity, "HOS:009", cap, live=20000)
                    account.release(identity)
            before = (shared / "account.jsonl").read_bytes()
            seen = []

            def fake_frame(row, media_path, **kwargs):
                dest = media_path / f"{row.plate_id}.png"
                dest.write_bytes(b"last frame of c1 take 3")
                return dest

            def fake_submitter(row, dest, frame, *, accounting, reservation, reservation_cap,
                               charge, evidence_path, after_reserve, other=0):
                seen.append((reservation, reservation_cap, charge))
                accounting.reserve(reservation, "HOS:009", reservation_cap, live=11090, floor=3000)
                self.assertNotIn(charge, ledger_path.read_text())           # nothing local until the reserve is in
                after_reserve()
                self.assertIn(charge, ledger_path.read_text())
                accounting.intent(charge, reservation, 100, live=11090)
                accounting.resolve(charge, submitted=True, evidence={"charge": charge})
                dest.write_bytes(b"fake-video")
                return {"charge": charge}

            with patch.object(RUNNER, "verified_output", return_value=True), \
                    patch.object(RUNNER, "prepare_start_frame", side_effect=fake_frame), \
                    patch.object(RUNNER, "strip_audio"), \
                    patch.object(RUNNER, "technical_report",
                                 side_effect=lambda path, **kw: {"ok": True, "sha256": RUNNER.sha256_file(path)}):
                written = RUNNER.execute_shared_batch(
                    [row], media=media, ledger_path=ledger_path, archive_dir=archive, accounting_state=shared,
                    reservation="J2630", reservation_cap=100, submitter=fake_submitter, still_maker=None,
                    test_archive=True, inventory_rows=[row], retakes_j2630=True, in_scope_keys={row.key})
            self.assertEqual(seen, [("J2630", 100, "HOS:009:P04:05_minute_second_c2:t2")])
            self.assertEqual([(item["plate_id"], item["take"]) for item in written], [("05_minute_second_c2", 2)])
            self.assertEqual(written[0]["input"]["sha256"], hashlib.sha256(b"last frame of c1 take 3").hexdigest())
            after = (shared / "account.jsonl").read_bytes()
            self.assertTrue(after.startswith(before))
            suffix = after.split(before, 1)[1]
            for identity in (b"J2033", b"J2583", b"J2626"):
                self.assertNotIn(b'"id": "' + identity + b'"', suffix)
            with RUNNER.SharedFlowAccounting(shared) as account:
                snap = account.snapshot()
                self.assertEqual(snap["reservations"]["J2630"]["cap"], 100)
                self.assertFalse(snap["reservations"]["J2630"]["active"])     # released after its one row
                with self.assertRaisesRegex(RUNNER.GuardError, "inactive reservation"):
                    account.intent("another-take", "J2630", 100, live=11090)

    def test_one_resolved_row_releases_and_an_unresolved_create_does_not(self):
        with tempfile.TemporaryDirectory() as tmp:
            with RUNNER.SharedFlowAccounting(Path(tmp)) as account:
                account.reserve("J2630", "HOS:009", 100, live=11090)
                self.assertEqual(RUNNER.note_retake_resolution(account, "J2630", {"status": "PENDING", "amount": 100}, 0), 0)
                self.assertTrue(account.snapshot()["reservations"]["J2630"]["active"])
                self.assertEqual(RUNNER.note_retake_resolution(account, "J2630", {"status": "POLICY_REFUSED", "amount": 0}, 0), 1)
                self.assertFalse(account.snapshot()["reservations"]["J2630"]["active"])


class TheCommandLineAndTheOtherPaths(unittest.TestCase):
    def test_the_flag_reaches_the_detached_submit_and_no_other_flag_adds_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            common = dict(repo=ROOT, media=root, archive=root, other=0, ledger=root / "ledger.jsonl",
                          lock=root / "writer.lock", pid=root / "runner.pid")
            for name, flags in (("plain", {}), ("old", dict(retakes_j2583=True)), ("third", dict(retakes_j2626=True))):
                command = RUNNER.detached_command(SCRIPT, root / f"{name}.log", root / f"{name}.done", **flags, **common)
                self.assertNotIn("--retakes-j2630", command[-1])
            child = shlex.split(RUNNER.detached_command(SCRIPT, root / "c2.log", root / "c2.done",
                                                        retakes_j2630=True, **common)[-1])
            self.assertIn("--retakes-j2630", child)
            self.assertFalse({"--retakes-j2583", "--retakes-j2626"} & set(child))
            with self.assertRaisesRegex(RUNNER.GuardError, "one retake job a run"):
                RUNNER.detached_command(SCRIPT, root / "two.log", root / "two.done", retakes_j2626=True,
                                        retakes_j2630=True, **common)
            self.assertFalse((root / "c2.log").exists())                     # print-only: nothing is started

    def test_one_flag_a_run(self):
        self.assertIsNone(RUNNER.retake_job())
        self.assertEqual([RUNNER.retake_job(*flags).job for flags in ((True,), (False, True), (False, False, True))],
                         ["J2583", "J2626", "J2630"])
        for flags in ((True, True), (True, False, True), (False, True, True), (True, True, True)):
            with self.assertRaisesRegex(RUNNER.GuardError, "one retake job a run, never both"):
                RUNNER.retake_job(*flags)

    def test_the_two_earlier_paths_still_refuse_c2(self):
        rows = {r.key: r for r in RUNNER.load_scope(ROOT)}
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RUNNER.GuardError, "J2583 permits only its three ordered rows, never c2"):
                RUNNER.validate_retakes([rows[C2]], ledger(), Path(tmp))
            with self.assertRaisesRegex(RUNNER.GuardError, "J2626 permits only its two ordered rows, never the apple row or c2"):
                RUNNER.validate_retakes([rows[C2]], ledger(), Path(tmp), "J2626")
        self.assertEqual((RUNNER.RETAKES["J2583"].parent_keep, RUNNER.RETAKES["J2626"].parent_keep), (None, None))
        self.assertEqual(RUNNER.RETAKES["J2630"].parent_keep, (C1, 3))

    def test_submit_without_the_arming_switch_is_refused_with_the_flag_too(self):
        with patch.dict(os.environ, {RUNNER.SUBMIT_ENV: "0"}):
            with self.assertRaises(SystemExit) as stop:
                RUNNER.main(["submit", "--retakes-j2630", "--media", "/unused", "--other-reservations", "0"])
        self.assertIn("generation is not armed", str(stop.exception))

    def test_the_header_says_what_the_flag_does(self):
        doc = RUNNER.__doc__
        self.assertIn("--retakes-j2630", doc)
        self.assertIn("J2630 at 100", doc)
        self.assertIn("refuses until the scope file records that c1 take 3 is KEEP", doc)


if __name__ == "__main__":
    unittest.main()
