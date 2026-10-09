---
name: design-anunciojuridico
description: >
  Marca e design system da Anúncio Jurídico (AJ), identidade v2 — símbolo A2 Dobra,
  violeta #5B2BE0, Sora + Manrope, marca plana com luz (halo no claro, brilho no escuro).
  Use SEMPRE que for criar ou alterar qualquer peça da AJ: landing page, site, telas do
  AJ OPS ou do Nosso CRM, painel, relatório, resumo de reunião, proposta, PDF, apresentação,
  slide, post, story, e-mail, assinatura, logo, ícone ou gráfico. Substitui a versão antiga
  (Rubik, roxo #7c3aed, dark com glow): nunca use as regras antigas. Não serve para clientes
  da AJ (HW Rocha e outros têm skill própria).
---

# Marca AJ (Anúncio Jurídico) — identidade v2

Versão %%VERSAO%%. Gerada por `interface/fonte/gen_skill.py` a partir do Design System; não edite à mão.

**Tecnologia que acolhe: precisa, calma e plana.** A AJ é a empresa de tecnologia que se importa com o negócio do advogado.

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
| Tela do AJ OPS, Nosso CRM, painel do cliente | `NavegacaoLateral`, `TituloDePagina`, `Tabela`, `Etiqueta`, `BotaoIcone`, `MenuSuspenso`, `Selecao`, `Campo`, `Escolhas`, `BuscaEFiltros`, `PaginacaoETrilha`, `Abas`, `Cartao`, `Indicador`, `Modal`, `PainelLateral`, `Aviso`, `Alerta`, `EstadoVazio`, `Esqueleto`, `Carregando`; `referencias/plataformas.md` | composição **Painel**; `TelaAJOps`, `TelaCRM` |
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

- **Plana.** Cor chapada. Sem vidro, sem gradiente em botão, cartão ou símbolo, sem 3D como padrão.
- **Uma cor:** violeta `#5B2BE0`. Lavanda `#D9CCFF` e luz `#B9A4FF` são o violeta iluminado. O resto é neutro: noite `#0B0620`, névoa `#F4F2FB`, branco quente `#FCFBFF`, grafite `#4B4566`. Exceção única: as cores de dados (`dado-2` laranja, `dado-3` verde-água) **só dentro de gráficos**.
- **Luz:** halo desfocado no fundo claro (nunca terminando em corte reto) e brilho do símbolo lavanda no escuro. Gradiente só no fundo e só na família do violeta.
- **Tipografia:** Sora nos títulos (300, com **uma** ênfase em 600; no máximo duas quando o título tem número e resultado) e Manrope no texto e na interface.
- **Símbolo A2 Dobra** sempre de arquivo. "AJ na frente": o símbolo sozinho é a marca do dia a dia; "Anúncio Jurídico" (com acento) na assinatura completa.
- **Composição:** Centrada (uma ação só), Leitura (marketing e documentos, à esquerda até 1180 px) ou Painel (sistemas). Nunca misture alinhamentos num bloco. Cartão só agrupa. Botão grande só no marketing.
- **Celular primeiro** (390 px): o público chega pela bio do Instagram.
- **Nada de item órfão:** sumário em grade leve; grades de cartões com colunas que fecham certo.
- **Voz:** segunda pessoa, frase curta, verbo + objeto no botão, erro que diz como resolver, número real ou nenhum.
- **Toda ação da landing leva ao formulário de aplicação/diagnóstico.** WhatsApp só depois do formulário, nunca link direto.

## Proibido

Clichê jurídico (balança, martelo, Themis, coluna, foto de banco com terno) · roxo neon, glow difuso, visual "espacial" · Rubik, Inter ou qualquer fonte fora de Sora/Manrope · a identidade antiga (roxo `#7c3aed`, "Anuncio" branco + "Juridico" roxo) · gradiente, contorno, sombra ou distorção no símbolo · emoji e ícone colorido · borda colorida na lateral de cartão · promessa sem prova · jargão de agência ("alavancar", "potencializar").

## Checklist antes de entregar

- [ ] Li `regras.md` e o arquivo de cada componente usado.
- [ ] Todas as cores, fontes, raios e sombras vêm dos tokens (`aj-tokens.css`).
- [ ] Um modelo de composição por tela; alinhamento único em cada bloco.
- [ ] Título com uma ênfase (duas só com número + resultado).
- [ ] Contraste: texto sobre os fundos permitidos; status sempre com palavra.
- [ ] Funciona em 390 px sem rolagem lateral; testei o tema escuro, se existir.
- [ ] Nenhum item sozinho numa linha (sumário, grades, rodapé).
- [ ] Halo sem corte reto; nada de gradiente no símbolo.
- [ ] Em PDF: A4, sumário na capa, nada partido entre páginas.
- [ ] Textos em pt-BR, com acento, na voz da marca; dados de exemplo marcados como exemplo.

## Mapa dos arquivos

```
referencias/
  regras.md            regras completas da marca (leia sempre)
  tokens.md            valores de todos os tokens, claro e escuro
  empresa.md           dados da empresa, produto, lema, provas, contatos, links
  plataformas.md       como aplicar no AJ OPS, painel e Nosso CRM (pontes CSS)
  apresentacao.md      estrutura da apresentação da marca
  componentes/INDICE.md e um arquivo por componente (regra + código)
assets/
  css/                 aj-tokens.css, aj-componentes.css, ponte-shadcn.css, ponte-nossocrm.css
  logos/               símbolo, assinaturas, ícone de app, favicon (SVG)
  modelos/             documento.html, instagram-*.html, og-compartilhamento.html, assinatura-email.html
```
