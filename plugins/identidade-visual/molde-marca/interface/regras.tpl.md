[[ESCREVA: a sensação da marca em uma linha (ex.: "Tecnologia que acolhe: precisa, calma e plana."), seguida de uma frase sobre o que a marca é para o cliente e onde estas regras valem (site, landing, sistemas, apresentações, posts).]]

<!--
MOLDE (pt-BR): este é o README do Design System, que vira `referencias/regras.md` na skill da marca.
- O que está escrito sem marcador são regras de SISTEMA, aprendidas na marca AJ, e valem para qualquer marca.
  Só mude com motivo, e registre o motivo em DIRECAO-MARCA.md.
- Cada [[ESCREVA: ...]] é regra da MARCA e tem de ser preenchido. A auditoria reprova se sobrar um.
- Exemplo preenchido: molde-marca/exemplo-aj/regras-README.md.
- Apague este comentário ao terminar.
-->

## Princípios

[[ESCREVA: 3 a 5 princípios, cada um com um nome em negrito e uma frase que diga o que fazer e o que nunca fazer. Um deles define a cor (quantas cores a marca tem e quais são neutras); outro define a "luz" ou o tratamento de fundo, se houver. O último é sempre: **Uma ousadia por tela.** Uma ação principal, uma ênfase no título, um efeito. O resto fica quieto.]]

## Voz e conteúdo

- [[ESCREVA: com quem a marca fala e em que pessoa ("você", "o seu negócio").]]
- Frase curta, uma ideia por frase. Português do Brasil sempre, com acento.
- Em título, uma ênfase: a palavra que carrega o sentido. No máximo duas quando o título traz um número e um resultado; nunca três. [[ESCREVA: 2 ou 3 exemplos reais de título da marca com a ênfase marcada em negrito.]]
- Botão é verbo + objeto e diz o que acontece ("Salvar cliente"). O aviso repete o verbo no particípio ("Cliente salvo").
- **Palavra da tese tem um sentido só.** O nome que a marca dá ao que ela pensa (as frentes, os pilares) não vira nome de serviço, de campo ou de coluna, e vice-versa.
- Erro explica o que houve e como resolver, sem desculpas.
- Número real quando houver prova. Nunca promessa sem prova.
- **Um número principal por bloco; o resto é apoio.** O resultado (o número que a pessoa veio buscar) é o único grande e o único com o destaque. Outro número no mesmo bloco (projeção, ilustração) vem menor, sem o destaque, com rótulo que diz o que ele é e de que período e uma linha que diz como foi feito; a ressalva do bloco cobre os dois, uma vez. O que se ganha daqui em diante e o que se recupera do passado nunca se misturam: cada um tem o próprio rótulo.
- **Lista fixa da marca (frentes, serviços, pilares) tem uma ordem só**, a da plataforma, em todo lugar: menu, site, documento, proposta, post, opções de formulário, `empresa.md`. [[ESCREVA: a lista e a ordem, se a marca tiver uma; senão apague esta frase.]]
- Nunca: [[ESCREVA: jargões, clichês visuais e verbais do setor da marca que ela recusa]], exclamação de enfeite, emoji.

## Cor

- Chão da página e do app: `fundo`. Cartões, tabelas, menus e campos: `superficie`. Faixas, cabeçalho de tabela e hover: `superficie-2`.
- Texto principal `texto`; apoio `texto-2`; placeholder e metadado `texto-3`. Todos passam 4,5:1 sobre `fundo`, `superficie` e `superficie-2` nos dois temas.
- Ação principal `acao` com texto `sobre-acao`; hover `acao-hover`. Item ativo e botão secundário: `realce` com texto `sobre-realce`.
- Status sempre com palavra: `sucesso`/`sucesso-fundo`, `atencao`/`atencao-fundo`, `critico`/`critico-fundo`. Informação usa `acao`.
- Divisórias `linha`. Borda de controle `borda-controle` (3:1).
- **Tom derivado só existe como token semântico, nunca como matiz novo.** Superfícies, hover, texto de apoio e as cores do tema escuro saem das cores da marca (mistura ou um passo da mesma cor), cada uma com papel fixo e contraste medido. Liste-os na regra da marca. Precisou de um tom que não está lá: ele entra no marca.json como token antes de ir para a tela.
- **Tela que segue o tema do aparelho** (login, área do cliente, painel): `data-theme="aparelho"` no `<html>`. Os tokens trocam para o escuro sozinhos com o aparelho no modo escuro (`prefers-color-scheme`), sem script, e os ajustes do escuro vêm junto. `data-theme="escuro"` força o escuro; `data-theme="claro"`, o claro (peça de comunicação). Tela de sistema sem o atributo fica clara num aparelho escuro.
- [[ESCREVA: o que é cada cor da marca (os nomes do marca.json) e onde ela entra; para que serve a escala.]]
- Gráficos usam as cores de dados `dado-1` a `dado-3` (seção Gráficos), não a escala da marca.

## Luz

[[ESCREVA: como a marca trata fundo e destaque. Se houver halo (`aj-halo`, manchas `halo-1` e `halo-2`) e brilho (`aj-brilho`), diga onde entram e onde nunca entram. Se a marca não usa luz, diga isso, ponha `"luz": false` no marca.json e descreva o efeito que faz o papel da luz (ex.: a moldura da Kleiciane Rocha), apagando os dois tópicos abaixo.]]

- O halo, quando existir, **nunca termina em corte reto**: ele se esvai antes do fim do contêiner. No PDF, ele não é recortado.
- Gradiente só no fundo, e só dentro da família da cor da marca. Nunca em botão, cartão ou símbolo.

## Tipografia

- [[ESCREVA: família de título e de texto, com o motivo da escolha em uma frase.]]
- `display` e `titulo-1` com **uma** ênfase de peso (duas quando há número e resultado). `titulo-3` para títulos de cartão.
- Rótulo e cabeçalho de tabela: `rotulo`, em caixa alta com espaçamento 0,08em. Se a marca não usa caixa alta, `"rotulo": {"caixa": "baixa", "italico": true}` no marca.json troca todos os rótulos do sistema pelo estilo `rotulo` do `tipo`; diga aqui como ele é. [[ESCREVA: o rótulo da marca, se não for o padrão; senão apague esta frase.]]
- Texto corrido `corpo`, até 65 caracteres por linha. Interface `corpo-sm`; botões e menus `interface`.
- **Piso de leitura na tela: nenhum texto abaixo de 14 px**, e só os corpos da escala do `tipo` (nada de tamanho solto entre dois degraus). No gráfico, conta o corpo renderizado. Conferido por `verificacao/piso.js` (marca.json `"piso"`, ligado por padrão).
- **Piso no papel e no PDF** (lido na tela ou impresso): corpo de texto de 10 pt ou mais; ressalva de 9,5 pt ou mais (também a que fica junto de um número); apoio técnico (cabeçalho e pé de página, rótulo de coluna, dados da empresa, nota de fonte e de metodologia) de 8 pt ou mais; cartão de visita, 7 pt ou mais. A ressalva nunca vai no corpo da nota técnica.
- **Título nunca termina com uma palavra sozinha**, na tela (`text-wrap: balance`) e no PDF e no DOCX: no HTML do PDF, `text-wrap: balance`; no DOCX, que não balanceia, a quebra é manual, no mesmo lugar do PDF.
- Números de indicador em `numero` com algarismos tabulares.

## Composição

Toda tela usa um de três modelos. Escolha o modelo antes de desenhar; dentro de um bloco, o alinhamento é um só.

- **Centrada** (uma ação só): login, estado vazio, confirmação, capa de apresentação, avatar e post com frase. Símbolo, título, texto de apoio e ação no eixo central, coluna de até 360 px (formulário) ou 34 caracteres (texto). Sem cartão: o fundo já é a superfície, e os campos ficam direto nele, com rótulos à esquerda. Texto de apoio em uma linha. Botão no tamanho padrão, na largura da coluna.
- **Cartão só agrupa.** Use `aj-cartao` para separar um grupo entre vários na mesma tela. Nunca para envolver a única coisa da tela.
- **Botão grande só no marketing.** `aj-botao--lg` é para o topo de landing e capa; em formulário e sistema, o tamanho padrão.
- **Leitura** (marketing e documentos): tudo alinhado à esquerda numa coluna de até 1180 px, texto até 65 caracteres. Título, texto, botões e prova começam na mesma linha vertical. Exemplo: `TelaLanding`.
- **Painel** (sistemas): menu lateral à esquerda (`NavegacaoLateral`) e conteúdo alinhado à esquerda; título da página à esquerda e ações à direita, na mesma linha. Exemplos: `TelaSistema`, `TelaCRM`, com as classes `aj-app` (nunca layout em estilo solto):
  - **o cabeçalho decide pela largura do conteúdo, nunca da janela** (container query em `aj-app__conteudo`): título e ações na mesma linha só com 860 px de conteúdo ou mais; com menos, o título ocupa a linha inteira e as ações descem para baixo dele, à esquerda, com a principal primeiro; com menos de 520 px, empilham na largura da coluna. O menu lateral come de 220 a 270 px, e a regra pela janela espremia o título até sobrar uma palavra sozinha entre 1024 e 1200 px (notebook de 1366 a 125%). A linha de contexto não começa linha com "·" (espaço sem quebra antes do ponto);
  - **a partir de 1024 px:** menu lateral; quatro indicadores por linha (`aj-indicadores`, que também decidem pelo conteúdo);
  - **abaixo de 1024 px:** o menu vira a barra do topo (`aj-app__barra`: a marca e o botão de menu de 44 px), que abre o menu como painel à esquerda, com o véu; o véu e o Esc fecham, o botão diz "Abrir menu" ou "Fechar menu", e o foco entra no primeiro item ao abrir e volta ao botão ao fechar; margem de 16 px; indicadores em 2 × 2 e, com menos de 520 px de conteúdo, em uma coluna;
  - **tabela e funil rolam dentro da própria caixa**, nunca a página (`aj-tabela-caixa`, `aj-funil`: colunas de pelo menos 180 px; no celular, uma por tela). Toda `Tela*` é conferida em 1280, 1024, 800, 390 e na largura mínima (`verificacao/prancha.js` e `verificacao/piso.js`).
- Nunca misture: um título centralizado sobre um texto alinhado à esquerda está errado.
- **Nada de item sozinho numa linha.** Sumário em grade leve; grades de cartões com número de colunas que feche certo; nunca colunas automáticas que deixem um item órfão.
- Grade: 12 colunas, intervalo `espaco-5` (24 px), margem lateral `espaco-4` (16 px) no celular e 48 px a partir de 1024 px, largura máxima 1180 px.
- Respiro vertical: `espaco-6` entre blocos de uma tela, `espaco-7` entre seções, `espaco-8` no topo de página de marketing.

## Formulário em etapas e resultado

- Uma pergunta por tela, em segunda pessoa e sem jargão. Contato só na última etapa.
- No computador, o formulário em tela inteira tem o trilho à esquerda (`aj-trilho`): a marca, o contador grande ("03 / 05"), a lista das etapas com a atual marcada e uma nota curta. No celular (abaixo de 1024 px), a barra de etapa no topo (`aj-etapas-barra`).
- Valor em dinheiro: `aj-moeda` (o "R$" dentro do campo, fora do valor) e, embaixo, até cinco atalhos (`aj-atalho`) com valores redondos. Sempre uma saída para quem não sabe ("Não sei ao certo").
- **Atalhos: até cinco numa linha, em colunas iguais** (`aj-atalhos` é uma grade de uma linha, com o valor centrado); no celular (até 760 px), três colunas, e cinco fecham 3 + 2 (quatro fecham 2 + 2). Nunca um atalho sozinho na segunda linha. Os valores precisam caber na coluna na largura mínima.
- O fim mostra o resultado (`aj-resultado`): o número com rótulo, as linhas que o explicam e a ressalva, uma vez, legível. A chamada que vem depois do resultado não leva cartão nem borda (cartão só agrupa): fica separada por um fio `linha`, como o resto da página. Dois valores comparados (`aj-comparacao`) ficam neutros: comparação não é status, então nunca vermelho para um e verde para o outro.
- **O contador tem um formato só** ("03 / 05": dois dígitos dos dois lados), no trilho, na barra do celular e no topo da variante dentro de página.
- As ações da etapa ficam alinhadas como o resto do bloco (à esquerda): no celular, o botão na largura da coluna e os links (Voltar, Ajuda) logo embaixo, à esquerda, com alvo de 44 px.

## Gráficos

- Uma série: tudo em `dado-1`. É o caso mais comum nos painéis.
- Duas ou três séries: `dado-1`, `dado-2` e `dado-3`, sempre nesta ordem. [[ESCREVA: quais cores são e o resultado da validação para daltonismo (rode verificacao/paleta_dados.sh).]] Mais de três séries: agrupe em "Outros" ou divida em gráficos.
- **Duas séries ou mais: a forma também separa** (série 2 `tracejada`, série 3 `pontilhada`; em barras, rótulo direto), e a legenda mostra a própria linha. O gráfico precisa continuar legível impresso em preto e branco e com daltonismo, inclusive tritanopia, que o validador só informa.
- **No celular, um desenho próprio** (`aj-grafico__desenho--largo`, viewBox de 480, e `--estreito`, viewBox de 300, com menos rótulos): o cartão troca um pelo outro abaixo de 480 px. Nunca o desenho do computador encolhido: a letra do eixo encolheria abaixo do piso.
- As cores de dados só existem dentro de gráficos. Nunca em botão, texto, fundo ou ilustração.
- **Cor de dados que pode lembrar uma cor proibida da marca** (ex.: um couro claro no escuro que lê como dourado): o limite é medido, não estimado. No marca.json, `croma_maximo` (croma CIELAB por tema) e `distancia_extra` contra o hex da cor proibida; `contraste.py` mede, e a paleta passa de novo pelo validador da skill dataviz.
- Rótulo direto só no ponto que importa (o último), ancorado no centro da marca (barra ou ponto) e inteiro dentro do desenho; o `aria-label` do gráfico diz o primeiro, o último e o maior valor certos.
- Um eixo só; duas escalas diferentes viram dois gráficos. Grade em `linha`, eixos e rótulos em `texto-3`, valores em `texto`.

## Camadas e telas

- Camadas (o que fica por cima): `camada-fixo` (cabeçalho), `camada-menu` (menu e seleção), `camada-painel` (painel lateral), `camada-modal`, `camada-aviso`, `camada-dica`. Nunca um número solto de z-index.
- Pontos de quebra: desenhe primeiro em `quebra-celular` (390 px). Abaixo de `quebra-tablet` (760 px) tudo vira uma coluna e o menu do site vira botão; a partir de `quebra-desktop` (1024 px) a margem lateral é 48 px e a tela de sistema ganha o menu lateral (abaixo disso, a barra do topo). Nenhuma tela, de marketing ou de sistema, rola para o lado em 390 px.
- **Largura mínima suportada: 360 px** (marca.json `largura_minima`; muitos Android e o iPhone com zoom de tela têm 360 a 375 px). Desenhe em 390, mas nada pode quebrar em 360: sem rolagem lateral, sem palavra sozinha em título ou botão, alvos de 44 px. `verificacao/piso.js` testa 1280, 390 e 360 em todo componente (as `Tela*` também em 1024 e 800) e os modelos de tela em 1440, 390 e 360; `prancha.js` renderiza as mesmas larguras.

## Espaço, raio e sombra

- Grade de 4 px: `espaco-1` (4) a `espaco-8` (64). Padding de cartão `espaco-5`; entre blocos `espaco-6`; entre seções `espaco-7`.
- Raios: `raio-sm` etiqueta; `raio-md` botão, campo e item de menu; `raio-lg` cartão, tabela e aviso; `raio-xl` modal e ícone de app.
- Sombras quase invisíveis: `sombra-1` em repouso, `sombra-2` para o que flutua, `sombra-3` para modal. Nunca sombra colorida saturada.

## Movimento

- Toda animação usa `curva-marca`. Durações: `tempo-rapido` para hover e foco, `tempo-base` para menus e avisos, `tempo-lento` para modal.
- [[ESCREVA: o movimento-assinatura da marca (como o símbolo se monta no `aj-carregando`, com `tempo-assinatura`; numa marca só tipográfica, como o nome entra, de `logo.trechos[].entrada`) e onde ele aparece.]]
- Com movimento reduzido ativado, tudo para: o símbolo aparece montado.

## Estados e acessibilidade

- Foco: anel de 2 px sólido em `foco`, afastado 2 px, em todo elemento interativo.
- Desabilitado: opacidade 45% e cursor bloqueado; o texto explica por quê quando não for óbvio.
- Erro de campo: borda `critico`, fundo `critico-fundo` e mensagem de correção.
- Cor nunca carrega sentido sozinha: status sempre com palavra, variação sempre com sinal.
- **Alvo de toque de 44 × 44 px ou mais** em todo controle: botão (inclusive o pequeno), botão de ícone, campo, item de menu e de navegação, aba, filtro, atalho, página, link de trilha, de cabeçalho e de rodapé, link de ação solto (Voltar, Ajuda) e a caixa de marcar e a opção única, que contam pelo rótulo inteiro. Link dentro de uma frase fica fora da conta. Exceção (botão menor numa tabela densa, só no computador) só escrita na regra da marca, com o motivo. Conferido por `verificacao/piso.js`, em 1280, 390 e 360 px, nos dois temas.
- **O alvo de 44 px não muda a linha de base.** Quando um link cresce até 44 px numa linha com texto solto (trilha, base do rodapé, pé de formulário, paginação), a linha centraliza tudo na vertical (`align-items: center`): o texto e o link ficam na mesma altura, nunca o texto no alto.
- **Modal no celular** (até 480 px): as ações empilham na largura do modal, a principal primeiro (em cima) e o cancelar embaixo. No computador, lado a lado à direita, a ação na ponta. O pé do painel lateral segue a mesma regra. Alerta com ação, no celular: o botão desce para baixo do texto, alinhado com ele.

## Ícones

- Ícones de traço do conjunto Lucide, traço 1,75, na cor do texto ao lado (`texto-2`; ativo `sobre-realce`). 16 px em botão, 18 px em menu, 20 px em aviso.
- Nunca ícone colorido, preenchido ou emoji.

## Imagens

- [[ESCREVA: que tipo de imagem a marca usa e qual proíbe (clichês de banco de imagem do setor).]]

## Logo

- [[ESCREVA: o nome do símbolo, qual arquivo usar em cada fundo (`assets/logos/simbolo-*.svg`) e a versão pequena para 24 px ou menos. Marca só tipográfica: como o nome é construído, `horizontal-*.svg` e `empilhado-*.svg`, a largura mínima em linha e o que faz o papel do avatar.]]
- [[ESCREVA: quando o símbolo aparece sozinho e quando entra a assinatura com o nome.]]
- Respiro de 1/3 da altura do símbolo. Nunca gradiente, contorno, sombra, distorção ou moldura.

## Aplicações

- **Compartilhamento de link:** `og-compartilhamento` (1200 × 630). [[ESCREVA: fundo, símbolo e frase.]]
- **Instagram:** post em 1080 × 1350 e story em 1080 × 1920. No story, deixe livres 250 px no topo e 340 px na base, onde ficam os controles do aplicativo. [[ESCREVA: onde fica o símbolo e o que diz a frase.]]
- **Assinatura de e-mail:** tabela simples com o símbolo em PNG hospedado, nome em negrito, cargo, e-mail e site na cor de ação. Fonte Arial no e-mail, porque programas de e-mail não carregam fonte da web. **O PNG do logo leva o próprio fundo** (o chão claro da marca, com o respiro em volta), nunca transparente: num programa de e-mail no modo escuro, um logo escuro sobre fundo transparente some. O texto ao lado é texto de verdade (o programa clareia no modo escuro).
- **Papel que vai para a impressora não leva chão.** PDF para imprimir no escritório (papel timbrado, carta) sai sem fundo: o papel da bandeja é o chão, e a margem que a impressora não alcança viraria uma moldura branca. O chão da marca fica só na versão digital (o PDF enviado, lido na tela).
- **Papel timbrado de impressão é a folha só com o cabeçalho e o pé**, com o corpo em branco: é o papel que vai para a bandeja, e a carta é impressa por cima. A carta de exemplo, com os campos a preencher, fica na versão digital e no DOCX (campo marcado com fundo, impresso no papel, sairia como mancha).
- **DOCX: o peso do título vem de uma instância estática.** Word e LibreOffice não escolhem o peso de uma fonte variável pelo estilo (o título sai no peso 400). Os estilos de título usam uma instância estática no peso certo, com nome de família próprio, que vai junto do modelo para instalar; a tabela de fontes do DOCX declara uma substituta de sistema. Confira convertendo o DOCX em PDF no LibreOffice e lendo o nome da fonte embutida nos títulos.
- **Documentos (relatório, resumo de reunião, proposta, contrato):** monte com o componente `Documento` (HTML que também vira PDF A4). Sumário com `Sumario`: uma grade leve dentro da capa, sem linhas, com número de dois dígitos na cor de ação (4 colunas na tela, 2 no celular e no PDF). Grades de cartões com número de colunas que feche certo. No PDF: margem de 14 mm em cima e embaixo e 16 mm nas laterais, primeira página com a capa e o sumário, cartão e linha de tabela nunca partidos entre páginas, cabeçalho de seção nunca sozinho no pé. Efeito de fundo só na capa; nada de marca d'água atrás do texto.
