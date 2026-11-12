"""Film 009, the four shots made again after the picture review (J2034, J2582, J2583).

Chief rulings on the desk (6792271903, 6792282370, 6792304982, 6792364829, 6792980991, 6792995872): the Moon must stay
the Moon, and no apple may move upward in a film about gravity. The wording of the four rows changed, so the scope
file's pinned board hashes changed with it. These tests read files only. They never touch Flow.

"The board as it is" here means the board as it was when the takes were made (tests/hos009_then.py). Shots that
later became drawn diagrams changed the boards again, and tests/test_hos009_final_boards.py checks those.
"""
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDIT = ROOT / "02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project"
RUNNER = EDIT / "_mint_flow_v05_tranche2.py"
RECORD = ROOT / "jobs/reviews/J2583/PROMPT_CHANGE_2026-11-11.json"
# Two of the four rows changed once more for their third takes (J2626, Chief 6798928858). These tests check the
# wording as J2583 left it: for those two rows that is the later record's `old`, for the others the board itself.
# tests/test_hos009_third_takes.py checks the later change, and that it starts exactly where this one ended.
LATER = ROOT / "jobs/reviews/J2626/PROMPT_CHANGE_2026-11-11.json"
RETAKES = EDIT / "TRANCHE2_RETAKES_J2583.json"
sys.path.insert(0, str(ROOT))
from tests.hos009_then import THEN, THEN_EDIT  # noqa: E402  the boards and scope as they were when the takes were made
CLOSING = "No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."

# The Chief's wording, word for word from the desk.
MOON = ("Same shot continues from the last frame of 01_really_falling. The camera drifts slowly. The same plain pale Moon "
        "stays in the sky above the orchard for the entire shot and glides gently sideways and downward along one smooth "
        "curve. A single thin curved line draws itself beneath the Moon, following its path. The Moon never fades, never "
        "changes size or colour, and never leaves the frame. No ball, no apple, no second object, no second line, no marks "
        "or face on the Moon.")
APPLE = ("The apple that already fell lies still in the grass for the entire shot and never moves. A second green apple "
         "with a red flush drops once from a branch straight down and lands in the grass beside it. Exactly two apples in "
         "the shot at the end. Nothing moves upward at any moment, and no apple returns to the branch.")
MINUTE_C1 = ("On the left, the apple that already fell lies still on the table at the foot of the ruler for the entire shot "
             "and never moves. A second green apple with a red flush drops once from beside the top of the ruler straight "
             "down and lands on the table beside it. Exactly two apples on the left at the end. Nothing moves upward at any "
             "moment. On the right, the Moon keeps moving forward along its curved path and never reverses.")
MINUTE_C2 = ("On the left, both apples lie still on the table beside the ruler for the entire shot and never move. No new "
             "apple appears. Nothing moves upward at any moment. On the right, the Moon keeps moving forward along its "
             "curved path and never slides back or upward. There is only the one curved path; no second bright arc appears "
             "over the Earth.")
WORDING = {"01_really_falling_c1": MOON, "08_the_apple_c1": APPLE,
           "05_minute_second_c1": MINUTE_C1, "05_minute_second_c2": MINUTE_C2}
ORDER = ["01_really_falling_c1", "08_the_apple_c1", "05_minute_second_c1", "05_minute_second_c2"]
PART = {"01_really_falling_c1": 3, "08_the_apple_c1": 2, "05_minute_second_c1": 4, "05_minute_second_c2": 4}


def load_runner():
    name = "retake_wording_runner_009"
    if name in sys.modules:
        return sys.modules[name]
    sys.path.insert(0, str(RUNNER.parent))
    spec = importlib.util.spec_from_file_location(name, RUNNER)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def board(part: int) -> Path:
    return THEN_EDIT / f"parts/part-0{part}_plates_v05.json"


def prompts(part: int) -> dict:
    return {p["id"]: p["prompt"] for p in json.loads(board(part).read_text())["plates"]}


def later() -> dict:
    return json.loads(LATER.read_text())


def as_j2583_left(rid: str) -> str:
    """The row's prompt as this change left it: the later record's `old` if the row changed again, else the board."""
    changed_again = {r["id"]: r["old"] for r in later()["rows"]}
    return changed_again.get(rid) or prompts(PART[rid])[rid]


class TheWording(unittest.TestCase):
    def setUp(self):
        self.runner = load_runner()
        self.record = json.loads(RECORD.read_text())
        self.now = {rid: as_j2583_left(rid) for rid in ORDER}

    def test_each_row_carries_the_chiefs_wording_word_for_word(self):
        for rid, wording in WORDING.items():
            with self.subTest(row=rid):
                self.assertEqual(self.now[rid].count(wording), 1)

    def test_the_closing_lines_of_every_changed_row_are_still_there(self):
        for rid, prompt in self.now.items():
            with self.subTest(row=rid):
                self.assertTrue(prompt.startswith("Premium Animistry-class 3D cartoon. Same shot continues from the last frame of "))
                self.assertTrue(prompt.endswith(CLOSING))
        self.assertIn("It never touches his head.", self.now["08_the_apple_c1"])
        for rid in ("05_minute_second_c1", "05_minute_second_c2"):
            self.assertIn("Split picture: ", self.now[rid])
            self.assertIn("No digits.", self.now[rid])

    def test_only_the_motion_line_changed_on_the_three_apple_rows(self):
        rows = {r["id"]: r for r in self.record["rows"]}
        self.assertEqual(sorted(rows), sorted(ORDER))
        for rid in ("08_the_apple_c1", "05_minute_second_c1", "05_minute_second_c2"):
            row = rows[rid]
            with self.subTest(row=rid):
                self.assertEqual(row["new"], self.now[rid])
                self.assertEqual(row["motion_new"], WORDING[rid])
                self.assertEqual(row["old"].count(row["motion_old"]), 1)
                self.assertEqual(row["new"], row["old"].replace(row["motion_old"], row["motion_new"]))
        self.assertEqual(rows["01_really_falling_c1"]["new"], self.now["01_really_falling_c1"])

    def test_nothing_may_move_upward_and_the_moon_is_never_swapped_for_a_ball(self):
        for rid in ("08_the_apple_c1", "05_minute_second_c1", "05_minute_second_c2"):
            self.assertIn("Nothing moves upward at any moment", self.now[rid])
        moon = self.now["01_really_falling_c1"]
        self.assertIn("No ball, no apple, no second object", moon)
        # The house line names a ball as a subject. Take 1 put a ball in the Moon's place, so this row leaves it out.
        self.assertNotIn("The Moon, ball or path", moon)
        self.assertIn("Nothing plummets straight at the Earth.", moon)
        # In c2 nothing drops on the left, so the sentence about both dropping went with the motion line.
        self.assertIn("Both drop the same distance.", self.now["05_minute_second_c1"])
        self.assertNotIn("Both drop the same distance.", self.now["05_minute_second_c2"])

    def test_no_changed_row_names_a_real_person(self):
        for rid, prompt in self.now.items():
            for name in ("Newton", "Isaac", "Halley", "Edmond", "Hooke", "Wren", "Kepler", "Galileo", "Flamsteed"):
                self.assertNotIn(name, prompt, rid)

    def test_the_kept_explorer_row_is_as_it_was(self):
        prompt = prompts(2)["11_explorer_apple_c1"]
        self.assertIn("The Explorer picks up the fallen apple, tosses it, catches it", prompt)
        self.assertIn("11_explorer_apple_c1", self.record["left_as_it_is"])
        self.assertNotIn("11_explorer_apple_c1", [r["id"] for r in self.record["rows"]])


class ThePins(unittest.TestCase):
    def setUp(self):
        self.runner = load_runner()
        self.record = json.loads(RECORD.read_text())
        self.scope = json.loads((THEN_EDIT / "TRANCHE2_SCOPE_J2026.json").read_text())

    def test_the_tranche_still_loads_with_the_edited_boards(self):
        rows = self.runner.load_scope(THEN)
        self.assertEqual(len(rows), 20)
        by_id = {r.plate_id: r for r in rows}
        changed_again = {r["id"] for r in later()["rows"]}
        for rid, wording in WORDING.items():
            if rid not in changed_again:
                self.assertIn(wording, by_id[rid].prompt)
            self.assertIn(wording, as_j2583_left(rid))

    def test_the_record_and_the_scope_pin_each_board_as_it_is(self):
        after = later()["boards"]
        for part in (2, 3, 4):
            name = f"part-0{part}_plates_v05.json"
            digest = self.runner.sha256_file(board(part))
            entry = self.record["boards"][name]
            with self.subTest(board=name):
                if name in after:   # changed once more: this record pins it as it left it, the later one as it is
                    self.assertEqual(entry["board_sha256_new"], after[name]["board_sha256_old"])
                    self.assertEqual(after[name]["board_sha256_new"], digest)
                else:
                    self.assertEqual(entry["board_sha256_new"], digest)
                self.assertNotEqual(entry["board_sha256_old"], digest)
                pinned = {r["id"]: r["board_sha256"] for r in self.scope["rows"] if r["board"].endswith(name)}
                self.assertEqual(sorted(pinned), entry["scope_rows_repinned"])
                self.assertEqual(set(pinned.values()), {digest})

    def test_boards_that_did_not_change_keep_their_pins(self):
        for part in (1, 5):
            name = f"part-0{part}_plates_v05.json"
            digest = self.runner.sha256_file(board(part))
            pinned = {r["board_sha256"] for r in self.scope["rows"] if r["board"].endswith(name)}
            self.assertEqual(pinned, {digest})
            self.assertNotIn(name, self.record["boards"])

    def test_part_four_follows_on_from_the_earlier_change(self):
        # J2033's change (the Halley plates name nobody) left part 04 at the hash this change started from.
        earlier = json.loads((ROOT / "jobs/reviews/J2033/PROMPT_CHANGE_2026-11-11.json").read_text())
        self.assertEqual(earlier["board_sha256_new"], self.record["boards"]["part-04_plates_v05.json"]["board_sha256_old"])


class TheRetakeScope(unittest.TestCase):
    def setUp(self):
        self.runner = load_runner()
        self.retakes = json.loads(RETAKES.read_text())
        self.scope = json.loads((THEN_EDIT / "TRANCHE2_SCOPE_J2026.json").read_text())

    def test_four_rows_one_take_each_and_400_credits_at_most(self):
        rows = self.retakes["rows"]
        self.assertEqual([r["id"] for r in sorted(rows, key=lambda r: r["order"])], ORDER)
        self.assertEqual([r["order"] for r in rows], [1, 2, 3, 4])
        self.assertEqual({r["take"] for r in rows}, {2})
        self.assertEqual(self.retakes["takes_per_row"], 1)
        self.assertEqual(self.retakes["max_credits_per_take"], self.runner.MAX_CREDITS_PER_TAKE)
        self.assertEqual(self.retakes["max_total_credits"], len(rows) * self.retakes["max_credits_per_take"])
        self.assertEqual(self.retakes["max_total_credits"], 400)
        self.assertEqual(self.retakes["cash_gbp"], 0)

    def test_every_row_is_one_of_the_twenty_and_pins_its_board(self):
        scope = {(int(r["part"]), r["id"]): r for r in self.scope["rows"]}
        after = later()["boards"]
        for row in self.retakes["rows"]:
            with self.subTest(row=row["id"]):
                pinned = scope[(row["part"], row["id"])]
                name = Path(row["board"]).name
                digest = self.runner.sha256_file(THEN / row["board"])
                self.assertEqual(row["board"], pinned["board"])
                self.assertEqual(pinned["board_sha256"], digest)             # the tranche scope pins the board as it is
                if name in after:
                    # The board changed once more for the third takes (J2626). This file is left pinning the board
                    # its second take was made from (Chief 6799192687), so the old flag refuses on the hash alone.
                    self.assertEqual(row["board_sha256"], after[name]["board_sha256_old"])
                    self.assertNotEqual(row["board_sha256"], digest)
                else:
                    self.assertEqual(row["board_sha256"], digest)
                self.assertLessEqual(row["take"], self.runner.MAX_TAKES_PER_ROW)

    def test_the_last_shot_waits_for_the_one_it_continues(self):
        last = self.retakes["rows"][-1]
        self.assertEqual(last["id"], "05_minute_second_c2")
        self.assertIn("05_minute_second_c1 take 2 is KEEP", last["only_after"])
        self.assertIn("TAKE 2", last["start_frame"])
        self.assertEqual([r["id"] for r in self.retakes["rows"] if r.get("only_after")], ["05_minute_second_c2"])

    def test_the_kept_rows_are_not_in_it(self):
        self.assertNotIn("11_explorer_apple_c1", [r["id"] for r in self.retakes["rows"]])
        self.assertIn("11_explorer_apple_c1", self.retakes["kept_not_remade"])
        self.assertIn("No second take", self.retakes["no_second_take"])


if __name__ == "__main__":
    unittest.main()
