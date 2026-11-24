"""Render Manim scenes and deliver a silent MP4 with captions."""
import argparse

from pipeline import BUILD, ROOT, base_timeline, ffmpeg, render_visuals
from Code.config import FINAL_FPS, FINAL_SIZE, GITHUB_LIMIT, SUBTITLES, THUMBNAIL, TITLE
from verify_video import verify


def write_chapters(path, timeline):
    records = [";FFMETADATA1", f"title={TITLE}"]
    for scene in timeline["scenes"]:
        start_ms = round(scene["start"] * 1000)
        end_ms = round((scene["start"] + scene["duration"]) * 1000)
        records += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={start_ms}",
                    f"END={end_ms}", f"title={scene['title']}"]
    path.write_text("\n".join(records) + "\n", encoding="utf-8")


def package(visual, output, timeline):
    chapters = output.parent / "chapters.ffmetadata"
    write_chapters(chapters, timeline)
    inputs = ["-i", visual, "-i", SUBTITLES, "-f", "ffmetadata", "-i", chapters]
    common = ["-map", "0:v:0", "-map", "1:s:0", "-map_metadata", "2",
              "-map_chapters", "2", "-an", "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
              "-movie_timescale", "1000", "-movflags", "+faststart"]
    if THUMBNAIL.is_file():
        inputs += ["-i", THUMBNAIL]
        common += ["-map", "3:v:0", "-c:v:1", "copy", "-disposition:v:1", "attached_pic"]
    ffmpeg(*inputs, *common, "-c:v:0", "copy", output)
    if output.stat().st_size >= GITHUB_LIMIT:
        budget = int((92 * 1024**2) * 8 / timeline["duration"] / 1000)
        log = output.parent / "x264-pass"
        encode = ["-c:v:0", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
                  "-b:v", f"{budget}k", "-passlogfile", log]
        ffmpeg("-i", visual, "-map", "0:v:0", *encode, "-pass", "1", "-an", "-f", "null", "/dev/null")
        ffmpeg(*inputs, *common, *encode, "-pass", "2", output)


def production(output, size, fps, build_name):
    from Code.math_utils import verify_math

    print(f"Verified {len(verify_math())} mathematical claims.", flush=True)
    timeline = base_timeline()
    visual = render_visuals(timeline, size, fps, build_name)
    pending = BUILD / build_name / "muxed.mp4"
    package(visual, pending, timeline)
    verify(pending, size, fps, timeline)
    pending.replace(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    output = ROOT / "Video.mp4"
    production(output, FINAL_SIZE, FINAL_FPS, "final")
    print(output)


if __name__ == "__main__":
    main()
