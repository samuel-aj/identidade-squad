# Identidade visual — squad

Cria a identidade visual completa de um cliente, do zero ou a partir da marca que ele já tem:
plataforma, referências, território visual, símbolo, logo, **design system com 37 componentes**,
aplicações, auditoria independente e, no fim, a **skill de design da marca** pronta para usar.

É o mesmo processo que construiu a marca da Anúncio Jurídico.

## Antes de começar (uma vez só)

Você precisa do **Claude Code** instalado e com login feito, e do **Node.js** (https://nodejs.org, versão LTS).

No terminal:

```bash
claude plugin marketplace add samuel-aj/identidade-squad
```

```bash
claude plugin install identidade-visual@identidade-squad
```

```bash
claude plugin install frontend-design@claude-plugins-official
```

Na primeira marca, o squad instala sozinho o resto das ferramentas (leva alguns minutos).

## Como usar

1. Crie uma pasta de trabalho, por exemplo `Documentos/marcas`. Use **sempre a mesma**:
   é nela que o squad guarda os projetos e o que aprende sobre o seu gosto.
2. Abra o Claude Code nessa pasta.
3. Escreva:

```
/identidade-visual:identidade Nome do Cliente
```

4. Mande junto o que tiver do cliente: logo atual, site, Instagram, transcrição de reunião.
   O squad monta o briefing, faz as perguntas que importam e para em cada decisão
   mostrando imagens para você escolher.

Para continuar um projeto parado, rode o mesmo comando com o mesmo nome: ele retoma de onde parou.

## O que você recebe no fim

- `entregas/marca-<cliente>/` e o `.zip`: estratégia, logo em todos os formatos, manual,
  design system, apresentação, aplicações e a skill.
- Links do manual, do design system e da apresentação.
- A skill da marca instalada no seu Claude, para qualquer peça futura sair no padrão.

## Atualizar

```bash
claude plugin marketplace update identidade-squad
```

Se o squad apontar uma melhoria no processo, ele grava em `marca/MELHORIAS-DO-MOLDE.md`.
Mande esse arquivo para o Samuel.
