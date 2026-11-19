import numpy as np
def lr_round(x,total):
    x=np.asarray(x,float); fl=np.floor(x); rem=int(round(total-fl.sum()))
    if rem>0:
        idx=np.argsort(-(x-fl).ravel(),kind='stable')[:rem]; fl.ravel()[idx]+=1
    return fl.astype(int)
def ipf(X,margins,iters=500,tol=1e-7):
    """X: array; margins: list of (labels(int array same shape as X), target vector). Ajuste proporcional iterativo."""
    X=X.astype(float).copy()
    for it in range(iters):
        err=0
        for L,t in margins:
            s=np.bincount(L.ravel(),X.ravel(),minlength=len(t))
            f=np.where(s>0,t/np.where(s>0,s,1),0); X*=f[L]
            err=max(err,np.abs(s-t).max())
        if err<tol: break
    return X,err
def multi_round(X,margins):
    """Arredondamento controlado: inteiros que respeitam exatamente todas as margens dadas (targets inteiros)."""
    X=np.asarray(X,float); fl=np.floor(X+1e-9); flat=fl.ravel().copy(); fr=(X-fl).ravel()
    defs=[]
    for L,t in margins:
        d=np.asarray(t)-np.bincount(L.ravel(),flat,minlength=len(t)); d=np.round(d).astype(int)
        assert (d>=0).all(), d.min(); defs.append(d)
    assert len({int(d.sum()) for d in defs})==1, [d.sum() for d in defs]
    Ls=[L.ravel() for L,_ in margins]
    order=np.argsort(-fr,kind='stable')
    for _ in range(3):
        for k in order:
            if all(d[L[k]]>0 for d,L in zip(defs,Ls)):
                flat[k]+=1
                for d,L in zip(defs,Ls): d[L[k]]-=1
        if defs[0].sum()==0: break
    # troca residual (raro): mover 1 unidade entre células para fechar margens
    guard=0
    while defs[0].sum()>0 and guard<10000:
        guard+=1
        need=[np.where(d>0)[0] for d in defs]
        # célula que satisfaz o máximo de margens com déficit
        score=sum((d[L]>0).astype(int) for d,L in zip(defs,Ls))
        k=int(np.argmax(score+fr*1e-3))
        flat[k]+=1
        for d,L in zip(defs,Ls): d[L[k]]-=1
        # compensar margens que ficaram negativas retirando de célula com frac pequena e que tenha >0
        for j,(d,L) in enumerate(zip(defs,Ls)):
            while (d<0).any():
                g=np.where(d<0)[0][0]
                cand=np.where((L==g)&(flat>0))[0]
                sc=np.array([sum(dd[LL[c]]<=0 for dd,LL in zip(defs,Ls)) for c in cand])
                c=cand[np.argmax(sc)]; flat[c]-=1
                for dd,LL in zip(defs,Ls): dd[LL[c]]+=1
    assert defs[0].sum()==0 and all((d==0).all() for d in defs), 'arredondamento não fechou'
    return flat.reshape(X.shape).astype(int)
def labels(shape,keep):
    """rótulo de grupo para manter os eixos 'keep'"""
    idx=np.indices(shape); dims=[shape[a] for a in keep]; L=np.zeros(shape,int)
    for a,n in zip(keep,dims): L=L*n+idx[a]
    return L
