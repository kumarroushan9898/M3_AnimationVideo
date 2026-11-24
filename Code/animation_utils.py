"""Shared visual language, plot geometry, and beat timing."""
from contextlib import contextmanager

import numpy as np
from manim import (
    AnimationGroup, Arrow, Dot, FadeIn, FadeOut, Line, MathTex, NumberPlane,
    ORIGIN, Polygon, Rectangle, RoundedRectangle, Scene, Text, Transform,
    ValueTracker, Vector, VGroup, config, smooth,
)

from Code.config import AXIS, BLUE, BORDER, EXAMPLE, GRID, INK, MUTED, SCENES, SHAPE, SURFACE
from Code.math_utils import A, I, intermediate, mapped

FONT = "Avenir Next"
PLOT_BOUNDS = (-7.28, 0.96, -3.28, 2.72)
PANEL_BOUNDS = (1.24, 7.28, -3.28, 2.72)


def words(text, size=25, color=INK, weight="NORMAL", width=None):
    label = Text(text, color=color, font=FONT, font_size=size, weight=weight,
                 line_spacing=1.05)
    if width is not None and label.width > width:
        label.scale_to_fit_width(width)
    return label


def formula(*parts, size=40, color=INK, colors=None, width=5.0):
    equation = MathTex(*parts, font_size=size, color=color)
    for index, tint in (colors or {}).items():
        equation[index].set_color(tint)
    if equation.width > width:
        equation.scale_to_fit_width(width)
    return equation


def place_left(mobject, x, y):
    return mobject.move_to([x + mobject.width / 2, y, 0])


def box(bounds):
    left, right, bottom, top = bounds
    return RoundedRectangle(
        width=right - left, height=top - bottom, corner_radius=0.18,
        stroke_color=BORDER, stroke_width=1.25, fill_color=SURFACE, fill_opacity=1,
    ).move_to([(left + right) / 2, (bottom + top) / 2, 0])


def rule(start, end, color=BORDER, thickness=1.25):
    return Line([*start, 0], [*end, 0], color=color, stroke_width=thickness)


def note(text):
    return words(text, size=26, color=MUTED, width=5.05)


def panel(heading, *items):
    top = place_left(words(heading, size=20, color=BLUE, weight="BOLD", width=5.01), 1.69, 2.22)
    divider = rule((1.69, 1.87), (6.83, 1.87))
    cursor, gap = 1.53, 0.38
    for item in items:
        place_left(item, 1.69, cursor - item.height / 2)
        cursor -= item.height + gap
    if cursor + gap < -2.86:
        raise ValueError(f"Panel content is too tall: {heading}")
    return VGroup(top, divider, *items)


def replace_panel(scene, old, new):
    scene.play(FadeOut(old, shift=np.array([0, -0.12, 0])),
               FadeIn(new, shift=np.array([0, 0.12, 0])), run_time=0.65)
    return new


class Plot:
    def __init__(self, bounds=PLOT_BOUNDS, origin=(-4.85, -1.25), unit=0.90, mini=False):
        self.bounds = bounds
        self.origin = np.array([*origin, 0.0])
        self.mini = mini
        self.plane = NumberPlane(
            x_range=(-10, 11, 1), y_range=(-8, 9, 1),
            x_length=21 * unit, y_length=17 * unit,
            tips=False, faded_line_ratio=0,
        )
        self.plane.shift(self.origin - self.plane.c2p(0, 0))
        # Start with a fixed set of world-space lines. Clip each image to the plot.
        left, right, bottom, top = bounds
        coordinates = np.array([[x, y] for x in (left, right) for y in (bottom, top)])
        radius = int(np.ceil(np.max(np.linalg.norm(coordinates - self.origin[:2], axis=1))
                             / unit * 2)) + 2
        self.world_lines = (
            [((i, 0), (0, 1), i == 0) for i in range(-radius, radius + 1)] +
            [((0, i), (1, 0), i == 0) for i in range(-radius, radius + 1)]
        )
        self.lines = VGroup(*(Line(ORIGIN, np.array([0.001, 0, 0])) for _ in self.world_lines))
        self.labels = VGroup()
        if not mini:
            self.labels.add(
                words("x", 19, MUTED, "BOLD").move_to([right - 0.23, origin[1] - 0.29, 0]),
                words("y", 19, MUTED, "BOLD").move_to([origin[0] - 0.23, top - 0.23, 0]),
            )
        self.update_grid(I)
        self.base = VGroup(box(bounds), self.lines, self.labels)

    def point(self, point, matrix=I):
        return self.plane.c2p(*mapped(point, matrix))

    def clip(self, point, direction):
        left, right, bottom, top = self.bounds
        margin = 0.12
        low, high = -np.inf, np.inf
        for value, slope, minimum, maximum in zip(
            point[:2], direction[:2], (left + margin, bottom + margin),
            (right - margin, top - margin),
        ):
            if abs(slope) < 1e-10:
                if not minimum <= value <= maximum:
                    return None
                continue
            ends = sorted(((minimum - value) / slope, (maximum - value) / slope))
            low, high = max(low, ends[0]), min(high, ends[1])
        if low >= high:
            return None
        return point + low * direction, point + high * direction

    def update_grid(self, matrix):
        for line, (point, direction, axis) in zip(self.lines, self.world_lines, strict=True):
            start = self.point(point, matrix)
            delta = self.point(direction, matrix) - self.origin
            clipped = self.clip(start, delta)
            if clipped is None:
                line.set_stroke(opacity=0)
                continue
            line.put_start_and_end_on(*clipped)
            line.set_stroke(AXIS if axis else GRID, 1.6 if axis else 1.0,
                            opacity=0.76 if axis else 0.68)
        if not self.mini:
            left, right, bottom, top = self.bounds
            clipped = self.clip(self.origin, self.point((0, 1), matrix) - self.origin)
            y_tip = clipped[1]
            label_x = np.clip(y_tip[0] - 0.23, left + 0.23, right - 0.23)
            label_y = np.clip(y_tip[1] - 0.13, bottom + 0.23, top - 0.23)
            self.labels[1].move_to([label_x, label_y, 0])

    def arrow(self, end, color=EXAMPLE, start=(0, 0), matrix=I):
        start_point, end_point = self.point(start, matrix), self.point(end, matrix)
        kwargs = dict(color=color, stroke_width=4.8 if not self.mini else 3,
                      max_tip_length_to_length_ratio=0.22, tip_length=0.19 if not self.mini else 0.12)
        if start == (0, 0):
            return Vector(end_point - start_point, **kwargs).shift(start_point)
        return Arrow(start_point, end_point, buff=0, **kwargs)

    def dot(self, at=(0, 0), matrix=I, color=INK):
        return Dot(self.point(at, matrix), color=color, radius=0.054 if self.mini else 0.075)

    def polygon(self, vertices, matrix=I, opacity=0.21):
        return Polygon(
            *(self.point(vertex, matrix) for vertex in vertices),
            color=SHAPE, stroke_width=3 if not self.mini else 2.2,
            fill_color=SHAPE, fill_opacity=opacity,
        )

    def line(self, start, end, color=BLUE, matrix=I):
        return Line(self.point(start, matrix), self.point(end, matrix), color=color, stroke_width=3)

    def label(self, tex, position, color=INK, delta=(0, 0.28)):
        label = formula(tex, size=29 if not self.mini else 22, color=color)
        return label.move_to(self.point(position) + np.array([*delta, 0]))

    def warp(self, scene, *pairs, matrix=A, run_time=3.0):
        tracker = ValueTracker(0)
        self.base.add_updater(lambda _base: self.update_grid(intermediate(tracker.get_value(), matrix)))
        try:
            scene.play(tracker.animate.set_value(1), *(Transform(a, b) for a, b in pairs),
                       run_time=run_time, rate_func=smooth)
        finally:
            self.base.clear_updaters()
        self.update_grid(matrix)


class Lesson(Scene):
    scene_index = 0

    def construct(self):
        name, self.topic, self.beats = SCENES[self.scene_index]
        self.beat_index = 0
        self.target_time = 0.0
        self.scene_origin = self.renderer.time
        self.add_footer()
        self.animate_lesson()
        if self.beat_index != len(self.beats):
            raise ValueError(f"{name} omitted a configured visual beat.")

    @contextmanager
    def beat(self, name):
        expected, seconds = self.beats[self.beat_index]
        if name != expected:
            raise ValueError(f"Expected {expected}, got {name}")
        self.beat_start = self.target_time
        self.beat_index += 1
        self.target_time += seconds
        yield
        remaining = self.target_time - (self.renderer.time - self.scene_origin)
        if remaining < -0.5 / config.frame_rate:
            raise ValueError(f"Visual beat {name} overran by {-remaining:.3f} seconds.")
        self.wait_frames(remaining)

    def hold_until(self, seconds):
        """Hold until the given offset within the current visual beat."""
        self.wait_frames(self.scene_origin + self.beat_start + seconds - self.renderer.time)

    def wait_frames(self, remaining):
        frames = round(remaining * config.frame_rate)
        if frames > 0:
            self.wait(frames / config.frame_rate, frozen_frame=True)

    def add_footer(self):
        part = f"{self.scene_index + 1:02}  /  {len(SCENES):02}"
        footer = VGroup(
            rule((-7.28, -3.58), (7.28, -3.58)),
            place_left(words(part, 18, MUTED, "BOLD"), -7.28, -3.98),
            place_left(words("LINEAR ALGEBRA AND CALCULUS", 17, MUTED), -5.94, -3.98),
        )
        for i in range(len(SCENES)):
            color = BLUE if i == self.scene_index else BORDER
            segment = Rectangle(width=0.43, height=0.034, stroke_width=0,
                                fill_color=color, fill_opacity=1)
            footer.add(segment.move_to([4.63 + i * 0.475, -3.98, 0]))
        self.add(footer)

    def add_heading(self):
        self.add(
            place_left(words(self.topic, 41, INK, "SEMIBOLD", 11), -7.28, 3.62),
            words("M3", 23, BLUE, "BOLD").move_to([6.94, 3.64, 0]),
            rule((-7.28, 3.04), (7.28, 3.04)),
        )

    def board(self, plot):
        self.add_heading()
        backdrop = box(PANEL_BOUNDS)
        self.add(plot.base, backdrop)
        return backdrop

    def reveal(self, *objects, duration=0.8):
        self.play(AnimationGroup(*(FadeIn(obj, shift=np.array([0, 0.10, 0])) for obj in objects),
                                 lag_ratio=0.12), run_time=duration)
