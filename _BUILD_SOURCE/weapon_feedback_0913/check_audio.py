import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE/trailer_v7'));import render_audio
from playwright.sync_api import sync_playwright
OUT=ROOT/'_shots/weapon_feedback_0913/video'
class Quiet(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
    def log_message(self,*a):pass
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
with sync_playwright()as p:
    br=p.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page();pg.goto('http://127.0.0.1:%d/index.html'%srv.server_port,timeout=120000)
    name=sys.argv[1]if len(sys.argv)>1 else 'juggernaut_dash';ev=json.loads((OUT/(name+'_events.json')).read_text());names=set(e[1]for e in ev['snd'])|set(ev['loops'])
    ours=[n for n in names if n.startswith('laserMist' if name=='laser_mist' else 'juggernaut')]
    report={}
    for label,exclude in [('full',[]),('without_new',ours),('new_only',[n for n in names if n not in ours]),*[(n,[k for k in names if k!=n])for n in names]]:
        r=pg.evaluate(render_audio.RENDER,{'ev':ev,'iife':render_audio.audio_module_source(),'tail':0,'exclude':exclude})
        report[label]={k:r[k]for k in ['peak','rms','counts','errs']};print(label+' '+json.dumps(report[label]),flush=True)
        if label=='full':render_audio.write_wav_float(str(OUT/(name+'_mix_check.wav')),base64.b64decode(r['b64']))
    (OUT/(name+'_mix-check.json')).write_text(json.dumps(report,indent=2));br.close()
srv.shutdown()
