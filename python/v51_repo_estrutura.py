import numpy as np, pandas as pd, os, glob
D='/home/claude/data/'; V=D+'v51/'; R='/home/claude/protocolo-metodologico-populacao-salvador-ds-raca/dados/estrutura/'
for f in ['estrutura_2000_ds.csv','estrutura_2010_ds.csv','estrutura_2022_ds.csv','estrutura_2022_bairro_ds.csv']:
    if os.path.exists(R+f): os.remove(R+f)
un=pd.read_csv('/home/claude/data/v51/units.csv')
for ano,f in [(2000,'C00_u'),(2010,'C10_u'),(2022,'C22_u')]:
    C=np.load(V+f+'.npy'); u,s,a,r=np.indices(C.shape)
    pd.DataFrame({'UNIDADE':u.ravel()+1,'DS':un.DS.values[u.ravel()],'COD_BAIRRO':un.COD_BAIRRO.values[u.ravel()],'SEXO':s.ravel()+1,'FXET':a.ravel()+1,'RACA':r.ravel()+1,'POP':C.ravel()}).to_csv(R+f'estrutura_{ano}_unidade.csv',index=False)
FX=np.array([1]+[2]*4+[3+(a-5)//5 for a in range(5,80)]+[18]*21)
P={k:np.load(V+k+'.npy') for k in ['P00','P10','P22']}; d,s,i=np.indices(P['P10'].shape)
pd.DataFrame({'DS':d.ravel()+1,'SEXO':s.ravel()+1,'IDADE':i.ravel(),'FXET':FX[i.ravel()],'P2000':P['P00'].ravel(),'P2010':P['P10'].ravel(),'P2022':P['P22'].ravel()}).to_csv(R+'proporcao_idade_simples_na_faixa.csv',index=False)
rows=[]
for ano,k in [(2000,'I00'),(2010,'I10'),(2022,'I22')]:
    I=np.load(V+k+'.npy'); d,s,i=np.indices(I.shape)
    rows.append(pd.DataFrame({'ANO':ano,'DS':d.ravel()+1,'SEXO':s.ravel()+1,'IDADE':i.ravel(),'FREQ':I.ravel()}))
pd.concat(rows).to_csv(R+'idade_simples_censos_ds.csv',index=False)
print(sorted(os.listdir(R)))
