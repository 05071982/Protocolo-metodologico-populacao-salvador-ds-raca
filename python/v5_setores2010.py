# v5 — Censo 2010 por setor censitário → unidades bairro × DS (limites atuais)
import pandas as pd, numpy as np
C='/home/claude/data/c2010/'; V='/home/claude/data/v5/'
import os; os.makedirs(V,exist_ok=True)
FX=np.array([1]+[2]*4+[3+(a-5)//5 for a in range(5,80)]+[18]*21)   # idade 0..100 -> FXET
# ---------- chave: setor -> unidade (maior área), restrita às 194 unidades de 2022 quando possível
k=pd.read_csv(C+'chave2010_codificada.csv',dtype={'CD_SETOR':str})
un=pd.read_csv('/home/claude/data/units.csv'); U=list(zip(un.DS,un.COD_BAIRRO)); Uidx={u:i for i,u in enumerate(U)}
k['u']=list(zip(k.DS,k.COD_BAIRRO.astype(int))); k['in22']=k.u.isin(Uidx)
k=k.sort_values(['CD_SETOR','area_int'],ascending=[True,False])
best=k.groupby('CD_SETOR').head(1).set_index('CD_SETOR')
best22=k[k.in22].groupby('CD_SETOR').head(1).set_index('CD_SETOR')
# ---------- dados por setor
def rd(f,enc='latin1'):
    d=pd.read_csv(C+f,sep=';',dtype=str,encoding=enc); d=d[d.Cod_setor.str.startswith('2927408')].set_index('Cod_setor')
    return d[[c for c in d.columns if c.startswith('V')]].apply(lambda s: pd.to_numeric(s.str.replace(',','.'),errors='coerce'))
P11=rd('Pessoa11_BA.csv'); P12=rd('Pessoa12_BA.csv'); P05=rd('Pessoa05_BA.csv')
P03=pd.read_csv(C+'Pessoa03_salvador.csv',sep=';',dtype=str).set_index('Cod_setor')
P03=P03[[c for c in P03.columns if c.startswith('V')]].apply(lambda s: pd.to_numeric(s,errors='coerce'))
setores=P11.index
sup=P11.V022.isna()|P03.V002.isna()
print('setores',len(setores),'| suprimidos (x):',int(sup.sum()),'| pop suprimida',int((P11.V001+P12.V001)[sup].sum()))
# idade simples por sexo: V022 (<1) + V035..V134 (1..100+)
def ages(P): return np.column_stack([P.V022.values]+[P['V%03d'%v].values for v in range(35,135)])
AGE=np.stack([ages(P11),ages(P12)],1)      # setor × sexo × 101
TOTS=np.stack([P11.V001.values,P12.V001.values],1)
# raça × sexo × grupos G: 0-4 (P05), 5-9 (5-6 + 7-9), 10-14, 15-19, 20-24..55-59, 60-69, 70+
G=['0-4','5-9','10-14','15-19','20-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-69','70+']
def raca_sexo(base):   # base = 87 (homens) ou 167 (mulheres)
    blocks=[[base,base+5]]                                      # 5-6 e 7-9 -> 5-9
    starts=[base+10,base+15]+[base+30+5*i for i in range(10)]   # 10-14,15-19, (pula 15-17 e 18-19), 20-24..70+
    out=[]
    v=lambda s: P03[['V%03d'%(s+j) for j in range(5)]].values
    out.append(v(base)+v(base+5))
    for s in starts: out.append(v(s))
    return np.stack(out,1)   # setor × 13 grupos (5-9..70+) × 5 raças
RM=raca_sexo(87); RF=raca_sexo(167)
R04=np.stack([P05[['V%03d'%i for i in range(1,6)]].values,P05[['V%03d'%i for i in range(6,11)]].values],1)  # setor × sexo × raça (0-4)
RG=np.concatenate([R04[:,:,None,:],np.stack([RM,RF],1)],2)   # setor × sexo × 14 G × 5 raças
GX=np.array([0,0,1,2,3,4,5,6,7,8,9,10,11,12,12,13,13,13])   # FXET -> G
# conferências nos setores não suprimidos
ok=~sup.values
print('soma idades = total por sexo (não suprimidos):',np.abs(np.nansum(AGE[ok],2)-TOTS[ok]).max())
gs=np.zeros((ok.sum(),2,14))
for f in range(18): gs[:,:,GX[f]]+=np.stack([AGE[ok][:,:,FX==f+1].sum(2)],0)[0]
print('raça×grupo = idade×grupo (máx dif por setor):',np.nanmax(np.abs(np.nansum(RG[ok],3)-gs)))
np.savez(V+'setores2010.npz',AGE=AGE,TOTS=TOTS,RG=RG,sup=sup.values,setores=np.array(setores))
sec=pd.DataFrame({'CD_SETOR':setores})
sec['u']=sec.CD_SETOR.map(best.u); sec['u22']=sec.CD_SETOR.map(best22.u); sec['prop']=sec.CD_SETOR.map(best.prop_area)
sec['pop']=TOTS.sum(1)
print('sem chave:',sec.u.isna().sum(),' pop',sec[sec.u.isna()]['pop'].sum())
fora=sec[sec.u.notna()&(sec.u!=sec.u22)]
print('setores cuja maior área cai em unidade fora das 194:',len(fora),' pop',int(fora['pop'].sum()))
print(fora.groupby(fora.u.astype(str))['pop'].sum().sort_values(ascending=False).head(10))
print('setores com <90% da área na unidade:',(sec.prop<0.9).sum(),' <50%:',(sec.prop<0.5).sum())
sec.to_pickle(V+'chave2010.pkl')
