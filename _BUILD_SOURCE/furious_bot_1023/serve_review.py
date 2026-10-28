from pathlib import Path
import http.server,functools,json,os
W=Path(__file__).resolve().parent
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(W/'review')))
(W/'server.json').write_text(json.dumps({'url':f'http://127.0.0.1:{server.server_address[1]}/index.html','pid':os.getpid()}))
server.serve_forever()
