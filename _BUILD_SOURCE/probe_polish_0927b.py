"""Native Chromium evidence for the September 27 follow-up gameplay pass."""
from pathlib import Path
import json,base64,http.server
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overhaul_0927b');OUT.mkdir(exist_ok=True,parents=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];report={}
SETUP="""c=>{diffKey=c.diff||'normal';DIFF=DIFFS[diffKey];run.mode='arcade';run.pilot='maverick';run.stage=c.stage;beginStage(c.stage);setState(GS.PLAY);player.reset();player.invuln=9999;story=null;stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;groundTargetingReset();mapScroll=c.stage===7?s7mEndScroll():2000;player.x=worldWidth()/2;player.y=VH*.80;camX=player.x-VW/2;if(c.mini)spawnSubBoss__inner(c.kind);else spawnBoss(c.kind);window.B=c.mini?subBoss:boss;window.modes=[];window.forms=[];window.moved=0;window.bombs=0;window.enters=0;return {hp:B.hp,max:B.maxhp};}"""
STEP="""n=>{for(let i=0;i<n;i++){let x=B.x,y=B.y,enter=B.enter;player.invuln=999;updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);if(!enter&&B.enter)enters++;moved=Math.max(moved,Math.hypot(B.x-x,B.y-y));let mode=B._bomber?.mode||B._er26?.mode||B._s7mod?.mode;if(!modes.includes(mode))modes.push(mode);if(B._er26&&!forms.includes(B._er26.form))forms.push(B._er26.form);bombs=Math.max(bombs,groundTargetingFx.length);}}"""
def shot(pg,name):
 (OUT/(name+'.png')).write_bytes(base64.b64decode(pg.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1100,'height':1100})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(70)
  p.evaluate("()=>{Object.keys(POLISH_ART).forEach(k=>XART.rdy('polish_'+k));s7mWarm();}")
  p.wait_for_function("()=>Object.keys(POLISH_ART).every(k=>XART.rdy('polish_'+k))")
  report['weapons']=p.evaluate("""()=>{const out=[];run.stage=2;run.pilot='maverick';special=null;run.sonicT=run.dkT=0;run.spaceMode=false;run.weapon=3;run.wlevel=5;run.wvars=[];run.forgeForms={};
    for(const e of [null,...Object.keys(INFUSIONS)]){run.forge=e?{3:{elem:e,lv:1}}:{};run.wvars[3]=e==='fire'?'mavhoming':null;run.infusion=null;pBullets=[];pShoot();out.push({element:e,variant:heldVariant(3),kinds:pBullets.map(q=>q.kind),levels:pBullets.map(q=>q.lv)});}return out;}""")
  report['previews']=p.evaluate("""()=>{const out=[];let sounds=0;const original=Audio.SFX;Audio.SFX=Object.fromEntries(Object.keys(original).map(k=>[k,()=>{sounds++;original[k]?.();}]));try{for(const w of FORGE_WEAPONS)for(const e of Object.keys(INFUSIONS)){const P=forgePreviewNew(w,e,1),before=sounds;for(let j=0;j<90;j++)forgePreviewTick(P,180,180,1/60);out.push({w,e,sounds:sounds-before,fired:P.fired,error:P.err});}}finally{Audio.SFX=original;}return out;}""")
  report['matrix']=[]
  cases=[{'stage':2,'kind':'magmaward','mini':True,'diff':d} for d in ['normal','hard','furious']]+[{'stage':3,'kind':k,'mini':mini,'diff':'furious'} for k,mini in [('frostcruiser',True),('cryospear',False)]]+[{'stage':4,'kind':'stormsovereign','mini':False,'diff':'hard'},{'stage':5,'kind':'siegebomber','mini':True,'diff':'hard'},{'stage':7,'kind':'sludgeemperor','mini':False,'diff':'normal'}]
  for c in cases:
   print('RUN',c,flush=True);p.evaluate(SETUP,c)
   for sec in range(36):
    p.evaluate(STEP,60)
    if sec in [3,6,9,13,20,30]:shot(p,c['kind']+'_'+c['diff']+'_'+str(sec))
    p.wait_for_timeout(15)
   report['matrix'].append(p.evaluate('c=>({c,modes,forms,moved,bombs,enters,hp:B.hp,mode:B._bomber?.mode||B._er26?.mode||B._s7mod?.mode})',c))
   if c['stage']==5:
    report['bomberDamage']=p.evaluate("""()=>{const out=[];for(const part of B._bomber.parts){const p=siegeBomberParts(B).find(p=>p.id===part.id);const before=part.hp;hitSubBoss(31,p.x,p.y);out.push({id:part.id,damage:before-part.hp});}return out;}""")
  p.evaluate("()=>{run.stage=4;run.wlevels=[1,1,1,1,1,1,0,0,0];run.forgeForms={3:{fire:{elem:'fire',lv:1}},0:{ice:{elem:'ice',lv:1}}};armoryOpen('title');setState(GS.ARMORY);}")
  for _ in range(3):p.evaluate(sh.STEP,2);p.wait_for_timeout(200)
  shot(p,'armory');report['collection']=p.evaluate('()=>polishCollection().map(c=>({w:c.w,elem:c.elem,owned:c.owned}))')
  report['errors']=errors;(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');browser.close()
finally:stop()
print(json.dumps({'matrix':report.get('matrix'),'errors':errors,'previewsBad':[r for r in report.get('previews',[]) if r['error'] or not r['sounds']]},indent=2))
assert not errors,errors
assert all(not r['error'] and r['sounds'] for r in report['previews'])
assert all(r['enters']==0 for r in report['matrix'])
