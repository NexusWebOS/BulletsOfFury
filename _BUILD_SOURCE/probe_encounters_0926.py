"""Native Chromium encounter matrix; authored pixels, progression and elemental contracts."""
import sys,json,base64,http.server
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path('_shots/encounters_0926');out.mkdir(exist_ok=True)
errors=[];report={'matrix':[]};port,stop=sh.serve(sh.GAME)
fixture="""cfg=>{
 diffKey=cfg.diff;DIFF=DIFFS[diffKey];run.stage=cfg.stage;curStage=STAGES[cfg.stage-1];beginStage(cfg.stage);setState(GS.PLAY);
 story=null;stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];explosions=[];particles=[];
 boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;stageTimer=0;player.reset();player.invuln=1e9;
 player.x=worldWidth()/2;player.y=VH*.79;camX=player.x-VW/2;
 if(cfg.mini)spawnSubBoss__inner(cfg.kind);else spawnBoss(cfg.kind);
 const b=cfg.mini?subBoss:boss;b._be=null;b.enter=false;b._noHit=false;b.x=worldWidth()/2;b.y=b._er26.home;b._drawY=b.y;
 b._er26.from={x:b.x,y:b.y};b._er26.to={x:b.x,y:b.y};b.t=0;window.testActor=b;
 window.er26Inspect={modes:[],forms:[],maxBullets:0,maxMove:0,last:{x:b.x,y:b.y},oldKind:b.kind,hp:b.maxhp,draws:0,colors:[]};
 return {name:b.name,kind:b.kind,hp:b.maxhp,w:b.w,h:b.h,world:worldWidth(),view:VW,VH};
}"""
def shot(pg,name):
 pg.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60)}')
 data=pg.evaluate('()=>ctx.canvas.toDataURL()');(out/(name+'.png')).write_bytes(base64.b64decode(data.split(',')[1]))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1100,'height':1000})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF)
  cases=[(2,'magmaward',True),(3,'frostcruiser',True),(3,'cryospear',False),(4,'olivewarden',True),(4,'stormsovereign',False)]
  for stage,kind,mini in cases:
   for diff in ['normal','hard','furious']:
    cfg={'stage':stage,'kind':kind,'mini':mini,'diff':diff};init=pg.evaluate(fixture,cfg)
    pg.wait_for_function("()=>{const b=testActor;return [SHIPBOSS[b._ship].key,'mwfx_fireball_3','l23fx_rime_orb_3','lz_bomb'].map(k=>XART.rdy(k)).every(Boolean)}",timeout=60000)
    print('RUN',kind,diff,flush=True)
    for second in range(76):
     pg.evaluate("""second=>{const b=testActor,R=b._er26,I=er26Inspect;
      if(second===30||second===53){
        b.hp=b.maxhp*(second===30?.49:.24);
        if(b._s4war&&!b._s4war.mini){for(const n of b._s4war.shield.nodes)stage4ShieldDestroyNode(b,n);stage4ShieldBeginRearm(b,second===30?.5:.25);}
      }
      for(let i=0;i<60;i++){
        player.invuln=2;player.x=clamp(worldWidth()/2+Math.sin((second*60+i)/170)*150,70,worldWidth()-70);
        updatePlay(1/60);I.maxMove=Math.max(I.maxMove,Math.hypot(b.x-I.last.x,b.y-I.last.y));I.last={x:b.x,y:b.y};
        I.maxBullets=Math.max(I.maxBullets,eBullets.length);
        if(!I.modes.includes(R.mode))I.modes.push(R.mode);if(!I.forms.includes(R.form))I.forms.push(R.form);
      }
      ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);
     }""",second)
     if second in [1,3,7,14,38,59,70] and (diff=='furious' or second in [7,38]):shot(pg,f'{kind}_{diff}_{second}')
     if second%8==0:pg.wait_for_timeout(12)
    result=pg.evaluate("""()=>{const b=testActor,R=b._er26;return {...er26Inspect,mode:R.mode,shots:R.shots,bodyShots:R.bodyShots,helperShots:R.helperShots,nuclear:b._s3Nuclear||null,kind:b.kind,same:testActor===(b.sub||b.mini?subBoss:boss),history:R.history,helpers:b._s4war?{drones:b._s4war.drones.map(d=>({dead:d.dead,x:d.x,y:d.y,shots:d.shots})),cores:b._s4war.coreTurrets.map(d=>({dead:d.dead,state:d.state,heat:d.heat})),coreShots:b._s4war.coreShots}:null}}""")
    report['matrix'].append({'cfg':cfg,'init':init,**result});(out/'matrix-progress.json').write_text(json.dumps(report,indent=2))
  # Actual hit paths, not just source text. The shared boundary must be neutral 1x,
  # opposite 2x, same 1x, with white ordinary hits on both original Stage 3 bodies.
  report['elements']=[]
  for mini,kind in [(True,'frostcruiser'),(False,'cryospear')]:
   pg.evaluate(fixture,{'stage':3,'kind':kind,'mini':mini,'diff':'furious'})
   result=pg.evaluate("""mini=>{const b=testActor,out=[];b._s3Nuclear={mode:'neutral',introDone:true};b._er26.neutralOpening=false;b._noHit=false;b._jcGhost=false;b._phaseInvuln=0;
    for(const form of ['neutral','fire','ice'])for(const element of ['fire','ice','fireice']){
      b._s3Nuclear.mode=form;b._er26.form=form;b.hp=b.maxhp;b.flash=0;_dmgBullet={kind:'bullet',_el:element};_lastHitX=b.x;_lastHitY=b.y;
      const expected=element==='fireice'&&form!=='neutral'||element==='fire'&&form==='ice'||element==='ice'&&form==='fire'?20:10;
      const before=b.hp;if(mini)hitSubBoss(10,b.x,b.y);else hitBoss(10);
      out.push({form,element,delta:before-b.hp,expected,flash:hitFlashColor(b,'#ffffff')});
    }_dmgBullet=null;return out;}""",mini)
   report['elements'].append({'kind':kind,'hits':result})
  report['errors']=errors;(out/'report.json').write_text(json.dumps(report,indent=2));br.close()
finally:stop()
print(json.dumps({'matrix':[{'kind':r['cfg']['kind'],'diff':r['cfg']['diff'],'modes':r['modes'],'forms':r['forms'],'maxBullets':r['maxBullets'],'maxMove':r['maxMove'],'shots':r['shots'],'bodyShots':r['bodyShots'],'helpers':r['helperShots']} for r in report['matrix']],'elements':report.get('elements'),'errors':errors},indent=2))
assert not errors,errors
for r in report['matrix']:
 assert len(r['modes'])>=5,r
 assert r['maxMove']<15,r
 assert r['kind']==r['init']['kind'],r
 if r['cfg']['stage']==3 and r['cfg']['diff']=='furious':assert set(r['forms'])=={'neutral','fire','ice'} and r['nuclear']['blasts']>=20,r
for r in report['elements']:
 for h in r['hits']:assert abs(h['delta']-h['expected'])<.001,(r['kind'],h)
