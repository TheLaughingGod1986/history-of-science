"""One status file per film (J2622): PIPELINE.json can become one file per film and come back with nothing lost.

The converter is 00_Brand/Channel-Setup/tools/film_status.py. These hold the promise it makes: `join(split(x)) == x`
for the real file and for awkward made-up ones, a film's file is in the shape Orbit With Ben's films use, and a film
is never filed under a guessed folder when two carry its number.
"""
import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load():
    name = "hos_film_status"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, ROOT / "00_Brand/Channel-Setup/tools/film_status.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


fs = load()

MADE_UP = {
    "updated": "2026-11-11", "updated_by": "Claude", "board_url": "https://example.invalid/board",
    "stages": [{"key": "script", "label": "Script", "weight": 60, "owner": "Grok"},
               {"key": "edit", "label": "Edit", "weight": 40, "owner": "Cursor"}],
    "next_steps": ["020: write the script"], "credits": [{"pool": "voice", "left": "1 of 2", "rule": "ask first"}],
    "films": [
        {"id": "020", "title": "How Penicillin Was Found", "air": "2027-01-21", "ready_by": "2027-01-17", "summary": "Planned.",
         "stages": {"script": {"status": "doing", "owner": "Grok", "since": "2026-11-10T09:00", "underway": True,
                               "steps": [2, 5], "steps_unit": "parts", "note": "part 3 next", "jobs": ["J1"]},
                    "edit": {"status": "todo", "due": "2027-01-10", "waiting": "the script", "left": "2 days", "eta": "2027-01-12"}}},
        {"id": "021", "title": "A film with nothing yet", "air": "", "ready_by": "", "summary": "",
         "stages": {"script": {"status": "todo"}, "edit": {"status": "todo"}}},
    ],
}


class RoundTrip(unittest.TestCase):
    def test_the_real_file_comes_back_unchanged(self):
        data = json.loads(fs.PIPELINE.read_text())
        board, statuses = fs.split(data)
        self.assertEqual(fs.join(board, statuses), data)
        self.assertEqual(len(statuses), len(data["films"]))
        self.assertNotIn("films", board)

    def test_a_made_up_file_with_every_field_comes_back_unchanged(self):
        before = copy.deepcopy(MADE_UP)
        board, statuses = fs.split(MADE_UP)
        self.assertEqual(fs.join(board, statuses), before)
        self.assertEqual(MADE_UP, before)                               # and the input is not changed on the way

    def test_an_order_that_is_not_by_number_is_kept(self):
        data = dict(MADE_UP, films=list(reversed(MADE_UP["films"])))
        board, statuses = fs.split(data)
        self.assertEqual(board["film_order"], ["021", "020"])
        self.assertEqual(fs.join(board, statuses), data)
        self.assertNotIn("film_order", fs.split(MADE_UP)[0])            # by number: nothing extra is stored

    def test_a_field_nobody_has_used_yet_survives(self):
        data = copy.deepcopy(MADE_UP)
        data["films"][0]["series"] = "medicine"
        data["films"][0]["stages"]["edit"]["reviewer"] = "Claude"
        data["a_new_top_level_thing"] = {"x": 1}
        self.assertEqual(fs.join(*fs.split(data)), data)

    def test_through_files_on_disk(self):
        with tempfile.TemporaryDirectory() as t:
            films, ideas, board_file = Path(t) / "02_Video-Projects", Path(t) / "ideas", Path(t) / "BOARD.json"
            films.mkdir(), ideas.mkdir()
            board, statuses = fs.split(MADE_UP)
            for fid, path in fs.paths(MADE_UP, films, ideas).items():
                path.parent.mkdir(parents=True)
                path.write_text(fs.dump(statuses[fid]))
            board_file.write_text(fs.dump(board))
            self.assertEqual(fs.read(films, board_file), MADE_UP)


class OneFilmsFile(unittest.TestCase):
    def test_it_is_in_the_shape_orbits_films_use(self):
        doc = fs.to_status(MADE_UP["films"][0])
        self.assertEqual(list(doc)[0], "film")
        self.assertEqual((doc["film"], doc["title"], doc["air"]), ("020", "How Penicillin Was Found", "2027-01-21"))
        self.assertEqual((doc["claims"], doc["next"]), ([], ""))
        self.assertEqual(doc["stages"]["script"]["state"], "doing")
        self.assertNotIn("status", doc["stages"]["script"])
        self.assertNotIn("id", doc)

    def test_what_this_channel_records_beyond_that_keeps_its_name(self):
        doc = fs.to_status(MADE_UP["films"][0])
        self.assertEqual((doc["ready_by"], doc["summary"]), ("2027-01-17", "Planned."))
        self.assertEqual(doc["stages"]["script"]["steps"], [2, 5])
        self.assertEqual(doc["stages"]["edit"]["waiting"], "the script")

    def test_a_claim_or_a_next_line_written_later_is_not_lost_on_the_way_back(self):
        doc = fs.to_status(MADE_UP["films"][0])
        doc["claims"] = [{"by": "Cursor", "stage": "edit"}]
        doc["next"] = "cut the opening"
        film = fs.from_status(doc)
        self.assertEqual((film["claims"], film["next"]), ([{"by": "Cursor", "stage": "edit"}], "cut the opening"))
        self.assertEqual(fs.to_status(film), doc)

    def test_a_stage_that_already_has_a_state_is_refused(self):
        film = copy.deepcopy(MADE_UP["films"][1])
        film["stages"]["script"]["state"] = "done"
        with self.assertRaisesRegex(ValueError, "already has a `state`"):
            fs.to_status(film)

    def test_two_films_with_one_number_are_refused(self):
        data = dict(MADE_UP, films=[MADE_UP["films"][0], dict(MADE_UP["films"][1], id="020")])
        with self.assertRaisesRegex(ValueError, "two films share a number: 020"):
            fs.split(data)


class WhereAFilmsFileGoes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.films, self.ideas = Path(self.tmp.name) / "02_Video-Projects", Path(self.tmp.name) / "ideas"
        self.films.mkdir(), self.ideas.mkdir()

    def test_the_folder_that_already_carries_its_number(self):
        (self.films / "020_Penicillin-Fleming-Florey").mkdir()
        (self.ideas / "020_Some-Other-Name").mkdir()
        self.assertEqual(fs.folder_for(MADE_UP["films"][0], self.films, self.ideas), self.films / "020_Penicillin-Fleming-Florey")

    def test_else_the_name_its_idea_folder_has(self):
        (self.ideas / "020_Penicillin-Fleming-Florey").mkdir()
        self.assertEqual(fs.folder_for(MADE_UP["films"][0], self.films, self.ideas), self.films / "020_Penicillin-Fleming-Florey")

    def test_else_a_name_made_from_its_title(self):
        self.assertEqual(fs.folder_for(MADE_UP["films"][0], self.films, self.ideas), self.films / "020_How-Penicillin-Was-Found")
        self.assertEqual(fs.slug("DNA: the X-ray photo that showed it!"), "DNA-The-X-Ray-Photo-That")
        self.assertEqual(fs.slug(""), "Untitled")

    def test_two_folders_with_its_number_is_an_error_not_a_guess(self):
        (self.films / "020_One").mkdir(), (self.films / "020_Two").mkdir()
        with self.assertRaisesRegex(ValueError, "more than one film folder carries this number: 020_One, 020_Two"):
            fs.folder_for(MADE_UP["films"][0], self.films, self.ideas)

    def test_every_real_film_has_one_place(self):
        data = json.loads(fs.PIPELINE.read_text())
        where = fs.paths(data)
        self.assertEqual(sorted(where), sorted(f["id"] for f in data["films"]))
        self.assertEqual(len({p.parent for p in where.values()}), len(where))        # no two films in one folder
        for fid, path in where.items():
            self.assertTrue(path.parent.name.startswith(fid + "_"), path)
            self.assertEqual(path.name, "status.json")


if __name__ == "__main__":
    unittest.main()
