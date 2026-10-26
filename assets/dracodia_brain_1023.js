'use strict';
/* Dracodia's Neural Archon replaces slot6 only. Whole authored actor, frame-measured
   eye sockets, expanding pre-rendered lasers, committed geysers and finite
   cloud shield. Campaign Harrier and every other Dracodia form are untouched. */
const NB23={base:{enter:v18Enter,native:v19Native,model:v18Model,frame:v18Frame,rig:v18Rig,body:v19Body,draw:r30DrawBoss,tick:r30Tick,at:r30At,targets:retinaBossTargets,hit:modularHit,clear:v18Clear,break:r30Break,rupture:v18Rupture,load:stageLoadBegin,keys:v18Keys,warm:v18Warm,attack:v18StartAttack,attackTick:v18AttackTick,shield:bossShieldFrac,contact:target17BossContact,download:dr21Download},events:[],draws:{},masks:new Map(),tags:new WeakMap()};
for(const s of Object.values(NB23_ART.sheets))XART._src[s.key]=s.path;
for(const rows of Object.values(NB23_ART.banks))for(const a of rows)BOFX.cells[a.key]=[a.sheet,...a.cell];
V18.names[6]='brain';Object.assign(F1003B_FORMS[6],{id:'brain',name:'DRACODIA â€” NEURAL ARCHON',color:'#cf78ff',book:['eyeExpansion','codeGeysers','cloudAegis']});
function nb23Own(b){return v18Owned(b)&&j3State(b).encounter===2&&b._r30.v18.form===6;}
function nb23Log(type,data={}){NB23.events.push({type,...data});if(NB23.events.length>300)NB23.events.shift();}
function nb23Keys(){return Object.values(NB23_ART.sheets).map(s=>s.key);}
function nb23Warm(){return nb23Keys().map(k=>XART.rdy(k)).every(Boolean);}
v18Keys=function(){return [...NB23.base.keys(),...nb23Keys()];};
v18Warm=function(){const prior=NB23.base.warm();return nb23Warm()&&prior;};
stageLoadBegin=function(n,keys){if(n===8)Snd.prepare(['bossWeaponCharge','combatBeam0927','expBig','shieldHitHeavy','shieldBreakCombat','teleportIn']);return NB23.base.load.call(this,n,[...(keys||[]),...(n===8?nb23Keys():[])]);};
v19Native=function(b){return nb23Own(b)?false:NB23.base.native.apply(this,arguments);};
v18Enter=function(b,n,form=0){const saved=n===2&&form===6?j3State(b).modules[6]?.filter(p=>p._nb23):null;
 const out=NB23.base.enter.apply(this,arguments);if(!nb23Own(b))return out;
 b.parts=saved?.length?saved:[{id:'core',hp:b.hp,maxhp:b.maxhp,destroyed:false,flash:0,kick:0,dmg:true,_nb23:true,spec:{role:'core'}}];
 b.parts[0].hp=b.hp;b.parts[0].destroyed=b.hp<=0;j3State(b).modules[6]=b.parts;
 const N=b._r30.v18;N.brainAge=0;N.brainShield=null;N.attack=null;N.beams=[];N.hazards=[];N.seq=0;N.swipe=null;N.acting=null;N.home={x:b.x,y:viewTopY()+220};b.y=N.home.y;b.ty=b.y;b.w=240;b.h=222;b._r30.finale1003b=b._r30.modular1003c=false;
 b.name='DRACODIA â€” NEURAL ARCHON';nb23Log('identity',{form:6,hp:b.hp,max:b.maxhp});return out;
};
v18Model=function(b){return nb23Own(b)?'brain':NB23.base.model.apply(this,arguments);};
function nb23Cell(bank,f=0){const rows=NB23_ART.banks[bank];return rows[Math.max(0,Math.min(rows.length-1,f|0))];}
function nb23Actor(b){const N=b._r30.v18,P=N.attack;
 if(P?._nb23&&P.type==='eyeExpansion'){
  if(P.t<P.tell){const bank=NB23_ART.banks.charge;return bank[Math.min(bank.length-1,Math.floor(P.t/P.tell*bank.length))];}
  if(P.t<P.tell+P.active){const bank=NB23_ART.banks.focus;return bank[Math.floor((P.t-P.tell)*10)%bank.length];}
  // Retract through the same whole charge poses, rather than popping off a glow.
  const bank=NB23_ART.banks.charge,u=clamp((P.t-P.tell-P.active)/Math.min(.55,P.recover),0,1);return bank[Math.floor((1-u)*(bank.length-1))];
 }
 return nb23Cell('brain',Math.floor((N.brainAge||0)*10)%NB23_ART.banks.brain.length);
}
function nb23BeamFrame(P){return Math.floor(Math.max(0,P.t-P.tell)*24)%NB23_ART.banks.beam_0.length;}
v18Frame=function(b){return nb23Own(b)?{core:nb23Actor(b)}:NB23.base.frame.apply(this,arguments);};
function nb23Blit(a,x,y,white=false){if(!a)return false;const key=white&&a.white?a.white:a.key;if(!XART.rdy(key))return false;const im=XART.get(key);NB23.tags.set(im,key);ctx.drawImage(im,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]));NB23.draws[key]=(NB23.draws[key]||0)+1;return true;}
function nb23Body(b){return nb23Blit(nb23Actor(b),b.x,b.y,Math.max(b.flash||0,b.parts[0]?.flash||0)>0);}
v19Body=function(b){return nb23Own(b)?nb23Body(b):NB23.base.body.apply(this,arguments);};v18Body=v19Body;
v18Rig=function(b){if(!nb23Own(b))return NB23.base.rig.apply(this,arguments);const a=nb23Actor(b),q=a.bounds;return b.parts.filter(p=>!p.destroyed).map(p=>({p,key:a.key,a,k:1,rot:0,alpha:1,x:b.x+(q[0]+q[2])/2-a.pivot[0],y:b.y+(q[1]+q[3])/2-a.pivot[1],ax:b.x,ay:b.y,bodyX:b.x,bodyY:b.y,w:q[2]-q[0],h:q[3]-q[1],anchor:a.pivot,spec:{role:'core'},layer:'brain'}));};
function nb23PixelAt(a,root,x,y){if(!XART.rdy(a.key))return false;let m=NB23.masks.get(a.key);if(!m){const c=document.createElement('canvas');c.width=a.w;c.height=a.h;const g=c.getContext('2d',{willReadFrequently:true});g.drawImage(XART.get(a.key),0,0);m=g.getImageData(0,0,a.w,a.h).data;NB23.masks.set(a.key,m);}const px=Math.floor(x-root.x+a.pivot[0]),py=Math.floor(y-root.y+a.pivot[1]);return px>=0&&py>=0&&px<a.w&&py<a.h&&m[(py*a.w+px)*4+3]>48;}
function nb23At(b,x,y){return nb23PixelAt(nb23Actor(b),b,x,y);}
r30At=function(b,x,y){if(!nb23Own(b))return NB23.base.at.apply(this,arguments);return r30Live(b)&&!b._noHit&&!b.parts[0].destroyed&&nb23At(b,x,y)?b.parts[0]:null;};
retinaBossTargets=function(b){if(!nb23Own(b))return NB23.base.targets.apply(this,arguments);const p=b.parts[0];if(!r30Live(b)||b._noHit||p.destroyed||p.hp<=0)return[];
 return[retinaDynamicPiece(b,'nb23-core','Neural Archon',()=>({x:b.x,y:b.y,hp:p.hp,dead:!nb23Own(b)||b._noHit||p.destroyed||p.hp<=0||!r30Live(b)}),d=>{if(!nb23Own(b)||b._noHit||p.destroyed)return;b._lastPart=p;hitBoss(d);},150,150)];};
function nb23Shield(b){const P=b?._r30?.v18?.attack;return nb23Own(b)&&b._r30.mode==='fight'&&P?._nb23&&P.type==='cloudAegis'&&P.t>=P.tell+.25&&P.t<P.tell+P.active&&P.shield>0?P:null;}
bossShieldFrac=function(b){const P=nb23Shield(b);return nb23Own(b)?P?P.shield/P.maxShield:0:NB23.base.shield.apply(this,arguments);};
modularHit=function(dmg){const b=boss;if(!nb23Own(b))return NB23.base.hit.apply(this,arguments);if(!r30Live(b)||b._noHit||!(dmg>0)||b.parts[0].destroyed)return;
 const P=nb23Shield(b),p=b.parts[0];markHit(b,.12);markHit(p,.12);
 if(P){P.shield=Math.max(0,P.shield-dmg);r30Sound(P.shield?'shieldHitHeavy':'shieldBreakCombat');nb23Log('shield-absorb',{remaining:P.shield});if(!P.shield)P.brokenAt=P.t;return;}
 const dealt=Math.min(dmg,b.hp);b.hp-=dealt;p.hp=b.hp;stageStats.dmgDealt+=dealt;j3Save(b);if(b.hp<=0){p.destroyed=true;r30Break(b);}
};
function nb23Eyes(b){const a=nb23Actor(b);return(a.eyes||NB23_ART.eyes).map(p=>({x:Math.round(b.x-a.pivot[0])+p[0],y:Math.round(b.y-a.pivot[1])+p[1]}));}
function nb23WarningEyes(b){return [0,1].map(i=>({x:Math.round(b.x)-NB23_ART.pivot[0]+Math.round(NB23_ART.banks.focus.reduce((n,a)=>n+a.eyes[i][0],0)/NB23_ART.banks.focus.length),y:Math.round(b.y)-NB23_ART.pivot[1]+Math.min(...NB23_ART.banks.focus.map(a=>a.eyes[i][1]))}));}
function nb23Start(b,type){const N=b._r30.v18,d=Math.min(2,v18Diff());type??=['eyeExpansion','codeGeysers','cloudAegis'][N.seq%3];N.seq++;
 const P=N.attack={_nb23:true,type,t:0,tell:diffKey==='easy'?1.4:[1.2,1.04,.9][d],active:type==='cloudAegis'?2.35:type==='eyeExpansion'?2.15:2.8,recover:[1.05,.9,.78][d],origin:{x:b.x,y:b.y},eyes:nb23Eyes(b),targets:[],shield:0,maxShield:Math.ceil(b.maxhp*.12),fired:false};
 if(type==='cloudAegis')P.shield=P.maxShield;
 if(type==='codeGeysers'){const count=d===0?3:d===1?4:5,spacing=Math.min(88,(viewW()-84)/(count-1)),half=(count-1)*spacing/2,x=clamp(player.x,camLeftX()+42+half,camRightX()-42-half),y=clamp(player.y+60,viewTopY()+220,VH-20);for(let i=0;i<count;i++)P.targets.push({x:x+(i-(count-1)/2)*spacing,y:y-(i%2)*62,at:i*[.40,.34,.29][d],released:false});}
 b._r30.attack=P;if(type==='eyeExpansion'){P.eyes=nb23Eyes(b);P.warningEyes=nb23WarningEyes(b);}combatWarningTick(b,'nb23-'+N.seq,0,P.tell,true);r30Sound('bossWeaponCharge');nb23Log('tell',{type,tell:P.tell});
}
v18StartAttack=function(b){return nb23Own(b)?nb23Start(b):NB23.base.attack.apply(this,arguments);};
function nb23Float(b){const N=b._r30.v18,t=N.brainAge,margin=125;b.x=clamp(N.home.x+Math.sin(t*.85)*Math.min(65,viewW()*.13),camLeftX()+margin,camRightX()-margin);b.y=N.home.y+Math.sin(t*1.36)*18;}
function nb23AttackTick(b,dt){const N=b._r30.v18,P=N.attack;if(!P)return;P.t+=dt;const u=P.t-P.tell;
 combatWarningTick(b,'nb23-'+N.seq,Math.min(P.t,P.tell),P.tell);
 if(P.type==='eyeExpansion'){b.x=P.origin.x;b.y=P.origin.y;P.eyes=nb23Eyes(b);if(u>=0&&!P.fired){P.fired=true;r30Sound('combatBeam0927');nb23Log('eye-release',{eyes:P.eyes});}
  if(u>=0&&u<P.active){P.widthStep=Math.min(5,Math.floor(u/.18));const half=NB23_ART.beamWidths[P.widthStep]/2;for(const eye of P.eyes)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&player.y>=eye.y&&player.y<=eye.y+NB23_ART.beamLength&&Math.abs(player.x-eye.x)<half+4){const a=nb23Cell('beam_'+P.widthStep,nb23BeamFrame(P));if([[0,0],[-4,0],[4,0],[0,-4],[0,4]].some(([x,y])=>nb23PixelAt(a,eye,player.x+x,player.y+y)))playerHit('Neural Archon eye laser');}});}
 }else{nb23Float(b);if(P.type==='codeGeysers')for(const q of P.targets){const age=u-q.at;if(age>=0&&!q.released){q.released=true;r30Sound('expBig');nb23Log('geyser-release',{x:q.x,y:q.y,age});}if(age>=.12&&age<.68)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.abs(player.x-q.x)<NB23_ART.geyserHalf&&player.y>q.y-NB23_ART.geyserHeight&&player.y<q.y+8){const a=nb23Cell('geyser',Math.floor(age/.85*NB23_ART.banks.geyser.length));if([[0,0],[-4,0],[4,0],[0,-4],[0,4]].some(([x,y])=>nb23PixelAt(a,q,player.x+x,player.y+y)))playerHit('Neural Archon code geyser');}});}}
 if(P.t>=P.tell+P.active+P.recover){N.attack=null;b._r30.attack=null;b._r30.cd=.65;j3State(b).attacks++;nb23Log('recovery-complete',{type:P.type});}
}
v18AttackTick=function(b,dt){return nb23Own(b)?nb23AttackTick(b,dt):NB23.base.attackTick.apply(this,arguments);};
r30Tick=function(b,dt){if(!nb23Own(b)||b._r30.mode!=='fight')return NB23.base.tick.apply(this,arguments);dt=clamp(dt||0,0,.05);const S=b._r30,N=S.v18,J=j3State(b);j3Timers(b,dt);N.age+=dt;N.brainAge+=dt;const Q=v17Clock(b);Q.t+=dt;Q.transition+=dt;Q.combat+=dt;dr5TalkTick(b,dt);b.enter=b._noHit=false;
 if(N.attack)nb23AttackTick(b,dt);else{nb23Float(b);S.cd-=dt;if(S.cd<=0){if(J.attacks>=3&&V18.forms.filter(i=>J.hp[i]>0).length>1){j3Save(b);return j3Morph(b,'home');}nb23Start(b);}}b._drawY=b.y;j3Save(b);
};
function nb23Warnings(b,P){if(P.type==='eyeExpansion'&&P.t<P.tell){const color=P.t/P.tell<.4?'green':P.t/P.tell<.74?'yellow':'red';for(const p of P.warningEyes||P.eyes)nb23Blit(nb23Cell('warn_laser_'+color),p.x,p.y);}
 if(P.type==='codeGeysers')for(const q of P.targets){const remain=P.tell+q.at-P.t;if(remain>0){const progress=clamp(1-remain/P.tell,0,1),color=progress<.4?'green':progress<.74?'yellow':'red';nb23Blit(nb23Cell('warn_geyser_'+color),q.x,q.y);}}
}
function nb23Draw(b){const N=b._r30.v18,P=N.attack;if(P)nb23Warnings(b,P);nb23Body(b);if(!P)return;const u=P.t-P.tell;
 if(P.type==='eyeExpansion'&&u>=0&&u<P.active){const f=nb23BeamFrame(P),step=P.widthStep||0;for(const e of nb23Eyes(b))nb23Blit(nb23Cell('beam_'+step,f),e.x,e.y);}
 if(P.type==='codeGeysers')for(const q of P.targets){const age=u-q.at;if(age>=0&&age<.85)nb23Blit(nb23Cell('geyser',Math.floor(age/.85*NB23_ART.banks.geyser.length)),q.x,q.y);}
 if(P.type==='cloudAegis'&&u>=0&&u<P.active){const bank=nb23Shield(b)?'cloud':'cloud_open',f=Math.floor(u*12)%NB23_ART.banks[bank].length;nb23Blit(nb23Cell(bank,f),b.x,b.y);}
}
dr21Download=function(b,t,duration,incoming){if(!nb23Own(b))return NB23.base.download.apply(this,arguments);const rows=NB23_ART.banks.morph,u=clamp(t/duration,0,.99999),i=Math.floor((incoming?u:1-u)*rows.length);nb23Blit(rows[Math.min(rows.length-1,i)],b.x,b.y);return true;};
r30DrawBoss=function(b){if(!nb23Own(b))return NB23.base.draw.apply(this,arguments);const S=b._r30;
 if(S.mode==='fight')return nb23Draw(b);
 if(S.mode==='v18formIn'||S.mode==='v18formOut')return dr21Download(b,S.t,S.mode==='v18formIn'?1.6:1.45,S.mode==='v18formIn');
 if(S.mode==='v19copyDeath'){const rows=NB23_ART.banks.morph;nb23Blit(rows[Math.max(0,rows.length-1-Math.floor(S.t/2.65*rows.length))],b.x,b.y);dr5EffectsDraw(b);return;}
 return nb23Body(b);
};
v18Rupture=function(b,p){if(!nb23Own(b))return NB23.base.rupture.apply(this,arguments);nb23Log('brain-rupture',{hp:b.hp});};
v18Clear=function(b){if(nb23Own(b)){const N=b._r30.v18;N.brainShield=null;N.attack=null;nb23Log('cancel');}return NB23.base.clear.apply(this,arguments);};
target17BossContact=function(b){return nb23Own(b)?false:NB23.base.contact.apply(this,arguments);};
globalThis.BOF_NEURAL_ARCHON=NB23;
