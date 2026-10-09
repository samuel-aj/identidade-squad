---
name: %%SKILL%%
description: >
  [[ESCREVA: uma frase com a marca e seus traços visíveis (símbolo, cor principal com hex, fontes, tratamento de luz).]]
  Use SEMPRE que for criar ou alterar qualquer peça da «NOME» («SIGLA»): landing page, site, telas de sistema,
  relatório, resumo de reunião, proposta, PDF, apresentação, slide, post, story, e-mail, assinatura, logo, ícone
  ou gráfico. [[ESCREVA: se houver identidade anterior, diga que esta skill a substitui e cite o que não usar mais.]]
---

# Marca «SIGLA» («NOME»)

Versão %%VERSAO%%. Gerada por `interface/fonte/gen_skill.py` a partir do Design System; não edite à mão.

**[[ESCREVA: a sensação da marca em uma linha.]]** [[ESCREVA: uma frase sobre o que a marca é para o cliente.]]

## Procedimento obrigatório — não pule nenhum passo

1. **Leia `referencias/regras.md` inteiro.** Sempre, para qualquer peça. São as regras da marca (voz, cor, luz, tipografia, composição, gráficos, documentos, logo).
2. **Ache o tipo de peça na tabela abaixo** e leia **todos** os arquivos da linha.
3. **Antes de escrever uma tela, liste os componentes que ela terá** e abra `referencias/componentes/<Nome>.md` de **cada um**. Cada arquivo traz a regra e o código de referência pronto. Não desenhe um componente de memória. O índice completo está em `referencias/componentes/INDICE.md`.
4. **Use os arquivos de `assets/`**: os CSS (`assets/css/aj-tokens.css` + `assets/css/aj-componentes.css`) por link ou colados inteiros; os logos por arquivo, nunca redesenhados; os modelos como ponto de partida. Nunca digite uma cor, fonte ou raio fora dos tokens.
5. **Se faltar regra ou componente para algo**, não improvise em silêncio: use o mais próximo, siga os princípios e diga ao usuário qual regra faltou.
6. **Passe pela checklist do fim** antes de entregar e confira o resultado renderizado (captura de tela ou PDF), nos dois temas quando houver.

## O que ler para cada peça

| Peça | Leia (além de `regras.md`) | Parta de |
|---|---|---|
| Landing page, site | componentes `CabecalhoSite`, `RodapeSite`, `Botao`, `FormularioEtapas`, `Sanfona`, `Depoimento`, `Indicador`, `TituloDePagina`, `Simbolo`; `referencias/empresa.md` | composição **Leitura**; `TelaLanding` |
| Tela de sistema («SISTEMA», «CRM», painel) | `NavegacaoLateral`, `TituloDePagina`, `Tabela`, `Etiqueta`, `BotaoIcone`, `MenuSuspenso`, `Selecao`, `Campo`, `Escolhas`, `BuscaEFiltros`, `PaginacaoETrilha`, `Abas`, `Cartao`, `Indicador`, `Modal`, `PainelLateral`, `Aviso`, `Alerta`, `EstadoVazio`, `Esqueleto`, `Carregando`; `referencias/plataformas.md` se existir | composição **Painel**; `TelaSistema`, `TelaCRM` |
| Formulário ou login | `Campo`, `Selecao`, `Escolhas`, `Botao`, `FormularioEtapas` | composição **Centrada** (login) |
| Relatório, resumo de reunião, proposta, PDF | `Documento`, `Sumario`, `Cartao`, `Tabela`, `Alerta`, `Etiqueta` | `assets/modelos/documento.html` |
| Gráfico em painel ou relatório | `Grafico` e a seção Gráficos de `regras.md` | — |
| Post ou story de Instagram | seção Aplicações de `regras.md` | `assets/modelos/instagram-*.html` |
| Apresentação, slides | `referencias/apresentacao.md` | a apresentação publicada (link no arquivo) |
| E-mail, assinatura de e-mail | seção Aplicações de `regras.md` | `assets/modelos/assinatura-email.html` |
| Logo, ícone de app, favicon, avatar | seção Logo de `regras.md` | `assets/logos/` |
| Imagem de compartilhamento de link | seção Aplicações | `assets/modelos/og-compartilhamento.html` |
| Qualquer texto (título, botão, aviso) | seção Voz de `regras.md`; `referencias/empresa.md` | — |

Os valores de todos os tokens (cor por tema, tipografia, espaço, raio, sombra, tempo, camadas, pontos de quebra) estão em `referencias/tokens.md`.

## O essencial (vale para tudo)

[[ESCREVA: 6 a 9 tópicos curtos com o que define a marca — cor (com hex), luz, tipografia (com pesos e a regra da ênfase), símbolo, composição, celular primeiro se for o caso, voz, e a regra de conversão do negócio se houver.]]
- **Composição:** Centrada (uma ação só), Leitura (marketing e documentos, à esquerda até 1180 px) ou Painel (sistemas). Nunca misture alinhamentos num bloco. Cartão só agrupa. Botão grande só no marketing.
- **Nada de item órfão:** sumário em grade leve; grades de cartões com colunas que fecham certo.

## Proibido

[[ESCREVA: a lista do que a marca nunca faz, numa linha separada por " · ": clichês do setor, efeitos, fontes fora do sistema, a identidade anterior se houver, deformações do símbolo, emoji, promessa sem prova, jargões.]]

## Checklist antes de entregar

- [ ] Li `regras.md` e o arquivo de cada componente usado.
- [ ] Todas as cores, fontes, raios e sombras vêm dos tokens (`aj-tokens.css`).
- [ ] Um modelo de composição por tela; alinhamento único em cada bloco.
- [ ] Título com uma ênfase (duas só com número + resultado).
- [ ] Contraste: texto sobre os fundos permitidos; status sempre com palavra.
- [ ] Funciona em 390 px sem rolagem lateral; testei o tema escuro, se existir.
- [ ] Nenhum item sozinho numa linha (sumário, grades, rodapé).
- [ ] Efeitos de fundo sem corte reto; nada de efeito no símbolo.
- [ ] Em PDF: A4, sumário na capa, nada partido entre páginas.
- [ ] Textos em pt-BR, com acento, na voz da marca; dados de exemplo marcados como exemplo.

## Mapa dos arquivos

```
referencias/
  regras.md            regras completas da marca (leia sempre)
  tokens.md            valores de todos os tokens, claro e escuro
  empresa.md           dados da empresa, produto, lema, provas, contatos, links
  plataformas.md       como aplicar nos sistemas da empresa (se existir)
  apresentacao.md      estrutura das apresentações
  componentes/INDICE.md e um arquivo por componente (regra + código)
assets/
  css/                 aj-tokens.css, aj-componentes.css, ponte-shadcn.css, ponte-nossocrm.css
  logos/               símbolo, assinaturas, ícone de app, favicon (SVG)
  modelos/             documento.html, instagram-*.html, og-compartilhamento.html, assinatura-email.html
```
