import importlib.util
import pathlib
import unittest

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("join_rough", HERE / "join_timing_rough_v10.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TimingRoughOrder(unittest.TestCase):
    def test_ninety_three_rows_cover_the_locked_film_without_a_gap(self):
        plan, by_id = mod.load_plan()
        ordered = mod.sequence(plan, by_id)
        self.assertEqual(len(ordered), 93)
        self.assertEqual(len(by_id), 88)
        held = [item["row_id"] for item in ordered if item["kind"] == "archive_download_held"]
        self.assertEqual(held, list(mod.HELD))
        self.assertEqual(ordered[0]["start_frame"], 0)
        self.assertEqual(ordered[-1]["end_frame_exclusive"], 16059)
        self.assertEqual(sum(item["frames"] for item in ordered), 16059)
        self.assertTrue(all(item["frames"] <= 240 for item in ordered))
        reuse = by_id["P5:16b_reuse_pocket_watch_to_globe"]
        self.assertEqual(reuse["status"], "dependency_slate")
        self.assertNotIn("P5:16b_reuse_pocket_watch_to_globe", mod.HELD)


if __name__ == "__main__":
    unittest.main()
