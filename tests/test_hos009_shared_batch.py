"""Shared-account batch integration. Fake browser and outputs; zero real submits."""
from pathlib import Path
from unittest.mock import patch
import tempfile
import unittest
from tests.test_hos009_tranche2_runner import RUNNER, THEN
from tests import test_hos009_tranche2_runner as fixtures


class SharedBatchTests(unittest.TestCase):
    def setup_batch(self, root, *, valid=True, drift=False, missing=False, disconnect=False):
        rows=RUNNER.order_rows(RUNNER.load_scope(THEN))[:2]
        calls=[]
        frame=root/'frame.png'
        frame.write_bytes(b'fake start still')
        def submitter(row,dest,frame,*,accounting,reservation,charge,evidence_path):
            calls.append(row.plate_id)
            accounting._assert_held()
            self.assertTrue(list((root/'archive').glob('.tranche2-write-probe-*')))
            page=fixtures.LiveCreateAdapterTests.Page(fixtures.LiveCreateAdapterTests().evidence())
            accounting.reserve(reservation,'HOS:009',RUNNER.MAX_TOTAL_CREDITS,live=10000)
            if drift: page.evidence['outputs']=['x4']
            if disconnect:
                def lost(): raise ConnectionError('uncertain around click')
                page.before_click=lost
            evidence=RUNNER.guarded_create(page,accounting,reservation=reservation,
                charge=charge,evidence_path=evidence_path)
            if not missing: dest.write_bytes(b'fake video fixture')
            return evidence
        def technical(dest,**kwargs):
            return {'ok':valid,'sha256':RUNNER.sha256_file(dest)}
        return rows,calls,submitter,technical

    def run_batch(self,root,rows,submitter,technical):
        inventory=[{'part':row.part,'plate_id':row.plate_id,'path':str((root/'frame.png').resolve()),
                    'sha256':RUNNER.sha256_file(root/'frame.png')} for row in rows if row.parent is None]
        with patch.object(RUNNER,'verify_still_inventory',return_value=inventory), \
             patch.object(RUNNER,'prepare_start_frame',return_value=root/'frame.png'), \
             patch.object(RUNNER,'strip_audio'),patch.object(RUNNER,'technical_report',side_effect=technical):
            return RUNNER.execute_shared_batch(rows,media=root/'media',ledger_path=root/'ledger.jsonl',
                archive_dir=root/'archive',accounting_state=root/'shared',submitter=submitter,
                test_archive=True,spend_ledger=root/'spend.jsonl')

    def test_two_outputs_have_distinct_shared_charges_and_immutable_receipts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'archive').mkdir()
            rows,calls,submit,technical=self.setup_batch(root)
            outputs=self.run_batch(root,rows,submit,technical)
            self.assertEqual(len(outputs),2)
            spend=[__import__('json').loads(line) for line in (root/'spend.jsonl').read_text().splitlines()]
            self.assertEqual(sum(r.get('amount',0) for r in spend),200)
            self.assertEqual(calls,[r.plate_id for r in rows])
            with RUNNER.SharedFlowAccounting(root/'shared') as account:
                snapshot=account.snapshot()
                self.assertEqual(len(snapshot['charges']),2)
                self.assertEqual(snapshot['liability'],6000)
            for entry in outputs:
                self.assertFalse(entry['keep'])
                self.assertEqual(entry['status'],'PENDING_REVIEW')
                self.assertTrue(Path(entry['archive']['dest']).exists())
                self.assertEqual(entry['shared_charge'],entry['create_evidence']['charge'])
                self.assertTrue((root/'archive'/(Path(entry['file']).name+'.receipt.json')).is_file())

    def test_bad_output_stops_before_second_row_and_cannot_be_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'archive').mkdir()
            rows,calls,submit,technical=self.setup_batch(root,valid=False)
            with self.assertRaisesRegex(RUNNER.GuardError,'technical output failed'):
                self.run_batch(root,rows,submit,technical)
            self.assertEqual(len(calls),1)
            latest=RUNNER.latest_entries(RUNNER.read_ledger(root/'ledger.jsonl'))
            self.assertEqual(latest[0]['status'],'FAILED')
            self.assertFalse(RUNNER.verified_output(latest[0]))

    def test_missing_output_keeps_local_hold_and_blocks_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'archive').mkdir()
            rows,calls,submit,technical=self.setup_batch(root,missing=True)
            with self.assertRaisesRegex(RUNNER.GuardError,'charged output missing'):
                self.run_batch(root,rows,submit,technical)
            with self.assertRaisesRegex(RUNNER.GuardError,'unresolved local output'):
                self.run_batch(root,rows,submit,technical)
            self.assertEqual(len(calls),1)

    def test_disconnect_blocks_another_channel_and_future_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'archive').mkdir()
            rows,calls,submit,technical=self.setup_batch(root,disconnect=True)
            with self.assertRaises(ConnectionError): self.run_batch(root,rows,submit,technical)
            with RUNNER.SharedFlowAccounting(root/'shared') as account:
                self.assertTrue(account.snapshot()['pending'])
                with self.assertRaises(RUNNER.GuardError):
                    account.reserve('owb','OWB:032',100,live=20000)
            with self.assertRaisesRegex(RUNNER.GuardError,'unresolved shared Create'):
                self.run_batch(root,rows,submit,technical)
            self.assertEqual(len(calls),1)

    def test_known_click_download_error_still_exports_once_and_blocks_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'archive').mkdir()
            rows,calls,submit,technical=self.setup_batch(root)
            def failed_download(*args,**kwargs):
                kwargs.pop('reservation_cap',None)  # the fixture submitter takes no cap (red on main since #522)
                submit(*args,**kwargs)
                raise RuntimeError('download failed after charge')
            with self.assertRaisesRegex(RuntimeError,'download failed'):
                self.run_batch(root,rows,failed_download,technical)
            original=(root/'spend.jsonl').read_bytes()
            self.assertEqual(len(original.splitlines()),2)
            with self.assertRaisesRegex(RUNNER.GuardError,'unresolved local output'):
                self.run_batch(root,rows,failed_download,technical)
            self.assertEqual((root/'spend.jsonl').read_bytes(),original)
            self.assertEqual(len(calls),1)

    def test_archive_missing_or_ui_drift_never_advances(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            rows,calls,submit,technical=self.setup_batch(root)
            with self.assertRaises(RUNNER.GuardError): self.run_batch(root,rows,submit,technical)
            self.assertFalse(calls)
            (root/'archive').mkdir()
            rows,calls,submit,technical=self.setup_batch(root,drift=True)
            with self.assertRaises(RUNNER.GuardError): self.run_batch(root,rows,submit,technical)
            with RUNNER.SharedFlowAccounting(root/'shared') as account:
                self.assertFalse(account.snapshot()['charges'])
            self.assertEqual(len(calls),1)


class ProductionPathTests(unittest.TestCase):
    def test_defaults_are_canonical_and_independent_of_environment(self):
        import os
        rows = RUNNER.load_scope(THEN)
        with patch.dict(os.environ, {'OWB_REPO': '/wrong/owb', 'HOS_REPO': '/wrong/hos'}), \
             patch.object(RUNNER, 'repo_root_from', return_value=THEN):
            state, report = RUNNER.production_batch_paths(
                accounting_state=None, spend_ledger=None, inventory_rows=rows)
        self.assertEqual(state, Path.home() / '_desk/state/flow/shared')
        self.assertEqual(report, Path.home() / 'YouTube/orbit-with-ben/05_Analytics/ai_spend/ledger.jsonl')

    def test_missing_subset_duplicate_and_modified_inventory_refused(self):
        from dataclasses import replace
        rows = RUNNER.load_scope(THEN)
        for inventory in (None, rows[:2], rows + [rows[0]],
                          [replace(rows[0], prompt='changed')] + rows[1:]):
            with self.subTest(inventory=inventory), \
                 patch.object(RUNNER, 'repo_root_from', return_value=THEN):
                with self.assertRaises(RUNNER.GuardError):
                    RUNNER.production_batch_paths(accounting_state=None,
                        spend_ledger=None, inventory_rows=inventory)

    def test_wrong_account_or_report_stops_before_archive_and_browser(self):
        rows = RUNNER.order_rows(RUNNER.load_scope(THEN))[:2]
        for overrides in ({'accounting_state': Path('/tmp/worktree/account')},
                          {'spend_ledger': Path('/tmp/worktree/report')}):
            with patch.object(RUNNER, 'require_archive') as archive, \
                 patch.object(RUNNER, 'live_video_submit') as submit:
                with self.assertRaises(RUNNER.GuardError):
                    RUNNER.execute_shared_batch(rows, media=Path('/unused'),
                        ledger_path=Path('/unused/ledger'), archive_dir=Path('/unused/archive'),
                        **overrides)
                archive.assert_not_called()
                submit.assert_not_called()


if __name__=='__main__': unittest.main()
