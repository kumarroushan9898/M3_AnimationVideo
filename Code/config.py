"""Project metadata and the locked visual edit, in seconds from each scene start."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / ".build"
THUMBNAIL = ROOT / "Thumbnail.jpg"
SUBTITLES = ROOT / "Subtitles/narration.srt"
TITLE = "What Matrices Really Do to Space"
SUBTITLE = "Understanding Linear Transformations Visually"
STUDENT_NAME = "Kumar Roushan"
STUDENT_ID = "E25B071257"
FINAL_SIZE = (1920, 1080)
FINAL_FPS = 60
PREVIEW_SIZE = (960, 540)
PREVIEW_FPS = 30
TARGET_SECONDS = 300
GITHUB_LIMIT = 100 * 1024**2

SURFACE = "#101B2F"
BORDER = "#283955"
GRID = "#2D547A"
AXIS = "#627E9E"
INK = "#F5F7FC"
MUTED = "#B5C6DB"
BLUE = "#80D8FA"
E1 = "#62E2A7"
E2 = "#FF7D92"
EXAMPLE = "#FFDB6E"
SHAPE = "#BEA1FF"

SCENES = (
    ("Hook", "What if matrices could move space?", (
        ("title", 2), ("grid", 6), ("warp", 9.5), ("question", 12.5),
    )),
    ("Concept", "What makes a transformation linear?", (
        ("vector", 6), ("addition", 4.5), ("scale", 3.5), ("mapping", 7.5),
        ("add_rule", 9.5), ("scale_rule", 6), ("origin", 8),
    )),
    ("BasisVectors", "The secret hidden inside a matrix", (
        ("basis", 14), ("matrix", 6.5), ("first", 6), ("second", 5.5),
        ("warp", 6), ("whole", 12),
    )),
    ("WorkedExample", "Matrix multiplication, without memorizing", (
        ("input", 7), ("path", 12), ("decompose", 6), ("parts", 8),
        ("map", 12), ("result", 13), ("setup", 5), ("first_row", 6),
        ("second_row", 6.5), ("compare", 16.5), ("general", 13),
    )),
    ("Interpretation", "The geometry behind the numbers", (
        ("square", 5), ("image", 5), ("origin", 4.5), ("lines", 4),
        ("gallery1", 6.5), ("gallery2", 4.5), ("applications", 15.5),
    )),
    ("Summary", "Summary and credits", (
        ("takeaways", 13.5), ("credits", 6.5), ("closing", 5),
    )),
)
