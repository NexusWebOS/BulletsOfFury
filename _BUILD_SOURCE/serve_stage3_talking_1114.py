from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import functools,re,json
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/stage3_talking_1114'
class Handler(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def send_head(self):
  self.remaining=None
  path=Path(self.translate_path(self.path))
  if path.is_file()and path.suffix.lower()in ['.mp4','.webm']:
   f=path.open('rb');size=path.stat().st_size;start=0;end=size-1;partial=False
   raw=self.headers.get('Range')
   if raw:
    m=re.fullmatch(r'bytes=(\d*)-(\d*)',raw)
    if not m or not any(m.groups()):
     f.close();self.send_error(416);return None
    if m[1]:start=int(m[1]);end=min(end,int(m[2]))if m[2]else end
    else:start=max(0,size-int(m[2]))
    if start>end or start>=size:
     f.close();self.send_response(416);self.send_header('Content-Range','bytes */'+str(size));self.end_headers();return None
    partial=True
   self.remaining=end-start+1;f.seek(start)
   self.send_response(206 if partial else 200);self.send_header('Content-Type',self.guess_type(str(path)));self.send_header('Accept-Ranges','bytes');self.send_header('Content-Length',str(self.remaining));self.send_header('Last-Modified',self.date_time_string(path.stat().st_mtime))
   if partial:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
   self.end_headers();return f
  return super().send_head()
 def copyfile(self,source,outputfile):
  try:
   if self.remaining is None:return super().copyfile(source,outputfile)
   left=self.remaining
   while left:
    chunk=source.read(min(left,1024*1024))
    if not chunk:break
    outputfile.write(chunk);left-=len(chunk)
  except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError):pass
for port in range(8766,8776):
 try:server=ThreadingHTTPServer(('127.0.0.1',port),functools.partial(Handler,directory=str(ROOT)));break
 except OSError:continue
else:raise RuntimeError('No free preview port')
url=f'http://127.0.0.1:{port}/_shots/stage3_talking_1114/review.html'
(OUT/'server.json').write_text(json.dumps({'port':port,'url':url,'root':str(ROOT),'supportsByteRanges':True},indent=2),encoding='utf-8')
print('Serving seekable cinematic preview: '+url,flush=True)
server.serve_forever()
