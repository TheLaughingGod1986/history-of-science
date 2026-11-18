"""Join the J2563 internal timing rough. No downloads and no generated pictures.

The five archive rows still waiting on the Wikimedia hold are labelled hold cards,
not the approved photographs. P5:16b stays the existing dependency slate.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
WAV = Path("/Volumes/data/studio-live/History Of Science/02_Video-Projects/011_Surgery-Before-Anaesthesia/02_Voiceover/hos_011_vo_v01.wav")
WAV_SHA = "d873f1d0c9158087fd61ce0b9f53de985055d778cd58b8df70c67c0701300ae2"
HELD = {
    "P5:03a_arch_squire_inhaler_1846": "Squire inhaler download held",
    "P5:04a": "Liston operating download held",
    "P5:06a_arch_simpson_1847": "Simpson pamphlet download held",
    "P5:07a_arch_snow_chloroform_1858": "Snow inhaler download held",
    "P5:14a": "Lister spray download held",
}


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def frames_for(row):
    start = round(row["in_s"] * 30)
    end = round(row["out_s"] * 30)
    return start, end, end - start


def load_plan():
    plan = json.loads((HERE / "PICTURE_PLAN_v03.json").read_text())
    index = json.loads((HERE / "ASSEMBLY_INDEX_v08.json").read_text())
    by_id = {row["row_id"]: row for row in index["rows"]}
    return plan, by_id


def sequence(plan, by_id):
    ordered = []
    for row in plan["rows"]:
        start, end, count = frames_for(row)
        if count <= 0 or count > 240:
            raise ValueError(f"{row['row_id']} is {count} frames")
        kind = "archive_download_held" if row["row_id"] in HELD else by_id[row["row_id"]]["status"]
        ordered.append({
            "row_id": row["row_id"],
            "in_s": row["in_s"],
            "out_s": row["out_s"],
            "start_frame": start,
            "end_frame_exclusive": end,
            "frames": count,
            "kind": kind,
        })
    if [item["row_id"] for item in ordered if item["kind"] == "archive_download_held"] != list(HELD):
        raise ValueError("Hold cards are not the five approved missing archive rows")
    if ordered[0]["start_frame"] != 0 or ordered[-1]["end_frame_exclusive"] != round(plan["vo_lock"]["film_end_s"] * 30):
        raise ValueError("Row frames do not cover 0 to the locked film end")
    for left, right in zip(ordered, ordered[1:]):
        if left["end_frame_exclusive"] != right["start_frame"]:
            raise ValueError(f"Gap between {left['row_id']} and {right['row_id']}")
    return ordered


def draw_hold(path, row, line):
    image = Image.new("RGB", (1920, 1080), (45, 30, 23))
    draw = ImageDraw.Draw(image)
    lines = ["INTERNAL TIMING ROUGH", row["row_id"], "ARCHIVE DOWNLOAD HELD", line, "Not the approved picture"]
    sizes = [64, 42, 54, 36, 36]
    for text, y, size in zip(lines, [180, 340, 500, 640, 760], sizes):
        font = ImageFont.truetype(FONT, size, index=1)
        box = draw.textbbox((0, 0), text, font=font)
        while box[2] > 1800 and size > 24:
            size -= 2
            font = ImageFont.truetype(FONT, size, index=1)
            box = draw.textbbox((0, 0), text, font=font)
        draw.text(((1920 - box[2]) / 2, y), text, font=font, fill=(239, 222, 184))
    image.save(path)


def render_hold(out, item):
    target = out / "holds" / f"{item['row_id'].replace(':', '_')}.mp4"
    target.parent.mkdir(parents=True, exist_ok=True)
    png = target.with_suffix(".png")
    draw_hold(png, item, HELD[item["row_id"]])
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", "30", "-i", str(png),
        "-frames:v", str(item["frames"]), "-an", "-c:v", "libx264", "-preset", "ultrafast",
        "-crf", "18", "-pix_fmt", "yuv420p", str(target),
    ], check=True)
    return target


def probe_frames(path):
    data = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=nb_frames,width,height,avg_frame_rate", "-of", "json", str(path),
    ], text=True))
    stream = data["streams"][0]
    if (int(stream["width"]), int(stream["height"]), stream["avg_frame_rate"]) != (1920, 1080, "30/1"):
        raise ValueError(f"{path} is not 1920x1080 at 30 fps")
    return int(stream["nb_frames"])


def fit_frames(out, item, path):
    actual = probe_frames(path)
    need = item["frames"]
    if actual == need:
        return path, None
    if abs(actual - need) != 1:
        raise ValueError(f"{item['row_id']} is {actual - need} frames away from v03 timing")
    fitted = out / "fitted" / f"{item['row_id'].replace(':', '_')}.mp4"
    fitted.parent.mkdir(parents=True, exist_ok=True)
    if actual > need:
        command = ["ffmpeg", "-y", "-v", "error", "-i", str(path), "-frames:v", str(need), "-an",
                   "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p", str(fitted)]
    else:
        command = ["ffmpeg", "-y", "-v", "error", "-i", str(path), "-vf", "tpad=stop_mode=clone:stop=1",
                   "-frames:v", str(need), "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
                   "-pix_fmt", "yuv420p", str(fitted)]
    subprocess.run(command, check=True)
    if probe_frames(fitted) != need:
        raise ValueError(f"{item['row_id']} could not be fitted to v03 timing")
    return fitted, actual


def source_for(out, item, by_id):
    if item["kind"] == "archive_download_held":
        path = render_hold(out, item)
        return path, sha256(path), None
    record = by_id[item["row_id"]]
    path = Path(record["path"])
    digest = sha256(path)
    if digest != record["sha256"]:
        raise ValueError(f"{item['row_id']} hash does not match the assembly index")
    used, source_frames = fit_frames(out, item, path)
    return used, digest, source_frames


def join(out):
    out.mkdir(parents=True, exist_ok=True)
    plan, by_id = load_plan()
    ordered = sequence(plan, by_id)
    if sha256(WAV) != WAV_SHA:
        raise ValueError("Locked narration hash does not match")
    rows = []
    listing = out / "concat.txt"
    with listing.open("w") as handle:
        for item in ordered:
            path, digest, source_frames = source_for(out, item, by_id)
            handle.write(f"file '{path}'\n")
            source_path = None if item["kind"] == "archive_download_held" else by_id[item["row_id"]]["path"]
            rows.append({**item, "path": str(path), "source_path": source_path, "sha256": digest, "source_frames": source_frames})
            print(item["row_id"], item["kind"], flush=True)
    rough = out / "hos_011_timing_rough_v10.mp4"
    frames = ordered[-1]["end_frame_exclusive"]
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listing), "-i", str(WAV),
        "-filter_complex", f"[1:a]apad=whole_dur={frames / 30:.3f}[a]",
        "-map", "0:v:0", "-map", "[a]", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-fps_mode", "passthrough", "-c:a", "aac", "-b:a", "160k",
        "-movflags", "+faststart", str(rough),
    ], check=True)
    if probe_frames(rough) != frames:
        raise ValueError("Joined rough frame count does not match the locked picture plan")
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(rough), "-f", "null", "-"], check=True)
    manifest = {
        "job": "J2563",
        "status": "Internal timing rough only. Five archive pictures remain download-held. Not a finished film.",
        "generation_authorized": False,
        "film_stage_approved": False,
        "audio_review": False,
        "motion_review": False,
        "spend_gbp": 0,
        "credits_used": 0,
        "plan": "PICTURE_PLAN_v03.json",
        "wav_sha256": WAV_SHA,
        "wav_duration_s": plan["vo_lock"]["duration_s"],
        "picture_frames": frames,
        "picture_duration_s": frames / 30,
        "rough": str(rough),
        "rough_sha256": sha256(rough),
        "rows": rows,
        "reuse": {
            "row_id": "P5:16b_reuse_pocket_watch_to_globe",
            "status": "dependency_slate",
            "note": "No generated P1:07b exists. The slate stays. No unused tail was invented.",
        },
    }
    (out / "TIMING_ROUGH_v10.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"PASS frames={frames} sha={manifest['rough_sha256']}")
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    join(parser.parse_args().out)


if __name__ == "__main__":
    main()
