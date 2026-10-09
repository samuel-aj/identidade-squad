# Gera os arquivos finais do logo a partir de <projeto>/marca.json. Rode de dentro de <projeto>/identidade/logo.
# Precisa: fonttools e uharfbuzz (ferramentas/instalar.sh) e o .ttf da fonte de título (baixado sozinho de
# fontes.titulo.ttf_url; se for fonte variável, cada trecho do nome vira uma instância estática com os eixos dele).
#
# O marca.json decide qual dos dois casos roda:
#
# 1) Marca COM símbolo (simbolo.pecas preenchido; exemplo completo: marca.exemplo.json, a AJ).
#    Gera símbolo em cada cor, assinaturas horizontal e vertical (símbolo + nome em curvas), ícone de app e favicon.
#    Campos de logo: assinatura_texto, peso, tracking, cores_simbolo, combinacoes {nome: [cor do símbolo, cor do texto]}.
#    Opcionais (sem eles, sai exatamente a assinatura da AJ: uma linha, centrada na caixa do símbolo):
#    linhas          o nome em uma ou mais linhas, cada uma com a própria instância da fonte (exemplo real:
#                    projetos/almeida-nascimento/marca.json):
#                    [{"texto": "Almeida Nascimento", "eixos": {"wght": 500, "opsz": 24}, "tracking": -0.005},
#                     {"texto": "Advocacia", "eixos": {"wght": 400, "opsz": 18}, "italico": true, "corpo": 0.76}]
#                    corpo = corpo da linha sobre o da primeira; italico pede fontes.titulo.ttf_url_italico.
#                    Linhas se alinham pela borda esquerda da TINTA (na vertical, pelo centro da tinta).
#    horizontal      {"proporcao": 2.7, "intervalo": 0.34}: proporcao = lado da caixa do símbolo / corpo da 1ª linha;
#                    intervalo = branco entre a tinta do símbolo e a do nome, em alturas do símbolo (altura da tinta).
#                    Alinhamento óptico: o topo da maiúscula da 1ª linha cai em simbolo.linhas_opticas.topo e a linha
#                    de base da última em simbolo.linhas_opticas.base (sem o campo: topo e pé da tinta); a entrelinha
#                    sai daí e vai para medidas.json. Com uma linha só, a maiúscula fica centrada entre as duas.
#    vertical        {"proporcao": 5.2, "intervalo": 0.3333}: símbolo centrado sobre as linhas; intervalo = do pé da tinta
#                    do símbolo ao topo da tinta da 1ª linha, em alturas do símbolo; entrelinha = a da horizontal.
#    combinacoes     também aceita {nome: {"simbolo": cor, "linhas": [cor, cor], "fundo": cor}}: cor de cada linha e o
#                    fundo de uso; o contraste do símbolo e de cada linha é medido no fundo (abaixo de contraste_minimo,
#                    padrão 3:1, a combinação NÃO é gerada e o motivo fica em medidas.json).
#    kerning_optico  o mesmo do caso 2 (abaixo), medido em cada linha; pares com espaço ficam fora.
#    icone           {"cor": c, "fundo": c, "raio": 0.2246, "caixa": 0.64, "pequeno": true,
#                     "favicon": {"lado": 16, "largura": 15, "raio": 3.5}, "variantes": {nome: {"cor": c, "fundo": c}}}
#                    ícone de app e favicon com o símbolo (a versão pequena, se pequeno); caixa = lado da caixa do
#                    símbolo sobre o lado do ícone. Favicon na grade: se simbolo.grade_pequeno {"x": x, "y": y} existir
#                    (uma vertical e uma horizontal da versão pequena, na caixa dela), as duas caem em pixel inteiro.
#                    Sem icone: o ícone da AJ (cor primária, e o escuro com luz).
#    Com linhas ou icone, escreve também medidas.json (corpos, proporção, entrelinha, alinhamento, contraste, kerning).
#
# 2) Marca SÓ TIPOGRÁFICA (simbolo null ou ausente): o nome é o logo. Campos de logo:
#    trechos         pedaços do nome, cada um com a própria instância da fonte variável:
#                    [{"texto": "Kleiciane", "eixos": {"wght": 600, "wdth": 100}, "tracking": -0.015}, ...]
#                    eixos = qualquer eixo do fvar (eixo omitido fica no padrão da fonte); tracking em em, só entre
#                    as letras do trecho. Na horizontal os trechos têm o mesmo corpo e a mesma linha de base, e o
#                    espaço entre eles é o caractere de espaço da própria fonte na instância do trecho anterior.
#    empilhado       {"vao": 0.34}: um trecho por linha; o corpo de cada linha é calculado para todas terem a mesma
#                    largura de TINTA (da primeira à última borda desenhada, não da caixa da letra); vao = distância
#                    da linha de base de cima ao topo da maiúscula de baixo, em alturas de maiúscula da linha de cima.
#    kerning_optico  {"profundidade": 0.15, "tolerancia": 0.10}: mede o branco de cada par de letras (área entre os
#                    perfis, com o fundo limitado a 15% da altura-x) e corrige só o par que foge mais de 10% da
#                    mediana do trecho, levando-o até a mediana. O kerning da fonte continua ligado.
#    extras          outras assinaturas na mesma construção (ex.: produto):
#                    [{"nome": "metodo-rocha", "trechos": [...], "formas": ["horizontal"]}]
#    combinacoes     {nome: {"cor": "ameixa", "sobre": ["rose-ar", "rose"]}}: cor do nome e os fundos onde ela vai.
#                    O contraste é medido em cada fundo; abaixo de contraste_minimo (padrão 3:1) a combinação NÃO é
#                    gerada, e o motivo fica em medidas.json.
#    icone           {"texto": "K", "eixos": {...}, "cor": "ameixa", "fundo": "rose", "altura": 0.625, "raio": 0.225}
#                    a letra que faz o papel de símbolo no ícone de app e no favicon; altura = altura da maiúscula
#                    sobre o lado do quadrado. O ícone de app usa os eixos da marca. O favicon é desenhado numa grade
#                    de 16: maiúscula, linha de base e borda da haste em pixel inteiro, e o peso recalculado para a
#                    haste medir pixels inteiros a 16 px (por ser grade, vale também a 32, 48, 192 e 512).
#    trechos[i].entrada, cenas   usados por video.js (ver o topo de video.js).
#    Unidade de todo SVG tipográfico: a altura da maiúscula do primeiro trecho vale 100; viewBox = caixa da tinta.
#    Saídas: assinatura/{horizontal,empilhado,<extra>}-<combinação>.svg, app/icone-app-marca.svg, favicon/favicon.svg,
#    movimento/geometria-entrada.json (para video.js) e medidas.json (corpos, larguras, kerning, contraste).
import json, os, io, sys, math, statistics, urllib.request
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.basePen import BasePen

AQUI = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(AQUI))
M = json.load(open(os.environ.get('MARCA_JSON', os.path.join(PROJ, 'marca.json'))))
S, L = M.get('simbolo') or None, M['logo']
CORES = {c['nome']: c['hex'] for c in M['cores']}
cor = lambda n: n if n.startswith('#') else CORES[n]
PAP = {k: cor(v) for k, v in M.get('papeis', {}).items()}

TTF = os.path.join(AQUI, 'fonte-titulo.ttf')
if not os.path.exists(TTF):
    urllib.request.urlretrieve(M['fontes']['titulo']['ttf_url'], TTF)
TTF_IT = os.path.join(AQUI, 'fonte-titulo-italico.ttf')
def _ttf(italico):
    """Arquivo da fonte: o itálico é baixado só quando algum trecho ou linha pede (fontes.titulo.ttf_url_italico)."""
    if not italico: return TTF
    if not os.path.exists(TTF_IT):
        url = M['fontes']['titulo'].get('ttf_url_italico')
        if not url: sys.exit('há trecho em itálico, mas falta fontes.titulo.ttf_url_italico no marca.json')
        urllib.request.urlretrieve(url, TTF_IT)
    return TTF_IT
_INST = {}
def fonte(eixos, italico=False):
    """Instância estática da fonte. eixos = {'wght': 600, 'wdth': 125} ou só o peso (número). Eixo omitido = padrão."""
    if not isinstance(eixos, dict): eixos = {'wght': eixos}
    k = (tuple(sorted(eixos.items())), bool(italico))
    if k not in _INST:
        f = TTFont(_ttf(italico))
        if 'fvar' in f: f = instantiateVariableFont(f, {a.axisTag: eixos.get(a.axisTag, a.defaultValue) for a in f['fvar'].axes})
        b = io.BytesIO(); f.save(b); _INST[k] = (f, b.getvalue())
    return _INST[k]
def texto_path(txt, w, size, x0, base, track):
    f, data = fonte(w); upm = f['head'].unitsPerEm
    face = hb.Face(data); font = hb.Font(face); buf = hb.Buffer(); buf.add_str(txt); buf.guess_segment_properties()
    hb.shape(font, buf, {'kern': True, 'liga': True})
    gs = f.getGlyphSet(); order = f.getGlyphOrder(); s = size / upm; x = 0; d = ''
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        pen = SVGPathPen(gs); gs[order[info.codepoint]].draw(TransformPen(pen, (s, 0, 0, -s, x0 + (x + pos.x_offset) * s, base)))
        d += pen.getCommands(); x += pos.x_advance + track * upm
    return d, (x - track * upm) * s, f['OS/2'].sCapHeight * s
def salva(nome, vb, corpo):
    os.makedirs(os.path.dirname(nome) or '.', exist_ok=True)
    open(f'{nome}.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{corpo}</svg>')

# ------------------------------------------------------------------------ ajudantes dos dois casos
def _num(v):
    t = ('%.2f' % v).rstrip('0').rstrip('.')
    return '0' if t in ('-0', '') else t
class _Caminho(BasePen):
    """Path SVG só com M, L, Q, C e Z: a mesma letra em duas instâncias dá a mesma sequência de comandos (video.js interpola)."""
    def __init__(s, gs): super().__init__(gs); s.c = []
    def _p(s, *ps): return ' '.join(f'{_num(x)} {_num(y)}' for x, y in ps)
    def _moveTo(s, p): s.c.append('M' + s._p(p))
    def _lineTo(s, p): s.c.append('L' + s._p(p))
    def _qCurveToOne(s, a, b): s.c.append('Q' + s._p(a, b))
    def _curveToOne(s, a, b, c): s.c.append('C' + s._p(a, b, c))
    def _closePath(s): s.c.append('Z')
    _endPath = _closePath
class _Linhas(BasePen):
    """Contorno achatado em retas: dá os cortes de cada linha horizontal (perfis, haste) e a área com sinal (centro de massa)."""
    def __init__(s, gs): super().__init__(gs); s.seg = []; s.p = s.ini = None
    def _moveTo(s, p): s.p = s.ini = p
    def _lineTo(s, p): s.seg.append((s.p, p)); s.p = p
    def _curva(s, f):
        for i in range(1, 17): q = f(i / 16); s.seg.append((s.p, q)); s.p = q
    def _qCurveToOne(s, a, b):
        p0 = s.p; s._curva(lambda t: tuple((1-t)**2 * p0[k] + 2*(1-t)*t * a[k] + t*t * b[k] for k in (0, 1)))
    def _curveToOne(s, a, b, c):
        p0 = s.p; s._curva(lambda t: tuple((1-t)**3 * p0[k] + 3*(1-t)**2*t * a[k] + 3*(1-t)*t*t * b[k] + t**3 * c[k] for k in (0, 1)))
    def _closePath(s):
        if s.p != s.ini: s.seg.append((s.p, s.ini))
        s.p = None
    _endPath = _closePath
    def cortes(s, y): return sorted(x0 + (y - y0) * (x1 - x0) / (y1 - y0) for (x0, y0), (x1, y1) in s.seg if (y0 <= y < y1) or (y1 <= y < y0))
def _lum(h):
    c = [int(h.lstrip('#')[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def contraste(a, b): la, lb = sorted((_lum(cor(a)), _lum(cor(b))), reverse=True); return round((la + 0.05) / (lb + 0.05), 2)

_MET = {}
def metr(eixos, italico=False):
    """Medidas da instância tiradas dos próprios desenhos: altura da maiúscula (topo do H), altura-x (topo do x), espaço."""
    k = (tuple(sorted(eixos.items())), bool(italico))
    if k not in _MET:
        f, _ = fonte(eixos, italico); gs = f.getGlyphSet(); cm = f.getBestCmap()
        def topo(ch, padrao):
            if ord(ch) not in cm: return padrao
            bp = BoundsPen(gs); gs[cm[ord(ch)]].draw(bp); return bp.bounds[3] if bp.bounds else padrao
        _MET[k] = dict(upm=f['head'].unitsPerEm, cap=topo('H', f['OS/2'].sCapHeight), xh=topo('x', f['OS/2'].sxHeight), espaco=f['hmtx'][cm[32]][0])
    return _MET[k]
def mt(tr): return metr(tr['eixos'], tr.get('italico'))
def corre(tr, ajustes=None):
    """Forma o trecho com HarfBuzz (kerning da fonte ligado). Devolve [(glifo, x, y, letra)] em unidades da fonte e o avanço."""
    f, data = fonte(tr['eixos'], tr.get('italico')); upm = f['head'].unitsPerEm; order = f.getGlyphOrder()
    font = hb.Font(hb.Face(data)); buf = hb.Buffer(); buf.add_str(tr['texto']); buf.guess_segment_properties()
    hb.shape(font, buf, {'kern': True, 'liga': True})
    n, x, out, track = len(buf.glyph_infos), 0, [], tr.get('tracking', 0) * upm
    for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        out.append((order[info.codepoint], x + pos.x_offset, pos.y_offset, tr['texto'][info.cluster]))
        x += pos.x_advance + ((track + (ajustes or {}).get(i, 0)) if i < n - 1 else 0)
    return out, x
def tinta(tr, ajustes=None):
    """Caixa da tinta do trecho, em unidades da fonte."""
    f, _ = fonte(tr['eixos'], tr.get('italico')); gs = f.getGlyphSet(); run, _ = corre(tr, ajustes); cx = []
    for g, x, y, _ in run:
        bp = BoundsPen(gs); gs[g].draw(bp)
        if bp.bounds: cx.append((bp.bounds[0] + x, bp.bounds[1] + y, bp.bounds[2] + x, bp.bounds[3] + y))
    return min(c[0] for c in cx), min(c[1] for c in cx), max(c[2] for c in cx), max(c[3] for c in cx)
def desenha(tr, ajustes, s, x0, base):
    """Trecho em curvas: s = unidades do logo por unidade da fonte; (x0, base) = origem e linha de base no logo."""
    f, _ = fonte(tr['eixos'], tr.get('italico')); gs = f.getGlyphSet(); run, _ = corre(tr, ajustes); d = ''
    for g, x, y, _ in run:
        pen = _Caminho(gs); gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x0 + x * s, base - y * s))); d += ''.join(pen.c)
    return d

def branco_do_par(gs, g1, x1, g2, x2, y0, y1, fundo):
    """Branco médio entre o perfil direito de g1 e o esquerdo de g2 na faixa y0..y1, com o fundo dos vãos limitado."""
    p1, p2 = _Linhas(gs), _Linhas(gs); gs[g1].draw(p1); gs[g2].draw(p2)
    ys = [y0 + (y1 - y0) * (k + .5) / 120 for k in range(120)]
    R = [(c[-1] + x1) if c else None for c in (p1.cortes(y) for y in ys)]
    E = [(c[0] + x2) if c else None for c in (p2.cortes(y) for y in ys)]
    mR, mE = max(r for r in R if r is not None), min(e for e in E if e is not None)
    return sum((mE + fundo if e is None else min(e, mE + fundo)) - (mR - fundo if r is None else max(r, mR - fundo)) for r, e in zip(R, E)) / len(ys)
def kerning_optico(tr):
    cfg = L.get('kerning_optico')
    if not cfg: return {}, []
    f, _ = fonte(tr['eixos'], tr.get('italico')); gs = f.getGlyphSet(); m = metr(tr['eixos'], tr.get('italico')); run, _ = corre(tr); pares = []
    for i, (a, b) in enumerate(zip(run, run[1:])):
        if a[3].isspace() or b[3].isspace(): continue   # par com espaço não tem branco entre letras para medir
        alta = a[3].isupper() and b[3].isupper()   # par de maiúsculas mede na altura da maiúscula; o resto, na altura-x
        pares.append([i, a[3] + b[3], branco_do_par(gs, a[0], a[1], b[0], b[1], 0, m['cap'] if alta else m['xh'], cfg.get('profundidade', .15) * m['xh'])])
    if not pares: return {}, []
    med = statistics.median(p[2] for p in pares); aj, rel = {}, []
    for i, par, area in pares:
        desvio = area / med - 1
        if abs(desvio) > cfg.get('tolerancia', .10): aj[i] = round(med - area)
        rel.append({'par': par, 'branco': round(area, 1), 'mediana': round(med, 1), 'desvio': round(desvio, 3), 'ajuste_em': round(aj.get(i, 0) / m['upm'], 3)})
    return aj, rel

MED = {'modo': 'simbolo' if S else 'tipografico', 'kerning': {}, 'contraste': {}, 'nao_gerados': [], 'assinaturas': {}}
_AJ = {}
def ajustes(tr):
    k = (tr['texto'], tuple(sorted(tr['eixos'].items())), tr.get('tracking', 0), bool(tr.get('italico')))
    if k not in _AJ:
        _AJ[k], rel = kerning_optico(tr)
        if rel: MED['kerning'][tr['texto']] = rel
    return _AJ[k]
def _caixa(partes):
    """partes = [(trecho, s, x0, base)] -> lista das caixas de tinta no logo e a caixa total."""
    cx = []
    for tr, s, x0, base in partes:
        b = tinta(tr, ajustes(tr)); cx.append((x0 + b[0] * s, base - b[3] * s, x0 + b[2] * s, base - b[1] * s))
    return cx, (min(c[0] for c in cx), min(c[1] for c in cx), max(c[2] for c in cx), max(c[3] for c in cx))
def _monta(partes):
    cxs, (X0, Y0, X1, Y1) = _caixa(partes)
    ds = [desenha(tr, ajustes(tr), s, x0 - X0, base - Y0) for tr, s, x0, base in partes]
    return f'0 0 {_num(X1 - X0)} {_num(Y1 - Y0)}', ds, (X0, Y0), cxs
def linha(trechos, nome, eixos_de=None):
    """Horizontal: mesmo corpo, mesma base; espaço = caractere de espaço da instância do trecho anterior.
    eixos_de (para video.js): desenha cada trecho também com outros eixos, com a origem no mesmo lugar."""
    s = 100 / mt(trechos[0])['cap']; x = 0; partes = []
    for i, tr in enumerate(trechos):
        if i: x += mt(trechos[i - 1])['espaco'] * s
        partes.append((tr, s, x, 0)); x += corre(tr, ajustes(tr))[1] * s
    vb, ds, (X0, Y0), cxs = _monta(partes)
    em = s * mt(trechos[0])['upm']
    MED['assinaturas'][nome] = {'viewBox': vb, 'corpo': round(em, 3),
        'espaco_entre_trechos_em': [round(mt(t)['espaco'] / mt(t)['upm'], 3) for t in trechos[:-1]],
        'vao_de_tinta_entre_trechos_em': [round((b[0] - a[2]) / em, 3) for a, b in zip(cxs, cxs[1:])]}
    if eixos_de:
        ini = [desenha(dict(tr, eixos={**tr['eixos'], **(eixos_de[i] or {})}), ajustes(tr), s, x0 - X0, b - Y0) for i, (tr, s, x0, b) in enumerate(partes)]
        return vb, ds, ini
    return vb, ds
def empilhado(trechos, nome, vao):
    """Um trecho por linha, todas com a mesma largura de tinta; vão em alturas de maiúscula da linha de cima."""
    s0 = 100 / mt(trechos[0])['cap']
    larg = [(lambda b: b[2] - b[0])(tinta(t, ajustes(t))) for t in trechos]; W = larg[0] * s0
    y = 0; partes = []; corpos = []; capant = 0
    for i, tr in enumerate(trechos):
        s = W / larg[i]; cap = mt(tr)['cap'] * s
        if i: y += vao * capant
        base = y + cap; partes.append((tr, s, -tinta(tr, ajustes(tr))[0] * s, base)); y = base; capant = cap
        corpos.append(round(s * mt(tr)['upm'], 3))
    vb, ds, _, cxs = _monta(partes)
    MED['assinaturas'][nome] = {'viewBox': vb, 'corpos': corpos, 'razao_dos_corpos': round(corpos[-1] / corpos[0], 4), 'largura_de_tinta': round(W, 3),
        'maior_diferenca_de_largura': max(abs((c[2] - c[0]) - W) for c in cxs), 'vao_em_maiusculas': vao}
    return vb, ds

if S:  # ---------------------------------------------------------------- caso 1: marca com símbolo
    VB = S.get('viewBox', '0 0 100 100'); _, _, VW, VH = map(float, VB.split())
    PECAS, PEQ = S['pecas'], S.get('pequeno') or S['pecas']
    def simb(c, tx=0, ty=0, k=1, peq=False):
        k = k * 100 / max(VW, VH)   # normaliza o símbolo para uma caixa de 100
        return f'<g transform="translate({tx:.2f} {ty:.2f}) scale({k:.4f})" fill="{c}">' + ''.join(f'<path d="{p}"/>' for p in (PEQ if peq else PECAS)) + '</g>'

    r3 = lambda x: round(x, 3)
    # 1) símbolo em cada cor
    for n, c in L['cores_simbolo'].items():
        salva(f'simbolo/simbolo-{n}', '0 0 100 100', simb(cor(c)))
        salva(f'simbolo/simbolo-pequeno-{n}', '0 0 100 100', simb(cor(c), peq=True))
    # 2) assinaturas (texto em curvas)
    if not L.get('linhas'):   # a assinatura da AJ: uma linha, centrada na caixa do símbolo
        NOME, PESO, TR = L['assinatura_texto'], L.get('peso', 400), L.get('tracking', -0.03)
        def horizontal(cs, ct):
            H = 100; size = 0.72 * H; x0 = H + 0.30 * H
            _, _, cap = texto_path(NOME, PESO, size, x0, 0, TR)
            d, w, _ = texto_path(NOME, PESO, size, x0, H / 2 + cap / 2, TR)
            return f'0 0 {x0 + w:.1f} {H}', simb(cs) + f'<path fill="{ct}" d="{d}"/>'
        def vertical(cs, ct):
            H = 100; size = 0.34 * H
            _, w, cap = texto_path(NOME, PESO, size, 0, 0, TR)
            W = max(w, H); base = H + 0.30 * H + cap
            d, w, _ = texto_path(NOME, PESO, size, (W - w) / 2, base, TR)
            return f'0 0 {W:.1f} {base + size * 0.28:.1f}', simb(cs, (W - H) / 2, 0) + f'<path fill="{ct}" d="{d}"/>'
        for n, (cs, ct) in L['combinacoes'].items():
            vb, b = horizontal(cor(cs), cor(ct)); salva(f'assinatura/horizontal-{n}', vb, b)
            vb, b = vertical(cor(cs), cor(ct)); salva(f'assinatura/vertical-{n}', vb, b)
    else:                     # o nome em linhas, com alinhamento óptico ao símbolo
        from fontTools.svgLib.path import parse_path
        kS = 100 / max(VW, VH)
        def caixa_d(ds):
            bp = BoundsPen(None)
            for d in ds: parse_path(d, bp)
            return [v * kS for v in bp.bounds]
        sx0, sy0, sx1, sy1 = caixa_d(PECAS)
        HT = sy1 - sy0                                   # altura do símbolo = altura da tinta
        OPT = S.get('linhas_opticas') or {}
        TOPO, BASE = OPT.get('topo', sy0 / kS) * kS, OPT.get('base', sy1 / kS) * kS
        LIN = L['linhas']; n = len(LIN)
        corpos = lambda c: [c * tr.get('corpo', 1) for tr in LIN]
        def linhas_em(c, G, base1, x_tinta):
            """[(linha, s, x0, base)]: a linha i com a base em base1 + i*G e a tinta começando em x_tinta(largura da tinta)."""
            partes = []
            for i, (tr, cp) in enumerate(zip(LIN, corpos(c))):
                s = cp / mt(tr)['upm']; b = tinta(tr, ajustes(tr))
                partes.append((tr, s, x_tinta((b[2] - b[0]) * s) - b[0] * s, base1 + i * G))
            return partes
        def caixas(partes):
            out = []
            for tr, s, x0, base in partes:
                b = tinta(tr, ajustes(tr)); out.append((x0 + b[0] * s, base - b[3] * s, x0 + b[2] * s, base - b[1] * s))
            return out
        def monta(partes, cs, cls):
            """Símbolo na origem + linhas; viewBox = caixa da tinta do conjunto."""
            cx = caixas(partes) + [(sx0, sy0, sx1, sy1)]
            X0, Y0 = min(c_[0] for c_ in cx), min(c_[1] for c_ in cx); X1, Y1 = max(c_[2] for c_ in cx), max(c_[3] for c_ in cx)
            corpo = simb(cs, -X0, -Y0) + ''.join(f'<path fill="{cls[min(i, len(cls) - 1)]}" d="{desenha(tr, ajustes(tr), s, x0 - X0, base - Y0)}"/>'
                                               for i, (tr, s, x0, base) in enumerate(partes))
            return f'0 0 {_num(X1 - X0)} {_num(Y1 - Y0)}', corpo, (X0, Y0, X1, Y1), cx
        HZ, VT = L.get('horizontal', {}), L.get('vertical', {})
        # horizontal: maiúscula da 1ª linha no topo óptico do símbolo, linha de base da última na base óptica
        c = 100 / HZ.get('proporcao', 2.7)
        cap1 = mt(LIN[0])['cap'] * c / mt(LIN[0])['upm']
        if n > 1: base1 = TOPO + cap1; G = (BASE - base1) / (n - 1)
        else: base1 = (TOPO + BASE + cap1) / 2; G = 0
        if n > 1 and G <= cap1 * .5: sys.exit(f'horizontal.proporcao {HZ.get("proporcao", 2.7)} deixa a entrelinha em {G / c:.2f} em: as linhas se tocam')
        xt = sx1 + HZ.get('intervalo', .37) * HT
        PH = linhas_em(c, G, base1, lambda w: xt)
        # vertical: símbolo centrado sobre as linhas, mesma entrelinha (em em) da horizontal
        cv = 100 / VT.get('proporcao', 5)
        Gv = VT.get('entrelinha', G / c if n > 1 else 1.25) * cv
        topo_tinta1 = tinta(LIN[0], ajustes(LIN[0]))[3] * cv / mt(LIN[0])['upm']
        eixo = (sx0 + sx1) / 2
        PV = linhas_em(cv, Gv, sy1 + VT.get('intervalo', 1 / 3) * HT + topo_tinta1, lambda w: eixo - w / 2)
        MIN = L.get('contraste_minimo', 3)
        for nc, v in L['combinacoes'].items():
            if isinstance(v, dict):
                cs = v['simbolo']; cls = v.get('linhas', cs); cls = cls if isinstance(cls, list) else [cls]
                cls = [cls[min(i, len(cls) - 1)] for i in range(n)]
                if v.get('fundo'):
                    med = {'simbolo': contraste(cs, v['fundo']), **{f'linha {i + 1}': contraste(x, v['fundo']) for i, x in enumerate(cls)}}
                    MED['contraste'][nc] = dict(fundo=v['fundo'], **med)
                    falha = {k_: r_ for k_, r_ in med.items() if r_ < MIN}
                    if falha:
                        MED['nao_gerados'].append({'combinacao': nc, 'motivo': f'contraste abaixo de {MIN}:1', 'medido': falha})
                        print(f'não gerado: {nc} (medido {falha}, mínimo {MIN}:1)'); continue
            else: cs, ct = v; cls = [ct]
            cs, cls = cor(cs), [cor(x) for x in cls]
            for forma, partes in (('horizontal', PH), ('vertical', PV)):
                vb, b, _, _ = monta(partes, cs, cls); salva(f'assinatura/{forma}-{nc}', vb, b)
        MED['simbolo'] = {'unidade': 'caixa do símbolo = 100', 'tinta': [r3(x) for x in (sx0, sy0, sx1, sy1)], 'altura': r3(HT),
                          'largura': r3(sx1 - sx0), 'linhas_opticas': {'topo': r3(TOPO), 'base': r3(BASE)}}
        vb, _, (X0, Y0, X1, Y1), cxh = monta(PH, '#000', ['#000'])
        MED['assinaturas']['horizontal'] = {'viewBox': vb, 'unidade': 'caixa do símbolo = 100', 'corpo': r3(c), 'corpos': [r3(x) for x in corpos(c)],
            'proporcao': {'caixa_do_simbolo_sobre_corpo': r3(100 / c), 'altura_do_simbolo_sobre_corpo': r3(HT / c)},
            'entrelinha_em': r3(G / c) if n > 1 else None,
            'intervalo': {'alturas_do_simbolo': HZ.get('intervalo', .37), 'corpos': r3((xt - sx1) / c), 'unidades': r3(xt - sx1)},
            'alinhamento': {'topo_do_simbolo': r3(TOPO), 'topo_da_maiuscula_1a_linha': r3(base1 - cap1),
                            'base_do_simbolo': r3(BASE), 'linha_de_base_da_ultima': r3(base1 + (n - 1) * G)},
            'tinta_das_linhas': [[r3(x) for x in b_] for b_ in cxh[:-1]],
            'altura_sobre_altura_do_simbolo': r3((Y1 - Y0) / HT), 'largura_sobre_altura': r3((X1 - X0) / (Y1 - Y0))}
        vb, _, (X0, Y0, X1, Y1), cxv = monta(PV, '#000', ['#000'])
        MED['assinaturas']['vertical'] = {'viewBox': vb, 'corpo': r3(cv), 'corpos': [r3(x) for x in corpos(cv)],
            'proporcao': {'caixa_do_simbolo_sobre_corpo': r3(100 / cv), 'altura_do_simbolo_sobre_corpo': r3(HT / cv)},
            'entrelinha_em': r3(Gv / cv), 'intervalo': {'alturas_do_simbolo': VT.get('intervalo', 1 / 3), 'unidades': r3(cxv[0][1] - sy1)},
            'largura_da_1a_linha_sobre_largura_do_simbolo': r3((cxv[0][2] - cxv[0][0]) / (sx1 - sx0)),
            'largura_sobre_altura': r3((X1 - X0) / (Y1 - Y0))}
        f_ = L.get('respiro_fracao', 1 / 3)
        MED['respiro'] = {'alturas_do_simbolo': r3(f_), 'unidades': r3(f_ * HT), 'corpos_da_horizontal': r3(f_ * HT / c)}
        MN = L.get('minimos')
        if MN:
            MED['minimos'] = dict(MN)
            if MN.get('menor_corpo_px'):   # a assinatura não desce abaixo do corpo mínimo da menor linha
                for forma, cc in (('horizontal', c), ('vertical', cv)):
                    px = MN['menor_corpo_px'] / min(corpos(cc)); a_ = MED['assinaturas'][forma]['viewBox'].split()
                    MED['minimos'][f'{forma}_px'] = {'largura': r3(float(a_[2]) * px), 'altura': r3(float(a_[3]) * px), 'caixa_do_simbolo': r3(100 * px)}
                    if 100 * px < MN.get('simbolo_px', 0): print(f'AVISO: no mínimo da {forma}, o símbolo fica com {100 * px:.1f} px (abaixo de {MN["simbolo_px"]})')
    # 3) ícone de app e favicon
    if not L.get('icone'):    # o da AJ: cor primária, e o escuro com luz
        salva('app/icone-app-marca', '0 0 1024 1024', f'<rect width="1024" height="1024" rx="230" fill="{PAP["primaria"]}"/>' + simb('#FFFFFF', 230, 230, 5.64))
        luz = (f'<defs><radialGradient id="f" cx=".3" cy=".08" r=".95"><stop offset="0" stop-color="{PAP.get("escuro_claro", PAP["escuro"])}"/><stop offset="1" stop-color="{PAP["escuro"]}"/></radialGradient>'
               f'<filter id="l" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur in="SourceAlpha" stdDeviation="3.2"/><feFlood flood-color="{PAP["primaria"]}" flood-opacity=".85"/><feComposite operator="in" in2="SourceAlpha"/><feGaussianBlur stdDeviation="2.4" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')
        salva('app/icone-app-escuro', '0 0 1024 1024', luz + f'<rect width="1024" height="1024" rx="230" fill="url(#f)"/><g filter="url(#l)">' + simb(PAP.get('realce_claro', '#FFFFFF'), 230, 230, 5.64) + '</g>')
        salva('favicon/favicon', '0 0 100 100', f'<rect width="100" height="100" rx="22" fill="{PAP["primaria"]}"/>' + simb('#FFFFFF', 18, 18, .64, peq=True))
    else:                     # ícone e favicon com o símbolo, nas cores pedidas, sem luz
        IC = L['icone']; peq = IC.get('pequeno', True); kS = 100 / max(VW, VH)
        def grupo(c_, tx, ty, k_):
            return f'<g transform="translate({tx:.4f} {ty:.4f}) scale({k_ * kS:.5f})" fill="{c_}">' + ''.join(f'<path d="{p}"/>' for p in (PEQ if peq else PECAS)) + '</g>'
        r = IC.get('raio', .225); a = IC.get('caixa', .64) * 1024 / 100
        FV = IC.get('favicon', {}); lado = FV.get('lado', 16); larg = FV.get('largura', lado - 1); rf = FV.get('raio', lado * r)
        af = larg / 100; bx = (lado - larg) / 2; by = lado / 2 - af * 50
        GR = S.get('grade_pequeno') if peq else S.get('grade')
        if GR:   # a vertical e a horizontal pedidas caem em pixel inteiro (vale para 32, 48... por ser grade)
            X = af * GR['x'] * kS + bx; bx += round(X) - X
            Y = af * GR['y'] * kS + by; by += round(Y) - Y
        MED['icone'] = {'versao': 'pequeno' if peq else 'completo', 'app': {'lado': 1024, 'raio': round(1024 * r, 3), 'escala': round(a, 4)},
                        'favicon': {'lado': lado, 'largura': larg, 'raio': rf, 'translate': [round(bx, 4), round(by, 4)], 'escala': af, 'grade': GR}, 'contraste': {}}
        for ni, v in [('marca', IC)] + list(IC.get('variantes', {}).items()):
            MED['icone']['contraste'][ni] = {v['fundo']: contraste(v['cor'], v['fundo'])}
            suf = '' if ni == 'marca' else f'-{ni}'
            salva(f'app/icone-app-{ni}', '0 0 1024 1024', f'<rect width="1024" height="1024" rx="{_num(1024 * r)}" fill="{cor(v["fundo"])}"/>' + grupo(cor(v['cor']), 512 - 50 * a, 512 - 50 * a, a))
            salva(f'favicon/favicon{suf}', f'0 0 {lado} {lado}', f'<rect width="{lado}" height="{lado}" rx="{_num(rf)}" fill="{cor(v["fundo"])}"/>' + grupo(cor(v['cor']), bx, by, af))
    if L.get('linhas') or L.get('icone'): json.dump(MED, open('medidas.json', 'w'), ensure_ascii=False, indent=1)
    print('svgs ok')
    sys.exit(0)

# 1) combinações: mede o contraste antes de gerar
MIN = L.get('contraste_minimo', 3)
COMB = {}
for n, c in L['combinacoes'].items():
    med = {f: contraste(c['cor'], f) for f in c.get('sobre', [])}; MED['contraste'][n] = med
    falha = {f: r for f, r in med.items() if r < MIN}
    if falha:
        MED['nao_gerados'].append({'combinacao': n, 'motivo': f'contraste abaixo de {MIN}:1', 'medido': falha})
        print(f'não gerado: {n} (medido {falha}, mínimo {MIN}:1)')
    else: COMB[n] = cor(c['cor'])
# 2) assinaturas em curvas
ASS = [('horizontal', L['trechos'], ['horizontal'] + (['empilhado'] if L.get('empilhado') else []))]
ASS += [(e['nome'], e['trechos'], e.get('formas', ['horizontal'])) for e in L.get('extras', [])]
for nome, trs, formas in ASS:
    for forma in formas:
        chave = forma if nome == 'horizontal' else (nome if forma == 'horizontal' else f'{nome}-{forma}')
        vb, ds = linha(trs, chave) if forma == 'horizontal' else empilhado(trs, chave, L['empilhado']['vao'])
        for n, hexa in COMB.items():
            salva(f'assinatura/{chave}-{n}', vb, ''.join(f'<path fill="{hexa}" d="{d}"/>' for d in ds))
# 3) ícone de app e favicon: uma letra no lugar do símbolo
def letra(ic, eixos, lado, grade=False):
    f, _ = fonte(eixos); gs = f.getGlyphSet(); m = metr(eixos); g = corre({'texto': ic['texto'], 'eixos': eixos})[0][0][0]
    alt = lado * ic.get('altura', .625); k = (round(alt) if grade else alt) / m['cap']
    p = _Linhas(gs); gs[g].draw(p); bp = BoundsPen(gs); gs[g].draw(bp); b = bp.bounds
    A = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in p.seg) / 2
    cm = sum((x0 + x1) * (x0 * y1 - x1 * y0) for (x0, y0), (x1, y1) in p.seg) / (6 * A)   # centro de massa da letra
    x = lado / 2 - ((b[0] + b[2]) / 2 + cm) / 2 * k                                       # meio caminho entre caixa e massa
    ys = [m['cap'] * (.15 + .7 * i / 40) for i in range(41)]
    haste = min((c[1] - c[0], c[0]) for c in (p.cortes(y) for y in ys) if len(c) >= 2)    # a menor primeira mancha de tinta
    topo = (lado - m['cap'] * k) / 2
    if grade: x = round(x + haste[1] * k) - haste[1] * k; topo = math.floor(topo)
    d = desenha({'texto': ic['texto'], 'eixos': eixos}, {}, k, x, topo + m['cap'] * k)
    return d, {'eixos': dict(eixos), 'altura_maiuscula': round(m['cap'] * k, 3), 'haste': round(haste[0] * k, 3), 'borda_da_haste': round(x + haste[1] * k, 3), 'topo': round(topo, 3)}
IC = L.get('icone')
if IC:
    MED['contraste']['icone'] = {IC['fundo']: contraste(IC['cor'], IC['fundo'])}
    if MED['contraste']['icone'][IC['fundo']] < MIN: print(f'AVISO: ícone com contraste {MED["contraste"]["icone"]} abaixo de {MIN}:1')
    r = IC.get('raio', .225); d, info = letra(IC, IC['eixos'], 1024)
    salva('app/icone-app-marca', '0 0 1024 1024', f'<rect width="1024" height="1024" rx="{_num(1024 * r)}" fill="{cor(IC["fundo"])}"/><path fill="{cor(IC["cor"])}" d="{d}"/>')
    MED['icone_app'] = info
    # favicon na grade de 16: procura o peso que põe a haste em pixel inteiro
    eix = dict(IC['eixos']); _, inf = letra(IC, eix, 16, grade=True); alvo = max(1, round(inf['haste']))
    fv = TTFont(TTF); ax = {a.axisTag: a for a in fv['fvar'].axes} if 'fvar' in fv else {}
    if 'wght' in ax and abs(inf['haste'] - alvo) > .02:
        lo, hi = ax['wght'].minValue, ax['wght'].maxValue
        for _ in range(16):
            meio = (lo + hi) / 2; eix['wght'] = round(meio, 1); _, inf = letra(IC, eix, 16, grade=True)
            if abs(inf['haste'] - alvo) <= .02: break
            lo, hi = (meio, hi) if inf['haste'] < alvo else (lo, meio)
    d, info = letra(IC, eix, 16, grade=True)
    salva('favicon/favicon', '0 0 16 16', f'<rect width="16" height="16" rx="{_num(16 * r)}" fill="{cor(IC["fundo"])}"/><path fill="{cor(IC["cor"])}" d="{d}"/>')
    MED['favicon'] = dict(info, haste_alvo=alvo, peso_da_marca=IC['eixos'].get('wght'), unidade='px a 16 px')
# 4) geometria da entrada animada (video.js): cada trecho no lugar final e, se pedir, nos eixos de partida
ent = [t.get('entrada', {}) for t in L['trechos']]
vb, fim, ini = linha(L['trechos'], 'horizontal', eixos_de=[e.get('eixos') for e in ent])
for i, (a, b) in enumerate(zip(ini, fim)):
    if [c for c in a if c.isalpha()] != [c for c in b if c.isalpha()]: sys.exit(f'trecho {i}: início e fim com comandos diferentes; não dá para interpolar')
os.makedirs('movimento', exist_ok=True)
json.dump({'viewBox': vb, 'trechos': [{'texto': t['texto'], 'inicio': a, 'fim': b, 'de': e.get('de', [0, 0]), 'atraso': e.get('atraso', 0)}
           for t, a, b, e in zip(L['trechos'], ini, fim, ent)]}, open('movimento/geometria-entrada.json', 'w'), ensure_ascii=False)
json.dump(MED, open('medidas.json', 'w'), ensure_ascii=False, indent=1)
print('svgs ok (só tipografia):', ', '.join(f'{k} {v["viewBox"]}' for k, v in MED['assinaturas'].items()))
