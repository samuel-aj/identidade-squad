# Regenera todo o sistema da marca, na ordem certa: tokens → CSS → componentes → README do Design System → skill.
# Uso: python3 interface/fonte/gerar.py   (de qualquer pasta)
import os, subprocess, sys, shutil
AQUI = os.path.dirname(os.path.abspath(__file__)); INTERFACE = os.path.dirname(AQUI)
DS = os.path.join(INTERFACE, 'design-system', 'project')
for s in ('gen_tokens.py', 'gen_css.py', 'gen_comp.py'):
    subprocess.run([sys.executable, os.path.join(AQUI, s)], check=True)
for origem, destino in (('regras.md', 'README.md'), ('plataformas.md', 'plataformas.md')):
    o = os.path.join(INTERFACE, origem)
    if os.path.exists(o):
        # o texto das regras usa as classes do molde (aj-*); o README publicado precisa do prefixo da marca, como a skill
        sys.path.insert(0, AQUI); from fonte import troca
        open(os.path.join(DS, destino), 'w', encoding='utf-8').write(troca(open(o, encoding='utf-8').read()))
    elif origem == 'regras.md': sys.exit('falta interface/regras.md (copie de molde-marca/interface/regras.tpl.md e preencha)')
# Modelos de peça gerados por script (aplicacoes/gera_modelos.py, opcional): rodam antes da skill, que os copia.
_gm = os.path.join(os.path.dirname(INTERFACE), 'aplicacoes', 'gera_modelos.py')
if os.path.exists(_gm): subprocess.run([sys.executable, _gm], check=True)
subprocess.run([sys.executable, os.path.join(AQUI, 'gen_skill.py')] + sys.argv[1:], check=True)
