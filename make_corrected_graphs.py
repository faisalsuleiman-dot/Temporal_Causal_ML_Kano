from pathlib import Path
import pandas as pd, matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[2]/'results/corrected_model'; G=R/'figures'; G.mkdir(exist_ok=True)
links=pd.read_csv(R/'pcmci_all_links.csv'); sig=links[links['Significant_FDR_0.05']]
plt.figure(figsize=(8,4))
for _,r in sig.iterrows(): plt.plot([0,1],[0,0],lw=3,label=f"{r.Cause} -> {r.Effect} (lag {r.Lag})")
plt.axis('off'); plt.title('Corrected PCMCI+ FDR-supported links'); plt.legend(); plt.savefig(G/'pcmci_causal_graph.png',dpi=220); plt.close()
nom=links[links['Significant_Raw_0.05']]; plt.figure(figsize=(8,4))
for i,(_,r) in enumerate(nom.iterrows()): plt.plot([0,1],[i,i],lw=2,label=f"{r.Cause} -> {r.Effect} (lag {r.Lag})")
plt.axis('off'); plt.title('PCMCI+ nominal p<0.05 links (UNCORRECTED)'); plt.legend(fontsize=7); plt.savefig(G/'pcmci_nominal_uncorrected.png',dpi=220); plt.close()
nom.groupby(['Cause','Effect']).size().plot(kind='bar',figsize=(8,4),title='Nominal link counts by pathway'); plt.tight_layout(); plt.savefig(G/'pcmci_lag_strength.png',dpi=220); plt.close()
e=pd.read_csv(R/'dml_effects.csv'); plt.figure(figsize=(8,4)); plt.errorbar(e.Effect,range(len(e)),xerr=[e.Effect-e.CI_Lower,e.CI_Upper-e.Effect],fmt='o'); plt.yticks(range(len(e)),e.Treatment+' -> '+e.Outcome); plt.axvline(0,color='k'); plt.title('DML effects with 95% intervals'); plt.tight_layout(); plt.savefig(G/'dml_effects_ci.png',dpi=220); plt.close()
s=pd.read_csv(R/'simulation_metrics.csv'); s[['Precision','Recall','F1','FDR','Lag_Accuracy']].plot(kind='box',figsize=(8,4),title='Simulation metric distribution'); plt.tight_layout(); plt.savefig(G/'simulation_metric_distribution.png',dpi=220); plt.close()
print('GRAPHS_COMPLETE')
