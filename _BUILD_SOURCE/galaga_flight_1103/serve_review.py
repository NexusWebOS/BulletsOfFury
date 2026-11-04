from pathlib import Path
import http.server,urllib.parse
R=Path(__file__).resolve().parents[2];W=Path(__file__).parent
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def translate_path(self,path):
  part=urllib.parse.unquote(urllib.parse.urlsplit(path).path)
  base=R if part.startswith('/game/') else W
  rel=part.removeprefix('/game/')if base==R else part.lstrip('/')
  if not rel:rel='review.html'
  target=(base/rel).resolve()
  if not target.is_relative_to(base.resolve())or any(p.startswith('.')for p in Path(rel).parts):return str(W/'unavailable')
  if base==R and rel!='index.html'and not rel.startswith(('assets/','expansion/','extensions/')):return str(W/'unavailable')
  return str(target)
class Server(http.server.ThreadingHTTPServer):
 request_queue_size=256
 daemon_threads=True
Server(('127.0.0.1',65042),Handler).serve_forever()
