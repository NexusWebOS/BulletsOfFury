module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path'),crypto=require('crypto'),root=path.resolve(__dirname,'..');
 console.log('=== October 10: full audio playthrough corrections ===');
 const files=[['smooth_motion_art_1009.js','SM10_ART'],['arcade_finish_art_1010.js','AF10_ART'],['smooth_motion_1009.js','SM10'],
  ['arcade_jets_art_1010.js','AC10_JET_ART'],['arcade_combat_1010.js','AC10'],['player_hud_art_1008.js','PH8_ART'],
  ['player_hud_1008.js','PH8'],['feedback_1009.js','FB9_HUD'],['orbs_1010.js','OB10'],
  ['audio_hud_art_1010.js','AP10_HUD_ART'],['audio_hud_1010.js','AP10_UI'],['audio_feedback_1010.js','AP10'],
  ['audio_fx_art_1010.js','AP10_FX_ART'],['audio_fx_1010.js','AP10_FX'],['audio_encounters_1010.js','AP10_E'],
  ['audio_wind_1010.js','AP10_W'],['map_briefing_1003g.js','MAPG_BRIEFINGS'],['audio_stagex_1010.js','AP10_X'],['audio_cinematic_art_1010.js','AP10_CIN_ART'],
  ['audio_cinematics_1010.js','AP10_C'],['audio_alien_1010.js','AP10_A'],['audio_fleet_1010.js','AP10_FLEET'],
  ['audio_fire_art_1010.js','AP10_FIRE_ART'],['audio_fire_1010.js','AP10_FIRE'],['audio_extra_art_1010.js','AP10_EXTRA_ART'],['audio_extra_1010.js','AP10_EXTRA'],
  ['hq_live_art_1010.js','HQ10_ART'],['hq_live_1010.js','HQ10'],['homecoming_art_1010.js','HC10_ART'],['homecoming_1010.js','HC10'],['survivor_art_1010.js','SV10_ART'],['survivor_1010.js','SV10'],
  ['hq_landing_art_1010.js','HL10_ART'],['hq_landing_1010.js','HL10']];
 for(const [f,symbol] of files)if(vm.runInContext('typeof '+symbol,c)==='undefined')vm.runInContext(fs.readFileSync(path.join(root,'assets',f),'utf8'),c,{filename:f});
 const banks=JSON.parse(vm.runInContext('JSON.stringify({...AP10_FX_ART,...AP10_CIN_ART,...AP10_FIRE_ART,...AP10_EXTRA_ART,...HQ10_ART,...Object.fromEntries(Object.entries(HL10_ART).map(([k,v])=>["homecoming_"+k,v])),...Object.fromEntries(Object.entries(SV10_ART).map(([k,v])=>["survivor_"+k,v])),...Object.fromEntries(Object.entries(HC10_ART).map(([k,v])=>["jet_takeover_"+k,v]))})',c));
 for(const [name,bank] of Object.entries(banks)){
  const valid=bank.every(a=>{const p=path.join(root,a.path);if(!fs.existsSync(p))return false;const b=fs.readFileSync(p);
   const reference=bank.find(q=>q.clip===a.clip);
   return a.w%2===0&&a.h%2===0&&a.w===b.readUInt32BE(16)&&a.h===b.readUInt32BE(20)&&a.w===reference.w&&a.h===reference.h&&String(a.pivot)===String(reference.pivot)&&crypto.createHash('sha256').update(b).digest('hex')===a.sha256;});
  ok(valid,name+': shipping pixels, even resolution and physical pivots match registration');
  ok(new Set(bank.map(a=>a.sha256)).size===bank.length,name+': all animation cells contain distinct authored pixels');
 }
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={};ht27Stop();coopOn=false;special=null;run.mode='campaign';run.pilot='yuri';diffKey='normal';DIFF=DIFFS.normal;
  achievementState.owned={};run.forgeElems={prism:1};run.forge={3:{elem:'prism',lv:4}};
  run.forgeForms={3:{prism:{elem:'prism',lv:4},wind:{elem:'wind',lv:2}}};run.infusion={elem:'prism',lv:4};
  ap10WindMigrate();o['Legacy Prism migration preserves the best crafted level']=run.forgeElems.wind&&run.forgeForms[3].wind.lv===4&&run.forge[3].elem==='wind'&&run.infusion.elem==='wind'&&!run.forgeForms[3].prism;
  run._earnedUnlocks={chaingun:true,laserMist:true,lightningOrb:true};run.forgeCombos=30;run.forgeRespecs=3;run.loadout=FORGE_WEAPONS.slice();
  run.forgeForms={};run.forge={};forgeComboGrant('wind');let wind=true;for(let w=0;w<9;w++){const result=forgeCombine(w,'wind');wind=(result==='ok')&&wind;}
  o['All nine Wind carriers are genuinely craftable']=wind&&Object.values(run.forgeForms).filter(F=>F.wind).length===9;
  const saved=campSnapshot();run.forgeForms={};run.forgeElems={};campApply(saved);
  o['Wind recipes survive a real campaign save/apply cycle']=run.forgeElems.wind&&Object.values(run.forgeForms).filter(F=>F.wind).length===9;
  run.stage=2;run.spaceMode=false;player.reset();player._fuse=1;special=null;run.bombs=15;pBullets=[];
  useBomb();autoFireMissiles();spaceVolleyAutoTick(1,true);
  o['A held charge blocks every missile entry without spending ammunition']=pBullets.length===0&&run.bombs===15;
  player._fuse=0;run._spaceShadowHeld=false;run._spaceShadowCharge=0;_frzOrb=null;
  o['Releasing the charge restores missile eligibility']=!ap10Charging();
  for(const d of ['easy','normal','hard','furious']){diffKey=d;DIFF=difficultyForRun('arcade',d);run.stage=3;
   const q=elementalDamageResult({x:200,y:180},'boss',{kind:'orb',_el:'ice'},100,200,180);
   o[d+': an ice boss resists 80% same-element damage']=q.dmg===20;
  }
  diffKey='normal';DIFF=DIFFS.normal;run.weapon=7;run.wlevel=5;pBullets=[];chaingunPlayerFire(5);
  o['Max chaingun is exactly two physical gun lanes']=pBullets.filter(b=>b.kind==='mg').length===2;
  run.stage=6;run._gp4StageX='left';bossDefeated=true;run.lives=3;run.bombs=2;run.forgeCombos=1;campaign.stageX1004={rewarded:false};delete run._ap10XReward;
  ap10StageXReward();const first=[run.lives,run.bombs,run.forgeCombos];ap10StageXReward();
  o['Stage X earns life, missiles and a forge credit once']=first.join()===[4,14,2].join()&&first.join()===[run.lives,run.bombs,run.forgeCombos].join();
  delete run._gp4StageX;bossDefeated=false;
  run._s5Resume={t:69.4,clock:70,wave:17,map:901,scroll:902,sky:903,miniDone:true};run._s5ResumeArm=1;
  beginStage(5);o['Space detour resumes its exact timeline and completed miniboss']=Math.abs(stageTimer-69.4)<1e-8&&subBossDone&&subBossTriggered&&_stage5SpaceScroll===903&&stagePlan.every(q=>q.t>69.4)&&state===GS.PLAY;
  o['HQ attack cinematic uses four live plates with an interactive radar beat']=BOFCinematicDirector.script(5).filter(b=>/^hq10_background_/.test(b.bg||'')).length===4&&BOFCinematicDirector.script(5).some(b=>b.interactive==='hq-radar'&&b.duration>=12);
  o['Sewer direction is spoken by Decker in the active cinematic owner']=BOFCinematicDirector.script(6).some(b=>b.who==='DECKER'&&/alien signal beneath/.test(b.text));
  o['All nine pilots warm their original static aircraft and two complete eight-frame body clips']=HL10.pilots.length===9&&HL10.pilots.every(pk=>HL10_ART[pk+'_exit'].length===8&&HL10_ART[pk+'_walk'].length===8&&hc10ShipAssets(pk).every(a=>hl10Assets(pk).some(q=>q.key===a.key))&&!hl10Assets(pk).some(a=>/^hc10_.*_(front|rear|landing)_/.test(a.key)));
  o['Each walking cell contains one complete pilot instead of neighbouring figure fragments']=HL10.pilots.every(pk=>HL10_ART[pk+'_walk'].every(a=>a.opaque_bounds[2]-a.opaque_bounds[0]<a.w*.60&&a.opaque_bounds[1]>0&&a.opaque_bounds[3]<a.h));
  o['Homecoming lands the static original aircraft before the selected pilot disembarks']=hl10Sample(11.2,'cole').grounded&&hl10Sample(13.5,'cole').shipFrame===0&&hl10Sample(13.5,'cole').actorClip===null&&hl10Sample(13.8,'cole').actorClip==='exit';
  o['The HQ door fully opens before physical entry, then closes']=hl10Sample(21.2).doorFrame===15&&hl10Sample(23.0).actorClip==='walk'&&hl10Sample(24.2).entered&&hl10Sample(25.8).doorFrame===0;
  o['The full sixteen-second satellite takeover starts only after the pilot enters HQ']=VICTORY_DISH_AT===HL10.times.end&&VICTORY_DISH_AT>HL10.times.entered&&Math.abs(VICTORY_WARNING_AT-VICTORY_DISH_AT-SV10.times.end)<1e-8&&SV10.times.end===16.4&&VICTORY_SPACE_AT>VICTORY_WARNING_AT&&VICTORY_CARD_AT>VICTORY_STINGER_AT;
  o['Survivor locomotion and archived launch art retain thirty-two native poses']=SV10_ART.crawl.length===32&&SV10_ART.burst.length===32&&SV10_ART.contact.length===16;
  o['The real ending warms every survivor cell and no longer uses the old wobbling still']=sv10Assets().every(a=>victoryEndingKeys().includes(a.key))&&!victoryEndingKeys().includes('cinend_symbiote_survivor');
  o['The survivor remains attached while thirty-two growth poses become a fully corrupted satellite']=sv10Sample(3.001).bank==='infection'&&sv10Sample(3.001).frame===0&&sv10Sample(5.799).frame===31&&sv10Sample(8.4).corruption===1&&sv10Sample(13).bank==='infection';
  o['All nine jets use the original straight front and rear ship images']=HC10.pilots.every(pk=>hc10FlightSample(1,pk).bank==='ship_'+pk+'_so6'&&hc10FlightSample(4,pk).bank==='ship_'+pk+'_so2'&&hc10FlightSample(1,pk).frame===0&&hc10ShipGeometry(pk,'front').w>0&&hc10ShipGeometry(pk,'rear').h>0);
  o['Every selected jet descends straight downward and shrinks into Earth without turning']=HC10.pilots.every(pk=>{const a=hc10FlightSample(3,pk),b=hc10FlightSample(4.5,pk),d=hc10FlightSample(5.99,pk);return a.x===.5&&b.x===.5&&d.x===.5&&a.y<b.y&&b.y<d.y&&a.width>b.width&&b.width>d.width&&a.rotation===0&&d.rotation===0;});
  o['The ending warms the exact return gate animation used by Dracodia']=HC10.pilots.every(pk=>AP10_CIN_ART.void.every(a=>hc10FlightAssets(pk).some(b=>b.key===a.key)));
  o['Binary and code grow across the screen after infection rather than before the survivor arrives']=sv10CodeSample(5.7,727,512).length===0&&sv10CodeSample(8,727,512).some(L=>L.text==='10001001000')&&sv10CodeSample(12,727,512).length>sv10CodeSample(6,727,512).length;
  return o;
 })())`,c));
 for(const [name,passed] of Object.entries(out))ok(passed,name);
};
