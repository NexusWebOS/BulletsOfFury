'use strict';
/* Mike explicitly approved a modular rotating gun for Draconus. A fixed whole
   body, independent authored36-phase gun and same-source foreground grip. */
const DGM1111={base:{pose:hb20Pose,blit:rd74Blit,image:b20Image,point:rd74Point,tick:v19NativeTick,rig:v19HammerRig,load:stageLoadBegin,keys:v18Keys,warm:v18Warm},draws:0,frames:new Set(),last:null};
const DGM1111_MATS=['regular','chrome','red','hit',...Array.from({length:8},(_,i)=>'arm'+i)];
for(const part of ['body','gun','grip'])for(const mat of DGM1111_MATS)XART._src['dgm1111_'+part+'_'+mat]='assets/game/shared/combat/draconus_modular_1111/'+part+'_'+mat+'.webp';
for(const mat of ['regular','chrome','red','hit'])XART._src['sf1111_gun-prop_'+mat]='assets/game/shared/combat/draconus_modular_1111/pickup_'+mat+'.webp';
Object.assign(SF1111_ART['gun-prop'].meta[0],DGM1111_ART.pickup);
function dgm1111Keys(){return Object.keys(XART._src).filter(k=>k.startsWith('dgm1111_'));}
function dgm1111Warm(){let ready=true;for(const key of dgm1111Keys())if(!XART.rdy(key))ready=false;return ready;}
stageLoadBegin=function(n,keys){return DGM1111.base.load.call(this,n,n===8?[...(keys||[]),...dgm1111Keys()]:keys);};
v18Keys=function(){const keys=DGM1111.base.keys();return run.stage===8?[...keys,...dgm1111Keys()]:keys;};
v18Warm=function(){const prior=DGM1111.base.warm();return prior&&(run.stage!==8||dgm1111Warm());};
function dgm1111Rotor(Q){const S=sf1111State(Q);return S.rotor??={angle:0,speed:0};}
function dgm1111Active(b){if(!rd74Own(b))return false;const Q=hb20State(b),A=Q.action;if(Q.rage||Q.rf1110||!sf1111Held(Q))return false;
 return !A||A.type==='armor'||A.type==='sf1111_arsenal'&&A.t>=4.55||A.type==='gun'&&A.t<5.40&&(!A.sf1111Equip||A.t>=1.05);
}
function dgm1111Material(Q){const A=Q.action;return A?.type==='armor'?'arm'+clamp(Math.floor(A.t/A.duration*8),0,7):rd74Mat(Q);}
function dgm1111Frame(Q){return Math.floor((((dgm1111Rotor(Q).angle%TAU)+TAU)%TAU)/TAU*36)%36;}
function dgm1111Sample(b){const Q=hb20State(b),f=dgm1111Frame(Q),m=dgm1111Material(Q),a=DGM1111_ART.body,g=DGM1111_ART.gun;return{a:{...a,key:'dgm1111_body_'+m,white:'dgm1111_body_hit',w:512,h:512,bank:'draconus-modular',frame:f,material:m,muzzle:[g.at[0]+g.muzzle[0],g.at[1]+g.muzzle[1]],gunBounds:g.meta[f].bounds,gunSpans:g.meta[f].spans,wholeGenerated:true,_sf1111:true,_dgm1111:true,_rd74:true},kind:'draconus-modular',k:1,rot:0};}
hb20Pose=function(b){return dgm1111Active(b)?dgm1111Sample(b):DGM1111.base.pose.apply(this,arguments);};
v19HammerRig=function(b){if(!dgm1111Active(b))return DGM1111.base.rig.apply(this,arguments);const Q=hb20State(b),q=dgm1111Sample(b),core=b20Piece(Q.parts[0],q.a,b,0,1,'core',1);core._rd74=true;const out=[core];if(Q.gunHP>0&&!Q.parts[2].destroyed){const gun=b20Piece(Q.parts[2],{...q.a,bounds:q.a.gunBounds,spans:q.a.gunSpans},b,0,1,'chaingun',5);gun._rd74=true;gun._dgm1111Gun=true;out.push(gun);}return out;};
function dgm1111Blit(q,x,y,hit=false){const a=q.a,g=DGM1111_ART.gun,mat=hit?'hit':a.material,Q=rd74Own(boss)&&hb20State(boss),gunmat=hit||(Q?.parts[2]?.flash||0)>0?'hit':a.material;const keys=['dgm1111_body_'+mat,'dgm1111_gun_'+gunmat,'dgm1111_grip_'+mat];if(!keys.map(k=>XART.rdy(k)).every(Boolean))return false;
 const left=Math.round(x-256),top=Math.round(y-256);ctx.drawImage(XART.get(keys[0]),left,top);ctx.drawImage(XART.get(keys[1]),a.frame%g.cols*g.cell[0],Math.floor(a.frame/g.cols)*g.cell[1],...g.cell,left+g.at[0],top+g.at[1],...g.cell);ctx.drawImage(XART.get(keys[2]),left,top);DGM1111.draws++;DGM1111.frames.add(a.frame);DGM1111.last={frame:a.frame,material:a.material,x,y,body:keys[0],gun:keys[1],muzzle:{x:x+a.muzzle[0]-256,y:y+a.muzzle[1]-256}};return true;
}
rd74Blit=function(q,x,y,hit=false){return q?.a._dgm1111?dgm1111Blit(q,x,y,hit):DGM1111.base.blit.apply(this,arguments);};
b20Image=function(a,x,y,k,rot,flash){return a?._dgm1111?dgm1111Blit({a},x,y,flash>0):DGM1111.base.image.apply(this,arguments);};
// The inherited warning asks for its original rest plate. Both warnings and
// actual volleys instead consume the independent gun's measured bore plane.
rd74Point=function(b,q,p='tip'){if(p==='muzzle'&&rd74Own(b)){const Q=hb20State(b),A=Q.action;if(A?.type==='gun'&&!Q.rage&&!Q.rf1110&&sf1111State(Q).acquired&&!sf1111State(Q).broken){const g=DGM1111_ART.gun;return{x:b.x+g.at[0]+g.muzzle[0]-256,y:b.y+g.at[1]+g.muzzle[1]-256};}}return DGM1111.base.point.apply(this,arguments);};
v19NativeTick=function(b,dt){if(rd74Own(b)){const Q=hb20State(b),R=dgm1111Rotor(Q),A=Q.action;let want=0;
 if(sf1111Held(Q)&&!Q.rage&&!Q.rf1110){if(A?.type==='gun'){want=A.t<A.tell?lerp(.25,1.5,clamp(A.t/A.tell,0,1)):A.t<5?4.7:A.t<5.4?4.7*(1-clamp((A.t-5)/.4,0,1)):0;}else if(A?.type==='sf1111_arsenal'&&A.t>=4.4)want=.3;}
 R.speed+=clamp(want-R.speed,-dt*14,dt*6);R.angle=(R.angle+Math.max(0,dt)*TAU*R.speed)%TAU;
 }const r=DGM1111.base.tick.apply(this,arguments);if(dgm1111Active(b)){const Q=hb20State(b);Q.parts[1].destroyed=true;Q.parts[2].destroyed=Q.gunHP<=0;}return r;};
globalThis.BOF_DRACONUS_MODULAR_1111=DGM1111;
