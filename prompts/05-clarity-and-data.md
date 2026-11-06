# 05 — Clarity improvements and data verification

**Prompt 10 (Hebrew):** "1,2,3,4,6" — choosing from my list of suggested improvements: (1) source badges on every slide, (2) a one-line takeaway per slide, (3) more legible footnotes over the 3D scene, (4) annotated events on the race slide, (6) replace rounded data with exact CBS data.

**What was done**
- (6) Data: the annual CPI series 1995–2024 was replaced by the official series (World Bank `FP.CPI.TOTL.ZG`, CBS-based, API read in full): it differs from the earlier rounded values (e.g. 2022 is 4.4%, not 5.3%), so the inflation slide text, the cumulative figures and the 3D data were regenerated from `data/data.json`. The 2024 dwelling price was replaced by the CBS annual average (2,340.3 thousand NIS, Table 2.2). The apartment prices for 2000–2020 and all wage points could not be retrieved (CBS blocks automated downloads, OECD query returned nothing), so they stay rounded and are labelled so.
- (1) Badges: official / press report / rounded / model / discussion, per slide.
- (2) Takeaways: one sentence under every title, computed from the data where it contains numbers.
- (3) Footnotes: translucent plate with blur and higher contrast.
- (4) Race slide: event markers on the time axis and a readout of the latest event; labels are general knowledge, not data.
- `src/build.py` now also re-syncs the chart arrays hard-coded in `index.html` (SVG charts and the Three.js scene) from `data/data.json`, so one source feeds everything.

**Problems found while verifying**
- The CSS block was injected again on every build (12 copies by the time I noticed) because it had no markers; fixed and the duplicates removed.
- Each build also added whitespace after the title of every slide; fixed. Three consecutive builds now produce byte-identical output.
- Several earlier statements in the deck depended on the old rounded series ("2003–2020 the index barely moved", "highest in two decades"); they were rewritten to match the official series.
