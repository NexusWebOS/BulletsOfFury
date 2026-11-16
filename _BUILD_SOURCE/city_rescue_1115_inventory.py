from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,base64,math
R=Path(__file__).resolve().parents[1];O=R/'_shots/city_rescue_1115';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(240000)
 p.goto('http://127.0.0.1:8765/index.html?city16-inventory');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{for(const k of [...TM115.keys,...TC119.keys])XART.rdy(k);for(const k of ['juggernaut','cole','decker'])XART.rdy(CP15_ART.banks[k].key);for(const k of REBEL_SHIPS)XART.rdy('rr_ship_'+k);}")
 p.wait_for_function("()=>[...TM115.keys,...TC119.keys,CP15_ART.banks.juggernaut.key,CP15_ART.banks.cole.key,CP15_ART.banks.decker.key,...REBEL_SHIPS.map(k=>'rr_ship_'+k)].every(k=>XART.rdy(k))",polling=50)
 p.evaluate("()=>{window.artBoss=fb112Create('thunder',false);artBoss.x=400;artBoss.y=400;for(const k of TC119.keys)TC119.images[k]=XART.get(k);artBoss.enter=false;artBoss._fb112.phase='recover';artBoss._fb112.scale=1;window.oldReady16=fb112Ready;fb112Ready=()=>true;}")
 meta=p.evaluate("()=>({engines:artBoss._fb112.M.engines,model:artBoss._fb112.M,depths:TC119_ART.depths,thrust:Object.fromEntries(Object.entries(TC119_ART.banks).filter(([k])=>k.startsWith('thrust_'))),ruralKeys:Object.entries(XART._src).filter(([k,v])=>/rural|countr|farmland|america/i.test(k+' '+v)).map(([k,v])=>({key:k,path:v})),jugg:CP15_ART.banks.juggernaut,faces:Object.fromEntries(['juggernaut','cole','decker'].map(k=>[k,CP15_ART.banks[k]])),functions:{point:String(fb112Point),blit:String(tc119Blit),phase:String(bg6Phase),mapFrame:String(cmap2Frame),drawMap:String(_drawStageSelectInner).slice(0,300)},rows:c16Rows('post-6').map(b=>({id:b.id,kind:b.kind,layout:b.layout,page:b.page,cm3:b.cm3})),beatTemplate:c16Rows('post-6')[0],demo:fb2TeamScript().map(b=>({who:b.who,text:b.text,kind:b.kind}))})")
 (O/'inventory.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
 for name,a in [('north',-math.pi/2),('south',math.pi/2),('nw',-math.pi*.65),('west',math.pi)]:
  uri=p.evaluate("a=>{artBoss._fb112.heading=a;for(const q of artBoss._fb112.parts)q.angle=a;const c=document.createElement('canvas');c.width=c.height=800;const g=c.getContext('2d'),base=ctx.drawImage,blit=tc119Blit;ctx.setTransform(1,0,0,1,0,0);ctx.save();efxClock=0;tm115State(artBoss).clock=artBoss._tc119.clock=0;tc119Blit=function(k){if(!k.startsWith('thrust_'))return blit.apply(this,arguments);};ctx.drawImage=function(im,...args){g.save();g.setTransform(ctx.getTransform());g.globalAlpha=ctx.globalAlpha;g.globalCompositeOperation=ctx.globalCompositeOperation;g.imageSmoothingEnabled=false;g.drawImage(im,...args);g.restore();};try{fb112Draw(artBoss);}finally{ctx.drawImage=base;tc119Blit=blit;ctx.restore();}return c.toDataURL('image/png');}",a)
  (O/('storm-clean-'+name+'.png')).write_bytes(base64.b64decode(uri.split(',')[1]))
  (O/('engines-'+name+'.json')).write_text(json.dumps(p.evaluate('artBoss._fb112.M.engines.map(e=>fb112Point(artBoss,e))')),encoding='utf8')
 for pk in ['juggernaut','cole','decker']:
  uri=p.evaluate("pk=>{const a=CP15_ART.banks[pk],im=XART.get(a.key),c=document.createElement('canvas');c.width=a.w;c.height=a.h;c.getContext('2d').drawImage(im,0,0,a.w,a.h,0,0,a.w,a.h);return c.toDataURL('image/png');}",pk)
  (O/(pk+'-cockpit-reference.png')).write_bytes(base64.b64decode(uri.split(',')[1]))
 uri=p.evaluate("()=>{const c=document.createElement('canvas');c.width=800;c.height=400;const g=c.getContext('2d');for(let i=0;i<REBEL_SHIPS.length;i++){const im=XART.get('rr_ship_'+REBEL_SHIPS[i]),k=140/Math.max(im.width,im.height);g.drawImage(im,80+i*150-im.width*k/2,200-im.height*k/2,im.width*k,im.height*k);}return c.toDataURL('image/png');}")
 (O/'five-rebels-reference.png').write_bytes(base64.b64decode(uri.split(',')[1]));b.close()
 print(json.dumps({'engines':meta['engines'],'ruralKeys':meta['ruralKeys'],'depths':meta['depths'],'template':meta['beatTemplate']})[:6500],flush=True)
