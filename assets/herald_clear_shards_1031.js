'use strict';
/* HR87: one-pass glass fragments and the existing inscribed spell seal before
   the tornado cast. Native damage, skull interception and storm behavior remain. */
const HR87={base:{start:hr28Start,draw:heraldDeathDraw,update:updatePlay},events:[],draws:{}};
hr28Start=function(b,kind){const r=HR87.base.start.apply(this,arguments),A=hh52Special(b);if(kind==='storm'&&A){A.warm=5.4;A._hr87Seal=true;A._hr87Phase=null;HR87.events.push({event:'storm-inscription-start',time:efxClock,warm:A.warm});}return r;};
function hr87Seal(b,A){const t=A.t,p=hs53SealPoint(b);let bank,f;
 if(t<.6)return;
 if(t<3.35){bank='seal_build';f=Math.floor((t-.6)/2.75*56);}
 else if(t<4.55){bank='seal_spin';f=Math.floor((t-3.35)/1.2*32)%32;}
 else if(t<5.4){bank='seal_pulse';f=Math.floor((t-4.55)/.85*24);}
 else if(t<6.05){bank='seal_burst';f=Math.floor((t-5.4)/.65*16);}
 if(bank){hs53Blit(bank,f,p.x,p.y);HR87.draws[bank]=(HR87.draws[bank]||0)+1;if(A._hr87Phase!==bank){A._hr87Phase=bank;HR87.events.push({event:'inscription-stage',time:efxClock,bank});}}
 if(HR87.events.length>400)HR87.events.shift();
}
heraldDeathDraw=function(b){const out=HR87.base.draw.apply(this,arguments),A=hh52Special(b);if(A?.kind==='storm'&&A._hr87Seal)hr87Seal(b,A);return out;};
function hr87Shard(q){return q?._hh52Chunk||q?._hg70Glass||q?._hs53==='shard';}
updatePlay=function(dt){const out=HR87.base.update.apply(this,arguments);for(const q of eBullets)if(hr87Shard(q)&&!q.dead){const p=72;if(q.x<camLeftX()-p||q.x>camRightX()+p||q.y<viewTopY()-p||q.y>VH+p)q.dead=true;}return out;};
globalThis.BOF_HERALD_CLEAR_SHARDS=HR87;
