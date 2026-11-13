import warnings; warnings.filterwarnings('ignore')
import pandas as pd,numpy as np,time
D='/home/claude/data/'
PB=pd.read_pickle(D+'pop_full.pkl')          # ANO DS COD_BAIRRO FXET SEXO RACA FREQ
PI=pd.read_pickle(D+'idade/pop_idade.pkl')   # ANO DS SEXO IDADE FXET FREQ
t0=time.time()
PB=PB.sort_values(['ANO','DS','SEXO','FXET','COD_BAIRRO','RACA']).reset_index(drop=True)
PI=PI.sort_values(['ANO','DS','SEXO','FXET','IDADE']).reset_index(drop=True)
gb=PB.groupby(['ANO','DS','SEXO','FXET'],sort=True).indices
gi=PI.groupby(['ANO','DS','SEXO','FXET'],sort=True).indices
outA=[];outI=[]; FREQ=PB.FREQ.values; AF=PI.FREQ.values; AG=PI.IDADE.values
for key,ib in gb.items():
    ia=gi[key]; B=FREQ[ib].astype(float); A=AF[ia].astype(float); n,m=len(B),len(A)
    assert B.sum()==A.sum(),key
    if m==1:
        outA.append(ib); outI.append(np.full(n,AG[ia[0]])); X=B.astype(int)[:,None]
    else:
        tot=A.sum()
        X=np.outer(B,A/tot) if tot>0 else np.zeros((n,m))
        Xi=np.floor(X).astype(int); r=(B-Xi.sum(1)).astype(int); c=(A-Xi.sum(0)).astype(int)
        if r.sum()>0:
            fr=(X-Xi).ravel(); order=np.argsort(-fr,kind='stable')
            for k in order:
                i,j=divmod(k,m)
                if r[i]>0 and c[j]>0: Xi[i,j]+=1; r[i]-=1; c[j]-=1
            for i in np.where(r>0)[0]:               # garantia (raramente usado)
                for j in np.where(c>0)[0]:
                    while r[i]>0 and c[j]>0: Xi[i,j]+=1; r[i]-=1; c[j]-=1
        X=Xi; outA.append(np.repeat(ib,m)); outI.append(np.tile(AG[ia],n))
    globals().setdefault('XS',[]).append(X.ravel())
idx=np.concatenate(outA); age=np.concatenate(outI); fq=np.concatenate(XS)
R=PB.loc[idx,['ANO','DS','COD_BAIRRO','FXET','SEXO','RACA']].reset_index(drop=True); R['IDADE']=age; R['FREQ']=fq
R=R[['ANO','DS','COD_BAIRRO','IDADE','FXET','SEXO','RACA','FREQ']]
print('linhas totais',len(R),' tempo %.0fs'%(time.time()-t0))
# checks
c1=R.groupby(['ANO','DS','COD_BAIRRO','FXET','SEXO','RACA']).FREQ.sum().reset_index().merge(PB,on=['ANO','DS','COD_BAIRRO','FXET','SEXO','RACA'])
c2=R.groupby(['ANO','DS','SEXO','IDADE']).FREQ.sum().reset_index().merge(PI,on=['ANO','DS','SEXO','IDADE'])
print('bate POP_BAIRRO:',(c1.FREQ_x==c1.FREQ_y).all(),' bate DS×idade:',(c2.FREQ_x==c2.FREQ_y).all(),' negativos:',(R.FREQ<0).sum())
Rz=R[R.FREQ>0]; print('linhas com FREQ>0:',len(Rz))
Rz.to_csv('/home/claude/protocolo-metodologico-populacao-salvador-ds-raca/resultados/populacao_salvador_bairro_ds_idade_raca_2000_2026.csv.gz',index=False,compression='gzip')
