'use strict';
/* Chronos rage: authored hot rings/scenery veil and a dedicated red remaining-HP gauge. */
const CF50={base:{tick:hammerBossTick,bg:drawBG,rings:drawShockRings,health:bossHealthFraction,theme:eh7Theme,load:stageLoadBegin,state:setState},rings:[],lastDim:0,lastRingFrames:[],events:[]};
for(const [key,s]of Object.entries(CF50_ART.sheets))XART._src[key]=s.path;
for(const bank of Object.values(CF50_ART.banks))XART._src['nca_'+bank.sheet]=CF50_ART.sheets[bank.sheet].path;
for(const bank of Object.values(CF50_ART.banks))for(const frame of bank.frames)BOFX.cells[frame.key]=[bank.sheet,...frame.cell];
EH7_ART.cf50_rage={...EH7_ART.stage_05,key:CF50_ART.health,path:CF50_ART.sheets[CF50_ART.health].path};
function cf50Own(b){return !!b&&c25Own(b)&&!b._heart;}
function cf50Sync(b){
 if(!cf50Own(b)||b.dead)return null;const h=b._hammer,C=h._hf22Charge;let m=h.cf50Rage;
 if(C&&m?.charge!==C||!m&&h._hf22Red){m=h.cf50Rage={charge:C||null,maxHp:Math.max(1,b.hp),before:clamp(b.hp/Math.max(1,b.maxhp),0,1),endAt:null};CF50.events.push({type:'rage-pool',hp:b.hp,max:b.maxhp,time:efxClock});}
 if(m&&!C&&h._hf22Red&&m.endAt==null)m.endAt=efxClock;
 return m;
}
function cf50DimLevel(b){const m=b?._hammer?.cf50Rage,h=b?._hammer;if(!m||!cf50Own(b)||b.dead)return 0;
 if(h._hf22Charge){const u=cgChargeU(b);return Math.round(clamp(c45Prog(u),0,1)*15);}
 if(!h._hf22Red)return 0;
 const u=clamp((efxClock-(m.endAt??efxClock))/C45_AFTER,0,1);return Math.round(15-6*u); // settles to45% scenery darkness
}
function cf50DimDraw(level){if(level<=0||!XART.rdy('cf50_scenery_dim'))return;const tile=CF50_ART.dim.tile,im=XART.get('cf50_scenery_dim'),sx=level%4*tile,sy=Math.floor(level/4)*tile;
 const left=Math.floor(camLeftX()),top=Math.floor(viewTopY()),right=Math.ceil(camRightX()),bottom=top+Math.ceil(viewH());
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.beginPath();ctx.rect(left,top,right-left,bottom-top);ctx.clip();
 for(let y=top;y<bottom;y+=tile)for(let x=left;x<right;x+=tile)ctx.drawImage(im,sx,sy,tile,tile,x,y,tile,tile);ctx.restore();
}
drawBG=function(){const out=CF50.base.bg.apply(this,arguments);const b=boss;
 CF50.lastDim=state===GS.PLAY&&cf50Own(b)?cf50DimLevel(b):0;if(CF50.lastDim)cf50DimDraw(CF50.lastDim);return out;};
function chronosRageRings(b){if(!cf50Own(b))return;CF50.rings=CF50.rings.filter(r=>r.owner!==b);
 for(const bank of ['small','large'])CF50.rings.push({owner:b,bank,x:Math.round(b.x),y:Math.round(b.y),start:efxClock});
 CF50.events.push({type:'hot-rings',time:efxClock,count:2});}
drawShockRings=function(){const out=CF50.base.rings.apply(this,arguments);CF50.lastRingFrames=[];
 for(const r of CF50.rings){if(r.owner.dead||r.owner!==boss||!cf50Own(r.owner))continue;
  const bank=CF50_ART.banks[r.bank],age=efxClock-r.start;if(age<0||age>=bank.life)continue;
  const i=Math.min(bank.frames.length-1,Math.floor(age/bank.life*bank.frames.length)),frame=bank.frames[i];if(!XART.rdy(frame.key))continue;
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.drawImage(XART.get(frame.key),r.x-frame.pivot[0],r.y-frame.pivot[1]);ctx.restore();
  CF50.lastRingFrames.push({bank:r.bank,index:i,key:frame.key,x:r.x,y:r.y});
 }return out;};
hammerBossTick=function(b,dt){cf50Sync(b);const out=CF50.base.tick.apply(this,arguments);cf50Sync(b);
 CF50.rings=CF50.rings.filter(r=>r.owner===boss&&!r.owner.dead&&cf50Own(r.owner)&&efxClock-r.start<CF50_ART.banks[r.bank].life);return out;};
bossHealthFraction=function(b){const m=b?._hammer?.cf50Rage,h=b?._hammer;
 if(cf50Own(b)&&!b.dead&&m){if(h._hf22Charge)return lerp(m.before,1,clamp(c45Prog(cgChargeU(b)),0,1));if(h._hf22Red)return clamp(b.hp/m.maxHp,0,1);}
 return CF50.base.health.apply(this,arguments);};
eh7Theme=function(b,stage){const h=b?._hammer,m=h?.cf50Rage;
 if(cf50Own(b)&&m&&(h._hf22Red||h._hf22Charge&&cgChargeU(b)>=C45_BEAT.readyEnd))return 'cf50_rage';
 return CF50.base.theme.apply(this,arguments);};
stageLoadBegin=function(n,keys){if(n===5)CF50.rings=[];return CF50.base.load.call(this,n,[...(keys||[]),...(n===5?Object.keys(CF50_ART.sheets):[])]);};
setState=function(next){if(next!==GS.PLAY&&next!==GS.PAUSED)CF50.rings=[];return CF50.base.state.apply(this,arguments);};
globalThis.BOF_CHRONOS_RAGE_PRESENTATION=CF50;
