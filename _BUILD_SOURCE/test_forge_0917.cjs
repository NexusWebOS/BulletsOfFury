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
  R("run.forge={}; run.forgeElems={}; run.loadout=null; run.forgeCombos=2; run.forgeRespecs=2; run.weapon=0; run.infusion=null; run.ngplus=false;");
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
  ok(R("forgeCombine(0,'fire')==='ok' && run.forge[0].lv===2 && run.forgeCombos===0"),
     'the same element again LEVELS it (L2) and spends the second combine');
  ok(R("forgeCombine(0,'fire')==='spent' && run.forge[0].lv===2"), 'a third combine is refused as spent and changes nothing');
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
  ok(R("forgeDiscovered().indexOf('toxic')<0"),
     'an element merely SEEN in the field is not combinable - only an earned pair is');
  R("forgeComboGrant('lightning',0); forgeComboGrant('fire',3); forgeComboGrant('dark',0);");
  ok(R("JSON.stringify(forgeDiscovered())==='[\"fire\",\"lightning\"]'"),
     'forgeDiscovered() is in table order and hides an EARNED element whose gate is shut (dark needs NEW GAME +)');
  /* and a pair is a pair: the element is on the slot it was earned for, and on no other */
  ok(R("forgeElemsFor(0).indexOf('lightning')>=0 && forgeElemsFor(3).indexOf('lightning')<0"),
     'forgeElemsFor answers per SLOT - lightning was earned for the machine gun, not for the laser');
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
  ok(R("forgeApply() && run.infusion.elem==='fire' && run.infusion.lv===3"), 'forgeApply seeds run.infusion from the forge at the forged level');
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
  ok((cv.match(/GS\.FORGE/g)||[]).length>=2, 'the Forge takes the debrief plate aspect in BOTH _setCinematicViewport lines');
  var ss=strip(R("String(setState)"));
  ok(ss.indexOf('GS.FORGE')>=0, 'and setState turns the cinematic viewport on for it (the fourth place - the one the unlock page missed first)');
  ok(R("_hudStateWants(GS.FORGE)===true"), '_hudStateWants keeps the HUD canvases for it, as it does for the debrief');
  var dsc=strip(R("String(drawStageClear)"));
  ok(dsc.indexOf('forgeVisible()')>=0 && dsc.indexOf('forgeStart(_leave)')>=0 && dsc.indexOf('unlocksStart(_un, _forgeThen)')>=0,
     'the debrief chains unlocks -> forge -> scLeaveStage, each from its own CONTINUE');
  var df=strip(R("String(drawForge)"));
  ok(/const mL=\(Input\.menuLeft\?Input\.menuLeft\(\):false\), mR=/.test(df) && /const mB=\(Input\.menuBack/.test(df) && /,\s*mS=\(Input\.menuStart/.test(df),
     'every consuming reader is read ONCE into a local before any is acted on');
  ok(df.indexOf("'pad_x'")>=0 && df.indexOf("'pad_start'")>=0, 'the footer names COMBINE, RE-SPEC and CONTINUE with the pad glyphs');
  ok(df.indexOf('unlockPanel(pl, UNLOCK_ART.box')>=0, "the six loadout boxes are the plate's own rank bay, the construction Mike approved for the unlock page");
  ok(R("Object.keys(MENU_BACK).indexOf(GS.FORGE)<0"), 'the Forge is NOT in MENU_BACK - back cancels an element pick, it never leaves the screen');

  /* ---- the save ---- */
  var cs=strip(R("String(campSnapshot)")), ca=strip(R("String(campApply)"));
  ok(cs.indexOf('forge:')>=0 && cs.indexOf('forgeElems:')>=0 && cs.indexOf('loadout:')>=0, 'campSnapshot carries forge, forgeElems and loadout');
  ok(ca.indexOf('run.forge=')>=0 && ca.indexOf('run.forgeElems=')>=0 && ca.indexOf('run.loadout=')>=0, 'campApply restores all three (optional fields, CAMP_SAVE_VER untouched)');
  var sr=strip(R("String(startRun)"));
  ok(/run\.forge=\{\};\s*run\.forgeElems=\{\};\s*run\.loadout=null;/.test(sr), 'a new run starts bare');
  R("run.forge={}; run.forgeElems={}; run.loadout=null; run.infusion=null; run.weapon=0;");
};
