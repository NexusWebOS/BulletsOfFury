// Local static art review only; no gameplay or write endpoints.
const http=require('http'),fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const mime={'.html':'text/html','.js':'text/javascript','.json':'application/json','.png':'image/png','.md':'text/plain'};
http.createServer((req,res)=>{let file;try{file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://127.0.0.1').pathname));}catch{res.writeHead(400).end();return;}if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}fs.readFile(file,(err,data)=>{if(err){res.writeHead(404).end();return;}res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});res.end(data);});}).listen(8771,'127.0.0.1',()=>console.log('Art review: http://127.0.0.1:8771/onfoot/preview.html'));
