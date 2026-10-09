import math, json
def fillet(pts, radii):
    """polígono fechado com raio por vértice -> path SVG com arcos de concordância"""
    n=len(pts); out=[]
    for i in range(n):
        p0,p1,p2=pts[i-1],pts[i],pts[(i+1)%n]; r=radii[i]
        if r==0: out.append(('L',p1)); continue
        v1=(p0[0]-p1[0],p0[1]-p1[1]); v2=(p2[0]-p1[0],p2[1]-p1[1])
        l1=math.hypot(*v1); l2=math.hypot(*v2)
        u1=(v1[0]/l1,v1[1]/l1); u2=(v2[0]/l2,v2[1]/l2)
        ang=math.acos(max(-1,min(1,u1[0]*u2[0]+u1[1]*u2[1])))
        t=r/math.tan(ang/2); t=min(t,l1*.49,l2*.49); r=t*math.tan(ang/2)
        a=(p1[0]+u1[0]*t,p1[1]+u1[1]*t); b=(p1[0]+u2[0]*t,p1[1]+u2[1]*t)
        cross=u1[0]*u2[1]-u1[1]*u2[0]
        out.append(('L',a)); out.append(('A',r,0 if cross>0 else 1,b))
    d=''
    for k,c in enumerate(out):
        if c[0]=='L': d+=('M' if k==0 else 'L')+f'{c[1][0]:.2f} {c[1][1]:.2f} '
        else: d+=f'A{c[1]:.2f} {c[1]:.2f} 0 0 {c[2]} {c[3][0]:.2f} {c[3][1]:.2f} '
    if out[0][0]=='A': d='M'+f'{out[-1][3][0] if out[-1][0]=="A" else out[-1][1][0]:.2f} 0 '+d
    return d+'Z'
# A0 atual: telhado/diagonal + haste + gancho
A0=[(4,78),(52,6),(82,6),(82,100),(34,100),(34,84),(66,84),(66,22),(60,22),(24,78)]
V={}
V['atual']=[fillet(A0,[0,0,0,26,0,0,10,0,0,0])]
V['macio']=[fillet(A0,[2.5,5,6,30,2.5,2.5,12,3,3,2.5])]
# dobra: corte em meia-esquadria a 45° de (82,6) até (66,22), com fresta g
g=2.6; h=g/math.sqrt(2)
tel=[(4,78),(52,6),(82-2*h,6),(66-2*h+0.0,22),(60,22),(24,78)]
tel=[(4,78),(52,6),(82-g*math.sqrt(2),6),(66,22+0)] 
# linha de dobra x+y=88; telhado fica do lado x+y<88-g', haste do lado x+y>88+g'
gp=g/2*math.sqrt(2)
tel=[(4,78),(52,6),(82-gp,6),(66-gp,22),(60,22),(24,78)]
has=[(82,6+gp),(82,100),(34,100),(34,84),(66,84),(66,22+gp)]
V['dobra']=[fillet(tel,[2.5,5,1,1,3,2.5]),fillet(has,[1,30,2.5,2.5,12,1])]
json.dump(V,open('variantes.json','w'),indent=1)
for k,ps in V.items():
    open(f'{k}.svg','w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'+''.join(f'<path fill="#5B2BE0" d="{d}"/>' for d in ps)+'</svg>')
print(open('dobra.svg').read())
