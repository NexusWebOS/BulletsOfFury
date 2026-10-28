'use strict';
/* One whole Nightwing plate and one native life. The Harrier keeps its modules. */
const NW28={base:{spawn:whvAceSpawn,tick:whvAceTick,draw:whvDrawAce,invuln:whvAceInvuln,hit:warhiveHitTest,damage:warhiveDamage,targets:retinaBossTargets,load:stageLoadBegin},events:[],alpha:new Map(),draws:0,last:null};
for(const key of['whole','whole_hit'])XART._src[NW28_ART[key].key]=NW28_ART[key].path;
function nw28Own(b){return run.stage===6&&!run._gp4StageX&&!b?._gp4Host&&!!b?._whv?.ace;}
function nw28Intro(A){return !!A?._nw28&&A._nw28.mode!=='fight';}
function nw28Log(b,event,data={}){NW28.events.push({event,time:efxClock,x:b._whv.ace.x,y:b._whv.ace.y,...data});if(NW28.events.length>240)NW28.events.shift();}
stageLoadBegin=function(n,keys){return NW28.base.load.call(this,n,n===6?[...(keys||[]),NW28_ART.whole.key,NW28_ART.whole_hit.key]:keys);};
function nw28Mode(b,mode){const A=b._whv.ace,M=A._nw28;M.mode=mode;M.t=0;M.from={x:A.x,y:A.y};M.heading=mode==='north'||mode==='north_wait'?'north':'south';nw28Log(b,'entrance-'+mode);}
whvAceSpawn=function(b){const out=NW28.base.spawn.apply(this,arguments);if(!nw28Own(b))return out;const A=b._whv.ace;
 A._nw28={mode:'south',t:0,heading:'south',from:{x:A.x,y:A.y},corner:player.x<camLeftX()+viewW()/2?camRightX()-105:camLeftX()+105,returnX:camLeftX()+viewW()/2};
 delete A.fl;delete A._hitMod;b.modular=false;b._noHit=true;b.w=184;b.h=192;nw28Log(b,'entrance-south');return out;};
whvAceTick=function(b,dt){if(!nw28Own(b)||!nw28Intro(b._whv.ace)||b.dead)return NW28.base.tick.apply(this,arguments);
 const A=b._whv.ace,M=A._nw28;dt=Math.min(.05,dt);M.t+=dt;A.t+=dt;A.st='emerge';A.vx=A.vy=0;b._noHit=true;
 if(M.mode==='south'){const u=clamp(M.t/1.1,0,1);A.y=lerp(M.from.y,VH+160,u*u);if(u>=1)nw28Mode(b,'south_wait');}
 else if(M.mode==='south_wait'){if(M.t>=.22){A.x=M.corner;A.y=VH+160;nw28Mode(b,'north');combatAudio0927(b,'jetDash',.45);}}
 else if(M.mode==='north'){const u=clamp(M.t/1.45,0,1);A.x=M.corner;A.y=lerp(VH+160,viewTopY()-160,u);if(u>=1)nw28Mode(b,'north_wait');}
 else if(M.mode==='north_wait'){if(M.t>=.22){A.x=M.returnX;A.y=viewTopY()-160;nw28Mode(b,'return');combatAudio0927(b,'launch',.4);}}
 else if(M.mode==='return'){const u=clamp(M.t/1.25,0,1),e=u*u*(3-2*u),home=clamp((WHV_ZONE.y0+WHV_ZONE.y1)/2,viewTopY()+110,VH*.45);A.y=lerp(M.from.y,home,e);if(u>=1)nw28Mode(b,'settle');}
 else if(M.mode==='settle'){if(M.t>=.4){nw28Mode(b,'fight');A.st='fight';A.t=0;A.rollCd=1.2;A.somerCd=3;A.gunCd=1.2;A.mslCd=4.5;A.dashCd=7;A._ra7Cd=5;b._noHit=false;}}
 b.x=A.x;b.y=A.y;b._drawY=A.y;delete A.fl;delete A._hitMod;
};
whvAceInvuln=function(A){return nw28Intro(A)||NW28.base.invuln.apply(this,arguments);};
function nw28Frame(b){const A=b._whv.ace,M=A._nw28,G=NW28_ART.groups,cycle=Math.floor(efxClock*14)%8;
 if(b.dead)return G.death.start+((Math.round((A.spin||0)/TAU*32)%32)+32)%32;
 if(nw28Intro(A))return G[M.heading==='north'?'north':'south'].start+cycle;
 if(A.somer){const f=Math.min(15,Math.floor(clamp(A.somer.t/.62,0,1)*16)),i=(f+(A.inverted?8:0))%16;return G[A.inverted?'inverted_somer':'somer'].start+i;}
 if(A.roll){const f=Math.min(15,Math.floor(clamp(A.roll.t/.46,0,1)*16));return G.roll.start+(A.roll.dir<0?(16-f)%16:f);}
 if(A.inverted)return G.inverted.start;if(Math.abs(A.vx)>170)return G[A.vx>0?'bank_right':'bank_left'].start;
 return G[b.hp/b.maxhp<.5?'damaged':'south'].start+cycle;
}
function nw28DrawBody(b){const A=b._whv.ace,a=NW28_ART[b.flash>0&&!b.dead?'whole_hit':'whole'],f=nw28Frame(b);if(!XART.rdy(a.key))return;
 ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(A.x)-a.pivot[0],Math.round(A.y)-a.pivot[1],a.cw,a.ch);NW28.draws++;NW28.last={frame:f,key:a.key,x:A.x,y:A.y,whole:true};}
function nw28AlphaAt(b,x,y){const A=b._whv.ace,a=NW28_ART.whole,f=nw28Frame(b),px=Math.floor(x-Math.round(A.x)+a.pivot[0]),py=Math.floor(y-Math.round(A.y)+a.pivot[1]);if(px<0||py<0||px>=a.cw||py>=a.ch||!XART.rdy(a.key))return false;
 let mask=NW28.alpha.get(f);if(!mask){const c=document.createElement('canvas');c.width=a.cw;c.height=a.ch;const g=c.getContext('2d');g.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,0,0,a.cw,a.ch);const d=g.getImageData(0,0,a.cw,a.ch).data;mask=Uint8Array.from({length:a.cw*a.ch},(_,i)=>d[i*4+3]);NW28.alpha.set(f,mask);}return mask[py*a.cw+px]>48;
}
warhiveHitTest=function(b,x,y){if(!nw28Own(b))return NW28.base.hit.apply(this,arguments);return !b.dead&&b._whv.mode==='ace'&&!whvAceInvuln(b._whv.ace)&&nw28AlphaAt(b,x,y);};
warhiveDamage=function(b,dmg){if(nw28Own(b)&&nw28Intro(b._whv.ace))return 0;const out=NW28.base.damage.apply(this,arguments);if(nw28Own(b)){delete b._whv.ace.fl;delete b._whv.ace._hitMod;}return out;};
retinaBossTargets=function(b){if(!nw28Own(b))return NW28.base.targets.apply(this,arguments);return !b.dead&&b._whv.mode==='ace'&&!whvAceInvuln(b._whv.ace)?[b]:[];};
whvDrawAce=function(b){if(!nw28Own(b))return NW28.base.draw.apply(this,arguments);const A=b._whv.ace;if(b.dead&&A.crash)return;
 if(!b.dead&&!nw28Intro(A)){const w=184,P=A.desp;if(A.dash?.st==='warn')combatWarningDraw(b,{x:A.x,y:A.y,ex:A.dash.ex,ey:A.dash.ey,progress:A.dash.t/.95,width:w*.65});
  if(P?.st==='warn')combatWarningDraw(b,{x:A.x,y:A.y,ex:A.x,ey:VH+60,progress:P.t/.8,width:w*.65});
  if(P?.st==='cross'&&P.t<P.lead){combatWarningDraw(b,{x:P.x0,y:P.y0,ex:P.x1,ey:P.y1,progress:P.t/P.lead,width:95,fieldOnly:true});return;}
  const gun=A._pw5Gun;if(gun&&gun.t<gun.tell)for(const side of[-1,1])combatWarningDraw(b,{x:A.x+side*16,y:A.y+30,ex:gun.tx+side*(gun.spread?90:24),ey:gun.ty,width:24,progress:gun.t/gun.tell,fieldOnly:true});
  const C=A._ra7Gate;if(C?.phase==='warn')for(const side of[-1,1])for(const spread of[0,.28]){const a=Math.PI/2-side*spread;combatWarningDraw(C,{x:C.x+side*50,y:C.y+48,ex:C.x+side*50+Math.cos(a)*VH,ey:C.y+48+Math.sin(a)*VH,width:19,progress:C.t/C.warn,fieldOnly:spread>0,laneShape:'line'});}
 }
 nw28DrawBody(b);
 if(!b.dead&&!nw28Intro(A)){const r=b.hp/b.maxhp;whvPartFx(b,{x:A.x-58,y:A.y},r,false,.8,5);whvPartFx(b,{x:A.x+58,y:A.y},r,false,.8,6.3);}
};
globalThis.BOF_NIGHTWING_ENTRANCE_1027=NW28;
