"""Current Stage 8 forms: native attacks, actual body blits, beams and cues."""
from pathlib import Path
import argparse,ast,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/forms';O.mkdir(parents=True,exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--scenes',default='colossus,hammer,helicopter,harrier,volcano,volcano-head');ap.add_argument('--seconds',type=int,default=36);ap.add_argument('--label',default='');a=ap.parse_args()
if a.label:O=O/a.label;O.mkdir(exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
cases=[];errors=[];port,stop=shoot.serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=128
def save():(O/'report.json').write_text(json.dumps(dict(method=f'Real Chromium, explicit phase fixtures x N/H/F, up to {a.seconds} native simulated seconds each, no player fire. Initial form is selected for isolation; no forced kills or phase changes during the sample. Visible protected pilot follows a fixed route. Body keys and rotations are actual native rig/blits, not sprite names inferred from disk. Audio numbers are cue invocations; the test browser is muted.',cases=cases,errors=errors),indent=2)+'\n',encoding='utf-8')
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{window.FA19={};const beam=av3Beam,warn=combatWarningTick,get=XART.get,draw=ctx.drawImage,tags=new WeakMap();
   av3Beam=function(){if(FA19.live&&FA19.drawScope){FA19.firstBeamPixels??=FA19.time;FA19.beamBlits++;const family=String(arguments[6]);FA19.beamFamilies[family]=(FA19.beamFamilies[family]||0)+1;}return beam.apply(this,arguments);};
   combatWarningTick=function(owner,key,t,warm){if(FA19.live){FA19.firstWarning??=FA19.time;const k=String(key);if(!FA19.warnings.some(q=>q.key===k))FA19.warnings.push({key:k,time:FA19.time,warm});}return warn.apply(this,arguments);};
   XART.get=function(key){const im=get.apply(this,arguments);if(im&&typeof im==='object')tags.set(im,key);return im;};
   ctx.drawImage=function(im){if(FA19.live&&FA19.drawScope){const key=tags.get(im)||(typeof PXG!=='undefined'?PXG.tags.get(im)?.key:null);if(key){FA19.drawKeys[key]=(FA19.drawKeys[key]||0)+1;if(FA19.rigKeys?.has(key))FA19.bodyDrawKeys[key]=(FA19.bodyDrawKeys[key]||0)+1;}}return draw.apply(this,arguments);};
   for(const key of Object.keys(Audio.SFX)){const f=Audio.SFX[key];if(typeof f==='function')Audio.SFX[key]=function(){if(FA19.live)FA19.sounds[key]=(FA19.sounds[key]||0)+1;return f.apply(this,arguments);};}
   window.fa19Step=n=>{for(let i=0;i<n;i++){if(FA19.finishedByMorph)return;FA19.time+=1/60;const t=FA19.time;player.invuln=1e9;Input.keys={};Input.mouse.down=false;player.x=camLeftX()+viewW()/2+Math.sin(t*.7)*100;player.y=VH-105+Math.sin(t*.9)*20;updatePlay(1/60);if(B._r30.v18.form!==FA19.form){FA19.finishedByMorph=true;return;}
    for(const q of eBullets)if(!FA19.seen.has(q)){FA19.seen.add(q);FA19.firstProjectile??=t;FA19.shots++;FA19.kinds[q.kind]=(FA19.kinds[q.kind]||0)+1;}
    FA19.peakProjectiles=Math.max(FA19.peakProjectiles,eBullets.filter(q=>!q.dead).length);
    for(const q of groundTargetingFx)if(!FA19.seenGround.has(q)){FA19.seenGround.add(q);FA19.ground++;}
    const form=B._r30.v18.form,donor=j3State(B).gp4Donors?.[form]?.p,phase=B._r30.mode+':'+(donor?._hammer?.state||donor?._fz?.phase||B._r30.v18.attack?.type||'');if(phase!==FA19.lastPhase){FA19.phases.push({time:t,mode:B._r30.mode,form,hammer:form===8?donor?._hammer?.state:null,volcano:form===2?donor?._fz?.phase:null});FA19.lastPhase=phase;}
    const rig=v18Rig(B);for(const v of rig){const a=FA19.modules[v.p.id]??={keys:[],minRot:Infinity,maxRot:-Infinity,minX:Infinity,maxX:-Infinity};if(!v.spec.hidden&&!a.keys.includes(v.key))a.keys.push(v.key);a.minRot=Math.min(a.minRot,v.rot||0);a.maxRot=Math.max(a.maxRot,v.rot||0);a.minX=Math.min(a.minX,v.x);a.maxX=Math.max(a.maxX,v.x);if(!v.spec.hidden){const states=FA19.stateKeys??={},keys=states[phase]??=[];if(!keys.includes(v.key))keys.push(v.key);}}
    if(i%12===0){FA19.rigKeys=new Set(rig.filter(v=>!v.spec.hidden).map(v=>v.key));FA19.drawScope=true;drawWorld(1/60);FA19.drawScope=false;}
   }};window.fa19Summary=()=>({...FA19,seen:undefined,seenGround:undefined,rigKeys:undefined,final:{mode:B._r30.mode,form:B._r30.v18.form,hp:B.hp,dead:B.dead},events:V19.events,archives:D20.events});
  }''')
  for scene,form,head in [('colossus',0,False),('hammer',8,False),('helicopter',1,False),('harrier',6,False),('volcano',2,False),('volcano-head',2,True)]:
   if scene not in a.scenes.split(','):continue
   for diff in ['normal','hard','furious']:
    print('RUN',scene,diff,flush=True);p.evaluate(SETUP,dict(stage=8,kind='vileexistence',diff=diff,pilot='cole'))
    p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&d20Warm()&&bmfReady("game")}',polling=50)
    p.evaluate('''o=>{v18Budget(B);v18Enter(B,2,o.form);v18Fight(B);B.enter=B._noHit=false;B.x=worldWidth()/2;B.y=PLAY.y+150;B._drawY=B.y;
     if(o.head){const F=gd4Create(B,2).p._fz;for(const q of B.parts)if(q.id!=='head'){q.hp=0;q.destroyed=true;F.pools[q.id==='core'?'body':q.id]=0;}furnaceEnter(gd4Create(B,2).p,'head');F.trans=0;B.hp=gd4Create(B,2).p.hp=F.pools.head;}
     H3.release=false;H3.ending=null;fb2Talk=fb2Intro=thaw=s6Opening=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=null;P2M.active=null;stagePlan=[];spawnClock=999999;warnT=0;warnKind=null;bossWarned=true;subBossTriggered=aminiTriggered=true;VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;enemies=[];eBullets=[];pBullets=[];powerups=[];run.shield=0;special=thunderStorm=null;run.sonicT=run.dkT=0;
     V19.events=[];D20.events=[];FA19={live:true,form:o.form,time:0,shots:0,peakProjectiles:0,kinds:{},sounds:{},beamFamilies:{},beamBlits:0,firstBeamPixels:null,firstWarning:null,firstProjectile:null,warnings:[],ground:0,modules:{},drawKeys:{},bodyDrawKeys:{},phases:[],seen:new WeakSet(),seenGround:new WeakSet()};SC12.refresh();__bofFit();}''',dict(form=form,head=head))
    for sec in range(a.seconds):
     for batch in range(5):p.evaluate('fa19Step(12)');p.wait_for_timeout(5)
     if sec in [2,9,19,a.seconds-1]:
      p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();');p.screenshot(path=str(O/f'{scene}-{diff}-{sec+1:02}.jpg'),type='jpeg',quality=83)
     if p.evaluate('!!FA19.finishedByMorph'):break
    row=p.evaluate('fa19Summary()');cases.append(dict(scene=scene,form=form,difficulty=diff,metrics=row));save();print('END',scene,diff,json.dumps(dict(shots=row['shots'],first=row['firstProjectile'],firstBeam=row['firstBeamPixels'],bodyDrawKeys=len(row['bodyDrawKeys']),modules={k:len(v['keys']) for k,v in row['modules'].items()},sounds=row['sounds'])),flush=True)
  br.close()
finally:stop();save()
print(json.dumps(dict(cases=len(cases),errors=errors)),flush=True);sys.exit(bool(errors))
