/* Base33: separately authored side-view scenery and physical low passages. */
(function(root){
 'use strict';
 const TD=root.TD,I=TD.Input,M=TD.M,A=TD.Audio,art=TD.AssaultArt,E=TD.Escape29,P=root.TD_BASE33_ART;
 const api=TD.Base33={build:'overdrive1015-base33-r1'},ground=E.floorAt;
 const draw=(c,k,x,y,s=1,o={})=>art.draw(c,k,x,y,{s,...o});
 const seq=(name,t)=>{const q=P.sequences['b33_'+name];return q.frames[Math.min(q.frames.length-1,Math.floor(t*q.fps))];};
 function tiles(c,key,x,y,w,h){const q=ART.get(key);if(!q)return;c.save();c.beginPath();c.rect(x,y,w,h);c.clip();for(let b=y;b<y+h;b+=q.sh)for(let a=x;a<x+w;a+=q.sw)c.drawImage(q.im,q.sx,q.sy,q.sw,q.sh,Math.round(a),Math.round(b),q.sw,q.sh);c.restore();}
 api.ensure=function(G){const e=G.escape29;if(!e)return;
  if(e.base33Solids===e.solids)return;e.base33Solids=e.solids;G.player.hidden33=false;G.player.alcove33=null;
  e.alcoves33=[{x:270,type:0},{x:1190,type:1},{x:2260,type:2},{x:3010,type:3}].map(q=>({...q,y:ground(q.x)}));
  e.passages33=[{x:900,w:126,clearance:28,key:'b33_slide_pipe',s:1.8,kind:'slide'},{x:1300,w:140,clearance:28,key:'b33_crawl_duct',s:2,kind:'crawl'}].map(q=>({...q,y:ground(q.x)}));
  e.secrets33=[{x:1540,y:ground(1540),hp:6,max:6,flash:0,claimed:false,open:false}];e.fx33=[];
  for(const [i,s]of e.solids.entries()){const key=['b33_crate','b33_stack','b33_barrier'][i%3],m=P.assets[key];s.key33=key;s.scale33=s.w/m.bodyWidth;s.h=m.bodyHeight*s.scale33;}
 };
 api.move=function(G,dt,oldX){const p=G.player,e=G.escape29;api.ensure(G);const [dx,dy]=I.dir();p.hidden33=false;p.alcove33=null;
  for(const o of e.passages33){const left=o.x-o.w/2-12,right=o.x+o.w/2+12,inside=p.x>left&&p.x<right,oldInside=oldX>left&&oldX<right;
   if(!inside)continue;
   // A low body cannot stand or jump into a solid overhead duct. Stay prone
   // until clear; the five-second slide cooldown is not reset or bypassed.
   if(oldInside&&p.y>o.y-o.clearance&&p.slide29<=0){p.prone=true;p.stance='prone';p.jump=0;p.velY29=0;p.y=o.y;}
   const h=p.prone||p.slide29>0?22:p.stance==='crouch'?48:94;
   if(p.y-h<o.y-o.clearance&&p.y>o.y-120){
    if(!oldInside){p.x=oldX<o.x?left:right;p.moving=false;}
    else {p.prone=true;p.stance='prone';p.jump=0;p.velY29=0;p.y=o.y;}
   }
  }
  // Background recesses occupy a separate depth plane. Their foreground pier
  // masks the real Yuri plate while tucked; popping out uses the Yuri32 bank.
  const hold=I.down('cover')||I.down('C'),recess=hold&&!dx&&!p.prone&&!p.roll&&!p.slide29&&!p.vault29&&e.alcoves33.find(q=>Math.abs(q.x-p.x)<104&&Math.abs(p.y-q.y)<2);
  if(recess){const side=p.sideFacing29==='west'?'right':'left',sgn=side==='left'?1:-1,peek=p.peek29||0,anchor=recess.x-sgn*79;
   p.alcove33={...recess,side};p.x=anchor+sgn*40*peek;p.sideCover29={x:anchor-sgn*24,y:recess.y,w:40,h:150,recess:true};p.stance='stand';p.hidden33=peek<=.75;
  }
  for(const v of e.secrets33)if(v.open&&!v.claimed&&p.prone&&Math.abs(p.x-v.x)<36&&Math.abs(p.y-v.y)<4){
   v.claimed=true;G.score+=2000;p.smoke=Math.min(9,(p.smoke||0)+2);const gun=p.weapons.find(q=>q.id==='spread_shotgun');if(gun)gun.ammo=Math.min(150,gun.ammo+36);else p.weapons.push({id:'spread_shotgun',ammo:36,lv:1});p.wi=p.weapons.findIndex(q=>q.id==='spread_shotgun');e.message='HOTWIRE: Hidden armory. Spread shotgun and two grenades. Keep going!';e.t=0;A.play('weaponFound',.65);e.fx33.push({kind:'steam',x:v.x,y:v.y,t:0});
  }
 };
 api.hitProp=function(G,s,impact,enemy=false){const e=G.escape29;if(!e||!['corridor','escape'].includes(e.phase))return false;api.ensure(G);
  for(const o of e.passages33)if(E.hitRect(s,o.x,o.y-o.clearance-16,o.w/2,16)){s.dead=true;impact(e,s.x,s.y);return true;}
  if(!enemy)for(const v of e.secrets33)if(!v.open&&E.hitRect(s,v.x,v.y-25,32,25)){v.hp-=s.damage||1;v.flash=.12;s.dead=true;impact(e,s.x,s.y);if(v.hp<=0){v.open=true;e.fx33.push({kind:'ventburst',x:v.x,y:v.y-25,t:0});A.play('gd_wallBreak',.55);TD.Cam.kick(3);}return true;}
  if(enemy&&G.player.hidden33&&G.player.alcove33){const p=G.player;if(E.hitRect(s,p.x,p.y-50,24,76)){s.dead=true;impact(e,p.x+(s.vx<0?18:-18),s.y);return true;}}
  return false;
 };
 api.drawChute=function(c,G){const e=G.escape29,t=e.age,speed=E.chuteScrollSpeed;
  c.save();c.translate(0,70);c.rotate(Math.PI/4);const offset=-(t*speed*(180/245)%256);tiles(c,'b33_wall_1',-512+offset,-768,2048,768);tiles(c,'b33_service',-512+offset,-240,2048,130);c.fillStyle='rgba(0,4,10,.28)';c.fillRect(-1024,-768,3072,768);
  const move=-(t*speed%256);tiles(c,'b33_chute_a',-512+move,0,2048,300);tiles(c,'b33_ceiling_b',-512+move,-385,2048,110);c.restore();
  for(const x of [90,550])draw(c,'b33_drone_hatch',x,109,1.35);
  draw(c,'b33_icon_down',588,192,.55);draw(c,'b33_siren',42,218,.7,{flash:Math.sin(t*7)>.8?.15:0});return true;
 };
 api.drawRoom=function(c,G){const e=G.escape29;api.ensure(G);const first=Math.floor(e.camX/256)*256;
  if(!TD.PixelLab38?.drawCorridorBackdrop?.(c,G))for(let x=first;x<e.camX+896;x+=256){const index=Math.abs(Math.floor(x/256))%4;tiles(c,'b33_wall_'+index,x,96,256,384);tiles(c,index%2?'b33_ceiling_b':'b33_ceiling_a',x,82,256,72);}
  for(const [left,right,y]of [[0,800,350],[800,1510,380],[1510,3700,410]]){c.save();c.beginPath();c.rect(left,y,right-left,480-y);c.clip();for(let x=Math.max(left,first);x<Math.min(right,e.camX+896);x+=256)tiles(c,x<1510?'b33_floor_a':'b33_floor_b',x,y,256,480-y);c.restore();}
  c.fillStyle='rgba(0,4,10,.24)';c.fillRect(e.camX,154,640,256);
  for(const q of e.alcoves33){draw(c,'b33_recess_'+q.type,q.x,q.y);draw(c,'b33_icon_cover',q.x,q.y-190,.55);}
  for(let x=600;x<3500;x+=720)draw(c,'b33_siren',x,205,.7,{flash:e.phase==='escape'&&Math.sin(e.age*8)>.8?.15:0});
  for(const o of e.passages33)draw(c,'b33_icon_'+o.kind,o.x,o.y-135,.65);
  for(const v of e.secrets33){draw(c,v.open?'b33_vent_open':v.hp<6?'b33_vent_damaged':'b33_vent_closed',v.x,v.y,1,{flash:v.flash>0?1:0});if(v.open&&!v.claimed)draw(c,'b33_icon_ammo',v.x,v.y-80,.55);}
  draw(c,'b33_icon_right',1620,242,.65);draw(c,'b33_icon_alarm',1760,240,.65);
 };
 api.drawProps=function(c,G){const e=G.escape29;for(const s of e.solids){if(!s.dead)draw(c,s.key33||'b33_crate',s.x,s.y,s.scale33||1,{flash:s.flash>0?1:0});else draw(c,'b33_barrier_broken',s.x,s.y,.65);}
  for(const b of e.barrels)if(!b.dead)draw(c,'b33_barrel',b.x,b.y,1.05,{flash:b.flash>0?1:0});
  draw(c,e.doorBroken?'b33_door_open':'b33_door',3410,410,2.25);draw(c,'b33_icon_exit',3410,240,.6);
 };
 api.drawForeground=function(c,G){const e=G.escape29,p=G.player;
  for(const o of e.passages33||[]){if(o.kind==='crawl'){for(const dx of [-73,73])draw(c,'b33_pillar',o.x+dx,o.y,.4);draw(c,o.key,o.x,o.y-16,o.s);}else draw(c,o.key,o.x,o.y,o.s);}
  if(p.alcove33){const q=p.alcove33;draw(c,'b33_recess_'+q.type+'_'+q.side,q.x,q.y);}
  for(const f of e.fx33||[])draw(c,seq(f.kind,f.t),f.x,f.y,f.kind==='steam'?.7:1);
 };
 const step=E.step;E.step=function(G,dt){api.ensure(G);step(G,dt);const e=G.escape29;if(!e)return;for(const v of e.secrets33||[])v.flash=Math.max(0,v.flash-dt);for(const f of e.fx33||[])f.t+=dt;e.fx33=(e.fx33||[]).filter(f=>f.t<(f.kind==='steam'?.5:.34));};
 api.impactKey=t=>seq('impact',t*1.8);
 const pose=E.pose;E.pose=function(G){const p=G.player;if(p.slide29>0&&G.escape29?.passages33?.some(o=>Math.abs(p.x-o.x)<o.w/2+12)&&.65-p.slide29>.34)return 'y32_slide_hold_'+(p.rollDir<0?'west':'east');return pose(G);};
 const hud=E.hud;E.hud=function(c,text,G){const r=hud(c,text,G),e=G.escape29,p=G.player;if(!['corridor','escape'].includes(e.phase))return r;let label='';
  if(p.alcove33)label=p.hidden33?'WALL COVER / FIRE TO LEAN OUT':'EXPOSED / RELEASE FIRE TO TUCK IN';
  else if(e.passages33?.some(o=>Math.abs(p.x-o.x)<o.w/2+72))label='SLIDE OR CRAWL THROUGH THE LOW GAP';
  else if(e.secrets33?.some(v=>Math.abs(p.x-v.x)<100&&!v.claimed))label='SHOOT VENT / CRAWL INTO CACHE';
  else if(e.alcoves33?.some(q=>Math.abs(p.x-q.x)<100))label='HOLD COVER TO HIDE IN RECESS';
  if(label)TD.OverdriveFont27.draw(c,label,320,132,9,'#a6ecf7',500);return r;
 };
})(window);
