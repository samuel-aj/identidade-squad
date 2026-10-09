---
name: identidade
description: Cria a identidade visual completa de uma marca, do zero ou evoluindo a existente — plataforma, referências e moodboard, território visual, símbolo calculado, logo final, sistema de interface com 37 componentes, aplicações, auditoria independente e, no fim, a skill de design da marca gerada e publicada. É o processo que construiu a marca da Anúncio Jurídico, transformado em squad. Retoma de onde parou se o projeto já existir.
argument-hint: <nome da marca ou empresa, ou o slug de um projeto para retomar>
user-invocable: true
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Skill, Agent, AskUserQuestion, Artifact, WebFetch]
---

<!--
PAPEL (pt-BR): Orquestra a criação de uma marca inteira. Roda na sessão
principal porque faz as perguntas e publica as páginas. Cada etapa grava em
disco; a próxima só lê arquivo. As lições da AJ estão embutidas: regra antes
de tela, lista fechada de componentes, uma rodada de opções, testes de PDF e
contraste, auditoria por quem não criou e a skill da marca como entrega final.
-->

# Identidade — da plataforma à skill da marca

You are running the brand-identity pipeline. Everything you say to the user is in **pt-BR** — every question, summary and label. The user never reads or writes English.

## What this flow learned from the AJ brand (do not relearn it)

1. **Rules before screens.** A screen built before its rule exists comes out wrong (the AJ login came out left-aligned and cluttered). Any screen defect means a missing rule: write the rule, then fix the screen.
2. **The component list is closed.** 37 components from the molde, all of them. The AJ lost a round when the user found the dropdown (and 19 others) missing.
3. **One round of options, structurally different.** Territories, symbols and hero layouts come in one round of three that differ in structure. The AJ landing lost two rounds to "title on the left + something on the side" three times.
4. **Test what breaks.** Contrast, leftovers, PDF breaks at 23 positions and a render of every component run before anyone calls it done. The AJ report broke at the summary, at the halo cut and at a section header alone at the foot of a page.
5. **The builder never audits.** A fresh-context auditor does.
6. **The skill is the deliverable.** It is generated from the system, not written by hand at the end.
7. **One publish command.** No hand-syncing six places.

## How to talk to the user

- **The user decides by seeing.** Every gate shows a rendered image or a live page. Never ask the user to judge a hex list or a parameter.
- **Don't ask granular design questions.** Decide with the skills (`frontend-design`, the molde's rules), record the decision and the reason, and show the result.
- **Gates** use `AskUserQuestion` with 3–4 labeled options that carry consequences, never yes/no. Record the user's answer **verbatim** in `RUN.md`.
- The user may be building a brand **for a client**. Questions about the client's business are about facts; if the user doesn't know, mark it `A CONFIRMAR COM O CLIENTE` and move on — never invent.

---

## Estágio 0 — boot

Slugify the argument into `<slug>`. Work in the **current folder** (the user's work folder, the same one every time): project root `projetos/<slug>/`, squad memory `marca/`.

- If `marca/` does not exist here, create it by copying `${CLAUDE_PLUGIN_ROOT}/marca-inicial/` (`cp -R ${CLAUDE_PLUGIN_ROOT}/marca-inicial marca`) and tell the user in one line that the squad's memory lives there. If the folder looks wrong (home directory, Desktop, a code repo), ask once which folder to use before creating anything.

- If `projetos/<slug>/RUN.md` exists, read `## Próxima ação` and ask: *continuar dali* / *recomeçar a etapa atual* / *começar do zero (guarda o que existe em _antes/)*.
- Probe once and record in `RUN.md ## Capacidades`: `Artifact` tool available? `node` on PATH or in `~/.local/node/bin`? Tools installed (`~/.cache/design-squad-identidade`)? If the tools are missing, run `${CLAUDE_PLUGIN_ROOT}/molde-marca/ferramentas/instalar.sh` — do not improvise substitutes.
- Read `marca/CASA.md`, `GOSTO.md`, `REJEITADOS.md`, `BIBLIOTECA.md`, and `marca/clientes/<cliente>.md` if it exists (create it from `_MODELO.md` if not).

## Estágio 1 — briefing da marca

**Do not interview.** Read everything the user gave (old logo, site, deck, meeting transcript, Instagram). Draft `BRIEFING-MARCA.md` with assumptions marked `SUPOSTO`: empresa, o que vende, público e por onde chega, onde a marca vai viver (site, landing, sistemas, documentos, redes, apresentações), concorrentes, marca atual (se houver), restrições. Then **one** `AskUserQuestion` confirming the two assumptions that matter most.

## Estágio 2 — plataforma

`Skill(brainstorm)` in **modo plataforma** → `PLATAFORMA.md`. Then write `RUMO.md` from its `## Vetor de busca` so the scout has concrete queries.

## Estágio 3 — referências e moodboard

Dispatch `Agent(identidade-visual:caca-referencias)` (Mode A if the user sent references, Mode B otherwise; for identity, Behance with `?search=...&field=branding` and studio case studies work best). Publish a **moodboard** page with the `Artifact` tool (load `artifact-design` first): each reference with its image and the one line "o que a gente puxa".

**Portão A** (only if the squad scouted): which references stay, and — more valuable — what the user rejects and why, verbatim into `marca/REJEITADOS.md`.

## Estágio 4 — território

Dispatch `Agent(identidade-visual:diretor-de-arte)` in **modo identidade** → `DIRECAO-MARCA.md` + three territory pranchas.

**Portão 1 — obrigatório.** Show the three pranchas (images, not text). Options: *T1* / *T2* / *T3* / *Misturar: a camada X de um com o resto de outro*. If the user picks none, **do not run another round of three**: ask what is wrong in one line, then take authorship — build the one territory you believe in and show it. Losing territories go to `marca/REJEITADOS.md` with the user's reason verbatim.

## Estágio 5 — símbolo e logo

Dispatch `Agent(identidade-visual:geometra)` in Mode A → `identidade/simbolo/PROPOSTAS.md` + `prancha.png`.

**Portão 2 — obrigatório.** Show the prancha. Options: the three concepts + *ajustar o escolhido (diga o quê)*. Then dispatch the geometer in Mode B with the user's words.

Then generate the final logo, in `identidade/logo/` (copy the scripts from `molde-marca/logo/`): `gera_final.py` → `png.js` → `ico.py` → `video.js`. Look at the signatures and the favicon at 16 px before moving on.

## Estágio 5b — apresentação da marca *(marca de cliente)*

When the brand belongs to a client (not to the user themselves), build the **presentation** right after the logo is approved and **before** the system. The client approves a brand, not 37 components: the deck tells the whole brand once (platform, logo, colors, type, the phrase rule, applications drawn with the rules already locked) and becomes the client's approval gate. Only then does the architect build the system, on approved ground. Use the Slides type (`Artifact(action: "quickstart", intent: "slides")`), the brand's own colors and type (no default design system), and the client's real photos. Pages sent to the client carry only what the client must judge — never internal notes, old rounds or competitor anti-references. Learned on Kleiciane Rocha (02/10/2026), the user's words: "para mostrar para o cliente, seria interessante ter uma apresentação da marca."

## Estágio 6 — sistema

Dispatch `Agent(identidade-visual:arquiteto-de-sistema)` → `marca.json`, rules, 37 components, the generated skill, `SISTEMA.md`, all four checks passing.

**Publish the Design System** as an Artifact: `Artifact(action: "quickstart", intent: "other")`, pick the Design System type, and publish the project folder `interface/design-system/project/` (README, tokens.json, components, bundle.css) plus a Cover. Read the type's instructions from the result before publishing; the index file goes last.

**Portão 3 — obrigatório, por partes.** Show first **three screens only**: `TelaLanding`, the login (Centrada) and `Documento` (cover + summary). Options: *aprovado, seguir* / *ajustar (diga onde)* / *a direção está errada*. Only after the user's yes, show the full component prancha. Adjustments always go into the rules or tokens, then regenerate — never patch a single screen.

## Estágio 7 — aplicações

Dispatch `Agent(identidade-visual:arquiteto-de-sistema)` in **modo aplicações** — it builds them *using the brand's own generated skill*, which is the real test of the skill. Also build, in this session:
- the **brand manual** page (Artifact): platform, symbol and construction, logo files, colors, type, light, composition, components, applications;
- the **presentation** with the Slides type (`Artifact(action: "quickstart", intent: "slides")`), following `referencias/apresentacao.md` of the brand skill.

Every application is rendered and looked at before it is shown. (The AJ business card went out ugly because nobody looked.)

## Estágio 8 — auditoria

Dispatch `Agent(identidade-visual:auditor-de-marca)` → `AUDITORIA.md`.
- `APROVADO` → estágio 9.
- `REVISAR` → one architect pass with `AUDITORIA.md` as input (its `## Faltou regra` goes into the rules), regenerate, audit again.
- `REFAZER` → back to Portão 1 or 2 with the user, explaining in one paragraph what is wrong.
- **Cap at two architect passes.** A third means the direction is wrong; escalate.

## Portão final — obrigatório

Show the manual, the presentation, the Design System and the audit verdict. Options: *Aprovado — publicar* / *Ajustes pontuais (diga quais)* / *Voltar ao sistema* / *Voltar ao território*.

## Estágio 9 — entrega

1. `python3 ${CLAUDE_PLUGIN_ROOT}/molde-marca/publicar/publicar.py projetos/<slug>` prints the plan; show it. In `marca.json → publicacao` use `"destinos": ["~/.claude/skills"]` and `"guarda": "entregas/marca-<slug>"`, and **no `github` key** (the GitHub step of that script belongs to another workspace). Then run it with `--executar`: the brand skill is installed in `~/.claude/skills` and copied to the package.
2. **Delivery package** `entregas/marca-<slug>/` with `01-estrategia · 02-logo · 03-manual · 04-sistema-de-interface · 05-exploracao · 07-apresentacao · 08-aplicacoes · 09-skill` + `LEIA-ME.md` (links to the published pages, pendências, how to regenerate), zipped next to it as `marca-<slug>.zip`.
3. Tell the user, in pt-BR, where the folder and the `.zip` are, and list the Artifact links (manual, Design System, presentation). Sending to the client (Drive, site, e-mail) is the user's call: offer it, never do it unasked.

## Estágio 10 — aprendizado

In the turn right after the final gate: `marca/clientes/<cliente>.md` (hard constraints of this brand), `marca/REJEITADOS.md`, `marca/GOSTO.md` (only preferences seen twice or more), `marca/PROJETOS.md`. If this run exposed a rule or component the molde lacked, write it in `marca/MELHORIAS-DO-MOLDE.md` (what was missing, the user's words, the fix) and tell the user to send that file to whoever maintains this plugin: the installed plugin folder is overwritten on update, so never edit it. Close `RUN.md`.

## Bookkeeping, every stage

Write `RUN.md` after each stage: stage status, gate log with the user's answers verbatim, `## Próxima ação` in one line. Nothing travels between stages in context alone.
