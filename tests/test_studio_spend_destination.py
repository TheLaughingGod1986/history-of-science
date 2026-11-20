"""Offline migration boundary for all standalone shared Flow exporters."""
import ast
import importlib.util
import inspect
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
RUNNERS = []
for prefix, filename in [('009_*', '_mint_flow_v05_tranche2.py'),
                         ('010_*', '_mint_flow_twelve_plates_j2268.py'),
                         ('013_*', '_mint_flow_v01_pass1.py')]:
    path = next(ROOT.glob('02_Video-Projects/' + prefix + '/07_Edit-Project/' + filename))
    name = 'spend_cutover_' + prefix[:3]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    RUNNERS.append(module)


class SpendDestination(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.home = self.root / 'home'
        self.marker = self.home / '_desk/state/active-studio.json'
        self.marker.parent.mkdir(parents=True)
        self.patch = patch.object(Path, 'home', return_value=self.home)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def arm(self, raw=None):
        self.marker.write_text(raw if raw is not None else json.dumps(
            {'version': 1, 'github': 'test/active'}))

    def ledger(self, name, identity):
        engine = self.root / name
        (engine / 'channels').mkdir(parents=True)
        (engine / 'channels/channels.json').write_text(json.dumps(
            {'studio': {'github': identity}}))
        return engine / '05_Analytics/ai_spend/ledger.jsonl'

    def test_standalone_boundaries_remain_identical(self):
        for name in ('active_spend_repository', 'require_active_spend_destination', 'canonical_spend_ledger'):
            sources = [ast.dump(ast.parse(inspect.getsource(getattr(m, name)))) for m in RUNNERS]
            self.assertEqual(len(set(sources)), 1)

    def test_unarmed_preserves_legacy_path_and_arbitrary_offline_export_target(self):
        for m in RUNNERS:
            with self.subTest(runner=m.__name__), patch.dict(os.environ, {'STUDIO_REPO': '/ignored'}):
                self.assertEqual(m.canonical_spend_ledger(), self.home / 'YouTube/orbit-with-ben/05_Analytics/ai_spend/ledger.jsonl')
                m.require_active_spend_destination(self.root / 'fixture.jsonl')

    def test_armed_selects_validated_engine_and_rejects_old_alias_or_unknown_roots(self):
        self.arm()
        active = self.ledger('active', 'test/active')
        retired = self.ledger('retired', 'test/retired')
        alias = self.root / 'alias'
        alias.symlink_to(retired.parents[2], target_is_directory=True)
        for m in RUNNERS:
            with self.subTest(runner=m.__name__), patch.dict(os.environ, {'STUDIO_REPO': str(active.parents[2])}):
                self.assertEqual(m.canonical_spend_ledger(), active)
                for bad in (retired, self.root / 'unknown.jsonl', alias / '05_Analytics/ai_spend/ledger.jsonl'):
                    with self.assertRaises(m.GuardError):
                        m.require_active_spend_destination(bad)
                with patch.dict(os.environ, {'STUDIO_REPO': 'relative'}):
                    with self.assertRaises(m.GuardError): m.canonical_spend_ledger()
        self.assertFalse(active.parent.exists())
        self.assertFalse(retired.parent.exists())

    def test_invalid_marker_or_registry_refuses_without_echoing_values(self):
        active = self.ledger('active', 'test/active')
        for m in RUNNERS:
            for raw in ('private-fixture', '[]', '{}', '{"version": 2, "github": "test/active"}'):
                self.arm(raw)
                with self.assertRaises(m.GuardError) as caught:
                    m.require_active_spend_destination(active)
                self.assertNotIn('private-fixture', str(caught.exception))
            self.arm()
            registry = active.parents[2] / 'channels/channels.json'
            registry.write_text('private-fixture')
            with self.assertRaises(m.GuardError): m.require_active_spend_destination(active)

    def test_direct_exports_preserve_old_ledger_and_replay_once_into_active(self):
        retired = self.ledger('retired', 'test/retired')
        retired.parent.mkdir(parents=True)
        retired.write_text('{"kind":"record","pool":"flow","left":10000}\n')
        original = retired.read_bytes()
        active = self.ledger('active', 'test/active')
        self.arm()
        for index, m in enumerate(RUNNERS):
            with self.subTest(runner=m.__name__), m.SharedFlowAccounting(self.root / ('account' + str(index))) as account:
                key = 'take' + str(index)
                account.reserve('job', 'HOS:009', 6000, live=10000)
                account.intent(key, 'job', 100, live=10000)
                account.resolve(key, submitted=True, evidence={'ui': {'balances': [10000]}, 'read_at': 'fixture'})
                before = account.snapshot()
                with self.assertRaises(m.GuardError): account.export_ai_spend(retired, by='codex')
                self.assertEqual(retired.read_bytes(), original)
                self.assertFalse(retired.with_name('ledger.jsonl.lock').exists())
                self.assertEqual(account.snapshot(), before)
                self.assertEqual(account.export_ai_spend(active, by='codex'), 2)
                self.assertEqual(account.export_ai_spend(active, by='codex'), 0)
                self.assertEqual(account.snapshot(), before)
        self.assertEqual(len(active.read_text().splitlines()), 6)


if __name__ == '__main__':
    unittest.main()
