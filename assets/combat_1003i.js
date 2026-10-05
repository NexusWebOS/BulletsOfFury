'use strict';
/* Mike's October 3 combat pass. Generated art stays unchanged on disk. Each
   moving Reaver module owns its draw, hardpoint, collision and Retina target. */
const AV3={clock:0,events:[],last:new Map(),seen:new WeakSet(),loops:new Set(),cells:new Map(),draws:{}};
for(const key of ['reaver_parts','laser_beams','laser_muzzles'])XART._src['av3_'+key]='assets/game/combat_1003i/'+key+'.png';
const AV3_CUES=['laser_charge','laser_burn','laser_release','fusion_cannon','cole_laser6','cole_laser7','target_acquire','teleport_out','teleport_in','firewall_launch','firewall_burn','toxic_spit','alien_orb','claw_lunge','impact_metal','impact_energy','impact_flesh','code_shatter','module_break','gravity_pulse'];
function av3Warm(){for(const key of ['reaver_parts','laser_beams','laser_muzzles'])XART.rdy('av3_'+key);}
function av3RegisterAudio(){
 if(typeof Snd==='undefined'||!Snd)return;
 for(const name of AV3_CUES){const key='av3_'+name,uri='assets/game/combat_1003i/'+name+'.mp3';
  BOFA.sfx[key]=uri;const list=[],slots=[];
  for(let i=0;i<3;i++)Object.defineProperty(list,i,{enumerable:true,get(){if(!slots[i])slots[i]={el:new window.Audio(),uri,attached:false,used:0};return Snd._touchVoice(slots[i]);}});
  Snd.pools[key]={list,slots,i:0};Snd.TAME[key]={g:/impact/.test(name)?.60:/burn|cole_laser/.test(name)?.68:.82,native:true,min:/impact/.test(name)?.10:/charge|target/.test(name)?.45:.13};
  Audio.SFX[key]=()=>av3Sound(name);
 }
}
function av3Sound(name,gain=1,gap=.13){
 if(!AV3_CUES.includes(name)||typeof Snd==='undefined'||!Snd)return false;
 const last=AV3.last.get(name);if(last!=null&&AV3.clock-last<gap)return false;
 AV3.last.set(name,AV3.clock);AV3.events.push({cue:name,t:AV3.clock,stage:run.stage});if(AV3.events.length>240)AV3.events.shift();
 return Snd.play('av3_'+name,gain);
}
function av3Loop(name,gain=.75){if(typeof Snd!=='undefined'&&Snd){AV3.loops.add(name);Snd.loopOn('av3_'+name,gain);}}
av3RegisterAudio();
const AV3_ALIASES={bossWeaponCharge:'laser_charge',enemyHeavyLaser:'laser_release',combatBeam0927:'laser_release',fusionBeam:'fusion_cannon',
 furnaceLaserCharge:'laser_charge',warshipCoreCharge:'laser_charge',hammerEradCharge:'laser_charge',quadCharge:'laser_charge',beamCharge:'laser_charge',
 furnaceLaserBurst:'laser_release',hammerEradBlast:'laser_release',quadFire:'laser_release',enemyPulseLaserAlien:'laser_release',
 teleportIn:'teleport_in',teleportOut:'teleport_out',firewallArrive:'firewall_launch',
 enemyToxicSpit:'toxic_spit',combatToxic0927:'toxic_spit',combatOrb0927:'alien_orb',combatModule0927:'module_break'};
for(const [old,cue]of Object.entries(AV3_ALIASES)){
 Audio.SFX[old]=()=>av3Sound(cue);
 // Several encounter directors use Snd.play directly instead of Audio.SFX.
 // Both entry points must resolve to the same generated recording.
 if(typeof Snd!=='undefined'&&Snd){BOFA.sfx[old]=BOFA.sfx['av3_'+cue];Snd.pools[old]=Snd.pools['av3_'+cue];Snd.TAME[old]=Snd.TAME['av3_'+cue];}
}
Audio.SFX.enemyMG=()=>Audio.SFX.enemyMachineGunHeavy();
Audio.SFX.bossRoar=()=>Audio.SFX.mechRoar();
const AV3_REALM_SOUND=r30Sound;
r30Sound=function(k){if(AV3_ALIASES[k])return av3Sound(AV3_ALIASES[k]);if(k==='enemyMG')return Audio.SFX.enemyMG();return AV3_REALM_SOUND.apply(this,arguments);};
function av3Color(name){
 const s=String(name||'ice').toLowerCase();
 if(/fire|flame|magma|inferno|orange/.test(s))return 0;
 if(/toxic|acid|green|venom/.test(s))return 2;
 if(/void|code|purple|violet|alien|shadow/.test(s))return 3;
 if(/red|crimson/.test(s))return 4;
 if(/gold|yellow|electric|lightning|storm/.test(s))return 5;
 if(/^#[a-f0-9]{6}$/.test(s)){const r=parseInt(s.slice(1,3),16),g=parseInt(s.slice(3,5),16),b=parseInt(s.slice(5),16);return r>g*1.35&&r>b*1.4?4:r>180&&g>140&&b<140?5:g>r*1.3&&g>b*1.25?2:r>90&&b>r*.85&&g<r*.8?3:1;}
 return 1;
}
function av3Muzzle(g,x,y,size,color,t=AV3.clock,alpha=1){
 if(!XART.rdy('av3_laser_muzzles'))return false;
 const row=typeof color==='number'?color:av3Color(color),f=Math.floor(t*18)%3,r=AV3_ART.muzzles[row][f];
 g.save();g.imageSmoothingEnabled=false;g.globalAlpha*=alpha;g.globalCompositeOperation='lighter';
 // The authored glow is bounded to its own cell and never paints a rectangle.
 g.beginPath();g.arc(x,y,size*.5,0,TAU);g.clip();g.drawImage(XART.get('av3_laser_muzzles'),...r,x-size*.5,y-size*.5,size,size);g.restore();
 AV3.draws.muzzle=(AV3.draws.muzzle||0)+1;return true;
}
function av3Beam(g,x,y,angle,length,width,color,t=AV3.clock,alpha=1,muzzle=true){
 if(!(length>0&&width>0)||!XART.rdy('av3_laser_beams'))return false;
 const row=typeof color==='number'?color:av3Color(color),r=AV3_ART.beams[row][Math.floor(t*18)%3],im=XART.get('av3_laser_beams');
 g.save();g.translate(x,y);g.rotate(angle);g.imageSmoothingEnabled=false;g.globalAlpha*=alpha;
 // Source strips are horizontal. Tile at their authored aspect; the collider's
 // width covers the bright body, with a small purely visual outer corona.
 const h=width*1.35,step=h*r[2]/r[3];g.beginPath();g.rect(0,-h/2,length,h);g.clip();
 for(let d=0;d<length;d+=step)g.drawImage(im,...r,d,-h/2,step+.5,h);
 g.restore();if(muzzle)av3Muzzle(g,x,y,clamp(width*2.1,22,78),row,t,alpha);
 AV3.draws.beam=(AV3.draws.beam||0)+1;return true;
}

/* Reaver: the original encounter director retains its attacks and timing. */
const AV3_R={init:er26Init,tick:er26Tick,draw:shipBossDraw,mount:shipBossMount,can:mr27CanFire,fire:mr27Fire,
 hit:hitSubBoss,at:subBossHitPart,solid:subBossSolidAt,beamHit:subBossBeamImpact,targets:retinaBossTargets};
function av3Reaver(b){return !!b?._av3Reaver;}
er26Init=function(b){AV3_R.init.apply(this,arguments);if(!b||b._ship!=='magmaward'||!b._er26||b._av3Reaver)return;
 av3Warm();b.w=218;b.h=206;b._er26.home=Math.max(b._er26.home,155);b._er26.to.y=b._er26.home;b._av3Reaver={clock:0,parts:[],debris:[]};
 for(const [id,cell,attach,pivot,w,hp] of [
  ['core',0,[0,0],[.5,.5],83,1],['wingL',1,[-28,-5],[.87,.66],98,.10],['wingR',2,[28,-5],[.13,.66],98,.10],
  ['gunL',3,[-52,0],[.35,.23],44,.14],['gunR',4,[52,0],[.65,.23],44,.14],['nose',5,[0,66],[.5,.5],35,.12]]){
  b._av3Reaver.parts.push({id,cell,attach:attach.map(v=>v*.88),pivot,w:w*.88,hp:Math.ceil(b.maxhp*hp),maxhp:Math.ceil(b.maxhp*hp),flash:0,kick:0,rot:0,dead:false});
 }
};
function av3Part(b,id){return b._av3Reaver.parts.find(p=>p.id===id);}
function av3PartPose(b,p){const r=AV3_ART.parts[p.cell],h=p.w*r[3]/r[2];return{x:b.x+p.attach[0],y:(b._drawY??b.y)+p.attach[1]-p.kick,a:p.rot,w:p.w,h};}
function av3PartPoint(b,p,u=.5,v=.5){const q=av3PartPose(b,p),x=(u-p.pivot[0])*q.w,y=(v-p.pivot[1])*q.h;return{x:q.x+x*Math.cos(q.a)-y*Math.sin(q.a),y:q.y+x*Math.sin(q.a)+y*Math.cos(q.a)};}
function av3Slot(slot){return /^(L|L0|L1|LW|gunL)$/.test(slot)?'gunL':/^(R|R0|R1|RW|gunR)$/.test(slot)?'gunR':'nose';}
shipBossMount=function(b,slot){if(av3Reaver(b)){const p=av3Part(b,av3Slot(slot));return {...av3PartPoint(b,p,.5,.96),_av3Part:p.id};}return AV3_R.mount.apply(this,arguments);};
mr27CanFire=function(b,slot){const id=typeof slot==='string'?av3Slot(slot):slot?._av3Part;return av3Reaver(b)&&id?!av3Part(b,id).dead:AV3_R.can.apply(this,arguments);};
mr27Fire=function(b,slot,a){const id=typeof slot==='string'?av3Slot(slot):slot?._av3Part;if(av3Reaver(b)&&id){const p=av3Part(b,id);p.kick=4;p.rot=clamp(a-Math.PI/2,-.5,.5);return;}return AV3_R.fire.apply(this,arguments);};
er26Tick=function(b,dt){const result=AV3_R.tick.apply(this,arguments);if(av3Reaver(b)){const M=b._av3Reaver;M.clock+=dt;
 for(const p of M.parts){p.flash=Math.max(0,p.flash-dt);p.kick=Math.max(0,p.kick-dt*35);
  if(p.id.startsWith('wing'))p.rot=(p.id==='wingL'?-1:1)*(.025+Math.sin(M.clock*2)*.035);
  if(p.id.startsWith('gun')){const B=b._l23Beam,i=B?.slots.findIndex(s=>av3Slot(s)===p.id)??-1;
   const target=i>=0?B.angles[i]-Math.PI/2:Math.atan2((b._er26.target?.y??player.y)-b.y,(b._er26.target?.x??player.x)-(b.x+p.attach[0]))-Math.PI/2;
   p.rot+=(clamp(target,-.5,.5)-p.rot)*Math.min(1,dt*8);}}
 for(const d of M.debris){d.t+=dt;d.pose.x+=d.vx*dt;d.pose.y+=d.vy*dt;d.pose.a+=d.spin*dt;}M.debris=M.debris.filter(d=>d.t<1.2);
 }return result;};
function av3ReaverAt(b,x,y){if(!av3Reaver(b)||b.enter||b.dead||b._noHit||!Number.isFinite(x+y))return null;
 for(const p of [...b._av3Reaver.parts].reverse()){if(p.dead)continue;const q=av3PartPose(b,p),dx=x-q.x,dy=y-q.y;
  const u=(dx*Math.cos(q.a)+dy*Math.sin(q.a))/q.w+p.pivot[0],v=(-dx*Math.sin(q.a)+dy*Math.cos(q.a))/q.h+p.pivot[1];
  if(u>=0&&u<1&&v>=0&&v<1&&av3PartOpaque(p,u,v))return p.id;}
 return null;
}
subBossHitPart=function(x,y){return av3Reaver(subBoss)?av3ReaverAt(subBoss,x,y):AV3_R.at.apply(this,arguments);};
subBossSolidAt=function(x,y){return av3Reaver(subBoss)?av3ReaverAt(subBoss,x,y)!==null:AV3_R.solid.apply(this,arguments);};
function av3Break(b,p){if(p.dead)return;p.dead=true;p.hp=0;const P=av3PartPose(b,p);b._av3Reaver.debris.push({p,pose:{...P},vx:p.id.endsWith('L')?-100:100,vy:90,spin:p.id.endsWith('L')?-2:2,t:0});
 const B=b._l23Beam;if(B){for(let i=B.slots.length-1;i>=0;i--)if(av3Slot(B.slots[i])===p.id){B.slots.splice(i,1);B.angles.splice(i,1);B.baseAngles.splice(i,1);if(Array.isArray(B.sweepArc))B.sweepArc.splice(i,1);}if(!B.slots.length)b._l23Beam=null;}
 const q=av3PartPoint(b,p);explode(q.x,q.y,54,'orange');av3Sound('module_break');shake=Math.max(shake,5);
}
function av3ReaverHit(b,dmg,x,y,part){if(b.dead||b.enter||b._noHit||!(dmg>0))return;const id=part||(Number.isFinite(x+y)?av3ReaverAt(b,x,y):'core'),p=av3Part(b,id);if(!p||p.dead)return;
 const before=b.hp,flash=b.flash;AV3_R.hit.call(this,dmg,x,y);const dealt=Math.max(0,before-b.hp);b.flash=flash;p.flash=.16;
 if(id!=='core'){p.hp=Math.max(0,p.hp-dealt);if(p.hp<=0)av3Break(b,p);}if(b.dead){b._l23Beam=null;groundTargetingCancel(b);}if(dealt>0)av3Sound('impact_metal',.75,.10);
}
hitSubBoss=function(d,x,y){if(av3Reaver(subBoss))return av3ReaverHit(subBoss,d,x,y);return AV3_R.hit.apply(this,arguments);};
subBossBeamImpact=function(b,beam){if(!av3Reaver(b))return AV3_R.beamHit.apply(this,arguments);const r=playerBeamRange(beam);if(!r)return null;
 for(let y=Math.min(r.bot,b.y+180);y>=Math.max(r.top,b.y-180);y-=2)for(const x of [r.x,r.x-r.half*.7,r.x+r.half*.7]){const key=av3ReaverAt(b,x,y);if(key)return{x,y,entry:y,key};}return null;
};
retinaBossTargets=function(b){if(!av3Reaver(b))return AV3_R.targets.apply(this,arguments);if(b.dead||b.enter||b._noHit)return [];
 return b._av3Reaver.parts.filter(p=>!p.dead).map(p=>{const q=av3PartPose(b,p);return retinaDynamicPiece(b,'reaver-'+p.id,p.id,()=>({...av3PartPoint(b,p),hp:p.id==='core'?b.hp:p.hp,dead:b.dead||p.dead}),d=>{const P=av3PartPoint(b,p);av3ReaverHit(b,d,P.x,P.y,p.id);},q.w*.75,q.h*.80);});
};
function av3PartDraw(b,p,q,alpha=1){const r=AV3_ART.parts[p.cell],im=XART.get('av3_reaver_parts');ctx.save();ctx.translate(q.x,q.y);ctx.rotate(q.a);ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=alpha;
 ctx.drawImage(im,...r,-p.pivot[0]*q.w,-p.pivot[1]*q.h,q.w,q.h);
 if(p.flash>0){const key='av3-part-white-'+p.cell;let white=AV3.cells.get(key);if(!white){white=document.createElement('canvas');white.width=r[2];white.height=r[3];const g=white.getContext('2d');g.drawImage(im,...r,0,0,r[2],r[3]);g.globalCompositeOperation='source-in';g.fillStyle='#fff';g.fillRect(0,0,r[2],r[3]);AV3.cells.set(key,white);}ctx.globalAlpha*=Math.min(.8,p.flash*5);ctx.drawImage(white,-p.pivot[0]*q.w,-p.pivot[1]*q.h,q.w,q.h);}
 ctx.restore();
}
shipBossDraw=function(b){if(!av3Reaver(b)||!XART.rdy('av3_reaver_parts'))return AV3_R.draw.apply(this,arguments);
 if(b._l23Beam)l23BossBeamDraw(b);for(const id of ['wingL','wingR','core','gunL','gunR','nose']){const p=av3Part(b,id);if(!p.dead)av3PartDraw(b,p,av3PartPose(b,p));}
 for(const d of b._av3Reaver.debris)av3PartDraw(b,d.p,d.pose,1-d.t/1.2);
 er26Draw(b);shipBossMuzzleDraw(b);AV3.draws.reaver=(AV3.draws.reaver||0)+1;return true;
};

/* Existing tells and collision remain authoritative. Only live beams change. */
const AV3_L23=l23BossBeamDraw;
l23BossBeamDraw=function(b){const B=b?._l23Beam;if(!B||!B.released||!XART.rdy('av3_laser_beams'))return AV3_L23.apply(this,arguments);
 for(let i=0;i<B.slots.length;i++){if(!mr27CanFire(b,B.slots[i]))continue;const p=shipBossMount(b,B.slots[i]);av3Beam(ctx,p.x,p.y,B.angles[i],Math.max(VW,VH)*1.25,B.width,B.family==='inferno'?'fire':'ice',B.t,Math.min(1,(B.warm+B.active+B.retract-B.t)/Math.max(.01,B.retract)));}return true;
};
const AV3_FZT=fztBeamDraw;
fztBeamDraw=function(q){if(q.kind==='flame'||!av3Beam(ctx,q.x,q.y,q.a+Math.PI/2,q.len,q.width*2,'fire',efxClock,1,true))return AV3_FZT.apply(this,arguments);};
const AV3_S8=s81003BeamsDraw;
s81003BeamsDraw=function(){if(!XART.rdy('av3_laser_beams'))return AV3_S8.apply(this,arguments);for(const q of S81003.beams)av3Beam(ctx,q.x,q.y,Math.atan2(q.ey-q.y,q.ex-q.x),Math.hypot(q.ex-q.x,q.ey-q.y),q.width,q.kind==='code'?'red':'void',q.t,Math.min(1,(q.dur-q.t)/.09));};
const AV3_TEMPEST=tempestJetBeamsDraw;
tempestJetBeamsDraw=function(p){if(!XART.rdy('av3_laser_beams'))return AV3_TEMPEST.apply(this,arguments);for(const q of p._tlv.beams){const end=tempestJetBeamEnd(q);if(q.active)av3Beam(ctx,q.x,q.y,q.ang,end.len,TLV_BEAM_HALF*TLV_S*2,'ice');else{combatWarningDraw(p,{x:q.x,y:q.y,ex:end.x,ey:end.y,progress:q.charge,width:TLV_BEAM_HALF*TLV_S+6,fieldOnly:true});if(q===p._tlv.beams[0])combatWarningDraw(p,{x:q.x,y:q.y,ex:end.x,ey:end.y,progress:q.charge,alertOnly:true});}}};
const AV3_HARRIER=chaosHarrierLaserDraw;
chaosHarrierLaserDraw=function(b){const q=b._chActiveLaser;if(!q)return;const p=chaosHarrierPoint(b,q.slot);if(!av3Beam(ctx,p.x,p.y,q.a,VH+120,q.width,'void'))return AV3_HARRIER.apply(this,arguments);};
const AV3_S9=s9aBeamDraw;
s9aBeamDraw=function(b){const B=b?._s9Beam;if(!B||B.t<(B.charge||S9_BEAM_CHARGE)||B.t>=(B.off||S9_BEAM_OFF)||!XART.rdy('av3_laser_beams'))return AV3_S9.apply(this,arguments);const D=S9_BEAM[b._ship],p=shipBossMount(b,'C');av3Beam(ctx,p.x,p.y,B.ang+Math.PI/2,VH-p.y+120,B.w||D.w,b._ship==='warpsentinel'?'void':'ice',B.t);};
const AV3_ORB=orbBeamsDraw;
orbBeamsDraw=function(){if(!XART.rdy('av3_laser_beams'))return AV3_ORB.apply(this,arguments);for(const b of orbBeams){if(b.t>=b.life+.12)continue;const fade=b.t>b.life?1-(b.t-b.life)/.12:1;av3Beam(ctx,b.x,b.y,Math.PI/2-b.ang,VH*1.2,b.w,b.col,b.t,fade);}};
const AV3_MUZ=wm26Draw;
wm26Draw=function(g,family,x,y,angle,progress,size,color){if(family==='laser'&&av3Muzzle(g,x,y,size||28,color||'ice',progress/18*3))return true;return AV3_MUZ.apply(this,arguments);};
const AV3_ROUND=roundLaserMuzzleDraw;
roundLaserMuzzleDraw=function(g,x,y,d,color,frame){return av3Muzzle(g,x,y,d,color,(frame||0)/18)||AV3_ROUND.apply(this,arguments);};

/* Event-based audio: no render-time playback and no per-bullet sound pileup. */
const AV3_WARNING=combatWarningTick;
combatWarningTick=function(owner,key,t,warm){if(owner){if(!owner._av3Warning)owner._av3Warning=new Map();const old=owner._av3Warning.get(key);if(t<=.08&&(old==null||t<old))av3Sound('target_acquire',.75,.5);if(owner._av3Warning.size>40)owner._av3Warning.clear();owner._av3Warning.set(key,t);}return AV3_WARNING.apply(this,arguments);};
const AV3_CODE_BREAK=cwdShatter,AV3_CODE_HIT=cwdImpact;
cwdShatter=function(){av3Sound('code_shatter');return AV3_CODE_BREAK.apply(this,arguments);};
cwdImpact=function(){av3Sound('impact_energy',.7,.12);return AV3_CODE_HIT.apply(this,arguments);};
const AV3_BEGIN=beginStage,AV3_UPDATE=updatePlay,AV3_STATE=setState;
function av3Stop(){AV3.loops.clear();if(typeof Snd==='undefined'||!Snd)return;for(const c of AV3_CUES){const k='av3_'+c;Snd.loopOff(k);Snd.stopCue(k);const L=Snd.loops?.[k];if(L){L.on=false;L.hold=0;L.lvl=0;L.playing=false;L.el.pause();}}}
beginStage=function(){av3Stop();AV3.seen=new WeakSet();AV3.last.clear();av3Warm();return AV3_BEGIN.apply(this,arguments);};
setState=function(s){if(s!==GS.PLAY)av3Stop();return AV3_STATE.apply(this,arguments);};
function av3ShotCue(q){const kind=String(q.kind||'')+' '+String(q._er26Art||'');if(/laser|beam|lance|rail/i.test(kind))return 'laser_release';if(/toxic|acid|spore|sludge/i.test(kind))return 'toxic_spit';if(/orb|plasma|void|alien|code|skull|spawn/i.test(kind))return 'alien_orb';return null;}
function av3HasBeam(b){return b&&!b.dead&&((b._l23Beam?.released&&b._l23Beam.t<b._l23Beam.warm+b._l23Beam.active)||(b._chActiveLaser)||(b._s9Beam&&b._s9Beam.t>=(b._s9Beam.charge||S9_BEAM_CHARGE)&&b._s9Beam.t<(b._s9Beam.off||S9_BEAM_OFF))||b._jc?.beamActive||b._fz?.beams?.some(q=>q.kind!=='flame')||b._tlv?.beams?.some(q=>q.active)||b._bomber?.mode==='beam');}
function av3AudioTick(dt){AV3.clock+=Math.max(0,dt);AV3.loops.clear();
 if(state!==GS.PLAY)return;
 let living=false;for(const seat of seatList())withSeat(seat,()=>{if(!player.dead){living=true;if(player._av3ColeUntil>AV3.clock&&colePilot()&&run.weapon===0)av3Loop(player._av3ColeTier>=7?'cole_laser7':'cole_laser6',.72);}});
 if(!living||h3Locked())return;
 if(run.stage===2&&wfx?.fseq?.wave&&!bossActive)av3Loop('firewall_burn',.66);
 for(const q of eBullets){if(AV3.seen.has(q))continue;AV3.seen.add(q);if(run.stage>=6||q._boss){const c=av3ShotCue(q);if(c)av3Sound(c,.74,c==='firewall_launch'?.45:.16);}}
 for(const b of [boss,subBoss,...(boss?._tempestDuo?.ships||[]),...(subBoss?._tempestDuo?.ships||[])]){if(!b||b.dead)continue;if(av3HasBeam(b)||[b._whv?.beam,b._whv?.beam2].some(q=>q&&q.t>=q.warn&&q.t<q.warn+q.fire)||b._hammer?.state==='mega_beam'||b._cnBeamFrame!=null||b.beam&&b.beam.t>=b.beam.tel&&b.beam.t<b.beam.tel+b.beam.dur)av3Loop('laser_burn',.68);
  const mode=b._s7mod?.mode||b._r30?.mode||b._chState||b._s7warden?.mode||'';
  if(mode!==b._av3Mode){if(/teleport|warpout|vanish/.test(mode))av3Sound('teleport_out');else if(/warpin|appear|material/.test(mode))av3Sound('teleport_in');else if(/orbit|gravity/.test(mode))av3Sound('gravity_pulse');b._av3Mode=mode;}}
 if(S81003.beams.length||orbBeams.length)av3Loop('laser_burn',.65);
 for(const e of enemies){if(e.dead)continue;const phase=e._mm1003?.phase||e._mutator?.phase||e._s8megaState||'';if(phase!==e._av3Phase){if(phase==='dash')av3Sound('claw_lunge',.85,.23);e._av3Phase=phase;}}
}
updatePlay=function(dt){AV3.clock+=Math.max(0,dt);const r=AV3_UPDATE.apply(this,arguments);av3AudioTick(0);if(typeof Snd!=='undefined'&&Snd)for(const c of ['laser_burn','cole_laser6','cole_laser7','firewall_burn'])if(!AV3.loops.has(c))Snd.loopOff('av3_'+c);return r;};

function av3PartOpaque(p,u,v){
 const key='mask-'+p.cell;let mask=AV3.cells.get(key);const r=AV3_ART.parts[p.cell];
 if(!mask){if(!XART.rdy('av3_reaver_parts'))return u>.2&&u<.8;const c=document.createElement('canvas');c.width=r[2];c.height=r[3];const g=c.getContext('2d',{willReadFrequently:true});g.drawImage(XART.get('av3_reaver_parts'),...r,0,0,r[2],r[3]);mask=g.getImageData(0,0,r[2],r[3]).data;AV3.cells.set(key,mask);}
 return mask[(Math.floor(v*r[3])*r[2]+Math.floor(u*r[2]))*4+3]>90;
}
const AV3_DREAD=drawDreadBeam,AV3_JUNGLE=jungleCruiserDrawUnder,AV3_SIEGE=siegeBomberBeamDraw;
drawDreadBeam=function(b){const B=b?.beam;if(!B||b.dead||B.t<B.tel||B.t>=B.tel+B.dur)return AV3_DREAD.apply(this,arguments);const y=(b._drawY||b.y)+(b._drawH||b.h)*.28;if(!av3Beam(ctx,B.x,y,Math.PI/2,VH-y,52,'fire'))return AV3_DREAD.apply(this,arguments);};
jungleCruiserDrawUnder=function(b){if(!b?._jc?.beamActive||!XART.rdy('av3_laser_beams'))return AV3_JUNGLE.apply(this,arguments);const J=b._jc,frost=b._ship==='frostcruiser';
 if(frost){s3FrostOrbDraw(b);ctx.save();ctx.fillStyle='rgba(1,5,13,.48)';ctx.fillRect(camLeftX()-8,viewTopY()-8,viewW()+16,viewH()+16);ctx.restore();}
 const p=shipBossMount(b,'C');av3Beam(ctx,p.x,p.y,Math.PI/2+(J.beamAng||0),VH*1.55,frost?FROST_BEAM_WIDTH:42,frost?'ice':'toxic',J.t);
};
siegeBomberBeamDraw=function(b){if(b.dead)return;if(b._bomber.mode!=='beam'||!XART.rdy('av3_laser_beams'))return AV3_SIEGE.apply(this,arguments);for(const p of siegeBomberParts(b).filter(p=>p.id.startsWith('laser'))){if(b._bomber.parts.find(q=>q.id===p.id).hp<=0)continue;const y=p.y+p.h*.46;av3Beam(ctx,p.x,y,Math.PI/2,VH-y+25,54,b._bomber.space?'ice':'fire',b._bomber.clock);if(typeof d27MuzzleDraw==='function')d27MuzzleDraw(ctx,'laser',p.x,y,Math.PI/2,(b._bomber.clock*13)%1,38);}};
const AV3_CHROMIUM=hammerChromiumDraw;
hammerChromiumDraw=function(x,y,bottom,width,t,dur){return av3Beam(ctx,x,y,bottom<y?-Math.PI/2:Math.PI/2,Math.abs(bottom-y),hammerChromiumWidth(t,dur,width),'ice',t)||AV3_CHROMIUM.apply(this,arguments);};
const AV3_EYE=fztEyeMuzzleDraw;
fztEyeMuzzleDraw=function(q){if(!av3Muzzle(ctx,q.x,q.y,34*FZT_S,'fire'))return AV3_EYE.apply(this,arguments);};
function av3Bolt(b,color){const a=Math.atan2(b.vy,b.vx),len=b.h||32;return av3Beam(ctx,b.x-Math.cos(a)*len/2,b.y-Math.sin(a)*len/2,a,len,b.w||8,color,b.t||0,1,false);}
const AV3_HAMMER_BOLT=hammerLaserDraw,AV3_FROST_BOLT=frostNoseLaserDraw,AV3_PROJECTILE=drawCombatFinalProjectile;
hammerLaserDraw=function(b){if(!av3Bolt(b,'ice'))return AV3_HAMMER_BOLT.apply(this,arguments);};
frostNoseLaserDraw=function(b){if(!av3Bolt(b,'ice'))return AV3_FROST_BOLT.apply(this,arguments);};
drawCombatFinalProjectile=function(b){if(['s7laser','eglaser','greenlaser'].includes(b?.kind)&&av3Bolt(b,['s7laser','greenlaser'].includes(b.kind)?'toxic':'ice'))return true;return AV3_PROJECTILE.apply(this,arguments);};

// Cole's VI/VII sound follows actual volley creation, including co-op and short
// taps. It cannot keep playing merely because an old projectile is still alive.
const AV3_TRI=coleTrident,AV3_MG=Audio.SFX.machineGun,AV3_FUSE=coleFuseRelease;
coleTrident=function(lv){const r=AV3_TRI.apply(this,arguments);player._av3ColeUntil=AV3.clock+.16;player._av3ColeTier=lv;av3Loop(lv>=7?'cole_laser7':'cole_laser6',.72);return r;};
Audio.SFX.machineGun=function(){if(colePilot()&&run.weapon===0&&run.wlevel>=6)return;return AV3_MG?.apply(this,arguments);};
coleFuseRelease=function(){const old=Audio.SFX.lzStack;Audio.SFX.lzStack=()=>av3Sound('fusion_cannon',1,.25);try{return AV3_FUSE.apply(this,arguments);}finally{Audio.SFX.lzStack=old;}};
const AV3_HIT_ENEMY=hitEnemy,AV3_HIT_BOSS=hitBoss,AV3_PART_HIT=mm1003PartHit;
function av3Impact(e){return e?._mutator1003||e?._r30?'impact_flesh':e?._s7mod||e?._hd1003?'impact_energy':'impact_metal';}
hitEnemy=function(e){const hp=e?.hp,r=AV3_HIT_ENEMY.apply(this,arguments);if(run.stage>=6&&run.stage<=8&&e?.hp<hp)av3Sound(av3Impact(e),.62,.12);return r;};
hitBoss=function(){const b=boss,hp=b?.hp,r=AV3_HIT_BOSS.apply(this,arguments);if(b?.hp<hp)av3Sound(av3Impact(b),.7,.12);return r;};
const AV3_HIT_MINI=hitSubBoss;
hitSubBoss=function(){const b=subBoss,hp=b?.hp,r=AV3_HIT_MINI.apply(this,arguments);if(b?.hp<hp&&!av3Reaver(b))av3Sound(av3Impact(b),.7,.12);return r;};
mm1003PartHit=function(e,p){const alive=!p.dead,r=AV3_PART_HIT.apply(this,arguments);if(r)av3Sound('impact_metal',.65,.12);if(alive&&p.dead)av3Sound('module_break',.8,.18);return r;};
const AV3_KNIGHT=s81003KnightEnter,AV3_ATTACK=r30AttackTick;
s81003KnightEnter=function(b,phase){
 const sound=r30Sound;r30Sound=function(k){if(k==='teleportIn'&&phase==='out')return av3Sound('teleport_out');if(k==='combatModule0927'&&['slash','sweep'].includes(phase))return av3Sound('claw_lunge',.8);return sound.apply(this,arguments);};
 try{return AV3_KNIGHT.apply(this,arguments);}finally{r30Sound=sound;}
};
// The cruiser used the player's sustained-laser bus. Give it its own bed;
// its shared active-beam scan refreshes and releases that bed every tick.
jungleCruiserBeamAudio=function(b,on){const J=b?._jc;if(!J)return;if(on&&!J.beamSound){J.beamSound=true;av3Sound('laser_release',.85);}else if(!on)J.beamSound=false;};
const AV3_STORM_TICK=s6StormTick;
s6StormTick=function(e,dt){const phase=e._phase,act=e._s6Act,fired=act?.fired,r=AV3_STORM_TICK.apply(this,arguments);if(e._s6storm==='s6turbine'&&act&&!fired&&act.fired)av3Sound('gravity_pulse',.68,.4);if(e._s6storm==='s6cyclone'&&e._phase==='charge'&&phase!=='charge')Audio.SFX.jetDash?.();return r;};
r30AttackTick=function(b,dt){const P=b?._r30?.attack,started=P?.started,r=AV3_ATTACK.apply(this,arguments);if(P&&!started&&P.started&&['gravity','turbines','orbit','iceOrbit'].includes(P.type))av3Sound('gravity_pulse',.9,.6);return r;};
av3Warm();

// Warhive's deployed nozzle uses its own flared collision envelope. Preserve
// that taper and its opening/closing timing around the shared generated beam.
const AV3_WHV=whvDrawShots;
whvDrawShots=function(b){
 if(!XART.rdy('av3_laser_beams'))return AV3_WHV.apply(this,arguments);
 const W=b._whv,beams=[W.beam,W.beam2];W.beam=W.beam2=null;
 try{AV3_WHV.apply(this,arguments);}finally{W.beam=beams[0];W.beam2=beams[1];}
 for(const B of beams){if(!B||W.parts[B.side].dead)continue;const G=s67WhvBeamShape(b,B);
  if(B.t<B.warn){combatWarningDraw(b,{x:G.x,y:G.y,ex:G.x,ey:G.bottom,progress:B.t/B.warn,width:B.w});continue;}
  if(!G.open)continue;ctx.save();ctx.beginPath();
  for(let y=0;y<=G.flare;y+=2){const x=G.x-s67WhvBeamHalf(G,G.y+y)*1.35;y?ctx.lineTo(x,G.y+y):ctx.moveTo(x,G.y+y);}
  ctx.lineTo(G.x-G.w*.675,G.bottom);ctx.lineTo(G.x+G.w*.675,G.bottom);
  for(let y=G.flare;y>=0;y-=2)ctx.lineTo(G.x+s67WhvBeamHalf(G,G.y+y)*1.35,G.y+y);
  ctx.closePath();ctx.clip();av3Beam(ctx,G.x,G.y,Math.PI/2,G.bottom-G.y,G.w,'ice',b.t||0,1,false);ctx.restore();av3Muzzle(ctx,G.x,G.y,Math.max(22,G.w*1.7),'ice',b.t||0);
 }
};
