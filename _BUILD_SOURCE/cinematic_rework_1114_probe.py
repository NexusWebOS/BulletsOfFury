from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/cinematic_rework_1114'
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
checks=[];errors=[];samples=[]
def ck(name,ok,data=None):
 checks.append({'name':name,'ok':bool(ok),'data':data})
 if not ok:print('FAIL '+name+' '+str(data),flush=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?cinematic-rework-qa=1114');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{run.mode='campaign';run.pilot='cole';pilotIndex=0;coopOn=false;beginStage(2);warmStage(2);}")
 p.wait_for_function('()=>{stageLoadTick();ls112Warm(2);return stageLoadInfo(2).ready&&ls112Keys(2).every(k=>XART.rdy(k));}',polling=50)
 p.evaluate("()=>{bossActive=subBossActive=false;mapScroll=levelScrollRange();player.x=worldWidth()/2;player.y=VH*.78;BOFCinematicDirector.start(2,()=>{});}")
 p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 p.evaluate("()=>{window.blit16=[];const get=XART.get,draw=ctx.drawImage,seen=new Map();XART.get=function(k){const im=get.apply(this,arguments);seen.set(im,k);return im;};ctx.drawImage=function(im,...args){const k=seen.get(im);if(k&&(k.startsWith('cw16_')||k.startsWith('fchg_')||k==='ls112_stage_2'))blit16.push({key:k,args,transform:Array.from([this.getTransform().a,this.getTransform().d,this.getTransform().e,this.getTransform().f])});return draw.call(this,im,...args);};}")
 for mode,t in [('heat',3),('alert',.5),('alert',2.1),('takeoff',1.3)]:
  p.evaluate('([mode,t])=>{const s=BOFCinematicDirector.current;s.i=s.beats.findIndex(b=>b.service14===mode);s.t=t;s.shown=s.beats[s.i].text.length;blit16=[];}',[mode,t])
  p.evaluate(shoot.STEP,1);q=p.evaluate('({last:SL14.last,draws:blit16,player:{x:player.x,y:player.y}})');samples.append(q)
  p.locator('#screen').screenshot(path=str(OUT/(mode+'-'+str(t)+'.png')))
  ck(mode+str(t)+' no attached fire ring',q['last']['shipFireRing']is False and not any(x['key'].startswith('fchg_')for x in q['draws']))
  if mode!='heat':ck(mode+str(t)+' authored wave actually draws',any(x['key']=='cw16_firewave'for x in q['draws']))
  f=q['last']['framing'];ck(mode+str(t)+' ground camera remains in bounds',f['visible']['left']>=f['inset']and f['visible']['right']<=f['terrainW']-f['inset'])
 ck('ground rumble moves rendered terrain',samples[1]['last']['groundRumble']!=samples[2]['last']['groundRumble'])
 ck('wave moves across ground',samples[1]['last']['fireWave']['y']<samples[2]['last']['fireWave']['y']<samples[3]['last']['fireWave']['y'])
 ck('cinematic does not move gameplay player',all(q['player']==samples[0]['player']for q in samples))
 p.evaluate("()=>D1110.preview('post-3','cole')");p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 rows=p.evaluate('BOFCinematicDirector.current.beats.map((b,i)=>({i,id:b.id,mode:b.cw16,panel:b.panel}))')
 for n in range(6):
  idx=next(q['i']for q in rows if q.get('mode')=='workshop'and q.get('panel')==n)
  p.evaluate('i=>{const s=BOFCinematicDirector.current;s.i=i;s.t=1.4;s.shown=s.beats[i].text.length;blit16=[];}',idx);p.evaluate(shoot.STEP,1)
  q=p.evaluate('({last:CW16.last,draws:blit16})');p.locator('#screen').screenshot(path=str(OUT/('workshop-'+str(n)+'.png')))
  ck('workshop panel '+str(n)+' native drawing',q['last']['panel']==n and any(x['key']=='cw16_workshop'for x in q['draws']),q['last'])
 idx=next(q['i']for q in rows if q.get('mode')=='photon')
 photon=[]
 for t in [1,2.1,3.8,5.1,6.8]:
  p.evaluate('([i,t])=>{const s=BOFCinematicDirector.current;s.i=i;s.t=t;blit16=[];}',[idx,t]);p.evaluate(shoot.STEP,1);q=p.evaluate('({last:CW16.last,draws:blit16})');photon.append(q)
  if t==3.8:p.locator('#screen').screenshot(path=str(OUT/'photon-firing.png'))
 ck('Photon charge burst sustain recovery frames',len({x['last']['frame']for x in photon})>=4,photon)
 ck('Photon actual authored bitmap',all(any(y['key']=='cw16_photon'for y in x['draws'])for x in photon))
 logic=p.evaluate(r"()=>CP15_ART.pilots.map(pk=>{const a=c16Rows('post-3',pk),b=c16Rows('post-4',pk);return{pk,old:[...a,...b].filter(q=>/power cell|recorder\. Every machine heard/i.test(q.text)),three:a.filter(q=>q.upgrade===3).length,four:b.filter(q=>q.upgrade===4).length,crew:[...new Set(a.filter(q=>q.tag==='briefing').map(q=>q.who))],panels:[...new Set(a.filter(q=>q.cw16==='workshop').map(q=>q.panel))]};})")
 for q in logic:ck(q['pk']+' revised story and earned upgrade contracts',not q['old']and q['three']==1 and q['four']==1 and len(q['crew'])==9 and q['panels']==list(range(6)),q)
 p.evaluate('()=>{BOFCinematicDirector.cancel();beginStage(3);warmStage(3);}')
 p.wait_for_function('()=>{stageLoadTick();ls112Warm(3);return stageLoadInfo(3).ready&&ls112Keys(3).every(k=>XART.rdy(k));}',polling=50)
 p.evaluate("()=>{story=null;setState(GS.INTRO);resetIntro();drawLaunch._phase=undefined;Input.clearTaps();last=__bofStepNow=performance.now();}")
 water=[]
 for i in range(125):
  e=p.evaluate(shoot.STEP,10)
  if e:errors.append(e);break
  q=p.evaluate('({state,t:stateT,water:CW16.water,last:LS112.clock.bed})');water.append(q)
  if i in [25,45]:p.locator('#screen').screenshot(path=str(OUT/('water-'+str(i)+'.png')))
  if q['state']=='play'and q['t']>.3:break
 launch=[q for q in water if q['state']=='launch'and q['water'].get('last')]
 ck('Stage3 water moves before PLAY',len({round(q['water']['last']['travel'])for q in launch})>10)
 ck('Stage3 water animates before PLAY',len({q['water']['last']['frame']for q in launch})>=4)
 ck('Stage3 complete arrival handoff',water[-1]['state']=='play'and water[-1]['water']['settled'],water[-1])
 ck('no native page console HTTP errors',not errors,errors);b.close()
(OUT/'native-qa.json').write_text(json.dumps({'checks':checks,'samples':samples,'water':water,'errors':errors},indent=2),encoding='utf-8');print(str(sum(c['ok']for c in checks))+'/'+str(len(checks))+' checks passed',flush=True)
assert all(c['ok']for c in checks)
