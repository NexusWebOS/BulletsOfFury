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
