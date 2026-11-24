"""Render a silent preview at 960×540 and 30 fps."""
import argparse

from pipeline import ROOT, base_timeline, render_visuals
from Code.config import PREVIEW_FPS, PREVIEW_SIZE
from Code.math_utils import verify_math


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--visual-only", action="store_true",
                        help="Export the silent visual preview (the default).")
    parser.parse_args()
    verify_math()
    source = render_visuals(base_timeline(), PREVIEW_SIZE, PREVIEW_FPS, "visual-preview")
    output = ROOT / "VisualPreview.mp4"
    source.replace(output)
    print(output)


if __name__ == "__main__":
    main()
