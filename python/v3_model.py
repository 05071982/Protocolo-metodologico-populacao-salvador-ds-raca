import warnings; warnings.filterwarnings('ignore')
import pandas as pd,numpy as np
D='/home/claude/data/'
R=['branco','preto','amarelo','pardo','indigena']
A11=['0a4','5a9','10a14','15a19','20a24','25a29','30a39','40a49','50a59','60a69','70m']
k=pd.read_csv(D+'chave.csv',dtype={'CD_SETOR':str,'CD_BAIRRO':str})
NM={'Vila Ruy Barbosa / Jardim Cruzeiro':'Vila Ruy Barbosa\\\\Jardim Cruzeiro','Centro Administrativo da Bahia - CAB':'Centro Administrativo da Bahia','Nordeste do Amaralina':'Nordeste de Amaralina',"Caixa D'água":'Caixa D´Água','Ilha dos Frades / Ilha de Santo Antônio':'Ilha dos Frades/Ilha de Santo Antônio','Beiru / Tancredo Neves':'Beiru/Tancredo Neves','Ilha Bom Jesus dos Passos':'Ilha de Bom Jesus dos Passos'}
print('sem bairro:',k.NM_BAIRRO.isna().sum(), k[k.NM_BAIRRO.isna()].CD_SETOR.tolist()[:5])
k['bairro']=k.NM_BAIRRO.replace(NM)
b=pd.read_csv(D+'bairros_final.csv')   # bairro,pop22,COD_BAIRRO
allnames=sorted(pd.read_csv(D+'setor_bairro_ds_2022.csv').bairro.tolist()); code={n:i+1 for i,n in enumerate(allnames)}
AQ=['292740805060214','292740805060258','292740805060274','292740805060421','292740805060436','292740805060477','292740805060478']
assert (k.loc[k.CD_SETOR.isin(AQ),'bairro']=='Pituba').all()
k.loc[k.CD_SETOR.isin(AQ),'bairro']='Aquarius'; code['Aquarius']=171
k['COD_BAIRRO']=k.bairro.map(code)
X=pd.read_pickle(D+'s22_sector_imputed.pkl').merge(k[['CD_SETOR','DS','COD_BAIRRO','bairro']],left_on='CD_setor',right_on='CD_SETOR')
print('setores c/ dados sem bairro:',X.COD_BAIRRO.isna().sum(), X[X.COD_BAIRRO.isna()].moradores.sum())
X['COD_BAIRRO']=X.COD_BAIRRO.fillna(0).astype(int)
# escala por bairro ao total oficial IBGE
off=b.set_index('COD_BAIRRO').pop22.copy()
obs=X.groupby('COD_BAIRRO').moradores.sum()
cp=code['Pituba']; tp=off[cp]; off[171]=tp*obs[171]/(obs[171]+obs[cp]); off[cp]=tp-off[171]
print('Aquarius 2022:',round(off[171]),' Pituba:',round(off[cp]),' setores AQ com dados:',X.CD_SETOR.isin(AQ).sum())
bb=b.copy(); bb.loc[bb.COD_BAIRRO==cp,'pop22']=off[cp]; bb=pd.concat([bb,pd.DataFrame({'bairro':['Aquarius'],'pop22':[off[171]],'COD_BAIRRO':[171],'DS':[bb.loc[bb.COD_BAIRRO==cp,'DS'].iloc[0]]})]); bb.to_csv(D+'bairros_final_v3.csv',index=False)
k.to_csv(D+'chave_v3.csv',index=False)
fac=(off/obs).reindex(obs.index); print('bairros sem setor com dados:', sorted(set(off.index)-set(obs.index)))
print('fator bairro: min %.3f mediana %.3f max %.3f'%(fac.min(),fac.median(),fac.max()))
fac=fac.fillna(1.0)
num=[c for c in X.columns if c not in ('CD_setor','CD_SETOR','DS','COD_BAIRRO','bairro')]
X[num]=X[num].mul(X.COD_BAIRRO.map(fac),axis=0)
G=X.groupby(['DS','COD_BAIRRO'])[num].sum()
print('total 2022:',round(G.moradores.sum()), ' unidades:',len(G))
S=pd.read_csv(D+'sesab2010.csv').pivot_table(index=['DS','SEXO'],columns='FXET',values='POP')
g4=[0,0,0,1,1,1,2,2,2,3,3]; g2=[0,0,1,1,1,1,1,1,1,1,1]
def fit(g,ds):
    N=g.moradores
    if N<=0: return np.zeros((2,18,5))
    nz=lambda M: M*N/M.sum() if M.sum()>0 else np.full(M.shape,N/M.size)
    M1=nz(np.array([[g[f'{s}_{a}'] for a in A11] for s in 'mf']))
    M2=nz(np.array([[g[f'{s}_{r}'] for r in R] for s in 'mf']))
    M3=nz(np.array([[g[f'{q}_{r}'] for r in R] for q in ['0a4','15a29','30a59','60m']]))
    M4=nz(np.array([[[g[f'{s}_{q}_{r}'] for r in R] for q in ['0a9','10m']] for s in 'mf']))
    X=np.ones((2,11,5)); sd=lambda a,b: np.where(b>0,a/np.where(b>0,b,1),0)
    for _ in range(200):
        X*=sd(M1[:,:,None],X.sum(2,keepdims=True)); X*=sd(M2[:,None,:],X.sum(1,keepdims=True))
        A=np.zeros((4,5)); [A.__setitem__(g4[i],A[g4[i]]+X[:,i,:].sum(0)) for i in range(11)]
        f=sd(M3,A); [X.__setitem__((slice(None),i,slice(None)),X[:,i,:]*f[g4[i]]) for i in range(11)]
        B=np.zeros((2,2,5))
        for i in range(11): B[:,g2[i],:]+=X[:,i,:]
        f=sd(M4,B)
        for i in range(11): X[:,i,:]*=f[:,g2[i],:]
    X*=N/X.sum()
    Y=np.zeros((2,18,5))
    for si,sx in enumerate([1,2]):
        s=S.loc[(ds,sx)].values; r2=lambda a,b: np.array([a,b])/(a+b)
        sp={0:(s[0:2]/s[0:2].sum(),[0,1]),1:([1],[2]),2:([1],[3]),3:([1],[4]),4:([1],[5]),5:([1],[6]),
            6:(r2(.4*s[4]+.6*s[5],.4*s[5]+.6*s[6]),[7,8]),7:(r2(.4*s[6]+.6*s[7],.4*s[7]+.6*s[8]),[9,10]),
            8:(r2(.4*s[8]+.6*s[9],.4*s[9]+.6*s[10]),[11,12]),9:(r2(.4*s[10]+.6*s[11],.4*s[11]+.6*s[12]),[13,14]),
            10:(s[15:18]/s[15:18].sum(),[15,16,17])}
        for i,(w,idx) in sp.items():
            for wj,j in zip(w,idx): Y[si,j,:]+=wj*X[si,i,:]
    return Y
units=list(G.index); U22=np.stack([fit(G.loc[u],u[0]) for u in units])
uds=np.array([u[0] for u in units]); ub=np.array([u[1] for u in units])
C22=np.stack([U22[uds==d].sum(0) for d in range(1,13)])
print('C22',round(C22.sum()), [round(C22[d].sum()) for d in range(12)])
np.save(D+'C22.npy',C22); np.save(D+'U22.npy',U22); pd.DataFrame({'DS':uds,'COD_BAIRRO':ub}).to_csv(D+'units.csv',index=False)
# 2010 raça (mesmo método da v1, semente = nova estrutura 2022 do DS)
race10={6:[104917,59657,3053,118255,857],7:[34103,24013,1358,56180,384],5:[39380,45731,1881,84347,565],9:[29580,53907,2741,98367,437],
12:[13858,32891,1528,56360,313],1:[21370,15114,833,35566,254],2:[20139,35466,1122,75194,247],8:[37818,44380,2563,87764,418],
4:[24170,56463,2219,92878,536],10:[27835,54431,2760,97299,510],3:[26000,67262,3187,118225,670],11:[31174,84843,4746,151515,705]}
C10=[]
for ds in range(1,13):
    M=np.array([S.loc[(ds,1)].values,S.loc[(ds,2)].values]); rr=np.array(race10[ds],float); rr=rr/rr.sum()*M.sum()
    Z=C22[ds-1]+0.01
    for _ in range(300): Z*=(M/Z.sum(2))[:,:,None]; Z*=(rr/Z.sum((0,1)))[None,None,:]
    C10.append(Z)
np.save(D+'C10.npy',np.stack(C10)); print('C10',round(np.stack(C10).sum()))
