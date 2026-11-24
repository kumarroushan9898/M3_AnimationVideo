"""Shared timing, render, and FFmpeg functions for the command-line tools."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from Code.config import BUILD, ROOT, SCENES, TARGET_SECONDS


def run(*command, capture=False, env=None):
    return subprocess.run(
        list(map(str, command)), cwd=ROOT, check=True, env=env, text=True,
        stdout=subprocess.PIPE if capture else None,
    ).stdout


def tool_environment(*names):
    env = os.environ.copy()
    candidates = [
        *sorted((BUILD / "tex" / "TinyTeX" / "bin").glob("*")),
        Path("/Library/TeX/texbin"), Path("/opt/homebrew/bin"), Path("/usr/local/bin"),
    ]
    env["PATH"] = os.pathsep.join([*(str(p) for p in candidates if p.is_dir()),
                                  env.get("PATH", "")])
    missing = [name for name in names if not shutil.which(name, path=env["PATH"])]
    if missing:
        raise RuntimeError(f"Missing tools: {', '.join(missing)}. See README.md for macOS setup.")
    return env


def probe(path):
    return json.loads(run("ffprobe", "-v", "error", "-show_format", "-show_streams", "-show_chapters", "-of", "json",
                          path, capture=True, env=tool_environment("ffprobe")))


def base_timeline():
    clock = 0
    scenes = []
    for name, title, beats in SCENES:
        duration = sum(seconds for _, seconds in beats)
        scenes.append({"class": name, "title": title, "start": clock, "duration": duration})
        clock += duration
    if clock != TARGET_SECONDS:
        raise ValueError(f"The visual edit lasts {clock} seconds, expected {TARGET_SECONDS}.")
    return {"duration": clock, "scenes": scenes}


def ffmpeg(*arguments):
    run("ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y", *arguments,
        env=tool_environment("ffmpeg"))


def concat_files(directory, paths, scenes, fps):
    listing = directory / "concat.txt"
    listing.write_text("ffconcat version 1.0\n" + "".join(
        f"file '{path.relative_to(directory).as_posix()}'\nduration {scene['duration']:.6f}\n"
        for path, scene in zip(paths, scenes, strict=True)
    ), encoding="utf-8")
    output = directory / "joined.mp4"
    # The Manim clips can carry sub-frame time-base rounding at animation joins.
    # Snap PTS and DTS to the same frame grid, preserving the encoder's B-frame order.
    tick = f"({fps}*TB)"
    cfr = f"setts=pts=round(PTS*{tick})/{tick}:dts=round(DTS*{tick})/{tick}:duration=1/{tick}"
    ffmpeg("-f", "concat", "-safe", "1", "-i", listing, "-map", "0:v:0",
           "-c:v", "copy", "-bsf:v", cfr, output)
    return output


def video_frames(path):
    stream = next(stream for stream in probe(path)["streams"] if stream["codec_type"] == "video")
    return int(stream["nb_frames"])


def render_visuals(timeline, size, fps, name):
    directory = BUILD / name
    directory.mkdir(parents=True, exist_ok=True)
    env = tool_environment("ffmpeg", "ffprobe", "latex", "dvisvgm")
    env["PYTHONUNBUFFERED"] = "1"
    command = (sys.executable, "-m", "manim", "render", "--media_dir", directory / "manim",
               "--fps", str(fps), "-r", f"{size[0]},{size[1]}")
    entrypoint = ROOT / "Code/main.py"
    run(*command, entrypoint, *(entry["class"] for entry in timeline["scenes"]), env=env)
    clips = []
    tolerance = max(3, round(0.20 * fps))
    for scene in timeline["scenes"]:
        candidates = list((directory / "manim" / "videos" / "main").glob(
            f"*/{scene['class']}.mp4"))
        if len(candidates) != 1:
            raise RuntimeError(f"Expected one Manim output for {scene['class']}.")
        source = candidates[0]
        target_frames = round(scene["duration"] * fps)
        frames = video_frames(source)
        if abs(frames - target_frames) > tolerance:
            print(f"Retrying {source.stem} with a fresh render to correct timing.", flush=True)
            run(*command, "--disable_caching", entrypoint, source.stem, env=env)
            frames = video_frames(source)
        if abs(frames - target_frames) > tolerance:
            raise RuntimeError(f"{scene['class']} rendered {frames} frames; expected {target_frames}.")
        if frames != target_frames:
            normalized = directory / f"{scene['class']}.mp4"
            ffmpeg("-i", source, "-vf", f"tpad=stop_mode=clone:stop_duration=0.20,"
                   f"trim=end_frame={target_frames}", "-c:v", "libx264", "-preset", "veryfast",
                   "-crf", "17", "-pix_fmt", "yuv420p", "-an", normalized)
            source = normalized
        clips.append(source)
    return concat_files(directory, clips, timeline["scenes"], fps)
