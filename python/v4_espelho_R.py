# Espelho fiel de R/04 e R/05 (v4), lendo apenas os CSV do repositório; compara com a referência Python
import pandas as pd, numpy as np, sys
R='/home/claude/protocolo-metodologico-populacao-salvador-ds-raca/'; V='/home/claude/data/v4/'
tot=pd.read_csv(R+'dados/entrada/totais_municipais.csv')
if len(sys.argv)>1: tot=pd.concat([tot,pd.DataFrame({'ANO':[2027],'TOTAL':[2555000],'FONTE':['teste'],'CENSITARIO':[0]})])
k=['DS','SEXO','FXET','RACA']; le=lambda a: pd.read_csv(R+'dados/estrutura/'+a)
e={a:le(f'estrutura_{a}_ds.csv').sort_values(k).reset_index(drop=True) for a in (2000,2010,2022)}
u22=le('estrutura_2022_bairro_ds.csv')
def arr(x,total):
    fl=np.floor(x); rem=int(round(total-fl.sum()))
    if rem>0: idx=np.argsort(-(x-fl),kind='stable')[:rem]; fl[idx]+=1
    return fl.astype(int)
part=lambda C:(C+.5)/(C+.5).sum(); s00,s10,s22=[part(e[a].POP.values) for a in (2000,2010,2022)]
def comp(ano):
    if ano<2010: w=(ano-2000)/10; s=np.exp((1-w)*np.log(s00)+w*np.log(s10))
    else: w=(ano-2010)/12; s=np.exp((1-w)*np.log(s10)+w*np.log(s22))
    return s/s.sum()
rows=[]
for ano,Tt in zip(tot.ANO,tot.TOTAL):
    Xi=e[ano].POP.values if ano in e else arr(comp(ano)*Tt,round(Tt))
    d=e[2010][k].copy(); d['ANO']=ano; d['FREQ_DS']=Xi; rows.append(d)
sd=pd.concat(rows)
c=u22.groupby(k).POP.sum().rename('C22_DS').reset_index(); u=u22.merge(c,on=k)
tu=u.groupby('UNIDADE').POP.transform('sum'); uds=u.groupby('UNIDADE').DS.first(); tud=u.groupby('UNIDADE').POP.sum().groupby(uds).sum()
u['SH']=np.where(u.C22_DS>0,u.POP/u.C22_DS.where(u.C22_DS>0,1),tu/u.DS.map(tud))
out=[]
for ano in tot.ANO:
    d=u[['UNIDADE','DS','COD_BAIRRO']+k[1:]+['SH']].merge(sd[sd.ANO==ano],on=k)
    d['X']=d.FREQ_DS*d.SH; d['FL']=np.floor(d.X+1e-9); d['FR']=d.X-d.FL
    d=d.sort_values(k+['FR','UNIDADE'],ascending=[True]*4+[False,True],kind='stable')
    falta=d.FREQ_DS-d.groupby(k).FL.transform('sum'); pos=d.groupby(k).cumcount()+1
    d['FREQ']=(d.FL+(pos<=falta)).astype(int); out.append(d[['ANO','DS','COD_BAIRRO','FXET','SEXO','RACA','FREQ']])
pop=pd.concat(out)
assert (pop.groupby('ANO').FREQ.sum().values==tot.TOTAL.round().values).all() and (pop.FREQ>=0).all()
ref=pd.read_pickle(V+'pop_full.pkl')
m=pop.merge(ref,on=['ANO','DS','COD_BAIRRO','FXET','SEXO','RACA'],suffixes=('_R','_ref'))
print('04: linhas',len(pop),'| comparadas',len(m),'| células diferentes:',(m.FREQ_R!=m.FREQ_ref).sum())
# ---- 05
fx=pop.groupby(['ANO','DS','SEXO','FXET']).FREQ.sum()
prop=le('proporcao_idade_simples_na_faixa.csv').sort_values(['DS','SEXO','IDADE']); fixo=le('idade_simples_censos_ds.csv')
eps=1e-6; res=[]
for ano in sorted(tot.ANO):
    for ds in range(1,13):
        for sx in (1,2):
            p=prop[(prop.DS==ds)&(prop.SEXO==sx)]
            if ano in (2000,2010,2022): freq=fixo[(fixo.ANO==ano)&(fixo.DS==ds)&(fixo.SEXO==sx)].sort_values('IDADE').FREQ.values
            else:
                A,B,w=(p.P2000.values,p.P2010.values,(ano-2000)/10) if ano<2010 else (p.P2010.values,p.P2022.values,(ano-2010)/12)
                q=np.exp((1-w)*np.log(A+eps)+w*np.log(B+eps)); freq=np.zeros(len(p),int)
                for f in range(1,19):
                    mm=np.where(p.FXET.values==f)[0]; tf=fx[(ano,ds,sx,f)]; freq[mm]=arr(q[mm]/q[mm].sum()*tf,tf)
            res.append(pd.DataFrame({'ANO':ano,'DS':ds,'SEXO':sx,'IDADE':p.IDADE.values,'FREQ':freq}))
pi=pd.concat(res); ri=pd.read_pickle(V+'pop_idade.pkl')
m=pi.merge(ri,on=['ANO','DS','SEXO','IDADE'],suffixes=('_R','_ref'))
c=pi.merge(prop[['DS','SEXO','IDADE','FXET']]).groupby(['ANO','DS','SEXO','FXET']).FREQ.sum()
print('05: comparadas',len(m),'| células diferentes:',(m.FREQ_R!=m.FREQ_ref).sum(),'| faixas batem:',(c.values==fx.loc[c.index].values).all())
if len(sys.argv)>1: print('2027 teste: total',pop[pop.ANO==2027].FREQ.sum(),'| idade',pi[pi.ANO==2027].FREQ.sum())
