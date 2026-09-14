"""Apply only named, checked replacements to the preserved 0913 runtime. No atlas rewrites."""
import hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
path=ROOT/'assets/game.js';s=(ROOT/'_shots/stage_1_5_0914/game.before.js').read_bytes().decode('utf-8')
def replace(a,b):
    global s
    n=s.count(a)
    if n!=1:raise ValueError('Expected one match, got %d: %s'%(n,a[:90]))
    s=s.replace(a,b,1)
def fn(name,body):
    global s
    a=s.index('\nfunction '+name+'(')+1;b=s.index('\n}',a)+2;s=s[:a]+body.strip()+s[b:]
replace('function nefArtFor(e){',(HERE/'runtime.js').read_text(encoding='utf-8')+'\nfunction nefArtFor(e){')
replace("function explode(x,y,size,palette='red',kind=null,fam=null,_cls=null,_hold=null){","function explode(x,y,size,palette='red',kind=null,fam=null,_cls=null,_hold=null,_quiet=false){")
replace('  if(size>40) Audio.SFX.expBig(); else Audio.SFX.expSmall();','  if(!_quiet){if(size>40) Audio.SFX.expBig(); else Audio.SFX.expSmall();}')
replace("  const state = navy?'intact':", "  const state = (navy||/^nef_s1_/.test(base))?'intact':")
replace('  if(e._nef) return;','  if(e._nef){stage1BurnDraw(e);return;}')
replace('  b.name=\'RAZORBACK\'; b.mini=true; b._rzb=null;',"  stageRevisionWarm('razorback');\n  b.name='RAZORBACK'; b.mini=true; b._rzb=null;")
# Razorback uses its own volley cues; do not double the generic eMG audio per barrel.
replace("if(typeof eMG==='function') eMG(mz.x,mz.y,rzbGameAng(a+Math.sin(beat*1.9)*0.07),rzbPxFrame(380));", "eShootT(mz.x,mz.y,eAimDown(rzbGameAng(a+Math.sin(beat*1.9)*0.07)),rzbPxFrame(380),'mg',{w:4,h:14,silent:true});")
replace('        R.guns[k].flash=0.08;','        R.guns[k].flash=0.08;stageRevisionCue(b,\'razorbackGun\',.12);')
# Limit replacements to the Razorback encounter body.
a=s.index('\nfunction razorbackInit(');b=s.index('\nfunction rzbSprite(',a);r=s[a:b]
r=r.replace("rzbSfx('coleSonicBoom')","stageRevisionCue(b,'razorbackPressure',.12)").replace("rzbSfx('sonicChargeStart')","stageRevisionCue(b,'razorbackCharge',.16)").replace("rzbSfx('missile')","stageRevisionCue(b,'razorbackRocket',.10)").replace("rzbSfx('furnacePowerSurge')","stageRevisionCue(b,'razorbackRam',.12)")
s=s[:a]+r+s[b:]
replace('    R.charge=Math.min(1,cycle/1.2);', "    R.charge=Math.min(1,cycle/1.2);\n    const audioBeat=R.pid+':'+beat;\n    if(cycle<1.2&&R._sonicAudioBeat!==audioBeat){R._sonicAudioBeat=audioBeat;stageRevisionCue(b,'razorbackCharge',.16);}")
replace("        if(beat>=0 && t<2.5) stageRevisionCue(b,'razorbackCharge',.16);",'        // Charge report belongs to the windup above; release has its own cue.')
replace('function updateOverlordX(b, dt){',"function updateOverlordX(b, dt){\n  if(!b._stageAudioWarm){stageRevisionWarm('damkeeper');b._stageAudioWarm=true;}\n  if(!b.dead)weaponFeedbackLoop('overlordRotor',.32);")
a=s.index('\nfunction ovTwinMG(');b=s.index('\nfunction updateOverlordX(',a);r=s[a:b]
old="  if(Audio.SFX.enemyMachineGunBurst) Audio.SFX.enemyMachineGunBurst(); else if(Audio.SFX.enemyMachineGunHeavy) Audio.SFX.enemyMachineGunHeavy(); else if(Audio.SFX.enemyShoot) Audio.SFX.enemyShoot();"
assert old in r;r=r.replace(old,"  stageRevisionCue(b,'overlordGun',.085);")
r=r.replace("if(Audio.SFX&&(Audio.SFX.missile||Audio.SFX.enemyBossCannon))(Audio.SFX.missile||Audio.SFX.enemyBossCannon)();","stageRevisionCue(b,'overlordRocket',.10);")
r=r.replace('function ovGreenVolley(b){',"function ovGreenVolley(b){\n  stageRevisionCue(b,'overlordLance',.10);").replace("silent:i>0,impact:'green'","silent:true,impact:'green'")
r=r.replace('function ovRotorTempest(b){',"function ovRotorTempest(b){\n  stageRevisionCue(b,'overlordWind',.20);")
r=r.replace('  if(Audio.SFX.bossPhase) Audio.SFX.bossPhase();',"  stageRevisionCue(b,'overlordCharge',.20);")
s=s[:a]+r+s[b:]
# The volcanic projectile sheet's four columns are different growth poses. Freeze a flight cell.
replace('  const fi=((b.t||0)*14|0)%4,mul=b.szMul||1,a=Math.atan2(b.vy||1,b.vx||0);', '  const fixed=stage2FlightFrame(b.kind),fi=fixed==null?((b.t||0)*14|0)%4:fixed,mul=b.szMul||1,a=Math.atan2(b.vy||1,b.vx||0);')
replace('  return combatAtlasDraw(S[0],4,S[1],S[2]*4+fi,b.x,b.y,S[4]*mul,S[4]*mul,{angle:angle});', "  const drawn=combatAtlasDraw(S[0],4,S[1],S[2]*4+fi,b.x,b.y,S[4]*mul,S[4]*mul,{angle:angle});\n  if(drawn&&fixed!=null){\n    /* A moving pixel light band animates only existing art; flight silhouette never swaps. */\n    ctx.save();ctx.translate(b.x,b.y);ctx.rotate(angle);ctx.beginPath();const size=S[4]*mul;ctx.rect(-size/2,-size/2+((b.t||0)*75%size),size,6);ctx.clip();\n    combatAtlasDraw(S[0],4,S[1],S[2]*4+fi,0,0,size,size,{blend:'lighter',alpha:.35});ctx.restore();\n  }\n  return drawn;")
replace('  const fi=b._s3StaticSpin?0:(Math.floor((b.t||0)*16)%8);', "  const fi=(b._s3StaticSpin||/^inferno_/.test(b._l23fx))?0:(Math.floor((b.t||0)*16)%8);")
# Store exact retired boat events without deleting any registered boat art/controller.
a=s.index('  if(stageNum===3){',s.index('\nfunction buildStagePlan('));b=s.index('  if(stageNum===4){',a);r=s[a:b]
import re,json
events=re.findall(r"    add\([^\n]*, ?\(\)=> encounterRipple\(\[\n      \{type:'s3barge'[^\n]*\n    \],\.[0-9]+\)\);",r)
assert len(events)==4, len(events)
for event in events:r=r.replace(event,'    // 0914: cryo-barge event stored in docs/STAGE3_STORED_BOATS_0914.json.')
r=r.replace("{type:'s3barge',fx:.24,scale:.72,opt:{inPlace:1}},",'').replace(",{type:'s3barge',fx:.76,scale:.72,opt:{inPlace:1}}",'')
assert "type:'s3barge'" not in r
stored_boats=json.dumps({'reason':'Mike 0914: remove boats from stage 3, store them for now','type':'s3barge','originalEvents':events,'finalWaveBoats':[{'fx':.24,'scale':.72,'opt':{'inPlace':1}},{'fx':.76,'scale':.72,'opt':{'inPlace':1}}],'artAndController':'Preserved in NEF_S3, S3ICE and XART; no assets removed.'},indent=2)
s=s[:a]+r+s[b:]
# Ordinary ice drones previously fell back to a tiny anonymous eshot.
replace("_noArsenal:_iceMini||_s4Mini});", "_noArsenal:_iceMini||_s4Mini,\n      _s3DroneShot:!!(run.stage===3&&e._dr&&['cryoeye','sharddart','glaciercarrier'].includes(e._dr.slug))});")
replace("    if(b._rzb&&typeof razorbackProjectileDraw==='function'&&razorbackProjectileDraw(b))continue;", "    if(stage3DroneShotDraw(b))continue;\n    if(b._rzb&&typeof razorbackProjectileDraw==='function'&&razorbackProjectileDraw(b))continue;")
replace('function stage3BossAttack(b,pat,step,ph,cdMul){', 'function stage3BossAttack(b,pat,step,ph,cdMul){\n  if(stage3WallLaserAttack(b,pat,step))return true;')
# Machine-gun hardware and three distinct attacks for the Warden.
fn('stage4WarfareMiniTick','function stage4WarfareMiniTick(b,dt){return stage4MiniDirector(b,dt);}')
replace("  const mini=b._ship==='olivewarden';", "  const mini=b._ship==='olivewarden';stageRevisionWarm(b._ship);\n  if(!mini){b.w=264;b.h=264;}")
replace("  if(XART.rdy(bk)){\n    const im=XART.get(bk),bh=S.mini?48:40", "  if(!S.mini&&XART.rdy(bk)){\n    const im=XART.get(bk),bh=S.mini?48:40")
replace("mounts:{L:[-0.28,0.18],C:[0,0.43],R:[0.28,0.18],MG_L:[-0.19,0.31],MG_R:[0.19,0.31]}", "mounts:{L:[-0.28,0.18],C:[0,0.43],R:[0.28,0.18],CL:[-.036,.430],CR:[.036,.430],MG_L:[-0.19,0.31],MG_R:[0.19,0.31]}")
replace("  const kind=role==='mg'?'s4brass':", "  const kind=role==='rocket'?'s4rocket':role==='mg'?'s4brass':")
replace("const p=shipBossMount(b,slot),pre='s4w_muzzle_'+(fam||'mg');", "const p=shipBossMount(b,slot),pre=fam==='rocket'?'bpfx_muzzle_missile':'s4w_muzzle_'+(fam||'mg');")
replace("  const role=b._s4wKind,t=b.t||0;", "  const role=b._s4wKind,t=b.t||0;\n  if(role==='machine')return drawMfx('mgcf_1_5',b.x,b.y,Math.atan2(b.vy,b.vx)-Math.PI/2,20,null,1,'#ffd36b');\n  if(role==='rocket')return drawMfx('bpfx_proj_missile_0',b.x,b.y,Math.atan2(b.vy,b.vx)-Math.PI/2,42,null,1,null);")
# Separate helper lanes outside the visual shield, directly above the generator columns.
replace('const S4H_SCALE=1.5, S4H_SIZE=', 'const S4H_SCALE=.40, S4H_SIZE=')
fn('stage4CoreTurretTarget',"function stage4CoreTurretTarget(b,side){const p=stage4GeneratorColumn(b,side);return {x:p.x,y:clamp(p.y-123,80,108)};}")
replace('const tx=clamp(b.x+n.side*xoff,46,W-46),ty=clamp(b.y+n.row*yoff,58,VH-82);', 'const p=stage4GeneratorColumn(b,n.side),tx=p.x,ty=clamp(p.y+n.row*yoff,58,VH-82);')
replace("        const _s4t=(typeof stage4CoreTurretBeamAt==='function')?stage4CoreTurretBeamAt(boss,b.x,b.w/2,b.top,b.bot):null;\n        const _s4n=(typeof stage4ShieldBeamNode==='function')?stage4ShieldBeamNode(boss,b.x,b.w/2,b.top,b.bot):null;\n        if(b._bt<=0&&_s4t){boss._s4CoreHit=_s4t;_lastHitX=_s4t.x;_lastHitY=_s4t.y;hitBoss(b.dmg);weaponHitSfx('laser');b._bt=.05;}\n        else if(b._bt<=0&&_s4n){boss._s4ShieldHit=_s4n;_lastHitX=_s4n.x;_lastHitY=_s4n.y;hitBoss(b.dmg);weaponHitSfx('laser');b._bt=.05;}", "        if(b._bt<=0&&stage4PiercingBeam(boss,b)){b._bt=.05;}")
replace('  const sy=S.homeY,margin=Math.max(154,b.w*.54),amp=Math.max(34,W*.5-margin);', '  if(S.ram&&stage4RamTick(b,dt))return true;\n  const mid=(camLeftX()+camRightX())*.5,sy=S.homeY,margin=Math.max(154,b.w*.54),amp=S.shield.active?2:12;')
# The authored bubble, whole carrier, generators and helpers must fit the visible 480px camera.
a=s.index('\nfunction stage4WarfareBossTick(');b=s.index('\n}',a)+2;r=s[a:b];r=r.replace('W*.5','mid');s=s[:a]+r+s[b:]
replace("sz=72*(.35+.65*mat)","sz=54*(.35+.65*mat)")
replace('hr=clamp(t.hp/Math.max(1,t.maxhp),0,1),bw=62,bh=4','hr=clamp(t.hp/Math.max(1,t.maxhp),0,1),bw=48,bh=4')
# Dense piercing contacts retain their authored VFX without multiplying full explosions in audio.
replace("n.flash=.16;explode(x==null?n.x:x,y==null?n.y:y,8,'blue');","n.flash=.16;stage4ContactFeedback(b,x==null?n.x:x,y==null?n.y:y,8,'blue');")
replace("  explode(t.x,t.y,9,'blue');","  stage4ContactFeedback(b,t.x,t.y,9,'blue');")
replace('function stage4WarfareSound(primary,fallback){',"function stage4WarfareSound(primary,fallback){\n  const own={enemyLightningChaingun:'sovereignHelperGun',bossShieldStatic:'sovereignHeat',bossWeaponCharge:'sovereignWindup',enemyHeavyLaser:'sovereignLaser'}[primary];\n  if(own){\n    const T=boss&&boss._s4war?boss:subBoss&&subBoss._s4war?subBoss:null;\n    if(T){stageRevisionCue(T,own,.09);return;}\n  }")
replace("n.dead=true;n.hp=0;n.flash=.3;explode(n.x,n.y,54,'blue');","n.dead=true;n.hp=0;n.flash=.3;explode(n.x,n.y,54,'blue',null,null,null,null,true);stageRevisionCue(b,'sovereignBreak',.12);")
replace("    explode(b.x,b.y,96,'blue');stage4WarfareSound('bossPhase','enemyHeavyLaser');","    explode(b.x,b.y,96,'blue',null,null,null,null,true);stageRevisionCue(b,'sovereignBreak',.12);stage4WarfareSound('bossPhase','enemyHeavyLaser');")
replace("t.hp=0;t.dead=true;explode(t.x,t.y,76,'blue');","t.hp=0;t.dead=true;explode(t.x,t.y,76,'blue',null,null,null,null,true);stageRevisionCue(b,'sovereignBreak',.12);")
a=s.index("        if(pb.kind==='beam'){ if(Math.abs(pb.x-b.x)");b=s.index('\n',a);r=s[a:b];assert r.count("else explode(b.x,b.y,7,'red');")==1;r=r.replace("else explode(b.x,b.y,7,'red');","else if(run.stage===4&&(boss&&boss._s4war||subBoss&&subBoss._s4war))stage4InterceptFeedback(b);else explode(b.x,b.y,7,'red');");s=s[:a]+r+s[b:]
replace("if(S.t>=4.25)stage4WarfareSetMode(b,'flyaway');", "if(S.t>=4.25&&!stage4RamStart(b))stage4WarfareSetMode(b,'flyaway');")
replace('  const D=SHIPBOSS[b&&b._ship]; if(!D) return false;', '  const D=SHIPBOSS[b&&b._ship]; if(!D) return false;\n  if(b._s4Airborne){stage4WarfareDrawOver(b);return true;}')
replace("  const fi=Math.floor((b.t||0)*22)%8,bk='s4w_drone_barrel_'+fi;", "  stage4RamShadowDraw(b);\n  const fi=Math.floor((b.t||0)*22)%8,bk='s4w_drone_barrel_'+fi;")
replace("  if(run.stage===5 && typeof s5RunForegroundDraw==='function') s5RunForegroundDraw();", "  stage4OverflightDraw();\n  if(run.stage===5 && typeof s5RunForegroundDraw==='function') s5RunForegroundDraw();")
replace('  H.rearming=true;H.rearmT=0;H.cycle++;', '  if(S.ram)stage4RamEnd(b);\n  H.rearming=true;H.rearmT=0;H.cycle++;')
replace("    if(boss._s4CoreHit)return true;\n  }", "    if(boss._s4CoreHit)return true;\n    if(boss._noHit)return false;\n  }")
replace("  if(!boss||boss.dead) return;\n  markHit(boss);", "  if(!boss||boss.dead) return;\n  if(boss._s4war&&boss._noHit&&!boss._s4CoreHit)return;\n  markHit(boss);")
# Space retains its authored missile style with immediate independent passive homing rounds.
fn('spaceVolleyFire', 'function spaceVolleyFire(levelOverride){spaceVolleyLaunchRack(levelOverride==null?spaceVolleyLevel():levelOverride);}')
replace('  return [right,center,left];', '  return [left,center,right];')
replace('  /* The left launcher takes the right-side lock and the right launcher takes the left-side lock.\n     Their independent entities therefore cross for a reason instead of being one fanned image. */', '  /* Each launcher retains the corresponding left, center or right target as an independent\n     passive homing missile, using the authored space-volley style. */')
replace('    /* Split outward first, then cross the centreline. Homing begins after that readable X beat;\n       each missile keeps its own lock until the target dies or exits the finite forward column. */', '    /* A short launch fan precedes normal homing. Each missile keeps its own lock until\n       the target dies or exits the finite forward column. */')
a=s.index("    if(b.side&&b.t>0.09&&b.t<0.34){",s.index('\nfunction spaceBulletTick('));b=s.index('    b._trailFx=',a)
s=s[:a]+"    if(tgt&&b.t>=.12){\n      const want=Math.atan2(spaceTargetY(tgt)-b.y,tgt.x-b.x),da=Math.atan2(Math.sin(want-ang),Math.cos(want-ang));\n      ang+=clamp(da,-(3.2+b.lv*.42)*dt,(3.2+b.lv*.42)*dt);\n    }\n    /* Forward passive missiles never U-turn or orbit a dead lock. Retain the space triple fan. */\n    ang=clamp(ang,-Math.PI+.12,-.12);\n    b.ang=ang;b.vx=Math.cos(ang)*b.spd;b.vy=Math.sin(ang)*b.spd;b.x+=b.vx*dt*60;b.y+=b.vy*dt*60;\n"+s[b:]
replace('dmg:tier.base*(0.55+power*0.95)', 'dmg:tier.base*(0.55+power*0.95)*1.35')
replace('spaceLaserCannon:    {g:1.00, native:true, min:0.10}', 'spaceLaserCannon:    {g:0.30, native:true, min:0.10}')
replace('spaceVolleyHit:      {g:0.92, native:true, min:0.09}', 'spaceVolleyHit:      {g:0.62, native:true, min:0.09}')
replace("      if(pick){Snd.play(pick,1.72);return true;}","      if(pick){const level=name==='spaceVolleyLaunch'?.92:name==='spaceShadowRelease'?1.08:1.72;Snd.play(pick,level);return true;}")
replace("explode(b.x,b.y,_sz,'red',null,'nxp_clus',null);","explode(b.x,b.y,_sz,'red',null,'nxp_clus',null,null,true);")
replace("explode(b.x+rnd(-9,9),b.y+rnd(-9,9),_sz*0.62,'red',null,'nxp_dense',null);","explode(b.x+rnd(-9,9),b.y+rnd(-9,9),_sz*0.62,'red',null,'nxp_dense',null,null,true);")
replace('    if(drawLaunch._pt>=0.45){', '    const skyLead=run.stage===5?STAGE5_SKY_LEAD:.45;\n    if(drawLaunch._pt>=skyLead){')
replace('        }else drawLaunch._pt=0.45;', '        }else drawLaunch._pt=skyLead;')
# Regent formations now own motion and lock their small weapon tells before release.
replace('function xenoRegentInit(b){','function xenoRegentInit(b){\n  regentCombatMixArm();')
replace("if(b._xenoRig&&typeof xenoRegentTick==='function')xenoRegentTick(b,dt);", "if(b._xenoRig&&typeof xenoRegentTick==='function'){xenoRegentTick(b,dt);xenoRegentFormationMove(b,dt);return true;}")
replace('  if(b._xenoGrid)xenoRegentGridTick(b,dt);', '  if(b._xenoGrid)xenoRegentGridTick(b,dt);\n  xenoRigAttackTick(b,R.mother,dt);for(const h of R.helpers)xenoRigAttackTick(b,h,dt);')
a=s.index('    if(R.t>1.25&&m.fire<=0&&!b._xenoGrid)');b=s.index('\n    }',a)+6
s=s[:a]+"    if(R.t>1.25&&m.fire<=0&&!b._xenoGrid&&!m.tell){m.fire=2.10;xenoRigTell(m);}\n"+s[b:]
a=s.index('    if(R.t>1.05&&h.fire<=0&&!b._xenoGrid)');b=s.index('\n    }',a)+6
s=s[:a]+"    if(R.t>1.05&&h.fire<=0&&!b._xenoGrid&&!h.tell){h.fire=1.60+(h.side>0?.24:0);xenoRigTell(h);}\n"+s[b:]
replace("  xenoRegentDrawPart(R.mother,'s5atk_twin_station_',190);", "  xenoRegentDrawPart(R.mother,'s5atk_twin_station_',190);xenoRigTellDraw(R.mother);")
replace("for(const h of R.helpers)xenoRegentDrawPart(h,'s5atk_heavy_interceptor_',112);", "for(const h of R.helpers){xenoRegentDrawPart(h,'s5atk_heavy_interceptor_',112);xenoRigTellDraw(h);}")
replace("  if(b._xenoGrid){b.fireCd=.24;return;}\n  if(ph===0)", "  if(b._xenoGrid){b.fireCd=.24;return;}\n  if(step%3===0){xenoRegentGridStart(b,step);return;}\n  if(ph===0)")
# Each grid row is warned independently, with the next opening visible before it changes.
replace("gapW:gapW,dir:(step&1)?1:-1,cols:cols,left:left,right:right};", "gapW:gapW,dir:(step&1)?1:-1,cols:cols,left:left,right:right,warnAt:0,rowTell:.82};")
replace('G.next+=.48;', 'G.warnAt=G.t;G.rowTell=.48;G.next+=.48;')
replace('if(!G||G.t>=G.tell)return;', 'if(!G||G.wave>=G.waves||G.t>=G.next)return;')
replace('pulse=.24+.18*Math.sin(G.t*22);', 'pulse=.34+.12*Math.sin(G.t*22);')
# Alias the authored sound bank at runtime, paired with gain/filter/gates in the owning TAME.
audio={
 'razorbackGun':('reviewed_enemy_heavy_mg.wav',.60,.11), 'razorbackPressure':('cole_pressure_release_0913.wav',.55,.13),
 'razorbackCharge':('cole_pressure_start_0913.wav',.52,.16),'razorbackRocket':('reviewed_enemy_missile_launch.wav',.62,.11),
 'razorbackRam':('juggernaut_ram_launch_0913.wav',.62,.13),'overlordGun':('reviewed_enemy_heavy_mg.wav',.60,.085),
 'overlordRocket':('reviewed_enemy_missile_launch.wav',.65,.10),'overlordLance':('reviewed_enemy_heavy_laser.wav',.55,.13),
 'overlordWind':('cole_pressure_release_0913.wav',.48,.18),'overlordCharge':('furnace_power_surge.wav',.53,.16),
 'overlordRotor':('furnace_servo_whirr.wav',.35,0),'wardenGun':('reviewed_enemy_heavy_mg.wav',.65,.11),
 'wardenCenterGun':('reviewed_enemy_light_mg.wav',.67,.10),'wardenRocket':('reviewed_enemy_missile_launch.wav',.68,.18),
 'wardenRackCharge':('furnace_servo_whirr.wav',.50,.18),'sovereignDive':('juggernaut_charge_start_0913.wav',.67,.16),
 'sovereignFlyby':('juggernaut_ram_launch_0913.wav',.72,.18),
 'sovereignContact':('shield_hit_heavy.wav',.43,.10),'sovereignIntercept':('enemy_electric_bolt.wav',.40,.10),
 'sovereignBreak':('expBig.mp3',.50,.12),'sovereignHelperGun':('enemy_machine_shot_heavy.wav',.52,.09),
 'sovereignHeat':('furnace_servo_whirr.wav',.35,.16),'sovereignWindup':('furnace_power_surge.wav',.35,.24),
 'sovereignLaser':('reviewed_enemy_heavy_laser.wav',.40,.13)}
# Resolve filenames from the live authored bank rather than trusting guessed review names.
bank={'reviewed_enemy_heavy_laser.wav':'enemyHeavyLaser','reviewed_enemy_light_mg.wav':'enemyMachineGunLight','furnace_power_surge.wav':'furnacePowerSurge','enemy_electric_bolt.wav':'enemyElectricBolt'}
audio={k:('nsp_rocket_launch.mp3' if file=='reviewed_enemy_missile_launch.wav' else file,g,gate)for k,(file,g,gate)in audio.items()}
for k,(file,g,gate)in list(audio.items()):
 if file in bank:
  m=re.search(r"\n\s+"+bank[file]+r":\s*'assets/game/sounds/([^']+)'",s);assert m,bank[file];audio[k]=(m.group(1),g,gate)
for file,_,_ in audio.values():assert (ROOT/'assets/game/sounds'/file).exists(),file
rows='    /* 0914 encounter-owned reports; matching TAME rows prevent per-round stacking. */\n'+''.join("    %s:'assets/game/sounds/%s',\n"%(k,file)for k,(file,_,_)in audio.items())
replace("    bossfireDamkeeper:'",rows+"    bossfireDamkeeper:'")
rows=''.join('    %s:{g:%s,lp:5600,min:%s},\n'%(k,g,gate)for k,(_,g,gate)in audio.items())
replace('    bossfireDamkeeper:      ',rows+'    bossfireDamkeeper:      ')
if '--dry-run' in sys.argv:
 out=ROOT/'_shots/stage_1_5_0914/game.expected.js'
else:
 if path.read_bytes() not in [(ROOT/'_shots/stage_1_5_0914/game.before.js').read_bytes(),s.encode('utf-8')]:
  raise ValueError('Runtime has subsequent edits. Use --dry-run and inspect the comparison; do not overwrite them.')
 out=path
 (ROOT/'docs/STAGE3_STORED_BOATS_0914.json').write_text(stored_boats,encoding='utf-8')
out.write_bytes(s.encode('utf-8'));print('Wrote %s SHA256 %s'%(out,hashlib.sha256(out.read_bytes()).hexdigest()))
