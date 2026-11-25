#!/usr/bin/env python3
"""Build HOS 011 PICTURE_PLAN_v04, part boards v04, PROMPT_AUDIT_v04, and PASS1_SCOPE_J3736.

Zero credits, zero browser, £0. Preserves immutable PICTURE_PLAN_v01..v03, all 93 word-safe
timings from v03, and all 26 already-built free rows (13 code_graphic + 13 free_archive).
Changes from v03 -> v04 (J3736):
1. Cleans 6 leaked stage-direction / bracket prefixes in Flow prompts (incl. P1:01b 'Why?' quote).
2. Resolves P5:16b_reuse_pocket_watch_to_globe (3.13 s overlap against P1:07b) by scoping
   1 dedicated moving 3D cartoon Flow plate (`P5:16b_closing_watch_and_globe`) between
   full-frame graphics P5:16a and P5:17_cream_end_card (93/93 rows, 0.00 s overlap).
3. Pins house style_refs, Explorer ref, post-5-Dec model classification per row, and
   `generation_authorized: false` across plan, part boards, and PASS1_SCOPE_J3736.json.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EDIT_REL = Path("02_Video-Projects/011_Surgery-Before-Anaesthesia/07_Edit-Project")
EXPLORER_REF_REL = "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg"
STYLE_REFS = [
    {
        "path": "04_Generated-Clips/_style_refs/04_sunny_window_v01.jpg",
        "sha256": "cdb8b421fa121454bb62d9b6dfc1c782c7c95b1634d80c856bb95555cfdc4b45",
    },
    {
        "path": "04_Generated-Clips/_style_refs/10_mint_jar_v01.jpg",
        "sha256": "311fe7b886f391eaabe32aabc0be1b1989e483dd814237c7095e3a118d423720",
    },
]

# Leaked stage-direction / bracket prefixes caught in J3736 prompt audit of v03.
PROMPT_PREFIX_CLEANUPS: dict[str, tuple[str, str]] = {
    "P1:01a": (
        "Answer image by 0:03: inside a steep-tiered",
        "Inside a steep-tiered",
    ),
    "P1:01b": (
        "Title question by 0:06 ('Why?') + physical apparatus (0:05\u20130:15): close push",
        "Close push",
    ),
    "P1:02a": (
        "Physical proof/apparatus (0:05\u20130:15): tight lateral pan",
        "Tight lateral pan",
    ),
    "P1:02b": (
        "Physical proof/apparatus (0:05\u20130:15): an assistant's hands",
        "An assistant's hands",
    ),
    "P2:03a": (
        "[EXPLORER ACTS] In the 1800 Bristol laboratory",
        "In the 1800 Bristol laboratory",
    ),
    "P3:07a": (
        "[EXPLORER ACTS] In the front row of the Boston operating dome gallery",
        "In the front row of the Boston operating dome gallery",
    ),
}

REAL_PERSON_NAMES = [
    "Liston", "Robert Liston", "Paré", "Pare", "Ambroise", "Davy", "Humphry", "Humphrey",
    "Crawford", "Venable", "James Venable", "Horace", "Colton", "Gardner",
    "Morton", "William", "John Collins", "Gilbert Abbott",
    "Holmes", "Oliver Wendell", "Charles Jackson", "Bigelow", "Henry Bigelow",
    "Boott", "Francis Boott", "Peter Squire", "James Robinson",
    "Simpson", "James Young", "John Snow", "Queen Victoria", "Victoria", "Leopold",
    "Lister", "Joseph Lister", "Pasteur", "Semmelweis", "Nightingale", "Florence",
    "Faraday", "Michael Faraday", "Hickman", "Beddoes", "Coleridge", "Southey",
    "Darwin", "Wallace", "Newton", "Franklin", "Curie", "Jenner", "Galileo", "Einstein",
]
COMMON_SURNAME_WORDS = {"Long", "Wells", "Snow", "Warren", "Jackson", "Abbott", "Squire", "Robinson"}
NAME_RE_CS = re.compile(
    r"\b(" + "|".join(re.escape(n) for n in [*REAL_PERSON_NAMES, *sorted(COMMON_SURNAME_WORDS)]) + r")\b"
)
NAME_RE_CI = re.compile(
    r"\b(" + "|".join(re.escape(n) for n in REAL_PERSON_NAMES) + r")\b",
    re.IGNORECASE,
)
FORBIDDEN_DNA_RE = re.compile(r"\b(same\s+dna|lab\s+dna|\bdna\b)\b", re.IGNORECASE)
TEXT_REQUEST_RE = re.compile(
    r"\b(reading|spelled|saying|lettered|inscribed|engraved\s+with|text\s+reads|title\s+reads|sign\s+says|banner\s+reads|title\s+question)\b",
    re.IGNORECASE,
)
LEAKED_STAGE_RE = re.compile(
    r"(Answer\s+image\s+by|Title\s+question\s+by|Physical\s+proof/apparatus|\[EXPLORER\s+ACTS\]|0:\d\d)",
    re.IGNORECASE,
)
FRAGILE_LIGHT_RE = re.compile(
    r"\b(lamps?|lanterns?|candles?|candlelight|flames?|glows?|glowing|chandeliers?|gaslights?|"
    r"firelight|hearths?|backlit|shimmers?|vapours?|vapors?|flasks?|vials?|inhalers?|"
    r"glass\s+globes?|ether\s+globes?|bell-?jars?|bottles?|tumblers?|glass\s+bulbs?|"
    r"retorts?|mists?)\b",
    re.IGNORECASE,
)
NEGATED_LIGHT_RE = re.compile(
    r"\bNo\s+(?:flames?|candles?|lamps?|emissive\s+light\s+sources?|emissive\s+screen\s+text)"
    r"(?:\s+or\s+(?:flames?|candles?|lamps?))?\.?",
    re.IGNORECASE,
)

STYLE_PREFIX = (
    "Stylised 3D animated historical scene, Pixar-meets-Arcane painterly lighting, "
    "rich period wood, brass and glass textures, warm tungsten and cool window daylight contrast, "
    "gentle background softness, no text, no letters, no numbers, no watermark, 16:9."
)

P5_16B_VISUAL = (
    "Late-afternoon golden window light sweeps gently across a quiet Boston surgical tray of clean "
    "white linen where a stopped brass pocket watch rests beside the clear two-necked glass ether "
    "globe; the camera pulls back slowly to reveal the calm, sunlit wooden amphitheatre benches "
    "rising behind, empty and peaceful. No flames or candles."
)
P5_16B_PROMPT = f"{STYLE_PREFIX} {P5_16B_VISUAL} Camera: pull-back."


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def classify_post_cutover(row: dict) -> tuple[str, str, int, list[str]]:
    prompt = str(row.get("prompt") or "")
    is_explorer = bool(row.get("explorer_start_frame") or "explorer" in prompt.lower())
    if is_explorer:
        return "explorer", "Omni 1.2 Flash", 24, ["explorer"]
    cleaned = NEGATED_LIGHT_RE.sub("", prompt)
    hits = sorted({m.group(0).lower() for m in FRAGILE_LIGHT_RE.finditer(cleaned)})
    if hits:
        return "fragile_light", "Omni 1.2 Flash", 24, hits
    return "standard", "Veo 3.1 - Lite", 5, []


def plate_id_from_row_id(row_id: str) -> str:
    if ":" in row_id:
        return row_id.split(":", 1)[1]
    return row_id


def route_for_source_kind(kind: str) -> str:
    if kind == "mint_quality":
        return "flow-first"
    if kind == "code_graphic":
        return "code-graphic"
    if kind == "free_archive":
        return "archive"
    if kind == "existing_plate_reuse":
        return "reuse"
    raise ValueError(f"unknown source_kind: {kind!r}")


def audit_prompt(row_id: str, prompt: str) -> dict:
    names = sorted(set(NAME_RE_CS.findall(prompt) + NAME_RE_CI.findall(prompt)))
    dna = sorted(set(FORBIDDEN_DNA_RE.findall(prompt)))
    text_req = sorted(set(TEXT_REQUEST_RE.findall(prompt)))
    leaks = sorted(set(LEAKED_STAGE_RE.findall(prompt)))
    has_no_text_guard = "no text, no letters, no numbers, no watermark" in prompt.lower()
    return {
        "row_id": row_id,
        "real_person_names": names,
        "forbidden_dna_terms": dna,
        "text_requests": text_req,
        "leaked_stage_directions": leaks,
        "has_no_text_guard": has_no_text_guard,
        "ok": (
            not names
            and not dna
            and not text_req
            and not leaks
            and has_no_text_guard
        ),
    }


def main() -> None:
    v03_path = HERE / "PICTURE_PLAN_v03.json"
    v03_sha = sha256_file(v03_path)
    v03 = json.loads(v03_path.read_text())

    new_rows: list[dict] = []
    prompt_cleanups_applied: list[dict] = []
    p5_16b_resolution: dict = {}

    for old_row in v03["rows"]:
        row = json.loads(json.dumps(old_row))
        rid = row["row_id"]

        if rid in PROMPT_PREFIX_CLEANUPS:
            old_prefix, new_prefix = PROMPT_PREFIX_CLEANUPS[rid]
            before_prompt = row["prompt"]
            assert old_prefix in before_prompt, f"expected cleanup target missing in {rid}"
            row["prompt"] = before_prompt.replace(old_prefix, new_prefix, 1)
            if old_prefix in str(row.get("visual") or ""):
                row["visual"] = row["visual"].replace(old_prefix, new_prefix, 1)
            prompt_cleanups_applied.append(
                {
                    "row_id": rid,
                    "removed_prefix": old_prefix,
                    "replaced_with": new_prefix,
                    "before_sha256": sha256_bytes(before_prompt.encode("utf-8")),
                    "after_sha256": sha256_bytes(row["prompt"].encode("utf-8")),
                }
            )

        if rid == "P5:16b_reuse_pocket_watch_to_globe":
            row["supersedes_v03_row_id"] = rid
            row["row_id"] = "P5:16b_closing_watch_and_globe"
            row["subject"] = (
                "Closing dedicated moving plate ('turned surgery from a race into a sleep'): "
                "stopped brass pocket watch & glass ether globe in calm Boston daylight"
            )
            row["visual"] = P5_16B_VISUAL
            row["prompt"] = P5_16B_PROMPT
            row["source_kind"] = "mint_quality"
            row["model"] = "veo-3.1-quality"
            row["picture_source"] = (
                "New dedicated closing plate to mint — Flow Veo 3.1 Quality "
                "(100 credits try-1 / 259 expected; post-5-Dec Omni 1.2 Flash 720p 24 cr; "
                "generation_authorized: false)"
            )
            row["reuses_row"] = None
            row["reuse_slice"] = None
            row["flow_clip_s"] = 8
            row["flow_credits_try1"] = 100
            row["flow_credits_expected"] = 259
            row["vertex_try1_gbp"] = 1.6
            row["vertex_expected_gbp"] = 4.14
            row["generation_authorized"] = False
            p5_16b_resolution = {
                "v03_row_id": rid,
                "v04_row_id": row["row_id"],
                "in_s": row["in_s"],
                "out_s": row["out_s"],
                "duration_s": row["duration_s"],
                "v03_issue": (
                    "P1:07b uses 6.61 s of an 8.00 s clip, leaving only 1.39 s unused; "
                    "reusing P1:07b for 4.52 s causes 3.13 s overlap (J2563/J2659)."
                ),
                "why_not_free_graphic": (
                    "P5:16b sits between full-frame code graphic P5:16a (closing triptych) "
                    "and full-frame code graphic P5:17_cream_end_card. HOS studio/RULES.md "
                    "forbids back-to-back full-frame teach graphics: a moving plate must sit between them."
                ),
                "resolution": "Scoped 1 dedicated 8s moving 3D cartoon Flow plate; 0.00 s overlap across all 93/93 rows.",
                "overlap_s": 0.0,
            }

        row["generation_authorized"] = False
        if row["source_kind"] == "mint_quality":
            tier, post_model, post_cr, cues = classify_post_cutover(row)
            row["post_cutover_tier"] = tier
            row["post_cutover_model"] = post_model
            row["post_cutover_credits_try1"] = post_cr
            row["post_cutover_cues"] = cues
        else:
            row["post_cutover_tier"] = "free"
            row["post_cutover_model"] = row["model"]
            row["post_cutover_credits_try1"] = 0
            row["post_cutover_cues"] = []

        new_rows.append(row)

    # Verify zero consecutive full-frame graphics and continuous 93-row coverage.
    assert len(new_rows) == 93
    for prev, nxt in zip(new_rows, new_rows[1:]):
        assert abs(prev["out_s"] - nxt["in_s"]) < 1e-9, f"gap between {prev['row_id']} and {nxt['row_id']}"
        assert not (
            prev["source_kind"] in ("code_graphic", "free_archive")
            and nxt["source_kind"] in ("code_graphic", "free_archive")
        ), f"consecutive full-frame graphics: {prev['row_id']} -> {nxt['row_id']}"

    mint_rows = [r for r in new_rows if r["source_kind"] == "mint_quality"]
    assert len(mint_rows) == 67
    assert sum(1 for r in new_rows if r["source_kind"] == "existing_plate_reuse") == 0
    assert sum(1 for r in new_rows if r["source_kind"] == "code_graphic") == 13
    assert sum(1 for r in new_rows if r["source_kind"] == "free_archive") == 13

    audits = [audit_prompt(r["row_id"], r["prompt"]) for r in mint_rows]
    failing = [a for a in audits if not a["ok"]]
    assert not failing, f"prompt audit failures: {failing}"

    omni_rows = [r for r in mint_rows if r["post_cutover_model"] == "Omni 1.2 Flash"]
    lite_rows = [r for r in mint_rows if r["post_cutover_model"] == "Veo 3.1 - Lite"]
    explorer_rows = [r for r in mint_rows if r["post_cutover_tier"] == "explorer"]
    fragile_rows = [r for r in mint_rows if r["post_cutover_tier"] == "fragile_light"]
    assert len(explorer_rows) == 2
    assert len(omni_rows) + len(lite_rows) == 67

    parts_summary = []
    for p in range(1, 6):
        prows = [r for r in new_rows if r["part"] == p]
        pmint = [r for r in prows if r["source_kind"] == "mint_quality"]
        pmeta = next(item for item in v03["parts"] if item["part"] == p)
        parts_summary.append(
            {
                **pmeta,
                "rows": len(prows),
                "mint_quality": len(pmint),
                "mint_fast": 0,
                "code_graphic": sum(1 for r in prows if r["source_kind"] == "code_graphic"),
                "free_archive": sum(1 for r in prows if r["source_kind"] == "free_archive"),
                "existing_plate_reuse": 0,
                "mint_rows": len(pmint),
                "free_rows": len(prows) - len(pmint),
                "flow_credits_try1": sum(r["flow_credits_try1"] for r in prows),
                "flow_credits_expected": sum(r["flow_credits_expected"] for r in prows),
                "post_cutover_hybrid_try1": sum(r["post_cutover_credits_try1"] for r in prows),
                "post_cutover_lp_hybrid_try1": sum(
                    r["post_cutover_credits_try1"] for r in prows if r["post_cutover_model"] == "Omni 1.2 Flash"
                ),
            }
        )

    plan_v04 = {
        "film": v03["film"],
        "plan_version": "v04",
        "title": v03["title"],
        "title_b": v03["title_b"],
        "air_date": "2026-12-17",
        "ben_watch_due": "2026-12-14",
        "job_id": "J3736",
        "source_plan": {
            "path": str(EDIT_REL / "PICTURE_PLAN_v03.json"),
            "sha256": v03_sha,
            "v02_retime_provenance": v03["retime_provenance"],
        },
        "chief_ruling": "J3734 unified HOS Dec-Jan line-up (25 Nov 2026); J3691 5 Dec 2026 Flow transition",
        "status": "PRICE_PASS_AND_RUNNER_READY_FOR_CHIEF_GO_NO_GENERATION",
        "generation_authorized": False,
        "style_refs": [item["path"] for item in STYLE_REFS],
        "explorer_ref": EXPLORER_REF_REL,
        "vo_lock": v03["vo_lock"],
        "hos_2026_11_e2_gate": v03["hos_2026_11_e2_gate"],
        "who_portraits": v03["who_portraits"],
        "p5_16b_resolution": p5_16b_resolution,
        "prompt_cleanups_applied": prompt_cleanups_applied,
        "parts": parts_summary,
        "totals": {
            "rows": 93,
            "mint_quality": 67,
            "mint_fast": 0,
            "code_graphic": 13,
            "free_archive": 13,
            "existing_plate_reuse": 0,
            "mint_rows": 67,
            "free_rows": 26,
            "explorer_rows": len(explorer_rows),
            "fragile_light_rows": len(fragile_rows),
            "standard_rows": len(lite_rows),
            "flow_credits_try1": 6700,
            "flow_credits_expected": 67 * 259,
            "post_cutover_hybrid_try1": len(omni_rows) * 24 + len(lite_rows) * 5,
            "post_cutover_lp_hybrid_try1": len(omni_rows) * 24,
            "post_cutover_all_omni_try1": 67 * 24,
            "post_cutover_all_lite_try1": 67 * 5,
            "vertex_try1_gbp": round(67 * 1.6, 2),
            "vertex_expected_gbp": round(67 * 4.14, 2),
        },
        "rows": new_rows,
    }

    plan_v04_path = HERE / "PICTURE_PLAN_v04.json"
    plan_v04_path.write_text(json.dumps(plan_v04, indent=2) + "\n")
    plan_v04_sha = sha256_file(plan_v04_path)

    # Write part-01..part-05_plates_v04.json synced 1:1 with PICTURE_PLAN_v04.json.
    parts_dir = HERE / "parts"
    parts_dir.mkdir(parents=True, exist_ok=True)
    boards_meta: dict[str, dict] = {}
    board_hashes: dict[int, tuple[str, str]] = {}
    for p in range(1, 6):
        prows = [r for r in new_rows if r["part"] == p]
        pmeta = next(item for item in parts_summary if item["part"] == p)
        plates = []
        for r in prows:
            pid = plate_id_from_row_id(r["row_id"])
            is_mint = r["source_kind"] == "mint_quality"
            plates.append(
                {
                    "id": pid,
                    "row_id": r["row_id"],
                    "part": p,
                    "index": r["index"],
                    "t_s": r["in_s"],
                    "t_end_s": r["out_s"],
                    "use_s": r["duration_s"],
                    "route": route_for_source_kind(r["source_kind"]),
                    "quality": "Quality" if is_mint else r["source_kind"],
                    "flow_model": "Veo 3.1 - Quality" if is_mint else None,
                    "flow_clip_s": 8 if is_mint else None,
                    "flow_credits_try1": 100 if is_mint else 0,
                    "post_cutover_tier": r["post_cutover_tier"],
                    "post_cutover_model": r["post_cutover_model"],
                    "post_cutover_credits_try1": r["post_cutover_credits_try1"],
                    "explorer": r["post_cutover_tier"] == "explorer",
                    "prompt": r["prompt"],
                    "vo_excerpt": r["vo_excerpt"],
                    "generation_authorized": False,
                }
            )
        board_doc = {
            "film": "HOS:011",
            "film_folder": "011_Surgery-Before-Anaesthesia",
            "plan_version": "v04",
            "part": p,
            "title": pmeta["title"],
            "generation_authorized": False,
            "plan_file": str(EDIT_REL / "PICTURE_PLAN_v04.json"),
            "plan_sha256": plan_v04_sha,
            "plates": plates,
        }
        board_rel = EDIT_REL / "parts" / f"part-0{p}_plates_v04.json"
        board_path = REPO / board_rel
        board_path.write_text(json.dumps(board_doc, indent=2) + "\n")
        bsha = sha256_file(board_path)
        boards_meta[str(p)] = {"path": str(board_rel), "sha256": bsha}
        board_hashes[p] = (str(board_rel), bsha)

    # Write PROMPT_AUDIT_v04.json.
    audit_doc = {
        "job": "J3736",
        "film": "HOS:011",
        "plan_file": str(EDIT_REL / "PICTURE_PLAN_v04.json"),
        "plan_sha256": plan_v04_sha,
        "source_plan_v03_sha256": v03_sha,
        "summary": {
            "total_rows": 93,
            "mint_rows_audited": 67,
            "free_rows_preserved": 26,
            "reuse_rows": 0,
            "overlap_s": 0.0,
            "consecutive_full_frame_graphics": 0,
            "real_person_name_hits": 0,
            "forbidden_dna_hits": 0,
            "text_request_hits": 0,
            "leaked_stage_direction_hits": 0,
            "all_carry_no_text_guard": True,
            "all_generation_authorized_false": True,
            "cleanups_applied_from_v03": len(prompt_cleanups_applied),
            "explorer_rows": [r["row_id"] for r in explorer_rows],
            "fragile_light_rows": [r["row_id"] for r in fragile_rows],
            "standard_rows": [r["row_id"] for r in lite_rows],
        },
        "p5_16b_resolution": p5_16b_resolution,
        "prompt_cleanups_applied": prompt_cleanups_applied,
        "rows": audits,
    }
    (HERE / "PROMPT_AUDIT_v04.json").write_text(json.dumps(audit_doc, indent=2) + "\n")

    # Write PASS1_SCOPE_J3736.json pinning plan, all 5 part boards, style refs, Explorer ref, and all 67 mint prompts.
    exp_sha = sha256_file(REPO / EXPLORER_REF_REL)
    scope_rows = []
    for idx, r in enumerate(mint_rows, start=1):
        p = r["part"]
        board_rel_str, bsha = board_hashes[p]
        prompt = r["prompt"]
        scope_rows.append(
            {
                "index": idx,
                "row_id": r["row_id"],
                "part": p,
                "id": plate_id_from_row_id(r["row_id"]),
                "t_s": r["in_s"],
                "t_end_s": r["out_s"],
                "use_s": r["duration_s"],
                "flow_clip_s": 8,
                "quality": "Quality",
                "flow_model": "Veo 3.1 - Quality",
                "try1_credits": 100,
                "max_takes": 1,
                "explorer": r["post_cutover_tier"] == "explorer",
                "post_cutover_tier": r["post_cutover_tier"],
                "post_cutover_model": r["post_cutover_model"],
                "post_cutover_credits_try1": r["post_cutover_credits_try1"],
                "board": board_rel_str,
                "board_sha256": bsha,
                "prompt_sha256": sha256_bytes(prompt.encode("utf-8")),
                "normalized_prompt_sha256": sha256_bytes(" ".join(prompt.split()).encode("utf-8")),
            }
        )

    scope_doc = {
        "job": "J3736",
        "film": "HOS:011",
        "film_folder": "011_Surgery-Before-Anaesthesia",
        "version": "v04",
        "written": "2026-11-25",
        "status": "RUNNER_READY_FOR_CHIEF_REVIEW_NO_GENERATION",
        "generation_authorized": False,
        "plan_file": str(EDIT_REL / "PICTURE_PLAN_v04.json"),
        "plan_sha256": plan_v04_sha,
        "account_rule": (
            "the studio Ultra account on flow.google.com "
            "(verified by SHA-256 digest; ULTRA badge required; personal account rejected)"
        ),
        "order_rule": "Part 01 first (first 30 seconds and opening proof), then Parts 02 to 05 in exact timeline order",
        "cutover_rule": (
            "Pre-5-Dec Veo 3.1 - Quality (100 cr) retires 2026-12-05 (J3691). "
            "Runner refuses Quality submission on/after 2026-12-05; post-cutover rows map to "
            "29 Omni 1.2 Flash 720p (24 cr) + 38 Veo 3.1 - Lite (5 cr / 0 cr Lower Priority)."
        ),
        "caps": {
            "max_total_credits": 6700,
            "max_takes_per_row": 1,
            "max_batch_rows": 5,
            "max_batch_credits": 1000,
            "headroom_floor": 3000,
            "prices": {"Quality": 100, "Still": 0},
            "models": {"Quality": "Veo 3.1 - Quality", "Still": "Nano Banana 2.1"},
            "clip_duration": "8s",
            "aspect_ratio": "16:9",
            "outputs": "x1",
        },
        "style_refs": {
            "house": STYLE_REFS,
            "explorer": {"path": EXPLORER_REF_REL, "sha256": exp_sha},
        },
        "totals": {
            "rows": 67,
            "Quality": 67,
            "Fast": 0,
            "explorer": len(explorer_rows),
            "fragile_light": len(fragile_rows),
            "standard": len(lite_rows),
            "flow_credits_try1": 6700,
            "post_cutover_hybrid_try1": len(omni_rows) * 24 + len(lite_rows) * 5,
            "post_cutover_lp_hybrid_try1": len(omni_rows) * 24,
        },
        "boards": boards_meta,
        "rows": scope_rows,
    }
    (HERE / "PASS1_SCOPE_J3736.json").write_text(json.dumps(scope_doc, indent=2) + "\n")

    # Write PICTURE_PLAN_v04.md summary.
    lines = [
        "# HOS 011 picture plan v04 — J3736",
        "",
        "Derived reproducibly from immutable `PICTURE_PLAN_v03.json` (J2655 / J2659). "
        "All 93 word-safe row boundaries, locked VO (`532.720 s`), and all 26 built free rows "
        "(13 code graphics + 13 archive composites, J2563 / PR #650) are preserved unchanged.",
        "",
        f"- **Source plan:** `PICTURE_PLAN_v03.json` (`sha256: {v03_sha}`)",
        f"- **Master plan:** `PICTURE_PLAN_v04.json` (`sha256: {plan_v04_sha}`)",
        "- **Slotted air date:** Thu 17 Dec 2026 18:00 London (Ben watch Mon 14 Dec 2026; J3734)",
        "- **Totals:** **93 rows** (`67` dedicated Flow plates + `13` built code graphics + `13` built free archives; `0` reuse rows; `0.00 s` overlap; `0` consecutive full-frame graphics)",
        "- **Prompt audit (`PROMPT_AUDIT_v04.json`):** 0 real person names, 0 `same DNA`/`lab DNA`, 0 text requests, 6 leaked stage-direction prefixes cleaned from v03 (including `P1:01b` `'Why?'` quote)",
        "- **P5:16b resolution:** `P5:16b_reuse_pocket_watch_to_globe` (which overlapped `P1:07b` by 3.13 s) replaced by dedicated moving 3D cartoon plate `P5:16b_closing_watch_and_globe` between full-frame graphics `P5:16a` and `P5:17_cream_end_card`.",
        "- **Authorization:** `generation_authorized: false` on every row, part board, and scope file. **£0 / 0 credits spent.**",
        "",
        "| Row | In–out | Seconds | Kind | Pre-5-Dec | Post-5-Dec tier (model) |",
        "|---|---|---:|---|---|---|",
    ]
    for r in new_rows:
        pre = "Veo 3.1 - Quality (100 cr)" if r["source_kind"] == "mint_quality" else "Free (0 cr)"
        post = (
            f"{r['post_cutover_tier']} ({r['post_cutover_model']}, {r['post_cutover_credits_try1']} cr)"
            if r["source_kind"] == "mint_quality"
            else "Free (0 cr)"
        )
        lines.append(
            f"| {r['row_id']} | {r['in']}–{r['out']} | {r['duration_s']:.2f} | {r['source_kind']} | {pre} | {post} |"
        )
    (HERE / "PICTURE_PLAN_v04.md").write_text("\n".join(lines) + "\n")

    print(
        f"BUILT v04: 93 rows (67 mint: {len(explorer_rows)} explorer + {len(fragile_rows)} fragile + {len(lite_rows)} standard; "
        f"26 free; 0 reuse); plan_sha256={plan_v04_sha[:12]}...; prompt_cleanups={len(prompt_cleanups_applied)}"
    )


if __name__ == "__main__":
    main()
