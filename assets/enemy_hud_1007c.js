'use strict';
/* Authored enemy frames with continuous fills. No combat values are changed. */
const EH7={cache:new Map(),lastBoss:null,lastRebels:[],stage:0};
const EH7_BASE={bar:drawHealthBarV2,rebels:rg4HealthBars,load:stageLoadBegin,retire:bofDerivedCachesRetire};
function eh7Theme(b,stage=run.stage){return stage===6&&run._gp4StageX&&b?.kind==='warhive'?'harrier':'stage_'+String(clamp(stage||1,1,9)).padStart(2,'0');}
function eh7Keys(stage){const a=EH7_ART['stage_'+String(stage).padStart(2,'0')];return a?[a.key,...(stage===6?[EH7_ART.harrier.key,EH7_ART.rebels.key]:[])]:[];}
stageLoadBegin=function(n,keys){EH7.lastBoss=null;EH7.lastRebels=[];return EH7_BASE.load.call(this,n,[...new Set([...(keys||[]),...eh7Keys(n)])]);};
bofDerivedCachesRetire=function(){EH7.cache.clear();EH7.lastBoss=null;EH7.lastRebels=[];return EH7_BASE.retire.apply(this,arguments);};
function eh7Frame(theme,variant,width){
 const a=EH7_ART[theme],d=a?.variants[variant];if(!d||!XART.rdy(a.key))return null;
 const w=Math.max(1,Math.round(width)),id=theme+'/'+variant+'/'+w;
 if(EH7.cache.has(id))return EH7.cache.get(id);
 const im=XART.get(a.key),c=d.crop,s=w/c[2],h=Math.ceil(c[3]*s),cv=document.createElement('canvas');cv.width=w;cv.height=h;
 const g=cv.getContext('2d');g.imageSmoothingEnabled=true;g.drawImage(im,...c,0,0,w,c[3]*s);
 function local(r){const x=Math.floor((r[0]-c[0])*s),y=Math.floor((r[1]-c[1])*s);return [x,y,Math.ceil((r[0]+r[2]-c[0])*s)-x,Math.ceil((r[1]+r[3]-c[1])*s)-y];}
 function empty(r,x){const p=local(r);g.clearRect(...p);g.drawImage(im,x,r[1],4,r[3],...p);return p;}
 const hp=empty(d.hp,d.emptyX),shield=d.shield?empty(d.shield,d.emptyX):null;
 if(d.nameErase)empty(d.nameErase,d.nameEmptyX);
 const frame={canvas:cv,hp,shield,source:im,def:d,w,h};
 // Resizing cannot accumulate an unbounded set of derived canvases.
 if(EH7.cache.size>=24)EH7.cache.delete(EH7.cache.keys().next().value);
 EH7.cache.set(id,frame);return frame;
}
function eh7Meter(frame,well,source,frac,x,y){
 const f=Number.isFinite(frac)?clamp(frac,0,1):0;if(!well||!f)return;
 ctx.save();ctx.beginPath();ctx.rect(x+well[0],y+well[1],well[2]*f,well[3]);ctx.clip();
 ctx.drawImage(frame.source,frame.def.litX,source[1],4,source[3],x+well[0],y+well[1],well[2],well[3]);ctx.restore();
}
function eh7Paint(frame,x,y,frac,shield){
 ctx.save();ctx.imageSmoothingEnabled=true;ctx.drawImage(frame.canvas,x,y);
 eh7Meter(frame,frame.hp,frame.def.hp,frac,x,y);
 if(frame.shield)eh7Meter(frame,frame.shield,frame.def.shield,shield,x,y);
 ctx.restore();
}
drawHealthBarV2=function(kind,frac,cx,cy,w,inWorld,lagKey){
 const b=kind==='boss'?boss:subBoss;
 // The squad has five independently anchored bars instead of an aggregate bar.
 if(kind==='boss'&&b?._rebels){EH7.lastBoss=null;return true;}
 if(kind!=='boss'&&kind!=='mini')return EH7_BASE.bar.apply(this,arguments);
 const sf=b?bossShieldFrac(b):null,theme=eh7Theme(b),variant=kind+(sf==null?'':'Shield'),frame=eh7Frame(theme,variant,w);
 if(!frame)return EH7_BASE.bar.apply(this,arguments);
 if(kind==='boss'&&b)frac=bossHealthFraction(b);
 const x=Math.round(cx-frame.w/2),y=Math.max(2,Math.round(cy-frame.h/2));
 ctx.save();if(inWorld===true)ctx.translate(camX,0);if(kind==='boss'&&b)ctx.globalAlpha*=bossHealthAlpha(b);
 eh7Paint(frame,x,y,frac,sf);
 // Keep Hammer's recovery telegraph and the final boss's real charge fraction.
 if(kind==='boss'&&b?._hammer)hammerRecoveryBarDraw(x+frame.hp[0],y+frame.hp[1],frame.hp[2],frame.hp[3],false);
 ctx.restore();EH7.lastBoss={theme,variant,frac,shield:sf,x,y,w:frame.w,h:frame.h};return true;
};
rg4HealthBars=function(b){
 const a=EH7_ART.rebels;if(!XART.rdy(a.key))return EH7_BASE.rebels.apply(this,arguments);
 EH7.lastRebels=[];
 for(const q of b._rebels.ships){
  if(q.dead||q.hp<=0||q.frCloak>0)continue;
  const frame=eh7Frame('rebels',q.key,78);if(!frame)continue;
  const x=Math.round(q.x-frame.w/2),y=Math.round(q.y-58),frac=clamp(q.hp/Math.max(1,q.max),0,1);
  eh7Paint(frame,x,y,frac,null);
  campText(q.key.toUpperCase(),q.x,y-5,7,'#e6efff');
  EH7.lastRebels.push({pilot:q.key,frac,x,y,w:frame.w,h:frame.h});
 }
};
window.BOFEnemyHUD=EH7;
