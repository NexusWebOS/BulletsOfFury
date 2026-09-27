"""Actual Chromium renders, part damage routing, ground limits, and menu navigation."""
import json,base64,sys
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/toxic_modular_0927');OUT.mkdir(parents=True,exist_ok=True)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60)}')
 (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
SETUP=r'''c=>{diffKey=c.diff||'normal';DIFF=DIFFS[diffKey];run.mode='arcade';run.pilot='cole';run.stage=7;curStage=STAGES[6];beginStage(7);setState(GS.PLAY);player.reset();player.invuln=9999;story=null;stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;groundTargetingReset();mapScroll=c.mini?2500:s7mEndScroll();player.x=worldWidth()/2;player.y=VH*.80;camX=player.x-VW/2;if(c.mini)spawnSubBoss__inner('dualscoopdredger');else spawnBoss('sludgeemperor');window.B=c.mini?subBoss:boss;s7mInit(B);B._be=null;s7mWarm();window.proof={modes:[],parts:[],kinds:[],maxMove:0,errors:[],bounds:0,scrollStart:mapScroll};return{world:worldWidth(),vw:VW,vh:VH,hp:B.hp};}'''
STEP=r'''n=>{for(let j=0;j<n;j++){player.invuln=10;let x=B.x,y=B.y;updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);proof.maxMove=Math.max(proof.maxMove,Math.hypot(B.x-x,B.y-y));if(!proof.modes.includes(B._s7mod.mode))proof.modes.push(B._s7mod.mode);for(const q of eBullets){if(!proof.kinds.includes(q.kind))proof.kinds.push(q.kind);if(!Number.isFinite(q.x+q.y+q.vx+q.vy))proof.errors.push('nonfinite projectile');}if(B._s7mod.tank&&B._s7mod.mode!=='entry'&&(B.x-B.w/2<worldWidth()*.345-.1||B.x+B.w/2>worldWidth()*.655+.1))proof.bounds++;}}'''
def run():
 port,stop=sh.serve(sh.GAME);errs=[];report={'matrix':[]}
 try:
  with sync_playwright() as pw:
   browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=browser.new_page(viewport={'width':1100,'height':1100})
   p.on('pageerror',lambda e:errs.append(str(e)));p.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
   for mini in [True,False]:
    for diff in ['normal','hard','furious']:
     print('RUN',mini,diff,flush=True);p.evaluate(SETUP,{'mini':mini,'diff':diff});p.wait_for_function("()=>Object.keys(S7M_ART).map(k=>XART.rdy('s7m_'+k)).every(Boolean)",timeout=60000)
     for sec in range(50):
      p.evaluate(STEP,60)
      if sec in [0,3,6,10,16,23,32,43] and diff=='normal':shot(p,('tank' if mini else 'warden')+'_'+str(sec))
      if sec%4==0:p.wait_for_timeout(15)
     if not mini:
      report.setdefault('destruction',[])
      for ids in [['gunL'],['frontL'],['frontR'],['rearL'],['rearR'],['shield'],['gunR'],['core']]:
       for id in ids:
        check=p.evaluate(r'''id=>{s7mSet(B,'recover');const M=B._s7mod;let before={phase:s7mStage(M),hp:B.hp,shield:bossShieldFrac(B)};if(id==='shield')s7mHit(B,1e6,0,0,'core');else s7mHit(B,1e6,0,0,id);return{id,before,after:{phase:s7mStage(M),mode:M.mode,hp:B.hp,shield:bossShieldFrac(B),parts:M.parts.map(p=>[p.id,p.hp]),targets:s7mTargets(B).map(p=>p.name)}};}''',id)
        report['destruction'].append(check);p.evaluate(STEP,35);shot(p,'break_'+id+'_'+diff)
      p.evaluate(STEP,220)
     report['matrix'].append(p.evaluate('()=>({...proof,tank:B._s7mod.tank,diff:diffKey,scrollEnd:mapScroll,dead:B.dead,state,history:B._s7mod.history})'))
   p.evaluate('()=>{setState(GS.PASSWORD);drawPassword.sel=36;drawPassword.typing=false;drawPassword(0)}')
   p.screenshot(path=str(OUT/'password.png'))
   p.evaluate('()=>{setState(GS.OPENER);opnI=OPN.length-1;opnT=4;drawOpener(0)}');p.wait_for_timeout(1200);p.evaluate('()=>drawOpener(0)');p.screenshot(path=str(OUT/'cover.png'))
   report['errors']=errs;(OUT/'report.json').write_text(json.dumps(report,indent=2));browser.close()
 finally:stop()
 print(json.dumps(report,indent=2));assert not errs,errs
 assert all(not r['errors'] and not r['bounds'] for r in report['matrix'])
if __name__=='__main__':run()
