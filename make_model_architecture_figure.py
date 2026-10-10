"""Create Figure 4.6: model architecture of the temporal causal ML framework."""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "corrected_model" / "figures" / "figure_4_6_model_architecture.png"

plt.style.use("seaborn-v0_8-white")
fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis("off")

palette = {
    "input": "#D9EAF7", "process": "#E3F2E8", "discovery": "#FFF0C9",
    "estimate": "#F8D7DA", "validate": "#E8DDF6", "output": "#D5E8D4",
}

def box(x, y, w, h, title, body, color):
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.12",
                           linewidth=1.6, edgecolor="#2F3E46", facecolor=color)
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h - 0.32, title, ha="center", va="top", fontsize=11,
            fontweight="bold", color="#172B4D")
    ax.text(x + w / 2, y + h / 2 - 0.2, body, ha="center", va="center", fontsize=9.2,
            linespacing=1.35, color="#1F2933")

def arrow(x1, y1, x2, y2, label=None):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#394B59"))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.18, label, ha="center", va="bottom", fontsize=8.3)

box(0.6, 6.7, 3.0, 2.1, "1. Study Data", "120 monthly observations\nJan 2015-Dec 2024\nPMS, AGO, Food CPI, FX, Brent,\nM2, KEDCO tariff, inflation", palette["input"])
box(4.4, 6.7, 3.1, 2.1, "2. Preparation", "Alignment and completeness checks\nLog differences for positive series\nInflation retained as YoY level\nADF and KPSS diagnostics", palette["process"])
box(8.3, 6.7, 3.1, 2.1, "3. Temporal Discovery", "PCMCI+ with ParCorr\nLag window: 1-6 months\npc_alpha = 0.10\nAll directed lagged links saved", palette["discovery"])
box(12.2, 6.7, 3.1, 2.1, "4. Multiplicity Control", "Benjamini-Hochberg FDR\nPrimary evidence: q < 0.05\nNominal links retained separately\nas exploratory candidates", palette["discovery"])

box(3.0, 3.35, 3.4, 2.1, "5. Selected Effect Estimation", "LinearDML at PCMCI+-selected lags\nRandom Forest nuisance learners\nControls: FX, Brent, M2, tariff\nTimeSeriesSplit(3)", palette["estimate"])
box(8.2, 3.35, 3.4, 2.1, "6. Validation and Sensitivity", "Chronological 80:20 nuisance diagnostics\nKnown-truth simulation (10 seeds)\nLag-window checks: tau_max 3, 6, 9\nFigures and saved reproducible outputs", palette["validate"])

box(12.5, 3.35, 2.8, 2.1, "7. Model Outputs", "FDR-supported links\nNominal exploratory links\nDML estimates and intervals\nLimitations and valid conclusions", palette["output"])

arrow(3.6, 7.75, 4.4, 7.75)
arrow(7.5, 7.75, 8.3, 7.75)
arrow(11.4, 7.75, 12.2, 7.75)
arrow(9.85, 6.7, 4.7, 5.45, "selected nominal pathways")
arrow(5.3, 5.45, 5.3, 5.45 - 0.01)
arrow(6.4, 4.4, 8.2, 4.4)
arrow(11.6, 4.4, 12.5, 4.4)
arrow(13.9, 6.7, 13.9, 5.45, "FDR classifications")

ax.text(8, 9.55, "Figure 4.6: Model Architecture for the Temporal Causal Machine Learning Framework",
        ha="center", va="center", fontsize=16, fontweight="bold", color="#172B4D")
ax.text(8, 0.65, "Source: Author's Design (2026)", ha="center", va="center", fontsize=10,
        style="italic", color="#374151")
fig.savefig(OUT, dpi=240, bbox_inches="tight")
plt.close(fig)
print(OUT)
