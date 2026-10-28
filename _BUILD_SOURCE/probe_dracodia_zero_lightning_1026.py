from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/dracodia_zero_lightning_1026/probe';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from barrage_review_common_1025 import boot,advance;from shoot import serve,STEP
port,stop=serve(str(R));errors=[]
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(b.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&bi24Warm()&&r25Warm(8)&&rd26Ready()&&rd28Ready()}',timeout=180000)
  assert advance(p,"boss._r30.mode==='fight'&&j3State(boss).encounter===0",1000,12)
  p.evaluate("()=>{Snd.vol.sfx=0;RD27.audio=[];RB23.events=[];for(const q of boss.parts.filter(q=>q.id!=='core')){boss._lastPart=q;modularHit(q.hp+1);}boss._lastPart=boss.parts[0];modularHit(boss.parts[0].hp+1);}")
  assert advance(p,'boss._r30.t>=13.97',1000,1)
  before=p.evaluate('({t:boss._r30.t,bolts:boss._r30.v18.rb23Rebirth.bolts})')
  assert advance(p,'boss._r30.t>=14',10,1)
  p.evaluate('drawWorld(0)');p.screenshot(path=str(W/'download-zero.png'))
  zero=p.evaluate("()=>({t:boss._r30.t,progress:RD25.last.progress,bolts:boss._r30.v18.rb23Rebirth.bolts,strikes:RD26.fx.strikes.length,wrap:RD26.fx.front.length+RD26.fx.back.length,audio:RD27.audio.slice(),ownPool:Snd.pools.rd27Lightning!==Snd.pools.combatBeam0927,gain:Snd.TAME.rd27Lightning.g,otherGain:Snd.TAME.combatBeam0927.g})")
  assert advance(p,'boss._r30.t>=23.1',1000,1)
  late=p.evaluate("()=>({bolts:boss._r30.v18.rb23Rebirth.bolts,audio:RD27.audio.slice(),wrap:RD26.fx.front.length+RD26.fx.back.length})")
  muted=p.evaluate("()=>{rd27Thunder(boss,999,'muted-test');const pool=Snd.pools.rd27Lightning;const m=pool.slots.filter(v=>v?.attached&&!v.el.paused).every(v=>v.el.volume===0);setState('paused');return{muted:m,stopped:pool.slots.every(v=>!v?.el||v.el.paused)}}")
  native=[q for q in late['audio']if q['kind']=='native'];checks={'noLightningBeforeDownload':before['bolts']==0,'firstStrikeAtZeroPercent':int(zero['progress']*100)==0 and zero['bolts']==1,'lightningAndWrapVisibleAtZero':zero['strikes']>0 and zero['wrap']>0,'firstStrikeHasOwnAudio':len(zero['audio'])==1 and zero['audio'][0]['played'],'formationPoolIsIndependent':zero['ownPool'],'formationGainRaised':zero['gain']>zero['otherGain'],'all24NativeBeatsRetained':late['bolts']==24 and len(native)==23,'eachEarlyStrikePlaysOnce':len({q['beat']for q in native})==23,'endingStormStillPlays':any(q['kind']=='ending'and q['beat']==24 for q in late['audio']),'wrapBuildsWithDownload':late['wrap']>zero['wrap'],'sfxMuteRespected':muted['muted'],'pauseStopsFormationAudio':muted['stopped'],'noRuntimeErrors':not [e for e in errors if 'ERR_NETWORK_IO_SUSPENDED'not in e]}
  (W/'checks.json').write_text(json.dumps({'checks':checks,'before':before,'zero':zero,'late':late,'errors':errors},indent=2));print(json.dumps(checks),flush=True);b.close();assert all(checks.values())
finally:stop()
