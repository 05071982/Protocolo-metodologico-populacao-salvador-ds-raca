import json,re,numpy as np,pandas as pd
s=json.load(open('/home/claude/data/interp2016.json'))['fileContent']
def tab(key):
    i=s.find(key); seg=s[i:i+4000]
    out={}
    for ds in range(1,13):
        m=re.search(r'\b%d ?- ?[^,]*,((?:"[\d,]+"|\d+)(?:,(?:"[\d,]+"|\d+)){18})'%ds, seg)
        vals=[int(v.replace(',','').strip('"')) for v in re.findall(r'"[\d,]+"|\d+', m.group(1))]
        out[ds]=vals
    return out
F=tab('sexo feminino nos Distritos Sanitarios de Salvador, 2010'); M=tab('sexo masculino nos Distritos Sanitarios de Salvador, 2010')
rows=[]
for ds in range(1,13):
    for sx,T in ((1,M),(2,F)):
        v=T[ds]; assert sum(v[1:])==v[0],(ds,sx,sum(v[1:]),v[0])
        for a in range(18): rows.append((ds,sx,a+1,v[a+1]))
d=pd.DataFrame(rows,columns=['DS','SEXO','FXET','POP']); print(d.POP.sum()); d.to_csv('/home/claude/data/sesab2010.csv',index=False)
