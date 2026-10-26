from pathlib import Path
import json,base64
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage59_1024/portal';O.mkdir(exist_ok=True);checks=[];errors=[]
def ck(n,ok,data=None):checks.append(dict(name=n,passed=bool(ok),data=data));print(('PASS 'if ok else'FAIL ')+n+(' '+json.dumps(data)if not ok else''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:300])if m.type=='error'else None);p.goto(f'http://127.0.0.1:{port}/index.html?debug=1');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{diffKey='furious';debugStartFight({stage:9,role:'mini',kind:'voidhorizon',name:'Horizon'},{pilot:'maverick'});spawnSubBoss__inner('voidhorizon');debugFight.spawned=true;window.B=subBoss;DBGT.god=true;BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=s6Opening=null;for(const cue of ['enemyElectricBolt','combatOrb0927'])Snd.prepare(cue);}''')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(9)&&s5924Keys().every(k=>XART.rdy(k))}')
  row=p.evaluate('''()=>{let count=0,changed=0;const blank=document.createElement('canvas');blank.width=blank.height=320;const native=ctx.drawImage;for(const[n,B]of Object.entries(S5924_ART.banks)){let last=-1;for(const a of B.frames){ctx.clearRect(0,0,320,320);ctx.drawImage(XART.get(a.key),0,0,256,256);const d=ctx.getImageData(0,0,256,256).data;let sum=0;for(let i=0;i<d.length;i+=4)sum+=d[i]+d[i+1]+d[i+2];if(last>=0&&sum!==last)changed++;last=sum;count++;}}return{count,changed}}''')
  ck('All60 authored cells render through native drawImage and animate',row['count']==60 and row['changed']>40,row)
  # Native sound assignment, mixer and decoded media playback, independent of
  # player weapon. One audible call per volley; silent partners stay silent.
  p.wait_for_function('()=>["enemyElectricBolt","combatOrb0927"].every(k=>Snd.pools[k]?.list.every(a=>a.readyState>=3))')
  p.evaluate('''async()=>{Snd.vol.master=1;Snd.vol.sfx=.4;window.audio59={playing:[],calls:[]};window.audio59ctx=new AudioContext();await audio59ctx.resume();window.audio59ans=[];for(const k of ['enemyElectricBolt','combatOrb0927'])for(const a of Snd.pools[k].list){const src=audio59ctx.createMediaElementSource(a),an=audio59ctx.createAnalyser();an.fftSize=1024;src.connect(an);an.connect(audio59ctx.destination);audio59ans.push(an);a.addEventListener('playing',()=>audio59.playing.push({cue:k,ready:a.readyState,volume:a.volume}));}window.audio59peak=0;window.audio59timer=setInterval(()=>{for(const an of audio59ans){const data=new Float32Array(an.fftSize);an.getFloatTimeDomainData(data);for(const v of data)audio59peak=Math.max(audio59peak,Math.abs(v));}},10);const play=Snd.play;Snd.play=function(k,...args){const accepted=play.call(this,k,...args);if(['enemyElectricBolt','combatOrb0927'].includes(k))audio59.calls.push({cue:k,accepted});return accepted;};B.enter=false;B._s9rift.core.x=B.x=worldWidth()/2;B._s9rift.core.y=B.y=150;s5924Set(B,'aimed');B._s9rift.s5924.t=B._s9rift.s5924.warm;s9VoidHorizonTick(B,1/60);}''')
  p.wait_for_timeout(650)
  p.evaluate("()=>{s5924Set(B,'spin');B._s9rift.s5924.t=B._s9rift.s5924.warm;s9VoidHorizonTick(B,1/60);}")
  p.wait_for_timeout(650);row=p.evaluate('()=>({playing:audio59.playing,calls:audio59.calls,peak:audio59peak,context:audio59ctx.state})')
  ck('Native eye volleys play decoded approved mixer audio',len({x['cue'] for x in row['playing']})==2 and row['peak']>0 and row['context']=='running',row)
  ck('Silent volley partners do not stack gun reports',len(row['playing'])==2 and len({q['cue']for q in row['playing']})==2,row)
  p.evaluate('''()=>{clearInterval(audio59timer);debugFight=null;subBoss=null;subBossActive=false;boss=null;bossActive=false;setState(GS.PLAY);run._s9gate={x:player.x,y:player.y-100};s9WarpStart();window.warp59Samples=[];}''')
  for frame in range(380):
   row=p.evaluate('''()=>{if(s9warp){s9WarpTick(1/60);s9WarpDraw();}return{warp:!!s9warp,phase:s9warp?.ph,age:s9warp?._s5924Age,state};}''')
   if frame in [85,120,170]:p.screenshot(path=str(O/f'warp-{frame}.png'))
   if frame==120:
    pixels=p.evaluate('''()=>{const d=ctx.getImageData(0,0,cv.width,cv.height).data,w=cv.width,h=cv.height;let bright=0;for(const[x,y]of [[1,1],[w-2,1],[1,h-2],[w-2,h-2],[w/2,h/2]]){const i=(Math.floor(y)*w+Math.floor(x))*4;if(d[i]+d[i+1]+d[i+2]>70)bright++;}return{bright,width:w,height:h,phase:s9warp?.ph,age:s9warp?._s5924Age}}''')
    overlay=p.evaluate('''()=>{const c=S5924.overlay,r=document.querySelector('#room').getBoundingClientRect(),q=c?.getBoundingClientRect();return{visible:!!c&&getComputedStyle(c).display!=='none',w:q?.width,h:q?.height,rw:r.width,rh:r.height}}''')
    ck('Animated water covers all viewport corners during travel',pixels['bright']==5 and (pixels['age']or 0)>.5 and overlay['visible'] and abs(overlay['w']-overlay['rw'])<2 and abs(overlay['h']-overlay['rh'])<2,dict(pixels=pixels,overlay=overlay))
   if not row['warp']:
    ck('Native portal completes protected travel and map handoff',row['state']=='stagesel' and frame>=300 and p.evaluate('!S5924.overlay||S5924.overlay.style.display==="none"'),row);break
  else:ck('Native portal completes protected travel and map handoff',False,row)
  ck('No page/console errors',not errors,errors);br.close()
finally:stop()
out=dict(passed=sum(q['passed']for q in checks),failed=sum(not q['passed']for q in checks),checks=checks,errors=errors);(O/'report.json').write_text(json.dumps(out,indent=2)+'\n');print('SUMMARY',out['passed'],out['failed']);raise SystemExit(bool(out['failed']))
