"""Create Table 5.5: paired PCMCI+ and LinearDML results for selected pathways."""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "corrected_model"
MAPPING = RESULTS / "pcmci_to_dml_mapping.csv"
EFFECTS = RESULTS / "dml_effects.csv"
OUTPUT = RESULTS / "table_5_5_comparative_pcmci_dml_results.csv"

DISPLAY = {
    ("pms", "food"): "PMS petrol price → Kano food CPI",
    ("ago", "food"): "AGO diesel price → Kano food CPI",
    ("food", "inflation"): "Kano food CPI → Kano headline inflation",
}


def p_text(value: float) -> str:
    return "<0.001" if value < 0.001 else f"{value:.5f}"


def main() -> None:
    with MAPPING.open(newline="", encoding="utf-8") as handle:
        mapping = list(csv.DictReader(handle))
    with EFFECTS.open(newline="", encoding="utf-8") as handle:
        effects = list(csv.DictReader(handle))
    effects_by_key = {(row["Treatment"], row["Outcome"], row["Lag"]): row for row in effects}

    rows = []
    for screening in mapping:
        key = (screening["Treatment"], screening["Outcome"])
        if key not in DISPLAY:
            continue
        effect = effects_by_key[(key[0], key[1], screening["PCMCI_Lag"])]
        rows.append({
            "Selected relationship": DISPLAY[key],
            "PCMCI+ lag (months)": int(screening["PCMCI_Lag"]),
            "PCMCI+ partial correlation": round(float(screening["PCMCI_Statistic"]), 5),
            "PCMCI+ raw p-value": p_text(float(screening["PCMCI_P"])),
            "PCMCI+ BH-FDR q-value": round(float(screening["PCMCI_Q"]), 5),
            "PCMCI+ evidence": screening["Evidence_Class"],
            "DML model": "LinearDML",
            "DML N": int(effect["N"]),
            "DML effect estimate": round(float(effect["Effect"]), 5),
            "DML standard error": round(float(effect["SE"]), 5),
            "DML 95% confidence interval": f"[{float(effect['CI_Lower']):.5f}, {float(effect['CI_Upper']):.5f}]",
            "DML p-value": p_text(float(effect["P_value"])),
        })

    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
