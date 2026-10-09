# Molde de marca

O motor que gerou a marca da Anúncio Jurídico (AJ), transformado em molde para qualquer marca. Uma marca inteira sai de **um arquivo** (`marca.json`) e de **um texto de regras** (`regras.md`): tokens, CSS, pontes para shadcn e NossoCRM, os 37 componentes do Design System, o logo em todos os formatos e a skill de design da marca.

Usado pelo fluxo `identidade` do design-squad. Os agentes leem este arquivo inteiro antes de começar.

## Como montar um projeto

```
projetos/<slug>/
  marca.json                    ← copie de molde-marca/marca.exemplo.json e troque tudo
  identidade/simbolo/           ← o geômetra: gera.py + geometria.py + variantes.json + prancha
  identidade/logo/              ← copie molde-marca/logo/{gera_final.py,png.js,ico.py,video.js}
  interface/regras.md           ← copie molde-marca/interface/regras.tpl.md e preencha
  interface/fonte/              ← copie molde-marca/interface/fonte/ inteira
  interface/fonte/marca.css     ← opcional: a camada própria da marca (veja "Camada da marca")
  identidade/fotos/             ← opcional: fotos aprovadas (marca de pessoa); vão para assets/fotos/ da skill
  aplicacoes/                   ← modelos de peça em HTML (landing, evento, slides, og, instagram, e-mail...);
                                  vão para assets/modelos/ da skill, então usam ../css, ../fotos e ../logos
  skill/<nome-da-skill>/        ← gerada; nunca editar à mão
```

Ferramentas (uma vez por máquina): `molde-marca/ferramentas/instalar.sh` → `~/.cache/design-squad-identidade` (Python com fonttools, uharfbuzz, pillow, pymupdf; Node com playwright e ffmpeg-static). Use `~/.cache/design-squad-identidade/.venv/bin/python` e `FERRAMENTAS=~/.cache/design-squad-identidade node`.

## Ordem de geração

1. **Logo** (dentro de `identidade/logo/`): `gera_final.py` → `png.js` → `ico.py` → `video.js`. O `.ttf` da fonte de título é baixado sozinho de `fontes.titulo.ttf_url`. Marca **só tipográfica** (`simbolo: null`): os mesmos quatro scripts geram nome em linha, empilhado, assinaturas extras, ícone de letra, favicon na grade de 16 e o vídeo do nome entrando; os campos estão no topo de `gera_final.py` (exemplo real: `projetos/kleiciane-rocha/marca.json`). Marca **com símbolo, nome em mais de uma linha e sem luz** (exemplo real: `projetos/almeida-nascimento/marca.json`): veja "Marca com símbolo: nome em linhas, alinhamento óptico e sem luz (logo)" abaixo.
2. **Sistema e skill**: `python3 interface/fonte/gerar.py` roda `gen_tokens` → `gen_css` → `gen_comp` → copia `regras.md` para o README do Design System → `gen_skill`. Marca só tipográfica: rode o logo **antes**, porque os componentes leem o logotipo de `identidade/logo/assinatura/`.
3. **Testes** (todos precisam passar antes de mostrar ao usuário):
   - `verificacao/contraste.py marca.json` — todos os pares de texto e controle, nos dois temas;
   - `verificacao/sobras.py <projeto>` — nenhum `[[ESCREVA]]`, `«MARCADOR»`, comentário de molde ou resto da AJ;
   - `verificacao/pdf_quebra.js <documento.html> <pasta>` + `pdf_quebra.py <pasta>` — nenhum cabeçalho sozinho no pé em 23 posições (o arquivo é aberto pelo endereço, então serve também para modelo que liga CSS externo, como uma apostila em `assets/modelos/`);
   - `verificacao/prancha.js <skill> <pasta> [--marca marca.json]` — renderiza cada componente (claro e escuro) e lista rolagem lateral. **Todos em 1280, 390 e na largura mínima (`largura_minima`, padrão 360 px), e as `Tela*` também em 1024 e 800** (até 07/10/2026 as telas só saíam em 1280 e 390, e o título do painel espremido entre 1024 e 1200 px passou como verde). Cada prévia abre de um arquivo com `<base>` na pasta da skill, então o código de referência pode usar `assets/fotos/...` e `assets/logos/...`;
   - `verificacao/piso.js <skill> <pasta> --marca marca.json --modelos <skill>/assets/modelos/<tela>.html ...` — o piso de leitura e de toque, em todo componente (1280, 390 e a largura mínima; as `Tela*` também em 1024 e 800; claro e escuro) e nas telas inteiras (login, formulário, documento, em 1440, 1024, 390 e a mínima; a que tem `data-theme="aparelho"` também com o aparelho no escuro): nenhum texto abaixo de 14 px (no gráfico, o corpo renderizado), nenhum alvo de toque abaixo de 44 × 44 px (link dentro de frase fica fora; caixa de marcar conta pelo rótulo), nenhuma pílula fora do avatar quando o marca.json diz `"pilula": false`, **nenhuma palavra sozinha na última linha** de título, pergunta, linha de contexto (`subtitulo`) ou botão (`SOZINHA`; espaço sem quebra junta palavras) e **nenhum item sozinho na última linha de uma grade** (atalhos, grades, indicadores, sumário, frentes: `ORFAO`; o item que ocupa a linha inteira de propósito não conta); avisa (sem reprovar) corpo menor que o `corpo` fora da escala do `tipo`. Rode os modelos **de dentro da skill** (eles ligam `../css`).
4. **Publicação**: `publicar/publicar.py <projeto>` (mostra o plano) → `--executar` → `--github` só com o sim do usuário.

## marca.json, campo a campo

| Campo | O que é |
|---|---|
| `nome`, `sigla` | Nome completo com acento e a forma curta ("Anúncio Jurídico", "AJ"). |
| `prefixo` | 2–3 letras minúsculas. Vira o prefixo de toda classe e variável (`aj-botao`, `--aj-fundo`) e dos arquivos (`aj-tokens.css`). |
| `slug`, `versao` | Pasta do projeto; versão da identidade (vai para a skill e o manifesto). |
| `produtos` | Nomes que aparecem nos exemplos de tela: `sistema`, `crm`, `metodo`. Opcional. |
| `fontes` | Família e pilha de título e de texto, pesos, `url` do Google Fonts e `ttf_url` da fonte de título (para converter o nome em curvas). Se alguma linha ou trecho do logo for itálico: `ttf_url_italico` (o arquivo itálico da mesma família; é baixado só quando pedido). |
| `papeis` | Quais cores fazem cada papel fixo: `primaria`, `primaria_forte`, `escuro`, `escuro_claro` (o tom do degradê do fundo escuro), `luz`, `realce_claro`, `fundo_claro`, `nevoa`. Nome de cor ou hex. |
| `cores` | As cores da marca com nome próprio, hex e uso. |
| `semanticos` | Os 27 tokens que os componentes usam, com valor no claro e no escuro (hex, rgba, `{nome-de-cor}` ou `{outro-token}`). A lista é obrigatória e é conferida por `fonte.py`. Marca só tipográfica: `logotipo` no lugar de `simbolo`. Marca sem luz: `halo-1`, `halo-2` e `brilho` saem da lista (use as vagas para tokens da própria marca, ex. `enfase`, `moldura`, `janela`). |
| `escala` | 50 a 950 da cor principal, para sistemas que pedem escala. |
| `tipo` | Estilos de título e de texto (tamanho, entrelinha, peso, espaçamento, uso). |
| `curva`, `tempo_assinatura` | A curva de toda animação e a duração do movimento-assinatura do símbolo. |
| `simbolo` | `pecas` (paths numa caixa 100×100, uma por peça), `pequeno` (versão para 24 px ou menos), `entrada` (de onde cada peça chega na animação). Opcionais, calculados da geometria do símbolo: `linhas_opticas` `{topo, base}` (onde o nome se alinha) e `grade_pequeno` `{x, y}` (as linhas da versão pequena que o favicon põe em pixel inteiro). Gerado pelo geômetra, nunca digitado. `null` quando a marca é só tipográfica. |
| `luz` | Opcional. Sem o campo, a marca tem halo e brilho (como a AJ). `false`: sem luz — as classes `aj-halo`, `aj-halo--respira` e `aj-brilho` saem do CSS e das prévias e os tokens de luz deixam de ser obrigatórios. |
| `contraste_extra` | Opcional. Pares próprios da marca que `contraste.py` também mede: `[["enfase", "moldura", 3, "só letra grande"], ...]` (token, cor da marca ou hex de cada lado, e o mínimo). |
| `distancia_extra` | Opcional. Distância mínima de cor (ΔE CIELAB) entre dois tokens, medida por `contraste.py` nos dois temas: `[["critico", "enfase", 20, "o erro não pode parecer a palavra em destaque"], ...]`. Use quando duas cores de papéis diferentes ficam perto (exemplo real: o crítico do escuro da Kleiciane Rocha era a ênfase clareada, ΔE 6). |
| `logo` | Com símbolo: texto da assinatura, peso, espaçamento, cores do símbolo por arquivo e combinações símbolo+nome; opcionais `linhas`, `horizontal`, `vertical`, `icone`, `avatar`, `cenas`, `respiro_fracao`, `minimos` (seção abaixo). Só tipografia: `trechos` (cada pedaço do nome com os próprios eixos da fonte variável, ex. `wght` e `wdth`), `empilhado`, `kerning_optico`, `extras`, `combinacoes` com os fundos de uso (contraste medido; abaixo do mínimo não gera), `icone` (a letra do favicon) e `cenas` do vídeo. |
| `publicacao` | Nome da skill, pastas de destino, repositório GitHub e pasta de guarda. Opcional `logos_png: true`: a skill leva também os PNG do logo e o `avatar/` (para e-mail, WhatsApp e redes). |
| `rotulo` | Opcional. Sem o campo, rótulo em caixa alta espaçada (a AJ). `{"caixa": "baixa", "italico": true, "familia": "texto"}`: todo rótulo do sistema (rótulo, cabeçalho de tabela, grupo de menu e de navegação, topo das etapas, coluna do rodapé) passa a usar o estilo `rotulo` do `tipo`, sem transformar a caixa. |
| `vocabulario_proprio` | Opcional. Palavras do setor da marca que a lista de restos da AJ do `sobras.py` acusaria, cada uma com o motivo: `[["advogado", "os sócios são advogados"], ...]`. Para cliente que é escritório de advocacia. |
| `modelos` | Opcional. Padrões (glob, relativos a `aplicacoes/`) de peças prontas em subpastas (PDF, DOCX, HTML, fontes) que vão para `assets/modelos/` no mesmo caminho relativo: `["propostas/*.pdf", "_fontes-pdf/*.ttf"]`. |
| `espaco`, `raio`, `sombra`, `quebra` | Opcionais. Sem eles, valem os padrões do sistema (os da AJ). |
| `piso` | Opcional. Sem o campo, ligado: o bloco `/* @se piso */` do `bundle.tpl.css` põe todo texto do sistema em 14 px ou mais e todo alvo de toque (botão, inclusive o pequeno, botão de ícone, campo, item de menu e de navegação, aba, filtro, atalho, página, link de trilha, cabeçalho e rodapé, caixa de marcar com o texto) em 44 × 44 px ou mais. `false` só na AJ (`marca.exemplo.json`), que nasceu antes da regra. Marca nova nunca desliga. |
| `largura_minima` | Opcional, padrão 360. A menor largura de tela suportada (px): `piso.js` e `prancha.js` testam 1280, 390 e esta (as `Tela*` também 1024 e 800). |
| `croma_maximo` | Opcional. Croma CIELAB máximo de um token, num tema: `[["dado-2", 40, "escuro", "motivo"], ...]` (`"claro"`, `"escuro"` ou `"ambos"`), medido por `contraste.py`. Para cor de dados ou status que não pode lembrar uma cor proibida (junto de `distancia_extra` contra o hex dela). |
| `pilula` | Opcional. `false` = a marca não tem pílula (só o avatar é redondo): `verificacao/piso.js` acusa qualquer elemento comprido de canto redondo. Use os tokens de raio na camada da marca para filtro, contador, progresso e interruptor. |

## Marca só tipográfica e marca sem luz (interface)

O mesmo motor gera as duas famílias de marca; a AJ (símbolo e luz) continua saindo **idêntica** (provado em 02/10/2026: o molde rodado com `marca.exemplo.json` e `exemplo-aj/` antes e depois da mudança dá `diff -r` vazio, exceto a correção de uma linha da ponte shadcn, `--ease-out: var(--aj-curva-marca)`, que antes apontava para uma variável que não existia).

- **`simbolo: null`** — `fonte.logotipo(forma)` lê o logotipo em curvas de `identidade/logo/assinatura/<forma>-<cor>.svg` (gerado por `gera_final.py`) e o põe inline com a classe `aj-logotipo`, pintado pelo token `logotipo`. Nos componentes, `SIMB()` devolve o logotipo e `MARCA_NOME()` não repete o nome em texto ao lado dele. O componente **Simbolo vira Logotipo** (em linha, empilhado e escuro) e o **Carregando** vira o nome entrando como no vídeo de abertura, a partir de `logo.trechos[].entrada` (texto vivo na fonte variável, animando `font-variation-settings` com as variáveis locais `--fv`/`--dfv`/`--dx`/`--dy`). O marcador `«LOGOTIPO_ALTURA»` dá a altura do logotipo em linha na largura mínima (`logo.empilhado.usar_abaixo_de_px`, padrão 200 px). O avatar de uma marca de pessoa é a foto: ponha as aprovadas em `identidade/fotos/`.
- **`luz: false`** — sem halo nem brilho; `comp()` tira as classes de luz das prévias e o modelo de documento sai sem `aj-halo`.
- **Blocos condicionais do `bundle.tpl.css`** — linhas entre `/* @se simbolo */`, `/* @se tipografica */`, `/* @se luz */` (ou várias condições juntas, `/* @se luz simbolo */`), com `/* @senao */` opcional, até `/* @fim */`. `fonte.condicional()` deixa só o que vale para a marca; as linhas dos marcadores sempre saem.

## Marca com símbolo: nome em linhas, alinhamento óptico e sem luz (logo)

Acrescentado em 06/10/2026 no projeto almeida-nascimento (símbolo + "Almeida Nascimento" em Literata 500 sobre "Advocacia" em itálico, cor de apoio). Tudo opcional: sem estes campos, o caso com símbolo sai **idêntico** ao da AJ (provado em 06/10/2026: `gera_final.py` → `png.js` → `ico.py` → `video.js` com `marca.exemplo.json`, antes e depois, dá os mesmos SVG, PNG, ICO e MP4 byte a byte; a Kleiciane Rocha, só tipográfica, também sai igual). Detalhe de cada campo no topo de `gera_final.py`, `png.js` e `video.js`.

- **`logo.linhas`** — o nome em uma ou mais linhas, cada uma com os próprios eixos da fonte variável, `italico`, `tracking` e `corpo` (relativo ao da primeira). As linhas se alinham pela borda da **tinta** (na vertical, pelo centro da tinta).
- **`logo.horizontal`** `{proporcao, intervalo}` — alinhamento óptico: o topo da maiúscula da 1ª linha cai em `simbolo.linhas_opticas.topo` e a linha de base da última em `simbolo.linhas_opticas.base`; `proporcao` (caixa do símbolo / corpo da 1ª linha) fixa o tamanho e a entrelinha sai disso. `intervalo` em alturas do símbolo (altura da tinta). **`logo.vertical`** `{proporcao, intervalo}`: símbolo centrado sobre as linhas, mesma entrelinha.
- **`logo.combinacoes`** também aceita `{nome: {"simbolo": cor, "linhas": [cor, cor], "fundo": cor}}` — cada linha com a sua cor; o contraste de cada uma é medido no fundo e, abaixo de `contraste_minimo`, a combinação não é gerada.
- **`logo.icone`** (com símbolo) `{cor, fundo, raio, caixa, pequeno, favicon: {lado, largura, raio}, variantes}` — ícone de app e favicon chapados, com a versão pequena; com `simbolo.grade_pequeno`, o favicon é desenhado na grade. **`logo.avatar`** `{caixa, pequeno, cenas}` e **`logo.cenas`** `{nome: {fundo, cor}}`: avatar e vídeo de fundo chapado, sem halo nem brilho (marca com `luz: false`).
- **`medidas.json`** passa a sair também no caso com símbolo quando há `linhas` ou `icone`: corpos, proporção, entrelinha, alinhamento, respiro (`respiro_fracao` da altura do símbolo), mínimos em px (`minimos.menor_corpo_px`: o corpo da menor linha no menor tamanho da assinatura), contraste e a geometria do favicon.
- O `kerning_optico` do caso 2 vale também para `linhas` (pares com espaço ficam fora). Cuidado: ele mede área de branco e foi pensado para sans; numa serifa de texto ele acusa o espaçamento clássico (haste com haste mais aberta, redondo com redondo mais fechado). Na Almeida Nascimento foi medido e **não** ligado.
- ~~Pendente no sistema: o Carregando com símbolo move só a primeira e a última peça.~~ Resolvido em 06/10/2026 (seção abaixo): com mais de duas peças, cada uma chega de `simbolo.entrada`.

## Sistema para marca com símbolo e nome em linhas, rótulo sem caixa alta e formulário-isca (06/10/2026)

Acrescentado no estágio 6 do projeto almeida-nascimento. Tudo é genérico e opcional; a AJ e a Kleiciane Rocha saem iguais, a não ser pelos acréscimos e por duas correções declaradas (prova em 06/10/2026, molde antes × depois com `marca.exemplo.json` + `exemplo-aj/` e com o marca.json da Kleiciane: `diff -r -x fonte` mostra só o bloco v2.3 acrescentado ao fim do CSS, os textos e prévias novos de `Campo`, `Indicador`, `FormularioEtapas` e `Modal`, e as duas linhas corrigidas de `.aj-campo`).

- **Rótulo sem caixa alta.** Campo `rotulo` no marca.json (tabela acima). No `bundle.tpl.css`, cada regra de rótulo tem a versão em caixa alta entre `/* @se caixa-alta */` e a versão pelo estilo do `tipo` em `/* @senao */`, com os marcadores `«ROTULO_FONTE»` (fonte inteira, com itálico e família) e `«ROTULO_ESPACO»`. Use os mesmos marcadores na camada da marca.
- **Assinatura inline.** Com símbolo e `logo.linhas`, `fonte.assinatura(forma)` devolve a assinatura oficial em curvas (de `identidade/logo/assinatura/`) com a classe `aj-assinatura`: o símbolo e a 1ª linha pintam com o token `simbolo`, as linhas seguintes com `texto-2`. `MARCA_NOME()` e o topo do `documento.html` usam a assinatura no lugar de símbolo + nome digitado. O CSS fica no bloco `/* @se linhas */`.
- **Carregando com mais de duas peças.** Cada `path` ganha `--dx`/`--dy` de `simbolo.entrada` (unidades da caixa 100, as mesmas do vídeo). Com duas peças (a AJ), nada muda.
- **`«SIMBOLO_MASCARA»`.** O símbolo como `mask-image` (data URI das peças): para o símbolo grande de capa ou o lugar do selo, pintado pelo fundo do elemento (um token), sem colar geometria no CSS.
- **Formulário-isca (bloco v2.3 do `bundle.tpl.css`).** `aj-etapas-tela` (tela inteira) com `aj-trilho` (marca, `aj-trilho__contador` "03 / 05", `aj-trilho__etapas` com `aria-current`, `aj-trilho__nota`) no computador e `aj-etapas-barra` no celular (abaixo de 1024 px); `aj-atalhos`/`aj-atalho` (valores prontos, `aria-pressed`); `aj-moeda` + `aj-entrada--grande` (campo de dinheiro com o prefixo dentro); `aj-comparacao` (dois valores, neutros, o do resultado com o fio em cima); `aj-resultado` (rótulo, número, linhas `dt`/`dd`, ressalva); `dialog.aj-modal` e `aj-modal--leitura` (ajuda e política de dados). Documentados nos README de `Campo`, `Indicador`, `FormularioEtapas` e `Modal` e na seção "Formulário em etapas e resultado" do `regras.tpl.md`. O fio de resultado usa `acao` no sistema; a marca troca pela cor dela na camada própria.
- **Correções declaradas.** `.aj-campo` ganhou `align-content: start` (numa grade de campos, o campo sem ajuda esticava o vão entre rótulo e controle) e o rótulo do campo passou a ser `.aj-campo > label:not([class])` (uma caixa de marcar dentro do campo herdava a letra do rótulo).
- **`sobras.py`:** `vocabulario_proprio` libera palavras do setor da marca; a lista da AJ ganhou restos dos textos de exemplo (Previdenciário, Trabalhista, tráfego pago, contas de anúncio, custo por lead), que um escritório cliente liberaria sem querer ao liberar "escritório" e "advogado".
- **`gen_skill.py`:** `modelos` (peças prontas em subpastas de `aplicacoes/`, no mesmo caminho relativo) e `publicacao.logos_png`.
- **`gerar.py`:** se existir `aplicacoes/gera_modelos.py`, ele roda antes da skill (modelos de tela gerados por script, com o símbolo e a assinatura do sistema).

Exemplo real de tudo isso: `projetos/almeida-nascimento/` (`marca.json`, `interface/regras.md`, `interface/fonte/marca.css`, `aplicacoes/gera_modelos.py`, `SISTEMA.md`).

## Acréscimos da auditoria 1 da Almeida Nascimento (07/10/2026)

A primeira auditoria independente de uma marca nova (projeto almeida-nascimento) achou o painel sem versão de celular, alvos e corpos abaixo do piso, uma pílula, restos da AJ em `rgba()`, e testes que deixaram tudo passar. O que era genérico entrou aqui; o que era da marca ficou na camada dela.

- **`bundle.tpl.css` › v2.4 (fim do arquivo):**
  - **painel do computador ao celular** (classes novas, nada muda nas antigas): `aj-app` (menu lateral + conteúdo), `aj-app__barra` (abaixo de 1024 px: a marca e o botão de menu de 44 px, que abre o menu como painel à esquerda com `data-menu="aberto"` e o véu `aj-veu aj-app__veu`), `aj-app__conteudo` (contêiner), `aj-app__cabeca` + `aj-app__acoes` (título e ações na mesma linha a partir de 1024 px; abaixo de 760 px as ações descem, a principal primeiro), `aj-indicadores` (4 → 2 × 2 → 1 pela largura do conteúdo, com rótulo, número e nota alinhados por subgrid), `aj-funil` (colunas de 180 px no mínimo, rolando na própria caixa; no celular, uma por tela), `aj-app__aviso`. `TelaSistema` e `TelaCRM` do `gen_comp.py` usam essas classes (nada de layout em estilo solto);
  - **gráfico**: `tracejada` e `pontilhada` (a forma também separa as séries: impressão em preto e branco, tritanopia), amostra da linha na legenda, e o par `aj-grafico__desenho--largo` / `--estreito` (o cartão é contêiner e troca de desenho abaixo de 480 px: nunca o desenho do computador encolhido no celular);
  - **piso** (`/* @se piso */`, campo `piso`): 14 px e 44 px, como na tabela acima.
- **Limpeza da camada base** (a AJ continua igual na tela, com as diferenças abaixo): `#FFFFFF` do botão de perigo → `sobre-acao`; a bolinha do interruptor → `superficie` (no escuro, `texto`); o fundo do botão de tocar vídeo `rgba(252,251,255,.92)` (o Branco quente da AJ, que ia para toda marca) → `superficie`, e a cor do triângulo → `acao`; o degradê do vídeo só em marca com luz (sem luz: `superficie-2`); `999px` → `var(--raio-pilula)`; o anel de foco do campo e da seleção afastado 2 px (a regra escrita; estava em 1 px); `font-size:13px` solto no topo do `documento.html`.
- **Tema do aparelho** (`gen_tokens.py`, `gen_css.py`): `data-theme="aparelho"` no `<html>` faz a tela seguir o modo do aparelho, sem script (os tokens do escuro dentro de `@media (prefers-color-scheme: dark)`, e cada regra `[data-theme="escuro"] …` ganha a gêmea `[data-theme="aparelho"] …` no mesmo `@media`).
- **`gen_skill.py`**: título das regras e dos tokens com o nome da marca (não a sigla); pesos da fonte uma vez só quando título e texto são a mesma família; os vídeos de `identidade/logo/movimento/*.mp4` vão para `assets/movimento/`.
- **`regras.tpl.md`**: número principal por bloco e número de apoio; ordem única de lista fixa da marca (novo `[[ESCREVA]]`); tom derivado só como token; tema do aparelho; piso de 14 px na tela e piso no papel (corpo 10 pt, ressalva 9,5 pt, apoio técnico 8 pt, cartão 7 pt); título sem palavra sozinha também no PDF e no DOCX; painel no celular; contador num formato só e ações da etapa à esquerda; gráfico com forma e desenho de celular; alvo de toque de 44 px; PNG do logo de e-mail com fundo; papel de impressora sem chão.
- **`verificacao/`**: `prancha.js` renderiza as `Tela*` também em 390 px; `piso.js` (novo); `sobras.py` lê cor da AJ escrita em `rgb()`/`rgba()`, varre também `interface/design-system/publicado/` (a cópia do que foi publicado: publicado defasado é sobra), ignora o registro de publicação (`"by"`, `"at"` do `design-system.json`) e conta nomes que são palavra inteira (Sora, noite, dobra…) só como palavra ("impressora" não é a Sora).

**Prova** (molde antes × depois, `marca.exemplo.json` + `exemplo-aj/`, `diff -r -x fonte`): mudam só o `aj-tokens.css` (o bloco do aparelho, acrescentado), o CSS dos componentes (as linhas da limpeza acima, o bloco v2.4 sem o piso e o bloco do aparelho), as prévias e os README de `TelaSistema`, `TelaCRM` e `NavegacaoLateral`, o `documento.html` (o CSS e o 13 px), os títulos de `regras.md` e `tokens.md` da skill e a frase do tema do aparelho no `tokens.md`. A Kleiciane Rocha (só tipográfica) gera sem erro; como não tem o campo `piso`, ganha o piso ao copiar o molde de novo: confira com `piso.js` antes de publicar.

**Exemplo AJ em 390 px**: com as `Tela*` agora testadas no celular, `TelaSistema` e `TelaCRM` passam; `CabecalhoSite`, `MenuSuspenso`, `Indicador` e `TelaLanding` do exemplo AJ ainda acusam rolagem lateral, porque as prévias da AJ põem as variantes de computador e celular lado a lado ou usam layout em estilo solto (textos da AJ v2.3). Marca nova reescreve essas prévias; confira cada uma na prancha.

## Acréscimos da auditoria 2 da Almeida Nascimento (07/10/2026)

A segunda auditoria achou o título do painel espremido até sobrar uma palavra (entre 1024 e 1200 px de janela), o quinto atalho sozinho na segunda linha, links de 44 px desalinhando a linha, o modal do celular com ações em escada, o Esc que não fechava o menu, a cor de dados do escuro lendo como dourado, títulos do DOCX no peso 400 e restos de ideias da AJ em comentários. Os testes não pegavam nenhum deles. O que era genérico entrou aqui:

- **`bundle.tpl.css`:**
  - **cabeçalho do painel pela largura do conteúdo** (v2.4, container query no `aj-app__conteudo`, que já era contêiner): título e ações na mesma linha só com 860 px de conteúdo ou mais; com menos, as ações descem para baixo do título, à esquerda, a principal primeiro; com menos de 520 px, empilham. Substitui a regra pela janela (`@media (max-width: 760px)`), que deixava o título espremido entre 1024 e 1200 px;
  - **atalhos** (v2.3): grade de uma linha, colunas iguais, valor centrado e 8 px de lado (eram `flex-wrap` com 14 px); no celular (até 760 px), três colunas (5 = 3 + 2; 4 = 2 + 2, por `:has()`);
  - **piso**: a linha onde um link cresce até 44 px centraliza tudo (`.aj-trilha ol`, `.aj-trilha li`, `.aj-rodape__base`, `.aj-cabecalho__links` com `align-items: center`);
  - **v2.5 (novo, no fim):** ações do modal e do pé do painel lateral empilhadas no celular (até 480 px), a principal primeiro (`column-reverse`, porque o HTML é cancelar → ação); alerta com ação no celular (até 560 px), o botão embaixo do texto;
  - comentários neutros no lugar de "UMA palavra em peso (a assinatura da voz)" e "Símbolo e as duas luzes" (iam para toda marca).
- **`gen_comp.py`** (exemplo AJ): o menu do celular das `Tela*` fecha com o Esc (`APP_ESC` no `aj-app`), o botão alterna "Abrir menu"/"Fechar menu" com `aria-expanded`, o foco entra no primeiro item ao abrir e volta ao botão ao fechar (`MENU_JS`); o véu fecha pelo mesmo caminho. README de `TelaSistema` e `NavegacaoLateral` dizem isso e a regra do cabeçalho pelo conteúdo.
- **`regras.tpl.md`**: cabeçalho do painel pelo conteúdo e o "·" da linha de contexto; Esc e foco do menu; atalhos numa linha; chamada depois do resultado sem cartão; cor de dados que lembra cor proibida (medida); rótulo direto no centro da marca e `aria-label` com os valores certos; largura mínima de 360 px; alvo de 44 px sem mudar a linha de base; modal, painel e alerta no celular; palavra da tese com um sentido só; papel timbrado de impressão só com cabeçalho e pé; título de DOCX em instância estática.
- **`verificacao/`**: `piso.js` com `SOZINHA` (palavra sozinha na última linha de título, pergunta, linha de contexto e botão), `ORFAO` (item sozinho na última linha de grade) e as larguras novas (1280, 390, mínima; `Tela*` também 1024 e 800; modelos em 1440, 1024, 390 e mínima); `prancha.js` com as mesmas larguras; `contraste.py` com `croma_maximo`; `sobras.py` acusa "palavra em peso" e "luzes" (outra marca libera em `vocabulario_proprio`). Controle negativo: o `piso.js` novo, rodado na skill da Almeida Nascimento de antes desta passada, acusa os casos da auditoria ("Bom dia, / Marina" em 1024 e 800, "Funil da / equiparação" em 1024, o estado vazio em 390, o botão do WhatsApp em 390, os atalhos 4 + 1).

**Prova** (molde antes × depois desta passada, `diff -r -x fonte`): **AJ** (`marca.exemplo.json` + `exemplo-aj/`) muda só o CSS dos componentes (os dois comentários, os atalhos, o cabeçalho do painel por container query no lugar do `@media` de 760 px, o bloco v2.5) e, por isso, o `documento.html`; as prévias de `TelaSistema` e `TelaCRM` (Esc e foco do menu) e os README de `TelaSistema` e `NavegacaoLateral`. O bloco do piso não muda a AJ (`"piso": false`). **Kleiciane Rocha** (o projeto com os geradores genéricos do molde de antes, trocando só o `bundle.tpl.css`) muda só o CSS dos componentes (o mesmo, mais o alinhamento do piso, que ela tem ligado) e o `documento.html`; a planilha muda só a data de criação dentro do arquivo. Nenhuma outra linha.

## Camada da marca (`interface/fonte/marca.css`)

O que a marca muda no sistema (ênfase de cor em vez de peso, botão em pílula, canto reto, a moldura, o topo da landing) vai num arquivo opcional, `interface/fonte/marca.css`, que `gen_css.py` acrescenta **depois** do `bundle.tpl.css` (vence pela ordem). Escreva como o bundle: classes `aj-*` e tokens sem prefixo (`var(--fundo)`), com os mesmos marcadores (`«PILHA_TITULO»`); o gerador troca tudo para o prefixo da marca. Nenhum valor de cor solto. Cada regra de sistema que a marca muda precisa do motivo registrado em `DIRECAO-MARCA.md`. Exemplo real: `projetos/kleiciane-rocha/interface/fonte/marca.css`.

## O que é sistema e o que é marca

- **Sistema** (vale para toda marca, aprendido na AJ): os 37 componentes e o CSS deles, os três modelos de composição, "cartão só agrupa", nada de item órfão, regras de documento e PDF, camadas, acessibilidade. Está pronto em `bundle.tpl.css`, nos geradores e no texto de `regras.tpl.md`.
- **Marca** (muda sempre): tudo no `marca.json`, cada `[[ESCREVA]]` dos modelos, e os **textos de exemplo** e frases dos README dos componentes em `gen_comp.py` e `gen_comp_extra.py`, que vieram da AJ (escritórios de advocacia, violeta, "a dobra"). O `sobras.py` lista cada um que faltar reescrever.

## Exemplo completo

`exemplo-aj/` tem a plataforma, a direção, as regras e os modelos da skill preenchidos para a AJ, e `marca.exemplo.json` tem o marca.json da AJ. Rodar o molde com eles reproduz o sistema da AJ (testado: tokens e componentes iguais, com os nomes genéricos `curva-marca` e `tempo-assinatura`).

Exemplo de marca **só tipográfica e sem luz**, com camada própria, fotos e modelos de peça: `projetos/kleiciane-rocha/` (`marca.json`, `interface/regras.md`, `interface/fonte/`, `aplicacoes/`, `SISTEMA.md`).

Para provar que uma mudança no molde não muda a AJ: monte uma pasta temporária com `interface/fonte/` (do molde), `marca.json` = `marca.exemplo.json`, `interface/regras.md` = `exemplo-aj/regras-README.md` e os três `exemplo-aj/*.tpl.md` dentro de `interface/fonte/`; rode `gerar.py` antes e depois e compare com `diff -r -x fonte`.

## Quando o molde muda

Se um projeto descobrir uma regra ou um componente que faltava, ele entra **aqui** (no `bundle.tpl.css`, nos geradores ou no `regras.tpl.md`), para a próxima marca já nascer com ele.


## Crédito da agência

Documento de entrega (manual, apresentação, README do Design System) pode levar o crédito "Anúncio Jurídico"; peça da marca do cliente, nunca. Marque a linha do crédito com `<!-- credito-agencia -->` (ou a palavra `credito-agencia` num atributo) para o `sobras.py` não acusar. Decisão de Samuel em 03/10/2026, no projeto kleiciane-rocha.
