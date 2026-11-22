import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, os, zipfile, shutil
D='/home/claude/data/'; V=D+'v5/'; REPO='/home/claude/protocolo-metodologico-populacao-salvador-ds-raca/'; OUT='/home/claude/out/v5/'
shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT+'por_ano')
bd=pd.read_csv(REPO+'dados/dicionarios/bairros.csv'); dsd=pd.read_csv(REPO+'dados/dicionarios/ds.csv')
DSN=dict(zip(dsd.DS,dsd.NOME_DS)); BN=dict(zip(bd.COD_BAIRRO,bd.BAIRRO))
PB=pd.read_pickle(V+'pop_full.pkl'); PI=pd.read_pickle(V+'pop_idade.pkl'); R=pd.read_pickle(V+'pop_bairro_idade.pkl'); pop=pd.read_pickle(V+'pop_ds.pkl')
zero=bd[~bd.COD_BAIRRO.isin(PB.COD_BAIRRO.unique())]
print('bairros sem população:',zero.COD_BAIRRO.tolist())
# grade zerada na tabela principal (ANO×sexo×faixa×raça) para cada bairro sem população
g=[]
for _,z in zero.iterrows():
    a,s,f,r=np.meshgrid(range(2000,2027),[1,2],range(1,19),range(1,6),indexing='ij')
    g.append(pd.DataFrame({'ANO':a.ravel(),'DS':z.DS_PRINCIPAL,'COD_BAIRRO':z.COD_BAIRRO,'FXET':f.ravel(),'SEXO':s.ravel(),'RACA':r.ravel(),'FREQ':0}))
PBz=pd.concat([PB]+g,ignore_index=True).sort_values(['ANO','DS','COD_BAIRRO','SEXO','FXET','RACA']).reset_index(drop=True)
PBz.to_pickle(V+'pop_full_z.pkl')
assert sorted(PBz.COD_BAIRRO.unique())==list(range(1,172))
# ---- repositório: CSV comprimidos
PBz[['ANO','DS','COD_BAIRRO','FXET','SEXO','RACA','FREQ']].to_csv(REPO+'resultados/populacao_salvador_bairro_ds_2000_2026.csv.gz',index=False,compression='gzip')
PI[['ANO','DS','SEXO','IDADE','FXET','FREQ']].to_csv(REPO+'resultados/populacao_salvador_ds_sexo_idade_2000_2026.csv.gz',index=False,compression='gzip')
Rz=pd.concat([R,pd.DataFrame([{'ANO':a,'DS':z.DS_PRINCIPAL,'COD_BAIRRO':z.COD_BAIRRO,'IDADE':0,'FXET':1,'SEXO':1,'RACA':1,'FREQ':0} for a in range(2000,2027) for _,z in zero.iterrows()])],ignore_index=True)
Rz=Rz.sort_values(['ANO','DS','COD_BAIRRO','IDADE','SEXO','RACA']).reset_index(drop=True)
Rz.to_csv(REPO+'resultados/populacao_salvador_bairro_ds_idade_raca_2000_2026.csv.gz',index=False,compression='gzip')
shutil.copy(V+'validacao_v5.csv',REPO+'resultados/validacao_v5.csv'); shutil.copy(V+'reconciliacao_sesab.csv',REPO+'resultados/reconciliacao_sesab_2000_2025.csv')
# ---- arquivos por ano (idade detalhada, com nomes)
Rz['NOME_DS']=Rz.DS.map(DSN); Rz['NOME_BAIRRO']=Rz.COD_BAIRRO.map(BN)
cols=['ANO','DS','NOME_DS','COD_BAIRRO','NOME_BAIRRO','IDADE','FXET','SEXO','RACA','FREQ']
assert Rz.NOME_BAIRRO.notna().all()
for a,d in Rz.groupby('ANO'):
    d[cols].to_csv(OUT+f'por_ano/pop_bairro_idade_raca_{a}.csv',sep=';',index=False,encoding='utf-8-sig')
bd.to_csv(OUT+'por_ano/dicionario_bairros.csv',sep=';',index=False,encoding='utf-8-sig')
pd.read_csv(V+'validacao_v5.csv').to_csv(OUT+'por_ano/VALIDACAO_v5.csv',sep=';',index=False,encoding='utf-8-sig')
pd.read_csv(V+'reconciliacao_sesab.csv').to_csv(OUT+'por_ano/RECONCILIACAO_SESAB_2000_2025.csv',sep=';',index=False,encoding='utf-8-sig')
FXN=['Menor de 1 ano','1 a 4 anos','5 a 9 anos','10 a 14 anos','15 a 19 anos','20 a 24 anos','25 a 29 anos','30 a 34 anos','35 a 39 anos','40 a 44 anos','45 a 49 anos','50 a 54 anos','55 a 59 anos','60 a 64 anos','65 a 69 anos','70 a 74 anos','75 a 79 anos','80 anos e mais']
FX=np.array([1]+[2]*4+[3+(a-5)//5 for a in range(5,80)]+[18]*21)
lei=['Dicionário de códigos — população de Salvador por DS, bairro, idade, sexo e raça/cor, 2000–2026 (versão 5)',
 'Arquivos pop_bairro_idade_raca_AAAA.csv: colunas ANO; DS; NOME_DS; COD_BAIRRO; NOME_BAIRRO; IDADE; FXET; SEXO; RACA; FREQ (separador ";", UTF-8). Um arquivo por ano porque a série completa passa do limite de linhas do Excel.',
 'Bairros: 171 oficiais. O código 2 (Aeroporto) não tem população residente; aparece com UMA linha por ano com FREQ = 0 (DS 8 Itapuã, IDADE 0, SEXO 1, RACA 1), apenas para constar. Bairros que cruzam limites de DS aparecem em mais de um DS (ver DS_TODOS).',
 'Código 171 (Aquarius): criado pela Lei 9.778/2024, desmembrado da Pituba; aparece em toda a série com o limite atual.',
 'Os arquivos trazem apenas linhas com FREQ > 0, exceto a linha do Aeroporto. Somando por ANO × DS × COD_BAIRRO × FXET × SEXO × RACA obtém-se exatamente a base principal (ANO | DS | COD_BAIRRO | FXET | SEXO | RACA | FREQ).',
 'Totais anuais: Censo (2000, 2010, 2022); TCU/IBGE nos demais anos (2023 = RIPSA; 2025 e 2026 = IBGE Cidades).',
 'Versão 5 — 2010 e 2022 construídos setor a setor (setores censitários nos limites atuais de bairro e DS) e calibrados ao IBGE: 2000 (sexo × faixa e idades 0–19 = Censo 2000; raça = SIDRA 136; totais por DS = tabela DS 2000), 2010 (bairros = soma dos setores; sexo × idade × raça = universo SIDRA 3175) e 2022 (bairros = IBGE; sexo × faixa e idades 0–19 = Censo 2022). Cada bairro tem tendência própria entre os censos.',
 'VALIDACAO_v5.csv: todas as conferências. RECONCILIACAO_SESAB_2000_2025.csv: comparação ano a ano com o TabNet SESAB (análise; a SESAB não foi usada como total fora dos anos de censo).',
 'Documentação: https://github.com/05071982/Protocolo-metodologico-populacao-salvador-ds-raca/wiki  ·  DOI 10.5281/zenodo.24096844']
with pd.ExcelWriter(OUT+'por_ano/DICIONARIO.xlsx') as w:
    pd.DataFrame({lei[0]:lei[1:]}).to_excel(w,'LEIAME',index=False)
    bd.to_excel(w,'BAIRRO',index=False); dsd.to_excel(w,'DS',index=False)
    pd.DataFrame({'FXET':range(1,19),'FAIXA':FXN}).to_excel(w,'FXET',index=False)
    pd.DataFrame({'IDADE':range(101),'DESCRICAO':['Menos de 1 ano']+[f'{a} ano' if a==1 else f'{a} anos' for a in range(1,100)]+['100 anos ou mais'],'FXET':FX}).to_excel(w,'IDADE',index=False)
    pd.DataFrame({'SEXO':[1,2],'DESCRICAO':['Masculino','Feminino']}).to_excel(w,'SEXO',index=False)
    pd.read_csv(REPO+'dados/dicionarios/raca.csv').to_excel(w,'RACA',index=False)
zp=OUT+'populacao_bairro_idade_raca_por_ano_v5.zip'
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir(OUT+'por_ano')): z.write(OUT+'por_ano/'+f,f)
# ---- conferência do zip relendo os arquivos
tot=pd.read_csv(D+'totais.csv',index_col=0).iloc[:,0]; n=0
with zipfile.ZipFile(zp) as z:
    names=z.namelist(); print(len(names),'arquivos no zip')
    for a in range(2000,2027):
        d=pd.read_csv(z.open(f'pop_bairro_idade_raca_{a}.csv'),sep=';',encoding='utf-8-sig'); n+=len(d)
        assert d.FREQ.sum()==tot[a] and sorted(d.COD_BAIRRO.unique())==list(range(1,172)) and not d.duplicated(['DS','COD_BAIRRO','IDADE','SEXO','RACA']).any()
        assert (d.NOME_BAIRRO==d.COD_BAIRRO.map(BN)).all() and (d[d.COD_BAIRRO==2].FREQ==0).all() and len(d[d.COD_BAIRRO==2])==1
        k=d.groupby(['DS','COD_BAIRRO','FXET','SEXO','RACA']).FREQ.sum(); p=PB[(PB.ANO==a)&(PB.FREQ>0)].set_index(['DS','COD_BAIRRO','FXET','SEXO','RACA']).FREQ
        assert k[k>0].sort_index().equals(p.sort_index())
    dic=pd.read_excel(z.open('DICIONARIO.xlsx'),'BAIRRO'); assert sorted(dic.COD_BAIRRO)==list(range(1,172))
print('zip conferido: 27 anos, linhas',n,'| 171 bairros em todo ano | totais oficiais | igual à base principal')
print(os.path.getsize(zp)/1e6,'MB')
