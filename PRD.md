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
| R3 | Python integrated into the presentation | `src/analysis.py` computes indices and draws a chart; `src/build.py` generates slides 4, 6, 7, 8, 9 and 10 from `data/data.json`; slide 8 is an animation whose data come from Python |
| R4 | 3D element (Three.js) | 3D "data city" of 30 columns that morphs per slide, plus a CSS-3D cube with coins on the title slide |
| R5 | Roughly 10 slides, not 30 | 11 slides |
| R6 | Single self-contained HTML file | `index.html` (Three.js and fonts are embedded) |
| R7 | GitHub: README with screenshots, PRD, prompts, several pushes | This repository |

## 4. Slide outline
1. Title and three headline numbers (cumulative prices, apartment price multiple, wage multiple)
2. Inflation 1995–2024 (3D bar chart)
3. Apartment price in "average salaries" (86 → 173)
4. Rents by city, rent index vs inflation *(Python-generated)*
5. Where household money goes, CBS Household Expenditure Survey 2023 (3D donut)
6. Top vs bottom income decile: ownership, renting, rent paid *(Python-generated)*
7. Python analysis: CPI vs wages vs apartment prices, 2000 = 100
8. Animated race of the three indices with a savings model: play/pause, scrubber, speed *(Python data, JS canvas)*
9. Israel vs OECD and wages vs prices *(Python-generated)*
10. Levers for the state and the market, for discussion *(Python-generated)*
11. Summary: recap, an interactive what-if calculator (savings rate, down payment, wage growth) and three levels of action (family, market, state) *(Python-generated, JS calculator)*

Every slide has its own 3D dataset and camera position in the Three.js scene behind the content.

## 5. Non-functional
- RTL and BiDi: numbers and years wrapped in `<bdi>`.
- Works in current Chrome/Safari; no console errors.
- Readable at 1600×900; navigation works with keyboard and mouse.
- Data provenance is stated on every slide with a badge (official / press report / rounded / model / discussion) and a source line: the CPI series, the 2024 dwelling price and the CBS 2023 survey are official; rents, OECD and wage-growth figures come from press reports; the 2000–2020 apartment prices and all wage points are rounded and unverified (`data/data.json` → `sources`).
- Each content slide has a one-sentence takeaway under the title, and footnotes sit on a translucent plate so they stay legible over the 3D scene.

## 5b. Mobile
- Responsive layout at phone width; swipe finger right = next, left = previous; swipes ignore sliders/buttons and vertical scrolling.

## 6. Out of scope
Live data fetching, user accounts, mobile-specific layout, translation to other languages.

## 7. Acceptance checks
- Open `index.html`: 10 slides, buttons and arrow keys navigate, no console errors.
- `python src/analysis.py && python src/build.py` regenerates the generated slides idempotently (run twice: no diff).
- Numbers on slide 7 equal `build/analysis.json`; the race on slide 8 plays `build/race.json`.
- Every inline script passes `node --check`; the console is empty on load.
