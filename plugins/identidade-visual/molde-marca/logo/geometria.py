# Biblioteca de geometria do símbolo. O símbolo é gerado por script a partir de pontos e raios, nunca desenhado à mão:
# assim toda variante, tamanho pequeno e animação sai da mesma fonte. Exemplo completo: gera_exemplo_aj.py (símbolo A2 Dobra da AJ).
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

def gira(pts, graus, cx=50, cy=50):
    a = math.radians(graus); c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]
def espelha(pts, eixo_x=50):
    return [(2 * eixo_x - x, y) for x, y in pts][::-1]
def grava(variantes, arquivo='variantes.json'):
    """variantes = {"nome": [path, path, ...]}. O marca.json aponta a escolhida em simbolo.pecas."""
    json.dump(variantes, open(arquivo, 'w'), indent=1)
