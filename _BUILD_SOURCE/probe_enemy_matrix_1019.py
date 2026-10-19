"""Current native roster x N/H/F. No player fire; full FOV, real controllers."""
from pathlib import Path
import argparse,http.server,json,sys,time
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/enemy_matrix';O.mkdir(parents=True,exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--stages',default='1,2,3,4,5,6,7,8,9');ap.add_argument('--diffs',default='normal,hard,furious');ap.add_argument('--seconds',type=int,default=16);ap.add_argument('--types',default='');ap.add_argument('--label',default='');ap.add_argument('--trace-children',action='store_true');a=ap.parse_args()
if a.label:O=O/a.label;O.mkdir(exist_ok=True)
rows=[];errors=[];rosters={};knownKeys={}
old=O/'report-v1.json'
if not old.exists() and (O/'report.json').exists():old.write_bytes((O/'report.json').read_bytes())
for preload in dict.fromkeys([old,R/'_shots/overnight_combat_1019/enemy_matrix/shipping-final-ai/report.json']):
 if not preload.exists():continue
 for row in json.loads(preload.read_text()).get('rows',[]):
  keys=knownKeys.setdefault(row['stage'],set())
  for bank in row.get('metrics',{}).get('art',{}).values():keys.update(bank)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
def save():
 expected=sum(len(v) for v in rosters.values())
 complete=len(rosters)==27 and len(rows)==expected and not a.types and not errors
 (O/'report.json').write_text(json.dumps(dict(version=6,complete=complete,expected=expected,method='Real Chromium, original authored spawn arguments and attached AI movement state, closest legal stationary camera lane, no player fire, protected pilot. Previous actors and delayed releases are cleared; adaptive and ambush directors are disabled while owned helpers remain. First authored pixels use opaque alpha bounds through the native drawImage transform and canvas clip, sampled every twelve simulation frames. Ordinary projectile ownership is recorded across native per-actor updates; helper and unattributed releases are separate from parent releases. Global native clock covers legacy controllers outside ai27. Separate warning-call and warning-pixel times, authored drawImage calls and real projectile traits. Not human survival evidence.',rows=rows,rosters=rosters,errors=errors),indent=2)+'\n',encoding='utf-8')
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  p.evaluate('''()=>{window.EM19={};const warn=combatWarningTick,warnDraw=combatWarningDraw,play=updatePlay,get=XART.get,draw=ctx.drawImage,enemy=drawEnemy,bullets=drawBullets,tags=new WeakMap(),boxes=new Map(),owners=new WeakMap(),starts=new WeakMap(),begin=ai27Begin,end=ai27End,spawn=spawnEnemy;
   spawnEnemy=function(){const n=enemies.length,r=spawn.apply(this,arguments);if(EM19.live&&window.em19TraceChildren)for(const e of enemies.slice(n))EM19.children.push({time:EM19.age,type:e.type,pattern:e.pattern,owner:ai27Context?.type||null,stack:new Error().stack.split('\\n').slice(2,7)});return r;};
   ai27Begin=function(e){if(EM19.live)starts.set(e,new Set(eBullets));return begin.apply(this,arguments);};
   ai27End=function(e){const known=starts.get(e);if(EM19.live&&known)for(const b of eBullets)if(!known.has(b)&&!owners.has(b))owners.set(b,e);return end.apply(this,arguments);};
   function opaque(im,a,key){const n=a.length,iw=im.naturalWidth||im.width,ih=im.naturalHeight||im.height,sx=n>=9?a[1]:0,sy=n>=9?a[2]:0,sw=n>=9?a[3]:iw,sh=n>=9?a[4]:ih,id=[sx,sy,sw,sh].join(','),bank=key?(boxes.get(key)||new Map()):new Map();if(key)boxes.set(key,bank);let b=bank.get(id);
    if(!b){const c=document.createElement('canvas');c.width=Math.ceil(sw);c.height=Math.ceil(sh);const g=c.getContext('2d');g.drawImage(im,sx,sy,sw,sh,0,0,c.width,c.height);const p=g.getImageData(0,0,c.width,c.height).data;let l=c.width,r=-1,t=c.height,z=-1;
     for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++)if(p[(y*c.width+x)*4+3]>32){l=Math.min(l,x);r=Math.max(r,x);t=Math.min(t,y);z=Math.max(z,y);}b={l:l/c.width,r:(r+1)/c.width,t:t/c.height,b:(z+1)/c.height,empty:r<0};bank.set(id,b);
    }return b;
   }
   XART.get=function(k){const im=get.apply(this,arguments);if(im&&typeof im==='object')tags.set(im,k);return im;};
   if(typeof frenzyPlate==='function'){const plate=frenzyPlate;frenzyPlate=function(e,k){const im=plate.apply(this,arguments);if(im&&typeof im==='object')tags.set(im,k);return im;};}
   ctx.drawImage=function(im){if(EM19.scope&&EM19.live&&im){const key=tags.get(im)||(typeof PXG!=='undefined'?PXG.tags.get(im)?.key:null);EM19.draws++;if(key)EM19.art[EM19.scope].add(key);
    const a=arguments,n=a.length,dx=n>=9?a[5]:a[1],dy=n>=9?a[6]:a[2],w=n>=9?a[7]:n>=5?a[3]:im.width,h=n>=9?a[8]:n>=5?a[4]:im.height,M=this.getTransform(),body=EM19.scope==='enemy'&&!/shadow|fov|alert|muzzle/i.test(key||''),b=body&&EM19.firstPixels==null?opaque(im,a,key):{l:0,r:1,t:0,b:1,empty:false},points=[[dx+w*b.l,dy+h*b.t],[dx+w*b.r,dy+h*b.t],[dx+w*b.l,dy+h*b.b],[dx+w*b.r,dy+h*b.b]].map(([x,y])=>({x:x*M.a+y*M.c+M.e,y:x*M.b+y*M.d+M.f}));
    const visible=!b.empty&&this.globalAlpha>.02&&Math.max(...points.map(q=>q.x))>0&&Math.min(...points.map(q=>q.x))<this.canvas.width&&Math.max(...points.map(q=>q.y))>0&&Math.min(...points.map(q=>q.y))<this.canvas.height;
    if(visible&&EM19.scope==='warning')EM19.firstWarningPixels??=EM19.age;
    if(visible&&body)EM19.firstPixels??=EM19.age;
   }return draw.apply(this,arguments);};
   drawEnemy=function(e){const old=EM19.scope;EM19.scope=typeof E!=='undefined'&&e===E?'enemy':null;try{return enemy.apply(this,arguments);}finally{EM19.scope=old;}};
   drawBullets=function(){const old=EM19.scope;EM19.scope='projectile';try{return bullets.apply(this,arguments);}finally{EM19.scope=old;}};
   updatePlay=function(dt){if(EM19.live)EM19.age+=dt;const r=play.apply(this,arguments);if(EM19.live&&typeof E!=='undefined'&&E){
    const visible=E.x>=camLeftX()&&E.x<=camRightX()&&(E._drawY??E.y)>=PLAY.y&&(E._drawY??E.y)<=VH;
    if(visible){EM19.firstVisible??=EM19.age;EM19.visibleSeconds+=dt;}if(visible&&!E._noHit&&!E.dead)EM19.firstTargetable??=EM19.age;
    EM19.maxOther=Math.max(EM19.maxOther,enemies.filter(e=>e!==E&&!e.dead).length);
    for(const q of eBullets)if(!EM19.seen.has(q)){EM19.seen.add(q);EM19.shots++;EM19.firstProjectile??=EM19.age;const owner=owners.get(q)||(q.owner&&typeof q.owner==='object'?q.owner:null),role=owner===E?'parent':owner?'helper':'unattributed';EM19[role+'Shots']++;if(role==='parent')EM19.firstParentProjectile??=EM19.age;const key=q.kind+'|'+!!q._shootable+'|'+!!q.homing;if(!EM19.traits.some(t=>t.key===key))EM19.traits.push({key,kind:q.kind,w:q.w,h:q.h,speed:Math.hypot(q.vx,q.vy),hp:q.hp,shootable:!!q._shootable,homing:!!q.homing,lock:!!q.lock,proof:enemyDefensiveProof(q),intercept:enemyOrdnanceCanIntercept(q)});}
    for(const q of [...orbBeams,...S81003.beams,...(typeof LL18==='undefined'?[]:LL18.beams)])if(!EM19.seenBeams.has(q)){EM19.seenBeams.add(q);EM19.beams++;EM19.firstBeam??=EM19.age;}
    for(const q of groundTargetingFx)if(!EM19.seenGround.has(q)){EM19.seenGround.add(q);EM19.ground++;EM19.firstGround??=EM19.age;const trait={kind:q.kind,warn:q.warn,radius:q.radius,track:q.track};if(!EM19.groundTraits.some(t=>JSON.stringify(t)===JSON.stringify(trait)))EM19.groundTraits.push(trait);}
   }return r;};
   combatWarningTick=function(owner,key,t,warm){if(EM19.live&&typeof E!=='undefined'&&owner===E){EM19.firstWarning??=EM19.age;let w=EM19.warnings.find(q=>q.key===key);if(w)w.warm=warm;else EM19.warnings.push({key,warm,age:EM19.age});}return warn.apply(this,arguments);};
   combatWarningDraw=function(owner){const old=EM19.scope;if(EM19.live&&(typeof E!=='undefined'&&owner===E||old==='enemy'))EM19.scope='warning';try{return warnDraw.apply(this,arguments);}finally{EM19.scope=old;}};
   window.em19Reset=()=>{EM19={live:true,age:0,draws:0,scope:null,shots:0,parentShots:0,helperShots:0,unattributedShots:0,beams:0,ground:0,visibleSeconds:0,maxOther:0,seen:new WeakSet(),seenBeams:new WeakSet(),seenGround:new WeakSet(),firstPixels:null,firstVisible:null,firstTargetable:null,firstProjectile:null,firstParentProjectile:null,firstWarning:null,firstWarningPixels:null,warnings:[],traits:[],art:{enemy:new Set(),projectile:new Set(),warning:new Set()}};
    VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;Input.keys={};Input.mouse.down=false;s6Wing=null;
    CP12.stage=run.stage;CP12.lastTimer=0;CP12.age=0;
    _adaptiveSpawnT=999999;EM19.children=[];EM19.groundTraits=[];EM19.initialOthers=enemies.filter(e=>e!==E&&!e.dead).map(e=>({type:e.type,pattern:e.pattern,flags:Object.keys(e).filter(k=>/^_[a-z]+\d/.test(k))}));
    // The original isolation fixture used bossWarned=true to disable the boss.
    // Veterans correctly withdraw at that real gameplay gate. Keep it open in
    // this isolated case and move only the test's terminal clock out of reach.
    if(E?._ll18){bossWarned=bossDefeated=false;warnT=0;subBossDone=subBossTriggered=true;curStage={...curStage,length:999999};}
   };
   window.em19Summary=()=>({...EM19,seen:undefined,seenBeams:undefined,seenGround:undefined,art:{enemy:[...EM19.art.enemy],projectile:[...EM19.art.projectile],warning:[...EM19.art.warning]},waves:EA11.rows.filter(q=>q.waveError)});
  }''')
  p.evaluate('v=>window.em19TraceChildren=v',a.trace_children)
  for stage in map(int,a.stages.split(',')):
   for diff in a.diffs.split(','):
    p.evaluate('([s,d])=>EA11.setup(s,d)',[stage,diff]);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game")}',polling=50)
    keys=sorted(knownKeys.get(stage,[]));p.evaluate('(ks)=>ks.forEach(k=>XART.rdy(k))',keys)
    p.wait_for_function('(ks)=>ks.every(k=>XART.rdy(k))',arg=keys,polling=50)
    p.evaluate('EM19.live=false;EA11.rows=[]');specs=p.evaluate('EA11.collect()');errors.extend('collector: '+str(q) for q in p.evaluate('EA11.rows.filter(q=>q.waveError)'));rosters[f'{stage}-{diff}']=specs;print('ROSTER',stage,diff,len(specs),flush=True)
    for index,spec in enumerate(specs):
     if a.types and spec['type'] not in a.types.split(','):continue
     if not p.evaluate('(s)=>EA11.case(s,{nativePlacement:true})',spec):continue
     p.evaluate('EM19.live=false;drawWorld(0)')
     p.wait_for_function('()=>Object.values(XART.img).every(im=>!im||im.complete!==false)',polling=50)
     p.evaluate('em19Reset()');initial=p.evaluate('({hp:E.hp,max:E.maxhp,w:E.w,h:E.h,type:E.type})');q=None;attackCapture=None
     for sec in range(a.seconds):
      for batch in range(5 if spec.get('flight') else 1):
       q=p.evaluate('EA11.step(12)' if spec.get('flight') else 'EA11.step(60)');p.wait_for_timeout(5)
       if spec.get('flight') and attackCapture is None and p.evaluate('EM19.shots+EM19.beams+EM19.ground>0'):
        attackCapture=f'{stage}-{diff}-{index:02}-{spec["flight"]["role"]}-{spec["flight"]["direction"]}-release.jpg';p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit()');p.screenshot(path=str(O/attackCapture),type='jpeg',quality=80)
       if q and q.get('dead'):break
      if q and q.get('dead'):break
     metrics=p.evaluate('em19Summary()');q={**(q or {}),'ai27Shots':(q or {}).get('shots'),'shots':metrics['shots'],'beams':metrics['beams'],'ground':metrics['ground'],'visible':metrics['visibleSeconds'],'age':metrics['age']};row=dict(stage=stage,difficulty=diff,spec=spec,initial=initial,state=q,metrics=metrics);rows.append(row)
     if attackCapture:row['screenshot']=attackCapture
     if index<2 or (not (q or {}).get('shots') and not (q or {}).get('beams') and not (q or {}).get('ground') and not (q or {}).get('ram') and not (q or {}).get('support')):
      if index<2 or (q or {}).get('visible',0)>3:
       name=f'{stage}-{diff}-{index:02}-{spec["type"]}.jpg';p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();');p.screenshot(path=str(O/name),type='jpeg',quality=78);row['screenshot']=name
     save();print('UNIT',stage,diff,spec['type'],json.dumps(dict(ai=spec.get('ai',{}),shots=(q or {}).get('shots'),parent=metrics['parentShots'],helper=metrics['helperShots'],unattributed=metrics['unattributedShots'],beams=(q or {}).get('beams'),ground=(q or {}).get('ground'),firstPixels=metrics['firstPixels'],firstVisible=metrics['firstVisible'],firstProjectile=metrics['firstProjectile'],firstParent=metrics['firstParentProjectile'],firstWarning=metrics['firstWarning'],hp=initial['hp'],finite=(q or {}).get('finite'))),flush=True)
  br.close()
finally:stop();save()
print(json.dumps(dict(cases=len(rows),errors=errors)),flush=True);sys.exit(bool(errors))
