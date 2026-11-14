from pathlib import Path
import sys,json,ast,base64,time,subprocess
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent.parent/'rage_palm_1110'
if not (W/'seed119.js').exists():W=Path(r'C:/Users/Mike/Documents/New project/BOF-Rage-Polish-1110')
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=R/'_shots/hammer_face_1110';O.mkdir(exist_ok=True);(Path(__file__).resolve().parent/'gifs').mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve;from barrage_review_common_1025 import boot
seed=(W/'seed119.js').read_text(encoding='utf8')
CAP=json.loads((W/'capture.json').read_text()).replace('c.height=800','c.height=844').replace('1280,800','1280,844').replace('290,755,700,38','290,800,700,38').replace('640,780','640,825')
errors=[];records=[];port,stop=serve(str(R));ff=imageio_ffmpeg.get_ffmpeg_exe()
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
  review_context=br.new_context(viewport={'width':1280,'height':800})
  for unit,stage in [('chronos',5),('dracodia',8)]:
   p=boot(review_context,port,stage,errors,'boss');p.wait_for_function('(s)=>{stageLoadTick();return rf1110Warm(s)&&ba119Warm(s)&&(s!==5||rh1110Warm())}',arg=stage,timeout=180000)
   p.evaluate("()=>{const hold=Input.hold;Input.hold=function(...a){return a.includes('fire')?false:hold.apply(this,a)};DBGT.god=true;player.invuln=1e9;}")
   if stage==5:p.evaluate(seed)
   else:p.evaluate("()=>{window.B=boss;v18Enter(B,2,8);B._r30.mode='fight';B._r30.v18.donorAge=0;B.enter=B._noHit=B.dead=false;BOFCinematicDirector.cancel();window.Q=hb20State(B);}")
   raw=O/(unit+'-hammer.webm');f=raw.open('wb');p.expose_function('save119',lambda b:f.write(base64.b64decode(b)));p.evaluate("u=>{label119=(u==='chronos'?'Stage 5 Chronos':'Stage 8 Dracodia / Chronos copy')+' / cap-leading hammer attacks / live engine, god observer';}",unit);p.evaluate(CAP);start=time.monotonic();print('Recording '+unit,flush=True)
   chapters=[]
   for material in ['regular','chrome']:
    chapters.append(dict(name=material,at=round(time.monotonic()-start,3)))
    if stage==5:p.evaluate("m=>{seed119('furious',m);}",material)
    else:p.evaluate("m=>{B._r30.mode='fight';B._r30.v18.donorAge=0;B.hp=B.maxhp;B.enter=B._noHit=B.dead=false;B.x=worldWidth()/2;B.y=viewTopY()+200;Q.rf1110=null;Q.rage=false;Q.chrome=m==='chrome';Q.action=null;Q.cool=999;Q.speech=null;Q.pendingRecall=Q.pendingGun=Q.pendingArsenal=false;eBullets=[];pBullets=[];hb20Start(B,'skystrike');}",material)
    p.wait_for_timeout(8500)
   stat=p.evaluate("async()=>{await new Promise(r=>{rec119.onstop=r;rec119.stop()});await pending119;live119=false;return{...captureStats,sfxStarts:AL116.stats.starts-captureStats.starts,errors:AL116.errors,events:RF1110.events.slice(),c32:C32.events.slice(-80),energy:CF49.events.slice(),lightning:CF48.events.slice(),dracAudio:RD74.events.filter(e=>e.event==='sound').slice(),phase:BOF_RAGE_PALM_1110.last};}");f.close();video=raw.with_suffix('.mp4');subprocess.run([ff,'-v','error','-y','-i',str(raw),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
   for name,start,end in [('hammer',chapters[0]['at'],chapters[1]['at'])]:
    dst=Path(__file__).resolve().parent/'gifs'/f'{unit}-{name}.gif';vf='crop=750:800:265:0,scale=420:448:flags=neighbor,fps=24,split[a][b];[a]palettegen=max_colors=256:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle';subprocess.run([ff,'-v','error','-y','-ss',str(start),'-t',str(max(1,end-start)),'-i',str(video),'-filter_complex',vf,'-loop','0',str(dst)],check=True)
   record=dict(unit=unit,video=str(video),seconds=round(time.monotonic()-start,2),chapters=chapters,audio=stat);records.append(record);(Path(__file__).resolve().parent/'recording.json').write_text(json.dumps(dict(records=records,errors=errors),indent=2));p.close();print('Finished '+unit,json.dumps(dict(audioPeak=stat['peak'],audioStarts=stat['sfxStarts'],chapters=chapters)),flush=True)
  br.close()
finally:stop()
