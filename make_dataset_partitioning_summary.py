"""Create a chronological dataset-partitioning table from final-model outputs."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "data" / "model" / "model_dataset_full_period_transformed.csv"
RESULTS = ROOT / "results" / "corrected_model"

data = pd.read_csv(MODEL, parse_dates=["Month"]).set_index("Month")
mapping = pd.read_csv(RESULTS / "pcmci_to_dml_mapping.csv")
metrics = pd.read_csv(RESULTS / "nuisance_metrics.csv")
settings = __import__("json").loads((RESULTS / "settings.json").read_text())

rows = [{
    "Analysis_Component": "Study dataset / transformed input",
    "Pathway": "All eight variables",
    "Lag_Months": 0,
    "Full_N": len(data),
    "Full_Period": f"{data.index.min():%b %Y}-{data.index.max():%b %Y}",
    "Training_N": "Not applicable",
    "Training_Period": "Not applicable",
    "Test_N": "Not applicable",
    "Test_Period": "Not applicable",
    "Partition_Rule": "Complete monthly study matrix",
}, {
    "Analysis_Component": "PCMCI+ primary discovery",
    "Pathway": "All eight variables",
    "Lag_Months": settings["tau_max"],
    "Full_N": settings["effective_pcmci_N"],
    "Full_Period": f"{data.index[settings['tau_max']]:%b %Y}-{data.index.max():%b %Y}",
    "Training_N": "Not applicable",
    "Training_Period": "Not applicable",
    "Test_N": "Not applicable",
    "Test_Period": "Not applicable",
    "Partition_Rule": "All effective lagged observations; no hold-out split",
}]

for _, item in mapping.iterrows():
    treatment, outcome, lag = item["Treatment"], item["Outcome"], int(item["PCMCI_Lag"])
    sample = pd.DataFrame({"Y": data[outcome], "T": data[treatment].shift(lag)}).dropna()
    metric = metrics[(metrics.Treatment == treatment) & (metrics.Outcome == outcome) & (metrics.Lag == lag)].iloc[0]
    train_n, test_n = int(metric.Train_N), int(metric.Test_N)
    rows.append({
        "Analysis_Component": "DML nuisance diagnostic",
        "Pathway": f"{treatment.upper()} -> {outcome.upper()}",
        "Lag_Months": lag,
        "Full_N": len(sample),
        "Full_Period": f"{sample.index.min():%b %Y}-{sample.index.max():%b %Y}",
        "Training_N": train_n,
        "Training_Period": f"{sample.index[:train_n].min():%b %Y}-{sample.index[:train_n].max():%b %Y}",
        "Test_N": test_n,
        "Test_Period": f"{sample.index[train_n:].min():%b %Y}-{sample.index[train_n:].max():%b %Y}",
        "Partition_Rule": "Chronological 80:20 split; no shuffling",
    })

out = pd.DataFrame(rows)
out.to_csv(RESULTS / "dataset_partitioning_summary.csv", index=False)
print(out.to_string(index=False))
