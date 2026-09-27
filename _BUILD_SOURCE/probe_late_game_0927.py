"""Native Chromium: late encounters and shared combat behavior, with authored pixels."""
import sys,json,base64
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/late_game_0927');OUT.mkdir(exist_ok=True,parents=True)
SETUP=r'''cfg=>{
 diffKey=cfg.diff;DIFF=DIFFS[diffKey];run.mode='arcade';run.pilot='cole';run.stage=cfg.stage;
 curStage=STAGES[cfg.stage-1];beginStage(cfg.stage);setState(GS.PLAY);player.reset();player.invuln=1e9;
 story=null;s6Opening=null;s6Wing=null;stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];explosions=[];particles=[];
 boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;stageTimer=0;groundTargetingReset();
 player.x=worldWidth()/2;player.y=VH*.8;camX=player.x-VW/2;
 if(cfg.mini)spawnSubBoss__inner(cfg.kind);else spawnBoss(cfg.kind);
 const b=cfg.mini?subBoss:boss;b._be=null;window.testActor=b;
 window.audit={modes:[],phases:[],kinds:[],maxMove:0,maxBullets:0,shots:0,invalid:0,last:{x:b.x,y:b.y}};
 return {kind:b.kind,ship:b._ship,hp:b.maxhp,world:worldWidth(),view:VW};
}'''
def shot(pg,name):
 pg.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60)}')
 data=pg.evaluate('()=>ctx.canvas.toDataURL()');(OUT/(name+'.png')).write_bytes(base64.b64decode(data.split(',')[1]))
def run():
 port,stop=sh.serve(sh.GAME);errors=[];report={'matrix':[]}
 try:
  with sync_playwright() as pw:
   br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1100,'height':1100})
   pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF);pg.wait_for_timeout(60)
   for stage,kind,mini in [(7,'dualscoopdredger',True),(7,'sludgeemperor',False),(9,'voidhorizon',True),(9,'tidalfusion',False)]:
    for diff in ['normal','hard','furious']:
     cfg={'stage':stage,'kind':kind,'mini':mini,'diff':diff};initial=pg.evaluate(SETUP,cfg)
     pg.evaluate('()=>late27Warm()');pg.wait_for_function("()=>['cfx_stage7_warden_walk','cfx_stage7_warden_cannon','warpcrystallance_3','tidaltorpedo_3'].map(k=>XART.rdy(k)).every(Boolean)",timeout=60000)
     print('RUN',kind,diff,flush=True)
     for second in range(75):
      pg.evaluate(r'''second=>{
       const b=testActor,I=audit;
       if(b._s9fusion&&second===22){for(const w of [b._s9fusion.left,b._s9fusion.right]){b._s9fusion.hit=w;s9FusionHit(b,1e6);}}
       if(b._s7warden&&[32,45,62].includes(second)){
        const ratio=second===32?.74:second===45?.49:.24;b._s7warden.noHit=false;s7WardenHit(b,Math.max(0,b.hp-b.maxhp*ratio),b.x,b.y);
       }
       if(b._s9rift&&second===35)b._s9rift.core.hp=b._s9rift.core.maxhp*.48;
       for(let j=0;j<60;j++){
        player.invuln=2;player.x=worldWidth()/2+Math.sin((second*60+j)/190)*140;
        updatePlay(1/60);
        const m=b._late27?.mode,phase=b._s7warden?.final.phase||b._s9fusion?.phase||'fight';
        if(m&&!I.modes.includes(m))I.modes.push(m);if(!I.phases.includes(phase))I.phases.push(phase);
        I.maxMove=Math.max(I.maxMove,Math.hypot(b.x-I.last.x,b.y-I.last.y));I.last={x:b.x,y:b.y};
        I.maxBullets=Math.max(I.maxBullets,eBullets.length);
        for(const q of eBullets){if(!I.kinds.includes(q.kind))I.kinds.push(q.kind);if(!Number.isFinite(q.x+q.y+q.vx+q.vy))I.invalid++;}
       }
       ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);
      }''',second)
      if second in [3,10,15,23,29,40,50,66] and (diff=='furious' or second in [15,29,50]):shot(pg,f'{kind}_{diff}_{second}')
      if second%5==0:pg.wait_for_timeout(15)
     row=pg.evaluate('()=>({...audit,history:testActor._late27?.history||[],turns:testActor._s9fusion?._late27?.history||[],hp:testActor.hp,maxhp:testActor.maxhp,actorRetained:testActor===(testActor.sub||testActor.mini?subBoss:boss)})')
     report['matrix'].append({'cfg':cfg,'initial':initial,**row});(OUT/'progress.json').write_text(json.dumps(report,indent=2))
   report['errors']=errors;(OUT/'report.json').write_text(json.dumps(report,indent=2));br.close()
 finally:stop()
 print(json.dumps({'matrix':[{k:r[k] for k in ['cfg','modes','phases','kinds','maxBullets','maxMove','invalid','turns']} for r in report['matrix']],'errors':errors},indent=2))
 assert not errors,errors
 for r in report['matrix']:
  assert r['invalid']==0,r
  assert len(r['modes'])>=5,r
  assert len(r['kinds'])>=2,r
  if r['cfg']['kind']=='tidalfusion':assert 'fuse' in r['phases'] and 'tidal' in r['phases'],r
if __name__=='__main__':run()
