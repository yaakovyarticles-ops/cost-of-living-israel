# 03 — Up-to-date data and four more slides

**Prompt 6 (Hebrew):** "כתוב שצריך 10 שקפים בערך לא?" (asked whether 6 slides meet the assignment)
→ LLM re-read the homework summary: about 10 slides is the guidance; 6 is on the low side. Proposed four additional slides (rent, deciles, international comparison, levers).

**Prompt 7 (Hebrew):** "אני מאשר, תמשוך את הנתונים העדכניים מאיפה שצריך. קודם נעבוד על המצגת אחר כך נעלה לגיטאהב"
→ Data search and reading:
- CBS Household Expenditure Survey 2023 press release (PDF, read in full): spending shares, deciles, housing tenure.
- Globes (rents Q3 2024, 2024 wage growth), Times of Israel (OECD 2022 price level), Globes (food vs OECD, 2017 data).
→ Result: `data/data.json` extended with sourced figures; the old household-spending split (26/16/14/10/5/29, unsourced) replaced by the CBS 2023 split.
→ `src/build.py` rewritten to generate slides 4, 6, 7, 8, 9; Three.js slide-to-dataset mapping fixed with `data-set` attributes (it was keyed to the slide index and would have broken with 10 slides).

**Verification**
- Rebuilt twice (idempotent), 10 `<section>`s, no console errors.
- Fixed wording that contradicted the data ("more than a third" for 55.4%, now "more than half").
- Screenshots: the 3D scene renders slowly in headless Chrome, so shots were taken from a temporary copy with animations disabled (the deck itself is unchanged).

**Not verified**
- Rent, OECD, food and wage figures come from press reports, not the primary releases; the food-vs-OECD figure is from 2017.
- A 2025 annual inflation figure (2.6%, Dec-on-Dec) is in the footnote of slide 2 only, from press reports.
