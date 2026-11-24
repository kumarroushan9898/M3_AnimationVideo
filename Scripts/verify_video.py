"""Verify the silent export, chapter times, captions, and embedded cover."""
import argparse
from fractions import Fraction
import json
from pathlib import Path

from pipeline import ROOT, base_timeline, probe, run, tool_environment
from Code.config import FINAL_FPS, FINAL_SIZE, GITHUB_LIMIT, SUBTITLES, THUMBNAIL


def verify_chapters(chapters, scenes):
    if len(chapters) != len(scenes):
        raise ValueError("The MP4 chapter count does not match the scene count.")
    for chapter, scene in zip(chapters, scenes, strict=True):
        if (abs(float(chapter["start_time"]) - scene["start"]) > 0.002
                or abs(float(chapter["end_time"]) - scene["start"] - scene["duration"]) > 0.002
                or chapter["tags"]["title"] != scene["title"]):
            raise ValueError(f"Chapter timing or title differs for {scene['class']}.")


def verify(path, size=FINAL_SIZE, fps=FINAL_FPS, timeline=None):
    timeline = base_timeline() if timeline is None else timeline
    data = probe(path)
    covers = [item for item in data["streams"] if item["disposition"]["attached_pic"]]
    streams = {item["codec_type"]: item for item in data["streams"] if item not in covers}
    video = streams.get("video")
    if not video:
        raise ValueError("The output is missing a playback video stream.")
    if "audio" in streams:
        raise ValueError("The build must export a silent video for manual voice-over.")
    if "subtitle" not in streams:
        raise ValueError("The output is missing the English subtitle stream.")
    if THUMBNAIL.is_file() and not covers:
        raise ValueError("The output is missing the embedded cover image.")
    if (video["width"], video["height"]) != tuple(size):
        raise ValueError(f"Unexpected video dimensions: {video['width']} × {video['height']}.")
    if Fraction(video["avg_frame_rate"]) != fps or Fraction(video["r_frame_rate"]) != fps:
        raise ValueError(f"Unexpected frame rate: {video['avg_frame_rate']}.")

    duration = float(data["format"]["duration"])
    frames = int(video["nb_frames"])
    if abs(duration - timeline["duration"]) > 1 / fps or frames != round(timeline["duration"] * fps):
        raise ValueError(f"Playback duration differs from the visual timeline: {duration:.3f}s.")
    if path.stat().st_size >= GITHUB_LIMIT:
        raise ValueError("The MP4 exceeds the regular GitHub file size limit.")
    verify_chapters(data.get("chapters", []), timeline["scenes"])

    captions = run("ffmpeg", "-v", "error", "-i", path, "-map", "0:s:0", "-f", "srt", "-",
                   capture=True, env=tool_environment("ffmpeg"))
    if captions.strip() != SUBTITLES.read_text(encoding="utf-8").strip():
        raise ValueError("Embedded captions differ from the supplied SRT.")

    stats = dict(duration=duration, width=video["width"], height=video["height"], fps=fps,
                 frames=frames, size_bytes=path.stat().st_size, video_codec=video["codec_name"],
                 audio_streams=0, captions=len(captions.strip().split("\n\n")),
                 thumbnail=bool(covers))
    print(json.dumps(stats, indent=2))
    return stats


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path, nargs="?", default=ROOT / "Video.mp4")
    args = parser.parse_args()
    verify(args.video.resolve())


if __name__ == "__main__":
    main()
