# 04 — More animation from Three.js and Python

**Prompt 8 (Hebrew, sent mid-task):** "אני רוצה להוסיף שם יותר אנימציות מthree.js ומקוד פייתון כמו שהוא אמר. ממש לצאת מהקופסה ולתת חווית משתמש ברמה מאוד מאוד גבוהה"
→ Three.js: the "data city" scene had five datasets keyed to the first five slide indexes. Added three new datasets (rent by city, owners vs renters by decile, international gaps), three camera poses and captions, and a `data-set` attribute on every slide so the scene follows the slide's content instead of its index.
→ Python: `src/analysis.py` now builds yearly series (2000–2024) and a savings model, writes `build/race.json`, and renders `docs/charts/race.gif`. A new slide (8) plays the series as an interactive canvas animation (`src/race.js`): auto-plays on entry, play/pause, year scrubber, speed, live readouts, respects `prefers-reduced-motion`, and stops arrow keys from navigating slides while the scrubber is focused.

**Prompt 9 (Hebrew, sent mid-task):** "איך אני מפעיל גיטאהב pages והאם יש צורך בזה לפי דרישות המרצה?"
→ Answered: not required by the assignment; Settings → Pages → Deploy from a branch → `main` / root.

**Problems found while verifying**
- `node --check` on the inline scripts found two syntax errors: (a) an unescaped quote in a 3D caption added in an earlier step and already pushed, so the 3D scene was not running in the screenshots taken then; (b) my own generator collapsed `}}` sequences in the race script. Both fixed; all scripts now pass.
- Headless Chrome only renders WebGL with `--enable-unsafe-swiftshader`; screenshots were retaken with it, so the 3D scene is visible in them.
- Screenshots come from a temporary copy with CSS transitions disabled and the race paused at 2017; the deck itself is unchanged.
