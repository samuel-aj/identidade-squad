# Componentes completados em 28/09/2026. Executado por gen_comp.py (usa comp, ic, I, SIMB, MARCA_NOME, ESC, AC já definidos lá).
I.update({
 'baixo':'<path d="m6 9 6 6 6-6"/>','cima':'<path d="m18 15-6-6-6 6"/>','esq':'<path d="m15 18-6-6 6-6"/>','dir':'<path d="m9 18 6-6-6-6"/>',
 'check':'<path d="M20 6 9 17l-5-5"/>','mais3':'<circle cx="12" cy="5" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="12" cy="19" r="1"/>',
 'x':'<path d="M18 6 6 18M6 6l12 12"/>','lapis':'<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
 'copiar':'<rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
 'lixo':'<path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m3 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/>',
 'baixar':'<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>','info':'<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
 'play':'<path d="M6 4l14 8-14 8z" fill="currentColor"/>','menu':'<path d="M4 6h16M4 12h16M4 18h16"/>','sair':'<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>',
 'alerta':'<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4M12 17h.01"/>'})
def nos(t): return f"\n**Nos sistemas:** {t}\n"

comp('BotaoIcone','Ações',110,"""# BotaoIcone
Botão quadrado só com ícone, para ações repetidas em lista e cabeçalho: mais opções (⋯), fechar, editar, copiar.

**O que você fornece:** `<button class="aj-botao-icone" aria-label="…">` com um ícone Lucide de 18 px. `aj-botao-icone--contorno` quando precisa de borda (fora de tabela).

- O `aria-label` é obrigatório e diz a ação: "Mais opções do contrato", "Fechar".
- Ação que a pessoa precisa descobrir sozinha não vai em botão só de ícone: use `aj-botao` com texto.
- Com menu aberto, `aria-expanded="true"` mantém o fundo aceso.
"""+nos("«SISTEMA» e painel: `button.tsx` com `size=\"icon\"`. «CRM»: o gatilho do `KebabMenu`."),
f"""<div style="display:flex;gap:12px;align-items:center">
<button class="aj-botao-icone" aria-label="Mais opções">{ic('mais3')}</button>
<button class="aj-botao-icone" aria-label="Editar">{ic('lapis')}</button>
<button class="aj-botao-icone" aria-label="Copiar ID">{ic('copiar')}</button>
<button class="aj-botao-icone" aria-expanded="true" aria-label="Mais opções (aberto)">{ic('mais3')}</button>
<button class="aj-botao-icone aj-botao-icone--contorno" aria-label="Fechar">{ic('x')}</button>
</div>""")

comp('MenuSuspenso','Ações',330,"""# MenuSuspenso
Lista de ações que abre a partir de um botão: as ações secundárias de uma linha, de um cartão ou do perfil.

**O que você fornece:** o gatilho (`aj-botao-icone` com `aria-haspopup="menu"` e `aria-expanded`) e um `<div class="aj-menu" role="menu">` com itens `aj-menu__item` (`role="menuitem"`), ícone opcional, atalho opcional (`aj-menu__atalho`), grupos (`aj-menu__grupo`) e divisores (`aj-menu__divisor`).

- Até 7 itens. Mais que isso vira uma tela ou um painel.
- A ação destrutiva fica por último, depois de um divisor, com `aj-menu__item--perigo`, e sempre abre a confirmação (`Modal`).
- Abre colado ao gatilho, alinhado pela borda; fecha com Esc, clique fora ou ao escolher. Setas navegam, Enter escolhe.
- Superfície: `superficie`, borda `linha`, `sombra-2`, camada `camada-menu`.
"""+nos("«SISTEMA» e painel: `dropdown-menu.tsx` (Base UI) — aplicar estas classes ao `Content` e aos `Item`. «CRM»: `KebabMenu.tsx` e `popover.tsx`."),
f"""<div style="display:flex;gap:40px;align-items:flex-start">
<div style="display:grid;gap:8px;justify-items:end"><button class="aj-botao-icone" aria-haspopup="menu" aria-expanded="true" aria-label="Mais opções do cliente">{ic('mais3')}</button>
<div class="aj-menu" role="menu" aria-label="Ações do cliente">
<button class="aj-menu__item" role="menuitem">{ic('lapis')}Editar ficha</button>
<button class="aj-menu__item" role="menuitem" data-ativo="true">{ic('reunioes')}Marcar reunião<span class="aj-menu__atalho">R</span></button>
<button class="aj-menu__item" role="menuitem">{ic('copiar')}Copiar ID</button>
<button class="aj-menu__item" role="menuitem">{ic('baixar')}Baixar relatório</button>
<div class="aj-menu__divisor" role="separator"></div>
<button class="aj-menu__item aj-menu__item--perigo" role="menuitem">{ic('lixo')}Excluir cliente</button>
</div></div>
<div class="aj-menu" role="menu" aria-label="Conta" style="min-width:240px">
<div class="aj-menu__grupo">samuel@anunciojuridico.com.br</div>
<button class="aj-menu__item" role="menuitemradio" aria-checked="true">{ic('check')}Tema claro</button>
<button class="aj-menu__item" role="menuitemradio" aria-checked="false"><span style="width:16px"></span>Tema escuro</button>
<div class="aj-menu__divisor" role="separator"></div>
<button class="aj-menu__item" role="menuitem">{ic('config')}Configurações</button>
<button class="aj-menu__item" role="menuitem">{ic('sair')}Sair</button>
</div></div>""")

comp('Selecao','Formulários',380,"""# Selecao
Campo de escolha que abre uma lista com busca: responsável, cliente, área, etapa do funil. Substitui o `select` nativo quando há mais de 7 opções ou quando a opção precisa de ícone ou avatar.

**O que você fornece:** rótulo (`aj-campo`), o gatilho `<button class="aj-selecao" aria-haspopup="listbox" aria-expanded>` com o valor e o ícone de seta, e a lista num `aj-menu` com `role="listbox"`: busca opcional (`aj-menu__busca` com `aj-busca`), itens `role="option"` e `aria-selected="true"` no escolhido, `aj-menu__vazio` quando a busca não acha nada.

- Até 7 opções e sem busca: o `select` nativo (`Campo`) basta e é melhor no celular.
- Sem valor, o gatilho mostra o texto de ajuda em `texto-3` ("Escolha o responsável").
- A busca filtra enquanto digita; "Nenhum cliente com esse nome." quando vazia.
"""+nos("«SISTEMA»: `select.tsx` e `choice-select.tsx`. «CRM»: `ContactSearchCombobox.tsx`."),
f"""<div style="display:flex;gap:32px;align-items:flex-start;flex-wrap:wrap">
<div class="aj-campo" style="width:280px"><label>Responsável</label><button class="aj-selecao" aria-haspopup="listbox" aria-expanded="true"><span style="display:flex;align-items:center;gap:8px"><span class="aj-avatar aj-avatar--sm">MA</span>Marina Alves</span>{ic('baixo')}</button>
<div class="aj-menu" role="listbox" aria-label="Responsáveis">
<div class="aj-menu__busca"><label class="aj-busca">{ic('busca')}<input class="aj-entrada" placeholder="Buscar pessoa" aria-label="Buscar pessoa"></label></div>
<div class="aj-menu__item" role="option" aria-selected="true"><span class="aj-avatar aj-avatar--sm">MA</span>Marina Alves<span class="aj-menu__atalho">{ic('check')}</span></div>
<div class="aj-menu__item" role="option"><span class="aj-avatar aj-avatar--sm">RC</span>Rafael Costa</div>
<div class="aj-menu__item" role="option"><span class="aj-avatar aj-avatar--sm">JS</span>Júlia Santos</div>
</div></div>
<div class="aj-campo" style="width:260px"><label>Etapa do funil</label><button class="aj-selecao" aria-haspopup="listbox" aria-expanded="false"><span class="aj-selecao__valor--vazio">Escolha a etapa</span>{ic('baixo')}</button><span class="aj-ajuda">Nomes de pessoas são exemplos.</span></div>
</div>""")

comp('Escolhas','Formulários',260,"""# Escolhas
Caixa de marcar, opção única e interruptor: as três formas de escolher algo dentro de um formulário.

**O que você fornece:** um `<label>` com a classe (`aj-marcar`, `aj-opcao` ou `aj-interruptor`) envolvendo o `<input>` nativo e o texto; texto de apoio opcional em `<small>`.

- **Caixa de marcar:** várias escolhas independentes, ou aceitar algo. Aceita estado intermediário (`indeterminate`) para "marcar todos".
- **Opção única:** uma entre 2 a 5 opções visíveis. Mais que isso, `Selecao`.
- **Interruptor:** liga e desliga algo que vale na hora, sem botão "Salvar" ("Receber aviso no WhatsApp").
- O texto diz o que acontece quando marcado. O clique vale no texto inteiro, não só no quadradinho.
"""+nos("«SISTEMA» e painel: `checkbox.tsx`, `radio-group.tsx`. «CRM»: Radix `checkbox`, `switch` (via `FormControls.tsx`)."),
f"""<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:28px;max-width:860px">
<div style="display:grid;gap:14px"><span class="aj-rotulo">Caixa de marcar</span>
<label class="aj-marcar"><input type="checkbox" checked><span>Enviar relatório mensal</span></label>
<label class="aj-marcar"><input type="checkbox"><span>Incluir custos de mídia<small>Aparece no PDF do cliente.</small></span></label>
<label class="aj-marcar"><input type="checkbox" disabled><span>Assinatura digital</span></label></div>
<div style="display:grid;gap:14px"><span class="aj-rotulo">Opção única</span>
<label class="aj-opcao"><input type="radio" name="per" checked><span>Últimos 30 dias</span></label>
<label class="aj-opcao"><input type="radio" name="per"><span>Este trimestre</span></label>
<label class="aj-opcao"><input type="radio" name="per"><span>Desde o início</span></label></div>
<div style="display:grid;gap:14px"><span class="aj-rotulo">Interruptor</span>
<label class="aj-interruptor"><input type="checkbox" role="switch" checked><span>Aviso no WhatsApp<small>Quando um lead novo chegar.</small></span></label>
<label class="aj-interruptor"><input type="checkbox" role="switch"><span>Resumo semanal por e-mail</span></label></div>
</div>""")

comp('BuscaEFiltros','Formulários',150,"""# BuscaEFiltros
Campo de busca com lupa e filtros em pílula, sempre numa linha só acima da lista ou tabela que filtram.

**O que você fornece:** `<label class="aj-busca">` com o ícone e um `input.aj-entrada` (com `aria-label`); filtros como `<button class="aj-filtro" aria-pressed>` dentro de `aj-filtros`, com contagem opcional (`aj-filtro__conta`).

- O placeholder diz o que se busca: "Buscar escritório ou responsável".
- Filtro ativo em `realce`. "Todos" é um filtro como os outros e começa ativo.
- A contagem mostra quantos itens o filtro deixa, não o total.
"""+nos("«SISTEMA»: filtros de `data-table.tsx`. «CRM»: busca do funil e da lista de contatos."),
f"""<div style="display:grid;gap:14px;max-width:760px">
<label class="aj-busca" style="max-width:360px">{ic('busca')}<input class="aj-entrada" placeholder="Buscar escritório ou responsável" aria-label="Buscar escritório ou responsável"></label>
<div class="aj-filtros"><button class="aj-filtro" aria-pressed="true">Todos <span class="aj-filtro__conta">42</span></button><button class="aj-filtro" aria-pressed="false">Em dia <span class="aj-filtro__conta">31</span></button><button class="aj-filtro" aria-pressed="false">Aguardando <span class="aj-filtro__conta">7</span></button><button class="aj-filtro" aria-pressed="false">Em risco <span class="aj-filtro__conta">4</span></button></div>
</div>""")

comp('FormularioEtapas','Formulários',520,"""# FormularioEtapas
A aplicação da landing: uma pergunta por tela, com opções em cartão, barra de etapas e Voltar / Continuar. É o único caminho para o diagnóstico; o WhatsApp só aparece no fim.

**O que você fornece:** o contêiner `aj-etapas` com o topo (`aj-etapas__topo`: nome e "Etapa X de N"), a barra (`Progresso` sem rótulo), a pergunta (`aj-etapas__pergunta`, «FONTE_TITULO» 300), as opções (`aj-escolha` com `input type="radio"`), as ações (`aj-etapas__acoes`) e a nota (`aj-etapas__nota`).

- Uma pergunta por etapa; de 4 a 6 etapas no total. Dados de contato na última, nunca na primeira.
- "Continuar" só habilita depois da escolha. "Voltar" guarda a resposta anterior.
- Pergunta em segunda pessoa e sem jargão: "Qual é a área principal do seu escritório?".
- A última tela confirma e leva ao WhatsApp: "Aplicação enviada. Vamos falar com você no WhatsApp."
- **Em tela inteira** (formulário-isca fora da landing): `aj-etapas-tela` com o trilho à esquerda (`aj-trilho`: marca, `aj-trilho__contador` "03 / 05", a lista `aj-trilho__etapas` com `aria-current` na atual e a nota `aj-trilho__nota`) e o formulário em `aj-etapas-tela__principal`. Abaixo de 1024 px o trilho some e entra a barra `aj-etapas-barra` (marca, `aj-etapas-barra__passo` e `aj-etapas-barra__linha`). Valor em dinheiro com `aj-moeda` e `aj-atalhos` (componente `Campo`); o fim mostra o `aj-resultado` (componente `Indicador`).
"""+nos("Landing e Typebot: é o desenho da aplicação/diagnóstico. As perguntas reais vêm do formulário de diagnóstico da «SIGLA»."),
f"""<form class="aj-etapas" onsubmit="event.preventDefault()">
<div class="aj-etapas__topo"><span>Aplicação</span><span>Etapa 1 de 5</span></div>
<div class="aj-progresso" aria-hidden="true"><div class="aj-progresso__trilho"><i class="aj-progresso__barra" style="width:20%"></i></div></div>
<p class="aj-etapas__pergunta" id="pq">Qual é a área principal do seu escritório?</p>
<div class="aj-etapas__escolhas" role="radiogroup" aria-labelledby="pq">
<label class="aj-escolha"><input type="radio" name="a" checked>Previdenciário</label>
<label class="aj-escolha"><input type="radio" name="a">Trabalhista</label>
<label class="aj-escolha"><input type="radio" name="a">Família e sucessões</label>
<label class="aj-escolha"><input type="radio" name="a">Outra área</label>
</div>
<div class="aj-etapas__acoes"><button class="aj-botao aj-botao--fantasma" type="button" disabled>Voltar</button><button class="aj-botao aj-botao--principal" type="submit">Continuar</button></div>
<p class="aj-etapas__nota">No fim, marcamos o diagnóstico pelo WhatsApp.</p>
</form>""")

comp('Abas','Navegação',180,"""# Abas
Troca entre visões do mesmo assunto sem sair da página: as partes da ficha do cliente, os períodos de um relatório.

**O que você fornece:** `<div class="aj-abas" role="tablist">` com `<button class="aj-aba" role="tab" aria-selected>`. Para 2 a 4 opções curtas que mudam um filtro, use a variante `aj-abas--segmento`.

- De 2 a 6 abas, com nome de uma ou duas palavras.
- A aba ativa tem traço `acao` embaixo e texto em peso; as outras, `texto-2`.
- No celular a linha rola na horizontal; não quebra em duas linhas.
"""+nos("«SISTEMA» e painel: `tabs.tsx`. «CRM»: `tabs.tsx`."),
"""<div style="display:grid;gap:28px;max-width:720px">
<div class="aj-abas" role="tablist" aria-label="Ficha do cliente"><button class="aj-aba" role="tab" aria-selected="true">Resumo</button><button class="aj-aba" role="tab" aria-selected="false">Contratos</button><button class="aj-aba" role="tab" aria-selected="false">Reuniões</button><button class="aj-aba" role="tab" aria-selected="false">Tráfego pago</button><button class="aj-aba" role="tab" aria-selected="false">Financeiro</button></div>
<div class="aj-abas aj-abas--segmento" role="tablist" aria-label="Período"><button class="aj-aba" role="tab" aria-selected="false">7 dias</button><button class="aj-aba" role="tab" aria-selected="true">30 dias</button><button class="aj-aba" role="tab" aria-selected="false">90 dias</button></div>
</div>""")

comp('PaginacaoETrilha','Navegação',160,"""# PaginacaoETrilha
Paginação embaixo de tabelas longas e trilha (breadcrumb) no topo de páginas de detalhe.

**O que você fornece:** paginação com `aj-paginacao` (texto "1–25 de 142" à esquerda e `aj-pagina` à direita, `aria-current="page"` na atual, setas com `aria-label`); trilha com `<nav class="aj-trilha" aria-label="Você está em"><ol>` e `aria-current="page"` no último item.

- Paginação só acima de 25 linhas. Mostre no máximo 5 números e reticências.
- A trilha aparece a partir do segundo nível ("Clientes / Silva Previdenciário"), nunca na página inicial.
"""+nos("«SISTEMA»: rodapé de `data-table.tsx`; topo das páginas de cliente e contrato."),
f"""<div style="display:grid;gap:28px;max-width:760px">
<nav class="aj-trilha" aria-label="Você está em"><ol><li><a href="#">Clientes</a></li><li><a href="#">Silva Previdenciário</a></li><li aria-current="page">Contrato 2026-031</li></ol></nav>
<div class="aj-paginacao"><span>1–25 de 142 clientes</span><div class="aj-paginacao__paginas"><button class="aj-pagina" aria-label="Página anterior" disabled>{ic('esq')}</button><button class="aj-pagina" aria-current="page">1</button><button class="aj-pagina">2</button><button class="aj-pagina">3</button><span class="aj-pagina" aria-hidden="true">…</span><button class="aj-pagina">6</button><button class="aj-pagina" aria-label="Próxima página">{ic('dir')}</button></div></div>
</div>""")

comp('Modal','Sobreposições',330,"""# Modal
Janela que interrompe para uma decisão curta: confirmar uma exclusão, preencher dois ou três campos. Todo o resto é página ou painel lateral.

**O que você fornece:** `aj-veu aj-veu--modal` (fundo escurecido, logo abaixo do modal) e `<div class="aj-modal" role="dialog" aria-modal="true" aria-labelledby>` com cabeça (`aj-modal__titulo` + `BotaoIcone` fechar), texto (`aj-modal__texto`) e ações (`aj-modal__acoes`: cancelar à esquerda, ação à direita).

- Título em pergunta quando é confirmação: "Excluir contrato?".
- O texto diz a consequência real, não "tem certeza?".
- O botão repete o verbo e o objeto: "Excluir contrato", em `aj-botao--perigo`. Nunca "Sim" / "OK".
- Esc e o botão fechar cancelam. O foco começa no botão de cancelar em ações destrutivas.
- `raio-xl`, `sombra-3`, camada `camada-modal`. Sem vidro no véu: só escurece.
- Texto longo (política de privacidade, termos): `aj-modal aj-modal--leitura`, que rola por dentro. Com `<dialog>` nativo, `<dialog class="aj-modal">`: o véu vem do `::backdrop`.
"""+nos("«SISTEMA» e painel: `dialog.tsx`. «CRM»: `Modal.tsx` e `LossReasonModal.tsx` (troque `modalStyles.ts` por estas classes)."),
f"""<div style="position:relative;display:grid;place-items:center;height:280px;border-radius:var(--raio-lg);overflow:hidden;background:var(--fundo)">
<div class="aj-veu aj-veu--modal" style="position:absolute"></div>
<div class="aj-modal" role="dialog" aria-modal="true" aria-labelledby="mt" style="position:relative">
<div class="aj-modal__cabeca"><h3 class="aj-modal__titulo" id="mt">Excluir contrato?</h3><button class="aj-botao-icone" aria-label="Fechar">{ic('x')}</button></div>
<p class="aj-modal__texto">O contrato 2026-031 de Silva Previdenciário sai do painel e não pode ser recuperado. Os pagamentos já registrados continuam no Financeiro.</p>
<div class="aj-modal__acoes"><button class="aj-botao aj-botao--contorno">Cancelar</button><button class="aj-botao aj-botao--perigo">Excluir contrato</button></div>
</div></div>""")

comp('PainelLateral','Sobreposições',520,"""# PainelLateral
Painel que desliza da direita com um formulário ou um detalhe, sem perder a lista de fundo: editar um lead, ver a pauta de uma reunião.

**O que você fornece:** `aj-veu` e `<aside class="aj-painel" role="dialog" aria-modal="true" aria-labelledby>` com cabeça (título + fechar), corpo (`aj-painel__corpo`, rola sozinho) e pé fixo (`aj-painel__pe`) com as ações.

- Largura de 440 px; no celular ocupa a tela inteira e vira folha de baixo para cima.
- Salvar fica no pé, sempre visível. Fechar com alterações não salvas pergunta antes (`Modal`).
- Camada `camada-painel`, entra em `tempo-lento` com `curva-marca`.
"""+nos("«CRM»: `Sheet.tsx`, `FullscreenSheet.tsx`, `ActionSheet.tsx`. «SISTEMA»: detalhes que hoje abrem em página inteira podem usar este painel."),
f"""<div style="position:relative;height:500px;border-radius:var(--raio-lg);overflow:hidden;background:var(--fundo);display:flex;justify-content:flex-end">
<div class="aj-veu" style="position:absolute"></div>
<aside class="aj-painel" role="dialog" aria-modal="true" aria-labelledby="pt" style="position:relative">
<div class="aj-painel__cabeca"><h3 class="aj-modal__titulo" id="pt">Editar lead</h3><button class="aj-botao-icone" aria-label="Fechar">{ic('x')}</button></div>
<div class="aj-painel__corpo">
<div class="aj-campo"><label for="pl1">Nome</label><input id="pl1" class="aj-entrada" value="Dra. Paula Reis"></div>
<div class="aj-campo"><label for="pl2">Área</label><select id="pl2" class="aj-entrada"><option>Previdenciário</option></select></div>
<div class="aj-campo"><label for="pl3">Observação</label><textarea id="pl3" class="aj-entrada" rows="3">Pediu retorno depois das 18h.</textarea></div>
</div>
<div class="aj-painel__pe"><button class="aj-botao aj-botao--fantasma">Cancelar</button><button class="aj-botao aj-botao--principal">Salvar lead</button></div>
</aside></div>""")

comp('Dica','Sobreposições',120,"""# Dica
Etiqueta curta que aparece ao passar o mouse ou focar um ícone: o nome de um botão só de ícone, o significado de uma sigla.

**O que você fornece:** um `<span class="aj-dica" role="tooltip" id>` ligado ao gatilho por `aria-describedby`; aparece em hover e foco, some com Esc.

- Uma frase curta, sem ação dentro. Se precisa de link ou botão, é um menu ou um painel.
- Nunca guarde informação importante só na dica: no celular não existe hover.
- Invertida (`texto` como fundo), camada `camada-dica`.
"""+nos("«CRM»: `tooltip.tsx`. «SISTEMA»: adicionar a partir do mesmo padrão."),
f"""<div style="display:flex;gap:48px;align-items:flex-end;padding-top:8px">
<div style="display:grid;gap:8px;justify-items:center"><span class="aj-dica" role="tooltip" id="d1">Copiar ID do contrato</span><button class="aj-botao-icone" aria-describedby="d1" aria-label="Copiar ID">{ic('copiar')}</button></div>
<div style="display:grid;gap:8px;justify-items:center"><span class="aj-dica" role="tooltip" id="d2">CPL: custo por lead</span><span class="aj-etiqueta" aria-describedby="d2">CPL R$ 41</span></div>
</div>""")

comp('Alerta','Retorno',300,"""# Alerta
Mensagem fixa dentro da página sobre o estado de algo: acesso vencido, meta em risco, uma novidade. Diferente do `Aviso`, não some sozinho.

**O que você fornece:** `<div class="aj-alerta" role="status">` (ou `role="alert"` para crítico) com ícone, título (`aj-alerta__titulo`), texto (`aj-alerta__texto`) e ação opcional (`aj-alerta__acao`). Variantes: nenhuma (informação), `--sucesso`, `--atencao`, `--critico`.

- Título diz o que houve; o texto diz o que fazer.
- Um alerta por área da tela. Vários problemas viram uma lista numa página de alertas.
- Fundo do status chapado, sem borda colorida na lateral.
"""+nos("Painel e «CRM»: `alert.tsx`. «SISTEMA»: topo da ficha do cliente e página Alertas."),
f"""<div style="display:grid;gap:10px;max-width:720px">
<div class="aj-alerta" role="status">{ic('info','aj-alerta__icone')}<div><p class="aj-alerta__titulo">Nova etapa no onboarding</p><p class="aj-alerta__texto">O checklist agora inclui a aprovação do script de atendimento.</p></div></div>
<div class="aj-alerta aj-alerta--atencao" role="status">{ic('alerta','aj-alerta__icone')}<div><p class="aj-alerta__titulo">Acesso ao Meta vence em 3 dias</p><p class="aj-alerta__texto">Peça ao escritório para renovar a permissão da conta de anúncios.</p></div><button class="aj-botao aj-botao--contorno aj-botao--sm aj-alerta__acao">Copiar pedido</button></div>
<div class="aj-alerta aj-alerta--critico" role="alert">{ic('erro','aj-alerta__icone')}<div><p class="aj-alerta__titulo">Campanha pausada</p><p class="aj-alerta__texto">O cartão do escritório foi recusado. A campanha volta quando o pagamento for aprovado.</p></div></div>
</div>""")

comp('Esqueleto','Retorno',190,"""# Esqueleto
Formas cinza no lugar do conteúdo enquanto ele carrega, na mesma posição e tamanho do que vai aparecer.

**O que você fornece:** blocos `<span class="aj-esqueleto" style="width;height">` que imitam o layout real, com `aria-hidden="true"`, e o contêiner com `aria-busy="true"`.

- Para listas, tabelas e cartões (carregamentos de 300 ms a 2 s). Página inteira usa `Carregando`.
- Mesma forma do conteúdo final: nada pula quando ele chega.
- Pulsa devagar; com movimento reduzido, fica parado.
""",
"""<div class="aj-cartao" aria-busy="true" style="display:grid;gap:14px;max-width:420px">
<div style="display:flex;gap:12px;align-items:center"><span class="aj-esqueleto" aria-hidden="true" style="width:36px;height:36px;border-radius:50%"></span><div style="display:grid;gap:8px;flex:1"><span class="aj-esqueleto" aria-hidden="true" style="width:60%;height:14px"></span><span class="aj-esqueleto" aria-hidden="true" style="width:40%;height:12px"></span></div></div>
<span class="aj-esqueleto" aria-hidden="true" style="width:100%;height:12px"></span><span class="aj-esqueleto" aria-hidden="true" style="width:85%;height:12px"></span>
</div>""")

comp('Progresso','Retorno',130,"""# Progresso
Barra que mostra quanto de algo já foi feito: etapas do onboarding, meta de contratos do mês, envio de arquivo.

**O que você fornece:** `aj-progresso` com rótulo (`aj-progresso__rotulo`: nome e número) e trilho (`aj-progresso__trilho` com `aj-progresso__barra` e `width`). Use `role="progressbar"` com `aria-valuenow`, `aria-valuemin` e `aria-valuemax`.

- Sempre com o número ao lado ("6 de 9 etapas", "72%"): a barra sozinha não informa.
- Cor `acao`. Meta estourada não vira vermelho; o texto diz "acima da meta".
""",
"""<div style="display:grid;gap:18px;max-width:420px">
<div class="aj-progresso" role="progressbar" aria-valuenow="6" aria-valuemin="0" aria-valuemax="9" aria-label="Onboarding"><div class="aj-progresso__rotulo"><span>Onboarding</span><span>6 de 9 etapas</span></div><div class="aj-progresso__trilho"><i class="aj-progresso__barra" style="width:66%"></i></div></div>
<div class="aj-progresso" role="progressbar" aria-valuenow="72" aria-valuemin="0" aria-valuemax="100" aria-label="Meta de contratos"><div class="aj-progresso__rotulo"><span>Meta de contratos de setembro</span><span>72%</span></div><div class="aj-progresso__trilho"><i class="aj-progresso__barra" style="width:72%"></i></div></div>
</div>""")

comp('Avatar','Conteúdo',120,"""# Avatar
Foto ou iniciais de uma pessoa: responsável pelo cliente, autor de uma nota, quem está numa reunião.

**O que você fornece:** `<span class="aj-avatar">` com `<img alt="Nome">` ou duas iniciais; tamanhos `--sm` (28), padrão (36) e `--lg` (48). Grupo com `aj-avatares`.

- Sem foto, iniciais em `realce` com `sobre-realce`. Nunca uma cor aleatória por pessoa.
- Grupo mostra até 3 e depois "+N".
- O nome aparece ao lado ou na `Dica`; o avatar sozinho não identifica ninguém.
"""+nos("«SISTEMA», painel e «CRM»: `avatar.tsx`."),
"""<div style="display:flex;gap:28px;align-items:center">
<span class="aj-avatar aj-avatar--sm">MA</span><span class="aj-avatar">RC</span><span class="aj-avatar aj-avatar--lg">SM</span>
<div class="aj-avatares"><span class="aj-avatar">MA</span><span class="aj-avatar">RC</span><span class="aj-avatar">JS</span><span class="aj-avatar" style="background:var(--superficie-2);color:var(--texto-2)">+2</span></div>
</div>""")

comp('Sanfona','Conteúdo',330,"""# Sanfona
Pergunta que abre a resposta: as perguntas frequentes da landing e detalhes que não precisam estar sempre à vista.

**O que você fornece:** `<details class="aj-sanfona">` com `<summary>` (a pergunta + ícone "mais", que gira) e `<div class="aj-sanfona__corpo">` (a resposta). Uma sanfona por pergunta, em sequência.

- Pergunta como o advogado perguntaria, em «FONTE_TITULO» 400.
- Resposta curta e direta, até 65 caracteres por linha.
- Nenhuma começa aberta, exceto quando a página chega pela âncora daquela pergunta.
"""+nos("Landing: seção Perguntas. «CRM»: `Disclosure.tsx`. Radix `accordion`."),
f"""<div style="max-width:720px">
<details class="aj-sanfona" open><summary>Quanto tempo leva para começar?{ic('mais')}</summary><div class="aj-sanfona__corpo">O diagnóstico acontece na primeira semana. Depois dele, a implementação segue marcos de 30, 60 e 90 dias.</div></details>
<details class="aj-sanfona"><summary>Preciso ter equipe comercial?{ic('mais')}</summary><div class="aj-sanfona__corpo">[Resposta da «SIGLA»]</div></details>
<details class="aj-sanfona"><summary>Vocês atendem qualquer área do direito?{ic('mais')}</summary><div class="aj-sanfona__corpo">[Resposta da «SIGLA»]</div></details>
</div>""")

# gráfico: barras (1 série) + linhas (2 séries) — valores de exemplo
meses=['abr','mai','jun','jul','ago','set']; vals=[184,203,221,247,284,318]
W,H,x0,y0=560,220,36,190; mx=350
bars=''
for i,(m,v) in enumerate(zip(meses,vals)):
    bw=48; gap=(W-x0-6*bw)/6; x=x0+gap/2+i*(bw+gap); h=v/mx*(y0-20); y=y0-h
    bars+=f'<rect class="d1 marca-barra" x="{x:.1f}" y="{y:.1f}" width="{bw}" height="{h:.1f}" rx="4"><title>{m}: {v} contratos</title></rect><text class="eixo" x="{x+bw/2:.1f}" y="{y0+18}" text-anchor="middle">{m}</text>'
    if i==5: bars+=f'<text class="valor" x="{x+bw/2:.1f}" y="{y-8:.1f}" text-anchor="middle">{v}</text>'
grade=''.join(f'<line class="grade" x1="{x0}" x2="{W}" y1="{y0-t/mx*(y0-20):.1f}" y2="{y0-t/mx*(y0-20):.1f}"/><text class="eixo" x="{x0-8}" y="{y0-t/mx*(y0-20)+4:.1f}" text-anchor="end">{t}</text>' for t in (0,100,200,300))
g1=[58,54,49,47,44,41]; g2=[39,42,45,43,48,52]; lmx=70
def pts(vs): return [(x0+20+i*((W-x0-40)/5), y0-v/lmx*(y0-20)) for i,v in enumerate(vs)]
def poly(vs,c): p=pts(vs); return f'<polyline class="linha-serie {c}" points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in p)}"/>'+''.join(f'<circle class="ponto {c.replace("l","d")}" cx="{a:.1f}" cy="{b:.1f}" r="4"><title>{meses[i]}: R$ {vs[i]}</title></circle>' for i,(a,b) in enumerate(p))
grade2=''.join(f'<line class="grade" x1="{x0}" x2="{W}" y1="{y0-t/lmx*(y0-20):.1f}" y2="{y0-t/lmx*(y0-20):.1f}"/><text class="eixo" x="{x0-8}" y="{y0-t/lmx*(y0-20)+4:.1f}" text-anchor="end">{t}</text>' for t in (0,20,40,60))
eixo2=''.join(f'<text class="eixo" x="{a:.1f}" y="{y0+18}" text-anchor="middle">{meses[i]}</text>' for i,(a,b) in enumerate(pts(g1)))
p1=pts(g1)[-1]; p2=pts(g2)[-1]
comp('Grafico','Conteúdo',420,"""# Grafico
Gráficos de barras e linhas dos painéis e relatórios, com as cores de dados da marca.

**O que você fornece:** um `aj-cartao` com `aj-grafico`: cabeça (título + `Abas` de período), legenda (`aj-grafico__legenda`, a partir de 2 séries) e o SVG com as classes `grade`, `eixo`, `valor`, `d1`–`d3` (preenchimento) e `l1`–`l3` (linha).

- **Uma série:** tudo em `dado-1` (o violeta). É o caso mais comum.
- **Duas ou três séries:** `dado-1`, `dado-2` (laranja) e `dado-3` (verde-água), nesta ordem, sempre. Validado para daltonismo nos dois temas. Mais de três: agrupe em "Outros" ou divida em gráficos.
- As cores de dados só existem dentro de gráficos. Nunca em botão, texto ou fundo.
- Um eixo só. Duas medidas de escalas diferentes viram dois gráficos.
- Barras finas com canto de 4 px, linhas de 2 px, pontos de 8 px com anel da cor da superfície.
- Rótulo direto só no ponto que importa (o último mês); o resto aparece ao passar o mouse.
- Texto e números em `texto`/`texto-3`, nunca na cor da série. `dado-3` fica abaixo de 3:1 no claro: sempre com rótulo direto ou tabela ao lado.
"""+nos("Painel: `chart.tsx` (Recharts) — passe `dado-1`…`dado-3` como cores e `linha` na grade. «SISTEMA»: `chart-1`…`chart-3` na ponte shadcn apontam para estas cores."),
f"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;max-width:1180px">
<div class="aj-cartao aj-grafico"><div class="aj-grafico__cabeca"><div><h3 class="aj-cartao__titulo">Contratos por mês</h3><span class="aj-ajuda">Dados de exemplo</span></div></div>
<svg viewBox="0 0 {W} {H}" role="img" aria-label="Barras: contratos por mês, de 184 em abril a 318 em setembro">{grade}{bars}</svg></div>
<div class="aj-cartao aj-grafico"><div class="aj-grafico__cabeca"><div><h3 class="aj-cartao__titulo">Custo por lead</h3><span class="aj-ajuda">Dados de exemplo</span></div>
<ul class="aj-grafico__legenda"><li><i style="background:var(--dado-1)"></i>Google</li><li><i style="background:var(--dado-2)"></i>Meta</li></ul></div>
<svg viewBox="0 0 {W} {H}" role="img" aria-label="Linhas: custo por lead no Google cai de 58 para 41 reais; no Meta sobe de 39 para 52 reais">{grade2}{poly(g1,'l1')}{poly(g2,'l2')}{eixo2}<text class="valor" x="{p1[0]+8:.1f}" y="{p1[1]+4:.1f}">R$ 41</text><text class="valor" x="{p2[0]+8:.1f}" y="{p2[1]+4:.1f}">R$ 52</text></svg></div>
</div>""")

comp('Depoimento','Conteúdo',470,"""# Depoimento
Depoimento em vídeo de cliente, com a frase principal e o resultado: a prova social da landing.

**O que você fornece:** `aj-depoimento` com o vídeo (`aj-depoimento__video`: capa real do vídeo em `<img>` e o botão `aj-depoimento__play` com `aria-label`), a frase (`aj-depoimento__frase`, trecho literal do vídeo) e o autor (`Avatar` + nome, escritório e o resultado numa `Etiqueta`).

- A frase é um trecho real do vídeo, entre aspas, sem editar o sentido.
- Resultado com número e período reais ("14 → 50 contratos por mês"). Sem número real, sem etiqueta.
- Foto e nome só com autorização do cliente.
""",
f"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;max-width:900px">
<div class="aj-depoimento"><div class="aj-depoimento__video"><button class="aj-depoimento__play" aria-label="Assistir depoimento">{ic('play')}</button></div>
<p class="aj-depoimento__frase">“[Trecho literal do depoimento em vídeo]”</p>
<div class="aj-depoimento__autor"><span class="aj-avatar">AN</span><div><b>[Nome do cliente]</b>[Escritório] · <span class="aj-etiqueta aj-etiqueta--sucesso">[resultado real]</span></div></div></div>
<div class="aj-depoimento"><div class="aj-depoimento__video"><button class="aj-depoimento__play" aria-label="Assistir depoimento">{ic('play')}</button></div>
<p class="aj-depoimento__frase">“[Trecho literal do depoimento em vídeo]”</p>
<div class="aj-depoimento__autor"><span class="aj-avatar">MP</span><div><b>[Nome do cliente]</b>[Escritório] · <span class="aj-etiqueta aj-etiqueta--sucesso">[resultado real]</span></div></div></div>
</div>""")

comp('CabecalhoSite','Navegação',430,"""# CabecalhoSite
O topo do site e das landings: assinatura, links para as seções e a ação principal. No celular, só o símbolo, a ação e o botão de menu.

**O que você fornece:** `<header class="aj-cabecalho">` com `aj-cabecalho__marca` (símbolo + `<span>` com o nome, que some no celular), `<nav class="aj-cabecalho__links">` (até 4 âncoras), a ação (`aj-botao--principal`) e `aj-cabecalho__menu` (`BotaoIcone` que abre o `aj-menu-movel`).

- A ação do topo é a mesma da página: "Fazer aplicação". Nada de WhatsApp direto.
- Links são âncoras da própria página, na ordem em que as seções aparecem.
- Pode fixar no topo ao rolar (camada `camada-fixo`) com fundo `fundo` chapado, sem vidro.
""",
f"""<div style="display:grid;grid-template-columns:1fr 340px;gap:24px;align-items:start">
<div style="padding:0 24px;border:1px solid var(--linha);border-radius:var(--raio-lg);background:var(--fundo)"><header class="aj-cabecalho"><a class="aj-cabecalho__marca" href="#">{MARCA_NOME()}</a><nav class="aj-cabecalho__links" aria-label="Seções"><a href="#">«METODO»</a><a href="#">Resultados</a><a href="#">Perguntas</a></nav><a class="aj-botao aj-botao--principal" href="#">Fazer aplicação</a></header></div>
<div style="display:grid;gap:10px;padding:0 16px 16px;border:1px solid var(--linha);border-radius:var(--raio-lg);background:var(--fundo)"><header class="aj-cabecalho" style="padding:16px 0"><a class="aj-cabecalho__marca" href="#">{SIMB()}</a><div style="display:flex;gap:8px"><a class="aj-botao aj-botao--principal aj-botao--sm" href="#">Fazer aplicação</a><button class="aj-botao-icone" aria-label="Abrir menu" aria-expanded="true">{ic('menu')}</button></div></header>
<nav class="aj-menu-movel" aria-label="Seções"><a href="#">«METODO»</a><a href="#">Resultados</a><a href="#">Perguntas</a></nav></div>
</div>""")

comp('RodapeSite','Navegação',330,"""# RodapeSite
O fim de toda página do site: assinatura, a frase do lema, links úteis e a linha legal.

**O que você fornece:** `<footer class="aj-rodape">` com o topo (`aj-rodape__topo`: assinatura + `aj-rodape__frase` à esquerda, `aj-rodape__colunas` à direita) e a base (`aj-rodape__base`: direitos e política de privacidade).

- A frase é o lema para o cliente, com a ênfase da marca.
- Até 3 colunas de links. Contato leva à aplicação, não a um número de WhatsApp.
- Na base: "© 2026 «NOME»" e o CNPJ ([preencher]) e o link da Política de privacidade.
""",
f"""<div style="padding:0 32px;border:1px solid var(--linha);border-radius:var(--raio-lg);background:var(--fundo)"><footer class="aj-rodape">
<div class="aj-rodape__topo"><div><a class="aj-cabecalho__marca" href="#">{MARCA_NOME()}</a><p class="aj-rodape__frase">Finalmente, alguém que <b>se importa</b> com o seu escritório.</p></div>
<div class="aj-rodape__colunas"><div class="aj-rodape__coluna"><strong>Método</strong><a href="#">Os 4 pilares</a><a href="#">Resultados</a><a href="#">Perguntas</a></div><div class="aj-rodape__coluna"><strong>Começar</strong><a href="#">Fazer aplicação</a><a href="#">Instagram</a></div></div></div>
<div class="aj-rodape__base"><span>© 2026 «NOME» · CNPJ [preencher]</span><a href="#" style="color:inherit">Política de privacidade</a></div>
</footer></div>""")

# ---------- v2.2 · documentos
SEC=[('diagnostico','Diagnóstico'),('atendimento','Atendimento'),('dados','Dados e documentos'),('crm','CRM'),('whatsapp','WhatsApp e robôs'),('marketing','Marketing'),('checklist','Checklist'),('proximos','Próximos passos')]
def sumario(itens): return '<nav aria-label="Sumário"><ol class="aj-sumario">'+''.join(f'<li><a href="#{i}"><span class="aj-sumario__n">{n:02d}</span>{t}</a></li>' for n,(i,t) in enumerate(itens,1))+'</ol></nav>'
comp('Sumario','Navegação',200,"""# Sumario
O índice das seções de um documento, relatório ou resumo de reunião: uma grade leve dentro da capa, com o número em violeta e o nome da seção, sem linhas nem caixas.

**O que você fornece:** `<nav aria-label="Sumário"><ol class="aj-sumario">` com um `<li>` por seção, cada um com `<a href="#id">`, o número de dois dígitos em `aj-sumario__n` ("01") e o nome da seção. Com 3, 6 ou 9 seções, use `aj-sumario--3`.

- Tela: 4 colunas (8 seções ficam em 2 fileiras de 4). Celular e PDF: 2 colunas, para nenhum nome quebrar em duas linhas.
- Fica dentro da capa, logo depois das etiquetas, com o mesmo respiro da capa. Não é uma tabela: sem linhas entre os itens, sem caixa em volta.
- Nunca monte o sumário como linha de botões ou pílulas que quebra onde couber: é isso que deixa o último item sozinho.
- Nome da seção em até 3 palavras.
- No PDF, os links continuam funcionando.
""",sumario(SEC))
DOC=f'''<div class="aj-doc" style="max-width:960px">
<div class="aj-doc__topo"><span style="display:flex;align-items:center;gap:10px;font:600 15px/20px «PILHA_TITULO»;letter-spacing:-.02em">{SIMB()+"«SIGLA»" if SIMBOLO else SIMB()}</span><small style="color:var(--texto-3);font-size:13px">Resumo de reunião · uso interno</small></div>
<div class="aj-doc__capa aj-halo"><span class="aj-rotulo">Reunião de 24/09/2026</span><h1 class="aj-titulo aj-titulo--display">Boas práticas de <b>atendimento</b></h1>
<p class="aj-subtitulo">O que ficou alinhado na reunião de processo comercial: como conduzir o lead no WhatsApp, como usar o CRM e o que muda no marketing.</p>
<div class="aj-doc__meta"><span class="aj-etiqueta aj-etiqueta--marca">Reconhecimento de vínculo trabalhista</span><span class="aj-etiqueta">3 participantes</span></div></div>
<div class="aj-doc__sumario">{sumario(SEC)}</div>
<section class="aj-doc__secao" id="diagnostico"><div class="aj-doc__cabeca"><span class="aj-rotulo">01 · Diagnóstico</span><h2 class="aj-titulo aj-titulo--secao">O que está acontecendo com os <b>leads</b></h2><p class="aj-subtitulo">Os leads têm o direito, mas chegam com pouca prontidão para entrar com a ação.</p></div>
<div class="aj-doc__grade aj-doc__grade--3">
<div class="aj-cartao" style="display:grid;gap:8px"><h3 class="aj-cartao__titulo">Curiosos, não compradores</h3><p class="aj-subtitulo" style="font-size:14px;line-height:22px">Chegam querendo saber se têm direito, não querendo contratar.</p></div>
<div class="aj-cartao" style="display:grid;gap:8px"><h3 class="aj-cartao__titulo">Pouca prontidão</h3><p class="aj-subtitulo" style="font-size:14px;line-height:22px">Não têm documentos e adiam a decisão.</p></div>
<div class="aj-cartao" style="display:grid;gap:8px"><h3 class="aj-cartao__titulo">Produto, não execução</h3><p class="aj-subtitulo" style="font-size:14px;line-height:22px">O gargalo está no produto e na consciência do público.</p></div>
</div></section></div>'''
comp('Documento','Telas',1000,"""# Documento
O modelo de relatório, resumo de reunião e proposta em HTML que também vira PDF A4: topo, capa, sumário, seções numeradas e cartões.

**O que você fornece:** `<main class="aj-doc">` com `aj-doc__topo` (símbolo + natureza do documento), `aj-doc__capa` (rótulo com a data, título `aj-titulo--display` com a ênfase da marca, subtítulo, etiquetas em `aj-doc__meta`), `aj-doc__sumario` (o `Sumario`) e uma `<section class="aj-doc__secao" id>` por seção, cada uma com `aj-doc__cabeca` e o conteúdo.

**Grades de cartões:** use `aj-doc__grade--2`, `--3` ou `--4` com um número de cartões que caiba certo: 2, 4 ou 6 na de 2; 3 ou 6 na de 3; 4 ou 8 na de 4. Nunca uma grade automática que deixe um cartão sozinho na última linha. No celular a de 3 vira uma coluna e a de 4 vira 2 × 2.

**No PDF (imprimir › salvar como PDF, A4):**
- Margem de 14 mm em cima e embaixo e 16 mm nas laterais.
- A primeira página é a capa com o sumário; quando a primeira seção não cabe inteira embaixo dele, ela começa na página seguinte (nunca o título sozinho no pé).
- O halo da capa não é recortado no PDF: ele se esvai sozinho sobre o sumário.
- Cartão, linha de tabela, alerta e item de lista nunca se partem entre páginas. O cabeçalho de seção nunca fica sozinho no pé da página.
- Parágrafo com no mínimo 3 linhas em cada lado da quebra.
- As cores e o halo saem na impressão (`print-color-adjust: exact`); a animação para.
- O que só serve na tela leva a classe `so-tela` e some no PDF.
""",DOC,' width=1000 page')
