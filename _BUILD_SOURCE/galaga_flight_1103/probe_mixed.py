import json,base64
from playwright.sync_api import sync_playwright
from native_flight import *
errors=[];results=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disk-cache-size=1','--media-cache-size=1'])
 p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));boot(p);setup(p)
 for kind in ['small','medium','large','mixed']:
  setup(p);units=spawn(p,kind)
  p.evaluate('()=>{window.MQ={trace:[],maxStep:0,nonfinite:false,closest:1,closeSeconds:0,overlapPeak:0,shots:0};for(const e of fleet)e._qaPrevious={x:e.x,y:e.y};}')
  for batch in range(68):
   data=p.evaluate('''()=>{for(let f=0;f<30;f++){stateT+=1/60;updatePlay(1/60);let close=0;const live=fleet.filter(e=>!e.dead&&e.y>viewTopY()+20&&e.y<VH-30);for(const e of fleet){const jump=Math.hypot(e.x-e._qaPrevious.x,e.y-e._qaPrevious.y);if(!e.dead&&jump>MQ.maxStep){MQ.maxStep=jump;MQ.maxEvent={id:e._gf113.id,type:e.type,age:e._gf113.age,phase:e._gf113.phase,native:gf113State(e)?.phase,before:e._qaPrevious,after:{x:e.x,y:e.y},desired:e._gf113.desired,paused:e._gf113.paused};}MQ.nonfinite||=!Number.isFinite(e.x+e.y+gf113Head(e));e._qaPrevious={x:e.x,y:e.y};}for(let i=0;i<live.length;i++)for(let j=0;j<i;j++){const a=live[i],b=live[j],v=Math.max(Math.abs(a.x-b.x)/((a.w+b.w)*.5),Math.abs(a.y-b.y)/((a.h+b.h)*.5));MQ.closest=Math.min(MQ.closest,v);if(v<.35)close++;}MQ.closeSeconds+=close/60;MQ.overlapPeak=Math.max(MQ.overlapPeak,close);MQ.shots=Math.max(MQ.shots,eBullets.length);}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);MQ.trace.push(fleet.map(e=>({id:e._gf113.id,x:e.x,y:e.y,phase:e._gf113.phase,dead:e.dead,held:e._gf113.held})));return fleet.every(e=>e.dead);}''')
   if batch in [10,18,26]:
    (W/f'mixed-{kind}-{batch}.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
   if data:break
  result=p.evaluate('()=>({...MQ,departed:fleet.every(e=>e.dead),units:fleet.map(e=>({id:e._gf113.id,type:e.type,hp:e.hp,phase:e._gf113.phase,age:e._gf113.age,events:GF113.events.filter(q=>q.id===e._gf113.id)}))})')
  result.update(kind=kind,spawn=units);results.append(result);print(kind,{k:result[k]for k in ['maxStep','nonfinite','closest','closeSeconds','overlapPeak','shots','departed']},flush=True)
 b.close()
(W/'mixed-checks.json').write_text(json.dumps({'cases':results,'errors':errors},indent=2),encoding='utf8')
assert not errors and all(q['departed']and not q['nonfinite']for q in results)
