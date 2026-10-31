/* Base36: the supplied vertical route, authored raised cover and relay gate. */
(function(root){
 'use strict';
 const TD=root.TD,W=TD.World,M=TD.M,A=TD.Audio,art=TD.AssaultArt,P=root.TD_LEVEL36_ART,D=TD.Depth35;
 const L=TD.Level36={build:P.build,gateOpens:0},mission=TD.MISSIONS.find(m=>m.id===3);
 const make=TD.makeStructure;
 TD.makeStructure=function(spec){
  const own=['od_column36','od_gate36','od_chest36','od_outer36','od_machine36'].includes(spec.kind);
  if(!own&&!spec.visual36)return make(spec);
  const s=make({...spec,kind:own?'od_barrier':spec.kind});s.kind=spec.kind;s.visual36=spec.visual36||spec.kind.slice(3).replace('36','');
  const defaults={od_column36:{hw:28,hh:26,hp:Infinity,indestructible:true,cover:true},od_gate36:{hw:332,hh:10,hp:Infinity,indestructible:true,cover:false},od_chest36:{hw:30,hh:20,hp:10,cover:true},od_outer36:{hw:40,hh:45,hp:Infinity,indestructible:true,cover:false},od_machine36:{hw:34,hh:28,hp:Infinity,indestructible:true,cover:true}};
  s.type={...s.type,...defaults[spec.kind],...(spec.dim36||{})};s.cover=s.type.cover;s.hp=s.max=s.type.hp;
  s.column36=spec.kind==='od_column36';s.gate36=spec.kind==='od_gate36';
  W.remove(s.rect);s.rect=W.add({x0:s.x-s.type.hw,y0:s.y-s.type.hh,x1:s.x+s.type.hw,y1:s.y+s.type.hh,t:'b',structure:s});return s;
 };
 const cover=(kind,x,y,extra={})=>({kind,x,y,...extra});
 const wall=(x,y,width,hp=56)=>cover('od_barrier',x,y,{visual36:'lowwall',dim36:{hw:width/2,hh:15,hp}});
 const structures=[
  ...[[170,2310],[538,2310],[238,2010],[515,2010]].map(([x,y])=>cover('od_column36',x,y)),
  ...[[112,2630],[95,1430],[700,1080]].map(([x,y])=>cover('od_relay',x,y,{visual36:'relay'})),
  cover('od_chest36',690,2680,{drop:'spread_shotgun'}),cover('od_chest36',710,1730,{drop:'minigun'}),cover('od_chest36',220,1120,{drop:'fusion_beam'}),
  wall(415,1515,180),wall(222,1180,240),wall(680,980,104),wall(220,650,300),
  cover('od_gate36',400,585),
  wall(300,310,90,30),wall(530,310,90,30),cover('od_bosswall',400,365,{visual36:'lowwall'}),
  ...[[125,150],[675,150],[145,480],[655,480]].map(([x,y])=>cover('od_machine36',x,y)),
  // Shallow side alcoves reproduce the sketch without blocking the center route.
  cover('od_outer36',95,1835,{visual36:'outer_down',dim36:{hw:27,hh:38}}),
  cover('od_outer36',132,1760,{visual36:'outer_v',dim36:{hw:64,hh:40}}),
  cover('od_outer36',95,1685,{visual36:'outer_up',dim36:{hw:27,hh:38}}),
  cover('od_outer36',705,1500,{visual36:'outer_up',dim36:{hw:27,hh:38}}),
  cover('od_outer36',668,1425,{visual36:'outer_v',dim36:{hw:64,hh:40}}),
  cover('od_outer36',705,1350,{visual36:'outer_down',dim36:{hw:27,hh:38}}),
  cover('od_barrel',590,1820,{visual36:'barrel'}),cover('od_crate',300,1780,{visual36:'crate',dim36:{hp:24}}),
  cover('od_barrel',610,1280,{visual36:'barrel'}),cover('od_crate',405,850,{visual36:'crate',dim36:{hp:24}})
 ];
 const schedule=[['shotgun',350,2450],['rifle',585,2360],['double',210,2210],['roller',550,2120],['heavy',350,1940],['shotgun',590,1810],['double',340,1660],['flame',590,1490],['roller',260,1340],['rocket',520,1220],['laser',315,1100],['flyer',600,950],['bat',210,860],['double',460,750]];
 Object.assign(mission.map,{key:'l36_ground',w:800,h:2800,rects:[[0,0,68,2800,'b'],[732,0,800,2800,'b'],[68,0,732,60,'b']]});
 Object.assign(mission.data,{name:'FORTRESS / DEAD SIGNAL',brief:['DESTROY THREE RED ELECTRICAL UNITS TO DROP THE SECURITY WALL.','FOUR BEAM COLUMNS: HOLD COVER TO BRACE YOUR BACK.','LOW WALLS: CROUCH, PEEK FIRE, THEN RELEASE TO HIDE.','BREAK OPEN WEAPON CHESTS. GOSFER WAITS IN THE NORTH ARENA.'],start:{x:400,y:2720,a:Math.PI},checkpoints:[[400,2430],[400,1940],[400,1290],[400,760]],gates:[[400,2750],[400,1950],[400,1250]],bossLine:560,boss:{x:400,y:195},structures,props:[],units:schedule.map(([kind,x,y])=>({type:'c35_'+kind,x,y,a:0,wp:[[x-20,y],[x+20,y]]}))});
 mission.setup=function(G){W.navR=10;TD.Pixel25.corpses=[];G.fortress={doorOpen:false,relays:0,pending:G.units.map((u,i)=>({type:u.type,x:u.x,y:u.y,id:i})),arrivals:[],gateDown36:false};G.units=[];L.gateOpens=0;};
 L.syncGate=function(G){const f=G.fortress;if(!f||f.gateDown36||f.relays<3)return;f.gateDown36=true;f.gateDropT36=0;const s=G.structures.find(s=>s.gate36);if(s){s.dead=true;W.remove(s.rect);}L.gateOpens++;A.play('shieldBreak',.65);TD.Cam.kick(4);G.say('ELECTRIC WALL OFFLINE / ADVANCE TO GOSFER',G.player);};
 const hit=TD.hitStructure;TD.hitStructure=function(G,s,...args){const was=s.dead,result=hit(G,s,...args);if(G.mission===3&&!was&&s.dead){if(s.kind==='od_chest36')s.openT36=0;L.syncGate(G);}return result;};
 const tick=mission.tick;mission.tick=function(G,dt){tick?.(G,dt);L.syncGate(G);if(G.fortress.gateDown36)G.fortress.gateDropT36+=dt;for(const s of G.structures)if(s.openT36!=null)s.openT36+=dt;};
 const pose=D.coverPose;D.coverPose=function(s){
  if(!s.visual36)return pose(s);const phase=s.dead?3:!Number.isFinite(s.max)?0:s.hp/s.max<.34?2:s.hp/s.max<.7?1:0;
  let key='l36_'+s.visual36+( ['column','lowwall','relay','chest'].includes(s.visual36)?'_'+phase:'');
  if(s.kind==='od_chest36')key='l36_chest_'+(s.dead?Math.min(3,2+Math.floor((s.openT36||0)*6)):s.flash>0?1:0);
  const m=P.assets[key];return m?{key,s:s.type.hw*2/P.assets['l36_'+s.visual36+(['column','lowwall','relay','chest'].includes(s.visual36)?'_0':'')].bodyWidth}:null;
 };
 const draw=D.drawCover;D.drawCover=function(ctx,s){
  if(s.gate36){if(s.dead)return true;const n=5,width=664/n,key=P.sequences.l36_field.frames[Math.floor((TD.game.time||0)*10)%4],scale=(width+5)/P.assets.l36_field_0.bodyWidth;for(let i=0;i<n;i++)art.draw(ctx,key,68+width*(i+.5),s.y+s.type.hh,{s:scale,flash:s.flash>0?.45:0});return true;}
  if(!s.visual36)return draw(ctx,s);const z=D.coverPose(s);if(!z)return false;
  if(s.visual36==='lowwall'){
   // Repeat authored wall modules at their original proportions; never stretch height with a long wall.
   const n=Math.max(1,Math.round(s.type.hw*2/100)),w=s.type.hw*2/n,scale=(w+(n>1?12:0))/P.assets.l36_lowwall_0.bodyWidth;
   for(let i=0;i<n;i++)art.draw(ctx,z.key,s.x-s.type.hw+w*(i+.5),s.y+s.type.hh,{s:scale,flash:s.gosfarWall43?Math.min(.52,(s.flash||0)*5):s.flash>0?1:0});
  }else art.draw(ctx,z.key,s.x,s.y+s.type.hh,{s:z.s,flash:s.flash>0?1:0});return true;
 };
 D.drawActors=function(ctx,G){
  const p=G.player,objects=G.structures.map(s=>({y:s.y+(s.type?.hh||0),draw:()=>s.assault?D.drawCover(ctx,s):TD.drawStructures(ctx,{...G,structures:[s]})}));
  for(const u of G.units)if(Math.abs(u.y-TD.Cam.y)<560)objects.push({y:u.y,draw:()=>TD.drawUnit(ctx,u)});
  if(G.boss)objects.push({y:G.boss.y,draw:()=>G.boss.draw(ctx,G.t/60)});
  objects.push({y:p.y,draw:()=>TD.drawFoot(ctx,p,{flash:p.inv>0&&Math.floor(p.inv/4)%2?1:0})});objects.sort((a,b)=>a.y-b.y).forEach(o=>o.draw());
 };
 const cam=mission.cam;mission.cam=function(G){if(G.boss){TD.Cam.follow(400,270,.10);}else cam(G);};
 mission.drawFloor=function(ctx,G){
  const arena=P.assets.l36_arena,scale=520/arena.bodyWidth;art.draw(ctx,'l36_arena',400,555,{s:scale});
  const door=G.fortress?.doorOpen?3:0;if(!TD.Gosfar43)art.draw(ctx,'l36_door_'+door,400,140,{s:150/P.assets.l36_door_0.bodyWidth});
  // Perimeter faces are scenery; their physical footprints are mission.map.rects.
  for(const x of [34,766])for(let y=Math.max(95,Math.floor(TD.Cam.y/90)*90);y<TD.Cam.y+TD.VH/TD.Cam.zoom+160&&y<2870;y+=90)if(!TD.Combat39?.breachedWall(G,y))art.draw(ctx,'l36_outer_v',x,y,{s:68/P.assets.l36_outer_v.bodyWidth});
  for(const x of [145,655])art.draw(ctx,'l36_outer_h',x,80,{s:.85});
 };
 mission.drawOver=function(ctx,G){const b=G.boss;if(!b||!['dialogue','transform'].includes(b.state))return;const amount=b.state==='transform'?.22+.35*M.clamp(b.transformT/1.5,0,1):b.line===2?.22*M.clamp(b.lineT/4,0,1):0;ctx.fillStyle='rgba(1,2,12,'+amount+')';ctx.fillRect(TD.Cam.x,TD.Cam.y,TD.VW/TD.Cam.zoom,TD.VH/TD.Cam.zoom);b.draw(ctx);b.drawOver(ctx);};
 mission.canSpawnBoss=G=>G.fortress?.gateDown36===true;
 ART.warm(Object.keys(P.assets));
})(window);
