"""Native Chromium evidence for the full October 10 audio pass."""
from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/audio_1010';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,value,data=None):
    checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS ' if value else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
  p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000)
  p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(650,450)
  p.evaluate(shoot.SETUP,dict(state='PLAY',stage=2,pilot='maverick',invuln=True))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(2).ready&&XART.rdy(AP10_HUD_ART.key)}',polling=50)
  p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;run.lives=7;run.bombs=18;run.score=123456;camX=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUDStrip(hudctx);fb9HudSplit();}')
  p.screenshot(path=str(OUT/'hud-desktop.png'))
  q=p.evaluate('''()=>{const f=ph8Frame(ph8Theme()),h=document.getElementById('hud-bot'),t=document.getElementById('hud-top');
   return{life:f.rect.lives,weapon:f.rect.weapon,missile:f.rect.missiles,radar:f.rect.radar,row:PH8.row,house:h.height,top:t.height};}''')
  check('Raised counters are above the weapon panels',q['life'][1]+q['life'][3]<q['weapon'][1] and q['missile'][1]+q['missile'][3]<q['weapon'][1],q)
  check('Radar lives in the top scoreboard strip',q['radar'][1]>=q['row'])
  for width in [1920,1280,820,480]:
   p.set_viewport_size(dict(width=width,height=900));p.evaluate('window.__bofFit?.()')
   q=p.evaluate('''()=>{const a=document.getElementById('hud-bottom').getBoundingClientRect(),b=cv.getBoundingClientRect();return{left:a.left,right:a.right,w:a.width,gamew:b.width,top:a.top,bottom:b.bottom};}''')
   check('Full-width housing at viewport '+str(width),abs(q['w']-q['gamew'])<2 and q['left']>=-1 and q['right']<=width+1 and q['top']>=q['bottom']-1,q)
  p.set_viewport_size(dict(width=1280,height=900));p.evaluate('window.__bofFit?.()')
  q=p.evaluate('''()=>{run.weapon=5;run.wlevel=5;run.wlevels[5]=5;pBullets=[];player._orbCd=0;special=null;
   for(let i=0;i<6;i++)pShoot();return pBullets.filter(b=>b.kind==='orb').length;}''')
  check('Level V orb remains one committed ball',q==1,q)
  q=p.evaluate('''()=>{run.weapon=7;run.wlevel=5;pBullets=[];chaingunPlayerFire(5);return pBullets.filter(b=>b.kind==='mg').length;}''')
  check('Max chaingun has two wing lanes',q==2,q)
  q=p.evaluate('''()=>{player._fuse=1;run.bombs=15;run.missileLevel=5;pBullets=[];
   useBomb();autoFireMissiles();spaceVolleyAutoTick(1,true);return{n:pBullets.length,ammo:run.bombs};}''')
  check('Charging suppresses manual, automatic and space missiles without spending ammo',q['n']==0 and q['ammo']==15,q)
  q=p.evaluate('''()=>{player._fuse=0;run.stage=3;const t={x:200,y:100};
   return elementalDamageResult(t,'boss',{kind:'orb',_el:'ice'},100,200,100);}''')
  check('Ice boss absorbs 80% same-element damage',q['dmg']==20,q)
  check('No page, console or asset errors',not errors,errors)
  br.close()
finally:stop()
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] else 0)
