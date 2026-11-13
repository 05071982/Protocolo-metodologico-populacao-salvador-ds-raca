# acrescenta abas tabuladas (2010/2022 × Masc/Fem/Total) ao workbook de idade simples
exec(open('/home/claude/scripts/idade_excel.py').read().split("wb.save(")[0])
from openpyxl.utils import get_column_letter as L
DSN={1:'Centro Histórico',2:'Itapagipe',3:'São Caetano/Valéria',4:'Liberdade',5:'Brotas',6:'Barra/Rio Vermelho',7:'Boca do Rio',8:'Itapuã',9:'Cabula/Beiru',10:'Pau da Lima',11:'Subúrbio Ferroviário',12:'Cajazeiras'}
def tabs(name,col,cats,labels,titulo):
    ws=wb.create_sheet(name); ws.column_dimensions['A'].width=24
    for j in range(2,len(cats)+3): ws.column_dimensions[L(j)].width=9
    rn=0; last=L(len(cats)+1); totc=L(len(cats)+2)
    for ano in (2010,2022):
        for sx,sxl in ((1,'Masculino'),(2,'Feminino'),(0,'Total (ambos os sexos)')):
            row(ws,[f'{titulo} — {sxl}, {ano}'],B); rn+=1
            row(ws,['Distrito Sanitário']+labels+['Total'],H,HF); rn+=1; first=rn+1
            for ds in range(1,13):
                rn+=1; v=[DSN[ds]]
                for c in cats:
                    cond=f'POP_IDADE!$A$2:$A${n},{ano},POP_IDADE!$B$2:$B${n},{ds},POP_IDADE!${col}$2:${col}${n},{c}'
                    if sx: cond+=f',POP_IDADE!$C$2:$C${n},{sx}'
                    v.append(f'=SUMIFS(POP_IDADE!$F$2:$F${n},{cond})')
                v.append(f'=SUM(B{rn}:{last}{rn})'); row(ws,v,fmt='#,##0')
            rn+=1; row(ws,['Salvador']+[f'=SUM({L(j)}{first}:{L(j)}{rn-1})' for j in range(2,len(cats)+3)],B,fmt='#,##0')
            row(ws,[]); rn+=1
tabs('TAB_IDADE_2010_2022','D',list(range(101)),[str(a) for a in range(100)]+['100+'],'População por Distrito Sanitário e idade simples')
tabs('TAB_FXET_2010_2022','E',list(range(1,19)),FXN,'População por Distrito Sanitário e faixa etária')
wb.save('/home/claude/out/POP_SSA_DS_SEXO_IDADE_SIMPLES_2000_2026.xlsx'); print('ok')
