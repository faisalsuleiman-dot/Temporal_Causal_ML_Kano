"""Create descriptive visualisations for the final corrected-model dataset."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "data" / "model"
FIGURES = ROOT / "results" / "corrected_model" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

raw = pd.read_csv(MODEL / "model_dataset_full_period_raw.csv", parse_dates=["Month"]).set_index("Month")
transformed = pd.read_csv(MODEL / "model_dataset_full_period_transformed.csv", parse_dates=["Month"]).set_index("Month")

plt.style.use("seaborn-v0_8-whitegrid")
blue, orange, green, red = "#1F4E78", "#E67E22", "#2E8B57", "#B03A2E"

fig, axes = plt.subplots(4, 1, figsize=(13, 14), sharex=True, constrained_layout=True)
axes[0].plot(raw.index, raw["pms"], label="PMS", color=blue, linewidth=1.8)
axes[0].plot(raw.index, raw["ago"], label="AGO", color=orange, linewidth=1.8)
axes[0].set_title("Kano fuel prices")
axes[0].set_ylabel("NGN/litre")
axes[0].legend(ncol=2, loc="upper left")

axes[1].plot(raw.index, raw["food"], label="Food CPI", color=green, linewidth=1.8)
axes[1].set_title("Kano food CPI and headline inflation")
axes[1].set_ylabel("Food CPI")
right = axes[1].twinx()
right.plot(raw.index, raw["inflation"], label="Headline inflation", color=red, linewidth=1.6)
right.set_ylabel("YoY percent")
lines, labels = axes[1].get_legend_handles_labels()
lines2, labels2 = right.get_legend_handles_labels()
axes[1].legend(lines + lines2, labels + labels2, ncol=2, loc="upper left")

axes[2].plot(raw.index, raw["fx"], label="NGN/USD", color=blue, linewidth=1.8)
axes[2].set_title("Exchange rate and Brent crude oil")
axes[2].set_ylabel("NGN per USD")
right = axes[2].twinx()
right.plot(raw.index, raw["brent"], label="Brent", color=orange, linewidth=1.6)
right.set_ylabel("USD/barrel")
lines, labels = axes[2].get_legend_handles_labels()
lines2, labels2 = right.get_legend_handles_labels()
axes[2].legend(lines + lines2, labels + labels2, ncol=2, loc="upper left")

axes[3].plot(raw.index, raw["m2"] / 1_000_000, label="M2", color=green, linewidth=1.8)
axes[3].set_title("Money supply and KEDCO electricity tariff")
axes[3].set_ylabel("M2 (NGN trillion)")
right = axes[3].twinx()
right.plot(raw.index, raw["tariff"], label="KEDCO tariff", color=red, linewidth=1.6)
right.set_ylabel("NGN/kWh")
lines, labels = axes[3].get_legend_handles_labels()
lines2, labels2 = right.get_legend_handles_labels()
axes[3].legend(lines + lines2, labels + labels2, ncol=2, loc="upper left")
axes[3].xaxis.set_major_locator(mdates.YearLocator(2))
axes[3].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

fig.suptitle("Dataset: monthly levels, January 2015--December 2024", fontsize=15, fontweight="bold")
fig.savefig(FIGURES / "dataset_line_charts.png", dpi=220, bbox_inches="tight")
plt.close(fig)

pairs = [
    ("pms", "food", "PMS change vs food-CPI change", blue),
    ("ago", "food", "AGO change vs food-CPI change", orange),
    ("food", "inflation", "Food-CPI change vs headline inflation", green),
    ("m2", "fx", "M2 change vs FX change", red),
]
fig, axes = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)
for ax, (x, y, title, color) in zip(axes.ravel(), pairs):
    ax.scatter(transformed[x], transformed[y], s=30, alpha=0.72, color=color, edgecolors="white", linewidths=0.35)
    ax.axhline(0, color="#777777", linewidth=0.7)
    ax.axvline(0, color="#777777", linewidth=0.7)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xlabel(f"{x}: log change")
    ax.set_ylabel("inflation: YoY percent" if y == "inflation" else f"{y}: log change")
fig.suptitle("Dataset: transformed-variable scatter plots", fontsize=14, fontweight="bold")
fig.savefig(FIGURES / "dataset_scatter_plots.png", dpi=220, bbox_inches="tight")
plt.close(fig)
print("DATASET_VISUALISATIONS_COMPLETE")
