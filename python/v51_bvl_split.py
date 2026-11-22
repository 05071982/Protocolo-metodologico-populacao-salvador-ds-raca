# v5.1: cria a unidade (DS 11, bairro 172 Boa Vista do Lobato) e transfere, das unidades de origem,
# a fração proporcional aos domicílios do CNEFE 2022 nos logradouros da Lei 9.919/2025.
import numpy as np, pandas as pd, pickle, sys
sys.path.insert(0,'/home/claude/scripts'); from v4_lib import lr_round
D='/home/claude/data/'; V='/home/claude/data/v5/'; O='/home/claude/data/v51/'
un=pd.read_csv(D+'units.csv'); U=list(zip(un.DS,un.COD_BAIRRO)); Uidx={u:i for i,u in enumerate(U)}; nu=len(U)
FX=np.array([1]+[2]*4+[3+(a-5)//5 for a in range(5,80)]+[18]*21)-1
G11=np.array([0,0,0,1,2,3,4,5,6,6,7,7,8,8,9,9,10,10])   # FXET -> grupos do setor 2022 (0a4,5a9,...,60a69,70+)
p10=pickle.load(open(D+'bvl/share_CD_SETOR_2010.pkl','rb')).p; p22=pickle.load(open(D+'bvl/share_CD_SETOR_2022.pkl','rb')).p
# ---- 2010: fração por unidade × sexo × FXET a partir das idades dos setores
z=np.load(V+'setores2010.npz',allow_pickle=True); AGE,sup,setores=z['AGE'],z['sup'],list(z['setores'])
sec=pd.read_pickle(V+'chave2010.pkl').set_index('CD_SETOR')
num10={}; den10={}
for i,s in enumerate(setores):
    u=sec.u22[s]; u=u if isinstance(u,tuple) else (11,120)
    a=np.stack([np.nan_to_num(AGE[i])[:,FX==f].sum(1) for f in range(18)],1)  # 2×18
    den10[u]=den10.get(u,0)+a
    if s in p10.index: num10[u]=num10.get(u,0)+p10[s]*a
phi10={u:np.where(den10[u]>0,num10[u]/np.maximum(den10[u],1e-9),0) for u in num10}
# ---- 2022: fração por unidade × sexo × grupo (11 grupos) a partir dos setores
X=pd.read_pickle(D+'s22_sector_imputed.pkl'); k=pd.read_csv(D+'chave_v3.csv',dtype={'CD_SETOR':str})
k['prop']=pd.to_numeric(k['prop_area  '],errors='coerce').fillna(1)
X=X.merge(k[['CD_SETOR','DS','COD_BAIRRO','prop']],left_on='CD_setor',right_on='CD_SETOR')
A11=['0a4','5a9','10a14','15a19','20a24','25a29','30a39','40a49','50a59','60a69','70m']
cols=[f'{sx}_{a}' for sx in 'mf' for a in A11]
num22={}; den22={}
for _,r in X.iterrows():
    u=(int(r.DS),int(r.COD_BAIRRO)) if not pd.isna(r.COD_BAIRRO) else None
    if u is None: continue
    a=r[cols].values.astype(float).reshape(2,11)*r.prop
    den22[u]=den22.get(u,0)+a
    if r.CD_setor in p22.index and int(r.DS)==11: num22[u]=num22.get(u,0)+p22[r.CD_setor]*a
phi22g={u:np.where(den22[u]>0,num22[u]/np.maximum(den22[u],1e-9),0) for u in num22}
phi22={u:v[:,G11] for u,v in phi22g.items()}
print('origens 2010',{u:round(float((num10[u]).sum())) for u in num10}); print('origens 2022',{u:round(float(num22[u].sum())) for u in num22})
# ---- aplica às estruturas inteiras
un2=pd.concat([un,pd.DataFrame({'DS':[11],'COD_BAIRRO':[172]})],ignore_index=True); un2.to_csv(O+'units.csv',index=False)
def split(C,phi):
    C2=np.concatenate([C,np.zeros((1,)+C.shape[1:],int)]); mv=np.zeros(C.shape[1:],int)
    for u,ph in phi.items():
        i=Uidx[u]; Xm=C[i]*ph[:,:,None]; n=int(round(Xm.sum()))
        M=lr_round(Xm,n); M=np.minimum(M,C[i]); C2[i]-=M; mv+=M
    C2[-1]=mv; assert C2.sum()==C.sum() and (C2>=0).all(); return C2
res={}
for nm,phi in [('C00',phi10),('C10',phi10),('C22',phi22)]:
    C=np.load(V+nm+'_u.npy'); C2=split(C,phi); np.save(O+nm+'_u.npy',C2); res[nm]=C2
    print(nm,'BVL',C2[-1].sum(),' origem:',{u:int(C[Uidx[u]].sum()-C2[Uidx[u]].sum()) for u in phi})
# idades simples observadas 2010 por unidade (para v5_idade): reparte a do Lobato etc. pela mesma fração por idade
AG=np.load(V+'AGEu10.npy'); AG2=np.concatenate([AG,np.zeros((1,2,101))])
for u,ph in phi10.items(): i=Uidx[u]; mvA=AG[i]*ph[:,FX]; AG2[i]-=mvA; AG2[-1]+=mvA
np.save(O+'AGEu10.npy',AG2)
