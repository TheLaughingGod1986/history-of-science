"""HOS 010 R1-R6 Create-path wiring (J2271).

Offline only. These tests never open Chrome, never click Create, and spend 0 credits.
"""
from __future__ import annotations

import importlib.util
import inspect
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/07_Edit-Project/_mint_flow_r1_r6_plates_j2271.py"
SCOPE_SHA = "e3c802d2bffbbc80bd45f3ecc65b6c0a149de9886a0b38f6cbf8a1485f6c9874"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ADAPT = _load("hos010_r1_r6_runner", SCRIPT)


def _copy_scope(dest: Path, mutate=None) -> None:
    for rel in (ADAPT.SCOPE_REL, ADAPT.REVIEW_REL):
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        data = json.loads((ROOT / rel).read_text())
        if mutate is not None:
            mutate(rel, data)
        target.write_text(json.dumps(data))


def _auth_file(path: Path, repo: Path, **overrides) -> Path:
    payload = ADAPT.authorization_template(repo)
    payload.update(overrides)
    path.write_text(json.dumps(payload))
    return path


def _price():
    return {
        "Quality": ADAPT.base.PriceEvidence(
            quality="Quality",
            model="Veo 3.1 - Quality",
            outputs="x1",
            aspect="16:9",
            duration="8s",
            credits=100,
            generate_line="Generating will use 100 credits",
            read_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )
    }


class _Harness:
    def __init__(self, *, text="25050 AI credits\nGenerating will use 100 credits\nULTRA", balance=25050, disk=11 * 1024**3, submit=None):
        self.text = text
        self.balance = balance
        self.disk = disk
        self.calls = []
        self.balance_reads = 0
        self.price_reads = 0
        self._submit = submit

    def page_text(self):
        return self.text

    def live_balance(self):
        self.balance_reads += 1
        return self.balance

    def live_prices(self):
        self.price_reads += 1
        return _price()

    def disk_free(self):
        return self.disk

    def submit(self, row, dest, frame, *, accounting, reservation, charge, evidence_path, floor):
        if self._submit is not None:
            return self._submit(row, dest, frame, accounting=accounting, reservation=reservation, charge=charge, evidence_path=evidence_path, floor=floor)
        self.calls.append(charge)
        if not accounting.held:
            raise ADAPT.GuardError("lock was not held")
        if reservation != ADAPT.DEFAULT_RESERVATION:
            raise ADAPT.GuardError("wrong reservation")
        return {"charge": charge, "keep": False, "create_clicks": 0}


class R1R6CreatePathTests(unittest.TestCase):
    def test_scope_hash_is_the_go_pin_and_plan_submits_nothing(self):
        self.assertEqual(ADAPT.sha256_file(ROOT / ADAPT.SCOPE_REL), SCOPE_SHA)
        plan = ADAPT.build_r1_r6_plan(ROOT)
        self.assertEqual(plan["submissions"], 0)
        self.assertEqual(plan["create_clicks"], 0)
        self.assertEqual(plan["credits_spent"], 0)
        self.assertFalse(plan["keep"])
        self.assertEqual([row["charge_id"] for row in plan["named_charges"]], list(ADAPT.EXPECTED_NAMED_CHARGES))
        self.assertEqual(plan["reservation_id"], ADAPT.DEFAULT_RESERVATION)

    def test_source_reuses_guarded_create_and_does_not_click_or_load_the_twelve_plate_scope(self):
        text = SCRIPT.read_text()
        self.assertNotIn("mouse.click", text)
        self.assertNotIn("execute_shared_batch", text)
        self.assertNotIn("load_scope", text)
        live = inspect.getsource(ADAPT.live_named_charge_submit)
        self.assertIn("read_live_evidence", live)
        self.assertIn("open_overlay=True", live)
        self.assertIn("guarded_create", live)
        self.assertIn("generate_clip", live)
        self.assertNotIn("mouse.click", live)
        batch = inspect.getsource(ADAPT.execute_r1_r6_batch)
        self.assertNotIn("latest_recorded_flow_balance", batch)
        self.assertIn("live_balance", batch)
        self.assertIn("SharedFlowAccounting", batch)

    def test_ordinary_credit_text_is_not_a_cash_prompt(self):
        ADAPT.refuse_flow_banners("25050 AI credits\nGenerating will use 100 credits\nULTRA")
        ADAPT.refuse_flow_banners("This site is protected by recaptcha")
        for text in (
            "Buy credits to keep going",
            "Top up your balance",
            "Get extra credits",
            "Move to a paid tier",
        ):
            with self.subTest(text=text):
                with self.assertRaisesRegex(ADAPT.GuardError, "cash prompt"):
                    ADAPT.refuse_flow_banners(text)
        with self.assertRaisesRegex(ADAPT.GuardError, "unusual-activity"):
            ADAPT.refuse_flow_banners("unusual activity on this account")

    def test_empty_page_text_stops_before_create(self):
        for text in ("", "   ", "\n\t"):
            with self.subTest(text=repr(text)):
                with self.assertRaisesRegex(ADAPT.GuardError, "page text is empty"):
                    ADAPT.refuse_flow_banners(text)

    def test_submit_refuses_without_the_signed_file_even_if_the_scope_flag_is_flipped(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop(ADAPT.SUBMIT_ENV, None)
            with self.assertRaises(SystemExit):
                ADAPT.main(["submit", "--repo", str(ROOT), "--media", "/tmp/unused", "--archive", "/tmp/unused-archive"])

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            auth = Path(tmp) / "auth.json"

            def flip(rel, data):
                if rel == ADAPT.SCOPE_REL:
                    data["generation_authorized"] = True
                    for row in data["rows"]:
                        row["generation_authorized"] = True

            _copy_scope(repo, flip)
            with self.assertRaisesRegex(ADAPT.GuardError, "signed Chief authorization file"):
                ADAPT.require_signed_go(repo, None)

            def forbid(rel, data):
                if rel == ADAPT.SCOPE_REL:
                    data["reservation_id"] = "HOS010_TWELVE_PLATES_J2270"

            forbidden = Path(tmp) / "forbidden"
            _copy_scope(forbidden, forbid)
            with self.assertRaisesRegex(ADAPT.GuardError, "forbidden reservation"):
                ADAPT.load_r1_r6_scope(forbidden)

            def tamper(rel, data):
                if rel == ADAPT.SCOPE_REL:
                    data["rows"][0]["prompt"] = "tampered prompt"
                else:
                    for item in data["scoped_repairs_for_chief_authorization"]:
                        if item.get("repair_id") == "R1":
                            item["proposed_prompt"] = "tampered prompt"

            tampered = Path(tmp) / "tampered"
            _copy_scope(tampered, tamper)
            _auth_file(auth, ROOT)
            with self.assertRaisesRegex(ADAPT.GuardError, "authorization file failed validation"):
                ADAPT.require_signed_go(tampered, auth)

            outside = Path(tmp) / "signed.json"
            written = ADAPT.write_authorization_template(ROOT, outside)
            self.assertEqual(written["scope_sha256"], SCOPE_SHA)
            self.assertEqual(written["desk_comment"], ADAPT.GO_COMMENT)
            self.assertEqual(written["authorized_cap_credits"], 600)
            self.assertTrue(written["cash_stop"])
            auth_ok = ADAPT.require_signed_go(ROOT, outside)
            self.assertEqual(auth_ok["scope_sha256"], SCOPE_SHA)
            with self.assertRaisesRegex(ADAPT.GuardError, "inside the repo"):
                ADAPT.write_authorization_template(ROOT, ROOT / "10_Shorts" / "not-allowed.json")

            env = os.environ.copy()
            env[ADAPT.SUBMIT_ENV] = "1"
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "submit", "--repo", str(ROOT), "--media", tmp, "--archive", tmp],
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 2)
            self.assertIn("signed Chief authorization file", proc.stderr)
            self.assertNotIn("Traceback", proc.stderr)
            self.assertNotIn("Traceback", proc.stdout)

    def _run(self, root: Path, harness: _Harness, *, ledger=None, state=None):
        media = root / "media"
        archive = root / "archive"
        media.mkdir(parents=True, exist_ok=True)
        archive.mkdir(parents=True, exist_ok=True)
        ledger_path = ledger or (root / "ledger.jsonl")
        state_path = state or (root / "shared")
        state_path.mkdir(parents=True, exist_ok=True)
        auth = _auth_file(root / "auth.json", ROOT)
        with patch.dict(os.environ, {ADAPT.SUBMIT_ENV: "1"}):
            return ADAPT.execute_r1_r6_batch(
                ROOT,
                authorization_file=auth,
                media=media,
                archive_dir=archive,
                ledger_path=ledger_path,
                accounting_state=state_path,
                harness=harness,
                test_archive=True,
            )

    def test_cash_prompt_low_balance_full_disk_and_held_lock_spend_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cash = _Harness(text="Please buy credits to continue")
            with self.assertRaisesRegex(ADAPT.GuardError, "cash prompt"):
                self._run(root / "cash", cash)
            self.assertEqual(cash.balance_reads, 0)
            self.assertEqual(cash.calls, [])
            self.assertFalse((root / "cash" / "shared" / "account.jsonl").exists())

            low = _Harness(balance=3599)
            with self.assertRaisesRegex(ADAPT.GuardError, "live headroom"):
                self._run(root / "low", low)
            self.assertEqual(low.price_reads, 0)
            self.assertEqual(low.calls, [])
            self.assertFalse((root / "low" / "shared" / "account.jsonl").exists())

            full = _Harness(disk=ADAPT.MIN_DISK_FREE_BYTES)
            with self.assertRaisesRegex(ADAPT.GuardError, "10 GiB"):
                self._run(root / "disk", full)
            self.assertEqual(full.balance_reads, 0)
            self.assertFalse((root / "disk" / "shared" / "writer.lock").exists())

            locked = root / "locked"
            state = locked / "shared"
            state.mkdir(parents=True)
            harness = _Harness()
            with ADAPT.base.WriterLock(state / "writer.lock"):
                with self.assertRaisesRegex(ADAPT.GuardError, "writer lock held"):
                    self._run(locked, harness, state=state)
            self.assertEqual(harness.calls, [])

    def test_forbidden_reservation_and_pending_charge_stop_before_create(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "shared"
            with ADAPT.SharedFlowAccounting(state) as accounting:
                accounting.reserve("HOS010_TWELVE_PLATES_J2270", "HOS:010", 3600, live=30000, floor=3000)
            harness = _Harness()
            with self.assertRaisesRegex(ADAPT.GuardError, "forbidden prior reservation"):
                self._run(root, harness, state=state)
            self.assertEqual(harness.balance_reads, 0)
            self.assertNotIn(ADAPT.DEFAULT_RESERVATION, (state / "account.jsonl").read_text())

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "shared"
            with ADAPT.SharedFlowAccounting(state) as accounting:
                accounting.reserve(ADAPT.DEFAULT_RESERVATION, "HOS:010", 600, live=30000, floor=3000)
                accounting.intent(ADAPT.EXPECTED_NAMED_CHARGES[0], ADAPT.DEFAULT_RESERVATION, 100, live=30000, floor=3000)
            before = (state / "account.jsonl").read_bytes()
            harness = _Harness()
            with self.assertRaisesRegex(ADAPT.GuardError, "unresolved shared Create"):
                self._run(root, harness, state=state)
            self.assertEqual((state / "account.jsonl").read_bytes(), before)
            self.assertEqual(harness.calls, [])

    def test_named_charges_run_as_batch_1_then_r6_and_never_keep(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            harness = _Harness()
            first = self._run(root, harness)
            self.assertEqual(harness.calls, list(ADAPT.EXPECTED_NAMED_CHARGES[:5]))
            self.assertTrue(all(row["keep"] is False and row["take"] == 2 for row in first))
            sample = ADAPT.to_base_row(ADAPT.load_r1_r6_scope(ROOT)[1][0])
            output = ADAPT.r1_r6_output(root / "media", sample)
            self.assertIn("v02_r1_r6_plates", str(output))
            self.assertNotIn("v01_twelve_plates", str(output))
            self.assertTrue(str(output).endswith("_t2.mp4"))
            still = ADAPT.r1_r6_still_path(root / "media", sample)
            self.assertIn("v02_r1_r6_plates_stills", str(still))
            self.assertNotIn("v01_twelve_plates_stills", str(still))
            self.assertTrue(str(still).endswith("_t2.png"))

            second = self._run(root, harness, ledger=root / "ledger.jsonl", state=root / "shared")
            self.assertEqual(second[0]["charge_id"], ADAPT.EXPECTED_NAMED_CHARGES[5])
            self.assertEqual(harness.calls, list(ADAPT.EXPECTED_NAMED_CHARGES))
            ledger = (root / "ledger.jsonl").read_text()
            self.assertNotIn('"keep": true', ledger)
            self.assertEqual(ledger.count('"keep": false'), 6)
            account = (root / "shared" / "account.jsonl").read_text()
            self.assertIn(ADAPT.DEFAULT_RESERVATION, account)
            self.assertNotIn("HOS010_TWELVE_PLATES_J2270", account)

            def keep_true(row, dest, frame, *, accounting, reservation, charge, evidence_path, floor):
                return {"charge": charge, "keep": True}

            kept = _Harness(submit=keep_true)
            with self.assertRaisesRegex(ADAPT.GuardError, "keep false"):
                self._run(Path(tmp) / "keep", kept)
            self.assertFalse((Path(tmp) / "keep" / "ledger.jsonl").exists())

    def test_default_submit_reaches_the_live_session_and_does_not_open_it_here(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            auth = _auth_file(root / "auth.json", ROOT)
            reached = {"n": 0}

            def boom(*_args, **_kwargs):
                reached["n"] += 1
                raise ADAPT.GuardError("live session reached")

            with patch.dict(os.environ, {ADAPT.SUBMIT_ENV: "1"}):
                with patch.object(ADAPT, "live_batch_session", boom):
                    with self.assertRaisesRegex(ADAPT.GuardError, "live session reached"):
                        ADAPT.cmd_submit(
                            ROOT,
                            authorization_file=auth,
                            media=root / "media",
                            archive_dir=root / "archive",
                            ledger_path=root / "ledger.jsonl",
                        )
            self.assertEqual(reached["n"], 1)

    def test_an_existing_t2_file_is_a_second_take_and_dry_run_spends_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            media = root / "media"
            row = ADAPT.to_base_row(ADAPT.load_r1_r6_scope(ROOT)[1][0])
            dest = ADAPT.r1_r6_output(media, row)
            dest.parent.mkdir(parents=True)
            dest.write_bytes(b"already there")
            harness = _Harness()
            with self.assertRaisesRegex(ADAPT.GuardError, "second take"):
                self._run(root, harness)
            self.assertEqual(harness.calls, [])

            state = root / "dry-shared"
            state.mkdir()
            with patch.object(ADAPT, "verify_nas_volume_mounted", side_effect=lambda path: Path(path)), patch.object(
                ADAPT, "verify_style_references", return_value={"house": [], "explorer": None, "staged": False}
            ):
                report = ADAPT.build_r1_r6_dry_run_report(
                    ROOT,
                    media=media,
                    accounting_state=state,
                    spend_ledger=root / "spend.jsonl",
                )
            self.assertEqual(report["submissions"], 0)
            self.assertEqual(report["create_clicks"], 0)
            self.assertEqual(report["credits_spent"], 0)
            self.assertFalse((state / "account.jsonl").exists())

    def test_live_named_charge_submit_opens_settings_overlay_before_guarded_create_and_reconciles(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "shared"
            frame = root / "start.png"
            frame.write_bytes(b"png")
            dest = root / "out" / "P02_05_almost_none_t2.mp4"
            row = ADAPT.to_base_row(ADAPT.load_r1_r6_scope(ROOT)[1][0])
            charge = ADAPT.EXPECTED_NAMED_CHARGES[0]
            order = []
            balances = iter([25050, 24950])

            class FakePage:
                class _Loc:
                    def inner_text(self, timeout=8000):
                        return "25050 AI credits\nGenerating will use 100 credits\nULTRA"

                def locator(self, _sel):
                    return self._Loc()

            fake_page = FakePage()

            def fake_balance(_page):
                order.append("read_live_balance")
                return next(balances)

            def fake_evidence(_page, *, quality, balance, open_overlay=False):
                order.append(("read_live_evidence", quality, balance, open_overlay))
                return {"balances": [balance]}

            def fake_guarded_create(_page, acc, *, row, reservation, charge, evidence_path, floor, balance):
                order.append(("guarded_create", charge, balance))
                acc.intent(charge, reservation, 100, live=balance, floor=floor)
                acc.resolve(charge, submitted=True, evidence={"ui": {"balances": [balance]}})
                return {"charge": charge, "ui": {"balances": [balance]}}

            class FakeFlow:
                @staticmethod
                def generate_clip(page, _prompt, _dest, *, create_guard, **_kwargs):
                    order.append("generate_clip")
                    create_guard(page)

            with patch.dict(os.environ, {ADAPT.SUBMIT_ENV: "1"}), patch.dict(
                sys.modules, {"orbit_flow_veo_ui": FakeFlow}
            ), patch.object(ADAPT.base, "read_live_balance", side_effect=fake_balance), patch.object(
                ADAPT.base, "read_live_evidence", side_effect=fake_evidence
            ), patch.object(ADAPT.base, "guarded_create", side_effect=fake_guarded_create):
                with ADAPT.SharedFlowAccounting(state) as accounting:
                    accounting.reserve(ADAPT.DEFAULT_RESERVATION, "HOS:010", 600, live=25050, floor=3000)
                    result = ADAPT.live_named_charge_submit(
                        row,
                        dest,
                        frame,
                        accounting=accounting,
                        reservation=ADAPT.DEFAULT_RESERVATION,
                        charge=charge,
                        evidence_path=root / "R1.create.json",
                        floor=3000,
                        page=fake_page,
                    )
                    snap = accounting.snapshot()

            self.assertEqual(
                order,
                [
                    "generate_clip",
                    "read_live_balance",
                    ("read_live_evidence", "Quality", 25050, True),
                    ("guarded_create", charge, 25050),
                    "read_live_balance",
                ],
            )
            self.assertEqual(result["charge"], charge)
            self.assertFalse(result["keep"])
            self.assertTrue(snap["charges"][charge]["posted"])

            with ADAPT.SharedFlowAccounting(state) as accounting:
                v01_frame = root / "v01_twelve_plates_stills" / "P02_05_almost_none_t1.png"
                with patch.dict(os.environ, {ADAPT.SUBMIT_ENV: "1"}):
                    with self.assertRaisesRegex(ADAPT.GuardError, "refusing to reuse v01 t1 start still"):
                        ADAPT.live_named_charge_submit(
                            row,
                            dest,
                            v01_frame,
                            accounting=accounting,
                            reservation=ADAPT.DEFAULT_RESERVATION,
                            charge=charge,
                            evidence_path=root / "R1.v01.create.json",
                            floor=3000,
                            page=fake_page,
                        )

                missing_frame = root / "v02_r1_r6_plates_stills" / "P02_05_almost_none_t2.png"
                minted_calls = []

                def fake_ensure(r, f, **kw):
                    minted_calls.append((r.row_id, f, kw["still_evidence_path"].name))
                    f.parent.mkdir(parents=True, exist_ok=True)
                    f.write_bytes(b"png2")
                    return f

                balances2 = iter([24950, 24850])
                charge2 = ADAPT.EXPECTED_NAMED_CHARGES[1]
                row2 = ADAPT.to_base_row(ADAPT.load_r1_r6_scope(ROOT)[1][1])
                with patch.dict(os.environ, {ADAPT.SUBMIT_ENV: "1"}), patch.dict(
                    sys.modules, {"orbit_flow_veo_ui": FakeFlow}
                ), patch.object(ADAPT, "ensure_r1_r6_start_still", side_effect=fake_ensure), patch.object(
                    ADAPT.base, "read_live_balance", side_effect=lambda _p: next(balances2)
                ), patch.object(ADAPT.base, "read_live_evidence", side_effect=fake_evidence), patch.object(
                    ADAPT.base, "guarded_create", side_effect=fake_guarded_create
                ):
                    ADAPT.live_named_charge_submit(
                        row2,
                        root / "out" / "P04_06_dust_veil_t2.mp4",
                        missing_frame,
                        accounting=accounting,
                        reservation=ADAPT.DEFAULT_RESERVATION,
                        charge=charge2,
                        evidence_path=root / "R2.create.json",
                        floor=3000,
                        page=fake_page,
                    )
                self.assertEqual(minted_calls, [(row2.row_id, missing_frame, "R2.still.create.json")])


if __name__ == "__main__":
    unittest.main()
