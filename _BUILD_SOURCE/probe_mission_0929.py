"""Real index.html/Chromium renderer. Immunity observes full patterns, not survival balance."""
import sys,os,json,base64,http.server
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import shoot as sh
from playwright.sync_api import sync_playwright

OUT=Path(sh.GAME)/'_shots/mission_0929';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def ok(condition,label):
    checks.append({'label':label,'ok':bool(condition)})
    print(('  ok ' if condition else 'FAIL ')+label,flush=True)

BOOT=r'''() => {
 ht27Stop();debugFight=null;coopOn=false;run.mode='arcade';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');
 window.__observe={keys:{},portals:{},jets:0,hits:0};window.__missionKey=null;window.__portalTag=null;
 const get=XART.get.bind(XART);XART.get=function(k){window.__missionKey=k.startsWith('mission29_')?k:null;return get(k);};
 const draw=ctx.drawImage;ctx.drawImage=function(){const k=window.__missionKey;window.__missionKey=null;
  if(k&&arguments.length===9){const A=Object.values(MISSION29_ART).find(a=>a.key===k);
   const f=A.frames.findIndex(r=>{const s=A.ink?[r[0]+A.ink[0],r[1]+A.ink[1],A.ink[2],A.ink[3]]:r;return s.every((v,i)=>v===arguments[i+1]);});if(f>=0){const d=window.__observe.keys[k]||(window.__observe.keys[k]={});d[f]=(d[f]||0)+1;}}
  if(window.__portalTag!=null){const f=window.__portalTag;window.__observe.portals[f]=(window.__observe.portals[f]||0)+1;}
  return draw.apply(this,arguments);};
 const blit=s7mBlit;s7mBlit=function(name,frame){const old=window.__portalTag;if(name==='portal')window.__portalTag=frame;
  try{return blit.apply(this,arguments);}finally{window.__portalTag=old;}};
 window.playerHit=function(){window.__observe.hits++;};window.__now=performance.now();missionWarm();
}'''
STEP=r'''n => {for(let i=0;i<n;i++){if(player&&!player.dead)player.invuln=0;window.__now+=1000/60;loop(window.__now);}
 return {state,stage:run.stage,t:stageTimer,phase:s6Opening?.phase,ot:s6Opening?.t,done:run._mission29OpeningDone,
  jets:enemies.filter(e=>e._mission29&&!e.dead).length,ground:groundTargetingFx.filter(q=>q._mission29&&!q.dead).length};}'''

def main():
 port,stop=sh.serve(sh.GAME)
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
  pg=br.new_page(viewport={'width':1200,'height':1000})
  pg.on('pageerror',lambda e:errors.append('page: '+str(e)))
  pg.on('console',lambda m:errors.append('console: '+m.text) if m.type=='error' or 'draw error' in m.text else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000)
  pg.wait_for_function('() => (window.__bofFrames|0)>4',timeout=120000)
  pg.evaluate(sh.TRAP_RAF);pg.evaluate(BOOT)
  for i in range(50):
   ready=pg.evaluate('() => Object.values(MISSION29_ART).every(a=>XART.rdy(a.key))&&XART.rdy("s7m_portal")')
   if ready:break
   pg.wait_for_timeout(150)
  ok(ready,'all generated radar/jet cells and nine beam atlases decode')
  def step(n):
   state=None
   while n>0:state=pg.evaluate(STEP,min(n,90));n-=min(n,90);pg.wait_for_timeout(20)
   return state
  def shot(name):
   d=pg.evaluate('() => document.getElementById("screen").toDataURL("image/png")')
   (OUT/(name+'.png')).write_bytes(base64.b64decode(d.split(',',1)[1]))

  # Fresh campaign with real profile history. Save/restore local profile records in this browser.
  fresh=pg.evaluate('''() => {run.mode='campaign';run.forgeElems={fire:1,ice:1};run.forgeForms={3:{ice:{elem:'ice',lv:1}}};run.infusion={elem:'ice',lv:4};
   achievementState.owned.forge_element_ice_E={at:1};achievementState.owned.forge_dark_3_C={at:1};chaingunUnlocked=true;laserMistUnlocked=true;startRun(1);
   return {elements:forgeDiscovered(),forms:ensureForgeForms(),infusion:run.infusion,chain:chaingunIsUnlocked(),mist:laserMistIsUnlocked()};}''')
  ok(not fresh['elements'] and not fresh['forms'] and not fresh['infusion'] and not fresh['chain'] and not fresh['mist'],'real fresh campaign ignores previous unsaved and profile progress')
  pg.evaluate('() => {storySkip();run.mode="arcade";}')

  # Complete actual opening, including normal launch/cloak dialogue. Fast-forward only wall clock.
  pg.evaluate('''() => {diffKey='furious';DIFF=DIFFS.furious;pilotIndex=PILOTS.findIndex(p=>p.key==='cole');startRun(6);}''')
  seen=set();history=[];max_jets=0;max_bombs=0;warning_shot=False;bomb_shot=False;speakers=[]
  for i in range(95):
   s=step(60);phase=s.get('phase');seen.add(phase)
   more=pg.evaluate('''() => ({radio:s6Opening?.radio?.who,lanes:s6Opening?.lanes?.length||0,history:s6Opening?.history||[],
    blind:s6Opening?.phase==='assault'&&groundTargetingFx.some(q=>q._mission29&&!q.impact),timer:stageTimer})''')
   if more['radio']:speakers.append(more['radio'])
   if more['history']:history=more['history']
   max_jets=max(max_jets,s['jets']);max_bombs=max(max_bombs,s['ground'])
   if more['lanes'] and not warning_shot:shot('stage6_horizontal_gates');warning_shot=True
   if more['blind'] and not bomb_shot:shot('stage6_retina_bombers');bomb_shot=True
   if s.get('done'):break
  ok('cloak' in seen and 'flyover' in seen and 'assault' in seen,'natural opening reaches cloak, Harrier and new live assault without teleporting')
  ok('DECKER' in speakers,'Cole opening threat is called by Decker')
  ok(s.get('done') and s['state']=='play','complete Furious assault hands control/progression to normal mission')
  ok(warning_shot and bomb_shot and max_jets>=2 and max_bombs>=2,'side fields, multiple live jets and ground-only bomb retinas actually appear')
  ok(history and history[0]=='lane:west' and 'lane:east' in history and 'bomb:east' in history and 'bomb:west' in history and history[-1]=='lane:south','all authored opening wave families execute in order')
  for diff in ['normal','hard']:
   pg.evaluate('''d=>{diffKey=d;DIFF=DIFFS[d];beginStage(6);setState(GS.PLAY);story=null;enemies=[];eBullets=[];groundTargetingReset();missionAssaultStart();}''',diff)
   s=step(4*60);shot('stage6_'+diff+'_gates')
   ok(pg.evaluate('() => eBullets.length===0&&groundTargetingFx.length===0'),'actual '+diff+' crossing gates do not fire or bomb')

  # Warden cinematic, authored doorway, then anchored escape.
  pg.evaluate('''() => {diffKey='furious';DIFF=DIFFS.furious;run.pilot='decker';beginStage(7);setState(GS.PLAY);story=null;spawnBoss('sludgeemperor');bossActive=true;s7mInit(boss);}''')
  step(2*60);shot('stage7_anomaly_radar')
  ok(pg.evaluate('() => missionIntro(boss)&&boss._s7warden.final.radio?.who==="COLE"'),'Decker pilot receives anomaly warning from Cole')
  step(3*60);shot('stage7_toxic_doorway')
  step(7*60)
  ok(pg.evaluate('() => boss._s7mod._mission29IntroDone&&!["portal","entry"].includes(boss._s7mod.mode)'),'cinematic finishes the authored boss entrance')
  pg.evaluate('() => {s7mSet(boss,"dead");window.__exit=[];}')
  for i in range(20):
   step(60)
   info=pg.evaluate('''() => {const E=boss?._s7mod?.frExit;if(!E)return null;return {t:E.t,y:boss.y,anchor:E.groundY,travel:E.travel,source:_masterSrcY,sy:E.sourceY,
    hidden:boss._s7warden.final.bossHidden,shipHidden:boss._s7warden.final.shipHidden};}''')
   if info:pg.evaluate('x=>window.__exit.push(x)',info)
   if i in [0,8,14,16,17]:shot('stage7_escape_'+str(i))
  exit_log=pg.evaluate('() => window.__exit')
  ok(all(abs(q['y']-q['anchor']-q['travel'])<.001 and abs(q['source']-(q['sy']-q['travel']))<.001 for q in exit_log),'drawn wreck and terrain use the same fixed world anchor through escape')
  ok(any(q['hidden'] for q in exit_log) and any(q['shipHidden'] for q in exit_log),'wreck leaves screen while pilot enters centered toxic door')

  # All nine beams render through actual drawBullets, with source-cell tracking.
  pg.evaluate('''() => {run.mode='arcade';beginStage(1);setState(GS.PLAY);story=null;stagePlan=[];waveIdx=999;enemies=[];pBullets=[];eBullets=[];s6Opening=null;
   for(const k of Object.keys(window.__observe.keys))if(k.startsWith('mission29_beam_'))delete window.__observe.keys[k];}''')
  beam_changes={}
  for elem in ['fire','ice','lightning','kinetic','chrome','dark','toxic','prism','water']:
   imgs=[]
   for f in range(4):
    result=pg.evaluate('''v=>{efxClock=(v.f+.05)/12;pBullets=[{kind:'beam',x:player.x,top:60,bot:player.y-14,w:26,_inf:v.elem,_infLv:1,lv:3}];drawWorld(0);
     return document.getElementById('screen').toDataURL('image/png');}''',{'elem':elem,'f':f})
    imgs.append(result)
    if f==2:(OUT/('laser_'+elem+'.png')).write_bytes(base64.b64decode(result.split(',',1)[1]))
   beam_changes[elem]=len(set(imgs))
  observe=pg.evaluate('() => window.__observe')
  for elem,n in beam_changes.items():
   ok(n==4 and len(observe['keys'].get('mission29_beam_'+elem,{}))==4,elem+' beam shows all four authored source cells and changing pixels')
  # Actual firing and menu demonstration, not only injected render entities.
  for elem in beam_changes:
   live=pg.evaluate('''e=>{run.mode='campaign';run.pilot='cole';run.weapon=3;run.wlevel=3;run.wlevels[3]=3;run.wvars[3]='laserbeam';run.forge={};run.forgeForms={};run.forgeElems={};run.infusion={elem:e,lv:1,hits:0};pBullets=[];pShoot();updatePlay(1/60);drawWorld(0);return pBullets.some(b=>b.kind==='beam'&&b._inf===e);}''',elem)
   ok(live,elem+' temporary infusion fires and draws its real held beam')
   preview=pg.evaluate('''e=>{run._earnedUnlocks={};const before=JSON.stringify(run),P=forgePreviewNew(3,e,1);P.audition=false;
    for(let i=0;i<18;i++)forgePreviewTick(P,260,300,1/30);forgePreviewDraw(P,60,80,260,300);
    return {err:P.err,kind:P.bullets[0]?.kind,isolated:JSON.stringify(run)===before};}''',elem)
   expected='firewhip' if elem=='fire' else 'iceLance' if elem=='ice' else 'beam'
   ok(not preview['err'] and preview['kind']==expected and preview['isolated'],elem+' Forge preview renders its real attack and preserves campaign state')
  p2=pg.evaluate('''()=>{run.mode='campaign';run.pilot='cole';run._earnedUnlocks={};coopOn=true;run2.pilot='yuri';run2._earnedUnlocks={};yuriLightningOrbGrantStage4();let yes=false;withSeat(2,()=>{yes=yuriLightningOrbIsUnlocked();});coopOn=false;return yes;}''')
  ok(p2,'Yuri in player slot two can use the earned campaign Orb')
  ok(len(observe['keys'].get('mission29_radar',{}))==4,'jammed radar animates all four authored frames in the HUD')
  ok(len(observe['keys'].get('mission29_bluejets',{}))==3,'east/west/south jet views render without hull rotation')
  ok(len(observe['portals'])>=8,'upright toxic portal opening/holding/closing frames draw in game')
  ok(not errors,'no page, console, missing assets or draw errors')
  (OUT/'qa.json').write_text(json.dumps({'checks':checks,'errors':errors,'openingHistory':history,'maxJets':max_jets,'maxRetinas':max_bombs,'observe':observe,'escape':exit_log},indent=2))
  br.close()
 stop();failed=sum(not c['ok'] for c in checks);print(f'{len(checks)-failed} passing, {failed} failures',flush=True);return int(bool(failed))

if __name__=='__main__':sys.exit(main())
