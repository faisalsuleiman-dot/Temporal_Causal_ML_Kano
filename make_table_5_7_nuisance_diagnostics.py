"""Format corrected DML nuisance diagnostic metrics as Table 5.7."""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "corrected_model"
INPUT = RESULTS / "nuisance_metrics.csv"
OUTPUT = RESULTS / "table_5_7_dml_nuisance_model_diagnostics.csv"

DISPLAY = {
    ("pms", "food"): "PMS petrol price → Kano food CPI",
    ("ago", "food"): "AGO diesel price → Kano food CPI",
    ("food", "inflation"): "Kano food CPI → Kano headline inflation",
}


def main() -> None:
    with INPUT.open(newline="", encoding="utf-8") as handle:
        diagnostics = list(csv.DictReader(handle))

    rows = []
    for item in diagnostics:
        key = (item["Treatment"], item["Outcome"])
        rows.append({
            "Selected relationship": DISPLAY[key],
            "Lag (months)": item["Lag"],
            "Diagnostic learner": item["Learner"],
            "Training N": item["Train_N"],
            "Test N": item["Test_N"],
            "Outcome nuisance R²": f"{float(item['R2_Y']):.3f}",
            "Outcome nuisance MAE": f"{float(item['MAE_Y']):.5f}",
            "Outcome nuisance RMSE": f"{float(item['RMSE_Y']):.5f}",
            "Treatment nuisance R²": f"{float(item['R2_T']):.3f}",
            "Treatment nuisance MAE": f"{float(item['MAE_T']):.5f}",
            "Treatment nuisance RMSE": f"{float(item['RMSE_T']):.5f}",
        })

    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
