from pathlib import Path
import sys,json,ast,base64,time,subprocess
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent.parent/'rage_palm_1110'
if not (W/'seed119.js').exists():W=Path(r'C:/Users/Mike/Documents/New project/BOF-Rage-Polish-1110')
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=R/'_shots/overhead_slam_1111';O.mkdir(exist_ok=True);(O/'gifs').mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve;from barrage_review_common_1025 import boot
seed=(W/'seed119.js').read_text(encoding='utf8')
CAP=json.loads((W/'capture.json').read_text()).replace('c.height=800','c.height=844').replace('1280,800','1280,844').replace('290,755,700,38','290,800,700,38').replace('640,780','640,825')
errors=[];records=[];contracts=[];port,stop=serve(str(R));ff=imageio_ffmpeg.get_ffmpeg_exe()
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
  review_context=br.new_context(viewport={'width':1280,'height':800})
  for unit,stage in [(sys.argv[1],5 if sys.argv[1]=='chronos' else 8)]:
   p=boot(review_context,port,stage,errors,'boss');p.wait_for_function('(s)=>{stageLoadTick();return rf1110Warm(s)&&ba119Warm(s)&&(s!==5||rh1110Warm())}',arg=stage,timeout=180000)
   p.wait_for_function('(s)=>{stageLoadTick();if(stageLoadReady(s))updatePlay(0);return stageLoadReady(s)&&!bp119Pending()}',arg=stage,timeout=180000)
   p.evaluate("()=>{const hold=Input.hold;Input.hold=function(...a){return a.includes('fire')?false:hold.apply(this,a)};DBGT.god=true;player.invuln=1e9;}")
   if stage==5:p.evaluate(seed)
   else:p.evaluate("()=>{window.B=boss;v18Enter(B,2,8);B._r30.mode='fight';B._r30.v18.donorAge=0;B.enter=B._noHit=B.dead=false;BOFCinematicDirector.cancel();window.Q=hb20State(B);}")
   if stage==5:
    contract=p.evaluate("""()=>{seed119('furious','regular');const h=B._hammer;h.t=.27;const q=ha21Blue(B),a=q.a,at={x:B.x+a.headCenter[0]-a.pivot[0],y:B.y+a.headCenter[1]-a.pivot[1]},hit=bossHitTest(at.x,at.y);const result={unit:'chronos',whole:q.a.wholeGenerated,heldTarget:hammerWeaponTargetable(B),heldIntercept:c26Shootable(B),headUsesActorMask:hit&&h._hammerModuleHit==null};hammerBoomerangStart(B);h.t=HAMMER_SPIN_TIME-.001;const end=ha21Blue(B),expected={x:B.x+end.a.headCenter[0]-end.a.pivot[0],y:B.y+end.a.headCenter[1]-end.a.pivot[1]};hammerBoomerangRelease(B);result.releaseError=Math.hypot(h.throw.x-expected.x,h.throw.y-expected.y);result.detachedTarget=hammerWeaponTargetable(B);result.detachedIntercept=c26Shootable(B);const dest=c35Catch(B).at;h.throw.phase='return';h.throw.x=dest.x+1;h.throw.y=dest.y;hammerBoomerangTick(B,1/60);const caught=ha21Blue(B),visible=hb20World(caught.a,caught.a.headCenter,B,caught.k,0);result.catchError=Math.hypot(dest.x-visible.x,dest.y-visible.y);result.catchWhole=caught.a.wholeGenerated&&!h.throw&&h.state==='hammer_catch';seed119('furious','regular');return result;}""")
    assert contract['whole'] and not contract['heldTarget'] and not contract['heldIntercept'] and contract['headUsesActorMask'] and contract['releaseError']<.1 and contract['detachedTarget'] and contract['detachedIntercept'] and contract['catchWhole'] and contract['catchError']<.1,contract
   else:
    contract=p.evaluate("""()=>{Q.rage=Q.chrome=false;Q.rf1110=null;Q.action=null;Q.cool=999;Q.speech=null;B._noHit=false;hb20Start(B,'skystrike');const old=rd74DrawTool;let toolDraws=0;rd74DrawTool=function(...a){toolDraws++;return old.apply(this,a)};const q=hb20Pose(B),head=rd74Point(B,q,'headCenter'),rig=v19HammerRig(B);drawWorld(0);const result={unit:'dracodia',whole:q.a.wholeGenerated,heldParts:rig.map(v=>v.p.id),heldToolDraws:toolDraws,headUsesActorMask:v19AtRect(rig[0],head.x,head.y)};hb20Start(B,'throw');const A=Q.action;A.t=A.tell-1/120;const expected=rf1110HammerCentre(B,ba119Row('corrupt-overhead',8,'regular'));v19NativeTick(B,1/60);result.releaseError=Math.hypot(A.launch.x-expected.x,A.launch.y-expected.y);result.detachedParts=v19HammerRig(B).map(v=>v.p.id);toolDraws=0;drawWorld(0);result.detachedToolDraws=toolDraws;result.releasedBodyBank=hb20Pose(B).a.bank;A.t=A.duration-.000001;const landing=rd74ToolAt(B,A),home=rf1110HammerCentre(B,ba119Row('corrupt-overhead',0,rd74Mat(Q)));result.catchError=Math.hypot(landing.x-home.x,landing.y-home.y);rd74DrawTool=old;Q.action=null;Q.cool=999;return result;}""")
    assert contract['whole'] and contract['heldParts']==['core'] and contract['heldToolDraws']==0 and contract['headUsesActorMask'] and contract['releaseError']<.1 and 'hammer'in contract['detachedParts'] and contract['detachedToolDraws']==1 and contract['releasedBodyBank']=='ba119_corrupt-empty_regular' and contract['catchError']<.01,contract
   contracts.append(contract);(Path(__file__).resolve().parent/(unit+'-whole-contract.json')).write_text(json.dumps(dict(checks=contracts,errors=errors),indent=2));print('PASS whole-actor / released-weapon contract',json.dumps(contract),flush=True)
   raw=O/(unit+'-hammer.webm');f=raw.open('wb');p.expose_function('save119',lambda b:f.write(base64.b64decode(b)));p.evaluate("u=>{label119=(u==='chronos'?'Stage 5 Chronos':'Stage 8 Dracodia / Chronos copy')+' / behind-head overheads / forward gaze / live engine, god observer';}",unit);p.evaluate(CAP);start=time.monotonic();print('Recording '+unit,flush=True)
   chapters=[]
   for material in ['regular','chrome']:
    chapters.append(dict(name=material,at=round(time.monotonic()-start,3)))
    if stage==5:p.evaluate("m=>{seed119('furious',m);}",material)
    else:p.evaluate("m=>{B._r30.mode='fight';B._r30.v18.donorAge=0;B.hp=B.maxhp;B.enter=B._noHit=B.dead=false;B.x=worldWidth()/2;B.y=viewTopY()+200;Q.rf1110=null;Q.rage=false;Q.chrome=m==='chrome';Q.action=null;Q.cool=999;Q.speech=null;Q.pendingRecall=Q.pendingGun=Q.pendingArsenal=false;eBullets=[];pBullets=[];hb20Start(B,'skystrike');}",material)
    p.wait_for_timeout(8500)
   chapters.append(dict(name='released throw',at=round(time.monotonic()-start,3)))
   if stage==5:p.evaluate("()=>{seed119('furious','regular');hammerBoomerangStart(B);}")
   else:p.evaluate("()=>{B._r30.mode='fight';B._r30.v18.donorAge=0;Q.rf1110=null;Q.rage=false;Q.chrome=false;Q.action=null;Q.cool=999;Q.speech=null;B.x=worldWidth()/2;B.y=viewTopY()+200;hb20Start(B,'throw');}")
   p.wait_for_timeout(14000)
   stat=p.evaluate("async()=>{await new Promise(r=>{rec119.onstop=r;rec119.stop()});await pending119;live119=false;return{...captureStats,sfxStarts:AL116.stats.starts-captureStats.starts,errors:AL116.errors,events:RF1110.events.slice(),c32:C32.events.slice(-80),energy:CF49.events.slice(),lightning:CF48.events.slice(),dracAudio:RD74.events.filter(e=>e.event==='sound').slice(),phase:BOF_RAGE_PALM_1110.last};}");f.close();video=raw.with_suffix('.mp4');subprocess.run([ff,'-v','error','-y','-i',str(raw),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
   for name,start,end in [('hammer',chapters[0]['at'],chapters[1]['at'])]:
    dst=O/'gifs'/f'{unit}-{name}.gif';vf='crop=750:800:265:0,scale=420:448:flags=neighbor,fps=24,split[a][b];[a]palettegen=max_colors=256:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle';subprocess.run([ff,'-v','error','-y','-ss',str(start),'-t',str(max(1,end-start)),'-i',str(video),'-filter_complex',vf,'-loop','0',str(dst)],check=True)
   import re
   info=subprocess.run([ff,'-i',str(video)],capture_output=True,text=True).stderr;dur=re.search(r'Duration: (\d+):(\d+):([\d.]+)',info);seconds=int(dur[1])*3600+int(dur[2])*60+float(dur[3]);record=dict(unit=unit,video=str(video),seconds=seconds,chapters=chapters,audio=stat);records.append(record);(Path(__file__).resolve().parent/(unit+'-recording.json')).write_text(json.dumps(dict(records=records,errors=errors),indent=2));p.close();print('Finished '+unit,json.dumps(dict(audioPeak=stat['peak'],audioStarts=stat['sfxStarts'],chapters=chapters)),flush=True)
  br.close()
finally:stop()
