"""Analyse data/data.json and produce numbers + a chart for the presentation.

Outputs:
  build/analysis.json      computed statistics (consumed by build.py)
  docs/charts/index_2000.png  indexed chart (2000 = 100)
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "data" / "data.json").read_text(encoding="utf-8"))

infl = {int(y): v for y, v in data["inflation_pct"].items()}
housing = data["housing"]

# Consumer price index, 2000 = 100, built from annual inflation.
cpi = {2000: 100.0}
for y in range(2001, 2025):
    cpi[y] = cpi[y - 1] * (1 + infl[y] / 100)

years = [h["year"] for h in housing]
wage_idx = [h["avg_wage"] / housing[0]["avg_wage"] * 100 for h in housing]
price_idx = [h["price_kils"] / housing[0]["price_kils"] * 100 for h in housing]
cpi_idx = [cpi[y] for y in years]
salaries = [round(h["price_kils"] * 1000 / h["avg_wage"]) for h in housing]

last = -1
stats = {
    "cpi_multiple_2000_2024": round(cpi[2024] / 100, 2),
    "wage_multiple": round(wage_idx[last] / 100, 2),
    "price_multiple": round(price_idx[last] / 100, 2),
    # real = nominal growth divided by price growth
    "real_wage_change_pct": round((wage_idx[last] / cpi_idx[last] - 1) * 100, 1),
    "real_house_price_change_pct": round((price_idx[last] / cpi_idx[last] - 1) * 100, 1),
    "salaries_to_buy_2000": salaries[0],
    "salaries_to_buy_2024": salaries[last],
    "worst_inflation_year": max((y for y in infl if y >= 2000), key=lambda y: infl[y]),
}

# Chart (English labels: avoids RTL shaping issues inside matplotlib).
BG, FG = "#0e1030", "#e9ecff"
fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=160, facecolor=BG)
ax.set_facecolor(BG)
ax.plot(years, price_idx, color="#ffc857", lw=3, marker="o", label="Average apartment price")
ax.plot(years, wage_idx, color="#3ddbc4", lw=3, marker="o", label="Average wage")
ax.plot(years, cpi_idx, color="#ff6b6b", lw=3, marker="o", label="Consumer prices (CPI)")
ax.set_title("Index, 2000 = 100", color=FG, fontsize=13, loc="left")
ax.tick_params(colors=FG)
ax.set_xticks(years)
for s in ax.spines.values():
    s.set_color("#5f6491")
ax.grid(axis="y", color="#5f6491", alpha=.35)
ax.legend(frameon=False, labelcolor=FG, loc="upper left")
fig.tight_layout()
(ROOT / "docs" / "charts").mkdir(parents=True, exist_ok=True)
fig.savefig(ROOT / "docs" / "charts" / "index_2000.png", facecolor=BG)

(ROOT / "build").mkdir(exist_ok=True)
(ROOT / "build" / "analysis.json").write_text(
    json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(stats, indent=2))
