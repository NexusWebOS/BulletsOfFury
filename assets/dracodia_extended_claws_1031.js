'use strict';
/* RD88: articulated edge-to-centre rakes, coiled depth jump and twin claw strikes.
   Same original anatomy/health owners; all rotations/depth/warnings baked offline. */
const RD88={base:{start:rd77Start,tick:r30Tick,draw:r30DrawBoss,rig:v18Rig,clear:v18Clear,contact:target17BossContact,warnings:v18Warnings,rupture:v18Rupture,donor:v19Rupture,keys:v18Keys,warm:v18Warm,load:stageLoadBegin},serial:0,events:[],draws:{},cues:['slice','hammerImpact','bossWeaponCharge','jetDash']};
for(const [key,a]of Object.entries(RD88_ART.pages)){XART._src[key]=a.path;XART._src[a.hitKey]=a.hitPath;}
for(const rows of Object.values(RD88_ART.warnings))for(const a of rows)XART._src[a.key]=a.path;
function rd88Keys(){return [...Object.entries(RD88_ART.pages).flatMap(([key,a])=>[key,a.hitKey]),...Object.values(RD88_ART.warnings).flatMap(rows=>rows.map(a=>a.key))];}
v18Keys=function(){return [...RD88.base.keys(),...rd88Keys()];};
v18Warm=function(){const prior=RD88.base.warm();return rd88Keys().map(k=>XART.rdy(k)).every(Boolean)&&prior;};
stageLoadBegin=function(n,keys){if(n===8)Snd.prepare(RD88.cues);return RD88.base.load.call(this,n,n===8?[...(keys||[]),...rd88Keys()]:keys);};
function rd88Act(b){return rd77Own(b)&&b._r30.v18.attack?._rd88?b._r30.v18.attack:null;}
function rd88Log(b,event,data={}){RD88.events.push({event,clock:b._r30.clock,...data});if(RD88.events.length>500)RD88.events.shift();}
function rd88Bank(side,jump=false){return (jump?'jump':'side')+(side==='left'?'L':'R');}
function rd88End(bank,side){const rows=RD88_ART.banks[bank],q=rows[bank.startsWith('jump')?27:31];return q.joints[side].tip.map((v,i)=>v-RD88_ART.pivot[i]);}
function rd88Anchor(mark,bank,side){const p=rd88End(bank,side);return{x:mark.x-p[0],y:mark.y-p[1]};}
rd77Start=function(b){const N=b._r30.v18,seq=N.rd77Seq||0,rank=target17Rank(),alive=rd77Arms(b),order=seq%2?['right','left']:['left','right'];
 if(!alive.length)return RD88.base.start.apply(this,arguments);if(alive.length===1)order.fill(alive[0].id);
 const target=targetShip(b.x,b.y),centre=(camLeftX()+camRightX())/2,sideHome={x:clamp(target.x,centre-38,centre+38),y:clamp(target.y-135,viewTopY()+205,VH-202)};
 const marks=order.map((side,i)=>({x:clamp(target.x+(i? (side==='left'?-68:68):0),camLeftX()+54,camRightX()-54),y:clamp(target.y-(i?24:0),viewTopY()+285,VH-55)}));
 v18Clear(b);N.rd77Seq=seq+1;N.seq++;
 const P=N.attack={_rd88:true,type:'rd88-extended-claws',serial:++RD88.serial,t:0,local:0,rank,order,marks,origin:{x:b.x,y:b.y},sideHome,home:{x:worldWidth()/2,y:viewTopY()+viewH()*.34},back:{x:centre+(seq%2?46:-46),y:viewTopY()+65},bank:'coil',frame:0,depth:1,index:0,stage:'prime',contacts:new Set(),impacts:new Set(),warned:new Set(),warning:null,previous:null};
 b._r30.attack=P;N.swipe=N.acting=null;N.archiveDepth=1;N.archiveEnergy=0;
 const tell=rank>=3?.95:rank>=2?1.05:1.15;P.steps=[{kind:'prime',duration:.5},{kind:'side-tell',duration:tell,index:0},{kind:'side-rake',duration:.3,index:0},{kind:'side-retract',duration:.32,index:0},{kind:'side-tell',duration:tell,index:1},{kind:'side-rake',duration:.3,index:1},{kind:'side-retract',duration:.32,index:1},{kind:'recede',duration:.65},{kind:'background',duration:.3},{kind:'leap',duration:.25},{kind:'approach',duration:.38},{kind:'jump-tell',duration:.55,index:0},{kind:'jump-strike',duration:.28,index:0},{kind:'jump-retract',duration:.16,index:0},{kind:'jump-tell',duration:rank>=3?.62:.72,index:1},{kind:'jump-strike',duration:.28,index:1},{kind:'jump-retract',duration:.16,index:1},{kind:'recover',duration:.85}];P.step=0;
 Snd.play('bossWeaponCharge',.8);rd88Log(b,'combo-start',{rank,order,marks:marks.map(q=>({...q})),sideHome:{...sideHome},hp:b.hp});return P;
};
function rd88Pose(P,bank,f){P.bank=bank;P.frame=clamp(Math.floor(f),0,RD88_ART.banks[bank].length-1);P.depth=RD88_ART.banks[bank][P.frame].depth;}
function rd88At(b,P,point){b.x=point.x;b.y=point.y;}
function rd88Warn(b,P,kind,index,age,duration,anchor,bank){const side=P.order[index];if(!rd77Side(b,side))return;const key=kind+'-'+index;
 if(!P.warned.has(key)){P.warned.add(key);rd88Log(b,'warning-committed',{kind,index,side,duration,anchor:{...anchor},mark:{...P.marks[index]}});}
 P.warning={kind,index,side,bank,anchor,progress:clamp(age/duration,0,1)};combatWarningTick(b,'rd88-'+P.serial+'-'+key,Math.min(age,duration),duration);
}
function rd88ClawContains(row,x,y){const xx=Math.floor(x-row.offset[0]),yy=Math.floor(y-row.offset[1]),sp=row.spans[yy];if(!sp)return false;for(let i=0;i<sp.length;i+=2)if(xx>=sp[i]&&xx<sp[i+1])return true;return false;}
function rd88Touch(b,P,side){if(P.depth<.85||b._noHit||!rd77Side(b,side))return;const prior=P.previous,rows=RD88_ART.banks[P.bank],from=prior?.bank===P.bank?prior.frame:P.frame,to=P.frame,steps=Math.max(1,Math.abs(to-from));
 for(const seat of seatList())withSeat(seat,()=>{const key=P.step+'-'+seat;if(player.dead||player.out||P.contacts.has(key))return;
  for(let i=0;i<=steps;i++){const f=Math.round(lerp(from,to,i/steps)),r=rows[f].claws[side],x=prior?.bank===P.bank?lerp(prior.x,b.x,i/steps):b.x,y=prior?.bank===P.bank?lerp(prior.y,b.y,i/steps):b.y;
   if([[0,0],[-4,0],[4,0],[0,-4],[0,4]].some(([dx,dy])=>rd88ClawContains(r,player.x+dx-x,player.y+dy-y))){P.contacts.add(key);playerHit('Dracodia extended '+side+' claw');rd88Log(b,'claw-contact',{seat,side,stage:P.stage});break;}
  }
 });
}
function rd88Impact(b,P,index){if(P.impacts.has(index)||!rd77Side(b,P.order[index]))return;P.impacts.add(index);const m=P.marks[index];explode(m.x,m.y,34,'purple');Snd.play('hammerImpact',.6);shake=Math.max(shake,2);rd88Log(b,'claw-ground-contact',{index,side:P.order[index],mark:{...m}});}
function rd88Finish(b,P){const N=b._r30.v18;N.attack=N.acting=null;N.archiveDepth=1;N.archiveEnergy=0;N.home={x:b.x,y:b.y};b._r30.attack=null;b._r30.cd=P.rank>=3?.85:1.1;b._noHit=false;j3State(b).attacks++;rd88Log(b,'combo-complete',{hp:b.hp});}
function rd88Tick(b,P,dt){P.t+=dt;P.local+=dt;P.warning=null;const N=b._r30.v18;if(!rd77Arms(b).length)return rd88Finish(b,P);
 while(P.step<P.steps.length&&P.local>=P.steps[P.step].duration){P.local-=P.steps[P.step].duration;P.step++;P.previous=null;}
 if(P.step>=P.steps.length)return rd88Finish(b,P);
 const S=P.steps[P.step],u=clamp(P.local/S.duration,0,1),e=v19Ease(u),side=P.order[S.index||0],bank=rd88Bank(side,S.kind.startsWith('jump')),anchor=rd88Anchor(P.marks[S.index||0],rd88Bank(side,true),side),firstAnchor=rd88Anchor(P.marks[0],rd88Bank(P.order[0],true),P.order[0]);
 if(P.stage!==S.kind||P.index!==S.index){P.stage=S.kind;P.index=S.index;rd88Log(b,'motion',{stage:S.kind,index:S.index,side,step:P.step});if(S.kind==='side-rake'||S.kind==='jump-strike')Snd.play('slice',.95);if(S.kind==='leap')Snd.play('jetDash',.65);}
 b._noHit=false;
 if(S.kind==='prime'){rd88Pose(P,'coil',e*19);b.x=lerp(P.origin.x,P.sideHome.x,e);b.y=lerp(P.origin.y,P.sideHome.y,e);}
 else if(S.kind==='side-tell'){rd88Pose(P,bank,e*15);rd88At(b,P,P.sideHome);rd88Warn(b,P,'rake',S.index,P.local,S.duration,P.sideHome,bank);}
 else if(S.kind==='side-rake'){rd88Pose(P,bank,16+u*15);rd88At(b,P,P.sideHome);rd88Touch(b,P,side);}
 else if(S.kind==='side-retract'){rd88Pose(P,bank,32+u*11);rd88At(b,P,P.sideHome);}
 else if(S.kind==='recede'){rd88Pose(P,'recede',e*19);b.x=lerp(P.sideHome.x,P.back.x,e);b.y=lerp(P.sideHome.y,P.back.y,e);rd88Warn(b,P,'landing',0,P.local,1.58,firstAnchor,rd88Bank(P.order[0],true));}
 else if(S.kind==='background'){rd88Pose(P,'recede',19);b.x=P.back.x+Math.sin(P.local*3)*3;b.y=P.back.y+Math.sin(P.local*4)*2;rd88Warn(b,P,'landing',0,.65+P.local,1.58,firstAnchor,rd88Bank(P.order[0],true));}
 else if(S.kind==='leap'){rd88Pose(P,'recede',19);b.x=lerp(P.back.x,firstAnchor.x,e);b.y=lerp(P.back.y,viewTopY()-150,e);b._noHit=true;rd88Warn(b,P,'landing',0,.95+P.local,1.58,firstAnchor,rd88Bank(P.order[0],true));}
 else if(S.kind==='approach'){rd88Pose(P,'approach',e*19);b.x=firstAnchor.x;b.y=lerp(viewTopY()-150,firstAnchor.y,e);rd88Warn(b,P,'landing',0,1.2+P.local,1.58,firstAnchor,rd88Bank(P.order[0],true));}
 else if(S.kind==='jump-tell'){rd88Pose(P,bank,e*11);const from=S.index?firstAnchor:anchor;b.x=lerp(from.x,anchor.x,e);b.y=lerp(from.y,anchor.y,e)-Math.sin(u*Math.PI)*(S.index?32:0);rd88Warn(b,P,'jump',S.index,P.local,S.duration,anchor,bank);}
 else if(S.kind==='jump-strike'){rd88Pose(P,bank,12+u*15);rd88At(b,P,anchor);rd88Touch(b,P,side);if(u>.84)rd88Impact(b,P,S.index);}
 else if(S.kind==='jump-retract'){rd88Pose(P,bank,28+u*7);rd88At(b,P,anchor);}
 else {rd88Pose(P,'settle',e*15);const lastSide=P.order[1],last=rd88Anchor(P.marks[1],rd88Bank(lastSide,true),lastSide);b.x=lerp(last.x,P.home.x,e);b.y=lerp(last.y,P.home.y,e);}
 b._noHit=b._noHit||P.depth<.85;b.enter=false;N.archiveDepth=P.depth;N.archiveEnergy=0;N.home={x:b.x,y:b.y};P.previous={bank:P.bank,frame:P.frame,x:b.x,y:b.y};
}
r30Tick=function(b,dt){const P=rd88Act(b);if(!P)return RD88.base.tick.apply(this,arguments);dt=clamp(dt||0,0,.05);j3Timers(b,dt);dr5TalkTick(b,dt);const N=b._r30.v18,Q=v17Clock(b);N.age+=dt;N.formClock+=dt;Q.t+=dt;Q.combat+=dt;Q.transition+=dt;rd88Tick(b,P,dt);};
function rd88Frame(b){const P=rd88Act(b);return P?RD88_ART.banks[P.bank][P.frame]:null;}
v18Rig=function(b){const q=rd88Frame(b);if(!q)return RD88.base.rig.apply(this,arguments);const N=b._r30.v18,P=rd88Act(b),mask=b.parts.map(p=>p.destroyed?'0':'1').join(''),old=N.rd88Rig;
 if(old&&old.pose===q&&old.x===b.x&&old.y===b.y&&old.mask===mask&&old.parts===b.parts)return old.rig;
 const rig=b.parts.filter(p=>!p.destroyed).map(p=>{const a=q.parts[p.id];return{_rd77:true,_rd88:true,p,a,key:a.key,ax:b.x,ay:b.y,x:b.x+a.target[0],y:b.y+a.target[1],w:a.w,h:a.h,k:1,rot:0,alpha:1,anchor:[-a.offset[0],-a.offset[1]],spec:{role:p.id==='core'?'core':'weapon'},z:p.id==='core'?1:0};});N.rd88Rig={pose:q,x:b.x,y:b.y,mask,parts:b.parts,rig};return rig;
};
function rd88Blit(a,b,hit=false){const key=hit?RD88_ART.pages[a.key].hitKey:a.key;if(!XART.rdy(key))return;ctx.drawImage(XART.get(key),...a.rect,Math.round(b.x+a.offset[0]),Math.round(b.y+a.offset[1]),a.w,a.h);RD88.draws[a.key]=(RD88.draws[a.key]||0)+1;}
function rd88Warning(b,P,front=false){const W=P.warning;if(!W||!rd77Side(b,W.side))return;
 if(!front&&W.kind!=='landing'){const colour=W.progress<.45?0:W.progress<.78?1:2,a=RD88_ART.warnings[W.bank][colour];if(XART.rdy(a.key)){ctx.drawImage(XART.get(a.key),Math.round(W.anchor.x-a.pivot[0]),Math.round(W.anchor.y-a.pivot[1]));RD88.draws.warning=(RD88.draws.warning||0)+1;}}
 if(front&&(W.kind==='landing'||W.kind==='jump')){const a=HL51_ART,q=P.marks[W.index],colour=W.progress<.5?0:W.progress<.8?1:2,f=colour*8+Math.min(7,Math.floor(W.progress*24));if(XART.rdy(a.key))ctx.drawImage(XART.get(a.key),f%8*64,Math.floor(f/8)*32,64,32,Math.round(q.x)-32,Math.round(q.y)-16,64,32);}
 if(front)combatWarningDraw(b,{x:b.x,y:b.y,progress:W.progress,alertOnly:true,alertX:b.x,alertY:Math.max(viewTopY()+28,b.y-155)});
}
r30DrawBoss=function(b){const P=rd88Act(b);if(!P)return RD88.base.draw.apply(this,arguments);rd88Warning(b,P);const q=rd88Frame(b);for(const id of ['left','core','right']){const part=b.parts.find(p=>p.id===id);if(part&&!part.destroyed)rd88Blit(q.parts[id],b,Math.max(b.flash||0,part.flash||0)>.025&&Math.floor(efxClock*36)%2===0);}rd88Warning(b,P,true);};
target17BossContact=function(b){if(rd88Act(b))return false;return RD88.base.contact.apply(this,arguments);};
v18Warnings=function(b){if(rd88Act(b))return;return RD88.base.warnings.apply(this,arguments);};
function rd88Break(b,p,base,args){const P=rd88Act(b);if(!P||p.id==='core')return base.apply(null,args);if(p._rd88Broken)return;p._rd88Broken=p._rd77Broken=p._rd30Shattered=true;const a=rd88Frame(b).parts[p.id];for(const q of a.rupture)explode(b.x+q[0],b.y+q[1],34,'purple');Snd.play('combatModule0927',.8);if(P.warning?.side===p.id)P.warning=null;rd88Log(b,'whole-claw-break',{part:p.id});}
v18Rupture=function(b,p){return rd88Break(b,p,RD88.base.rupture,arguments);};
v19Rupture=function(b,p){return rd88Break(b,p,RD88.base.donor,arguments);};
v18Clear=function(b){const P=b?._r30?.v18?.attack;if(P?._rd88){P.warning=null;P.contacts.clear();b._r30.v18.rd88Rig=null;rd88Log(b,'combo-cancel');}return RD88.base.clear.apply(this,arguments);};
globalThis.BOF_DRACODIA_EXTENDED_CLAWS=RD88;
