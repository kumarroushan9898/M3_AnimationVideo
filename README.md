# What Matrices Really Do to Space

**Understanding Linear Transformations Visually**

Linear Algebra and Calculus (M3) · Second-year BTech · English

**Student** Kumar Roushan

**Student ID** E25B071257

Follow a coordinate grid as it stretches and shears. The motion reveals what the matrix columns mean, why a linear transformation fixes the origin, and how multiplying a matrix by a vector combines the transformed basis vectors.

## Learning objectives

- Explain the effect of a matrix on the two-dimensional plane.
- Read the images of the standard basis vectors from the matrix columns.
- Derive matrix-vector multiplication using additivity and scalar multiplication, then check it with row arithmetic.

## Scene guide

| Target time | Scene | What to watch for |
| --- | --- | --- |
| 0:00–0:30 | Hook | A single map stretches the blue grid and carries the purple square and the colored arrows with it. |
| 0:30–1:15 | Concept | Tip-to-tail addition and scaling lead to the two rules of linearity. Scaling by zero explains the fixed origin. |
| 1:15–2:05 | Basis vectors | The green and red arrows reveal the first and second columns of A. Their images determine every output. |
| 2:05–3:50 | Worked example | Two green basis steps and one red step land at (5, 1). The two matrix rows verify that result. |
| 3:50–4:35 | Interpretation | A unit square becomes a parallelogram. Four more maps illustrate rotation, reflection, scaling and shearing. |
| 4:35–5:00 | Summary and credits | Three takeaways, student and software credits, and references. |

The storyboard and MP4 chapters follow the fixed scene times above. The MP4 also includes selectable English captions from the supplied SRT.

## Mathematical derivation

For column vectors, let

    A = [[2, 1],
         [0, 1]]

The standard basis is e₁ = (1, 0) and e₂ = (0, 1). Multiplying by e₁ selects the first column, (2, 0). Multiplying by e₂ selects the second column, (1, 1). Additivity and scalar multiplication let us keep the input coefficients.

$$
\begin{aligned}
T(u+v)&=T(u)+T(v), & T(cu)&=cT(u),\\
T(0)&=T(0u)=0T(u)=0,\\
T(x,y)&=x(2,0)+y(1,1)=(2x+y,y).
\end{aligned}
$$

For **v = (2, 1)**, apply the same linear combination to the new basis vectors.

$$
\begin{aligned}
v&=2e_1+e_2,\\
Av&=2Ae_1+Ae_2=2(2,0)+(1,1)=(5,1),\\
Av&=(2\cdot2+1\cdot1,\ 0\cdot2+1\cdot1)=(5,1).
\end{aligned}
$$

The square's vertices map to (0, 0), (2, 0), (3, 1), and (1, 1), in boundary order. The determinant is 2, so A is invertible and the square's area doubles. A linear map can send a line to a line or collapse it to a point. Here invertibility keeps distinct parallel lines distinct and parallel.

## Install on macOS

Install the free command-line tools with [Homebrew](https://brew.sh/). The project was built with Python 3.14.7.

```bash
brew install python@3.14 pkgconf cairo pango ffmpeg poppler
brew install --cask basictex
export PATH="/Library/TeX/texbin:$PATH"
sudo tlmgr update --self
sudo tlmgr install standalone preview dvisvgm amsmath amsfonts babel-english \
  doublestroke setspace tipa relsize wasy wasysym physics xcolor microtype
bash Scripts/setup.sh
source .venv/bin/activate
```

An existing TeX Live or MacTeX installation also works when `latex`, `dvisvgm`, and the template packages are available. The scripts also recognize TinyTeX installed under `.build/tex/TinyTeX`. Set `M3_PYTHON` when running setup to choose another supported Python interpreter.

## Rebuild

```bash
# Optional silent preview at 960 × 540 and 30 fps.
python Scripts/render_preview.py

# Build and verify the silent MP4.
python Scripts/render_video.py
python Scripts/verify_video.py

# Optional storyboard with the fixed scene times.
python Scripts/generate_storyboard.py
```

The build exports a silent five-minute `Video.mp4` for recording your own voice-over. The preview is saved as `VisualPreview.mp4`. Manim uses the scene timings in the source code. FFmpeg packages the chapters, the English captions in `Subtitles/narration.srt`, and the embedded cover.

## Repository guide

| Path | Contents |
| --- | --- |
| `Video.mp4` | Locally generated silent 1920 × 1080, 60 fps H.264 export with English captions |
| [Thumbnail.jpg](Thumbnail.jpg) | Opening title image and embedded video cover |
| `Storyboard.pdf` | Two-page scene plan and illustrated derivation |
| `Code/` | Manim entry point, six scenes, shared plotting code and verified math |
| `narration.md` | Local voice-over script, excluded by Git |
| `Subtitles/` | Synchronized SRT |
| `Scripts/` | Setup, PDF, preview, production and verification |
| `Tests/` | Numeric, symbolic and animation-map tests |
| `manim.cfg` and `requirements.txt` | Render configuration and pinned Python dependencies |

Python coordinates the pipeline. Manim CE, NumPy and LaTeX produce the visuals. SymPy verifies the mathematical claims. FFmpeg and FFprobe process and inspect media. ReportLab produces the storyboard. Git records the project history.

## Troubleshooting

- For a missing `standalone.cls` or other TeX packages, rerun the `tlmgr install` command and confirm `latex` and `dvisvgm` are on the path.
- For stale partial renders, remove `.build/final/manim` or `.build/visual-preview/manim` and rerun the corresponding command.
- Run `python -m unittest discover -s Tests -v` from the project root to check the linear algebra independently.

## Public GitHub submission

The video credits use the student details in `Code/config.py`. The production pipeline keeps the MP4 below GitHub's 100 MiB individual file limit. [M3_AnimationVideo](https://github.com/kumarroushan9898/M3_AnimationVideo)

Push committed changes from the project repository.

```bash
git push -u origin main
```
