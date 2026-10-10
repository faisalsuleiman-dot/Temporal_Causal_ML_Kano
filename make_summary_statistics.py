"""Create Table 4.3 from the 120-month final corrected-model study dataset."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "model" / "model_dataset_full_period_raw.csv"
OUT = ROOT / "results" / "corrected_model" / "summary_statistics_study_variables.csv"

labels = {
    "pms": ("PMS petrol price", "NGN/litre"),
    "ago": ("AGO diesel price", "NGN/litre"),
    "food": ("Kano food CPI", "CPI index"),
    "fx": ("NGN/USD exchange rate", "NGN per USD"),
    "brent": ("Brent crude-oil price", "USD/barrel"),
    "m2": ("Broad money supply (M2)", "NGN million"),
    "tariff": ("KEDCO electricity tariff", "NGN/kWh"),
    "inflation": ("Kano headline inflation", "YoY percent"),
}

data = pd.read_csv(RAW)
rows = []
for field, (name, unit) in labels.items():
    series = pd.to_numeric(data[field], errors="raise")
    rows.append({
        "Variable": name,
        "Unit": unit,
        "N": int(series.count()),
        "Mean": series.mean(),
        "Std_Dev": series.std(ddof=1),
        "Median": series.median(),
        "Minimum": series.min(),
        "Maximum": series.max(),
    })
table = pd.DataFrame(rows)
table.to_csv(OUT, index=False)
print(table.to_string(index=False, float_format=lambda x: f"{x:,.2f}"))
print(OUT)
