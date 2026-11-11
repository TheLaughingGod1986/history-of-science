"""Zero-cost reversal for a Flow take refused under Flow's content policy.

J2033, 11 Nov 2026: P04:08_halley_visit_c1:t1 was refused ("generating prominent
people") and charged nothing (14,890 - 13,490 = 14 outputs x 100), but the shared
ledger held it as CHARGED 100 with no supported way back to 0. These tests never
touch Flow.
"""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNERS = {
    "009": ROOT / "02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/_mint_flow_v05_tranche2.py",
    "010": ROOT / "02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/07_Edit-Project/_mint_flow_twelve_plates_j2268.py",
    "013": ROOT / "02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project/_mint_flow_v01_pass1.py",
}
EVIDENCE = {"desk": "HOS #180 6784299215", "balance_before": 14890, "balance_live": 13490, "outputs": 14}


def load(film: str):
    name = f"policy_refusal_runner_{film}"
    if name in sys.modules:
        return sys.modules[name]
    path = RUNNERS[film]
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def charged_take(runner, state: Path, key: str = "take1") -> None:
    with runner.SharedFlowAccounting(state) as account:
        account.reserve("J2033", "HOS:009", 600, live=20000)
        account.intent(key, "J2033", 100, live=20000)
        account.resolve(key, submitted=True, evidence={"ui": {"balances": [14190]}})


class SharedReversalTests(unittest.TestCase):
    """The same rules hold in every runner that reads the shared Flow ledger."""

    def test_charged_take_reverses_to_zero_net(self):
        for film in RUNNERS:
            with self.subTest(film=film), tempfile.TemporaryDirectory() as tmp:
                runner, state = load(film), Path(tmp)
                charged_take(runner, state)
                with runner.SharedFlowAccounting(state) as account:
                    before = account.snapshot()
                    self.assertEqual(before["charges"]["take1"]["status"], "CHARGED")
                    self.assertEqual(before["liability"], 600)  # 100 unposted + 500 unused cap
                    self.assertTrue(account.reverse_policy_refusal("take1", evidence=EVIDENCE))
                    after = account.snapshot()
                self.assertEqual(after["charges"]["take1"]["status"], "POLICY_REFUSED")
                self.assertEqual(after["charges"]["take1"]["amount"], 0)
                self.assertEqual(after["liability"], 600)  # the 100 returns to unused cap
                self.assertFalse(after["pending"])

    def test_rerun_is_idempotent_and_appends_once(self):
        for film in RUNNERS:
            with self.subTest(film=film), tempfile.TemporaryDirectory() as tmp:
                runner, state = load(film), Path(tmp)
                charged_take(runner, state)
                with runner.SharedFlowAccounting(state) as account:
                    self.assertTrue(account.reverse_policy_refusal("take1", evidence=EVIDENCE))
                    lines = account.path.read_text().splitlines()
                    self.assertFalse(account.reverse_policy_refusal("take1", evidence=EVIDENCE))
                    self.assertEqual(account.path.read_text().splitlines(), lines)
                self.assertEqual(sum(json.loads(l)["kind"] == "policy_refused" for l in lines), 1)

    def test_history_is_appended_never_rewritten(self):
        for film in RUNNERS:
            with self.subTest(film=film), tempfile.TemporaryDirectory() as tmp:
                runner, state = load(film), Path(tmp)
                charged_take(runner, state)
                path = state / "account.jsonl"
                before = path.read_text()
                with runner.SharedFlowAccounting(state) as account:
                    account.reverse_policy_refusal("take1", evidence=EVIDENCE)
                self.assertTrue(path.read_text().startswith(before))

    def test_refuses_pending_posted_unknown_or_unevidenced(self):
        for film in RUNNERS:
            with self.subTest(film=film), tempfile.TemporaryDirectory() as tmp:
                runner, state = load(film), Path(tmp)
                with runner.SharedFlowAccounting(state) as account:
                    account.reserve("J2033", "HOS:009", 600, live=20000)
                    account.intent("pending", "J2033", 100, live=20000)
                    with self.assertRaises(runner.GuardError):
                        account.reverse_policy_refusal("pending", evidence=EVIDENCE)
                    account.resolve("pending", submitted=True, evidence={"ui": {}})
                    with self.assertRaises(runner.GuardError):
                        account.reverse_policy_refusal("pending", evidence={})
                    with self.assertRaises(runner.GuardError):
                        account.reverse_policy_refusal("missing", evidence=EVIDENCE)
                    account.reconcile_posted("pending", evidence={"balance": 13490})
                    with self.assertRaises(runner.GuardError):
                        account.reverse_policy_refusal("pending", evidence=EVIDENCE)

    def test_hand_written_reversal_of_posted_charge_blocks_every_reader(self):
        for film in RUNNERS:
            with self.subTest(film=film), tempfile.TemporaryDirectory() as tmp:
                runner, state = load(film), Path(tmp)
                charged_take(runner, state)
                with runner.SharedFlowAccounting(state) as account:
                    account.reconcile_posted("take1", evidence={"balance": 13490})
                with (state / "account.jsonl").open("a") as handle:
                    handle.write(json.dumps({"kind": "policy_refused", "id": "take1",
                                             "evidence": EVIDENCE, "at": "x"}) + "\n")
                with self.assertRaises(runner.GuardError):
                    with runner.SharedFlowAccounting(state):
                        pass

    def test_every_runner_reads_a_ledger_written_by_another(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            writer = load("009")
            charged_take(writer, state)
            with writer.SharedFlowAccounting(state) as account:
                account.reverse_policy_refusal("take1", evidence=EVIDENCE)
            for film in ("010", "013"):
                with self.subTest(film=film):
                    runner = load(film)
                    with runner.SharedFlowAccounting(state) as account:
                        self.assertEqual(account.snapshot()["charges"]["take1"]["status"], "POLICY_REFUSED")

    def test_spend_export_skips_reversed_take(self):
        for film in RUNNERS:
            with self.subTest(film=film), tempfile.TemporaryDirectory() as tmp:
                runner, root = load(film), Path(tmp)
                charged_take(runner, root / "state", key="refused")
                with runner.SharedFlowAccounting(root / "state") as account:
                    account.intent("delivered", "J2033", 100, live=20000)
                    account.resolve("delivered", submitted=True, evidence={"ui": {"balances": [14090]}})
                    account.reverse_policy_refusal("refused", evidence=EVIDENCE)
                    account.export_ai_spend(root / "spend.jsonl", by="test")
                rows = [json.loads(l) for l in (root / "spend.jsonl").read_text().splitlines()]
                spends = [r for r in rows if r["kind"] == "spend"]
                self.assertEqual([r["charge"] for r in spends], ["delivered"])


class TrancheLedgerTests(unittest.TestCase):
    def setUp(self):
        self.runner = load("009")

    def test_failed_policy_counts_zero_and_keeps_the_take(self):
        entries = [
            self.runner.submitting_record("08_halley_visit_c1", 4, 1, Path("x.mp4")),
            self.runner.policy_refusal_record("08_halley_visit_c1", 4, 1,
                                              reason="Flow policy: prominent people", evidence=EVIDENCE),
        ]
        spent, pending, unknown, takes = self.runner.ledger_totals(entries)
        self.assertEqual((spent, pending, unknown), (0, 0, False))
        self.assertEqual(takes["08_halley_visit_c1"], 1)  # t2 is the next and only retry

    def test_failed_policy_needs_zero_credits_and_a_reason(self):
        base = self.runner.policy_refusal_record("p", 4, 1, reason="policy", evidence=EVIDENCE)
        for bad in ({"credits_used": 100}, {"credits_used": None}, {"credits_used": False}, {"reason": " "}):
            with self.subTest(bad=bad):
                with self.assertRaises(self.runner.GuardError):
                    self.runner.ledger_totals([{**base, **bad}])
        with self.assertRaises(self.runner.GuardError):
            self.runner.policy_refusal_record("p", 4, 1, reason="", evidence=EVIDENCE)

    def test_reconcile_both_ledgers_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger = root / "ledger.jsonl"
            self.runner.append_ledger(ledger, self.runner.submitting_record("08_halley_visit_c1", 4, 1, root / "x.mp4"))
            charged_take(self.runner, root / "state", key="HOS:009:P04:08_halley_visit_c1:t1")
            kwargs = dict(accounting_state=root / "state", ledger_path=ledger, lock_path=root / "writer.lock",
                          key="HOS:009:P04:08_halley_visit_c1:t1", plate_id="08_halley_visit_c1", part=4, take=1,
                          reason="Flow policy: prominent people", evidence=EVIDENCE)
            self.assertEqual(self.runner.reconcile_policy_refusal(**kwargs),
                             {"shared_appended": True, "tranche_appended": True})
            self.assertEqual(self.runner.reconcile_policy_refusal(**kwargs),
                             {"shared_appended": False, "tranche_appended": False})
            entries = self.runner.read_ledger(ledger)
            self.assertEqual([e["status"] for e in entries], ["SUBMITTING", "FAILED_POLICY"])
            self.assertEqual(self.runner.ledger_totals(entries)[:3], (0, 0, False))

    def test_reconcile_refuses_a_delivered_take(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger = root / "ledger.jsonl"
            self.runner.append_ledger(ledger, {**self.runner.submitting_record("p", 4, 1, root / "x.mp4"),
                                               "status": "PENDING_REVIEW", "credits_used": 100})
            charged_take(self.runner, root / "state", key="k")
            with self.assertRaises(self.runner.GuardError):
                self.runner.reconcile_policy_refusal(
                    accounting_state=root / "state", ledger_path=ledger, lock_path=root / "writer.lock",
                    key="k", plate_id="p", part=4, take=1, reason="policy", evidence=EVIDENCE)
            with self.runner.SharedFlowAccounting(root / "state") as account:
                self.assertEqual(account.snapshot()["charges"]["k"]["status"], "CHARGED")


if __name__ == "__main__":
    unittest.main()
