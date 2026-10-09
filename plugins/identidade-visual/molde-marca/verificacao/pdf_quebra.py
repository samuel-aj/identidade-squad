# Confere os PDFs do pdf_quebra.js: nenhuma página pode terminar num cabeçalho de seção (título ou resumo sem o
# conteúdo embaixo). Uso: python3 pdf_quebra.py <pasta>   (precisa de pymupdf: ferramentas/instalar.sh)
import fitz, glob, os, sys
ruins = []
for f in sorted(glob.glob(os.path.join(sys.argv[1], '*.pdf'))):
    d = fitz.open(f)
    for i, p in enumerate(d):
        bl = sorted(p.get_text('blocks'), key=lambda b: b[1])
        if i < d.page_count - 1 and bl and ('[Título da seção' in bl[-1][4] or '[Uma a três frases' in bl[-1][4]):
            ruins.append(f'{os.path.basename(f)} página {i + 1}')
print('\n'.join('CABEÇALHO SOZINHO NO PÉ: ' + r for r in ruins) or 'ok: nenhum cabeçalho sozinho no pé em nenhuma posição')
sys.exit(1 if ruins else 0)
