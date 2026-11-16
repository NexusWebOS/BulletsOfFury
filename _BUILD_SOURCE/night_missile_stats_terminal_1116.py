from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/missile-stats';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
rows=[];errors=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox'])
 for stage,role in[(1,'mini')]:
  p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(150000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto('http://127.0.0.1:8765/index.html?missile-stats-contract=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
  if not p.evaluate("typeof NMS16!=='undefined'"):p.add_script_tag(path=str(Path(__file__).with_name('night_missile_stats_1116.js')))
  p.evaluate("q=>{BOFOnline.submitScore=()=>{};debugUnlocked=true;BOSSMODE.start(q.stage,q.role,'cole',false,'hard');DBGT.god=true;Input.clearTaps();for(const k of Object.keys(Input.keys))Input.keys[k]=false;}",{'stage':stage,'role':role});p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}')
  for i in range(180):
   if p.evaluate('!!BOFCinematicDirector.active'):p.evaluate("Input.injectTap('enter')")
   e=p.evaluate(shoot.STEP,6);assert not e;p.wait_for_timeout(1)
  q=p.evaluate('''()=>{const b=boss||subBoss,targets=_lockTargets().filter(t=>!t.dead&&t.hp>0),target=targets.find(t=>t._retinaOwner===b)||targets.find(t=>t===b)||targets[0]||b;if(!target)return{missing:true};const noRetina=targets.indexOf(target)<0;const before={hp:target.hp,owner:b.hp,damage:stageStats.dmgDealt,hits:stageStats.mslHits},oldBullet=_dmgBullet,oldSrc=_dmgSrc;
  useBomb(target);const shot=pBullets.findLast(q=>hammerMissile(q));if(!shot)return{noMissile:true};shot.x=target.x;shot.y=target.y;const returns=[];function damage(n,projectile=shot){if(!noRetina)return retinaMissileDamage(target,n,projectile);const qb=_dmgBullet,qs=_dmgSrc;_dmgBullet=projectile;_dmgSrc='missile';try{return b===boss?hitBoss(n):hitSubBoss(n,target.x,target.y);}finally{_dmgBullet=qb;_dmgSrc=qs;}}returns.push(damage(24));const first={hp:target.hp,owner:b.hp,damage:stageStats.dmgDealt,hits:stageStats.mslHits};returns.push(damage(10));const second={hp:target.hp,owner:b.hp,damage:stageStats.dmgDealt,hits:stageStats.mslHits};const contextRestored=_dmgBullet===oldBullet&&_dmgSrc===oldSrc;const valid=before.hp>first.hp||before.owner>first.owner||before.damage<first.damage;
  const sameProjectile=second.hits===first.hits;retinaMissileDamage(null,24,shot);const invalidNoCredit=stageStats.mslHits===second.hits;
  _dmgBullet=null;_dmgSrc=null;const h=stageStats.mslHits;if(b===boss)hitBoss(1);else hitSubBoss(1,b.x,b.y);const primaryNoCredit=stageStats.mslHits===h;_dmgBullet=oldBullet;_dmgSrc=oldSrc;
  const terminalBefore={hp:target.hp,hits:stageStats.mslHits};useBomb(target);const finish=pBullets.findLast(q=>hammerMissile(q));finish.x=target.x;finish.y=target.y;retinaMissileDamage(target,target.hp+100,finish);const terminalAfter={hp:target.hp,dead:target.dead,hits:stageStats.mslHits};retinaMissileDamage(target,10,finish);const terminal={before:terminalBefore,after:terminalAfter,lastHits:stageStats.mslHits,checks:{destroyed:target.dead||target.hp<=0,creditedOnce:terminalAfter.hits===terminalBefore.hits+1,noDeadCredit:stageStats.mslHits===terminalAfter.hits}};
  return{before,first,second,noRetina,terminal,kind:b.kind,target:target.kind||target._retinaId||'hull',returns,valid,checks:{appliedDamageGetsCredit:valid?first.hits===before.hits+1:first.hits===before.hits,sameProjectile,invalidNoCredit,primaryNoCredit,contextRestored},scope:'Native encounter and actual missile factory; controlled native Retina damage calls to test bookkeeping and duplicate splash, not physical impact, boss win or balance.'};}''');q.update({'stage':stage,'role':role});rows.append(q);p.screenshot(path=str(O/f'contract-{stage}-{role}.jpg'),type='jpeg',quality=85);p.close();(O/'terminal.json').write_text(json.dumps({'rows':rows,'errors':errors},indent=2),encoding='utf8');print(json.dumps(q),flush=True)
 b.close()
assert not errors and len(rows)==1 and all(q.get('checks')and all(q['checks'].values())and all(q['terminal']['checks'].values())for q in rows)
