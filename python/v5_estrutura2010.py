import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, sys
sys.path.insert(0,'/home/claude/scripts'); from v4_lib import *
V='/home/claude/data/v5/'; V4='/home/claude/data/v4/'
z=np.load(V+'setores2010.npz',allow_pickle=True); AGE,TOTS,RG,sup=z['AGE'],z['TOTS'],z['RG'],z['sup']
sec=pd.read_pickle(V+'chave2010.pkl')
un=pd.read_csv('/home/claude/data/units.csv'); U=list(zip(un.DS,un.COD_BAIRRO)); Uidx={u:i for i,u in enumerate(U)}; nu=len(U); uds=un.DS.values-1
sec['uf']=[Uidx[u] if isinstance(u,tuple) else Uidx[(11,120)] for u in sec.u22]
FX=np.array([1]+[2]*4+[3+(a-5)//5 for a in range(5,80)]+[18]*21)-1
GX=np.array([0,0,1,2,3,4,5,6,7,8,9,10,11,12,12,13,13,13])
ok=~sup; ui=np.array(sec.uf.values,int)
AGEu=np.zeros((nu,2,101)); RGu=np.zeros((nu,2,14,5)); TOTu=np.zeros((nu,2))
np.add.at(AGEu,ui[ok],np.nan_to_num(AGE[ok])); np.add.at(RGu,ui[ok],np.nan_to_num(RG[ok])); np.add.at(TOTu,ui,TOTS)
# setores suprimidos: totais por sexo conhecidos; idade e raça pela distribuição da própria unidade
for i in np.where(sup)[0]:
    u=ui[i]
    for s in range(2):
        a=AGEu[u,s]/max(AGEu[u,s].sum(),1); r=RGu[u,s]/max(RGu[u,s].sum(),1)
        AGEu[u,s]+=a*TOTS[i,s]; RGu[u,s]+=r*TOTS[i,s]
print('total',TOTu.sum(),' idade',AGEu.sum(),' raça',RGu.sum())
A=np.stack([AGEu[:,:,FX==f].sum(2) for f in range(18)],2)      # u × s × 18
R3=np.load(V4+'R3_2010.npy'); R10=np.stack([R3[:,FX==f].sum(1) for f in range(18)],1)   # s×18×5 (universo 3175)
print('sexo×FXET setores − 3175: máx',np.abs(A.sum(0)-R10.sum(2)).max(),' total',A.sum()-R10.sum())
print('raça setores (soma grupos) vs 3175:',RGu.sum((0,1,2)).round(), R10.sum((0,1)))
# semente: idade do setor × proporção de raça no grupo G (unidade, sexo); sem raça -> proporção do DS
seed=np.zeros((nu,2,18,5))
RGds=np.zeros((12,2,14,5)); np.add.at(RGds,uds,RGu)
for f in range(18):
    g=GX[f]; r=RGu[:,:,g,:]; tot=r.sum(2,keepdims=True)
    rd=RGds[uds][:,:,g,:]; rd=rd/np.maximum(rd.sum(2,keepdims=True),1e-9)
    p=np.where(tot>0,r/np.maximum(tot,1e-9),rd)
    seed[:,:,f,:]=A[:,:,f,None]*p
sh=seed.shape
# calibração: unidade × sexo × faixa (setores, ajustado ao universo), unidade × sexo × G × raça (setores, proporção), sexo × faixa × raça (3175)
At=A.copy()
for s in range(2):
    for f in range(18):
        At[:,s,f]=A[:,s,f]*R10[s,f].sum()/A[:,s,f].sum()
Lusf=labels(sh,[0,1,2]); Lsfr=labels(sh,[1,2,3])
idx=np.indices(sh); Lugr=((idx[0]*2+idx[1])*14+GX[idx[2]])*5+idx[3]
RGt=np.zeros((nu,2,14,5))
for f in range(18): pass
# raça no grupo reescalonada para o total de idade do grupo
Ag=np.zeros((nu,2,14)); 
for f in range(18): Ag[:,:,GX[f]]+=At[:,:,f]
RGt=np.where(RGu.sum(3,keepdims=True)>0,RGu/np.maximum(RGu.sum(3,keepdims=True),1e-9),0)*Ag[...,None]
X,e=ipf(seed+1e-6,[(Lugr,RGt.ravel()),(Lsfr,R10.ravel().astype(float)),(Lusf,At.ravel())],iters=3000)
print('IPF resíduo',e,' | unidade×sexo×faixa máx dif',np.abs(X.sum(3)-At).max(),' | 3175 máx dif',np.abs(X.sum(0)-R10).max())
dev=np.abs(np.bincount(Lugr.ravel(),X.ravel(),minlength=RGt.size)-RGt.ravel()); print('unidade×sexo×G×raça: desvio máx',dev.max().round(1),' soma desvios',dev.sum().round())
np.save(V+'U10f.npy',X); np.save(V+'AGEu10.npy',AGEu)
# DS 2010 nos limites atuais vs tabela SESAB (limites antigos)
ds=np.array([X[uds==d].sum() for d in range(12)]); s10=pd.read_csv('/home/claude/data/sesab2010.csv').groupby('DS').POP.sum().values
nm=pd.read_csv('/home/claude/protocolo-metodologico-populacao-salvador-ds-raca/dados/dicionarios/ds.csv').NOME_DS.values
print(pd.DataFrame({'DS':nm,'setores_limites_atuais':ds.round(),'SESAB_limites_2010':s10,'dif%':((ds/s10-1)*100).round(1)}).to_string())
