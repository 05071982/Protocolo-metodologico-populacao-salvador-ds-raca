import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, sys
sys.path.insert(0,'/home/claude/scripts'); from v4_lib import *
exec(open('/home/claude/scripts/idade_simples.py').read().split('# --- validation 2010')[0].split("b=pd.read_excel")[0])  # imports
src=open('/home/claude/scripts/idade_simples.py').read()
exec(src[src.index('# FXET of each single age'):src.index('# --- validation 2010')])   # FX, sprague, split_shape, obs_shape
D='/home/claude/data/'; V=D+'v5/'; V4=D+'v4/'
SES=pd.read_pickle(V4+'sesab.pkl'); R3=np.load(V4+'R3_2010.npy'); _A=np.load(V+'AGEu10.npy'); _ud=pd.read_csv(D+'units.csv').DS.values-1; OBS=np.zeros((12,2,101)); np.add.at(OBS,_ud,_A)
C00=np.load(V+'C00.npy').sum(3); C10=np.load(V+'C10.npy').sum(3); C22=np.load(V+'C22.npy').sum(3)
def calib(Cfx, seedP, colT):
    """Cfx: DS×sexo×FXET inteiros; seedP: DS×sexo×101 proporções dentro da faixa; colT: sexo×101 totais municipais por idade (NaN = sem restrição).
       devolve inteiros DS×sexo×101 que fecham nas faixas do DS e, onde houver, na idade municipal."""
    out=np.zeros((12,2,101),int); P=np.zeros((12,2,101))
    for s in range(2):
        for f in range(1,19):
            m=np.where(FX==f)[0]; rows=Cfx[:,s,f-1]
            X=seedP[:,s,m]/np.maximum(seedP[:,s,m].sum(1,keepdims=True),1e-12)*rows[:,None]
            if not np.isnan(colT[s,m]).any() and len(m)>1:
                X,_=ipf(X+1e-9,[(labels(X.shape,[1]),colT[s,m]),(labels(X.shape,[0]),rows.astype(float))],iters=2000)
                Xi=multi_round(X,[(labels(X.shape,[0]),rows),(labels(X.shape,[1]),colT[s,m].astype(int))])
            else:
                Xi=np.stack([lr_round(X[d],rows[d]) for d in range(12)])
            out[:,s,m]=Xi; P[:,s,m]=X/np.maximum(X.sum(1,keepdims=True),1e-12)
    return out,P
nan=np.full((2,101),np.nan)
# 2010: forma observada no banco por DS, calibrada às idades simples do universo (3175)
P10s=np.stack([[obs_shape(OBS[d,s]) for s in range(2)] for d in range(12)])
I10,P10=calib(C10,P10s,R3.sum(2).astype(float))
# 2022: Sprague por DS; 0–19 anos calibrados às idades simples do Censo 2022 (SESAB)
P22s=np.stack([[split_shape(C22[d,s],OBS[d,s,80:]) for s in range(2)] for d in range(12)])
c22=nan.copy(); c22[:,:20]=SES[2022][1]
I22,P22=calib(C22,P22s,c22)
# 2000: Sprague por DS (20+); 0–19 calibrados às idades simples do Censo 2000 (SESAB)
P00s=np.stack([[split_shape(C00[d,s],OBS[d,s,80:]) for s in range(2)] for d in range(12)])
c00=nan.copy(); c00[:,:20]=SES[2000][1]
I00,P00=calib(C00,P00s,c00)
for nm,I,C in [('2000',I00,C00),('2010',I10,C10),('2022',I22,C22)]:
    chk=np.stack([I[:,:,FX==f].sum(2) for f in range(1,19)],2)
    print(nm,'faixas DS ok:',(chk==C).all())
print('2010 idade municipal = 3175:',(I10.sum(0)==R3.sum(2)).all(),'| 2000 0–19 = censo:',(I00.sum(0)[:,:20]==SES[2000][1]).all(),'| 2022 0–19 = censo:',(I22.sum(0)[:,:20]==SES[2022][1]).all())
# série
pop=pd.read_pickle(V+'pop_ds.pkl'); G=pop.groupby(['ANO','DS','SEXO','FXET']).FREQ.sum().unstack('FXET')
eps=1e-6; rows=[]; FIX={2000:I00,2010:I10,2022:I22}
for (ano,ds,sx),r in G.iterrows():
    d,s=ds-1,sx-1
    if ano in FIX: out=FIX[ano][d,s]
    else:
        if ano<2010: w=(ano-2000)/10; A,B=P00,P10
        else: w=(ano-2010)/12; A,B=P10,P22
        q=np.exp((1-w)*np.log(A[d,s]+eps)+w*np.log(B[d,s]+eps)); out=np.zeros(101,int)
        for f in range(1,19):
            m=np.where(FX==f)[0]; out[m]=lr_round(q[m]/q[m].sum()*r[f],r[f])
    rows.append(pd.DataFrame({'ANO':ano,'DS':ds,'SEXO':sx,'IDADE':np.arange(101),'FXET':FX,'FREQ':out}))
PI=pd.concat(rows,ignore_index=True)
chk=PI.groupby(['ANO','DS','SEXO','FXET']).FREQ.sum().unstack('FXET')
print('linhas',len(PI),'| bate com FXET:',(chk.values==G.values).all(),'| negativos',(PI.FREQ<0).sum())
PI.to_pickle(V+'pop_idade.pkl')
np.save(V+'P00.npy',P00); np.save(V+'P10.npy',P10); np.save(V+'P22.npy',P22)
np.save(V+'I00.npy',I00); np.save(V+'I10.npy',I10); np.save(V+'I22.npy',I22)
