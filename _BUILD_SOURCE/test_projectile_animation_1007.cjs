module.exports=function(vm,c,ok){
 console.log('=== Projectile animation stability 1007 ===');
 const result=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const out={},b={t:0,anim:4,_visualAge:0};
  out['a newborn shot stays on frame zero instead of falling back to wall time']=projectileVisualFrame(b,14,8)===0;
  out['negative directional offsets resolve to real asset frames']=[-100,-9,-3,0,9,100].every(p=>projectileVisualFrame(b,14,8,p)>=0&&projectileVisualFrame(b,14,8,p)<8);
  out['render sampling leaves damage and animation clocks untouched']=(()=>{for(let i=0;i<50;i++)projectileVisualFrame(b,14,8);return b.t===0&&b.anim===4&&b._visualAge===0;})();
  const frames=[];for(const hz of [30,60,120]){const q={_visualAge:0};for(let i=0;i<hz;i++)q._visualAge+=1/hz;frames.push(projectileVisualFrame(q,12,8));}
  out['30/60/120 Hz agree at the same authored frame boundary']=frames.every(f=>f===4);
  out['visual age is independent of the shot damage/fuse timer']=projectileVisualAge({_visualAge:.25,t:8,anim:3})===.25;
  const oldAtlas=combatAtlasDraw,oldReady=XART.rdy,calls=[];
  combatAtlasDraw=(...args)=>{calls.push(args);return true;};XART.rdy=()=>false;
  try{
   for(const kind of Object.keys(CFX_STAGE_PROJECTILE))for(let i=0;i<16;i++)drawCfxStageProjectile({kind,x:240,y:220,vx:3,vy:0,t:i/16,szMul:1});
   out['flight never cycles back through charge-size columns']=calls.length===Object.keys(CFX_STAGE_PROJECTILE).length*16&&calls.every(a=>a[3]%4===1);
   out['all selected flight cells fit inside their source grids']=calls.every(a=>a[3]>=0&&a[3]<a[1]*a[2]&&a.slice(4,8).every(Number.isFinite));
   calls.length=0;drawCfxStageProjectile({kind:'s8missile',x:240,y:220,vx:3,vy:0,t:0});
   out['exact horizontal travel does not acquire a false downward component']=Math.abs(calls[0][8].angle-Math.PI/2)<1e-9;
   calls.length=0;drawCfxStageProjectile({kind:'s8blade',x:240,y:220,vx:0,vy:3,t:0});
   const c=calls[0],p=CFX_FLIGHT_PIVOT.s8blade;
   out['crescent core stays at its physical projectile pivot']=Math.abs(c[4]+(p[0]-.5)*c[6]-240)<1e-9&&Math.abs(c[5]+(p[1]-.5)*c[7]-220)<1e-9;
  }finally{combatAtlasDraw=oldAtlas;XART.rdy=oldReady;}
  const trajectories=[];for(const hz of [30,60,120]){const p={x:0,y:0,vx:100,vy:50,t:0,life:2};for(let i=0;i<hz;i++)deathDebrisTick(p,1/hz);trajectories.push(p);}
  out['debris travels in pixels per second instead of disappearing offscreen']=trajectories.every(p=>p.x>50&&p.x<65&&p.y>25&&p.y<33);
  out['debris drag and travel agree at 30/60/120 Hz']=trajectories.every(p=>Math.abs(p.x-trajectories[0].x)<1e-8&&Math.abs(p.y-trajectories[0].y)<1e-8);
  const fragment={x:0,y:0,vx:100,vy:50,t:0,life:.2};deathDebrisTick(fragment,.21);
  out['fragments retain their authored lifetime']=fragment.dead===true;
  const thrust={_thrustPower:0,_thrustFrame:0};pf27ThrustTick(thrust,.1,0,-1,false);const phase=thrust._thrustFrame;pf27ThrustTick(thrust,0,0,0,false);
  out['thruster animation advances continuously and freezes on zero-step updates']=phase>0&&thrust._thrustFrame===phase;
  const oldCell=repair30Cell,trace=[];repair30Cell=(...args)=>{trace.push(args);return true;};
  try{for(const t of [0,.1,.23,.45])chaingunRoundDraw({kind:'mg',_cal50:true,lv:3,x:100,y:100,vx:0,vy:-4,t,_visualAge:t});
   out['chaingun holds one authored flight pose across the former shrinking reel']=trace.length===12&&trace.every(a=>a[0]==='chaingun_round'&&a[1]===0);
   out['chaingun lighting preserves its dimensions']=trace.every(a=>a[4]===trace[0][4]&&a[5]===trace[0][5]);
  }finally{repair30Cell=oldCell;}
  const rawReady=XART.rdy,rawGet=XART.get,flightKeys=[];XART.rdy=()=>true;XART.get=k=>{flightKeys.push(k);return {width:48,height:80,naturalWidth:48,naturalHeight:80};};
  try{for(let i=0;i<32;i++)drawStage4WarfareProjectile({_s4wKind:'lightningmg',t:i/34,x:100,y:100,vx:0,vy:4});
   out['Stage 4 lightning rounds never select the fully transparent eighth cell']=flightKeys.length===32&&flightKeys.every(k=>/^s4w_lightning_mg_round_[0-6]$/.test(k));
  }finally{XART.rdy=rawReady;XART.get=rawGet;}
  return out;
 })())`,c));for(const [name,value] of Object.entries(result))ok(value,name);
};
