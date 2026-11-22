import warnings; warnings.filterwarnings('ignore')
import pandas as pd,numpy as np
from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Font,PatternFill,Alignment
D='/home/claude/data/'
pop=pd.read_pickle(D+'v51/pop_ds.pkl'); pb=pd.read_pickle(D+'v51/pop_full_z.pkl'); b=pd.read_csv(D+'bairros_final_v51.csv').sort_values('COD_BAIRRO')
tot=pd.read_csv(D+'totais.csv',index_col=0).iloc[:,0]

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
L=[('T','População de Salvador por Distrito Sanitário, bairro, sexo, faixa etária e raça/cor — 2000 a 2026 (versão 5.1)'),
('','Elaboração: Sala de Situação em Saúde de Salvador (SDSS/SMS). Totais municipais: Censos 2000, 2010 e 2022 e estimativas TCU/IBGE nos demais anos (2023: RIPSA; 2025–2026: IBGE Cidades). Distribuição interna (DS, bairro): setores censitários de 2010 e 2022 nos limites atuais. Documentação: wiki do repositório · DOI 10.5281/zenodo.24096844.'),
('',''),('B','Abas'),
('','POP_BAIRRO — tabela completa (ANO, DS, COD_BAIRRO, FXET, SEXO, RACA, FREQ), 172 bairros (inclui Aquarius, cód. 171, Boa Vista do Lobato, cód. 172, e Aeroporto, cód. 2, com FREQ = 0). Cada linha é a parte de um bairro dentro de um DS. Somando por DS obtém-se exatamente POP_DS. Use no TabNet e no BI.'),
('','POP_DS — mesma série agregada por DS no formato do pop14 (ANO, FXET, DS, SEXO, RACA, FREQ, FREQ_CENSO). FREQ = totais oficiais; FREQ_CENSO = série alternativa com totais apenas censitários (tendência).'),
('','RECONCILIACAO_SESAB — comparação ano a ano com o TabNet SESAB (total e estrutura sexo × faixa). VALIDACAO — conferências da versão 5.1.'),
('','SETORES, TOTAIS, CHECAGENS, DICIONARIO, METODOLOGIA e LIMITACOES.'),
('',''),('B','O que mudou na versão 5.1'),
('','• Novo bairro 172, Boa Vista do Lobato (Lei 9.919/2025), delimitado pelos endereços do CNEFE 2022 nos logradouros da lei e desmembrado do Lobato, Alto do Cabrito e Boa Vista de São Caetano (DS 11). Aparece em toda a série nos limites atuais.'),
('',''),('B','O que mudou na versão 5'),
('','• 2010 passa a ser construído setor a setor (3.546 setores do Censo 2010, agregados por setor do IBGE), nos limites atuais de bairro e DS, com raça/cor do universo em todos os setores (antes: tabela por DS e banco parcial).'),
('','• Cada bairro tem estrutura observada em 2010 e em 2022 e segue a própria tendência entre os censos (antes: proporção fixa de 2022 dentro do DS).'),
('','• Anos censitários continuam fechando exatamente com o IBGE: 2000 (sexo × faixa, raça, DS), 2010 (sexo × idade × raça; bairros = soma dos setores) e 2022 (sexo × faixa; bairros).'),
('','• Após 2022, a tendência é aplicada no nível do DS e repartida pelos bairros na proporção de 2022, para não extrapolar crescimentos pontuais de bairros.'),
('',''),('B','Leitura rápida'),
('','• Totais TCU têm quebras metodológicas (2009→2010, 2021→2022, 2022→2023, e 2007) que não são variação real. Para tendência use FREQ_CENSO.'),
('','• Raça/cor: 1 Branca, 2 Preta, 3 Amarela, 4 Parda, 5 Indígena. "Negra" = 2+4. Sem declaração redistribuída proporcionalmente.'),
('','• Inteiros por arredondamento controlado: totais e margens censitárias fecham exatamente; células muito pequenas são estimativas.')]
for k,v in L: row(ws,[v],T if k=='T' else B if k=='B' else N)
# ---------- METODOLOGIA
ws=wb.create_sheet('METODOLOGIA'); ws.column_dimensions['A'].width=6; ws.column_dimensions['B'].width=130
M=[('1','Unidade e células'),('','2.160 células por ano (12 DS × 2 sexos × 18 faixas × 5 raças), repartidas em 195 unidades bairro × DS (172 bairros). Cada ano soma o total municipal oficial.'),
('2','Hierarquia de fontes (versão 5)'),
('','Nível 1 — total do município: Censo (2000, 2010, 2022) e TCU/IBGE nos demais anos. Nível 2 — sexo × idade do município: censos. Nível 3 — raça do município: Censo 2000 (amostra, SIDRA 136), 2010 e 2022 (universo). Nível 4 — DS e bairro: setores censitários. SESAB fora dos censos: comparação publicada (RECONCILIACAO_SESAB), não ajuste.'),
('3','Censo 2022'),('','Agregados por setor (4.542 setores; chave setor→bairro→DS por maior área; sigilo "X" imputado por resíduo do bloco; raça por IPF com 4 margens do IBGE; 11 faixas abertas em 18). Bairros calibrados ao total oficial IBGE 2022. Versão 4: IPF por unidade bairro × DS com margens (a) total da unidade, (b) unidade × raça e (c) sexo × faixa do município = Censo 2022 (as idades simples 0–19 também fecham com o censo).'),
('4','Censo 2010'),('','Agregados por setor do universo (3.546 setores com moradores; malha 2010 do IBGE). Chave setor → bairro × DS: unidade da chave 2022 para setores com o mesmo código (quando o polígono de 2010 tem ao menos 25% da área nela) e, nos demais, maior área de interseção com a malha oficial de bairros e DS. Idade simples por sexo (Pessoa11/12) e raça por sexo e grupo etário (Pessoa03/05). IPF por unidade: unidade × sexo × faixa (setores), unidade × sexo × grupo × raça (setores) e sexo × faixa × raça do município (SIDRA 3175). 9 setores com sigilo (475 pessoas): estrutura da própria unidade.'),
('5','Censo 2000'),('','IPF partindo da estrutura de 2010 por bairro × DS (interações bairro × idade × raça) com margens: total por DS (tabela DS 2000, mesmos limites), sexo × faixa (Censo 2000) e raça (SIDRA 136, sem declaração redistribuída). Idades simples 0–19 fecham com o Censo 2000.'),
('6','Série anual'),('','Razão Censitária com razões variáveis: s(t) ∝ s2000^(1−w)·s2010^w, w=(t−2000)/10 em 2001–2009; s(t) ∝ s2010^(1−w)·s2022^w, w=(t−2010)/12 de 2011 a 2021, aplicadas a cada célula bairro × DS × sexo × faixa × raça (cada bairro com tendência própria). Após 2022: tendência no nível DS × sexo × faixa × raça (w>1), repartida entre os bairros do DS na proporção de 2022. FREQ = total oficial × s(t), arredondamento de maior resto.'),
('7','Atualização anual'),('','Acrescente o total do ano em dados/entrada/totais_municipais.csv e rode R/04 a R/07 (ver wiki).'),
('8','Fontes'),('','IBGE: Censos 2000, 2010 e 2022 (agregados por setor; SIDRA 136 e 3175); estimativas TCU/IBGE; RIPSA 2023. SESAB/SUVISA/DIVEP: população por sexo e faixa etária (TabNet) e tabela por DS 2010. SMS Salvador: totais por DS 2000; shapefiles de DS e bairros.')]
for k,v in M: row(ws,[k,v],B if k else N)
# ---------- LIMITACOES
ws=wb.create_sheet('LIMITACOES'); ws.column_dimensions['A'].width=130
for v in ['1. Limites: 2010 e 2022 foram reagregados nos limites atuais de bairro e DS. A tabela SESAB 2010 (limites da época) difere da base em até 0,8% por DS.',
'2. Setores atribuídos inteiros a uma unidade bairro × DS (2022: maior área; 2010: código da chave 2022 ou maior área). Setores divididos entre bairros geram imprecisão em bairros pequenos (ex.: Centro Administrativo da Bahia, Mares).',
'3. Bairros de 2022 seguem a codificação de bairros do IBGE; em 2010, 96% da população cai no mesmo bairro pelos dois critérios.',
'4. Raça 2000 vem da amostra do censo; a interação bairro × idade × raça de 2000 é a de 2010 ajustada às margens de 2000.',
'5. Idades simples por DS: 2010 observadas (setores); 2000 e 2022 por Sprague nas idades 20+ (0–19 fecham com os censos).',
'6. Em 2010, raça por faixa dentro de 60–69 e 70+ segue o grupo amplo do setor, ajustada ao universo municipal.',
'7. FREQ usa totais TCU (quebras em 2007, 2010, 2022, 2023). Diferenças com a SESAB estão na aba RECONCILIACAO_SESAB.',
'8. 2023–2026 prolongam a tendência 2010–2022 por DS; os bairros mantêm a proporção de 2022 dentro do DS.',
'9. Aquarius (lei de 2024) aparece em toda a série nos limites atuais: os setores que hoje caem em seu polígono foram atribuídos ao código 171.',
'10. Boa Vista do Lobato (lei de 2025) não tem polígono oficial: foi delimitado pelos endereços do CNEFE 2022 nos 34 logradouros da lei (33 encontrados; a Rua Aristóteles Boaventura não consta do CNEFE). Cada setor contribui com a fração de seus domicílios nessas ruas. Revisar quando a Prefeitura publicar o polígono.']: row(ws,[v])
# ---------- DICIONARIO
ws=wb.create_sheet('DICIONARIO'); [setattr(ws.column_dimensions[c],'width',w) for c,w in zip('ABCDEFGH',[12,24,4,10,24,4,12,40])]
H_(ws,['FXET','Faixa etária','','DS','Distrito Sanitário','','COD_BAIRRO','Bairro'])
dic=pd.read_csv(D+'dicionario_bairros_172.csv'); bl=list(zip(dic.COD_BAIRRO,dic.BAIRRO+dic.COD_BAIRRO.map({2:' (sem população residente)'}).fillna('')))
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
('Boa Vista do Lobato 2022 (cód. 172) = 6.219',6219,f'=SUMIFS(POP_BAIRRO!$G$2:$G${nb},POP_BAIRRO!$A$2:$A${nb},2022,POP_BAIRRO!$C$2:$C${nb},172)'),
('Aquarius 2022 (cód. 171) > 0',True,f'=SUMIFS(POP_BAIRRO!$G$2:$G${nb},POP_BAIRRO!$A$2:$A${nb},2022,POP_BAIRRO!$C$2:$C${nb},171)>0'),
('POP_BAIRRO DS Itapuã 2024 = POP_DS','=TOTAIS!I26',f'=SUMIFS(POP_BAIRRO!$G$2:$G${nb},POP_BAIRRO!$A$2:$A${nb},2024,POP_BAIRRO!$B$2:$B${nb},8)'),
('DS Barra/RV 2010 = soma dos setores (limites atuais)',338299,'=TOTAIS!G12'),
('2000: Masculino = Censo 2000',1150252,'=TOTAIS!O2'),('2022: Feminino = Censo 2022',1315298,'=TOTAIS!P24')]
r=2
for lab,e,o in chk:
    if e is None: continue
    row(ws,[lab,e,o,f'=IF(B{r}=C{r},"OK","VERIFICAR")'],fmt='#,##0'); r+=1
row(ws,['DS 2010 (limites atuais) × tabela SESAB (limites de 2010): ver aba VALIDACAO — diferença máxima 0,8%','','',''])
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
ws=wb.create_sheet('RECONCILIACAO_SESAB'); rc=pd.read_csv(D+'v51/reconciliacao_sesab.csv'); H_(ws,list(rc.columns)+['NOTA'])
NT={2000:'Censo',2010:'Censo',2022:'Censo',2007:'SESAB usa projeção UNFPA/IBGE; base usa TCU',2023:'SESAB repete Censo 2022; base usa RIPSA',2001:'Arquivo TCU',2002:'Arquivo TCU'}
for r_ in rc.itertuples(index=False): row(ws,list(r_)+[NT.get(r_[0],'Fora dos censos a SESAB quase repete a estrutura do censo anterior' if r_[4]>3 else '')])
ws=wb.create_sheet('VALIDACAO'); vv=pd.read_csv(D+'v51/validacao_v5_1.csv'); H_(ws,list(vv.columns))
for r_ in vv.fillna('').itertuples(index=False): row(ws,list(r_))
ws=wb.create_sheet('SETORES')
k=pd.read_csv(D+'chave_v3.csv',dtype={'CD_SETOR':str,'CD_BAIRRO':str}); Xs=pd.read_pickle(D+'s22_sector_imputed.pkl')[['CD_setor','populacao','domicilios']]
k.columns=[c.strip() for c in k.columns]; k['prop_area']=pd.to_numeric(k['prop_area'].astype(str).str.strip(),errors='coerce'); k=k.merge(Xs,left_on='CD_SETOR',right_on='CD_setor',how='left')
H_(ws,['CD_SETOR','CD_BAIRRO_IBGE','NM_BAIRRO_IBGE','COD_BAIRRO','BAIRRO','DS','NOME_DS','PROP_AREA_NO_DS','AREA_KM2','POP_2022_SETOR','DOMICILIOS_2022','TEM_DADOS_DEMOGRAFIA'])
for r in k.itertuples(index=False):
    ws.append([r.CD_SETOR,r.CD_BAIRRO,r.NM_BAIRRO if isinstance(r.NM_BAIRRO,str) else None,None if pd.isna(r.COD_BAIRRO) else int(r.COD_BAIRRO),r.bairro if isinstance(r.bairro,str) else None,int(r.DS),DSN[int(r.DS)],None if pd.isna(r.prop_area) else round(float(r.prop_area),4),round(float(r.AREA_KM2),4),None if pd.isna(r.populacao) else int(round(r.populacao)),None if pd.isna(r.domicilios) else int(round(r.domicilios)),'Sim' if not pd.isna(r.populacao) else 'Não'])
ws=wb.create_sheet('BOA_VISTA_LOBATO'); bvf=pd.read_csv('/home/claude/protocolo-metodologico-populacao-salvador-ds-raca/dados/entrada/boa_vista_lobato_fracao_setores.csv',dtype={'CD_SETOR':str})
row(ws,['Bairro 172 — Boa Vista do Lobato (Lei 9.919/2025). Fração de cada setor = domicílios do CNEFE 2022 nos logradouros da lei ÷ domicílios do setor. Setor 2010 localizado pelas coordenadas dos endereços.'],B)
H_(ws,list(bvf.columns))
for r_ in bvf.itertuples(index=False): row(ws,list(r_))
wb.save('/home/claude/out/POP_SSA_DS_BAIRRO_RACA_2000_2026_v5_1.xlsx'); print('ok')
