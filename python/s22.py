import json,csv,io,pandas as pd,numpy as np
D='/home/claude/data/'
fr=[]
for ds in range(1,13):
    s=json.load(open(f'{D}s22/ds{ds}.json'))['fileContent'].replace('\\_','_')
    rows=list(csv.reader(io.StringIO(s)))
    h=[x.strip() for x in rows[0]]
    df=pd.DataFrame([[c.strip() for c in r] for r in rows[1:] if len(r)==len(h)],columns=h)
    df['DS']=ds; fr.append(df)
a=pd.concat(fr,ignore_index=True); a=a.drop(columns=[''])
print(a.shape, a.CD_setor.nunique())
k=a.groupby('CD_setor').DS.nunique(); print('setores em k DS:',k.value_counts().to_dict())
a['k']=a.CD_setor.map(k)
a.to_pickle(D+'s22_raw.pkl')
num=lambda c: pd.to_numeric(a[c].replace('X',np.nan),errors='coerce')
u=a.drop_duplicates('CD_setor')
print('pop setores unicos:',pd.to_numeric(u.populacao).sum())
print('X share in m_0a4:', (a.m_0a4=='X').mean(), ' in pardo:',(a.pardo=='X').mean(), 'indigena', (a.indigena=='X').mean())
