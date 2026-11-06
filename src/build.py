"""Inject the Python analysis (stats + chart) into index.html as a slide.

Run src/analysis.py first. Idempotent: the slide lives between the
<!--PY:START--> / <!--PY:END--> markers and is regenerated on every run.
"""
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
html_path = ROOT / "index.html"
html = html_path.read_text(encoding="utf-8")
st = json.loads((ROOT / "build" / "analysis.json").read_text(encoding="utf-8"))
img = base64.b64encode((ROOT / "docs" / "charts" / "index_2000.png").read_bytes()).decode()

slide = f"""<!--PY:START-->
<section class="slide" data-title="ניתוח פייתון">
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
  <div class="src">חושב ב־Python (<bdi>src/analysis.py</bdi>) מתוך <bdi>data/data.json</bdi>; נתונים מעוגלים להמחשה, יש לאמת מול הלמ"ס.</div>
</section>
<!--PY:END-->
"""

if "<!--PY:START-->" in html:
    a = html.index("<!--PY:START-->")
    b = html.index("<!--PY:END-->") + len("<!--PY:END-->")
    html = html[:a] + slide.rstrip("\n") + html[b:]
else:
    anchor = "<!-- 5 -->"
    assert anchor in html, "summary slide marker not found"
    html = html.replace(anchor, slide + "\n" + anchor, 1)

html_path.write_text(html, encoding="utf-8")
print("slide written to", html_path)
