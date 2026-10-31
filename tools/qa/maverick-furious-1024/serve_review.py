"""Local evidence viewer with byte-range support for long video seeking."""
from pathlib import Path
import http.server,functools,json,re,shutil,os
W=Path(__file__).resolve().parent;O=W/'review'
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def send_head(self):
  path=Path(self.translate_path(self.path)).resolve()
  if path.is_file()and self.headers.get('Range'):
   if O.resolve()not in path.parents:self.send_error(403);return None
   size=path.stat().st_size;m=re.fullmatch(r'bytes=(\d+)-(\d*)',self.headers['Range'])
   if not m:self.send_error(416);return None
   start=int(m[1]);end=min(int(m[2])if m[2]else size-1,size-1)
   if start>=size or end<start:self.send_error(416);return None
   f=path.open('rb');f.seek(start);self._remaining=end-start+1
   self.send_response(206);self.send_header('Content-type',self.guess_type(str(path)));self.send_header('Accept-Ranges','bytes');self.send_header('Content-Range',f'bytes {start}-{end}/{size}');self.send_header('Content-Length',str(self._remaining));self.end_headers();return f
  self._remaining=None;return super().send_head()
 def copyfile(self,source,outputfile):
  left=getattr(self,'_remaining',None)
  try:
   if left is None:return super().copyfile(source,outputfile)
   while left:
    block=source.read(min(left,1024*1024))
    if not block:break
    outputfile.write(block);left-=len(block)
  except(ConnectionResetError,BrokenPipeError):pass
if __name__=='__main__':
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(O)))
 (W/'viewer.json').write_text(json.dumps({'url':f'http://127.0.0.1:{server.server_address[1]}','pid':os.getpid()}));server.serve_forever()
