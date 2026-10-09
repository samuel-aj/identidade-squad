// Piso de leitura e de toque: renderiza cada componente da skill (o código de referência de referencias/componentes/*.md)
// em 1280 e em 390 px, claro e escuro, e acusa:
//   - texto abaixo de 14 px (o corpo renderizado: no SVG, a letra vezes a escala do desenho; um eixo de 14 num gráfico
//     encolhido para caber no celular sai com 8 px e conta como falha);
//   - alvo de toque abaixo de 44 × 44 px (botão, link de ação solto, campo, item de menu, aba, filtro, página, opção;
//     a caixa de marcar e a opção única contam pelo rótulo inteiro; link dentro de uma frase fica fora da conta);
//   - pílula (canto ≥ metade do lado menor num elemento comprido), só quando o marca.json diz "pilula": false;
//   - palavra sozinha na última linha de título, pergunta, linha de contexto ou botão (ex.: "Bom dia, / Marina");
//   - item sozinho na última linha de uma grade (atalhos, grades de cartões, indicadores, sumário, frentes): 4 + 1, nunca;
//   - e, como aviso (não reprova), corpos de texto menores que o `corpo` e fora da escala do `tipo` (ex.: 15 px).
// Larguras: todo componente em 1280, 390 e na largura mínima da marca (marca.json "largura_minima", padrão 360 px);
// as telas inteiras (Tela*) também em 1024 e 800, onde o menu lateral e a barra do topo apertam o conteúdo.
// Uso: node piso.js <pasta-da-skill> [<saída>] [--marca <marca.json>] [--modelos <arquivo.html> ...]
//   --modelos: páginas inteiras (login, formulário) abertas pelo endereço, em 1440, 1024, 390 e na largura mínima; as que têm
//   data-theme="aparelho" também com o aparelho no modo escuro.
// Sai com erro se houver falha. Grava <saída>/PISO.txt com a lista (padrão: a pasta atual).
const F = process.env.FERRAMENTAS || require('path').join(require('os').homedir(), '.cache/design-squad-identidade');
const { chromium } = require(F + '/node_modules/playwright');
const fs = require('fs'), path = require('path'), url = require('url');
const args = process.argv.slice(2);
const sk = args[0];
const iMarca = args.indexOf('--marca'), iMod = args.indexOf('--modelos');
const out = (args[1] && !args[1].startsWith('--')) ? args[1] : '.';
const marcaJson = iMarca > 0 ? args[iMarca + 1] : path.join(sk, '..', '..', 'marca.json');
const modelos = iMod > 0 ? args.slice(iMod + 1).filter(a => !a.startsWith('--')) : [];
const M = fs.existsSync(marcaJson) ? JSON.parse(fs.readFileSync(marcaJson, 'utf8')) : {};
const P = M.prefixo || (fs.readdirSync(path.join(sk, 'assets/css')).find(f => f.endsWith('-tokens.css')) || 'aj-').split('-')[0];
const SEM_PILULA = M.pilula === false;
const estilos = (M.tipo && M.tipo.groups || []).flatMap(g => g.styles);
const corpo = parseFloat((estilos.find(s => s.name === 'corpo') || {}).fontSize || '16');
const ESCALA = [...new Set(estilos.map(s => parseFloat(s.fontSize)))];
const TEXTO_MIN = 14, ALVO_MIN = 44;
const MINIMA = M.largura_minima || 360;
const LARG = [[1280, 'desk'], [390, 'cel'], ...(MINIMA < 390 ? [[MINIMA, String(MINIMA)]] : [])];
const LARG_TELA = [[1024, '1024'], [800, '800']];
fs.mkdirSync(out, { recursive: true });
const css = fs.readdirSync(path.join(sk, 'assets/css')).filter(f => /-(tokens|componentes)\.css$/.test(f)).sort().reverse()
  .map(f => fs.readFileSync(path.join(sk, 'assets/css', f), 'utf8')).join('\n');
const dir = path.join(sk, 'referencias/componentes');
const comps = fs.readdirSync(dir).filter(f => f.endsWith('.md') && f !== 'INDICE.md')
  .map(f => [f.replace('.md', ''), (fs.readFileSync(path.join(dir, f), 'utf8').match(/```html\n([\s\S]*?)\n```/) || [])[1]]).filter(c => c[1]);
const base = url.pathToFileURL(path.resolve(sk) + '/').href, pagina = path.resolve(out, '_piso.html');

// roda dentro da página: devolve {texto: [...], alvo: [...], pilula: [...], escala: [...]}
function medir(o) {
  const { TEXTO_MIN, ALVO_MIN, SEM_PILULA, P, corpo, ESCALA } = o;
  const vis = e => { const s = getComputedStyle(e); if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0) return false;
    const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const nome = e => e.tagName.toLowerCase() + ([...e.classList].slice(0, 2).map(c => '.' + c).join(''));
  const curto = t => t.replace(/\s+/g, ' ').trim().slice(0, 40);
  const r = { texto: [], alvo: [], pilula: [], escala: [], sozinha: [], orfao: [] };
  // texto
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
  const vistos = new Set();
  while ((n = w.nextNode())) {
    if (!n.textContent.trim()) continue;
    const el = n.parentElement;
    if (!el || el.closest('style,script,title,desc,option,noscript') || !vis(el)) continue;
    let fs = parseFloat(getComputedStyle(el).fontSize);
    if (el instanceof SVGElement) { const m = (el.closest('text') || el).getScreenCTM(); if (m) fs *= Math.hypot(m.a, m.b); }
    fs = Math.round(fs * 10) / 10;
    const chave = nome(el) + fs;
    if (fs < TEXTO_MIN - 0.05) { if (!vistos.has(chave)) r.texto.push(`${nome(el)} "${curto(n.textContent)}" ${fs}px`); vistos.add(chave); }
    else if (!(el instanceof SVGElement) && fs < corpo && !ESCALA.includes(fs) && !vistos.has('e' + chave)) { r.escala.push(`${nome(el)} "${curto(n.textContent)}" ${fs}px`); vistos.add('e' + chave); }
  }
  // alvos
  const SEL = 'a[href],button,input:not([type=hidden]),select,textarea,summary,[role=button],[role=tab],[role=menuitem],[role=menuitemradio],[role=menuitemcheckbox],[role=option],[role=switch],[tabindex]:not([tabindex="-1"])';
  const emFrase = a => { const p = a.parentElement; if (!p) return false;
    return [...p.childNodes].some(c => c !== a && ((c.nodeType === 3 && c.textContent.trim()) ||
      (c.nodeType === 1 && getComputedStyle(c).display === 'inline' && !c.matches('a,button') && c.textContent.trim()))); };
  const feitos = new Set();
  for (const e of document.querySelectorAll(SEL)) {
    if (!vis(e) && !e.matches('input[type=checkbox],input[type=radio]')) continue;
    let alvo = e;
    if (e.matches('input[type=checkbox],input[type=radio]')) { const l = e.closest('label'); if (l) alvo = l; else if (!vis(e)) continue; }
    if (e.tagName === 'A' && emFrase(e)) continue;
    if (feitos.has(alvo) || !vis(alvo)) continue; feitos.add(alvo);
    const q = alvo.getBoundingClientRect();
    if (q.width < ALVO_MIN - 0.5 || q.height < ALVO_MIN - 0.5)
      r.alvo.push(`${nome(alvo)} "${curto(alvo.getAttribute('aria-label') || alvo.textContent || '')}" ${Math.round(q.width)}×${Math.round(q.height)}`);
  }
  // palavra sozinha na última linha: título, pergunta, linha de contexto e botão (o rótulo do botão quebra no celular)
  const SOZ = `h1,h2,h3,h4,.${P}-titulo,.${P}-subtitulo,.${P}-etapas__pergunta,.${P}-vazio__titulo,.${P}-cartao__titulo,.${P}-modal__titulo,.${P}-botao`;
  for (const e of document.querySelectorAll(SOZ)) {
    if (!vis(e) || e.closest('svg')) continue;
    const pal = []; const tw = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let t;
    while ((t = tw.nextNode())) {
      const re = /[^ \t\n\r]+/g; let m;  // espaço sem quebra (&nbsp;) não separa palavras: "2&nbsp;pendências" é uma só
      while ((m = re.exec(t.textContent))) {
        const g = document.createRange(); g.setStart(t, m.index); g.setEnd(t, m.index + m[0].length);
        const q = [...g.getClientRects()].filter(x => x.width > 0); if (q.length) pal.push({ topo: q[q.length - 1].top, alt: q[q.length - 1].height });
      }
    }
    if (pal.length < 2) continue;
    const linhas = [];
    for (const x of pal) { const l = linhas.find(l => Math.abs(l.topo - x.topo) < x.alt * 0.5); if (l) l.n++; else linhas.push({ topo: x.topo, n: 1 }); }
    linhas.sort((a, b) => a.topo - b.topo);
    if (linhas.length >= 2 && linhas[linhas.length - 1].n === 1) r.sozinha.push(`${nome(e)} "${curto(e.textContent)}" (${linhas.length} linhas)`);
  }
  // item sozinho na última linha de uma grade (o 5º atalho caindo para a segunda linha, um cartão órfão)
  const GRADES = `.${P}-atalhos,.${P}-grade,[class*="${P}-grade--"],[class*="${P}-doc__grade"],.${P}-indicadores,.${P}-sumario,.${P}-frentes`;
  for (const g of document.querySelectorAll(GRADES)) {
    if (!vis(g)) continue;
    const filhos = [...g.children].filter(vis); if (filhos.length < 3) continue;
    const linhas = [];
    for (const f of filhos) { const q = f.getBoundingClientRect(); const l = linhas.find(l => Math.abs(l.topo - q.top) < 4); if (l) l.n++; else linhas.push({ topo: q.top, n: 1, larg: q.width }); }
    linhas.sort((a, b) => a.topo - b.topo);
    const ult = linhas[linhas.length - 1];  // o item que ocupa a linha inteira de propósito (grid-column: 1 / -1) não é órfão
    if (linhas.length >= 2 && linhas[0].n >= 2 && ult.n === 1 && ult.larg < g.getBoundingClientRect().width * 0.9)
      r.orfao.push(`${nome(g)} ${linhas.map(l => l.n).join(' + ')} (${filhos.length} itens)`);
  }
  // pílula
  if (SEM_PILULA) for (const e of document.body.querySelectorAll('*')) {
    if (e instanceof SVGElement || e.closest(`.${P}-avatar`) || !vis(e)) continue;
    const s = getComputedStyle(e), q = e.getBoundingClientRect(), menor = Math.min(q.width, q.height);
    if (menor < 6 || Math.abs(q.width - q.height) <= 2) continue;
    const v = s.borderTopLeftRadius; const raio = v.endsWith("%") ? parseFloat(v) / 100 * menor : parseFloat(v);
    if (raio >= menor / 2 - 0.5 && (s.backgroundColor !== 'rgba(0, 0, 0, 0)' || parseFloat(s.borderTopWidth) > 0 || e.matches('input')))
      r.pilula.push(`${nome(e)} ${Math.round(q.width)}×${Math.round(q.height)}, canto ${v}`);
  }
  return r;
}

(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  const falhas = [], avisos = [];
  const anota = (onde, r) => {
    r.texto.forEach(x => falhas.push(`TEXTO   ${onde}: ${x}`));
    r.alvo.forEach(x => falhas.push(`ALVO    ${onde}: ${x}`));
    r.pilula.forEach(x => falhas.push(`PILULA  ${onde}: ${x}`));
    r.sozinha.forEach(x => falhas.push(`SOZINHA ${onde}: ${x}`));
    r.orfao.forEach(x => falhas.push(`ORFAO   ${onde}: ${x}`));
    r.escala.forEach(x => avisos.push(`ESCALA  ${onde}: ${x}`));
  };
  const o = { TEXTO_MIN, ALVO_MIN, SEM_PILULA, P, corpo, ESCALA };
  for (const tema of ['claro', 'escuro']) for (const [nome, html] of comps) for (const [w, suf] of [...LARG, ...(nome.startsWith('Tela') ? LARG_TELA : [])]) {
    await p.setViewportSize({ width: w, height: 800 });
    fs.writeFileSync(pagina, `<!doctype html><html data-theme="${tema}"><head><meta charset="utf-8"><base href="${base}"><style>${css}body{margin:0;background:var(--${P}-fundo)}</style></head><body>${html}</body></html>`);
    await p.goto(url.pathToFileURL(pagina).href, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(100);
    anota(`${nome} (${suf}, ${tema})`, await p.evaluate(medir, o));
  }
  for (const m of modelos) {
    const h = fs.readFileSync(m, 'utf8'), aparelho = /data-theme="aparelho"/.test(h);
    for (const esquema of aparelho ? ['light', 'dark'] : ['light']) for (const [w, suf] of [[1440, 'desk'], [1024, '1024'], ...LARG.slice(1)]) {
      await p.emulateMedia({ colorScheme: esquema });
      await p.setViewportSize({ width: w, height: 900 });
      await p.goto(url.pathToFileURL(path.resolve(m)).href, { waitUntil: 'load' });
      await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(100);
      anota(`${path.basename(m)} (${suf}${aparelho ? ', aparelho ' + (esquema === 'dark' ? 'escuro' : 'claro') : ''})`, await p.evaluate(medir, o));
    }
  }
  await b.close(); fs.unlinkSync(pagina);
  const txt = [`piso: texto ≥ ${TEXTO_MIN} px, alvo ≥ ${ALVO_MIN} × ${ALVO_MIN} px${SEM_PILULA ? ', sem pílula' : ''}, nenhuma palavra sozinha na última linha de título ou botão, nenhum item sozinho na última linha de grade; larguras ${LARG.map(l => l[0]).join(', ')} (Tela* também ${LARG_TELA.map(l => l[0]).join(' e ')}; modelos em 1440, 1024, ${LARG.slice(1).map(l => l[0]).join(' e ')})`, '',
    ...(falhas.length ? falhas : ['nenhuma falha']), '', `avisos (corpo menor que o corpo de ${corpo} px e fora da escala do tipo: ${ESCALA.sort((a, b) => a - b).join(', ')} px)`,
    ...(avisos.length ? avisos : ['nenhum'])].join('\n');
  fs.writeFileSync(path.join(out, 'PISO.txt'), txt + '\n');
  console.log(falhas.join('\n'));
  console.log(`\n${comps.length} componentes${modelos.length ? ` e ${modelos.length} modelo(s)` : ''}: ${falhas.length} falha(s) de piso; ${avisos.length} aviso(s) de escala (lista em ${path.join(out, 'PISO.txt')}).`);
  process.exit(falhas.length ? 1 : 0);
})();
