"""Format the three selected LinearDML pathway estimates as Table 5.4."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "corrected_model"
INPUT = RESULTS / "dml_effects.csv"
OUTPUT = RESULTS / "table_5_4_linear_dml_effect_estimates.csv"

DISPLAY = {
    ("pms", "food"): "PMS petrol price → Kano food CPI",
    ("ago", "food"): "AGO diesel price → Kano food CPI",
    ("food", "inflation"): "Kano food CPI → Kano headline inflation",
}


def p_value(value: float) -> str:
    return "<0.001" if value < 0.001 else f"{value:.5f}"


def main() -> None:
    effects = pd.read_csv(INPUT)
    rows = []
    for _, effect in effects.iterrows():
        key = (effect["Treatment"], effect["Outcome"])
        if key not in DISPLAY:
            continue
        rows.append({
            "Pathway": DISPLAY[key],
            "DML model": "LinearDML",
            "Lag (months)": int(effect["Lag"]),
            "N": int(effect["N"]),
            "Effect estimate": round(effect["Effect"], 5),
            "Standard error": round(effect["SE"], 5),
            "95% confidence interval": f"[{effect['CI_Lower']:.5f}, {effect['CI_Upper']:.5f}]",
            "p-value": p_value(effect["P_value"]),
            "PCMCI+ evidence class": effect["Evidence_Class"],
        })
    pd.DataFrame(rows).to_csv(OUTPUT, index=False)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
