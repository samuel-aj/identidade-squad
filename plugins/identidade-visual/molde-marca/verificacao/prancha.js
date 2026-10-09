// Renderiza cada componente da skill (o código de referência de referencias/componentes/*.md) no computador e no
// celular, claro e escuro, e monta uma prancha por tema para a auditoria olhar. Uso: node prancha.js <pasta-da-skill> <saída>
// Todos em 1280 e em 390 px, inclusive as telas inteiras (Tela*): tela de sistema também tem de caber no celular sem rolagem lateral.
// Também na largura mínima da marca (marca.json "largura_minima", padrão 360 px: <Nome>-360-<tema>.png), e as Tela* em 1024
// e 800 px (<Nome>-1024-<tema>.png), onde o menu lateral e a barra do topo apertam o conteúdo. Uso: node prancha.js <skill> <saída> [--marca marca.json]
// Cada prévia abre de um arquivo com <base> na pasta da skill, para caminhos como assets/fotos/... funcionarem.
const F=process.env.FERRAMENTAS||require('path').join(require('os').homedir(),'.cache/design-squad-identidade');
const {chromium}=require(F+'/node_modules/playwright');const fs=require('fs'),path=require('path'),url=require('url');
const [sk,out]=process.argv.slice(2);fs.mkdirSync(out,{recursive:true});
const _im=process.argv.indexOf('--marca'),_mj=_im>0?process.argv[_im+1]:path.join(sk,'..','..','marca.json');
const MINIMA=(fs.existsSync(_mj)?JSON.parse(fs.readFileSync(_mj,'utf8')).largura_minima:0)||360;
const LARG=[[1280,'desk'],[390,'cel'],...(MINIMA<390?[[MINIMA,String(MINIMA)]]:[])],LARG_TELA=[[1024,'1024'],[800,'800']];
const css=fs.readdirSync(path.join(sk,'assets/css')).filter(f=>/-(tokens|componentes)\.css$/.test(f)).sort().reverse().map(f=>fs.readFileSync(path.join(sk,'assets/css',f),'utf8')).join('\n');
const dir=path.join(sk,'referencias/componentes');
const comps=fs.readdirSync(dir).filter(f=>f.endsWith('.md')&&f!=='INDICE.md').map(f=>[f.replace('.md',''),(fs.readFileSync(path.join(dir,f),'utf8').match(/```html\n([\s\S]*?)\n```/)||[])[1]]).filter(c=>c[1]);
const base=url.pathToFileURL(path.resolve(sk)+'/').href, pagina=path.resolve(out,'_pagina.html');
(async()=>{const b=await chromium.launch();const p=await b.newPage();const cel=[];
 for(const tema of ['claro','escuro']){
  for(const [nome,html] of comps){for(const [w,suf] of [...LARG,...(nome.startsWith('Tela')?LARG_TELA:[])]){
   await p.setViewportSize({width:w,height:800});
   fs.writeFileSync(pagina,`<!doctype html><html data-theme="${tema}"><head><meta charset="utf-8"><base href="${base}"><style>${css}body{margin:0;background:var(--${css.match(/--([a-z0-9]+)-fundo/)[1]}-fundo)}</style></head><body>${html}</body></html>`);
   await p.goto(url.pathToFileURL(pagina).href,{waitUntil:'load'});
   await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(150);
   const larg=await p.evaluate(()=>document.documentElement.scrollWidth);if(larg>w+1)cel.push(`${nome} (${suf}, ${tema}): rolagem lateral de ${larg-w}px`);
   await p.screenshot({path:`${out}/${nome}-${suf}-${tema}.png`,fullPage:true});}}}
 await b.close();fs.unlinkSync(pagina);
 fs.writeFileSync(`${out}/ROLAGEM.txt`,cel.join('\n')||'nenhum componente com rolagem lateral');
 console.log(comps.length,'componentes renderizados;',cel.length,'com rolagem lateral');})();
