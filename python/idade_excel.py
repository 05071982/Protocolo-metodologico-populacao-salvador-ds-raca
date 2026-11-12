import pandas as pd
from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Font,PatternFill
D='/home/claude/data/'
PI=pd.read_pickle(D+'idade/pop_idade.pkl'); tot=pd.read_csv(D+'totais.csv',index_col=0).iloc[:,0]
F='Arial'; H=Font(name=F,bold=True,color='FFFFFF'); HF=PatternFill('solid',fgColor='1F4E78'); N=Font(name=F); B=Font(name=F,bold=True); T=Font(name=F,bold=True,size=13)
wb=Workbook(write_only=True)
def row(ws,v,font=N,fill=None,fmt=None):
    cs=[]
    for x in v:
        c=WriteOnlyCell(ws,value=x); c.font=font
        if fill: c.fill=fill
        if fmt: c.number_format=fmt
        cs.append(c)
    ws.append(cs)
ws=wb.create_sheet('LEIAME'); ws.column_dimensions['A'].width=125
for k,v in [('T','População de Salvador por Distrito Sanitário, sexo e idade simples (0 a 100+ anos) — 2000 a 2026'),
 ('','Complemento da base POP_SSA_DS_BAIRRO_RACA_2000_2026_v3 (DOI 10.5281/zenodo.24096844). Para o TabNet Salvador (idade detalhada).'),('',''),
 ('B','Aba POP_IDADE'),('','ANO, DS, SEXO, IDADE, FXET, FREQ — 65.448 linhas (27 anos × 12 DS × 2 sexos × 101 idades). IDADE 100 = 100 anos e mais.'),
 ('','FXET é a faixa etária (18 faixas) a que a idade pertence. Somando FREQ por ANO × DS × SEXO × FXET obtém-se EXATAMENTE a base principal (POP_DS / POP_BAIRRO), em todos os anos.'),
 ('',''),('B','Método'),
 ('','1. 2010 (observado): proporção de cada idade dentro da sua faixa, por DS e sexo, do banco Censo 2010 por DS (idades simples do IBGE; usado só como proporção).'),
 ('','2. 2022 (estimado): o Censo 2022 por setor só traz faixas; as faixas quinquenais de cada DS × sexo foram desagregadas em idades simples pela interpolação osculatória de Sprague (Siegel & Swanson, 2004). Idade 0 = faixa <1; 1–4 rateados pelos multiplicadores; 80–100+ com a forma observada em 2010.'),
 ('','3. Demais anos: Razão Censitária com razões variáveis aplicada DENTRO de cada faixa: p(idade|faixa,t) ∝ p2010^(1−w) × p2022^w, w = (t−2010)/12; FREQ = população da faixa (base principal) × p, arredondada pelo maior resto dentro da faixa.'),
 ('','Validação: aplicando Sprague às faixas de 2010 e comparando com as idades observadas de 2010, o erro absoluto total foi de 4,1% (idades 1–79, por DS e sexo) — parte dele é a preferência digital do censo (idades terminadas em 0 e 5), que o método suaviza.'),
 ('',''),('B','Cuidados'),('','• Idades simples por DS têm mais ruído que as faixas; para taxas, prefira agrupar idades sempre que possível.'),
 ('','• 80 a 100+ seguem a forma de 2010 (o Censo 2022 por setor só tem 70+).')]:
    row(ws,[v],T if k=='T' else B if k=='B' else N)
ws=wb.create_sheet('DICIONARIO'); [setattr(ws.column_dimensions[c],'width',w) for c,w in zip('ABCDE',[8,10,4,8,28])]
FXN=['<1','1-4','5-9','10-14','15-19','20-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79','80+']
row(ws,['IDADE','FXET','','FXET','Faixa'],H,HF)
fx=PI[(PI.ANO==2022)&(PI.DS==1)&(PI.SEXO==1)][['IDADE','FXET']].values
for i,(a,f) in enumerate(fx): row(ws,['100+' if a==100 else int(a),int(f),None]+([i+1,FXN[i]] if i<18 else [None,None]))
ws=wb.create_sheet('TOTAIS'); ws.column_dimensions['A'].width=8; ws.column_dimensions['B'].width=18; ws.column_dimensions['C'].width=18; ws.column_dimensions['D'].width=10
row(ws,['ANO','Total oficial','Soma POP_IDADE','OK?'],H,HF); n=len(PI)+1
for i,t in enumerate(tot.index):
    r=i+2; row(ws,[int(t),int(tot[t]),f'=SUMIFS(POP_IDADE!$F$2:$F${n},POP_IDADE!$A$2:$A${n},A{r})',f'=IF(B{r}=C{r},"OK","VERIFICAR")'],fmt='#,##0')
ws=wb.create_sheet('POP_IDADE'); row(ws,['ANO','DS','SEXO','IDADE','FXET','FREQ'],H,HF)
for t in PI[['ANO','DS','SEXO','IDADE','FXET','FREQ']].itertuples(index=False): ws.append(list(map(int,t)))
wb.save('/home/claude/out/POP_SSA_DS_SEXO_IDADE_SIMPLES_2000_2026.xlsx'); print('ok')
