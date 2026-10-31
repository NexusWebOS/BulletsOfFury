'use strict';
/* NB80: aperture-filling eye optics. Actual current pose owns the lens pixels,
   warning origin, continuous shaft and damage. No purple generic muzzle. */
const NB80={base:{draw:r30DrawBoss,body:nb23Body,eyes:nb23Eyes,warningEyes:nb23WarningEyes,warnings:nb23Warnings,tick:nb23AttackTick,keys:v18Keys,warm:v18Warm,load:stageLoadBegin},events:[],draws:{}};
for(const [key,a]of Object.entries(NB80_ART.pages))XART._src[key]=a.path;
function nb80Keys(){return Object.keys(NB80_ART.pages);}
v18Keys=function(){return[...NB80.base.keys(),...nb80Keys()];};
v18Warm=function(){const prior=NB80.base.warm();return nb80Keys().map(k=>XART.rdy(k)).every(Boolean)&&prior;};
stageLoadBegin=function(n,keys){return NB80.base.load.call(this,n,n===8?[...(keys||[]),...nb80Keys()]:keys);};
function nb80Act(b){return nb23Own(b)&&!b.dead&&b._r30.mode==='fight'&&b._r30.v18.attack?.type==='eyeExpansion'?b._r30.v18.attack:null;}
function nb80Blit(name,f,x,y){const rows=NB80_ART.banks[name];if(!rows)return false;const a=rows[clamp(f|0,0,rows.length-1)];if(!XART.rdy(a.key))return false;ctx.drawImage(XART.get(a.key),...a.rect,Math.round(x+a.offset[0]),Math.round(y+a.offset[1]),a.w,a.h);NB80.draws[name]=(NB80.draws[name]||0)+1;return true;}
function nb80Lens(b){const P=nb80Act(b),a=nb23Actor(b);if(!P)return null;let bank,index;
 if(P.t<P.tell){bank='charge';index=Math.min(7,Math.floor(P.t/P.tell*8));}
 else if(P.t<P.tell+P.active){bank='focus';index=Math.floor((P.t-P.tell)*10)%4;}
 else{bank='charge';const u=clamp((P.t-P.tell-P.active)/Math.min(.55,P.recover),0,1);index=Math.floor((1-u)*7);}
 return{a,bank,index};
}
nb23Eyes=function(b){if(!nb80Act(b))return NB80.base.eyes.apply(this,arguments);const a=nb23Actor(b);return a.eyes.map(q=>({x:Math.round(b.x-a.pivot[0])+q[0],y:Math.round(b.y-a.pivot[1])+q[1]}));};
nb23WarningEyes=function(b){return nb80Act(b)?nb23Eyes(b):NB80.base.warningEyes.apply(this,arguments);};
function nb80Body(b){nb23Blit(nb23Actor(b),b.x,b.y,Math.max(b.flash||0,b.parts[0]?.flash||0)>0);}
nb23Body=function(b){return nb80Act(b)?nb80Body(b):NB80.base.body.apply(this,arguments);};
function nb80Inside(a,eye,x,y){const xx=Math.floor(x-eye.x-a.offset[0]),yy=Math.floor(y-eye.y-a.offset[1]),row=a.spans[yy];if(!row)return false;for(let i=0;i<row.length;i+=2)if(xx>=row[i]&&xx<row[i+1])return true;return false;}
function nb80Frame(P){return Math.floor(Math.max(0,P.t-P.tell)*24)%16;}
function nb80Beam(P){const u=Math.max(0,P.t-P.tell),level=P.widthStep??Math.min(5,Math.floor(u/.08)),launch=u<.16,name=(launch?'start_':'beam_')+level,f=launch?Math.min(4,Math.floor(u/.032)):nb80Frame(P);return{name,f,a:NB80_ART.banks[name][f]};}
nb23AttackTick=function(b,dt){const P=nb80Act(b);if(!P)return NB80.base.tick.apply(this,arguments);const N=b._r30.v18;P.t+=dt;const u=P.t-P.tell;
 combatWarningTick(b,'nb23-'+N.seq,Math.min(P.t,P.tell),P.tell);b.x=P.origin.x;b.y=P.origin.y;P.eyes=nb23Eyes(b);P.warningEyes=P.eyes.map(q=>({...q}));
 if(u>=0&&!P.fired){P.fired=true;r30Sound('combatBeam0927');nb23Log('eye-release',{eyes:P.eyes});NB80.events.push({event:'eye-release',clock:b._r30.clock,eyes:P.eyes.map(q=>({...q})),width:NB80_ART.widths[0]});if(NB80.events.length>120)NB80.events.shift();}
 if(u>=0&&u<P.active){P.widthStep=Math.min(5,Math.floor(u/.08));const a=nb80Beam(P).a;for(const eye of P.eyes)for(const seat of seatList())withSeat(seat,()=>{if(player.dead||player.y<eye.y||player.y>eye.y+NB80_ART.beamLength)return;if([[0,0],[-4,0],[4,0],[0,-4],[0,4]].some(([x,y])=>nb80Inside(a,eye,player.x+x,player.y+y)))playerHit('Neural Archon eye laser');});}
 if(P.t>=P.tell+P.active+P.recover){N.attack=null;b._r30.attack=null;b._r30.cd=.65;j3State(b).attacks++;nb23Log('recovery-complete',{type:P.type});}
};
nb23Warnings=function(b,P){if(!nb80Act(b))return NB80.base.warnings.apply(this,arguments);if(P.t>=P.tell)return;const u=P.t/P.tell,colour=u<.4?'green':u<.74?'yellow':'red';for(const eye of nb23Eyes(b))nb80Blit('warning_'+colour,0,eye.x,eye.y);};
r30DrawBoss=function(b){const P=nb80Act(b);if(!P)return NB80.base.draw.apply(this,arguments);const Q=nb80Lens(b),u=P.t-P.tell;nb23Warnings(b,P);nb80Body(b);
 if(u>=0&&u<P.active){const q=nb80Beam(P);for(const eye of nb23Eyes(b))nb80Blit(q.name,q.f,eye.x,eye.y);}
 else if(u>=P.active&&u<P.active+.32)for(const eye of nb23Eyes(b))nb80Blit('recover',Math.floor((u-P.active)/.32*16),eye.x,eye.y);
 // These are the warm emitting pixels from this exact whole-body frame, not
 // a generic orb, static face rectangle or a separately interpolated socket.
 nb80Blit('eyes_'+Q.bank,Q.index,b.x,b.y);
};
globalThis.BOF_NEURAL_OPTICS_1030=NB80;
