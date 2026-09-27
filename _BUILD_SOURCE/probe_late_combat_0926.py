import sys,json,base64,http.server
from pathlib import Path
sys.path.insert(0,str(Path('_BUILD_SOURCE').resolve()))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path('_shots/late_combat_0926');out.mkdir(exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[];report={}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
  pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':True})
  report['hammer']=pg.evaluate("""() => {
    story=null;stagePlan=[];enemies=[];powerups=[];pBullets=[];eBullets=[];
    spawnBoss('chromehammer');boss.enter=false;boss._noHit=false;bossActive=true;boss.x=worldWidth()/2;boss.y=180;
    hammerState(boss,'hammer');const h=boss._hammer;h.balance0922=true;
    const target=retinaBossTargets(boss).find(t=>t.kind==='hammer'),hp=h.hammerHP;
    const missile={kind:'gmiss',x:target.x,y:target.y,dmg:15};
    retinaMissileDamage(target,15,missile);const moduleHit=h.hammerHP<hp;
    h.mode='chaingun';hammerState(boss,'chaingun');const cannon=retinaBossTargets(boss).find(t=>t.kind==='chaingun');
    const cannonHP=h.chainHP;retinaMissileDamage(cannon,15,{kind:'gmiss',x:cannon.x,y:cannon.y});
    const cannonHit=h.chainHP<cannonHP,finite=Number.isFinite(cannon.x)&&Number.isFinite(cannon.y);
    hammerState(boss,'giant_dive');boss._noHit=false;
    spaceDamageTarget(boss,12,{kind:'spaceVolley',x:boss.x,y:boss.y});
    return {moduleHit,cannonHit,finite,counter:h.state,contextRestored:_dmgBullet===null};
  }""")
  pg.evaluate("() => {XART.rdy('arch_whirlwind_0926');XART.rdy('late_campaign_flight_0926');}")
  pg.wait_for_function("()=>XART.rdy('arch_whirlwind_0926')&&XART.rdy('late_campaign_flight_0926')",timeout=20000)
  sheet=pg.evaluate("""() => {
    ctx.canvas.width=1200;ctx.canvas.height=680;ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#152433';ctx.fillRect(0,0,1200,680);
    boss._hammer.state='whirlwind';for(let f=0;f<8;f++){boss.x=(f%4)*300+150;boss.y=Math.floor(f/4)*330+165;boss._hammer.t=(f+.1)/18;hammerCombatDraw(boss);}
    return ctx.canvas.toDataURL('image/png');
  }""")
  (out/'whirlwind.png').write_bytes(base64.b64decode(sheet.split(',')[1]))
  sheet=pg.evaluate("""() => {
    ctx.canvas.width=640;ctx.canvas.height=800;ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#142330';ctx.fillRect(0,0,640,800);
    for(let row=0;row<8;row++)for(let f=0;f<4;f++)lateCampaignProjectileBlit({x:80+f*160,y:50+row*100,t:(f+.1)/14,vx:0,vy:-1},row,80);
    return ctx.canvas.toDataURL('image/png');
  }""")
  (out/'projectiles.png').write_bytes(base64.b64decode(sheet.split(',')[1]))
  # Real encounter update/draw smoke pass, no input cheats or forced deaths.
  report['stages']=[]
  for stage,difficulty in [(s,d) for s in [5,6,7,8,9] for d in ['normal','hard','furious']]:
   pg.reload(wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF)
   pg.evaluate('(d)=>{diffKey=d;DIFF=DIFFS[d];}',difficulty)
   pg.evaluate(sh.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True})
   pg.evaluate("""() => {ctx.canvas.width=VW*SS;ctx.canvas.height=VH*SS;story=null;s6Opening=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];spawnBoss(STAGES[run.stage-1].boss);window.__states=new Set();window.__shotKinds=new Set();}""")
   for i in range(30):
    pg.evaluate("""() => {for(let i=0;i<60;i++){updatePlay(1/60);if(boss)__states.add(boss._hammer?.state||boss._s7warden?.phase||boss._s9fusion?.phase||boss._whv?.mode||boss._v24?.phase||boss.phase);for(const b of eBullets)__shotKinds.add(b.kind);}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}""")
    pg.wait_for_timeout(35)
   report['stages'].append(pg.evaluate("() => ({difficulty:diffKey,stage:run.stage,boss:boss?.kind,enter:boss?.enter,states:[...__states],shots:[...__shotKinds],locks:_lockTargets().length})"))
   data=pg.evaluate("()=>ctx.canvas.toDataURL('image/png')");(out/f'stage{stage}_{difficulty}.png').write_bytes(base64.b64decode(data.split(',')[1]))
  br.close()
finally:stop()
report['errors']=errors;(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
assert not errors
assert all(report['hammer'][k] for k in ['moduleHit','cannonHit','finite','contextRestored'])
assert report['hammer']['counter']=='giant_knockback'

