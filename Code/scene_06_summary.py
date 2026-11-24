"""Close with three ideas, references, and credits."""
from manim import FadeIn, FadeOut, VGroup

from Code.animation_utils import Lesson, box, formula, place_left, rule, words
from Code.config import BLUE, E1, E2, EXAMPLE, MUTED, STUDENT_ID, STUDENT_NAME


class Summary(Lesson):
    scene_index = 5

    def animate_lesson(self):
        self.add_heading()
        cards = (
            ("Matrices represent linear transformations", r"\mathbf v\ \mapsto\ A\mathbf v", BLUE),
            ("Columns describe transformed basis vectors", r"A=[\,A\mathbf e_1\ \ A\mathbf e_2\,]", E1),
            ("Multiplication combines the columns", r"A(x,y)=xA\mathbf e_1+yA\mathbf e_2", EXAMPLE),
        )
        takeaways = VGroup()
        for index, (copy, tex, color) in enumerate(cards):
            y = 1.95 - 1.72 * index
            backdrop = box((-7.28, 7.28, y - 0.70, y + 0.70))
            title = place_left(words(copy, 33, weight="SEMIBOLD", width=7.7), -6.94, y)
            statement = formula(tex, size=37, color=color, width=5.0).move_to([4.37, y, 0])
            takeaways.add(VGroup(backdrop, title, statement))
        with self.beat("takeaways"):
            for start, card in zip((2.182, 5.126, 8.068), takeaways, strict=True):
                self.hold_until(start)
                self.reveal(card, duration=0.8)
        with self.beat("credits"):
            self.play(FadeOut(takeaways), run_time=0.5)
            left = (
                (2.28, "STUDENT"),
                (1.67, f"{STUDENT_NAME}   /   {STUDENT_ID}"),
                (0.62, "SOFTWARE"),
                (0.01, "Python · Manim CE · NumPy · SymPy"),
                (-0.54, "LaTeX · FFmpeg · ReportLab"),
            )
            right = (
                (2.28, "REFERENCES"),
                (1.67, "Gilbert Strang · MIT OpenCourseWare, 18.06"),
                (1.14, "Grant Sanderson · Essence of Linear Algebra"),
            )

            def column(rows, x):
                return VGroup(*(place_left(words(value, 23 if value.isupper() else 25,
                                                  BLUE if value.isupper() else MUTED,
                                                  width=6.58), x, y) for y, value in rows))

            credits = VGroup(column(left, -7.22), column(right, 0.58),
                             rule((0.09, -0.96), (0.09, 2.63)))
            self.play(FadeIn(credits), run_time=0.9)
        with self.beat("closing"):
            quote_1 = place_left(words("A matrix is not just a table of numbers.", 43,
                                       weight="SEMIBOLD", width=14.1), -7.23, 1.24)
            quote_2 = place_left(words("It is a description of how space changes.", 48, BLUE,
                                       "SEMIBOLD", 14.1), -7.23, -0.17)
            accent = rule((-7.22, -1.34), (0.80, -1.34), E2, 2)
            self.play(FadeOut(credits), FadeIn(quote_1), run_time=0.65)
            self.hold_until(2.352)
            self.reveal(quote_2, accent, duration=1.0)
