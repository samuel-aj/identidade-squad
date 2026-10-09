# Confere o contraste de todos os pares de tokens que a interface usa, nos dois temas. Sai com erro se algum falhar.
# Pares próprios da marca (ex.: a palavra de ênfase sobre a moldura) entram em `contraste_extra` no marca.json:
# [["enfase", "moldura", 3, "só letra grande"], ...] — cada lado é um token semântico, uma cor da marca ou um hex.
# Distâncias mínimas de cor entre dois tokens (ex.: o crítico não pode parecer a ênfase) entram em `distancia_extra`:
# [["critico", "enfase", 20, "motivo"], ...] — ΔE CIELAB 1976, medida nos dois temas.
# Croma máximo de um token (ex.: a cor de dados do escuro não pode ler como dourado) entra em `croma_maximo`:
# [["dado-2", 40, "escuro", "motivo"], ...] — croma CIELAB (LCh), no tema dado ("claro", "escuro" ou "ambos").
# Uso: python3 contraste.py [<projeto>/marca.json]
import json, os, sys
M = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'marca.json'))
cor = {c['nome']: c['hex'] for c in M['cores']}; sem = {s['nome']: s for s in M['semanticos']}
def r(v, t):
    while v.startswith('{'):
        n = v[1:-1]; v = cor[n] if n in cor else sem[n][t]
    return v
def lum(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def razao(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)
CHAOS = ['fundo', 'superficie', 'superficie-2']
PARES = [(t, c, 4.5) for t in ('texto', 'texto-2', 'texto-3') for c in CHAOS] + [
    ('sobre-acao', 'acao', 4.5), ('sobre-acao', 'acao-hover', 4.5), ('sobre-realce', 'realce', 4.5),
    ('acao', 'fundo', 3), ('acao', 'superficie', 3), ('foco', 'fundo', 3), ('foco', 'superficie', 3),
    ('borda-controle', 'superficie', 3),
    ('sucesso', 'superficie', 4.5), ('sucesso', 'sucesso-fundo', 4.5), ('atencao', 'superficie', 4.5), ('atencao', 'atencao-fundo', 4.5),
    ('critico', 'superficie', 4.5), ('critico', 'critico-fundo', 4.5), ('dado-1', 'superficie', 3), ('dado-2', 'superficie', 3)]
PARES += [tuple(p[:3]) for p in M.get('contraste_extra', [])]
def val(n, t): return n if n.startswith('#') else (sem[n][t] if n in sem else '{' + n + '}')
falhas = 0
for tema in ('claro', 'escuro'):
    print(f'\n## {tema}')
    for a, b, minimo in PARES:
        ha, hb = r(val(a, tema), tema), r(val(b, tema), tema)
        if not (ha.startswith('#') and hb.startswith('#')): continue
        x = razao(ha, hb); ok = x >= minimo; falhas += not ok
        print(f"{'ok  ' if ok else 'FALHA'} {a:15} sobre {b:14} {x:5.2f}:1 (mínimo {minimo}:1)")
def lab(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    r, g, b = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    X = (0.4124564*r + 0.3575761*g + 0.1804375*b) / 0.95047; Y = 0.2126729*r + 0.7151522*g + 0.0721750*b; Z = (0.0193339*r + 0.1191920*g + 0.9503041*b) / 1.08883
    f = lambda t: t ** (1/3) if t > 0.008856 else 7.787 * t + 16 / 116
    return (116 * f(Y) - 16, 500 * (f(X) - f(Y)), 200 * (f(Y) - f(Z)))
if M.get('distancia_extra'):
    for tema in ('claro', 'escuro'):
        print(f'\n## distância de cor, {tema} (ΔE CIELAB)')
        for a, b, minimo, *nota in M['distancia_extra']:
            ha, hb = r(val(a, tema), tema), r(val(b, tema), tema)
            if not (ha.startswith('#') and hb.startswith('#')): continue
            d = sum((x - y) ** 2 for x, y in zip(lab(ha), lab(hb))) ** .5; ok = d >= minimo; falhas += not ok
            print(f"{'ok  ' if ok else 'FALHA'} {a:15} e {b:16} ΔE {d:5.1f} (mínimo {minimo}){'  ' + nota[0] if nota else ''}")
if M.get('croma_maximo'):
    print('\n## croma máximo (CIELAB)')
    for n, maximo, tema_c, *nota in M['croma_maximo']:
        for tema in (('claro', 'escuro') if tema_c == 'ambos' else (tema_c,)):
            h = r(val(n, tema), tema)
            if not h.startswith('#'): continue
            L, a_, b_ = lab(h); c = (a_ ** 2 + b_ ** 2) ** .5; ok = c <= maximo; falhas += not ok
            print(f"{'ok  ' if ok else 'FALHA'} {n:15} {tema:7} {h} croma {c:5.1f} (máximo {maximo}){'  ' + nota[0] if nota else ''}")
print(f'\n{falhas} par(es) abaixo do mínimo.' if falhas else '\nTodos os pares passam.')
sys.exit(1 if falhas else 0)
