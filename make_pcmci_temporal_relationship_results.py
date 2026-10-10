"""Create Table 5.2 from FDR-supported primary PCMCI+ relationships."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "corrected_model"
SOURCE = RESULTS / "pcmci_fdr_significant_links.csv"
OUT = RESULTS / "pcmci_temporal_relationship_results.csv"

labels = {
    "pms": "PMS petrol price", "ago": "AGO diesel price", "food": "Kano food CPI",
    "fx": "NGN/USD exchange rate", "brent": "Brent crude-oil price",
    "m2": "Broad money supply (M2)", "tariff": "KEDCO electricity tariff",
    "inflation": "Kano headline inflation",
}

links = pd.read_csv(SOURCE)
table = pd.DataFrame({
    "Cause": links["Cause"].map(labels),
    "Effect": links["Effect"].map(labels),
    "Lag_Months": links["Lag"],
    "PCMCI_Partial_Correlation": links["Statistic"],
    "Raw_P_Value": links["Raw_P"],
    "BH_FDR_Q_Value": links["BH_FDR_Q"],
    "Evidence": "BH-FDR supported (q < 0.05)",
})
table.to_csv(OUT, index=False)
print(table.to_string(index=False))
print(OUT)
