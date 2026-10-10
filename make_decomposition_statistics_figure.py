"""Create Figure 4.5: comparable time-series decomposition statistics."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "model" / "model_dataset_full_period_raw.csv"
FIGURES = ROOT / "results" / "corrected_model" / "figures"
OUT = FIGURES / "figure_4_5_decomposition_statistics.png"
CSV = ROOT / "results" / "corrected_model" / "decomposition_statistics.csv"

data = pd.read_csv(INPUT, parse_dates=["Month"]).set_index("Month")
variables = [
    ("pms", "PMS"), ("ago", "AGO"), ("food", "Food CPI"),
    ("fx", "FX"), ("brent", "Brent"), ("m2", "M2"),
    ("tariff", "KEDCO tariff"), ("inflation", "Headline inflation"),
]
rows = []
for field, label in variables:
    series = data[field].asfreq("MS")
    result = seasonal_decompose(series, model="additive", period=12, extrapolate_trend="freq")
    observed_sd = series.std(ddof=1)
    rows.append({
        "Variable": label,
        "Observed_SD": observed_sd,
        "Trend_to_Observed_SD": result.trend.std(ddof=1) / observed_sd,
        "Seasonal_to_Observed_SD": result.seasonal.std(ddof=1) / observed_sd,
        "Residual_to_Observed_SD": result.resid.std(ddof=1) / observed_sd,
    })
table = pd.DataFrame(rows)
table.to_csv(CSV, index=False)

matrix = table[["Trend_to_Observed_SD", "Seasonal_to_Observed_SD", "Residual_to_Observed_SD"]].to_numpy()
plt.style.use("seaborn-v0_8-white")
fig, axis = plt.subplots(figsize=(10.5, 7.2), constrained_layout=True)
image = axis.imshow(matrix, cmap="YlGnBu", aspect="auto", vmin=0, vmax=1)
axis.set_xticks(range(3), ["Trend / observed SD", "Seasonal / observed SD", "Residual / observed SD"])
axis.set_yticks(range(len(table)), table["Variable"])
for row in range(matrix.shape[0]):
    for column in range(matrix.shape[1]):
        value = matrix[row, column]
        axis.text(column, row, f"{value:.2f}", ha="center", va="center",
                  color="white" if value > 0.55 else "black", fontweight="bold")
colorbar = fig.colorbar(image, ax=axis, shrink=0.88)
colorbar.set_label("Component SD relative to observed-series SD")
axis.set_title("Figure 4.5: Time Series Decomposition Statistics", fontsize=15, fontweight="bold", pad=15)
axis.text(0.5, -0.12, "Additive 12-month decomposition; values are ratios, not variance shares.",
          transform=axis.transAxes, ha="center", fontsize=9)
fig.savefig(OUT, dpi=220, bbox_inches="tight")
plt.close(fig)
print(OUT)
print(CSV)
