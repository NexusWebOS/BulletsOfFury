"""Focused native Herald lightning regression; fixture selects attack, not HP."""
from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/herald_retina_1031/probe';W.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256
checks=[];errors=[]
def ck(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print('PASS'if value else'FAIL',name,json.dumps(data)[:800]if not value else'',flush=True)
 (W/'checks.json').write_text(json.dumps(checks,indent=2))
def step(p,n):
 for i in range(0,n,30):
  e=p.evaluate(STEP,min(30,n-i))
  if e:raise RuntimeError(e)
  p.wait_for_timeout(1)
def draws(p):
 return p.evaluate("""()=>{const get=XART.get,draw=ctx.drawImage,blit=hh52Blit,ground=groundTargetReticleDraw,field=combatWarningDraw;
 const images=new WeakMap(),cells=[],old=[],marks=[],fields=[];
 XART.get=function(k){const im=get.call(this,k);if(im&&typeof im==='object')images.set(im,k);return im;};
 ctx.drawImage=function(im,...a){const k=images.get(im);if(k===HL51_ART.key||k===HH101_ART.key)cells.push({key:k,args:a});return draw.call(this,im,...a);};
 hh52Blit=function(...a){old.push(a[0]);return blit.apply(this,a)};
 groundTargetReticleDraw=function(...a){marks.push(a);return ground.apply(this,a)};
 combatWarningDraw=function(...a){fields.push(a);return field.apply(this,a)};
 try{drawWorld(0)}finally{XART.get=get;ctx.drawImage=draw;hh52Blit=blit;groundTargetReticleDraw=ground;combatWarningDraw=field;}
 return{cells,old,marks,fields,pending:B._hd1003.er28?.bolts.filter(p=>!p.done).map(p=>({...p})),live:B._hd1003.er28?.bolts.filter(p=>p.done).map(p=>({...p}))};}""")
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
  bc=br.new_context(viewport={'width':1280,'height':800});p=boot(bc,port,8,errors)
  p.evaluate("()=>{beginStage(8);BOFCinematicDirector.cancel();story=null;diffKey='furious';debugStartFight({stage:8,role:'mini',kind:'heralddeath'},{pilot:'cole',record:false});spawnSubBoss('heralddeath');debugFight.spawned=true;subBossActive=true;warnT=0;DBGT.god=true;player.invuln=1e9;setState(GS.PLAY);window.B=subBoss;HH52.events=[];pBullets=[];eBullets=[];}")
  step(p,150)
  ck('Ground Retina and electric strip preload before attack',p.evaluate('XART.rdy(HH101_ART.key)&&XART.rdy(HL51_ART.key)'))
  ck('16 fixed even electric frames and pivot',p.evaluate('HH101_ART.frames===16&&HH101_ART.cw===128&&HH101_ART.ch===128&&HH101_ART.pivot.every(x=>x===64)'))
  p.evaluate("()=>{hr28Start(B,'rage');HH52.events=[];}");step(p,150+160)
  d=draws(p)
  ck('One ground Retina per committed pending lightning target',len(d['pending'])>0 and len([c for c in d['cells']if c['key']=='hl51_arrival_retina'])==len(d['pending']),d)
  ck('No filled impact discs, asterisks or duplicate broad warnings',not any(s=='star'or s.startswith('impact_')for s in d['old'])and not d['marks']and not d['fields'],d)
  ck('Ground Retinas use exact authored64x32 cells',all(c['args'][2:4]==[64,32]and c['args'][6:8]==[64,32]for c in d['cells']if c['key']=='hl51_arrival_retina'),d['cells'])
  p.screenshot(path=str(W/'ground-retinas.png'))
  old=p.evaluate('B._hd1003.er28.bolts.map(p=>({x:p.x,y:p.y,at:p.at,id:p.id}))');p.evaluate('player.x-=90');step(p,35)
  ck('Committed Retinas stay fixed when player moves',p.evaluate('(old)=>old.every(o=>{const p=B._hd1003.er28.bolts.find(p=>p.id===o.id);return!p||p.x===o.x&&p.y===o.y&&p.at===o.at;})',old))
  colours=set();frames=set();captured=False
  for i in range(245):
   step(p,1);d=draws(p)
   for c in d['cells']:
    if c['key']=='hl51_arrival_retina':colours.add(c['args'][1]//32)
    else:frames.add(c['args'][1]//128*4+c['args'][0]//128)
   if not captured and any(.10<q['age']<.17 for q in d['live']):
    p.screenshot(path=str(W/'red-electric-impact.png'));captured=True
  ck('Retina keeps green/yellow/red reaction phases',colours=={0,1,2},sorted(colours))
  ck('Native strike displays all16 authored electric frames',frames==set(range(16)),sorted(frames))
  ck('Actual impact screenshot captured',captured)
  p.wait_for_timeout(350)
  audio=p.evaluate("()=>({impact:Snd.pools.element_lightning_hit?.slots.map(s=>({attached:s.attached,ready:s.el.readyState,duration:s.el.duration,error:!!s.el.error})),bolt:Snd.pools.geyserLightning?.slots.map(s=>({attached:s.attached,ready:s.el.readyState,duration:s.el.duration,error:!!s.el.error}))})")
  ck('Electric impact and lightning decode through shared mixer',all(any(s['attached']and s['ready']>=2 and s['duration']>0 and not s['error']for s in audio[k]or[])for k in ['impact','bolt']),audio)
  rounds=p.evaluate('eBullets.filter(q=>q._hh52Lightning&&!q.dead).map(q=>({proof:!enemyOrdnanceCanIntercept(q)}))')
  ck('Native red energy remains ordinary unshootable ordnance',len(rounds)>0 and all(q['proof']for q in rounds),rounds[:6])
  step(p,800)
  events=p.evaluate('HH52.events');strikes=[e for e in events if e['event']=='lightning-strike'];tells=[e for e in events if e['event']=='lightning-tell']
  ck('All lightning impacts retain full two-second warning',len(strikes)>8 and all(2-1e-7<=e['delay']<2.035 for e in strikes),strikes)
  ck('Warning cadence accelerates without shortening reaction time',len(tells)>8 and tells[1]['time']-tells[0]['time']>2*(tells[-1]['time']-tells[-2]['time']))
  ck('Native attack recovers and removes all impact visuals',p.evaluate('!hh52Special(B)||hh52Special(B).kind!=="rage"'))
  p.evaluate("()=>{hr28Start(B,'nuke');B.x=camLeftX()+viewW()/2;B.y=viewTopY()+155}");step(p,35)
  pix=p.evaluate("""()=>{drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data,part=hd1003Part(B,'gunR'),hp=part.hp;hd1003Hit(B,10,0,0,'gunR');drawWorld(0);const d=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<d.length;i+=4)if(d[i]>240&&d[i+1]>240&&d[i+2]>240&&a[i]+a[i+1]+a[i+2]<650)white++;return{white,hp:part.hp,before:hp,flash:part.flash}}""")
  ck('Native damaged hull pixels and hit flash remain visible',pix['white']>4 and pix['hp']<pix['before']and pix['flash']>0,pix);step(p,20)
  ck('Native part hit flash expires',p.evaluate("hd1003Part(B,'gunR').flash===0"))
  ck('No page, console or asset errors',not errors,errors)
  (W/'events.json').write_text(json.dumps(events,indent=2));br.close()
finally:stop()
print('RESULT',sum(q['passed']for q in checks),'/',len(checks),flush=True)
if any(not q['passed']for q in checks):raise SystemExit(1)
