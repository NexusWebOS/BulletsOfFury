"""Native pixels and lifecycle fixtures for the new launch sockets and red bank."""
from barrage_review_common_1025 import ROOT,OUT,boot,advance
from shoot import serve,STEP
from playwright.sync_api import sync_playwright
import json

checks=[];errors=[];folder=OUT/'sockets';folder.mkdir(exist_ok=True)
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));print(('PASS 'if v else'FAIL ')+n+(' '+json.dumps(d)if not v else''),flush=True)
port,stop=serve(str(ROOT))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);bc=b.new_context(viewport={'width':1280,'height':800})
  p=boot(bc,port,7,errors);advance(p,'!!reviewActor._bh25',250)
  d=p.evaluate("""()=>{const c=s7mCell('tank',1,true),g=c.getContext('2d'),holes=[-.371,-.276,.270,.361].map(x=>[...g.getImageData(Math.round((x+.5)*c.width),Math.round(.95*c.height),1,1).data]);const v=s7mCell('tank',2,true),green=[...v.getContext('2d').getImageData(Math.floor(v.width*.5),Math.floor(v.height*.185),1,1).data];return{holes,green};}""")
  ck('All four measured Dredger barrel mouths land on opaque dark apertures',all(v[3]>200 and max(v[:3])<140 for v in d['holes']),d['holes'])
  ck('Dredger dorsal source lands on the authored green liquid opening',d['green'][1]>d['green'][0]*1.5 and d['green'][1]>d['green'][2]*1.5,d['green'])
  d=p.evaluate("""()=>{const port=bh25Ports(reviewActor)[0];bh25Flash(reviewActor,port,Math.PI/2);const f=_navalFlashes.at(-1),saved=_navalFlashes;_navalFlashes=[];drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data;_navalFlashes=saved;f.t=.06;drawWorld(0);const z=ctx.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<z.length;i+=4)if(z[i]!==a[i]||z[i+1]!==a[i+1]||z[i+2]!==a[i+2])n++;return{changed:n,angle:f.angle,port:port.a,at:f.follow(),barrel:port.barrel};}""")
  ck('Dredger toxic muzzle flash visibly renders on its barrel',d['changed']>5,d)
  ck('Dredger flash points along the barrel and stays on its selected aperture',abs(d['angle']-d['port'])<1e-6 and d['at']['barrel']==d['barrel'],d)
  p.screenshot(path=str(folder/'dredger-native-muzzle.png'))
  p.evaluate("()=>{bh25Cancel(reviewActor,'fixture');s7mSet(reviewActor,'bh25');reviewActor._bh25DredgerTurns=1;bh25Start(reviewActor,'dredger',()=>s7mSet(reviewActor,'recover'));}")
  ck('Dorsal shell owns a native warned and arcing lob',p.evaluate("reviewActor._bh25.lob.mode==='lob'&&reviewActor._bh25.lob.warm>=1.18&&reviewActor._bh25.lob.arc>100"))
  p.evaluate("()=>{window.cancelShell=reviewActor._bh25.lob;bh25Cancel(reviewActor,'fixture-cancel');}")
  ck('Cancelling the Dredger attack cancels its pending dorsal shell',p.evaluate('cancelShell.dead&&!reviewActor._bh25'))
  p.close()
  p=boot(bc,port,8,errors);advance(p,'!!reviewActor._bh25',120)
  d=p.evaluate("""()=>{const id=hb25Claws(reviewActor)[0],m=hd1003Muzzle(reviewActor,id),q=hb25Shot(reviewActor,id,m,Math.PI/2,2.4);const born={offense:enemyOrdnanceCanIntercept(q),defense:enemyDefensiveProof(q),shootable:q._shootable,t:q.t};q.x=200;q.y=300;ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawCombatFinalProjectile(q);const d=ctx.getImageData(180,280,40,40).data;let red=0,white=0;for(let i=0;i<d.length;i+=4){if(d[i]>100&&d[i]>d[i+1]*1.5&&d[i]>d[i+2]*1.5)red++;if(d[i]>220&&d[i+1]>180&&d[i+2]>180)white++;}ctx.restore();q.dead=true;return{born,red,white};}""")
  ck('A new Herald chaos ball is unshootable before its first update',not d['born']['offense']and not d['born']['shootable']and not d['born']['defense'],d['born'])
  ck('Herald native projectile pixels are visibly red with a bright core',d['red']>40 and d['white']>2,d)
  d=p.evaluate("""()=>{const id=hb25Claws(reviewActor)[0];hb25Flash(reviewActor,id);const f=wm26Releases.at(-1),saved=wm26Releases;wm26Releases=[];drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data;wm26Releases=saved;f.age=.07;drawWorld(0);const z=ctx.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<z.length;i+=4)if(z[i]!==a[i]||z[i+1]!==a[i+1]||z[i+2]!==a[i+2])n++;return{changed:n,family:f.family,color:f.color};}""")
  ck('Herald uses a visible authored red energy muzzle flash',d['changed']>5 and d['family']=='void'and d['color']=='#ff303c',d)
  p.screenshot(path=str(folder/'herald-native-energy-flash.png'))
  d=p.evaluate("""()=>{const a=HB25_ART,im=XART.get(a.key),c=document.createElement('canvas');c.width=a.w;c.height=a.h;const g=c.getContext('2d');let same=true;for(let f=0;f<8;f++){g.clearRect(0,0,128,128);g.drawImage(im,...a.cells[f],0,0,128,128);if(c.width%2||c.height%2)same=false;}return{same,frames:a.frames,pivot:a.pivot,turn:hb25Turn(Math.PI*1.5,0,1)-Math.PI*1.5};}""")
  ck('Red chaos animation retains eight even fixed cells and the common pivot',d['same']and d['frames']==8 and d['pivot']==[64,64],d)
  ck('Herald return rotation takes the short arc',abs(d['turn'])<=3.1416/2+.001,d['turn'])
  # Native break fixture while a fall is pending; the real damage owner kills it.
  p.evaluate("()=>{const id='gunL',m=hd1003Muzzle(reviewActor,id);window.pendingChaos=hb25Shot(reviewActor,id,m,Math.PI/2,1,{at:efxClock+.5,target:{x:200,y:300},escapeX:250,rank:3,seed:0});hd1003Hit(reviewActor,hd1003Part(reviewActor,id).hp+10,0,0,id);}")
  p.evaluate(STEP,40)
  ck('A broken claw cannot finish its pending bomb burst',p.evaluate("!eBullets.some(q=>q._hb25Chaos&&!q.dead&&q._heraldPart1003==='gunL')"))
  d=p.evaluate("""async()=>{const a=Snd._audioCtx();await a.resume();const out=[];for(const key of ['bossfireSludgeemperor','combatToxic0927','bossfireVileexistence','combatOrb0927','jetDash','bossWeaponCharge']){const buf=await a.decodeAudioData(await(await fetch(BOFA.sfx[key])).arrayBuffer());let peak=0;for(const v of buf.getChannelData(0))peak=Math.max(peak,Math.abs(v));out.push({key,peak,duration:buf.duration});}return out;}""")
  ck('Every new launcher, burst and flight cue decodes to audible native audio',all(q['peak']>.01 and q['duration']>0 for q in d),d)
  p.close();b.close()
finally:stop()
ck('Socket and pixel fixtures have no browser errors',not errors,errors)
(folder/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf8')
print(json.dumps({'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks)}),flush=True)
raise SystemExit(0 if all(c['passed']for c in checks)and not errors else 1)
