"""Seeded before/after field pressure plus actual nine-stage enemy updates."""
import sys,json,base64,http.server
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/late_game_0927');OUT.mkdir(exist_ok=True,parents=True)
def run():
 port,stop=sh.serve(sh.GAME);errors=[];report={'pressure':[],'fields':[]}
 try:
  with sync_playwright() as pw:
   br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
   for version in ['before','after']:
    pg=br.new_page(viewport={'width':1000,'height':1100})
    pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
    if version=='before':
     pg.route('**/assets/game.js',lambda route:route.fulfill(path=str(OUT/'game-before.js'),content_type='application/javascript'))
     pg.route('**/assets/*0927.js',lambda route:route.fulfill(body='',content_type='application/javascript'))
    pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF);pg.wait_for_timeout(60)
    for difficulty in ['normal','hard','furious']:
     pg.evaluate(r'''d=>{
      diffKey=d;DIFF=DIFFS[d];run.mode='arcade';run.pilot='cole';beginStage(6);setState(GS.PLAY);player.reset();player.invuln=1e9;
      story=null;s6Opening=null;boss=null;bossActive=false;bossWarned=true;subBoss=null;subBossActive=false;subBossDone=true;subBossTriggered=true;
      enemies=[];eBullets=[];pBullets=[];powerups=[];stageTimer=10;
      s6Wing.beats=2;s6Wing.all=true;s6WingLaunch(8,true);
      window.rndOriginal=Math.random;let seed=927;Math.random=()=>((seed=(Math.imul(seed,1664525)+1013904223)>>>0)/4294967296);
      window.fieldAudit={maxEnemies:0,maxHostile:0,maxFriendly:0,hostileSum:0,friendlySum:0,n:0,rolls:[],types:[],reactionTypes:[],blocked:0};
     }''',difficulty)
     for second in range(38):
      pg.evaluate(r'''s=>{for(let i=0;i<60;i++){
       player.invuln=2;player.x=worldWidth()/2+Math.sin((s*60+i)/175)*100;
       updatePlay(1/60);const a=fieldAudit;a.maxEnemies=Math.max(a.maxEnemies,enemies.filter(e=>!e.dead).length);a.maxHostile=Math.max(a.maxHostile,eBullets.length);a.maxFriendly=Math.max(a.maxFriendly,pBullets.length);
       a.hostileSum+=eBullets.length;a.friendlySum+=pBullets.length;a.n++;
       for(const q of s6Wing.ships){if(q.dodgeT>0&&!q._qaWasDodging)a.rolls.push({key:q.key,mode:q.dodgeMode,t:s+i/60});q._qaWasDodging=q.dodgeT>0;}
       for(const e of enemies){if(!a.types.includes(e.type))a.types.push(e.type);if(e._ai27){if(!a.reactionTypes.includes(e.type))a.reactionTypes.push(e.type);}}
      }ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}''',second)
      if second%5==0:pg.wait_for_timeout(12)
      if second==24:
       data=pg.evaluate('()=>ctx.canvas.toDataURL()');(OUT/f'stage6_{version}_{difficulty}.png').write_bytes(base64.b64decode(data.split(',')[1]))
     row=pg.evaluate('()=>{Math.random=rndOriginal;return {...fieldAudit,pressure:s6PressureMultiplier()};}')
     report['pressure'].append({'version':version,'difficulty':difficulty,**row})
     print('PRESSURE',version,difficulty,row['maxEnemies'],row['maxHostile'],row['maxFriendly'],flush=True)
    if version=='after':
     for stage in range(1,10):
      pg.evaluate(r'''st=>{
       diffKey='hard';DIFF=DIFFS.hard;run.mode='arcade';run.pilot='cole';beginStage(st);setState(GS.PLAY);story=null;s6Opening=null;s6Wing=null;
       player.reset();player.invuln=1e9;subBossDone=true;subBossTriggered=true;bossWarned=true;window.stageAudit={types:[],managed:[],air:[],shooters:[],reactions:[],maxBullets:0,invalid:0,playerJump:0};
      }''',stage)
      for second in range(27):
       pg.evaluate(r'''second=>{for(let j=0;j<60;j++){
        player.invuln=2;const old={x:player.x,y:player.y};updatePlay(1/60);const a=stageAudit;
        a.playerJump=Math.max(a.playerJump,Math.hypot(player.x-old.x,player.y-old.y));a.maxBullets=Math.max(a.maxBullets,eBullets.length);
        for(const e of enemies){if(!a.types.includes(e.type))a.types.push(e.type);const A=e._ai27;if(A){if(!a.managed.includes(e.type))a.managed.push(e.type);if(A.air&&!a.air.includes(e.type))a.air.push(e.type);if(A.shots&&!a.shooters.includes(e.type))a.shooters.push(e.type);if(A.reactions&&!a.reactions.includes(e.type))a.reactions.push(e.type);}if(!Number.isFinite(e.x+e.y))a.invalid++;}
        ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);
       }}''',second)
       if second%6==0:pg.wait_for_timeout(10)
      report['fields'].append({'stage':stage,**pg.evaluate('()=>stageAudit')})
      data=pg.evaluate('()=>ctx.canvas.toDataURL()');(OUT/f'field_stage{stage}.png').write_bytes(base64.b64decode(data.split(',')[1]))
      print('FIELD',stage,report['fields'][-1],flush=True)
    pg.close()
   report['errors']=errors;(OUT/'field_report.json').write_text(json.dumps(report,indent=2));br.close()
 finally:stop()
 assert not errors,errors
 assert all(r['invalid']==0 for r in report['fields'])
if __name__=='__main__':run()
