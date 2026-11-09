"""Bend three woven plies along the hero's original Bezier thread."""
import math
from bisect import bisect_left

def render(curves=None, prefix="hero-ply"):
    curves=curves or [((-20,80),(90,20),(70,180),(210,135)),((210,135),(350,90),(370,40),(430,100)),((430,100),(490,160),(440,195),(390,147)),((390,147),(340,99),(570,68),(690,130)),((690,130),(810,192),(860,200),(1020,90))]
    points=[]
    for a,b,c,d in curves:
        for k in range(301):
            t=k/300;u=1-t
            points.append(tuple(u**3*a[j]+3*u*u*t*b[j]+3*u*t*t*c[j]+t**3*d[j] for j in (0,1)))
    lengths=[0.0]
    for a,b in zip(points,points[1:]):lengths.append(lengths[-1]+math.dist(a,b))
    total=lengths[-1];period=32;amplitude=2.7
    def point(s,i):
        s=max(0,min(total,s));k=max(1,min(len(points)-1,bisect_left(lengths,s)))
        while lengths[k]==lengths[k-1] and k<len(points)-1:k+=1
        a,b=points[k-1:k+1];distance=lengths[k]-lengths[k-1]
        t=(s-lengths[k-1])/distance if distance else 0
        dx,dy=b[0]-a[0],b[1]-a[1];norm=math.hypot(dx,dy) or 1
        offset=amplitude*math.sin(2*math.pi*s/period+i*2*math.pi/3)
        return a[0]+t*dx-offset*dy/norm,a[1]+t*dy+offset*dx/norm
    def path(i,start,end):
        n=max(2,math.ceil((end-start)*2))
        return 'M'+' L'.join('%.2f,%.2f'%point(start+(end-start)*k/n,i) for k in range(n+1))
    gaps=[[],[],[]]
    for i in range(3):
        for j in range(i+1,3):
            for k in range(-3,int(total/period)*2+5):
                s=period/(2*math.pi)*(math.pi/2+k*math.pi-(i+j)*math.pi/3)
                if 0<s<total:
                    over=i if k%2==0 else j;under=j if over==i else i
                    gaps[under].append(f'<path d="{path(over,s-2,s+2)}" stroke="black" stroke-width="2.9"/>')
    defs=''.join(f'<mask id="{prefix}-{i}" maskUnits="userSpaceOnUse" x="-200" y="-200" width="1500" height="500"><rect x="-200" y="-200" width="1500" height="500" fill="white"/>'+''.join(gaps[i])+'</mask>' for i in range(3))
    return '<defs>'+defs+'</defs>'+''.join(f'<path d="{path(i,0,total)}" stroke="{color}" stroke-width="1.9" stroke-linecap="round" mask="url(#{prefix}-{i})"/>' for i,color in enumerate(['#bd6038','#e88a50','#f4b17b']))


def render_ball():
    # Each curved winding is itself made of the same three woven plies.
    wraps=[]
    for n,y in enumerate(range(-84,85,9)):
        curve=[((-82,y+20),(-35,y-28),(36,y-28),(82,y+20))]
        wraps.append(render(curve, f"ball-wrap-{n}"))
    cross=[]
    for n,x in enumerate(range(-38,39,9)):
        curve=[((x-38,-78),(x+38,-25),(x+38,25),(x-38,78))]
        cross.append(render(curve,f"ball-cross-{n}"))
    return ('<g transform="translate(1080 88) rotate(-20)"><defs>'
      '<clipPath id="yarn-ball-clip"><circle r="65"/></clipPath>'
      '<radialGradient id="yarn-ball-light" cx="30%" cy="25%" r="80%"><stop stop-color="#fff0d1" stop-opacity=".18"/><stop offset=".65" stop-color="#fff0d1" stop-opacity="0"/><stop offset="1" stop-color="#77351e" stop-opacity=".22"/></radialGradient></defs>'
      '<circle r="65" fill="#d87d4d"/><g clip-path="url(#yarn-ball-clip)"><g transform="rotate(-32)">'+''.join(wraps)+'</g><g transform="rotate(-20)">'+''.join(cross)+'</g></g>'
      '<circle r="65" fill="url(#yarn-ball-light)" stroke="#a55433" stroke-width="1.2"/></g>')
