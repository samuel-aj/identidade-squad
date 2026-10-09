# Fonte única dos tokens da marca. Tudo (tokens.json, CSS, pontes, componentes, skill) sai daqui.
# Os valores vêm de <projeto>/marca.json; o que é regra de sistema (espaço, raio, camadas...) tem padrão aqui
# e pode ser trocado no marca.json. Não edite os arquivos gerados: edite o marca.json e regenere.
import json, os, re
AQUI = os.path.dirname(os.path.abspath(__file__))
INTERFACE = os.path.dirname(AQUI)
PROJETO = os.path.dirname(INTERFACE)
DS = os.path.join(INTERFACE, 'design-system', 'project')
M = json.load(open(os.environ.get('MARCA_JSON', os.path.join(PROJETO, 'marca.json'))))
P = M['prefixo']

MARCA = [(c['nome'], c['hex'], c['hex'], c['uso']) for c in M['cores']]
SEM = [(s['nome'], s['claro'], s['escuro'], s['uso']) for s in M['semanticos']]
ESCALA = [(p['nome'], p['hex']) for p in M['escala']['passos']]
TIPO = M['tipo']

# Dois interruptores da marca (LEIA-ME, "Marca só tipográfica e marca sem luz"):
# `simbolo: null` = marca só tipográfica. O logotipo (o nome em curvas, de identidade/logo/assinatura/) faz o papel
#   do símbolo nos componentes, e o token `logotipo` substitui o token `simbolo`.
# `luz: false` = a marca não tem halo nem brilho. Os tokens halo-1, halo-2 e brilho deixam de ser obrigatórios e as
#   classes de luz saem do CSS e das prévias. Sem o campo `luz`, vale o padrão (com luz, como na AJ).
SIMBOLO = M.get('simbolo') or None
LUZ = bool(M.get('luz', True))

# Os componentes dependem destes nomes. Faltou um, o CSS quebra em silêncio: por isso a checagem.
OBRIGATORIOS = ['fundo', 'superficie', 'superficie-2', 'texto', 'texto-2', 'texto-3', 'linha', 'borda-controle', 'acao',
    'acao-hover', 'sobre-acao', 'realce', 'sobre-realce', 'foco', 'simbolo', 'sucesso', 'sucesso-fundo', 'atencao',
    'atencao-fundo', 'critico', 'critico-fundo', 'halo-1', 'halo-2', 'brilho', 'dado-1', 'dado-2', 'dado-3']
if not SIMBOLO: OBRIGATORIOS = ['logotipo' if n == 'simbolo' else n for n in OBRIGATORIOS]
if not LUZ: OBRIGATORIOS = [n for n in OBRIGATORIOS if n not in ('halo-1', 'halo-2', 'brilho')]
_falta = [n for n in OBRIGATORIOS if n not in {s[0] for s in SEM}]
if _falta: raise SystemExit('marca.json: faltam tokens semânticos obrigatórios: ' + ', '.join(_falta))

_pad = lambda chave, padrao: [tuple(x) for x in M.get(chave, padrao)]
ESPACO = _pad('espaco', [('espaco-1','4px','Entre ícone e texto.'),('espaco-2','8px','Entre controles agrupados.'),('espaco-3','12px','Padding de etiqueta e item de menu.'),('espaco-4','16px','Padding de campo e célula; margem lateral no celular.'),('espaco-5','24px','Padding de cartão.'),('espaco-6','32px','Entre blocos de uma página.'),('espaco-7','48px','Entre seções.'),('espaco-8','64px','Respiro de topo em página de marketing.')])
RAIO = _pad('raio', [('raio-sm','8px','Etiqueta, caixa de marcar, célula destacada.'),('raio-md','12px','Botão, campo, seleção, item de menu.'),('raio-lg','16px','Cartão, tabela, painel, aviso.'),('raio-xl','22px','Modal, ícone de app, bloco de destaque.'),('raio-pilula','999px','Avatar, filtro em pílula.')])

def _hex(nome_ou_hex):
    if nome_ou_hex.startswith('#'): return nome_ou_hex
    return {n: h for n, h, _, _ in MARCA}[nome_ou_hex]
def _rgb(h): h = _hex(h).lstrip('#'); return ','.join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))
PAPEL = {k: _hex(v) for k, v in M['papeis'].items()}
RGB_P, RGB_E = _rgb(PAPEL['primaria']), _rgb(PAPEL['escuro'])

SOMBRA = _pad('sombra', [('sombra-1',f'0 1px 2px rgba({RGB_E},0.05)','0 1px 2px rgba(0,0,0,0.4)','Cartão em repouso.'),
 ('sombra-2',f'0 1px 2px rgba({RGB_E},0.04), 0 12px 32px -16px rgba({RGB_P},0.22)','0 1px 2px rgba(0,0,0,0.4), 0 16px 40px -18px rgba(0,0,0,0.7)','Menu suspenso, aviso, cartão em hover.'),
 ('sombra-3',f'0 24px 64px -24px rgba({RGB_E},0.35)','0 24px 64px -20px rgba(0,0,0,0.8)','Modal.')])
TEMPO = [('tempo-rapido','150ms','Hover, foco, troca de cor.'),('tempo-base','240ms','Abrir menu, aviso entrando.'),('tempo-lento','400ms','Modal, painel lateral.'),
         ('tempo-assinatura', M['tempo_assinatura']['valor'], M['tempo_assinatura']['uso'])]
CURVA = [('curva-marca', M['curva']['valor'], M['curva']['uso'])]
QUEBRA = _pad('quebra', [('quebra-celular','390px','Largura de referência do celular. Desenhe aqui primeiro.'),('quebra-tablet','760px','Abaixo disto: uma coluna, menu do site vira botão, margem lateral 16 px.'),('quebra-desktop','1024px','A partir daqui: margem lateral 48 px e grade de 12 colunas.'),('quebra-largo','1280px','Conteúdo trava em 1180 px; o fundo continua.')])
CAMADA = [('camada-base','0','Conteúdo da página.'),('camada-fixo','10','Cabeçalho fixo e barra lateral.'),('camada-menu','20','Menu suspenso, seleção e popover.'),('camada-painel','30','Painel lateral e seu véu.'),('camada-modal','40','Modal e seu véu.'),('camada-aviso','50','Avisos (toast): ficam acima de tudo.'),('camada-dica','60','Dica (tooltip).')]

def cores():
    return MARCA + SEM
def resolve(v, tema):
    idx = {n: (c, e) for n, c, e, _ in cores()}
    while v.startswith('{'):
        c, e = idx[v[1:-1]]; v = c if tema == 'claro' else e
    return v

# Rótulo (LEIA-ME, "Rótulo sem caixa alta"): sem o campo, o rótulo é caixa alta espaçada (como na AJ). Com
# `"rotulo": {"caixa": "baixa"}`, todo rótulo do sistema (rótulo, cabeçalho de tabela, grupo de menu, topo das etapas,
# título de coluna do rodapé) usa o estilo `rotulo` do `tipo` (ex.: itálico em caixa baixa), sem transformar a caixa.
ROTULO = M.get('rotulo') or {}
CAIXA_ALTA = ROTULO.get('caixa', 'alta') != 'baixa'
def _rotulo_fonte():
    est = next((s for g in TIPO['groups'] for s in g['styles'] if s['name'] == 'rotulo'), None) or {}
    fam = M['fontes']['titulo' if ROTULO.get('familia') == 'titulo' else 'texto']['pilha']
    return (('italic ' if ROTULO.get('italico') else '') + f"{est.get('fontWeight', 500)} {est.get('fontSize', '12px')}/{est.get('lineHeight', '16px')} {fam}",
            est.get('letterSpacing', '0'))
# Marca com símbolo e nome em linhas (logo.linhas): a assinatura oficial em curvas entra inline (fonte.assinatura).
LINHAS = bool(SIMBOLO and M.get('logo', {}).get('linhas'))
# Piso de leitura e de toque (LEIA-ME, "Piso"): sem o campo, ligado — nenhum texto abaixo de 14 px e nenhum alvo de toque
# abaixo de 44 px (bloco `/* @se piso */` do bundle). `"piso": false` só na AJ (marca.exemplo.json), que nasceu antes da regra.
PISO = M.get('piso', True) is not False

PR = M.get('produtos', {})
MARCADORES = {
    '«NOME»': M['nome'], '«SIGLA»': M['sigla'],
    '«SISTEMA»': PR.get('sistema', M['sigla'] + ' Sistema'), '«CRM»': PR.get('crm', 'CRM'), '«METODO»': PR.get('metodo', 'Método'),
    '«FONTE_TITULO»': M['fontes']['titulo']['familia'], '«FONTE_TEXTO»': M['fontes']['texto']['familia'],
    '«PILHA_TITULO»': M['fontes']['titulo']['pilha'], '«PILHA_TEXTO»': M['fontes']['texto']['pilha'],
    '«FONTES_URL»': M['fontes']['url'], '«RGB_PRIMARIA»': RGB_P, '«RGB_ESCURO»': RGB_E,
    '«HEX_PRIMARIA»': PAPEL['primaria'], '«HEX_ESCURO»': PAPEL['escuro'], '«ESCURO_CLARO»': PAPEL.get('escuro_claro', PAPEL['escuro']),
    '«ROTULO_FONTE»': _rotulo_fonte()[0], '«ROTULO_ESPACO»': _rotulo_fonte()[1],
}

# O símbolo como máscara de CSS (`mask-image: «SIMBOLO_MASCARA»`): a forma vem das peças do marca.json e a cor, do
# fundo do elemento (um token). Para o símbolo grande de capa e o lugar do selo, sem colar geometria à mão no CSS.
if SIMBOLO:
    MARCADORES['«SIMBOLO_MASCARA»'] = ('url("data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'' + SIMBOLO.get('viewBox', '0 0 100 100')
        + '\'>' + ''.join(f"<path d=\'{d}\'/>" for d in SIMBOLO['pecas']) + '</svg>")')

# ---------- marca só tipográfica: o logotipo em curvas ----------
LOGO = os.path.join(PROJETO, 'identidade', 'logo')
def _logotipo_svg(forma):
    """(viewBox, [d, ...]) do logotipo gerado por identidade/logo/gera_final.py, na primeira combinação de cor que existir."""
    for comb in M.get('logo', {}).get('combinacoes', {}):
        f = os.path.join(LOGO, 'assinatura', f'{forma}-{comb}.svg')
        if os.path.exists(f):
            s = open(f).read()
            return re.search(r'viewBox="([^"]+)"', s).group(1), re.findall(r' d="([^"]+)"', s)
    raise SystemExit(f'falta identidade/logo/assinatura/{forma}-*.svg: rode identidade/logo/gera_final.py antes do sistema')
def logotipo(forma='horizontal', cls='aj-logotipo', extra='', rotulo='«NOME»'):
    """O logotipo inline, pintado pelo token `logotipo` (classe aj-logotipo). Nunca digite o nome no lugar dele."""
    vb, ds = _logotipo_svg(forma)
    return f'<svg class="{cls}" viewBox="{vb}"{extra} role="img" aria-label="{rotulo}">' + ''.join(f'<path d="{d}"/>' for d in ds) + '</svg>'
if not SIMBOLO:
    # Altura do logotipo em linha na largura mínima (logo.empilhado.usar_abaixo_de_px, padrão 200 px). Abaixo dela, o empilhado.
    _vb = [float(x) for x in _logotipo_svg('horizontal')[0].split()]
    LOGOTIPO_MIN = M['logo'].get('empilhado', {}).get('usar_abaixo_de_px', 200)
    MARCADORES['«LOGOTIPO_ALTURA»'] = f'{-(-LOGOTIPO_MIN * _vb[3] * 10 // _vb[2]) / 10:g}px'
    MARCADORES['«LOGOTIPO_MIN»'] = f'{LOGOTIPO_MIN}px'

# ---------- marca com símbolo e nome em linhas: a assinatura oficial inline ----------
def assinatura(forma='horizontal', cls='aj-assinatura', rotulo='«NOME»'):
    """A assinatura (símbolo + nome em linhas) gerada por identidade/logo/gera_final.py, inline e pintada por token:
    o símbolo e a 1ª linha com `simbolo`, as linhas seguintes com `texto-2` (classe aj-assinatura). Nunca digite o nome
    ao lado do símbolo no lugar dela."""
    for comb in M.get('logo', {}).get('combinacoes', {}):
        f = os.path.join(LOGO, 'assinatura', f'{forma}-{comb}.svg')
        if os.path.exists(f): break
    else: raise SystemExit(f'falta identidade/logo/assinatura/{forma}-*.svg: rode identidade/logo/gera_final.py antes do sistema')
    s = open(f).read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    g = re.search(r'<g transform="([^"]+)"[^>]*>(.*?)</g>', s, re.S)
    simb = re.sub(r' fill="[^"]*"', '', g.group(2))
    linhas = re.findall(r'<path fill="[^"]*" d="([^"]+)"/>', s[g.end():])
    return (f'<svg class="{cls}" viewBox="{vb}" role="img" aria-label="{rotulo}"><g class="aj-assinatura__simbolo" transform="{g.group(1)}">{simb}</g>'
            + ''.join(f'<path class="aj-assinatura__linha aj-assinatura__linha--{i}" d="{d}"/>' for i, d in enumerate(linhas, 1)) + '</svg>')

# ---------- blocos condicionais do bundle.tpl.css ----------
def condicional(t):
    """Linhas entre `/* @se X Y */` e `/* @fim */` (com `/* @senao */` opcional) ficam só quando a marca tem X e Y.
    Condições: simbolo, tipografica (sem símbolo), luz, sem-luz, caixa-alta (rótulo em caixa alta, o padrão),
    linhas (símbolo com o nome em linhas), piso (piso de 14 px e 44 px, o padrão). As linhas dos marcadores sempre saem."""
    flag = {'simbolo': bool(SIMBOLO), 'tipografica': not SIMBOLO, 'luz': LUZ, 'sem-luz': not LUZ, 'caixa-alta': CAIXA_ALTA, 'linhas': LINHAS, 'piso': PISO}
    out, pilha = [], []  # pilha de (ativo_por_fora, condição, no_senao)
    ativo = lambda: all(a and (c != s) for a, c, s in pilha)
    for linha in t.split('\n'):
        m = re.fullmatch(r'\s*/\* @se ([a-z\- ]+) \*/\s*', linha)
        if m: pilha.append((ativo(), all(flag[x] for x in m.group(1).split()), False)); continue
        if re.fullmatch(r'\s*/\* @senao \*/\s*', linha): a, c, _ = pilha.pop(); pilha.append((a, c, True)); continue
        if re.fullmatch(r'\s*/\* @fim \*/\s*', linha): pilha.pop(); continue
        if ativo(): out.append(linha)
    return '\n'.join(out)
def troca(t):
    """Aplica os marcadores e troca o prefixo `aj` do molde pelo prefixo da marca."""
    for a, b in MARCADORES.items(): t = t.replace(a, b)
    if P != 'aj': t = re.sub(r'(?<![A-Za-z0-9_])aj(?=[-"\s.{,:)\]])', P, t)
    return t
def grava(caminho, texto):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    open(caminho, 'w').write(troca(texto))
