"""Create Table 5.1 for the final corrected-model data-preparation workflow."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "corrected_model" / "dataset_preparation_summary.csv"

table = pd.DataFrame([
    ["Study scope", "Monthly Kano dataset, January 2015-December 2024", "120 raw study observations across eight model variables"],
    ["Temporal alignment", "Common month-start index applied to every input series", "One aligned monthly matrix; no duplicate study months"],
    ["Completeness check", "Required variables checked before matrix construction", "No missing values in the final 120-row raw or transformed input"],
    ["2015 AGO completion", "Researcher-provided Kano AGO values for January-May 2015", "Five early observations retained with explicit provenance"],
    ["2015 headline inflation", "Calculated from Kano all-items CPI: 100 * (CPI_2015 / CPI_2014 - 1)", "Complete January-December 2015 YoY inflation series"],
    ["Predecessor observations", "December 2014 values used only to calculate January 2015 log changes", "January 2015 retained; predecessor is not an added study-month row"],
    ["Transformation", "One-period log differences for PMS, AGO, Food CPI, FX, Brent, M2, and tariff", "120 transformed observations for each positive-valued series"],
    ["Inflation representation", "Kano headline inflation retained as YoY percentage level", "120 observations; no log transformation"],
    ["Stationarity diagnostics", "ADF unit-root and KPSS stationarity tests", "Diagnostics saved; series are retained for the specified temporal analysis"],
    ["PCMCI+ input", "Final transformed data matrix written before temporal discovery", "120 rows; effective sample is 114 at tau_max = 6"],
], columns=["Preparation step", "Method", "Final output / result"])
table.to_csv(OUT, index=False)
print(table.to_string(index=False))
print(OUT)
