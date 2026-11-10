import pandas as pd,numpy as np
D='/home/claude/data/'
a=pd.read_pickle(D+'s22_raw.pkl')
R=['branco','preto','amarelo','pardo','indigena']
A11=['0a4','5a9','10a14','15a19','20a24','25a29','30a39','40a49','50a59','60a69','70m']
cols=[c for c in a.columns if c not in ('CD_setor','DS','k','Cod_municipio')]
X=a[cols].replace('X',np.nan).apply(pd.to_numeric,errors='coerce')
X['populacao']=X['populacao'].fillna(X['moradores'])
X['moradores']=X['moradores'].fillna(X['populacao'])
def fill(total, parts):
    """distribute residual of total among NaN parts equally (>=0)"""
    T=X[total]; P=X[parts]; known=P.sum(1,skipna=True); nmiss=P.isna().sum(1)
    res=(T-known).clip(lower=0); val=(res/nmiss.replace(0,np.nan))
    for c in parts: X[c]=X[c].fillna(val)
    X[parts]=X[parts].fillna(0)
# totals first
for t,o in (('masculino','feminino'),('feminino','masculino')):
    X[t]=X[t].fillna(X['moradores']-X[o])
fill('moradores',['masculino','feminino'])
fill('masculino',['m_'+x for x in A11]); fill('feminino',['f_'+x for x in A11])
fill('moradores',R); fill('masculino',['m_'+r for r in R]); fill('feminino',['f_'+r for r in R])
for sx,s in (('m','masculino'),('f','feminino')):
    X[sx+'_0a9']=X[sx+'_0a4']+X[sx+'_5a9']; X[sx+'_10m']=X[s]-X[sx+'_0a9']
    fill(sx+'_0a9',[f'{sx}_0a9_{r}' for r in R]); fill(sx+'_10m',[f'{sx}_10m_{r}' for r in R])
age4={'0a4':['0a4','5a9','10a14'],'15a29':['15a19','20a24','25a29'],'30a59':['30a39','40a49','50a59'],'60m':['60a69','70m']}
for g,ags in age4.items():
    X['tot_'+g]=sum(X['m_'+x]+X['f_'+x] for x in ags); fill('tot_'+g,[f'{g}_{r}' for r in R])
X['CD_setor']=a['CD_setor'].values; X.drop_duplicates('CD_setor').to_pickle(D+'s22_sector_imputed.pkl')
X['w']=1/a['k']; X['DS']=a['DS']; X=X.drop(columns=['CD_setor'])
W=X.drop(columns=['DS','w']).mul(X.w,axis=0); W['DS']=X.DS
G=W.groupby('DS').sum()
G.to_pickle(D+'ds2022_margins.pkl')
print(G[['moradores','masculino','feminino']].round().astype(int)); print(G.moradores.sum())
# consistency
print('race vs pop:',(G[R].sum(1)/G.moradores).round(4).tolist())
