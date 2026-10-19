"""Slowest-ship keyboard response samples for each real Rebel signature."""
from pathlib import Path
import argparse,ast,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/rebels/escapes';O.mkdir(parents=True,exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--reactive',action='store_true');ap.add_argument('--stationary',action='store_true');ap.add_argument('--types',default='turbo,fusion,cloak,slug,rookhook,rockets,helix,ram');ap.add_argument('--edges',default='left,right');ap.add_argument('--label',default='');ap.add_argument('--serial',type=int,default=0);a=ap.parse_args()
if a.reactive:O=O.parent/'escapes-reactive';O.mkdir(exist_ok=True)
if a.label:O=R/'_shots/overnight_combat_1019/rebels'/a.label;O.mkdir(exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
rows=[];errors=[];port,stop=shoot.serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=128
def save():(O/'report.json').write_text(json.dumps(dict(method=('Stationary native positive controls with no directional input; native grabs/throws can still move the player. ' if a.stationary else 'Slowest Juggernaut with actual keyboard movement after a 0.25-second response delay. ')+ 'One active signature at a time; others remain alive with cooldowns/stun held for isolation. Ordinary eBullets, G.ord and G.beams are counted separately. No player fire/roll/somersault. A test-only hit guard records actual contacts and preserves the actor. These samples do not establish five-on-five human win rates or unavoidable attacks.',rows=rows,errors=errors),indent=2)+'\n',encoding='utf-8')
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{window.RE19={};const hit=playerHit;playerHit=function(source){if(!RE19.live)return hit.apply(this,arguments);if(player.dead||player.invuln>0)return;RE19.contacts.push({time:RE19.time,source:String(source||''),x:player.x,y:player.y});player.invuln=57;};
   window.re19Step=n=>{for(let i=0;i<n;i++){RE19.time+=1/60;for(const q of R.ships)if(q!==Q){q.stun=9999;q.rg4.cd=q.rg4.gunCd=9999;}if(!Q.rg4.act)Q.rg4.cd=9999;updatePlay(1/60);if(player._ra7Caught||player._ra7Thrown)RE19.caught=true;
    const A=Q.rg4.act;if(A){RE19.maxTravel=Math.max(RE19.maxTravel,A.travel||A.distance||0);if(!RE19.phases.includes(A.phase))RE19.phases.push(A.phase);}RE19.closest=Math.min(RE19.closest,Math.hypot(Q.x-player.x,Q.y-player.y));
    for(const b of eBullets)if(!RE19.seen.has(b)){RE19.seen.add(b);RE19.shots++;RE19.kinds[b.kind]=(RE19.kinds[b.kind]||0)+1;RE19.interceptable||=enemyOrdnanceCanIntercept(b);}
    for(const b of G.ord)if(!RE19.seenOrd.has(b)){RE19.seenOrd.add(b);RE19.ord++;RE19.ordKinds[b.kind]=(RE19.ordKinds[b.kind]||0)+1;}
    for(const b of G.beams)if(!RE19.seenBeams.has(b)){RE19.seenBeams.add(b);RE19.beams++;}
    if(i%12===0)drawWorld(1/60);
   }};
   window.re19Intent=()=>{const A=Q.rg4.act,P=A?._ra7Pulse,W=P||(['charge','row'].includes(A?.phase)?A:null),tag=P?'pulse':A?.phase+':'+(A?.cycle||0);if(W&&(W!==RE19.lastWarn||tag!==RE19.warnTag)){RE19.lastWarn=W;RE19.warnTag=tag;RE19.respondAt=RE19.time+.25;RE19.angle=W.a??A.a;RE19.intent=null;}
    if(RE19.time<(RE19.respondAt||0))return[];
    if(RE19.angle!=null&&!RE19.intent){const candidates=[RE19.angle+Math.PI/2,RE19.angle-Math.PI/2],score=a=>{const dx=Math.cos(a),dy=Math.sin(a),limits=[];if(Math.abs(dx)>.01)limits.push(((dx>0?worldWidth()-28:28)-player.x)/dx);if(Math.abs(dy)>.01)limits.push(((dy>0?VH-45:PLAY.y+60)-player.y)/dy);return Math.min(...limits);};RE19.intent=candidates.sort((x,y)=>score(y)-score(x))[0];}
    let angle=RE19.intent??(player.x<worldWidth()/2?0:Math.PI),dx=Math.cos(angle),dy=Math.sin(angle);if((player.x<32&&dx<0)||(player.x>worldWidth()-32&&dx>0))dx=-dx;if((player.y<PLAY.y+64&&dy<0)||(player.y>VH-49&&dy>0))dy=-dy;const keys=[];if(Math.abs(dx)>.35)keys.push(dx>0?'ArrowRight':'ArrowLeft');if(Math.abs(dy)>.35)keys.push(dy>0?'ArrowDown':'ArrowUp');return keys;};}''')
  for diff in ['normal','hard','furious']:
   for key,kind in [('voss','turbo'),('voss','fusion'),('nyx','cloak'),('rook','slug'),('rook','rookhook'),('kaia','rockets'),('jace','helix'),('jace','ram')]:
    if kind not in a.types.split(','):continue
    for edge in a.edges.split(','):
     p.evaluate(SETUP,dict(stage=6,kind='rebelsquad',diff=diff,pilot='juggernaut'))
     p.wait_for_function('()=>{stageLoadTick();rg4Warm();return stageLoadReady(6)&&XART.rdy(RA7.sheet)&&XART.rdy("ra4_ui")&&bmfReady("game")}',polling=50)
     out=p.evaluate('''o=>{R=B._rebels;rf28Init(B,R);R.frIntro={done:true};B.enter=B._noHit=false;G=rg4Init(B);G.gang=true;G.scene=null;G.rescueDone=true;G.rescueAt=Infinity;G.releaseAt=99999;s6Wing=null;
      for(const q of R.ships){q.rg4.act=null;q.rg4.cd=q.rg4.gunCd=9999;q.rg4.supply=null;q.rg4.armed=null;q.stun=9999;q.frCloak=0;}G.rebelBoxes=[];Q=R.ships.find(q=>q.key===o.key);Q.stun=0;Q.x=camLeftX()+viewW()/2;Q.y=PLAY.y+110;Q.rg4.gunCd=99999;
      BOFCinematicDirector.cancel();AP10_X.intro=null;story=fb2Talk=fb2Intro=thaw=s6Opening=null;H3.release=false;H3.ending=null;P2M.active=null;run.spaceMode=false;run.shield=0;run.sonicT=run.dkT=0;special=thunderStorm=null;run._megaShield=false;
      VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;stagePlan=[];spawnClock=999999;warnT=0;warnKind=null;subBossTriggered=aminiTriggered=true;powerups=[];enemies=[];eBullets=[];pBullets=[];
      pilotIndex=PILOTS.findIndex(q=>q.key==='juggernaut');const pilot=PILOTS[pilotIndex];PILOTMOD={spd:pilot.spd,fire:pilot.fire,range:pilot.range,tint:pilot.tint};run.speed=0;Input.keys={};Input.mouse.down=false;player.invuln=0;player.roll=player.somer=null;delete player._ra7Caught;delete player._ra7Thrown;player.x=o.edge==='left'?camLeftX()+35:o.edge==='right'?camRightX()-35:camLeftX()+viewW()/2;player.y=VH-110;player.fireCd=999999;Q.rg4.serial=o.serial;
      RE19={live:true,time:0,contacts:[],caught:false,shots:0,kinds:{},ord:0,ordKinds:{},beams:0,phases:[],maxTravel:0,closest:99999,interceptable:false,start:player.x,seen:new WeakSet(),seenOrd:new WeakSet(),seenBeams:new WeakSet()};RA7.events=[];RA4.events=[];rg4Attack(Q,R,G,o.kind);G.releaseAt=999999;SC12.refresh();__bofFit();return{kind:Q.rg4.act?.kind,warm:Q.rg4.act?.warm,target:Q.rg4.act?.target?.key,locked:!!Q.rg4.act?.locked};}''',dict(key=key,kind=kind,edge=edge,serial=a.serial))
     if out.get('kind')!=kind:raise RuntimeError('Native forced signature did not start: '+str(out))
     direction='ArrowRight' if edge=='left' else 'ArrowLeft';held=set()
     if not a.reactive and not a.stationary:p.evaluate('re19Step(15)');p.keyboard.down(direction);held.add(direction)
     for n in range(42 if a.stationary else 38):
      if a.reactive:
       want=set(p.evaluate('re19Intent()'))
       for k in held-want:p.keyboard.up(k)
       for k in want-held:p.keyboard.down(k)
       held=want
      p.evaluate('re19Step(12)');p.wait_for_timeout(5)
     for k in held:p.keyboard.up(k)
     row=p.evaluate('''()=>({metrics:{...RE19,seen:undefined,seenOrd:undefined,seenBeams:undefined,lastWarn:undefined},final:{x:player.x,y:player.y,dead:player.dead,roll:!!player.roll,somer:!!player.somer,base:playerBaseSpeed(),phase:Q.rg4.act?.phase},airEvents:RA7.events,arsenalEvents:RA4.events})''');rows.append(dict(difficulty=diff,pilot=key,kind=kind,edge=edge,initial=out,reactive=a.reactive,stationary=a.stationary,**row));save()
     print(diff,key,kind,edge,json.dumps(dict(contacts=len(row['metrics']['contacts']),caught=row['metrics']['caught'],warm=out['warm'],shots=row['metrics']['shots'],ord=row['metrics']['ord'],beams=row['metrics']['beams'],interceptable=row['metrics']['interceptable'],moved=round(abs(row['final']['x']-row['metrics']['start']),1))),flush=True)
     if edge=='left' and diff=='normal':p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();');p.screenshot(path=str(O/(kind+'.jpg')),type='jpeg',quality=82)
  br.close()
finally:stop();save()
print(json.dumps(dict(cases=len(rows),errors=errors)),flush=True);sys.exit(bool(errors))
