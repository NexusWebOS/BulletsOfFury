"""Real Chromium: Warden gun pixels, player fire, tank hull clearance and roadside density."""
from pathlib import Path
import ast,json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage4_engine_1018/native';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof WC18!=="undefined"');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.pilot='cole';startRun(4)")
  p.evaluate('''()=>{window.wc18DrawKeys={};window.wc18DrawKey=null;const cell=mr27Cell,draw=ctx.drawImage;
   mr27Cell=function(s,c){const out=cell.apply(this,arguments);wc18DrawKey=s==='iron'&&c>=100?'wc18_gun_'+String(c-100).padStart(2,'0'):null;return out;};
   ctx.drawImage=function(){if(wc18DrawKey)wc18DrawKeys[wc18DrawKey]=(wc18DrawKeys[wc18DrawKey]||0)+1;return draw.apply(this,arguments);};
   window.nativePixels=fn=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();const d=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return d;};
   window.changedPixels=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(a[i+3]>100&&Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>20)n++;return n;};
   window.trafficAudit=()=>{const es=enemies.filter(groundTrafficVehicle),pairs=[];for(let i=0;i<es.length;i++)for(let j=i+1;j<es.length;j++)if(groundTrafficTouch(es[i],es[j]))pairs.push([es[i]._traffic18,es[j]._traffic18]);
    return{count:es.length,pairs,visible:es.filter(e=>e.y>viewTopY()&&e.y<VH).map(e=>({x:e.x,y:e.y,legal:groundTrafficLegal(e,e.x,e.y),foot:groundTrafficFootprint(e)})),stats:{...GT18.stats}};};}''')
  def frames(n,extra=''):
   for i in range(0,n,12):
    err=p.evaluate(shoot.STEP,min(12,n-i))
    if err:errors.append(err)
    if extra:p.evaluate(extra)
    p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}');p.screenshot(path=str(O/(name+'.png')))
  def setup(diff='normal',mini=False,stage=4):
   p.keyboard.up('j');p.evaluate(SETUP,dict(stage=stage,pilot='cole',diff=diff,**(dict(kind='olivewarden',mini=True) if mini else {})))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&wc18Ready()&&bmfReady("game")}',polling=50)
   p.evaluate('''()=>{BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=s6Opening=null;AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;warnT=0;warnKind=null;
    VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;stagePlan=[];subBossTriggered=aminiTriggered=true;stageEnding=0;bossDefeated=false;Input.keys={};Input.mouse.down=false;
    run.spaceMode=false;run.shield=0;run.sonicT=run.dkT=0;special=thunderStorm=null;chaingunUnlocked=false;run._earnedUnlocks={...(run._earnedUnlocks||{}),chaingun:false};weaponFormSelect(7,{kind:'primary1003b',id:'mg'});
    run.weapon=0;run.wlevel=run.wlevels[0]=0;run.wvars[0]=null;run.forge={};run.forgeForms={};run.infusion=null;run.loadout=[0];player.fireCd=0;player.x=worldWidth()/2;player.y=VH-60;player.invuln=0;playerHit=()=>{};powerups=[];
    if(subBoss){subBoss._be=null;subBoss.enter=subBoss._noHit=false;subBoss._phaseInvuln=0;subBoss.x=worldWidth()/2;subBoss.y=subBoss._er26.home;subBoss._drawY=subBoss.y;mr27Init(subBoss);}
    camX=clamp(player.x-VW/2,0,worldWidth()-VW);SC12.refresh();__bofFit();}''');frames(1)
  setup('normal',True);frames(210)
  p.evaluate("()=>{window.trace18=[];const damage=mr27Damage;mr27Damage=function(b,d,x,y){const before=mr27Part(b,'gunC')?.hp,r=damage.apply(this,arguments);trace18.push({dmg:d,x,y,id:b._ship,hull:b.hp,before,after:mr27Part(b,'gunC')?.hp,bullet:_dmgBullet?.kind});return r;};}")
  def info():return p.evaluate("()=>({hull:B.hp,mini:B===subBoss,kind:B.kind,ship:B._ship,gun:mr27Part(B,'gunC'),bullets:pBullets.map(q=>({kind:q.kind,x:q.x,y:q.y})),e:eBullets.length,source:B._er26Source,proof:B._weaponProof,trace:trace18.slice(-6)})")
  print('before',json.dumps(info()),flush=True)
  p.evaluate("()=>{eBullets=[];pBullets=[];er26Set(B,'recover');const m=mr27Shape(B,'gunC');player.x=m.x;player.y=m.y+160;player.fireCd=0;}")
  p.keyboard.down('j')
  for i in range(6):
   frames(10);print(i,json.dumps(info()),flush=True)
  p.keyboard.up('j');snap('debug-gun')
  br.close()
finally:stop()
