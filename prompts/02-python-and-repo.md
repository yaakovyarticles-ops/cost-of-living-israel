# 02 — Python integration and repository

**Prompt 5 (Hebrew, sent mid-task):** "אני רוצה שתשלב בה גם פייתון ושתעלה את הגופנים גם לגיטאהב"
→ (a) Python: `data/data.json` holds the figures, `src/analysis.py` computes CPI/wage/price indices and a matplotlib chart, `src/build.py` injects a new slide between `<!--PY:START-->` and `<!--PY:END-->` markers in `index.html`.
→ (b) Fonts: the five base64 `@font-face` blobs were decoded into `fonts/*.ttf` (the deck stays self-contained; the files are also in the repo).

**Verification steps done by the LLM**
- Served the folder locally and screenshotted all 6 slides with headless Chrome; checked console for errors (none).
- Found and fixed a BiDi problem on slide 5: signed percentages were rendered as `%26.1+`; wrapped them in `<bdi dir="ltr">`.
- Found a stale slide counter (`1 / 5`) after adding a slide; changed to `1 / 6`.
- Screenshots taken too early caught mid-transition frames; retaken with a longer virtual-time budget.

**Critical notes**
- Figures are rounded and unverified against CBS; the deck says so on each slide.
- Only Assistant is clearly under an open license; see `fonts/README.md`.
