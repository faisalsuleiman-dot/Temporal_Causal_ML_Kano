"""Create Figure 4.4: 12-month decomposition of all study variables."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.seasonal import seasonal_decompose

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "model" / "model_dataset_full_period_raw.csv"
FIGURES = ROOT / "results" / "corrected_model" / "figures"

data = pd.read_csv(INPUT, parse_dates=["Month"]).set_index("Month")
variables = [
    ("pms", "PMS (NGN/litre)", 1.0),
    ("ago", "AGO (NGN/litre)", 1.0),
    ("food", "Food CPI", 1.0),
    ("fx", "NGN/USD", 1.0),
    ("brent", "Brent (USD/barrel)", 1.0),
    ("m2", "M2 (NGN trillion)", 1_000_000.0),
    ("tariff", "KEDCO tariff (NGN/kWh)", 1.0),
    ("inflation", "Headline inflation (YoY %)", 1.0),
]

plt.style.use("seaborn-v0_8-whitegrid")
columns = ["Observed", "Trend", "Seasonal", "Residual"]
colors = ["#1F4E78", "#2E8B57", "#E67E22", "#B03A2E"]

def make_part(items, part, outfile):
    fig, axes = plt.subplots(len(items), 4, figsize=(19, 13), constrained_layout=True)
    for row, (field, label, divisor) in enumerate(items):
        series = (data[field] / divisor).asfreq("MS")
        decomposition = seasonal_decompose(series, model="additive", period=12, extrapolate_trend="freq")
        values = [series, decomposition.trend, decomposition.seasonal, decomposition.resid]
        for column, (axis, value, name, color) in enumerate(zip(axes[row], values, columns, colors)):
            axis.plot(value.index, value, color=color, linewidth=1.5)
            axis.axhline(0, color="#8A8A8A", linewidth=0.55)
            if row == 0:
                axis.set_title(name, fontsize=13, fontweight="bold")
            if column == 0:
                axis.set_ylabel(label, fontsize=10, fontweight="bold")
            axis.xaxis.set_major_locator(mdates.YearLocator(2))
            axis.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
            axis.tick_params(axis="both", labelsize=9)
    fig.suptitle(f"Figure 4.4{part}: Time Series Decomposition of Study Variables", fontsize=17, fontweight="bold")
    fig.savefig(outfile, dpi=240, bbox_inches="tight")
    plt.close(fig)

make_part(variables[:4], "a", FIGURES / "figure_4_4a_study_variables_decomposition.png")
make_part(variables[4:], "b", FIGURES / "figure_4_4b_study_variables_decomposition.png")
print(FIGURES / "figure_4_4a_study_variables_decomposition.png")
print(FIGURES / "figure_4_4b_study_variables_decomposition.png")
