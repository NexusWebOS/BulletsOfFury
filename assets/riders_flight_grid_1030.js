'use strict';
/* One continuous position per live aircraft. The native attack books, target
   warnings, hit masks and HP remain authoritative. Authored grid replaces rock wall. */
const RR65={base:{tick:rebelSquadTick,load:stageLoadBegin,wall:rr26DrawWall},frame:0,resolving:false,events:[],samples:[],maxStep:0,blocked:0};
const RR65_GRID={key:'rr65_gold_grid',path:'assets/game/levels/stage_06/boss/riders_flight_grid_1030/gold_grid.png',cw:480,ch:64,cols:8,frames:40};
XART._src[RR65_GRID.key]=RR65_GRID.path;
stageLoadBegin=function(n,keys){return RR65.base.load.call(this,n,n===6?[...(keys||[]),RR65_GRID.key]:keys);};
function rr65Home(q,age=0){const w=viewW(),span=Math.min(100,(w-120)/4),cx=camLeftX()+w/2;
 const rook=boss?._rebels?.ships.find(q=>q.key==='rook'),A=rook?.rg4?.act;
 if(q!==rook&&A?.kind==='rk38spin'&&A.phase!=='recover'){const side=q.i<2?-1:1;return{x:cx+side*(w/2-62),y:PLAY.y+(q.i%2?232:97)};}
 return{x:cx+(q.i-2)*span+Math.sin(age*.65+q.i)*5,y:PLAY.y+105+(q.i%2)*120+Math.sin(age*1.1+q.i)*5};}
function rr65FleetPin(q,F){const pins=F?.name==='star'?[[0,-1],[.95,-.31],[.4,.81],[-.4,.81],[-.95,-.31]]:RD21_PINS[F?.name]||RD21_PINS.bowling,p=pins[q.i%5],sx=Math.min(184,(viewW()-100)/2),sy=76;
 if(F?._rr65Pins?.has(q))return F._rr65Pins.get(q);
 return{x:camLeftX()+viewW()/2+p[0]*sx,y:PLAY.y+124+p[1]*sy};}
function rr65FleetReady(F){if(!F._rr65Pins)return false;const arrived=[...F._rr65Pins].every(([q,p])=>!rd21Live(q)||Math.hypot((q._rr65Position?.x??q.x)-p.x,(q._rr65Position?.y??q.y)-p.y)<12);
 if(arrived)return true;
 // Congested traffic commits its current clear slots after a finite approach.
 // Never wait forever or teleport an aircraft into the requested formation.
 if(F.t>=4.8){for(const[q]of F._rr65Pins){const p=q._rr65Position||q;F._rr65Pins.set(q,{x:p.x,y:p.y});q.x=p.x;q.y=p.y;}RR65.events.push({event:'clear-formation-hold',name:F.name,time:rg4State()?.age});if(RR65.events.length>100)RR65.events.shift();return true;}
 return false;}
function rr65Active(){return rr45Scope()&&!rr33Protected()&&!boss.dead;}
function rr65Visible(p){return p.x>camLeftX()-80&&p.x<camRightX()+80&&p.y>PLAY.y-80&&p.y<VH+80;}
function rr65Fast(q){const A=q.rg4?.act;return !!(A&&((A._vs41&&['dash','north','rr45_cross','approach'].includes(A.phase))||A.kind==='rk38dash'&&A.phase==='fire'));}
function rr65Body(q){const b=rr45Bounds(q);return{w:b.w+3.5,h:b.h+4.5};}
function rr65Inside(x,y,B,o){return Math.abs(x-o.x)<B.w+o.B.w+2&&Math.abs(y-o.y)<B.h+o.B.h+2;}
function rr65Route(row,goal,rows,age){const q=row.q,B=row.B,left=camLeftX()+B.w+7,right=camRightX()-B.w-7,top=PLAY.y+32,bot=Math.min(VH*.61,VH-B.h-10),obstacles=rows.filter(o=>o!==row&&!o.safe&&rr65Visible(o.p)).map(o=>({x:o.p.x,y:o.p.y,B:o.B}));
 const clear=(x,y)=>x>=left&&x<=right&&y>=top&&y<=bot&&!obstacles.some(o=>rr65Inside(x,y,B,o));
 const clearLine=(a,b)=>{if(!clear(b.x,b.y))return false;for(const o of obstacles){if(rr65Inside(a.x,a.y,B,o))continue;let lo=0,hi=1;for(const [p,d,r]of[[a.x-o.x,b.x-a.x,B.w+o.B.w+2],[a.y-o.y,b.y-a.y,B.h+o.B.h+2]]){if(Math.abs(d)<1e-9){if(Math.abs(p)>=r){lo=2;break;}continue;}let x=(-r-p)/d,y=(r-p)/d;if(x>y)[x,y]=[y,x];lo=Math.max(lo,x);hi=Math.min(hi,y);}if(lo<=hi&&lo<1&&hi>0)return false;}return true;};
 if(clearLine(row.p,goal)){delete q._rr65Nav;return goal;}
 let N=q._rr65Nav;
 if(!N||age>=N.until||Math.hypot(goal.x-N.goal.x,goal.y-N.goal.y)>18){
  const points=[{...row.p}];if(clear(goal.x,goal.y))points.push({...goal});
  for(const o of obstacles){const w=B.w+o.B.w+3,h=B.h+o.B.h+3;for(const x of[o.x-w,o.x+w])for(const y of[o.y-h,o.y+h])if(clear(x,y))points.push({x,y});}
  const end=points.length>1?points.slice(1).reduce((best,p,i)=>{const d=(p.x-goal.x)**2+(p.y-goal.y)**2;return !best||d<best.d?{id:i+1,d}:best;},null):null;
  let path=[];
  if(end){const cost=points.map(()=>Infinity),from=[],used=new Set();cost[0]=0;
   for(let n=0;n<points.length;n++){let id=-1;for(let i=0;i<points.length;i++)if(!used.has(i)&&(id<0||cost[i]<cost[id]))id=i;if(id<0||!Number.isFinite(cost[id]))break;if(id===end.id){let cur=id;while(cur>0){path.push(points[cur]);cur=from[cur];}path.reverse();break;}used.add(id);
    for(let j=1;j<points.length;j++)if(!used.has(j)&&clearLine(points[id],points[j])){const c=cost[id]+Math.hypot(points[id].x-points[j].x,points[id].y-points[j].y);if(c<cost[j]){cost[j]=c;from[j]=id;}}
   }
  }
  N=q._rr65Nav={goal:{...goal},path,until:age+.45};
 }
 while(N.path.length>1&&Math.hypot(N.path[0].x-row.p.x,N.path[0].y-row.p.y)<8)N.path.shift();
 for(let i=N.path.length-1;i>0;i--)if(clearLine(row.p,N.path[i])){N.path.splice(0,i);break;}
 return N.path[0]||row.p;
}
function rr65Sweep(a,b){const x=b.p.x-a.p.x,y=b.p.y-a.p.y,w=a.B.w+b.B.w,h=a.B.h+b.B.h,dx=(b.x-b.p.x)-(a.x-a.p.x),dy=(b.y-b.p.y)-(a.y-a.p.y);
 // Existing overlap is cleared gradually by steering, never by teleporting a hull.
 if(Math.abs(x)<w-.01&&Math.abs(y)<h-.01)return null;
 let enter=0,exit=1;
 for(const [p,d,r]of[[x,dx,w],[y,dy,h]]){if(Math.abs(d)<1e-9){if(Math.abs(p)>=r)return null;continue;}let lo=(-r-p)/d,hi=(r-p)/d;if(lo>hi)[lo,hi]=[hi,lo];enter=Math.max(enter,lo);exit=Math.min(exit,hi);if(enter>exit)return null;}
 return enter>=0&&enter<1&&exit>0?Math.max(0,enter-.002):null;
}
function rr65Resolve(b,dt,prior){if(!rr65Active())return;const G=b._rebels.gang1004,F=G?.rd21?.fleet;
 const rows=b._rebels.ships.filter(rd21Live).map(q=>{if(!q.rg4?.act&&!F){q.rfHeading=Math.PI/2;q._rd21Scale=1;}const p=prior.get(q)||{x:q.x,y:q.y},raw={x:q.x,y:q.y},B=rr65Body(q);let x=q.x,y=q.y;
  const safe=vs41Safe(q);let fast=rr65Fast(q),speed=fast?1600:F?360:q.rg4?.act?540:205;
  // An offscreen route may relocate while completely hidden. Visible travel stays physical.
  if(rr65Visible(p)||rr65Visible(raw)){const dx=x-p.x,dy=y-p.y,d=Math.hypot(dx,dy),step=speed*dt;if(d>step&&d>0){x=p.x+dx/d*step;y=p.y+dy/d*step;}}
  return{q,p,raw,B,x,y,safe,fast};});
 if(F?.phase==='assemble'&&!F._rr65Pins){const pins=rows.map(r=>rr65FleetPin(r.q,F));let best=null;const assign=(i,used,chosen,cost)=>{if(best&&cost>=best.cost)return;if(i===rows.length){best={cost,chosen:chosen.slice()};return;}for(let j=0;j<pins.length;j++)if(!(used&(1<<j))){const p=pins[j],r=rows[i];chosen.push(p);assign(i+1,used|(1<<j),chosen,cost+(p.x-r.p.x)**2+(p.y-r.p.y)**2);chosen.pop();}};assign(0,0,[],0);F._rr65Pins=new Map(rows.map((r,i)=>[r.q,best.chosen[i]]));}
 for(const r of rows){const q=r.q;if(r.safe||q.rg4?.act||!rr65Visible(r.p))continue;let goal;
  if(F?.phase==='assemble')goal=rr65FleetPin(q,F);else if(!F){goal=rr65Home(q,G.age);if(q.evadeT>0)goal.x=q.evadeX;}else continue;
  const target=rr65Route(r,goal,rows,G.age),dx=target.x-r.p.x,dy=target.y-r.p.y,d=Math.hypot(dx,dy),s=Math.min(d,(F?300:205)*dt);r.x=r.p.x+(d?dx/d*s:0);r.y=r.p.y+(d?dy/d*s:0);
 }
 // Reserve the actual swept hull, not its eventual destination. All ships share this pass.
 for(let pass=0;pass<8;pass++){let changed=false;
  for(let i=0;i<rows.length;i++)for(let j=i+1;j<rows.length;j++){const a=rows[i],c=rows[j];if(a.safe||c.safe||!rr65Visible(a.p)||!rr65Visible(c.p))continue;
   const t=rr65Sweep(a,c);if(t==null)continue;
   for(const r of[a,c]){r.x=r.p.x+(r.x-r.p.x)*t;r.y=r.p.y+(r.y-r.p.y)*t;}
   RR65.blocked++;changed=true;
   for(const r of[a,c])if(r.q._rr65Nav)r.q._rr65Nav.until=0;
  }if(!changed)break;
 }
 for(const r of rows){const q=r.q,dx=r.x-r.raw.x,dy=r.y-r.raw.y;q.x=r.x;q.y=r.y;
  // Newly emitted ordnance shares the resolved physical socket. Existing shots keep flying.
  if(Math.abs(dx)+Math.abs(dy)>.001){for(const o of RR65.freshOrd||[])if(o.owner===q){o.x+=dx;o.y+=dy;}for(const o of RR65.freshRounds||[])if(o.owner===q){o.x+=dx;o.y+=dy;}}
  const d=Math.hypot(q.x-r.p.x,q.y-r.p.y);if(rr65Visible(r.p)&&rr65Visible(q))RR65.maxStep=Math.max(RR65.maxStep,d);
  q._rr65Position={x:q.x,y:q.y};
 }
}
// Old separation call sites now defer to the single outer motion owner.
function rr65Separate(){return;}
rebelSquadTick=function(b,dt){if(!rr45Scope(b))return RR65.base.tick.apply(this,arguments);const prior=new Map(b._rebels.ships.map(q=>[q,{x:q.x,y:q.y}])),G=b._rebels.gang1004,ord=new Set(G?.ord||[]),rounds=new Set(eBullets);RR65.frame++;
 const r=RR65.base.tick.apply(this,arguments);RR65.freshOrd=(b._rebels.gang1004?.ord||[]).filter(o=>!ord.has(o));RR65.freshRounds=eBullets.filter(o=>!rounds.has(o));
 rr65Resolve(b,clamp(dt,0,.05),prior);RR65.freshOrd=null;RR65.freshRounds=null;return r;};
rr26DrawWall=function(W){if(!rr45Scope()||!W._rr45||W.t<W.cast)return RR65.base.wall.apply(this,arguments);const a=RR65_GRID;if(!XART.rdy(a.key))return;
 const f=W.t<W.cast+W.build?Math.min(15,Math.floor((W.t-W.cast)/W.build*16)):W.t>W.dur-W.fade?32+Math.min(7,Math.floor((W.t-W.dur+W.fade)/W.fade*8)):16+Math.floor(W.t*24)%16,r=rr26WallRect();
 ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(r.x+r.w/2-a.cw/2),Math.round(r.y+r.h/2-a.ch/2),a.cw,a.ch);
};
globalThis.BOF_RIDERS_FLIGHT_GRID_1030=RR65;
