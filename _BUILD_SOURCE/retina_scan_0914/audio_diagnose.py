import json,threading,http.server,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path.cwd();sys.path.insert(0,str(R/'_BUILD_SOURCE/retina_scan_0914'));import record
class Q(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**k):super().__init__(*a,directory=str(R),**k)
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),Q);threading.Thread(target=s.serve_forever,daemon=True).start()
e=json.loads((record.OUT/'retina_scan_events.json').read_text())
with sync_playwright()as p:
 b=p.chromium.launch(args=['--no-sandbox','--mute-audio']);g=b.new_page();g.goto('http://127.0.0.1:%d/index.html'%s.server_port,wait_until='load')
 print('COUNTS', {n:sum(v[1]==n for v in e['snd'])for n in set(v[1]for v in e['snd'])},flush=True)
 for level in [.70,.55,.40]:
  import copy
  x=copy.deepcopy(e)
  for ev in x['snd']:
   if ev[1]=='select':ev[2]*=level
  r=g.evaluate(record.render_audio.RENDER,{'ev':x,'iife':record.render_audio.audio_module_source(),'tail':0,'exclude':[]});print('SELECT',level,'peak',r['peak'],flush=True)
 b.close()
s.shutdown()
