---
name: brainstorm
description: Brainstorm de design em dois modos — divergente, para descobrir o que procurar antes de buscar referências, e convergente, para cravar a direção mais assertiva depois de tê-las. Roda sozinho ou dentro do pipeline do design-squad.
argument-hint: [divergente|convergente] <slug ou descrição do projeto>
user-invocable: true
allowed-tools: [Read, Write, Edit, Glob, Grep, AskUserQuestion]
---

<!--
PAPEL (pt-BR): É o brainstorm que faltava — a skill /brainstorming não existe
nesta máquina, então esta foi feita sob medida para design. Dois modos com
objetivos opostos: um abre o leque antes da busca, o outro fecha o leque antes
do DNA. Roda na sessão principal porque precisa conversar com o usuário.
-->

# Brainstorm de design

Two modes, opposite jobs — plus a third, **plataforma**, used only by the `identidade` flow before any visual work. Pick by the argument, or by what exists on disk: no `REFERENCIAS.md` yet means divergent; references in hand means convergent.

**Every question you ask is in pt-BR, and every question is an `AskUserQuestion` with labeled options.** Do not make the user type prose. The user tells you what the user wants by clicking, and by writing a line when the user wants to.

Ask **one question per call with up to four options**, or group at most three related questions into one call. Never chain more than three calls in a mode — a brainstorm that becomes a questionnaire gets abandoned.

---

## Modo divergente — "o que a gente vai procurar?"

Runs when the user has no references. Its output is what stops the scout from searching blind.

Read `BRIEFING.md` and `marca/` first. **Do not ask what you can already read.** If the brief names the vertical, do not ask for the vertical — ask what the brief left open.

What to draw out, in roughly this order:

**A sensação.** The highest-value question and the one people ask badly. Never offer "moderno / clássico / minimalista" — those words mean nothing and produce generic. Offer concrete, opposed images with a consequence attached: *"sério feito cartório — tipografia com peso, pouca cor, nada anima"* versus *"afiado feito escritório de M&A — muito branco, uma cor só, tudo alinhado ao milímetro"* versus *"caloroso feito consultório — cor quente, cantos arredondados, foto de gente"*. The user picks a world, not an adjective.

**O trabalho único.** What has to happen when someone lands here — a call booked, a form filled, a name remembered, a doubt killed. One thing. A page that does three things does none.

**Três marcas que ele admira, e por quê.** The "why" is the payload. "Gosto da Apple" is worthless; "gosto de como a Apple deixa a página quase vazia e ainda assim eu sei exatamente onde clicar" is a design instruction.

**O que ele não quer de jeito nenhum.** The single most productive question in the whole pipeline. Negative constraints are sharper, easier to answer, and easier to check than positive ones. Offer real options drawn from what actually goes wrong — *"nada de foto de banco de imagem com gente sorrindo de terno"*, *"nada de gradiente roxo de startup"*, *"nada de ícone genérico de linha fina"* — plus room for the user's own.

Check `marca/REJEITADOS.md` before asking, and do not re-ask what the user has already killed. Show the user what you already know the user rejects and ask only whether it still holds.

### Saída — `<projeto>/RUMO.md`, em pt-BR

```
# RUMO — <slug>
## Sensação          o mundo escolhido, nas palavras dele + a consequência de design
## Trabalho único    uma frase
## Admira            marca | o que exatamente ele admira nela
## Proibido          o que ele não quer, verbatim
## Vetor de busca    3–5 consultas CONCRETAS que o scout vai rodar
## Onde procurar     tipos de site que provavelmente resolveram isso bem
```

The queries are the deliverable. Not "sites de advocacia bonitos" — something a search engine can actually use: *"escritório boutique de direito tributário site tipografia serifa"*, *"landing page consultoria B2B prova social sem depoimento genérico"*. Include the language and the register in the query when they matter.

---

## Modo convergente — "qual é a direção mais assertiva?"

Always runs, with the references in hand. Its job is to force the decision **before** anyone spends tokens on a DNA.

Read `REFERENCIAS.md`, `BRIEFING.md`, `RUMO.md` if it exists, and `marca/`.

Present what you have compactly — the reference name and its one-line "o que a gente rouba" — then converge:

**De cada referência, o que exatamente puxamos?** Not "gostei da R2". Which layer: the typography of one, the layout rhythm of another, the palette of none of them. Make this concrete by offering the layers as options per reference. A design assembled from three whole references is a collage; a design assembled from one layer of each is a direction.

**A tese da página, em uma frase.** What it argues. "Este escritório resolve o problema que os grandes não pegam" is a thesis; "somos os melhores" is not. This becomes the hero, and `frontend-design` is explicit that the hero is a thesis.

**Onde vai a única ousadia?** The boldness gets spent in one place and everything around it stays quiet. Offer the candidates: the typography, the hero, one moment of motion, the color, a structural device. The user picks one. Picking two is picking none.

**A estrutura do argumento** — for a sales page or anything that has to convert: what is the offer, what is the proof, and what is the one objection that kills the sale. This feeds the builder's copy, which is why there is no separate copywriter agent.

### Saída — `<projeto>/DIRECAO.md`, em pt-BR

```
# DIREÇÃO — <slug>
## Tese              uma frase — o que a página argumenta
## Camadas puxadas   referência | camada (tipografia/layout/paleta/movimento) | por quê
## A ousadia         onde vai, e por que ali
## Fica quieto       o que fica disciplinado ao redor da ousadia
## Argumento         oferta | prova | objeção principal e como ela morre
## Fora de questão   restrições duras vindas desta conversa e de marca/REJEITADOS.md
## Palavras dele     verbatim, em pt-BR
```

**This file is a constraint for the art director, not a suggestion.** Write it precisely enough to be obeyed. Where you leave an axis open, say so explicitly — silence reads as freedom, and freedom on an unstated axis is where generic design comes from.

---

## Modo plataforma — "o que essa marca é?" *(só no fluxo identidade)*

Runs first in the `identidade` flow, before references. Its output is the platform every later stage obeys. Read `BRIEFING-MARCA.md`, `marca/clientes/<cliente>.md` and anything the client supplied (old logo, site, deck, transcript). **Do not ask what those already answer.**

What to draw out, with the same rules (labelled options, at most three calls):

**A tese.** What the company argues that competitors don't. Offer 2–3 candidate theses written from the material, not generic claims.

**A sensação.** Concrete, opposed worlds with a consequence each, exactly as in the divergent mode (never "moderno / clássico"). In the AJ project the winning answer was *"tecnologia que acolhe"* — a world, not an adjective.

**O ponto de partida do símbolo.** *Evoluir o que existe* / *Partir do zero* / *Só tipografia (sem símbolo)*. Show the existing mark if there is one.

**O que ela nunca é.** Sector clichés and looks the user rejects, offered as real options.

### Saída — `<projeto>/PLATAFORMA.md`, em pt-BR

```
# PLATAFORMA DA MARCA — <nome>
## Tese            uma frase
## Lema            a frase que o cliente diria
## Sensação        o mundo escolhido + a consequência de design
## Personalidade   3–5 traços, cada um com o que ele faz e o que ele nunca faz
## Nome            como a marca é escrita e abreviada (com acento)
## Símbolo         evoluir / do zero / só tipografia, e o que ele precisa dizer
## Nunca é         verbatim
## Vetor de busca  3–5 consultas concretas para o caça-referências (Behance, sites de estúdio)
## Palavras dele   verbatim
```

---

## O que os dois modos nunca fazem

Do not propose a palette, a font pairing, or a layout. That is the art director's job at estágio 5. If you decide the design here, the user reacts to your guess instead of to the user's own references — and the two brainstorms exist precisely so the direction comes from the user.
