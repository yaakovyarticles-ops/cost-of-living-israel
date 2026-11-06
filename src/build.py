"""Generate the data-driven slides of index.html with Python.

Run src/analysis.py first. Idempotent: every generated block lives between
<!--PY:name:START--> / <!--PY:name:END--> markers and is rebuilt on each run.

Generated blocks
  css        small stylesheet for the bar rows (in <head>)
  rent       slide: rents by city (from data.json)
  deciles    slide: top vs bottom income decile (from data.json)
  analysis   slide: indices chart + numbers computed by analysis.py
  race       slide: animated race of the three indices + savings model (Python JSON, JS canvas)
  oecd       slide: international comparison and wages
  policy     slide: levers (qualitative)
"""
import base64
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
html_path = ROOT / "index.html"
html = html_path.read_text(encoding="utf-8")
data = json.loads((ROOT / "data" / "data.json").read_text(encoding="utf-8"))
st = json.loads((ROOT / "build" / "analysis.json").read_text(encoding="utf-8"))
img = base64.b64encode((ROOT / "docs" / "charts" / "index_2000.png").read_bytes()).decode()


def fmt(n):
    return f"{n:,}"


def bar_row(label, value, vmax, text, color):
    w = max(2, round(value / vmax * 100))
    return (f'<div class="brow"><span class="bl">{label}</span>'
            f'<span class="bt"><i style="width:{w}%;background:{color}"></i></span>'
            f'<b class="bv"><bdi dir="ltr">{text}</bdi></b></div>')


# ---------- css ----------
css = """<!--PY:css:START--><style>
.brow{display:grid;grid-template-columns:7.5em 1fr 4.6em;align-items:center;gap:.8em;margin:.7em 0;font-size:1.02em}
.brow .bt{display:block;height:1.15em;border-radius:.6em;background:rgba(255,255,255,.07);overflow:hidden;direction:rtl}
.brow .bt i{display:block;height:100%;border-radius:.6em}
.brow .bv{text-align:start}
.bgroup{margin-top:1.2em}.bgroup h4{margin:0 0 .2em;font-weight:700;opacity:.9}
.pair{display:flex;gap:1.1em;font-size:.82em;opacity:.85;margin-bottom:.6em}.pair span i{display:inline-block;width:.8em;height:.8em;border-radius:50%;margin-inline-end:.4em}
.bigstats{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4vw;margin-top:1.2em}
.bigstats .stat{padding:1.4em 1.2em}.bigstats .stat b{display:block;font-size:3.1em;line-height:1}
.bigstats .stat span{display:block;margin-top:.6em}
.levers{display:grid;grid-template-columns:repeat(2,1fr);gap:1.4vw;margin-top:1.2em}
.levers .glass{padding:1.2em 1.4em}.levers h3{margin:0 0 .4em}.levers p{margin:0}
#raceCv{width:100%;height:clamp(220px,36vh,340px);display:block}
.rctl{display:flex;align-items:center;gap:.8em;margin-top:.7em;direction:ltr}
.rctl input[type=range]{flex:1;accent-color:#ffc857}
.rbtn,.rctl select{background:rgba(255,255,255,.1);color:inherit;border:1px solid rgba(255,255,255,.18);border-radius:.7em;padding:.3em .8em;font:inherit;cursor:pointer}
.rbtn:hover,.rctl select:hover{background:rgba(255,255,255,.18)}
.rread b.big{font-size:2.1em;line-height:1}
.badge{display:inline-block;margin-inline-start:.9em;padding:.12em .7em;border-radius:2em;font-size:.82em;font-weight:700;border:1px solid currentColor;vertical-align:middle;letter-spacing:.01em}
.badge.ok{color:#3ddbc4;background:rgba(61,219,196,.12)}.badge.press{color:#ffc857;background:rgba(255,200,87,.12)}
.badge.est{color:#ff8f8f;background:rgba(255,107,107,.12)}.badge.mdl{color:#b3a8ff;background:rgba(139,124,255,.14)}.badge.talk{color:#c9ccea;background:rgba(255,255,255,.08)}
.chips{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2vw;margin:.6em 0 .2em}
.chip{display:flex;align-items:baseline;gap:.7em;padding:.5em 1em}.chip b{font-size:1.9em;line-height:1}.chip span{font-size:.92em;opacity:.9}
.calc h3{margin:0 0 .4em;font-size:1em}.crow{display:grid;grid-template-columns:8.6em 1fr 3.6em;align-items:center;gap:.7em;margin:.25em 0;font-size:.92em;direction:rtl}
.crow input{direction:ltr;accent-color:#ffc857;width:100%}.crow b{text-align:start;direction:ltr}
.cbars{margin-top:.7em}.cbar{display:grid;grid-template-columns:6.4em 1fr 3em;align-items:center;gap:.6em;margin:.3em 0;font-size:.92em}
.cbar .bt{display:block;height:1em;border-radius:.6em;background:rgba(255,255,255,.07);overflow:hidden;direction:rtl}.cbar .bt i{display:block;height:100%;border-radius:.6em;transition:width .25s}
.cnote{margin-top:.5em;font-size:.9em;line-height:1.4}.cnote .rbtn{padding:.1em .7em;font-size:.9em;margin-inline-start:.5em}.cnote b{color:#ffc857}
.levels li{align-items:flex-start;font-size:.95em}.levels b{color:#ffc857}
html{touch-action:pan-y}
@media(max-width:860px){
 .bigstats,.levers{grid-template-columns:1fr}.bigstats .stat b{font-size:2.3em}
 .brow{grid-template-columns:5.4em 1fr 3.5em;font-size:.95em;gap:.5em}
 .crow{grid-template-columns:6.6em 1fr 3em;gap:.5em}.cbar{grid-template-columns:5.6em 1fr 2.6em}
 #raceCv{height:230px}.rctl{gap:.5em}
 .take{font-size:1em;margin:.3em 0 .6em}.badge{display:block;margin:.5em 0 0;width:fit-content}
 .src{font-size:.78em;padding:.5em .7em}
 .slide>*{flex-shrink:0}.dots{display:none}.controls{gap:.9rem}
 .levels li,.points li{font-size:.98em}
}
.take{margin:.2em 0 .5em;max-width:46em;font-size:1.08em;line-height:1.5;color:rgba(233,236,255,.86)}
.take b{color:#ffc857}
.src{background:rgba(10,12,32,.66);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);padding:.4em .9em;border-radius:.7em;color:rgba(233,236,255,.86)!important}
</style><!--PY:css:END-->"""

# ---------- rent ----------
r = data["rent_4room_q3_2024_nis"]
vmax = max(v for _, v in r["items"])
he_city = {"Tel Aviv": "תל אביב", "Jerusalem": "ירושלים", "National average": "ממוצע ארצי",
           "Haifa": "חיפה", "Beersheba": "באר שבע"}
rows = "".join(bar_row(he_city[n], v, vmax, fmt(v), "#ff6b6b" if n == "National average" else "#ffc857")
               for n, v in r["items"])
rent = f"""<!--PY:rent:START-->
<section class="slide" data-title="שכירות" data-set="5">
  <div class="tag rv">פרק ב · שכירות</div>
  <h2 class="rv">מי שלא קנה, <em>שוכר</em> ביוקר</h2>
  <div class="cols">
    <div class="chart-box glass rv">
      <div class="pair"><span>שכר דירה חודשי, דירת <bdi>4</bdi> חדרים, רבעון <bdi>3</bdi> <bdi>2024</bdi> (ש"ח)</span></div>
      {rows}
    </div>
    <ul class="points rv">
      <li><span class="ic">₪</span><span>ממוצע ארצי לדירת <bdi>4</bdi> חדרים: <b class="num"><bdi>{fmt(5200)}</bdi></b> ש"ח בחודש; בתל אביב <bdi>{fmt(8500)}</bdi>.</span></li>
      <li><span class="ic">▲</span><span>מדד שירותי הדיור, המשקף שכר דירה, עלה ב־<bdi>{r['housing_services_index_yoy_pct']}%</bdi> בשנה, מול אינפלציה כללית של <bdi>{r['cpi_yoy_pct']}%</bdi>.</span></li>
      <li><span class="ic">%</span><span>שכר דירה הוא כ־<bdi>{r['rent_share_of_cpi_pct']}%</bdi> ממדד המחירים לצרכן, ולכן הוא משפיע על כל המדד.</span></li>
    </ul>
  </div>
  <div class="src">מקור: הלמ"ס, כפי שפורסם ב־Globes (<bdi>24.12.2024</bdi>).</div>
</section>
<!--PY:rent:END-->"""

# ---------- deciles ----------
d = data["deciles_2023"]
tb = d["top_vs_bottom"]
def pair_rows(label, key, vmax):
    top, bot = tb[key]
    return (f'<div class="bgroup"><h4>{label}</h4>'
            + bar_row("עשירון עליון", top, vmax, f"{top}%", "#3ddbc4")
            + bar_row("עשירון תחתון", bot, vmax, f"{bot}%", "#ff6b6b") + "</div>")
dec_rows = pair_rows("גרים בדירה בבעלותם", "owner_occupied_pct", 100) + pair_rows("גרים בדירה שכורה", "renting_pct", 100)
deciles = f"""<!--PY:deciles:START-->
<section class="slide" data-title="פערים" data-set="6">
  <div class="tag rv">פרק ג · פערים</div>
  <h2 class="rv">לא כולם מרגישים <em>אותו דבר</em></h2>
  <div class="cols">
    <div class="chart-box glass rv">{dec_rows}</div>
    <ul class="points rv">
      <li><span class="ic">×</span><span>פער ההכנסות בין העשירון העליון לתחתון: פי <b class="num"><bdi>{d['income_gap_x']}</bdi></b>. פער ההוצאות: פי <bdi>{d['spending_gap_x']}</bdi> בלבד.</span></li>
      <li><span class="ic">₪</span><span>העשירון העליון משלם שכר דירה של <bdi>{fmt(tb['monthly_rent_nis'][0])}</bdi> ש"ח, התחתון <bdi>{fmt(tb['monthly_rent_nis'][1])}</bdi>.</span></li>
      <li><span class="ic">⌂</span><span>ערך דירה ממוצעת בבעלות: כ־<bdi>3.96</bdi> מיליון ש"ח בעשירון העליון, כ־<bdi>1.51</bdi> בתחתון.</span></li>
    </ul>
  </div>
  <div class="src">מקור: הלמ"ס, סקר הוצאות משק הבית <bdi>2023</bdi> (עשירונים לפי הכנסה נטו לנפש סטנדרטית). מדד ג'יני: <bdi>{d['gini']}</bdi>.</div>
</section>
<!--PY:deciles:END-->"""

# ---------- analysis ----------
analysis = f"""<!--PY:analysis:START-->
<section class="slide" data-title="ניתוח פייתון" data-set="4">
  <div class="tag rv">פרק ד · ניתוח ב־Python</div>
  <h2 class="rv">מחירים, שכר ודירות: <em>מדד אחד</em></h2>
  <div class="cols">
    <div class="chart-box glass rv"><img src="data:image/png;base64,{img}" alt="מדד מחירים, שכר ומחיר דירה, 2000 = 100" style="width:100%;height:auto;border-radius:10px"></div>
    <ul class="points rv">
      <li><span class="ic">₪</span><span>מחירי הצריכה עלו פי <b class="num"><bdi>{st['cpi_multiple_2000_2024']}</bdi></b> מ־<bdi>2000</bdi> עד <bdi>2024</bdi>.</span></li>
      <li><span class="ic">▲</span><span>השכר עלה פי <b class="num"><bdi>{st['wage_multiple']}</bdi></b>, כלומר שינוי ריאלי של <bdi dir="ltr">{st['real_wage_change_pct']:+}%</bdi>.</span></li>
      <li><span class="ic">⌂</span><span>הדירה עלתה פי <b class="num"><bdi>{st['price_multiple']}</bdi></b>: ריאלית <bdi dir="ltr">{st['real_house_price_change_pct']:+}%</bdi>, ומ־<bdi>{st['salaries_to_buy_2000']}</bdi> ל־<bdi>{st['salaries_to_buy_2024']}</bdi> משכורות לדירה.</span></li>
    </ul>
  </div>
  <div class="src">חושב ב־Python (<bdi>src/analysis.py</bdi>) מתוך <bdi>data/data.json</bdi>; נתוני המחירים והשכר מעוגלים להמחשה, יש לאמת מול הלמ"ס.</div>
</section>
<!--PY:analysis:END-->"""


# ---------- race (animated; Python computes the data, JS draws it) ----------
race_data = (ROOT / "build" / "race.json").read_text(encoding="utf-8")
race_js = (ROOT / "src" / "race.js").read_text(encoding="utf-8")
race = f"""<!--PY:race:START-->
<section class="slide" id="raceSlide" data-title="מירוץ הדירה" data-set="4">
  <div class="tag rv">פרק ד · אנימציה שחושבה ב־Python</div>
  <h2 class="rv">המירוץ: <em>דירה מול משכורת</em></h2>
  <div class="cols">
    <div class="chart-box glass rv">
      <canvas id="raceCv" role="img" aria-label="אנימציה: מדד מחיר דירה, שכר ומחירים 2000 עד 2024"></canvas>
      <div class="rctl"><button class="rbtn" id="rPlay" aria-label="השהיה">⏸</button><input id="rRange" type="range" min="0" max="1000" value="0" aria-label="שנה"><select id="rSpeed" aria-label="מהירות"><option value="0.5">×0.5</option><option value="1" selected>×1</option><option value="2">×2</option></select></div>
    </div>
    <ul class="points rv rread">
      <li><span class="ic">◷</span><span>שנת <b class="big num" id="rYear">2000</b></span></li>
      <li><span class="ic">%</span><span>מדד (<bdi>2000 = 100</bdi>): דירה <b class="num" id="rPrice">100</b>, שכר <b class="num" id="rWage">100</b>, מחירים <b class="num" id="rCpi">100</b></span></li>
      <li><span class="ic">!</span><span id="rEvent">—</span></li>
      <li><span class="ic">⌛</span><span>שנות חיסכון למקדמה: <b class="big num" id="rSave">{st['years_to_save_2000']}</b></span></li>
    </ul>
  </div>
  <div class="src">מודל המחשה (<bdi>src/analysis.py</bdi>): חיסכון של <bdi>20%</bdi> מהשכר הממוצע עד מקדמה של <bdi>25%</bdi> ממחיר דירה ממוצעת. השנים שבין נקודות הנתונים מושלמות בקו ישר, והנתונים מעוגלים: זו המחשה ולא מדידה.</div>
  <script type="application/json" id="raceData">{race_data}</script>
  <script>{race_js}</script>
</section>
<!--PY:race:END-->"""

# ---------- oecd ----------
o = data["oecd_and_wages"]
oecd = f"""<!--PY:oecd:START-->
<section class="slide" data-title="בהשוואה בינלאומית" data-set="7">
  <div class="tag rv">פרק ה · בהשוואה</div>
  <h2 class="rv">מחירים גבוהים, <em>שכר שרץ אחריהם</em></h2>
  <div class="bigstats rv">
    <div class="stat glass"><b class="c-coral num">+<bdi>{o['price_level_vs_oecd_2022_pct']}%</bdi></b><span>רמת המחירים הכללית בישראל מעל ממוצע ה־<bdi>OECD</bdi> ב־<bdi>2022</bdi>, הגבוהה בין החברות.</span></div>
    <div class="stat glass"><b class="c-gold num">+<bdi>{o['food_vs_oecd_pct']}%</bdi></b><span>מחירי המזון מעל ממוצע ה־<bdi>OECD</bdi> (נתוני <bdi>{o['food_vs_oecd_year']}</bdi>, משרד הכלכלה). הערכות אחרות גבוהות יותר.</span></div>
    <div class="stat glass"><b class="c-teal num">+<bdi>{o['real_wage_change_2024_pct']}%</bdi></b><span>עליית השכר הריאלי ב־<bdi>2024</bdi> (נומינלית <bdi>{o['nominal_wage_change_2024_pct']}%</bdi>). בינואר <bdi>2025</bdi> השכר עלה רק <bdi>{o['wage_jan2025_yoy_pct']}%</bdi> מול אינפלציה של <bdi>{o['cpi_jan2025_yoy_pct']}%</bdi>.</span></div>
  </div>
  <div class="src">מקורות: <bdi>Times of Israel</bdi> (מדד יוקר המחיה של ה־<bdi>OECD</bdi>), <bdi>Globes</bdi> (משרד הכלכלה; הלמ"ס, <bdi>4.3.2025</bdi>). נתונים משנים שונות וסלים שונים, אין להשוות ביניהם ישירות.</div>
</section>
<!--PY:oecd:END-->"""


# ---------- summary: recap + what-if calculator + three levels of action ----------
calc_data = json.dumps({"price": data["housing"][-1]["price_kils"], "wage": data["housing"][-1]["avg_wage"],
                        "years2000": st["years_to_save_2000"], "years2024": st["years_to_save_2024"]})
summary_js = (ROOT / "src" / "summary.js").read_text(encoding="utf-8")
summary = f"""<!--PY:summary:START-->
<section class="slide" id="sumSlide" data-title="סיכום" data-set="8">
  <div class="tag rv">סיכום</div>
  <h2 class="rv">מה למדנו <em>ומה אפשר לעשות?</em></h2>
  <div class="cols">
    <div class="chart-box glass rv calc">
      <h3>מחשבון "מה אם": שנות חיסכון למקדמה</h3>
      <div class="crow"><label for="cRate">חיסכון מהשכר</label><input id="cRate" type="range" min="5" max="50" value="20"><b id="cRateV">20%</b></div>
      <div class="crow"><label for="cDown">גובה המקדמה</label><input id="cDown" type="range" min="10" max="50" value="25"><b id="cDownV">25%</b></div>
      <div class="crow"><label for="cWage">עליית שכר ריאלית</label><input id="cWage" type="range" min="0" max="60" value="0"><b id="cWageV">+0%</b></div>
      <div class="cbars">
        <div class="cbar"><span>2000</span><span class="bt"><i id="cB0" style="background:#3ddbc4"></i></span><b class="num"><bdi>{st['years_to_save_2000']}</bdi></b></div>
        <div class="cbar"><span>2024</span><span class="bt"><i id="cB1" style="background:#ff6b6b"></i></span><b class="num"><bdi>{st['years_to_save_2024']}</bdi></b></div>
        <div class="cbar"><span>התרחיש שלך</span><span class="bt"><i id="cB2" style="background:#ffc857"></i></span><b class="num" id="cV2">0</b></div>
      </div>
      <div class="cnote"><b class="num" id="cYears">0</b> שנים בתרחיש; לחזור ל־<bdi>{st['years_to_save_2000']}</bdi> של <bdi>2000</bdi> דורש חיסכון של <b class="num" id="cNeed">0%</b> מהשכר. <button class="rbtn" id="cReset">איפוס</button></div>
    </div>
    <ul class="points rv levels">
      <li><span class="ic">🏠</span><span><b>המשפחה:</b> לחסוך מוקדם ולהשוות עלות חודשית של שכירות מול משכנתא.</span></li>
      <li><span class="ic">🏗</span><span><b>השוק:</b> יותר היצע דירות ותחרות במזון (<bdi>25.3%</bdi> ו־<bdi>17.9%</bdi> מההוצאה).</span></li>
      <li><span class="ic">🏛</span><span><b>המדינה:</b> תחבורה ציבורית, הגנה על שוכרים (<bdi>55.4%</bdi> בעשירון התחתון) ותמיכה בדיור ראשון.</span></li>
    </ul>
  </div>
  <div class="src">המחשבון הוא מודל להמחשה: מחיר דירה <bdi>2024</bdi> רשמי (הלמ"ס), שכר מעוגל, והנחות המודל לפי הסליידרים. כיוונים לדיון, לא המלצות מדיניות מבוססות מחקר.</div>
  <script type="application/json" id="calcData">{calc_data}</script>
  <script>{summary_js}</script>
</section>
<!--PY:summary:END-->"""

# ---------- policy ----------
policy = """<!--PY:policy:START-->
<section class="slide" data-title="מה אפשר לעשות" data-set="4">
  <div class="tag rv">פרק ו · מדיניות</div>
  <h2 class="rv">מנופים של <em>המדינה והשוק</em></h2>
  <div class="levers rv">
    <div class="glass"><h3>להגדיל היצע</h3><p>קצב תכנון ובנייה גבוה יותר: דיור הוא <bdi>25.3%</bdi> מהוצאות משק הבית.</p></div>
    <div class="glass"><h3>לחזק תחרות</h3><p>פחות חסמים ליבוא ולרשתות קטנות במזון, שהוא <bdi>17.9%</bdi> מההוצאה.</p></div>
    <div class="glass"><h3>תחבורה ציבורית</h3><p>תחבורה ותקשורת הם <bdi>18.6%</bdi> מההוצאה: חלופה לרכב שנייה מקטינה את העלות.</p></div>
    <div class="glass"><h3>להגן על שוכרים</h3><p>יותר ממחצית מהעשירון התחתון שוכרים (<bdi>55.4%</bdi>), מול <bdi>12.6%</bdi> בעליון.</p></div>
  </div>
  <div class="src">כיוונים לדיון, לא המלצות מדיניות מבוססות מחקר. המספרים: הלמ"ס, סקר הוצאות משק הבית <bdi>2023</bdi>.</div>
</section>
<!--PY:policy:END-->"""


def put(name, block, anchor, before=True):
    global html
    start, end = f"<!--PY:{name}:START-->", f"<!--PY:{name}:END-->"
    if start in html:
        a = html.index(start)
        b = html.index(end) + len(end)
        html = html[:a] + block + html[b:]
    else:
        assert anchor in html, f"anchor {anchor!r} not found"
        html = html.replace(anchor, (block + "\n\n" + anchor) if before else (anchor + "\n\n" + block), 1)


# migrate the earlier single-slide markers
html = html.replace("<!--PY:START-->", "<!--PY:analysis:START-->").replace("<!--PY:END-->", "<!--PY:analysis:END-->")

put("css", css, "</head>")
put("rent", rent, "<!-- 4 -->")
put("analysis", analysis, "<!-- 5 -->")
put("deciles", deciles, "<!--PY:analysis:START-->")
put("race", race, "<!--PY:analysis:END-->", before=False)
put("oecd", oecd, "<!--PY:race:END-->", before=False)
put("policy", policy, "<!--PY:oecd:END-->", before=False)
if "<!--PY:summary:START-->" not in html:
    m = re.search(r'<section class="slide[^"]*"[^>]*data-title="סיכום"[^>]*>.*?</section>', html, re.S)
    assert m, "static summary slide not found"
    html = html[:m.start()] + "<!--PY:summary:START--><!--PY:summary:END-->" + html[m.end():]
put("summary", summary, "<!--PY:summary:END-->")


# ---------- sync the hard-coded chart data inside index.html with data.json ----------
import re


def sync_core(h):
    infl = data["inflation_pct"]
    h = re.sub(r"var infl=\{[^}]*\};", "var infl={" + ",".join(f"{y}:{v}" for y, v in infl.items()) + "};", h)
    h = re.sub(r"var infl=\[[^\]]*\];", "var infl=[" + ",".join(str(infl[str(y)]) for y in range(1995, 2025)) + "];", h)
    hs = data["housing"]
    h = re.sub(r"var house=\[[^\]]*\];", "var house=[" + ",".join(
        f'{{y:{x["year"]},p:{x["price_kils"]},w:{x["avg_wage"]}}}' for x in hs) + "];", h)
    ratio = [(x["year"], round(x["price_kils"] * 1000 / x["avg_wage"], 1)) for x in hs]
    h = re.sub(r"var pts=\[\[[^;]*?\]\];", "var pts=[" + ",".join(f"[{y},{r}]" for y, r in ratio) + "];", h)
    r0, r1 = round(ratio[0][1]), round(ratio[-1][1])
    h = re.sub(r'data-to="\d+">\d+</b> משכורות; כיום כ־<b class="num" data-to="\d+">\d+</b>',
               f'data-to="{r0}">{r0}</b> משכורות; כיום כ־<b class="num" data-to="{r1}">{r1}</b>', h)
    h = re.sub(r'מכ־<bdi>[\d.]+</bdi> מיליון ש"ח לכ־<bdi>[\d.]+</bdi> מיליון',
               f'מכ־<bdi>{hs[0]["price_kils"]/1000:.1f}</bdi> מיליון ש"ח לכ־<bdi>{hs[-1]["price_kils"]/1000:.2f}</bdi> מיליון', h)
    # inflation slide: text that depends on the series
    for old, new in [
        ('<b>שנות ה־<bdi>90</bdi>:</b> אינפלציה של <bdi>7–11%</bdi> בשנה, ושחיקה מהירה של הכנסות.',
         '<b>שנות ה־<bdi>90</bdi>:</b> אינפלציה של <bdi>5–11%</bdi> בשנה (ממוצע שנתי), ושחיקה מהירה של הכנסות.'),
        ('<b>עשור של יציבות:</b> בין <bdi>2003</bdi> ל־<bdi>2020</bdi> המדד כמעט ולא זז, ולעיתים אף ירד.',
         '<b>עשור של יציבות:</b> בכל אחת מהשנים <bdi>2012</bdi>–<bdi>2021</bdi> האינפלציה הייתה בין <bdi dir="ltr">-0.6%</bdi> ל־<bdi>1.7%</bdi>, ולעיתים המחירים אף ירדו.'),
        ('<b><bdi>2022</bdi>:</b> זינוק של כ־<bdi>5.3%</bdi>, השיא מזה כשני עשורים.',
         '<b><bdi>2022</bdi>:</b> זינוק ל־<bdi>4.4%</bdi>, הגבוה ביותר מאז <bdi>2008</bdi> (<bdi>4.5%</bdi>); ב־<bdi>2023</bdi> <bdi>4.2%</bdi>.'),
        ('מקור: הלמ"ס, מדד המחירים לצרכן (שינוי שנתי, ערכים מעוגלים; לא אומת מחדש מול הסדרה הרשמית). ב־<bdi>2025</bdi>: <bdi>2.6%</bdi> (דצמבר מול דצמבר, כפי שדווח בתקשורת).',
         'מקור: הבנק העולמי (<bdi>FP.CPI.TOTL.ZG</bdi>), המבוסס על נתוני הלמ"ס: שינוי שנתי בממוצע מדד המחירים לצרכן. ב־<bdi>2025</bdi>: <bdi>3.0%</bdi>. קראתי את כל הסדרה, <bdi>1995</bdi>–<bdi>2024</bdi>.'),
        ('נתונים מעוגלים להמחשה, על בסיס הלמ"ס ובנק ישראל. יש לאמת מספרים מדויקים לפני הגשה.',
         'מחיר הדירה ב־<bdi>2024</bdi> רשמי (הלמ"ס, טבלה <bdi>2.2</bdi>: <bdi>2,340.3</bdi> אלף ש"ח). שאר נקודות המחיר והשכר מעוגלות להמחשה ולא אומתו; יש לאמת מול הלמ"ס.'),
        ('נתוני המחירים והשכר מעוגלים להמחשה, יש לאמת מול הלמ"ס.',
         'האינפלציה רשמית; מחיר <bdi>2024</bdi> רשמי; יתר נקודות המחיר והשכר מעוגלות ולא אומתו.'),
    ]:
        h = h.replace(old, new)
    return h


# ---------- source badges and one-line takeaways ----------
def decorate(h):
    def b(x, nd=1):
        return f"<bdi>{x}</bdi>"
    ratio0 = round(data["housing"][0]["price_kils"] * 1000 / data["housing"][0]["avg_wage"])
    ratio1 = round(data["housing"][-1]["price_kils"] * 1000 / data["housing"][-1]["avg_wage"])
    top, bot = tb["owner_occupied_pct"]
    cfg = {
        "אינפלציה": ("ok", "רשמי", "קצב עליית המחירים ירד מ־<bdi>5–11%</bdi> בשנה בשנות ה־90 לפחות מ־<bdi>2%</bdi> בכל אחת מהשנים <bdi>2012</bdi>–<bdi>2021</bdi>, ושב לעלות ב־<bdi>2022</bdi>."),
        "דיור ושכר": ("est", "2024 רשמי, השאר מעוגל", f"ב־<bdi>2000</bdi> דירה ממוצעת שווה <b>{ratio0}</b> משכורות; ב־<bdi>2024</bdi> כבר <b>{ratio1}</b>: יותר מהכפלה."),
        "שכירות": ("press", "דיווח על נתוני הלמ\"ס", f"גם מי שלא קנה דירה משלם יותר: מדד שכר הדירה עלה ב־<bdi>{r['housing_services_index_yoy_pct']}%</bdi> בשנה, מול אינפלציה של <bdi>{r['cpi_yoy_pct']}%</bdi>."),
        "הוצאות משק הבית": ("ok", "רשמי", "דיור, תחבורה ותקשורת ומזון הם יחד כ־<b><bdi>61.8%</bdi></b> מההוצאה של משק בית ממוצע."),
        "פערים": ("ok", "רשמי", f"הבית שבו גרים משנה הרבה: <b><bdi>{top}%</bdi></b> מהעשירון העליון בעלי דירה, לעומת <bdi>{bot}%</bdi> בתחתון."),
        "ניתוח פייתון": ("est", "חישוב; נתונים חלקית מעוגלים", f"מ־<bdi>2000</bdi> עד <bdi>2024</bdi> הדירה התייקרה פי <b><bdi>{st['price_multiple']}</bdi></b> והשכר פי <bdi>{st['wage_multiple']}</bdi>, כשהמחירים הכלליים עלו פי <bdi>{st['cpi_multiple_2000_2024']}</bdi>."),
        "מירוץ הדירה": ("mdl", "מודל להמחשה", f"ככל שהשנים עוברות, החיסכון למקדמה לוקח יותר זמן: מ־<b><bdi>{st['years_to_save_2000']}</bdi></b> שנים ב־<bdi>2000</bdi> ל־<b><bdi>{st['years_to_save_2024']}</bdi></b> ב־<bdi>2024</bdi>."),
        "בהשוואה בינלאומית": ("press", "דיווחי תקשורת", "רמת המחירים בישראל גבוהה מממוצע ה־<bdi>OECD</bdi>, ובתחילת <bdi>2025</bdi> השכר עלה לאט מהמחירים."),
        "מה אפשר לעשות": ("talk", "דיון", "ארבעה מנופים בולטים של המדינה והשוק: היצע דיור, תחרות בשוק המזון, תחבורה ציבורית והגנה על שוכרים."),
        "סיכום": ("mdl", "מחשבון להמחשה", "האם הדור הבא יוכל לקנות דירה? זה תלוי במה נחליט לעשות עכשיו. נסו במחשבון מה צריך להשתנות."),
    }
    for title, (cls, label, take) in cfg.items():
        pat = re.compile(r'(<section class="slide[^"]*"[^>]*data-title="' + re.escape(title) + r'"[^>]*>)(.*?)(</section>)', re.S)
        m = pat.search(h)
        assert m, title
        body = m.group(2)
        body = re.sub(r'<span class="badge[^>]*>.*?</span>', "", body)
        body = re.sub(r'\s*<p class="take rv">.*?</p>', "", body, flags=re.S)
        body = re.sub(r'(<div class="tag rv">.*?)(</div>)', lambda mm: mm.group(1) + f'<span class="badge {cls}">{label}</span>' + mm.group(2), body, count=1, flags=re.S)
        body = re.sub(r'(<h2 class="rv">.*?</h2>)', lambda mm: mm.group(1) + f'\n  <p class="take rv">{take}</p>', body, count=1, flags=re.S)
        h = h[:m.start()] + m.group(1) + body + m.group(3) + h[m.end():]
    return h


html = sync_core(html)
html = decorate(html)

# slide counter initial text
n = len(re.findall(r'<section class="slide', html))
html = re.sub(r'(id="counter">1 / )\d+', rf"\g<1>{n}", html)
html_path.write_text(html, encoding="utf-8")
print("slides:", n)
