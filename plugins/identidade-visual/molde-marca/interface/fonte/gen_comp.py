# Gera os componentes do Design System (preview.html + README.md de cada um). Os textos de exemplo e as regras
# dos README vieram da marca AJ: reescreva-os para a marca do projeto (a auditoria acusa o que sobrar).
# Marca só tipográfica (simbolo null): SIMB() devolve o logotipo em curvas, o componente Simbolo vira Logotipo e o
# Carregando passa a ser o nome entrando como no vídeo de abertura. Marca sem luz (luz false): as classes de halo e
# brilho saem das prévias (veja comp()).
import json,os,re,sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from fonte import *
if SIMBOLO:
    VB=SIMBOLO.get('viewBox','0 0 100 100'); PECAS=SIMBOLO['pecas']
    def SIMB(cls='aj-simbolo',w=None,extra=''):
        a=f' width="{w}" height="{w}"' if w else ''
        return f'<svg class="{cls}" viewBox="{VB}"{a}{extra} aria-hidden="true">'+''.join(f'<path d="{d}"/>' for d in PECAS)+'</svg>'
    # Símbolo com mais de duas peças: cada uma chega de simbolo.entrada (unidades da caixa 100, como no vídeo de abertura);
    # com duas (a AJ), a primeira e a última vêm pela diagonal do bundle.tpl.css.
    _ENTRA=SIMBOLO.get('entrada') if len(PECAS)>2 else None
    def CARREG(w=48): return f'<svg class="aj-carregando" viewBox="{VB}" width="{w}" height="{w}" role="img" aria-label="Carregando">'+''.join((f'<path style="--dx:{_ENTRA[i][0]:g}px;--dy:{_ENTRA[i][1]:g}px" d="{d}"/>' if _ENTRA else f'<path d="{d}"/>') for i,d in enumerate(PECAS))+'</svg>'
    # Nome em linhas (logo.linhas): a assinatura oficial em curvas, nunca o nome digitado ao lado do símbolo.
    def MARCA_NOME(): return assinatura() if LINHAS else f'{SIMB()}<span>«NOME»</span>'
else:
    def SIMB(cls='aj-logotipo',w=None,extra=''): return logotipo('horizontal',cls,extra)
    def MARCA_NOME(): return SIMB()  # o logotipo já é o nome: nada de repetir o nome em texto ao lado
    _MED=os.path.join(LOGO,'medidas.json')
    _CORPO=(json.load(open(_MED)).get('assinaturas',{}).get('horizontal',{}).get('corpo') if os.path.exists(_MED) else None) or 140
    def _fv(eixos): return ', '.join(f"'{k}' {v}" for k,v in eixos.items())
    def CARREG(px=28):
        """O nome entrando: cada trecho de logo.trechos com a própria entrada (deslocamento `de` em unidades da altura
        da maiúscula = 100, eixos de partida `eixos` e `atraso` em ms), como em identidade/logo/video.js."""
        h=f'<span class="aj-carregando" role="img" aria-label="Carregando" style="font-size:{px}px">'
        for i,tr in enumerate(M['logo']['trechos']):
            en=tr.get('entrada',{}); de=en.get('de',[0,0]); ini=dict(tr['eixos'],**en.get('eixos',{}))
            h+=(' ' if i else '')+f'<span style="--fv:{_fv(tr["eixos"])};--dfv:{_fv(ini)};--dx:{de[0]/_CORPO:.3f}em;--dy:{de[1]/_CORPO:.3f}em;letter-spacing:{tr.get("tracking",0)}em;animation-delay:{en.get("atraso",0)}ms">{tr["texto"]}</span>'
        return h+'</span>'
I={'inicio':'<rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/>',
 'contratos':'<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M9 13h6M9 17h6"/>',
 'onboarding':'<path d="m9 11 3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
 'clientes':'<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
 'reunioes':'<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
 'alertas':'<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4M12 17h.01"/>',
 'anuncios':'<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
 'relatorios':'<path d="M3 3v18h18"/><path d="M18 17V9M13 17V5M8 17v-3"/>',
 'financeiro':'<path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
 'config':'<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/>',
 'funil':'<path d="M6 5v11M12 5v6M18 5v14"/>','conversas':'<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
 'ok':'<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>','erro':'<circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>',
 'mais':'<path d="M12 5v14M5 12h14"/>','busca':'<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>','seta':'<path d="M5 12h14M13 6l6 6-6 6"/>'}
def ic(n,cls=''): return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[n]}</svg>'
C={}
def _sem_luz(h):
    h=re.sub(r'\s*\baj-(?:halo--respira|halo|brilho)\b','',h)
    return h.replace(' class=""','')
def comp(nome,grupo,altura,readme,corpo,extra=''):
    pad='0' if 'page' in extra else '24px'
    if not LUZ: corpo=_sem_luz(corpo)
    C[nome]=(f'<!-- @dsCard group="{grupo}" height={altura}{extra} -->\n<div class="aj" style="padding:{pad};background:var(--fundo);min-height:100%">\n{corpo}\n</div>\n',readme)
ESC='data-theme="escuro"'
AC=' aria-current="page"'
if SIMBOLO:
    comp('Simbolo','Marca',260,
"""# Simbolo
O símbolo A2 Dobra com as duas luzes da marca: violeta chapado com halo no fundo claro, lavanda com brilho próprio no escuro.

**O que você fornece:** o SVG inline (dois `path`, arquivo `assets/Logos/simbolo-*.svg`) com a classe `aj-simbolo`; ele pinta com o token `simbolo`. No escuro, acrescente `aj-brilho`. O halo é uma classe do **contêiner** (`aj-halo`), nunca do símbolo.

- Use a versão com a dobra de 32 px para cima; em 24 px ou menos, `simbolo-pequeno-violeta.svg` (sem fresta).
- Respiro livre em volta: 1/3 da altura do símbolo.
- Nunca: gradiente, contorno, sombra dura, distorção, moldura, 3D como padrão.
""",
f"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
<div class="aj-halo" style="height:200px;border-radius:var(--raio-lg);display:grid;place-items:center;background:var(--fundo);border:1px solid var(--linha)">{SIMB(w=84)}</div>
<div {ESC} class="aj-halo" style="height:200px;border-radius:var(--raio-lg);display:grid;place-items:center;background:var(--fundo)">{SIMB('aj-simbolo aj-brilho',84)}</div>
</div>""")
    comp('Carregando','Marca',180,
"""# Carregando
A dobra se fecha: as duas peças do símbolo chegam pela diagonal de 45° e se encaixam. É o único indicador de carregamento da marca.

**O que você fornece:** o SVG do símbolo com a classe `aj-carregando` e `role="img"` + `aria-label="Carregando"`. Duração 1,6 s em laço, curva `curva-marca`.

- Use em carregamento de página ou de painel (mais de 400 ms). Para ações curtas dentro de um botão, desabilite o botão e troque o texto ("Salvando…").
- Com movimento reduzido ativado, o símbolo fica parado.
- Não use girador (spinner) genérico.
""",
f"""<div style="display:flex;gap:40px;align-items:center;justify-content:center;height:120px">
{CARREG(48)}
<div {ESC} style="background:var(--fundo);border-radius:var(--raio-lg);padding:28px 36px">{CARREG(48).replace('aj-carregando','aj-carregando aj-brilho')}</div>
</div>""")
else:
    _TR=' e '.join(f'"{tr["texto"]}" ('+', '.join(f'{k} {v}' for k,v in tr['eixos'].items())+')' for tr in M['logo']['trechos'])
    _COMB='; '.join(f"`{c['cor']}` sobre "+', '.join(f'`{s}`' for s in c['sobre']) for c in M['logo']['combinacoes'].values())
    _EXTRAS=''.join(f", `{x['nome']}-*.svg`" for x in M['logo'].get('extras',[]))
    comp('Logotipo','Marca',300,
f"""# Logotipo
O nome «NOME» em curvas: a marca é só tipográfica, não tem símbolo. Trechos: {_TR}, na «FONTE_TITULO».

**O que você fornece:** o arquivo de `assets/logos/` por `<img>` (`horizontal-*.svg`, `empilhado-*.svg`{_EXTRAS}) ou o SVG inline com a classe `aj-logotipo`; inline, ele pinta com o token `logotipo` e mede «LOGOTIPO_ALTURA» de altura em linha. Nunca digite o nome em texto no lugar do logotipo.

- Em linha a partir de «LOGOTIPO_MIN» de largura; abaixo disso, o empilhado (`aj-logotipo aj-logotipo--empilhado`).
- Cores (contraste medido em `identidade/logo/medidas.json`): {_COMB}.
- Respiro livre em volta: {M['logo'].get('respiro','a altura de uma maiúscula')}.
- Nunca: contorno, sombra, gradiente, distorção, outra fonte, letra espaçada à mão ou cor fora das combinações.
""",
f"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
<div style="height:200px;border-radius:var(--raio-lg);display:grid;place-items:center;background:var(--fundo);border:1px solid var(--linha)">{SIMB()}</div>
<div style="height:200px;border-radius:var(--raio-lg);display:grid;place-items:center;background:var(--superficie);border:1px solid var(--linha)">{logotipo('empilhado','aj-logotipo aj-logotipo--empilhado')}</div>
<div {ESC} style="grid-column:1/-1;height:160px;border-radius:var(--raio-lg);display:grid;place-items:center;background:var(--fundo)">{SIMB()}</div>
</div>""")
    comp('Carregando','Marca',180,
"""# Carregando
O nome entrando como na abertura em vídeo: cada trecho do logotipo chega do jeito definido em `logo.trechos` do marca.json. É o único indicador de carregamento da marca.

**O que você fornece:** o `<span class="aj-carregando" role="img" aria-label="Carregando">` com um `<span>` por trecho, cada um com as variáveis `--fv` (eixos finais), `--dfv` (eixos de partida), `--dx`/`--dy` (de onde desliza) e `animation-delay`. Copie a marcação da prévia; o laço dura duas vezes `tempo-assinatura`, com `curva-marca`.

- Use em carregamento de página ou de painel (mais de 400 ms). Para ações curtas dentro de um botão, desabilite o botão e troque o texto ("Salvando…").
- Com movimento reduzido ativado, o nome fica parado, já montado.
- Não use girador (spinner) genérico.
""",
f"""<div style="display:flex;flex-wrap:wrap;gap:24px 40px;align-items:center;justify-content:center;min-height:120px">
{CARREG()}
<div {ESC} style="background:var(--fundo);border-radius:var(--raio-lg);padding:28px 36px">{CARREG()}</div>
</div>""")
comp('Botao','Ações',200,
"""# Botao
Botão da marca em cinco variantes; a principal é violeta chapado e aparece uma vez por tela.

**O que você fornece:** um `<button>` (ou `<a>`) com `aj-botao` + uma variante: `aj-botao--principal`, `--secundario`, `--contorno`, `--fantasma` ou `--perigo`; tamanho opcional `--sm` (32 px) ou `--lg` (48 px). O texto diz o que acontece.

- Uma ação principal por tela. As outras, secundário ou contorno.
- O texto é verbo + objeto: "Solicitar diagnóstico", "Salvar cliente". O aviso de resultado usa o mesmo verbo no particípio: "Cliente salvo".
- Raio `raio-md`, altura 40 px, texto `interface`. Foco: anel `foco` de 2 px.
- Nada de gradiente, sombra colorida ou pílula no botão principal.
""",
f"""<div style="display:grid;gap:16px">
<div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">
<button class="aj-botao aj-botao--principal">Solicitar diagnóstico</button>
<button class="aj-botao aj-botao--secundario">Ver método</button>
<button class="aj-botao aj-botao--contorno">{ic('mais')}Novo cliente</button>
<button class="aj-botao aj-botao--fantasma">Cancelar</button>
<button class="aj-botao aj-botao--perigo">Excluir contrato</button>
</div>
<div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">
<button class="aj-botao aj-botao--principal aj-botao--lg">Começar agora{ic('seta')}</button>
<button class="aj-botao aj-botao--principal aj-botao--sm">Salvar</button>
<button class="aj-botao aj-botao--principal" disabled>Salvando…</button>
</div></div>""")
comp('Campo','Formulários',270,
"""# Campo
Campo de texto, seleção e área de texto com rótulo sempre visível, ajuda e estado de erro.

**O que você fornece:** um contêiner `aj-campo` com `<label for>`, o controle com `aj-entrada` (`input`, `select` ou `textarea`) e, opcional, `<span class="aj-ajuda">`. Para erro, acrescente `aj-campo--erro` ao contêiner e escreva na ajuda o que corrigir.

- Rótulo em cima, nunca só placeholder.
- A borda usa `borda-controle` (3:1 ou mais); o foco, `foco`.
- A mensagem de erro diz como resolver: "Informe um e-mail com @", não "Campo inválido".
- **Valor em dinheiro:** `aj-moeda` com o prefixo em `aj-moeda__prefixo` ("R$") e o campo `aj-entrada aj-entrada--grande` com `inputmode="numeric"`; embaixo, opcional, `aj-atalhos` com botões `aj-atalho` (`aria-pressed="true"` no escolhido) que preenchem o campo com valores redondos.
""",
"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:640px">
<div class="aj-campo" style="grid-column:1/-1"><label for="c0">Investimento mensal em anúncios</label><div class="aj-moeda"><span class="aj-moeda__prefixo">R$</span><input id="c0" class="aj-entrada aj-entrada--grande" inputmode="numeric" value="3.000"></div>
<div class="aj-atalhos" role="group" aria-label="Valores prontos"><button class="aj-atalho" aria-pressed="false">R$ 1.500</button><button class="aj-atalho" aria-pressed="true">R$ 3.000</button><button class="aj-atalho" aria-pressed="false">R$ 5.000</button></div><span class="aj-ajuda">Valores de exemplo.</span></div>
<div class="aj-campo"><label for="c1">Nome do escritório</label><input id="c1" class="aj-entrada" placeholder="Ex.: Almeida Advocacia"><span class="aj-ajuda">Como aparece para o cliente.</span></div>
<div class="aj-campo"><label for="c2">Área principal</label><select id="c2" class="aj-entrada"><option>Previdenciário</option><option>Trabalhista</option><option>Família</option></select></div>
<div class="aj-campo aj-campo--erro"><label for="c3">E-mail</label><input id="c3" class="aj-entrada" value="contato@almeida" aria-invalid="true"><span class="aj-ajuda">Informe um e-mail completo, com domínio.</span></div>
<div class="aj-campo"><label for="c4">Observação</label><textarea id="c4" class="aj-entrada" rows="2" placeholder="Opcional"></textarea></div>
</div>""")
comp('Cartao','Conteúdo',230,
"""# Cartao
Superfície branca chapada com borda fina e sombra quase invisível; é o contêiner padrão de conteúdo.

**O que você fornece:** um elemento com `aj-cartao` e o conteúdo; título opcional com `aj-cartao__titulo`.

- Fundo `superficie`, borda `linha`, raio `raio-lg`, padding `espaco-5`, sombra `sombra-1`.
- Sem vidro, sem gradiente, sem borda colorida à esquerda.
- Cartão dentro de cartão, não: use `superficie-2` para agrupar dentro dele.
""",
"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;max-width:720px">
<div class="aj-cartao" style="display:grid;gap:8px"><h3 class="aj-cartao__titulo">Próxima reunião</h3><p class="aj-subtitulo" style="font-size:14px;line-height:20px">Alinhamento mensal com o escritório, hoje às 15h.</p><div><button class="aj-botao aj-botao--secundario aj-botao--sm">Abrir pauta</button></div></div>
<div data-theme="escuro" class="aj-cartao" style="display:grid;gap:8px;color:var(--texto)"><h3 class="aj-cartao__titulo">Próxima reunião</h3><p class="aj-subtitulo" style="font-size:14px;line-height:20px">Alinhamento mensal com o escritório, hoje às 15h.</p><div><button class="aj-botao aj-botao--secundario aj-botao--sm">Abrir pauta</button></div></div>
</div>""")
comp('Indicador','Conteúdo',560,
"""# Indicador
Número grande em «FONTE_TITULO» com rótulo em caixa alta e a variação ao lado; usado nos topos de painel.

**O que você fornece:** dentro de um `aj-cartao`, um `aj-indicador` com `aj-rotulo`, `aj-indicador__valor` e, opcional, `aj-indicador__variacao--sobe` ou `--desce` (sempre com sinal e texto, nunca só cor).

- No máximo quatro indicadores por linha. Mostre só números que levam a uma decisão.
- Algarismos tabulares; moeda como "R$ 48.200".
- **Dois valores comparados** (antes × depois): `aj-comparacao` com dois `aj-comparacao__item` (rótulo, `aj-comparacao__valor`, `aj-comparacao__nota`); o do resultado leva `aj-comparacao__item--resultado` (o fio em cima). Neutra: nunca vermelho para um e verde para o outro.
- **Resultado** (o número que a pessoa veio buscar, no fim de um formulário ou simulação): `aj-resultado` com `aj-resultado__destaque` (rótulo + `aj-resultado__valor`), as linhas que o explicam (`<dl class="aj-resultado__linhas">` com um `aj-resultado__linha` por par `dt`/`dd`) e a ressalva (`aj-resultado__ressalva`), uma vez, legível.
""",
"""<div style="display:grid;gap:28px;max-width:760px">
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px">
<div class="aj-cartao aj-indicador"><span class="aj-rotulo">Contratos no mês</span><span class="aj-indicador__valor">318</span><span class="aj-indicador__variacao aj-indicador__variacao--sobe">+12% vs. agosto</span></div>
<div class="aj-cartao aj-indicador"><span class="aj-rotulo">Custo por lead</span><span class="aj-indicador__valor">R$ 41</span><span class="aj-indicador__variacao aj-indicador__variacao--desce">+8% acima da meta</span></div>
<div class="aj-cartao aj-indicador"><span class="aj-rotulo">Clientes ativos</span><span class="aj-indicador__valor">42</span><span class="aj-legenda" style="font-size:12px;color:var(--texto-3)">Dados de exemplo</span></div>
</div>
<div class="aj-comparacao"><div class="aj-comparacao__item"><span class="aj-rotulo">Custo por contrato antes</span><span class="aj-comparacao__valor">R$ 410</span><span class="aj-comparacao__nota">média de abril a junho</span></div>
<div class="aj-comparacao__item aj-comparacao__item--resultado"><span class="aj-rotulo">Custo por contrato agora</span><span class="aj-comparacao__valor">R$ 180</span><span class="aj-comparacao__nota">média de julho a setembro</span></div></div>
<div class="aj-resultado"><div class="aj-resultado__destaque"><span class="aj-rotulo">Contratos a mais por mês</span><p class="aj-resultado__valor">+ 12</p></div>
<dl class="aj-resultado__linhas"><div class="aj-resultado__linha"><dt>Leads por mês</dt><dd>140</dd></div><div class="aj-resultado__linha"><dt>Taxa de fechamento</dt><dd>8,5%</dd></div></dl>
<p class="aj-resultado__ressalva">Dados de exemplo. Simulação, não promessa: o resultado depende do produto e do atendimento de cada escritório.</p></div>
</div>""")
comp('Etiqueta','Conteúdo',110,
"""# Etiqueta
Etiqueta de status com ponto e palavra; a cor nunca carrega o sentido sozinha.

**O que você fornece:** um `<span class="aj-etiqueta">` com a palavra de status e uma variante: `--sucesso`, `--atencao`, `--critico`, `--marca` ou nenhuma (neutra).

- Palavras curtas e fixas por estado: "Em dia", "Aguardando", "Em risco", "Novo".
- Texto e fundo vêm de pares testados (`sucesso` sobre `sucesso-fundo` etc., 4,5:1 ou mais nos dois temas).
""",
"""<div style="display:grid;gap:12px">
<div style="display:flex;gap:8px;flex-wrap:wrap"><span class="aj-etiqueta aj-etiqueta--sucesso">Em dia</span><span class="aj-etiqueta aj-etiqueta--atencao">Aguardando acesso</span><span class="aj-etiqueta aj-etiqueta--critico">Em risco</span><span class="aj-etiqueta aj-etiqueta--marca">Novo</span><span class="aj-etiqueta">Pausado</span></div>
<div data-theme="escuro" style="display:flex;gap:8px;flex-wrap:wrap;background:var(--fundo);padding:12px;border-radius:var(--raio-md)"><span class="aj-etiqueta aj-etiqueta--sucesso">Em dia</span><span class="aj-etiqueta aj-etiqueta--atencao">Aguardando acesso</span><span class="aj-etiqueta aj-etiqueta--critico">Em risco</span><span class="aj-etiqueta aj-etiqueta--marca">Novo</span><span class="aj-etiqueta">Pausado</span></div>
</div>""")
LIN=[('Almeida & Nascimento','Onboarding','atencao','Aguardando acesso','R$ 6.500'),('Silva Previdenciário','Em operação','sucesso','Em dia','R$ 8.000'),('Costa & Ribeiro','Em operação','critico','Custo acima da meta','R$ 7.200'),('Moura Trabalhista','Renovação','marca','Reunião marcada','R$ 5.900')]
TAB='<div class="aj-tabela-caixa"><table class="aj-tabela"><thead><tr><th>Escritório</th><th>Fase</th><th>Status</th><th class="num">Mensalidade</th></tr></thead><tbody>'+''.join(f'<tr><td>{a}</td><td class="fraco">{b}</td><td><span class="aj-etiqueta aj-etiqueta--{c}">{d}</span></td><td class="num">{e}</td></tr>' for a,b,c,d,e in LIN)+'</tbody></table></div>'
comp('Tabela','Conteúdo',300,
"""# Tabela
Tabela em superfície branca com cabeçalho em `superficie-2`, linhas separadas por `linha` e números alinhados à direita.

**O que você fornece:** `aj-tabela-caixa` envolvendo um `<table class="aj-tabela">`; células numéricas com `num`, texto secundário com `fraco`; status sempre como `aj-etiqueta`.

- Cabeçalho em `rotulo` («FONTE_TITULO» 500, caixa alta). Célula em `corpo-sm`.
- Sem listras zebradas; o hover de linha usa `superficie-2`.
- No celular, a caixa rola na horizontal; a página não.
""",TAB+'<p class="aj-ajuda" style="margin:8px 0 0">Dados de exemplo.</p>')
comp('Aviso','Retorno',230,
"""# Aviso
Aviso flutuante (toast) que confirma uma ação ou explica um erro, com título curto e uma frase.

**O que você fornece:** `aj-aviso` + `--sucesso`, `--critico` ou `--marca`; ícone em `aj-aviso__icone`, `aj-aviso__titulo` e `aj-aviso__texto`. Em código com sonner/toast, aplique estas classes ao contêiner.

- O título repete o verbo do botão no particípio: "Relatório enviado".
- O erro diz o que houve e o que fazer, sem pedir desculpas.
- Some sozinho em 5 s; erro fica até ser fechado.
""",
f"""<div style="display:grid;gap:10px">
<div class="aj-aviso aj-aviso--sucesso">{ic('ok','aj-aviso__icone')}<div><p class="aj-aviso__titulo">Relatório enviado</p><p class="aj-aviso__texto">O escritório recebeu o resumo de setembro por e-mail.</p></div></div>
<div class="aj-aviso aj-aviso--critico">{ic('erro','aj-aviso__icone')}<div><p class="aj-aviso__titulo">Não foi possível conectar a conta de anúncios</p><p class="aj-aviso__texto">O acesso expirou. Peça ao escritório para aprovar de novo no Meta.</p></div></div>
</div>""")
comp('EstadoVazio','Conteúdo',290,
"""# EstadoVazio
Tela sem dados: halo suave, o símbolo, uma frase leve com uma palavra em peso e uma única ação.

**O que você fornece:** um contêiner `aj-vazio aj-halo` com o símbolo (`aj-simbolo`), `aj-vazio__titulo` (uma palavra em `<b>`), `aj-vazio__texto` e um botão.

- É um dos três lugares do app onde o halo aparece (os outros: login e o topo do Início).
- A frase explica o próximo passo, não o problema.
""",
f"""<div class="aj-vazio aj-halo">{SIMB() if SIMBOLO else ''}<h3 class="aj-vazio__titulo">Nenhuma reunião <b>hoje</b></h3><p class="aj-vazio__texto">Quando uma reunião for marcada com um escritório, ela aparece aqui com a pauta pronta.</p><button class="aj-botao aj-botao--principal">Marcar reunião</button></div>""")
NAV=[('Operação',[('inicio','Início',True,''),('contratos','Contratos',False,''),('onboarding','Onboarding',False,'3'),('clientes','Clientes',False,''),('reunioes','Reuniões',False,''),('alertas','Alertas',False,'4')]),('Tráfego pago',[('anuncios','Contas de anúncio',False,''),('relatorios','Relatórios',False,'')]),('Gestão',[('financeiro','Financeiro',False,'')]),('Sistema',[('config','Configurações',False,'')])]
NAV_MARCA='aj-nav__marca' if SIMBOLO else 'aj-nav__marca aj-nav__marca--logotipo'
def nav(marca='«SISTEMA»'):
    h=f'<nav class="aj-nav" aria-label="Principal"><div class="{NAV_MARCA}">{SIMB()}<span>{marca}</span></div>'
    for g,its in NAV:
        h+=f'<div class="aj-nav__grupo">{g}</div>'
        for i,t,a,n in its:
            h+=f'<a class="aj-nav__item" href="#"{AC if a else ""}>{ic(i)}{t}'+(f'<span class="aj-nav__contador">{n}</span>' if n else '')+'</a>'
    return h+'</nav>'
I.setdefault('menu','<path d="M4 6h16M4 12h16M4 18h16"/>')
def barra_app(marca='«SISTEMA»'):
    return (f'<header class="aj-app__barra"><div class="{NAV_MARCA}" style="padding:0">{SIMB()}<span>{marca}</span></div>'
            f'<button class="aj-botao-icone" aria-label="Abrir menu" aria-expanded="false" onclick="{MENU_JS}">{ic("menu")}</button></header>')
# O menu do celular: o botão abre e fecha (aria-expanded e aria-label acompanham) e leva o foco para o primeiro item do
# menu; ao fechar, o foco volta ao botão. O véu e o Esc fecham (APP_ESC vai no <div class="aj-app">).
MENU_JS=("var a=this.closest('.aj-app'),abre=a.dataset.menu!=='aberto';a.dataset.menu=abre?'aberto':'';"
         "this.setAttribute('aria-expanded',abre);this.setAttribute('aria-label',abre?'Fechar menu':'Abrir menu');"
         "if(abre){var i=a.querySelector('.aj-nav a,.aj-nav button');if(i)i.focus()}else this.focus()")
VEU_APP='<div class="aj-veu aj-app__veu" onclick="this.closest(\'.aj-app\').querySelector(\'.aj-app__barra [aria-expanded]\').click()"></div>'
APP_ESC=' onkeydown="if(event.key===\'Escape\'&amp;&amp;this.dataset.menu===\'aberto\')this.querySelector(\'.aj-app__barra [aria-expanded]\').click()"'
comp('NavegacaoLateral','Navegação',640,
"""# NavegacaoLateral
Menu lateral branco com o símbolo no topo, grupos em rótulo e o item ativo em `realce`.

**O que você fornece:** `<nav class="aj-nav">` com `aj-nav__marca` (símbolo + nome do produto), `aj-nav__grupo` para cada grupo e links `aj-nav__item` com ícone de traço (lucide, 1,75) e `aria-current="page"` no ativo; contador opcional `aj-nav__contador`.

- O ativo é marcado por fundo `realce` e texto `sobre-realce`, não por barra colorida na lateral.
- Ícones de traço fino, na cor do texto. Nunca ícone colorido ou emoji.
- **No celular e no tablet (abaixo de 1024 px)** o menu sai da lateral: dentro de `aj-app`, a barra do topo (`aj-app__barra`: a marca e um `aj-botao-icone` de menu, 44 px) abre o menu como painel à esquerda (`data-menu="aberto"` no `aj-app`, com o véu `aj-veu aj-app__veu`). O véu e o Esc fecham; o botão alterna "Abrir menu" e "Fechar menu" (`aria-label` e `aria-expanded`), o foco entra no primeiro item ao abrir e volta ao botão ao fechar. Veja `TelaSistema`.
""",f'<div style="display:flex;height:600px;border:1px solid var(--linha);border-radius:var(--raio-lg);overflow:hidden;width:max-content">{nav()}</div>')
comp('TituloDePagina','Navegação',150,
"""# TituloDePagina
O título de cada página: frase em «FONTE_TITULO» 300 com uma única palavra em 600, e uma linha de contexto embaixo.

**O que você fornece:** `<h1 class="aj-titulo">` com uma palavra em `<b>` e, opcional, `<p class="aj-subtitulo">`.

- Uma palavra em peso por título: a que carrega o sentido ("Bom dia, **Samuel**", "Contratos de **setembro**").
- Sem ponto final em título de app. Em página de marketing, frase completa com ponto.
""",
"""<div style="display:grid;gap:8px"><h1 class="aj-titulo">Bom dia, <b>Samuel</b></h1><p class="aj-subtitulo">Sexta, 26 de setembro · 4 alertas pedem sua atenção</p></div>""")
# ---------- telas ----------
LAND=f"""<div class="aj" style="background:var(--fundo)">
<header style="display:flex;align-items:center;justify-content:space-between;padding:22px 56px">
<div style="display:flex;align-items:center;gap:12px">{SIMB(w=30)+'<span style="font:400 19px/1 «PILHA_TITULO»;letter-spacing:-0.035em">«NOME»</span>' if SIMBOLO else SIMB()}</div>
<nav style="display:flex;gap:28px;font:500 14px/20px «PILHA_TEXTO»;color:var(--texto-2)"><span>«METODO»</span><span>Resultados</span><span>Sobre</span><span>Perguntas</span></nav>
<button class="aj-botao aj-botao--principal">Solicitar diagnóstico</button></header>
<section class="aj-halo aj-halo--respira" style="padding:96px 56px 88px;display:grid;gap:28px;justify-items:start">
<span class="aj-rotulo">«METODO» · De advogado para advogado</span>
<h1 class="aj-titulo aj-titulo--display" style="max-width:15ch">Seu escritório como uma <b>empresa</b>. Lucrativa, previsível, escalável.</h1>
<p class="aj-subtitulo" style="font-size:18px;line-height:28px">Escolhemos com você um único produto jurídico e implementamos captação, processo comercial e dados em torno dele. Você executa o comercial; nós operamos o resto.</p>
<div style="display:flex;gap:12px"><button class="aj-botao aj-botao--principal aj-botao--lg">Solicitar diagnóstico gratuito</button><button class="aj-botao aj-botao--contorno aj-botao--lg">Ver como funciona</button></div>
<div style="display:flex;gap:48px;margin-top:40px;padding-top:28px;border-top:1px solid var(--linha);width:100%">
<div class="aj-indicador"><span class="aj-indicador__valor">50+</span><span class="aj-rotulo">escritórios atendidos</span></div>
<div class="aj-indicador"><span class="aj-indicador__valor">+R$ 100 mi</span><span class="aj-rotulo">em contratos fechados</span></div>
<div class="aj-indicador"><span class="aj-indicador__valor">90%</span><span class="aj-rotulo">com resultado</span></div></div>
</section></div>"""
comp('TelaLanding','Telas',760,
"""# TelaLanding
O topo da landing do site aplicando o sistema: halo que respira, título display com uma palavra em peso, uma ação principal e a prova em números.

Números e textos vêm do briefing do site («METODO», 50+ escritórios, +R$ 100 mi, 90%). Esta tela é referência de composição, não a página final.
""",LAND,' width=1280 page')
OPS=f"""<div class="aj aj-app" style="min-height:760px"{APP_ESC}>{barra_app()}{nav()}{VEU_APP}
<main class="aj-app__conteudo">
<div class="aj-app__cabeca">
<div><h1 class="aj-titulo">Bom dia, <b>Samuel</b></h1><p class="aj-subtitulo">Sexta, 26 de setembro · 4 alertas pedem sua atenção</p></div>
<div class="aj-app__acoes"><button class="aj-botao aj-botao--contorno">{ic('busca')}Buscar</button><button class="aj-botao aj-botao--principal">{ic('mais')}Novo cliente</button></div></div>
<div class="aj-indicadores">
<div class="aj-cartao aj-indicador"><span class="aj-rotulo">Clientes ativos</span><span class="aj-indicador__valor">42</span><span class="aj-indicador__variacao aj-indicador__variacao--sobe">+3 este mês</span></div>
<div class="aj-cartao aj-indicador"><span class="aj-rotulo">Contratos no mês</span><span class="aj-indicador__valor">318</span><span class="aj-indicador__variacao aj-indicador__variacao--sobe">+12% vs. agosto</span></div>
<div class="aj-cartao aj-indicador"><span class="aj-rotulo">Reuniões hoje</span><span class="aj-indicador__valor">6</span><span class="aj-ajuda">Próxima às 15h</span></div>
<div class="aj-cartao aj-indicador"><span class="aj-rotulo">Alertas abertos</span><span class="aj-indicador__valor">4</span><span class="aj-indicador__variacao aj-indicador__variacao--desce">2 em risco</span></div></div>
<div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap"><h2 class="aj-titulo aj-titulo--secao">Clientes que pedem <b>atenção</b></h2><span class="aj-etiqueta">Dados de exemplo</span></div>
{TAB}
<div class="aj-aviso aj-aviso--sucesso aj-app__aviso">{ic('ok','aj-aviso__icone')}<div><p class="aj-aviso__titulo">Relatório enviado</p><p class="aj-aviso__texto">Silva Previdenciário recebeu o resumo de setembro.</p></div></div>
</main></div>"""
comp('TelaSistema','Telas',780,
"""# TelaAJOps
O Início do «SISTEMA» aplicando o sistema: navegação lateral com os módulos reais, título com uma palavra em peso, indicadores, tabela com status e um aviso.

**O que você fornece:** `<div class="aj-app">` com a barra do celular (`aj-app__barra`), o `NavegacaoLateral`, o véu (`aj-veu aj-app__veu`) e `<main class="aj-app__conteudo">`; dentro, `aj-app__cabeca` (título e linha de contexto à esquerda, `aj-app__acoes` à direita, na mesma linha), `aj-indicadores` (4, depois 2 × 2, depois 1 coluna, pela largura do conteúdo) e a `Tabela`, que rola na própria caixa; o aviso da tela em `aj-app__aviso`. Abaixo de 1024 px o menu vira a barra do topo (o véu e o Esc fecham o menu, e o foco entra no primeiro item ao abrir). Título e ações dividem a linha só com 860 px de conteúdo ou mais (container query, nunca a largura da janela); com menos, as ações descem para baixo do título, à esquerda, com a principal primeiro, e com menos de 520 px empilham na largura da coluna.

Os módulos vêm do menu atual do «SISTEMA». Os números e escritórios da tela são dados de exemplo.
""",OPS,' width=1280 page')
COLS=[('Novo lead',[('Dra. Paula Reis','Previdenciário','há 2 h'),('Marcos Tavares Adv.','Trabalhista','há 5 h'),('Escritório Lima','Família','ontem')]),
 ('Qualificado',[('Rocha & Mendes','Previdenciário','há 1 dia'),('Dr. André Faria','Bancário','há 2 dias')]),
 ('Diagnóstico marcado',[('Nunes Advocacia','Trabalhista','amanhã, 10h'),('Castro & Pires','Previdenciário','seg., 14h')]),
 ('Proposta',[('Barbosa Adv.','Tributário','R$ 7.500/mês')]),
 ('Fechado',[('Silva Previdenciário','Previdenciário','R$ 8.000/mês')])]
def col(t,cs,i):
    h=f'<div class="aj-funil__coluna"><div class="aj-funil__cabeca"><span class="aj-rotulo">{t}</span><span class="aj-nav__contador">{len(cs)}</span></div>'
    for n,a,m in cs:
        et='<span class="aj-etiqueta aj-etiqueta--sucesso">Ganho</span>' if i==4 else ('<span class="aj-etiqueta aj-etiqueta--marca">Novo</span>' if i==0 else '')
        h+=f'<div class="aj-cartao" style="padding:14px;display:grid;gap:6px"><div style="font:600 14px/20px «FONTE_TEXTO»">{n}</div><div class="aj-ajuda" style="display:grid;gap:2px;color:var(--texto-2)"><span>{a}</span><span style="color:var(--texto-3)">{m}</span></div>{et}</div>'
    return h+'</div>'
CRMN=[('funil','Funil',True),('clientes','Contatos',False),('conversas','Conversas',False),('reunioes','Agenda',False),('relatorios','Relatórios',False),('config','Configurações',False)]
CRM=f"""<div class="aj aj-app" style="min-height:720px"{APP_ESC}>{barra_app('CRM')}
<nav class="aj-nav" aria-label="Principal" style="width:220px"><div class="{NAV_MARCA}">{SIMB()}<span>CRM</span></div>{''.join(f'<a class="aj-nav__item" href="#"{AC if a else ""}>{ic(i)}{t}</a>' for i,t,a in CRMN)}</nav>{VEU_APP}
<main class="aj-app__conteudo" style="padding-inline:32px;gap:20px">
<div class="aj-app__cabeca"><div><h1 class="aj-titulo">Funil de <b>vendas</b></h1><p class="aj-subtitulo">9 oportunidades abertas · R$ 58.400 em proposta</p></div>
<div class="aj-app__acoes"><span class="aj-etiqueta">Dados de exemplo</span><button class="aj-botao aj-botao--principal">{ic('mais')}Nova oportunidade</button></div></div>
<div class="aj-funil">{''.join(col(t,cs,i) for i,(t,cs) in enumerate(COLS))}</div>
</main></div>"""
comp('TelaCRM','Telas',740,
"""# TelaCRM
O funil do «CRM» aplicando o sistema: colunas em `superficie-2`, cartões brancos chapados, contadores e etiquetas só onde mudam a decisão.

Os nomes das colunas seguem um funil de vendas comum para escritórios; ajuste aos estágios reais do CRM. Todos os contatos são dados de exemplo.

**O que você fornece:** o mesmo `aj-app` da `TelaSistema` e o funil em `aj-funil` (uma `aj-funil__coluna` por estágio, com `aj-funil__cabeca`). O funil rola na horizontal dentro da própria caixa quando as colunas não cabem; no celular, uma coluna por tela, com a ponta da seguinte à vista.
""",CRM,' width=1280 page')
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'gen_comp_extra.py')).read())
for n,(pv,rd) in C.items():
    grava(os.path.join(DS,'components',n,'preview.html'),pv)
    grava(os.path.join(DS,'components',n,'README.md'),rd)
print(len(C),'componentes')
