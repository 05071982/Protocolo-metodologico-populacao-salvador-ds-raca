import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, sys, time
sys.path.insert(0,'/home/claude/scripts'); from v4_lib import *
D='/home/claude/data/'; V='/home/claude/data/v51/'; V4=D+'v4/'
un=pd.read_csv(V+'units.csv'); nu=len(un); uds=un.DS.values-1
sh=(nu,2,18,5); t0=time.time()
C00,C10,C22=[np.load(V+f'{n}_u.npy') for n in ('C00','C10','C22')]
# ---- série anual por unidade
tot=pd.read_csv(D+'totais.csv',index_col=0).iloc[:,0].to_dict(); totc=pd.read_csv(D+'totais_censo2.csv',index_col=0).iloc[:,0].to_dict()
EPS=0.1
s00,s10,s22=[(C+EPS)/(C+EPS).sum() for C in (C00,C10,C22)]
def share(t):
    if t<2010: w=(t-2000)/10; s=np.exp((1-w)*np.log(s00)+w*np.log(s10))
    else: w=(t-2010)/12; s=np.exp((1-w)*np.log(s10)+w*np.log(s22))
    return s/s.sum()
years=range(2000,2027); FIX={2000:C00,2010:C10,2022:C22}
# após 2022 (extrapolação): tendência 2010→2022 no nível DS × sexo × faixa × raça (2.160 células, estável),
# repartida entre as unidades do DS pela proporção de 2022 — evita explosão de células pequenas de bairro
D10=np.zeros((12,2,18,5)); np.add.at(D10,uds,C10); D22=np.zeros((12,2,18,5)); np.add.at(D22,uds,C22)
d10,d22=[(C+0.5)/(C+0.5).sum() for C in (D10,D22)]
shu=np.where(D22[uds]>0,C22/np.where(D22[uds]>0,D22[uds],1),0)
for d in range(12):          # células do DS sem população em 2022: proporção da unidade no total do DS
    m=uds==d; tu=C22[m].sum((1,2,3)); shu[m]=np.where(D22[d][None]>0,shu[m],(tu/tu.sum())[:,None,None,None])
def extrap(t,T):
    w=(t-2010)/12; s=np.exp((1-w)*np.log(d10)+w*np.log(d22)); s/=s.sum()
    Xd=lr_round(s*T,round(T)); X=Xd[uds]*shu; Xi=np.floor(X+1e-9).astype(int)
    for d in range(12):
        m=np.where(uds==d)[0]; need=Xd[d]-Xi[m].sum(0); fr=X[m]-Xi[m]; order=np.argsort(-fr,axis=0,kind='stable')
        for idx in np.ndindex(need.shape):
            n=need[idx]; assert n>=0
            if n>0: Xi[(m[order[(slice(0,n),)+idx]],)+idx]+=1
    return Xi
def serie(T): return {t:(FIX[t] if t in FIX else (extrap(t,T[t]) if t>2022 else lr_round(share(t)*T[t],round(T[t])))) for t in years}
SU=serie(tot); SC=serie(totc)
rows=[]
for t in years:
    assert SU[t].sum()==round(tot[t])
    u,s,f,r=np.indices(sh)
    rows.append(pd.DataFrame({'ANO':t,'DS':un.DS.values[u.ravel()],'COD_BAIRRO':un.COD_BAIRRO.values[u.ravel()],'FXET':f.ravel()+1,'SEXO':s.ravel()+1,'RACA':r.ravel()+1,'FREQ':SU[t].ravel()}))
P=pd.concat(rows,ignore_index=True); P.to_pickle(V+'pop_full.pkl')
dsr=[]
for t in years:
    for nm,S in [('FREQ',SU),('FREQ_CENSO',SC)]:
        A=np.zeros((12,2,18,5)); np.add.at(A,uds,S[t]); 
        if nm=='FREQ': cur=A
        else: cen=A
    d,s,f,r=np.indices(cur.shape)
    dsr.append(pd.DataFrame({'ANO':t,'FXET':f.ravel()+1,'DS':d.ravel()+1,'SEXO':s.ravel()+1,'RACA':r.ravel()+1,'FREQ':cur.ravel().astype(int),'FREQ_CENSO':cen.ravel().astype(int)}))
pop=pd.concat(dsr,ignore_index=True); pop.to_pickle(V+'pop_ds.pkl')
for t,C in FIX.items():
    A=np.zeros((12,2,18,5)); np.add.at(A,uds,C); np.save(V+f'C{str(t)[2:]}.npy',A.astype(int))
print('linhas',len(P),'negativos',(P.FREQ<0).sum(),'tempo',round(time.time()-t0))
print(pop.groupby('ANO')[['FREQ','FREQ_CENSO']].sum().T.to_string())
