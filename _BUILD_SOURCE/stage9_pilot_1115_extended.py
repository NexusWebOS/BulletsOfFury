from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage9_pilot_1115';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[];pools={};timelines={}
def ck(n,v,data=None):checks.append({'name':n,'ok':bool(v),'data':data});print(('PASS 'if v else'FAIL ')+n,flush=True)
def step(p,n=6):
 e=p.evaluate(shoot.STEP,n)
 if e:raise RuntimeError(e)
 p.wait_for_timeout(1)
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(240000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8765/index.html?pilot-extended=1115');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(content=(R/'_BUILD_SOURCE/balance_lab_1007.js').read_text(encoding='utf8'))
 for diff in ['normal','hard','furious']:
  p.evaluate("d=>{BAL7.setup({stage:9,kind:'tidalfusion',pilot:'cole',diff:d,mode:'campaign',fire:false});DBGT.god=true;player.invuln=999;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;}",diff)
  p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(9).ready&&Object.values(CB112_ART.banks).every(a=>XART.rdy(a.key))}',polling=50)
  p.evaluate("()=>{boss._ts58.half=true;boss._ts58.protected=false;boss.enter=false;boss.x=worldWidth()/2;boss.y=boss._drawY=155;let n=0;while(boss._w9p15.phase==='ship'&&n++<1000){efxClock+=1/60;hitBoss(10000);}}")
  for i in range(38):step(p)
  pools[diff]=p.evaluate('boss.maxhp');q=p.evaluate('({phase:boss._w9p15.phase,targets:_lockTargets().filter(t=>t._retinaOwner===boss).length,contact:target17BossContact(boss,boss.x,boss.y),shipFX:boss._w9p15.wreck.fx._deathFxStarted,hostFX:!!boss._deathFxStarted})');ck(diff+' pilot handoff, safe body and separate destruction owner',q['phase']=='pilot'and q['targets']>0 and q['contact']is False and q['shipFX']and not q['hostFX'],q)
  # Highest regular primary, held through the actual input owner. God mode is only player survival.
  p.evaluate("()=>{window.START_T=stageTimer;window.FIRE_KEY=keybindFor(1).fire.find(k=>!k.startsWith('mouse'));if(FIRE_KEY)Input.keys[FIRE_KEY]=true;}")
  timeline=[]
  for i in range(500):
   step(p);q=p.evaluate('({phase:boss._w9p15.actor._cb112.phase,hp:boss.hp,dead:boss.dead,t:stageTimer-START_T,score:run.score})');timeline.append(q)
   if q['dead']:break
  p.evaluate('()=>{if(FIRE_KEY)Input.keys[FIRE_KEY]=false;Input.clearTaps();}');timelines[diff]=timeline
  ck(diff+' native primary damages humanoid without Retina',min(v['hp']for v in timeline)<pools[diff],{'hpStart':pools[diff],'end':timeline[-1],'phases':list(dict.fromkeys(v['phase']for v in timeline))})
  p.evaluate("()=>{const e=boss._w9p15.actor;if(!boss.dead){cb112Set(e,'grenade-charge');let n=0;while(!boss.dead&&n++<1000){efxClock+=1/60;hitBoss(10000);}}window.DEAD_BOSS=boss;window.DEAD_SCORE=run.score;bossDie();bossDie();}")
  q=p.evaluate('({dead:DEAD_BOSS.dead,scoreStable:run.score===DEAD_SCORE,finalFX:DEAD_BOSS._deathFxStarted,shipFX:DEAD_BOSS._w9p15.wreck.fx._deathFxStarted})');ck(diff+' final explosion and repeat-defeat guard',q['dead']and q['scoreStable']and q['finalFX']and q['shipFX'],q)
  for i in range(180):
   step(p)
   if p.evaluate('state!==GS.PLAY'):break
  q=p.evaluate('({state,dying:DEAD_BOSS.dying,ending:stageEnding,phase:DEAD_BOSS._w9p15.phase})');ck(diff+' native death timer and stage-clear continue',q['dying']>1 and q['state']!='play',q);p.screenshot(path=str(O/('final-'+diff+'.png')))
 ck('shared15 percent difficulty HP ladder',pools['normal']==2200 and abs(pools['hard']/pools['normal']-1.15)<.002 and abs(pools['furious']/pools['hard']-1.15)<.002,pools)
 ck('no console or page errors',not errors,errors);b.close()
(O/'extended-qa.json').write_text(json.dumps({'checks':checks,'errors':errors,'pools':pools,'timelines':timelines,'scope':'Native primary-input damage, three difficulty handoffs/final destruction and exact once-only terminal score. Player invulnerable; terminal cleanup uses native scripted damage when needed. Not campaign-win or complete balance certification.'},indent=2),encoding='utf8');print(str(sum(c['ok']for c in checks))+'/'+str(len(checks))+' extended checks passed');assert all(c['ok']for c in checks)
