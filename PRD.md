# PRD — "Cost of Living in Israel, 1995–2024" (interactive HTML presentation)

## 1. Goal
A single-file, Hebrew (RTL) presentation that explains how prices, wages and housing costs moved in Israel over 30 years, and why the apartment-to-salary ratio is the real issue. It must work by double-clicking the file, with no build step and no network.

## 2. Audience
Course instructor and classmates (AI course, semester A). Non-economists: the message has to be clear in about 3 minutes.

## 3. Requirements (from the assignment)
| # | Requirement | How it is met |
|---|---|---|
| R1 | Topic of personal interest | Cost of living / housing in Israel |
| R2 | JavaScript: buttons and interaction | Prev/next buttons, dots, keyboard (RTL: ← forward), `#n` deep links, auto-play with `?auto` |
| R3 | Python integrated into the presentation | `src/analysis.py` computes indices and draws a chart; `src/build.py` injects the results as slide 5 |
| R4 | 3D element (Three.js) | 3D "data city" of 30 columns that morphs per slide, plus a CSS-3D cube with coins on the title slide |
| R5 | Roughly 10 slides, not 30 | 6 slides |
| R6 | Single self-contained HTML file | `index.html` (Three.js and fonts are embedded) |
| R7 | GitHub: README with screenshots, PRD, prompts, several pushes | This repository |

## 4. Slide outline
1. Title and three headline numbers (cumulative prices, apartment price multiple, wage multiple)
2. Inflation 1995–2024 (3D bar chart)
3. Apartment price in "average salaries" (86 → 173)
4. Where household money goes (3D donut)
5. Python analysis: CPI vs wages vs apartment prices, 2000 = 100
6. Summary and the closing question

## 5. Non-functional
- RTL and BiDi: numbers and years wrapped in `<bdi>`.
- Works in current Chrome/Safari; no console errors.
- Readable at 1600×900; navigation works with keyboard and mouse.
- Data are rounded illustrative figures and must be verified against CBS (lms.gov.il) and Bank of Israel before anything beyond the course.

## 6. Out of scope
Live data fetching, user accounts, mobile-specific layout, translation to other languages.

## 7. Acceptance checks
- Open `index.html`: 6 slides, buttons and arrow keys navigate, no console errors.
- `python src/analysis.py && python src/build.py` regenerates slide 5 idempotently.
- Numbers on slide 5 equal `build/analysis.json`.
