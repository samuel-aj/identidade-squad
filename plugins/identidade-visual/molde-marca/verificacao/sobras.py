# Procura o que não pode sobrar na entrega de uma marca: marcadores do molde ([[ESCREVA, «...», comentário MOLDE)
# e restos da marca AJ (de onde o molde veio). Uso: python3 sobras.py <projeto> [pastas...]
# Sai com erro se achar algo. Palavras que a própria marca usa (nome, fontes, cores do marca.json) são ignoradas.
import json, os, re, sys
proj = sys.argv[1]; M = json.load(open(os.path.join(proj, 'marca.json')))
# Também a cópia do que foi publicado (interface/design-system/publicado/), quando existe: o publicado defasado é sobra também.
pastas = sys.argv[2:] or [os.path.join(proj, d) for d in ('skill', 'interface/design-system/project', 'interface/design-system/publicado', 'identidade/logo', 'aplicacoes')
                          if os.path.isdir(os.path.join(proj, d))]
MARCADORES = [r'\[\[ESCREVA', r'«[A-Z_]+»', r'MOLDE \(pt-BR\)', r'MOLDE:']
AJ = ['Anúncio Jurídico', 'Anuncio Juridico', 'jurídic', 'advog', 'escritório', 'AJ OPS', 'Nosso CRM', 'EDL', 'violeta', 'lavanda',
      'noite', 'névoa', 'dobra', 'Dobra', 'Sora', 'Manrope', 'Previdenci', 'Trabalhista', 'tráfego pago', 'Contas de anúncio', 'custo por lead', '#5B2BE0', '#0B0620', '#D9CCFF', '#B9A4FF', '#4A1FC4', '#221850', '#ECE6FF', '#3A1C9E', '#130D2A', '#FCFBFF', '#F4F2FB', '91,43,224', '185,164,255', 'Samuel', 'Ji-Paraná', 'Almeida',
      'palavra em peso', 'luzes']  # ideias da voz e da luz da AJ ("UMA palavra em peso", "as duas luzes"); outra marca libera em vocabulario_proprio
# Só a identidade da própria marca libera uma palavra (não os textos de uso, que podem ter vindo do exemplo AJ).
# `vocabulario_proprio` (marca.json): palavras do setor da própria marca que a lista da AJ acusaria (um escritório de
# advocacia diz "advogado", "escritório", "jurídico"). Cada uma precisa de motivo; o resto da lista continua valendo.
proprio = ' '.join([M['nome'], M['sigla'], *M.get('produtos', {}).values(), M['fontes']['titulo']['familia'], M['fontes']['texto']['familia'],
                    M['escala']['nome'], *[c['nome'] + ' ' + c['hex'] for c in M['cores']],
                    *[v if isinstance(v, str) else v[0] for v in M.get('vocabulario_proprio', [])]]).lower()
AJ = [p for p in AJ if p.lower() not in proprio] if M.get('slug') != 'anuncio-juridico' else []
# Nomes que são palavra inteira (a fonte Sora, a cor noite) só contam como palavra: "impressora" não é a Sora, "pernoite" não é
# a noite. Os outros itens da lista são raízes ("jurídic", "advog", "Previdenci") e contam em qualquer lugar da palavra.
INTEIRAS = {'Sora', 'Manrope', 'EDL', 'Samuel', 'noite', 'névoa', 'dobra', 'Dobra', 'violeta', 'lavanda', 'Almeida'}
# A sigla sozinha ("AJ —" num comentário, "a AJ") só aparece com caixa alta e palavra inteira: busca à parte, sensível à caixa.
# o prefixo de classe do molde (aj-botao, --aj-fundo) esquecido num texto da marca: a peça não acha o CSS
PREFIXO_AJ = re.compile(r'(?<![A-Za-z0-9_])-{0,2}aj-[a-z]') if M.get('prefixo', 'aj') != 'aj' else None
AJ_SIGLA = re.compile(r'(?<![A-Za-z0-9_-])AJ(?![A-Za-z0-9_-])') if M.get('slug') != 'anuncio-juridico' else None
# Cores da AJ escritas em rgb()/rgba() (ex.: rgba(252,251,255,.92), o Branco quente): o mesmo hex da lista, em números.
def _rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
_proprias = {_rgb(c['hex']) for c in M['cores']} | {_rgb(s[k]) for s in M['semanticos'] for k in ('claro', 'escuro') if str(s.get(k, '')).startswith('#') and len(s[k]) == 7}
AJ_RGB = {_rgb(h): h for h in AJ if re.fullmatch(r'#[0-9A-Fa-f]{6}', h)} if M.get('slug') != 'anuncio-juridico' else {}
AJ_RGB.update({tuple(map(int, p.split(','))): p for p in AJ if re.fullmatch(r'\d+,\d+,\d+', p)})
AJ_RGB = {k: v for k, v in AJ_RGB.items() if k not in _proprias}
RGB = re.compile(r'rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})')
achados = 0
for pasta in pastas:
    for raiz, _, arqs in os.walk(pasta):
        if 'movimento' in raiz: continue
        for a in arqs:
            if not a.endswith(('.md', '.html', '.css', '.json', '.svg')): continue
            c = os.path.join(raiz, a)
            for n, linha in enumerate(open(c, encoding='utf-8', errors='ignore'), 1):
                if 'credito-agencia' in linha: continue  # crédito da agência em documento de entrega (marcado de propósito)
                if a == 'design-system.json' and re.match(r'\s*"(by|at|createdBy|updatedBy)"\s*:', linha): continue  # registro de publicação (quem e quando)
                for p in MARCADORES:
                    if re.search(p, linha): achados += 1; print(f'MARCADOR  {c}:{n}  {linha.strip()[:110]}')
                for p in AJ:
                    if (re.search(rf'(?<!\w){re.escape(p)}(?!\w)', linha, re.I) if p in INTEIRAS else p.lower() in linha.lower()):
                        achados += 1; print(f'RESTO-AJ  {c}:{n}  "{p}"  {linha.strip()[:90]}')
                if PREFIXO_AJ and PREFIXO_AJ.search(linha): achados += 1; print(f'PREFIXO-AJ  {c}:{n}  {linha.strip()[:90]}')
                if AJ_SIGLA and AJ_SIGLA.search(linha): achados += 1; print(f'RESTO-AJ  {c}:{n}  "AJ"  {linha.strip()[:90]}')
                for m in RGB.finditer(linha):
                    k = tuple(int(x) for x in m.groups())
                    if k in AJ_RGB and AJ_RGB[k].replace(' ', '') not in linha.replace(' ', ''):  # o "91,43,224" literal já foi contado acima
                        achados += 1; print(f'RESTO-AJ  {c}:{n}  "{m.group(0)}…" = {AJ_RGB[k]}  {linha.strip()[:90]}')
print(f'\n{achados} sobra(s).' if achados else 'Nenhuma sobra.')
sys.exit(1 if achados else 0)
