"""Construct the image geometrically, then check it by reading the two rows."""
from manim import (
    Create, FadeIn, FadeOut, GrowArrow, Indicate, Matrix, RIGHT, SurroundingRectangle,
    TransformMatchingTex, VGroup, Write,
)

from Code.animation_utils import Lesson, Plot, formula, note, panel, place_left, replace_panel, words
from Code.config import BLUE, E1, E2, EXAMPLE, INK, SHAPE
from Code.math_utils import A, INPUT, mapped


class WorkedExample(Lesson):
    scene_index = 3

    def animate_lesson(self):
        plot = Plot()
        self.board(plot)
        image = mapped(INPUT)
        vector = plot.arrow(INPUT)
        label = plot.label(r"\mathbf v=(2,1)", INPUT, EXAMPLE, delta=(0.67, 0.33))
        self.add(plot.dot())

        with self.beat("input"):
            card = panel("INPUT VECTOR", formula(r"\mathbf v=(2,1)", color=EXAMPLE),
                         note("Walk two units right\nand one unit up."))
            self.play(FadeIn(card), run_time=0.55)
            self.hold_until(3.104)
            self.play(GrowArrow(vector), Write(label), run_time=1.1)
        with self.beat("path"):
            card = replace_panel(self, card, panel("FOLLOW THE STEPS",
                                 formula(r"\mathbf e_1", "+", r"\mathbf e_1", "+", r"\mathbf e_2",
                                         colors={0: E1, 2: E1, 4: E2}),
                                 note("Join each step at the tip\nof the previous one.")))
            starts = [(0, 0), (1, 0), (2, 0)]
            ends = [(1, 0), (2, 0), INPUT]
            colors = [E1, E1, E2]
            steps = [plot.arrow(end, color, start) for start, end, color in zip(starts, ends, colors)]
            intermediate_dots = [plot.dot(end, color=color) for end, color in zip(ends, colors)]
            self.hold_until(5.019)
            for step, endpoint in zip(steps, intermediate_dots):
                self.play(GrowArrow(step), FadeIn(endpoint), run_time=1.25)
        with self.beat("decompose"):
            card = replace_panel(self, card, panel("WRITE THE DECOMPOSITION",
                                 formula(r"\mathbf v", "=", r"2\mathbf e_1", "+", r"\mathbf e_2",
                                         colors={0: EXAMPLE, 2: E1, 4: E2}),
                                 note("Two copies of the horizontal basis\nvector and one vertical basis step.")))
            self.play(Indicate(vector, color=EXAMPLE, scale_factor=1.025), run_time=1.2)
        with self.beat("parts"):
            expression = card[2]
            new_expression = formula(r"A\mathbf v", "=", r"2A\mathbf e_1", "+", r"A\mathbf e_2",
                                     colors={0: EXAMPLE, 2: E1, 4: E2}, size=40)
            new_card = panel("APPLY LINEARITY", new_expression,
                             note("The coefficients stay two and one.\nMap the basis vectors they multiply."))
            self.play(FadeOut(VGroup(card[0], card[1], card[3])),
                      FadeIn(VGroup(new_card[0], new_card[1], new_card[3])),
                      TransformMatchingTex(expression, new_expression), run_time=1.4)
            self.remove(card)
            self.add(new_card)
            card = new_card
            basis_images = VGroup(
                place_left(formula(r"A\mathbf e_1=(2,0)", color=E1, size=33), 1.69, -1.15),
                place_left(formula(r"A\mathbf e_2=(1,1)", color=E2, size=33), 1.69, -1.85),
            )
            for start, image_formula in zip((2.388, 4.978), basis_images, strict=True):
                self.hold_until(start)
                self.play(Write(image_formula), run_time=0.65)
        with self.beat("map"):
            self.play(FadeOut(basis_images), run_time=0.35)
            card = replace_panel(self, card, panel("MAP EACH STEP",
                                 formula(r"2(2,0)", "+", r"(1,1)", colors={0: E1, 2: E2}),
                                 note("The two green steps double in length.\nThe red step tilts to the right.")))
            new_steps = [plot.arrow(end, color, start, matrix=A)
                         for start, end, color in zip(starts, ends, colors)]
            new_dots = [plot.dot(end, A, color) for end, color in zip(ends, colors)]
            pairs = list(zip(steps, new_steps)) + list(zip(intermediate_dots, new_dots))
            pairs.append((vector, plot.arrow(INPUT, matrix=A)))
            self.play(FadeOut(label), run_time=0.45)
            plot.warp(self, *pairs, run_time=5.2)
            image_label = plot.label(r"A\mathbf v", image, EXAMPLE, delta=(0.42, 0.38))
            self.play(FadeIn(image_label), run_time=0.5)
        with self.beat("result"):
            card = replace_panel(self, card, panel("READ THE ENDPOINT",
                                 formula(r"2(2,0)", "+", r"(1,1)", "=", r"(5,1)",
                                         colors={0: E1, 2: E2, 4: EXAMPLE}, size=39),
                                 formula(r"(4,0)+(1,1)=(5,1)", size=34),
                                 note("Four horizontal units, then one\nright and one up.")))
            answer_dot = plot.dot(image, color=EXAMPLE).scale(1.35)
            endpoint = plot.label(r"(5,1)", image, EXAMPLE, delta=(0.30, -0.39))
            projections = VGroup(plot.line((5, 0), image, EXAMPLE),
                                 plot.line((0, 1), image, EXAMPLE)).set_opacity(0.30)
            self.hold_until(3.213)
            self.play(Create(projections), FadeIn(answer_dot), Write(endpoint), run_time=1.45)
        with self.beat("setup"):
            matrix = Matrix(A.tolist(), h_buff=0.75, v_buff=0.68).scale(0.79).set_color(INK)
            column = Matrix([[2], [1]], v_buff=0.68).scale(0.79).set_color(EXAMPLE)
            row_display = VGroup(formula(r"A\mathbf v=", size=36), matrix, column).arrange(RIGHT, buff=0.17)
            card = replace_panel(self, card, panel("CHECK BY MATRIX MULTIPLICATION", row_display))
            matrix_rows = matrix.get_rows()
            column_box = SurroundingRectangle(column.get_entries(), color=EXAMPLE, buff=0.1,
                                                  stroke_width=2, corner_radius=0.08)
            self.play(Create(column_box), run_time=0.9)
        with self.beat("first_row"):
            row_box_1 = SurroundingRectangle(matrix_rows[0], color=BLUE, buff=0.10,
                                             stroke_width=2, corner_radius=0.08)
            first = place_left(formula(r"2", r"\cdot 2+", r"1", r"\cdot 1=", r"5",
                                       colors={0: BLUE, 2: BLUE, 4: EXAMPLE}, size=35), 1.69, -0.26)
            first_label = place_left(words("First output coordinate", 23, BLUE), 1.69, -0.77)
            self.play(Create(row_box_1), matrix_rows[0].animate.set_color(BLUE), Write(first),
                      FadeIn(first_label), run_time=1.65)
        with self.beat("second_row"):
            row_box_2 = SurroundingRectangle(matrix_rows[1], color=SHAPE, buff=0.10,
                                             stroke_width=2, corner_radius=0.08)
            second = place_left(formula(r"0", r"\cdot 2+", r"1", r"\cdot 1=", r"1",
                                        colors={0: SHAPE, 2: SHAPE, 4: EXAMPLE}, size=35), 1.69, -1.40)
            second_label = place_left(words("Second output coordinate", 23, SHAPE), 1.69, -1.91)
            self.play(Create(row_box_2), matrix_rows[1].animate.set_color(SHAPE), Write(second),
                      FadeIn(second_label), run_time=1.65)
        with self.beat("compare"):
            extra = VGroup(row_box_1, row_box_2, column_box, first, second, first_label, second_label)
            self.play(FadeOut(extra), run_time=0.45)
            result = formula(r"A\mathbf v=(5,1)", size=48, color=EXAMPLE)
            card = replace_panel(self, card, panel("BOTH METHODS AGREE", result,
                                 note("Geometry combines the columns.\nArithmetic reads the rows.")))
            self.play(Indicate(result, scale_factor=1.06, color=EXAMPLE),
                      Indicate(answer_dot, scale_factor=1.65, color=EXAMPLE), run_time=1.45)
        with self.beat("general"):
            replace_panel(self, card, panel("ANY INPUT VECTOR",
                          formula(r"A(x,y)=xA\mathbf e_1+yA\mathbf e_2", size=36),
                          formula(r"T(x,y)=(2x+y,\ y)", size=40, color=BLUE),
                          note("The coordinates give the weights\nfor the two transformed basis vectors.")))
