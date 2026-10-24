from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import functools,re,json,os
from urllib.parse import unquote,urlsplit
W=Path(__file__).resolve().parent;ROOT=W.parent/'BOF-Furious-Bot-1023/review'
class Handler(SimpleHTTPRequestHandler):
 def translate_path(self,path):
  raw=unquote(urlsplit(path).path)
  if raw.startswith("/corrections/"):
   root=(W/"review").resolve();p=(root/raw[len("/corrections/"):]).resolve()
   return str(p if p.is_relative_to(root) else root/"missing")
  return super().translate_path(path)
 def log_message(self,*a):pass
 def send_head(self):
  self.range_left=None;p=Path(self.translate_path(self.path))
  if not p.is_file():return super().send_head()
  f=p.open('rb');size=p.stat().st_size;r=self.headers.get('Range');lo=0;hi=size-1
  if r:
   m=re.fullmatch(r'bytes=(\d*)-(\d*)',r)
   if not m:self.send_error(416);f.close();return
   if m[1]:lo=int(m[1]);hi=min(size-1,int(m[2])) if m[2] else size-1
   elif m[2]:lo=max(0,size-int(m[2]))
   if lo>=size or hi<lo:
    self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.end_headers();f.close();return
  self.send_response(206 if r else 200);self.send_header('Content-Type',self.guess_type(str(p)));self.send_header('Accept-Ranges','bytes');self.send_header('Content-Length',str(hi-lo+1))
  if r:self.send_header('Content-Range',f'bytes {lo}-{hi}/{size}')
  self.send_header('Cache-Control','no-cache' if p.suffix=='.html' else 'private, max-age=3600');self.end_headers();f.seek(lo);self.range_left=hi-lo+1;return f
 def copyfile(self,source,outputfile):
  if self.range_left is None:return super().copyfile(source,outputfile)
  left=self.range_left
  try:
   while left:
    chunk=source.read(min(left,1024*1024))
    if not chunk:break
    outputfile.write(chunk);left-=len(chunk)
  except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError):pass
server=ThreadingHTTPServer(('127.0.0.1',62566),functools.partial(Handler,directory=str(ROOT)))
(W/'range-server.json').write_text(json.dumps({'pid':os.getpid(),'url':'http://127.0.0.1:62566/index.html'}));server.serve_forever()
