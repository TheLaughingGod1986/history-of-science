"""The status tool reads each film's own status file (J2622) and keeps no built page in the repo.

`00_Brand/Channel-Setup/tools/status_board.py` puts the board together from every film's `status.json` and the
channel's `BOARD.json`, checks them, and builds the two pages on demand. These hold that: the pages are drawn from the
per-film files, a wrong file is named, dates count from the day the page is built, and a built page that someone
commits again is caught.
"""
import contextlib
import datetime as dt
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "00_Brand/Channel-Setup/tools"


def load(name, file):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, TOOLS / file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


sb = load("hos_status_board", "status_board.py")
fs = sb.film_status

BOARD = {
    "updated": "2026-10-01", "updated_by": "someone", "board_url": "",
    "stages": [{"key": "script", "label": "Script", "weight": 60, "owner": "Grok"},
               {"key": "edit", "label": "Edit", "weight": 40, "owner": "Cursor"}],
    "next_steps": ["020: finish the script"], "credits": [],
}
FILMS = {
    "020": {"film": "020", "title": "How Penicillin Was Found", "air": "2027-01-21", "ready_by": "2027-01-17", "summary": "Planned.",
            "stages": {"script": {"state": "doing", "underway": True, "steps": [2, 5], "steps_unit": "parts"},
                       "edit": {"state": "todo", "due": "2027-01-10"}}, "claims": [], "next": ""},
    "021": {"film": "021", "title": "A Second Film", "air": "", "ready_by": "", "summary": "",
            "stages": {"script": {"state": "done"}, "edit": {"state": "todo"}}, "claims": [], "next": ""},
}


class FromEachFilmsOwnFile(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.films, self.board, self.channel = root / "02_Video-Projects", root / "BOARD.json", root / "channel.json"
        for fid, doc in FILMS.items():
            folder = self.films / f"{fid}_X"
            folder.mkdir(parents=True)
            (folder / "status.json").write_text(json.dumps(doc))
        self.board.write_text(json.dumps({k: v for k, v in BOARD.items() if k != "stages"}))
        self.channel.write_text(json.dumps({"stages": fs.stages_out(BOARD["stages"])}))
        for name, value in (("FILMS", self.films), ("BOARD", self.board), ("CHANNEL", self.channel)):
            patch = mock.patch.object(fs, name, value)
            patch.start()
            self.addCleanup(patch.stop)
        # read() takes its defaults when it is defined, so hand it the made-up places
        patch = mock.patch.object(fs, "read", lambda films=self.films, board=self.board, channel=self.channel, _read=fs.read:
                                  _read(films, board, channel))
        patch.start()
        self.addCleanup(patch.stop)

    def test_the_page_is_drawn_from_the_per_film_files(self):
        data = sb.load(dt.date(2026, 11, 12))
        self.assertEqual([f["id"] for f in data["films"]], ["020", "021"])
        self.assertEqual(data["films"][0]["stages"]["script"]["status"], "doing")      # the shape the renderers read
        page = sb.render(data)
        self.assertIn("| **020** How Penicillin Was Found |", page)
        self.assertIn("| **021** A Second Film |", page)
        self.assertIn("1. 020: finish the script", page)
        self.assertEqual(sb.validate(data), [])

    def test_dates_count_from_the_day_it_is_built_not_from_a_stamp_in_a_file(self):
        early, late = sb.render(sb.load(dt.date(2026, 11, 12))), sb.render(sb.load(dt.date(2026, 12, 12)))
        self.assertIn("**Built Thu 12 Nov 2026**", early)
        self.assertIn("**Built Sat 12 Dec 2026**", late)
        self.assertIn("(70 d)", early)                                               # to the 21 Jan air date
        self.assertIn("(40 d)", late)
        self.assertNotIn("2026-10-01", early)                                        # the old shared stamp is not used
        self.assertNotIn("updated by", early)

    def test_the_page_says_it_is_built_and_names_no_file_that_is_gone(self):
        page = sb.render(sb.load(dt.date(2026, 11, 12)))
        self.assertIn("This page is not kept in the repo", page)
        self.assertNotIn("PIPELINE.json", page)

    def test_a_wrong_status_file_is_named(self):
        bad = dict(FILMS["021"], stages={"script": {"state": "finished"}, "edit": {"state": "todo"}})
        (self.films / "021_X" / "status.json").write_text(json.dumps(bad))
        self.assertIn("021/script: status must be one of", " ".join(sb.validate(sb.load(dt.date(2026, 11, 12)))))
        with contextlib.redirect_stderr(io.StringIO()) as err, mock.patch.object(sb, "kept_pages", lambda root=None: []):
            self.assertEqual(sb.main(["--check"]), 1)
        self.assertIn("021/script", err.getvalue())

    def test_a_film_missing_a_stage_is_named(self):
        short = dict(FILMS["021"], stages={"script": {"state": "done"}})
        (self.films / "021_X" / "status.json").write_text(json.dumps(short))
        self.assertIn("021: missing stage 'edit'", sb.validate(sb.load(dt.date(2026, 11, 12))))

    def test_check_writes_nothing_and_a_plain_run_builds_both_pages(self):
        out, kanban = Path(self.tmp.name) / "STATUS.md", Path(self.tmp.name) / "index.html"
        template = Path(self.tmp.name) / "template.html"
        template.write_text("<script>const SNAPSHOT = /*SNAPSHOT*/null;</script>")
        with mock.patch.object(sb, "OUT", out), mock.patch.object(sb, "KANBAN_OUT", kanban), \
                mock.patch.object(sb, "KANBAN_TEMPLATE", template), mock.patch.object(sb, "ROOT", Path(self.tmp.name)), \
                mock.patch.object(sb, "kept_pages", lambda root=None: []), contextlib.redirect_stdout(io.StringIO()) as said:
            self.assertEqual(sb.main(["--check"]), 0)
            self.assertFalse(out.exists() or kanban.exists())
            self.assertIn("2 status files and BOARD.json are in order", said.getvalue())
            self.assertEqual(sb.main([]), 0)
        self.assertIn("How Penicillin Was Found", out.read_text())
        self.assertIn('"title":"How Penicillin Was Found"', kanban.read_text())


class TheBuiltPagesStayOutOfTheRepo(unittest.TestCase):
    def test_a_built_page_that_is_committed_again_is_caught(self):
        with tempfile.TemporaryDirectory() as t:
            repo = Path(t)
            run = lambda *a: subprocess.run(["git", "-C", t, *a], capture_output=True, check=True)
            run("init", "-q")
            (repo / "STATUS.md").write_text("built\n")
            (repo / "notes.md").write_text("kept\n")
            with mock.patch.object(sb, "ROOT", repo), mock.patch.object(sb, "OUT", repo / "STATUS.md"), \
                    mock.patch.object(sb, "KANBAN_OUT", repo / "00_Brand/Channel-Setup/kanban/index.html"):
                self.assertEqual(sb.kept_pages(repo), [])                       # built here, not committed: fine
                run("add", "notes.md", "STATUS.md")
                self.assertEqual(sb.kept_pages(repo), ["STATUS.md"])

    def test_this_repo_keeps_neither_once_the_films_have_their_own_files(self):
        if not fs.BOARD.exists():
            self.skipTest("the films are still in PIPELINE.json: the switch has not been made")
        self.assertEqual(sb.kept_pages(), [])
        self.assertFalse(fs.PIPELINE.exists(), "PIPELINE.json and the per-film files must not both be kept")


if __name__ == "__main__":
    unittest.main()
