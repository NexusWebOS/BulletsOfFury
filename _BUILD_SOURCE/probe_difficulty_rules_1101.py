"""Native shared15% health/aim/cadence checks and real damaged-pixel verification."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/waves_all_1101';checks=[];errors=[];samples=[]
def ck(n,ok,data=None):
 checks.append(dict(name=n,passed=bool(ok),data=data));(O/'difficulty-checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if ok else'FAIL',n,flush=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
 p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});");p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
 q=p.evaluate('()=>Object.fromEntries(DR15.keys.map(k=>[k,{factor:difficultyEnhancement15(k),hp:DIFFS[k].eHp,fire:DIFFS[k].eFire}]))');ck('Engine curve compounds15% exactly without legacy stacking',abs(q['hard']['factor']-1.15)<1e-9 and abs(q['furious']['factor']/q['hard']['factor']-1.15)<1e-9 and abs(q['hard']['hp']/q['normal']['hp']-1.15)<1e-9 and abs(q['furious']['fire']/q['hard']['fire']-1.15)<1e-9,q)
 for stage in range(1,10):
  p.evaluate('s=>EA11.setup(s,"furious")',stage);specs=p.evaluate('EA11.collect()');data=[]
  for spec in specs:
   if spec['type']in['cloudcarrierbridge','cloudcarrierbay']:continue
   row={}
   for diff in ['normal','hard','furious']:
    z=p.evaluate('q=>{diffKey=q.diff;DIFF=difficultyForRun(run.mode,diffKey);EA11.case(q.spec);return E&&!E.dead?{type:E.type,hp:E.hp,max:E.maxhp||E._maxhp||E.hp,shield:E._esh?.max||0}:null}',dict(diff=diff,spec=spec));row[diff]=z
   if row['normal']and row['hard']and row['furious']:
    valid=all(abs(row[d]['hp']-row['normal']['hp']*(1.15 if d=='hard'else 1.3225))<=max(3,row['normal']['hp']*.008) for d in['hard','furious']);shields=all(abs(row[d]['shield']-row['normal']['shield']*(1.15 if d=='hard'else 1.3225))<=3 for d in['hard','furious'])
    data.append(dict(type=spec['type'],pattern=spec['pattern'],valid=valid,shields=shields,pools=row))
  samples.append(dict(stage=stage,rows=data));(O/'ordinary-health.json').write_text(json.dumps(samples,indent=2));ck('Stage'+str(stage)+' live enemy and shield HP follow one curve',bool(data)and all(x['valid']and x['shields']for x in data),[x for x in data if not x['valid']or not x['shields']])
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}',timeout=180000)
  candidates=[s for s in specs if s['type']not in['cloudcarrierbridge','cloudcarrierbay']]
  chosen=next((s for s in candidates if stage==4 and s['type']=='s4command'),next((s for s in candidates if not s['type'].startswith(('mod','s1truck'))),candidates[0]));p.evaluate('s=>{diffKey="furious";DIFF=difficultyForRun(run.mode,diffKey);EA11.case(s);drawWorld(0)}',chosen);p.wait_for_timeout(150)
  q=p.evaluate('''()=>{E.x=worldWidth()/2;E.y=230;camX=E.x-VW/2;_dmgBullet=null;const pixels=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();const a=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<a.length;i+=4)if(a[i]>235&&a[i+1]>235&&a[i+2]>235&&a[i+3]>180)white++;return white;};const clean=pixels();markHit(E,.09);const hit=pixels();for(let i=0;i<30;i++)updatePlay(1/60);const expired=pixels();drawWorld(0);return{type:E.type,clean,hit,expired,flash:E.flash};}''');p.screenshot(path=str(O/('stage'+str(stage)+'-native-hit.png')));ck('Stage'+str(stage)+' native damaged pixels and expiry remain visible',q['hit']>q['clean']+10 and q['expired']<q['hit']and q['flash']<=0,q)
 # Measure the native turret solver and timer assignment, independently of helpers.
 p.evaluate('EA11.setup(1,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}',timeout=180000)
 row={}
 for diff in ['normal','hard','furious']:
  row[diff]=p.evaluate('''d=>{diffKey=d;DIFF=difficultyForRun(run.mode,d);run.stage=1;bossActive=subBossActive=false;player.x=400;player.y=600;const e={x:300,y:220,w:64,h:64,hp:20,dead:false,_modTurret:{stage:1,weapon:'mg',angle:0,mode:'wait',timer:100}};modularGroundTurretTick(e,1/60);const angle=e._modTurret.angle;e._modTurret={stage:1,weapon:'mg',angle:Math.PI/2,mode:'burst',timer:0,shots:6};modularGroundTurretTick(e,1/60);const gap=e._modTurret.timer;e._modTurret={stage:1,weapon:'mg',angle:Math.PI/2,mode:'wait',timer:0};modularGroundTurretTick(e,1/60);return{angle,gap,warm:e._modTurret.timer,ordinary:eBullets.filter(q=>!q.dead).every(q=>!enemyOrdnanceCanIntercept(q))};}''',diff)
 ck('Actual turret aim step increases15% per selected difficulty',abs(row['hard']['angle']/row['normal']['angle']-1.15)<1e-8 and abs(row['furious']['angle']/row['hard']['angle']-1.15)<1e-8,row)
 ck('Actual native burst gap produces15% faster firing per difficulty',abs(row['normal']['gap']/row['hard']['gap']-1.15)<1e-8 and abs(row['hard']['gap']/row['furious']['gap']-1.15)<1e-8,row)
 ck('Committed warning windows and ordinary bullet interception stay intact',all(abs(z['warm']-.65)<1e-8 and z['ordinary']for z in row.values()),row)
 ck('No runtime or console errors',not errors,errors);b.close()
audit=json.loads((O/'audit-final.json').read_text());before=json.loads((O/'audit-before.json').read_text())
for s,prior in zip(audit['rows'],before['rows']):
 for role in ['mini','boss']:
  ps={z['diff']:z for z in s['pools']if z['role']==role};old=next(z for z in prior['pools']if z['diff']=='normal'and z['role']==role)
  ck('Stage'+str(s['stage'])+' '+role+' Normal baseline and scaled live budget',abs(ps['normal']['max']-old['max'])<=1 and all(abs(ps[d]['max']-ps['normal']['max']*f)<=max(5,ps['normal']['max']*.004)for d,f in [('hard',1.15),('furious',1.3225)]),{d:z['max']for d,z in ps.items()})
print('SUMMARY',sum(q['passed']for q in checks),'/',len(checks));sys.exit(0 if all(q['passed']for q in checks)else 1)
