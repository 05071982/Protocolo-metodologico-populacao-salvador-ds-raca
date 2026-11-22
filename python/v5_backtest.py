import numpy as np, pandas as pd
V='/home/claude/data/v5/'; pop=pd.read_pickle(V+'pop_ds.pkl'); PB=pd.read_pickle(V+'pop_full.pkl')
DS00=np.load('/home/claude/data/v4/DS00.npy').astype(float)
d10=pop[pop.ANO==2010].groupby('DS').FREQ.sum().values.astype(float); d22=pop[pop.ANO==2022].groupby('DS').FREQ.sum().values.astype(float)
T22=d22.sum()
lag=d10+(d10-DS00)*12/10
fix=d10/d10.sum()*T22
lagc=lag/lag.sum()*T22
s00,s10=DS00/DS00.sum(),d10/d10.sum(); w=22/10; sv=np.exp((1-w)*np.log(s00)+w*np.log(s10)); var=sv/sv.sum()*T22
nm=pd.read_csv('/home/claude/protocolo-metodologico-populacao-salvador-ds-raca/dados/dicionarios/ds.csv').NOME_DS.values
b=pd.DataFrame({'DS':nm,'pop2000':DS00.astype(int),'pop2010':d10.astype(int),'obs2022':d22.astype(int),'lagrange_lin':lag.round(),'razao_fixa':fix.round(),'lagrange_lin_calibrado':lagc.round(),'razao_variavel':var.round()})
b.to_csv('/home/claude/protocolo-metodologico-populacao-salvador-ds-raca/resultados/backtest_metodos_ds_2022.csv',index=False)
for c in ['lagrange_lin','razao_fixa','lagrange_lin_calibrado','razao_variavel']:
    e=(b[c]/b.obs2022-1)*100; print(c,'EPAM',round(e.abs().mean(),1),'max',round(e.abs().max(),1),'total %',round((b[c].sum()/T22-1)*100,1))
# negativos: Lagrange linear nas células DS×sexo×faixa×raça até 2026 (a partir de 2010 e 2022)
C10=np.load(V+'C10.npy').astype(float); C22=np.load(V+'C22.npy').astype(float)
L26=C22+(C22-C10)*4/12; print('Lagrange células DS negativas em 2026:',int((L26<0).sum()),'de',L26.size)
U10=np.load(V+'C10_u.npy').astype(float); U22=np.load(V+'C22_u.npy').astype(float); LU=U22+(U22-U10)*4/12; print('Lagrange células bairro×DS negativas em 2026:',int((LU<0).sum()),'de',LU.size)
# bairros: participação de 2010 mantida fixa até 2022 × observado
bb=PB[PB.ANO.isin([2010,2022])].groupby(['ANO','COD_BAIRRO']).FREQ.sum().unstack(0); bb=bb[bb[2022]>=1000]
fixb=bb[2010]/bb[2010].sum()*bb[2022].sum(); e=(fixb/bb[2022]-1)*100
print('Bairros (pop22>=1000, n=%d): razão fixa 2010 → 2022 EPAM %.1f%%, mediana %.1f%%, p90 %.1f%%'%(len(bb),e.abs().mean(),e.abs().median(),e.abs().quantile(.9)))
g=(bb[2022]/bb[2010]-1)*100; print('variação 2010→2022 por bairro: p10 %.1f%%  mediana %.1f%%  p90 %.1f%%'%(g.quantile(.1),g.median(),g.quantile(.9)))
print('Aquarius 2010/2022:',PB[(PB.COD_BAIRRO==171)&PB.ANO.isin([2010,2022])].groupby('ANO').FREQ.sum().to_dict())
print(pd.DataFrame({'2010':bb[2010],'2022':bb[2022],'var%':g.round(1)}).sort_values('var%').iloc[[0,1,2,-3,-2,-1]])
