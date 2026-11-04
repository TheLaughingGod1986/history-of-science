#!/usr/bin/env python3
"""Tests for vo_check.norm(): what counts as the same word (no audio, no faster-whisper)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vo_check  # noqa: E402


class Norm(unittest.TestCase):
    def same(self, script: str, heard: str):
        self.assertEqual(vo_check.norm(script), vo_check.norm(heard))

    def test_decade_heard_as_digits(self):
        # 008 Part 02, 7 Oct 2026: the full-file pass FAILED "in the forties" vs "in the"
        self.same("In the seventeen-forties, electricity was a party trick.",
                  "In the 1740s, electricity was a party trick.")

    def test_year_heard_as_digits(self):
        self.same("In seventeen forty-nine, Franklin wrote", "In 1749, Franklin wrote")
        self.same("In May seventeen fifty-two, in a garden", "In May 1752, in a garden")

    def test_us_spellings_match_uk_script(self):
        self.same("Travelling lecturers rubbed glass", "Traveling lecturers rubbed glass")
        self.same("of the same colour they both moved", "of the same color they both moved")
        self.same("an invention called a Leyden jar", "an invention called a Leiden jar")

    def test_real_word_change_still_differs(self):
        self.assertNotEqual(vo_check.norm("a garden at Marly near Paris"), vo_check.norm("a garden at Mali near Paris"))
        self.assertNotEqual(vo_check.norm("in the forties"), vo_check.norm("in the fortress"))
        self.assertNotEqual(vo_check.norm("what was doing the shaping"), vo_check.norm("what was doing was shaping"))
        self.assertNotEqual(vo_check.norm("one second later"), vo_check.norm("one sec later"))
        self.assertNotEqual(vo_check.norm("one second later"), vo_check.norm("one later"))
        self.assertNotEqual(vo_check.norm("the first of July"), vo_check.norm("the of July"))
        self.assertNotEqual(vo_check.norm("the third of July"), vo_check.norm("the fourth of July"))

    def test_lyell_and_better_aliases(self):
        self.same("his friend Charles Lyell", "his friend Charles Lyle")
        self.same("Lyell's book", "Lyle's book")
        self.same("a half better beak", "a half bedder beak")

    def test_ordinal_dates(self):
        self.same("On the first of July", "On the 1st of July")
        self.same("the second of May", "the 2nd of May")
        self.same("the twenty-third of June", "the 23rd of June")
        ordinals = ("first second third fourth fifth sixth seventh eighth ninth tenth eleventh twelfth "
                    "thirteenth fourteenth fifteenth sixteenth seventeenth eighteenth nineteenth twentieth "
                    "twenty-first twenty-second twenty-third twenty-fourth twenty-fifth twenty-sixth "
                    "twenty-seventh twenty-eighth twenty-ninth thirtieth thirty-first").split()
        for n, word in enumerate(ordinals, 1):
            suffix = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
            with self.subTest(n=n):
                self.same(f"the {word} of June", f"the {n}{suffix} of June")

    def test_large_ordinals(self):
        for digits, words in (
            ("40th", "fortieth"), ("50th", "fiftieth"), ("60th", "sixtieth"),
            ("70th", "seventieth"), ("80th", "eightieth"), ("90th", "ninetieth"),
            ("100th", "hundredth"), ("101st", "one hundred and first"),
            ("123rd", "one hundred and twenty-third"), ("200th", "two hundredth"),
            ("1000th", "thousandth"), ("1100th", "one thousand one hundredth"),
            ("1234th", "one thousand two hundred and thirty-fourth"),
            ("1000000th", "millionth"), ("1000000000th", "billionth"),
        ):
            with self.subTest(digits=digits):
                self.same(f"the {words} attempt", f"the {digits} attempt")

    def test_ordinal_words_are_retained(self):
        self.assertEqual(vo_check.norm("first and second"), ["first", "and", "second"])
        self.assertEqual(vo_check.norm("one second later"), ["second", "later"])
        self.assertEqual(vo_check.norm("the 23rd of June"), ["the", "third", "of", "june"])


class ScriptLines(unittest.TestCase):
    def test_notes_after_rule_are_not_spoken(self):
        # 008 Part 05, 7 Oct 2026: the FACT_NOTES table after the last part's "---" was read as script (421 wpm)
        import tempfile
        md = ("# Title\n\n## PART 01: One\n\nFirst line.\n\n## PART 02: Two\n\n[CHAPTER CARD: Two]\n\nLast line.\n"
              "| stray | table |\n\n---\n\n## New claims for FACT_NOTES\n\n| Claim | Source |\n|---|---|\n| x | y |\n\nA note.\n")
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(md)
        self.assertEqual(vo_check.script_lines(Path(f.name), 2), ["Last line."])
        self.assertEqual(vo_check.script_lines(Path(f.name), 1), ["First line."])


if __name__ == "__main__":
    unittest.main()
