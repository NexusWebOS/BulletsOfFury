from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,base64
R=Path(__file__).resolve().parents[1];O=R/'_shots/crossed_fate_1115';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000)
 errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8765/index.html?fate-inventory');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 q=p.evaluate("()=>({model:TM115_ART.model,banks:Object.fromEntries(Object.entries(TM115_ART.banks).map(([k,a])=>[k,{frames:a.frames,cw:a.cw,ch:a.ch,pivot:a.pivot}])),harrier:HF28_ART,funcs:{leave:String(scLeaveStage),choice:String(s6WingChoiceDraw),wing:String(s6WingDraw)},keys:Object.keys(XART._src).filter(k=>/scorch|ach_plq|burnmark|crater/.test(k)).slice(0,55),screens:{w:VW,h:VH,mapW:campaignViewWidth()},errors:window.__bofLastError})")
 (O/'native-inventory.json').write_text(json.dumps(q,indent=2),encoding='utf8')
 p.evaluate("()=>{run.stage=6;run.mode='campaign';run.pilot='cole';diffKey='furious';DIFF=difficultyForRun('campaign','furious');for(const k of [...TM115.keys,...TC119.keys])XART.rdy(k);for(const a of Object.values(HF28_ART))XART.rdy(a.key);}")
 p.wait_for_function('()=>[...TM115.keys,...TC119.keys].every(k=>XART.rdy(k))&&Object.values(HF28_ART).every(a=>XART.rdy(a.key))',polling=50)
 p.evaluate("()=>{window.artBoss=fb112Create('thunder',false);artBoss.x=400;artBoss.y=400;for(const k of TC119.keys)TC119.images[k]=XART.get(k);artBoss.enter=false;artBoss._fb112.phase='recover';artBoss._fb112.heading=-Math.PI*.65;artBoss._fb112.scale=1;window.oldReady=fb112Ready;fb112Ready=()=>true;}")
 for i in range(32):
  direction='nw'if i<16 else'w'
  p.evaluate('a=>artBoss._fb112.heading=a',-3.141592653589793*.65 if i<16 else 3.141592653589793)
  uri=p.evaluate("f=>{const c=document.createElement('canvas');c.width=c.height=800;const g=c.getContext('2d'),base=ctx.drawImage;ctx.setTransform(1,0,0,1,0,0);ctx.save();ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';efxClock=f/16;const s=tm115State(artBoss);s.clock=f/16;artBoss._tc119.clock=f/16;ctx.drawImage=function(im,...a){g.save();g.setTransform(ctx.getTransform());g.globalAlpha=ctx.globalAlpha;g.globalCompositeOperation=ctx.globalCompositeOperation;g.imageSmoothingEnabled=false;g.drawImage(im,...a);g.restore();};try{fb112Draw(artBoss);}finally{ctx.drawImage=base;ctx.restore();}return c.toDataURL('image/png');}",i)
  (O/('storm-native-'+direction+'-%02d.png'%(i%16))).write_bytes(base64.b64decode(uri.split(',')[1]))
 for name,key in [('harrier-north',q['harrier']['closed_north']['key']),('harrier-south',q['harrier']['closed_south']['key']),('harrier-broken',q['harrier']['broken_south']['key'])]:
  uri=p.evaluate("key=>{const im=XART.get(key),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return c.toDataURL('image/png');}",key)
  (O/(name+'.png')).write_bytes(base64.b64decode(uri.split(',')[1]))
 print(json.dumps({'models':q['model'],'choice':q['funcs']['choice'][:1800],'leave':q['funcs']['leave'][:900],'keys':q['keys'],'errors':errors}),flush=True)
 b.close()
