import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd
D='/home/claude/data/'; V=D+'v4/'; REPO='/home/claude/protocolo-metodologico-populacao-salvador-ds-raca/'
pop=pd.read_pickle(V+'pop_ds.pkl'); PB=pd.read_pickle(V+'pop_full.pkl'); PI=pd.read_pickle(V+'pop_idade.pkl'); R=pd.read_pickle(V+'pop_bairro_idade.pkl')
SES=pd.read_pickle(V+'sesab.pkl'); R3=np.load(V+'R3_2010.npy'); DS00=np.load(V+'DS00.npy'); R00i=np.load(V+'R00i.npy')
tot=pd.read_csv(D+'totais.csv',index_col=0).iloc[:,0]
res=[]
def ok(nome,cond,obs=''): res.append((nome,'OK' if cond else 'FALHOU',obs))
g=pop.groupby('ANO').FREQ.sum(); ok('Total de cada ano = total oficial (Censo/TCU/RIPSA/IBGE)',(g.values==tot.values).all())
for nm,df in [('POP_BAIRRO',PB),('DS×idade',PI),('bairro×idade×raça',R)]:
    ok(f'{nm}: total de cada ano = POP_DS',(df.groupby('ANO').FREQ.sum().values==g.values).all())
a=pop[pop.ANO==2000]
ok('2000: total por DS = tabela DS 2000 (mesmos limites)',(a.groupby('DS').FREQ.sum().values==DS00).all())
ok('2000: sexo × faixa etária = Censo 2000 (SESAB)',(a.groupby(['SEXO','FXET']).FREQ.sum().values==SES[2000][0].ravel()).all())
ok('2000: raça = SIDRA 136 (sem declaração redistribuída)',(a.groupby('RACA').FREQ.sum().values==R00i).all(),str(R00i.tolist()))
p=PI[PI.ANO==2000].groupby(['SEXO','IDADE']).FREQ.sum().unstack().values
ok('2000: idades simples 0–19 por sexo = Censo 2000',(p[:,:20]==SES[2000][1]).all())
a=pop[pop.ANO==2010]
R10=np.stack([R3[:,np.r_[[0],[1]*4,[2+(x-5)//5 for x in range(5,80)],[17]*21]==f].sum(1) for f in range(18)],1)
ok('2010: sexo × faixa × raça = universo SIDRA 3175',(a.groupby(['SEXO','FXET','RACA']).FREQ.sum().values==R10.ravel()).all())
p=PI[PI.ANO==2010].groupby(['SEXO','IDADE']).FREQ.sum().unstack().values
ok('2010: idade simples 0–100+ por sexo = SIDRA 3175',(p==R3.sum(2)).all())
s10=pd.read_csv(D+'sesab2010.csv').sort_values(['DS','SEXO','FXET']).POP.values
d=np.abs(a.groupby(['DS','SEXO','FXET']).FREQ.sum().values-s10); ok('2010: DS × sexo × faixa = tabela SESAB por DS (±1 pessoa)',d.max()<=1,f'máx {d.max()}, células ajustadas {int((d>0).sum())}')
a=pop[pop.ANO==2022]
ok('2022: sexo × faixa etária = Censo 2022',(a.groupby(['SEXO','FXET']).FREQ.sum().values==SES[2022][0].ravel()).all())
p=PI[PI.ANO==2022].groupby(['SEXO','IDADE']).FREQ.sum().unstack().values
ok('2022: idades simples 0–19 por sexo = Censo 2022',(p[:,:20]==SES[2022][1]).all())
b=pd.read_csv(D+'bairros_final_v3.csv').set_index('COD_BAIRRO').pop22
dd=(PB[PB.ANO==2022].groupby('COD_BAIRRO').FREQ.sum()-b).abs(); ok('2022: população dos bairros = IBGE (arredondamento)',dd.max()<=20,f'máx ±{int(dd.max())}')
c1=R.groupby(['ANO','DS','COD_BAIRRO','FXET','SEXO','RACA']).FREQ.sum().reset_index().merge(PB[PB.FREQ>0],on=['ANO','DS','COD_BAIRRO','FXET','SEXO','RACA'],how='outer').fillna(0)
ok('Detalhada (idade) agregada = POP_BAIRRO em todas as células',(c1.FREQ_x==c1.FREQ_y).all())
c2=R.groupby(['ANO','DS','SEXO','IDADE']).FREQ.sum().reset_index().merge(PI[PI.FREQ>0],on=['ANO','DS','SEXO','IDADE'],how='outer').fillna(0)
ok('Detalhada agregada = DS × sexo × idade em todas as células',(c2.FREQ_x==c2.FREQ_y).all())
ok('Sem valores negativos',(PB.FREQ>=0).all() and (PI.FREQ>=0).all() and (R.FREQ>=0).all())
bd=pd.read_csv(REPO+'dados/dicionarios/bairros.csv'); ok('Dicionário com 171 bairros (1–171)',sorted(bd.COD_BAIRRO)==list(range(1,172)))
cods=set(PB.COD_BAIRRO.unique()); ok('Bairros com população na base',len(cods)==170 and 2 not in cods,f'{len(cods)} com população; sem população: {sorted(set(range(1,172))-cods)}')
for r_ in res: print('%-70s %-7s %s'%r_)
pd.DataFrame(res,columns=['CONFERENCIA','RESULTADO','OBS']).to_csv(V+'validacao_v4.csv',index=False)
# reconciliação com SESAB (análise)
rows=[]
for ano in range(2000,2026):
    F=SES[ano][0]; B=pop[pop.ANO==ano].groupby(['SEXO','FXET']).FREQ.sum().values.reshape(2,18)
    rows.append({'ANO':ano,'TOTAL_SESAB':int(F.sum()),'TOTAL_BASE':int(B.sum()),'DIF':int(B.sum()-F.sum()),'DISSIMILARIDADE_%':round(50*np.abs(F/F.sum()-B/B.sum()).sum(),2)})
rc=pd.DataFrame(rows); rc.to_csv(V+'reconciliacao_sesab.csv',index=False); print(rc.to_string(index=False))
