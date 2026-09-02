const http=require('http'),fs=require('fs'),path=require('path');
let playwright;try{playwright=require('playwright');}catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime','dependencies','node','node_modules','playwright'));}
const ROOT=path.resolve(__dirname,'..');
const server=http.createServer((req,res)=>{const rel=decodeURIComponent((req.url||'/').split('?')[0]).replace(/^\/+/, '')||'index.html',f=path.resolve(ROOT,rel);fs.readFile(f,(e,d)=>{if(e){res.writeHead(404);res.end();}else{res.writeHead(200);res.end(d);}});});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const b=await playwright.chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'}),p=await b.newPage();await p.goto(`http://127.0.0.1:${server.address().port}/index.html`);await p.waitForFunction(()=>window.__bofFrames>4);
  const out=await p.evaluate(()=>{const r={};for(const n of [4,8]){beginStage(n);r[n]=_stageLoads[n].keys.slice();}return r;});console.log(JSON.stringify(out,null,2));await b.close();server.close();})().catch(e=>{console.error(e);server.close();process.exit(1);});
