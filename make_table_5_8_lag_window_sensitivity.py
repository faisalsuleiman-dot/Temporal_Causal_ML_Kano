"""Format selected PCMCI+ relationships across maximum-lag sensitivity windows."""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "corrected_model"
INPUT = RESULTS / "robustness_links.csv"
OUTPUT = RESULTS / "table_5_8_pcmci_sensitivity_maximum_lag_windows.csv"

RELATIONSHIPS = [
    ("pms", "food", 2, "PMS petrol price → Kano food CPI"),
    ("ago", "food", 5, "AGO diesel price → Kano food CPI"),
    ("food", "inflation", 3, "Kano food CPI → Kano headline inflation"),
]
WINDOWS = [3, 6, 9]


def p_text(value: float) -> str:
    return "<0.001" if value < 0.001 else f"{value:.5f}"


def main() -> None:
    with INPUT.open(newline="", encoding="utf-8") as handle:
        links = list(csv.DictReader(handle))
    lookup = {(row["Cause"], row["Effect"], int(row["Lag"]), int(row["tau_max"])): row for row in links}

    rows = []
    for cause, effect, lag, label in RELATIONSHIPS:
        for tau_max in WINDOWS:
            if lag > tau_max:
                rows.append({
                    "Selected relationship": label,
                    "Maximum lag window (months)": tau_max,
                    "Tested relationship lag (months)": lag,
                    "PCMCI+ partial correlation": "Not tested",
                    "Raw p-value": "Not tested",
                    "BH-FDR q-value": "Not tested",
                    "Evidence classification": f"Not tested: lag {lag} exceeds maximum lag {tau_max}",
                })
                continue
            row = lookup[(cause, effect, lag, tau_max)]
            classification = "Nominal exploratory" if row["Significant_Raw_0.05"] == "True" else "Not nominally supported"
            rows.append({
                "Selected relationship": label,
                "Maximum lag window (months)": tau_max,
                "Tested relationship lag (months)": lag,
                "PCMCI+ partial correlation": f"{float(row['Statistic']):.5f}",
                "Raw p-value": p_text(float(row["Raw_P"])),
                "BH-FDR q-value": f"{float(row['BH_FDR_Q']):.5f}",
                "Evidence classification": classification,
            })

    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
