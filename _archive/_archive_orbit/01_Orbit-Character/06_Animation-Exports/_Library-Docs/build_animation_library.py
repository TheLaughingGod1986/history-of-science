#!/usr/bin/env python3
"""Build Orbit reusable animation library: prompts, index, docs, folder map."""
from __future__ import annotations

import csv
import shutil
from pathlib import Path

ROOT = Path("/Users/ben/code/Orbit-YouTube")
LIB = ROOT / "01_Orbit-Character/06_Animation-Exports"
PROMPTS = LIB / "_Prompts"
DOCS = LIB / "_Library-Docs"
PACK = Path.home() / "Desktop/Orbit-Animation-Library-Pack"

CONSISTENCY = """
Preserve Orbit exactly as shown in the uploaded reference image. Maintain the same rounded orange body, black faceplate, cream expressive eyes, single glowing antenna, side arms, proportions, materials and warm animated-film visual style. Do not redesign the character. Do not add limbs, fingers, facial features, clothing, text, logos or accessories.
""".strip()

STYLE = """
Cinematic premium animated-film rendering (Pixar-like quality). Soft volumetric light, warm rim lighting, deep space background with subtle stars/nebula. Orbit floats naturally in zero gravity — smooth, subtle, weightless, believable. No exaggerated bouncing. No childish cartoon motion. No camera shake. No text, logos, watermarks.
""".strip()

# id, category_folder, filename_stem, title, duration_s, description, usage, action_prompt
ANIMS = [
    # HOVER
    ("01", "Hover", "orbit_idle-hover", "Idle Hover", 6,
     "Orbit gently floats in place with very small body drift and an occasional soft blink.",
     "Background bed under narration; idle hold between beats",
     "Orbit floats gently in deep space, nearly still. Tiny weightless body drift. Occasional soft blink. Antenna glow steady and soft. Mostly static camera."),
    ("02", "Hover", "orbit_looking-around", "Looking Around", 6,
     "Orbit slowly scans the environment; eyes move naturally left to right.",
     "Curiosity beats; surveying a scene before explaining",
     "Orbit hovers and slowly looks around space. Cream eyes track naturally left to right. Subtle head follow. Soft blink once. Calm curiosity."),
    ("03", "Hover", "orbit_listening", "Listening", 6,
     "Orbit looks attentive with a small head tilt and soft blink.",
     "When posing a question to the viewer; pause before an answer",
     "Orbit hovers attentively facing camera. Small thoughtful head tilt. Soft blink. Quiet listening energy. Minimal arm movement."),
    # TALKING
    ("04", "Talking", "orbit_explaining", "Explaining", 8,
     "Gentle explanatory arm gestures with a friendly confident expression.",
     "Primary talking bed under educational narration",
     "Orbit faces camera while hovering. Small natural explanatory gestures with side arms, alternating lightly. Friendly confident eyes. Imperceptible zero-g rock. Slow cinematic push-in."),
    ("05", "Talking", "orbit_point-left", "Point Left", 6,
     "Orbit points left with a side arm, then returns to neutral.",
     "Callouts to left-side graphics, maps, or B-roll",
     "Orbit points clearly to screen-left with one side arm, holds briefly, then returns to neutral hover. Friendly eyes. Controlled premium motion."),
    ("06", "Talking", "orbit_point-right", "Point Right", 6,
     "Orbit points right with a side arm, then returns to neutral.",
     "Callouts to right-side graphics or on-screen facts",
     "Orbit points clearly to screen-right with one side arm, holds briefly, then returns to neutral hover. Friendly eyes. Controlled premium motion."),
    ("07", "Talking", "orbit_counting", "Counting", 8,
     "Orbit counts three invisible objects with restrained hand/arm gestures.",
     "Numbered lists; three-step explanations",
     "Orbit counts three invisible items in front of him with clear but restrained arm gestures — one, two, three — then rests. Warm educational tone. No props."),
    ("08", "Talking", "orbit_welcoming", "Welcoming", 8,
     "Orbit opens both arms in a warm welcoming gesture.",
     "Channel intros; section openers; subscribe soft-asks",
     "Orbit opens both side arms in a warm welcoming gesture toward camera, then gently returns toward neutral. Friendly cream eyes. Soft antenna glow."),
    # REACTIONS
    ("09", "Reactions", "orbit_curious", "Curious", 6,
     "Eyes widen slightly; Orbit looks upward with curiosity.",
     "Wonder beats; before revealing a big idea",
     "Orbit’s cream eyes widen slightly with curiosity. He looks upward toward stars. Small forward lean in zero-g. Restrained, premium."),
    ("10", "Reactions", "orbit_thinking", "Thinking", 6,
     "Looks up, tilts head; brief tasteful question-mark hologram.",
     "Rhetorical questions; Fermi-paradox style beats",
     "Orbit looks upward, tilts head slightly. A small tasteful glowing question-mark hologram appears beside him briefly and fades. Subtle float. Mostly static camera."),
    ("11", "Reactions", "orbit_surprised", "Surprised", 6,
     "Eyes widen; turns smoothly to look off-screen.",
     "Reveals; plot twists; sudden discoveries",
     "Orbit notices something off-screen. Eyes widen, body turns smoothly, looks toward a distant glowing galaxy. Expressive but not cartoonish."),
    ("12", "Reactions", "orbit_happy", "Happy", 6,
     "Warm eye-smile and a small affirming nod.",
     "Payoffs; positive conclusions; good news",
     "Orbit smiles warmly with his cream eyes (no mouth). Small affirming nod. Soft contentment. Subtle float."),
    ("13", "Reactions", "orbit_excited", "Excited", 6,
     "Subtle excitement with gentle arm movement — never hyperactive.",
     "Breakthrough moments; exciting science news",
     "Orbit shows subtle excitement: brighter eye energy, gentle arm lift, soft antenna pulse. Not cartoonish. Not hyperactive. Premium restraint."),
    ("14", "Reactions", "orbit_concerned", "Concerned", 6,
     "Thoughtful, softened eyes; very restrained concern.",
     "Risks, Great Filter, cautionary science beats",
     "Orbit looks thoughtfully concerned. Eyes soften. Very small downward tilt. Deeply restrained. No melodrama."),
    # MOVEMENT
    ("15", "Movement", "orbit_fly-in", "Fly In", 8,
     "Orbit flies into frame and settles into a natural hover.",
     "Scene openers; returning to Orbit after B-roll",
     "Orbit flies smoothly into frame from deep space and settles into a natural hover facing camera. Soft deceleration. Cinematic."),
    ("16", "Movement", "orbit_fly-out", "Fly Out", 8,
     "Orbit leaves the frame smoothly.",
     "Scene exits; handoff to B-roll",
     "Orbit turns slightly and flies smoothly out of frame into deep space. Elegant exit. No abrupt cut feel."),
    ("17", "Movement", "orbit_rotate", "Rotate", 8,
     "Slow full 360° rotation showing consistent design.",
     "Character showcases; design appreciation moments",
     "Orbit slowly rotates 360 degrees while hovering, showcasing front, side, and back consistently. Smooth constant angular speed. Premium lighting."),
    ("18", "Movement", "orbit_turn-around", "Turn Around", 6,
     "Turns to face another direction.",
     "Redirecting attention; changing topic visually",
     "Orbit turns smoothly about 120–180 degrees to face a new direction, then settles. Clean silhouette throughout."),
    # TRANSITIONS
    ("19", "Transitions", "orbit_enter-from-left", "Enter From Left", 6,
     "Orbit enters from frame left and settles.",
     "Left-to-right section transitions",
     "Orbit enters from the left edge of frame, drifts to center-left, and settles into a gentle hover."),
    ("20", "Transitions", "orbit_enter-from-right", "Enter From Right", 6,
     "Orbit enters from frame right and settles.",
     "Right-to-left section transitions",
     "Orbit enters from the right edge of frame, drifts to center-right, and settles into a gentle hover."),
    ("21", "Transitions", "orbit_enter-from-bottom", "Enter From Bottom", 6,
     "Orbit rises into frame from below.",
     "Rising energy; new chapter starts",
     "Orbit rises into frame from below, floating upward to a natural mid-frame hover. Soft deceleration."),
    ("22", "Transitions", "orbit_exit-upwards", "Exit Upwards", 6,
     "Orbit exits upward out of frame.",
     "Ascending exits; skyward topic shifts",
     "Orbit drifts upward and exits the top of frame toward the stars. Calm, cinematic."),
    ("23", "Transitions", "orbit_slow-drift", "Slow Drift Across Screen", 8,
     "Orbit slowly drifts across the frame.",
     "Long narration beds; contemplative passages",
     "Orbit slowly drifts horizontally across deep space, gentle idle motion and one blink. Continuous elegant path. Loop-friendly mid section."),
    # ENDINGS
    ("24", "Ending", "orbit_goodbye", "Goodbye Wave", 8,
     "Friendly goodbye wave toward camera.",
     "Outros; end cards; subscribe soft close",
     "Orbit faces camera, smiles with his eyes, and gives a gentle goodbye wave. Warm, calm, cinematic."),
    ("25", "Ending", "orbit_looking-at-earth", "Looking At Earth", 8,
     "Orbit silently watches Earth.",
     "Reflective outros; Earth-context conclusions",
     "Orbit hovers in foreground, looking toward a beautiful Earth in the distance. Quiet wonder. Slow camera drift. No wave."),
    ("26", "Ending", "orbit_looking-at-stars", "Looking At The Stars", 8,
     "Orbit watches the Milky Way.",
     "Cosmic wonder outros; series enders",
     "Orbit looks toward a luminous Milky Way star field. Silent, thoughtful, hopeful. Soft antenna glow. Slow cinematic drift."),
    ("27", "Ending", "orbit_final-fly-away", "Final Fly Away", 10,
     "Orbit flies toward the stars as camera pulls back.",
     "Series finales; emotional end titles",
     "Orbit faces camera briefly, then turns and flies slowly toward a luminous star field. Camera gradually pulls back revealing more of the Milky Way as Orbit becomes a small silhouette. Emotional, calm, cinematic."),
]

EXPRESSIONS = [
    ("neutral", "Front-facing Orbit, calm neutral cream eyes, centered, soft space lighting."),
    ("happy", "Orbit with warm smiling eye shapes, friendly uplifted expression."),
    ("thinking", "Orbit looking slightly upward, thoughtful eye pose, subtle head tilt."),
    ("surprised", "Orbit with widened cream eyes, soft surprise, no cartoon squash."),
    ("curious", "Orbit with curious eye shapes looking upward/sideways."),
    ("concerned", "Orbit with softened, slightly downturned thoughtful eyes."),
    ("looking-left", "Orbit facing camera body, cream eyes looking clearly left."),
    ("looking-right", "Orbit facing camera body, cream eyes looking clearly right."),
    ("looking-up", "Orbit cream eyes looking upward toward stars."),
    ("eyes-closed", "Orbit with closed cream eye shapes (gentle blink/rest), peaceful."),
]

STATUS_READY = {
    "orbit_explaining": ("ready", 8.5, "Migrated from polished Seedance explaining bed"),
    "orbit_surprised": ("ready", 8.0, "Migrated from polished Seedance surprised reaction"),
    "orbit_goodbye": ("ready", 8.0, "Migrated from polished Seedance ending goodbye wave"),
}


def prompt_text(action: str, duration: int) -> str:
    return f"""Use the uploaded Orbit character sheet / reference image as the ONLY character reference.

{action}

Duration: {duration} seconds.
Aspect ratio: 16:9 landscape.
Resolution target: 1920×1080.

{STYLE}

{CONSISTENCY}

Negative constraints: no redesign, no extra limbs, no fingers, no clothing, no hats, no accessories, no text, no logos, no watermark, no faceplate distortion, no eye deformation, no missing antenna, no body morphing, no camera shake.
"""


def ensure_dirs() -> None:
    for folder in sorted({a[1] for a in ANIMS}):
        (LIB / folder).mkdir(parents=True, exist_ok=True)
    for name, _ in EXPRESSIONS:
        (LIB / "Expressions" / name).mkdir(parents=True, exist_ok=True)
    for d in ("Utilities", "_Prompts", "_Raw", "_Rejected", "_Library-Docs"):
        (LIB / d).mkdir(parents=True, exist_ok=True)
    (PACK / "prompts").mkdir(parents=True, exist_ok=True)
    (PACK / "reference").mkdir(parents=True, exist_ok=True)


def write_prompts() -> None:
    for _id, folder, stem, title, dur, _desc, _use, action in ANIMS:
        body = prompt_text(action, dur)
        for dest in (PROMPTS / f"{stem}_v01.txt", PACK / "prompts" / f"{stem}_v01.txt"):
            dest.write_text(body)
        # per-category prompt copy
        (LIB / folder / f"{stem}_prompt_v01.txt").write_text(body)

    # Expression still prompts (image gen / Seedream style)
    exp_dir = PROMPTS / "expressions"
    exp_dir.mkdir(exist_ok=True)
    (PACK / "prompts" / "expressions").mkdir(exist_ok=True)
    for name, desc in EXPRESSIONS:
        body = f"""Create a single transparent PNG still of Orbit for a YouTube mascot expression library.

Subject: {desc}

Framing: Orbit centered, mid-shot, transparent background (alpha) if supported; otherwise clean solid deep-space black that can be keyed.
Style: premium animated-film, soft rim light, same materials as reference.

{CONSISTENCY}

No text, no logos, no watermark, no extra props.
Filename target: orbit_expression-{name}_v01.png
"""
        (exp_dir / f"orbit_expression-{name}_v01.txt").write_text(body)
        (PACK / "prompts" / "expressions" / f"orbit_expression-{name}_v01.txt").write_text(body)


def write_index_and_docs() -> None:
    rows = []
    md_sections = {
        "Hover": [],
        "Talking": [],
        "Reactions": [],
        "Movement": [],
        "Transitions": [],
        "Ending": [],
    }

    for _id, folder, stem, title, dur, desc, usage, _action in ANIMS:
        filename = f"{stem}_v01.mp4"
        path = LIB / folder / filename
        # existing alternate names
        status, score, notes = STATUS_READY.get(stem, ("pending_generation", None, "Awaiting Seedance generation"))
        if path.exists():
            status = "ready"
            if score is None:
                score = 8.0
                notes = "File present in library"
        elif stem == "orbit_explaining" and (LIB / "Talking" / filename).exists():
            status = "ready"
        # case-insensitive path check already via folder names

        rel = f"01_Orbit-Character/06_Animation-Exports/{folder}/{filename}"
        rows.append({
            "animation_name": title,
            "id": _id,
            "category": folder,
            "duration_s": dur,
            "filename": filename,
            "folder": f"06_Animation-Exports/{folder}/",
            "recommended_use": usage,
            "status": status,
            "quality_score": score if score is not None else "",
            "notes": notes,
            "path": rel,
        })
        md_sections[folder].append(
            f"### {_id}. {title}\n\n"
            f"- **File:** `{filename}`\n"
            f"- **Duration:** {dur}s\n"
            f"- **Status:** {status}\n"
            f"- **Quality:** {score if score is not None else '—'}/10\n"
            f"- **Description:** {desc}\n"
            f"- **Recommended usage:** {usage}\n"
            f"- **Notes:** {notes}\n"
        )

    # CSV
    csv_path = DOCS / "animation-index.csv"
    pack_csv = PACK / "animation-index.csv"
    fields = [
        "id", "animation_name", "category", "duration_s", "filename",
        "folder", "recommended_use", "status", "quality_score", "notes",
    ]
    for dest in (csv_path, pack_csv):
        with dest.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                w.writerow(r)

    ready = sum(1 for r in rows if r["status"] == "ready")
    pending = len(rows) - ready
    # Rough credit estimate: Seedance Mini ~50 per 5s; scale by duration/5
    est_credits = 0
    for r in rows:
        if r["status"] != "ready":
            est_credits += max(50, int(round(50 * (int(r["duration_s"]) / 5.0))))

    md = []
    md.append("# Orbit Animation Library\n")
    md.append("**Channel:** Orbit  \n")
    md.append("**Purpose:** Reusable Pixar-quality mascot beds for 100+ future videos  \n")
    md.append("**Root:** `~/code/Orbit-YouTube/01_Orbit-Character/06_Animation-Exports/`  \n")
    md.append("**Canonical reference:** `01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-v01.png`  \n")
    md.append("**Protected master sheet:** `01_Orbit-Character/01_Master-References/orbit-character-sheet-master-v01.png` (never overwrite)\n")
    md.append("\n---\n")
    md.append("## Library status\n\n")
    md.append(f"| Metric | Value |\n|---|---|\n")
    md.append(f"| Animations defined | {len(rows)} |\n")
    md.append(f"| Ready | {ready} |\n")
    md.append(f"| Pending generation | {pending} |\n")
    md.append(f"| Expression stills defined | {len(EXPRESSIONS)} |\n")
    md.append(f"| Est. Seedance credits (pending, Mini @ ~50/5s) | ~{est_credits} |\n")
    md.append("\n> **Credit gate:** Do not batch-generate all pending clips until Ben confirms Seedance/Dreamina credit budget.\n")
    md.append("\n---\n")
    md.append("## Character lock (mandatory)\n\n")
    md.append("Orange rounded body · black faceplate · cream eyes · single glowing antenna · two side arms · same proportions/materials/lighting · warm optimistic personality · never childish or hyperactive.\n\n")
    md.append(f"```\n{CONSISTENCY}\n```\n")
    md.append("\n---\n")
    md.append("## Export standard\n\n")
    md.append("- 1920×1080 · 16:9 · MP4 H.264 · high bitrate · no watermark\n")
    md.append("- Prefer transparent ProRes/WebM later in `Utilities/` when pipeline supports alpha\n")
    md.append("- Naming: `orbit_<action>_v01.mp4` (bump version, never overwrite masters)\n")
    md.append("- Raw gens → `_Raw/` · rejects → `_Rejected/` · polished masters → category folders\n")
    md.append("\n---\n")

    for folder in md_sections:
        md.append(f"## {folder}\n\n")
        md.append("\n".join(md_sections[folder]))
        md.append("\n")

    md.append("## Expressions (transparent PNG targets)\n\n")
    for name, desc in EXPRESSIONS:
        status = "pending_generation"
        png = LIB / "Expressions" / name / f"orbit_expression-{name}_v01.png"
        if png.exists():
            status = "ready"
        md.append(f"- **{name}** — `{png.name}` — {desc} — **{status}**\n")

    md.append("\n---\n")
    md.append("## Generation workflow\n\n")
    md.append("1. Upload `orbit-seedance-reference-v01.png` as sole character reference.\n")
    md.append("2. Paste matching prompt from `_Prompts/` or Desktop `Orbit-Animation-Library-Pack/prompts/`.\n")
    md.append("3. Generate 16:9; prefer ≥2 takes when credits allow.\n")
    md.append("4. QC against rejection list; save raw; polish selected; copy master into category folder.\n")
    md.append("5. Update `animation-index.csv` status + quality score.\n")
    md.append("\n## QC rejection list\n\n")
    md.append("Reject: redesign, wrong colours, extra/missing limbs, missing antenna, face/eye distortion, camera shake, morphing, text, watermark, artefacts.\n")

    for dest in (DOCS / "animation-library.md", PACK / "animation-library.md", LIB / "animation-library.md"):
        dest.write_text("".join(md))

    # README in pack
    (PACK / "README_GENERATE.txt").write_text(
        f"""Orbit Animation Library — Generation Pack

Reference: reference/orbit-seedance-reference-v01.png
Prompts: prompts/*.txt ({len(ANIMS)} animations + expressions/)

READY ALREADY (do not regenerate unless upgrading quality):
- orbit_explaining_v01.mp4
- orbit_surprised_v01.mp4
- orbit_goodbye_v01.mp4

PENDING: {pending} animations (~{est_credits} credits estimated on Seedance Mini)

Confirm credit budget before generating the full batch.
Then reply to the agent: "generate library batch" or generate manually and drop files into the category folders.
"""
    )

    print(f"wrote {len(rows)} anim rows; ready={ready} pending={pending} est_credits~{est_credits}")


def copy_reference_to_pack() -> None:
    src = ROOT / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-v01.png"
    shutil.copy2(src, PACK / "reference" / src.name)
    src16 = ROOT / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
    if src16.exists():
        shutil.copy2(src16, PACK / "reference" / src16.name)


def main() -> None:
    ensure_dirs()
    write_prompts()
    copy_reference_to_pack()
    write_index_and_docs()
    print("LIB", LIB)
    print("PACK", PACK)


if __name__ == "__main__":
    main()
