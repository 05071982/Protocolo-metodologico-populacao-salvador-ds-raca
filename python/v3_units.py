import warnings; warnings.filterwarnings('ignore')
import pandas as pd,numpy as np
D='/home/claude/data/'
DSY=np.load(D+'DSY.npy'); U22=np.load(D+'U22.npy'); C22=np.load(D+'C22.npy'); un=pd.read_csv(D+'units.csv')
uds=un.DS.values-1; years=list(range(2000,2027))
# share of each unit within its DS cell (2022); fallback unit total share
tot_u=U22.sum((1,2,3)); dsT=np.array([tot_u[uds==d].sum() for d in range(12)])
sh=np.where(C22[uds]>0, U22/np.where(C22[uds]>0,C22[uds],1), (tot_u/dsT[uds])[:,None,None,None])
out=[]
for ti,t in enumerate(years):
    X=DSY[ti][uds]*sh              # units x sx x fx x r
    Xi=np.floor(X).astype(int)
    for d in range(12):
        m=np.where(uds==d)[0]
        need=DSY[ti][d]-Xi[m].sum(0)   # sx fx r
        fr=X[m]-Xi[m]
        order=np.argsort(-fr,axis=0,kind='stable')
        for idx in np.ndindex(need.shape):
            n=need[idx]
            if n>0:
                sel=order[(slice(0,n),)+idx]; Xi[(m[sel],)+idx]+=1
    u,sx,a,r=np.indices(Xi.shape)
    out.append(pd.DataFrame({'ANO':t,'DS':un.DS.values[u.ravel()],'COD_BAIRRO':un.COD_BAIRRO.values[u.ravel()],'FXET':a.ravel()+1,'SEXO':sx.ravel()+1,'RACA':r.ravel()+1,'FREQ':Xi.ravel()}))
P=pd.concat(out,ignore_index=True); P.to_pickle(D+'pop_full.pkl')
chk=P.groupby(['ANO','DS','SEXO','FXET','RACA']).FREQ.sum().values
pd_=pd.read_pickle(D+'pop_ds.pkl').sort_values(['ANO','DS','SEXO','FXET','RACA']).FREQ.values
print(len(P), 'DS bate:', (chk==pd_).all(), 'neg:',(P.FREQ<0).sum())
b=pd.read_csv(D+'bairros_final_v3.csv').set_index('COD_BAIRRO').pop22
print('bairro 2022 bate IBGE:', (P[P.ANO==2022].groupby('COD_BAIRRO').FREQ.sum()-b).abs().max())
