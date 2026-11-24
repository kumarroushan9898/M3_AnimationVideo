"""Start with a visual question and a transformation of the whole grid."""
from manim import FadeIn, FadeOut, GrowArrow, ImageMobject, Write, config

from Code.animation_utils import Lesson, Plot, formula, note, panel, place_left, replace_panel, words
from Code.config import BLUE, E1, E2, EXAMPLE, MUTED, STUDENT_ID, STUDENT_NAME, SUBTITLE, THUMBNAIL
from Code.math_utils import A, UNIT_SQUARE


class Hook(Lesson):
    def animate_lesson(self):
        plot = Plot()
        self.board(plot)
        origin = plot.dot()
        self.add(origin)
        with self.beat("title"):
            card = panel("M3  /  LINEAR TRANSFORMATIONS",
                         words("What Matrices\nReally Do to Space", 49, weight="BOLD", width=5.05),
                         words(SUBTITLE, 23, MUTED, width=5.05),
                         words(f"{STUDENT_NAME}   /   {STUDENT_ID}", 19, MUTED, width=5.05))
            self.add(card)
            if THUMBNAIL.is_file():
                cover = ImageMobject(str(THUMBNAIL)).scale_to_fit_width(config.frame_width)
                self.add(cover)
                self.wait(1.2, frozen_frame=True)
                self.play(FadeOut(cover), run_time=0.3)
        with self.beat("grid"):
            square = plot.polygon(UNIT_SQUARE)
            first = plot.arrow((1, 0), E1)
            second = plot.arrow((0, 1), E2)
            vector = plot.arrow((2, 1), EXAMPLE)
            self.play(FadeIn(square), GrowArrow(first), GrowArrow(second), GrowArrow(vector),
                      run_time=1.2)
        with self.beat("warp"):
            card = replace_panel(self, card, panel("AFTER THE MAP",
                                 note("Horizontal steps stretch.\nVertical steps lean to the right."),
                                 note("The arrows and the square\nmove with the grid.")))
            self.hold_until(2.525)
            plot.warp(self, (square, plot.polygon(UNIT_SQUARE, A)),
                      (first, plot.arrow((1, 0), E1, matrix=A)),
                      (second, plot.arrow((0, 1), E2, matrix=A)),
                      (vector, plot.arrow((2, 1), EXAMPLE, matrix=A)), run_time=4.0)
        with self.beat("question"):
            card = replace_panel(self, card, panel("THE QUESTION",
                                 words("Could a matrix be a\nmachine that changes\nspace?", 36, weight="SEMIBOLD",
                                       width=5.05)))
            image = formula(r"(2,1)\ \longmapsto\ (5,1)", size=34, color=EXAMPLE)
            place_left(image, 1.69, -0.92)
            self.play(Write(image), run_time=1.15)
