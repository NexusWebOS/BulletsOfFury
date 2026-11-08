from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import argparse,json,mimetypes,os,re,urllib.parse
W=Path(__file__).resolve().parent;routes=json.loads((W/'routes.json').read_text());ap=argparse.ArgumentParser();ap.add_argument('--port',type=int,default=65044);args=ap.parse_args()
static={'/':W/'index.html','/index.html':W/'index.html','/manifest.json':W/'manifest.json','/report.json':W/'report.json'}
static.update({'/posters/'+p.name:p for p in(W/'posters').glob('*.png')})
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_HEAD(self):self.reply(False)
 def do_GET(self):self.reply(True)
 def reply(self,body):
  name=urllib.parse.urlparse(self.path).path
  if name=='/favicon.ico':self.send_response(204);self.end_headers();return
  active_routes=json.loads((W/'routes.json').read_text())
  path=Path(active_routes[name])if name in active_routes else static.get(name)
  if not path or not path.is_file():self.send_error(404);return
  total=path.stat().st_size;start=0;end=total-1;status=200;range_=self.headers.get('Range')
  if range_:
   m=re.fullmatch(r'bytes=(\d*)-(\d*)',range_)
   if not m:self.send_error(416);return
   if not m[1]:start=max(0,total-int(m[2]))
   else:start=int(m[1]);end=min(end,int(m[2]))if m[2]else end
   if start>end or start>=total:self.send_response(416);self.send_header('Content-Range',f'bytes */{total}');self.end_headers();return
   status=206
  self.send_response(status);self.send_header('Content-Type',mimetypes.guess_type(str(path))[0]or'application/octet-stream');self.send_header('Content-Length',str(end-start+1));self.send_header('Accept-Ranges','bytes');self.send_header('Cache-Control','no-cache')
  if status==206:self.send_header('Content-Range',f'bytes {start}-{end}/{total}')
  self.end_headers()
  if not body:return
  try:
   with path.open('rb')as f:
    f.seek(start);left=end-start+1
    while left:
     data=f.read(min(left,1024*1024))
     if not data:break
     self.wfile.write(data);left-=len(data)
  except(ConnectionResetError,ConnectionAbortedError,BrokenPipeError):pass
server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler);server.daemon_threads=True
(W/'server.json').write_text(json.dumps({'url':'http://127.0.0.1:'+str(server.server_port)+'/','port':server.server_port,'pid':os.getpid()}));server.serve_forever()
