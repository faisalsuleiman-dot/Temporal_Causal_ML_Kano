"""Create Figure 4.5: seasonal decomposition of Kano headline inflation."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.seasonal import seasonal_decompose

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "model" / "model_dataset_full_period_raw.csv"
OUT = ROOT / "results" / "corrected_model" / "figures" / "figure_4_5_decomposition_analysis.png"

data = pd.read_csv(INPUT, parse_dates=["Month"]).set_index("Month")
series = data["inflation"].asfreq("MS")
result = seasonal_decompose(series, model="additive", period=12, extrapolate_trend="freq")

plt.style.use("seaborn-v0_8-whitegrid")
fig, axes = plt.subplots(4, 1, figsize=(13, 10), sharex=True, constrained_layout=True)
components = [
    (series, "Observed: Kano headline inflation (YoY %)", "#1F4E78"),
    (result.trend, "Trend", "#2E8B57"),
    (result.seasonal, "Seasonal component (12-month period)", "#E67E22"),
    (result.resid, "Residual", "#B03A2E"),
]
for axis, (values, label, color) in zip(axes, components):
    axis.plot(values.index, values, color=color, linewidth=1.7)
    axis.axhline(0, color="#777777", linewidth=0.7)
    axis.set_ylabel(label, fontsize=9)

axes[-1].xaxis.set_major_locator(mdates.YearLocator(1))
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
fig.suptitle("Figure 4.5: Decomposition Analysis of Kano Headline Inflation", fontsize=15, fontweight="bold")
fig.savefig(OUT, dpi=220, bbox_inches="tight")
plt.close(fig)
print(OUT)
