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
