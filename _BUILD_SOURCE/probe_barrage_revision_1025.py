"""Real Chromium; observation plus explicitly labelled native-damage fixtures."""
from barrage_review_common_1025 import ROOT,OUT,boot,advance
from shoot import serve,STEP
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import json,base64,time

folder=OUT/'probe';folder.mkdir(exist_ok=True)
checks=[];errors=[];shots=[];details={}
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS 'if ok else'FAIL ')+name+(' '+json.dumps(data)if not ok else''),flush=True)
def shot(p,name):
 p.evaluate('drawWorld(0)');f=folder/(name+'.png');p.screenshot(path=str(f));shots.append((f,name))
def pixels(p,code):
 return p.evaluate("""code=>{drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data;eval(code);drawWorld(0);const d=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0,changed=0;for(let i=0;i<d.length;i+=4){if(d[i]!==a[i]||d[i+1]!==a[i+1]||d[i+2]!==a[i+2])changed++;if(d[i]>240&&d[i+1]>240&&d[i+2]>240&&a[i]+a[i+1]+a[i+2]<650)white++;}return{white,changed};}""",code)
port,stop=serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);bc=browser.new_context(viewport={'width':1280,'height':800})
  p=boot(bc,port,3,errors)
  ck('Stage3 reaches a native frost barrage',advance(p,'!!reviewActor._bh25',250))
  p.evaluate('HB25.dim=0');shot(p,'stage3-before')
  p.evaluate('HB25.dim=.46');shot(p,'stage3-after')
  contrast=p.evaluate("""()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);function lum(dim){HB25.dim=dim;drawBG(0);const d=ctx.getImageData(20,100,400,340).data;let l=0;for(let i=0;i<d.length;i+=4)l+=d[i]*.2126+d[i+1]*.7152+d[i+2]*.0722;return l/(d.length/4);}const old=lum(0),now=lum(.46);ctx.restore();return{old,now,ratio:now/old};}""")
  ck('Stage3 scenery luminance drops while retaining authored detail',.48<contrast['ratio']<.62,contrast)
  pp=p.evaluate("""()=>{const q={kind:'mg',x:200,y:300,vx:0,vy:2,mg:true,_coldTracer1002:true};function sample(dim){HB25.dim=dim;ctx.clearRect(0,0,cv.width,cv.height);drawCombatFinalProjectile(q);drawFireType(q);return [...ctx.getImageData(170,260,60,80).data];}return JSON.stringify(sample(0))===JSON.stringify(sample(.46));}""")
  ck('Stage3 lighting does not recolour native projectile pixels',pp)
  details['stage3']=contrast;p.close()

  p=boot(bc,port,6,errors)
  ck('Stage6 carrier completes its protected arrival',advance(p,"reviewActor._cargo13.ready&&reviewActor._cargo13.mode==='batteries'",700))
  d=p.evaluate("({sequences:reviewActor._cargo13.sequence,hp:reviewActor.hp,bar:BH25.events.filter(e=>e.event==='section-start').length,ports:bh25Ports(reviewActor,'fortress')})")
  ck('Stage6 live battery guns retain native sequences without bullet hell',d['sequences']>=1 and d['bar']==0,d)
  ck('Protected Stage6 reactor has no barrage emitter',not d['ports'])
  shot(p,'stage6-native-batteries')
  # The native Stage6 wing destroys the batteries while the player withholds fire.
  ck('Exposed Stage6 core reaches its own barrage between battery turns',advance(p,'!!reviewActor._bh25',450))
  ck('All six native battery breaks expose the Stage6 core',p.evaluate('sc13Open(reviewActor)&&reviewActor._cargo13.guns.every(g=>g.dead)'))
  ports=p.evaluate("bh25Ports(reviewActor)");ck('Every Stage6 barrage port is the visible reactor',len(ports)==1 and ports[0]['id']=='core',ports)
  advance(p,'eBullets.some(q=>q._bh25Owner===reviewActor&&!q.dead)',40,5);shot(p,'stage6-core-barrage')
  round=p.evaluate("()=>{const q=eBullets.find(q=>q._bh25Owner===reviewActor&&!q.dead),m=sc13Core(reviewActor);return{part:q?._bh25Part,proof:q?!enemyOrdnanceCanIntercept(q):false};}")
  ck('Stage6 core rounds remain ordinary unshootable energy',round['part']=='core'and round['proof'],round)
  ck('Stage6 core barrage completes and native carrier combat resumes',advance(p,"BH25.events.some(e=>e.event==='section-complete')",120))
  details['stage6']=p.evaluate('({events:BH25.events,guns:reviewActor._cargo13.guns,core:reviewActor._cargo13.core})');p.close()

  p=boot(bc,port,7,errors)
  ck('Dredger reaches its first barrage through native decisions',advance(p,"reviewActor._bh25?.kind==='dredger'",350))
  ck('Dredger starts with actual turret barrels',p.evaluate("!reviewActor._bh25.dorsal&&bh25Ports(reviewActor).every(p=>p.id.startsWith('gun'))"))
  bank=p.evaluate("()=>{const c=s7mCell('tank',1,true);return c.toDataURL().split(',')[1];}");(folder/'dredger-native-gun.png').write_bytes(base64.b64decode(bank))
  births=[];seen=set();peak=0
  for i in range(350):
   p.evaluate(STEP,3)
   q=p.evaluate("""()=>({events:BH25.events.slice(-50),phase:reviewActor._bh25?.phase,dorsal:reviewActor._bh25?.dorsal,wave:reviewActor._bh25?.wave,live:eBullets.filter(q=>q._bh25Owner===reviewActor&&!q.dead).length,flash:_navalFlashes.filter(f=>f.owner===reviewActor||f.fam==='weapon_muzzle_toxic').length})""")
   peak=max(peak,q['live'])
   key=('dorsal-'if q.get('dorsal')else'guns-')+str(q.get('wave'))
   if key not in seen and q.get('wave')in[1,3,5]:seen.add(key);shot(p,'dredger-'+key)
   if not p.evaluate('!!reviewActor._bh25'):break
   if i%12==0:p.wait_for_timeout(1)
  ck('Dredger turret barrage releases from both native gun modules',p.evaluate("['gunL','gunR'].every(id=>BH25.events.some(e=>e.event==='round'&&e.part===id))"))
  ck('Dredger turret barrage stays within 128 rounds',0<peak<=128,peak)
  q=pixels(p,"s7mHit(reviewActor,1,undefined,undefined,'gunL')");ck('Dredger native gun damage still flashes actual pixels',q['white']>5,q);shot(p,'dredger-hit')
  p.evaluate(STEP,20);ck('Dredger gun flash expires natively',p.evaluate("reviewActor._s7mod.parts.find(p=>p.id==='gunL').flash<=0"))
  ck('Dredger naturally alternates into a top-opening sludge barrage',advance(p,'!!reviewActor._bh25?.dorsal',450))
  peak=0;lobseen=set()
  for i in range(280):
   p.evaluate(STEP,3)
   q=p.evaluate("({phase:reviewActor._bh25?.phase,wave:reviewActor._bh25?.wave,live:eBullets.filter(q=>q._bh25Owner===reviewActor&&!q.dead).length,lob:reviewActor._bh25?.lob?.phase})");peak=max(peak,q['live'])
   key=str(q.get('lob'))+'-'+str(q.get('wave'))
   if key not in lobseen and q.get('wave')in[0,1,2]:lobseen.add(key);shot(p,'dredger-lob-'+key)
   if p.evaluate("BH25.events.filter(e=>e.event==='section-complete').length>=2"):break
   if i%12==0:p.wait_for_timeout(1)
  ck('Top sludge visibly releases, arcs and splashes into outward rounds',p.evaluate("BH25.events.some(e=>e.event==='dorsal-release')&&BH25.events.some(e=>e.event==='dorsal-splash')"))
  ck('Top sludge barrage is finite and has a bounded projectile budget',p.evaluate("BH25.events.filter(e=>e.event==='section-complete').length>=2")and 0<peak<=128,peak)
  details['dredger']=p.evaluate('BH25.events');p.close()

  p=boot(bc,port,8,errors)
  ck('Herald opens with a native red chaos barrage',advance(p,"reviewActor._bh25?.kind==='herald'",100))
  ck('Herald barrage launchers are surviving claws',p.evaluate("bh25Ports(reviewActor).every(p=>p.id.startsWith('gun'))"))
  advance(p,"eBullets.some(q=>q._hb25Chaos&&!q.dead)",40,4);shot(p,'herald-red-barrage')
  d=p.evaluate("()=>{const qs=eBullets.filter(q=>q._heraldOwner1003===reviewActor&&!q.dead);return{n:qs.length,round:qs.every(q=>q.w===q.h&&q._hb25Chaos&&!q._hp22Feather),proof:qs.every(q=>!enemyOrdnanceCanIntercept(q)&&!q._shootable&&!enemyDefensiveProof(q))};}")
  ck('Herald rounds are round red chaos art instead of thin feathers',d['n']>0 and d['round'],d)
  ck('Herald chaos rounds preserve offensive and defensive cancellation rules',d['proof'])
  observed=set();peak=0
  for i in range(900):
   p.evaluate(STEP,3)
   d=p.evaluate("()=>{const Q=reviewActor._hd1003._hb25;return{kind:Q?.kind,phase:Q?.phase,pass:Q?.pass,scale:Q?.scale,angle:Q?.angle,x:reviewActor.x,y:reviewActor.y,pending:!!Q?.pending,bombs:eBullets.filter(q=>q._hb25Bomb&&!q.dead).length,live:eBullets.filter(q=>q._hb25Chaos&&!q.dead).length};}")
   peak=max(peak,d['live']);key=str(d.get('kind'))+'-'+str(d.get('phase'))+'-'+str(d.get('pass'))
   if key not in observed and d.get('kind'):
    if d['phase']!='strike'or d['x']>p.evaluate('camLeftX()+viewW()*.35')and d['x']<p.evaluate('camLeftX()+viewW()*.65'):
     observed.add(key);shot(p,'herald-'+key)
   if d.get('pending')and 'pending'not in observed:observed.add('pending');shot(p,'herald-claw-warning')
   if d.get('bombs')and 'bomb'not in observed:observed.add('bomb');shot(p,'herald-claw-bomb')
   if p.evaluate("HB25.events.some(e=>e.event==='flight-complete'&&e.kind==='bomber')"):break
   if i%12==0:p.wait_for_timeout(1)
  ev=p.evaluate('HB25.events');details['herald']=ev
  ck('Herald performs warned corner swoops and visible returns',any(e['event']=='flight-complete'and e.get('kind')=='swoop'for e in ev))
  ck('Herald completes two bomber passes on Furious',any(e['event']=='flight-complete'and e.get('kind')=='bomber'and e.get('passes')==2 for e in ev))
  ck('Herald drops energy bombs from both living claws with matching muzzle flashes',all(any(e['event']=='bomb-drop'and e.get('id')==id for e in ev)and any(e['event']=='claw-flash'and e.get('id')==id for e in ev)for id in ['gunL','gunR']))
  ck('Herald bomb drops burst into visible chaos with a committed gap',any(e['event']=='bomb-burst'and e.get('half',0)>=.32 for e in ev))
  ck('Herald chaos projectile count remains bounded',0<peak<=128,peak)
  # Explicit native-hit fixture during an authored flight.
  p.evaluate("hb25Flight(reviewActor,'bomber')");advance(p,"reviewActor._hd1003._hb25?.phase==='strike'",120,3);p.evaluate(STEP,60)
  q=pixels(p,"hd1003Hit(reviewActor,1,0,0,'gunL')");ck('Herald moving claws visibly flash when hit',q['white']>4,q);shot(p,'herald-flight-hit')
  p.evaluate(STEP,20);ck('Herald part hit flash expires during flight',p.evaluate("hd1003Part(reviewActor,'gunL').flash<=0"))
  p.evaluate("hd1003Hit(reviewActor,hd1003Part(reviewActor,'gunL').hp+2,0,0,'gunL')")
  ck('Destroyed Herald claw stops exposing its barrage or bomb launcher',p.evaluate("!hb25Claws(reviewActor).includes('gunL')&&!bh25Ports(reviewActor,'herald').some(p=>p.id==='gunL')"))
  p.evaluate(STEP,10);ck('Destroyed claw cancels its pending shots and falling bombs',p.evaluate("eBullets.filter(q=>q._hb25Chaos&&!q.dead).every(q=>q._heraldPart1003!=='gunL')"))
  shot(p,'herald-one-claw');p.close();browser.close()
finally:stop()
ck('Native browser reports no page or console errors',not errors,errors)
(folder/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors,details=details),indent=2),encoding='utf8')
if shots:
 contact=Image.new('RGB',(1280,((len(shots)+3)//4)*218),(5,10,17));g=ImageDraw.Draw(contact)
 for i,(f,label)in enumerate(shots):contact.paste(Image.open(f).convert('RGB').resize((320,200)),((i%4)*320,(i//4)*218));g.text(((i%4)*320+3,(i//4)*218+201),label,fill='white')
 contact.save(folder/'contact.jpg')
print(json.dumps({'passed':sum(x['passed']for x in checks),'failed':sum(not x['passed']for x in checks),'errors':errors}),flush=True)
raise SystemExit(0 if all(x['passed']for x in checks)and not errors else 1)
