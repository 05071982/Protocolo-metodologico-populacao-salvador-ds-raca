# Lê e valida insumos externos da v4: SIDRA 3175 (2010), SIDRA 136 (2000), SESAB/Censo sexo×idade (2000, 2010, 2022), DS 2000
import openpyxl, numpy as np, pandas as pd, re, io
D='/home/claude/data/'; V=D+'v4/'
ws=openpyxl.load_workbook('/mnt/user-data/uploads/d721d2e5-Tabela_3175.xlsx',data_only=True)['Tabela']
rows=list(ws.iter_rows(values_only=True))
num=lambda v: 0 if v in ('-',None) else int(v)
T3175=np.zeros((2,101,6))   # sexo, idade 0..100+, raça (B,P,A,Pd,I,SemDecl)
for sx,(a,b) in enumerate([(143,279),(279,415)]):
    for r in rows[a:b]:
        lab=r[1]
        if lab=='Menos de 1 ano': i=0
        elif re.fullmatch(r'\d+ anos?',lab): i=int(lab.split()[0])
        elif lab.startswith('100 anos'): i=100
        else: continue
        T3175[sx,i]=[num(v) for v in r[3:9]]
tot=np.array([num(rows[143][2]),num(rows[279][2])])
assert (T3175.sum((1,2))==tot).all(), (T3175.sum((1,2)),tot)
print('3175 ok: H',tot[0],'M',tot[1],'raças',T3175.sum((0,1)))
np.save(V+'T3175.npy',T3175)
# SESAB (2000-2025, município): faixas detalhadas por sexo
def load(f):
    L=open(f,encoding='latin1').read().splitlines(); i=[k for k,l in enumerate(L) if l.startswith('"Faixa')][0]
    d=pd.read_csv(io.StringIO("\n".join(l for l in L[i:] if l.startswith('"'))),sep=';'); d=d.set_index(d.columns[0]); return d
SM,SF=load(D+'sesab/masc.csv'),load(D+'sesab/fem.csv')
def fx(f):
    if f.startswith('Menor'): return 1
    if f.startswith('80'): return 18
    a=int(f.split()[0]); return 2 if a<5 else (3+(a-5)//5 if a<20 else 6+(a-20)//5)
def single(f):  # idade simples 0..19 quando houver
    if f.startswith('Menor'): return 0
    m=re.fullmatch(r'(\d+) anos?',f); return int(m.group(1)) if m else None
SES={}   # ano -> (FXET[2,18], SING[2,20])
for ano in [str(y) for y in range(2000,2026)]:
    F=np.zeros((2,18)); S=np.zeros((2,20))
    for si,dd in enumerate([SM,SF]):
        for f,v in dd[ano].items():
            if f=='Total': assert v==dd[ano].drop('Total').sum(); continue
            F[si,fx(f)-1]+=v; s=single(f)
            if s is not None: S[si,s]=v
    SES[int(ano)]=(F,S)
pd.to_pickle(SES,V+'sesab.pkl')
# validações cruzadas
F10=np.zeros((2,18))
FX=np.array([1]+[2]*4+[3+(a-5)//5 for a in range(5,80)]+[18]*21)
for f in range(18): F10[:,f]=T3175[:,FX==f+1,:].sum((1,2))
print('SESAB 2010 = 3175 (sexo×FXET):',np.abs(SES[2010][0]-F10).max())
print('SESAB 2010 idades 0-19 = 3175:',np.abs(SES[2010][1]-T3175[:,:20].sum(2)).max())
s10=pd.read_csv(D+'sesab2010.csv').groupby(['SEXO','FXET']).POP.sum().unstack().values
print('sesab2010 por DS (soma) = 3175:',np.abs(s10-F10).max())
OBS=np.load(D+'idade/OBS2010.npy'); print('banco DS 2010 idade simples (soma) vs 3175: máx dif',np.abs(OBS.sum(0)-T3175.sum(2)).max(),' total banco',OBS.sum())
C10=np.load(D+'C10.npy'); print('C10 DS×sexo×FXET vs sesab2010 por DS: máx',np.abs(C10.sum(3)-pd.read_csv(D+'sesab2010.csv').pivot_table(index=['DS','SEXO'],columns='FXET',values='POP').values.reshape(12,2,18)).max())
# raça 2000 (SIDRA 136)
R00=np.array([562834,498591,7342,1338878,18712],float); sd=16749
print('SIDRA136 2000 soma',R00.sum()+sd,'(total censo 2443107)')
R10_136=np.array([505739,733253,37043,1386842,7932]); print('3175 vs 136 (2010):',T3175.sum((0,1))[:5]-R10_136, 'sem decl 3175',T3175[...,5].sum(),'136',4847)
DS00=np.array([72262,160374,227858,183647,190971,330697,104447,199307,335138,194950,304305,139151]); print('DS 2000 soma',DS00.sum())
np.save(V+'DS00.npy',DS00); np.save(V+'R00.npy',R00)
C22=np.load(D+'C22.npy'); print('C22 sexo×FXET - censo 2022 máx',np.abs(C22.sum((0,3))-SES[2022][0]).max(),' raça C22',C22.sum((0,1,2)).round())
