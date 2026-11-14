from pathlib import Path
W=Path(__file__).resolve().parent
p=W/'boss_animation_1109.js';s=p.read_text()
old="""function ba119Root(b,A){const q=ba119Corrupt(hb20State(b),11),a=q.a;
 const bounds=[a.bounds],left=Math.max(...bounds.map(r=>a.pivot[0]-r[0]))+4,right=Math.max(...bounds.map(r=>r[2]-a.pivot[0]))+4;"""
new="""function ba119Clearance(prefix,k=1){const rows=['overhead','sides','right'].flatMap(n=>BA119_ART[prefix+'-'+n].meta.map(m=>({m,p:BA119_ART[prefix+'-'+n].pivot})));
 return{left:Math.max(...rows.map(({m,p})=>p[0]-m.bounds[0]))*k+4,right:Math.max(...rows.map(({m,p})=>m.bounds[2]-p[0]))*k+4};}
function ba119Root(b,A){const q=ba119Corrupt(hb20State(b),11),a=q.a;
 const {left,right}=ba119Clearance('corrupt');"""
assert s.count(old)==1;s=s.replace(old,new);p.write_text(s)
p=W/'whole_hammer_1110.js';s=p.read_text().split('// HA1111:')[0];module=(W/'runtime-whirl.js').read_text();p.write_text(s+module)
for stage in [5,8]:
 p=W.parent/f'verify_heavy_stage{stage}.py';s=p.read_text()
 if stage==5:
  s=s.replace("samples.push({t:P.clock,x:B.x,y:B.y,bank:q?.a.bank,f:q?.a.frame});","samples.push({t:P.clock,x:B.x,y:B.y,bank:q?.a.bank,f:q?.a.frame,left:B.x+(q.a.bounds[0]-q.a.pivot[0])*(q.k||1)-camLeftX(),right:camRightX()-B.x-(q.a.bounds[2]-q.a.pivot[0])*(q.k||1)});")
  needle="    ck(f'Stage5 {diff}/{mat}: new poses used'"
  s=s.replace(needle,"    ck(f'Stage5 {diff}/{mat}: full planted combo remains inside playfield',all(z['left']>=0 and z['right']>=0 for z in q['samples']),q['samples'])\n"+needle)
 else:
  s=s.replace('let root=null,drift=0,poses=new Set()','let root=null,drift=0,clipped=0,poses=new Set()')
  s=s.replace("if(A.t-A.tell>=.55){root??=", "if(A.t-A.tell>=.55){if(B.x+q.a.bounds[0]-q.a.pivot[0]<camLeftX()||B.x+q.a.bounds[2]-q.a.pivot[0]>camRightX())clipped++;root??=")
  s=s.replace('mat:m,drift,unique:poses.size','mat:m,drift,clipped,unique:poses.size')
  needle="    ck(f'Stage8 {diff}/{mat}: actual behind-head"
  s=s.replace(needle,"    ck(f'Stage8 {diff}/{mat}: full planted combo remains inside playfield',q['clipped']==0,q['clipped'])\n"+needle)
 p.write_text(s)
print('Prepared full-combo clearance and one-transition-only whirlwind recovery.')
