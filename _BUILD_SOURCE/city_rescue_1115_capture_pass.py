from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys,base64,math
R=Path(__file__).resolve().parents[1];O=R/'_shots/city_rescue_1115';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(240000)
 errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8765/index.html?city16-pass');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.evaluate('()=>{for(const k of [...TM115.keys,...TC119.keys])XART.rdy(k);city16Warm();}')
 p.wait_for_function('()=>[...TM115.keys,...TC119.keys].every(k=>XART.rdy(k))&&city16Warm()',polling=50)
 p.evaluate("()=>{window.artBoss=fb112Create('thunder',false);artBoss.x=artBoss.y=400;for(const k of TC119.keys)TC119.images[k]=XART.get(k);artBoss.enter=false;artBoss._fb112.phase='recover';artBoss._fb112.scale=1;fb112Ready=()=>true;}")
 capture="""({angle,f,shadow})=>{const B=artBoss;B._fb112.heading=angle;for(const q of B._fb112.parts)q.angle=angle;const c=document.createElement('canvas');c.width=c.height=800;const g=c.getContext('2d'),base=ctx.drawImage,bank=city16Bank;ctx.setTransform(1,0,0,1,0,0);ctx.save();efxClock=f*1.5/16;tm115State(B).clock=B._tc119.clock=f*1.5/16;let engine=0;
 city16Bank=function(n,frame,x,y){if(n.startsWith('thrust-')){if(shadow)return true;frame=(f+engine++*3)%16;}return bank(n,frame,x,y);};ctx.drawImage=function(im,...a){g.save();g.setTransform(ctx.getTransform());g.globalAlpha=ctx.globalAlpha;g.globalCompositeOperation=ctx.globalCompositeOperation;g.imageSmoothingEnabled=false;g.drawImage(im,...a);g.restore();};try{fb112Draw(B);}finally{ctx.drawImage=base;city16Bank=bank;ctx.restore();}return c.toDataURL('image/png');}"""
 for name,a in [('nw',-math.pi*.65),('w',math.pi),('south',math.pi/2),('north',-math.pi/2)]:
  for f in range(16 if name in ['nw','w']else 1):
   for shadow in ([False,True]if name in ['nw','w']else[False]):
    uri=p.evaluate(capture,{'angle':a,'f':f,'shadow':shadow});fn='storm-'+name+('-body'if shadow else'')+'-%02d.png'%f;(O/fn).write_bytes(base64.b64decode(uri.split(',')[1]))
 assert not errors,errors;b.close();print('Captured current corrected hull/nozzles:32 flight and32 body-only shadow cells, both cardinal proofs; no console/page errors.',flush=True)
