from pathlib import Path
import ast,sys,json,base64,http.server
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/performance_finish_1020';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
CLEAR='''()=>{VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;spawnClock=999999;stagePlan=[];subBossTriggered=aminiTriggered=true;subBossDone=true;warnT=0;warnKind=null;bossWarned=false;bossDefeated=false;stageTimer=0;BOFCinematicDirector.cancel();AP10_X.intro=null;story=fb2Talk=fb2Intro=thaw=s6Opening=null;H3.release=false;H3.ending=null;P2M.active=null;run.shield=0;run.sonicT=run.dkT=0;special=thunderStorm=null;run._megaShield=false;player.fireCd=999999;Input.keys={};Input.mouse.down=false;powerups=[];eBullets=[];pBullets=[];}'''
checks=[];errors=[]
def ck(name,v,data=None):checks.append(dict(name=name,ok=bool(v),data=data));print(('PASS ' if v else 'FAIL ')+name,flush=True)
def shot(p,n):
 (O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('''()=>{const c=document.createElement('canvas');c.width=Math.round(VW*SS);c.height=Math.round(VH*SS);c.getContext('2d').drawImage(cv,0,0);return c.toDataURL().split(',')[1];}''')))
def report():
 (O/'verification.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf-8')
def setup(p,stage=1,kind=None,mini=False,diff='normal',pilot='cole'):
 p.evaluate(SETUP,dict(stage=stage,kind=kind,mini=mini,diff=diff,pilot=pilot));p.evaluate(CLEAR)
 p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}')
def steps(p,n,paint=True):
 for i in range(0,n,30):
  p.evaluate('''arg=>{for(let i=0;i<arg.n;i++){player.invuln=1e9;updatePlay(1/60);if(arg.paint&&i%6===0)ppPaint();}}''',dict(n=min(30,n-i),paint=paint));p.wait_for_timeout(2)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport=dict(width=1366,height=900));p.set_default_timeout(180000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400]) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof BOFPERFORMANCE!=="undefined"');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{BOFPERFORMANCE.warm();for(const k of victoryEndingKeys())XART.rdy(k);dr21Warm();window.PP={banks:{},blits:0};const get=XART.get,draw=ctx.drawImage,tags=new WeakMap();XART.get=function(k){const im=get.apply(this,arguments);if(im)tags.set(im,k);return im;};ctx.drawImage=function(im,...a){const k=tags.get(im);if(k?.startsWith('pf20_')&&a.length===8){const bank=Object.values(PF20_ART).find(b=>b.key===k);if(bank){const i=bank.cells.findIndex(c=>c[0]===a[0]&&c[1]===a[1]);(PP.banks[k]||(PP.banks[k]=new Set())).add(i);PP.blits++;}}return draw.call(this,im,...a);};window.ppPaint=()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);};window.ppClear=()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);ctx.fillStyle='#0b1420';ctx.fillRect(0,0,VW,VH);};window.ppPixels=()=>new Uint8ClampedArray(ctx.getImageData(0,0,cv.width,cv.height).data);window.ppDiff=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]||a[i+3]!==b[i+3])n++;return n;};}''')
  p.wait_for_function('()=>{BOFPERFORMANCE.warm();return BOFPERFORMANCE.ready&&dr21Warm()&&victoryEndingKeys().every(k=>XART.rdy(k));}')
  p.evaluate('''()=>{PP.all={};const get=XART.get,pal=xartPalette,tint=xartTint,draw=ctx.drawImage,tags=new WeakMap();for(const n of ['get','palette','tint']){const fn=n==='get'?get:n==='palette'?pal:tint;const owner=n==='get'?XART:window;const wrap=function(k){const im=fn.apply(this,arguments);if(im)tags.set(im,k);return im;};if(n==='get')XART.get=wrap;else if(n==='palette')xartPalette=wrap;else xartTint=wrap;}ctx.drawImage=function(im,...a){const k=tags.get(im),bank=Object.values(PF20_ART).find(b=>b.key===k);if(bank&&a.length===8){const i=bank.cells.findIndex(c=>c[0]===a[0]&&c[1]===a[1]);(PP.all[k]||(PP.all[k]=new Set())).add(i);(PP.banks[k]||(PP.banks[k]=new Set())).add(i);}return draw.call(this,im,...a);};}''')
  ck('All nine atlases and both cleaned full-body bases decode',p.evaluate('BOFPERFORMANCE.ready'))
  for diff in ['easy','normal','hard','furious']:
   for stage,kind,mini,bank in [(5,'siegebomber',True,'bomber_cannon'),(6,'siegefortress17',True,'carrier_turret'),(6,'warhive',False,'carrier_turret')]:
    setup(p,stage,kind,mini,diff);p.evaluate('PP.banks={};PP.blits=0;')
    if kind=='siegebomber':p.evaluate('siegeBomberSet(B,"charge")')
    steps(p,1800)
    out=p.evaluate('({blits:PP.blits,frames:Object.fromEntries(Object.entries(PP.banks).map(([k,v])=>[k,[...v].sort((a,b)=>a-b)])),dead:B.dead,x:B.x,y:B.y,parts:B._carrier17?.parts?.length||B._cargo13?.guns?.length||B._bomber?.parts?.length})')
    ck(diff+' '+kind+' real phase animations and finite actor',out['blits']>10 and len(out['frames'].get('pf20_'+bank,[]))>=8 and isinstance(out['x'],(float,int)),out)
    if diff=='normal':p.evaluate('ppPaint()');shot(p,'fight-'+kind)
    # Actual native damage path; compare the physical weapon pixels before/after and after timer expiry.
    out=p.evaluate('''kind=>{let draw,hit,expire,part;if(kind==='siegebomber'){part=B._bomber.parts.find(q=>q.id.startsWith('laser'));B._bomber.mode='recover';B._bomber.t=.5;part.flash=0;draw=()=>{PF20.bomber=B;const p=siegeBomberParts(B).find(q=>q.id===part.id);polishBlit('bomber',2,p.x,p.y,p.w,p.h,part.flash);PF20.bomber=null;};hit=()=>siegeBomberHit(B,1,NaN,NaN,part.id);expire=()=>part.flash=0;}
     else if(kind==='siegefortress17'){part=B._cargo13.guns.find(g=>!g.dead);B._cargo13.mode='batteries';B._cargo13.lasers=[];part.fl=part.flash=0;draw=()=>sc13GunDraw(B,part);hit=()=>{B._cargo13.directId=part.id;warhiveDamage(B,1);};expire=()=>{part.fl=part.flash=0;};}
     else{part=B._carrier17.parts.find(g=>g.kind==='laser'&&!g.dead);B._carrier17.depth=false;B._carrier17.phase='fight';part.phase='rest';part.t=1;part.flash=0;draw=()=>pf20TurretDraw(part,200,200,38,47.5,part.flash);hit=()=>{B._carrier17.hit=part.id;roster17Damage(B,1);};expire=()=>part.flash=0;}
     const paint=()=>{ppClear();draw();return ppPixels();};hit();const flash=part.flash||part.fl,b=paint();expire();const a=paint(),c=paint();return{changed:ppDiff(a,b),restored:ppDiff(a,c),flash,hp:part.hp};}''',kind)
    ck(diff+' '+kind+' damaged module visibly flashes and restores',out['changed']>10 and out['restored']==0 and out['flash']>0,out)
    report()
  # Full native player-hit classifications and actual victim sprites.
  for kind,source in [('laser',{'kind':'carrierLaser'}),('ice','cryo shard'),('dark','void abyss'),('shadow','Dracodia shadow eradication')]:
   setup(p);out=p.evaluate('''s=>{player.invuln=0;player.dead=false;player.roll=player.somer=null;run.shield=0;const lives=run.lives;playerHit(s);const D=player._dr21Death;return{kind:D?.kind,life:D?.life,dead:player.dead,lost:lives-run.lives};}''',source)
   ck(kind+' native hit creates contextual death',out.get('kind')==kind and out['dead'],out)
   if not out.get('kind'):continue
   for i,t in enumerate([.10,.35,.55,.8,1.05,1.3]):
    p.evaluate('t=>{player._dr21Death.t=t;ppClear();drawDeathSpin();}',t);shot(p,'death-'+kind+'-'+str(i))
   if kind!='laser':
    out=p.evaluate('''()=>{const D=player._dr21Death,p=pf20ShardMasks(D),src=D.image.getContext('2d').getImageData(0,0,192,192).data,out=new Uint16Array(src.length);for(const s of p){const a=s.im.getContext('2d').getImageData(0,0,192,192).data;for(let i=0;i<a.length;i++)out[i]+=a[i];}let bad=0,premul=0;for(let i=0;i<src.length;i+=4){if(src[i+3]!==out[i+3])bad++;for(let c=0;c<3;c++)premul=Math.max(premul,Math.abs(src[i+c]-out[i+c])*src[i+3]/255);}return{pieces:p.length,alphaMismatch:bad,premul};}''')
    ck(kind+' irregular fragments preserve victim coverage and color',out['pieces']>=8 and out['alphaMismatch']==0 and out['premul']<=1.1,out)
   out=p.evaluate('''()=>{const D=player._dr21Death;D.t=.45;D._pf20Cue=false;updateDeathSpin(.02);const cue=D._pf20Cue;updateDeathSpin(D.life);return{cue,ended:D.ended,t:D.t,life:D.life};}''')
   ck(kind+' finite terminal sequence and one transition cue',out['ended'] and out['cue'] and out['t']>=out['life'],out)
  for mode in ['shield','iframe','roll','somer']:
   setup(p);out=p.evaluate('''mode=>{player.invuln=mode==='iframe'?2:0;player.roll=player.somer=null;player._rollCool=player._somerCool=0;if(mode==='roll')startRoll(1);if(mode==='somer')startSomersault();run.shield=mode==='shield'?2:0;playerHit('laser beam');return{dead:player.dead,context:!!player._dr21Death};}''',mode)
   ck(mode+' preserves native hit protection',not out['dead'] and not out['context'],out)
  setup(p);out=p.evaluate('''()=>{player.invuln=0;run.shield=0;playerHit('ordinary bullet');return{dead:player.dead,context:!!player._dr21Death,spin:!!player._spin};}''')
  ck('Ordinary bullet death retains original spin owner',out['dead'] and not out['context'] and out['spin'],out)
  setup(p);p.evaluate('''()=>{setState(GS.VICTORY);run.pilot='cole';window.S={inv20:null};}''')
  for name,t in [('report',28.8),('alarm',40.4),('horror',58.8)]:
   p.evaluate('t=>{ctx.setTransform(SS,0,0,SS,0,0);inv20Draw(t,VW,VH,S);}',t);shot(p,'cinematic-'+name)
  frames=[]
  for horror in [False,True]:
   out=p.evaluate('''horror=>{const data=[];for(const t of [0,.5,.8,1.4,2.2,3.2,4.7]){ppClear();INV20.last={scene:horror?'alarm':'report'};INV20.active=true;const q=inv20Pose('cole',VW/2,VH-25,VH*.85,t,horror);const im=ppPixels();let hash=0;for(let i=0;i<im.length;i+=4)hash=(hash*33+im[i]+im[i+1]*3+im[i+2]*7)>>>0;data.push({t,q,hash,frame:PF20.cole});}return data;}''',horror)
   ck(('Horrified' if horror else 'Reporting')+' Cole uses distinct face/gesture frames on fixed full-body geometry',len(set(q['hash'] for q in out))>=5 and all(q['q'].get('performance') for q in out),out)
   for i in range(24):
    p.evaluate('''arg=>{ppClear();INV20.last={scene:arg.h?'alarm':'report'};INV20.active=true;inv20Pose('cole',VW/2,VH-20,VH*.88,arg.i/8,arg.h);}''',dict(h=horror,i=i));f=O/f'cole-{int(horror)}-{i:02}.png';shot(p,f.stem);frames.append(f)
   imgs=[Image.open(O/f'cole-{int(horror)}-{i:02}.png').convert('RGB') for i in range(24)];imgs[0].save(O/('cole-horror-native.gif' if horror else 'cole-report-native.gif'),save_all=True,append_images=imgs[1:],duration=125,loop=0)
  out=p.evaluate('''()=>{const rows=[];for(const k of CE20.pilots.filter(k=>k!=='cole')){ppClear();const q=inv20Pose(k,VW/2,VH-20,400,1,true);rows.push({key:k,performance:!!q?.performance,draw:q?.key});}return rows;}''')
  ck('Other eight pilot identities retain existing poses for likeness review',len(out)==8 and all(not q['performance'] for q in out),out)
  ck('Native renderer used all nine atlas banks',p.evaluate('Object.keys(PP.all).length===9'),p.evaluate('Object.fromEntries(Object.entries(PP.all).map(([k,v])=>[k,[...v]]))'))
  ck('No browser/page errors',not errors,errors);report();browser.close()
finally:stop()
print(json.dumps(dict(passed=sum(q['ok'] for q in checks),failed=sum(not q['ok'] for q in checks),errors=errors)),flush=True)
raise SystemExit(bool(errors) or any(not q['ok'] for q in checks))
