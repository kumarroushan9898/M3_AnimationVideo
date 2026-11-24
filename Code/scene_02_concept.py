"""Use visible displacements to explain addition, scaling, and the fixed origin."""
from manim import FadeIn, FadeOut, GrowArrow, Indicate, ReplacementTransform, Write

from Code.animation_utils import Lesson, Plot, formula, note, panel, replace_panel
from Code.config import BLUE, E1, E2, EXAMPLE, SHAPE
from Code.math_utils import E1_POINT, E2_POINT


class Concept(Lesson):
    scene_index = 1

    def animate_lesson(self):
        plot = Plot()
        self.board(plot)
        dot = plot.dot()
        u = plot.arrow(E1_POINT, E1)
        u_label = plot.label(r"\mathbf u", E1_POINT, E1, delta=(0.03, -0.28))
        with self.beat("vector"):
            card = panel("VECTOR = DISPLACEMENT", formula(r"\mathbf u=(1,0)", color=E1),
                         note("The coordinates tell us how far\nto move along each axis."))
            self.play(FadeIn(card), FadeIn(dot), GrowArrow(u), Write(u_label), run_time=1.1)
        with self.beat("addition"):
            card = replace_panel(self, card, panel("ADD TIP TO TAIL",
                                 formula(r"\mathbf u", "+", r"\mathbf v", "=", "(1,1)",
                                         colors={0: E1, 2: E2, 4: EXAMPLE}),
                                 note("Start the second arrow at\nthe tip of the first.")))
            v = plot.arrow((1, 1), E2, start=E1_POINT)
            v_label = plot.label(r"\mathbf v", (1, 0.5), E2, delta=(0.28, 0))
            total = plot.arrow((1, 1))
            self.play(GrowArrow(v), FadeIn(v_label), run_time=1.05)
            self.play(GrowArrow(total), run_time=1.1)
        with self.beat("scale"):
            card = replace_panel(self, card, panel("MULTIPLY BY A SCALAR",
                                 formula(r"2\mathbf u=(2,0)", color=E1), note("Twice the length.\nSame direction for this positive scalar.")))
            doubled = plot.arrow((2, 0), E1)
            doubled_label = plot.label(r"2\mathbf u", (2, 0), E1, delta=(0, -0.29))
            self.play(FadeOut(v), FadeOut(v_label), FadeOut(total),
                      ReplacementTransform(u, doubled), ReplacementTransform(u_label, doubled_label),
                      run_time=1.55)
        with self.beat("mapping"):
            card = replace_panel(self, card, panel("A TRANSFORMATION IS A MAP",
                                 formula(r"\text{input}", r"\ \xrightarrow{\ T\ }\ ", r"\text{output}",
                                         colors={0: BLUE, 2: EXAMPLE}),
                                 note("One output is assigned to\neach input vector.")))
            start = plot.arrow(E2_POINT, E2)
            end = plot.arrow((1, 1), SHAPE)
            before = plot.label(r"\mathbf v", E2_POINT, E2, delta=(-0.23, 0.20))
            after = plot.label(r"T(\mathbf v)", (1, 1), SHAPE, delta=(0.66, 0.10))
            self.play(FadeOut(doubled), FadeOut(doubled_label), GrowArrow(start), FadeIn(before),
                      run_time=0.9)
            self.play(GrowArrow(end), Write(after), run_time=1.25)
        with self.beat("add_rule"):
            card = replace_panel(self, card, panel("LINEARITY  /  ADDITION",
                                 formula(r"T(\mathbf u+\mathbf v)=T(\mathbf u)+T(\mathbf v)", size=39),
                                 note("Adding then mapping gives\nthe same endpoint as mapping\nthen adding.")))
            joined = plot.arrow((1, 1))
            pair_u = plot.arrow((2, 0), E1)
            pair_v = plot.arrow((3, 1), E2, start=(2, 0))
            image = plot.arrow((3, 1))
            self.play(FadeOut(start), FadeOut(end), FadeOut(before), FadeOut(after),
                      GrowArrow(joined), run_time=1.0)
            self.play(ReplacementTransform(joined, image), GrowArrow(pair_u), GrowArrow(pair_v),
                      run_time=2.05)
        with self.beat("scale_rule"):
            card = replace_panel(self, card, panel("LINEARITY  /  SCALING",
                                 formula(r"T(c\mathbf u)=cT(\mathbf u)"),
                                 note("Scaling an input by c scales\nits image by the same amount.")))
            input_arrow = plot.arrow((2, 0), EXAMPLE)
            image_arrow = plot.arrow((4, 0), EXAMPLE)
            step_1 = plot.arrow((2, 0), E1, start=(0, 0)).shift([0, 0.11, 0])
            step_2 = plot.arrow((4, 0), E1, start=(2, 0)).shift([0, 0.11, 0])
            self.play(FadeOut(image), FadeOut(pair_u), FadeOut(pair_v), GrowArrow(input_arrow),
                      run_time=0.9)
            self.play(ReplacementTransform(input_arrow, image_arrow), GrowArrow(step_1),
                      GrowArrow(step_2), run_time=1.9)
        with self.beat("origin"):
            card = replace_panel(self, card, panel("THE ORIGIN STAYS FIXED",
                                 formula(r"T(\mathbf 0)=T(0\mathbf u)", size=37),
                                 formula(r"=0T(\mathbf u)=\mathbf 0", color=BLUE, size=37),
                                 note("Use the scaling rule with c = 0.")))
            self.play(FadeOut(image_arrow), FadeOut(step_1), FadeOut(step_2), run_time=0.7)
            origin_label = plot.label(r"(0,0)", (0, 0), BLUE, delta=(0.52, -0.36))
            self.play(Indicate(dot, color=BLUE, scale_factor=1.9), FadeIn(origin_label), run_time=1.25)
