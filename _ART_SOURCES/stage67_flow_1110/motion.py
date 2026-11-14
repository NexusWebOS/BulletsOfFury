from pathlib import Path
import hashlib,json
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;C=W/'candidate';C.mkdir(parents=True,exist_ok=True)
p=R/'assets/sumpjaw_tandem_1105.js';live=p.read_bytes();old=C/'sumpjaw_tandem_1105.js.before';before=old.read_bytes()if old.exists()else live
assert live==before or live==(C/'sumpjaw_tandem_1105.js').read_bytes(),'Concurrent motion change'
if not old.exists():old.write_bytes(before)
s=before.decode()
s=s.replace("sj98Ready=function(){if(!sr110Ready())return false;if(SJ120.ready)return true;", "sj98Ready=function(){if(SJ120.ready)return true;if(!Object.keys(SR110.art).filter(k=>k.startsWith('rib')||k.startsWith('snake-')).map(k=>XART.rdy('sr110_'+k)).every(Boolean))return false;",1)
s=s.replace('a.from={x:a.x,y:a.gy};a.hits=new Map();','a.from={x:a.x,y:a.gy,h:a.height||0};a.hits=new Map();',1)
start=s.index('function sj120Motion(b,a,dt)');end=s.index('function sj120Next',start)
motion='''// Continuous locomotion is independent of attack windup and release clocks.
function sj121RowMotion(a,mid,slot){const phase=a.clock*1.9;return{x:mid+slot+Math.sin(phase)*62,y:210+Math.cos(phase)*16,h:54*(.5-.5*Math.cos((a.clock+a.i*.12)*TAU/.95))};}
function sj120Motion(b,a,dt){const C=b._sj120,u=clamp(C.t/C.dur,0,1),k=u*u*(3-2*u),mid=worldWidth()/2,live=b._sj98.actors.filter(a=>!a.dead).length;a.jaw=0;a.mouthLevel=0;a.phase=C.mode;a.t=C.t;
 if(C.mode==='entry'){a.phase='entry';a.heading=0;a.x=mid+(a.i?120:-120);a.gy=lerp(a.from.y,165+a.i*40,k);a.height=0;}
 else if(C.mode==='hop-warn'){const side=Math.sign(a.to.x-a.from.x)||((a.i?1:-1));a.x=a.from.x+side*32*u;a.gy=a.from.y+6*u+Math.sin(u*Math.PI)*12;a.height=(a.from.h||0)*(1-u);a.heading+=clamp(ss116Wrap(-a.heading),-dt*8,dt*8);a.jaw=1;a.mouthLevel=Math.min(3,1+Math.floor(u*3));sj98Tell(a,C.t,C.dur);}
 else if(C.mode==='hop'){const bend=a.pathBend*Math.sin(u*Math.PI);a.x=lerp(a.from.x,a.to.x,u);a.gy=lerp(a.from.y,a.to.y,u)+bend;a.height=Math.sin(u*Math.PI)*a.hopArc;a.heading=0;a.jaw=1;a.mouthLevel=3;if(u>.20&&u<.82)sj120Fire(b,a,live===2?.24:.18);}
 else if(C.mode==='row-form'){const r=sj121RowMotion(a,mid,C.rowSlots.get(a.i));a.x=lerp(a.from.x,r.x,k);a.gy=lerp(a.from.y,r.y,k);a.height=lerp(a.from.h||0,r.h,k)+Math.sin(u*Math.PI)*20;a.heading+=clamp(ss116Wrap(-a.heading),-dt*8,dt*8);}
 else if(C.mode==='row-charge'||C.mode==='row-fire'){const r=sj121RowMotion(a,mid,C.rowSlots.get(a.i));a.x=r.x;a.gy=r.y;a.height=r.h;a.heading=0;a.jaw=1;
  if(C.mode==='row-charge'){a.mouthLevel=Math.min(3,1+Math.floor(u*3));sj98Tell(a,C.t,C.dur);}else{const burst=C.t%1.2<.86;a.mouthLevel=burst?3:1;if(burst)sj120Fire(b,a,live===2?.14:.105);}}
 else if(C.mode==='split'){const side=a.from.x>=mid?1:-1;a.x=lerp(a.from.x,mid+side*Math.min(145,viewW()/2-88),u);a.gy=lerp(a.from.y,260,u);a.height=(a.from.h||0)*(1-u)+Math.sin(u*Math.PI)*90;a.heading=0;a.jaw=1;a.mouthLevel=2;if(u>.3&&u<.7)sj120Fire(b,a,.26);}
 else if(C.mode==='north'){a.gy=lerp(a.from.y,-300,k);a.x=a.from.x;a.height=Math.sin(u*Math.PI)*80;ss116Heading(a,0,-1,dt);}
 else if(C.mode==='cross'){const x=lerp(a.from.x,a.to.x,u);ss116Heading(a,x-a.x,0,dt);a.x=x;a.gy=240;a.height=(a.i?30:128)+Math.sin(u*Math.PI)*(a.i?18:30);}
 else if(C.mode==='return'){a.gy=lerp(-260,175,k);a.height=Math.sin(u*Math.PI)*66;a.heading=0;}
 if(a.stun>0){a.mouthLevel=0;a.jaw=0;}a.y=a.gy-a.height;sj120Trail(a);sj120Contact(b,a);
}
'''
s=s[:start]+motion+s[end:]
(C/'sumpjaw_tandem_1105.js').write_text(s,encoding='utf-8',newline='\n');(W/'motion-manifest.json').write_text(json.dumps({'hash':hashlib.sha256(live).hexdigest(),'motion':'continuous movement during warning, charge and firing; repeating grounded takeoff/landing through row phases; attack clocks retained'},indent=2));print('Prepared continuously moving Sumpjaw director')
