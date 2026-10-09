Tecnologia que acolhe: precisa, calma e plana. A AJ é a empresa de tecnologia que se importa com o negócio do advogado, e cada tela prova isso antes de qualquer frase. Siga estas regras em todo produto da AJ: site, landing pages, AJ OPS, Nosso CRM, apresentações e posts.

## Princípios

- **Plana.** Superfícies chapadas. Sem vidro (`backdrop-filter`), sem gradiente em botão, cartão ou símbolo, sem 3D como padrão.
- **Uma cor.** O violeta é a única cor da marca. `lavanda` e `luz` são o violeta iluminado. Todo o resto é neutro (`fundo`, `superficie`, `texto`).
- **Luz em vez de brilho.** A luz aparece de dois jeitos só: o halo no fundo claro (`aj-halo`) e o brilho do símbolo no escuro (`aj-brilho`).
- **Uma ousadia por tela.** Uma ação principal, uma palavra em peso no título, um halo. O resto fica quieto.

## Voz e conteúdo

- Fale com o advogado em segunda pessoa: "o seu escritório", "a sua equipe".
- Frase curta, uma ideia por frase. Português do Brasil sempre, com acento ("Jurídico").
- Em título, uma ênfase em peso: a palavra que carrega o cuidado ou o sentido. No máximo duas quando o título traz um número e um resultado ("**4 pilares** para construir uma advocacia previsível, escalável e **lucrativa**"); nunca três. Exemplos reais: "Finalmente, alguém que **se importa** com o seu escritório." · "Bom dia, **Samuel**" · "Clientes que pedem **atenção**".
- Botão é verbo + objeto e diz o que acontece: "Solicitar diagnóstico", "Salvar cliente". O aviso repete o verbo no particípio: "Cliente salvo".
- Erro explica o que houve e como resolver, sem desculpas: "O acesso expirou. Peça ao escritório para aprovar de novo no Meta."
- Número real quando houver prova ("+R$ 100 mi em contratos fechados"). Nunca promessa sem prova.
- Nunca: jargão de agência ("alavancar", "potencializar"), exclamação de enfeite, emoji, clichê jurídico (balança, martelo, coluna).

## Cor

- Chão da página e do app: `fundo`. Cartões, tabelas, menus e campos: `superficie`. Faixas, cabeçalho de tabela e hover: `superficie-2`.
- Texto principal `texto`; apoio `texto-2`; placeholder e metadado `texto-3`. Todos passam 4,5:1 sobre `fundo`, `superficie` e `superficie-2` nos dois temas.
- Ação principal `acao` com texto `sobre-acao`; hover `acao-hover`. Item ativo e botão secundário: `realce` com texto `sobre-realce`.
- Status sempre com palavra: `sucesso`/`sucesso-fundo`, `atencao`/`atencao-fundo`, `critico`/`critico-fundo`. Informação usa `acao`.
- Divisórias `linha`. Borda de controle `borda-controle` (3:1).
- Escala `violeta-50` a `violeta-950` só para sistemas que exigem escala (Nosso CRM). Na interface, use os tokens semânticos.
- Gráficos usam as cores de dados `dado-1` a `dado-3` (veja a seção Gráficos), não a escala do violeta.

## Luz

- **Halo** (fundo claro): `aj-halo` no contêiner; duas manchas desfocadas `halo-1` e `halo-2`. Use em: topo de página de marketing, login, estado vazio e topo do Início. Nunca atrás de texto longo, nunca em tabela ou formulário.
- O halo **nunca termina em corte reto**: ele se esvai antes do fim do contêiner, e o que vem embaixo (sumário, primeira seção) aparece sobre o fundo limpo. No PDF, o halo não é recortado e se esvai sozinho.
- **Brilho** (fundo escuro): `aj-brilho` no símbolo lavanda. Só no símbolo e no carregamento.
- Gradiente só no fundo e só na família do violeta. Degradê entre cores diferentes (violeta para rosa, violeta para azul) não entra em lugar nenhum.

## Tipografia

- Títulos em Sora (`titulo`), texto e interface em Manrope (`texto`), ambas do Google Fonts.
- `display` e `titulo-1` em Sora 300 com **uma** ênfase em 600 (duas quando há número e resultado). `titulo-3` em 500 para títulos de cartão.
- Rótulo e cabeçalho de tabela: `rotulo`, em caixa alta com espaçamento 0,08em.
- Texto corrido `corpo`, até 65 caracteres por linha. Interface `corpo-sm`; botões e menus `interface`.
- Números de indicador em `numero` com algarismos tabulares.

## Composição

Toda tela usa um de três modelos. Escolha o modelo antes de desenhar; dentro de um bloco, o alinhamento é um só.

- **Centrada** (uma ação só): login, estado vazio, confirmação, capa de apresentação, avatar e post com frase. Símbolo, título, texto de apoio e ação no eixo central, coluna de até 360 px (formulário) ou 34 caracteres (texto). Sem cartão: o fundo com halo já é a superfície, e os campos ficam direto nele, com rótulos à esquerda. Texto de apoio em uma linha. Botão no tamanho padrão, na largura da coluna. Exemplos: tela de login, `EstadoVazio`.
- **Cartão só agrupa.** Use `aj-cartao` para separar um grupo entre vários na mesma tela (indicadores, pauta, item do funil). Nunca para envolver a única coisa da tela.
- **Botão grande só no marketing.** `aj-botao--lg` é para o topo de landing e capa; em formulário e sistema, o tamanho padrão.
- **Leitura** (marketing e documentos): topo de landing, seções de site, manual, proposta. Tudo alinhado à esquerda numa coluna de até 1180 px, texto até 65 caracteres. Título, texto, botões e prova começam na mesma linha vertical. Exemplo: `TelaLanding`.
- **Painel** (sistemas): AJ OPS, Nosso CRM, painel do cliente. Menu lateral à esquerda (`NavegacaoLateral`) e conteúdo alinhado à esquerda; título da página à esquerda e ações à direita, na mesma linha. Exemplos: `TelaAJOps`, `TelaCRM`.
- Nunca misture: um título centralizado sobre um texto alinhado à esquerda, ou um símbolo à esquerda sobre um cartão centralizado, está errado.
- Grade: 12 colunas, intervalo `espaco-5` (24 px), margem lateral `espaco-4` (16 px) no celular e 48 px a partir de 1024 px, largura máxima 1180 px.
- Respiro vertical: `espaco-6` entre blocos de uma tela, `espaco-7` entre seções, `espaco-8` no topo de página de marketing.

## Gráficos

- Uma série: tudo em `dado-1` (o violeta). É o caso mais comum nos painéis.
- Duas ou três séries: `dado-1`, `dado-2` (laranja) e `dado-3` (verde-água), sempre nesta ordem. A combinação foi validada para daltonismo e para visão normal, nos dois temas. Mais de três séries: agrupe em "Outros" ou divida em gráficos.
- As cores de dados são a única exceção à regra de uma cor só, e só existem dentro de gráficos. Nunca em botão, texto, fundo ou ilustração.
- Um eixo só; duas escalas diferentes viram dois gráficos. Grade em `linha`, eixos e rótulos em `texto-3`, valores em `texto`.
- `dado-3` fica abaixo de 3:1 no claro: use sempre rótulo direto ou uma tabela ao lado. Veja o componente `Grafico`.

## Camadas e telas

- Camadas (o que fica por cima): `camada-fixo` (cabeçalho), `camada-menu` (menu e seleção), `camada-painel` (painel lateral), `camada-modal`, `camada-aviso`, `camada-dica`. Nunca um número solto de z-index.
- Pontos de quebra: desenhe primeiro em `quebra-celular` (390 px), porque a maior parte do público chega pelo Instagram. Abaixo de `quebra-tablet` (760 px) tudo vira uma coluna e o menu do site vira botão; a partir de `quebra-desktop` (1024 px) a margem lateral é 48 px.

## Espaço, raio e sombra

- Grade de 4 px: `espaco-1` (4) a `espaco-8` (64). Padding de cartão `espaco-5`; entre blocos `espaco-6`; entre seções `espaco-7`.
- Raios: `raio-sm` etiqueta; `raio-md` botão, campo e item de menu; `raio-lg` cartão, tabela e aviso; `raio-xl` modal e ícone de app.
- Sombras quase invisíveis: `sombra-1` em repouso, `sombra-2` para o que flutua (menu, aviso), `sombra-3` para modal. Nunca sombra colorida saturada.

## Movimento

- Toda animação usa `curva-dobra` (sai rápido, chega devagar). Durações: `tempo-rapido` para hover e foco, `tempo-base` para menus e avisos, `tempo-lento` para modal.
- Assinatura: **a dobra se fecha** (`aj-carregando`, `tempo-dobra`). É o carregamento de página, a abertura de vídeo e o fim de apresentação.
- O halo pode respirar (`aj-halo--respira`, 7 s) só em página de marketing.
- Com movimento reduzido ativado, tudo para: o símbolo aparece montado.

## Estados e acessibilidade

- Foco: anel de 2 px sólido em `foco`, afastado 2 px, em todo elemento interativo.
- Desabilitado: opacidade 45% e cursor bloqueado; o texto explica por quê quando não for óbvio.
- Erro de campo: borda `critico`, fundo `critico-fundo` e mensagem de correção.
- Cor nunca carrega sentido sozinha: status sempre com palavra, variação sempre com sinal.

## Ícones

- Ícones de traço do conjunto Lucide, traço 1,75, na cor do texto ao lado (`texto-2`; ativo `sobre-realce`). 16 px em botão, 18 px em menu, 20 px em aviso.
- Nunca ícone colorido, preenchido ou emoji.

## Imagens

- Sem foto de banco com gente de terno, sem balança, martelo ou coluna.
- Prefira a interface real do produto e números reais. Foto só de pessoas reais da AJ ou de clientes com autorização.

## Logo

- Símbolo A2 Dobra: `assets/Logos/simbolo-violeta.svg` no claro, `simbolo-lavanda.svg` no escuro (com `aj-brilho`), `simbolo-branco.svg` sobre violeta. Em 24 px ou menos, `simbolo-pequeno-violeta.svg`.
- AJ na frente: o símbolo sozinho é a marca do dia a dia (avatar, app, favicon, menu). A assinatura com "Anúncio Jurídico" entra em documento, rodapé, contrato e topo do site.
- Respiro de 1/3 da altura do símbolo. Nunca gradiente, contorno, sombra, distorção ou moldura.

## Aplicações

- **Compartilhamento de link:** `assets/Aplicacoes/og-compartilhamento.png` (1200 × 630), fundo noite, símbolo com brilho e o lema. É a imagem que aparece quando alguém cola o link do site no WhatsApp ou no LinkedIn.
- **Instagram:** post em 1080 × 1350 (claro com halo ou escuro com brilho) e story em 1080 × 1920. Símbolo no canto superior esquerdo (post) ou centralizado (story), frase em Sora 300 com a ênfase da marca, endereço do site no pé. No story, deixe livres 250 px no topo e 340 px na base, onde ficam os controles do aplicativo. Modelos em `assets/Aplicacoes/`.
- **Assinatura de e-mail:** tabela simples com o símbolo (PNG hospedado em `marca.anunciojuridico.com.br/publico/email/`), nome em negrito, cargo, e-mail e site em violeta. Fonte Arial no e-mail, porque programas de e-mail não carregam Sora. Prévia em `assets/Aplicacoes/assinatura-email-previa.png`.
- **Documentos (relatório, resumo de reunião, proposta, contrato):** monte com o componente `Documento` (HTML que também vira PDF A4). Sumário com `Sumario`: uma grade leve dentro da capa, sem linhas, com número de dois dígitos em violeta (4 colunas na tela, 2 no celular e no PDF); nunca uma linha de botões que quebra deixando um item sozinho. Grades de cartões com número de colunas que feche certo (3 cartões na grade de 3, 4 na de 2 ou 4), nunca colunas automáticas. No PDF: margem de 14 mm em cima e embaixo e 16 mm nas laterais, primeira página com a capa e o sumário, cartão e linha de tabela nunca partidos entre páginas, cabeçalho de seção nunca sozinho no pé. Títulos em Sora 300 com a ênfase da marca, texto em Manrope. Halo só na capa; nada de marca d'água ou fundo colorido atrás do texto.
