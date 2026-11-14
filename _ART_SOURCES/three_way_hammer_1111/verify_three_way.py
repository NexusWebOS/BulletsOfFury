from pathlib import Path
import json
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs/Three-way-hammer'
def run_three_way(p,stage,ck,shot):
 rows=[]
 for mat in ['regular','chrome']:
  for i,direction in enumerate(['center','right','left']):
   if stage==5:
    q=p.evaluate("""([mat,i])=>{B._hammer._td1111Next=i;seed119('furious',mat);const h=B._hammer,selected=h._td1111Dir;let root=null,drift=0,minClear=9999,seen=new Set();for(let j=0;j<650;j++){updateBoss(1/60);const P=h._hj22Pair||h.c27Combo||h._hf22StormPair,q=ha21Blue(B);if(q?.a.bank?.startsWith('blue-overhead')&&q.a.frame>=16)seen.add(q.a.direction);if(P?.ba119){root??={x:B.x,y:B.y};drift=Math.max(drift,Math.hypot(B.x-root.x,B.y-root.y));minClear=Math.min(minClear,B.x+q.a.bounds[0]-q.a.pivot[0]-camLeftX(),camRightX()-B.x-q.a.bounds[2]+q.a.pivot[0]);}if(root&&!P)break;}return{selected,seen:[...seen],drift,minClear,contacts:HF22.events.filter(e=>e.type==='first-down').length+BA119.events.filter(e=>e.type==='planted-contact').length};}""",[mat,i])
    p.evaluate("""([mat,i])=>{B._hammer._td1111Next=i;seed119('furious',mat);B.x=worldWidth()/2;B.y=viewTopY()+260;B._drawY=B.y;B._hammer.t=.58;B.flash=0;}""",[mat,i])
    shot(p,f'stage{stage}-{mat}-{direction}-windup')
    p.evaluate("""()=>{hammerState(B,'recover');B._hammer.t=0;B._hammer._hj22Pair=B._hammer.c27Combo=B._hammer._hf22StormPair=null;B.x=worldWidth()/2;B.y=viewTopY()+260;B._drawY=B.y;}""")
    tip=p.evaluate("""()=>{const q=ha21Blue(B),at=ba119At(B,q.a,q.k||1),P=hj22Pair(B,'blue',{...at});P.clock=.25;hj22PairTick(B,P);const impact=ba119At(B,ba119Row('blue-overhead',11,c27Material(B)));return{bank:q.a.bank,direction:q.a.direction,headOffset:q.a.headCenter[0]-q.a.pivot[0],tipOffset:q.a.tip[0]-q.a.pivot[0],warningError:Math.hypot(P.ba119Mark.x-impact.x,P.ba119Mark.y-impact.y),key:q.a.key};}""")
    p.evaluate('B.flash=0')
   else:
    q=p.evaluate("""([mat,i])=>{diffKey='furious';DIFF=difficultyForRun(run.mode,diffKey);B._r30.mode='fight';B._r30.v18.donorAge=0;B.x=worldWidth()/2;B.y=viewTopY()+200;Q.rf1110=null;Q.rage=false;Q.chrome=mat==='chrome';Q.action=null;Q.cool=999;Q._td1111Next=i;BA119.events=[];hb20Start(B,'skystrike');const A=Q.action,selected=Q._td1111Dir;let root=null,drift=0,minClear=9999,seen=new Set();for(let j=0;j<650&&Q.action===A;j++){v19NativeTick(B,1/60);if(Q.action===A){const q=hb20Pose(B);if(q?.a.bank?.startsWith('ba119_corrupt-overhead')&&q.a.frame>=16)seen.add(q.a.direction);if(A.t-A.tell>=.55){root??={x:B.x,y:B.y};drift=Math.max(drift,Math.hypot(B.x-root.x,B.y-root.y));minClear=Math.min(minClear,B.x+q.a.bounds[0]-q.a.pivot[0]-camLeftX(),camRightX()-B.x-q.a.bounds[2]+q.a.pivot[0]);}}}return{selected,seen:[...seen],drift,minClear,contacts:BA119.events.filter(e=>e.type==='planted-contact').length};}""",[mat,i])
    p.evaluate("""([mat,i])=>{Q.action=null;Q.rf1110=null;Q.rage=false;Q.chrome=mat==='chrome';Q._td1111Next=i;Q.cool=999;B.x=worldWidth()/2;B.y=viewTopY()+260;B._drawY=B.y;hb20Start(B,'skystrike');Q.action.t=Q.action.tell;B.flash=0;}""",[mat,i])
    shot(p,f'stage{stage}-{mat}-{direction}-windup')
    p.evaluate("""()=>{Q.action.t=Q.action.tell+1;ba119Root(B,Q.action);}""")
    tip=p.evaluate("""()=>{const q=hb20Pose(B),at=rd74Point(B,q),target=Q.action.target;return{bank:q.a.bank,direction:q.a.direction,headOffset:q.a.headCenter[0]-q.a.pivot[0],tipOffset:q.a.tip[0]-q.a.pivot[0],warningError:Math.hypot(at.x-target.x,at.y-target.y),key:q.a.key};}""")
   shot(p,f'stage{stage}-{mat}-{direction}-contact')
   ck(f'Stage{stage} {mat}/{direction}: committed bank, four native hits and planted clearance',q['selected']==direction and q['seen']==[direction]and q['contacts']==4 and q['drift']<.01 and q['minClear']>=0,q)
   expected=abs(tip['headOffset'])<=18 if direction=='center'else tip['headOffset']>75 if direction=='right'else tip['headOffset']<-75
   ck(f'Stage{stage} {mat}/{direction}: actual cap and native warning align',expected and tip['direction']==direction and tip['warningError']<2,tip)
   rows.append(dict(stage=stage,material=mat,direction=direction,simulation=q,contact=tip))
 if stage==5:
  cycle=p.evaluate("""()=>{B._hammer._td1111Next=0;const out=[];for(let i=0;i<3;i++){hammerState(B,'warn');out.push(B._hammer._td1111Dir);}return out;}""")
 else:
  cycle=p.evaluate("""()=>{Q._td1111Next=0;const out=[];for(let i=0;i<3;i++){Q.action=null;hb20Start(B,'skystrike');out.push(Q._td1111Dir);}return out;}""")
 ck(f'Stage{stage}: native attacks select center then mirrored right then left',cycle==['center','right','left'],cycle)
 if stage==5:
  transfer=p.evaluate("""()=>{B._hammer._td1111Dir='left';B._hammer._td1111Next=1;hammerState(B,'warn');B._hammer.t=0;const before=ha21Blue(B).a.bank;B._hammer.t=.58;const after=ha21Blue(B).a.bank;return{before,after};}""")
  continuous=transfer['before']=='blue-overhead-left'and transfer['after']=='blue-overhead-right'
 else:
  transfer=p.evaluate("""()=>{Q._td1111Dir='left';Q._td1111Next=1;Q.action=null;hb20Start(B,'skystrike');Q.action.t=0;const before=hb20Pose(B).a.bank;Q.action.t=Q.action.tell+.6;const after=hb20Pose(B).a.bank;return{before,after};}""")
  continuous='overhead-left_'in transfer['before']and'overhead-right_'in transfer['after']
 ck(f'Stage{stage}: keep previous grip through lift before changing strike direction',continuous,transfer)
 (O/f'verification-stage{stage}/three-direction-pixels.json').write_text(json.dumps(rows,indent=2))
