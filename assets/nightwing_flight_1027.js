'use strict';
/* Authored whole-ship banking/depth; native Harrier/Nightwing life and rewards. */
const NF29={base:{model:bf22Model,init:warhiveInit,bay:s6r18Bay,launch:whvLaunchJet,tick:whvAceTick,draw:whvDrawAce,body:nw28DrawBody,alpha:nw28AlphaAt,invuln:whvAceInvuln,damage:warhiveDamage,death:whvAceDeathTick,load:stageLoadBegin},events:[],last:null,alpha:new Map()};
const NF29_ESCORT={id:'royal_harrier_escort',M:{...BF22_ART.models.sky_stratus,id:'royal_harrier_escort',banks:NF29_ART.escorts}};
for(const a of [...Object.values(NF29_ART.banks),...Object.values(NF29_ART.escorts)])XART._src[a.key]=a.path;
function nf29Cap(){return diffKey==='furious'?5:diffKey==='hard'?2:0;}
function nf29Carrier(b){return run.stage===6&&!run._gp4StageX&&!b?._gp4Host&&!!b?._whv;}
bf22Model=function(e){return run.stage===6&&e?._whvEscort?NF29_ESCORT:NF29.base.model.apply(this,arguments);};
warhiveInit=function(b){const r=NF29.base.init.apply(this,arguments);if(nf29Carrier(b))b._whv.jetN=nf29Cap();return r;};
s6r18Bay=function(b,dt){if(!nf29Carrier(b))return NF29.base.bay.apply(this,arguments);b._whv.jetN=nf29Cap();
 if(!b._whv.jetN){const D=s6r18State(b).bay;D.mode='wait';D.open=D.t=D.launched=0;b._carrier17.bayOpen=false;return;}
 return NF29.base.bay.apply(this,arguments);};
whvLaunchJet=function(b){if(nf29Carrier(b)){b._whv.jetN=nf29Cap();if(!b._whv.jetN||whvJetsAlive(b._whv)>=b._whv.jetN)return;}return NF29.base.launch.apply(this,arguments);};
stageLoadBegin=function(n,keys){return NF29.base.load.call(this,n,n===6?[...(keys||[]),...Object.values(NF29_ART.banks).map(a=>a.key),...Object.values(NF29_ART.escorts).map(a=>a.key)]:keys);};
function nf29Log(b,event,data={}){NF29.events.push({event,time:efxClock,x:b._whv.ace.x,y:b._whv.ace.y,...data});if(NF29.events.length>300)NF29.events.shift();}
function nf29Art(name){return globalThis.BOF_NIGHTWING_WIND_1028&&nw30Palette()?NW30_ART.banks[name]:NF29_ART.banks[name];}
function nf29Heading(angle,bank=0){const n=nf29Art('heading').directions||32;return{bank:'heading',frame:(bank<0?n:bank>0?n*2:0)+((Math.round((angle-Math.PI/2)/TAU*n)%n+n)%n),scale:1,heading:angle};}
function nf29Pose(A,bank,t,dur,scale=1){const a=nf29Art(bank);A._nf29Pose={bank,frame:Math.min(a.frames-1,Math.floor(clamp(t/dur,0,.9999)*a.frames)),scale};}
function nf29Sync(b){const A=b._whv.ace;b.x=A.x;b.y=A.y;b._drawY=A.y;const s=A._nf29Pose?.scale||1;b.w=184*s;b.h=192*s;delete A.fl;delete A._hitMod;}
function nf29Curve(P,u){const v=1-u,x=v*v*v*P[0].x+3*v*v*u*P[1].x+3*v*u*u*P[2].x+u*u*u*P[3].x,y=v*v*v*P[0].y+3*v*v*u*P[1].y+3*v*u*u*P[2].y+u*u*u*P[3].y,dx=3*v*v*(P[1].x-P[0].x)+6*v*u*(P[2].x-P[1].x)+3*u*u*(P[3].x-P[2].x),dy=3*v*v*(P[1].y-P[0].y)+6*v*u*(P[2].y-P[1].y)+3*u*u*(P[3].y-P[2].y);return{x,y,angle:Math.atan2(dy,dx)};}
function nf29Entry(b,dt){const A=b._whv.ace,M=A._nw28,mid=camLeftX()+viewW()/2,top=viewTopY(),home=clamp((WHV_ZONE.y0+WHV_ZONE.y1)/2,top+110,VH*.45);M.t+=dt;A.t+=dt;A.st='emerge';b._noHit=true;
 const north=M.mode==='north',dur=north?1.7:1.35,u=clamp(M.t/dur,0,1),side=M.corner<mid?-1:1;
 const P=north?[{x:M.corner,y:VH+160},{x:M.corner,y:VH*.62},{x:mid,y:top+80},{x:mid,y:top-160}]:[{x:mid,y:top-160},{x:mid+side*115,y:top-70},{x:mid,y:home-85},{x:mid,y:home}];
 const p=nf29Curve(P,u);A.x=p.x;A.y=p.y;A._nf29Pose=nf29Heading(p.angle,u>.08&&u<.9?-side:0);nf29Sync(b);
 if(u>=1){delete A._nf29Pose;nw28Mode(b,north?'north_wait':'settle');nf29Log(b,'curved-entry-'+(north?'north':'return'));}
}
function nf29Begin(b){const A=b._whv.ace,D=A.dash;D._nf29=true;D.st='warn';D.t=0;D.ang=Math.atan2(player.y-A.y,player.x-A.x);D.laneX=clamp(player.x,camLeftX()+120,camRightX()-120);D.side=D.laneX<camLeftX()+viewW()/2?1:-1;
 A._pw5Gun=A._ra7Gate=A.roll=A.somer=null;A.burst=0;A._pw5Missiles=0;
 // Pending locks belong to this launcher. Existing released rounds keep flying.
 if(typeof playerLocks!=='undefined'&&Array.isArray(playerLocks))for(const L of playerLocks)if(L.src===b)L.launches=L.launches.filter(q=>q.done);
 nf29Log(b,'charge-warn',{second:!!D.second});
}
function nf29Mode(b,phase){const A=b._whv.ace,D=A.dash;D.st=phase;D.t=0;D.from={x:A.x,y:A.y};nf29Log(b,'charge-'+phase,{second:!!D.second});}
function nf29Charge(b,dt){const A=b._whv.ace,D=A.dash;D.t+=dt;A.t+=dt;A.st='fight';A.vx=A.vy=0;A._pw5Gun=A._ra7Gate=null;A.burst=0;
 const home=clamp((WHV_ZONE.y0+WHV_ZONE.y1)/2,viewTopY()+120,VH*.42);
 if(D.st==='warn'){
  D.ex=A.x+Math.cos(D.ang)*1100;D.ey=A.y+Math.sin(D.ang)*1100;combatWarningTick(b,'nf29dash',D.t,.95);A._nf29Pose=nf29Heading(D.ang);
  if(D.t>=.95){nf29Mode(b,'go');combatAudio0927(b,'jetDash',.65);}
 }else if(D.st==='go'){
  A.x=D.from.x+Math.cos(D.ang)*D.t*670;A.y=D.from.y+Math.sin(D.ang)*D.t*670;A._nf29Pose=nf29Heading(D.ang);shake=Math.max(shake,1.6);
  if(A.x<camLeftX()-180||A.x>camRightX()+180||A.y>VH+180||A.y<viewTopY()-180||D.t>1.8)nf29Mode(b,'offscreen');
 }else if(D.st==='offscreen'){
  if(D.t>=.2){A.x=D.laneX;A.y=VH+245;nf29Mode(b,'flyover_warn');}
 }else if(D.st==='flyover_warn'){
  combatWarningTick(b,'nf29flyover',D.t,.85);if(D.t>=.85){nf29Mode(b,'flyover');combatAudio0927(b,'jetDash',.8);}
 }else if(D.st==='flyover'){
  const u=clamp(D.t/1.15,0,1);A.x=D.laneX;A.y=lerp(VH+245,home,u);nf29Pose(A,'flyover',D.t%(.08*8),.08*8,1.6);
  if(u>=1)nf29Mode(b,'drift');
 }else if(D.st==='drift'){
  const u=clamp(D.t/.95,0,1);A.x=D.laneX+D.side*70*(1-Math.cos(Math.PI*u));A.y=home-70*Math.sin(Math.PI*u);nf29Pose(A,D.side>0?'drift_right':'drift_left',D.t,.95,1.6-.95*(u*u*(3-2*u)));
  if(u>=1)nf29Mode(b,'approach');
 }else if(D.st==='approach'){
  const u=clamp(D.t/.72,0,1),e=u*u*(3-2*u);A.x=lerp(D.from.x,camLeftX()+viewW()/2,e);A.y=home+e*30;nf29Pose(A,'approach',D.t,.72,.65+.35*Math.pow(u,.65));
  if(u>=1){const again=b._whv.fur&&b.hp<=b.maxhp*.5&&!D.second;A.dash=again?{st:'warn',t:0,x0:A.x,y0:A.y,second:true}:null;delete A._nf29Pose;b._noHit=false;b.w=184;b.h=192;A.gunCd=Math.max(A.gunCd,1.15);A.mslCd=Math.max(A.mslCd,1.5);A._ra7Cd=Math.max(A._ra7Cd,2);A.vx=A.vy=0;nf29Log(b,'charge-complete',{second:!!D.second});if(again)nf29Begin(b);}
 }
 if(A.dash){b._noHit=['offscreen','flyover_warn'].includes(D.st)||(A._nf29Pose?.scale||1)<.95;nf29Sync(b);}
}
whvAceTick=function(b,dt){if(!nw28Own(b)||b.dead)return NF29.base.tick.apply(this,arguments);const A=b._whv.ace;dt=Math.min(.05,dt);
 if(nw28Intro(A)&&['north','return'].includes(A._nw28.mode))return nf29Entry(b,dt);
 if(A.dash&&!nw28Intro(A)&&(!A.desp||A.desp.st==='done')){if(!A.dash._nf29)nf29Begin(b);return nf29Charge(b,dt);}
 delete A._nf29Pose;b.w=184;b.h=192;return NF29.base.tick.apply(this,arguments);
};
function nf29Hidden(A){return !!A?.dash?._nf29&&(['offscreen','flyover_warn'].includes(A.dash.st)||(A._nf29Pose?.scale||1)<.95);}
whvAceInvuln=function(A){return nf29Hidden(A)||NF29.base.invuln.apply(this,arguments);};
warhiveDamage=function(b,dmg){if(nw28Own(b)&&nf29Hidden(b._whv.ace))return 0;return NF29.base.damage.apply(this,arguments);};
function nf29Cell(b){const A=b._whv.ace,p=A._nf29Pose;if(!p)return null;const a=nf29Art(p.bank+(b.flash>0&&!b.dead?'_hit':''));return{a,frame:p.frame,pose:p};}
nw28DrawBody=function(b){if(!nw28Own(b))return NF29.base.body.apply(this,arguments);const A=b._whv.ace;if(nf29Hidden(A)&&['offscreen','flyover_warn'].includes(A.dash.st))return;
 const p=nf29Cell(b);if(!p)return NF29.base.body.apply(this,arguments);const{a,frame:f}=p;if(!XART.rdy(a.key))return;
 const s=nf29Art(p.pose.bank+'_shadow');if(s&&XART.rdy(s.key))ctx.drawImage(XART.get(s.key),f%s.cols*s.cw,Math.floor(f/s.cols)*s.ch,s.cw,s.ch,Math.round(A.x)+18-s.pivot[0],Math.round(A.y)+75-s.pivot[1],s.cw,s.ch);
 ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(A.x)-a.pivot[0],Math.round(A.y)-a.pivot[1],a.cw,a.ch);NF29.last={bank:p.pose.bank,frame:f,key:a.key,x:A.x,y:A.y,scale:p.pose.scale,whole:true};NW28.draws++;
};
nw28AlphaAt=function(b,x,y){const p=nf29Cell(b);if(!p)return NF29.base.alpha.apply(this,arguments);const A=b._whv.ace,a=nf29Art(p.pose.bank),f=p.frame,px=Math.floor(x-Math.round(A.x)+a.pivot[0]),py=Math.floor(y-Math.round(A.y)+a.pivot[1]);if(px<0||py<0||px>=a.cw||py>=a.ch||!XART.rdy(a.key))return false;
 const key=a.key+'|'+f;let mask=NF29.alpha.get(key);if(!mask){const c=document.createElement('canvas');c.width=a.cw;c.height=a.ch;const g=c.getContext('2d');g.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,0,0,a.cw,a.ch);const d=g.getImageData(0,0,a.cw,a.ch).data;mask=Uint8Array.from({length:a.cw*a.ch},(_,i)=>d[i*4+3]);NF29.alpha.set(key,mask);}return mask[py*a.cw+px]>48;
};
whvDrawAce=function(b){if(nw28Own(b)&&!b.dead){const A=b._whv.ace,D=A.dash;if(D?._nf29&&D.st==='flyover_warn')combatWarningDraw(b,{x:D.laneX,y:VH,ex:D.laneX,ey:viewTopY()-60,progress:D.t/.85,width:210,fieldOnly:true});}return NF29.base.draw.apply(this,arguments);};
whvAceDeathTick=function(b,dt){const A=b._whv.ace;if(nw28Own(b)&&!A._nf29DeathChecked){A._nf29DeathChecked=true;A._nf29LargeDeath=(A._nf29Pose?.scale||1)>1.25;delete A._nf29Pose;}
 const r=NF29.base.death.apply(this,arguments);if(nw28Own(b)&&A._nf29LargeDeath&&!A.crash)A._nf29Pose={bank:'death_large',frame:((Math.round((A.spin||0)/TAU*32)%32)+32)%32,scale:1.6};return r;};
globalThis.BOF_NIGHTWING_FLIGHT_1027=NF29;
