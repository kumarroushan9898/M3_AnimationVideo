"""Follow a square, two parallel lines, and four more examples."""
from manim import Create, FadeIn, FadeOut, Indicate, PI, Rotate, Transform, VGroup

from Code.animation_utils import Lesson, Plot, formula, note, panel, replace_panel, words
from Code.config import BLUE, E1, E2, EXAMPLE, MUTED, SHAPE
from Code.math_utils import A, REFLECTION, ROTATION, SCALING, SHEAR, UNIT_SQUARE, mapped

FLAG = ((0, 0), (1, 0), (1, 0.35), (0.35, 0.35), (0.35, 1), (0, 1))


class Interpretation(Lesson):
    scene_index = 4

    def comparison(self, side, title, tex, matrix):
        offset = -3.69 if side == "left" else 3.69
        plot = Plot((offset - 3.52, offset + 3.52, -3.14, 1.55),
                    origin=(offset, -1.0), unit=0.91, mini=True)
        heading = words(title, 32, BLUE, "SEMIBOLD").move_to([offset, 2.23, 0])
        caption = formula(tex, size=30).move_to([offset, 1.79, 0])
        before = plot.polygon(FLAG, opacity=0.0).set_stroke(SHAPE, opacity=0.38)
        shape = plot.polygon(FLAG, opacity=0.55)
        target = plot.polygon(FLAG, matrix, opacity=0.55)
        return VGroup(heading, caption, plot.base, before, plot.dot()), shape, target, plot

    def animate_lesson(self):
        plot = Plot()
        backdrop = self.board(plot)
        square = plot.polygon(UNIT_SQUARE)
        origin = plot.dot()
        dot_1 = plot.dot((1, 0), color=E1)
        dot_2 = plot.dot((0, 1), color=E2)
        dot_3 = plot.dot((1, 1), color=SHAPE)
        with self.beat("square"):
            card = panel("START WITH THE UNIT SQUARE",
                         formula(r"(0,0),\ (1,0),\ (1,1),\ (0,1)", size=34),
                         note("Each side follows a grid direction."))
            self.play(FadeIn(card), FadeIn(square), FadeIn(origin), FadeIn(dot_1), FadeIn(dot_2),
                      FadeIn(dot_3), run_time=1.4)
        with self.beat("image"):
            card = replace_panel(self, card, panel("THE IMAGE IS A PARALLELOGRAM",
                                 formula(r"(0,0),\ (2,0),\ (3,1),\ (1,1)", size=34),
                                 formula(r"\mathrm{area}=2", size=37, color=SHAPE),
                                 note("The determinant is 2.\nThe area doubles.")))
            pairs = [(square, plot.polygon(UNIT_SQUARE, A)),
                     (dot_1, plot.dot((1, 0), A, E1)), (dot_2, plot.dot((0, 1), A, E2)),
                     (dot_3, plot.dot((1, 1), A, SHAPE))]
            plot.warp(self, *pairs, run_time=3.0)
            labels = VGroup(
                plot.label(r"(0,0)", (0, 0), delta=(-0.53, -0.37)),
                plot.label(r"(2,0)", mapped((1, 0)), E1, delta=(0.02, -0.34)),
                plot.label(r"(3,1)", mapped((1, 1)), SHAPE, delta=(0.08, 0.34)),
                plot.label(r"(1,1)", mapped((0, 1)), E2, delta=(-0.30, 0.35)),
            )
            self.play(FadeIn(labels), run_time=0.85)
        with self.beat("origin"):
            card = replace_panel(self, card, panel("THE ORIGIN IS STILL FIXED",
                                 formula(r"A(0,0)=(0,0)", color=BLUE),
                                 note("The origin stays put.\nThe grid lines stay straight.")))
            self.play(Indicate(origin, scale_factor=2.1, color=BLUE), run_time=1.25)
        with self.beat("lines"):
            card = replace_panel(self, card, panel("WHAT HAPPENS TO LINES?",
                                 note("A line maps to a line or a point."),
                                 note("Here A is invertible. Parallel lines\nstay parallel and distinct.")))
            lines = VGroup(plot.line((-0.8, 2), (1.85, 2), BLUE, A),
                           plot.line((-0.65, 3), (1.25, 3), BLUE, A))
            self.play(Create(lines), run_time=1.9)
        with self.beat("gallery1"):
            self.play(FadeOut(VGroup(plot.base, backdrop, square, origin, dot_1, dot_2,
                                     dot_3, labels, lines, card)), run_time=0.55)
            left, lhs, _, left_plot = self.comparison("left", "Rotation", r"(x,y)\mapsto(-y,x)", ROTATION)
            right, rhs, rhs_target, _ = self.comparison("right", "Reflection", r"(x,y)\mapsto(-x,y)", REFLECTION)
            self.reveal(left, right, lhs, rhs, duration=0.7)
            self.hold_until(2.904)
            self.play(Rotate(lhs, PI / 2, about_point=left_plot.origin), run_time=1.35)
            self.hold_until(4.778)
            self.play(FadeOut(rhs), FadeIn(rhs_target), run_time=0.65)
        with self.beat("gallery2"):
            self.play(FadeOut(VGroup(left, right, lhs, rhs_target)), run_time=0.35)
            left, lhs, lhs_target, _ = self.comparison("left", "Scaling", r"(x,y)\mapsto(2x,2y)", SCALING)
            right, rhs, rhs_target, _ = self.comparison("right", "Shearing", r"(x,y)\mapsto(x+y,y)", SHEAR)
            self.reveal(left, right, lhs, rhs, duration=0.45)
            self.play(Transform(lhs, lhs_target), run_time=1.05)
            self.hold_until(1.929)
            self.play(Transform(rhs, rhs_target), run_time=1.15)
        with self.beat("applications"):
            self.play(FadeOut(VGroup(left, right, lhs, rhs)), run_time=0.50)
            applications = VGroup(
                words("Computer graphics", 37, BLUE, "SEMIBOLD"),
                words("Shape and orientation of objects", 26, MUTED),
                words("Robotics", 37, E1, "SEMIBOLD"),
                words("Directions in different coordinate frames", 26, MUTED),
                words("Engineering", 37, EXAMPLE, "SEMIBOLD"),
                words("Local models of small deformations", 26, MUTED),
            )
            for i, app in enumerate(applications):
                app.move_to([0, 2.15 - (i // 2) * 1.70 - (i % 2) * 0.52, 0])
            for index, start in enumerate((2.303, 4.975, 7.151)):
                self.hold_until(start)
                self.reveal(*applications[index * 2:index * 2 + 2], duration=0.6)
