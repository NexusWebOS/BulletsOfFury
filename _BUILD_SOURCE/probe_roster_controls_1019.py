"""Visibility/ownership controls for the final roster; no production code changes."""
from pathlib import Path
import argparse,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/roster-controls';O.mkdir(parents=True,exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--stage6-only',action='store_true');args=ap.parse_args()
if args.stage6_only:O=O.with_name('roster-controls-stage6');O.mkdir(exist_ok=True)
matrix=json.loads((R/'_shots/overnight_combat_1019/enemy_matrix/shipping-final-ai/report.json').read_text())
rows=[];errors=[];port,stop=shoot.serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=128
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  p.evaluate('''()=>{window.DC19_OFF=1;window.RC19={active:false};const spawn=spawnEnemy,play=updatePlay,begin=ai27Begin,end=ai27End,owners=new WeakMap(),starts=new WeakMap();
   spawnEnemy=function(){const n=enemies.length,r=spawn.apply(this,arguments);if(RC19.active)for(const e of enemies.slice(n))RC19.children.push({time:RC19.time,type:e.type,prop:!!(e.prop||e._prop),pattern:e.pattern,stack:new Error().stack.split('\\n').slice(2,7)});return r;};
   ai27Begin=function(e){if(RC19.active)starts.set(e,new Set(eBullets));return begin.apply(this,arguments);};
   ai27End=function(e){const known=starts.get(e);if(RC19.active&&known)for(const b of eBullets)if(!known.has(b))owners.set(b,e);return end.apply(this,arguments);};
   updatePlay=function(dt){if(RC19.active){RC19.time+=dt;if(RC19.pan){player.x=clamp(E.x,40,worldWidth()-40);camX=clamp(player.x-VW/2,0,worldWidth()-viewW());}}
    const r=play.apply(this,arguments);if(!RC19.active)return r;const visible=E.x>camLeftX()&&E.x<camRightX()&&E.y>PLAY.y&&E.y<VH;if(visible)RC19.visible+=dt;
    const D=E._dr,phase=D?.phase||'none';if(phase!==RC19.last){RC19.phases.push({time:RC19.time,phase,x:E.x,y:E.y,visible});RC19.last=phase;}
    for(const b of eBullets)if(!RC19.seen.has(b)){RC19.seen.add(b);const owner=owners.get(b);RC19.shots.push({time:RC19.time,kind:b.kind,parent:owner===E,owner:owner?.type||null,x:b.x,y:b.y,visible});}
    return r;
   };
   window.rc19Start=pan=>{VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;_adaptiveSpawnT=999999;s6Wing=null;RC19={active:true,time:0,pan,visible:0,shots:[],children:[],phases:[],last:null,seen:new WeakSet()};};
   window.rc19Step=n=>{for(let i=0;i<n&&!E.dead;i++){player.invuln=40002;updatePlay(1/60);if(i%3===0)drawWorld(0);}return{...RC19,seen:undefined,dead:E.dead,ai:E._ai,dr:E._dr?{phase:E._dr.phase,cd:E._dr.cd,pt:E._dr.pt}:null};};
  }''')
  for diff in ([] if args.stage6_only else ['normal','hard','furious']):
   sample=next(q for q in matrix['rows'] if q['stage']==3 and q['difficulty']==diff and q['spec']['type']=='sharddart' and q['spec']['ai']['kind']=='diag')
   for pan in [False,True]:
    p.evaluate('RC19.active=false');p.evaluate('([s,d])=>EA11.setup(s,d)',[3,diff]);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game")}',polling=50);p.evaluate('s=>EA11.case(s,{nativePlacement:true})',sample['spec']);p.evaluate('drawWorld(0)');p.wait_for_function('()=>Object.values(XART.img).every(im=>!im||im.complete!==false)',polling=50);p.evaluate('rc19Start',pan);captured=False
    for i in range(80):
     m=p.evaluate('rc19Step(12)');p.wait_for_timeout(5)
     if m['shots'] and not captured:p.evaluate('shake=0;SC12.refresh();__bofFit()');p.screenshot(path=str(O/f'{diff}-pan-{int(pan)}.jpg'),type='jpeg',quality=80);captured=True
     if m['dead']:break
    rows.append(dict(stage=3,type='sharddart',difficulty=diff,pan=pan,metrics=m));print('DART',diff,pan,len(m['shots']),m['visible'],m['phases'],flush=True)
  for stage,kind in ([(6,'s6dart')] if args.stage6_only else [(1,'s1truckmissile'),(2,'miner')]):
   sample=next(q for q in matrix['rows'] if q['stage']==stage and q['difficulty']=='furious' and q['spec']['type']==kind and (not args.stage6_only or q['metrics']['maxOther']>0))
   p.evaluate('RC19.active=false');p.evaluate('([s,d])=>EA11.setup(s,d)',[stage,'furious']);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game")}',polling=50)
   if args.stage6_only:p.evaluate('EA11.collect()')
   p.evaluate('s=>EA11.case(s,{nativePlacement:true})',sample['spec']);p.evaluate('drawWorld(0)');p.wait_for_function('()=>Object.values(XART.img).every(im=>!im||im.complete!==false)',polling=50);p.evaluate('rc19Start(false)')
   for i in range(80):m=p.evaluate('rc19Step(12)');p.wait_for_timeout(5)
   rows.append(dict(stage=stage,type=kind,difficulty='furious',pan=False,metrics=m));print('OWNER',kind,m['children'],[b for b in m['shots'] if not b['parent']],flush=True)
  br.close()
finally:stop()
(O/'report.json').write_text(json.dumps(dict(method='Native authored diagonal replay; stationary camera versus diagnostic camera following. Following is a visibility positive control, not feasible human movement. Additional child-spawn stacks distinguish environmental actors from parent weapons.',rows=rows,errors=errors),indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(cases=len(rows),errors=errors)),flush=True);sys.exit(bool(errors))
