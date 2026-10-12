from unittest.mock import patch
import copy, datetime as dt, json, pathlib, sys, tempfile, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import studio
import sync_rules

T0 = dt.datetime(2026, 10, 5, 15, 0, tzinfo=dt.timezone.utc)

def blank():
    d = studio.load(studio.PIPELINE)
    d["claims"] = []
    return d

class Claims(unittest.TestCase):
    def test_claim_release_and_takeover(self):
        d = blank()
        self.assertIsNone(studio.do_claim(d, "008", "facts", "chief", 30, "draft", T0))
        self.assertEqual(studio.film(d, "008")["stages"]["facts"]["status"], "doing")
        self.assertEqual(d["claims"][0]["eta"], "2026-10-05T15:30Z")
        self.assertTrue(studio.do_claim(d, "008", "facts", "other", 30, "", T0).startswith("held"))
        self.assertIsNone(studio.do_claim(d, "009", "facts", "other", 30, "", T0))
        self.assertIsNone(studio.do_claim(d, "008", "picture", "other", 30, "", T0))
        self.assertIsNone(studio.do_claim(d, "008", "facts", "chief", 30, "renew", T0))
        self.assertEqual(len(d["claims"]), 3)
        self.assertIsNone(studio.do_claim(d, "008", "facts", "other", 60, "retry", T0 + dt.timedelta(minutes=31)))
        self.assertIn("took over stalled", d["claims"][-1]["note"])
        self.assertIsNotNone(studio.do_release(d, "008", "facts", "chief", "done", None))
        self.assertIsNone(studio.do_release(d, "008", "facts", "other", "done", "abc"))
        self.assertEqual(studio.film(d, "008")["stages"]["facts"]["status"], "done")

class BoardAndStale(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = pathlib.Path(self.tmp.name) / "PIPELINE.json"
        self.out = pathlib.Path(self.tmp.name) / "STATUS.md"
        self.path.write_text(json.dumps(blank()))
    def tearDown(self):
        self.tmp.cleanup()
    def cli(self, *args, at=T0):
        with patch.object(studio, "now", return_value=at):
            return studio.main(["--pipeline", str(self.path), "--status", str(self.out), *args])
    def test_round_trip_regenerates_and_preserves_source(self):
        original = studio.load(self.path)
        self.assertEqual(self.cli("claim", "008", "vo", "--by", "chief"), 0)
        d = studio.load(self.path)
        self.assertEqual(self.out.read_text(), studio.status_board.render(d))
        self.assertIn("chief", self.out.read_text())
        self.assertEqual(d["as_of"], studio.iso(T0))
        self.assertEqual(self.cli("claim", "008", "vo", "--by", "other"), 75)
        self.assertEqual(self.cli("release", "008", "vo", "--by", "chief", "--state", "doing"), 0)
        d = studio.load(self.path)
        self.assertEqual(d["claims"], [])
        self.assertEqual(self.out.read_text(), studio.status_board.render(d))
        self.assertEqual(original["next_steps"], d["next_steps"])
        self.assertEqual(original["credits"], d["credits"])
    def test_unknown_rejected_without_write(self):
        before = self.path.read_text()
        self.assertEqual(self.cli("claim", "004", "vo", "--by", "chief"), 1)
        self.assertEqual(self.cli("claim", "008", "sources", "--by", "chief"), 1)
        self.assertEqual(self.path.read_text(), before)
        self.assertFalse(self.out.exists())
    def test_stale_real_clock_and_board(self):
        self.assertEqual(self.cli("claim", "008", "vo", "--by", "chief", "--eta", "30"), 0)
        self.assertEqual(self.cli("stale", at=T0 + dt.timedelta(minutes=29)), 0)
        self.assertEqual(self.cli("stale", at=T0 + dt.timedelta(minutes=31)), 1)
        self.assertIn("STALLED", studio.board(studio.load(self.path), T0 + dt.timedelta(minutes=31)))
    def test_set_regenerates(self):
        self.assertEqual(self.cli("set", "008", "vo", "blocked", "--ref", "abc"), 0)
        d = studio.load(self.path)
        self.assertEqual(studio.film(d, "008")["stages"]["vo"]["status"], "blocked")
        self.assertEqual(self.out.read_text(), studio.status_board.render(d))

class GitClaims(unittest.TestCase):
    def test_retry_reads_new_holder_and_returns_held(self):
        import subprocess
        initial = blank()
        winner = blank()
        studio.do_claim(winner, "008", "vo", "winner", 60, "", T0)
        calls = []
        def fake_git(*args):
            calls.append(args)
            return subprocess.CompletedProcess(args, 1 if args[0] == "push" else 0, "", "")
        with patch.object(studio, "git", side_effect=fake_git), patch.object(studio, "load", side_effect=[initial, winner]), patch.object(studio, "save") as save, patch.object(studio, "now", return_value=T0):
            err = studio.with_git(studio.PIPELINE, studio.STATUS,
                lambda d: studio.do_claim(d, "008", "vo", "loser", 60, "", T0), "claim", T0)
        self.assertTrue(err.startswith("held by winner"))
        self.assertEqual(save.call_count, 1)
        self.assertEqual(sum(c[0] == "push" for c in calls), 1)
        commit = next(c for c in calls if c[0] == "commit")
        self.assertEqual(commit[-2:], (str(studio.PIPELINE), str(studio.STATUS)))
        self.assertIn(("reset", "--soft", "HEAD~1"), calls)

class StatusBoard(unittest.TestCase):
    def test_validation_and_deterministic_stalled(self):
        d = blank()
        studio.do_claim(d, "008", "vo", "chief", 30, "pipe | newline\n", T0)
        d["as_of"] = studio.iso(T0)
        self.assertEqual(studio.status_board.validate(d), [])
        rendered = studio.status_board.render(d)
        self.assertNotIn("**STALLED**", rendered)
        with patch.object(studio, "now", return_value=T0 + dt.timedelta(days=100)):
            self.assertEqual(studio.status_board.render(d), rendered)
        d["as_of"] = studio.iso(T0 + dt.timedelta(minutes=31))
        self.assertIn("**STALLED**", studio.status_board.render(d))
        for field, value in (("film", "004"), ("stage", "sources"), ("at", "bad"), ("eta", "2026-10-05T15:00")):
            broken = copy.deepcopy(d)
            broken["claims"][0][field] = value
            self.assertTrue(studio.status_board.validate(broken))
        d["claims"] = {}
        self.assertTrue(studio.status_board.validate(d))

class SyncRules(unittest.TestCase):
    SRC = "# A\n\n## Never\n- one\n- two\n\n## Other\nx\n"

    def test_hos_stale_merge_authority(self):
        stale = [rx for rx, _ in sync_rules.STALE]
        import re
        self.assertTrue(any(re.search(rx, "merging a PR;", re.I) for rx in stale))
        self.assertTrue(any(re.search(rx, "Stop for Ben's OK", re.I) for rx in stale))
        self.assertFalse(any(re.search(rx, "merging a PR that Claude hasn't PASSed;", re.I) for rx in stale))

    def test_section_body(self):
        self.assertEqual(sync_rules.section(self.SRC, "Never"), "- one\n- two\n")

    def test_block_rewritten_from_source(self):
        doc = "top\n<!-- SYNC: AGENTS.md#Never -->\n- stale\n<!-- /SYNC -->\nend\n"
        self.assertEqual(sync_rules.sync(doc, self.SRC),
                         "top\n<!-- SYNC: AGENTS.md#Never -->\n- one\n- two\n<!-- /SYNC -->\nend\n")

    def test_repo_rules_are_in_sync(self):
        self.assertEqual(sync_rules.main.__name__, "main")
        src = sync_rules.SOURCE.read_text()
        for rel in sync_rules.TARGETS:
            text = (sync_rules.ROOT / rel).read_text()
            self.assertEqual(sync_rules.sync(text, src), text, rel)
        self.assertEqual(sync_rules.stale_hits(), [])


if __name__ == "__main__":
    unittest.main()
