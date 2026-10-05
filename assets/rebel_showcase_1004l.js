'use strict';
/* Stolen-tech introduction uses private, non-colliding demo objects. The live
   background, ships and authored radio continue; combat controllers resume afterward. */
const RS1004_BASE={lines:h3RebelLines,intro:h3RebelTick,draw:rebelSquadDraw,ship:fr27RebelDrawShip,
 cell:rg4Cell,friendly:rg4Friendly,attack:rg4AttackTick,helix:ra4Helix,formation:rg4Formation,radio:h3Radio};
const RS1004={events:[],draws:{}};
function rs1004Log(event,data={}){RS1004.events.push({event,...data});if(RS1004.events.length>80)RS1004.events.shift();}
rg4Cell=function(row,f,x,y,w,h,alpha=1,color){
 if(row===1||row===2){ctx.save();ctx.globalAlpha*=alpha;const r=cf1004Cell('cloak',f/18,x,y,w,h,CF1004.clock*3.2);ctx.restore();return r;}
 return RS1004_BASE.cell.apply(this,arguments);
};
h3RebelLines=function(R){
 const alive=k=>R.ships.some(q=>q.key===k&&!q.dead),rows=[],who=_pilotKey().toUpperCase();
 if(alive('voss'))rows.push({who:'VOSS',text:'THE DIVISION BETRAYED EVERY ONE OF US. THERE ARE NO ORDERS LEFT WORTH FOLLOWING.'});
 rows.push({who,text:'WE WERE ONE UNIT ONCE. IT DOES NOT HAVE TO BE LIKE THIS. WE CAN STILL STOP THIS.'});
 if(alive('nyx'))rows.push({who:'NYX',text:'THEY BUILT THIS WORLD ON OUR BONES. YOUR CLOAK BELONGS TO US NOW.',demo:'cloak'});
 if(alive('kaia'))rows.push({who:'KAIA',text:'YOU SHOULD HAVE STAYED OUT OF THIS. I WILL NOT MISS A SECOND TIME.'});
 if(alive('jace')){
  rows.push({who:'JACE',text:'RECOGNIZE THIS LITTLE BEAUTY? WE ARE NOT GOING HOME EMPTY-HANDED.',demo:'helix'});
  const friends=[_pilotKey(),...(s6Wing?.ships||[]).filter(q=>q.hp>0).map(q=>q.key)],gasp=friends.includes('decker')?'DECKER':friends.includes('cole')?'COLE':who;
  rows.push({who:gasp,text:'WHAT?! THAT IS OUR HELIX CANNON! THEY STOLE THE FULL PROTOTYPE!',demo:'gasp'});
 }
 if(alive('rook'))rows.push({who:'ROOK',text:'WHAT IS THE MATTER? BIG GUNS SCARE YA WHEN YOU ARE NOT THE ONLY ONE WHO HAS THEM?',demo:'slug'});
 if(alive('voss'))rows.push({who:'VOSS',text:'GET OUT OF OUR WAY, OR BURN WITH IT. TRY KEEPING UP WITH THIS!',demo:'turbo'});
 return rows;
};
function rs1004DemoTick(R,I,dt){
 const S=I.showcase||(I.showcase={fx:[],events:new Set(),slot:-1,current:null});
 for(const f of S.fx){f.t+=dt;f.x+=(f.vx||0)*dt;f.y+=(f.vy||0)*dt;}S.fx=S.fx.filter(f=>f.t<f.life);
 const line=I.rows[I.i];if(!line){for(const q of R.ships){q.frCloak=0;q.rfHeading=null;q._rsMuzzle=0;}S.current=null;return;}
 if(S.slot!==I.i){S.slot=I.i;const q=R.ships.find(q=>q.key===line.who.toLowerCase());S.current={kind:line.demo,q,t:0,released:false,ox:q?.x,oy:q?.y};}
 const D=S.current;if(!D?.kind)return;D.t=Math.max(0,I.t);const q=D.q;
 if(D.kind==='gasp')return;
 if(!q||q.dead)return;const afterText=line.text.length/32+.12;
 if(D.kind==='cloak'){
  q.frCloak=D.t>1.65?10:0;D.cloak=Math.min(1,D.t/1.65);if(!D.released&&D.t>=1.65){D.released=true;av3Sound('teleport_out',.8);rs1004Log('cloakDemo');}
 }
 if(D.kind==='helix'&&!D.released&&D.t>=afterText){D.released=true;
  S.fx.push({kind:'ball',x:q.x,y:q.y+54,vx:-360,vy:-145,t:0,life:1.15,w:104,h:104});
  Audio.SFX.maverickHelixRelease?.();rs1004Log('helixDemo',{diameter:104});
 }
 if(D.kind==='slug'&&D.t>.7&&D.t<afterText+1.2){D.next=(D.next||0)-dt;if(D.next<=0){D.next=.11;const side=(D.shot=(D.shot||0)+1)%2?1:-1;
   // Decorative lanes deliberately travel outward, never through the friendly formation.
   S.fx.push({kind:'slug',x:q.x+side*24,y:q.y+29,vx:side*280,vy:115,t:0,life:.75,w:8,h:22});q._rsMuzzle=.11;
   Audio.SFX.enemyMachineGunHeavy?.();rs1004Log('slugDemo');}}
 if(D.kind==='turbo'){
  const warm=Math.max(1.25,afterText),t=D.t-warm;
  if(t>=0){if(!D.released){D.released=true;D.ox=q.x;D.oy=q.y;Audio.SFX.chargeDash?.();rs1004Log('turboDemo',{speed:1250});}
   if(t<.45){q.rfHeading=-.42;q.x=D.ox+t*1100*Math.cos(-.42);q.y=D.oy+t*1100*Math.sin(-.42);}
   else if(t<1.25){const pass=t-.45;q.rfHeading=0;q.x=camLeftX()-90+pass*1250;q.y=PLAY.y+110;}
   else {const p=clamp((t-1.25)/1.15,0,1);q.rfHeading=Math.PI;q.x=lerp(camRightX()+90,D.ox,p);q.y=lerp(PLAY.y+110,D.oy,p);if(p===1)q.rfHeading=null;}
   S.fx.push({kind:'dash',x:q.x,y:q.y,t:0,life:.16,w:120,h:32,a:q.rfHeading});
  }
 }
 q._rsMuzzle=Math.max(0,(q._rsMuzzle||0)-dt);
}
h3RebelTick=function(b,dt){const r=RS1004_BASE.intro.apply(this,arguments),R=b._rebels,I=R.h3Intro;if(I)rs1004DemoTick(R,I,dt);return r;};
function rs1004Ball(x,y,size,t){return ra4Blit(ra4Palette('nhxsb_g_2'),x,y,size,size,Math.sin(t*13)*.10);}
function rs1004DemoDraw(R){const S=R.h3Intro?.showcase;if(!S)return;const D=S.current,q=D?.q;
 if(q&&D.kind==='helix'&&!D.released){const p=clamp(D.t/(R.h3Intro.rows[R.h3Intro.i].text.length/32),0,1);
  ra4Blit(ra4Palette('fchgc_'+Math.min(3,Math.floor(p*4))),q.x,q.y,104,135);rs1004Ball(q.x,q.y+53,28+p*76,D.t);}
 if(q&&D.kind==='cloak'&&D.t<2.4)cf1004Cell('cloak',D.t*1.35,q.x,q.y,88,118,CF1004.clock*3.2);
 if(q&&D.kind==='slug'){
  const key=CHAINGUN_POD_KEY+(Math.floor(D.t*20)%4),im=XART.rdy(key)?XART.get(key):null;
  if(im)for(const side of [-1,1]){const h=38,w=h*im.width/im.height;ra4Blit(im,q.x+side*23,q.y+20,w,h);if(q._rsMuzzle>0)wm26Draw(ctx,'chaingun',q.x+side*23,q.y+39,Math.PI/2,1-q._rsMuzzle/.11,26);}
 }
 if(q&&D.kind==='turbo'&&!D.released){ra4Reel('dash',Math.floor(D.t*16)%6,q.x,q.y+25,110,38,-Math.PI/2);cf1004Cell('muzzle',D.t,q.x,q.y-12,34,55);}
 for(const f of S.fx){if(f.kind==='ball')rs1004Ball(f.x,f.y,f.w,f.t);
  else if(f.kind==='dash')ra4Reel('dash',Math.floor(f.t*30)%6,f.x,f.y,f.w,f.h,f.a);
  else if(f.kind==='slug')chaingunRoundDraw({x:f.x,y:f.y,vx:f.vx,vy:f.vy,t:f.t,lv:5});
 }
 RS1004.draws.demo=(RS1004.draws.demo||0)+1;
}
rebelSquadDraw=function(b){const r=RS1004_BASE.draw.apply(this,arguments);if(!b._rebels.frIntro?.done)rs1004DemoDraw(b._rebels);return r;};
h3Radio=function(who,text,shown,y){if(!/THAT IS OUR HELIX CANNON/.test(text))return RS1004_BASE.radio.apply(this,arguments);
 dlgBox._tw={key:'h3|'+who+'|'+text,count:shown,at:performance.now(),auto:false};
 const key='port_cf_'+who.toLowerCase()+'_talk-o';XART.rdy(key);const pw=Math.round(VW*.94),ph=Math.max(104,Math.round(VH*.23));
 dlgBox({who,portrait:who.toLowerCase(),portraitKey:XART.rdy(key)?key:undefined,full:text,shown:text.slice(0,shown),forceShown:true,fade:1,
 tint:dialogueNameColor(who,'#cfd6e6'),pw,ph,x:(VW-pw)/2,y:y??VH*.58});
};
/* Jace stole the full-size charged ball, not a small copy of a normal orb. */
ra4Helix=function(q,G,A){RS1004_BASE.helix.apply(this,arguments);const o=G.ord.at(-1);if(o?.kind==='helix'){o.r=38;o._rsFullBall=true;}};
fr27RebelDrawShip=function(q){const r=RS1004_BASE.ship.apply(this,arguments),A=q.rg4?.act;
 if(A?.kind==='helix'&&A.phase==='charge'){const p=clamp(A.t/A.warm,0,1);rs1004Ball(q.x,q.y+52,32+72*p,A.t);}
 if(A?.kind==='cloak'&&A.phase==='charge')cf1004Cell('cloak',A.t*1.5,q.x,q.y,88,118,CF1004.clock*3.2);return r;
};
rg4AttackTick=function(q,R,G,dt){const r=RS1004_BASE.attack.apply(this,arguments),A=q.rg4?.act;if(A?.kind==='cloak'&&A.phase==='charge'&&A.t<A.warm*.7)q.frCloak=0;return r;};
rg4Formation=function(G){const r=RS1004_BASE.formation.apply(this,arguments);for(const [i,m]of G.members.entries())m.pin.y=VH*.64+(i?Math.ceil(i/2)*38:0);return r;};
