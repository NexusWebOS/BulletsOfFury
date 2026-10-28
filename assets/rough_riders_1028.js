"use strict";
/* THE ROUGH RIDERS: matched crew identity and protected Stage 6 airshow.
   Existing weapons, health pools, combat AI and defeat remain the owners. */
const RR33={name:'THE ROUGH RIDERS',events:[],draws:0,last:null,base:{init:rebelSquadInit,intro:h3RebelTick,lines:h3RebelLines,ship:fr27RebelDrawShip,tick:rebelSquadTick,world:drawWorld,bg:drawLevelMaster,clouds:drawClouds,targets:retinaBossTargets,hit:rebelSquadHitTest,damage:rebelSquadDamage,load:stageLoadBegin}};
for(const a of Object.values(RR33_ART.banks))XART._src[a.key]=a.path;
function rr33Group(b){return run.stage===6&&!run._gp4StageX&&!b?._rebels?.frStageX&&b?._rebels?.ships?.length===5;}
function rr33Protected(b=boss){return rr33Group(b)&&!b.dead&&!b._rebels.frIntro?.done;}
function rr33Log(S,event,data={}){RR33.events.push({event,time:S.t,...data});if(RR33.events.length>200)RR33.events.shift();}
rebelSquadInit=function(b){const result=RR33.base.init.apply(this,arguments);if(b._rebels)b.name=RR33.name;return result;};
stageLoadBegin=function(n,keys){if(n===6)Snd.prepare?.(['chargeDash','launch','impactMetal']);const live=['font_chrome',...REBEL_KEYS.map(k=>'flight_'+k)];return RR33.base.load.call(this,n,n===6?[...(keys||[]),...live.map(k=>RR33_ART.banks[k].key)]:keys);};
function rr33Frame(q,frame){const a=RR33_ART.banks[RR33_ART.models[q.key]?.bank];if(!a||!XART.rdy(a.key))return false;frame=Math.max(0,Math.min(a.frames-1,frame|0));
 ctx.drawImage(XART.get(a.key),frame%a.cols*a.cw,Math.floor(frame/a.cols)*a.ch,a.cw,a.ch,Math.round(q.x-a.pivot[0]),Math.round(q.y-a.pivot[1]),a.cw,a.ch);RR33.draws++;return true;}
function rr33Text(text,x,y,variant='chrome'){const a=RR33_ART.banks['font_'+variant],glyphs=RR33_ART.font.glyphs;if(!XART.rdy(a.key))return false;const chars=Array.from(text),width=chars.reduce((n,ch)=>n+(glyphs[ch]?.advance||12),0);let left=Math.round(x-width/2);
 for(const ch of chars){const g=glyphs[ch];if(!g){left+=12;continue;}if(g.frame>=0)ctx.drawImage(XART.get(a.key),g.frame%a.cols*a.cw,Math.floor(g.frame/a.cols)*a.ch,a.cw,a.ch,left,Math.round(y-16),a.cw,a.ch);left+=g.advance;}return true;}
function rr33Pins(q){const cx=camLeftX()+viewW()/2,span=Math.min(168,(viewW()-144)/2),p=[[0,28],[-.5,-28],[.5,-28],[-1,-84],[1,-84]][q.i];return{x:cx+p[0]*span,y:VH*.41+p[1]};}
function rr33Ease(u){u=clamp(u,0,1);return u*u*(3-2*u);}
function rr33Path(q,u){const p=rr33Pins(q),start=camLeftX()+viewW()*[.18,.82,.30,.70,.50][q.i],v=rr33Ease(u),weave=(q.i%2?-1:1)*Math.min(62,viewW()*.13)*Math.sin(u*TAU)*Math.sin(u*Math.PI);
 return{x:lerp(start,p.x,v)+weave,y:lerp(-115,p.y,v)+86*Math.sin(u*Math.PI)};}
function rr33Actors(b,S,dt){const R=b._rebels,cx=camLeftX()+viewW()/2;
 if(s6Wing)for(const q of s6Wing.ships){q.all=true;q.phase='fight';q.t+=dt;const side=q.slot%2?1:-1,rank=Math.floor(q.slot/2);q.x=clamp(cx+side*(80+rank*52),camLeftX()+38,camRightX()-38);q.y=VH*.81+(q.slot%2)*18+Math.sin(S.t*1.2+q.slot)*3;}
 player.x=S.playerX+Math.sin(S.t*.65)*2;player.y=S.playerY+Math.sin(S.t*1.2)*3;
 for(const q of R.ships){q.mode='entry';q.t=S.t;const pin=rr33Pins(q),phaseFrame=Math.floor(S.t*24)%8;
  if(S.phase==='catch-up'){const u=rr33Ease(S.t/2.8);q.x=pin.x;q.y=lerp(-100-q.i*22,112+(q.i===0?25:q.i<3?0:-25),u);q.rfHeading=-Math.PI/2;q._rr33Frame=56+phaseFrame;}
  else if(S.phase==='spool'||S.phase==='boost'){const u=S.phase==='spool'?0:clamp((S.t-3.35)/.9,0,1);q.x=pin.x;q.y=112+(q.i===0?25:q.i<3?0:-25)-(570+q.i*30)*u*u;q.rfHeading=-Math.PI/2;q._rr33Frame=64+phaseFrame;}
  else if(S.phase==='away'){q.y=-250-q.i*30;q.rfHeading=-Math.PI/2;q._rr33Frame=64+phaseFrame;}
  else if(S.phase==='airshow'){const u=clamp((S.t-4.75-q.i*.16)/3.95,0,1),p=rr33Path(q,u),next=rr33Path(q,Math.min(1,u+.008));q.x=p.x;q.y=p.y;
   const first=u>=.22&&u<.57,second=u>=.63&&u<.94;let f;
   if(first||second){const v=first?(u-.22)/.35:(u-.63)/.31;f=32+Math.min(15,Math.floor(v*16));q.rfHeading=Math.PI/2;q._rr33Depth=Math.sin(v*TAU)*(q.i%2?1:-1);}
   else{const a=u<.02?Math.PI/2:Math.atan2(next.y-p.y,next.x-p.x),nearest=Math.round((a+TAU)%TAU/TAU*32)%32;f=nearest;q.rfHeading=a;q._rr33Depth=0;}
   q._rr33Frame=u>=.98?48+phaseFrame:f;
  }else{q.x=pin.x+Math.sin(S.t*.65)*3;q.y=pin.y+Math.sin(S.t*1.25+q.i*.6)*3;q.rfHeading=Math.PI/2;q._rr33Frame=48+phaseFrame;q._rr33Depth=0;}
 }
}
function rr33Start(b){const R=b._rebels;if(!R.rf)rf28Init(b,R);const S=R.rough33={t:0,phase:'catch-up',scroll:1,resume:0,playerX:player.x,playerY:player.y,events:new Set(),health:R.ships.map(q=>q.hp)};
 R.frIntro={t:0,beat:0,done:false};R.h3Intro=null;R.frRadio=null;h3ClearCombat();if(s6Wing)s6Wing.line=null;h3RebelMusic();rr33Log(S,'catch-up');return S;}
function rr33Phase(S){return S.t<2.8?'catch-up':S.t<3.35?'spool':S.t<4.25?'boost':S.t<4.75?'away':S.t<9.6?'airshow':S.t<11.4?'settle':'dialogue';}
h3RebelLines=function(R){const rows=RR33.base.lines.apply(this,arguments).map(q=>({...q}));if(R.ships.length!==5)return rows;
 const first=rows.find(q=>q.who==='VOSS');if(first)first.text='SO YOU FINALLY CAUGHT UP. THE ROUGH RIDERS ANSWER TO NO ONE. THE DIVISION BETRAYED ALL OF US.';
 for(const row of rows)if(row.demo==='turbo'){delete row.demo;row.text='ROUGH RIDERS. BREAK FORMATION. SHOW FURY WHAT FREEDOM LOOKS LIKE!';}return rows;};
h3RebelTick=function(b,dt){if(!rr33Group(b))return RR33.base.intro.apply(this,arguments);const R=b._rebels,S=R.rough33||rr33Start(b);dt=clamp(dt,0,.05);S.t+=dt;const old=S.phase;S.phase=rr33Phase(S);R.frIntro.t=S.t;b._noHit=true;h3RebelMusic();
 if(S.phase!==old){rr33Log(S,S.phase);if(S.phase==='spool')Snd.play('launch',.7);if(S.phase==='boost'||S.phase==='airshow')Audio.SFX.chargeDash?.();if(S.phase==='settle')Snd.play('impactMetal',.65);}
 S.scroll=S.phase==='settle'?lerp(.9,.055,rr33Ease((S.t-9.6)/1.8)):S.phase==='dialogue'?.055:S.phase==='boost'?1.12:S.phase==='airshow'?.9:1;
 rr33Actors(b,S,dt);
 if(S.phase==='dialogue'){
  if(!R.h3Intro){R.h3Intro={rows:h3RebelLines(R),i:0,t:0,shown:0,age:S.t};rr33Log(S,'bowling-dialogue',{pins:R.ships.map(q=>({key:q.key,x:q.x,y:q.y}))});}
  const I=R.h3Intro;I.t+=dt;I.age=S.t;const line=I.rows[I.i];if(line){const n=Math.min(line.text.length,Math.floor(I.t*32));dialogueLetterTicks?.(line.text,I.shown,n);I.shown=n;if(I.t>line.text.length/32+2.8){I.i++;I.t=0;I.shown=0;R.frIntro.beat=I.i;}}
  if(typeof rs1004DemoTick==='function')rs1004DemoTick(R,I,dt);
  if(I.i>=I.rows.length){R.frIntro.done=true;b._noHit=false;R.t=0;R.releaseAt=1.6;S.phase='combat';S.resume=0;for(const q of R.ships){q.mode='fight';q.t=0;q.cd=1.6+q.i*.4;delete q._rr33Frame;delete q._rr33Depth;}Input.clearTaps?.();rr33Log(S,'native-combat-release');}
 }
 RR33.last={phase:S.phase,t:S.t,scroll:S.scroll,protected:!R.frIntro.done,ships:R.ships.map(q=>({key:q.key,x:q.x,y:q.y,heading:q.rfHeading,frame:q._rr33Frame})),allies:s6Wing?.ships.length||0};
};
fr27RebelDrawShip=function(q){if(rr33Protected()&&boss._rebels.rough33?.phase!=='dialogue'&&q._rr33Frame!=null)return rr33Frame(q,q._rr33Frame);return RR33.base.ship.apply(this,arguments);};
// Draw the crossing pilots in depth order without changing their native slots.
const rr33DrawSquad=rebelSquadDraw;
rebelSquadDraw=function(b){const R=b?._rebels;if(!rr33Protected(b)||R.rough33?.phase==='dialogue')return rr33DrawSquad.apply(this,arguments);
 for(const q of R.ships.slice().sort((a,b)=>(a._rr33Depth||0)-(b._rr33Depth||0)))fr27RebelDrawShip(q);};
rebelSquadHitTest=function(b){return rr33Protected(b)?false:RR33.base.hit.apply(this,arguments);};
rebelSquadDamage=function(b){if(rr33Protected(b))return;return RR33.base.damage.apply(this,arguments);};
retinaBossTargets=function(b){return rr33Protected(b)?[]:RR33.base.targets.apply(this,arguments);};
rebelSquadTick=function(b,dt){const r=RR33.base.tick.apply(this,arguments),S=b?._rebels?.rough33;if(S&&b._rebels.frIntro?.done){S.resume=Math.min(1.6,S.resume+Math.max(0,dt));S.scroll=lerp(.055,1,rr33Ease(S.resume/1.6));}return r;};
function rr33Scroll(){const S=boss?._rebels?.rough33;return state===GS.PLAY&&rr33Group(boss)&&S&&(!boss._rebels.frIntro.done||S.resume<1.6)?S.scroll:1;}
drawLevelMaster=function(dt){return RR33.base.bg.call(this,Math.max(0,dt||0)*rr33Scroll());};
drawClouds=function(dt){return RR33.base.clouds.call(this,Math.max(0,dt||0)*rr33Scroll());};
drawWorld=function(dt){const r=RR33.base.world.apply(this,arguments),S=boss?._rebels?.rough33;if(rr33Protected()&&S&&['settle','dialogue'].includes(S.phase)){ctx.save();worldXformEscape();rr33Text(RR33.name,VW/2,61,'chrome');ctx.restore();}return r;};
globalThis.BOF_ROUGH_RIDERS_1028=RR33;

// Combat airshow: separated curved fan-out, overhead loops, then a south-facing settle.
function rr34Point(q,u){const left=camLeftX(),w=viewW(),home={x:left+(q.i+.5)*w/5,y:PLAY.y+100+(q.i%2)*60},side=q.i<2?-1:q.i>2?1:(q.i%2?1:-1);
 const radius=38+q.i*5,angle=u*TAU,spread=Math.sin(Math.PI*u);
 return{x:home.x+side*radius*spread+Math.sin(angle)*18,y:home.y-115*Math.sin(Math.PI*u)+Math.sin(angle)*22};}
const rr34FleetBase=rd21Fleet;
rd21Fleet=function(b,G,D,dt){const F=D.fleet;if(!F)return;const live=b._rebels.ships.filter(rd21Live);G.releaseAt=G.age+2;
 F.t+=dt;
 if(F.phase==='assemble'){
  const u=clamp(F.t/1.8,0,1),v=u*u*(3-2*u);for(const q of live){const h=rr34Point(q,0);q.x=lerp(q._rd21From.x,h.x,v);q.y=lerp(q._rd21From.y,h.y,v);q.rfHeading=Math.PI/2;q.evadeT=0;}
  if(u===1){F.phase='tell';F.t=0;const targets=ra4Targets();live.forEach((q,i)=>{const target=targets[i%targets.length]||{ref:player};q._rd21Volley={t:0,warm:2.1,locked:true,target,shot:0,_rr34:true,a:Math.PI/2};});Audio.SFX.retinaCharge?.();}
 }else if(F.phase==='tell'||F.phase==='volley'){
  for(const q of live){const A=q._rd21Volley;if(!A)continue;A.t=F.phase==='tell'?F.t:A.warm;A.a=Math.atan2(A.target.ref.y-q.y,A.target.ref.x-q.x);}
  if(F.phase==='tell'&&F.t>=2.1){F.phase='volley';F.t=0;F.salvo=0;}
  if(F.phase==='volley'&&F.t>=F.salvo*.24&&F.salvo<3){for(const q of live){const A=q._rd21Volley;if(!A)continue;ra4Rocket(q,G,A);A.shot++;}F.salvo++;}
  if(F.phase==='volley'&&F.t>1){for(const q of live)q._rd21Volley=null;F.phase='stunt';F.t=0;}
 }else{
  const u=clamp(F.t/3.4,0,1);for(const q of live){const p=rr34Point(q,u),next=rr34Point(q,Math.min(1,u+.003)),a=u>.94?Math.PI/2:Math.atan2(next.y-p.y,next.x-p.x);q.x=p.x;q.y=p.y;q.rfHeading=a;q._rd21Scale=1;q.evadeT=0;
   q._rr34Frame=u>.94?48+Math.floor(F.t*24)%8:Math.round((a+TAU)%TAU/TAU*32)%32;}
  if(u===1){for(const q of live){delete q._rr34Frame;q.rfHeading=Math.PI/2;q.rg4.cd=Math.max(2,q.rg4.cd);}D.fleet=null;D.next=G.age+11;rr26Log('north-south-return');}
 }
};
// Draw all five independently coloured locks at their actual victims, above combat art.
const rr34World=drawWorld;
drawWorld=function(dt){const r=rr34World.apply(this,arguments);if(state!==GS.PLAY||!boss?._rebels)return r;
 ctx.save();const z=viewZoom();if(z!==1){ctx.scale(z,z);ctx.translate(0,VH*(1-z)/z);}if(worldWidth()>viewW())ctx.translate(-camX,0);
 for(const q of boss._rebels.ships){const A=q._rd21Volley;if(rd21Live(q)&&A?._rr34)ra4LockWarning(A,q.key);}ctx.restore();return r;};
const rr34Ship=fr27RebelDrawShip;
fr27RebelDrawShip=function(q){if(q._rr34Frame==null||q.dead)return rr34Ship.apply(this,arguments);
 const a=RR33_ART.banks[RR33_ART.models[q.key]?.bank];if(!a||!XART.rdy(a.key))return rr34Ship.apply(this,arguments);
 const f=q._rr34Frame,im=q.flash>0?xartTint(a.key,'#ffffff',1):XART.get(a.key),mods=fr27RebelModules(q),w=SHIP_DRAW_H*1.5;
 for(const [lo,hi,id] of [[-.5,-.17,'left'],[-.17,.17,null],[.17,.5,'right']]){if(id&&mods.find(m=>m.id===id)?.hp<=0)continue;ctx.save();ctx.beginPath();ctx.rect(q.x+(lo===-.5?-a.cw:lo*w),q.y-a.ch,lo===-.5?a.cw+hi*w:hi===.5?a.cw-lo*w:(hi-lo)*w,a.ch*2);ctx.clip();ctx.drawImage(im,f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,q.x-a.pivot[0],q.y-a.pivot[1],a.cw,a.ch);ctx.restore();}return true;
};
// Prioritise the physical missile locked onto each ally; ordinary bullets are excluded.
const rr34Navigate=s6WingNavigate;
s6WingNavigate=function(q,W,dt){const supply=rr34Navigate.apply(this,arguments);if(supply||q.hp<=0||q.phase!=='fight')return supply;
 const m=eBullets.filter(m=>m._ra4Rocket&&!m.dead&&m.hp>0&&m.lock?.ref===q&&m.y<q.y-24).sort((a,b)=>Math.hypot(a.x-q.x,a.y-q.y)-Math.hypot(b.x-q.x,b.y-q.y))[0];
 if(m){q.target=m;q._rd21Intercept=m;q.gx=clamp(m.x,camLeftX()+34,camRightX()-34);q.fireCd=Math.min(q.fireCd||0,.08);}return supply;
};
