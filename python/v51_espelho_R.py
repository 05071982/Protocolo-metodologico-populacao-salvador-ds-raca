# Espelho fiel de R/04 (v5) e R/05, lendo só os CSV do repositório; compara com a referência Python
import pandas as pd, numpy as np, sys
R='/home/claude/protocolo-metodologico-populacao-salvador-ds-raca/'; V='/home/claude/data/v51/'
tot=pd.read_csv(R+'dados/entrada/totais_municipais.csv')
if len(sys.argv)>1: tot=pd.concat([tot,pd.DataFrame({'ANO':[2027],'TOTAL':[2555000],'FONTE':['teste'],'CENSITARIO':[0]})])
k=['UNIDADE','SEXO','FXET','RACA']
le=lambda a: pd.read_csv(R+'dados/estrutura/'+a).sort_values(k).reset_index(drop=True)
e={a:le(f'estrutura_{a}_unidade.csv') for a in (2000,2010,2022)}; cel=e[2010][['UNIDADE','DS','COD_BAIRRO','SEXO','FXET','RACA']]
def arr(x,total):
    fl=np.floor(x); rem=int(round(total-fl.sum()))
    if rem>0: idx=np.argsort(-(x-fl),kind='stable')[:rem]; fl[idx]+=1
    return fl.astype(int)
part=lambda C,eps:(C+eps)/(C+eps).sum()
C={a:e[a].POP.values for a in e}; s00,s10,s22=[part(C[a],0.1) for a in (2000,2010,2022)]
def comp(ano):
    if ano<2010: w=(ano-2000)/10; s=np.exp((1-w)*np.log(s00)+w*np.log(s10))
    else: w=(ano-2010)/12; s=np.exp((1-w)*np.log(s10)+w*np.log(s22))
    return s/s.sum()
key=cel.DS.astype(str)+' '+cel.SEXO.astype(str)+' '+cel.FXET.astype(str)+' '+cel.RACA.astype(str)
dsc=cel[['DS','SEXO','FXET','RACA']].drop_duplicates().sort_values(['DS','SEXO','FXET','RACA'])
kds=list(dsc.DS.astype(str)+' '+dsc.SEXO.astype(str)+' '+dsc.FXET.astype(str)+' '+dsc.RACA.astype(str)); pos_k={x:i for i,x in enumerate(kds)}
ki=key.map(pos_k).values
D10=np.bincount(ki,C[2010],minlength=len(kds)); D22=np.bincount(ki,C[2022],minlength=len(kds))
d10,d22=part(D10,0.5),part(D22,0.5)
tu=pd.Series(C[2022]).groupby(cel.UNIDADE).sum(); udsm=cel.groupby('UNIDADE').DS.first(); tds=tu.groupby(udsm).sum()
fb=(cel.UNIDADE.map(tu)/cel.DS.map(tds)).values
SH=np.where(D22[ki]>0,C[2022]/np.where(D22[ki]>0,D22[ki],1),fb)
def extrap(ano,T):
    w=(ano-2010)/12; s=np.exp((1-w)*np.log(d10)+w*np.log(d22)); s/=s.sum()
    Xd=arr(s*T,round(T)); X=Xd[ki]*SH; FL=np.floor(X+1e-9); FR=X-FL
    df=pd.DataFrame({'k':ki,'FR':-FR,'U':cel.UNIDADE.values,'i':np.arange(len(X))}).sort_values(['k','FR','U'],kind='stable')
    df['pos']=df.groupby('k').cumcount()+1; pos=np.empty(len(X),int); pos[df.i.values]=df.pos.values
    falta=Xd[ki]-pd.Series(FL).groupby(ki).transform('sum').values
    return (FL+(pos<=falta)).astype(int)
out=[]
for ano,T in zip(tot.ANO,tot.TOTAL):
    Xi=C[ano] if ano in C else (extrap(ano,T) if ano>2022 else arr(comp(ano)*T,round(T)))
    d=cel[['DS','COD_BAIRRO','FXET','SEXO','RACA']].copy(); d['ANO']=ano; d['FREQ']=Xi; out.append(d)
pop=pd.concat(out); assert (pop.groupby('ANO').FREQ.sum().values==tot.TOTAL.round().values).all() and (pop.FREQ>=0).all()
ref=pd.read_pickle(V+'pop_full.pkl')
m=pop.merge(ref,on=['ANO','DS','COD_BAIRRO','FXET','SEXO','RACA'],suffixes=('_R','_ref'))
print('04: linhas',len(pop),'| comparadas',len(m),'| células diferentes:',(m.FREQ_R!=m.FREQ_ref).sum())
fx=pop.groupby(['ANO','DS','SEXO','FXET']).FREQ.sum()
prop=pd.read_csv(R+'dados/estrutura/proporcao_idade_simples_na_faixa.csv').sort_values(['DS','SEXO','IDADE']); fixo=pd.read_csv(R+'dados/estrutura/idade_simples_censos_ds.csv')
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
pi=pd.concat(res); ri=pd.read_pickle(V+'pop_idade.pkl'); m=pi.merge(ri,on=['ANO','DS','SEXO','IDADE'],suffixes=('_R','_ref'))
print('05: comparadas',len(m),'| células diferentes:',(m.FREQ_R!=m.FREQ_ref).sum())
if len(sys.argv)>1: print('2027 teste: total',pop[pop.ANO==2027].FREQ.sum(),'| negativos',(pop.FREQ<0).sum())
