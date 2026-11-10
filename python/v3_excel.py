import warnings; warnings.filterwarnings('ignore')
import pandas as pd,numpy as np
from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Font,PatternFill,Alignment
D='/home/claude/data/'
pop=pd.read_pickle(D+'pop_ds.pkl'); pb=pd.read_pickle(D+'pop_full.pkl'); b=pd.read_csv(D+'bairros_final_v3.csv').sort_values('COD_BAIRRO')
tot=pd.read_csv(D+'totais.csv',index_col=0).iloc[:,0]
pc=pd.read_pickle(D+'pop_ds_censo.pkl'); pop=pop.merge(pc.rename(columns={'FREQ':'FREQ_CENSO'}),on=['ANO','FXET','DS','SEXO','RACA'])
DSN={1:'Centro Histórico',2:'Itapagipe',3:'São Caetano/Valéria',4:'Liberdade',5:'Brotas',6:'Barra/Rio Vermelho',7:'Boca do Rio',8:'Itapuã',9:'Cabula/Beiru',10:'Pau da Lima',11:'Subúrbio Ferroviário',12:'Cajazeiras'}
FX=['Menor de 1 ano','1 a 4 anos','5 a 9 anos','10 a 14 anos','15 a 19 anos','20 a 24 anos','25 a 29 anos','30 a 34 anos','35 a 39 anos','40 a 44 anos','45 a 49 anos','50 a 54 anos','55 a 59 anos','60 a 64 anos','65 a 69 anos','70 a 74 anos','75 a 79 anos','80 anos e mais']
RC=['Branca','Preta','Amarela','Parda','Indígena']
Q={**{t:'Estimativa TCU' for t in range(2000,2027)},2000:'Censo 2000',2010:'Censo 2010',2022:'Censo 2022',2023:'Estimativa RIPSA',2025:'Estimativa IBGE Cidades',2026:'Estimativa IBGE Cidades'}
F='Arial'; H=Font(name=F,bold=True,color='FFFFFF'); HF=PatternFill('solid',fgColor='1F4E78'); N=Font(name=F); T=Font(name=F,bold=True,size=13); B=Font(name=F,bold=True)
wb=Workbook(write_only=True)
def hdr(ws,vals): ws.append([WriteOnlyCell(ws,value=v) for v in vals]); [setattr(c,'font',H) or setattr(c,'fill',HF) for c in []]
def row(ws,vals,font=N,fill=None,fmt=None):
    cs=[]
    for v in vals:
        c=WriteOnlyCell(ws,value=v); c.font=font
        if fill: c.fill=fill
        if fmt and isinstance(v,(int,float)) or (fmt and isinstance(v,str) and v.startswith('=')): c.number_format=fmt
        cs.append(c)
    ws.append(cs)
def H_(ws,vals): row(ws,vals,H,HF)
# ---------- LEIAME
ws=wb.create_sheet('LEIAME'); ws.column_dimensions['A'].width=120
L=[('T','População de Salvador por Distrito Sanitário, bairro, sexo, faixa etária e raça/cor — 2000 a 2026 (versão 3)'),
('','Elaboração: Sala de Situação em Saúde de Salvador (SDSS/SMS). Totais municipais: Censo (2000, 2010, 2022) e estimativas TCU/IBGE nos demais anos (2023: RIPSA). Estrutura interna: Censos 2010 e 2022 (IBGE) e tabela SESAB/SUVISA/DIS 2010 por DS.'),
('',''),('B','Abas'),
('','POP_BAIRRO — tabela completa (ANO, DS, COD_BAIRRO, FXET, SEXO, RACA, FREQ), 942.840 linhas, 171 bairros (inclui Aquarius, cód. 171). Cada linha é a parte de um bairro dentro de um DS (bairros que cruzam limites de DS aparecem em mais de um DS). Somando por DS obtém-se exatamente POP_DS; somando por bairro obtém-se o bairro inteiro. Use no BI socioambiental.'),
('','POP_DS — mesma série agregada por DS no formato do pop14 (ANO, FXET, DS, SEXO, RACA, FREQ, FREQ_CENSO), 58.320 linhas. FREQ = total TCU; FREQ_CENSO = série alternativa com totais apenas censitários (para análise de tendência). Use FREQ no TabNet.'),
('','SETORES — chave dos 4.542 setores censitários 2022: bairro, DS, proporção de área e população recenseada do setor (referência).'),
('','TOTAIS — população por ano e DS calculada por fórmulas (SUMIFS) sobre POP_DS.'),
('','CHECAGENS — conferências de consistência (fórmulas).'),
('','DICIONARIO — códigos de FXET, DS, SEXO, RACA, BAIRRO e tipo de estimativa por ano.'),
('','METODOLOGIA e LIMITACOES — descrição completa do método.'),
('',''),('B','Leitura rápida'),
('','• 2010 e 2022 são anos censitários (valores observados, com ajustes descritos na metodologia).'),
('','• Anos não censitários: total municipal = estimativa TCU/IBGE (a mesma do IBGE Cidades; 2023 = RIPSA). A distribuição interna vem da interpolação das razões entre 2010 e 2022.'),
('','• Atenção: os totais TCU têm quebras metodológicas (2009→2010, 2021→2022, 2022→2023) que não são variação real da população. Para tendência use FREQ_CENSO.'),
('','• Aquarius (Lei 9.778/2024) aparece em toda a série com o limite atual, a partir de 7 setores 2022 antes atribuídos à Pituba.'),
('','• Raça/cor segue os códigos IBGE/SIM/SINASC: 1 Branca, 2 Preta, 3 Amarela, 4 Parda, 5 Indígena. "Negra" = Preta + Parda (2+4).'),
('','• Valores inteiros obtidos por arredondamento controlado (maior resto): os totais anuais fecham exatamente; células muito pequenas (ex.: indígena por bairro) são estimativas, não contagens.')]
for k,v in L: row(ws,[v],T if k=='T' else B if k=='B' else N)
# ---------- METODOLOGIA
ws=wb.create_sheet('METODOLOGIA'); ws.column_dimensions['A'].width=6; ws.column_dimensions['B'].width=130
M=[('1','Unidade e células'),('','A população é estimada em 2.160 células por ano: 12 DS × 2 sexos × 18 faixas etárias (as mesmas do pop14) × 5 categorias de raça/cor. Cada ano soma o total municipal desse ano.'),
('2','Base 2010 (Censo 2010)'),('','Sexo × faixa etária por DS: tabela oficial SESAB/SUVISA/DIS 2010 (arquivo POPULAÇÃO_INTERPOLAÇÃO_COM_BASE_CENSO_2010), total 2.675.656 = Censo 2010. O banco 2010 por DS reconstruído em 2026 soma só 2.082.781 (≈78% de cobertura, perda de setores no cruzamento); por isso foi usado apenas para a PROPORÇÃO de raça/cor de cada DS.'),
('','Raça 2010: ajuste proporcional iterativo (IPF/raking) com duas margens — sexo×faixa (SESAB) e distribuição de raça do DS (banco 2010) — partindo da estrutura sexo×idade×raça do próprio DS em 2022 como semente (preserva as interações idade×raça observadas em 2022).'),
('3','Base 2022 (Censo 2022, agregados por setor)'),
('','a) Os 12 arquivos por DS originais (st_intersection) duplicavam 386 setores de fronteira. Na versão 2 cada setor tem um único DS e um bairro pela chave do item 5.'),
('','b) Sigilo IBGE ("X"): cada célula suprimida recebeu o resíduo entre o total conhecido do bloco e a soma das demais células (dividido igualmente entre as células "X" do bloco). Blocos usados: sexo; sexo×idade; raça; sexo×raça; idade larga×raça; sexo×(0–9/10+)×raça.'),
('','c) Raça 2022 por DS: IPF sobre a matriz sexo × 11 faixas × raça com 4 margens publicadas pelo IBGE: sexo×faixa; sexo×raça; (0–14, 15–29, 30–59, 60+)×raça; sexo×(0–9, 10+)×raça.'),
('','d) Abertura das 11 faixas censitárias nas 18 faixas: 0–4 → <1 e 1–4, e 70+ → 70–74, 75–79, 80+ pelas proporções de 2010 do mesmo DS e sexo; 30–39, 40–49, 50–59 e 60–69 → quinquenais pelo método de coortes (a coorte com 30–34 anos em 2022 tinha 18–22 em 2010; interpolação linear das faixas quinquenais SESAB 2010 do mesmo DS e sexo). A raça de cada subfaixa segue a da faixa-mãe.'),
('','e) Calibração: os setores de cada bairro foram escalados para o total oficial do bairro (IBGE 2022), de modo que Salvador fecha em 2.417.678 e os ≈171 setores sem dados demográficos são compensados dentro do próprio bairro.'),
('4','Série anual'),
('','Totais municipais (FREQ): anos censitários = Censo (2000: 2.443.107; 2010: 2.675.656; 2022: 2.417.678); demais anos = estimativas TCU/IBGE do arquivo pop_TCU.csv da SMS (2023 = RIPSA 2.589.296; 2024 = 2.568.928), 2025 = 2.564.204 e 2026 = 2.559.945 (IBGE Cidades). Os totais por DS do pop_TCU (Lagrange/razão fixa) NÃO foram usados — apenas a linha Total.'),
('','Série alternativa (FREQ_CENSO): totais por crescimento geométrico entre censos e, após 2022, variação anual IBGE (−0,18%/ano), com a mesma estrutura interna.'),
('','Método de distribuição: Razão Censitária (Siegel & Swanson, 2004) com razões variáveis — em vez de fixar a participação de 2010, a participação de cada célula é interpolada geometricamente entre os censos 2010 e 2022 e prolongada fora desse intervalo. Não foi usada extrapolação polinomial de Lagrange (instável e sujeita a valores negativos em células pequenas).'),
('','Composição: a participação de cada célula evolui geometricamente entre 2010 e 2022: s(t) ∝ s2010^(1−w) × s2022^w, w = (t−2010)/12. Para 2023–2026 (w>1) e 2000–2009 (w<0) a mesma fórmula prolonga a tendência 2010–2022 (envelhecimento, deslocamento para Itapuã/Cajazeiras, aumento da autodeclaração preta). Exceção: em 2000–2009 só DS×sexo×idade seguem a tendência; a distribuição de raça dentro de cada DS×sexo×faixa fica igual à de 2010, para não extrapolar para trás a mudança de autodeclaração. FREQ = total do ano × s(t), com arredondamento de maior resto.'),
('5','Bairros (versão 3)'),
('','Total do bairro em 2022 = população oficial IBGE por bairro (169 bairros, soma 2.417.678). Cada bairro foi atribuído ao DS que contém o centróide do seu polígono. Nos outros anos o bairro varia como o seu DS, recalibrado para o total municipal. Sexo×idade×raça do bairro = estrutura do DS no ano. Versão 2: com a chave setor→bairro→DS (script R enviado) a estrutura passa a ser a do próprio bairro.'),
('6','Fontes'),('','IBGE, Censo Demográfico 2010 e 2022 – Agregados por setores censitários (básico, demografia, cor ou raça); IBGE, Estimativas da População 2024–2026; SESAB/SUVISA/DIS, Estimativa da população por faixa etária e sexo nos DS de Salvador, 2010; SMS Salvador, DISTRITO_SANITARIO.shp (2023).')]
for k,v in M: row(ws,[k,v],B if k else N)
# ---------- LIMITACOES
ws=wb.create_sheet('LIMITACOES'); ws.column_dimensions['A'].width=130
for v in ['1. Limites de DS: a tabela SESAB 2010 usa a divisão de DS da época; 2022 usa o shapefile de 2023. Subúrbio, São Caetano/Valéria e Itapagipe seguem divisão administrativa diferente (nota Limitações.docx). Parte da variação 2010→2022 desses DS pode ser mudança de limite.',
'2. Setores atribuídos inteiros ao DS de maior área (60 setores com <90% da área no DS); bairros na interseção com DS seguem essa atribuição.',
'3. Raça 2010 usa proporções de um banco com 78% de cobertura (assume que os setores perdidos têm a mesma composição racial do DS).',
'4. Abertura de faixas (30–39 etc.) por coortes ignora a mortalidade diferencial entre as duas metades da faixa (erro pequeno, maior em 60–69).',
'5. 2000–2009 é retroprojeção sem uso da estrutura do Censo 2000 (não usado por decisão do projeto); qualidade inferior aos demais anos; raça congelada na distribuição de 2010.',
'6. 2023–2026 seguem a tendência; não incorporam migração intramunicipal recente.',
'7. Bairros fora de 2022 seguem a dinâmica do seu DS (estrutura relativa de 2022 constante dentro do DS). Totais de bairro em 2022 diferem do IBGE em no máximo ±19 pessoas por arredondamento. Células pequenas (indígena, amarela por bairro) são estimativas.',
'8. FREQ usa totais TCU, que mudam de método entre períodos (projeções de 2000, de 2010 e, após 2022, com correção de cobertura): saltos em 2010, 2022 e 2023 são artefatos. Não coincide com as estimativas do MS/DATASUS 2000–2024.',
'9. Aquarius: delimitado por área dos setores; o setor 292740805060272 (35% no Aquarius) ficou na Pituba.']: row(ws,[v])
# ---------- DICIONARIO
ws=wb.create_sheet('DICIONARIO'); [setattr(ws.column_dimensions[c],'width',w) for c,w in zip('ABCDEFGH',[12,24,4,10,24,4,12,40])]
H_(ws,['FXET','Faixa etária','','DS','Distrito Sanitário','','COD_BAIRRO','Bairro'])
bl=list(zip(b.COD_BAIRRO,b.bairro))
n=max(18,len(bl))
for i in range(n):
    r=[i+1 if i<18 else None, FX[i] if i<18 else None,None, i+1 if i<12 else None, DSN.get(i+1) if i<12 else None,None]
    r+= [bl[i][0],bl[i][1]] if i<len(bl) else [None,None]
    row(ws,r)
row(ws,[]); H_(ws,['SEXO','Descrição','','RACA','Descrição','','ANO','Tipo de estimativa'])
yrs=list(range(2000,2027))
for i in range(len(yrs)):
    r=[[1,'Masculino'],[2,'Feminino']][i] if i<2 else [None,None]
    r+=[None]+([i+1,RC[i]] if i<5 else [None,None])+[None,str(yrs[i]),Q[yrs[i]]]
    row(ws,r)
# ---------- TOTAIS (fórmulas)
ws=wb.create_sheet('TOTAIS'); ws.column_dimensions['A'].width=10
for c in 'BCDEFGHIJKLMNOPQRS': ws.column_dimensions[c].width=13
H_(ws,['ANO']+[DSN[d] for d in range(1,13)]+['Total (fórmula)','Masculino','Feminino','% negra (2+4)','Tipo','Total só censos (FREQ_CENSO)'])
nr=len(pop)+1
for i,t in enumerate(yrs):
    r=i+2
    v=[t]+[f'=SUMIFS(POP_DS!$F$2:$F${nr},POP_DS!$A$2:$A${nr},$A{r},POP_DS!$C$2:$C${nr},{d})' for d in range(1,13)]
    v+=[f'=SUM(B{r}:M{r})',f'=SUMIFS(POP_DS!$F$2:$F${nr},POP_DS!$A$2:$A${nr},$A{r},POP_DS!$D$2:$D${nr},1)',f'=SUMIFS(POP_DS!$F$2:$F${nr},POP_DS!$A$2:$A${nr},$A{r},POP_DS!$D$2:$D${nr},2)',
        f'=(SUMIFS(POP_DS!$F$2:$F${nr},POP_DS!$A$2:$A${nr},$A{r},POP_DS!$E$2:$E${nr},2)+SUMIFS(POP_DS!$F$2:$F${nr},POP_DS!$A$2:$A${nr},$A{r},POP_DS!$E$2:$E${nr},4))/N{r}',Q[t],f'=SUMIFS(POP_DS!$G$2:$G${nr},POP_DS!$A$2:$A${nr},$A{r})']
    cs=[]
    for j,x in enumerate(v):
        c=WriteOnlyCell(ws,value=x); c.font=N; c.number_format='0.0%' if j==16 else '#,##0' if j>0 else '0'; cs.append(c)
    ws.append(cs)
# ---------- CHECAGENS
ws=wb.create_sheet('CHECAGENS'); ws.column_dimensions['A'].width=70; ws.column_dimensions['B'].width=16; ws.column_dimensions['C'].width=16; ws.column_dimensions['D'].width=12
H_(ws,['Conferência','Esperado','Obtido','OK?'])
nb=len(pb)+1
chk=[('Total 2010 = Censo 2010 (SESAB)',2675656,'=TOTAIS!N12'),('Total 2022 = Censo 2022',2417678,'=TOTAIS!N24'),('Total 2000 = Censo 2000',2443107,'=TOTAIS!N2'),('Total 2014 = TCU',2902927,'=TOTAIS!N16'),('Total 2025 = IBGE Cidades',2564204,'=TOTAIS!N27'),
('POP_BAIRRO 2022 = soma bairros IBGE',2417678,f'=SUMIFS(POP_BAIRRO!$G$2:$G${nb},POP_BAIRRO!$A$2:$A${nb},2022)'),
('POP_BAIRRO 2026 = POP_DS 2026','=TOTAIS!N28',f'=SUMIFS(POP_BAIRRO!$G$2:$G${nb},POP_BAIRRO!$A$2:$A${nb},2026)'),
('Aquarius 2022 (cód. 171) > 0',True,f'=SUMIFS(POP_BAIRRO!$G$2:$G${nb},POP_BAIRRO!$A$2:$A${nb},2022,POP_BAIRRO!$C$2:$C${nb},171)>0'),
('POP_BAIRRO DS Itapuã 2024 = POP_DS','=TOTAIS!I26',f'=SUMIFS(POP_BAIRRO!$G$2:$G${nb},POP_BAIRRO!$A$2:$A${nb},2024,POP_BAIRRO!$B$2:$B${nb},8)'),
('DS Barra/RV 2010 = SESAB',338921,'=TOTAIS!G12'),('DS Cabula/Beiru 2010 = SESAB',385852,'=TOTAIS!J12'),
('Menores de 1 ano 2010 (SESAB)',33296 if False else None,None)]
r=2
for lab,e,o in chk:
    if e is None: continue
    row(ws,[lab,e,o,f'=IF(B{r}=C{r},"OK","VERIFICAR")'],fmt='#,##0'); r+=1
row(ws,[]); row(ws,['Composição racial 2022 (Salvador, estimada) — % do total',None,None,None],B)
for k in range(5):
    rr=r+2+k
    row(ws,[RC[k],None,f'=SUMIFS(POP_DS!$F$2:$F${nr},POP_DS!$A$2:$A${nr},2022,POP_DS!$E$2:$E${nr},{k+1})/TOTAIS!N24',None],fmt='0.0%')
# ---------- POP_DS
ws=wb.create_sheet('POP_DS')
H_(ws,['ANO','FXET','DS','SEXO','RACA','FREQ','FREQ_CENSO'])
for t in pop[['ANO','FXET','DS','SEXO','RACA','FREQ','FREQ_CENSO']].itertuples(index=False): ws.append(list(map(int,t)))
ws=wb.create_sheet('POP_BAIRRO')
H_(ws,['ANO','DS','COD_BAIRRO','FXET','SEXO','RACA','FREQ'])
for t in pb[['ANO','DS','COD_BAIRRO','FXET','SEXO','RACA','FREQ']].itertuples(index=False): ws.append(list(map(int,t)))
ws=wb.create_sheet('SETORES')
k=pd.read_csv(D+'chave_v3.csv',dtype={'CD_SETOR':str,'CD_BAIRRO':str}); Xs=pd.read_pickle(D+'s22_sector_imputed.pkl')[['CD_setor','populacao','domicilios']]
k.columns=[c.strip() for c in k.columns]; k['prop_area']=pd.to_numeric(k['prop_area'].astype(str).str.strip(),errors='coerce'); k=k.merge(Xs,left_on='CD_SETOR',right_on='CD_setor',how='left')
H_(ws,['CD_SETOR','CD_BAIRRO_IBGE','NM_BAIRRO_IBGE','COD_BAIRRO','BAIRRO','DS','NOME_DS','PROP_AREA_NO_DS','AREA_KM2','POP_2022_SETOR','DOMICILIOS_2022','TEM_DADOS_DEMOGRAFIA'])
for r in k.itertuples(index=False):
    ws.append([r.CD_SETOR,r.CD_BAIRRO,r.NM_BAIRRO if isinstance(r.NM_BAIRRO,str) else None,None if pd.isna(r.COD_BAIRRO) else int(r.COD_BAIRRO),r.bairro if isinstance(r.bairro,str) else None,int(r.DS),DSN[int(r.DS)],None if pd.isna(r.prop_area) else round(float(r.prop_area),4),round(float(r.AREA_KM2),4),None if pd.isna(r.populacao) else int(round(r.populacao)),None if pd.isna(r.domicilios) else int(round(r.domicilios)),'Sim' if not pd.isna(r.populacao) else 'Não'])
wb.save('/home/claude/out/POP_SSA_DS_BAIRRO_RACA_2000_2026_v3.xlsx'); print('ok')
