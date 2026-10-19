"""Native incoming MG against late heavy hulls. Pool trial stays in the harness.

One actual wave specification per type, native spawn margin and controllers,
stationary protected Cole, held Level-1 machine gun. Not a human balance trial.
"""
from pathlib import Path
import argparse,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--label',default='baseline-trial');ap.add_argument('--seconds',type=int,default=16);ap.add_argument('--arms',default='baseline,authored-trial');ap.add_argument('--candidate',default='');ap.add_argument('--diffs',default='normal,hard,furious');ap.add_argument('--types',default='');a=ap.parse_args()
O=R/'_shots/overnight_combat_1019/heavy_exposure'/a.label;O.mkdir(parents=True,exist_ok=True)
source=json.loads((R/'_shots/overnight_combat_1019/enemy_matrix/report.json').read_text())['rows']
kinds={7:['s7pipe','s7tank','s7barge'],8:['s8interceptor','s8deathorb','s8carrier','s8bomber','s8tentacle']}
rows=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
def save():
 (O/'report.json').write_text(json.dumps(dict(method=__doc__,rows=rows,errors=errors),indent=2)+'\n',encoding='utf-8')
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  if a.candidate:p.add_script_tag(path=str(R/a.candidate))
  p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  p.evaluate('''()=>{window.HE19={live:false};const play=updatePlay,draw=drawEnemy,warning=combatWarningTick,core=_hitEnemyCore,blit=ctx.drawImage,pickup=applyPowerup,cache=new WeakMap();let scope=0;
   applyPowerup=function(q){if(HE19.live){HE19.suppressedPickups.push(q.kind);return;}return pickup.apply(this,arguments);};
   _hitEnemyCore=function(e){if(HE19.live&&e===E&&HE19.gate&&((e._drawY??e.y)<PLAY.y+2||e.x<camLeftX()||e.x>camRightX()))return;return core.apply(this,arguments);};
   ctx.drawImage=function(im){if(scope&&HE19.live&&HE19.firstPixels==null&&im){
    const a=arguments,n=a.length,iw=im.naturalWidth||im.width,ih=im.naturalHeight||im.height,sx=n>=9?a[1]:0,sy=n>=9?a[2]:0,sw=n>=9?a[3]:iw,sh=n>=9?a[4]:ih,dx=n>=9?a[5]:a[1],dy=n>=9?a[6]:a[2],dw=n>=9?a[7]:n>=5?a[3]:iw,dh=n>=9?a[8]:n>=5?a[4]:ih,key=[sx,sy,sw,sh].join(','),bank=cache.get(im)||new Map();cache.set(im,bank);let box=bank.get(key);
    if(!box&&sw>0&&sh>0){const c=document.createElement('canvas');c.width=sw;c.height=sh;const g=c.getContext('2d');g.drawImage(im,sx,sy,sw,sh,0,0,sw,sh);const px=g.getImageData(0,0,sw,sh).data;let l=sw,r=-1,t=sh,b=-1;for(let y=0;y<sh;y++)for(let x=0;x<sw;x++)if(px[(y*sw+x)*4+3]>32){l=Math.min(l,x);r=Math.max(r,x);t=Math.min(t,y);b=Math.max(b,y);}box={l,r,t,b};bank.set(key,box);}
    if(box&&box.r>=0&&this.globalAlpha>.02){const M=this.getTransform(),xs=[dx+dw*box.l/sw,dx+dw*(box.r+1)/sw],ys=[dy+dh*box.t/sh,dy+dh*(box.b+1)/sh],v=xs.flatMap(x=>ys.map(y=>({x:x*M.a+y*M.c+M.e,y:x*M.b+y*M.d+M.f})));
     if(Math.max(...v.map(q=>q.x))>0&&Math.min(...v.map(q=>q.x))<cv.width&&Math.max(...v.map(q=>q.y))>PLAY.y*SS&&Math.min(...v.map(q=>q.y))<cv.height)HE19.firstPixels=HE19.time;
    }
   }return blit.apply(this,arguments);};
   combatWarningTick=function(owner){if(HE19.live&&owner===E)HE19.firstWarning??=HE19.time;return warning.apply(this,arguments);};
   drawEnemy=function(e){if(HE19.live&&e===E&&e.y>=PLAY.y&&e.y<=VH)HE19.firstVisible??=HE19.time;if(e===E)scope++;try{return draw.apply(this,arguments);}finally{if(e===E)scope--;}};
   updatePlay=function(dt){if(HE19.live){HE19.time+=dt;Input.keys.j=true;player.invuln=40002;}
    const r=play.apply(this,arguments);if(HE19.live){if(E.hp<HE19.lastHP){HE19.damage+=HE19.lastHP-E.hp;HE19.firstDamage??=HE19.time;}HE19.lastHP=E.hp;
     for(const q of pBullets)if(!HE19.seenP.has(q)){HE19.seenP.add(q);HE19.playerRounds++;HE19.playerKinds[q.kind]=(HE19.playerKinds[q.kind]||0)+1;}
     for(const q of eBullets)if(!HE19.seen.has(q)){HE19.seen.add(q);HE19.rounds++;HE19.firstRound??=HE19.time;}
     HE19.peak=Math.max(HE19.peak,eBullets.length);HE19.finite&&=[E,...eBullets,...pBullets].every(q=>Number.isFinite(q.x+q.y));
     if(E.dead||E._dyingT!=null)HE19.died??=HE19.time;
    }return r;};
   window.he19Summary=()=>({...HE19,seen:undefined,seenP:undefined,hp:E.hp,dead:!!E.dead||E._dyingT!=null,helpers:enemies.filter(q=>q!==E&&!q.dead).length,weapon:run.weapon,level:run.wlevel,pilot:run.pilot});
  }''')
  for stage,types in kinds.items():
   for diff in a.diffs.split(','):
    p.evaluate('([s,d])=>EA11.setup(s,d)',[stage,diff]);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game")}',polling=50)
    for kind in types:
     if a.types and kind not in a.types.split(','):continue
     spec=next(q['spec'] for q in source if q['stage']==stage and q['difficulty']==diff and q['spec']['type']==kind)
     for arm in a.arms.split(','):
      p.evaluate('arm=>{HE19.live=false;window.LF19_OFF=arm==="baseline"?1:0;}',arm);p.evaluate('([s,d])=>EA11.setup(s,d)',[stage,diff]);p.evaluate('(s)=>EA11.case(s)',spec)
      initial=p.evaluate('''arm=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');PILOTMOD={...PILOTS[pilotIndex]};run.weapon=0;run.wlevel=1;run.wlevels=WEAPONS.map(()=>0);run.wlevels[0]=1;run.spaceMode=false;run.infusion=null;run.forge={};run.forgeForms={};run.loadout=[0];
       // Stages 6-8 default to Chaingun even for Cole under the authored October
       // 3 progression rule. Select MG through its real loadout-form API.
       if(weaponFormSelect(0,{kind:'primary1003b',id:'mg'})!=='ok')throw Error('Native MG loadout selection failed');
       player.reset();special=thunderStorm=null;run.sonicT=run.dkT=0;
       VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;spawnClock=999999;stagePlan=[];s6Wing=null;
       // Input.down owns the original keys map in its closure. Mutate that map;
       // replacing Input.keys only changes the exposed property, not held input.
       for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.keys.j=true;Input.mouse.down=false;player.fireCd=0;run.missileLevel=0;
       if(!Input.hold(1,'fire'))throw Error('Held primary input did not reach the native key map');
       const spec=run.stage===7?S7TOXIC[E._s7toxic]:S8MEGA[E._s8mega],before=E.hp,heavy=spec.hp>=40;
       if(['authored-trial','combined-trial'].includes(arm)&&heavy){const saved=diffKey,current=EHP(spec.hp);let normal;try{diffKey='normal';normal=EHP(spec.hp);}finally{diffKey=saved;}E.hp=E.maxhp=E._maxhp=Math.max(before,Math.round(spec.hp*current/Math.max(1,normal)));}
       player.x=E.x;player.y=VH*.80;camX=clamp(player.x-VW/2,0,worldWidth()-VW);pBullets=[];eBullets=[];player.fireCd=0;
       HE19={live:true,gate:['visible-trial','combined-trial'].includes(arm),time:0,firstPixels:null,firstVisible:null,firstWarning:null,firstRound:null,firstDamage:null,died:null,lastHP:E.hp,damage:0,rounds:0,playerRounds:0,playerKinds:{},suppressedPickups:[],peak:0,seen:new WeakSet(),seenP:new WeakSet(),finite:true};return{before,hp:E.hp,authored:spec.hp,heavy,x:E.x,y:E.y};}''',arm)
      p.evaluate('HE19.live=false;drawEnemy(E)');p.wait_for_function('()=>Object.values(XART.img).every(im=>!im||im.complete!==false)',polling=50);p.evaluate('HE19.live=true')
      for tick in range(a.seconds*5):
       p.evaluate(shoot.STEP,12);p.wait_for_timeout(4)
       if p.evaluate('HE19.died!=null'):break
      metrics=p.evaluate('he19Summary()');row=dict(stage=stage,difficulty=diff,kind=kind,arm=arm,initial=initial,metrics=metrics);rows.append(row)
      if not metrics['playerRounds']:errors.append(f'{stage}-{diff}-{kind}-{arm}: no actual primary rounds; invalid incoming-fire fixture')
      if metrics['weapon']!=0 or metrics['level']!=1:errors.append(f'{stage}-{diff}-{kind}-{arm}: primary gear changed during isolated sample')
      if diff=='normal':
       p.evaluate('HE19.live=false;shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit()');name=f'{stage}-{kind}-{arm}.jpg';p.screenshot(path=str(O/name),type='jpeg',quality=75);row['screenshot']=name
      save();print('CASE',stage,diff,kind,arm,json.dumps(dict(hp=initial['hp'],pixels=metrics['firstPixels'],centerVisible=metrics['firstVisible'],warning=metrics['firstWarning'],round=metrics['firstRound'],death=metrics['died'],damage=metrics['damage'],playerRounds=metrics['playerRounds'],finite=metrics['finite'])),flush=True)
  HE=None;br.close()
finally:stop();save()
print(json.dumps(dict(cases=len(rows),errors=errors)),flush=True);sys.exit(bool(errors))
