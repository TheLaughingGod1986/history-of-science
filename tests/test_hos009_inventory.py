"""Inventory gate regressions: synthetic fixtures only, zero browser submits."""
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tests.test_hos009_tranche2_runner import RUNNER, ROOT

class StillInventoryTests(unittest.TestCase):
    def test_missing_corrupt_small_and_valid_inventory(self):
        rows = [row for row in RUNNER.load_scope(ROOT) if row.parent is None][:1]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp)
            path = RUNNER.still_path(media, row.part, row.plate_id)
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.verify_still_inventory(rows, media)
            path.parent.mkdir(parents=True)
            path.write_bytes(b'not an image')
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.verify_still_inventory(rows, media)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
                            'color=s=640x360', '-frames:v', '1', str(path)], check=True)
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.verify_still_inventory(rows, media)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
                            'color=s=1280x720', '-frames:v', '1', str(path)], check=True)
            inventory = RUNNER.verify_still_inventory(rows, media)
            self.assertEqual(inventory[0]['sha256'], RUNNER.sha256_file(path))
            self.assertEqual(inventory[0]['path'], str(path.resolve()))
            # Real Flow Nano Banana 2 / 2.1 16:9 stills are 1376x768 (1.791667, diff 0.0139 < 0.02).
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
                            'color=s=1376x768', '-frames:v', '1', str(path)], check=True)
            inventory_flow = RUNNER.verify_still_inventory(rows, media)
            self.assertEqual((inventory_flow[0]['width'], inventory_flow[0]['height']), (1376, 768))
            # Non-16:9 HD stills (e.g. 4:3 1440x1080) still fail closed.
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
                            'color=s=1440x1080', '-frames:v', '1', str(path)], check=True)
            with self.assertRaises(RUNNER.GuardError):
                RUNNER.verify_still_inventory(rows, media)

class InventoryBatchTests(unittest.TestCase):
    def make_still(self, media, row):
        path = RUNNER.still_path(media, row.part, row.plate_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
                        'color=s=1280x720', '-frames:v', '1', str(path)], check=True)
        return path

    def test_missing_later_row_blocks_first_submit(self):
        rows = RUNNER.order_rows(RUNNER.load_scope(ROOT))[:2]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); archive = root/'archive'; archive.mkdir()
            self.make_still(root/'media', rows[0])
            with patch.object(RUNNER, 'live_video_submit') as submit:
                with self.assertRaisesRegex(RUNNER.GuardError, 'missing inventory'):
                    RUNNER.execute_shared_batch(rows, media=root/'media', ledger_path=root/'ledger',
                        archive_dir=archive, accounting_state=root/'shared', test_archive=True)
                submit.assert_not_called()
            self.assertFalse((root/'ledger').exists())
            with RUNNER.SharedFlowAccounting(root/'shared') as account:
                self.assertFalse(account.snapshot()['charges'])

    def test_pinned_hash_mismatch_stops_inventory(self):
        rows = RUNNER.order_rows(RUNNER.load_scope(ROOT))[:1]
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp)
            path = self.make_still(media, rows[0])
            path.with_suffix('.sha256').write_text('0'*64+'\n')
            with self.assertRaisesRegex(RUNNER.GuardError, 'pinned'):
                RUNNER.verify_still_inventory(rows, media)

    def test_frame_changed_after_inventory_never_enters_browser(self):
        rows = RUNNER.order_rows(RUNNER.load_scope(ROOT))[:1]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); archive = root/'archive'; archive.mkdir()
            path = self.make_still(root/'media', rows[0])
            def changed(*args, **kwargs):
                path.write_bytes(b'changed after verification')
                return path
            with patch.object(RUNNER, 'prepare_start_frame', side_effect=changed), \
                 patch.object(RUNNER, 'live_video_submit') as submit:
                with self.assertRaisesRegex(RUNNER.GuardError, 'changed after inventory'):
                    RUNNER.execute_shared_batch(rows, media=root/'media', ledger_path=root/'ledger',
                        archive_dir=archive, accounting_state=root/'shared', test_archive=True)
                submit.assert_not_called()
            self.assertEqual(len(list(archive.glob('inventory-*.json'))), 1)
            self.assertFalse((root/'ledger').exists())
