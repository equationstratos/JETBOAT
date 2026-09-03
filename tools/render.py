import struct,sys,math
import numpy as np
from PIL import Image

def load(p):
    with open(p,'rb') as f:
        h=f.read(84); n=struct.unpack('<I',h[80:84])[0]
        raw=f.read(n*50)
        d=np.frombuffer(raw,dtype=np.uint8).reshape(n,50)
        return d[:,12:48].copy().view('<f4').reshape(n,3,3).astype(np.float64)

def rotm(ax,ay,az):
    cx,sx=math.cos(ax),math.sin(ax); cy,sy=math.cos(ay),math.sin(ay); cz,sz=math.cos(az),math.sin(az)
    Rx=np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]])
    Ry=np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]])
    Rz=np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]])
    return Rz@Ry@Rx

def render(tri_list, colors, view, W=700,H=520, bg=(18,22,28), cull=True):
    # view: (elev, azim) degrees. camera looks along -Z after rotation
    el,az=[math.radians(a) for a in view]
    R = rotm(-el,0,0) @ rotm(0,-az,0)
    allv=np.vstack([t.reshape(-1,3) for t in tri_list])
    c=(allv.min(0)+allv.max(0))/2
    P=[ (t-c)@R.T for t in tri_list]
    pv=np.vstack([p.reshape(-1,3) for p in P])
    mn=pv[:,:2].min(0); mx=pv[:,:2].max(0)
    span=max(mx[0]-mn[0], mx[1]-mn[1])*1.06
    sc=min(W,H)/span
    cx=(mn[0]+mx[0])/2; cy=(mn[1]+mx[1])/2
    img=np.zeros((H,W,3),np.float64); img[:]=bg
    zb=np.full((H,W),-1e18)
    light=np.array([0.4,0.6,0.7]); light/=np.linalg.norm(light)
    for p,col in zip(P,colors):
        n=np.cross(p[:,1]-p[:,0],p[:,2]-p[:,0])
        ln=np.linalg.norm(n,axis=1); ln[ln==0]=1; n=n/ln[:,None]
        sh=(np.abs(n@light) if not cull else np.clip(n@light,0,1))*0.75+0.25
        sx=(p[:,:,0]-cx)*sc+W/2; sy=H/2-(p[:,:,1]-cy)*sc
        z=p[:,:,2]
        # cull back faces
        keep=(n[:,2]>0) if cull else np.ones(len(n),bool)
        for idx in np.nonzero(keep)[0]:
            x0,x1,x2=sx[idx]; y0,y1,y2=sy[idx]; z0,z1,z2=z[idx]
            xmin=max(int(min(x0,x1,x2)),0); xmax=min(int(max(x0,x1,x2))+1,W-1)
            ymin=max(int(min(y0,y1,y2)),0); ymax=min(int(max(y0,y1,y2))+1,H-1)
            if xmax<xmin or ymax<ymin: continue
            X,Y=np.meshgrid(np.arange(xmin,xmax+1),np.arange(ymin,ymax+1))
            d=( (y1-y2)*(x0-x2)+(x2-x1)*(y0-y2) )
            if abs(d)<1e-9: continue
            w0=((y1-y2)*(X-x2)+(x2-x1)*(Y-y2))/d
            w1=((y2-y0)*(X-x2)+(x0-x2)*(Y-y2))/d
            w2=1-w0-w1
            m=(w0>=0)&(w1>=0)&(w2>=0)
            if not m.any(): continue
            zz=w0*z0+w1*z1+w2*z2
            sub=zb[ymin:ymax+1,xmin:xmax+1]
            upd=m&(zz>sub)
            if not upd.any(): continue
            sub[upd]=zz[upd]
            tgt=img[ymin:ymax+1,xmin:xmax+1]
            tgt[upd]=np.array(col)*sh[idx]
    return Image.fromarray(np.clip(img,0,255).astype(np.uint8))
