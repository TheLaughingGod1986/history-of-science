"""Film 009, the two third takes (J2626 builds the path, J2628 makes them, J2629 checks them).

Chief rulings on the desk (6798928858, 6798955014, 6799165375, 6799192687, 6799192880): of the three second takes, the
apple shot is kept on a trim, and the falling Moon and the minute-and-second shot each get one third take with a new
motion line. The runner gets a second retake path, `--retakes-j2626`, with its own identity J2626 and 200 credits. The
old path, `--retakes-j2583`, and its scope file are left exactly as they were. These tests read files and use fakes.
They never arm Flow and never submit a take.
"""
import copy
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
RECORD = ROOT / "jobs/reviews/J2626/PROMPT_CHANGE_2026-11-11.json"
EARLIER = ROOT / "jobs/reviews/J2583/PROMPT_CHANGE_2026-11-11.json"
SCOPE_FILE = EDIT / "TRANCHE2_RETAKES_J2626.json"
OLD_SCOPE_FILE = EDIT / "TRANCHE2_RETAKES_J2583.json"
CLOSING = "No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."

# The Chief's wording, word for word from the desk (6798928858 points 1 and 3).
MOON_LINE = ("The single golden curve stays exactly as it is in the first frame: its upper-right end keeps pointing up and "
             "to the right and never bends back, loops, wraps around or crosses the Moon. The Moon glides smoothly forward "
             "along that path at the same size, brightness and colour. No second line or object appears.")
RULER_LINE = ("On the left, the apple that already fell lies still on the table at the foot of the ruler for the entire shot "
              "and never moves or rolls. A second green apple with a red flush drops once from beside the top of the ruler "
              "straight down and lands on the table beside it. Exactly two apples on the left at the end, and no other apple "
              "appears. Nothing moves upward at any moment. On the right there is no apple at all: only the Moon, which keeps "
              "moving forward along its single curved path and never reverses. No second bright arc appears over the Earth.")
# The sentences the Chief had taken out (desk 6799192880): the one that told the model to draw a line, and the house
# line that names a ball as a subject, from c1 and from c2. Nothing else may go.
HOUSE_LINE = "The Moon, ball or path slides sideways and down along a smooth curve."
DROPPED = {"01_really_falling_c1": ["A single thin curved line draws itself beneath the Moon, following its path."],
           "05_minute_second_c1": [HOUSE_LINE], "05_minute_second_c2": [HOUSE_LINE]}
MOON, RULER = (3, "01_really_falling_c1"), (4, "05_minute_second_c1")
APPLE, C2 = (2, "08_the_apple_c1"), (4, "05_minute_second_c2")


def load_runner():
    name = "third_takes_runner_009"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


RUNNER = load_runner()


def prompts(part: int) -> dict:
    board = EDIT / f"parts/part-0{part}_plates_v05.json"
    return {p["id"]: p["prompt"] for p in json.loads(board.read_text())["plates"]}


def takes(*numbers, keys=(MOON, RULER), **last):
    """Ledger lines: each row has these takes; `last` overrides fields of each row's highest take."""
    entries = []
    for part, plate in keys:
        for n in numbers:
            entry = {"part": part, "plate_id": plate, "take": n, "status": "PENDING_REVIEW"}
            if n == numbers[-1]:
                entry.update(last)
            entries.append(entry)
    return entries


def boards_as_take_two_was_made_from():
    """Each board J2583's file pins reads as the hash pinned there: the boards as they were before this change."""
    scope = json.loads(OLD_SCOPE_FILE.read_text())
    pins = {(ROOT / row["board"]).resolve(): row["board_sha256"] for row in scope["rows"]}
    real = RUNNER.sha256_file
    return patch.object(RUNNER, "sha256_file", side_effect=lambda path: pins.get(Path(path).resolve()) or real(path))


class TheWording(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(RECORD.read_text())
        self.rows = {r["id"]: r for r in self.record["rows"]}
        self.now = {"01_really_falling_c1": prompts(3)["01_really_falling_c1"],
                    "05_minute_second_c1": prompts(4)["05_minute_second_c1"],
                    "05_minute_second_c2": prompts(4)["05_minute_second_c2"]}

    def test_each_row_carries_the_chiefs_line_once_word_for_word(self):
        self.assertEqual(self.now["01_really_falling_c1"].count(MOON_LINE), 1)
        self.assertEqual(self.now["05_minute_second_c1"].count(RULER_LINE), 1)
        self.assertEqual(self.rows["01_really_falling_c1"]["motion_added"], MOON_LINE)
        self.assertEqual(self.rows["05_minute_second_c1"]["motion_new"], RULER_LINE)

    def test_the_record_is_the_board_and_the_change_is_only_what_was_ruled(self):
        self.assertEqual(sorted(self.rows), sorted(self.now))
        for rid, row in self.rows.items():
            self.assertEqual(row["new"], self.now[rid], rid)
            self.assertEqual(row["dropped"], DROPPED[rid], rid)
            for sentence in row["dropped"]:
                self.assertEqual(row["old"].count(sentence + " "), 1, rid)
                self.assertNotIn(sentence, row["new"], rid)
        moon, ruler, c2 = (self.rows[rid] for rid in ("01_really_falling_c1", "05_minute_second_c1", "05_minute_second_c2"))
        anchor = "no marks or face on the Moon."
        self.assertEqual(moon["old"].count(anchor), 1)
        expected = moon["old"].replace(anchor, anchor + " " + MOON_LINE)      # added after the motion wording
        self.assertEqual(moon["new"], expected.replace(DROPPED["01_really_falling_c1"][0] + " ", ""))
        self.assertEqual(ruler["old"].count(ruler["motion_old"]), 1)
        expected = ruler["old"].replace(ruler["motion_old"], RULER_LINE)       # replaces the old motion line
        self.assertEqual(ruler["new"], expected.replace(HOUSE_LINE + " ", ""))
        self.assertEqual(c2["new"], c2["old"].replace(HOUSE_LINE + " ", ""))   # c2: that one line and nothing else

    def test_the_rows_usual_closing_lines_stay_after_it(self):
        for rid, prompt in self.now.items():
            with self.subTest(row=rid):
                self.assertTrue(prompt.startswith("Premium Animistry-class 3D cartoon. Same shot continues from the last frame of "))
                self.assertTrue(prompt.endswith("Nothing plummets straight at the Earth. " + CLOSING))
                self.assertNotIn("ball or path", prompt)                     # no row names a ball as a subject now
        moon = self.now["01_really_falling_c1"]
        self.assertLess(moon.index(MOON_LINE), moon.index("Nothing plummets straight at the Earth."))
        self.assertIn("No ball, no apple, no second object, no second line, no marks or face on the Moon.", moon)
        self.assertNotIn("draws itself", moon)                               # the curve is in the start frame already
        self.assertIn("The same plain pale Moon stays in the sky above the orchard for the entire shot", moon)
        ruler = self.now["05_minute_second_c1"]
        for kept in ("Split picture: ", "Both drop the same distance.", "No digits."):
            self.assertIn(kept, ruler)
        self.assertLess(ruler.index(RULER_LINE), ruler.index("Both drop the same distance."))
        c2 = self.now["05_minute_second_c2"]
        for kept in ("Split picture: ", "No digits.", "There is only the one curved path; no second bright arc appears over the Earth."):
            self.assertIn(kept, c2)

    def test_nothing_may_move_upward_and_no_real_person_is_named(self):
        self.assertIn("Nothing moves upward at any moment", self.now["05_minute_second_c1"])
        self.assertIn("never bends back, loops, wraps around or crosses the Moon", self.now["01_really_falling_c1"])
        for rid, prompt in self.now.items():
            for name in ("Newton", "Isaac", "Halley", "Edmond", "Hooke", "Wren", "Kepler", "Galileo", "Flamsteed"):
                self.assertNotIn(name, prompt, rid)

    def test_the_apple_row_is_as_j2583_left_it_and_c2_lost_only_the_house_line(self):
        earlier = {r["id"]: r["new"] for r in json.loads(EARLIER.read_text())["rows"]}
        self.assertEqual(prompts(2)["08_the_apple_c1"], earlier["08_the_apple_c1"])
        self.assertEqual(prompts(4)["05_minute_second_c2"], earlier["05_minute_second_c2"].replace(HOUSE_LINE + " ", ""))
        self.assertNotIn("05_minute_second_c2", [r["id"] for r in json.loads(SCOPE_FILE.read_text())["rows"]])

    def test_this_change_starts_where_the_last_one_ended(self):
        earlier = json.loads(EARLIER.read_text())
        was = {r["id"]: r["new"] for r in earlier["rows"]}
        for rid, row in self.rows.items():
            self.assertEqual(row["old"], was[rid], rid)
        for name, entry in self.record["boards"].items():
            with self.subTest(board=name):
                self.assertEqual(entry["board_sha256_old"], earlier["boards"][name]["board_sha256_new"])
                # the hashes the Chief named as the ones take 2 was made from (desk 6799192687 point 1)
                self.assertEqual(entry["board_sha256_old"], self.record["take_2_was_made_from"][name])
                self.assertEqual(entry["board_sha256_new"], RUNNER.sha256_file(EDIT / "parts" / name))
                self.assertNotEqual(entry["board_sha256_old"], entry["board_sha256_new"])
        self.assertEqual(sorted(self.record["boards"]), ["part-03_plates_v05.json", "part-04_plates_v05.json"])


class ThePins(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(RECORD.read_text())
        self.tranche = json.loads((EDIT / "TRANCHE2_SCOPE_J2026.json").read_text())

    def test_the_tranche_still_loads_with_the_edited_boards(self):
        rows = {r.plate_id: r for r in RUNNER.load_scope(ROOT)}
        self.assertEqual(len(rows), 20)
        self.assertIn(MOON_LINE, rows["01_really_falling_c1"].prompt)
        self.assertIn(RULER_LINE, rows["05_minute_second_c1"].prompt)

    def test_the_tranche_and_the_new_scope_pin_each_board_as_it_is_and_the_old_file_as_it_was(self):
        old = json.loads(OLD_SCOPE_FILE.read_text())
        new = json.loads(SCOPE_FILE.read_text())
        for name, entry in self.record["boards"].items():
            digest = RUNNER.sha256_file(EDIT / "parts" / name)
            with self.subTest(board=name):
                pinned = {r["id"]: r["board_sha256"] for r in self.tranche["rows"] if r["board"].endswith(name)}
                self.assertEqual(sorted(pinned), entry["scope_rows_repinned"])
                self.assertEqual(set(pinned.values()), {digest})
                self.assertEqual({r["board_sha256"] for r in new["rows"] if r["board"].endswith(name)}, {digest})
                # J2583's file is left as it is: it still pins the board its second takes were made from
                self.assertEqual({r["board_sha256"] for r in old["rows"] if r["board"].endswith(name)},
                                 {entry["board_sha256_old"]})

    def test_boards_this_change_left_alone_keep_their_pins(self):
        for part in (1, 2, 5):
            name = f"part-0{part}_plates_v05.json"
            digest = RUNNER.sha256_file(EDIT / "parts" / name)
            self.assertEqual({r["board_sha256"] for r in self.tranche["rows"] if r["board"].endswith(name)}, {digest})
            self.assertNotIn(name, self.record["boards"])


class TheScope(unittest.TestCase):
    def setUp(self):
        self.scope = json.loads(SCOPE_FILE.read_text())

    def test_two_rows_in_order_one_third_take_each(self):
        rows = self.scope["rows"]
        self.assertEqual([(r["part"], r["id"]) for r in rows], [MOON, RULER])
        self.assertEqual(tuple((r["part"], r["id"]) for r in rows), RUNNER.J2626_KEYS)
        self.assertEqual([r["order"] for r in rows], [1, 2])
        self.assertEqual({r["take"] for r in rows}, {3})
        self.assertEqual(RUNNER.MAX_TAKES_PER_ROW, 3)                        # so there is no fourth
        self.assertEqual(self.scope["takes_per_row"], 1)
        self.assertEqual((self.scope["job"], self.scope["takes_made_by_job"]), ("J2626", "J2628"))

    def test_the_money_adds_up_to_the_ceiling_and_no_cash(self):
        s = self.scope
        self.assertEqual(s["max_credits_per_take"], RUNNER.MAX_CREDITS_PER_TAKE)
        self.assertEqual(s["reservation_cap"], len(s["rows"]) * s["max_credits_per_take"])
        self.assertEqual((s["spent_before_by_j2583"], s["reservation_cap"], s["held_back_for_c2"]), (300, 200, 100))
        self.assertEqual(s["spent_before_by_j2583"] + s["reservation_cap"] + s["held_back_for_c2"], s["max_total_credits"])
        self.assertEqual(s["max_total_credits"], 600)
        self.assertEqual(s["cash_gbp"], 0)
        self.assertEqual((RUNNER.J2626_RESERVE_CAP, RUNNER.J2626_CEILING, RUNNER.J2583_RESERVE_CAP), (200, 600, 300))

    def test_the_apple_row_and_c2_are_named_as_not_in_it(self):
        ids = [r["id"] for r in self.scope["rows"]]
        for rid in ("08_the_apple_c1", "05_minute_second_c2"):
            self.assertNotIn(rid, ids)
            self.assertIn(rid, self.scope["not_in_this_job"])
        self.assertIn("f107", self.scope["not_in_this_job"]["08_the_apple_c1"])
        self.assertIn("parked", self.scope["no_fourth_take"])
        self.assertIn("6798928858", " ".join(self.scope["rulings"]))


class TheRunnerPath(unittest.TestCase):
    def setUp(self):
        self.rows = RUNNER.load_scope(ROOT)

    def batch(self, entries, media):
        return RUNNER.retake_batch(ROOT, self.rows, entries, Path(media), "J2626")

    def test_only_the_two_rows_in_order(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(RUNNER, "verified_output", return_value=True):
            batch = self.batch(takes(1, 2), tmp)
        self.assertEqual(tuple(r.key for r in batch), (MOON, RULER))
        self.assertTrue(all(r.parent is not None for r in batch))            # each continues from its parent's last frame

    def test_a_row_must_hold_takes_one_and_two_only_with_take_two_finished(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(RUNNER, "verified_output", return_value=True):
                for entries in (takes(1), takes(2), [], takes(1, 2, keys=(MOON,))):
                    with self.assertRaisesRegex(RUNNER.GuardError, "takes 1 and 2 only"):
                        self.batch(entries, tmp)
                # any line at all for take 3 means it was already tried: made, refused, failed or half-submitted
                for status in ("SUBMITTING", "FAILED", "FAILED_POLICY", "PENDING_REVIEW"):
                    with self.assertRaisesRegex(RUNNER.GuardError, "takes 1 and 2 only"):
                        self.batch(takes(1, 2) + [dict(takes(1, 2)[1], take=3, status=status)], tmp)
            with patch.object(RUNNER, "verified_output", return_value=False):   # take 2 is not a finished, archived output
                with self.assertRaisesRegex(RUNNER.GuardError, "take 2 verified"):
                    self.batch(takes(1, 2), tmp)

    def test_it_is_take_two_that_must_be_verified(self):
        seen = []
        with tempfile.TemporaryDirectory() as tmp, \
                patch.object(RUNNER, "verified_output", side_effect=lambda e: seen.append(e["take"]) or True):
            self.batch(takes(1, 2), tmp)
        self.assertEqual(seen, [2, 2])

    def test_a_take_three_file_already_there_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(RUNNER, "verified_output", return_value=True):
            dest = RUNNER.versioned_output(Path(tmp), *RULER, 3)
            dest.parent.mkdir(parents=True)
            dest.write_bytes(b"preserve")
            with self.assertRaisesRegex(RUNNER.GuardError, "already has 3 versioned files|without overwriting"):
                self.batch(takes(1, 2), tmp)
            self.assertEqual(dest.read_bytes(), b"preserve")

    def test_the_apple_row_c2_and_every_other_row_are_refused(self):
        by_key = {r.key: r for r in self.rows}
        moon, ruler = by_key[MOON], by_key[RULER]
        wrong = ([moon], [ruler, moon], [moon, ruler, by_key[APPLE]], [moon, by_key[C2]], [by_key[APPLE], ruler],
                 [moon, ruler, by_key[C2]], self.rows[:2], self.rows, [])
        with tempfile.TemporaryDirectory() as tmp:
            for batch in wrong:
                with self.assertRaisesRegex(RUNNER.GuardError, "only its two ordered rows"):
                    RUNNER.validate_retakes(batch, takes(1, 2), Path(tmp), "J2626")

    def test_a_changed_scope_file_is_refused(self):
        original = json.loads(SCOPE_FILE.read_text())
        changes = [("max_total_credits", 700), ("max_total_credits", 400), ("takes_per_row", 2), ("max_credits_per_take", 200),
                   ("reservation_cap", 300), ("spent_before_by_j2583", 200), ("held_back_for_c2", 0), ("job", "J2583")]
        for field, value in changes:
            changed = copy.deepcopy(original)
            changed[field] = value
            with self.subTest(field=field, value=value), patch.object(RUNNER.json, "loads", return_value=changed):
                with self.assertRaisesRegex(RUNNER.GuardError, "differs from the approved two third takes"):
                    self.batch(takes(1, 2), "/unused")

        def rows(edit):
            changed = copy.deepcopy(original)
            edit(changed["rows"])
            return changed
        for changed in (rows(lambda r: r.reverse()), rows(lambda r: r.pop()), rows(lambda r: r[0].update(take=2)),
                        rows(lambda r: r[1].update(take=4)), rows(lambda r: r.append(dict(r[1], id="05_minute_second_c2"))),
                        rows(lambda r: r[0].update(part=2, id="08_the_apple_c1"))):
            with patch.object(RUNNER.json, "loads", return_value=changed):
                with self.assertRaisesRegex(RUNNER.GuardError, "differs from the approved two third takes"):
                    self.batch(takes(1, 2), "/unused")
        with patch.object(RUNNER.json, "loads", return_value=rows(lambda r: r[0].update(board_sha256="0" * 64))):
            with self.assertRaisesRegex(RUNNER.GuardError, "J2626 retake board hash mismatch"):
                self.batch(takes(1, 2), "/unused")


class TheOldPathIsAsItWas(unittest.TestCase):
    """Chief 6798955014 point 3: `--retakes-j2583` is not loosened, so the new takes cannot be reached through it."""

    def setUp(self):
        self.rows = RUNNER.load_scope(ROOT)

    def test_the_old_flag_still_refuses_a_row_on_take_two(self):
        # Today's real state: all three J2583 rows hold takes 1 and 2. With the boards as they were, the take-1-only
        # guard refuses, exactly as before this change.
        today = takes(1, 2, keys=RUNNER.J2583_KEYS)
        with tempfile.TemporaryDirectory() as tmp, patch.object(RUNNER, "verified_output", return_value=True), \
                boards_as_take_two_was_made_from():
            with self.assertRaisesRegex(RUNNER.GuardError, "J2583 requires verified take 1 only"):
                RUNNER.retake_batch(ROOT, self.rows, today, Path(tmp))
            with self.assertRaisesRegex(RUNNER.GuardError, "J2583 requires verified take 1 only"):
                RUNNER.retake_batch(ROOT, self.rows, today, Path(tmp), "J2583")

    def test_the_old_flag_refuses_on_the_boards_as_they_are_now(self):
        # And on the real boards it refuses a step earlier: its file pins the boards as they were, even for a row on take 1.
        with tempfile.TemporaryDirectory() as tmp, patch.object(RUNNER, "verified_output", return_value=True):
            for entries in (takes(1, 2, keys=RUNNER.J2583_KEYS), takes(1, keys=RUNNER.J2583_KEYS)):
                with self.assertRaisesRegex(RUNNER.GuardError, "J2583 retake board hash mismatch"):
                    RUNNER.retake_batch(ROOT, self.rows, entries, Path(tmp))

    def test_the_old_scope_file_is_byte_for_byte_what_it_was(self):
        self.assertEqual(RUNNER.sha256_file(OLD_SCOPE_FILE), "414b67533ade151402d51c159d43075996c3f930109f47776be136560eb4bf7a")

    def test_the_old_path_is_the_default_and_keeps_its_rows_its_take_and_its_money(self):
        old = RUNNER.RETAKES["J2583"]
        self.assertEqual((old.keys, old.take, old.reserve, old.ceiling), (RUNNER.J2583_KEYS, 2, 300, 400))
        self.assertEqual(old.file_keys, (*RUNNER.J2583_KEYS, C2))
        self.assertEqual(RUNNER.retake_credit_cap(ROOT), 400)
        with tempfile.TemporaryDirectory() as tmp, patch.object(RUNNER, "verified_output", return_value=True), \
                boards_as_take_two_was_made_from():
            batch = RUNNER.retake_batch(ROOT, self.rows, takes(1, keys=RUNNER.J2583_KEYS), Path(tmp))
            self.assertEqual(tuple(r.key for r in batch), RUNNER.J2583_KEYS)
            with self.assertRaisesRegex(RUNNER.GuardError, "J2583 permits only its three ordered rows, never c2"):
                RUNNER.validate_retakes(batch[:2], takes(1, keys=RUNNER.J2583_KEYS), Path(tmp))

    def test_the_two_flags_are_never_used_together(self):
        with self.assertRaisesRegex(RUNNER.GuardError, "never both"):
            RUNNER.retake_job(True, True)
        self.assertIsNone(RUNNER.retake_job())
        self.assertEqual(RUNNER.retake_job(True).job, "J2583")
        self.assertEqual(RUNNER.retake_job(False, True).job, "J2626")
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {RUNNER.SUBMIT_ENV: "1"}):
            root = Path(tmp)
            with self.assertRaisesRegex(RUNNER.GuardError, "never both"):
                RUNNER.cmd_submit(ROOT, other=0, media=root, ledger_path=root / "l.jsonl", lock_path=root / "w.lock",
                                  pid_path=root / "r.pid", done_path=root / "r.done", archive_dir=root,
                                  test_archive=True, retakes_j2583=True, retakes_j2626=True)
            self.assertFalse((root / "l.jsonl").exists())


class TheReservation(unittest.TestCase):
    """Its own identity at 200, written before any local intent, released after the second row."""

    def rows(self):
        by_key = {row.key: row for row in RUNNER.load_scope(ROOT)}
        return [by_key[MOON], by_key[RULER]]

    FRAME = b"frame-bytes"

    def seed(self, ledger: Path, frame: bytes = FRAME):
        import hashlib
        for part, plate in (MOON, RULER):
            for take in (1, 2):
                RUNNER.append_ledger(ledger, {
                    "part": part, "plate_id": plate, "take": take, "status": "PENDING_REVIEW",
                    "keep": False, "generated": True, "credits_used": 100, "credits_reserved": 100,
                    "input": {"file": f"/then/{plate}.png", "sha256": hashlib.sha256(frame).hexdigest()}})

    def test_the_ceiling_is_the_approved_600(self):
        self.assertEqual(RUNNER.retake_credit_cap(ROOT, "J2626"), 600)
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            dest = repo / RUNNER.EDIT_REL
            dest.mkdir(parents=True)
            scope = json.loads(SCOPE_FILE.read_text())
            for ceiling, message in ((6000, "approved 600"), (500, "approved 600"), (100, "exceeds the approved ceiling")):
                scope["max_total_credits"] = ceiling
                (dest / "TRANCHE2_RETAKES_J2626.json").write_text(json.dumps(scope))
                with self.assertRaisesRegex(RUNNER.GuardError, message):
                    RUNNER.retake_credit_cap(repo, "J2626")
            (dest / "TRANCHE2_RETAKES_J2626.json").write_text(json.dumps(dict(scope, job="J2583", max_total_credits=600)))
            with self.assertRaisesRegex(RUNNER.GuardError, "missing or invalid"):
                RUNNER.retake_credit_cap(repo, "J2626")
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RUNNER.GuardError, "J2626 retake cap file is missing or invalid"):
                RUNNER.retake_credit_cap(Path(tmp), "J2626")

    def test_cmd_submit_reserves_j2626_at_200_and_only_for_its_flag(self):
        row = self.rows()[0]
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {RUNNER.SUBMIT_ENV: "1"}):
            root = Path(tmp)
            (root / "archive").mkdir()
            common = dict(other=0, media=root / "media", ledger_path=root / "ledger.jsonl", lock_path=root / "writer.lock",
                          pid_path=root / "runner.pid", done_path=root / "runner.done", archive_dir=root / "archive",
                          test_archive=True)
            with patch.object(RUNNER, "retake_batch", return_value=[row]) as chosen, \
                    patch.object(RUNNER, "execute_shared_batch", return_value=[]) as run:
                RUNNER.cmd_submit(ROOT, retakes_j2626=True, **common)
            self.assertEqual(chosen.call_args.args[-1], "J2626")
            self.assertEqual((run.call_args.kwargs["reservation"], run.call_args.kwargs["reservation_cap"]), ("J2626", 200))
            self.assertTrue(run.call_args.kwargs["retakes_j2626"])
            self.assertFalse(run.call_args.kwargs["retakes_j2583"])
            with patch.object(RUNNER, "execute_shared_batch", return_value=[]) as run:
                RUNNER.cmd_submit(ROOT, **common)
            self.assertEqual((run.call_args.kwargs["reservation"], run.call_args.kwargs["reservation_cap"]), ("J2033", 6000))
            self.assertNotIn("retakes_j2626", run.call_args.kwargs)

    def test_the_batch_refuses_another_identity_or_another_amount(self):
        rows = self.rows()
        for reservation, cap in (("J2583", 300), ("J2626", 300), ("J2033", 6000), ("J2626", 100)):
            with tempfile.TemporaryDirectory() as tmp, self.subTest(reservation=reservation, cap=cap):
                root = Path(tmp)
                (root / "archive").mkdir()
                with self.assertRaisesRegex(RUNNER.GuardError, "J2626 retakes reserve identity J2626 at 200 credits"):
                    RUNNER.execute_shared_batch(
                        rows, media=root, ledger_path=root / "ledger.jsonl", archive_dir=root / "archive",
                        accounting_state=root / "shared", reservation=reservation, reservation_cap=cap,
                        submitter=lambda *a, **k: None, still_maker=None, test_archive=True, inventory_rows=rows,
                        retakes_j2626=True, in_scope_keys={r.key for r in rows})

    def test_two_third_takes_reserve_200_before_local_intent_and_release_after_the_second(self):
        selected = self.rows()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive, shared, ledger, media = root / "archive", root / "shared", root / "ledger.jsonl", root / "media"
            archive.mkdir()
            media.mkdir()
            self.seed(ledger)
            # The Mini's real state: the tranche identity closed, and J2583 spent and released.
            with RUNNER.SharedFlowAccounting(shared) as account:
                account.reserve("J2033", "HOS:009", 6000, live=20000)
                account.release("J2033")
                account.reserve("J2583", "HOS:009", 300, live=20000)
                for n in range(3):
                    account.intent(f"second-{n}", "J2583", 100, live=20000)
                    account.resolve(f"second-{n}", submitted=True, evidence={"n": n})
                account.release("J2583")
            before = (shared / "account.jsonl").read_bytes()
            seen = []

            def fake_frame(row, media_path, **kwargs):
                dest = media_path / f"{row.plate_id}.png"
                dest.write_bytes(self.FRAME)
                return dest

            def fake_submitter(row, dest, frame, *, accounting, reservation, reservation_cap,
                               charge, evidence_path, after_reserve, other=0):
                seen.append((reservation, reservation_cap, charge))
                self.assertNotIn(charge, ledger.read_text())
                accounting.reserve(reservation, "HOS:009", reservation_cap, live=11290, floor=3000)
                self.assertNotIn(charge, ledger.read_text())             # nothing local until the reserve is in
                after_reserve()
                self.assertIn(charge, ledger.read_text())
                accounting.intent(charge, reservation, 100, live=11290)
                accounting.resolve(charge, submitted=True, evidence={"charge": charge})
                dest.write_bytes(b"fake-video")
                return {"charge": charge}

            with patch.object(RUNNER, "verified_output", return_value=True), \
                    patch.object(RUNNER, "prepare_start_frame", side_effect=fake_frame), \
                    patch.object(RUNNER, "strip_audio"), \
                    patch.object(RUNNER, "technical_report",
                                 side_effect=lambda path, **kw: {"ok": True, "sha256": RUNNER.sha256_file(path)}):
                written = RUNNER.execute_shared_batch(
                    selected, media=media, ledger_path=ledger, archive_dir=archive, accounting_state=shared,
                    reservation="J2626", reservation_cap=200, submitter=fake_submitter, still_maker=None,
                    test_archive=True, inventory_rows=selected, retakes_j2626=True,
                    in_scope_keys={row.key for row in selected})
            self.assertEqual(seen, [("J2626", 200, "HOS:009:P03:01_really_falling_c1:t3"),
                                    ("J2626", 200, "HOS:009:P04:05_minute_second_c1:t3")])
            self.assertEqual([(item["plate_id"], item["take"]) for item in written],
                             [("01_really_falling_c1", 3), ("05_minute_second_c1", 3)])
            self.assertEqual({Path(item["file"]).name for item in written},
                             {RUNNER.versioned_output(media, *key, 3).name for key in (MOON, RULER)})
            after = (shared / "account.jsonl").read_bytes()
            self.assertTrue(after.startswith(before))                     # the earlier identities' lines are untouched
            suffix = after.split(before, 1)[1]
            self.assertNotIn(b'"id": "J2033"', suffix)
            self.assertNotIn(b'"id": "J2583"', suffix)
            with RUNNER.SharedFlowAccounting(shared) as account:
                snap = account.snapshot()
                self.assertEqual(snap["reservations"]["J2626"]["cap"], 200)
                for identity in ("J2033", "J2583", "J2626"):
                    self.assertFalse(snap["reservations"][identity]["active"], identity)
                with self.assertRaisesRegex(RUNNER.GuardError, "inactive reservation"):
                    account.intent("a-fourth-take", "J2626", 100, live=11290)
            # run again: both rows now hold take 3, so the same flag refuses
            with patch.object(RUNNER, "verified_output", return_value=True):
                with self.assertRaisesRegex(RUNNER.GuardError, "takes 1 and 2 only"):
                    RUNNER.retake_batch(ROOT, RUNNER.load_scope(ROOT), RUNNER.read_ledger(ledger), media, "J2626")

    def test_a_third_take_starts_from_the_frame_its_second_take_started_from(self):
        selected = self.rows()
        for seeded, why in ((b"another-frame", "a different frame"), (None, "no frame on record")):
            with tempfile.TemporaryDirectory() as tmp, self.subTest(why=why):
                root = Path(tmp)
                archive, shared, ledger, media = root / "archive", root / "shared", root / "ledger.jsonl", root / "media"
                archive.mkdir()
                media.mkdir()
                if seeded is None:
                    for entry in takes(1, 2, keep=False, generated=True):
                        RUNNER.append_ledger(ledger, entry)
                else:
                    self.seed(ledger, seeded)
                called = []

                def fake_frame(row, media_path, **kwargs):
                    dest = media_path / f"{row.plate_id}.png"
                    dest.write_bytes(self.FRAME)
                    return dest

                with patch.object(RUNNER, "verified_output", return_value=True), \
                        patch.object(RUNNER, "prepare_start_frame", side_effect=fake_frame):
                    with self.assertRaisesRegex(RUNNER.GuardError, "start frame is not the one take 2 was made from; no Create"):
                        RUNNER.execute_shared_batch(
                            selected, media=media, ledger_path=ledger, archive_dir=archive, accounting_state=shared,
                            reservation="J2626", reservation_cap=200, submitter=lambda *a, **k: called.append(a),
                            still_maker=None, test_archive=True, inventory_rows=selected, retakes_j2626=True,
                            in_scope_keys={row.key for row in selected})
                self.assertEqual(called, [])                                 # the submitter was never reached
                self.assertNotIn("SUBMITTING", ledger.read_text())
                self.assertFalse((shared / "account.jsonl").exists() and b"J2626" in (shared / "account.jsonl").read_bytes())

    def test_a_third_charge_under_the_200_is_refused_by_the_account(self):
        with tempfile.TemporaryDirectory() as tmp:
            with RUNNER.SharedFlowAccounting(Path(tmp)) as account:
                account.reserve("J2626", "HOS:009", 200, live=11290)
                for n in range(2):
                    account.intent(f"third-{n}", "J2626", 100, live=11290)
                    account.resolve(f"third-{n}", submitted=True, evidence={"n": n})
                with self.assertRaisesRegex(RUNNER.GuardError, "charge exceeds reservation cap"):
                    account.intent("c2", "J2626", 100, live=11290)

    def test_the_second_resolved_row_releases_even_when_a_take_was_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            with RUNNER.SharedFlowAccounting(Path(tmp)) as account:
                account.reserve("J2626", "HOS:009", 200, live=11290)
                resolved = RUNNER.note_retake_resolution(account, "J2626", {"status": "POLICY_REFUSED", "amount": 0}, 0)
                self.assertTrue(account.snapshot()["reservations"]["J2626"]["active"])
                resolved = RUNNER.note_retake_resolution(account, "J2626", {"status": "PENDING", "amount": 100}, resolved)
                self.assertEqual(resolved, 1)                               # an unresolved Create does not count
                resolved = RUNNER.note_retake_resolution(account, "J2626", {"status": "CHARGED", "amount": 100}, resolved)
                self.assertEqual(resolved, 2)
                self.assertFalse(account.snapshot()["reservations"]["J2626"]["active"])
                self.assertEqual(RUNNER.note_retake_resolution(account, "J2033", {"status": "CHARGED"}, 0), 0)


class TheCommandLine(unittest.TestCase):
    def test_the_flag_reaches_the_detached_submit_and_the_default_omits_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            common = dict(repo=ROOT, media=root, archive=root, other=0, ledger=root / "ledger.jsonl",
                          lock=root / "writer.lock", pid=root / "runner.pid")
            plain = RUNNER.detached_command(SCRIPT, root / "run.log", root / "run.done", **common)
            self.assertNotIn("--retakes-j2626", plain[-1])
            old = RUNNER.detached_command(SCRIPT, root / "old.log", root / "old.done", retakes_j2583=True, **common)
            self.assertNotIn("--retakes-j2626", old[-1])
            command = RUNNER.detached_command(SCRIPT, root / "third.log", root / "third.done", retakes_j2626=True, **common)
            child = shlex.split(command[-1])
            self.assertIn("--retakes-j2626", child)
            self.assertNotIn("--retakes-j2583", child)
            self.assertEqual(child[2], "launch-worker")
            with self.assertRaisesRegex(RUNNER.GuardError, "never both"):
                RUNNER.detached_command(SCRIPT, root / "both.log", root / "both.done", retakes_j2583=True,
                                        retakes_j2626=True, **common)
            self.assertFalse((root / "third.log").exists())                 # print-only: nothing is started

    def test_submit_without_the_arming_switch_is_refused_with_the_flag_too(self):
        with patch.dict(os.environ, {RUNNER.SUBMIT_ENV: "0"}):
            with self.assertRaises(SystemExit) as stop:
                RUNNER.main(["submit", "--retakes-j2626", "--media", "/unused", "--other-reservations", "0"])
        self.assertIn("generation is not armed", str(stop.exception))

    def test_the_header_says_what_the_flag_does(self):
        doc = RUNNER.__doc__
        self.assertIn("--retakes-j2626", doc)
        self.assertIn("J2626 at 200", doc)
        self.assertIn("never makes c2 and never makes a fourth take", doc)


if __name__ == "__main__":
    unittest.main()
