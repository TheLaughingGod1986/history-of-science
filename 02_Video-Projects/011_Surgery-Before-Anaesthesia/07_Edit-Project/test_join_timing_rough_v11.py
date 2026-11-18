import importlib.util
import pathlib
import unittest

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("join_v11", HERE / "join_timing_rough_v11.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TimingRoughV11(unittest.TestCase):
    def test_five_archive_rows_replace_the_holds(self):
        plan, by_id = mod.v10.load_plan()
        ordered = mod.sequence(plan, by_id)
        self.assertEqual(len(ordered), 93)
        self.assertEqual(ordered[0]["start_frame"], 0)
        self.assertEqual(ordered[-1]["end_frame_exclusive"], 16059)
        self.assertEqual(sum(item["frames"] for item in ordered), 16059)
        composites = [item["row_id"] for item in ordered if item["kind"] == "archive_composite"]
        self.assertEqual(composites, list(mod.FIVE))
        self.assertFalse(any(item["kind"] == "archive_download_held" for item in ordered))
        self.assertEqual(by_id["P5:16b_reuse_pocket_watch_to_globe"]["status"], "dependency_slate")


if __name__ == "__main__":
    unittest.main()
