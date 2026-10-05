"""Actual player projectile emitters and boss collision paths, isolated hulls."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_1005'
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
port,stop=sh.serve(str(R));errors=[];out={'laserHP':[],'checks':[]}
def ck(v,n):out['checks'].append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox']);p=b.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate(SETUP,{'stage':6,'kind':'rebelsquad','pilot':'cole','diff':'furious'})
  p.evaluate('()=>{window.R=B._rebels;rf28Init(B,R);R.frIntro={done:true};B._noHit=false;window.G=rg4Init(B);G.releaseAt=9999;G.rescueAt=9999;for(const q of R.ships){q.mode="fight";q.warp=0;q.rg4.cd=9999;q.rg4.act=null;}run._primary1003b="mg";run.weapon=0;run._cfUnlocked=8;run.wlevels[0]=8;}')
  for tier in [6,7,8]:
   for pilot in ['voss','nyx','rook','kaia','jace']:
    v=p.evaluate('([tier,key])=>{const q=R.ships.find(q=>q.key===key);for(const s of R.ships){s.x=-1500;s.frCloak=0;}q.x=player.x=worldWidth()/2;q.y=220;const hp=q.hp;run._cfTier=run.wlevel=tier;player.fireCd=0;pBullets=[];if(tier===8)coleFuseRelease(FUSE_FULL);else pShoot();const kinds=pBullets.map(p=>p.kind);for(const t of pBullets){t.x=t.cx=q.x;t.y=q.y;t.vx=0;t.vy=t._cfFusion?0:-.01;}updatePlay(1/60);return{tier,pilot:key,kinds,before:hp,after:q.hp};}',[tier,pilot]);out['laserHP'].append(v)
    ck(v['after']<v['before'],'Cole '+str(tier)+' damages '+pilot+' using emitted '+','.join(v['kinds']))
  ck(p.evaluate('()=>{const q=R.ships.find(q=>q.key==="jace");for(const s of R.ships)s.x=-1500;q.x=300;q.y=200;return _coleNearest(300,450)?._retinaId==="on5-cole-jace";}'),'homing Cole lasers acquire an actual fighter rather than empty squad center')
  ck(p.evaluate('()=>{const q=R.ships.find(q=>q.key==="jace");q.frCloak=5;return _coleNearest(300,450)?._retinaId!=="on5-cole-jace";}'),'cloak excludes Cole homing acquisition')
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'cole','diff':'furious'})
  p.evaluate('()=>{window.J=j3State(B);window.S=B._r30;j3Encounter(B,2);j3Mimic(B,5);S.mode="fight";B.enter=false;B._noHit=false;on5Shield(B,"red",9);S.wallAge1003=1;const q=r30ShieldBounds(B);player.x=q.x;pBullets=[{kind:"beam",x:q.x,w:12,h:player.y,top:-20,bot:player.y-14,life:.5,dmg:9,_ht:0,_hit:[],seat:1}];updatePlay(1/60);}')
  ck(p.evaluate('()=>S.shield===0&&CWD.effects.some(f=>f.kind==="shatter")'),'actual sustained laser exhausts code shield and triggers shatter')
  ck(not errors,'zero browser errors');b.close()
finally:
 stop();out['errors']=errors;(O/'lasers.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
sys.exit(0 if all(q['ok'] for q in out['checks']) and not errors else 1)
