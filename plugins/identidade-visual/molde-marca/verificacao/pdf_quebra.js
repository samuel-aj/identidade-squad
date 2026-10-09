// Teste de estresse da quebra de página: empurra o conteúdo do modelo de documento em passos de 20 px e gera
// um PDF A4 por posição. Depois rode pdf_quebra.py para conferir. Uso: node pdf_quebra.js <documento.html> <pasta-saída>
// O arquivo é aberto pelo endereço (file://), não colado na página: assim um modelo que liga CSS externo (../css/…,
// como a apostila da skill de uma marca) sai com o estilo, e o teste não acusa quebra de uma página sem CSS. O espaçador
// entra pelo DOM, antes do sumário do documento (<div class="xx-doc__sumario">) ou, sem ele, antes do <main>.
const F=process.env.FERRAMENTAS||require('path').join(require('os').homedir(),'.cache/design-squad-identidade');
const {chromium}=require(F+'/node_modules/playwright');const fs=require('fs'),path=require('path'),url=require('url');
const [src,out]=process.argv.slice(2);fs.mkdirSync(out,{recursive:true});
(async()=>{const b=await chromium.launch();const p=await b.newPage();
 await p.goto(url.pathToFileURL(path.resolve(src)).href,{waitUntil:'load'});await p.evaluate(()=>document.fonts.ready);
 const onde=await p.evaluate(()=>{
  const alvo=[...document.querySelectorAll('div[class]')].find(e=>/^[a-z0-9]+-doc__sumario$/.test(e.getAttribute('class')))||document.querySelector('main');
  if(!alvo) return null;
  const e=document.createElement('div');e.id='__espacador_pdf_quebra';e.style.height='0px';alvo.before(e);
  return alvo.tagName.toLowerCase()+'.'+(alvo.getAttribute('class')||'');});
 if(!onde){console.error('sem sumário (xx-doc__sumario) nem <main> para empurrar');process.exit(1);}
 for(let h=0;h<=440;h+=20){
  await p.evaluate(h=>{document.getElementById('__espacador_pdf_quebra').style.height=h+'px';return document.fonts.ready;},h);
  fs.writeFileSync(`${out}/${String(h).padStart(3,'0')}.pdf`,await p.pdf({format:'A4',printBackground:true,preferCSSPageSize:true}));}
 await b.close();console.log('23 PDFs em',out,`(espaçador antes de ${onde})`);})();
