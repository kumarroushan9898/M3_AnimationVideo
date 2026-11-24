"""Read the columns first, then animate the same map across the plane."""
from manim import (
    Create, FadeIn, FadeOut, GrowArrow, Indicate, Matrix, ReplacementTransform, RIGHT,
    SurroundingRectangle, VGroup, Write,
)

from Code.animation_utils import Lesson, Plot, formula, note, panel, place_left, replace_panel
from Code.config import BLUE, E1, E2, EXAMPLE, INK
from Code.math_utils import A, E1_POINT, E2_POINT, INPUT, mapped


class BasisVectors(Lesson):
    scene_index = 2

    def animate_lesson(self):
        plot = Plot()
        self.board(plot)
        e1, e2 = plot.arrow(E1_POINT, E1), plot.arrow(E2_POINT, E2)
        x_label = plot.label(r"\mathbf e_1", E1_POINT, E1, delta=(0, -0.30))
        y_label = plot.label(r"\mathbf e_2", E2_POINT, E2, delta=(-0.37, 0))
        self.add(plot.dot())
        with self.beat("basis"):
            card = panel("THE STANDARD BASIS", formula(r"\mathbf e_1=(1,0)", color=E1),
                         formula(r"\mathbf e_2=(0,1)", color=E2),
                         note("One step right and one step up.\nEvery vector combines these steps."))
            self.play(FadeIn(card), run_time=0.7)
            self.hold_until(6.566)
            self.play(GrowArrow(e1), Write(x_label), run_time=1.0)
            self.hold_until(8.998)
            self.play(GrowArrow(e2), Write(y_label), run_time=1.0)
        with self.beat("matrix"):
            matrix = Matrix(A.tolist(), h_buff=0.82, v_buff=0.69).scale(0.83).set_color(INK)
            assignment = formula("A=", size=43)
            display = VGroup(assignment, matrix).arrange(RIGHT, buff=0.19)
            card = replace_panel(self, card, panel("READ THE MATRIX BY COLUMN", display))
            columns = matrix.get_columns()
            for start, row in zip((1.548, 3.584), matrix.get_rows(), strict=True):
                self.hold_until(start)
                self.play(Indicate(row, color=BLUE, scale_factor=1.05), run_time=0.65)
        with self.beat("first"):
            first_box = SurroundingRectangle(columns[0], buff=0.11, color=E1, stroke_width=2,
                                            corner_radius=0.08)
            cols_1 = place_left(formula(r"A\mathbf e_1=(2,0)", color=E1, size=36), 1.69, -0.39)
            demo_1 = plot.arrow(E1_POINT, E1, matrix=A)
            demo_1_label = plot.label(r"(2,0)", mapped(E1_POINT), E1, delta=(0, -0.30))
            self.play(Create(first_box), columns[0].animate.set_color(E1), Write(cols_1), run_time=0.95)
            self.hold_until(2.717)
            self.play(ReplacementTransform(e1.copy(), demo_1), FadeIn(demo_1_label), run_time=2.4)
        with self.beat("second"):
            second_box = SurroundingRectangle(columns[1], buff=0.11, color=E2, stroke_width=2,
                                             corner_radius=0.08)
            cols_2 = place_left(formula(r"A\mathbf e_2=(1,1)", color=E2, size=36), 1.69, -1.17)
            demo_2 = plot.arrow(E2_POINT, E2, matrix=A)
            demo_2_label = plot.label(r"(1,1)", mapped(E2_POINT), E2, delta=(0.40, 0.25))
            self.play(Create(second_box), columns[1].animate.set_color(E2), Write(cols_2), run_time=0.95)
            self.hold_until(2.755)
            self.play(ReplacementTransform(e2.copy(), demo_2), FadeIn(demo_2_label), run_time=2.4)
        with self.beat("warp"):
            self.play(FadeOut(demo_1), FadeOut(demo_2), FadeOut(demo_1_label), FadeOut(demo_2_label),
                      run_time=0.55)
            example = plot.arrow(INPUT)
            self.play(GrowArrow(example), run_time=0.7)
            plot.warp(self, (e1, plot.arrow(E1_POINT, E1, matrix=A)),
                      (e2, plot.arrow(E2_POINT, E2, matrix=A)),
                      (example, plot.arrow(INPUT, matrix=A)),
                      (x_label, x_label.copy().move_to(demo_1_label)),
                      (y_label, y_label.copy().move_to(demo_2_label)), run_time=4.1)
            self.play(FadeOut(x_label), FadeOut(y_label), FadeIn(demo_1_label), FadeIn(demo_2_label),
                      run_time=0.5)
        with self.beat("whole"):
            for obj in (first_box, second_box, cols_1, cols_2):
                self.remove(obj)
            card = replace_panel(self, card, panel("TWO COLUMNS DETERMINE THE MAP",
                                 formula(r"T(x,y)=xA\mathbf e_1+yA\mathbf e_2", size=37),
                                 formula(r"T(x,y)=(2x+y,\ y)", size=40, color=BLUE),
                                 note("Preserve the input coefficients x and y.\nApply them to the transformed basis.")))
            target = plot.label(r"A\mathbf v", mapped(INPUT), EXAMPLE, delta=(0, 0.35))
            self.play(Write(target), run_time=0.85)
