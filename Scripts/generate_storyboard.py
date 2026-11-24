"""Build the two-page storyboard with ReportLab."""
from math import atan2, cos, sin

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle

from pipeline import ROOT, base_timeline
from Code.config import STUDENT_ID, STUDENT_NAME, SUBTITLE, TITLE
from Code.math_utils import UNIT_SQUARE, mapped, verify_math

NAVY = colors.HexColor("#111D33")
DIM = colors.HexColor("#405570")
BLUE = colors.HexColor("#125B80")
PAD = colors.HexColor("#E9F0F8")
LINE = colors.HexColor("#D7E3EF")
GREEN = colors.HexColor("#137654")
RED = colors.HexColor("#AF334C")
PURPLE = colors.HexColor("#7551CD")
WIDTH, HEIGHT = A4
MARGIN = 43
BODY = ParagraphStyle("Body", fontName="Helvetica", fontSize=10, leading=14,
                      textColor=NAVY, alignment=TA_LEFT)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=9.1, leading=12.7)
TABLE_TEXT = ParagraphStyle("Table", parent=SMALL, fontSize=9.45, leading=12.8)
TABLE_HEAD = ParagraphStyle("Header", parent=TABLE_TEXT, fontName="Helvetica-Bold",
                            textColor=colors.white)

BEATS = (
    ("Hook and context",
     "Reveal the title and student information. Stretch and shear a grid and move its arrows and unit square together.",
     "Ask whether a matrix can describe how an entire space moves."),
    ("From vectors to linear maps",
     "Build a tip-to-tail sum and a scaled arrow. Compare the routes through addition and scaling on the grid.",
     "Explain both rules of linearity. Use a scalar of zero to show why the origin is fixed."),
    ("Follow the basis vectors",
     "Color the first matrix column green and the second red. Follow each basis arrow, then apply the same map to the grid.",
     "Read the two transformed basis vectors from the columns. Preserve the input coefficients to find any image."),
    ("Worked example",
     "Draw two green steps and one red step. Transform that path and the yellow result, then highlight each matrix row.",
     "Compute the image of (2, 1) by combining columns and then verify it by row-by-column multiplication."),
    ("Interpret the geometry",
     "Move the unit square into a parallelogram. Trace parallel lines and preview rotation, reflection, scaling and shearing.",
     "Connect the determinant to area and relate linear maps to graphics, robotics and engineering."),
    ("Summary and credits",
     "Reveal three takeaways, references, software credits and student details.",
     "Summarize the role of a matrix, its columns and linear combinations. Close with the spatial interpretation."),
)


def paragraph(pdf, text, x, top, width, style=BODY):
    block = Paragraph(text, style)
    _, height = block.wrap(width, 800)
    block.drawOn(pdf, x, top - height)
    return top - height


def label(pdf, text, x, y):
    pdf.setFillColor(BLUE)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(x, y, text)


def text(pdf, value, x, y, size=11, font="Helvetica", color=NAVY):
    pdf.setFillColor(color)
    pdf.setFont(font, size)
    pdf.drawString(x, y, value)


def footer(pdf, page):
    pdf.setStrokeColor(LINE)
    pdf.line(MARGIN, 47, WIDTH - MARGIN, 47)
    text(pdf, "M3  /  LINEAR ALGEBRA AND CALCULUS", MARGIN, 31, 8, "Helvetica-Bold", DIM)
    text(pdf, f"{page} / 2", WIDTH - MARGIN - 21, 31, 8, "Helvetica-Bold", DIM)


def clock(seconds):
    minutes, remainder = divmod(seconds, 60)
    suffix = ".5" if remainder % 1 else ""
    return f"{int(minutes)}:{int(remainder):02}{suffix}"


def first_page(pdf, timeline):
    pdf.setFillColor(NAVY)
    pdf.rect(0, HEIGHT - 179, WIDTH, 179, fill=1, stroke=0)
    text(pdf, "M3 PROJECT  /  STORYBOARD", MARGIN, HEIGHT - 48, 11, "Helvetica-Bold",
         colors.HexColor("#94DBFB"))
    text(pdf, TITLE, MARGIN, HEIGHT - 91, 27, "Helvetica-Bold", colors.white)
    text(pdf, SUBTITLE, MARGIN, HEIGHT - 118, 14, color=colors.HexColor("#D0DBEA"))
    text(pdf, f"{STUDENT_NAME}  /  {STUDENT_ID}", MARGIN, HEIGHT - 150, 10, color=colors.white)

    label(pdf, "LEARNING OBJECTIVE", MARGIN, HEIGHT - 210)
    paragraph(pdf, "By the end, second-year BTech students can describe how a matrix changes the "
              "plane, read transformed basis vectors from its columns, and derive matrix-vector "
              "multiplication from linearity.", MARGIN, HEIGHT - 220, WIDTH - 2 * MARGIN)
    label(pdf, "SIX-SCENE TIMELINE", MARGIN, HEIGHT - 286)

    rows = [[Paragraph(value, TABLE_HEAD) for value in ("Time / Scene", "On screen", "Narration")]]
    for scene, (heading, visual, narration) in zip(timeline["scenes"], BEATS, strict=True):
        start, end = scene["start"], scene["start"] + scene["duration"]
        time = f"{clock(start)} - {clock(end)}"
        rows.append([Paragraph(f"<b>{time}</b><br/>{heading}", TABLE_TEXT),
                     Paragraph(visual, TABLE_TEXT), Paragraph(narration, TABLE_TEXT)])
    widths = [124, 185, WIDTH - 2 * MARGIN - 309]
    table = Table(rows, colWidths=widths)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAD, colors.white]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LINEBELOW", (0, 1), (-1, -1), 0.45, LINE),
    ]))
    _, height = table.wrap(WIDTH, HEIGHT)
    table.drawOn(pdf, MARGIN, HEIGHT - 300 - height)
    footer(pdf, 1)
    pdf.showPage()


def arrow(pdf, start, end, color):
    pdf.setStrokeColor(color)
    pdf.setFillColor(color)
    pdf.setLineWidth(2.2)
    pdf.line(*start, *end)
    angle = atan2(end[1] - start[1], end[0] - start[0])
    tip = pdf.beginPath()
    tip.moveTo(*end)
    for turn in (-0.55, 0.55):
        tip.lineTo(end[0] - 9 * cos(angle + turn), end[1] - 9 * sin(angle + turn))
    tip.close()
    pdf.drawPath(tip, fill=1, stroke=0)


def diagram(pdf, left, bottom, transformed):
    width, height = 244, 132
    pdf.setFillColor(PAD)
    pdf.roundRect(left, bottom, width, height, 9, fill=1, stroke=0)
    label(pdf, "AFTER APPLYING A" if transformed else "BEFORE APPLYING A", left + 15, bottom + 112)

    def point(p):
        return left + 47 + p[0] * 27, bottom + 32 + p[1] * 27

    pdf.setLineWidth(0.45)
    pdf.setStrokeColor(LINE)
    for x in range(-1, 7):
        pdf.line(*point((x, -0.5)), *point((x, 2.55)))
    for y in range(3):
        pdf.line(*point((-1, y)), *point((6.35, y)))
    pdf.setStrokeColor(DIM)
    pdf.line(*point((-1, 0)), *point((6.35, 0)))
    pdf.line(*point((0, -0.5)), *point((0, 2.55)))

    def image(p):
        return mapped(p) if transformed else p

    shape = pdf.beginPath()
    shape.moveTo(*point(image(UNIT_SQUARE[0])))
    for vertex in UNIT_SQUARE[1:]:
        shape.lineTo(*point(image(vertex)))
    shape.close()
    pdf.setFillColor(colors.HexColor("#DCCFFC"))
    pdf.setStrokeColor(PURPLE)
    pdf.setLineWidth(1.3)
    pdf.drawPath(shape, fill=1, stroke=1)
    arrow(pdf, point((0, 0)), point(image((1, 0))), GREEN)
    arrow(pdf, point((0, 0)), point(image((0, 1))), RED)
    arrow(pdf, point((0, 0)), point(image((2, 1))), colors.HexColor("#876109"))
    text(pdf, "(5, 1)" if transformed else "(2, 1)", *point((5.21 if transformed else 2.22, 1.22)),
         9, "Helvetica-Bold", DIM)


def second_page(pdf):
    label(pdf, "MATHEMATICAL NOTES", MARGIN, HEIGHT - 64)
    text(pdf, "Why the columns tell the whole story", MARGIN, HEIGHT - 100, 23, "Helvetica-Bold")
    line_width = WIDTH - 2 * MARGIN
    paragraph(pdf, "Write each input as a combination of the standard basis vectors. For a linear "
              "map, the same coefficients act on the images of those vectors.", MARGIN, HEIGHT - 121,
              line_width)
    diagram(pdf, MARGIN, HEIGHT - 309, False)
    diagram(pdf, WIDTH - MARGIN - 244, HEIGHT - 309, True)
    label(pdf, "MAIN MAP AND WORKED EXAMPLE", MARGIN, HEIGHT - 338)
    math_rows = (
        "<b>Read the columns.</b> A = [[2, 1], [0, 1]]. Its first column is Ae<sub>1</sub> = (2, 0) "
        "and its second is Ae<sub>2</sub> = (1, 1).",
        "<b>Combine.</b> v = (2, 1) = 2e<sub>1</sub> + e<sub>2</sub>, so Av = "
        "2(2, 0) + (1, 1) = (5, 1).",
        "<b>Check by rows.</b> Av = (2 × 2 + 1 × 1, 0 × 2 + 1 × 1) = (5, 1).",
        "<b>Generalize.</b> T(x, y) = x(2, 0) + y(1, 1) = (2x + y, y).",
        "<b>Use linearity.</b> T(u + v) = T(u) + T(v) and T(cu) = cT(u). "
        "Setting c = 0 gives T(0) = 0.",
        "<b>Read the shape.</b> The square maps to (0, 0), (2, 0), (3, 1) and (1, 1). Its area is 2.",
    )
    y = HEIGHT - 350
    for row in math_rows:
        y = paragraph(pdf, row, MARGIN, y, line_width) - 7

    label(pdf, "REFERENCES AND DISCLOSURE", MARGIN, y - 14)
    sources = (
        '<link href="https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/'
        'lecture-30-linear-transformations-and-their-matrices/" color="#125B80">MIT OpenCourseWare '
        '18.06, Lecture 30, Linear transformations and their matrices</link><br/>'
        '<link href="https://www.3blue1brown.com/lessons/linear-transformations/" color="#125B80">'
        '3Blue1Brown, Linear transformations and matrices</link><br/>'
        '<link href="https://docs.manim.community/" color="#125B80">Manim Community documentation</link>'
    )
    y = paragraph(pdf, sources, MARGIN, y - 24, line_width, SMALL)
    paragraph(pdf, "OpenAI Codex assisted with the production plan, script, animation code and debugging. "
              "The project uses original rendered visuals and exports a silent video for a separately "
              "recorded voice-over.", MARGIN, y - 10,
              line_width, SMALL)
    footer(pdf, 2)
    pdf.showPage()


def main():
    verify_math()
    timeline = base_timeline()
    output = ROOT / "Storyboard.pdf"
    pdf = canvas.Canvas(str(output), pagesize=A4, invariant=True)
    pdf.setTitle(TITLE + " | Storyboard")
    pdf.setAuthor(STUDENT_NAME)
    first_page(pdf, timeline)
    second_page(pdf)
    pdf.save()
    print(output)


if __name__ == "__main__":
    main()
