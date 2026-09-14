const http=require('http'),fs=require('fs'),path=require('path');
http.createServer((req,res)=>{let p;try{p=path.resolve(__dirname,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname))}catch{res.writeHead(400).end();return}if(!p.startsWith(__dirname+path.sep)&&p!==__dirname){res.writeHead(403).end();return}if(p===__dirname)p=path.join(p,'index.html');fs.readFile(p,(e,b)=>{if(e){res.writeHead(404).end();return}res.setHeader('Content-Type',({'.png':'image/png','.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css'})[path.extname(p)]||'text/plain');res.setHeader('Cache-Control','no-store');res.end(b)})}).listen(8783,'127.0.0.1',()=>console.log('Tempest encounter: http://127.0.0.1:8783/'));



