import pandas as pd, numpy as np, io
def load(f,sx):
    L=open(f,encoding='latin1').read().splitlines()
    i=[k for k,l in enumerate(L) if l.startswith('"Faixa')][0]
    rows=[l for l in L[i:] if l.startswith('"')]
    d=pd.read_csv(io.StringIO("\n".join(rows)),sep=';')
    d=d.rename(columns={d.columns[0]:'faixa'}).set_index('faixa')
    d=d.drop('Total').melt(ignore_index=False,var_name='ANO',value_name='SESAB').reset_index()
    d['ANO']=d.ANO.astype(int); d['SEXO']=sx; return d
s=pd.concat([load('/home/claude/data/sesab/masc.csv',1),load('/home/claude/data/sesab/fem.csv',2)])
def fx(f):
    if f.startswith('Menor'): return 1
    if f.startswith('80'): return 18
    a=int(f.split()[0])
    if a<5: return 2
    if a<20: return 3+(a-5)//5
    return 6+(a-20)//5
s['FXET']=s.faixa.map(fx)
s=s.groupby(['ANO','SEXO','FXET']).SESAB.sum().reset_index()
b=pd.read_csv('/home/claude/protocolo-metodologico-populacao-salvador-ds-raca/resultados/populacao_salvador_bairro_ds_2000_2026.csv.gz',sep=None,engine='python')
b=b.groupby(['ANO','SEXO','FXET']).FREQ.sum().reset_index().rename(columns={'FREQ':'BASE'})
m=s.merge(b,on=['ANO','SEXO','FXET'])
m['DIF']=m.BASE-m.SESAB; m['DIF%']=m.DIF/m.SESAB*100
m.to_csv('/home/claude/data/sesab/comparacao.csv',index=False)
t=m.groupby('ANO')[['SESAB','BASE']].sum(); t['dif%']=(t.BASE/t.SESAB-1)*100
print(t.round(2).to_string())
# medida de estrutura: índice de dissimilaridade (% pop que precisaria mudar de célula)
def dis(g): return 0.5*np.abs(g.SESAB/g.SESAB.sum()-g.BASE/g.BASE.sum()).sum()*100
print('Dissimilaridade estrutura sexo×FXET (%)');print(m.groupby('ANO').apply(dis,include_groups=False).round(2).to_string())
sx=m.groupby(['ANO','SEXO'])[['SESAB','BASE']].sum().unstack()
print('Razão de sexo (H/100M)');print(pd.DataFrame({'SESAB':sx['SESAB'][1]/sx['SESAB'][2]*100,'BASE':sx['BASE'][1]/sx['BASE'][2]*100}).round(1).loc[2000:2012].to_string())
