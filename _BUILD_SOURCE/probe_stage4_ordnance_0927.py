"""Render every generated ammunition animation through the game's own renderer."""
import ast,base64,http.server,json
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overnight_0927/ordnance');OUT.mkdir(parents=True,exist_ok=True)
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];report={}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1100})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  p.evaluate(SETUP,{'stage':4,'kind':'olivewarden','mini':True,'diff':'hard'});p.wait_for_function("()=>XART.rdy('polish_ordnance')")
  report['art']=p.evaluate("""()=>{const im=XART.get('polish_ordnance'),c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);const a=g.getImageData(0,0,c.width,c.height).data;let clear=0;for(let i=3;i<a.length;i+=4)clear+=a[i]===0;return {width:im.width,height:im.height,transparent:clear/(a.length/4)};}""")
  report['frames']=p.evaluate("""()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#111923';ctx.fillRect(0,0,VW,VH);const rows=['steel','brass','rocket','missile','bomb','rail'],seen=[];let gets=0,draws=0;const get=XART.get,draw=ctx.drawImage;XART.get=function(k){if(k==='polish_ordnance')gets++;return get.call(XART,k);};ctx.drawImage=function(...a){draws++;return draw.apply(ctx,a);};try{rows.forEach((role,row)=>{for(let f=0;f<4;f++){const q={x:110+f*96,y:70+row*73,vx:0,vy:3,t:(f+.1)/18,szMul:1.6};seen.push({role,frame:f,drawn:drawStage4Projectile(q,role)});}});}finally{XART.get=get;ctx.drawImage=draw;}return {seen,gets,draws};}""")
  (OUT/'all-frames.png').write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
  report['liveRoutes']=p.evaluate("""()=>{const out=[];for(const kind of ['s4steel','s4brass','s4rocket','s4missile','s4bomb','s4rail']){
   eBullets=[];pBullets=[];const q=eShootT(240,270,Math.PI/2,3,kind,{w:9,h:17,silent:true});let gets=0;const get=XART.get;XART.get=function(k){if(k==='polish_ordnance')gets++;return get.call(XART,k);};
   try{drawBullets();}finally{XART.get=get;}out.push({kind,gets,w:q.w,h:q.h});}return out;}""")
  report['bossRoutes']=p.evaluate("""()=>{const out=[];for(const role of ['mg','rocket']){const q=stage4WarfareShot(B,'L',Math.PI/2,3,role);let key=null;const get=XART.get;XART.get=function(k){if(k==='polish_ordnance')key=k;return get.call(XART,k);};try{drawStage4WarfareProjectile(q);}finally{XART.get=get;}out.push({role,key,w:q.w,h:q.h,kind:q.kind});}return out;}""")
  p.evaluate('()=>{for(const k of Object.keys(Input.keys))Input.keys[k]=false;eBullets=[];player.invuln=999;}')
  for sec in range(18):
   p.evaluate('()=>{for(let i=0;i<60;i++){updatePlay(1/60);if(i%4===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/15);}}}');p.wait_for_timeout(20)
   if sec in [3,7,12,17]:(OUT/f'fight-{sec}.png').write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
  report['errors']=errors;br.close()
finally:stop()
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
assert not errors,errors
assert report['art']['transparent']>.7
assert len(report['frames']['seen'])==24 and report['frames']['gets']==24 and report['frames']['draws']==24 and all(x['drawn'] for x in report['frames']['seen'])
assert all(q['key']=='polish_ordnance' and q['w']==8 and q['h']==21 for q in report['bossRoutes'])
assert all(q['gets']==1 and q['w']==9 and q['h']==17 for q in report['liveRoutes'])
