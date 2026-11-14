from pathlib import Path
import sys,json,ast,base64,time,subprocess
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
W=Path(r'C:/Users/Mike/Documents/Codex/2026-11-11/i-k/work/rage_palm_1110')
if not (W/'seed119.js').exists():W=Path(r'C:/Users/Mike/Documents/New project/BOF-Rage-Polish-1110')
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=Path(r'C:/Users/Mike/Documents/Codex/2026-11-11/i-k/outputs/Solid-metal-hammers');O.mkdir(exist_ok=True);(O/'gifs').mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve;from barrage_review_common_1025 import boot
seed=(W/'seed119.js').read_text(encoding='utf8')
CAP=json.loads((W/'capture.json').read_text()).replace('c.height=800','c.height=844').replace('1280,800','1280,844').replace('290,755,700,38','290,800,700,38').replace('640,780','640,825')

ff=imageio_ffmpeg.get_ffmpeg_exe()
def record_loaded(p,stage,errors):
 unit="chronos" if stage==5 else "dracodia"
 records=[];contracts=[]
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

 # Step the real native loop and capture its rendered pixels. This avoids a stalled live MediaRecorder.
 import io
 from PIL import Image
 from shoot import STEP
 video=O/(unit+'-hammer.mp4'); encoder=imageio_ffmpeg.write_frames(str(video),(1280,800),fps=20,codec='libx264',quality=7,output_params=['-movflags','+faststart'])
 encoder.send(None); chapters=[]; seen=[]; total=0
 try:
  for material in ['regular','chrome']:
   chapters.append(dict(name=material,at=total/20))
   if stage==5:p.evaluate("m=>seed119('furious',m)",material)
   else:p.evaluate("m=>{diffKey='furious';DIFF=difficultyForRun(run.mode,diffKey);B._r30.mode='fight';B._r30.v18.donorAge=0;B.hp=B.maxhp;B.enter=B._noHit=B.dead=false;B.x=worldWidth()/2;B.y=viewTopY()+200;Q.rf1110=null;Q.rage=false;Q.chrome=m==='chrome';Q.action=null;Q.cool=999;Q.speech=null;Q.pendingRecall=Q.pendingGun=Q.pendingArsenal=false;eBullets=[];pBullets=[];hb20Start(B,'skystrike');}",material)
   for i in range(140):
    err=p.evaluate(STEP,3); assert err is None,err
    p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}')
    encoder.send(Image.open(io.BytesIO(p.screenshot())).convert('RGB').tobytes());total+=1
    if i%20==0:
     q=p.evaluate("s=>{const p=s===5?ha21Blue(B):hb20Pose(B);return{bank:p?.a.bank,frame:p?.a.frame}}",stage);seen.append(dict(material=material,i=i,**q));print('Captured '+unit+' '+material+' '+str(i+1)+'/140',flush=True)
 finally: encoder.close()
 dst=O/'gifs'/f'{unit}-hammer.gif';vf='crop=750:800:265:0,scale=420:448:flags=neighbor,fps=20,split[a][b];[a]palettegen=max_colors=256:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle'
 subprocess.run([ff,'-v','error','-y','-i',str(video),'-filter_complex',vf,'-loop','0',str(dst)],check=True)
 record=dict(unit=unit,video=str(video),seconds=total/20,chapters=chapters,frames=total,audioIncluded=False,method='Deterministic native game loop, one screenshot per three60Hz ticks; silent20FPS playback',sampledPoses=seen)
 (Path(__file__).resolve().parent/(unit+'-recording.json')).write_text(json.dumps(dict(records=[record],errors=errors),indent=2));p.close();print('Finished native frame-step capture '+unit,flush=True)
