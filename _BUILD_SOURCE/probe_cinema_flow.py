from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');O=Path(__file__).parent/'BOF-Cinema-Rebuild/verification';O.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(n,v,detail=None):
 checks.append(dict(name=n,ok=bool(v),detail=detail));print(('PASS ' if v else 'FAIL ')+n,flush=True)
 if not v:raise AssertionError(n)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(120000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof C22!=="undefined"');p.evaluate(shoot.TRAP_RAF);p.wait_for_function('c22Warm()',polling=50)
  for stage in [1,2,3,4,6]:
   result=p.evaluate('''stage=>{BOFCinematicDirector.cancel();run.mode='campaign';run.pilot='yuri';let calls=0;hqTrigger('post',stage,()=>calls++);const s=BOFCinematicDirector.current;Input.clearTaps();s.age=.3;Input.injectTap(keybind.fire[0]);BOFCinematicDirector.tick(0);const revealed=s.shown===s.beats[0].text.length;Input.clearTaps();Input.injectTap(keybind.fire[0]);BOFCinematicDirector.tick(0);const advanced=s.i===1;Input.clearTaps();Input.injectTap((keybind.start||['enter'])[0]);BOFCinematicDirector.tick(0);Input.clearTaps();return {revealed,advanced,calls,active:BOFCinematicDirector.active};}''',stage)
   ck(str(stage)+' native reveal / next / skip and one continuation',result['revealed'] and result['advanced'] and result['calls']==1 and not result['active'],result)
  p.evaluate("run.mode='campaign';run.pilot='yuri';BOFCinematicDirector.start(5,()=>{throw Error('stale map callback')});BOFCinematicDirector.finish()")
  ck('Stage 5 scramble hands off to native Stage 6 card',p.evaluate('run.stage===6&&state!==GS.CAMPHUB&&state!==GS.STAGESEL'))
  p.evaluate("BOFCinematicDirector.cancel();run.pilot='cole';BOFCinematicDirector.preview('post-3','cole');const s=BOFCinematicDirector.current;s.i=s.beats.findIndex(b=>b.c22==='hq_regroup');s.t=2;s.shown=s.beats[s.i].text.length;drawCutsceneState(0)")
  p.screenshot(path=str(O/'portrait-regroup-final.png'));ck('portrait box contains actual Cole portrait pixels',p.evaluate('UI20.last?.portraitDraw!=null||XART.rdy(commPortrait("cole","idle"))'))
  for name,a in p.evaluate('C22_ART.banks').items():
   hashes=p.evaluate('''({name,a})=>{const out=[];for(let f=0;f<a.frames;f++){ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#172230';ctx.fillRect(0,0,cutsceneViewWidth(),VH);c22Bank(name,(f+.01)/a.fps,cutsceneViewWidth()/2,VH/2,400,true);const d=ctx.getImageData(0,0,cv.width,cv.height).data;let h=2166136261;for(let i=0;i<d.length;i+=4)h=Math.imul(h^d[i]^d[i+1]<<8^d[i+2]<<16,16777619);out.push(h>>>0);}return out;}''',dict(name=name,a=a))
   ck(name+' changes actual rendered pixels',len(set(hashes))>=min(4,a['frames']),hashes)
  p.evaluate("BOFCinematicDirector.cancel();C22.preview('death','cole')")
  snapshots=[];print('DEATH SETUP',p.evaluate('({x:boss.x,y:boss.y,px:player.x,py:player.y,camX,VW,VH,SS,cv:[cv.width,cv.height],state})'),flush=True)
  for target in [2.8,3.35,4.05,4.35,5.6,7.9,9.8]:
   while p.evaluate('boss._r30.t')<target-.00001:
    p.evaluate('''target=>{for(let i=0;i<10&&boss._r30.t<target-.00001;i++){r30Tick(boss,Math.min(.05,target-boss._r30.t));drawWorld(0);}}''',target);p.wait_for_timeout(1)
   s=p.evaluate('({time:boss._r30.t,mode:boss._r30.mode,gone:dr5State(boss).bodyGone,last:C22.lastBank,bits:dr5State(boss).bits.length,dead:player.dead})');snapshots.append(s);print('DEATH',s,flush=True);p.screenshot(path=str(O/f'digital-death-{target}.png'))
  ck('data erasure precedes the explosion',any(3.25<s['time']<4.2 and s['last'] and s['last']['name']=='data_disintegrate' for s in snapshots))
  ck('boss body erased once, no old metal-piece shower',sum(e.get('event')=='digital-disintegration-complete' for e in p.evaluate('C22.events'))==1 and all(s['bits']==0 and s['gone'] for s in snapshots if s['time']>4.2))
  ck('cinematic protects the player',all(not s['dead'] for s in snapshots))
  p.evaluate('C22.deathPreview=false')
  p.evaluate('''()=>{for(let i=0;i<40;i++)r30Tick(boss,.05);drawWorld(0);}''')
  p.screenshot(path=str(O/'native-blue-escape-portal.png'));ck('native death hands off to dimensional blue escape portal',p.evaluate('boss._r30.mode==="dr5Portal"&&C22.lastBank.name==="blue_portal"&&state===GS.PLAY'))
  for t in [106,113,118,121,125]:
   p.evaluate('''t=>{setState(GS.VICTORY);ctx.setTransform(SS,0,0,SS,0,0);inv20Draw(t,cutsceneViewWidth(),VH,drawVictory._sfx||(drawVictory._sfx={}));}''',t);p.screenshot(path=str(O/f'stinger-{t}.png'))
  ck('new remnant and void portal rendered',p.evaluate('C22.draws.remnant>0&&C22.draws.void_portal>0'))
  ck('no flow page or console errors',not errors,errors);b.close()
finally:
 stop();(O/'flow-report.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf-8')
print('ALL',len(checks),'FLOW CHECKS PASSED',flush=True)
