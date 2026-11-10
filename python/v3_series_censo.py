import warnings; warnings.filterwarnings('ignore')
import pandas as pd,numpy as np
D='/home/claude/data/'
C10=np.load(D+'C10.npy'); C22=np.load(D+'C22.npy')   # [12 DS,2 sexo,18 fx,5 raca]
tcu=dict(zip(range(2000,2026),[2443107,2485502,2520705,2556430,2592239,2673557,2714977,2892625,2948733,2998058,2675656,2693606,2710968,2883672,2902927,2921087,2938092,2953986,2857329,2872347,2886698,2900319,2417678,2589296,2568928,2548560]))
tcu[2025]=2564204; tcu[2026]=2559945
T={2000:2443107,2010:2675656,2022:2417678}
for t in range(2001,2010): T[t]=T[2000]*(T[2010]/T[2000])**((t-2000)/10)
for t in range(2011,2022): T[t]=T[2010]*(T[2022]/T[2010])**((t-2010)/12)
for t in range(2000,2027): T[t]=tcu[t]
r25=0; r26=2559945/2564204-1
for t in range(2000,2027): T[t]=tcu[t]
TC={2000:2443107,2010:2675656,2022:2417678}
for t in range(2001,2010): TC[t]=TC[2000]*(TC[2010]/TC[2000])**((t-2000)/10)
for t in range(2011,2022): TC[t]=TC[2010]*(TC[2022]/TC[2010])**((t-2010)/12)
rr=2564204/2568928-1; TC[2023]=TC[2022]*(1+rr); TC[2024]=TC[2023]*(1+rr); TC[2025]=TC[2024]*(1+rr); TC[2026]=TC[2025]*(2559945/2564204)
pd.Series({t:round(TC[t]) for t in range(2000,2027)}).to_csv(D+'totais_censo.csv')
T=TC
s10=(C10+0.5)/(C10+0.5).sum(); s22=(C22+0.5)/(C22+0.5).sum()
def lr_round(x,total):
    fl=np.floor(x); rem=int(round(total-fl.sum()))
    if rem>0:
        idx=np.argsort(-(x-fl).ravel(),kind='stable')[:rem]; fl.ravel()[idx]+=1
    return fl.astype(int)
rows=[]; years=list(range(2000,2027)); DSY={}
for t in years:
    w=(t-2010)/12
    s=np.exp((1-w)*np.log(s10)+w*np.log(s22)); s/=s.sum()
    if t<2010:
        agg=s.sum(3,keepdims=True); pr=C10/np.where(C10.sum(3,keepdims=True)>0,C10.sum(3,keepdims=True),1)
        s=agg*pr; s/=s.sum()
    if t==2010: X=C10
    elif t==2022: X=C22
    else: X=s*T[t]
    if t==2010:
        Xi=np.zeros_like(X,dtype=int)
        for idx in np.ndindex(X.shape[:3]): Xi[idx]=lr_round(X[idx],round(X[idx].sum()))
    else: Xi=lr_round(X,round(T[t]))
    DSY[t]=Xi
    d,sx,a,r=np.indices(Xi.shape)
    rows.append(pd.DataFrame({'ANO':t,'FXET':a.ravel()+1,'DS':d.ravel()+1,'SEXO':sx.ravel()+1,'RACA':r.ravel()+1,'FREQ':Xi.ravel()}))
pop=pd.concat(rows,ignore_index=True)
q={**{t:'Retroprojeção (2000–2009)' for t in range(2000,2010)},2010:'Censo 2010',**{t:'Interpolação intercensitária' for t in range(2011,2022)},2022:'Censo 2022',**{t:'Projeção (variação IBGE)' for t in range(2023,2027)}}
pop.to_pickle(D+'pop_ds_censo.pkl'); np.save(D+'DSY_censo.npy',np.stack([DSY[t] for t in years]))
pd.Series({t:round(T[t]) for t in years}).to_csv(D+'totais_censo2.csv')
print(pop.groupby('ANO').FREQ.sum().to_string())
print(len(pop))
