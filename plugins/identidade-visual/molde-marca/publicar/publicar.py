# Publica a skill da marca em todos os destinos do marca.json (publicacao). Mostra o plano e só copia com --executar.
# O envio ao GitHub é um passo à parte (--github), porque publica fora da máquina: só com o "sim" do usuário.
# Sempre por branch e PR, com a skill e a pasta da marca; --ensaio monta tudo num clone temporário sem enviar.
# Uso: python3 publicar.py <projeto> [--executar] [--github [--ensaio]]
import json, os, shutil, subprocess, sys, tempfile, hashlib
proj = os.path.abspath(sys.argv[1]); M = json.load(open(os.path.join(proj, 'marca.json'))); PB = M['publicacao']
nome = PB['skill']; origem = os.path.join(proj, 'skill', nome)
if not os.path.isfile(os.path.join(origem, 'SKILL.md')): sys.exit(f'skill não gerada em {origem}: rode interface/fonte/gerar.py')
exe, gh = '--executar' in sys.argv, '--github' in sys.argv
destinos = [os.path.expanduser(d) for d in PB.get('destinos', [])]
guarda = os.path.expanduser(PB['guarda']) if PB.get('guarda') else None
print('Skill:', origem)
for d in destinos: print('  →', os.path.join(d, nome))
if guarda: print('  → cópia de guarda:', os.path.join(guarda, '09-skill'))
if PB.get('github'): print('  → GitHub:', PB['github']['repo'], '/', PB['github'].get('pasta', 'skills'), '(só com --github)')
if not exe: print('\n(plano apenas: rode com --executar para copiar)'); sys.exit(0)
def copia(dst):
    if os.path.isdir(dst): shutil.rmtree(dst)
    shutil.copytree(origem, dst, ignore=shutil.ignore_patterns('.DS_Store')); print('copiado:', dst)
for d in destinos: os.makedirs(d, exist_ok=True); copia(os.path.join(d, nome))
if guarda: copia(os.path.join(guarda, '09-skill'))
if gh and PB.get('github'):
    # GitHub sempre por branch e PR (main intacta): lição da Kleiciane e da Almeida Nascimento. Leva a skill e, se houver
    # pasta de guarda, a pasta da marca (sem a skill duplicada) em <pasta_arquivos>/<slug>-identidade. --ensaio faz tudo
    # no clone temporário e para antes do push.
    g = PB['github']; tmp = tempfile.mkdtemp(); ensaio = '--ensaio' in sys.argv
    subprocess.run(['gh', 'repo', 'clone', g['repo'], tmp, '--', '--depth', '20', '-q'], check=True)
    ramo = g.get('ramo', f'feat/{nome}'); subprocess.run(['git', '-C', tmp, 'checkout', '-q', '-b', ramo], check=True)
    alvo = os.path.join(tmp, g.get('pasta', 'skills'), nome); copia(alvo)
    if guarda and os.path.isdir(guarda) and g.get('pasta_arquivos', 'output'):
        slug = os.path.basename(proj.rstrip('/')); arq = os.path.join(tmp, g.get('pasta_arquivos', 'output'), f'{slug}-identidade')
        if os.path.isdir(arq): shutil.rmtree(arq)
        shutil.copytree(guarda, arq, ignore=shutil.ignore_patterns('.DS_Store', 'skill', '09-skill')); print('copiado:', arq)
    # Repositório com manifesto de skills (samuel-aj/aj-workspace): versão e hash no formato do instalador, na ordem alfabética.
    man = os.path.join(tmp, 'config', 'managed-skills.json'); novo_nome = False
    if os.path.exists(man):
        ents = []
        for r, _, fs in os.walk(alvo):
            for f in fs:
                p = os.path.join(r, f); ents.append((os.path.relpath(p, alvo).replace(os.sep, '/'), hashlib.sha256(open(p, 'rb').read()).hexdigest()))
        ents.sort(key=lambda e: e[0].encode('utf-16-be'))
        h = hashlib.sha256(''.join(f'{a}:{b}\n' for a, b in ents).encode()).hexdigest()
        J = json.load(open(man)); versao = M.get('versao', '1.0') + '.0' if M.get('versao', '1.0').count('.') == 1 else M.get('versao', '1.0.0')
        for s in J['skills']:
            if s['name'] == nome: s.update(version=versao, sha256=h); break
        else:
            novo_nome = True; ent = {'name': nome, 'version': versao, 'destinations': ['agents', 'claude'], 'sha256': h}
            pos = next((i for i, s in enumerate(J['skills']) if s['name'] > nome), len(J['skills'])); J['skills'].insert(pos, ent)
        txt = '{\n  "schemaVersion": 1,\n  "skills": [\n' + ',\n'.join('    ' + json.dumps(s, ensure_ascii=False, separators=(',', ':')) for s in J['skills']) + '\n  ]\n}\n'
        open(man, 'w').write(txt)
        print(f'manifesto: {nome} {versao} {h[:12]}…')
    # Teste que fixa a lista de skills (tests/Core.Tests.ps1): acrescenta o nome na ordem e acerta o número do título.
    tst = os.path.join(tmp, 'tests', 'Core.Tests.ps1')
    if novo_nome and os.path.exists(tst):
        import re
        t = open(tst, encoding='utf-8').read(); m = re.search(r"It 'contains exactly the (\d+) managed skills without duplicates' \{\s*\$expectedNames = @\((.*?)\)", t, re.S)
        if m:
            nomes = re.findall(r"'([^']+)'", m.group(2)); nomes.append(nome); nomes.sort()
            ind = re.search(r"\n(\s*)'", m.group(2)).group(1)
            bloco = '\n' + '\n'.join(f"{ind}'{n}'" for n in nomes) + '\n' + ind[:-4]
            t = t[:m.start(2)] + bloco + t[m.end(2):]
            t = t.replace(f"It 'contains exactly the {m.group(1)} managed skills", f"It 'contains exactly the {len(nomes)} managed skills", 1)
            open(tst, 'w', encoding='utf-8').write(t); print(f'teste: lista com {len(nomes)} skills')
    subprocess.run(['git', '-C', tmp, 'add', '-A'], check=True)
    subprocess.run(['git', '-C', tmp, 'commit', '-q', '-m', f'feat: {nome} {M.get("versao", "1.0")}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>'], check=True)
    if ensaio:
        print(subprocess.run(['git', '-C', tmp, 'show', '--stat', '--oneline', 'HEAD'], capture_output=True, text=True).stdout[-1500:]); print('ensaio: nada enviado. Clone em', tmp)
    else:
        subprocess.run(['git', '-C', tmp, 'push', '-q', '-u', 'origin', ramo], check=True)
        corpo = f'Skill `{nome}` e a pasta da marca, gerados pelo design-squad (fluxo identidade).\n\nRodar os testes do repositório antes de mesclar.\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)'
        r = subprocess.run(['gh', 'pr', 'create', '-R', g['repo'], '--base', g.get('base', 'main'), '--head', ramo, '--title', f'feat: {nome} {M.get("versao", "1.0")}', '--body', corpo], capture_output=True, text=True)
        print('PR:', r.stdout.strip() or r.stderr.strip())
