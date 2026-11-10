"""Replay real shared-account events into temporary report ledgers; no browser."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tests.test_hos009_tranche2_runner import RUNNER


class SpendExportTests(unittest.TestCase):
    def charge(self, account, key='take1', submitted=True):
        account.reserve('job', 'HOS:009', 6000, live=10000)
        account.intent(key, 'job', 100, live=10000)
        account.resolve(key, submitted=submitted,
                        evidence={'ui': {'balances': [10000], 'account': 'private-fixture'},
                                  'read_at': 'fixture'})

    def test_replay_records_reading_and_spend_once_without_releasing_liability(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); target=root/'report.jsonl'
            # Old ai_spend records without IDs remain valid.
            target.write_text(json.dumps({'kind':'record','pool':'flow','left':12000})+'\n')
            with RUNNER.SharedFlowAccounting(root/'state') as account:
                self.charge(account)
                before=account.snapshot()
                self.assertEqual(account.export_ai_spend(target,by='codex'),2)
                self.assertEqual(account.export_ai_spend(target,by='gemini'),0)
                self.assertEqual(account.snapshot(),before)
            text=target.read_text(); self.assertNotIn('private-fixture',text)
            rows=[json.loads(line) for line in text.splitlines()]
            self.assertEqual([r['kind'] for r in rows],['record','record','spend'])
            self.assertEqual(rows[-1]['amount'],100)
            self.assertEqual(rows[-1]['film'],'HOS:009')
            with RUNNER.SharedFlowAccounting(root/'state') as recovered:
                self.assertEqual(recovered.export_ai_spend(target,by='codex'),0)

    def test_pending_and_not_submitted_never_become_confirmed_spend(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); target=root/'report.jsonl'
            with RUNNER.SharedFlowAccounting(root/'state') as account:
                self.charge(account,submitted=False)
                account.intent('unknown','job',100,live=10000)
                self.assertEqual(account.export_ai_spend(target,by='codex'),0)
                self.assertFalse(target.exists())
                self.assertTrue(account.snapshot()['pending'])

    def test_crash_after_write_replays_without_duplicate_or_lost_charge(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); target=root/'report.jsonl'
            with RUNNER.SharedFlowAccounting(root/'state') as account:
                self.charge(account)
                with patch.object(RUNNER.os,'fsync',side_effect=OSError('crash after append')):
                    with self.assertRaises(OSError): account.export_ai_spend(target,by='codex')
                self.assertEqual(account.export_ai_spend(target,by='codex'),0)
                self.assertEqual(len(target.read_text().splitlines()),2)
                self.assertEqual(account.snapshot()['liability'],6000)

    def test_collision_corrupt_and_duplicate_destinations_fail_without_append(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); target=root/'report.jsonl'
            with RUNNER.SharedFlowAccounting(root/'state') as account:
                self.charge(account)
                fixtures=[b'{',b'null\n',b'{bad}\n',
                    b'{"id":"flow:spend:take1","amount":999}\n',
                    b'{"id":"same"}\n{"id":"same"}\n']
                for data in fixtures:
                    target.write_bytes(data)
                    with self.assertRaises(RUNNER.GuardError): account.export_ai_spend(target,by='codex')
                    self.assertEqual(target.read_bytes(),data)
                with self.assertRaises(RUNNER.GuardError): account.export_ai_spend(account.path,by='codex')
                with self.assertRaises(RUNNER.GuardError): account.export_ai_spend(target,by='')

    def test_export_requires_account_and_destination_locks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); target=root/'report.jsonl'
            account=RUNNER.SharedFlowAccounting(root/'state')
            with self.assertRaises(RUNNER.GuardError): account.export_ai_spend(target,by='codex')
            with account:
                self.charge(account)
                with RUNNER.WriterLock(target.with_name(target.name+'.lock')):
                    with self.assertRaises(RUNNER.GuardError): account.export_ai_spend(target,by='codex')
                self.assertFalse(target.exists())


if __name__=='__main__': unittest.main()
