# 06 — Better summary slide, mobile layout, swipe direction

**Prompt 11 (Hebrew):** "בשקופית סיכום אני רוצה שתציע דרכים איך להתמודד עם הבעיה, כי הסיכום בסוף לא נראה הכי וואו"
→ The summary slide was rebuilt: an interactive what-if calculator (sliders for savings rate, down payment and real wage growth; live years of saving next to the 2000 and 2024 values; the savings rate needed to return to the 2000 level), three levels of action (family, market, state) tied to the CBS figures, and a new 3D dataset whose third column follows the calculator. The old policy slide (10) was retitled "levers for the state and the market" so the two slides do not repeat each other. The first layout overflowed (stat chips, closing question, long texts); it was cut down until it fit at 1600×900 and 1366×768.

**Prompt 12 (Hebrew, sent mid-task):** "התאמה לנייד שיהיה רספוניסיבי. בנוסף ההחלקה בנייד ימינה גולל שמאלה והחלקה שמאלה גוללת ימינה, תתקן את זה."
→ Swipe: the direction was reversed (finger right = next, left = previous, book-style for RTL) and the transition wipe now follows the finger. I read the request as "make the slide follow the finger"; if the opposite was meant it is a one-character change in the touch handler (`dx>0` → `dx<0`). Swipes now ignore sliders, buttons and mostly-vertical moves.
→ Mobile: at 375 px the original media query was not enough: flex children shrank and overlapped, the control bar overflowed (the dots pushed the buttons out of the screen), and the new slides had no mobile rules. Fixed: no flex-shrink on slide children, dots hidden on phones, single-column grids for the new components.

**Verification**
- Emulated 375×812 in the app browser: no horizontal overflow on any of the 11 slides; control bar fits; slides scroll vertically.
- Swipe tested with synthetic touch events: right → next, left → previous, a 15 px move does nothing.
- Not tested on a physical phone, and the 3D scene is heavy on weak phones (it is dimmed on small screens).
