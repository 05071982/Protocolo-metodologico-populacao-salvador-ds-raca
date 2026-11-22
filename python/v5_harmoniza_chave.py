# harmoniza a chave 2010 com a de 2022: setores com o mesmo código usam a unidade da chave 2022
# quando ela é uma das unidades que o polígono de 2010 de fato intersecta (>= 25% da área)
import pandas as pd, numpy as np
V='/home/claude/data/v5/'
sec=pd.read_pickle(V+'chave2010.pkl')
if 'u_poly' not in sec: sec['u_poly']=sec['u22']
k=pd.read_csv('/home/claude/data/c2010/chave2010_codificada.csv',dtype={'CD_SETOR':str}); k['u']=list(zip(k.DS,k.COD_BAIRRO.astype(int)))
cand=k.groupby('CD_SETOR').apply(lambda g: dict(zip(g.u,g.prop_area)),include_groups=False).to_dict()
c=pd.read_csv('/home/claude/data/chave_v3.csv',dtype=str); c=c[c.COD_BAIRRO.notna()]
c22=dict(zip(c.CD_SETOR,zip(c.DS.astype(int),c.COD_BAIRRO.astype(float).astype(int))))
un=pd.read_csv('/home/claude/data/units.csv'); U=set(zip(un.DS,un.COD_BAIRRO))
new=[];why=[]
for s,up in zip(sec.CD_SETOR,sec.u_poly):
    u2=c22.get(s); cd=cand.get(s,{})
    if u2 is not None and u2 in U and cd.get(u2,0)>=0.25: new.append(u2); why.append('codigo_2022')
    else: new.append(up if isinstance(up,tuple) else (11,120)); why.append('poligono' if isinstance(up,tuple) else 'sem_intersecao')
sec['u22']=new; sec['origem_chave']=why
print(sec.origem_chave.value_counts().to_dict()); print('setores que mudaram de unidade:',(sec.u22!=sec.u_poly).sum(),' pop',sec[sec.u22!=sec.u_poly]['pop'].sum())
sec.to_pickle(V+'chave2010.pkl')
