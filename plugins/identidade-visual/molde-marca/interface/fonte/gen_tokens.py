import json,sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from fonte import *
# ---------- tokens.json (formato do Design System) ----------
toks=[]
for n,c,e,u in MARCA: toks.append({'name':n,'value':c,'usage':u})
for n,c,e,u in SEM: toks.append({'name':n,'value':{'claro':c,'escuro':e},'usage':u})
for n,h in ESCALA: toks.append({'name':n,'value':h,'usage':f"Escala da cor {M['escala']['nome']} para gráficos e para sistemas que pedem escala (`primary-*`). Na interface, prefira os tokens semânticos."})
tj={'name':M['sigla'],'version':1,
 'color':{'themes':[{'id':'claro','name':'Claro'},{'id':'escuro','name':'Escuro'}],'tokens':toks},
 'type':{'fonts':[],'families':TIPO['families'],'groups':TIPO['groups']},
 'spacing':{'tokens':[{'name':n,'value':v,'usage':u} for n,v,u in ESPACO]},
 'radius':{'tokens':[{'name':n,'value':v,'usage':u} for n,v,u in RAIO]},
 'shadow':{'tokens':[{'name':n,'value':{'claro':c,'escuro':e},'usage':u} for n,c,e,u in SOMBRA]},
 'duracao':{'note':'Durações de animação. Toda animação usa `curva-marca` e respeita a preferência de movimento reduzido.','tokens':[{'name':n,'value':v,'usage':u} for n,v,u in TEMPO]},
 'curva':{'tokens':[{'name':n,'value':v,'usage':u} for n,v,u in CURVA]},
 'ponto-de-quebra':{'note':'Larguras de tela. Desenhe primeiro em 390 px.','tokens':[{'name':n,'value':v,'usage':u} for n,v,u in QUEBRA]},
 'camada':{'note':'Ordem do que fica por cima (z-index). Use o token, nunca um número solto.','tokens':[{'name':n,'value':v,'usage':u} for n,v,u in CAMADA]}}
os.makedirs(DS,exist_ok=True); json.dump(tj,open(os.path.join(DS,'tokens.json'),'w'),ensure_ascii=False,indent=1)

# ---------- <prefixo>-tokens.css (código, independente de ferramenta) ----------
def bloco(tema):
    out=[]
    for n,c,e,u in MARCA: out.append(f'  --aj-{n}: {c};')
    for n,c,e,u in SEM:
        v=c if tema=='claro' else e
        v=f'var(--aj-{v[1:-1]})' if v.startswith('{') else v
        out.append(f'  --aj-{n}: {v};')
    return out
css=['/* «SIGLA» — tokens da marca. Fonte única: marca.json + interface/fonte. Não edite à mão; regenere. */',
 "@import url('«FONTES_URL»');",'',
 ':root, [data-theme="claro"], [data-theme="aparelho"] {','  color-scheme: light;']+bloco('claro')
css+=[f'  --aj-{n}: {h};' for n,h in ESCALA]
css+=[f'  --aj-{n}: {c};' for n,c,e,u in SOMBRA]
css+=[f'  --aj-{n}: {v};' for n,v,u in ESPACO+RAIO+TEMPO+CURVA+QUEBRA+CAMADA]
css+=["  --aj-fonte-titulo: «PILHA_TITULO»;","  --aj-fonte-texto: «PILHA_TEXTO»;",'}','',
 '[data-theme="escuro"], .dark {','  color-scheme: dark;']
css+=[l for l in bloco('escuro') if not any(l.startswith(f'  --aj-{n}:') for n,*_ in MARCA)]
css+=[f'  --aj-{n}: {e};' for n,c,e,u in SOMBRA]+['}']
# Tela que segue o tema do aparelho (login, área do cliente): data-theme="aparelho" no <html> (ou no contêiner) troca os
# tokens pelo escuro quando o aparelho está no modo escuro, sem script. Peça de comunicação continua com data-theme="claro".
css+=['','@media (prefers-color-scheme: dark) {','  [data-theme="aparelho"] {','    color-scheme: dark;']
css+=['  '+l for l in bloco('escuro') if not any(l.startswith(f'  --aj-{n}:') for n,*_ in MARCA)]
css+=[f'    --aj-{n}: {e};' for n,c,e,u in SOMBRA]+['  }','}']
grava(os.path.join(INTERFACE,f'{P}-tokens.css'),'\n'.join(css)+'\n')

# ---------- ponte shadcn (sistemas e sites em Next + shadcn) ----------
def sh(t):
    R=lambda n:f'var(--aj-{n})'
    return [f'  --background: {R("fundo")};',f'  --foreground: {R("texto")};',
     f'  --card: {R("superficie")};',f'  --card-foreground: {R("texto")};',
     f'  --popover: {R("superficie")};',f'  --popover-foreground: {R("texto")};',
     f'  --primary: {R("acao")};',f'  --primary-foreground: {R("sobre-acao")};',
     f'  --secondary: {R("realce")};',f'  --secondary-foreground: {R("sobre-realce")};',
     f'  --muted: {R("superficie-2")};',f'  --muted-foreground: {R("texto-2")};',
     f'  --accent: {R("realce")};',f'  --accent-foreground: {R("sobre-realce")};',
     f'  --destructive: {R("critico")};',f'  --border: {R("linha")};',f'  --input: {R("borda-controle")};',f'  --ring: {R("foco")};',
     '  --chart-1: var(--aj-dado-1);','  --chart-2: var(--aj-dado-2);','  --chart-3: var(--aj-dado-3);','  --chart-4: var(--aj-texto-3);','  --chart-5: var(--aj-linha);',
     f'  --sidebar: {R("superficie")};',f'  --sidebar-foreground: {R("texto-2")};',f'  --sidebar-primary: {R("acao")};',f'  --sidebar-primary-foreground: {R("sobre-acao")};',
     f'  --sidebar-accent: {R("realce")};',f'  --sidebar-accent-foreground: {R("sobre-realce")};',f'  --sidebar-border: {R("linha")};',f'  --sidebar-ring: {R("foco")};',
     f'  --success: {R("sucesso")};',f'  --warning: {R("atencao")};',f'  --info: {R("acao")};',
     f'  --status-neutral: {R("texto-2")};',f'  --status-info: {R("acao")};',f'  --status-attention: {R("atencao")};',f'  --status-critical: {R("critico")};']
p=['/* Ponte «SIGLA» → shadcn/ui (sistemas em Next + shadcn). Importe DEPOIS de aj-tokens.css e no lugar dos blocos :root/.dark atuais. */',
 '@import "./aj-tokens.css";','',':root {']+sh('claro')+['  --radius: 12px;','}','','.dark {']+sh('escuro')+['}','',
 '@theme inline {','  --font-sans: var(--aj-fonte-texto);','  --font-heading: var(--aj-fonte-titulo);',
 '  --color-success: var(--success);','  --color-warning: var(--warning);','  --color-info: var(--info);',
 '  --shadow-sm: var(--aj-sombra-1);','  --shadow-md: var(--aj-sombra-2);','  --shadow-lg: var(--aj-sombra-3);',
 '  --ease-out: var(--aj-curva-marca);','}']
grava(os.path.join(INTERFACE,'ponte-shadcn.css'),'\n'.join(p)+'\n')

# ---------- ponte NossoCRM (--color-* + primary-50..900 + nomes shadcn do button) ----------
def crm():
    R=lambda n:f'var(--aj-{n})'
    return [f'  --color-bg: {R("fundo")};',f'  --color-surface: {R("superficie")};',f'  --color-muted: {R("superficie-2")};',
     f'  --color-border: {R("borda-controle")};',f'  --color-border-subtle: {R("linha")};',
     f'  --color-text-primary: {R("texto")};',f'  --color-text-secondary: {R("texto-2")};',f'  --color-text-muted: {R("texto-3")};',f'  --color-text-subtle: {R("texto-3")};',
     f'  --color-success: {R("sucesso")};',f'  --color-success-hover: {R("sucesso")};',f'  --color-success-bg: {R("sucesso-fundo")};',f'  --color-success-text: {R("sucesso")};',
     f'  --color-warning: {R("atencao")};',f'  --color-warning-hover: {R("atencao")};',f'  --color-warning-bg: {R("atencao-fundo")};',f'  --color-warning-text: {R("atencao")};',
     f'  --color-error: {R("critico")};',f'  --color-error-hover: {R("critico")};',f'  --color-error-bg: {R("critico-fundo")};',f'  --color-error-text: {R("critico")};',
     f'  --color-info: {R("acao")};',f'  --color-info-hover: {R("acao-hover")};',f'  --color-info-bg: {R("realce")};',f'  --color-info-text: {R("sobre-realce")};',
     f'  --primary: {R("acao")};',f'  --primary-foreground: {R("sobre-acao")};',f'  --destructive: {R("critico")};',f'  --ring: {R("foco")};',
     f'  --background: {R("fundo")};',f'  --foreground: {R("texto")};',f'  --border: {R("linha")};',f'  --input: {R("borda-controle")};',
     f'  --secondary: {R("realce")};',f'  --secondary-foreground: {R("sobre-realce")};',f'  --muted: {R("superficie-2")};',f'  --muted-foreground: {R("texto-2")};',
     f'  --accent: {R("realce")};',f'  --accent-foreground: {R("sobre-realce")};']
p=['/* Ponte «SIGLA» → NossoCRM (Tailwind 4 com --color-*). Importe DEPOIS de aj-tokens.css; substitui o @theme de primary/dark e os blocos :root/.dark de --color-*. */',
 '@import "./aj-tokens.css";','','@theme {',"  --font-sans: «PILHA_TEXTO»;","  --font-display: «PILHA_TITULO»;"]
p+=[f'  --color-primary-{n.rsplit("-",1)[1]}: {h};' for n,h in ESCALA if not n.endswith('-950')]
E=lambda n: resolve({x[0]:x[2] for x in SEM}[n],'escuro')
p+=[f'  --color-dark-bg: {E("fundo")};',f'  --color-dark-card: {E("superficie")};',f'  --color-dark-border: {E("linha")};',f'  --color-dark-hover: {E("superficie-2")};','}','',':root {']+crm()+['}','','.dark {']+crm()+['}',
 '','/* O efeito de vidro (--glass-*) sai: a marca é plana. Mapeie para superfície chapada. */',':root, .dark {','  --glass-bg: var(--aj-superficie);','  --glass-border: var(--aj-linha);','  --glass-blur: 0px;','}']
grava(os.path.join(INTERFACE,'ponte-nossocrm.css'),'\n'.join(p)+'\n')
print('ok',len(toks))
