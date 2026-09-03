import struct,sys
import numpy as np
def load(p):
    with open(p,'rb') as f:
        h=f.read(84); n=struct.unpack('<I',h[80:84])[0]
        raw=f.read(n*50)
        d=np.frombuffer(raw,dtype=np.uint8).reshape(n,50)
        return d[:,12:48].copy().view('<f4').reshape(n,3,3).astype(np.float64)

def slice_pts(t, axis, val):
    out=[]
    for i in range(3):
        a=t[:,i,:]; b=t[:,(i+1)%3,:]
        da=a[:,axis]-val; db=b[:,axis]-val
        m=((da<=0)&(db>0))|((da>0)&(db<=0))
        if m.sum()==0: continue
        aa=a[m]; bb=b[m]; f=(val-aa[:,axis])/(bb[:,axis]-aa[:,axis])
        out.append(aa+f[:,None]*(bb-aa))
    if not out: return np.zeros((0,3))
    return np.vstack(out)

def show(pts, a1,a2, lo,hi,res):
    w=int((hi[0]-lo[0])/res)+1; h=int((hi[1]-lo[1])/res)+1
    g=[[' ']*w for _ in range(h)]
    for p in pts:
        i=int((p[a1]-lo[0])/res); j=int((p[a2]-lo[1])/res)
        if 0<=i<w and 0<=j<h: g[j][i]='#'
    return '\n'.join(''.join(r) for r in reversed(g))

if __name__=='__main__':
    p=sys.argv[1]; axis=int(sys.argv[2]); vals=[float(x) for x in sys.argv[3].split(',')]
    a1,a2=[int(x) for x in sys.argv[4].split(',')]
    res=float(sys.argv[5]) if len(sys.argv)>5 else 1.2
    t=load(p); v=t.reshape(-1,3)
    lo=[v[:,a1].min(),v[:,a2].min()]; hi=[v[:,a1].max(),v[:,a2].max()]
    for val in vals:
        pts=slice_pts(t,axis,val)
        print(f'=== {p} {"XYZ"[axis]}={val}  h={"XYZ"[a1]}[{lo[0]:.1f},{hi[0]:.1f}] v={"XYZ"[a2]}[{lo[1]:.1f},{hi[1]:.1f}] res={res} ===')
        if len(pts)==0: print('(empty)'); continue
        print(f'   local range h[{pts[:,a1].min():.2f},{pts[:,a1].max():.2f}] v[{pts[:,a2].min():.2f},{pts[:,a2].max():.2f}]')
        print(show(pts,a1,a2,lo,hi,res))
