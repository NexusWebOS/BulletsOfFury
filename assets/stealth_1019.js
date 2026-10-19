"use strict";
/* PixelLab refraction surrounds the actual ship. Stealth never substitutes a
   portal/diamond for Nyx or hides the player's friendly silhouette. */
const SK19={draws:[],base:{load:stageLoadBegin,spiral:ra7NyxSpiral,air:air13DrawRebel,friendly:rg4Friendly,cell:rg4Cell,mount:lzMountDraw}};
for(const bank of Object.values(SK19_ART.banks))for(const a of bank)XART._src[a.key]=a.path;
function sk19Keys(){return Object.values(SK19_ART.banks).flat().map(a=>a.key);}
function sk19Ready(){let ready=true;for(const k of sk19Keys())if(!XART.rdy(k))ready=false;return ready;}
function sk19Index(bank,progress){const n=SK19_ART.banks[bank].length;return clamp(Math.floor(clamp(progress,0,1)*n),0,n-1);}
stageLoadBegin=function(n,keys){return SK19.base.load.call(this,n,[...(keys||[]),...(n===6||n===10?sk19Keys():[])]);};
function sk19Draw(bank,frame,x,y,scale,alpha=1,front=false){const a=SK19_ART.banks[bank]?.[frame];if(!a||!XART.rdy(a.key))return false;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=alpha;
 if(front){ctx.beginPath();for(const [top,h]of [[-.36,.13],[-.05,.15],[.26,.13]])ctx.rect(x-80*scale,y+192*scale*top,160*scale,192*scale*h);ctx.clip();}
 ctx.drawImage(XART.get(a.key),x-80*scale,y-96*scale,160*scale,192*scale);ctx.restore();
 SK19.draws.push({key:a.key,x,y,scale,alpha,front});if(SK19.draws.length>160)SK19.draws.shift();return true;
}
function sk19NyxPose(q){const A=q.rg4?.act,demo=q._ra7CloakDemo;
 if(demo)return{bank:'in',frame:sk19Index('in',demo.t/1.65),alpha:1};
 if(A?.kind==='cloak'&&A.phase==='charge')return{bank:'in',frame:sk19Index('in',A.t/A.warm),alpha:1};
 if(q._ra7Reveal>0)return{bank:'out',frame:sk19Index('out',1-q._ra7Reveal/.55),alpha:.8};
 if(q.frCloak>0)return{bank:'loop',frame:Math.floor((rg4State()?.age??q.t??0)*18)%32,alpha:.72};
 return null;
}
ra7NyxSpiral=function(q,front=false){const P=sk19NyxPose(q);if(!P)return;
 return sk19Draw(P.bank,P.frame,q.x,q.y,.72,P.alpha*(front?.70:.42),front);};
air13DrawRebel=function(q,opts){if(q?.key==='nyx'&&!q.dead){const A=q.rg4?.act;let alpha=opts?.alpha??1;
  if(A?.kind==='cloak'&&A.phase==='charge')alpha=1-.82*clamp(A.t/A.warm,0,1);
  else if(q._ra7Reveal>0)alpha=.18+.82*(1-clamp(q._ra7Reveal/.55,0,1));
  else if(q.frCloak>0)alpha=.18;
  return SK19.base.air.call(this,q,{...(opts||{}),alpha});
 }return SK19.base.air.apply(this,arguments);
};
rg4Friendly=function(m,G){const q=m.ref,key='ship_'+m.key;if(!XART.rdy(key))return SK19.base.friendly.apply(this,arguments);
 const im=XART.get(key),h=SHIP_DRAW_H,w=h*im.width/im.height,C=G.scene,k=clamp(G.cloak||0,0,1);let P=null;
 if(C?.revealAt!=null){P={bank:'out',frame:sk19Index('out',(C.age-C.revealAt)/1.35)};}
 else if(C?.castAt!=null&&C.age-C.castAt>=1){P=k<.97?{bank:'in',frame:sk19Index('in',k)}:{bank:'loop',frame:Math.floor(G.age*18)%32};}
 if(P)sk19Draw(P.bank,P.frame,q.x,q.y,.45,.44,false);
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=1-k*.48;ctx.drawImage(im,q.x-w/2,q.y-h/2,w,h);
 if(q.flash>0){const hit=xartTint(key,hitFlashColor(q),1);if(hit){ctx.globalAlpha=Math.min(1,q.flash*9);ctx.drawImage(hit,q.x-w/2,q.y-h/2,w,h);}}
 ctx.restore();if(P)sk19Draw(P.bank,P.frame,q.x,q.y,.45,.58,true);
 // The authored counter-scan still closes its real Retina on the cloaked squad.
 if(C?.scanAt!=null&&C.revealAt==null){const p=clamp((C.age-C.scanAt-1)/3.5,0,1),f=Math.floor(G.age*10)%4,ret=retinaTinted(p>=1?'retB':'retA',f,G.scanner||'kaia');
  if(ret){const x=q.x+Math.sin(G.age*2+m.pin.y)*(1-p)*100,y=q.y+Math.cos(G.age*1.7+m.pin.x)*(1-p)*90;ctx.save();ctx.globalAlpha=.85;ctx.drawImage(ret,x-25,y-25,50,50);ctx.restore();RG4.draws.scan=(RG4.draws.scan||0)+1;}}
};
rg4Cell=function(row,f,x,y,w,h=w,alpha=1,color){if((row===1||row===2)&&rg4State()){
 const bank=row===2?'out':'loop',frame=row===2?sk19Index('out',f/5):Math.floor(rg4State().age*18)%32;
 return sk19Draw(bank,frame,x,y,Math.min(w/128,h/160),alpha*.72,false);
 }return SK19.base.cell.apply(this,arguments);
};
lzMountDraw=function(){const G=rg4State(),m=G?.scene?.kind==='rescue'&&lzMount?.docked?
 G.members?.find(q=>q.seat&&q.key==='lizzie'):null;
 if(!m||!Number.isFinite(lzMount.x)||!Number.isFinite(lzMount.y))return SK19.base.mount.apply(this,arguments);
 // The rescue moves actual aircraft while its ordinary attachment clock is
 // paused. Compensate only in painting; do not advance the loan or mutate it.
 ctx.save();ctx.translate(m.ref.x-lzMount.x,m.ref.y-14-lzMount.y);
 ctx.globalAlpha*=1-clamp(G.cloak||0,0,1)*.48;
 try{return SK19.base.mount.apply(this,arguments);}finally{ctx.restore();}
};
window.BOF_STEALTH={state:SK19,ready:sk19Ready,draw:sk19Draw,nyxPose:sk19NyxPose};
