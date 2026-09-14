"""Recover already recorded native frames/audio logs, with export-only peak control."""
from pathlib import Path
import sys,json,base64,array,subprocess,http.server,threading,ast,hashlib
R=Path(__file__).resolve().parents[2];O=R/'_shots/furyship_live_0914/video'
sys.path.insert(0,str(R/'_BUILD_SOURCE/trailer_v7'))
sys.path.insert(0,str(R/'_BUILD_SOURCE/stage_1_5_0914'));import audio_export
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
class Quiet(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(R),**kw)
 def log_message(self,*a):pass
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
ff=imageio_ffmpeg.get_ffmpeg_exe();report=json.loads((O/'report.json').read_text());reports=[]
assert report['runtimeSha256']==hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest()
with sync_playwright()as p:
 b=p.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=b.new_page();pg.goto('http://127.0.0.1:%d/index.html'%srv.server_port,wait_until='load',timeout=120000)
 for name,seconds in [('transformation',12),('flight',14)]:
  ev=json.loads((O/(name+'_events.json')).read_text())
  res=pg.evaluate(audio_export.RENDER,{'ev':ev,'iife':audio_export.audio_module_source(),'tail':0,'exclude':[]})
  assert not res['errs']and res['rms']>0,res['errs']
  gain=min(1,.85/res['peak']);samples=array.array('f');samples.frombytes(base64.b64decode(res['b64']))
  raw=array.array('f',(v*gain for v in samples)).tobytes();wav=O/(name+'_sfx.wav');audio_export.write_wav_float(str(wav),raw)
  subprocess.run([ff,'-y','-v','error','-i',str(O/(name+'_picture.mp4')),'-i',str(wav),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',str(O/(name+'.mp4'))],check=True)
  take=next((q for q in report['takes']if q['name']==name),{'name':name,'seconds':seconds})
  take['timeline']=[{'s':float(line.split(' ',2)[1]),**ast.literal_eval(line.split(' ',2)[2])}for line in (O.parent/'record.log').read_text().splitlines()if line.startswith(name+' ')]
  take['audio']={**{k:res[k]for k in ['peak','rms','counts','errs']},'exportGain':gain,'exportPeak':res['peak']*gain};take['sounds']=sorted(set(e[1]for e in ev['snd']));reports.append(take)
  print(name,take['audio'],flush=True)
 b.close()
srv.shutdown();report['takes']=reports;report['exportNote']='Recorded pictures preserved. Audio rebuilt from existing frame log with constant per-take gain to hold raw sample peaks at 0.85; gameplay sound settings unchanged.'
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
concat=O/'concat.txt';concat.write_text(''.join("file '%s'\n"%(O/(r['name']+'.mp4')).as_posix()for r in reports))
final=O/'BulletsOfFury_Furyship_0914.mp4'
subprocess.run([ff,'-y','-v','error','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(final)],check=True)
subprocess.run([ff,'-v','error','-i',str(final),'-f','null','-'],check=True)
print('VIDEO',final,flush=True)
