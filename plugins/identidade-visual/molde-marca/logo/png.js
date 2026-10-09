// PNG transparentes de todos os SVG do logo + avatares de redes. Rode de dentro de <projeto>/identidade/logo.
// Avatar: com logo.avatar {"caixa": 0.5, "pequeno": true, "cenas": {nome: {"fundo": cor, "cor": cor}}} sai chapado, sem
// halo nem brilho (marca sem luz): o símbolo centrado, com a caixa dele = caixa x lado. Sem o campo: o da AJ (halo e brilho).
// Marca só tipográfica (simbolo null): converte só as pastas que existirem e não gera avatar (o avatar dela é outra
// peça, em geral a foto; não existe símbolo para pôr no centro).
const F=process.env.FERRAMENTAS||require('path').join(require('os').homedir(),'.cache/design-squad-identidade');
const {chromium}=require(F+'/node_modules/playwright');const fs=require('fs'),path=require('path');
const M=JSON.parse(fs.readFileSync(process.env.MARCA_JSON||path.resolve('../../marca.json'),'utf8'));
const cor=Object.fromEntries(M.cores.map(c=>[c.nome,c.hex]));
const P=Object.fromEntries(Object.entries(M.papeis||{}).map(([k,v])=>[k,v.startsWith('#')?v:cor[v]]));
(async()=>{const b=await chromium.launch();const p=await b.newPage();
 for(const dir of ['simbolo','assinatura','app','favicon'].filter(d=>fs.existsSync('./'+d))) for(const f of fs.readdirSync('./'+dir).filter(x=>x.endsWith('.svg'))){
   const svg=fs.readFileSync(`./${dir}/${f}`,'utf8');const vb=svg.match(/viewBox="([^"]+)"/)[1].split(' ').map(Number);
   const sizes=dir==='app'?[1024,512,180]:dir==='favicon'?[512,192,48,32,16]:[2048];
   for(const W of sizes){const H=Math.round(W*vb[3]/vb[2]);await p.setViewportSize({width:W,height:H});
     await p.setContent(`<html><body style="margin:0;background:transparent">${svg.replace('<svg ',`<svg width="${W}" height="${H}" `)}</body></html>`);
     const suf=sizes.length>1?`-${W}`:'';await p.screenshot({path:`./${dir}/${f.replace('.svg','')}${suf}.png`,omitBackground:true});}
 }
 const C=v=>v.startsWith('#')?v:cor[v];
 if(M.simbolo&&M.logo.avatar){
 const S=M.simbolo,av=M.logo.avatar,ps=av.pequeno?(S.pequeno||S.pecas):S.pecas,lado=Math.round(1080*(av.caixa||.41));
 fs.mkdirSync('./avatar',{recursive:true});await p.setViewportSize({width:1080,height:1080});
 for(const [n,c] of Object.entries(av.cenas)){
   await p.setContent(`<body style="margin:0;width:1080px;height:1080px;background:${C(c.fundo)};display:grid;place-items:center"><svg viewBox="${S.viewBox||'0 0 100 100'}" width="${lado}" height="${lado}" fill="${C(c.cor)}">${ps.map(d=>`<path d="${d}"/>`).join('')}</svg></body>`);
   await p.screenshot({path:`./avatar/avatar-${n}-1080.png`});}
 }else if(M.simbolo){
 const sem=Object.fromEntries(M.semanticos.map(s=>[s.nome,s]));
 const R=(v,t)=>{while(v.startsWith('{')){const n=v.slice(1,-1);v=cor[n]||sem[n][t];}return v;};
 const halo=`radial-gradient(38% 42% at 72% 32%,${R(sem['halo-1'].claro,'claro')},transparent 70%),radial-gradient(34% 38% at 26% 84%,${R(sem['halo-2'].claro,'claro')},transparent 70%)`;
 const brilho=R(sem['brilho'].escuro,'escuro');
 fs.mkdirSync('./avatar',{recursive:true});
 const s=n=>fs.readFileSync(`./simbolo/simbolo-${n}.svg`,'utf8').replace('<svg ','<svg width="440" height="440" ');
 const cs=M.logo.cores_simbolo;const claro=Object.keys(cs).find(k=>k==='primaria')||Object.keys(cs)[0];const noEscuro=Object.keys(cs).find(k=>k==='claro')||'branco';
 await p.setViewportSize({width:1080,height:1080});
 await p.setContent(`<body style="margin:0;width:1080px;height:1080px;background:${P.fundo_claro||'#FFFFFF'};position:relative;overflow:hidden;display:grid;place-items:center"><div style="position:absolute;inset:-25%;background:${halo};filter:blur(30px)"></div><div style="position:relative">${s(claro)}</div></body>`);
 await p.screenshot({path:'./avatar/avatar-claro-1080.png'});
 await p.setContent(`<body style="margin:0;width:1080px;height:1080px;background:radial-gradient(90% 80% at 30% 0%,${P.escuro_claro||P.escuro},${P.escuro} 62%);display:grid;place-items:center"><div style="filter:drop-shadow(0 0 1px rgba(255,255,255,.25)) drop-shadow(0 0 50px ${brilho})">${s(noEscuro)}</div></body>`);
 await p.screenshot({path:'./avatar/avatar-escuro-1080.png'});
 }
 await b.close();console.log('png ok');})();
