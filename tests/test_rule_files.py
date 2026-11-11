"""The rule book is two files (J2578, 11 Nov 2026): AGENTS.md, then this channel's own studio/RULES.md.

The move itself is recorded in jobs/reviews/J2578/move.py, which checked that no line was lost or changed. These
tests keep what the move set up: the copies are generated from the right file, each file sends its reader to the
other, and each kind of rule is where an agent will look for it.
"""
import importlib.util
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = (ROOT / "AGENTS.md").read_text()
RULES = (ROOT / "studio/RULES.md").read_text()


def load_sync():
    name = "hos_sync_rules"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts/sync_rules.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def heads(text: str) -> list[str]:
    return re.findall(r"^## (.+)$", text, re.M)


def never(text: str, heading: str) -> str:
    return text.split(f"\n## {heading}\n", 1)[1].split("\n## ", 1)[0]


class EachFileSendsItsReaderToTheOther(unittest.TestCase):
    def test_agents_md_names_the_channel_file_in_its_first_screen(self):
        first_screen = "\n".join(AGENTS.split("\n")[:12])
        self.assertIn("**Then read `studio/RULES.md`.**", first_screen)
        self.assertIn("Where they disagree, this file wins.", first_screen)

    def test_the_channel_file_starts_by_naming_agents_md(self):
        first_screen = "\n".join(RULES.split("\n")[:6])
        self.assertIn("Read `AGENTS.md` first.", first_screen)
        self.assertIn("Where they disagree, `AGENTS.md` wins.", first_screen)

    def test_the_entry_points_name_both_files(self):
        self.assertIn("@AGENTS.md", (ROOT / "CLAUDE.md").read_text())
        self.assertIn("@studio/RULES.md", (ROOT / "CLAUDE.md").read_text())
        rule = (ROOT / ".cursor/rules/hos-studio.mdc").read_text()
        self.assertIn("then `studio/RULES.md`", rule)
        self.assertIn("then `studio/RULES.md`", (ROOT / ".cursor/hooks/hos-session-start.py").read_text())
        self.assertIn("Follow AGENTS.md, then studio/RULES.md", (ROOT / "00_Brand/Channel-Setup/tools/hos_desk.py").read_text())


class EachRuleIsWhereAnAgentLooksForIt(unittest.TestCase):
    def test_no_section_is_in_both_files(self):
        both = set(heads(AGENTS)) & set(heads(RULES))
        self.assertEqual(both, set())

    def test_the_channels_sections_are_in_the_channel_file(self):
        for head in ("Docs in force (in order of precedence)", "Definition of done (the contract)",
                     "Teach on screen (Ben, 11 Oct 2026)", "Polish pass (Astrum ref, 11 Oct 2026)",
                     "Reference lessons (HOTU + SEA, 11 Oct 2026)", "Packaging (Astrum ref, 11 Oct 2026)",
                     "Never (this channel's additions)"):
            self.assertIn(head, heads(RULES))
            self.assertNotIn(head, heads(AGENTS))

    def test_the_rules_that_are_not_the_channels_alone_stay_in_agents_md(self):
        for head in ("Commands", "The desk (Claude ↔ Grok)", "Who does what (11 Oct 2026)", "Status board",
                     "Ben's check-in (2 Oct 2026: one final OK, not one per stage)", "Never", "Git",
                     "Missing footage fallback", "Studio core (Ben, 15 Oct 2026)", "Changing the rules"):
            self.assertIn(head, heads(AGENTS))

    def test_the_two_never_lists_hold_their_own_lines(self):
        studio, channel = never(AGENTS, "Never"), never(RULES, "Never (this channel's additions)")
        for line in ("- **Uploads:**", "  - Delete a video.", "  - Ship a silent or near-silent file.", "- **Studio:**",
                     "- **Secrets:**", "- **Network details:**"):
            self.assertIn(line, studio)
            self.assertNotIn(line, channel)
        for line in ("- **Channels:**", "  - Premiere a long", "  - Put the Explorer at frame 0 of a Short.",
                     "- **Titles:**", "- **Picture:**", "  - The Orbit robot in any HOS film.", "- **Voice:**",
                     "- **TikTok:**", "- **Social:**"):
            self.assertIn(line, channel)
            self.assertNotIn(line, studio)
        self.assertIn("These add to the Never list in `AGENTS.md`. They remove nothing from it.", channel)
        self.assertIn('in `studio/RULES.md` ("Never (this channel\'s additions)")', studio)

    def test_the_channel_file_says_every_shot_fills_the_frame(self):
        # The shared Shorts gate fails a padded shot; until J2578 no rule file here said so.
        channel = never(RULES, "Never (this channel's additions)")
        self.assertIn("does not fill the 9:16 frame", channel)
        self.assertIn("`gate_shorts_open.py` fails it", channel)


class TheCopiesComeFromTheRightFile(unittest.TestCase):
    def setUp(self):
        self.sync = load_sync()

    def test_every_marker_names_the_file_that_holds_its_section(self):
        sources = {name: path.read_text() for name, path in self.sync.SOURCES.items()}
        seen = []
        for rel in self.sync.TARGETS:
            for m in self.sync.BLOCK.finditer((ROOT / rel).read_text()):
                seen.append((m.group("file"), m.group("head").strip()))
                self.assertIsNotNone(self.sync.find_section(sources[m.group("file")], m.group("head").strip()), m.group(1))
        moved = {head for name, head in seen if name == "studio/RULES.md"}
        self.assertEqual(moved, {"Teach on screen (Ben, 11 Oct 2026)", "Polish pass (Astrum ref, 11 Oct 2026)"})
        self.assertIn(("AGENTS.md", "Ben's check-in (2 Oct 2026: one final OK, not one per stage)"), seen)

    def test_the_copies_are_in_step(self):
        sources = {name: path.read_text() for name, path in self.sync.SOURCES.items()}
        for rel in self.sync.TARGETS:
            text = (ROOT / rel).read_text()
            self.assertEqual(self.sync.sync(text, sources), text, f"{rel}: run python3 scripts/sync_rules.py")

    def test_a_marker_that_names_the_wrong_file_says_where_the_section_is(self):
        sources = {"AGENTS.md": "## Never\n- a\n", "studio/RULES.md": "## Teach on screen\n- b\n"}
        self.assertEqual(self.sync.section(sources, "studio/RULES.md", "Teach on screen"), "- b\n")
        with self.assertRaises(SystemExit) as e:
            self.sync.section(sources, "AGENTS.md", "Teach on screen")
        self.assertIn("it is in studio/RULES.md", str(e.exception))
        with self.assertRaises(SystemExit) as e:
            self.sync.section(sources, "AGENTS.md", "No such section")
        self.assertNotIn("it is in", str(e.exception))

    def test_a_block_is_filled_from_the_file_it_names(self):
        sources = {"AGENTS.md": "## Never\n- studio line\n", "studio/RULES.md": "## Teach on screen\n- channel line\n"}
        text = ("<!-- SYNC: AGENTS.md#Never -->\nold\n<!-- /SYNC -->\n"
                "<!-- SYNC: studio/RULES.md#Teach on screen -->\nold\n<!-- /SYNC -->\n")
        out = self.sync.sync(text, sources)
        self.assertIn("<!-- SYNC: AGENTS.md#Never -->\n- studio line\n<!-- /SYNC -->", out)
        self.assertIn("<!-- SYNC: studio/RULES.md#Teach on screen -->\n- channel line\n<!-- /SYNC -->", out)
        self.assertIn("- studio line", self.sync.sync("<!-- SYNC: AGENTS.md#Never -->\nold\n<!-- /SYNC -->\n", sources["AGENTS.md"]))

    def test_both_files_are_scanned_for_stale_wording_and_trigger_the_check(self):
        self.assertIn("studio/RULES.md", self.sync.SCAN)
        workflow = (ROOT / ".github/workflows/rules-check.yml").read_text()
        self.assertEqual(workflow.count('"AGENTS.md", "studio/RULES.md"'), 2)


if __name__ == "__main__":
    unittest.main()
