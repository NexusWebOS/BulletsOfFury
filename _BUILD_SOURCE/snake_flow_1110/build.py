from pathlib import Path
import json,hashlib
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;C=W/'candidate';C.mkdir(exist_ok=True);O=W.parents[1]/'outputs/snake-flow';O.mkdir(parents=True,exist_ok=True)
p=R/'assets/sumpjaw_tandem_1105.js';live=p.read_bytes();backup=C/'before.js';before=backup.read_bytes()if backup.exists()else live
assert live==before or live==(C/p.name).read_bytes(),'Concurrent snake changes'
if not backup.exists():backup.write_bytes(before)
s=before.decode();start=s.index('function sj120ResetTrail');end=s.index('function sj120Set',start)
s=s[:start]+'''// Ground path and vertical follow-through use separate histories. A slow head
// must never leave a body section suspended at an old spatial sample's height.
const SJ122={stations:[0,12,24,36,48,60,72,84,96,108,120,132,144,156,168,180,191,201,210,218],liftDelay:.0014,rowPeriod:1.12,rowFlight:.72};
function sj120ResetTrail(a){const p=sj120Neck(a);a.trail=Array.from({length:110},(_,i)=>({x:p.x+Math.sin(a.heading)*i*3,y:p.y-Math.cos(a.heading)*i*3,h:p.h,heading:a.heading}));a.liftTrail=[{t:a.clock,h:a.height},{t:a.clock-3,h:a.height}];a.liftClock=a.clock;a.lands=0;}
function sj120Trail(a){const p=sj120Neck(a),q=a.trail[0],d=Math.hypot(p.x-q.x,p.y-q.y),n=Math.max(1,Math.ceil(d/2));if(d>1){for(let i=1;i<=n;i++){const u=i/n;a.trail.unshift({x:lerp(q.x,p.x,u),y:lerp(q.y,p.y,u),h:p.h,heading:p.heading});}}if(a.trail.length>360)a.trail.length=360;
 const old=a.liftTrail[0];a.liftTrail.unshift({t:a.clock,h:a.height});a.liftClock=a.clock;while(a.liftTrail.length>2&&a.liftTrail.at(-2).t<a.clock-1.2)a.liftTrail.pop();if(old.h>0&&a.height===0){a.lands++;}}
function sj122Lift(a,d){const t=(a.dead?a.liftClock:a.clock)-d*SJ122.liftDelay,L=a.liftTrail;if(!L?.length)return a.height||0;if(t>=L[0].t)return L[0].h;for(let i=1;i<L.length;i++){const p=L[i-1],q=L[i];if(t>=q.t)return lerp(q.h,p.h,clamp((t-q.t)/Math.max(.00001,p.t-q.t),0,1));}return L.at(-1).h;}
''' +s[end:]
start=s.index('function sj121RowMotion');end=s.index('function sj120Motion',start)
s=s[:start]+'''function sj121RowMotion(a,mid,slot){const phase=a.clock*1.9,t=((a.clock+a.i*.18)%SJ122.rowPeriod+SJ122.rowPeriod)%SJ122.rowPeriod,u=clamp(t/SJ122.rowFlight,0,1);return{x:mid+slot+Math.sin(phase)*62,y:210+Math.cos(phase)*20,h:t<SJ122.rowFlight?4*64*u*(1-u):0};}
''' +s[end:]
s=s.replace("a.height=(a.from.h||0)*(1-u);a.heading+=", "a.height=(a.from.h||0)*(1-u)*(1-u);a.heading+=",1)
s=s.replace("a.height=Math.sin(u*Math.PI)*a.hopArc;a.heading=0;", "a.height=4*u*(1-u)*a.hopArc;a.heading=Math.sin(u*Math.PI)*Math.sin(a.clock*6.5+a.i*Math.PI)*.20;",1)
s=s.replace("a.x=r.x;a.gy=r.y;a.height=r.h;a.heading=0;", "a.x=r.x;a.gy=r.y;a.height=r.h;a.heading=Math.sin(a.clock*6.5+a.i*Math.PI)*.12;",1)
s=s.replace("a.y=a.gy-a.height;sj120Trail(a);sj120Contact(b,a);", "a.y=a.gy-a.height;const lands=a.lands;sj120Trail(a);if(a.lands>lands&&['row-charge','row-fire'].includes(C.mode)){combatAudio0927(a,'hammerImpact',.2);sj120Log(b,'row-landing',{actor:a.i});}sj122Segments(a);sj120Contact(b,a);",1)
s=s.replace("const p=ss116Point(a,15+j*21);explode", "const p=sr110SnakePoint(a,15+j*21);explode",1)
start=s.index('function sr110SnakePoint');end=s.index('function sj120Warnings',start)
s=s[:start]+'''function sr110SnakePoint(a,d){const p=ss116Point(a,d),amp=Math.min(27,d*.22)*Math.min(1,(245-d)/60),wave=Math.sin(a.clock*8.5-d*.052+a.i*Math.PI)*Math.max(0,amp);return{x:p.x+Math.cos(p.heading)*wave,y:p.y+Math.sin(p.heading)*wave,h:sj122Lift(a,d)};}
function sj122Segments(a){a.segments=SJ122.stations.map(d=>{const p=sr110SnakePoint(a,d),lead=sr110SnakePoint(a,Math.max(0,d-3)),tail=sr110SnakePoint(a,d+3),angle=Math.atan2(-(lead.x-tail.x),lead.y-tail.y),n=((Math.round(angle/TAU*32)%32)+32)%32,type=d<42?0:d<90?1:d<132?2:d<170?3:d<205?4:5;return{...p,n,type,d};});}
function sj120Segments(a,shadow){if(!a.segments)sj122Segments(a);for(let i=a.segments.length-1;i>=0;i--){const p=a.segments[i];sr110Blit('rib'+p.type+'-'+(shadow?'shadow':a.flash>0?'hit':'body'),p.n,p.x,p.y+(shadow?12:-p.h));}}
''' +s[end:]
(C/p.name).write_text(s,encoding='utf-8',newline='\n');m={'expected_source_hash':hashlib.sha256(live).hexdigest(),'owner':p.name,'changes':['Separate time-based vertical history for every body section','20 closely spaced tapered source-rib sections','Continuous traveling lateral wave and subtle authored head turns','Ballistic main leaps and repeated row jumps with grounded landings','Native attack clocks, warning points, health pools, sockets, projectiles and rewards retained'],'body_delay_seconds':.3052,'row_jump':{'period':1.12,'flight':.72,'ground':.4,'height':64},'render':'existing authored direction frames at native scale; positions and frame selection only'};(O/'manifest.json').write_text(json.dumps(m,indent=2));print(json.dumps(m))
