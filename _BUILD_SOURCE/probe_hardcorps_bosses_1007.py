"""Native encounter choreography, laser crossings, module ownership, and pixels."""
from pathlib import Path
import base64,json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'_shots/hardcorps_bosses_1007';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[],'scenes':[]};errors=[]
def ck(v,name):
 report['checks'].append({'ok':bool(v),'name':name});print(('OK ' if v else 'FAIL ')+name,flush=True)
def frames(p,n,expr='updatePlay(1/60);drawWorld(1/60);'):
 for i in range(0,n,12):p.evaluate('(n)=>{for(let i=0;i<n;i++){'+expr+'}}',min(12,n-i));p.wait_for_timeout(3)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
def setup(p,stage,kind,mini=True,diff='normal'):
 p.evaluate(SETUP,{'stage':stage,'kind':kind,'mini':mini,'diff':diff})
 p.evaluate('()=>{storySkip();BOFCinematicDirector.cancel();story=null;thaw=null;enemies=[];if(B._bomber){B._bomber.mode="recover";B._bomber.t=0;}if(B._s4war){B._s4war.shield.rearming=false;B._er26.neutralOpening=false;B._er26.nuclearRevealed=true;}hc1007Warm();}')
 p.wait_for_function('()=>XART.rdy("av3_laser_beams")&&XART.rdy("av3_laser_muzzles")',timeout=120000)
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  if not p.evaluate('()=>typeof HC1007!=="undefined"'):p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/hardcorps_bosses_1007.js')
  for diff in ['easy','normal','hard','furious']:
   for stage,kind in [(5,'spacebomber'),(6,'siegebomber')]:
    setup(p,stage,kind,diff=diff);frames(p,15)
    # Explicitly start the chosen pattern after using the actual registered encounter.
    p.evaluate('()=>hc1007BomberSet(B,B._bomber.space?"cross":"flak")')
    frames(p,50);shot(p,f'{stage}-{diff}-tell')
    q=p.evaluate('()=>({hp:B.hp,max:B.maxhp,mode:B._hc1007.mode,warm:B._hc1007.cross?.warm||B._hc1007.warm,parts:B._bomber.parts.length})')
    ck(q['parts']==4 and q['warm']>=1, f'Stage {stage} {diff}: four intact modules and committed warning')
    frames(p,65);shot(p,f'{stage}-{diff}-release')
    if stage==5:
     ck(p.evaluate('()=>HC1007.draws.beam>0&&B._hc1007.cross.releases>0'),f'Stage 5 {diff}: authored four-way beam draws and releases')
     p.evaluate('()=>{const C=B._hc1007.cross;C.age=C.warm+C.on+C.fade+.08;}');shot(p,f'5-{diff}-crossing')
     ck(p.evaluate('()=>hc1007CrossState(B).mode==="gap"'),f'Stage 5 {diff}: four beams fully disappear between sweeps')
     p.evaluate('()=>{window.positive=0;window.saveHit=playerHit;playerHit=()=>positive++;const C=B._hc1007.cross;C.age=C.warm+.10;const L=hc1007CrossState(B).rays[0];player.x=L.x+(L.ex-L.x)*.14;player.y=L.y+(L.ey-L.y)*.14;hc1007CrossTick(B,.00001);}')
     ck(p.evaluate('()=>positive>0'),f'Stage 5 {diff}: actual laser collision damages on the visible ray')
     p.evaluate('()=>{positive=0;const C=B._hc1007.cross;C.age=C.warm+C.on+C.fade+.08;hc1007CrossTick(B,.00001);playerHit=saveHit;}')
     ck(p.evaluate('()=>positive===0'),f'Stage 5 {diff}: crossing interval has no invisible damage')
     p.evaluate('()=>{const C=B._hc1007.cross;window.duration=C.duration;C.age=C.warm+C.duration;window.rotation=hc1007CrossState(B).angle-C.angle;hc1007CrossTick(B,0);}')
     ck(p.evaluate('()=>Math.abs(rotation-TAU)<1e-8&&!B._hc1007.cross'),f'Stage 5 {diff}: exact full revolution ends and clears')
    else:
     if diff=='easy':frames(p,26)
     ck(p.evaluate('()=>B._hc1007.flakCount-B._hc1007.lines.length===1&&B._hc1007.lines.every(L=>L.fire)&&B._bomber.bombs.length>0'),f'Stage 6 {diff}: flak retains exactly one fixed safe lane')
   setup(p,4,'stormsovereign',False,diff);p.evaluate('()=>er26Set(B,"hc-cross1007")');frames(p,115);shot(p,'4-'+diff+'-cross')
   ck(p.evaluate('()=>!!B._hc1007.cross&&B._hc1007.cross.releases>0'),f'Sovereign {diff}: new cross runs through real shield controller')
   p.evaluate('()=>{const m=B._mr27.parts.find(p=>p.id==="lightning"),q=mr27Shape(B,"lightning");mr27Damage(B,m.hp+1,q.x,q.y);}');frames(p,1)
   ck(p.evaluate('()=>B._mr27.parts.find(p=>p.id==="lightning").dead&&!B._hc1007.cross'),f'Sovereign {diff}: destroying lightning weapon cancels every ray immediately')
  setup(p,5,'spacebomber',diff='furious');frames(p,2);p.evaluate('()=>hc1007BomberSet(B,"cross")');frames(p,105)
  p.evaluate('()=>{siegeBomberHit(B,1e6,null,null,"laserL");}');shot(p,'space-left-gun-broken')
  ck(p.evaluate('()=>hc1007CrossState(B).rays.length===2&&hc1007CrossState(B).rays.every(L=>L.id==="laserR")'),'two surviving space rays share the live opposite cannon')
  p.evaluate('()=>{siegeBomberHit(B,1e6,null,null,"core");}');frames(p,1)
  ck(p.evaluate('()=>B.dead&&!B._hc1007.cross'),'bomber death clears all custom warning/collision state')
  setup(p,8,'heralddeath',diff='furious');p.wait_for_function('()=>XART.rdy(HD1003_ART.key)',timeout=120000)
  p.evaluate('()=>{B._hd1003.seq=3;hd1003Tell(B);}');frames(p,55);shot(p,'herald-cross-tell');frames(p,55);shot(p,'herald-cross-live')
  ck(p.evaluate('()=>B._hd1003.attack==="eclipse-cross"&&B._hc1007.cross.releases===1'),'Herald teaches original attacks before its wing-driven cross')
  p.evaluate('()=>hd1003Break(B,hd1003Part(B,"wingL"))');frames(p,5);shot(p,'herald-wing-detached')
  ck(p.evaluate('()=>hc1007CrossState(B).rays.length===2&&hc1007CrossState(B).rays.every(L=>L.id==="wingR")'),'Herald wing disarm cancels its opposite ray pair')
  p.evaluate('()=>{window.drawAlpha=[];const f=HC1007_BASE.heraldBlit;HC1007_BASE.heraldBlit=function(p,P,flash,a){if(p.dead)drawAlpha.push(a);return f.apply(this,arguments);};}');frames(p,35);shot(p,'herald-opaque-falling-wing')
  ck(p.evaluate('()=>drawAlpha.length>0&&drawAlpha.every(a=>a===1)'),'broken Herald module stays fully opaque during native falling animation')
  # Actual held movement crosses the expired ray without roll or invulnerability.
  setup(p,5,'spacebomber',diff='furious');frames(p,2);p.evaluate('()=>{hc1007BomberSet(B,"cross");const C=B._hc1007.cross;C.age=C.warm+C.on+C.fade+.03;window.moveStart=player.x;player.invuln=0;run.shield=0;window.contacts=0;window.realHit=playerHit;playerHit=function(){contacts++;return realHit.apply(this,arguments);};}')
  p.keyboard.down('ArrowRight');frames(p,23);p.keyboard.up('ArrowRight')
  ck(p.evaluate('()=>Math.abs(player.x-moveStart)>35&&contacts===0&&!player.roll&&!player.somer'),'ordinary movement uses the absent-laser crossing window without damage')
  p.evaluate('()=>playerHit=realHit')
  # Natural entry and complete attack books, without forcing a custom state.
  for stage,kind in [(5,'spacebomber'),(6,'siegebomber')]:
   setup(p,stage,kind,diff='normal');frames(p,2200,'updatePlay(1/60);')
   q=p.evaluate('()=>({history:B._bomber.history,finite:Number.isFinite(B.x+B.y),hp:B.hp,mode:B._hc1007.mode})');report['scenes'].append({'stage':stage,**q})
   ck(q['finite'] and all('hc-'+m in q['history'] for m in (['relocate','lances','cross','strafe','recover'] if stage==5 else ['relocate','flak','strafe','lances','recover'])),f'Stage {stage}: natural full book relocates, attacks, and recovers')
   shot(p,f'{stage}-natural-book')
  report['draws']=p.evaluate('()=>HC1007.draws');report['errors']=errors;ck(not errors,'no browser page or console errors')
  report['scope']='Short native fixtures, positive damage controls and one ordinary movement crossing; not full campaign clears or balance certification.'
  (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');br.close()
finally:stop()
print(json.dumps({'checks':len(report['checks']),'failed':[q['name'] for q in report['checks'] if not q['ok']],'errors':errors}))
if errors or any(not q['ok'] for q in report['checks']):raise SystemExit(1)
