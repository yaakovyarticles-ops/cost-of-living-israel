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


# ---------------------------------------------------------------------------
# Yearly series and a savings model, used by the animated "race" slide.
# Price and wage points exist for 2000, 2005, 2010, 2015, 2020, 2024; the years
# in between are linearly interpolated (an assumption, stated on the slide).
def interp(points, year):
    ys = sorted(points)
    for a, b in zip(ys, ys[1:]):
        if a <= year <= b:
            t = (year - a) / (b - a)
            return points[a] + (points[b] - points[a]) * t
    return points[ys[-1]]

price_pts = {h["year"]: h["price_kils"] for h in housing}      # thousand NIS
wage_pts = {h["year"]: h["avg_wage"] for h in housing}         # NIS / month
SAVE_RATE, DOWN_PAYMENT = 0.20, 0.25   # model assumptions (illustrative)
race_years = list(range(2000, 2025))
race = {"years": race_years, "price_idx": [], "wage_idx": [], "cpi_idx": [],
        "price_k": [], "wage": [], "years_to_save": [],
        "assumptions": {"save_rate": SAVE_RATE, "down_payment": DOWN_PAYMENT}}
for y in race_years:
    pr, wg = interp(price_pts, y), interp(wage_pts, y)
    race["price_k"].append(round(pr))
    race["wage"].append(round(wg))
    race["price_idx"].append(round(pr / price_pts[2000] * 100, 1))
    race["wage_idx"].append(round(wg / wage_pts[2000] * 100, 1))
    race["cpi_idx"].append(round(cpi[y], 1))
    # years of saving SAVE_RATE of the average wage to reach the down payment
    race["years_to_save"].append(round(pr * 1000 * DOWN_PAYMENT / (wg * 12 * SAVE_RATE), 1))
(ROOT / "build" / "race.json").write_text(json.dumps(race, ensure_ascii=False), encoding="utf-8")
stats["years_to_save_2000"] = race["years_to_save"][0]
stats["years_to_save_2024"] = race["years_to_save"][-1]
(ROOT / "build" / "analysis.json").write_text(
    json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")

# Animated GIF of the same series (used in the README, which cannot run JS).
from matplotlib.animation import FuncAnimation, PillowWriter
fig2, ax2 = plt.subplots(figsize=(7.2, 4.0), dpi=110, facecolor=BG)
ax2.set_facecolor(BG)
ymax = max(race["price_idx"]) * 1.08
def frame(k):
    ax2.clear(); ax2.set_facecolor(BG)
    ax2.set_xlim(2000, 2024); ax2.set_ylim(90, ymax)
    for key, color, label in (("price_idx", "#ffc857", "Apartment price"),
                              ("wage_idx", "#3ddbc4", "Average wage"),
                              ("cpi_idx", "#ff6b6b", "Consumer prices")):
        ax2.plot(race_years[:k + 1], race[key][:k + 1], color=color, lw=3, label=label)
        ax2.scatter([race_years[k]], [race[key][k]], color=color, s=60, zorder=3)
    ax2.set_title(f"{race_years[k]}  |  index 2000 = 100  |  years of saving for a down payment: "
                  f"{race['years_to_save'][k]}", color=FG, fontsize=10, loc="left")
    ax2.tick_params(colors=FG)
    for sp in ax2.spines.values(): sp.set_color("#5f6491")
    ax2.grid(axis="y", color="#5f6491", alpha=.3)
    ax2.legend(frameon=False, labelcolor=FG, loc="upper left")
def frame_hold(k): frame(min(k, len(race_years) - 1))
anim = FuncAnimation(fig2, frame_hold, frames=len(race_years) + 6, interval=180)
anim.save(ROOT / "docs" / "charts" / "race.gif", writer=PillowWriter(fps=6), savefig_kwargs={"facecolor": BG})
print("race.json + race.gif written")
