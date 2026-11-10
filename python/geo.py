import json, re, struct, numpy as np, pandas as pd
from matplotlib.path import Path
D='/home/claude/data/'
# --- DS shapefile
b=open(D+'DS.shp','rb').read()
DSORDER=[4,5,9,10,11,11,11,11,11,2,1,6,7,8,12,3]
pos=100; recs=[]
while pos<len(b):
    num,ln=struct.unpack('>ii',b[pos:pos+8]); c=b[pos+8:pos+8+ln*2]; pos+=8+ln*2
    st=struct.unpack('<i',c[:4])[0]
    nparts,npts=struct.unpack('<ii',c[36:44])
    parts=list(struct.unpack('<%di'%nparts,c[44:44+4*nparts]))
    pts=np.frombuffer(c[44+4*nparts:44+4*nparts+16*npts],dtype='<f8').reshape(-1,2)
    rings=[pts[parts[i]:(parts[i+1] if i+1<nparts else npts)] for i in range(nparts)]
    recs.append(rings)
print('DS records',len(recs))
def inside(rings,P):
    r=np.zeros(len(P),bool)
    for ring in rings: r ^= Path(ring).contains_points(P)
    return r
# --- sectors
s=json.load(open(D+'entorno_bairros2022.json'))['fileContent']
rows=re.findall(r'"\d+","([^"]*)","(\d{15})"(?:,"[^"]*"){6},(list\(.*?\)\))',s,flags=re.S)
print('sectors',len(rows))
out=[]
for bairro,cd,geo in rows:
    polys=re.findall(r'c\(([^()]*)\)',geo)
    best=None
    for pstr in polys:
        v=np.array([float(x) for x in pstr.replace('\n',' ').split(',')]); n=len(v)//2
        x,y=v[:n],v[n:]
        a=0.5*np.sum(x[:-1]*y[1:]-x[1:]*y[:-1])
        if abs(a)<1e-9: cx,cy=x.mean(),y.mean()
        else:
            cx=np.sum((x[:-1]+x[1:])*(x[:-1]*y[1:]-x[1:]*y[:-1]))/(6*a); cy=np.sum((y[:-1]+y[1:])*(x[:-1]*y[1:]-x[1:]*y[:-1]))/(6*a)
        if best is None or abs(a)>best[0]: best=(abs(a),cx,cy,x,y)
    out.append((cd,bairro,best[1],best[2],best[0]))
sec=pd.DataFrame(out,columns=['CD_setor','bairro','x','y','area'])
P=sec[['x','y']].values
sec['DS']=0
for rings,ds in zip(recs,DSORDER):
    m=inside(rings,P)&(sec.DS.values==0); sec.loc[m,'DS']=ds
# fallback nearest vertex for centroids falling outside
miss=sec.DS==0
if miss.any():
    allpts=np.vstack([np.c_[r,np.full(len(r),ds)] for rings,ds in zip(recs,DSORDER) for r in rings])
    for i in sec.index[miss]:
        d=((allpts[:,0]-sec.x[i])**2+(allpts[:,1]-sec.y[i])**2); sec.loc[i,'DS']=int(allpts[d.argmin(),2])
print('miss',miss.sum()); print(sec.DS.value_counts().sort_index())
sec.to_csv(D+'setor_bairro_ds_2022.csv',index=False)
# bairro x DS cross
ct=pd.crosstab(sec.bairro,sec.DS); multi=ct[(ct>0).sum(1)>1]; print('bairros em >1 DS:',len(multi)); print(multi.to_string())
