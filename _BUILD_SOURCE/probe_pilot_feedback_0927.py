"""Native pixels for single emitters, tier palettes, ice breath and acceleration."""
import ast,base64,http.server,json
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
OUT=Path('_shots/pilot_feedback_0927');OUT.mkdir(exist_ok=True,parents=True)
def constant(file,key):
 t=ast.parse(Path(file).read_text(encoding='utf-8'));return next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and any(getattr(a,'id',None)==key for a in n.targets))
RESET=constant('_BUILD_SOURCE/verify_weapon_feedback_0926.py','RESET')
def shot(p,name):
 (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];report={}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1050});p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF)
  p.evaluate("()=>{wm26Warm();XART.rdy('ice_breath_0927');XART.rdy('mav_lances_0919');PILOTS.forEach(p=>['','_g1','_g2','_pv2','_pv2_g1','_pv2_g2'].forEach(s=>XART.rdy('ship_'+p.key+s)));}")
  p.wait_for_function("()=>XART.rdy('ice_breath_0927')&&XART.rdy('mav_lances_0919')&&Object.keys(DIRECTOR_ART.sheets).every(k=>XART.rdy('d27_'+k))&&PILOTS.every(p=>['','_g1','_g2','_pv2','_pv2_g1','_pv2_g2'].every(s=>XART.rdy('ship_'+p.key+s)))")
  p.evaluate(sh.SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':False});p.evaluate(RESET,{})
  p.evaluate("()=>{window.PFdraw=wm26Draw;window.PFdirect=d27MuzzleDraw;window.PFcalls=[];window.PFturrets=[];wm26Draw=function(...a){PFcalls.push({family:a[1],x:a[2],y:a[3]});return PFdraw(...a);};d27MuzzleDraw=function(...a){PFturrets.push({family:a[1],x:a[2],y:a[3]});return PFdirect(...a);};}")
  report['muzzles']=[]
  for w in [0,1,2,7]:
   p.evaluate(RESET,{'pilot':'cole','weapon':w})
   r=p.evaluate("""()=>{run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);pShoot();wm26Tick(.025);pShoot();wm26Tick(.045);PFcalls=[];ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return {weapon:run.weapon,flashes:wm26Releases.map(f=>({family:f.family,x:f.x,y:f.y})),draws:PFcalls,player:{x:player.x,y:player.y}};}""")
   report['muzzles'].append(r);shot(p,'muzzle-'+str(w))
  p.evaluate(sh.SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':False})
  p.wait_for_function('()=>furyShipReady()');p.evaluate("()=>{story=null;run.stage=5;gravityMode=GRAVITY_SHIP_ACTIVE;run.spaceMode=true;run.gravityShipReady=true;enemies=[];stagePlan=[];spawnClock=99999;wm26Releases=[];pBullets=[];spaceLaserFire();spaceVolleyLaunchRack(3);player._spaceMuzzle=.09;wm26Tick(.035);PFcalls=[];PFturrets=[];ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}")
  report['space']=p.evaluate("()=>({draws:PFcalls,turrets:PFturrets,ports:spaceShipHardpoints(player.x,player.y,SPACE_SHIP_SIZE)})");shot(p,'space-muzzles')
  report['thrusters']=p.evaluate("()=>PILOTS.map(p=>({pilot:p.key,...pf27TailParts('ship_'+p.key)}))")
  for boost in [0,1]:
   p.evaluate("""boost=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#111a29';ctx.fillRect(0,0,VW,VH);PILOTS.forEach((p,i)=>{const key='ship_'+p.key,im=d27ShipFrame(key,2),h=90,w=h*im.width/im.height,x=80+i%3*160,y=62+Math.floor(i/3)*172;pf27PlaneThrustDraw(ctx,key,x,y,w,h,boost);ctx.drawImage(im,x-w/2,y-h/2,w,h);ctx.fillStyle='white';ctx.font='11px monospace';ctx.textAlign='center';ctx.fillText(p.key,x,y-48);});}""",boost);shot(p,'thrusters-'+str(boost))
  p.evaluate(sh.SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':False});p.evaluate(RESET,{})
  report['acceleration']=[]
  for up,n in [(True,12),(True,18),(False,8),(False,50)]:
   p.evaluate("v=>{for(const k of keybind.up)Input.keys[k]=v;}",up);p.evaluate(sh.STEP,n)
   report['acceleration'].append(p.evaluate('()=>({power:player._thrustPower,y:player.y,zoom:viewZoom()})'));shot(p,'flight-'+str(len(report['acceleration'])))
  p.evaluate(sh.SETUP,{'state':'PLAY','stage':2,'pilot':'freezer','invuln':False});p.evaluate(RESET,{'pilot':'freezer','weapon':4});p.evaluate("()=>{run.wvars[4]='icebreath';flameFire(3);updatePlay(1/60);window.PFice=pBullets.find(b=>b.kind==='flame');}")
  report['iceFrames']=[]
  for i in range(12):
   r=p.evaluate("""i=>{PFice.anim=(i+.1)/18;PFice.life=1;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return {frame:Math.floor(PFice.anim*18)%12,span:PFice.bot-PFice.top};}""",i)
   report['iceFrames'].append(r)
   if i in [0,3,6,9]:shot(p,'ice-'+str(i))
  report['palettes']=p.evaluate("""()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#111a29';ctx.fillRect(0,0,VW,VH);const out=[];for(let lv=1;lv<=5;lv++){const im=pf27LanceArt(1,lv),c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);const a=g.getImageData(0,0,c.width,c.height).data;let hash=0;for(let i=0;i<a.length;i++)hash=(hash*31+a[i])|0;out.push({level:lv,hash});ctx.drawImage(im,lv*90-56,110,48,140);ctx.fillStyle='white';ctx.font='13px monospace';ctx.textAlign='center';ctx.fillText('LEVEL '+lv,lv*90-32,290);}return out;}""");shot(p,'lance-colors')
  p.evaluate(sh.SETUP,{'state':'PLAY','stage':1,'pilot':'maverick','invuln':False});p.evaluate(RESET,{'pilot':'maverick','weapon':3})
  report['lanceVolleys']=p.evaluate("""()=>{const out=[];run.wvars[3]='mavhoming';for(let lv=1;lv<=5;lv++){run.wlevels[3]=lv;run.wlevel=1;pBullets=[];wm26Releases=[];pShoot();wm26Tick(.04);for(let i=0;i<4;i++)updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);out.push({tier:lv,shots:pBullets.length,color:pBullets[0].colorLv,damage:pBullets[0].dmg,fixedTier:pBullets[0].lv,muzzleCount:wm26Releases.length,muzzleColor:wm26Releases[0]?.color,expectedColor:wlvGlow(lv)});}return out;}""");shot(p,'lance-level5-native')
  report['errors']=errors;br.close()
finally:stop()
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
assert not errors,errors
assert all(len(r['flashes'])==1 and len(r['draws'])==1 and r['draws'][0]['x']==r['player']['x'] for r in report['muzzles']),report['muzzles']
assert len(report['space']['turrets'])==2,report['space']
assert all(min(((f['x']-pt['x'])**2+(f['y']-pt['y'])**2)**.5 for pt in report['space']['ports']['laser'])<.01 for f in report['space']['turrets'])
assert len(set(p['hash'] for p in report['palettes']))==5
assert all(v['shots']==3 and v['color']==v['tier'] and v['fixedTier']==1 and abs(v['damage']-.62)<.001 and v['muzzleCount']==1 and v['muzzleColor']==v['expectedColor'] for v in report['lanceVolleys'])
assert len(set(i['frame'] for i in report['iceFrames']))==12
assert all(p['parts'] for p in report['thrusters'])
assert report['acceleration'][1]['power']>.9 and report['acceleration'][-1]['power']<.02
