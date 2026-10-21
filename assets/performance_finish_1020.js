'use strict';
/* Selected older weapon banks, three terminal effects, Cole-only cinematic performance.
   Combat timings, damage, warnings, hull identity, death accounting and cinematic callbacks retain their owners. */
const PF20={base:{load:stageLoadBegin,bomber:siegeBomberDraw,blit:polishBlit,shot:siegeBomberShot,
 gun:sc13GunDraw,death:dr21HullDeath,kind:dr21DeathKind,deathTick:updateDeathSpin,reset:player.reset,pose:inv20Pose,scene:inv20Draw,cinKeys:inv20Keys},bomber:null,draws:{},last:null};
for(const a of Object.values(PF20_ART))XART._src[a.key]=a.path;
for(const pose of ['report','horror'])XART._src['pf20_cole_'+pose+'_base']='assets/game/pilots/cole/body_frames/performance_1020/cole_'+pose+'_base.webp';
const pf20Keys=names=>names.map(n=>PF20_ART[n]?.key).filter(Boolean);
stageLoadBegin=function(n,keys){const names=['laser_terminal','ice_shatter','dark_terminal'];if(n===5)names.push('bomber_cannon');if(n===6)names.push('carrier_turret');
 return PF20.base.load.call(this,n,[...(keys||[]),...pf20Keys(names)]);};
inv20Keys=function(){return [...PF20.base.cinKeys(),...pf20Keys(['cole_report_face','cole_horror_face','cole_report_gesture','cole_horror_gesture']),'pf20_cole_report_base','pf20_cole_horror_base'];};
function pf20Ready(n){return !!PF20_ART[n]&&XART.rdy(PF20_ART[n].key);}
function pf20Frame(n,i,x,y,k=1,flash=0,color=null,alpha=1){const a=PF20_ART[n];if(!a||!XART.rdy(a.key))return false;
 i=clamp(i|0,0,a.frames-1);const c=a.cells[i],im=color?(xartPalette(a.key,color)||XART.get(a.key)):XART.get(a.key);
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=alpha;ctx.drawImage(im,...c,x-a.pivot[0]*k,y-a.pivot[1]*k,a.w*k,a.h*k);
 if(flash>0){ctx.globalAlpha*=clamp(flash/.12,0,1);ctx.drawImage(xartTint(a.key,'#ffffff',1),...c,x-a.pivot[0]*k,y-a.pivot[1]*k,a.w*k,a.h*k);}
 ctx.restore();PF20.draws[n]=(PF20.draws[n]||0)+1;PF20.last={bank:n,frame:i,x,y,k};return true;
}
function pf20WeaponFrame(phase,t,dur=1){if(phase==='tell'||phase==='charge')return Math.min(7,Math.floor(clamp(t/dur,0,.999)*8));
 if(phase==='fire'||phase==='beam')return 8+Math.min(2,Math.floor(t/.045));
 if(phase==='recover')return 11+Math.min(4,Math.floor(clamp(t/dur,0,.999)*5));return 0;}
siegeBomberDraw=function(b){const old=PF20.bomber;if(b?._bomber&&!b._bomber.space&&!b.dead)PF20.bomber=b;
 try{return PF20.base.bomber.apply(this,arguments);}finally{PF20.bomber=old;}};
polishBlit=function(name,i,x,y,w,h,flash){const b=PF20.bomber;
 if(b&&name==='bomber'&&i===2&&pf20Ready('bomber_cannon')){const B=b._bomber,H=b._hc1007;let phase=B.mode,clock=B.t,duration=phase==='recover'?Math.min(.45,B.dur):B.dur;
  if(H){phase=H.mode==='recover'?'recover':'rest';clock=H.age;duration=.45;
   const part=siegeBomberParts(b).find(p=>p.cell===2&&Math.abs(p.x-x)<1&&Math.abs(p.y-y)<1),L=H.lines?.find(q=>q.id===part?.id);
   if(L&&['lances','strafe'].includes(H.mode)){const age=H.age-L.delay;phase=age<0?'rest':age<H.warm?'tell':age<H.warm+(H.mode==='lances'?.76:1.25)?'fire':'recover';clock=phase==='tell'?age:phase==='fire'?age-H.warm:age-H.warm-(H.mode==='lances'?.76:1.25);duration=phase==='tell'?H.warm:.45;}
   else if(H.mode==='cross'){const S=hc1007CrossState(b);if(S){phase=S.mode==='tell'?'tell':S.mode==='live'?'fire':'recover';clock=phase==='tell'?S.p:phase==='fire'?S.local:Math.max(0,S.local-H.cross.on);duration=phase==='tell'?1:.45;}}
  }
  const frame=pf20WeaponFrame(phase,clock,duration);
  return pf20Frame('bomber_cannon',frame,x,y,h/216,flash);}
 return PF20.base.blit.apply(this,arguments);
};
function pf20TurretDraw(part,x,y,w,h,flash=0){if(part.dead||!pf20Ready('carrier_turret'))return false;
 const phase=part.phase==='rest'&&part.t<.32?'recover':part.phase,frame=pf20WeaponFrame(phase,part.t||0,phase==='tell'?1.12:phase==='recover'?.32:1);
 // Keep the main carrier's original q.y-22 placement (its crop pivot differs from the mini's socket).
 return pf20Frame('carrier_turret',frame,x,y-h*22/47.5+60*w/128,w/128,flash,phase==='tell'||phase==='fire'?'#78dfff':null);
}
sc13GunDraw=function(b,g){if(g.dead||!pf20Ready('carrier_turret'))return PF20.base.gun.apply(this,arguments);
 const p=sc13Mount(b,g.id),L=b._cargo13.lasers.find(q=>q.id===g.id),phase=L?(L.t<L.warm?'tell':'fire'):g.cool>0?'recover':'rest';
 const age=L?(phase==='tell'?L.t:L.t-L.warm):g.cool>0?.4-g.cool:0,duration=L&&phase==='tell'?L.warm:.4;
 pf20Frame('carrier_turret',pf20WeaponFrame(phase,age,duration),p.x,p.y,42/128,Math.max(g.fl||0,g.flash||0),phase==='tell'||phase==='fire'?sc13Light(b,g).color:null);
 sc13MuzzleDraw(b,g);if(g.hp<g.maxhp){ctx.fillStyle='#061320';ctx.fillRect(p.x-16,p.y-26,32,4);ctx.fillStyle='#7ee7ff';ctx.fillRect(p.x-15,p.y-25,30*g.hp/g.maxhp,2);}
};
// Terminal variants use the exact current aircraft captured by the existing life/death owner.
function pf20Reset(){this._dr21Death=null;return PF20.base.reset.apply(this,arguments);}
player.reset=player2.reset=pf20Reset;
dr21DeathKind=function(source){const text=source&&typeof source==='object'?source.kind||source.type||'':source,old=PF20.base.kind(text);if(old)return old;
 const s=String(text||'').toLowerCase();if(/committed bomber lance|veteran ion lance/.test(s))return 'laser';
 return /\b(dark|void|abyss)\b|^shadow$|s9warp|s8rift|s5null|s8void/.test(s)?'dark':null;
};
function pf20ShardMasks(D){if(D._pf20Shards)return D._pf20Shards;const im=D.image,w=im.width,h=im.height,g=im.getContext('2d'),src=g.getImageData(0,0,w,h);
 const sites=[[.38,.20],[.62,.24],[.50,.38],[.31,.43],[.71,.48],[.45,.55],[.59,.61],[.26,.65],[.77,.68],[.42,.78],[.62,.81],[.51,.91]].map(p=>[p[0]*w,p[1]*h]);
 const data=sites.map(()=>new Uint8ClampedArray(w*h*4)),centers=sites.map(()=>[0,0,0]);
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){const off=(y*w+x)*4;if(!src.data[off+3])continue;let id=0,best=Infinity;
  for(let i=0;i<sites.length;i++){const d=(x-sites[i][0])**2+(y-sites[i][1])**2;if(d<best){best=d;id=i;}}
  data[id].set(src.data.subarray(off,off+4),off);centers[id][0]+=x;centers[id][1]+=y;centers[id][2]++;
 }
 D._pf20Shards=data.map((a,i)=>{const c=document.createElement('canvas');c.width=w;c.height=h;c.getContext('2d').putImageData(new ImageData(a,w,h),0,0);return{im:c,cx:centers[i][2]?centers[i][0]/centers[i][2]:sites[i][0],cy:centers[i][2]?centers[i][1]/centers[i][2]:sites[i][1],pixels:centers[i][2]};}).filter(q=>q.pixels>0);
 return D._pf20Shards;
}
function pf20HullWhite(D){if(D._pf20White)return D._pf20White;const c=document.createElement('canvas');c.width=D.image.width;c.height=D.image.height;const g=c.getContext('2d');g.drawImage(D.image,0,0);g.globalCompositeOperation='source-in';g.fillStyle='#eeffff';g.fillRect(0,0,c.width,c.height);return D._pf20White=c;}
function pf20DeathArt(n,u,x,y,size,alpha=1){const a=PF20_ART[n];return a&&pf20Frame(n,Math.floor(clamp(u,0,.999)*a.frames),x,y,size/a.w,0,null,alpha);}
dr21HullDeath=function(D){if(!['laser','ice','shadow','dark'].includes(D.kind))return PF20.base.death(D);
 const needed=D.kind==='ice'?'ice_shatter':D.kind==='laser'?'laser_terminal':'dark_terminal';if(!pf20Ready(needed))return PF20.base.death(D);
 const t=D.t,u=clamp(t/D.life,0,1),shadow=D.kind==='shadow',scale=shadow?lerp(.60,3.25,v19Ease(u/.65)):.65,x=D.x,y=D.y-(shadow?80*v19Ease(u):0),w=D.image.width,h=D.image.height,size=w*scale;
 ctx.save();ctx.imageSmoothingEnabled=false;
 if(shadow)dr21Art('ball',t+(D.ballTime||0),x,y,lerp(D.foreground||300,Math.max(1100,(D.foreground||300)*1.4),v19Ease(u)),1-clamp((u-.75)/.25,0,1),false,(t+(D.ballTime||0))*TAU*.85);
 if(D.kind==='laser'){
  const cut=clamp((u-.16)/.58,0,1);if(cut<1){ctx.save();ctx.beginPath();ctx.rect(x-size/2,y-size/2+size*cut,size,size*(1-cut));ctx.clip();ctx.drawImage(D.image,x-size/2,y-size/2,size,size);
   ctx.globalAlpha=.72*(1-cut);ctx.drawImage(pf20HullWhite(D),x-size/2,y-size/2,size,size);ctx.restore();}
  pf20DeathArt('laser_terminal',t/1.12,x,y,200,1-clamp((u-.75)/.25,0,1));
 }else if(D.kind==='ice'){
  const q=clamp((t-.46)/.85,0,1);
  if(t<.46){ctx.drawImage(D.image,x-size/2,y-size/2,size,size);dr21Art('ice',Math.min(t,.4),x,y,190,1,true);}
  else{for(const [i,p] of pf20ShardMasks(D).entries()){const dx=p.cx-w/2,dy=p.cy-h/2,len=Math.hypot(dx,dy)||1,spread=115*q;
    ctx.save();ctx.translate(x+dx*scale+dx/len*spread,y+dy*scale+dy/len*spread+70*q*q);ctx.rotate(((i%5)-2)*q*1.1);ctx.globalAlpha=1-clamp((q-.66)/.34,0,1);ctx.drawImage(p.im,-p.cx*scale,-p.cy*scale,w*scale,h*scale);ctx.restore();}
   pf20DeathArt('ice_shatter',q,x,y,220,1-clamp((q-.85)/.15,0,1));}
 }else{
  const q=clamp((u-.12)/.73,0,1),a=q*2.4,c=Math.cos(a),s=Math.sin(a),collapse=1-q,local=scale*(1-q*.8);
  for(const [i,p] of pf20ShardMasks(D).entries()){const dx=(p.cx-w/2)*scale,dy=(p.cy-h/2)*scale;
   ctx.save();ctx.translate(x+(dx*c-dy*s)*collapse,y+(dx*s+dy*c)*collapse);ctx.rotate(q*((i%3)-1)*1.5);ctx.globalAlpha=1-q*q;ctx.drawImage(p.im,-p.cx*local,-p.cy*local,w*local,h*local);ctx.restore();}
  pf20DeathArt('dark_terminal',Math.max(0,t-.08)/1.2,x,y,shadow?200+u*280:210,.85*(1-clamp((u-.78)/.22,0,1)));
 }
 ctx.restore();PF20.deaths=PF20.deaths||{};PF20.deaths[D.kind]=(PF20.deaths[D.kind]||0)+1;
};
updateDeathSpin=function(dt){const D=player._dr21Death,before=D?.t||0,r=PF20.base.deathTick.apply(this,arguments);
 if(D&&D.t>=.46&&before<.46&&!D._pf20Cue){D._pf20Cue=true;
  if(D.kind==='ice')(Audio.SFX.expIce||Audio.SFX.hit)();else if(D.kind==='laser')Audio.SFX.slice?.();else if(D.kind==='dark'||D.kind==='shadow')Audio.SFX.shadowRelease?.();}
 return r;};
// Cole alone: fixed full-body reference geometry, small generated gesture/eyelid/lip regions.
inv20Draw=function(t){const old=PF20.cinematicScene;PF20.cinematicScene=INV20.shots.find(a=>t>=a[1]&&t<a[2])?.[0]||'';try{return PF20.base.scene.apply(this,arguments);}finally{PF20.cinematicScene=old;}};
inv20Pose=function(pk,x,bottom,height,t=0,horror=false){if(pk!=='cole')return PF20.base.pose.apply(this,arguments);
 const face='cole_'+(horror?'horror':'report')+'_face',gesture='cole_'+(horror?'horror':'report')+'_gesture',base='pf20_cole_'+(horror?'horror':'report')+'_base',fallback='ui20_cole-'+(horror?'horror':'report');
 const source=XART.rdy(base)?base:XART.rdy(fallback)?fallback:null;if(!source)return PF20.base.pose.apply(this,arguments);
 const scene=PF20.cinematicScene||INV20.last?.scene||'',sourceH=['relief','alarm','federation','horror'].includes(scene)?704:1024,
  im=XART.get(source),k=height/sourceH,cx=Math.max(x,256*k+6),left=cx-256*k,top=bottom-height,
  speaking=!horror&&(scene==='report'||INV20.active&&scene===''),clock=Math.max(0,t),
  gf=horror?(clock<3?Math.min(23,Math.floor(clock*8)):12+Math.floor((clock-3)*8)%12):Math.floor(clock*8)%24,
  ff=horror?(clock<2?Math.min(15,Math.floor(clock*8)):clock%4.8>4.1?Math.min(15,Math.floor((clock%4.8-4.1)*20)):15):speaking?Math.floor(clock*8)%16:(clock%4.8>4.1?Math.floor((clock%4.8-4.1)*20)%16:0);
 ctx.save();ctx.imageSmoothingEnabled=false;
 if(!pf20Ready(face)||!pf20Ready(gesture)){ctx.drawImage(im,0,0,512,sourceH,left,top,512*k,height);ctx.restore();return {pilot:pk,key:source,x:cx,bottom,height,horror,performance:false};}
 // The old owner read only704 of1024 source rows; source feet now meet the floor.
 ctx.drawImage(im,0,0,512,168,left,top,512*k,168*k);ctx.drawImage(im,0,480,512,sourceH-480,left,top+480*k,512*k,(sourceH-480)*k);
 const G=PF20_ART[gesture],F=PF20_ART[face];ctx.drawImage(XART.get(G.key),...G.cells[gf],left,top,512*k,512*k);
 for(const r of [[50,88,36,22],[98,88,36,22],[64,123,58,25]]){const c=F.cells[ff];ctx.drawImage(XART.get(F.key),c[0]+r[0],c[1]+r[1],r[2],r[3],left+(160+r[0])*k,top+r[1]*k,r[2]*k,r[3]*k);}
 ctx.restore();PF20.cole={face:ff,gesture:gf,horror,x:cx,bottom,height,scene};INV20.draws[base]=(INV20.draws[base]||0)+1;CE20.draws[base]=(CE20.draws[base]||0)+1;
 return {pilot:pk,key:F.key,x:cx,bottom,height,horror,performance:true};
};
window.BOFPERFORMANCE={get state(){return PF20;},warm(){for(const a of Object.values(PF20_ART))XART.rdy(a.key);XART.rdy('pf20_cole_report_base');XART.rdy('pf20_cole_horror_base');},get ready(){return Object.values(PF20_ART).every(a=>XART.rdy(a.key))&&XART.rdy('pf20_cole_report_base')&&XART.rdy('pf20_cole_horror_base');}};
