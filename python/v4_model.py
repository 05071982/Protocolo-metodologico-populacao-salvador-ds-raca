# v4: calibração censitária (2000, 2010, 2022) mantendo a estrutura interna dos setores censitários
import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, sys
sys.path.insert(0,'/home/claude/scripts'); from v4_lib import *
D='/home/claude/data/'; V=D+'v4/'
SES=pd.read_pickle(V+'sesab.pkl'); T3175=np.load(V+'T3175.npy'); DS00=np.load(V+'DS00.npy'); R00=np.load(V+'R00.npy')
FXA=np.array([1]+[2]*4+[3+(a-5)//5 for a in range(5,80)]+[18]*21)-1   # idade 0..100 -> FXET-1
C10o=np.load(D+'C10.npy'); C22o=np.load(D+'C22.npy'); U22o=np.load(D+'U22.npy'); un=pd.read_csv(D+'units.csv'); uds=un.DS.values-1
sh=(12,2,18,5); rep={}
# ---------------- 2010 ----------------
# raça × sexo × idade (universo, 3175): sem declaração redistribuída proporcionalmente em cada sexo×idade
R3=np.zeros((2,101,5),int)
for s in range(2):
    for a in range(101):
        v=T3175[s,a]; R3[s,a]=lr_round(v[:5]/v[:5].sum()*v.sum(),v.sum()) if v[:5].sum()>0 else lr_round(np.full(5,v.sum()/5),v.sum())
R10=np.zeros((2,18,5),int)
for f in range(18): R10[:,f]=R3[:,FXA==f].sum(1)
np.save(V+'R3_2010.npy',R3)
S10=pd.read_csv(D+'sesab2010.csv').pivot_table(index=['DS','SEXO'],columns='FXET',values='POP').values.reshape(12,2,18)
M1=np.zeros((12,2,18),int)
for s in range(2):
    for f in range(18): M1[:,s,f]=lr_round(S10[:,s,f]/S10[:,s,f].sum()*R10[s,f].sum(),R10[s,f].sum())
rep['2010: ajuste máx. da tabela SESAB por DS para fechar no universo 3175 (pessoas)']=int(np.abs(M1-S10).max())
race10={6:[104917,59657,3053,118255,857],7:[34103,24013,1358,56180,384],5:[39380,45731,1881,84347,565],9:[29580,53907,2741,98367,437],
12:[13858,32891,1528,56360,313],1:[21370,15114,833,35566,254],2:[20139,35466,1122,75194,247],8:[37818,44380,2563,87764,418],
4:[24170,56463,2219,92878,536],10:[27835,54431,2760,97299,510],3:[26000,67262,3187,118225,670],11:[31174,84843,4746,151515,705]}
RB=np.array([race10[d] for d in range(1,13)],float)
RB,_=ipf(RB,[(labels((12,5),[0]),M1.sum((1,2)).astype(float)),(labels((12,5),[1]),R10.sum((0,1)).astype(float))])
L_dsf=labels(sh,[0,1,2]); L_sfr=labels(sh,[1,2,3]); L_dr=labels(sh,[0,3])
C10f,e=ipf(C10o+0.01,[(L_dr,RB.ravel()),(L_sfr,R10.ravel().astype(float)),(L_dsf,M1.ravel().astype(float))],iters=2000)
C10=multi_round(C10f,[(L_dsf,M1.ravel()),(L_sfr,R10.ravel())])
rep['2010: resíduo IPF']=float(e)
# ---------------- 2022 ----------------
F22=SES[2022][0].astype(int)
g11=np.array([0,0,1,2,3,4,5,6,6,7,7,8,8,9,9,10,10,10])
nu=U22o.shape[0]; shu=U22o.shape
Lu=labels(shu,[0]); Lsfm=labels(shu,[1,2])
A11=np.zeros((nu,2,11,5))
for f in range(18): A11[:,:,g11[f],:]+=U22o[:,:,f,:]
idx=np.indices(shu); Lua=((idx[0]*2+idx[1])*11+g11[idx[2]])*5+idx[3]
Lur=labels(shu,[0,3])
ut=U22o.sum((1,2,3))
U22,e=ipf(U22o+1e-4,[(Lur,U22o.sum((1,2)).ravel()),(Lu,ut),(Lsfm,F22.ravel().astype(float))],iters=3000)
rep['2022: resíduo margem sexo×FXET (deve ~0)']=float(np.abs(U22.sum((0,3))-F22).max())
rep['2022: desvio máx. total de unidade bairro×DS (pessoas)']=float(np.abs(U22.sum((1,2,3))-ut).max())
rep['2022: desvio relativo máx. unidade×sexo×idade11×raça vs setores (%)']=float(np.nanmax(np.abs(np.bincount(Lua.ravel(),U22.ravel(),minlength=A11.size)/np.where(A11.ravel()>50,A11.ravel(),np.nan)-1))*100)
C22f=np.stack([U22[uds==d].sum(0) for d in range(12)])
dst=lr_round(C22f.sum((1,2,3)),2417678)
C22=multi_round(C22f,[(labels(sh,[0]),dst),(labels(sh,[1,2]),F22.ravel())])
# ---------------- 2000 ----------------
F00=SES[2000][0].astype(int); R00i=lr_round(R00/R00.sum()*2443107,2443107)
C00f,e=ipf(C10.astype(float)+0.01,[(labels(sh,[3]),R00i.astype(float)),(labels(sh,[0]),DS00.astype(float)),(labels(sh,[1,2]),F00.ravel().astype(float))],iters=3000)
rep['2000: resíduo IPF']=float(e)
C00=multi_round(C00f,[(labels(sh,[0]),DS00),(labels(sh,[1,2]),F00.ravel()),(labels(sh,[3]),R00i)])
np.save(V+'C00.npy',C00); np.save(V+'C10.npy',C10); np.save(V+'C22.npy',C22); np.save(V+'U22.npy',U22); np.save(V+'R00i.npy',R00i)
for k,v in rep.items(): print(k,':',round(v,4) if isinstance(v,float) else v)
print('2000 DS',(C00.sum((1,2,3))==DS00).all(),' sexo×FX',(C00.sum((0,3))==F00).all(),' raça',(C00.sum((0,1,2))==R00i).all())
print('2010 DS×sexo×FX',(C10.sum(3)==M1).all(),' sexo×FX×raça=3175',(C10.sum(0)==R10).all())
print('2022 sexo×FX=censo',(C22.sum((0,3))==F22).all(),' DS',(C22.sum((1,2,3))==dst).all(), ' total',C22.sum())
