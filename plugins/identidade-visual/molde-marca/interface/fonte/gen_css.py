# Gera design-system/project/components/bundle.css (nomes do Design System) e interface/<prefixo>-componentes.css
# (variáveis --<prefixo>-*) a partir de bundle.tpl.css, mais a camada própria da marca (marca.css), se existir.
# bundle.tpl.css tem blocos condicionais (/* @se simbolo */, /* @se tipografica */, /* @se luz */ ... /* @fim */):
# ficam só os que valem para a marca (fonte.condicional). marca.css vem por último e sobrescreve o sistema onde a
# marca pede; é escrita como o bundle (classes aj-*, tokens sem prefixo) e passa pelas mesmas trocas.
import re,os,sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from fonte import *
t=condicional(open(os.path.join(AQUI,'bundle.tpl.css')).read())
if os.path.exists(os.path.join(AQUI,'marca.css')): t+='\n'+open(os.path.join(AQUI,'marca.css')).read()
# Tema do aparelho: toda regra de uma linha que começa em [data-theme="escuro"] ganha a gêmea [data-theme="aparelho"] dentro de
# @media (prefers-color-scheme: dark), para a tela que segue o aparelho (login, área do cliente) ter os mesmos ajustes do escuro.
_gemeas=[]
for _l in t.split('\n'):
    _m=re.match(r'^(\[data-theme="escuro"\][^{]*)\{(.*)\}\s*$',_l)
    if not _m: continue
    _sel=[s.strip() for s in _m.group(1).split(',') if 'data-theme="escuro"' in s]
    _gemeas.append('  '+', '.join(s.replace('data-theme="escuro"','data-theme="aparelho"') for s in _sel)+' {'+_m.group(2)+'}')
if _gemeas: t+='\n\n/* Tela que segue o tema do aparelho (data-theme="aparelho"): os mesmos ajustes do tema escuro, quando o aparelho está no escuro */\n@media (prefers-color-scheme: dark) {\n'+'\n'.join(_gemeas)+'\n}\n'
grava(os.path.join(DS,'components','bundle.css'),t)
# --dx/--dy (deslocamento) e --fv/--dfv (eixos da fonte) são variáveis locais do Carregando, não tokens: ficam sem prefixo.
t2=re.sub(r'var\(--(?!aj-|dx\)|dy\)|fv\)|dfv\))',r'var(--aj-',t)
# Todo seletor que começa em [data-theme="escuro"] ganha o gêmeo .dark (sistemas com shadcn usam a classe .dark).
t2=re.sub(r'(?m)^\[data-theme="escuro"\] ([^,{]+?)(\s*[,{])',lambda m:f'[data-theme="escuro"] {m.group(1)}, .dark {m.group(1)}{m.group(2)}',t2)
grava(os.path.join(INTERFACE,f'{P}-componentes.css'),'/* «SIGLA» — componentes (CSS puro, qualquer framework). Requer aj-tokens.css. Gerado por fonte/gen_css.py. */\n'+t2.split('\n',1)[1])
print('css ok')
