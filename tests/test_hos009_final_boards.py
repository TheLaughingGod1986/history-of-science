"""Film 009's picture tool and the boards as they are now (J2636).

Twenty shots were approved for the second tranche and made. The Chief has since replaced some of them with drawn
diagrams (the five-metre graphic, J2631, then the falling-Moon graphic, J2632). Each replacement changes a board, and
the tool pins its boards by hash. On 11 Nov 2026 that turned 77 tests red on main, and no check showed it.

The other 009 tests now stand where the takes were made (tests/hos009_then.py). These read the real repo:

- the scope pins every board as it is, so the tool loads;
- a shot that is now a drawn diagram is marked in the scope, and is never among the rows the tool works from;
- a scope and a board that disagree about that refuse the run;
- the two retake paths whose takes are made refuse on the real repo, and their records are untouched;
- the c2 path that was never used is gone;
- the frozen boards the other tests use are the ones the takes were made from;
- one command puts the scope back in step with a board that changed, and changes nothing else.

They read files and use fakes. They never arm Flow and never submit a take.
"""
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tests.hos009_then import BOARDS, EDIT_REL, FIXTURE, THEN, THEN_EDIT  # noqa: E402

EDIT = ROOT / EDIT_REL
SCRIPT = EDIT / "_mint_flow_v05_tranche2.py"
REPIN_SCRIPT = EDIT / "_repin_tranche2_scope.py"
SCOPE = "TRANCHE2_SCOPE_J2026.json"
DIAGRAM = {"route": "code-graphic", "tranche": 0, "generation_authorized": False, "flow_credits_try1": 0}
# The retake records are history: their takes are made. Each is exactly the file that was merged.
RECORDS = {"TRANCHE2_RETAKES_J2583.json": "414b67533ade151402d51c159d43075996c3f930109f47776be136560eb4bf7a",
           "TRANCHE2_RETAKES_J2626.json": "e7503e258ae5bfb4c908141754fe7fee90e99fdb386fb0511dd7b97e43a9d243"}
# The frozen copies: the scope and the five boards as they were at #528 (4d94db91).
FROZEN = {
    SCOPE: "70198f6bd536029f6ca64c5efc19fd853c5cd5ea307f09a9dc7dd6967504df74",
    "parts/part-01_plates_v05.json": "beb72c067b81ccfab5bf8cc574c06ce4951e8aa08930f7dc2e405c5af68f6cbc",
    "parts/part-02_plates_v05.json": "0aabf081a6adf7a6921a938bb39fa4e69a5bc64bb562e04a2da0bfc1bb34ad49",
    "parts/part-03_plates_v05.json": "36f8f8bb0ebd18006569aa2b10b1df5c01b08b53de90dcd6f706c616ca779899",
    "parts/part-04_plates_v05.json": "7eac7c34c8a44edeccb607f9eeda0e1a0855e393f4ab9e131e9e2d370c39a52d",
    "parts/part-05_plates_v05.json": "3153a646aa83cc2b97208a4267b02909a673a9fef696f4b76e4390b84f26d6b2",
}


def load_runner():
    name = "final_boards_runner_009"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


RUNNER = load_runner()


def load_repin():
    name = "repin_scope_009"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, REPIN_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


REPIN = load_repin()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scope_rows(edit: Path = EDIT) -> list:
    return json.loads((edit / SCOPE).read_text())["rows"]


def plates(edit: Path, row: dict) -> dict:
    board = json.loads((edit / "parts" / Path(row["board"]).name).read_text())
    return {p["id"]: p for p in board["plates"]}


def made_up_repo(tmp: str, change_scope=None, change_board=None) -> Path:
    """A repo with film 009's scope and boards as they were when the takes were made, after the given changes.

    `change_board(part, board)` edits a board; every scope row is then pinned to its board as written, so only the
    thing under test can refuse. `change_scope(rows)` is applied last.
    """
    repo = Path(tmp)
    edit = repo / EDIT_REL
    (edit / "parts").mkdir(parents=True)
    scope = json.loads((THEN_EDIT / SCOPE).read_text())
    for rel in BOARDS:
        board = json.loads((THEN_EDIT / rel).read_text())
        if change_board:
            change_board(int(Path(rel).name[6]), board)
        (edit / rel).write_text(json.dumps(board, indent=2) + "\n")
    for row in scope["rows"]:
        row["board_sha256"] = sha(repo / row["board"])
    if change_scope:
        change_scope(scope["rows"])
    (edit / SCOPE).write_text(json.dumps(scope, indent=2) + "\n")
    return repo


def row_of(rows: list, plate_id: str) -> dict:
    return next(r for r in rows if r["id"] == plate_id)


def make_a_diagram(board: dict, plate_id: str) -> None:
    next(p for p in board["plates"] if p["id"] == plate_id).update(DIAGRAM, quality="code_graphic", flow_model=None)


NOTE = {"route": "code-graphic", "job": "J2631", "ruling": "history-of-science#180 comment 6801964131"}


class TheScopePinsTheBoardsAsTheyAre(unittest.TestCase):
    def test_every_one_of_the_twenty_rows_pins_its_board_as_it_is(self):
        rows = scope_rows()
        self.assertEqual(len(rows), 20)
        for row in rows:
            with self.subTest(row=row["id"]):
                self.assertEqual(row["board_sha256"], sha(ROOT / row["board"]),
                                 "a board changed: run 07_Edit-Project/_repin_tranche2_scope.py --write in the same pull request")

    def test_the_tool_loads_and_plans_and_spends_nothing(self):
        replaced = [r for r in scope_rows() if "replaced_by" in r]
        self.assertEqual(len(RUNNER.load_scope(ROOT)), 20 - len(replaced))
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "plan.json"
            env = {k: v for k, v in os.environ.items() if k != RUNNER.SUBMIT_ENV}
            done = subprocess.run([sys.executable, str(SCRIPT), "plan", "--repo", str(ROOT), "--out", str(out)],
                                  capture_output=True, text=True, env=env)
            self.assertEqual(done.returncode, 0, done.stderr)
            plan = json.loads(out.read_text())
            self.assertEqual((plan["submissions"], plan["keep"]), (0, False))


class ShotsThatBecameDrawnDiagrams(unittest.TestCase):
    def setUp(self):
        self.rows = scope_rows()
        self.replaced = [r for r in self.rows if "replaced_by" in r]

    def test_three_of_the_twenty_are_drawn_diagrams_now(self):
        # The five-metre graphic (J2631) took the place of both halves of one shot; the falling-Moon graphic (J2632)
        # took the place of the continuation whose third take failed its sheet.
        self.assertEqual({r["id"]: r["replaced_by"]["job"] for r in self.replaced},
                         {"05_minute_second_c1": "J2631", "05_minute_second_c2": "J2631", "01_really_falling_c1": "J2632"})

    def test_each_is_marked_in_the_scope_and_is_a_diagram_on_its_board(self):
        for row in self.rows:
            plate = plates(EDIT, row)[row["id"]]
            with self.subTest(row=row["id"]):
                if "replaced_by" in row:
                    self.assertEqual({k: plate.get(k) for k in DIAGRAM}, DIAGRAM)
                    self.assertEqual(row["replaced_by"]["route"], "code-graphic")
                    self.assertRegex(row["replaced_by"]["job"], r"^J\d{4}$")
                    self.assertTrue(row["replaced_by"]["ruling"].strip())
                    # The mark says what the board row itself records: the job, the ruling that scoped the diagram, the file.
                    spec = plate["code_graphic_spec"]
                    self.assertEqual(row["replaced_by"]["file"], spec["file"])
                    self.assertTrue(plate["engine_reason"].startswith(row["replaced_by"]["job"] + ":"))
                    self.assertTrue(spec["approval_ref"].endswith("/pull/180#issuecomment-" + row["replaced_by"]["ruling"].split()[-1]))
                else:
                    self.assertEqual((plate.get("route"), plate.get("tranche")), ("flow-first", 2))

    def test_the_tool_never_works_from_one(self):
        gone = {(int(r["part"]), r["id"]) for r in self.replaced}
        self.assertTrue(gone)
        rows = RUNNER.load_scope(ROOT)
        self.assertEqual(gone & {r.key for r in rows}, set())
        named = json.dumps(RUNNER.build_plan(rows, repo=ROOT))
        for _, plate_id in gone:
            self.assertNotIn(f'"{plate_id}"', named)
        # With nothing in the ledger the tool would start from the two parents, then work through its rows: none is one.
        batches = RUNNER.batch_rows(RUNNER.order_rows(rows))
        self.assertEqual(gone & {r.key for batch in batches for r in batch}, set())

    def test_every_other_row_reads_as_it_did_when_its_take_was_made(self):
        # The tests of how a take is guarded stand on the frozen boards. They still describe the tool only while
        # every row it may make reads the same on the real board. If this fails, a row still to be made was changed:
        # refresh tests/fixtures/hos009_as_minted with it, in the same reviewed change.
        then = {r.key: r for r in RUNNER.load_scope(THEN)}
        for row in RUNNER.load_scope(ROOT):
            with self.subTest(row=row.plate_id):
                self.assertEqual(row, then[row.key])


class AScopeAndABoardThatDisagree(unittest.TestCase):
    def refused(self, says, **changes):
        with tempfile.TemporaryDirectory() as tmp:
            repo = made_up_repo(tmp, **changes)
            with self.assertRaisesRegex(RUNNER.GuardError, says):
                RUNNER.load_scope(repo)

    def test_the_made_up_repo_loads_when_nothing_is_changed(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(len(RUNNER.load_scope(made_up_repo(tmp))), 20)

    def test_a_shot_drawn_on_the_board_and_marked_in_the_scope_is_left_out(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = made_up_repo(
                tmp, change_board=lambda part, board: part == 5 and make_a_diagram(board, "06_iss_apple_c1"),
                change_scope=lambda rows: row_of(rows, "06_iss_apple_c1").update(replaced_by=dict(NOTE)))
            rows = RUNNER.load_scope(repo)
            self.assertEqual(len(rows), 19)
            self.assertNotIn("06_iss_apple_c1", [r.plate_id for r in rows])

    def test_marked_replaced_while_the_board_still_allows_a_mint(self):
        self.refused("06_iss_apple_c1 is marked as replaced by a drawn diagram, but its board still allows a mint",
                     change_scope=lambda rows: row_of(rows, "06_iss_apple_c1").update(replaced_by=dict(NOTE)))

    def test_each_thing_that_makes_a_row_a_mint_is_checked(self):
        for field, value in (("route", "flow-first"), ("tranche", 2), ("generation_authorized", True), ("flow_credits_try1", 100)):
            def half(part, board, field=field, value=value):
                if part == 5:
                    make_a_diagram(board, "06_iss_apple_c1")
                    next(p for p in board["plates"] if p["id"] == "06_iss_apple_c1")[field] = value
            with self.subTest(field=field):
                self.refused("still allows a mint", change_board=half,
                             change_scope=lambda rows: row_of(rows, "06_iss_apple_c1").update(replaced_by=dict(NOTE)))

    def test_a_diagram_on_the_board_that_the_scope_does_not_mark(self):
        self.refused("06_iss_apple_c1 is not an authorised flow-first tranche-2 plate",
                     change_board=lambda part, board: part == 5 and make_a_diagram(board, "06_iss_apple_c1"))

    def test_the_mark_must_give_the_route_the_job_and_the_ruling(self):
        for bad in ({}, "J2631", dict(NOTE, route="flow-first"), dict(NOTE, job="the diagram job"), dict(NOTE, job=""),
                    dict(NOTE, ruling="  "), {k: v for k, v in NOTE.items() if k != "ruling"}, None):
            with self.subTest(mark=bad):
                self.refused("`replaced_by` must give the route `code-graphic`, the job and the Chief's ruling",
                             change_board=lambda part, board: part == 5 and make_a_diagram(board, "06_iss_apple_c1"),
                             change_scope=lambda rows, bad=bad: row_of(rows, "06_iss_apple_c1").update(replaced_by=copy.deepcopy(bad)))

    def test_a_replaced_row_still_has_to_match_its_pinned_board(self):
        def stale(rows):
            row_of(rows, "06_iss_apple_c1").update(replaced_by=dict(NOTE), board_sha256="0" * 64)
        self.refused("board hash mismatch", change_scope=stale,
                     change_board=lambda part, board: part == 5 and make_a_diagram(board, "06_iss_apple_c1"))

    def test_a_shot_that_continues_a_diagram_cannot_be_made(self):
        # c2 starts from c1's last frame. If only c1 became a diagram, there would be no clip for c2 to start from.
        self.refused("05_minute_second_c2 continues P4:05_minute_second_c1, which is now a drawn diagram",
                     change_board=lambda part, board: part == 4 and make_a_diagram(board, "05_minute_second_c1"),
                     change_scope=lambda rows: row_of(rows, "05_minute_second_c1").update(replaced_by=dict(NOTE)))

    def test_a_parent_that_became_a_diagram_stops_the_tool(self):
        self.refused("scope is missing parents P02:10_how_high",
                     change_board=lambda part, board: part == 2 and make_a_diagram(board, "10_how_high"),
                     change_scope=lambda rows: row_of(rows, "10_how_high").update(replaced_by=dict(NOTE)))

    def test_the_same_row_twice_is_refused_marked_or_not(self):
        def twice(rows):
            rows[-1] = dict(rows[0])
        self.refused("duplicate scope row", change_scope=twice)

        def marked_twice(rows):
            row_of(rows, "06_iss_apple_c1").update(replaced_by=dict(NOTE))
            rows[0] = dict(row_of(rows, "06_iss_apple_c1"))
        self.refused("duplicate scope row", change_scope=marked_twice,
                     change_board=lambda part, board: part == 5 and make_a_diagram(board, "06_iss_apple_c1"))


def draw(board: dict, plate_id: str, job="J2999", ref="https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-123",
         file="code_graphic_009_made_up.mp4") -> None:
    """Make a row a drawn diagram the way a real change does: the route, and the job, ruling and file on the row."""
    make_a_diagram(board, plate_id)
    plate = next(p for p in board["plates"] if p["id"] == plate_id)
    plate["engine_reason"] = f"{job}: Chief-scoped no-spend diagram" if job else "a diagram"
    plate["code_graphic_spec"] = {k: v for k, v in (("file", file), ("approval_ref", ref)) if v}


class KeepingTheScopeInStep(unittest.TestCase):
    """`_repin_tranche2_scope.py`: run in the pull request that changes a board, so both are reviewed together."""

    def run_it(self, *args):
        return subprocess.run([sys.executable, str(REPIN_SCRIPT), *args], capture_output=True, text=True)

    def test_the_real_scope_is_in_step(self):
        self.assertEqual(REPIN.repin(ROOT)[1], [])
        done = self.run_it()
        self.assertEqual((done.returncode, done.stdout.strip()), (0, "the scope pins every board as it is"))

    def test_it_would_write_the_real_scope_exactly_as_it_is(self):
        scope, _ = REPIN.repin(ROOT)
        self.assertEqual(json.dumps(scope, indent=2) + "\n", (EDIT / SCOPE).read_text())

    def test_a_changed_board_is_pinned_again_and_nothing_else_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = made_up_repo(tmp)
            before = scope_rows(repo / EDIT_REL)
            board = repo / EDIT_REL / "parts/part-05_plates_v05.json"
            doc = json.loads(board.read_text())
            doc["plates"][0]["a_keep_record"] = "KEEP by the Chief"
            board.write_text(json.dumps(doc, indent=2) + "\n")
            with self.assertRaisesRegex(RUNNER.GuardError, "board hash mismatch"):
                RUNNER.load_scope(repo)
            said = self.run_it("--repo", str(repo))                        # only says so, and writes nothing
            self.assertEqual(said.returncode, 1)
            self.assertIn("out of step", said.stderr)
            self.assertEqual(scope_rows(repo / EDIT_REL), before)
            done = self.run_it("--repo", str(repo), "--write")
            self.assertEqual(done.returncode, 0, done.stderr)
            after = scope_rows(repo / EDIT_REL)
            moved = [a["id"] for a, b in zip(after, before) if a != b]
            self.assertEqual(moved, [r["id"] for r in before if r["board"].endswith("part-05_plates_v05.json")])
            for a, b in zip(after, before):
                self.assertEqual({k: v for k, v in a.items() if k != "board_sha256"},
                                 {k: v for k, v in b.items() if k != "board_sha256"})
            self.assertEqual(len(RUNNER.load_scope(repo)), 20)
            self.assertEqual(self.run_it("--repo", str(repo)).returncode, 0)

    def test_a_shot_that_became_a_diagram_is_marked_from_what_its_board_row_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = made_up_repo(tmp, change_board=lambda part, board: part == 5 and draw(board, "06_iss_apple_c1"))
            with self.assertRaisesRegex(RUNNER.GuardError, "not an authorised flow-first tranche-2 plate"):
                RUNNER.load_scope(repo)
            self.assertEqual(self.run_it("--repo", str(repo), "--write").returncode, 0)
            mark = row_of(scope_rows(repo / EDIT_REL), "06_iss_apple_c1")["replaced_by"]
            self.assertEqual(mark, {"route": "code-graphic", "job": "J2999", "ruling": "history-of-science#180 comment 123",
                                    "file": "code_graphic_009_made_up.mp4"})
            rows = RUNNER.load_scope(repo)
            self.assertEqual((len(rows), "06_iss_apple_c1" in [r.plate_id for r in rows]), (19, False))

    def test_a_diagram_row_that_does_not_record_its_job_ruling_and_file_stops_it(self):
        for missing in ({"job": ""}, {"ref": ""}, {"ref": "desk 123"}, {"file": ""}):
            with self.subTest(missing=missing), tempfile.TemporaryDirectory() as tmp:
                repo = made_up_repo(tmp, change_board=lambda part, board: part == 5 and draw(board, "06_iss_apple_c1", **missing))
                with self.assertRaisesRegex(REPIN.RepinError, "does not name its job"):
                    REPIN.repin(repo)
                done = self.run_it("--repo", str(repo), "--write")
                self.assertEqual(done.returncode, 2)
                self.assertNotIn("replaced_by", row_of(scope_rows(repo / EDIT_REL), "06_iss_apple_c1"))

    def test_a_marked_row_whose_board_is_a_mint_again_is_not_unmarked(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = made_up_repo(tmp, change_scope=lambda rows: row_of(rows, "06_iss_apple_c1").update(replaced_by=dict(NOTE)))
            with self.assertRaisesRegex(REPIN.RepinError, "06_iss_apple_c1 is marked replaced, but its board routes it to 'flow-first' again"):
                REPIN.repin(repo)


class TheRetakePathsAreHistory(unittest.TestCase):
    """J2583's second takes and J2626's third takes are made, and their evidence is merged. Each scope file is left
    pinning the boards its takes were made from, so on the real repo the old flags refuse before any Create."""

    def test_the_old_flags_refuse_on_the_real_repo(self):
        rows = RUNNER.load_scope(ROOT)
        for job in ("J2583", "J2626"):
            with self.subTest(job=job), tempfile.TemporaryDirectory() as tmp:
                with self.assertRaisesRegex(RUNNER.GuardError, f"{job} retake (board hash mismatch|outside original tranche scope)"):
                    RUNNER.retake_batch(ROOT, rows, [], Path(tmp), job)

    def test_their_records_are_exactly_as_they_were_merged(self):
        self.assertEqual({name: sha(EDIT / name) for name in RECORDS}, RECORDS)

    def test_the_tool_knows_those_two_and_no_other(self):
        self.assertEqual(sorted(RUNNER.RETAKES), ["J2583", "J2626"])



class TheC2PathIsGone(unittest.TestCase):
    """The second take of 05_minute_second_c2 was never made: both halves of that shot became the five-metre graphic.
    The Chief closed the path once the graphic was KEEP (desk 6800446389 point 3)."""

    def test_no_file_no_flag_no_code(self):
        self.assertFalse((EDIT / "TRANCHE2_RETAKES_J2630.json").exists())
        self.assertFalse((ROOT / "tests/test_hos009_c2_path.py").exists())
        text = SCRIPT.read_text()
        for word in ("J2630", "j2630", "parent_keep"):
            self.assertNotIn(word, text)

    def test_the_flag_is_not_a_flag_any_more(self):
        done = subprocess.run([sys.executable, str(SCRIPT), "submit", "--retakes-j2630"], capture_output=True, text=True,
                              env={k: v for k, v in os.environ.items() if k != RUNNER.SUBMIT_ENV})
        self.assertEqual(done.returncode, 2)
        self.assertIn("unrecognized arguments: --retakes-j2630", done.stderr)


class TheFrozenBoards(unittest.TestCase):
    """tests/fixtures/hos009_as_minted: the five boards and the scope as they were at #528, before any diagram."""

    def test_the_frozen_scope_pins_the_frozen_boards_and_all_twenty_load(self):
        for row in scope_rows(FIXTURE):
            self.assertEqual(row["board_sha256"], sha(FIXTURE / "parts" / Path(row["board"]).name))
            self.assertNotIn("replaced_by", row)
        self.assertEqual(len(RUNNER.load_scope(THEN)), 20)

    def test_they_are_the_boards_the_third_takes_were_made_from(self):
        record = json.loads((EDIT / "TRANCHE2_RETAKES_J2626.json").read_text())
        for row in record["rows"]:
            self.assertEqual(row["board_sha256"], sha(FIXTURE / "parts" / Path(row["board"]).name))

    def test_the_frozen_copies_are_not_edited(self):
        self.assertEqual({rel: sha(FIXTURE / rel) for rel in (SCOPE, *BOARDS)}, FROZEN)

    def test_the_repo_as_it_was_holds_the_frozen_files_and_links_to_the_rest(self):
        for rel in (SCOPE, *BOARDS):
            self.assertFalse((THEN_EDIT / rel).is_symlink())
            self.assertEqual(sha(THEN_EDIT / rel), FROZEN[rel])
        self.assertTrue((THEN_EDIT / "TRANCHE2_RETAKES_J2626.json").is_symlink())
        self.assertEqual((THEN_EDIT / "_mint_flow_v05_tranche2.py").resolve(), SCRIPT.resolve())
        self.assertFalse((THEN / ".git").exists())


if __name__ == "__main__":
    unittest.main()
