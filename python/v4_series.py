import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, sys
sys.path.insert(0,'/home/claude/scripts'); from v4_lib import *
D='/home/claude/data/'; V=D+'v4/'
C00=np.load(V+'C00.npy'); C10=np.load(V+'C10.npy'); C22=np.load(V+'C22.npy'); U22=np.load(V+'U22.npy')
tot=pd.read_csv(D+'totais.csv',index_col=0).iloc[:,0].to_dict()         # TCU/IBGE (oficial)
totc=pd.read_csv(D+'totais_censo2.csv',index_col=0).iloc[:,0].to_dict()  # série só censitária
years=list(range(2000,2027))
s00,s10,s22=[(C+0.5)/(C+0.5).sum() for C in (C00,C10,C22)]
def share(t):
    if t<2010: w=(t-2000)/10; s=np.exp((1-w)*np.log(s00)+w*np.log(s10))
    else: w=(t-2010)/12; s=np.exp((1-w)*np.log(s10)+w*np.log(s22))
    return s/s.sum()
def serie(T):
    out={}
    for t in years:
        if t==2000: X=C00
        elif t==2010: X=C10
        elif t==2022: X=C22
        else: X=lr_round(share(t)*T[t],round(T[t]))
        assert X.sum()==round(T[t]); out[t]=X
    return out
DSY=serie(tot); DSC=serie(totc)
np.save(V+'DSY.npy',np.stack([DSY[t] for t in years])); np.save(V+'DSY_censo.npy',np.stack([DSC[t] for t in years]))
rows=[]
for t in years:
    d,sx,a,r=np.indices(DSY[t].shape)
    rows.append(pd.DataFrame({'ANO':t,'FXET':a.ravel()+1,'DS':d.ravel()+1,'SEXO':sx.ravel()+1,'RACA':r.ravel()+1,'FREQ':DSY[t].ravel(),'FREQ_CENSO':DSC[t].ravel()}))
pop=pd.concat(rows,ignore_index=True); pop.to_pickle(V+'pop_ds.pkl')
# ---- desagregação bairro × DS (partes de bairro em cada DS), proporções 2022 dentro da célula DS
un=pd.read_csv(D+'units.csv'); uds=un.DS.values-1
C22u=np.stack([U22[uds==d].sum(0) for d in range(12)])
tot_u=U22.sum((1,2,3)); dsT=np.array([tot_u[uds==d].sum() for d in range(12)])
sh=np.where(C22u[uds]>0,U22/np.where(C22u[uds]>0,C22u[uds],1),(tot_u/dsT[uds])[:,None,None,None])
out=[]
for t in years:
    X=DSY[t][uds]*sh; Xi=np.floor(X+1e-9).astype(int)
    for d in range(12):
        m=np.where(uds==d)[0]; need=DSY[t][d]-Xi[m].sum(0); fr=X[m]-Xi[m]; order=np.argsort(-fr,axis=0,kind='stable')
        for idx in np.ndindex(need.shape):
            n=need[idx]
            if n>0: sel=order[(slice(0,n),)+idx]; Xi[(m[sel],)+idx]+=1
            assert n>=0
    u,sx,a,r=np.indices(Xi.shape)
    out.append(pd.DataFrame({'ANO':t,'DS':un.DS.values[u.ravel()],'COD_BAIRRO':un.COD_BAIRRO.values[u.ravel()],'FXET':a.ravel()+1,'SEXO':sx.ravel()+1,'RACA':r.ravel()+1,'FREQ':Xi.ravel()}))
P=pd.concat(out,ignore_index=True); P.to_pickle(V+'pop_full.pkl')
chk=P.groupby(['ANO','DS','SEXO','FXET','RACA']).FREQ.sum().values
print('linhas',len(P),'| bairro soma = DS:',(chk==pop.sort_values(['ANO','DS','SEXO','FXET','RACA']).FREQ.values).all(),'| negativos',(P.FREQ<0).sum())
b=pd.read_csv(D+'bairros_final_v3.csv').set_index('COD_BAIRRO').pop22
print('2022 bairro vs IBGE máx |dif|:',(P[P.ANO==2022].groupby('COD_BAIRRO').FREQ.sum()-b).abs().max())
print(pop.groupby('ANO')[['FREQ','FREQ_CENSO']].sum().T.to_string())
