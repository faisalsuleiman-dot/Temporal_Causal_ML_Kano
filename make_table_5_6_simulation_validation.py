"""Summarise final PCMCI+ simulation-validation replications as Table 5.6."""

import csv
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "corrected_model"
INPUT = RESULTS / "simulation_metrics.csv"
OUTPUT = RESULTS / "table_5_6_pcmci_simulation_validation_results.csv"

METRICS = [
    ("TP", "True positives"),
    ("FP", "False positives"),
    ("FN", "False negatives"),
    ("Precision", "Precision"),
    ("Recall", "Recall"),
    ("F1", "F1 score"),
    ("FDR", "False discovery rate"),
    ("Lag_Accuracy", "Directed-pair recovery"),
]


def main() -> None:
    with INPUT.open(newline="", encoding="utf-8") as handle:
        simulations = list(csv.DictReader(handle))

    rows = []
    for key, name in METRICS:
        values = [float(row[key]) for row in simulations]
        rows.append({
            "Metric": name,
            "Replications": len(values),
            "Mean": f"{statistics.mean(values):.3f}",
            "Standard deviation": f"{statistics.stdev(values):.3f}",
            "Minimum": f"{min(values):.3f}",
            "Maximum": f"{max(values):.3f}",
        })

    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
