# Gera a skill de design da marca a partir do Design System e do marca.json.
# Uso: python3 gen_skill.py [pasta-de-saída]   (padrão: <projeto>/skill/<nome-da-skill>)
import os, re, sys, json, shutil, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from fonte import *
NOME_SKILL = M['publicacao']['skill']
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PROJETO, 'skill', NOME_SKILL)
LOGO = os.path.join(PROJETO, 'identidade', 'logo')
APLIC = os.path.join(PROJETO, 'aplicacoes')
VERSAO = M.get('versao', '1.0') + ' · ' + datetime.date.today().strftime('%d/%m/%Y')

prefixa = lambda t: re.sub(r'var\(--(?!aj-|dx\)|dy\)|fv\)|dfv\))', 'var(--aj-', t)
shutil.rmtree(OUT, ignore_errors=True)
for d in ('referencias/componentes', 'assets/css', 'assets/logos', 'assets/modelos'):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)

# SKILL.md
grava(os.path.join(OUT, 'SKILL.md'), open(os.path.join(AQUI, 'SKILL.tpl.md')).read().replace('%%VERSAO%%', VERSAO).replace('%%SKILL%%', NOME_SKILL))

# regras, plataformas, empresa, apresentação
grava(os.path.join(OUT, 'referencias/regras.md'), '# Regras da marca «NOME»\n\n' + open(os.path.join(DS, 'README.md')).read())
if os.path.exists(os.path.join(DS, 'plataformas.md')): grava(os.path.join(OUT, 'referencias/plataformas.md'), open(os.path.join(DS, 'plataformas.md')).read())
for n in ('empresa', 'apresentacao'):
    if os.path.exists(os.path.join(AQUI, f'{n}.tpl.md')): grava(os.path.join(OUT, f'referencias/{n}.md'), open(os.path.join(AQUI, f'{n}.tpl.md')).read())

# tokens.md
tj = json.load(open(os.path.join(DS, 'tokens.json')))
idx = {t['name']: t['value'] for t in tj['color']['tokens']}
def res(v, tema):
    v = v if isinstance(v, str) else v.get(tema, v.get('claro'))
    while isinstance(v, str) and v.startswith('{'):
        w = idx[v[1:-1]]; v = w if isinstance(w, str) else w.get(tema, w.get('claro'))
    return v
# pesos por família; quando título e texto são a mesma família, ela aparece uma vez só
_ft, _fx = M['fontes']['titulo'], M['fontes']['texto']
_PESOS = (f"{_ft['familia']} {'/'.join(map(str, sorted(set(_ft['pesos']) | set(_fx['pesos']))))}" if _ft['familia'] == _fx['familia']
          else f"{_ft['familia']} {'/'.join(map(str, _ft['pesos']))} e {_fx['familia']} {'/'.join(map(str, _fx['pesos']))}")
L = ['# Tokens da marca «NOME»', '', 'No CSS, cada token é `var(--aj-<nome>)` (arquivo `assets/css/aj-tokens.css`). O tema escuro vale com `.dark` ou `[data-theme="escuro"]` no `<html>`; `[data-theme="aparelho"]` segue o tema do aparelho (claro ou escuro, sem script), para login e área do cliente.', '', '## Cores', '', '| Token | Claro | Escuro | Uso |', '|---|---|---|---|']
for t in tj['color']['tokens']:
    L.append(f"| `{t['name']}` | `{res(t['value'],'claro')}` | `{res(t['value'],'escuro')}` | {t['usage']} |")
L += ['', '## Tipografia', '', f"Famílias: título `{tj['type']['families']['titulo']}` · texto `{tj['type']['families']['texto']}` (Google Fonts, pesos {_PESOS}).", '', '| Estilo | Família | Tamanho/entrelinha | Peso | Espaçamento | Uso |', '|---|---|---|---|---|---|']
for g in tj['type']['groups']:
    for s in g['styles']:
        L.append(f"| `{s['name']}` | {g['family']} | {s['fontSize']}/{s['lineHeight']} | {s['fontWeight']} | {s.get('letterSpacing','0')} | {s['usage']} |")
for fam, tit in (('spacing','Espaço'),('radius','Raio'),('shadow','Sombra'),('duracao','Duração'),('curva','Curva'),('ponto-de-quebra','Pontos de quebra'),('camada','Camadas')):
    L += ['', f'## {tit}', '', '| Token | Valor | Uso |', '|---|---|---|']
    for t in tj[fam]['tokens']:
        v = t['value'] if isinstance(t['value'], str) else f"claro `{t['value']['claro']}` · escuro `{t['value']['escuro']}`"
        L.append(f"| `{t['name']}` | `{v}` | {t['usage']} |" if isinstance(t['value'], str) else f"| `{t['name']}` | {v} | {t['usage']} |")
grava(os.path.join(OUT, 'referencias/tokens.md'), '\n'.join(L) + '\n')

# componentes: um arquivo por componente (regra + código) e o índice
indice = []
comps = sorted(c for c in os.listdir(os.path.join(DS, 'components')) if os.path.isdir(os.path.join(DS, 'components', c)) and c != 'Cover')
for c in comps:
    rd = open(os.path.join(DS, 'components', c, 'README.md')).read().strip()
    pv = open(os.path.join(DS, 'components', c, 'preview.html')).read()
    marca, corpo = pv.split('\n', 1)
    grupo = (re.search(r'group="([^"]+)"', marca) or [None, 'Outros'])[1]
    resumo = re.sub(r'^# .*\n+', '', rd).split('\n')[0]
    resumo = re.split(r'(?<=\.)\s', resumo)[0]
    corpo = prefixa(corpo.strip())
    grava(os.path.join(OUT, f'referencias/componentes/{c}.md'),
        f"{rd}\n\n**Grupo:** {grupo}. **CSS:** `assets/css/aj-componentes.css` (classes `aj-*`) sobre `assets/css/aj-tokens.css`.\n\n## Código de referência\n\nMarcação usada na prévia do Design System. Os textos e dados são exemplos; mantenha a estrutura e as classes.\n\n```html\n{corpo}\n```\n")
    indice.append((grupo, c, resumo))
ordem = ['Marca', 'Ações', 'Formulários', 'Navegação', 'Sobreposições', 'Retorno', 'Conteúdo', 'Telas']
indice.sort(key=lambda x: (ordem.index(x[0]) if x[0] in ordem else 99, x[1]))
I = ['# Índice de componentes', '', f'{len(indice)} componentes. Antes de montar uma tela, liste os que ela usa e abra o arquivo de cada um.', '', '| Grupo | Componente | Para quê | Arquivo |', '|---|---|---|---|']
I += [f"| {g} | `{c}` | {r} | `componentes/{c}.md` |" for g, c, r in indice]
grava(os.path.join(OUT, 'referencias/componentes/INDICE.md'), '\n'.join(I) + '\n')

# assets: CSS, logos, modelos
for f in (f'{P}-tokens.css', f'{P}-componentes.css', 'ponte-shadcn.css', 'ponte-nossocrm.css'):
    shutil.copy(os.path.join(INTERFACE, f), os.path.join(OUT, 'assets/css', f))
# publicacao.logos_png: true leva também os PNG (assinatura, símbolo, ícone, favicon e avatar) para quem não pode usar SVG
# (assinatura de e-mail, WhatsApp, redes). Sem o campo, só SVG e ICO, como na AJ.
_PNG = bool(M.get('publicacao', {}).get('logos_png'))
for sub in ('simbolo', 'assinatura', 'app', 'favicon') + (('avatar',) if _PNG else ()):
    d = os.path.join(LOGO, sub)
    for f in (os.listdir(d) if os.path.isdir(d) else []):
        if f.endswith('.svg') or f.endswith('.ico') or (_PNG and f.endswith('.png')):
            shutil.copy(os.path.join(d, f), os.path.join(OUT, 'assets/logos', f))
# vídeos do movimento-assinatura (identidade/logo/movimento/*.mp4) → assets/movimento/, para a skill não apontar para o projeto
MOV = os.path.join(LOGO, 'movimento')
if os.path.isdir(MOV) and any(f.endswith('.mp4') for f in os.listdir(MOV)):
    os.makedirs(os.path.join(OUT, 'assets/movimento'), exist_ok=True)
    for f in sorted(os.listdir(MOV)):
        if f.endswith('.mp4'): shutil.copy(os.path.join(MOV, f), os.path.join(OUT, 'assets/movimento', f))
# fotos aprovadas da marca (marca de pessoa, foto no lugar do símbolo): <projeto>/identidade/fotos/ → assets/fotos/
FOTOS = os.path.join(PROJETO, 'identidade', 'fotos')
if os.path.isdir(FOTOS):
    os.makedirs(os.path.join(OUT, 'assets/fotos'), exist_ok=True)
    for f in sorted(os.listdir(FOTOS)):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')): shutil.copy(os.path.join(FOTOS, f), os.path.join(OUT, 'assets/fotos', f))
for f in (os.listdir(APLIC) if os.path.isdir(APLIC) else []):
    if f.endswith('.html'):
        shutil.copy(os.path.join(APLIC, f), os.path.join(OUT, 'assets/modelos', f))
# Modelos que vivem em subpastas de aplicacoes/ (peças prontas com PDF, DOCX, fontes): o campo `modelos` do marca.json
# lista os padrões (glob, relativos a aplicacoes/), e cada arquivo vai para assets/modelos/ no mesmo caminho relativo,
# para os links entre eles (../fontes, ../../_fontes-pdf) continuarem valendo.
import glob
for padrao in M.get('modelos', []):
    achou = glob.glob(os.path.join(APLIC, padrao))
    if not achou: raise SystemExit(f'marca.json, modelos: nada em aplicacoes/{padrao}')
    for f in achou:
        if os.path.isfile(f):
            destino = os.path.join(OUT, 'assets/modelos', os.path.relpath(f, APLIC))
            os.makedirs(os.path.dirname(destino), exist_ok=True); shutil.copy(f, destino)

# modelo de documento autossuficiente (CSS embutido)
css = open(os.path.join(INTERFACE, f'{P}-tokens.css')).read() + '\n' + open(os.path.join(INTERFACE, f'{P}-componentes.css')).read()
if SIMBOLO:
    simb = f'<svg class="aj-simbolo" viewBox="{SIMBOLO.get("viewBox", "0 0 100 100")}" aria-hidden="true">' + ''.join(f'<path d="{d}"/>' for d in SIMBOLO['pecas']) + '</svg>'
    marca_topo = assinatura() if LINHAS else simb + '«NOME»'  # nome em linhas: a assinatura oficial, não o nome digitado
else:
    marca_topo = logotipo('horizontal')  # marca só tipográfica: o logotipo já é o nome
capa_cls = 'aj-doc__capa aj-halo' if LUZ else 'aj-doc__capa'
secoes = [('secao-1', '[Seção 1]'), ('secao-2', '[Seção 2]'), ('secao-3', '[Seção 3]'), ('secao-4', '[Seção 4]')]
sumario = '<nav aria-label="Sumário"><ol class="aj-sumario">' + ''.join(f'<li><a href="#{i}"><span class="aj-sumario__n">{n:02d}</span>{t}</a></li>' for n, (i, t) in enumerate(secoes, 1)) + '</ol></nav>'
secs = ''.join(f'''
<section class="aj-doc__secao" id="{i}">
  <div class="aj-doc__cabeca"><span class="aj-rotulo">{n:02d} · {t}</span><h2 class="aj-titulo aj-titulo--secao">[Título da seção com uma <b>ênfase</b>]</h2><p class="aj-subtitulo">[Uma a três frases que resumem a seção.]</p></div>
  <div class="aj-doc__grade aj-doc__grade--3">
    <div class="aj-cartao"><h3 class="aj-cartao__titulo">[Ponto 1]</h3><p class="aj-subtitulo">[Explicação curta.]</p></div>
    <div class="aj-cartao"><h3 class="aj-cartao__titulo">[Ponto 2]</h3><p class="aj-subtitulo">[Explicação curta.]</p></div>
    <div class="aj-cartao"><h3 class="aj-cartao__titulo">[Ponto 3]</h3><p class="aj-subtitulo">[Explicação curta.]</p></div>
  </div>
</section>''' for n, (i, t) in enumerate(secoes, 1))
doc = f'''<!doctype html>
<html lang="pt-BR" data-theme="claro">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>[Título do documento] · «NOME»</title>
<!-- Modelo de documento «SIGLA» (relatório, resumo de reunião, proposta). Abra no navegador; para PDF: Imprimir › Salvar como PDF, A4, com gráficos de fundo. -->
<style>
{css}
body {{ margin: 0; }}
.aj-cartao {{ display: grid; gap: 8px; align-content: start; }}
.aj-cartao .aj-subtitulo {{ font-size: 14px; line-height: 22px; }}
</style>
</head>
<body class="aj">
<main class="aj-doc">
  <div class="aj-doc__topo"><span style="display:flex;align-items:center;gap:10px;font:600 15px/20px «PILHA_TITULO»;letter-spacing:-.02em">{marca_topo}</span><small style="color:var(--aj-texto-3)">[Natureza do documento] · [uso interno]</small></div>
  <div class="{capa_cls}"><span class="aj-rotulo">[Tipo] de [dd/mm/aaaa]</span><h1 class="aj-titulo aj-titulo--display">[Título do documento com uma <b>ênfase</b>]</h1>
  <p class="aj-subtitulo">[Duas ou três linhas dizendo o que o documento traz e para quê.]</p>
  <div class="aj-doc__meta"><span class="aj-etiqueta aj-etiqueta--marca">[Produto ou tema]</span><span class="aj-etiqueta">[Participantes]</span></div></div>
  <div class="aj-doc__sumario">{sumario}</div>
{secs}
</main>
</body>
</html>
'''
grava(os.path.join(OUT, 'assets/modelos/documento.html'), doc)

n = sum(len(f) for _, _, f in os.walk(OUT))
print(f'skill gerada em {OUT}: {n} arquivos, {len(indice)} componentes')
