"""Real password arenas, all native ace poses/hit PNGs and bomber damage checks."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json, base64, io, sys
import shoot as sh

R=Path(__file__).resolve().parents[1];O=R/'_shots/sky_repair_1004i';O.mkdir(exist_ok=True)
checks=[];errors=[];frames=[]
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
def ck(v,n):checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def ticks(p,n):
 for i in range(0,n,20):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}}',min(20,n-i));p.wait_for_timeout(10)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))

port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
  p=browser.new_page(viewport={'width':1400,'height':980})
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000)
  p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate('()=>{map4hPreviewStorage();ht27Stop();debugFight=null;coopOn=false;pilotIndex=PILOTS.findIndex(p=>p.key==="yuri");diffKey="furious";DIFF=DIFFS.furious;gp4AceWarm();stageXArenaReady();}')
  p.wait_for_function('()=>stageXArenaReady()&&Object.values(SKY4I_ART).every(a=>XART.rdy(a.key)&&XART.rdy(a.flash))',timeout=120000)
  p.evaluate('()=>{window.__arenaCalls=0;window.__arenaDraw=stageXArenaDraw;stageXArenaDraw=function(dt){window.__arenaCalls++;return window.__arenaDraw(dt);};}')
  for code in ['XHARR','XREBEL','HARR6','REBEL6']:
   p.evaluate('()=>{_pwTyped=[];pwInput="";setState(GS.PASSWORD);Input.clearTaps?.();ctx.setTransform(SS,0,0,SS,0,0);drawPassword(0);}')
   p.keyboard.type(code,delay=12);p.evaluate('()=>drawPassword(1/60)');p.keyboard.press('Enter');p.evaluate('()=>drawPassword(1/60)')
   ck(p.evaluate('()=>state===GS.DIFF&&PENDING_STAGE===6'),'password '+code+' enters the real difficulty flow')
   p.evaluate('()=>startRun(PENDING_STAGE)');ticks(p,120);shot(p,'arena-'+code)
   arena=p.evaluate('()=>{__arenaCalls=0;ctx.setTransform(SS,0,0,SS,0,0);drawBG(0);return {calls:__arenaCalls,active:stageXArenaActive(),kind:boss.kind,x:run._gp4StageX};}')
   ck(bool(arena['calls'])==code.startswith('X') and arena['active']==code.startswith('X'),code+' draws the correct arena through the game renderer')
   ck(arena['kind']==('rebelsquad' if 'REBEL' in code else 'warhive'),code+' retains its intended encounter')
  for route in ['left','right']:
   p.evaluate('(route)=>{run.mode="campaign";campaign.unlockedMax=8;campaign.stageX1004={route,done:false};cf4LaunchX();}',route)
   ck(p.evaluate('()=>{__arenaCalls=0;ctx.setTransform(SS,0,0,SS,0,0);drawBG(0);return __arenaCalls>0;}'),'campaign '+route+' rematch shares Stage X arena')
  p.evaluate(SETUP,{'stage':6,'kind':'warhive','diff':'furious'})
  p.evaluate('()=>{whvAceSpawn(B);B._whv.mode="ace";B._whv.ace.st="fight";B._whv.ace.x=VW/2;B._whv.ace.y=210;B._whv.ace.desp=null;B._whv.ace.dash=null;window.__aceFrame=enc30AceFrame;enc30AceFrame=()=>window.__pose;window.__drawKeys=[];window.__get=XART.get;XART.get=function(k){__drawKeys.push(k);return __get.apply(this,arguments);};}')
  # The actual renderer draws every full pose and both separated damage states.
  for f in range(20):
   pair=[]
   for hit in [False,True]:
    raw=p.evaluate('([frame,hit])=>{__pose=frame;B.flash=hit?.16:0;B._whv.ace.fl={body:0,wingL:0,wingR:0};B.hp=B.maxhp*(frame===1?.4:.9);__drawKeys=[];ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle="#000";ctx.fillRect(0,0,VW,VH);whvDrawAce(B);return cv.toDataURL().split(",")[1];}',[f,hit])
    im=Image.open(io.BytesIO(base64.b64decode(raw))).convert('RGB')
    scale=p.evaluate('()=>SS');box=(int((240-95)*scale),int((210-98)*scale),int((240+95)*scale),int((210+98)*scale))
    crop=im.crop(box);pair.append(crop)
   bp=list(pair[0].getdata());hp=list(pair[1].getdata())
   blue=sum(b>r*1.5 and b>g*1.25 and b>45 for r,g,b in bp)
   white=sum(min(q)>235 and max(q)-min(q)<5 and max(a)-min(a)>15 for a,q in zip(bp,hp))
   keys=p.evaluate('()=>__drawKeys.filter(k=>k.startsWith("sky4i_"))')
   ck(blue>100 and white>100 and any(k.endswith('_flash') for k in keys),'native ace pose '+str(f)+' stays blue and draws white hit pixels')
   frames.append({'frame':f,'blue_pixels':blue,'white_hit_pixels':white,'keys':keys})
   joined=Image.new('RGB',(380,196),(8,10,16));joined.paste(pair[0].resize((190,196)),(0,0));joined.paste(pair[1].resize((190,196)),(190,0))
   if f==0:montage=Image.new('RGB',(380*4,196*5))
   montage.paste(joined,((f%4)*380,(f//4)*196))
  montage.save(O/'native-poses-and-hits.png')
  p.evaluate('()=>{enc30AceFrame=__aceFrame;XART.get=__get;B._whv.ace.roll=null;B._whv.ace.somer=null;B._whv.ace.inverted=false;B._whv.ace.vx=0;B.flash=0;}')
  for dx,id in [(0,'body'),(-55,'wingL'),(55,'wingR')]:
   r=p.evaluate('([dx,id])=>{const A=B._whv.ace;B.flash=0;A.fl={body:0,wingL:0,wingR:0};const old=B.hp;_lastHitX=A.x+dx;_lastHitY=A.y;_dmgBullet=null;GP4.clock+=.2;const hit=warhiveHitTest(B,_lastHitX,_lastHitY);if(hit)hitBoss(1);ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle="#000";ctx.fillRect(0,0,VW,VH);whvDrawAce(B);return {hit,hp:B.hp,old,flash:B.flash,part:A.fl[id],key:A._hitMod};}',[dx,id])
   ck(r['hit'] and r['hp']<r['old'] and r['flash']>0 and r['part']>0,'real collision and boss damage flash '+id)
  shot(p,'blue-ace-hit')
  for diff in ['easy','normal','hard','furious','insanity']:
   p.evaluate(SETUP,{'stage':6,'diff':diff})
   for role in ['red','green','orange','opening','bomb-lane']:
    data=p.evaluate('(role)=>{enemies=[];const e=role==="opening"||role==="bomb-lane"?missionJetSpawn({kind:role==="opening"?"bomb":"lane",direction:role==="opening"?"south":"east",attack:2,x:player.x,y:180},{n:fr27Difficulty()}):fb2FlightSpawn({direction:"south",role,x:player.x,y:180});e.x=player.x;e.y=180;e._noHit=false;const hp=e.hp;_dmgBullet={kind:"mg",dmg:1};_dmgSrc="shot";for(let i=0;i<6;i++)if(!e.dead&&e._dyingT==null)hitEnemy(e,1);return {hp,max:e.maxhp,remaining:e.hp,dying:e.dead||e._dyingT!=null};}',role)
    ck(data['hp']==6 and data['max']==6 and data['dying'],diff+' '+role+' bomber dies to six base rounds')
   ck(p.evaluate('()=>{const e=fb2FlightSpawn({direction:"south",role:"green",x:player.x,y:180});e.y=180;e._noHit=false;_dmgBullet={kind:"gmiss",dmg:20};_dmgSrc="missile";hitEnemy(e,20);return e.hp<=0&&(e.dead||e._dyingT!=null);}'),diff+' lethal missile destroys bomber on first impact')
  # Pending warnings and actual attacks still release on Furious.
  p.evaluate(SETUP,{'stage':6,'diff':'furious'})
  p.evaluate('()=>{player.x=worldWidth()/2;player.y=VH-90;const e=fb2FlightSpawn({direction:"south",role:"orange",x:player.x,y:130});e.y=180;window.__bomber=e;fb2FlightTick(e,.36);}')
  ck(p.evaluate('()=>__bomber._fb2Rounds>=3'),'fragile bombers retain their authored attacks')
  shot(p,'arcade-bomber')
  p.goto(f'http://127.0.0.1:{port}/_shots/sky_repair_1004i/review.html',timeout=120000)
  game=p.frame(url=lambda u:'index.html?build=sky-repair-1004i-review' in u)
  game.wait_for_function('()=>window.__bofFrames>4&&bossActive',timeout=120000)
  for code in ['XHARR','XREBEL','HARR6','REBEL6','ACE','BOMBERS']:
   p.locator('[data-code="'+code+'"]').click();p.wait_for_timeout(120)
   if code=='ACE':valid=game.evaluate('()=>boss._whv.mode==="ace"&&XART.rdy("sky4i_ace")')
   elif code=='BOMBERS':valid=game.evaluate('()=>!bossActive&&fb2Flights.length===3&&!s6Opening')
   else:valid=game.evaluate('([x,kind])=>stageXArenaActive()===x&&boss.kind===kind',[code.startswith('X'),'rebelsquad' if 'REBEL' in code else 'warhive'])
   ck(valid,'playable review '+code+' button reaches the intended encounter')
  ck(not errors,'zero page and console errors');browser.close()
finally:stop()
(O/'checks.json').write_text(json.dumps({'checks':checks,'errors':errors,'poses':frames},indent=2)+'\n',encoding='utf-8')
print('RESULT',sum(c['ok'] for c in checks),'/',len(checks));sys.exit(bool(errors) or any(not c['ok'] for c in checks))
