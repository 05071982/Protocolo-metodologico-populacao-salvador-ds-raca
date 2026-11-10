import json,csv,io,pandas as pd,numpy as np
D='/home/claude/data/'
sec=pd.read_csv(D+'setor_bairro_ds_2022.csv',dtype={'CD_setor':str})  # actually bairro polygons
s=json.load(open(D+'bairros2022.json'))['fileContent'].replace('\\_','_')
rows=list(csv.reader(io.StringIO(s)))
b=pd.DataFrame([[r[1].strip(),int(r[2]),int(r[3]),int(r[-1])] for r in rows[1:] if len(r)>5],columns=['bairro','pop22','dom22','nset'])
m=b.merge(sec[['bairro','DS','area']],on='bairro',how='outer',indicator=True)
print(m._merge.value_counts()); print(m[m._merge!='both'])
print(m[m.bairro.duplicated(keep=False)])
b=m[m._merge=='both'].copy(); b.to_csv(D+'bairro_ds_2022.csv',index=False)
a=pd.read_pickle(D+'s22_raw.pkl'); a['pop']=pd.to_numeric(a.populacao); a['w']=1/a.k
t=pd.DataFrame({'bairros':b.groupby('DS').pop22.sum(),'setores_w':(a['pop']*a.w).groupby(a.DS).sum().round(),'setores_brutos':a.groupby('DS')['pop'].sum(),'setores_unicos':a[a.k==1].groupby('DS')['pop'].sum()})
t.loc['Tot']=t.sum(); print(t.astype(int))
