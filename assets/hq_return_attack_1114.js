"use strict";
/* HQ19: native Chronos destruction -> delayed Earth approach -> physical HQ
   homecoming -> crew/radar -> evacuation and base assault. Combat stays native. */
const HQ19={base:{rows:c16Rows,keys:d1110Keys,step:d1110Step,visual:d1110Visual,load:stageLoadBegin,
 endingTick:h3EndingTick,endingDraw:h3EndingDraw,openingTick:s6OpeningTick},last:null,events:[],parked:new Map(),returnDuration:12.4};
for(const a of [...Object.values(HQ19_ART.banks),...Object.values(HQ20_ART.pilots),HQ20_ART.door,...Object.values(HQ21_ART.pilots),...Object.values(HQ22_ART.flips)])XART._src[a.key]=a.path+'?v='+a.sha256.slice(0,12);
const HQ19_PILOTS=['cole','axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva'];
const HQ19_SQUAD=HQ19_PILOTS.filter(p=>p!=='decker'&&p!=='axel');
const HQ22={flight:.75,spacing:.9,launch:7.5,arrival:.32,spawn:.24,maxEnemies:32,attack:1.6,defend:4.2,swarm:2.8,escape:3.4,flipDuration:.5,guardBorn:{decker:.65,axel:1.0},flipStart:{decker:7.1,axel:8.0},boostStart:{decker:7.6,axel:8.5}};
const HQ19_AUDIO=['enemyMissile','somersault','gd_doorOpen','gd_footstepA','gd_footstepB','jetDash','gravityLock','blip','enemyMachineGunLight','expSmall','expBig','select'];
Snd.prepare?.(HQ19_AUDIO);
const hq19Ease=v=>{v=clamp(v,0,1);return v*v*(3-2*v);};
function hq19Rows(p){
 const row=(id,mode,duration,extra={})=>({id:'HQ19-'+id,hq19:mode,c16:true,d1110:true,kind:'wide',layout:'panel',page:0,art:'comic',location:'hangar',
  people:[],who:'SYSTEM',text:'',readings:[],duration,speechEnd:0,_cueSet:new Set(),...extra});
 const footsteps=(a,z)=>{const out=[];for(let t=a;t<z;t+=.36)out.push({name:Math.round(t/.36)%2?'gd_footstepA':'gd_footstepB',at:t});return out;};
 const rows=[
  row('LAND','land',7.0,{c16Cues:[{name:'jetDash',at:.12},{name:'gravityLock',at:4.3}]}),
  row('EXIT','exit',3.0,{c16Cues:[{name:'gd_doorOpen',at:.15}]}),
  row('ENTER','enter',6.6,{c16Cues:[{name:'gd_doorOpen',at:1.5},{name:'gd_doorOpen',at:4.9},...footsteps(.2,4.6)]}),
  row('CORRIDOR','corridor',6.6,{c16Cues:footsteps(.2,5.8)}),
  row('WELCOME','welcome',7.0,{upgrade:5,c16Cues:[{name:'select',at:1.7},{name:'blip',at:3.0}]})
 ];
 // Preserve the existing Easy/Normal completion/difficulty-choice owner.
 if(!['easy','normal'].includes(diffKey)){
  const beeps=[];for(let t=.3;t<8.5;t+=t<3?.85:.43)beeps.push({name:'blip',at:t});
  rows.push(row('RADAR','radar',9.0,{c16Cues:beeps}),
   row('LAUNCH','launch',HQ22.launch,{c16Cues:[{name:'gd_doorOpen',at:.05},...HQ19_SQUAD.map((_,i)=>({name:'jetDash',at:1.1+i*HQ22.spacing}))]}),
   row('QUIET','quiet',5.0,{c16Cues:[{name:'gd_doorOpen',at:.05}]}),
   row('ATTACK','attack',HQ22.attack,{c16Cues:[{name:'enemyMachineGunLight',at:.3},{name:'enemyMissile',at:.55},{name:'expSmall',at:.8},{name:'enemyMissile',at:1.25}]}),
   row('DECKER','defend',HQ22.defend,{who:'DECKER',text:'Dammit! They made it to our base too!',c16Cues:[{name:'gd_doorOpen',at:.05},{name:'jetDash',at:.65},{name:'jetDash',at:1.0},...Array.from({length:10},(_,i)=>[{name:'enemyMachineGunLight',at:1.3+i*.25},{name:i%2?'expSmall':'expBig',at:1.65+i*.25}]).flat(),...[.2,1,1.8,2.6,3.4].map(at=>({name:'enemyMissile',at}))]}),
   row('SWARM','swarm',HQ22.swarm,{who:'DECKER',text:'More are coming! We gotta warn the others!',c16Cues:[{name:'blip',at:.1},...[.2,1,1.8].map(at=>({name:'enemyMissile',at})),{name:'expBig',at:1.1},{name:'enemyMachineGunLight',at:2.1}]}),
   row('AXEL','escape',HQ22.escape,{who:'AXEL',text:'Punch it! I will warn the team!',c16Cues:[{name:'somersault',at:.1},{name:'jetDash',at:.6},{name:'somersault',at:1.0},{name:'jetDash',at:1.5},...[.15,.9,1.8,2.7].map(at=>({name:'enemyMissile',at})),{name:'expBig',at:2.3},{name:'gd_doorOpen',at:2.4}]})
  );
 }
 return rows;
}
c16Rows=function(id,p=run.pilot,route=s113Route()){return id==='post-5'?hq19Rows(p):HQ19.base.rows.apply(this,arguments);};
C16.rows=CM3.rows=FP5.rows=c16Rows;
function hq19Keys(p=run.pilot){
 const keys=[...Object.values(HQ19_ART.banks),...Object.values(HQ20_ART.pilots),HQ20_ART.door,...Object.values(HQ21_ART.pilots),...Object.values(HQ22_ART.flips)].map(a=>a.key);
 for(const pk of HQ19_PILOTS)for(const pose of ['neutral','back','happy','ecstatic','jump_cheer'])keys.push(C112.key(pk,pose));
 for(const pk of d1110Active(p)){
  for(const pose of ['walk_0','walk_1','walk_2','walk_3'])keys.push(C112.key(pk,pose));
  for(const bank of ['exit','walk'])for(const a of HL10_ART[pk+'_'+bank])keys.push(a.key);
  for(const tail of ['','_g1','_g2'])keys.push('ship_'+pk+tail);
 }
 for(const pk of HQ19_PILOTS)for(const tail of ['','_g1','_g2'])keys.push('ship_'+pk+tail);
 for(let i=0;i<8;i++)keys.push('cinfx_airburst_'+i);
 for(let i=0;i<4;i++)keys.push('weapon_muzzle_rotary_'+i);
 keys.push('whv_ace','mgcf_1_5','h3_earth','bg_stage05_loop_0923','pav_decker','pav_axel','cd27_neutral_460');
 for(const a of HL10_ART.shadow)keys.push(a.key);
 for(let i=0;i<8;i++)keys.push('cinfx_missile_'+i);
 for(const id of ['stealth_red','stealth_green','stealth_orange']){const m=AF21.aliases.get(id)?.M;for(const kind of ['idle','attack'])if(m?.banks[kind])keys.push(m.banks[kind].key);}
 for(let i=0;i<4;i++)keys.push('weapon_muzzle_missile_'+i);
 for(const pk of ['decker','axel'])for(const suffix of ['_pv0','_pv1','_pv3','_pv4'])for(const tail of ['','_g1','_g2'])keys.push('ship_'+pk+suffix+tail);
 return [...new Set(keys.filter(Boolean))];
}
d1110Keys=function(rows,p=run.pilot){const own=rows.some(b=>b.hq19),other=rows.filter(b=>!b.hq19);return [...new Set([...(other.length?HQ19.base.keys.call(this,other,p):[]),...(own?hq19Keys(p):[])])];};
stageLoadBegin=function(n,keys){return HQ19.base.load.call(this,n,n===5?[...(keys||[]),...hq19Keys()]:keys);};
d1110Step=function(s,dt,onAdvance,onFinish){const b=s.beats[s.i],before=s.t;const out=HQ19.base.step.apply(this,arguments);
 if(b?.hq19&&s.beats[s.i]===b){for(const q of b.c16Cues||[])d1110Cue(s,b,q.name,q.at,before);
  if(['defend','swarm','escape'].includes(b.hq19))run._hq19Scrambled=true;}
 return out;};
function hq19Backdrop(name,frame,box){const a=name==='exterior'?HQ20_ART.door:HQ19_ART.banks[name];if(!a||!XART.rdy(a.key))return null;
 const[x,y,w,h]=box,k=Math.max(w/a.w,h/a.h),dw=a.w*k,dh=a.h*k,f=clamp(Math.floor(frame),0,a.frames-1),r={x:x+(w-dw)/2,y:y+(h-dh)/2,w:dw,h:dh};
 ctx.drawImage(XART.get(a.key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,r.x,r.y,dw,dh);return r;}
function hq19Parked(pk){if(HQ19.parked.has(pk))return HQ19.parked.get(pk);const key='ship_'+pk,tails=pf27TailParts(key);if(!tails||!XART.rdy(key+'_g1')||!XART.rdy(key+'_g2'))return XART.get(key);
 const src=D27_RAW_GET(key),hi=D27_RAW_GET(key+'_g1'),lo=D27_RAW_GET(key+'_g2'),c=document.createElement('canvas');c.width=src.width;c.height=src.height;const g=c.getContext('2d');g.drawImage(src,0,0);const d=g.getImageData(0,0,c.width,c.height);
 const tmp=document.createElement('canvas');tmp.width=c.width;tmp.height=c.height;const q=tmp.getContext('2d');q.drawImage(hi,0,0);const a=q.getImageData(0,0,c.width,c.height).data;q.clearRect(0,0,c.width,c.height);q.drawImage(lo,0,0);const b=q.getImageData(0,0,c.width,c.height).data;
 for(const r of tails.parts)for(let y=r.y;y<r.y+r.h;y++)for(let x=r.x;x<r.x+r.w;x++){const i=(y*c.width+x)*4;if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2])d.data[i+3]=0;}
 g.putImageData(d,0,0);HQ19.parked.set(pk,c);return c;}
function hq21BankKey(pk,bank){const ab=Math.abs(bank),right=SHIP_BANK_FLIP[pk]?bank<0:bank>0;return 'ship_'+pk+(ab<.12?'':ab<.48?(right?'_pv3':'_pv1'):(right?'_pv4':'_pv0'));}
function hq21FlightHull(key,t,h,power){const im=D27_RAW_GET(key),w=h*im.width/im.height,previous=player._thrustFrame;player._thrustFrame=Math.floor(t*15)%6;
 try{ctx.drawImage(im,-w/2,-h/2,w,h);pf27PlaneThrustDraw(ctx,key,0,0,w,h,power);}finally{player._thrustFrame=previous;}}
function hq19Ship(pk,t,x,y,h,power,south=false,heading=null,bank=null){ctx.save();ctx.translate(x,y);const rotation=heading??(south?Math.PI:0),key=bank===null?'ship_'+pk:hq21BankKey(pk,bank);ctx.rotate(rotation);
 if(power>0){if(bank===null)pt11OpeningShip(pk,t,0,0,h,power);else hq21FlightHull(key,t,h,power);}else{const im=hq19Parked(pk);if(im)ctx.drawImage(im,-h*im.width/im.height/2,-h/2,h*im.width/im.height,h);}
 ctx.restore();return{pilot:pk,key,x,y,h,power,south,heading:rotation,bank};}
function hq20Performance(pk,kind,t,x,foot,height){const a=HQ20_ART.pilots[pk];if(!a||!XART.rdy(a.key))return null;
 const f=(kind==='walk'?0:8)+Math.floor(Math.max(0,t)*(kind==='walk'?10:6))%8,k=height/a.bodyHeight;
 ctx.drawImage(XART.get(a.key),f%4*a.w,Math.floor(f/4)*a.h,a.w,a.h,x-a.pivot[0]*k,foot-a.pivot[1]*k,a.w*k,a.h*k);
 return{pilot:pk,key:a.key,pose:kind,frame:f,x,foot,height};}

function hq19Actor(pk,clip,f,x,foot,height){const a=HL10_ART[pk+'_'+clip]?.[f],body=hl10BodyGeometry(pk);if(!a||!XART.rdy(a.key))return;
 const k=height/body.height;ctx.drawImage(XART.get(a.key),x-a.pivot[0]*k,foot-(a.pivot[1]+body.foot)*k,a.w*k,a.h*k);return{pilot:pk,key:a.key,x,foot,height};}
function hq19Exterior(b,s,box){const t=s.t,mode=b.hq19,actors=[],ships=[];let door=0;
 if(mode==='enter')door=t<1.5?0:t<4.9?Math.min(15,(t-1.5)/1.2*16):Math.max(0,15-(t-4.9)/1.3*16);
 const r=hq19Backdrop('exterior',door,box);if(!r)return;const pad={x:r.x+r.w*.5,y:r.y+r.h*.727},entry={x:r.x+r.w*.5,y:r.y+r.h*.451};
 const active=d1110Active(),spacing=active.length>1?76:0;
 active.forEach((pk,i)=>{const x=pad.x+(i-(active.length-1)/2)*spacing,u=hq19Ease(t/4.3),land=mode==='land';
  const sy=land?lerp(box[1]+box[3]+150,pad.y,u):pad.y,h=land?lerp(172,82,u):82,power=land&&t<4.3?lerp(.95,.1,u):0;
  hl10Cell('shadow',Math.min(3,Math.floor((land?u:1)*4)),x+5,pad.y+19,72);
  ships.push(hq19Ship(pk,t,x,sy,h,power));
  if(mode==='exit')actors.push(hq19Actor(pk,'exit',Math.min(7,Math.floor(t/2.7*8)),lerp(x,x+31,hq19Ease(t/2.7)),pad.y+27,30));
  if(mode==='enter'){const walk=clamp((t-i*.3)/4.9,0,1),e=hq19Ease(walk),ax=lerp(x+31,entry.x+(i?8:-8),e),ay=lerp(pad.y+27,entry.y-16,e);
   if(walk<1){ctx.save();if(walk>.82){ctx.beginPath();ctx.rect(entry.x-62,entry.y-37,124,47);ctx.clip();}actors.push(hq19Actor(pk,'walk',Math.floor(t*9)%8,ax,ay,lerp(30,23,e)));ctx.restore();}}
 });
 HQ19.last={mode,time:t,door:clamp(Math.floor(door),0,15),ships,actors,pad,entry,solidPanel:true};
}
function hq19Interior(b,s,box){const t=s.t,mode=b.hq19,active=d1110Active(),cast=[];
 if(mode==='corridor'){hq19Backdrop('corridor',0,box);active.forEach((p,i)=>{const u=hq19Ease(clamp((t-i*.4)/5.8,0,1)),x=lerp(95,830,u);cast.push(hq20Performance(p,'walk',t,x,439+i*12,230));});}
 else{const f=mode==='radar'?(t<2?Math.min(15,Math.floor(t*8)):8+Math.floor((t-2)*8)%8):0;hq19Backdrop('radar',f,box);
  if(mode==='radar'){HQ19_PILOTS.forEach((p,i)=>{const x=160+i*74,foot=460+Math.abs(i-4)*4;C112.draw(p,'back',x,foot,225);cast.push({pilot:p,pose:'back',x,foot});});}
  else{const crew=HQ19_PILOTS.filter(p=>!active.includes(p));crew.forEach((p,i)=>{const x=360+(i%5)*97,foot=i<5?414:478;cast.push(hq20Performance(p,'cheer',t+i*.17,x,foot,p==='juggernaut'?220:205));});
   active.forEach((p,i)=>{const x=lerp(65-i*60,245-i*85,hq19Ease(t/2.5)),foot=467+i*15;cast.push(hq20Performance(p,t<2.5?'walk':'cheer',t<2.5?t:t-2.5,x,foot,220));});}
  HQ19.last={mode,time:t,frame:f,cast:cast.filter(Boolean),solidPanel:true};return;
 }
 HQ19.last={mode,time:t,cast:cast.filter(Boolean),solidPanel:true};
}

function hq19Launch(pk,t,start,index,r,origin=null){const duration=HQ22.flight,u=clamp((t-start)/duration,0,1);if(t<start||u>=1)return null;
 const side=index%2===0?-1:1,v=.4*u+.6*u*u,cx=r.x+r.w*.5,p0=origin||{x:cx,y:r.y+r.h*.451,h:25},p1={x:p0.x,y:p0.y+110},p2={x:p0.x+side*r.w*.28,y:r.y+r.h*.83},p3={x:cx+side*r.w*.64,y:hq19Bottom(r)+210},iv=1-v;
 const x=iv**3*p0.x+3*iv*iv*v*p1.x+3*iv*v*v*p2.x+v**3*p3.x,y=iv**3*p0.y+3*iv*iv*v*p1.y+3*iv*v*v*p2.y+v**3*p3.y;
 const a=HQ21_ART.pilots[pk==='lizzie'&&typeof lizzieSkinOn!=='undefined'&&lizzieSkinOn?'lizzie_b42':pk];if(!a||!XART.rdy(a.key))return null;const frame=Math.min(a.frames-1,Math.floor(u*a.frames)),pose=a.poses[frame],h=lerp(p0.h||25,172,u),k=h/a.bodyHeight;
 // Heading, wing bank and exhaust are authored together in this fixed-pivot cell.
 ctx.drawImage(XART.get(a.key),frame%a.cols*a.w,Math.floor(frame/a.cols)*a.h,a.w,a.h,x-a.pivot[0]*k,y-a.pivot[1]*k,a.w*k,a.h*k);
 return{pilot:pk,key:a.key,x,y,h,power:.95,south:true,heading:pose.heading,bank:pose.bank,sourceKey:pose.sourceKey,turnFrame:frame,start,duration,side:side<0?'southwest':'southeast',progress:u};}
function hq19Bottom(r){return r.y+r.h;}
function hq20EnemyPose(i,age,r){const born=i<2?0:(i-1)*HQ22.spawn,u=clamp((age-born)/HQ22.arrival,0,1),a=i*2.39996+age*(i%2?.22:-.23),cx=r.x+r.w*.5,cy=r.y+r.h*.35,rad=.20+(i%6)*.023;
 const x=lerp(r.x+(i%2?r.w+70:-70),cx+Math.cos(a)*r.w*rad,hq19Ease(u)),y=lerp(r.y-70,cy+Math.sin(a)*r.h*(.20+(i%4)*.026),hq19Ease(u));return{id:i,born,u,x,y,angle:Math.atan2(cy-y,cx-x),h:i%3===0?48+(i%2)*4:36+(i%3)*4};}
const HQ20_KILLS=Array.from({length:10},(_,i)=>({id:i,at:1.65+i*.25,pilot:i%2?'axel':'decker'}));
function hq22Stealth(i){return i%3===0?'stealth_'+['red','green','orange'][Math.floor(i/3)%3]:null;}
function hq22Missiles(age,defense,r){const missiles=[];
 for(let id=0;id<HQ22.maxEnemies;id++){const role=hq22Stealth(id);if(!role)continue;const born=id<2?0:(id-1)*HQ22.spawn,hit=HQ20_KILLS.find(q=>q.id===id);
  for(let volley=0;volley<14;volley++){const launchAt=born+.55+volley*.9,life=age-launchAt;if(life<0||life>1.03||defense!==null&&hit&&launchAt>=HQ22.attack+hit.at)continue;
   const e=hq20EnemyPose(id,launchAt,r),side=volley%2?1:-1,nx=e.x+Math.cos(e.angle)*e.h*.16+Math.cos(e.angle+Math.PI/2)*side*e.h*.22,ny=e.y+Math.sin(e.angle)*e.h*.16+Math.sin(e.angle+Math.PI/2)*side*e.h*.22;
   const tx=r.x+r.w*(.50+((id+volley)%5-2)*.045),ty=r.y+r.h*(.25+((id+volley)%3)*.07),u=clamp(life/.68,0,1),v=u*u,a=Math.atan2(ty-ny,tx-nx),x=lerp(nx,tx,v),y=lerp(ny,ty,v);
   if(life<.68){cinFx('missile',x,y,34,life,a-Math.PI/2);if(life<.14)wm26Draw(ctx,'missile',nx,ny,a,life/.14,20);}else cinFx('airburst',tx,ty,58,life-.68);
   missiles.push({launcher:id,role,launchAt,life,x,y,target:{x:tx,y:ty},impact:life>=.68});
  }
 }
 return missiles;}
function hq19Attack(age,r,defense=null){const jets=[],shots=[],kills=[],im=XART.rdy('whv_ace')?XART.get('whv_ace'):null,n=Math.min(HQ22.maxEnemies,2+Math.floor(age/HQ22.spawn));if(!im)return{jets,shots,kills,missiles:[]};
 for(let i=0;i<n;i++){const hit=defense===null?null:HQ20_KILLS.find(q=>q.id===i),since=hit?defense-hit.at:-1;
  if(since>=0){const p=hq20EnemyPose(i,HQ22.attack+hit.at,r);kills.push({...hit,x:p.x,y:p.y,age:since});if(since<.5)cinFx('airburst',p.x,p.y,90,since);continue;}
  const p=hq20EnemyPose(i,age,r),{x,y,angle:ang,h,u,born}=p,role=hq22Stealth(i),flash=hit&&defense>=hit.at-.08;
  let source='whv_ace';if(role){const pose=af21Pose(role,'attack',(age-born)*1.8);if(pose){pose.rotation=ang-Math.PI/2;af21Draw(pose,x,y,h,1,flash?'#ffffff':null);source=pose.key;}}
  else{const plate=flash?xartTint('whv_ace','#ffffff'):im,w=h*im.width/im.height;ctx.save();ctx.translate(x,y);ctx.rotate(ang-Math.PI/2);ctx.drawImage(plate,-w/2,-h/2,w,h);ctx.restore();}
  jets.push({key:source,role:role||'fighter',flash:!!flash,...p});
  const beat=(age-born+i*.17)%.55;if(u>.65&&beat<.26){const nx=x+Math.cos(ang)*h*.39,ny=y+Math.sin(ang)*h*.39;wm26Draw(ctx,'mg',nx,ny,ang,beat/.26,15);
   for(let j=0;j<3;j++){const v=clamp(beat/.26-j*.19,0,1);if(v<=0)continue;const px=lerp(nx,r.x+r.w*.5,v),py=lerp(ny,r.y+r.h*.35,v);drawMfx('mgcf_1_5',px,py,ang-Math.PI/2,12,null,1,'#ffd36b');shots.push({x:px,y:py,from:{x:nx,y:ny}});}}
 }
 for(let i=0;i<4;i++){const t=(age-i*.23)%.75;if(t<0||t>.45)continue;cinFx('airburst',r.x+r.w*(.34+(i%3)*.16),r.y+r.h*(.22+(i%2)*.24),45+(i%2)*25,t);}
 return{jets,shots,kills,missiles:hq22Missiles(age,defense,r)};}
function hq21GuardHeading(pk,t,r){const side=pk==='decker'?-1:1,born=HQ22.guardBorn[pk],q=clamp((t-born)/.55,0,1),cx=r.x+r.w*.5,padY=r.y+r.h*.727,x=lerp(cx,cx+side*r.w*.13,hq19Ease(q)),y=lerp(r.y+r.h*.451,padY+18,hq19Ease(q));
 const own=HQ20_KILLS.filter(k=>k.pilot===pk),angle=k=>{const e=hq20EnemyPose(k.id,HQ22.attack+k.at,r);return Math.atan2(e.y-y,e.x-x)+Math.PI/2;},delta=(a,b)=>((b-a+Math.PI*3)%(Math.PI*2))-Math.PI;
 let aim=angle(own[0]);for(let i=1;i<own.length;i++){const at=own[i-1].at+.025;if(t>at)aim+=delta(aim,angle(own[i]))*hq19Ease((t-at)/.12);}
 const initial=side<0?-Math.PI:Math.PI;let heading=initial+delta(initial,aim)*hq19Ease((q-.2)/.8),ready=HQ21_ART.pilots[pk].poses[0].heading;
 if(t>HQ22.flipStart[pk]-.42)heading+=delta(heading,ready)*hq19Ease((t-HQ22.flipStart[pk]+.42)/.30);return heading;}
function hq22Flip(pk,t,x,y,h){const a=HQ22_ART.flips[pk],u=clamp((t-HQ22.flipStart[pk])/HQ22.flipDuration,0,1),f=Math.min(7,Math.floor(u*8)),k=h/a.bodyHeight,dy=y-Math.sin(u*Math.PI)*24;
 ctx.drawImage(XART.get(a.key),f%4*a.w,Math.floor(f/4)*a.h,a.w,a.h,x-a.pivot[0]*k,dy-a.pivot[1]*k,a.w*k,a.h*k);
 return{pilot:pk,key:a.key,x,y:dy,h,motion:'somersault',flipFrame:f,progress:u,heading:a.heading};}
function hq20Defenders(et,r){const ships=[],fire=[],cx=r.x+r.w*.5,padY=r.y+r.h*.727;
 for(const[p,index,side]of [['decker',7,-1],['axel',8,1]]){const born=HQ22.guardBorn[p],start=HQ22.boostStart[p];if(et<born)continue;
  const q=clamp((et-born)/.55,0,1),x=lerp(cx,cx+side*r.w*.13,hq19Ease(q)),y=lerp(r.y+r.h*.451,padY+18,hq19Ease(q)),h=lerp(25,96,q),turnTime=Math.floor(et*15)/15,heading=hq21GuardHeading(p,turnTime,r),previous=hq21GuardHeading(p,turnTime-1/15,r),turnDelta=((heading-previous+Math.PI*3)%(Math.PI*2))-Math.PI,bank=clamp(turnDelta*15/4,-.46,.46);
  if(et>=start){const launch=hq19Launch(p,et,start,index,r,{x:cx+side*r.w*.13,y:padY+18,h:96,heading:HQ21_ART.pilots[p].poses[0].heading});if(launch)ships.push({...launch,motion:'boost'});continue;}
  if(et>=HQ22.flipStart[p]){ships.push(hq22Flip(p,et,x,y,96));continue;}
  ships.push({...hq19Ship(p,turnTime,x,y,h,.45,false,heading,bank),defending:true,motion:'defend'});
  for(const k of HQ20_KILLS.filter(k=>k.pilot===p)){const firing=et-(k.at-.35);if(firing<0||firing>=.35)continue;const to=hq20EnemyPose(k.id,HQ22.attack+k.at,r),a=Math.atan2(to.y-y,to.x-x),nx=x+Math.cos(a)*h*.39,ny=y+Math.sin(a)*h*.39;wm26Draw(ctx,'mg',nx,ny,a,(firing%.08)/.08,22);
   for(let j=0;j<4;j++){const u=clamp(firing/.35-j*.15,0,1);if(u<=0)continue;const px=lerp(nx,to.x,u),py=lerp(ny,to.y,u);drawMfx('mgcf_1_5',px,py,a-Math.PI/2,17,null,1,'#fff4a3');fire.push({pilot:p,target:k.id,x:px,y:py,from:{x:nx,y:ny},to:{x:to.x,y:to.y},impactAt:k.at});}
  }
 }
 return{ships,fire};}
function hq19Evac(b,s,box){const mode=b.hq19,t=s.t,guard=['defend','swarm','escape'].includes(mode),et=t+(mode==='swarm'?HQ22.defend:mode==='escape'?HQ22.defend+HQ22.swarm:0),age=mode==='attack'?t:HQ22.attack+et;
 const door=mode==='launch'?Math.min(15,t/.85*16):mode==='quiet'?Math.max(0,15-t/.7*16):guard?(et>9.4?Math.max(0,15-(et-9.4)/.7*16):Math.min(15,et/.55*16)):0,r=hq19Backdrop('exterior',door,box);if(!r)return;
 let attack={jets:[],shots:[],kills:[],missiles:[]},ships=[],friendlyShots=[];
 if(mode==='launch')HQ19_SQUAD.forEach((p,i)=>{const q=hq19Launch(p,t,1.1+i*HQ22.spacing,i,r);if(q)ships.push(q);});
 if(mode==='attack'||guard)attack=hq19Attack(age,r,guard?et:null);
 if(guard){const defense=hq20Defenders(et,r);ships=defense.ships;friendlyShots=defense.fire;}
 HQ19.last={mode,time:t,defenseTime:guard?et:null,attackAge:mode==='quiet'||mode==='launch'?null:age,door:clamp(Math.floor(door),0,15),ships,enemies:attack.jets,shots:attack.shots,kills:attack.kills,missiles:attack.missiles,friendlyShots,quietDuration:mode==='quiet'?b.duration:0,solidPanel:true};
}
d1110Visual=function(b,s){if(!b.hq19)return HQ19.base.visual.apply(this,arguments);const box=[12,12,888,488];ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#050a10';ctx.fillRect(0,0,912,512);
 c16Clip(box,()=>{if(['land','exit','enter'].includes(b.hq19))hq19Exterior(b,s,box);else if(['corridor','welcome','radar'].includes(b.hq19))hq19Interior(b,s,box);else hq19Evac(b,s,box);});sl14Frame(box);
 if(b.text)dlgBox({who:b.who,portrait:b.who.toLowerCase(),full:b.text,shown:b.text.slice(0,s.shown),forceShown:true,y:16,screenSpace:false});
 const fadeOut=['enter','corridor','welcome','radar','escape'].includes(b.hq19)?clamp((s.t-b.duration+.4)/.4,0,1):0;
 const fadeIn=['land','corridor','welcome','radar','launch'].includes(b.hq19)?1-clamp(s.t/.45,0,1):0,fade=Math.max(fadeOut,fadeIn);
 if(fade){ctx.fillStyle='rgba(0,0,0,'+fade+')';ctx.fillRect(0,0,912,512);}
 msgFaceUse('dialogue');controlHintRow([['pad_start','SKIP']],730,505,887,9);msgFaceUse(null);ctx.restore();D1110.last={...HQ19.last,id:s.id,shot:b.id,pilot:run.pilot,text:b.text,shown:s.shown};};
// Finish the existing real destruction first; its static orbital/Earth cutaways
// are replaced only after the original armor breakup reaches its native end.
h3EndingTick=function(dt){const e=H3.ending;if(!e?.hf17||e.hf17.phase!=='after')return HQ19.base.endingTick.apply(this,arguments);
 const r=e.hq19Return||(e.hq19Return={t:0}),scrollDt=Math.min(dt,Math.max(0,4.8-r.t));r.t+=dt;stageEnding=0;whiteBlast=0;shake=0;_stage5SpaceScroll+=scrollDt*210;efxTick(dt);
 if(r.t>=HQ19.returnDuration){e.t=24;e.cheer=H3_CHEERS.length;e.descent=9.8;HQ19.base.endingTick.call(this,dt);}
};
function hq19ReturnDraw(e){const r=e.hq19Return||(e.hq19Return={t:0}),t=r.t;ctx.save();worldXformEscape();
 if(t>=4.8&&r.background){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.drawImage(r.background,0,0,cv.width,cv.height);ctx.restore();}
 else{ctx.save();ctx.translate(-camX,0);drawBG(0);ctx.restore();if(t>=4.8){r.background=document.createElement('canvas');r.background.width=cv.width;r.background.height=cv.height;r.background.getContext('2d').drawImage(cv,0,0);}}
 const visible=t>=2.4,size=VW*.76,planetY=lerp(-size*.6,VH*.61,hq19Ease((t-2.4)/2.4));
 if(visible&&XART.rdy('h3_earth')){const im=XART.get('h3_earth'),h=size*im.height/im.width;ctx.drawImage(im,VW/2-size/2,planetY-h/2,size,h);}
 let ship=null;if(t<2.6){const y=lerp(VH*.78,-170,hq19Ease(t/2.6)),h=SPACE_SHIP_SIZE*1.5;furyShipDrawFlight(VW/2,y,h,run.pilot,{key:'base'},t);ship={x:VW/2,y,h,south:false};}
 else if(t>=4.8){const u=hq19Ease((t-4.8)/6.5),y=lerp(-90,VH*.61,u),h=lerp(SPACE_SHIP_SIZE*1.5,3,u);ctx.save();ctx.translate(VW/2,y);ctx.rotate(Math.PI);furyShipDrawFlight(0,0,h,run.pilot,{key:'base'},t);ctx.restore();ship={x:VW/2,y,h,south:true};}
 const fade=clamp((t-11.6)/.8,0,1);if(fade){ctx.fillStyle='rgba(0,0,0,'+fade+')';ctx.fillRect(0,0,VW,VH);}ctx.restore();HQ19.last={mode:'earth-return',phase:t<2.4?'space-departure':t<4.8?'earth-reveal':'earth-descent',time:t,earthVisible:visible,planetY,ship,fade,scrollFrozen:t>=4.8};}
h3EndingDraw=function(){const e=H3.ending;if(e?.hf17?.phase==='after')return hq19ReturnDraw(e);return HQ19.base.endingDraw.apply(this,arguments);};
// Scope the revised radio continuity to the squad that just evacuated this HQ.
s6OpeningTick=function(dt){const out=HQ19.base.openingTick.apply(this,arguments),O=s6Opening;if(run._hq19Scrambled&&O?.radio){const lines=['FURY FLIGHT, REGROUP OVER THE CITY!','AXEL AND I ARE CLEAR! WE ARE HEADING YOUR WAY!','THOSE FIGHTERS FOLLOWED US FROM HQ!','KEEP YOUR EYES OPEN...','LOOK OUT! STEALTH FIGHTERS ON BOTH SIDES!'];const i=O.radioIndex-1;if(lines[i])O.radio.full=lines[i];if([1,3,4].includes(i))O.radio.who='DECKER';}return out;};
HQ19.rows=hq19Rows;HQ19.preview=(p='cole')=>D1110.preview('post-5',p);window.BOF_HQ_RETURN_ATTACK_1114=HQ19;
