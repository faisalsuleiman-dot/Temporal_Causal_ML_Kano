from pathlib import Path
import json, warnings
import numpy as np,pandas as pd
warnings.filterwarnings('ignore')
from statsmodels.tsa.stattools import adfuller,kpss
from statsmodels.stats.multitest import multipletests
from sklearn.ensemble import RandomForestRegressor,HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
from econml.dml import LinearDML
from tigramite import data_processing as pp
from tigramite.pcmci import PCMCI
from tigramite.independence_tests.parcorr import ParCorr
ROOT=Path(__file__).resolve().parents[2]; D=ROOT/'data/model/model_dataset_full_period_transformed.csv'; O=ROOT/'results/corrected_model'; O.mkdir(parents=True,exist_ok=True)
X=pd.read_csv(D,parse_dates=['Month']).set_index('Month'); cols=list(X.columns); X=X[cols]
st=[]; final=X.copy()
for c in cols:
 y=final[c].dropna(); a=adfuller(y,autolag='AIC');
 try: k=kpss(y,nlags='auto')
 except: k=(np.nan,np.nan)
 decision='stationary' if a[1]<.05 and k[1]>=.05 else ('nonstationary' if a[1]>=.05 and k[1]<.05 else 'contradictory/indeterminate')
 st.append({'Variable':c,'Transformation':'log difference' if c!='inflation' else 'YoY level','N':len(y),'ADF_stat':a[0],'ADF_p':a[1],'KPSS_stat':k[0],'KPSS_p':k[1],'Decision':decision})
pd.DataFrame(st).to_csv(O/'transformed_stationarity.csv',index=False); final.to_csv(O/'pcmci_input_matrix.csv')
def pcm(arr,tau): return PCMCI(dataframe=pp.DataFrame(arr),cond_ind_test=ParCorr()).run_pcmciplus(tau_min=1,tau_max=tau,pc_alpha=.1)
def links(res,tau):
 rows=[]
 for i,a in enumerate(cols):
  for j,b in enumerate(cols):
   for lag in range(1,tau+1): rows.append({'Cause':a,'Effect':b,'Lag':lag,'Statistic':float(res['val_matrix'][i,j,lag]),'Raw_P':float(res['p_matrix'][i,j,lag])})
 d=pd.DataFrame(rows); d['BH_FDR_Q']=multipletests(d.Raw_P,method='fdr_bh')[1]; d['Significant_Raw_0.05']=d.Raw_P<.05; d['Significant_FDR_0.05']=d.BH_FDR_Q<.05; return d
r6=pcm(final.to_numpy(),6); all6=links(r6,6); all6.to_csv(O/'pcmci_all_links.csv',index=False); all6[all6["Significant_FDR_0.05"]].to_csv(O/'pcmci_fdr_significant_links.csv',index=False); all6[all6["Significant_Raw_0.05"]].to_csv(O/'pcmci_nominal_links.csv',index=False)
rows=[]
for tau in [3,6,9]:
 if len(final)-tau<50:
  continue
 q=links(pcm(final.to_numpy(),tau),tau); q=q[(q.Cause.isin(['pms','ago','food'])) & (q.Effect.isin(['food','inflation']))]; q['tau_max']=tau; rows.append(q)
rob=pd.concat(rows,ignore_index=True); rob.to_csv(O/'robustness_links.csv',index=False)
# DML on every nominally relevant pathway, with actual discovered lag; FDR class where applicable
targets=all6[(all6["Significant_Raw_0.05"])&(all6.Cause.isin(['pms','ago','food']))&(all6.Effect.isin(['food','inflation']))&(all6.Cause != all6.Effect)].copy(); targets=targets.drop_duplicates(['Cause','Effect'],keep='first')
maps=[]; effects=[]; nuis=[]
learners={'Ridge':Ridge(alpha=1.0),'RandomForest':RandomForestRegressor(n_estimators=100,min_samples_leaf=4,random_state=42)}
for _,r in targets.iterrows():
 t,y,k=r.Cause,r.Effect,int(r.Lag); q=pd.DataFrame({'Y':final[y],'T':final[t].shift(k),'fx':final.fx,'brent':final.brent,'m2':final.m2,'tariff':final.tariff}).dropna(); maps.append({'Treatment':t,'Outcome':y,'PCMCI_Lag':k,'PCMCI_Statistic':r.Statistic,'PCMCI_P':r.Raw_P,'PCMCI_Q':r.BH_FDR_Q,'Evidence_Class':'FDR-supported' if r["Significant_FDR_0.05"] else 'Nominal exploratory','DML_Run':'yes'})
 Y=q.Y.to_numpy(); T=q['T'].to_numpy(); W=q[['fx','brent','m2','tariff']].to_numpy(); n=len(q); cut=int(n*.8)
 for name,learner in learners.items():
  yy=learner.fit(W[:cut],Y[:cut]); tt=learners[name].__class__(**({'alpha':1.0} if name=='Ridge' else {})) if name=='Ridge' else learner.__class__(**({'n_estimators':100,'min_samples_leaf':4,'random_state':42} if name=='RandomForest' else {'max_iter':100,'l2_regularization':1.0,'random_state':42})); tt.fit(W[:cut],T[:cut]); yp=yy.predict(W[cut:]); tp=tt.predict(W[cut:]); nuis.append({'Treatment':t,'Outcome':y,'Lag':k,'Learner':name,'Train_N':cut,'Test_N':n-cut,'R2_Y':r2_score(Y[cut:],yp),'MAE_Y':mean_absolute_error(Y[cut:],yp),'RMSE_Y':mean_squared_error(Y[cut:],yp)**.5,'R2_T':r2_score(T[cut:],tp),'MAE_T':mean_absolute_error(T[cut:],tp),'RMSE_T':mean_squared_error(T[cut:],tp)**.5})
 est=LinearDML(model_y=RandomForestRegressor(n_estimators=100,min_samples_leaf=4,random_state=42),model_t=RandomForestRegressor(n_estimators=100,min_samples_leaf=4,random_state=42),cv=TimeSeriesSplit(3),random_state=42); est.fit(Y,T,X=None,W=W,inference='statsmodels'); eff=float(np.asarray(est.const_marginal_ate()).ravel()[0]); ci=est.const_marginal_ate_interval(alpha=.05); se=(float(ci[1])-float(ci[0]))/(2*1.96); p=2*(1-__import__('scipy').stats.norm.cdf(abs(eff/se))) if se>0 else np.nan; effects.append({'Treatment':t,'Outcome':y,'Lag':k,'N':n,'Effect':eff,'SE':se,'CI_Lower':float(ci[0]),'CI_Upper':float(ci[1]),'P_value':p,'Nuisance':'RandomForest 100 trees min_leaf 4','Cross_fitting':'TimeSeriesSplit(3)','Evidence_Class':'FDR-supported' if r["Significant_FDR_0.05"] else 'Nominal exploratory'})
pd.DataFrame(maps).to_csv(O/'pcmci_to_dml_mapping.csv',index=False); pd.DataFrame(effects).to_csv(O/'dml_effects.csv',index=False); pd.DataFrame(nuis).to_csv(O/'nuisance_metrics.csv',index=False)
# simulation replications
sim=[]
for seed in range(10):
 rng=np.random.default_rng(seed); z=np.zeros((500,3))
 for t in range(2,500): z[t,0]=.5*z[t-1,0]+rng.normal(); z[t,1]=.4*z[t-1,1]+.8*z[t-2,0]+rng.normal(); z[t,2]=.3*z[t-1,2]+.7*z[t-1,1]+rng.normal()
 rr=pcm(z,3); rec={(i,j,l) for i in range(3) for j in range(3) for l in range(1,4) if rr['p_matrix'][i,j,l]<.05}; true={(0,1,2),(1,2,1)}; tp=len(rec&true); fp=len(rec-true); fn=len(true-rec); pr=tp/(tp+fp) if tp+fp else 0; re=tp/(tp+fn) if tp+fn else 0; sim.append({'seed':seed,'TP':tp,'FP':fp,'FN':fn,'Precision':pr,'Recall':re,'F1':2*pr*re/(pr+re) if pr+re else 0,'FDR':fp/(tp+fp) if tp+fp else 0,'Lag_Accuracy':len({x for x in rec if (x[0],x[1]) in {(0,1),(1,2)}})/2})
pd.DataFrame(sim).to_csv(O/'simulation_metrics.csv',index=False)
with open(O/'settings.json','w') as f: json.dump({'tau_min':1,'tau_max':6,'pc_alpha':.1,'alpha':.05,'ci_test':'ParCorr','fdr':'Benjamini-Hochberg','effective_pcmci_N':len(final)-6,'replications':10,'seed_range':'0-9'},f,indent=2)
print('CORRECTED_MODEL_COMPLETE'); print('FDR LINKS'); print(all6[all6["Significant_FDR_0.05"]][['Cause','Effect','Lag','Raw_P','BH_FDR_Q']].to_string(index=False)); print('DML'); print(pd.DataFrame(effects).to_string(index=False)); print('SIM MEANS',pd.DataFrame(sim).mean(numeric_only=True).to_dict())




