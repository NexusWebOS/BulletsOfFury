from pathlib import Path
import ast,sys,json,time,base64,subprocess
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;O=R/'_shots/dracodia_ball_1109';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
from barrage_review_common_1025 import boot
a=ast.parse((W/'verify.py').read_text(encoding='utf8'));SEED=next(n.value.value for n in a.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='SEED'for t in n.targets));CAPTURE=json.loads((W/'capture.json').read_text(encoding='utf8'))

def capture_session(p):
 errors=getattr(sys.modules['__main__'],'errors',[]);chapters=[]
 cap=CAPTURE.replace('c.height=800','c.height=844').replace('1280,800','1280,844').replace('290,755,700,38','290,800,700,38').replace('640,780','640,825')
 # verify.py already has a running RAF owner. Avoid starting a second loop.
 cap=cap.replace('requestAnimationFrame(loop);render();','render();')
 raw=O/'dracodia-ball.webm';f=raw.open('wb');p.expose_function('save119',lambda b:f.write(base64.b64decode(b)));p.evaluate(cap);start=time.monotonic()
 for mat in ['regular','chrome','red']:
  p.evaluate("m=>{ballSeed(m);label119='Dracodia Chronos ball / '+m+(m==='chrome'?' / gun impact and real Retina rocket counter':' / native curl, ricochet and unfold');}",mat)
  chapter=dict(material=mat,seconds=round(time.monotonic()-start,2));chapters.append(chapter);print('Recording '+mat,flush=True)
  if mat=='chrome':
   p.wait_for_function("db119Own(B)&&db119Phase(Q.action)==='roll'&&Q.action.t>Q.action.tell+.15",timeout=20000)
   p.evaluate("()=>{bossHitTest(B.x,B.y);_dmgBullet={kind:'mg',x:B.x,y:B.y+30};_dmgSrc='bullet';modularHit(2);_dmgBullet=null;_dmgSrc=null;}")
   p.wait_for_timeout(650)
   chapter['rocketLaunched']=p.evaluate("()=>{run.bombs=20;const t=retinaBossTargets(B).find(t=>t._retinaId==='hb20-core');return !!t&&useBomb(t);}")
   try:p.wait_for_function("DB119.events.some(e=>e.event==='rocket-deflect')",timeout=12000);chapter['realRocketDeflected']=True
   except Exception:chapter['realRocketDeflected']=False
  p.wait_for_function('!db119Own(B)',timeout=25000);chapter['end']=round(time.monotonic()-start,2);chapter['events']=p.evaluate('DB119.events.slice()')
 stats=p.evaluate("async()=>{await new Promise(r=>{rec119.onstop=r;rec119.stop()});await pending119;live119=false;return{...captureStats,sfxStarts:AL116.stats.starts-captureStats.starts,errors:AL116.errors};}");f.close();
 ff=imageio_ffmpeg.get_ffmpeg_exe();video=O/'dracodia-ball.mp4';subprocess.run([ff,'-v','error','-y','-i',str(raw),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
 report=dict(route='Live native-engine Furious attack checkpoints, god mode observer; explicitly triggered gun impact; real inventory Retina rocket launch and travel.',chapters=chapters,audio=stats,errors=errors,video=str(video));(O/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf8')
 G=W/'gifs';G.mkdir(exist_ok=True)
 for chapter in chapters[:2]:
  dst=G/('dracodia-ball-'+chapter['material']+'.gif');vf='crop=750:800:265:0,scale=480:512:flags=neighbor,fps=24,split[a][b];[a]palettegen=max_colors=256:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle'
  subprocess.run([ff,'-v','error','-y','-ss',str(chapter['seconds']),'-t',str(chapter['end']-chapter['seconds']),'-i',str(video),'-filter_complex',vf,'-loop','0',str(dst)],check=True)
 print(json.dumps(dict(video=str(video),rocket=[c.get('realRocketDeflected')for c in chapters if c['material']=='chrome'],audio=stats,errors=errors)),flush=True)
