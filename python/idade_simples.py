import warnings; warnings.filterwarnings('ignore')
import pandas as pd,numpy as np
D='/home/claude/data/'
b=pd.read_excel(D+'idade/banco2010.xlsx').dropna(subset=['distrito_sanitario'])
nm={'Barra/ Rio Vermelho':6,'Boca do Rio':7,'Brotas':5,'Cabula/ Beiru':9,'Cajazeiras':12,'Centro Histórico':1,'Itapagipe':2,'Itapuã':8,'Liberdade':4,'Pau da Lima':10,'São Caetano/ Valéria':3,'Subúrbio Ferroviário':11}
b['DS']=b.distrito_sanitario.map(nm); assert b.DS.notna().all()
# observed single ages 2010 by DS x sex: 0..99, 100+
OBS=np.zeros((12,2,101))
for _,r in b.iterrows():
    for si,s in enumerate('mf'):
        v=[r[f'{s}_me_1ano']]+[r[f'{s}_{a}ano'] for a in range(1,100)]+[r[f'{s}_100ano_m']]
        OBS[int(r.DS)-1,si]=v
# FXET of each single age
FX=np.array([1]+[2]*4+[3+(a-5)//5 for a in range(5,80)]+[18]*21)  # ages 0..100
assert FX[79]==17 and FX[80]==18 and FX[5]==3 and FX[14]==4
# Sprague multipliers
P1=np.array([[.3616,-.2768,.1488,-.0336,0],[.2640,-.0960,.0400,-.0080,0],[.1840,.0400,-.0320,.0080,0],[.1200,.1360,-.0720,.0160,0],[.0704,.1968,-.0848,.0176,0]])
P2=np.array([[.0336,.2272,-.0752,.0144,0],[.0080,.2320,-.0480,.0080,0],[-.0080,.2160,-.0080,0,0],[-.0160,.1840,.0400,-.0080,0],[-.0176,.1408,.0912,-.0144,0]])
PM=np.array([[-.0128,.0848,.1504,-.0240,.0016],[-.0016,.0144,.2224,-.0416,.0064],[.0064,-.0336,.2544,-.0336,.0064],[.0064,-.0416,.2224,.0144,-.0016],[.0016,-.0240,.1504,.0848,-.0128]])
PN=P2[::-1,::-1]; PL=P1[::-1,::-1]
def sprague(G):  # G: 16 five-year groups 0-4..75-79 -> 80 single ages
    n=len(G); out=np.zeros(n*5)
    for i in range(n):
        if i==0: M,w=P1,G[0:5]
        elif i==1: M,w=P2,G[0:5]
        elif i==n-2: M,w=PN,G[n-5:n]
        elif i==n-1: M,w=PL,G[n-5:n]
        else: M,w=PM,G[i-2:i+3]
        out[i*5:i*5+5]=M@w
    return out
def split_shape(F18, obs80=None):
    """F18: 18 FXET counts -> within-group proportions for ages 0..100 (80+ uses obs80 shape)"""
    G=np.r_[F18[0]+F18[1],F18[2:17]]          # 16 groups 0-4..75-79
    s=sprague(G)
    p=np.zeros(101)
    p[0]=1.0
    v=np.clip(s[1:5],0,None); p[1:5]=v/v.sum() if v.sum()>0 else .25
    for g in range(1,16):
        v=np.clip(s[g*5:g*5+5],0,None); p[g*5:g*5+5]=v/v.sum() if v.sum()>0 else .2
    o=obs80 if obs80 is not None else np.ones(21); p[80:]=o/o.sum()
    return p
def obs_shape(O):
    p=np.zeros(101)
    for f in range(1,19):
        m=FX==f; t=O[m].sum(); p[m]=O[m]/t if t>0 else 1/m.sum()
    return p
# --- validation 2010: Sprague from observed 5-yr groups vs observed single ages
err=[];errw=[]
for d in range(12):
    for s in range(2):
        O=OBS[d,s]; F18=np.array([O[FX==f].sum() for f in range(1,19)])
        p=split_shape(F18,O[80:]); est=p*F18[FX-1]
        m=(np.arange(101)>=1)&(np.arange(101)<80)
        e=np.abs(est[m]-O[m]); err.append(e.sum()/O[m].sum()); errw.append(np.mean(e/np.maximum(O[m],1)))
print('Sprague 2010 (DS×sexo, idades 1-79): erro absoluto total %.2f%% | MAPE por idade %.2f%%'%(np.mean(err)*100,np.mean(errw)*100))
# municipal check with Pessoa11/12 (full census)
def mun(f):
    x=pd.read_csv(D+'idade/'+f,sep=';',dtype={'Cod_setor':str},encoding='latin1')
    x=x[x.Cod_setor.str.startswith('2927408')]
    v=x.drop(columns=['Cod_setor','Situacao_setor']).replace('X',0).apply(pd.to_numeric,errors='coerce').fillna(0).sum()
    return v
v=mun('Pessoa11_BA.csv'); print('Pessoa11 V001', v['V001'], ' n cols',len(v)); np.save(D+'idade/OBS2010.npy',OBS)

# ---------------- construção da série por idade simples ----------------
pop=pd.read_pickle(D+'pop_ds.pkl')            # FREQ TCU, DS×sexo×FXET×raça
G=pop.groupby(['ANO','DS','SEXO','FXET']).FREQ.sum().unstack('FXET')   # anos×DS×sexo x 18
C22=np.load(D+'C22.npy').sum(3)               # DS×sexo×FXET (2022, fracionário)
P10=np.zeros((12,2,101)); P22=np.zeros((12,2,101))
for d in range(12):
    for s in range(2):
        P10[d,s]=obs_shape(OBS[d,s]); P22[d,s]=split_shape(C22[d,s],OBS[d,s,80:])
np.save(D+'idade/P10.npy',P10); np.save(D+'idade/P22.npy',P22)
def lr(x,total):
    fl=np.floor(x); rem=int(round(total-fl.sum()))
    if rem>0: idx=np.argsort(-(x-fl),kind='stable')[:rem]; fl[idx]+=1
    return fl.astype(int)
eps=1e-6; rows=[]
for (ano,ds,sx),r in G.iterrows():
    w=(ano-2010)/12; d,s=ds-1,sx-1
    q=np.exp((1-w)*np.log(P10[d,s]+eps)+w*np.log(P22[d,s]+eps))
    out=np.zeros(101,int)
    for f in range(1,19):
        m=np.where(FX==f)[0]; pp=q[m]/q[m].sum(); out[m]=lr(pp*r[f],r[f])
    rows.append(pd.DataFrame({'ANO':ano,'DS':ds,'SEXO':sx,'IDADE':np.arange(101),'FXET':FX,'FREQ':out}))
PI=pd.concat(rows,ignore_index=True)
chk=PI.groupby(['ANO','DS','SEXO','FXET']).FREQ.sum().unstack('FXET')
print('linhas',len(PI),'| bate com FXET da base principal:',(chk.values==G.values).all(),'| negativos',(PI.FREQ<0).sum())
PI.to_pickle(D+'idade/pop_idade.pkl')
s=PI[PI.ANO==2022].groupby('IDADE').FREQ.sum(); print('2022 idades 0-14:',s.iloc[:15].tolist())
