"""Native art/animation, mounted weapon, destruction and Furious Tempest checks."""
import ast,base64,http.server,json
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
OUT=Path('_shots/director_0927');OUT.mkdir(parents=True,exist_ok=True)
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);report={};errors=[]
def shot(p,name):
 (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1050,'height':1100});p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF)
  p.evaluate("()=>{wm26Warm();for(const k of Object.keys(MR27_ART))XART.rdy('mr27_'+k);for(const p of PILOTS)for(const s of ['', '_g1','_g2'])XART.rdy('ship_'+p.key+s);}")
  p.wait_for_function("()=>Object.keys(DIRECTOR_ART.sheets).every(k=>XART.rdy('d27_'+k))&&PILOTS.every(p=>['','_g1','_g2'].every(s=>XART.rdy('ship_'+p.key+s)))&&XART.rdy('mr27_space')")
  report['reels']=p.evaluate("()=>Object.keys(DIRECTOR_ART.reels).map(k=>({family:k,frames:DIRECTOR_ART.reels[k].frames.length,ready:!!d27MuzzleArt(k,2)}))")
  for fi in range(6):
   p.evaluate("""f=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#101c28';ctx.fillRect(0,0,VW,VH);let i=0;for(const k of Object.keys(DIRECTOR_ART.reels)){const x=60+(i%4)*120,y=109+Math.floor(i/4)*126;d27MuzzleDraw(ctx,k,x,y,-Math.PI/2,f/6,90);ctx.fillStyle='#d5eaff';ctx.font='10px monospace';ctx.textAlign='center';ctx.fillText(k,x,y+12);i++;}}""",fi);shot(p,'muzzles-'+str(fi))
  report['pilots']=p.evaluate("""()=>PILOTS.map(p=>{const key='ship_'+p.key,F=d27ShipFrames(key),src=D27_RAW_GET(key),c=document.createElement('canvas');c.width=src.width;c.height=src.height;const g=c.getContext('2d'),read=im=>{g.clearRect(0,0,c.width,c.height);g.drawImage(im,0,0);return g.getImageData(0,0,c.width,c.height).data;},base=read(src),hi=read(D27_RAW_GET(key+'_g1')),lo=read(D27_RAW_GET(key+'_g2'));let changed=0,outside=0,alpha=0,hashes=[];for(const im of F||[]){const b=read(im);let hash=0;for(let i=0;i<b.length;i+=4){const mask=hi[i]!==lo[i]||hi[i+1]!==lo[i+1]||hi[i+2]!==lo[i+2],diff=b[i]!==base[i]||b[i+1]!==base[i+1]||b[i+2]!==base[i+2];if(diff){changed++;if(!mask)outside++;}if(b[i+3]!==base[i+3])alpha++;hash=(hash*31+b[i]+b[i+1]*3+b[i+2]*7)|0;}hashes.push(hash);}return {pilot:p.key,frames:F?.length||0,unique:new Set(hashes).size,changed,outside,alpha};})""")
  for fi in range(6):
   p.evaluate("""f=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#101c28';ctx.fillRect(0,0,VW,VH);PILOTS.forEach((p,i)=>{const im=d27ShipFrame('ship_'+p.key,f),h=136,w=h*im.width/im.height,x=80+i%3*160,y=74+Math.floor(i/3)*169;ctx.drawImage(im,x-w/2,y-h/2,w,h);ctx.fillStyle='#d5eaff';ctx.font='11px monospace';ctx.textAlign='center';ctx.fillText(p.key,x,y+81);});}""",fi);shot(p,'pilots-'+str(fi))
  report['tempest']=[]
  for diff in ['normal','hard','furious']:
   p.evaluate(SETUP,{'stage':5,'kind':'spacebomber','mini':True,'diff':diff});p.evaluate("()=>{story=null;s6Opening=null;s6Wing=null;for(const k of Object.keys(Input.keys))Input.keys[k]=false;window.D={states:[],maxBullets:0,travel:0,lastX:B.x,maxMove:0};}")
   for sec in range(35):
    p.evaluate("""()=>{for(let i=0;i<60;i++){player.invuln=999;updatePlay(1/60);D.travel+=Math.abs(B.x-D.lastX);D.maxMove=Math.max(D.maxMove,Math.abs(B.x-D.lastX));D.lastX=B.x;D.maxBullets=Math.max(D.maxBullets,eBullets.length);if(!D.states.includes(B._bomber.mode))D.states.push(B._bomber.mode);if(i%4===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(4/60);}}}""");p.wait_for_timeout(12)
    if sec in [6,12,22,33]:shot(p,f'tempest-{diff}-{sec}')
   report['tempest'].append(p.evaluate("()=>({difficulty:diffKey,name:B.name,variant:B._bomber.variant,...D,zoom:viewZoom(),finite:eBullets.every(b=>Number.isFinite(b.x+b.y+b.vx+b.vy))})"))
  report['rupture']=p.evaluate("""()=>{_xChain=[];const part=B._bomber.parts.find(p=>p.id==='laserL'),q=siegeBomberParts(B).find(p=>p.id===part.id);siegeBomberSet(B,'charge');siegeBomberHit(B,part.hp+1,q.x,q.y,part.id);const n=_xChain.filter(q=>q.module).length;d27ModuleRupture(B,part,q,'red');return {count:n,idempotent:n===_xChain.filter(q=>q.module).length,mode:B._bomber.mode};}""")
  for i in range(110):
   p.evaluate("()=>{player.invuln=999;updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}")
   if i in [5,25,55,85]:shot(p,'rupture-'+str(i))
   if i%6==0:p.wait_for_timeout(8)
  report['rupture']['remaining']=p.evaluate('()=>_xChain.filter(q=>q.module).length')
  report['errors']=errors;br.close()
finally:stop()
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
assert not errors,errors
assert all(p['unique']==6 and p['outside']==p['alpha']==0 and p['changed']>0 for p in report['pilots'])
assert all(t['finite'] and t['zoom']==1 for t in report['tempest'])
assert report['rupture']['count']>=12 and report['rupture']['idempotent'] and report['rupture']['remaining']==0
