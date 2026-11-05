"""Code graphic lookup must use the exact film/part/row, without inventing media."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('hos_rule', Path(__file__).resolve().parents[1] / '00_Brand/Channel-Setup/tools/hos_build_rule_v02.py')
RULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RULE)

class GraphicResolution(unittest.TestCase):
    def test_exact_graphic_and_missing_row(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            film = root / '010_Alvarez-Clay-Line-Dinosaurs'
            folder = film / '07_Edit-Project/code_graphics_v01'
            folder.mkdir(parents=True)
            graphic = folder / 'code_graphic_010_p4_01_iridium_spike.mp4'
            graphic.touch()
            self.assertEqual(RULE.resolve_plate_path(root, '010', 'P4:01_iridium_spike', str(film)), graphic)
            self.assertIsNone(RULE.resolve_plate_path(root, '010', 'P5:01_iridium_spike', str(film)))
            self.assertIsNone(RULE.resolve_plate_path(root, '010', 'P4:02_missing', str(film)))

    def test_010_shorts_picture_plan_v03_passes_check_short(self):
        repo_root = Path(__file__).resolve().parents[1]
        plan_path = repo_root / '02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/10_Shorts/SHORTS_PICTURE_PLAN_v03.json'
        plan = RULE.load(plan_path)
        with tempfile.TemporaryDirectory() as temporary:
            film = Path(temporary) / '010_Alvarez-Clay-Line-Dinosaurs'
            folder = film / '07_Edit-Project/code_graphics_v01'
            folder.mkdir(parents=True)
            g1 = folder / 'code_graphic_010_p4_01_iridium_spike.mp4'
            g2 = folder / 'code_graphic_010_p5_11_why_survive.mp4'
            g1.touch()
            g2.touch()
            RULE._PROBE_CACHE[str(g1)] = 17.033
            RULE._PROBE_CACHE[str(g2)] = 14.4
            for short in plan['shorts']:
                errs = []
                RULE.check_short(repo_root, '010_Alvarez-Clay-Line-Dinosaurs', f"010:{short['id']}", short, str(film), errs)
                self.assertEqual(errs, [], f"{short['id']} failed check_short: {errs}")
