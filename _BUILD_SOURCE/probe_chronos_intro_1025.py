"""Native opening: dialogue hold -> authored armor charge/lock -> first attack."""
from pathlib import Path
import base64,json
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP

R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_contract_1025/intro';O.mkdir(exist_ok=True)
checks=[];errors=[];runs=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 if not ok:print(json.dumps(data),flush=True)

port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required'])
  p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(30)
  p.evaluate("""()=>{window.orderEvents=[];window.orderChargeFrames=new Set();window.orderIntroEnds=[];const state=hammerState,paint=b20Image,end=fb2IntroEnd;fb2IntroEnd=function(){const first=fb2Intro&&!fb2Intro.done,b=fb2Intro?.boss;const r=end.apply(this,arguments);if(first&&b===boss)orderIntroEnds.push(efxClock);return r;};hammerState=function(b,s){if(b===boss)orderEvents.push({to:s,time:efxClock,intro:fb2IntroActive(),done:!!fb2Intro?.done,armor:!!fr27Armor(b)?.activated,hp:b.hp,maxhp:b.maxhp});return state.apply(this,arguments);};b20Image=function(a){if(boss?._hammer?.state==='fr_activation'&&(a.key.startsWith('c27_activation_')))orderChargeFrames.add(a.key);return paint.apply(this,arguments);};}""")
  for mode,diff in [('arcade','normal'),('arcade','hard'),('arcade','furious'),('campaign','furious')]:
   label=mode+'-'+diff
   p.evaluate("""([mode,diff])=>{diffKey=diff;debugStartFight({stage:5,role:'boss',kind:'chromehammer',name:'Chronos'},{pilot:'cole'});run.mode=mode;orderEvents.length=0;orderChargeFrames.clear();orderIntroEnds.length=0;player.invuln=999;bi24Warm();}""",[mode,diff])
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()&&ch23Warm()&&UI20_KEYS.every(k=>XART.rdy(k))}',timeout=180000)
   samples=[];seen=set();attack=None;intro_shot=False;charge_shots=set();end_time=None;motion=None
   for step in range(700):
    p.evaluate(STEP,6)
    q=p.evaluate("""()=>{player.invuln=999;const h=boss?._hammer,A=fr27Armor(boss);return{time:efxClock,state:h?.state,t:h?.t,intro:fb2IntroActive(),introDone:!!fb2Intro?.done,beat:fb2Intro?.i,bullets:eBullets.length,armor:!!A,activated:!!A?.activated,armorMax:A?.max,maxhp:boss?.maxhp,scroll:_stage5SpaceScroll,x:player.x,bx:boss?.x,by:boss?.y,frame:h?ha21Blue(boss)?.a.key:null};}""")
    samples.append(q)
    if q.get('state'):seen.add(q['state'])
    if q['intro'] and not intro_shot:
     intro_shot=True;p.screenshot(path=str(O/(label+'-dialogue.png')))
     before=q.copy();p.keyboard.down('d');p.evaluate(STEP,18);p.keyboard.up('d')
     after=p.evaluate('()=>({x:player.x,scroll:_stage5SpaceScroll})');motion=dict(before=before,after=after)
    if q['state']=='fr_activation':
     phase='charge' if q['t']<1 else 'lock' if q['t']>2.35 else 'forming'
     if phase not in charge_shots:
      charge_shots.add(phase);p.screenshot(path=str(O/(label+'-'+phase+'.png')))
    if not q['intro'] and intro_shot and end_time is None:end_time=q['time']
    if q.get('state') not in [None,'flyby','return','unfold','hammer','fr_activation']:
     attack=q;p.screenshot(path=str(O/(label+'-first-attack.png')));break
    if step%15==0:p.wait_for_timeout(5)
   events=p.evaluate('orderEvents');frames=p.evaluate('Array.from(orderChargeFrames)');ends=p.evaluate('orderIntroEnds')
   intro=[s for s in samples if s['intro']];charge=[s for s in samples if s.get('state')=='fr_activation'];activations=[e for e in events if e['to']=='fr_activation']
   ck(label+' no attacks or armor during opening dialogue',bool(intro) and all(s.get('state')=='unfold' and not s['armor'] and s['bullets']==0 and s['frame']=='c27_takeoff_regular_0' for s in intro),dict(states=sorted(seen),introSamples=len(intro),violations=[s for s in intro if s.get('state')!='unfold' or s['armor'] or s['bullets']]))
   ck(label+' dialogue finishes before armor begins',bool(activations) and len(ends)==1 and ends[0]<=activations[0]['time'] and not activations[0]['intro'],dict(activations=activations,introEnds=ends))
   ck(label+' full visible armor animation completes before first attack',bool(attack) and attack['activated'] and len(frames)>=6 and len(charge)>=25 and end_time is not None and attack['time']>end_time+2.8,dict(attack=attack,frames=frames,chargeSamples=len(charge),dialogueEnd=end_time))
   ck(label+' world scroll and player movement continue during dialogue',bool(motion) and motion['after']['scroll']>motion['before']['scroll']+50 and motion['after']['x']>motion['before']['x']+10,motion)
   expected=(attack or {}).get('maxhp',0)*{'normal':.30,'hard':.60,'furious':.75}[diff]
   ck(label+' preserves difficulty-scaled armor budget',bool(attack) and abs(attack['armorMax']-expected)<.01,dict(actual=(attack or {}).get('armorMax'),expected=expected))
   runs.append(dict(label=label,events=events,samples=samples,chargeFrames=frames))
  ck('No page or console errors',not errors,errors);br.close()
finally:stop()
result=dict(checks=checks,runs=runs,errors=errors,passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks))
(O/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(passed=result['passed'],failed=result['failed'])),flush=True)
raise SystemExit(0 if not result['failed'] else 1)
