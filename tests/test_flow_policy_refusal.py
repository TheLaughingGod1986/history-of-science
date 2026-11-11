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


class RefusedTakeAlreadyInTheReportTests(unittest.TestCase):
    """The Halley take reached the spend report as 100 credits before it was reversed."""

    def spends(self, target: Path) -> list[dict]:
        return [r for r in (json.loads(l) for l in target.read_text().splitlines()) if r["kind"] == "spend"]

    def test_one_more_receipt_takes_it_back(self):
        for film in RUNNERS:
            with self.subTest(film=film), tempfile.TemporaryDirectory() as tmp:
                runner, root = load(film), Path(tmp)
                target = root / "spend.jsonl"
                charged_take(runner, root / "state", key="refused")
                with runner.SharedFlowAccounting(root / "state") as account:
                    self.assertEqual(account.export_ai_spend(target, by="codex"), 2)  # balance read + spend
                    first = target.read_bytes()
                    account.reverse_policy_refusal("refused", evidence=EVIDENCE)
                    self.assertEqual(account.export_ai_spend(target, by="codex"), 1)
                    again = target.read_bytes()
                    self.assertEqual(account.export_ai_spend(target, by="gemini"), 0)
                self.assertEqual(target.read_bytes(), again)
                self.assertTrue(again.startswith(first))      # the first receipt is not written over
                spends = self.spends(target)
                self.assertEqual([(r["id"], r["amount"]) for r in spends],
                                 [("flow:spend:refused", 100), ("flow:reversal:refused", -100)])
                self.assertEqual(sum(r["amount"] for r in spends), 0)
                self.assertEqual(spends[1]["film"], "HOS:009")

    def test_a_correction_entered_by_hand_is_not_made_twice(self):
        # The Chief's ruling lets the Mini correct the receipt with the ai_spend tool. If that
        # line names the charge, the export must not take the 100 back a second time.
        for film in RUNNERS:
            with self.subTest(film=film), tempfile.TemporaryDirectory() as tmp:
                runner, root = load(film), Path(tmp)
                target = root / "spend.jsonl"
                charged_take(runner, root / "state", key="HOS:009:P04:08_halley_visit_c1:t1")
                with runner.SharedFlowAccounting(root / "state") as account:
                    account.export_ai_spend(target, by="codex")
                    account.reverse_policy_refusal("HOS:009:P04:08_halley_visit_c1:t1", evidence=EVIDENCE)
                with target.open("a") as handle:   # what `ai_spend.py spend --amount -100 ...` appends
                    handle.write(json.dumps({"at": "2026-11-11T03:30:00Z", "kind": "spend", "pool": "flow",
                                             "amount": -100.0, "film": "HOS:009", "by": "gemini",
                                             "what": "HOS:009:P04:08_halley_visit_c1:t1 refused by Flow policy"}) + "\n")
                with runner.SharedFlowAccounting(root / "state") as account:
                    self.assertEqual(account.export_ai_spend(target, by="codex"), 0)
                self.assertEqual(sum(r["amount"] for r in self.spends(target)), 0)

    def test_every_runner_writes_the_same_receipt(self):
        # Each runner replays the shared ledger into the one report at the start of a batch.
        # A receipt that differed between them would stop the next one as an identity collision.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "spend.jsonl"
            charged_take(load("009"), root / "state", key="refused")
            with load("009").SharedFlowAccounting(root / "state") as account:
                account.export_ai_spend(target, by="codex")
                account.reverse_policy_refusal("refused", evidence=EVIDENCE)
            for film in ("013", "010", "009"):
                with self.subTest(film=film):
                    with load(film).SharedFlowAccounting(root / "state") as account:
                        account.export_ai_spend(target, by=film)
            self.assertEqual([r["amount"] for r in self.spends(target)], [100, -100])


class RetryAfterRefusalTests(unittest.TestCase):
    """The refused take left no file. Its retry must still be take 2."""

    def setUp(self):
        self.runner = load("009")

    def test_a_take_in_the_ledger_is_not_numbered_again(self):
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp)
            entries = [
                self.runner.submitting_record("08_halley_visit_c1", 4, 1, media / "x.mp4"),
                self.runner.policy_refusal_record("08_halley_visit_c1", 4, 1,
                                                  reason="Flow policy: prominent people", evidence=EVIDENCE),
                self.runner.submitting_record("08_halley_visit_c1", 5, 1, media / "y.mp4"),  # another part
            ]
            used = self.runner.takes_recorded(entries, 4, "08_halley_visit_c1")
            self.assertEqual(used, {1})
            take, dest = self.runner.next_version(media, 4, "08_halley_visit_c1", used)
            self.assertEqual((take, dest.name), (2, "08_halley_visit_c1_t2.mp4"))
            # Going by files alone, the retry would be t1 again.
            self.assertEqual(self.runner.next_version(media, 4, "08_halley_visit_c1")[0], 1)
            with self.assertRaises(self.runner.GuardError):
                self.runner.next_version(media, 4, "08_halley_visit_c1", {1, 2, 3})

    def test_the_batch_after_a_refusal_submits_take_two(self):
        import os
        import subprocess
        from unittest.mock import patch
        runner = self.runner
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger, state, archive = root / "ledger.jsonl", root / "shared", root / "archive"
            archive.mkdir()
            refused = "HOS:009:P02:10_how_high:t1"
            waiting = runner.submitting_record("10_how_high", 2, 1, root / "media" / "10_how_high_t1.mp4")
            waiting["shared_charge"] = refused
            runner.append_ledger(ledger, waiting)
            with runner.SharedFlowAccounting(state) as account:
                account.reserve("J2033", "HOS:009", runner.MAX_TOTAL_CREDITS, live=20000)
                account.intent(refused, "J2033", 100, live=20000)
                account.resolve(refused, submitted=True, evidence={"ui": {"balances": [20000]}})
            runner.reconcile_policy_refusal(
                accounting_state=state, ledger_path=ledger, lock_path=root / "writer.lock", key=refused,
                plate_id="10_how_high", part=2, take=1, reason="Flow policy: prominent people", evidence=EVIDENCE)
            charges = []

            def fake_still_maker(row, dest, *, accounting, reservation, evidence_path, other=0):
                dest.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=s=1280x720",
                                "-frames:v", "1", str(dest)], check=True)
                runner.immutable_bytes(evidence_path, b'{"credits":0,"ui":{"balances":[20000]}}\n')
                return dest

            def fake_submitter(row, dest, frame, *, accounting, reservation, charge, evidence_path, other=0):
                charges.append(charge)
                accounting.intent(charge, reservation, 100, live=20000)  # t1 again would stop here
                accounting.resolve(charge, submitted=True, evidence={"ui": {"balances": [20000]}})
                dest.write_bytes(b"fake video fixture")
                return {"charge": charge}

            with patch.dict(os.environ, {runner.SUBMIT_ENV: "1"}), patch.object(runner, "strip_audio"), \
                 patch.object(runner, "technical_report",
                              side_effect=lambda p, **kw: {"ok": True, "sha256": runner.sha256_file(p)}):
                written = runner.cmd_submit(
                    ROOT, other=0, media=root / "media", ledger_path=ledger, lock_path=root / "writer.lock",
                    pid_path=root / "runner.pid", done_path=root / "runner.done", archive_dir=archive,
                    accounting_state=state, spend_ledger=root / "spend.jsonl", submitter=fake_submitter,
                    still_maker=fake_still_maker, test_archive=True)
            self.assertEqual(charges, ["HOS:009:P02:10_how_high:t2", "HOS:009:P03:07_ball_to_moon:t1"])
            self.assertEqual([(e["plate_id"], e["take"]) for e in written], [("10_how_high", 2), ("07_ball_to_moon", 1)])
            latest = {(e["plate_id"], e["take"]): e["status"] for e in runner.read_ledger(ledger)}
            self.assertEqual(latest[("10_how_high", 1)], "FAILED_POLICY")   # the refusal still stands
            self.assertEqual(latest[("10_how_high", 2)], "PENDING_REVIEW")


class NoNameWordingTests(unittest.TestCase):
    """Chief rulings 6784284999, 6784299215 and 6785808071: the Halley plates describe the two men
    and name neither. The board changed, so the scope file's pinned hash changed with it."""

    EDIT = ROOT / "02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project"
    RECORD = ROOT / "jobs/reviews/J2033/PROMPT_CHANGE_2026-11-11.json"
    HALLEY_ROWS = ("08_halley_visit", "08_halley_visit_c1", "08_halley_visit_c2")
    YOUNG = "young astronomer of about twenty-eight, long dark natural hair, no wig, travelling coat"
    OLDER = "an older scholar of about forty-one, his own dark hair, no wig, plain dark coat"

    def setUp(self):
        self.runner = load("009")
        self.board = json.loads((self.EDIT / "parts/part-04_plates_v05.json").read_text())
        self.record = json.loads(self.RECORD.read_text())

    def test_the_tranche_still_loads_with_the_edited_board(self):
        rows = self.runner.load_scope(ROOT)
        self.assertEqual(len(rows), 20)
        halley = [r for r in rows if r.plate_id.startswith("08_halley_visit")]
        self.assertEqual([r.plate_id for r in halley], ["08_halley_visit_c1", "08_halley_visit_c2"])
        for row in halley:
            self.assertIn(self.YOUNG, row.prompt)
            self.assertIn(self.OLDER, row.prompt)

    def test_the_three_halley_prompts_name_nobody(self):
        prompts = {p["id"]: p["prompt"] for p in self.board["plates"] if p["id"] in self.HALLEY_ROWS}
        self.assertEqual(sorted(prompts), sorted(self.HALLEY_ROWS))
        for plate_id, prompt in prompts.items():
            with self.subTest(row=plate_id):
                for name in ("Halley", "Newton", "Edmond", "Isaac"):
                    self.assertNotIn(name, prompt)
                self.assertIn(self.YOUNG, prompt)
                self.assertIn(self.OLDER, prompt)

    def test_only_the_names_changed(self):
        prompts = {p["id"]: p["prompt"] for p in self.board["plates"]}
        for row in self.record["rows"]:
            with self.subTest(row=row["id"]):
                self.assertEqual(row["new"], prompts[row["id"]])
                self.assertEqual(row["new"], row["old"].replace(self.record["wording_old"], self.record["wording_new"]))
                self.assertEqual(row["old"].count(self.record["wording_old"]), 1)

    def test_the_record_and_the_scope_pin_the_board_as_it_is(self):
        digest = self.runner.sha256_file(self.EDIT / "parts/part-04_plates_v05.json")
        self.assertEqual(self.record["board_sha256_new"], digest)
        self.assertNotEqual(self.record["board_sha256_old"], digest)
        scope = json.loads((self.EDIT / "TRANCHE2_SCOPE_J2026.json").read_text())
        pinned = {r["id"]: r["board_sha256"] for r in scope["rows"] if r["board"].endswith("part-04_plates_v05.json")}
        self.assertEqual(sorted(pinned), sorted(self.record["scope_rows_repinned"]))
        self.assertEqual(set(pinned.values()), {digest})

    def test_no_row_still_to_be_made_names_a_real_person(self):
        still_to_make = {"08_halley_visit_c1", "08_halley_visit_c2", "04_comet_1758_c1",
                         "05_iss_orbit_c1", "05_iss_orbit_c2", "06_iss_apple_c1"}
        rows = [r for r in self.runner.load_scope(ROOT) if r.plate_id in still_to_make]
        self.assertEqual(len(rows), 6)
        for row in rows:
            with self.subTest(row=row.plate_id):
                for name in ("Halley", "Newton", "Edmond", "Isaac", "Hooke", "Wren", "Kepler", "Galileo", "Flamsteed"):
                    self.assertNotIn(name, row.prompt)


if __name__ == "__main__":
    unittest.main()
