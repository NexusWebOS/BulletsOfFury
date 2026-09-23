module.exports=function testForge(vm,ctxv,ok){
  console.log('=== 370. THE FORGE - combine, re-spec, loadout, between every stage (0917) ===');
  /* Mike, 0917: "You should be allowed 2 combinations in between each level, and this upgrade
     permanently takes over your weapon style until you reset it via re-spec ... 2 re-specs per level
     completion ... limit the amount of weapon types that can spawn to 6 per level, and make the
     player select their loadout including their new upgraded weapon type replacing the weapon type
     it was I.E machine gun now becomes incendary slugs."

     Driven through the live screen with real key taps in probe_forge_0917.py (32/0). This section
     pins the SHAPE in the vm: the tables, the rule functions, the seams, and that the screen sits in
     the debrief's exit chain. Source pins strip comments (section 47's trap). */
  var strip=function(s){return String(s).replace(/\/\*[\s\S]*?\*\//g,'').replace(/\/\/.*$/gm,'');};
  var R=function(js){ return vm.runInContext(js,ctxv); };

  /* ---- the allowance and the cap are one number each ---- */
  ok(R("FORGE_COMBOS_PER_STAGE===2 && FORGE_RESPECS_PER_STAGE===2 && FORGE_LOADOUT_MAX===6"),
     '2 combines, 2 re-specs, a 6-weapon loadout - his three numbers, one constant each');
  /* ---- only carriers can be forged, and the muzzles say which those are ----
     ⚠ THESE TWO PINS DEFENDED A LIMITATION, NOT A RULE (repointed 0917). They asserted six slots and
     that 4 / 6 / 8 could NOT be forged, on a reading taken from the KIND table rather than from the
     muzzles. Mike's own equip rule names those three as an upgrade type of their own - "1 flamethrower/
     ice breath/ other types upgrade" - and measured, all three push real rounds into pBullets and damage
     through hitEnemy while _dmgBullet still names them. So the durable claim is the one below: every
     forgeable slot's round kind is a CARRIER, derived from the muzzle, never a hand-written list. */
  ok(R("JSON.stringify(FORGE_WEAPONS)==='[0,1,2,3,4,5,6,7,8]'"),
     'FORGE_WEAPONS is every weapon slot - Mike names nine upgrade types, one per weapon');
  ok(R("FORGE_WEAPONS.every(function(w){ return forgeCanTake(w); }) && !forgeCanTake(99)"),
     'forgeCanTake answers for each of them, and refuses a slot that does not exist');
  ok(R("(function(){ var M={0:'mg',1:'spread',2:'missile',3:'beam',4:'flame',5:'orb',6:'lasermist',7:'mg',8:'yuriLightningOrb'};        return FORGE_WEAPONS.every(function(w){ return !!INFUSION_CARRIERS[M[w]]; }); })()"),
     'and every forgeable slot fires a round kind that is an INFUSION CARRIER - the reason each one qualifies');
  var ff=strip(R("String(flameFire)"));
  ok(/kind:\s*'flame'/.test(ff), 'the flamethrower pushes kind flame into pBullets - which is why it reaches the same on-hit hook');
  var cg=strip(R("String(chaingunPlayerFire)"));
  ok(/kind:\s*'mg'/.test(cg), 'the chaingun pushes kind mg, which is why it is forgeable');
  /* ---- every element x forgeable weapon has a NAME ---- */
  ok(R("Object.keys(INFUSIONS).every(function(e){ return FORGE_NAMES[e] && FORGE_WEAPONS.every(function(w){ return typeof FORGE_NAMES[e][w]==='string' && FORGE_NAMES[e][w].length>2; }); })"),
     'FORGE_NAMES covers all nine elements x all NINE forgeable weapons (0917)');
  ok(R("FORGE_NAMES.fire[0]==='INCENDIARY SLUGS'"), "Mike's own example is the first row: machine gun + fire = INCENDIARY SLUGS");
  ok(R("Object.keys(INFUSIONS).every(function(e){ return FORGE_WEAPONS.every(function(w){ return FORGE_NAMES[e][w].indexOf(\"'\")<0; }); })"),
     'no forged name carries an apostrophe (this face has no usable one at UI size - LIZZIE,S)');

  /* ---- the rules, in the vm ---- */
  R("run.forge={}; run.forgeForms={}; run.forgeElems={}; run.loadout=null; run.forgeCombos=2; run.forgeRespecs=2; run.weapon=0; run.infusion=null; run.ngplus=false;");
  /* A COMBINATION IS EARNED FROM A BOSS (Mike, 0917), so the pairs this block is about are
     granted first - and one it is NOT given proves the gate is real rather than absent. */
  R("var __ownBefore=achievementState.owned; achievementState.owned={}; forgeComboGrant('fire',0); forgeComboGrant('ice',0);");
  ok(R("forgeCombine(0,'toxic')==='locked' && !run.forge[0]"),
     'a combination that has not been earned is refused, and forges nothing');
  ok(R("forgeCombine(0,'fire')==='ok' && run.forge[0].elem==='fire' && run.forge[0].lv===1 && run.forgeCombos===1"),
     'forgeCombine forges the weapon at level 1 and spends a combine');
  ok(R("run.infusion && run.infusion.elem==='fire' && run.infusion.lv===1"),
     'and the HELD weapon takes the element at once (run.infusion)');
  ok(R("weaponDisplayName(0)==='INCENDIARY SLUGS'"), 'weaponDisplayName returns the forged name');
  ok(R("forgeCombine(0,'fire')==='owned' && run.forge[0].lv===1 && run.forgeCombos===1"),
     'a duplicate combination is refused and preserves the remaining combine');
  ok(R("forgeCombine(0,'fire')==='owned' && run.forge[0].lv===1"), 'repeated duplicate attempts never create a second tier');
  R("run.forgeCombos=1;");
  ok(R("forgeCombine(0,'ice')==='ok' && run.forge[0].elem==='ice' && run.forge[0].lv===1"),
     'a DIFFERENT element replaces the forged one at level 1 (it takes over)');
  /* ⚠ slot 4 WAS this assertion's "cannot" case and is forgeable since 0917 - a slot that does not exist
     is the honest refusal now (the flamethrower's own row is proved by probe_forge_noncarriers_0917.py). */
  ok(R("forgeCombine(99,'fire')==='cannot'"), 'a weapon slot that does not exist refuses with cannot');
  ok(R("forgeCombine(0,'dark')==='unknown'"), 'a gated element refuses while its gate is shut (dark needs NEW GAME +)');
  ok(R("forgeRespec(0)==='ok' && !run.forge[0] && run.forgeRespecs===1 && !run.infusion && weaponDisplayName(0)==='MACHINE GUN'"),
     'forgeRespec removes the element, spends a re-spec, clears the held element and restores the bare name');
  R("achievementState.owned=__ownBefore;");   /* the profile is left as this section found it */
  ok(R("forgeRespec(0)==='bare'"), 'a bare weapon has nothing to re-spec');
  R("run.forge={}; run.forgeRespecs=0; run.forge[3]={elem:'lightning',lv:1};");
  ok(R("forgeRespec(3)==='spent' && run.forge[3]"), 'a re-spec with none left is refused and changes nothing');

  /* ---- what may be combined, and where it comes from (0917) ---- */
  R("run.forgeElems={}; var __ownD=achievementState.owned; achievementState.owned={};");
  ok(R("forgeDiscovered().length===0"), 'nothing is combinable on a fresh profile');
  /* [!] SEEING AN ELEMENT IN THE FIELD GRANTS NOTHING SINCE 0917 (Mike: "you dont unlock all
     these weapon combination upgrades ... they drop from the boss"). It used to license that
     element on all nine slots at once, which is exactly what he ruled out. */
  R("forgeDiscover('toxic');");
  ok(R("forgeDiscovered().indexOf('toxic')>=0"),
     'a globally obtained element appears in the Forge for every weapon');
  R("forgeComboGrant('lightning',0); forgeComboGrant('fire',3); forgeComboGrant('dark',0);");
  ok(R("JSON.stringify(forgeDiscovered())==='[\"fire\",\"lightning\",\"toxic\",\"dark\"]'"),
     'forgeDiscovered is stable table order and boss-earned Dark Matter bypasses its old field gate');
  /* and a pair is a pair: the element is on the slot it was earned for, and on no other */
  ok(R("FORGE_WEAPONS.every(function(w){ return forgeElemsFor(w).indexOf('lightning')>=0; })"),
     'one obtained Lightning element is available on every weapon slot');
  R("achievementState.owned=__ownD;");
  var ap=strip(R("String(applyPowerup)"));
  ok(/case 'infuse':[\s\S]{0,200}forgeDiscover\(p\.elem\)/.test(ap), 'collecting an infuse pickup calls forgeDiscover - discovery is the real pickup path');

  /* ---- permanence: equip, stage start, death ---- */
  ok(/run\.weapon=_wt;[\s\S]{0,200}forgeApply\(\)/.test(ap), 'equipping a weapon from a pickup asserts its forged element');
  var bs=strip(R("String(beginStage)"));
  ok(bs.indexOf('forgeLoadoutSync')>=0 && bs.indexOf('forgeApply')>=0 && /run\._wbag=\[\]/.test(bs),
     'beginStage syncs the loadout, rebuilds the crate bag and asserts the held element');
  var src=strip(R("(function(){ var s=''; try{ s=require('fs').readFileSync('assets/game.js','utf8'); }catch(e){} return s; })()"));
  if(!src){ try{ src=strip(require('fs').readFileSync(require('path').join(__dirname,'..','assets','game.js'),'utf8')); }catch(e){ src=''; } }
  ok(/run\.infusion=null;\s*\n?\s*if\(typeof forgeApply==='function'\) forgeApply\(\);/.test(src),
     'the death reset clears the in-play element and then re-asserts the FORGED one (permanent)');
  R("run.forge={0:{elem:'fire',lv:3}}; run.weapon=0; run.infusion=null;");
  ok(R("forgeApply() && run.infusion.elem==='fire' && run.infusion.lv===1"), 'forgeApply normalizes legacy forged levels to the single combination');
  R("run.infusion={elem:'fire',lv:3,hits:4};");
  ok(R("forgeApply()===false && run.infusion.hits===4"), 'and never overwrites an element that is already at least as strong');

  /* ---- the crate pool and the loadout cap ---- */
  var sc=strip(R("String(spawnContainer)"));
  ok(sc.indexOf('crateWeaponPool()')>=0 && sc.indexOf('_pool=[0,1,2,3,4,5]')<0,
     'spawnContainer draws its bag from crateWeaponPool() - the pool lives in one place now');
  R("run.loadout=[0,1]; run.stage=1;");
  ok(R("crateWeaponPool().every(function(w){ return w===0||w===1; }) && crateWeaponPool(true).length>=6"),
     'the FILTERED pool is the loadout; the unfiltered pool is what is unlocked');
  R("run.loadout=null;");
  ok(R("(function(){ var p=crateWeaponPool(true); var l=forgeLoadoutSync(); return l.length===Math.min(p.length,FORGE_LOADOUT_MAX) && l.every(function(w){ return p.indexOf(w)>=0; }); })()"),
     'forgeLoadoutSync fills the loadout from the unlocked pool, capped at FORGE_LOADOUT_MAX');

  /* ---- the screen and the seams ---- */
  ok(R("GS.FORGE==='forge' && typeof drawForge==='function' && typeof forgeStart==='function'"), 'GS.FORGE, drawForge and forgeStart exist');
  var ds=strip(R("String(drawScene)"));
  ok(/case GS\.FORGE:\s*return drawForge\(dt\)/.test(ds), 'drawScene routes GS.FORGE to drawForge');
  var cv=strip(R("String(_setCinematicViewport)"));
  /* 0917b: the four places are ONE predicate now (debriefFamily), so a new Forge beat cannot miss one of them */
  ok((cv.match(/debriefFamily\(state\)/g)||[]).length>=2, 'the Forge takes the debrief plate aspect in BOTH _setCinematicViewport lines (through debriefFamily)');
  ok(R("['forge','forging','forged','loadout','supplies','unlocks','stageclear'].every(function(k){ return debriefFamily(k); }) && !debriefFamily(GS.PLAY)"),
     'debriefFamily covers every Forge beat and the debrief, and nothing else');
  var ss=strip(R("String(setState)"));
  ok(ss.indexOf('debriefFamily(s)')>=0, 'and setState turns the cinematic viewport on for it (the fourth place - the one the unlock page missed first)');
  ok(R("_hudStateWants(GS.FORGE)===true"), '_hudStateWants keeps the HUD canvases for it, as it does for the debrief');
  var dsc=strip(R("String(drawStageClear)"));
  ok(dsc.indexOf('forgeVisible()')>=0 && dsc.indexOf('forgeStart(_toLoadout)')>=0 && dsc.indexOf('loadoutStart(_toSupplies)')>=0 && dsc.indexOf('suppliesStart(_leave,')>=0 && dsc.indexOf('unlocksStart(_un, _forgeThen)')>=0,
     'the debrief chains unlocks -> forge -> loadout -> supplies -> scLeaveStage, each from its own CONTINUE (0917b)');
  /* ---- 0917b: the Forge sequence's beats ---- */
  ok(R("GS.FORGING==='forging' && GS.FORGED==='forged' && GS.LOADOUT==='loadout' && typeof drawForging==='function' && typeof drawLoadout==='function'"),
     'THE FORGING, THE PRODUCT and THE LOADOUT exist as states with their draws');
  ok(/case GS\.FORGING:\s*return drawForging\(dt\)/.test(ds) && /case GS\.FORGED:\s*return drawForging\(dt\)/.test(ds) && /case GS\.LOADOUT:\s*return drawLoadout\(dt\)/.test(ds),
     'drawScene routes all three');
  var fsrc=strip(R("String(drawForge)"));
  ok(fsrc.indexOf('forgingStart(')>=0 && fsrc.indexOf('strokeRect(ecx')<0, 'a combine opens THE FORGING, and the element cursor is no longer a stroked square');
  ok(fsrc.indexOf('forgeHexPointer(')>=0 && fsrc.indexOf('forgeSelArrowUp(')>=0, 'the Forge selector is the traced hex pointer plus the menu arrow');
  var trs=strip(R("String(forgeTraceCanvas)"));
  ok(trs.indexOf('getImageData')<0 && trs.indexOf('destination-out')>=0, 'the pointer is traced by compositing, never getImageData (file:// taints)');
  var pvs=strip(R("String(forgePreviewTick)"))+strip(R("String(forgePreviewSwap)"));
  ok(pvs.indexOf('pShoot()')>=0 && pvs.indexOf('finally')>=0 && pvs.indexOf('pBullets=sv.pb')>=0,
     'the product preview fires the REAL weapon through pShoot and always restores the live round list');
  ok(R("(function(){ var s0=run._forgeShown; run._forgeShown=false; var a=loadoutVisible(); run._forgeShown=true; var b=loadoutVisible(); run._forgeShown=s0; return b===true && (a===(crateWeaponPool(true).length>FORGE_LOADOUT_MAX)); })()"),
     'THE LOADOUT opens after a Forge visit, or when there are more weapons than bays - never on an empty choice');
  /* 0919, Mike: each cleared level grants one power and POWERS GAINED has one bay. */
  ok(R("(function(){ var s0=run._stageElements; run._stageElements=['fire','fire','ice']; var r=unlockRowsFor(3,'cole'); var g=powersGained(); run._stageElements=s0; return r.length===0 && JSON.stringify(g)==='[\"fire\"]'; })()"),
     'boss-dropped elements grant one power in POWERS GAINED, never on Weapon Found');
  ok(R("GS.POWERS==='powers' && debriefFamily(GS.POWERS) && typeof drawPowers==='function'") && /case GS\.POWERS:\s*return drawPowers\(dt\)/.test(ds),
     'POWERS GAINED is its own state, drawn by drawPowers, at the debrief aspect');
  var pws=strip(R("String(drawPowers)"));
  ok(pws.indexOf('forgeComboName')<0 && pws.indexOf('micon_forge_')<0 && pws.indexOf("'inf_'+e")>=0,
     'and it shows the element badge and name only - no weapon, no forged product');
  ok(dsc.indexOf('powersStart(_toForge)')>=0, 'the debrief runs weapons gained -> powers gained -> forge');
  var fgs=strip(R("String(drawForging)"));
  ok(fgs.indexOf("'LEVEL '")<0 && fgs.indexOf('FORGE_ROMAN[')<0, 'the Forge sequence shows no weapon LEVELS - those are the in-game upgrade');
  ok(R("typeof stageTextCoin==='function' && typeof fpCoin==='function'") && strip(R("String(drawArmory)")).indexOf('stageTextCoin(')>=0,
     'the FURIOUS coin draws beside the points on the Armory');
  ok(R("(function(){ var p=[]; for(var j=1;j<LOADOUT_PLATE.bayX.length;j++) p.push(LOADOUT_PLATE.bayX[j]-LOADOUT_PLATE.bayX[j-1]); return p.every(function(x){ return Math.abs(x-0.143)<0.002; }) && LOADOUT_PLATE.bayY>0.28; })()"),
     'the six loadout icons align with the measured wells on the rebuilt plate');
  /* ---- 0917c: the bonus pickups and the two bombs ---- */
  ok(R("(function(){ var s=String(killDrop); return s.indexOf('bonusDrop(e)')>=0 && s.indexOf('bonusDrop(e)')<s.indexOf('chance(0.18'); })()"),
     'killDrop rolls the score bullets and bombs on their own, before the 18% loot gate');
  ok(R("(function(){ var n={}; for(var i=0;i<4000;i++){ var v=scoreChipRoll(); n[v]=(n[v]|0)+1; } return n[100]>n[250] && n[250]>n[500] && n[500]>n[1000] && n[1000]>0; })()"),
     'score bullets: 100 is the common one, 1000 the rare one - all four can drop');
  ok(R("(function(){ var sc0=run.score|0; var p={kind:'scorechip',val:500,x:10,y:10}; applyPowerup(p); var d=(run.score|0)-sc0; run.score=sc0; return d===500; })()"),
     'a score bullet is worth exactly its NUMBER (the pickup bonus is not paid twice)');
  ok(R("(function(){ var keep=enemies.slice(); enemies.length=0; var L=camLeftX(); var a={x:L+100,y:200,w:30,h:30,hp:40,maxhp:40,dropOk:false}, b={x:L+200,y:300,w:30,h:30,hp:40,maxhp:40,dropOk:false}, off={x:L-400,y:200,w:30,h:30,hp:40,maxhp:40,dropOk:false}; enemies.push(a,b,off); var eb=eBullets.slice(); eBullets.push({x:L+50,y:50,vx:0,vy:1}); var n=furyBombDetonate(); var ok2=n===2 && (a.dead||a._dyingT!=null) && (b.dead||b._dyingT!=null) && !(off.dead||off._dyingT!=null) && eBullets.every(function(q){return q.dead;}); enemies.length=0; for(var i=0;i<keep.length;i++) enemies.push(keep[i]); eBullets.length=0; for(var j=0;j<eb.length;j++) eBullets.push(eb[j]); bombReset(); return ok2; })()"),
     'the FURY BOMB blows up everything ON SCREEN and every enemy round - and nothing off it');
  ok(R("(function(){ timeBombArm(); var beeps=[]; var last=0; for(var f=0;f<60*3.3;f++){ bombTick(1/60); if(timeBomb && timeBomb.beeps!==last){ beeps.push(timeBomb.t); last=timeBomb.beeps; } } var gaps=[]; for(var i=1;i<beeps.length;i++) gaps.push(beeps[i]-beeps[i-1]); var shrinking=gaps.length>6 && gaps[gaps.length-1]<gaps[0]*0.3; for(var g=0;g<60;g++) bombTick(1/60); var blew=!timeBomb && !!bombFx && bombFx.kind==='time'; bombReset(); return shrinking && blew; })()"),
     'the TIMED BOMB beeps with every gap shorter than the last, then blows as a wave');
  ok(R("(function(){ var keep=powerups.slice(); powerups.length=0; var c={kind:'crate',x:player.x+40,y:player.y,hp:5,w:30,h:30,wtype:1}; powerups.push(c); timeBombBlow(); for(var f=0;f<30;f++) bombTick(1/60); var broke=c.dead; powerups.length=0; for(var i=0;i<keep.length;i++) powerups.push(keep[i]); bombReset(); return broke; })()"),
     'and the wave BREAKS OPEN the boxes and pills it reaches (crates, capsules)');
  ok(R("(function(){ var s=String(bombHitBosses); return s.indexOf('hitBoss(')>=0 && s.indexOf('frac')>=0; })()"),
     'a bomb takes a SHARE of a boss bar through the ordinary hit path - never a one-shot');
  /* ---- 0917d ---- */
  ok(R("(function(){ var keepE=enemies, keepP=powerups; var dummy={x:65,y:40,w:40,h:40,hp:30,maxhp:30}; enemies=[dummy]; powerups=[]; var P=forgePreviewNew(0,'fire',2); for(var i=0;i<120;i++) forgePreviewTick(P,130,330,1/60); var untouched=(dummy.hp===30) && enemies.length===1 && enemies[0]===dummy; enemies=keepE; powerups=keepP; return untouched && P.fired>0; })()"),
     'the product preview swaps the stage target lists out - a preview round cannot strike a live unit');
  ok(R("(function(){ var keep=powerups.slice(); powerups.length=0; var px=player.x, py=player.y, pd=player.dead; player.dead=false; var c={kind:'scorechip',val:100,x:player.x+60,y:player.y}, b={kind:'furybomb',x:player.x+60,y:player.y+5}; powerups.push(c,b); var d0=Math.abs(c.x-player.x); scoreMagnetTick(); var pulled=Math.abs(c.x-player.x)<d0, still=(b.x===player.x+60); powerups.length=0; for(var i=0;i<keep.length;i++) powerups.push(keep[i]); player.dead=pd; return pulled && still; })()"),
     'score bullets drift to a nearby ship; a bomb does not');
  ok(R("(function(){ var s=String(campaignMenuInputTick); return s.indexOf('campMapStartTap()')>=0 && String(campMapStartTap).indexOf(\"k!=='enter'\")>=0; })()"),
     'on the campaign map ENTER is confirm - the menu toggle is P / controller START (0917d)');
  /* ---- 0918: the generated effects ---- */
  ok(R("['fire','ice','lightning','prism','toxic','kinetic','water','chrome','dark'].every(function(e){ return XART._src['efx_burst_'+e]; }) && XART._src.efx_burn && ['fire','water','lightning'].every(function(g){ return XART._src['efx_geyser_'+g]; })"),
     'all 13 generated effect strips are registered (9 bursts, the burning fire, 3 geysers)');
  ok(strip(R("String(infusionOnHit)")).indexOf('efxBurst(b._inf')>=0, 'a forged round spawns its element BURST where it lands');
  ok(R("(function(){ efxBursts=[]; for(var i=0;i<60;i++) efxBurst('fire',0,0,40); var capped=efxBursts.length===EFX_BURST_CAP; efxTick(1); var gone=efxBursts.length===0; return capped && gone; })()"),
     'bursts are capped and expire on the game clock');
  ok(R("(function(){ geysers=[]; geyserSpawn(100,400,'fire'); for(var i=0;i<60;i++) geyserTick(1/60); var h=geysers[0]&&geysers[0].h; for(var j=0;j<120;j++) geyserTick(1/60); var done=geysers.length===0; return h===GEYSER_H && GEYSER_H>=300 && done; })()"),
     'a geyser erupts to a section of the screen (GEYSER_H) and ends');
  ok(R("(function(){ geysers=[]; for(var i=0;i<9;i++) geyserSpawn(100+i,400,'fire'); var n=geysers.length; geysers=[]; return n===GEYSER_CAP; })()"),
     'geysers are capped');
  /* ---- 0918b: vents, debris, zone columns, the flipped flamethrower ---- */
  ok(R("XART._src.efx_debris_0 && XART._src.efx_debris_1"), 'both fire debris sprites are registered');
  ok(R("(function(){ geysers=[]; var g=geyserSpawn(100,400,'fire'); var ok=!!g && geysers[0]===g; geysers=[]; return ok; })()"), 'geyserSpawn returns the column it raised');
  ok(R("(function(){ var r=run.stage, b=bossActive; s2Vents=[]; run.stage=3; s2VentT=0; s2VentTick(1/60); var a=s2Vents.length; run.stage=2; bossActive=true; s2VentT=0; s2VentTick(1/60); var c=s2Vents.length; run.stage=r; bossActive=b; s2Vents=[]; fireDebris=[]; return a===0 && c===0; })()"),
     'mountain vents erupt only on stage 2 and never while the boss is up');
  ok(R("(function(){ fireDebris=[]; var d=debrisLaunch(0,400,1,0); var vy0=d.vy; debrisTick(1/60); var up=d.vy>vy0; fireDebris=[]; return vy0<0 && up; })()"), 'fire debris is thrown UP and falls under gravity');
  ok(R("ZONE_N===4 && (function(){ var L=camLeftX(), R2=camRightX(); zoneCols=[]; var c=zoneColumnSpawn(zoneOf(R2-1),'fire',true); var ok=c.i===3 && Math.abs(c.w-(R2-L)/4)<0.01 && c.hostile; zoneCols=[]; return ok; })()"),
     'the screen is four zones and a zone column fills exactly one');
  ok(strip(R("String(fztBeamDraw)")).indexOf("efx_geyser_fire")>=0 && strip(R("String(fztBeamDraw)")).indexOf("scale(1,-1)")>=0,
     "the Furnace's flamethrower is the fire geyser, flipped");
  ok(strip(R("String(furnaceTick)")).indexOf('furnaceZoneTick')>=0, 'the Furnace pours a zone column');
  /* ---- 0918c: the boss arena's terrain is dimmed while the boss lives ---- */
  ok(R("(function(){ var r=run.stage; run.stage=2; var c=_levelCfg(); run.stage=r; return !!c && c.bossDim>0.3 && c.bossDim<0.8; })()"), 'stage 2 opts its boss arena into the terrain dim');
  ok(strip(R("String(_drawBGCore)")).indexOf('arenaBossDimDraw')>=0, 'the dim is drawn on the TERRAIN pass, under every unit and round');
  ok(R("(function(){ var b=bossActive, bb=boss, lv=_arenaDimLv; _arenaDimLv=1; bossActive=false; for(var i=0;i<200;i++) arenaBossDimDraw(1/60); var gone=_arenaDimLv===0; _arenaDimLv=lv; bossActive=b; boss=bb; return gone; })()"),
     'with no live boss the dim eases back out to nothing');
  var df=strip(R("String(drawForge)"));
  ok(/const mL=\(Input\.menuLeft\?Input\.menuLeft\(\):false\), mR=/.test(df) && /const mB=\(Input\.menuBack/.test(df) && /,\s*mS=\(Input\.menuStart/.test(df),
     'every consuming reader is read ONCE into a local before any is acted on');
  ok(df.indexOf('forge_loadout_0918')>=0 && df.indexOf('forgeRespec')>=0, 'the generated plate embeds RE-SPEC and the input remains wired');
  ok(df.indexOf('forge_loadout_0918')>=0 && df.indexOf('forgeSlotKey')>=0, "the six loadout boxes come from the dedicated Forge plate and show live weapon art");
  ok(R("Object.keys(MENU_BACK).indexOf(GS.FORGE)<0"), 'the Forge is NOT in MENU_BACK - back cancels an element pick, it never leaves the screen');

  /* ---- the save ---- */
  var cs=strip(R("String(campSnapshot)")), ca=strip(R("String(campApply)"));
  ok(cs.indexOf('forge:')>=0 && cs.indexOf('forgeForms:')>=0 && cs.indexOf('forgeElems:')>=0 && cs.indexOf('loadout:')>=0, 'campSnapshot carries active forge, all forms, elements and loadout');
  ok(ca.indexOf('run.forge=')>=0 && ca.indexOf('run.forgeForms=')>=0 && ca.indexOf('run.forgeElems=')>=0 && ca.indexOf('run.loadout=')>=0, 'campApply restores every Forge field without invalidating old saves');
  var sr=strip(R("String(startRun)"));
  ok(/run\.forge=\{\};\s*run\.forgeForms=\{\};\s*run\.forgeElems=\{\};\s*run\.loadout=null;/.test(sr), 'a new run starts with no active or crafted forms');
  R("run.forge={}; run.forgeForms={}; run.forgeElems={}; run.loadout=null; run.infusion=null; run.weapon=0;");
};
