# Cost of Living in Israel, 1995–2024

An interactive Hebrew (RTL) presentation: thirty years of prices, wages and housing costs in Israel, in a single HTML file with a Three.js 3D scene, JavaScript navigation, and a slide produced by Python.

**Open it:** download the repository and double-click `index.html` (no server, no network needed).

| | |
|---|---|
| ![Title slide](docs/screenshots/slide-01.png) | ![Inflation](docs/screenshots/slide-02.png) |
| 1 · Title and three headline numbers | 2 · Annual inflation, 3D bars |
| ![Housing](docs/screenshots/slide-03.png) | ![Household spending](docs/screenshots/slide-04.png) |
| 3 · An apartment costs 86 → 173 average salaries | 4 · Where the monthly budget goes |
| ![Python analysis](docs/screenshots/slide-05.png) | ![Summary](docs/screenshots/slide-06.png) |
| 5 · **Python analysis**, index 2000 = 100 | 6 · Summary |

## The finding
Between 2000 and 2024 consumer prices rose about 1.5×, the average wage 1.9× and the average apartment 3.8×. In real terms wages gained roughly 26% while apartment prices gained about 154%, so the number of average salaries needed to buy an apartment doubled (86 → 173).

## How the requirements are met
- **JavaScript:** previous/next buttons, progress dots, keyboard (← forward in RTL), `#3` deep links, `?auto` auto-play.
- **Three.js (3D):** a "data city" of 30 columns that morphs between datasets as slides change; the title slide also has a CSS-3D cube with coins.
- **Python:** `src/analysis.py` reads `data/data.json`, computes the indices and draws `docs/charts/index_2000.png`; `src/build.py` embeds the chart and the computed numbers into slide 5.
- **Single file:** Three.js and the fonts are embedded in `index.html`. The same fonts are also stored in `fonts/` (see `fonts/README.md` for licensing notes).

## Regenerate the Python slide
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python src/analysis.py
.venv/bin/python src/build.py
```

## Repository layout
```
index.html          the presentation (open this)
PRD.md              product requirements document
prompts/            the prompts given to the LLM, per stage
src/                analysis.py (stats + chart), build.py (inject slide)
data/data.json      the figures used
docs/               screenshots and generated chart
fonts/              extracted .ttf files
```

## Process and critical review
Work was led through Claude Code in the terminal: requirements first (PRD), then an audit of the existing deck against the assignment, then Python integration, then verification by serving the page, screenshotting every slide, and reading the browser console. The prompts are in [`prompts/`](prompts/README.md).

What I corrected along the way: a BiDi bug that rendered `+26.1%` as `%26.1+`, a stale slide counter after adding a slide, and screenshots captured mid-transition.

Known limitations:
- The numbers are rounded, illustrative figures based on CBS and Bank of Israel publications; they were **not** re-verified against the official series. Verify before citing.
- The Python chart uses English labels to avoid RTL shaping issues in matplotlib.
- Only the Assistant font is clearly open-licensed; check the others before reuse.
- The original 4-chart deck was generated in an earlier session whose prompts were not saved.

## Authors
Yaakov Geppert and partner (details are in the submission form).
