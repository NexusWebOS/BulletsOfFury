"use strict";
/* HQ19: native Chronos destruction -> delayed Earth approach -> physical HQ
   homecoming -> crew/radar -> evacuation and base assault. Combat stays native. */
const HQ19={base:{rows:c16Rows,keys:d1110Keys,step:d1110Step,visual:d1110Visual,load:stageLoadBegin,
 endingTick:h3EndingTick,endingDraw:h3EndingDraw,openingTick:s6OpeningTick},last:null,events:[],parked:new Map(),returnDuration:12.4};
for(const a of Object.values(HQ19_ART.banks))XART._src[a.key]=a.path+'?v='+a.sha256.slice(0,12);
const HQ19_PILOTS=['cole','axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva'];
const HQ19_SQUAD=HQ19_PILOTS.filter(p=>p!=='decker'&&p!=='axel');
const HQ19_AUDIO=['gd_doorOpen','gd_footstepA','gd_footstepB','jetDash','gravityLock','blip','enemyMachineGunLight','expSmall','expBig','select'];
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
   row('LAUNCH','launch',9.2,{c16Cues:[{name:'gd_doorOpen',at:.1},...HQ19_SQUAD.map((_,i)=>({name:'jetDash',at:1.5+i*.7}))]}),
   row('QUIET','quiet',5.0,{c16Cues:[{name:'gd_doorOpen',at:.12}]}),
   row('ATTACK','attack',3.4,{c16Cues:[{name:'enemyMachineGunLight',at:.7},{name:'expSmall',at:1.1},{name:'enemyMachineGunLight',at:1.8},{name:'expSmall',at:2.6}]}),
   row('DECKER','escape-decker',4.2,{who:'DECKER',text:'Dammit! They made it to our base too!',c16Cues:[{name:'gd_doorOpen',at:.05},{name:'jetDash',at:1.1},{name:'jetDash',at:2.0},{name:'enemyMachineGunLight',at:2.6},{name:'expBig',at:3.2}]}),
   row('AXEL','escape-axel',4.6,{who:'AXEL',text:'We gotta tell the others!',c16Cues:[{name:'enemyMachineGunLight',at:.4},{name:'expSmall',at:1.1},{name:'enemyMachineGunLight',at:2.0},{name:'expBig',at:3.2}]})
  );
 }
 return rows;
}
c16Rows=function(id,p=run.pilot,route=s113Route()){return id==='post-5'?hq19Rows(p):HQ19.base.rows.apply(this,arguments);};
C16.rows=CM3.rows=FP5.rows=c16Rows;
function hq19Keys(p=run.pilot){
 const keys=Object.values(HQ19_ART.banks).map(a=>a.key);
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
 return [...new Set(keys.filter(Boolean))];
}
d1110Keys=function(rows,p=run.pilot){const own=rows.some(b=>b.hq19),other=rows.filter(b=>!b.hq19);return [...new Set([...(other.length?HQ19.base.keys.call(this,other,p):[]),...(own?hq19Keys(p):[])])];};
stageLoadBegin=function(n,keys){return HQ19.base.load.call(this,n,n===5?[...(keys||[]),...hq19Keys()]:keys);};
d1110Step=function(s,dt,onAdvance,onFinish){const b=s.beats[s.i],before=s.t;const out=HQ19.base.step.apply(this,arguments);
 if(b?.hq19&&s.beats[s.i]===b){for(const q of b.c16Cues||[])d1110Cue(s,b,q.name,q.at,before);
  if(b.hq19.startsWith('escape-'))run._hq19Scrambled=true;}
 return out;};
function hq19Backdrop(name,frame,box){const a=HQ19_ART.banks[name];if(!a||!XART.rdy(a.key))return null;
 const[x,y,w,h]=box,k=Math.max(w/a.w,h/a.h),dw=a.w*k,dh=a.h*k,f=clamp(Math.floor(frame),0,a.frames-1),r={x:x+(w-dw)/2,y:y+(h-dh)/2,w:dw,h:dh};
 ctx.drawImage(XART.get(a.key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,r.x,r.y,dw,dh);return r;}
function hq19Parked(pk){if(HQ19.parked.has(pk))return HQ19.parked.get(pk);const key='ship_'+pk,tails=pf27TailParts(key);if(!tails||!XART.rdy(key+'_g1')||!XART.rdy(key+'_g2'))return XART.get(key);
 const src=D27_RAW_GET(key),hi=D27_RAW_GET(key+'_g1'),lo=D27_RAW_GET(key+'_g2'),c=document.createElement('canvas');c.width=src.width;c.height=src.height;const g=c.getContext('2d');g.drawImage(src,0,0);const d=g.getImageData(0,0,c.width,c.height);
 const tmp=document.createElement('canvas');tmp.width=c.width;tmp.height=c.height;const q=tmp.getContext('2d');q.drawImage(hi,0,0);const a=q.getImageData(0,0,c.width,c.height).data;q.clearRect(0,0,c.width,c.height);q.drawImage(lo,0,0);const b=q.getImageData(0,0,c.width,c.height).data;
 for(const r of tails.parts)for(let y=r.y;y<r.y+r.h;y++)for(let x=r.x;x<r.x+r.w;x++){const i=(y*c.width+x)*4;if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2])d.data[i+3]=0;}
 g.putImageData(d,0,0);HQ19.parked.set(pk,c);return c;}
function hq19Ship(pk,t,x,y,h,power,south=false){ctx.save();ctx.translate(x,y);if(south)ctx.rotate(Math.PI);
 if(power>0)pt11OpeningShip(pk,t,0,0,h,power);else{const im=hq19Parked(pk);if(im)ctx.drawImage(im,-h*im.width/im.height/2,-h/2,h*im.width/im.height,h);}
 ctx.restore();return{pilot:pk,key:'ship_'+pk,x,y,h,power,south};}
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
 if(mode==='corridor'){hq19Backdrop('corridor',0,box);active.forEach((p,i)=>{const u=hq19Ease(clamp((t-i*.4)/5.8,0,1)),x=lerp(95,830,u);C112.stride(p,'walk',t,x,439+i*12,270);cast.push({pilot:p,pose:'walk',x});});}
 else{const f=mode==='radar'?(t<2?Math.min(15,Math.floor(t*8)):8+Math.floor((t-2)*8)%8):0;hq19Backdrop('radar',f,box);
  if(mode==='radar'){HQ19_PILOTS.forEach((p,i)=>{const x=160+i*74,foot=460+Math.abs(i-4)*4;C112.draw(p,'back',x,foot,225);cast.push({pilot:p,pose:'back',x,foot});});}
  else{const crew=HQ19_PILOTS.filter(p=>!active.includes(p));crew.forEach((p,i)=>{const x=360+(i%5)*97,foot=i<5?414:478,poses=['happy','ecstatic','happy','jump_cheer'],pose=poses[(Math.floor(t*2)+i)%4];C112.draw(p,pose,x,foot,225);cast.push({pilot:p,pose,x,foot});});
   active.forEach((p,i)=>{const x=lerp(65-i*60,245-i*85,hq19Ease(t/2.5)),foot=467+i*15;if(t<2.5)C112.stride(p,'walk',t,x,foot,235);else C112.draw(p,'happy',x,foot,235);cast.push({pilot:p,pose:t<2.5?'walk':'happy',x,foot});});}
  HQ19.last={mode,time:t,frame:f,cast,solidPanel:true};return;
 }
 HQ19.last={mode,time:t,cast,solidPanel:true};
}
function hq19Launch(pk,t,start,index,r){const u=clamp((t-start)/3.5,0,1);if(t<start||u>=1)return null;
 const e=u*u,x=r.x+r.w*.5+(index-3)*r.w*.024*e,y=lerp(r.y+r.h*.451,hq19Bottom(r)+185,e),h=lerp(25,172,u);
 return hq19Ship(pk,t,x,y,h,.9,true);}
function hq19Bottom(r){return r.y+r.h;}
function hq19Attack(age,r){const jets=[],shots=[],im=XART.rdy('whv_ace')?XART.get('whv_ace'):null,n=Math.min(14,2+Math.floor(age/1.05));
 if(!im)return{jets,shots};
 for(let i=0;i<n;i++){const born=i<2?0:(i-1)*1.05,u=clamp((age-born)/1.0,0,1),a=i*2.39996+age*(i%2?.16:-.14),cx=r.x+r.w*.5,cy=r.y+r.h*.35,
  x=lerp(r.x+(i%2?r.w+70:-70),cx+Math.cos(a)*r.w*.32,hq19Ease(u)),y=lerp(r.y-70,cy+Math.sin(a)*r.h*.25,hq19Ease(u)),ang=Math.atan2(cy-y,cx-x),h=36+(i%3)*4,w=h*im.width/im.height;
  ctx.save();ctx.translate(x,y);ctx.rotate(ang-Math.PI/2);ctx.drawImage(im,-w/2,-h/2,w,h);ctx.restore();jets.push({key:'whv_ace',x,y,angle:ang});
  const beat=(age-born+i*.17)%.9;if(u>.65&&beat<.42){const nx=x+Math.cos(ang)*h*.39,ny=y+Math.sin(ang)*h*.39;wm26Draw(ctx,'mg',nx,ny,ang,beat/.42,15);
   for(let j=0;j<3;j++){const v=clamp(beat/.42-j*.19,0,1);if(v<=0)continue;const px=lerp(nx,cx,v),py=lerp(ny,cy,v);drawMfx('mgcf_1_5',px,py,ang-Math.PI/2,12,null,1,'#ffd36b');shots.push({x:px,y:py,from:{x:nx,y:ny}});}}
 }
 for(let i=0;i<5;i++){const t=(age-i*.23)%.85;if(t<0||t>.6)continue;cinFx('airburst',r.x+r.w*(.34+(i%3)*.16),r.y+r.h*(.22+(i%2)*.24),45+(i%2)*25,t);}
 return{jets,shots};}
function hq19Evac(b,s,box){const mode=b.hq19,t=s.t,escape=mode.startsWith('escape'),et=t+(mode==='escape-axel'?4.2:0),age=mode==='attack'?t:3.4+et;
 const door=mode==='launch'?Math.min(15,t/1.3*16):mode==='quiet'?Math.max(0,15-t/1.4*16):escape?Math.min(15,et/1.1*16):0,r=hq19Backdrop('exterior',door,box);if(!r)return;
 let attack={jets:[],shots:[]},ships=[];
 if(mode==='launch')HQ19_SQUAD.forEach((p,i)=>{const q=hq19Launch(p,t,1.5+i*.7,i,r);if(q)ships.push(q);});
 if(mode==='attack'||escape)attack=hq19Attack(age,r);
 if(escape)for(const[p,start,i]of [['decker',1.1,2],['axel',2.0,4]]){const q=hq19Launch(p,et,start,i,r);if(q)ships.push(q);}
 HQ19.last={mode,time:t,attackAge:mode==='quiet'||mode==='launch'?null:age,door:clamp(Math.floor(door),0,15),ships,enemies:attack.jets,shots:attack.shots,quietDuration:mode==='quiet'?b.duration:0,solidPanel:true};
}
d1110Visual=function(b,s){if(!b.hq19)return HQ19.base.visual.apply(this,arguments);const box=[12,12,888,488];ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#050a10';ctx.fillRect(0,0,912,512);
 c16Clip(box,()=>{if(['land','exit','enter'].includes(b.hq19))hq19Exterior(b,s,box);else if(['corridor','welcome','radar'].includes(b.hq19))hq19Interior(b,s,box);else hq19Evac(b,s,box);});sl14Frame(box);
 if(b.text)dlgBox({who:b.who,portrait:b.who.toLowerCase(),full:b.text,shown:b.text.slice(0,s.shown),forceShown:true,y:16,screenSpace:false});
 const fadeOut=['enter','corridor','welcome','radar','escape-axel'].includes(b.hq19)?clamp((s.t-b.duration+.4)/.4,0,1):0;
 const fadeIn=['land','corridor','welcome','radar','launch'].includes(b.hq19)?1-clamp(s.t/.45,0,1):0,fade=Math.max(fadeOut,fadeIn);
 if(fade){ctx.fillStyle='rgba(0,0,0,'+fade+')';ctx.fillRect(0,0,912,512);}
 msgFaceUse('dialogue');controlHintRow([['pad_start','SKIP']],730,505,887,9);msgFaceUse(null);ctx.restore();D1110.last={...HQ19.last,id:s.id,shot:b.id,pilot:run.pilot,text:b.text,shown:s.shown};};
// Finish the existing real destruction first; its static orbital/Earth cutaways
// are replaced only after the original armor breakup reaches its native end.
h3EndingTick=function(dt){const e=H3.ending;if(!e?.hf17||e.hf17.phase!=='after')return HQ19.base.endingTick.apply(this,arguments);
 const r=e.hq19Return||(e.hq19Return={t:0});r.t+=dt;stageEnding=0;whiteBlast=0;shake=0;_stage5SpaceScroll+=dt*210;efxTick(dt);
 if(r.t>=HQ19.returnDuration){e.t=24;e.cheer=H3_CHEERS.length;e.descent=9.8;HQ19.base.endingTick.call(this,dt);}
};
function hq19ReturnDraw(e){const t=e.hq19Return?.t||0;ctx.save();worldXformEscape();ctx.save();ctx.translate(-camX,0);drawBG(0);ctx.restore();
 const visible=t>=2.4,size=VW*.76,planetY=lerp(-size*.6,VH*.61,hq19Ease((t-2.4)/2.4));
 if(visible&&XART.rdy('h3_earth')){const im=XART.get('h3_earth'),h=size*im.height/im.width;ctx.drawImage(im,VW/2-size/2,planetY-h/2,size,h);}
 let ship=null;if(t<2.6){const y=lerp(VH*.78,-170,hq19Ease(t/2.6)),h=SPACE_SHIP_SIZE*1.5;furyShipDrawFlight(VW/2,y,h,run.pilot,{key:'base'},t);ship={x:VW/2,y,h,south:false};}
 else if(t>=4.8){const u=hq19Ease((t-4.8)/6.5),y=lerp(-90,VH*.61,u),h=lerp(SPACE_SHIP_SIZE*1.5,3,u);ctx.save();ctx.translate(VW/2,y);ctx.rotate(Math.PI);furyShipDrawFlight(0,0,h,run.pilot,{key:'base'},t);ctx.restore();ship={x:VW/2,y,h,south:true};}
 const fade=clamp((t-11.6)/.8,0,1);if(fade){ctx.fillStyle='rgba(0,0,0,'+fade+')';ctx.fillRect(0,0,VW,VH);}ctx.restore();HQ19.last={mode:'earth-return',phase:t<2.4?'space-departure':t<4.8?'earth-reveal':'earth-descent',time:t,earthVisible:visible,planetY,ship,fade};}
h3EndingDraw=function(){const e=H3.ending;if(e?.hf17?.phase==='after')return hq19ReturnDraw(e);return HQ19.base.endingDraw.apply(this,arguments);};
// Scope the revised radio continuity to the squad that just evacuated this HQ.
s6OpeningTick=function(dt){const out=HQ19.base.openingTick.apply(this,arguments),O=s6Opening;if(run._hq19Scrambled&&O?.radio){const lines=['FURY FLIGHT, REGROUP OVER THE CITY!','AXEL AND I ARE CLEAR! WE ARE HEADING YOUR WAY!','THOSE FIGHTERS FOLLOWED US FROM HQ!','KEEP YOUR EYES OPEN...','LOOK OUT! STEALTH FIGHTERS ON BOTH SIDES!'];const i=O.radioIndex-1;if(lines[i])O.radio.full=lines[i];if([1,3,4].includes(i))O.radio.who='DECKER';}return out;};
HQ19.rows=hq19Rows;HQ19.preview=(p='cole')=>D1110.preview('post-5',p);window.BOF_HQ_RETURN_ATTACK_1114=HQ19;
