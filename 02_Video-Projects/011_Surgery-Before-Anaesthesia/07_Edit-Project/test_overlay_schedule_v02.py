"""The Anaesthesia cue schedule follows the locked words and never stacks two cards."""
import importlib.util
import json
import pathlib
import unittest

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("schedule", HERE / "overlay_schedule_v02.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

FORBIDDEN = (
    "4,848",
    "4848",
    "wembley",
    "jefferson",
    "$2",
    "egg",
    "january 1845",
    "7 april",
    "4 november",
    "42 years",
    "three minutes",
    "under 3",
    "30 march",
)


class OverlaySchedule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan, cls.words, cls.raw_path, cls.manifest = mod.load()
        cls.result = mod.build()

    def test_cards_start_on_the_last_spoken_word_and_do_not_stack(self):
        scheduled = self.result["scheduled"]
        self.assertGreaterEqual(len(scheduled), 30)
        self.assertFalse(self.result["checks"]["film_stage_pass"])
        for cue in scheduled:
            last = cue["word_indices"][-1]
            self.assertEqual(cue["in_s"], round(self.words[last]["start"], 3))
            self.assertEqual(
                cue["anchor_text"],
                " ".join(self.words[index]["text"] for index in cue["word_indices"]),
            )
            self.assertEqual(
                cue["raw_stt_indices"],
                [self.words[index]["raw_index"] for index in cue["word_indices"]],
            )
            self.assertGreater(cue["out_s"], cue["in_s"])
            self.assertLessEqual(round(cue["out_s"] - cue["in_s"], 3), 4)
            spoken = cue["text"].lower()
            for banned in FORBIDDEN:
                self.assertNotIn(banned, spoken)
        ordered = sorted(scheduled, key=lambda cue: cue["in_s"])
        for earlier, later in zip(ordered, ordered[1:]):
            self.assertLessEqual(earlier["out_s"], later["in_s"])

    def test_liston_is_named_when_he_is_first_said(self):
        liston = next(cue for cue in self.result["scheduled"] if cue["text"].startswith("Robert Liston"))
        date = next(cue for cue in self.result["scheduled"] if cue["text"] == "London, 21 December 1846")
        self.assertEqual(liston["in_s"], round(self.words[liston["word_indices"][-1]]["start"], 3))
        self.assertLessEqual(date["out_s"], liston["in_s"])
        self.assertGreaterEqual(round(date["out_s"] - date["in_s"], 3), 0.8)

    def test_unspoken_specifics_stay_held(self):
        reasons = " ".join(item.get("reason", "") for item in self.result["held"]).lower()
        scales = " ".join(item.get("reason", "") for item in self.result["scales"]).lower()
        for needle in ("under 3 minutes", "4,848", "january 1845", "two-dollar", "jefferson"):
            self.assertIn(needle, reasons)
        self.assertIn("wembley", scales)
        garden = next(cue for cue in self.result["scheduled"] if cue["text"] == "Public garden")
        self.assertNotIn("1868", garden["text"])
        spoken = " ".join(word["text"] for word in self.words).lower()
        for absent in ("wembley", "jefferson", "4,848", "boiling an egg"):
            self.assertNotIn(absent, spoken)

    def test_archive_credits_keep_the_approved_line(self):
        by_asset = {item["source_asset"]: item for item in self.result["credits"]}
        archives = [asset for asset in self.manifest["assets"] if asset["role"] == "archive"]
        self.assertEqual(len(archives), 13)
        for asset in archives:
            self.assertEqual(by_asset[asset["asset_id"]]["text"], asset["credit"])
        snow = by_asset["archive_P5_07a_arch_snow_chloroform_1858"]
        self.assertEqual(snow["status"], "held_layout_conflict")
        self.assertIn("P5:06b/who", snow["name_cards_on_row"])

    def test_saved_file_matches_the_builder(self):
        saved = json.loads((HERE / "OVERLAY_CUE_SCHEDULE_v02.json").read_text())
        self.assertEqual(saved, self.result)


if __name__ == "__main__":
    unittest.main()
