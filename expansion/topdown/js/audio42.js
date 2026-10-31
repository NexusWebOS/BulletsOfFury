/* Overdrive sound ownership, semantic cues and vehicle/flame loop lifetime. */
(function(root){'use strict';const TD=root.TD,A=TD.Audio,D=TD.Depth35,P=root.TD_COLESFX75;if(!P)return;
 const gains={truckEngine:.16,mustangEngine:.12,turretServo:.16,flameLoop:.27};
 for(const [key,v]of Object.entries(P.cues))A.sounds['od75_'+key]={file:'expansion/topdown/audio/colesfx75/'+v.file,gain:gains[key]??v.gain,min:v.min,loop:v.loop};
 const aliases={gd_soldierRifle:'rifle',gd_footstepA:'footstepA',gd_footstepB:'footstepB',gd_coverEnter:'coverEnter',gd_ammoPickup:'ammoPickup',gd_mineArm:'mineArm',gd_doorOpen:'doorUnlock',gd_wallBreak:'wallBreach',gd_crateBreak:'crateBreak',impactMetal:'metalHit',missileLaunch:'rocketLaunch',rankStamp:'rankStamp'};
 for(const [key,v]of Object.entries(aliases))A.aliases[key]='od75_'+v;
 const guns={rifle:'rifle',heavy:'minigunShot',laser:'sniper',rocket:'rocketLaunch',shotgun:'shotgun',double:'shotgun',roller:'plasma',flame:'flameIgnite',flyer:'plasma',bat:'plasma'};
 for(const [kind,cue]of Object.entries(guns))D.profiles[kind].cue='od75_'+cue;
 D.profiles.flame.cue='od75_flameLoop';TD.FOOT_GUNS.flamethrower.cue='od75_flameLoop';TD.FOOT_GUNS.cryo_lance.cue='od75_cryoLaunch';
 const actor=A.actor;A.actor=function(p,gain,player){const G=TD.game,c=G?.mission===6?G.night39:null;
  if(player&&c&&['pursuit','ram','impact'].includes(c.phase)){
   this.loop('od75_truckEngine','night42-truck',this.engineVol*(c.phase==='ram'?1.2:.8),c.phase==='ram'?1.15:1+Math.sin(c.combat*.6)*.035);
   this.loop('od75_mustangEngine','night42-car',this.engineVol*.7,1.05);
   const a=TD.NightRun39.gun(c).angle;if(c.audioAim42!=null&&Math.abs(a-c.audioAim42)>.003)this.loop('od75_turretServo','night42-servo',.6);c.audioAim42=a;
  }else actor.call(this,p,gain,player);
  if(!player)return;
  const flaming=p.firing>0&&(p.weapons?.[p.wi]?.id==='flamethrower'||p.groundGun==='flamethrower');if(flaming){if(!p.audioFlame42)this.play('od75_flameIgnite',.6);this.loop('od75_flameLoop','player42-flame',.55);}else if(p.audioFlame42)this.play('od75_flameEnd',.5);p.audioFlame42=flaming;
  for(const u of G.units||[]){if(u.dead)continue;const kind=u.kind35||u.kind,phase=u.action35,changed=u.audioPhase42!==phase;
   if(changed){if(kind==='flame'&&u.audioPhase42==='fire_forward')this.play('od75_flameEnd',.5);u.audioPhase42=phase;u.reloadCue42=0;if(kind==='flame'&&phase==='fire_forward')this.play('od75_flameIgnite',.6);if(phase==='spin_up')this.play('od75_minigunSpinUp',.6);if(phase==='spin_down')this.play('od75_minigunSpinDown',.6);if(phase==='reload_pump')this.play('od75_shotgunPump',.65);if(phase==='reload_break_action')this.play('od75_breakOpen',.6);}
   if(kind==='flame'&&u.firing>0)this.loop('od75_flameLoop',u,.55);
   if(phase==='reload_break_action'){const age=u.actionT35||0;if(age>.3&&u.reloadCue42<1){this.play('od75_shellInsert',.6);u.reloadCue42=1;}if(age>.7&&u.reloadCue42<2){this.play('od75_breakClose',.6);u.reloadCue42=2;}}
  }
 };
})(window);
