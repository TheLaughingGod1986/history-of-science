"""Join the J2563 internal timing rough after the five archive pictures exist.

P5:16b stays the dependency slate. This is not a finished film.
"""
import argparse, importlib.util, json, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v10 = _load("join_timing_rough_v10")
FIVE = (
    "P5:03a_arch_squire_inhaler_1846",
    "P5:04a",
    "P5:06a_arch_simpson_1847",
    "P5:07a_arch_snow_chloroform_1858",
    "P5:14a",
)


def sequence(plan, by_id):
    ordered = v10.sequence(plan, by_id)
    for item in ordered:
        if item["row_id"] in FIVE:
            item["kind"] = "archive_composite"
    kinds = [item["row_id"] for item in ordered if item["kind"] == "archive_composite"]
    if kinds != list(FIVE):
        raise ValueError("The five archive composites are not in plan order")
    if any(item["kind"] == "archive_download_held" for item in ordered):
        raise ValueError("A download hold is still in the rough")
    return ordered


def source_for(out, item, by_id, composites):
    if item["kind"] != "archive_composite":
        return v10.source_for(out, item, by_id)
    record = composites[item["row_id"]]
    path = Path(record["path"])
    digest = v10.sha256(path)
    if digest != record["sha256"]:
        raise ValueError(f"{item['row_id']} hash does not match the composite manifest")
    if v10.probe_frames(path) != item["frames"]:
        raise ValueError(f"{item['row_id']} frame count does not match v03")
    return path, digest, item["frames"]


def join(out, composites_json):
    out.mkdir(parents=True, exist_ok=True)
    composites = {row["row_id"]: row for row in json.loads(Path(composites_json).read_text())["rows"]}
    plan, by_id = v10.load_plan()
    ordered = sequence(plan, by_id)
    if v10.sha256(v10.WAV) != v10.WAV_SHA:
        raise ValueError("Locked narration hash does not match")
    rows = []
    listing = out / "concat.txt"
    with listing.open("w") as handle:
        for item in ordered:
            path, digest, source_frames = source_for(out, item, by_id, composites)
            handle.write(f"file '{path}'\n")
            source_path = str(path) if item["kind"] == "archive_composite" else by_id[item["row_id"]]["path"]
            rows.append({**item, "path": str(path), "source_path": source_path, "sha256": digest, "source_frames": source_frames})
            print(item["row_id"], item["kind"], flush=True)
    rough = out / "hos_011_timing_rough_v11.mp4"
    frames = ordered[-1]["end_frame_exclusive"]
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listing), "-i", str(v10.WAV),
        "-filter_complex", f"[1:a]apad=whole_dur={frames / 30:.3f}[a]",
        "-map", "0:v:0", "-map", "[a]", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-fps_mode", "passthrough", "-c:a", "aac", "-b:a", "160k",
        "-movflags", "+faststart", str(rough),
    ], check=True)
    if v10.probe_frames(rough) != frames:
        raise ValueError("Joined rough frame count does not match the locked picture plan")
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(rough), "-f", "null", "-"], check=True)
    level = subprocess.check_output([
        "ffmpeg", "-i", str(rough), "-af", "volumedetect", "-f", "null", "-",
    ], stderr=subprocess.STDOUT, text=True)
    manifest = {
        "job": "J2563",
        "status": "Internal timing rough. Five archive photographs replace the download holds. Not a finished film.",
        "generation_authorized": False,
        "film_stage_approved": False,
        "audio_review": False,
        "motion_review": False,
        "spend_gbp": 0,
        "credits_used": 0,
        "plan": "PICTURE_PLAN_v03.json",
        "wav_sha256": v10.WAV_SHA,
        "wav_duration_s": plan["vo_lock"]["duration_s"],
        "picture_frames": frames,
        "picture_duration_s": frames / 30,
        "rough": str(rough),
        "rough_sha256": v10.sha256(rough),
        "level_meter": level[-500:],
        "rows": rows,
        "reuse": {
            "row_id": "P5:16b_reuse_pocket_watch_to_globe",
            "status": "dependency_slate",
            "p1_07b_duration_s": None,
            "p1_07b_in_s": None,
            "p1_07b_out_s": None,
            "p5_16b_need_s": 4.52,
            "p1_07b_plan_s": 6.61,
            "disjoint_need_s": 11.13,
            "hypothetical_8s_overlap_s": 3.13,
            "note": "No generated P1:07b file exists, so actual duration, in and out are empty. A disjoint tail was not invented.",
        },
    }
    (out / "TIMING_ROUGH_v11.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"PASS frames={frames} sha={manifest['rough_sha256']}")
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--composites", type=Path, required=True)
    args = parser.parse_args()
    join(args.out, args.composites)


if __name__ == "__main__":
    main()
