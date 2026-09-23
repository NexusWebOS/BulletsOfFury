import base64,json,sys,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
from shoot import GAME,SETUP,TRAP_RAF,serve
from playwright.sync_api import sync_playwright
OUT=ROOT/'_shots/hammer_combat_0923';OUT.mkdir(exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=serve(GAME);errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4')
  pg.evaluate(TRAP_RAF);pg.evaluate(SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':True})
  pg.evaluate("""()=>{diffKey='furious';DIFF=DIFFS.furious;run.spaceMode=true;story=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];powerups=[];
    spawnBoss('chromehammer');boss.enter=false;boss._noHit=false;boss.x=worldWidth()/2;boss.y=VH*.34;boss.hp=boss.maxhp;
    boss._hammer.balance0922=true;boss._hammer.mode='hammer';player.invuln=1e9;player.dead=false;
    XART.rdy('arch_combat_0923');XART.rdy('arch_stun_0920');
    window.advanceHammer=(seconds)=>{for(let t=0;t<seconds;t+=1/60)hammerBossTick(boss,1/60);};
  }""")
  pg.wait_for_function("()=>XART.rdy('arch_combat_0923')&&XART.rdy('arch_stun_0920')&&XART.rdy('arch_spiked_ball')",timeout=30000)
  def shot(name):
   pg.evaluate('()=>{shake=0;boss.flash=0;drawWorld(0)}')
   data=pg.evaluate("document.getElementById('screen').toDataURL('image/png').split(',')[1]")
   (OUT/(name+'.png')).write_bytes(base64.b64decode(data))
  results={}
  results['ball']=pg.evaluate("""()=>{const h=boss._hammer;hammerBallArm(boss);hammerState(boss,'curl');advanceHammer(1.3);
    const start={x:boss.x,y:boss.y};advanceHammer(.5);const slow=Math.hypot(boss.x-start.x,boss.y-start.y)/.5;
    advanceHammer(10);return {slow,bounces:h.ballBounces,x:boss.x,y:boss.y,state:h.state};}""")
  assert results['ball']['bounces']>=5,results['ball'];shot('ball')
  results['nova']=pg.evaluate("""()=>{const h=boss._hammer;hammerState(boss,'uncurl');advanceHammer(1.4);advanceHammer(.8);return {state:h.state};}""")
  assert results['nova']['state']=='nova_charge';shot('nova_charge')
  results['nova']=pg.evaluate("""()=>{advanceHammer(2);return {shots:eBullets.filter(q=>q._hammerNova).length,state:boss._hammer.state};}""")
  assert results['nova']['shots']==96,results['nova'];shot('nova_release')
  results['stun']=pg.evaluate("""()=>{const h=boss._hammer;h.mode='hammer';h.hammerDestroyed=false;h.hammerHP=1;hammerState(boss,'throw');
    h.throw={x:boss.x-120,y:boss.y+130};const shot={kind:'spaceLaser',x:h.throw.x,y:h.throw.y,dmg:10,w:8,h:20,vx:0,vy:-8,t:0};_dmgBullet=shot;
    spaceBulletHit(shot,false);const broken=h.hammerDestroyed&&h.state==='hammer_exposed';
    bossHitTest(boss.x,boss.y);const doubled=hammerBossDamage(boss,10);advanceHammer(4.8);
    return {broken,doubled,state:h.state,t:h.t};}""")
  assert results['stun']['broken'] and results['stun']['doubled']==20 and results['stun']['state']=='hammer_stun',results['stun'];shot('stun')
  results['recovery']=pg.evaluate("""()=>{advanceHammer(.3);const at=boss._hammer.state;advanceHammer(.7);advanceHammer(.02);return {at,state:boss._hammer.state,restored:!boss._hammer.hammerDestroyed};}""")
  assert results['recovery']['restored'] and results['recovery']['state']=='warn',results['recovery']
  pg.evaluate("()=>{eBullets=[];hammerWhirlStart(boss);advanceHammer(1.5)}");shot('whirlwind')
  pg.evaluate("()=>{advanceHammer(2.1)}");shot('giant_warning')
  results['counter']=pg.evaluate("""()=>{const h=boss._hammer;hammerGiantArm(boss);advanceHammer(1.15);
    const q={kind:'spaceLaser',x:boss.x,y:boss.y,vx:0,vy:-8,w:8,h:18,dmg:8,t:0};_dmgBullet=q;spaceBulletHit(q,false);
    const reflected=!!q._enemyReflected,sy=q.y;spaceBulletTick(q,.05);
    _dmgBullet={kind:'gmiss',x:boss.x,y:boss.y+30};hammerBossDamage(boss,8);_dmgBullet=null;
    return {reflected,moved:q.y>sy,state:h.state};}""")
  assert results['counter']=={'reflected':True,'moved':True,'state':'giant_knockback'},results['counter'];shot('missile_counter')
  results['doubleStrike']=pg.evaluate("""()=>{const h=boss._hammer;h.giantLeft=2;hammerGiantArm(boss);let strikes=0,last=h.state;
    for(let i=0;i<650;i++){hammerBossTick(boss,1/60);if(h.state==='giant_sweep'&&last!==h.state)strikes++;last=h.state;}
    return {strikes,state:h.state,noHit:boss._noHit};}""")
  assert results['doubleStrike']['strikes']==2 and not results['doubleStrike']['noHit'],results['doubleStrike']
  pg.evaluate("()=>{hammerGiantArm(boss);advanceHammer(1.64)}");shot('giant_sweep')
  results['hardNova']=pg.evaluate("""()=>{diffKey='hard';DIFF=DIFFS.hard;eBullets=[];boss._hammer.novaShots=0;hammerState(boss,'nova_charge');advanceHammer(2.5);return eBullets.filter(q=>q._hammerNova).length;}""")
  assert results['hardNova']==32,results['hardNova']
  results['normalRecovery']=pg.evaluate("""()=>{diffKey='normal';DIFF=DIFFS.normal;boss.hp=boss.maxhp;hammerState(boss,'uncurl');advanceHammer(1.3);return boss._hammer.state;}""")
  assert results['normalRecovery']=='hammer',results['normalRecovery']
  assert not errors,errors
  results['errors']=errors;(OUT/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2));br.close()
finally:stop()
