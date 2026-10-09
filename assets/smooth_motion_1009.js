"use strict";
/* Timed last words -> portrait to white -> core Retina -> one player missile.
   Only that impact starts the existing acted death and subsequent cutaways. */
const SM10={events:[],clock:0,base:{start:h3EndingStart,tick:h3EndingTick,draw:h3EndingDraw,
 deathTick:hammerBossDeathTick,deathDraw:fb1002HammerDeathDraw,load:stageLoadBegin,begin:beginStage,touch:XART._touch,
 enemy:drawEnemy,play:updatePlay,tank:drawModularTank,get:XART.get,fury:furyShipCanvas},furyCache:{}};
for(const bank of Object.values(SM10_ART))for(const a of bank)XART._src[a.key]=a.path;
function sm10Warm(names){for(const n of names)for(const a of SM10_ART[n]||[])XART.rdy(a.key);}
function sm10Log(event,data={}){SM10.events.push({event,...data});if(SM10.events.length>240)SM10.events.shift();}
function sm10Cell(name,i,x,y,size,flash=0){const a=SM10_ART[name]?.[i];if(!a||!XART.rdy(a.key))return false;
 const im=flash>0?xartTint(a.key,'#ffffff',1):XART.get(a.key);ctx.save();ctx.imageSmoothingEnabled=false;
 const k=size/Math.max(a.w,a.h);ctx.drawImage(im,x-a.pivot[0]*k,y-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();return true;}
function sm10StageBanks(n){return [...Object.keys(SM10_ART).filter(k=>k.startsWith('pilot_')||k.startsWith('furyship')),
 ...({2:['heat_disc','furnace_pod','thermal_jet'],3:['shard_sentry','ice_patrol'],4:['desert_hull','desert_tractor'],
 5:['electric_ring','orbital_frigate','orbital_rammer'],6:['storm_jet'],7:['toxic_pipe','toxic_walker'],8:['alien_fighter','alien_stalker']}[n]||[])];}
stageLoadBegin=function(n,keys){return SM10.base.load.call(this,n,[...(keys||[]),...sm10StageBanks(n).flatMap(name=>(SM10_ART[name]||[]).map(a=>a.key))]);};
beginStage=function(n){const r=SM10.base.begin.apply(this,arguments);SM10.clock=0;SM10.events=[];sm10Warm(sm10StageBanks(n));return r;};
updatePlay=function(dt){const r=SM10.base.play.apply(this,arguments);if(state===GS.PLAY)SM10.clock+=dt;return r;};
function sm10Core(b){return{x:b.x+17,y:b.y-26};} // measured reactor pivot of hammer_death reel
h3EndingStart=function(b){SM10.base.start(b);const e=H3.ending;e.sm10={phase:'words',t:0,line:0,shown:0,portrait:0,window:1};
 delete e.engineDeath;e.phase='lastWords';b.dying=0;sm10Log('hammer-last-words');sm10Warm(['electric_ring']);XART.rdy('fb1002_hammer_portrait');XART.rdy('nbret_'+_pilotKey());};
XART._touch=function(k){if(k!=='sm10_hammer_portrait')return SM10.base.touch.apply(this,arguments);
 if(!XART.rdy('fb1002_hammer_portrait'))return null;const im=XART.get('fb1002_hammer_portrait'),c=document.createElement('canvas');
 c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);
 g.globalCompositeOperation='source-atop';g.fillStyle='rgba(255,255,255,'+(H3.ending?.sm10?.portrait||0)+')';g.fillRect(0,0,c.width,c.height);
 c.complete=true;c.naturalWidth=c.width;c.naturalHeight=c.height;return c;};
const SM10_LAST_WORDS=['This cannot be..','You were a worthy opponent, mortal.'];
function sm10Phase(e,phase){e.sm10.phase=phase;e.sm10.t=0;sm10Log('hammer-'+phase);
 if(phase==='lock')Audio.SFX.retinaCharge?.();if(phase==='missile')Audio.SFX.retinaLockBeep?.();}
h3EndingTick=function(dt){const e=H3.ending,Q=e?.sm10;if(!Q)return SM10.base.tick.apply(this,arguments);
 if(Q.phase==='death')return SM10.base.tick.apply(this,arguments);
 const ready=XART.rdy('fb1002_hammer_portrait')&&furyShipReady();if(!ready)return;
 Q.t+=dt;stageEnding=0;whiteBlast=0;shake=0;_stage5SpaceScroll+=dt*12;efxTick(dt);
 if(Q.phase==='words'){const line=SM10_LAST_WORDS[Q.line],n=Math.min(line.length,Math.floor(Q.t*32));dialogueLetterTicks(line,Q.shown,n);Q.shown=n;
  if(Q.t>=line.length/32+2){if(Q.line===0){Q.line=1;Q.t=0;Q.shown=0;}else sm10Phase(e,'portraitWhite');}}
 else if(Q.phase==='portraitWhite'){Q.portrait=clamp(Q.t/1.1,0,1);if(Q.t>=1.3)sm10Phase(e,'windowOut');}
 else if(Q.phase==='windowOut'){Q.window=1-clamp(Q.t/.7,0,1);if(Q.t>=.7)sm10Phase(e,'lock');}
 else if(Q.phase==='lock'&&Q.t>=.9){const p=spaceShipHardpoints(player.x,Math.min(player.y,VH*.78),SPACE_SHIP_SIZE*1.5).nose;
  Q.from=p;sm10Phase(e,'missile');Audio.SFX.missile?.();}
 else if(Q.phase==='missile'&&Q.t>=.65){const c=sm10Core(e.boss);sm10Log('hammer-core-impact',c);Audio.SFX.expBig?.();
  sm10Phase(e,'death');e.engineDeath=0;e.phase='engineDeath';e.boss.dying=0;shake=12;}
};
function sm10Missile(Q,b){const c=sm10Core(b),u=clamp(Q.t/.65,0,1),x=lerp(Q.from.x,c.x,u),y=lerp(Q.from.y,c.y,u),a=Math.atan2(c.y-Q.from.y,c.x-Q.from.x);
 ctx.save();ctx.translate(x,y);ctx.rotate(a+Math.PI/2);const f=Math.floor(Q.t*16)%4;
 spaceAtlasDraw(ctx,'volley_3_trail_'+f,0,18,20,36,true,null);spaceAtlasDraw(ctx,'volley_3_missile_0',0,0,22,36,true,null);ctx.restore();}
h3EndingDraw=function(){const e=H3.ending,Q=e?.sm10;if(!Q||Q.phase==='death')return SM10.base.draw.apply(this,arguments);
 ctx.save();worldXformEscape();ctx.save();ctx.translate(-camX,0);drawBG(0);bm9Draw('hammer_death',0,e.boss.x+17,e.boss.y-26,.57);
 furyShipDrawFlight(player.x,Math.min(player.y,VH*.78),SPACE_SHIP_SIZE*1.5,_pilotKey(),{key:'base'},Q.t);
 const c=sm10Core(e.boss);if(Q.phase==='lock'||Q.phase==='missile')drawBossRetina(e.boss,c.x,c.y,Q.phase==='lock'?(1-clamp(Q.t/.9,0,1))*TAU:0,1);
 if(Q.phase==='missile')sm10Missile(Q,e.boss);ctx.restore();
 if(['words','portraitWhite','windowOut'].includes(Q.phase)){const line=SM10_LAST_WORDS[Q.line];ctx.globalAlpha=Q.window;
  dlgBox({who:'CHROME HAMMER',portrait:false,portraitKey:'sm10_hammer_portrait',full:line,shown:line.slice(0,Q.shown),forceShown:true,screenSpace:false,fade:1,tint:'#96c8ff',pw:VW*.94,ph:VH*.26,x:VW*.03,y:VH*.67});}
 ctx.restore();};
/* Replace random death pops with individually timed, seated authored blasts.
   Rings shatter into authored electric fragments; sprite cells remain opaque. */
hammerBossDeathTick=function(b,dt){const q=H3.ending?.sm10;if(!fb1002NormalHammer(b)||q?.phase!=='death')return SM10.base.deathTick.apply(this,arguments);
 const h=b._hammer;if(!h.sm10Death){h.sm10Death=true;h.deathEvents1002=['hammer-core'];h.deathFx1002=[];}
 const r=SM10.base.deathTick.apply(this,arguments);h.deathFx1002=[];
 for(let i=0;i<9;i++){const at=.12+i*.46;if(b.dying>=at&&!h.deathEvents1002.includes('sm10-'+i)){
  h.deathEvents1002.push('sm10-'+i);Audio.SFX.shieldBreakCombat?.();sm10Log('hammer-electrical-pop',{i,at});}}
 return r;};
fb1002HammerDeathDraw=function(b){const r=SM10.base.deathDraw.apply(this,arguments);if(!b._hammer?.sm10Death)return r;
 const t=b.dying;for(let i=0;i<9;i++){const age=t-(.12+i*.46);if(age<0||age>=1.0)continue;
  const a=i*2.399,x=b.x+17+Math.cos(a)*(i?72:0),y=b.y-26+Math.sin(a)*(i?90:0),size=100+(i%3)*22;
  fb1002Cell('electrical',Math.min(15,Math.floor(age*16)),x,y,size,size,null,0,1);
  sm10Cell('electric_ring',Math.min(7,Math.floor(age*8)),x,y,size*1.8);}
 return r;};

const SM10_ENEMIES={2:{disc:{bank:'heat_disc',h:77},eye:{bank:'furnace_pod',h:73}},
 3:{s3mine:{bank:'shard_sentry',h:80},s3interceptor:{bank:'ice_patrol',h:88}}};
// Shared hull families use the measured height of the current native plate.
// This table preserves each actor's physics/controller, not just its type name.
for(const a of SM10_TARGETS){SM10_ENEMIES[a.stage]??={};SM10_ENEMIES[a.stage][a.type]=a;}
function sm10EnemyPlate(e,a){const frames=SM10_ART[a.bank];if(!frames)return false;
 const f=Math.floor((e.t||0)*12)%frames.length,A=frames[f];if(!XART.rdy(A.key))return false;
 const dh=a.h||e.h*a.hScale,k=dh/A.inkH,relative=e.h/(a.baseH||e.h);
 ctx.save();ctx.translate(e.x+(a.ox||0)*relative,e.y+(a.oy||0)*relative+(e._volc?volcHover(e):0));
 if(!e._s6storm)ctx.rotate(e.spin||0);
 ctx.imageSmoothingEnabled=false;const im=e.flash>0?xartTint(A.key,'#ffffff',1):(frenzyPlate(e,A.key)||XART.get(A.key));
 ctx.drawImage(im,-A.pivot[0]*k,-A.pivot[1]*k,A.w*k,A.h*k);
 const frac=clamp(e.hp/(e._maxhp||e.maxhp||e.hp||1),0,1),dw=A.inkW*k;
 // Preserve the live encounter's damage tells and release effects. New idle
 // reels do not replace its attack controller or its independently aimed guns.
 if(e._s6storm)drawS6DamageOverlay(e,frac,dw,dh);
 else if(e._s7toxic)drawS7DamageOverlay(e,frac,dw,dh);
 else if(e._s5space)drawSpaceDamage(e,frac,dw,dh,false);
 else if(e._s8mega)drawS8Damage(e,frac,dw,dh);
 ctx.restore();
 e._drawW=A.inkW*k;e._drawH=dh;e._sm10Frame=f;return true;}
drawModularTank=function(e){if(e._modTank!==4||e.dead||e._dyingT!=null)return SM10.base.tank.apply(this,arguments);
 const A=SM10_ART.desert_hull?.[Math.floor((e.t||0)*12)%8],tk='overhaul_tank_4_turret';
 if(!A||!XART.rdy(A.key)||!XART.rdy(tk))return SM10.base.tank.apply(this,arguments);
 const size=e.w*1.05,back=(e._kick||e._recoil||0)*3;
 ctx.save();ctx.imageSmoothingEnabled=false;const flash=e.flash>0;
 ctx.drawImage(flash?xartTint(A.key,'#ffffff',1):(frenzyPlate(e,A.key)||XART.get(A.key)),e.x-size/2,e.y-size/2,size,size);
 ctx.translate(e.x,e.y);ctx.rotate((e._modAngle||Math.PI/2)-Math.PI/2);
 ctx.drawImage(flash?xartTint(tk,'#ffffff',1):XART.get(tk),-size/2,-size/2-back,size,size);ctx.restore();
 e._drawW=e.w;e._drawH=e.h;e._sm10Frame=Math.floor((e.t||0)*12)%8;return true;};
/* Neutral cells have exactly the original native canvas bounds. The existing
   lean/roll frames, physical muzzle/nozzle rigs and pilot colors stay authoritative. */
XART.get=function(k){const m=/^ship_(axel|cole|decker|falva|freezer|juggernaut|lizzie|maverick|yuri)$/.exec(k);
 if(m&&state===GS.PLAY){const a=SM10_ART['pilot_'+m[1]]?.[Math.floor(SM10.clock*12)%8];
  if(a&&XART.rdy(a.key))return SM10.base.get.call(this,a.key);}
 return SM10.base.get.apply(this,arguments);};
furyShipCanvas=function(k,pilot){const f=Math.floor(SM10.clock*12)%8,A=SM10_ART.furyship?.[f],M=SM10_ART.furyship_blue?.[f];
 if(k!=='base'||!A||!M||!XART.rdy(A.key)||!XART.rdy(M.key))return SM10.base.fury.apply(this,arguments);
 const src=XART.get(A.key);if(!pilot||pilot==='axel')return src;
 const ck=f+'|'+pilot;if(SM10.furyCache[ck])return SM10.furyCache[ck];
 const mask=XART.get(M.key),c=document.createElement('canvas');c.width=A.w;c.height=A.h;const g=c.getContext('2d');g.drawImage(src,0,0);
 const m=document.createElement('canvas');m.width=A.w;m.height=A.h;const mg=m.getContext('2d');mg.drawImage(mask,0,0);
 const lum=GRAVITY_PILOT_LUM[pilot]||1;if(lum>1){mg.globalCompositeOperation='lighter';mg.globalAlpha=Math.min(1,lum-1);mg.drawImage(mask,0,0);mg.globalAlpha=1;}
 mg.globalCompositeOperation='multiply';mg.fillStyle=GRAVITY_PILOT_PAL[pilot]||GRAVITY_PILOT_PAL.axel;mg.fillRect(0,0,m.width,m.height);
 mg.globalCompositeOperation='destination-in';mg.drawImage(mask,0,0);g.drawImage(m,0,0);c.complete=true;c.naturalWidth=c.width;c.naturalHeight=c.height;
 return SM10.furyCache[ck]=c;};
/* Route blue and true palette-swapped strike sheets from their actual flight
   direction. A north cell must never be selected by a transient spin/bank. */
function sm10StrikeDraw(e){if(run.stage!==6||e.dead||e._dyingT!=null)return false;
 const A=e._fb2Stealth||e._mission29||e._s6Strike;if(!A||!e._mission29&&!on5Bomber(e))return false;
 const dir=A.direction||(e._dir<0?'west':'east'),size=e._s67Draw||104;
 const role=e._fb2Stealth?.role||(e._mission29?fb2MissionRole(e._mission29):null)||(on5Bomber(e)?(e._side??e._dir??1)>0?'red':'green':null);
 e._sm10Facing=dir;
 if(role){fb2Warm();fb2SheetCell('fb2_stealth_'+role,FB2_DIR_FRAME[dir]??2,e.x-size/2,e.y-size/2,size,e);}
 else{const f=dir==='east'?0:dir==='west'?1:2;ctx.save();ctx.translate(e.x,e.y);if(dir==='north')ctx.rotate(Math.PI);
  missionCell('bluejets',f,-size/2,-size/2,size,size);
  if(e.flash>0)s67CellFlash('bluejets',f,-size/2,-size/2,size,size,e);ctx.restore();}
 e._drawW=e._drawH=size;return true;}
drawEnemy=function(e){if(!e.dead&&e._dyingT==null){const a=SM10_ENEMIES[run.stage]?.[e.type];if(a&&!e._s8Roll&&sm10EnemyPlate(e,a))return;
 if(sm10StrikeDraw(e))return;}return SM10.base.enemy.apply(this,arguments);};
