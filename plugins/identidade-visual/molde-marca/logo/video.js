// Abertura em vídeo (MP4 1920×1080, 4 s). Rode de dentro de <projeto>/identidade/logo, depois de gera_final.py.
// Com símbolo: claro e escuro; as peças do símbolo chegam de simbolo.entrada e se encaixam. Com logo.cenas
//   {nome: {"fundo": cor, "cor": cor do símbolo}}, uma cena por item, de fundo chapado e sem halo nem brilho (marca sem luz).
// Só tipografia (simbolo null): o nome em curvas, a partir de movimento/geometria-entrada.json (gerado por gera_final.py).
//   Cada trecho entra do jeito pedido em logo.trechos[i].entrada: "de" [dx, dy] (deslocamento inicial, em unidades do
//   logo: altura da maiúscula = 100), "eixos" (eixos de partida; o desenho se transforma até os eixos finais, ex.:
//   largura 100 -> 125) e "atraso" (ms). Duração de cada trecho = tempo_assinatura; curva = curva da marca.
//   Uma cena por item de logo.cenas {nome: {"fundo": cor, "cor": cor do nome}}; o nome ocupa metade da largura do quadro.
const F=process.env.FERRAMENTAS||require('path').join(require('os').homedir(),'.cache/design-squad-identidade');
const {chromium}=require(F+'/node_modules/playwright');const ff=require(F+'/node_modules/ffmpeg-static');
const fs=require('fs'),path=require('path');const {execFileSync}=require('child_process');
const M=JSON.parse(fs.readFileSync(process.env.MARCA_JSON||path.resolve('../../marca.json'),'utf8'));
const cor=Object.fromEntries(M.cores.map(c=>[c.nome,c.hex]));
const P=Object.fromEntries(Object.entries(M.papeis||{}).map(([k,v])=>[k,v.startsWith('#')?v:cor[v]]));
const curva=M.curva.valor.replace(/ /g,'');const dur=parseInt(M.tempo_assinatura.valor);
const grava=(dir,nome)=>{
 execFileSync(ff,['-y','-loglevel','error','-framerate','30','-i',`${dir}/%04d.png`,'-c:v','libx264','-pix_fmt','yuv420p','-crf','16','-movflags','+faststart',`./movimento/abertura-${nome}.mp4`]);
 fs.copyFileSync(`${dir}/0100.png`,`./movimento/quadro-final-${nome}.png`);fs.rmSync(dir,{recursive:true,force:true});
 console.log('video',nome);};

async function comSimbolo(){
const sem=Object.fromEntries((M.semanticos||[]).map(s=>[s.nome,s]));
const R=(v,t)=>{while(v.startsWith('{')){const n=v.slice(1,-1);v=cor[n]||sem[n][t];}return v;};
const Cc=v=>v.startsWith('#')?v:cor[v];
const S=M.simbolo,VB=S.viewBox||'0 0 100 100',ent=S.entrada||S.pecas.map((_,i)=>i%2?[14,14]:[-14,-14]);
const csim=M.logo.cores_simbolo;const C=n=>{const v=csim[n];return v&&(v.startsWith('#')?v:cor[v]);};
const cenas=M.logo.cenas?Object.fromEntries(Object.entries(M.logo.cenas).map(([n,c])=>[n,{bg:Cc(c.fundo),cor:Cc(c.cor),fx:'',halo:''}])):{
 escuro:{bg:`radial-gradient(90% 80% at 30% 0%,${P.escuro_claro||P.escuro},${P.escuro} 62%)`,cor:C('claro')||'#FFFFFF',fx:`filter:drop-shadow(0 0 1px rgba(255,255,255,.25)) drop-shadow(0 0 22px ${R(sem.brilho.escuro,'escuro')})`,halo:''},
 claro:{bg:P.fundo_claro||'#FFFFFF',cor:C('primaria')||P.primaria,fx:'',halo:`<div id="h" style="position:absolute;inset:-25%;background:radial-gradient(38% 42% at 68% 34%,${R(sem['halo-1'].claro,'claro')},transparent 70%),radial-gradient(34% 38% at 28% 80%,${R(sem['halo-2'].claro,'claro')},transparent 70%);filter:blur(30px)"></div>`}};
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
fs.mkdirSync('./movimento',{recursive:true});
for(const [nome,c] of Object.entries(cenas)){
 const paths=S.pecas.map((d,i)=>`<path id="p${i}" fill="${c.cor}" d="${d}"/>`).join('');
 await p.setContent(`<body style="margin:0;width:1920px;height:1080px;overflow:hidden;position:relative;background:${c.bg};display:grid;place-items:center">${c.halo}<svg viewBox="${VB}" width="420" height="420" style="position:relative;overflow:visible;${c.fx}">${paths}</svg></body>`);
 await p.evaluate(({n,ent,curva,dur})=>{for(let i=0;i<n;i++){const [x,y]=ent[i]||[0,0];
   document.getElementById('p'+i).animate([{transform:`translate(${x}px,${y}px)`,opacity:0},{opacity:1,offset:.35},{transform:'none',opacity:1}],{duration:dur,delay:300,easing:curva,fill:'both'});}
  const h=document.getElementById('h');if(h)h.animate([{opacity:.6,transform:'scale(.97)'},{opacity:1,transform:'scale(1.04)'},{opacity:.8,transform:'scale(1)'}],{duration:4000,easing:'ease-in-out',fill:'both'});
  document.getAnimations().forEach(a=>a.pause());},{n:S.pecas.length,ent,curva,dur});
 const dir=`quadros-${nome}`;fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir);
 for(let i=0;i<120;i++){await p.evaluate(t=>document.getAnimations().forEach(a=>a.currentTime=t),i*1000/30);await p.screenshot({path:`${dir}/${String(i).padStart(4,'0')}.png`});}
 grava(dir,nome);}
await b.close();}

async function soTipografia(){
const G=JSON.parse(fs.readFileSync('./movimento/geometria-entrada.json','utf8'));const [,,VW,VH]=G.viewBox.split(' ').map(Number);
const C=v=>v.startsWith('#')?v:cor[v];
const cenas=M.logo.cenas||{claro:{fundo:P.fundo_claro||'#FFFFFF',cor:Object.values(M.logo.combinacoes)[0].cor}};
const num=/-?\d*\.?\d+(?:e-?\d+)?/g;
const tr=G.trechos.map(t=>({a:t.inicio.match(num).map(Number),b:t.fim.match(num).map(Number),partes:t.fim.split(num),de:t.de,atraso:t.atraso}));
tr.forEach((t,i)=>{if(t.a.length!==t.b.length)throw new Error(`trecho ${i}: início e fim com números diferentes`);});
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
fs.mkdirSync('./movimento',{recursive:true});
for(const [nome,c] of Object.entries(cenas)){
 const paths=G.trechos.map((t,i)=>`<path id="t${i}" fill="${C(c.cor)}" d="${t.fim}"/>`).join('');
 await p.setContent(`<body style="margin:0;width:1920px;height:1080px;overflow:hidden;background:${C(c.fundo)};display:grid;place-items:center"><svg viewBox="${G.viewBox}" width="960" height="${960*VH/VW}" style="overflow:visible">${paths}</svg></body>`);
 await p.evaluate(({tr,curva,dur})=>{
  const [x1,y1,x2,y2]=curva.match(/-?[\d.]+/g).map(Number);
  const ease=t=>{if(t<=0)return 0;if(t>=1)return 1;let lo=0,hi=1,u=t;for(let k=0;k<50;k++){u=(lo+hi)/2;const x=3*(1-u)**2*u*x1+3*(1-u)*u*u*x2+u**3;if(x<t)lo=u;else hi=u;}return 3*(1-u)**2*u*y1+3*(1-u)*u*u*y2+u**3;};
  window.quadro=ms=>tr.forEach((t,i)=>{const e=ease((ms-300-t.atraso)/dur),el=document.getElementById('t'+i);
   el.setAttribute('opacity',Math.min(1,e/.35));el.setAttribute('transform',`translate(${t.de[0]*(1-e)} ${t.de[1]*(1-e)})`);
   let d=t.partes[0];for(let k=0;k<t.b.length;k++)d+=(t.a[k]+(t.b[k]-t.a[k])*e).toFixed(2)+t.partes[k+1];el.setAttribute('d',d);});
 },{tr,curva,dur});
 const dir=`quadros-${nome}`;fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir);
 for(let i=0;i<120;i++){await p.evaluate(t=>window.quadro(t),i*1000/30);await p.screenshot({path:`${dir}/${String(i).padStart(4,'0')}.png`});}
 grava(dir,nome);}
await b.close();}

(M.simbolo?comSimbolo:soTipografia)();
