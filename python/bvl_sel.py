import pickle, numpy as np, pandas as pd
d,lei=pickle.load(open('/home/claude/data/bvl/d.pkl','rb'))
def r(tipo,nome,titulo=None):
    m=(d.TIPO==tipo)&(d.NOME==nome)
    m&= d.TITULO.isna() if titulo is None else (d.TITULO==titulo)
    return m
M={ # lei -> lista de (TIPO,NOME,TITULO)
'1ª Travessa Itaquaraci':[('TRAVESSA','ITAQUARACI')],'2ª Travessa Itaquaraci':[('TRAVESSA','ITAQUARACI')],
'1ª Travessa João Rodrigues Mendes':[('1A TRAVESSA DA RUA','JOAO RODRIGUES MENDES')],
'1ª Travessa Paulo Geovane':[('TRAVESSA','1 PAULO GEOVANE')],'1ª Travessa Ramalho Santos':[('1A TRAVESSA DA RUA','RAMALHO SANTOS')],
'Avenida Afrânio Peixoto':[('AVENIDA','AFRANIO PEIXOTO')],'Avenida Pedro Veríssimo':[('AVENIDA','PEDRO VERISSIMO')],
'Rua Ana Piedade':[('RUA','ANA PIEDADE')],'Rua Aristóteles Boaventura':[],'Rua Boa Fé':[('RUA','BOA FE')],
'Rua Boa Ventura':[('RUA','BOA VENTURA')],'Rua Francisco José':[('TRAVESSA','FRANCISCO JOSE')],'Rua Itaquaraci':[('RUA','ITAQUARACI')],
'Rua Marciano Porcino':[('RUA','MARCIANO PORCINO')],'Rua Nilcélia Pontes':[('RUA','NICELIA PONTES')],'Rua Nova Direta':[('RUA','NOVA DIRETA')],
'Rua Nova do Meio':[('RUA','NOVA DO MEIO')],'Rua Paulo Geovane':[('RUA','PAULO GEOVANE')],'Rua Santo Antônio':[('RUA','ANTONIO','SANTO')],
'Rua São Barnabé':[('RUA','BARNABE','SAO')],'Rua São Cornélio':[('RUA','CORNELIO','SAO')],'Rua São Jorge da Boa Vista':[('RUA','JORGE DA BOA VISTA','SAO')],
'Rua São Luís':[('RUA','LUIS','SAO')],'Travessa Ana Piedade':[('1A TRAVESSA DA RUA','ANA PIEDADE'),('2A TRAVESSA DA RUA','ANA PIEDADE'),('3A TRAVESSA DA RUA','ANA PIEDADE')],
'Travessa Boa Fé':[('TRAVESSA','BOA FE')],'Travessa João Rodrigues Mendes':[('TRAVESSA','JOAO RODRIGUES MENDES')],
'Travessa Luciano Barreto':[('TRAVESSA','LUCIANO BARRETO')],'Travessa Oswaldo Martins de Castro':[('RUA','OSWALDO MARTINS DE CASTRO')],
'Travessa Paulo Geovane':[('TRAVESSA','PAULO GEOVANE')],'Travessa Sansué':[('TRAVESSA','SANSUE')],'Travessa Santo Antônio':[('TRAVESSA','ANTONIO','SANTO')],
'Travessa São José da Boa Vista':[('TRAVESSA','JOSE DA BOA VISTA','SAO')],'Travessa São Sebastião':[('TRAVESSA','SEBASTIAO','SAO')],
'Travessa Tranquilino Mendes':[('TRAVESSA','TRANQUILINO MENDES')]}
d['LEI']=''
for k,v in M.items():
    for t in v:
        m=r(*t); d.loc[m&(d.LEI==''),'LEI']=k
# metros
lat0=d.LAT.mean(); d['X']=(d.LON-d.LON.mean())*111320*np.cos(np.radians(lat0)); d['Y']=(d.LAT-lat0)*110540
core=['Rua Itaquaraci','Rua Marciano Porcino','Rua Nilcélia Pontes','Rua Nova Direta','Rua Nova do Meio','Rua Paulo Geovane','Rua São Barnabé','Rua São Cornélio','Rua São Jorge da Boa Vista','Rua Boa Ventura','Travessa Sansué','Travessa Oswaldo Martins de Castro','Travessa Luciano Barreto','Travessa Tranquilino Mendes','Travessa João Rodrigues Mendes']
c=d[d.LEI.isin(core)]; cx=np.average(c.X,weights=c.N_END); cy=np.average(c.Y,weights=c.N_END)
d['DIST']=np.hypot(d.X-cx,d.Y-cy)
pickle.dump((d,M,core,cx,cy),open('/home/claude/data/bvl/sel.pkl','wb'))
