"""Unit tests for Google Flow post-5 Dec 2026 model lineup in orbit_flow_veo_ui.py.

Covers Veo 3.1 - Lite, Veo 3.1 - Lite [Lower Priority], Omni 1.2 Flash (opt-in),
exact dropdown label matching (preventing Lite vs Lite [Lower Priority] collisions),
Omni 1.2 Flash 720p + Length slider controls, credit estimation, and CLI --dry-run.
Never opens Chrome/CDP and spends 0 credits.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "04_Audio/tools/orbit_flow_veo_ui.py"


def load_tool():
    name = "orbit_flow_veo_ui_lineup_test"
    if name in sys.modules:
        return sys.modules[name]
    sys.path.insert(0, str(TOOL_PATH.parent))
    spec = importlib.util.spec_from_file_location(name, TOOL_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


class FakeLocator:
    def __init__(self, text: str | None = None):
        self._text = text
        self.clicks = 0

    def count(self) -> int:
        return 1 if self._text is not None else 0

    def filter(self, **_kwargs):
        return self

    @property
    def last(self):
        return self

    def inner_text(self) -> str:
        return self._text or ""

    def click(self, **_kwargs) -> None:
        self.clicks += 1


class FlowModelResolutionTests(unittest.TestCase):
    def setUp(self):
        self.tool = load_tool()

    def test_default_stays_safe_pre_cutover(self):
        self.assertEqual(self.tool.MODEL_VEO_QUALITY, "Veo 3.1 - Quality")
        self.assertEqual(self.tool.POST_CUTOVER_DEFAULT_MODEL, "Veo 3.1 - Lite")
        self.assertEqual(self.tool.FLOW_CUTOVER_DATE, "2026-12-05")
        self.assertTrue(self.tool.is_retired_model("Veo 3.1 - Quality"))
        self.assertTrue(self.tool.is_retired_model("Veo 3.1 - Fast"))
        self.assertTrue(self.tool.is_retired_model("Omni 1.1 Flash"))
        self.assertFalse(self.tool.is_retired_model("Veo 3.1 - Lite"))
        self.assertFalse(self.tool.is_retired_model("Veo 3.1 - Lite [Lower Priority]"))
        self.assertFalse(self.tool.is_retired_model("Omni 1.2 Flash"))

    def test_veo3_models_and_aliases_resolve_cleanly(self):
        self.assertEqual(self.tool.resolve_flow_model("lite"), "Veo 3.1 - Lite")
        self.assertEqual(
            self.tool.resolve_flow_model("lite", lower_priority=True),
            "Veo 3.1 - Lite [Lower Priority]",
        )
        self.assertEqual(
            self.tool.resolve_flow_model("lite-lp"),
            "Veo 3.1 - Lite [Lower Priority]",
        )
        self.assertEqual(
            self.tool.resolve_flow_model("Veo 3.1 - Lite [Lower Priority]"),
            "Veo 3.1 - Lite [Lower Priority]",
        )
        self.assertEqual(
            self.tool.resolve_flow_model("Veo 3.1 - Fast\nLeaving 5 Dec"),
            "Veo 3.1 - Fast",
        )
        self.assertEqual(
            self.tool.resolve_flow_model("Veo 3.1 - Quality | Leaving 5 Dec"),
            "Veo 3.1 - Quality",
        )

    def test_lower_priority_rejected_for_non_lite_models(self):
        for bad in ("Veo 3.1 - Quality", "Veo 3.1 - Fast", "Omni 1.2 Flash"):
            with self.subTest(model=bad):
                with self.assertRaises(RuntimeError):
                    self.tool.resolve_flow_model(
                        bad, lower_priority=True, allow_omni_1_2=True
                    )

    def test_omni_1_2_requires_explicit_opt_in_and_retired_models_always_refused(self):
        with self.assertRaises(RuntimeError):
            self.tool.resolve_flow_model("Omni 1.2 Flash")
        self.assertEqual(
            self.tool.resolve_flow_model("Omni 1.2 Flash", allow_omni_1_2=True),
            "Omni 1.2 Flash",
        )
        self.assertEqual(
            self.tool.resolve_flow_model("Omni Flash 1.2", allow_omni_1_2=True),
            "Omni 1.2 Flash",
        )
        self.assertEqual(
            self.tool.resolve_flow_model("omni-1.2", allow_omni_1_2=True),
            "Omni 1.2 Flash",
        )
        for forbidden in ("Omni 1.1 Flash", "Omni Flash", "Nano Banana", "Nano Banana 2"):
            with self.subTest(forbidden=forbidden):
                with self.assertRaises(RuntimeError):
                    self.tool.resolve_flow_model(forbidden, allow_omni_1_2=True)

    def test_credit_estimates_match_live_flow_ui(self):
        self.assertEqual(self.tool.estimate_flow_credits("Veo 3.1 - Quality"), 100)
        self.assertEqual(self.tool.estimate_flow_credits("Veo 3.1 - Fast"), 10)
        self.assertEqual(self.tool.estimate_flow_credits("Veo 3.1 - Lite"), 5)
        self.assertEqual(
            self.tool.estimate_flow_credits("Veo 3.1 - Lite [Lower Priority]"), 0
        )
        self.assertEqual(
            self.tool.estimate_flow_credits("Omni 1.2 Flash", duration_s=8, resolution="720p"),
            24,
        )
        self.assertEqual(
            self.tool.estimate_flow_credits("Omni 1.2 Flash", duration_s=6, resolution="720p"),
            18,
        )
        self.assertEqual(
            self.tool.estimate_flow_credits("Omni 1.2 Flash", duration_s=4, resolution="720p"),
            12,
        )


class FlowDropdownAndControlsTests(unittest.TestCase):
    def setUp(self):
        self.tool = load_tool()

    def test_dropdown_distinguishes_lite_from_lite_lower_priority(self):
        # Currently selected is Lower Priority; asking for standard Lite MUST open menu.
        state = {"selected": "Veo 3.1 - Lite [Lower Priority]"}
        dd = FakeLocator("Veo 3.1 - Lite [Lower Priority]\narrow_drop_down")
        page = Mock()

        def locator(sel):
            if sel == 'button[aria-label="Select model family"]':
                return dd
            return FakeLocator(None)

        def evaluate(js, *args):
            if args and "role=menuitem" in js:
                target = args[0]
                state["selected"] = target
                dd._text = f"{target}\narrow_drop_down"
                return target
            return state["selected"]

        page.locator.side_effect = locator
        page.evaluate.side_effect = evaluate

        got = self.tool._select_veo_from_dropdown(page, "Veo 3.1 - Lite")
        self.assertEqual(got, "Veo 3.1 - Lite")
        self.assertEqual(dd.clicks, 1)

    def test_dropdown_selects_omni_1_2_when_allowed(self):
        state = {"selected": "Veo 3.1 - Quality"}
        dd = FakeLocator("Veo 3.1 - Quality\narrow_drop_down")
        page = Mock()

        def locator(sel):
            if sel == 'button[aria-label="Select model family"]':
                return dd
            return FakeLocator(None)

        def evaluate(js, *args):
            if args and "role=menuitem" in js:
                target = args[0]
                state["selected"] = target
                dd._text = f"{target}\narrow_drop_down"
                return target
            return state["selected"]

        page.locator.side_effect = locator
        page.evaluate.side_effect = evaluate

        got = self.tool._select_veo_from_dropdown(
            page, "Omni 1.2 Flash", allow_omni_1_2=True
        )
        self.assertEqual(got, "Omni 1.2 Flash")
        self.assertEqual(dd.clicks, 1)

    def test_omni_controls_select_720p_and_length_slider(self):
        clicked_kinds = []
        slider_calls = []
        page = Mock()

        def evaluate(js, arg=None):
            if 'aria-label="Length"' in js:
                slider_calls.append(arg)
                return {"value": str(arg), "min": "0", "max": "12"}
            clicked_kinds.append(arg)
            return {"x": 100, "y": 100, "t": str(arg)}

        page.evaluate.side_effect = evaluate
        self.tool._set_video_aspect_and_outputs(
            page,
            frames_mode=True,
            aspect="16:9",
            duration_s=6,
            resolution="720p",
            model="Omni 1.2 Flash",
        )
        self.assertEqual(clicked_kinds, ["frames", "16:9", "720p", "x1"])
        # min=0 -> 3s, so 6s maps to slider index 3
        self.assertEqual(slider_calls, [3])

    def test_omni_rejects_360p_and_out_of_range_duration(self):
        page = Mock()
        with self.assertRaises(ValueError):
            self.tool._set_video_aspect_and_outputs(
                page, duration_s=8, resolution="360p", model="Omni 1.2 Flash"
            )
        with self.assertRaises(ValueError):
            self.tool._set_video_aspect_and_outputs(
                page, duration_s=2, resolution="720p", model="Omni 1.2 Flash"
            )
        with self.assertRaises(ValueError):
            self.tool._set_video_aspect_and_outputs(
                page, duration_s=16, resolution="720p", model="Omni 1.2 Flash"
            )
        page.evaluate.assert_not_called()

    def test_veo3_controls_accept_9_16_and_6s_and_reject_invalid_duration(self):
        clicked_kinds = []
        page = Mock()
        page.evaluate.side_effect = lambda _js, arg=None: (
            clicked_kinds.append(arg) or {"x": 100, "y": 100, "t": str(arg)}
        )
        self.tool._set_video_aspect_and_outputs(
            page,
            frames_mode=True,
            aspect="9:16",
            duration_s=6,
            model="Veo 3.1 - Lite [Lower Priority]",
        )
        self.assertEqual(clicked_kinds, ["frames", "9:16", "6s", "x1"])
        with self.assertRaises(ValueError):
            self.tool._set_video_aspect_and_outputs(
                page, duration_s=5, model="Veo 3.1 - Lite"
            )


class FlowCliDryRunTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(TOOL_PATH), "--dry-run", *args],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )

    def test_dry_run_default_lite_lower_priority_and_omni_1_2(self):
        r_def = self.run_cli("--scenery-only", "--prompt", "Victorian lamp glows")
        self.assertEqual(r_def.returncode, 0, r_def.stderr)
        self.assertIn("model=Veo 3.1 - Quality", r_def.stdout)
        self.assertIn("est_credits=100", r_def.stdout)
        self.assertIn("retires on 2026-12-05", r_def.stdout)

        r_lite = self.run_cli("--scenery-only", "--model", "lite", "--prompt", "Test")
        self.assertEqual(r_lite.returncode, 0, r_lite.stderr)
        self.assertIn("model=Veo 3.1 - Lite", r_lite.stdout)
        self.assertIn("est_credits=5", r_lite.stdout)

        r_lp = self.run_cli(
            "--scenery-only", "--model", "lite", "--lower-priority", "--prompt", "Test"
        )
        self.assertEqual(r_lp.returncode, 0, r_lp.stderr)
        self.assertIn("model=Veo 3.1 - Lite [Lower Priority]", r_lp.stdout)
        self.assertIn("est_credits=0", r_lp.stdout)

        r_omni = self.run_cli(
            "--scenery-only",
            "--model",
            "Omni 1.2 Flash",
            "--allow-omni",
            "--duration",
            "6",
            "--prompt",
            "Test",
        )
        self.assertEqual(r_omni.returncode, 0, r_omni.stderr)
        self.assertIn("model=Omni 1.2 Flash", r_omni.stdout)
        self.assertIn("duration=6s", r_omni.stdout)
        self.assertIn("est_credits=18", r_omni.stdout)

    def test_dry_run_refuses_omni_without_flag_and_retired_omni_1_1(self):
        r_no_flag = self.run_cli("--scenery-only", "--model", "Omni 1.2 Flash", "--prompt", "Test")
        self.assertNotEqual(r_no_flag.returncode, 0)

        r_old = self.run_cli(
            "--scenery-only", "--model", "Omni 1.1 Flash", "--allow-omni", "--prompt", "Test"
        )
        self.assertNotEqual(r_old.returncode, 0)


if __name__ == "__main__":
    unittest.main()
