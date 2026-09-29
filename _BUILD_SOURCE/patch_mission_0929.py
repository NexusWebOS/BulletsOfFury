from pathlib import Path
import argparse

def replace(text, before, after):
    assert text.count(before)==1, (before[:100], text.count(before))
    return text.replace(before, after)

def patch(root):
    p=root/'assets/game.js'; s=p.read_text(encoding='utf-8')
    s=replace(s, 'for(const c of forgeCombosOwned()) run.forgeElems[c.elem]=1;', "if(run.mode!=='campaign')for(const c of forgeCombosOwned()) run.forgeElems[c.elem]=1;")
    s=replace(s, 'for(const id of Object.keys(achievementState.owned||{})){\n    const m=/^forge_', "if(run.mode!=='campaign')for(const id of Object.keys(achievementState.owned||{})){\n    const m=/^forge_")
    s=replace(s, '|| furiousOwned(forgeElementId(elem)) || furiousOwned(forgeComboId(elem,w))', "|| (run.mode!=='campaign'&&(furiousOwned(forgeElementId(elem)) || furiousOwned(forgeComboId(elem,w))))")
    s=replace(s, 'run._missileBonus=null;\n  run.forge={};', 'run._missileBonus=null;\n  run.infusion=null;run._stageElements=[];run._earnedUnlocks={};run._chainSeeded=false;run._chainLightningLevel=1;run._wbag=[];run._forgeBlastSeq={};\n  if(run.mode===\'campaign\'){run.ngplus=false;run.affiliation={};run.allies=[];}\n  run.forge={};')
    s=replace(s, 'run2.speed = 0;', 'run2.infusion=null;run2.forge={};run2.forgeForms={};run2.forgeElems={};run2.loadout=null;run2._earnedUnlocks={};run2._chainSeeded=false;run2._stageElements=[];\n    run2.speed = 0;')
    s=replace(s, 'function laserMistIsUnlocked(){return !!laserMistUnlocked;}', "function laserMistIsUnlocked(){return run&&run.mode==='campaign'?!!run._earnedUnlocks?.mist:!!laserMistUnlocked;}")
    s=replace(s, 'if(laserMistUnlocked)return false;\n  laserMistUnlocked=true;', "if(laserMistIsUnlocked())return false;\n  if(run){run._earnedUnlocks=run._earnedUnlocks||{};run._earnedUnlocks.mist=true;}\n  laserMistUnlocked=true;")
    s=replace(s, 'function chaingunIsUnlocked(){return !!chaingunUnlocked;}', "function chaingunIsUnlocked(){return run&&run.mode==='campaign'?!!run._earnedUnlocks?.chaingun:!!chaingunUnlocked;}")
    s=replace(s, 'function yuriLightningOrbIsUnlocked(){return !!yuriLightningOrbUnlocked;}', "function yuriLightningOrbIsUnlocked(){return run&&run.mode==='campaign'?!!run._earnedUnlocks?.lightningOrb:!!yuriLightningOrbUnlocked;}")
    s=replace(s, "yuriWon=true;if(!R.wlevels)", "yuriWon=true;R._earnedUnlocks=R._earnedUnlocks||{};R._earnedUnlocks.lightningOrb=true;if(!R.wlevels)")
    s=replace(s, '  if(!yuriWon)return false;\n', '  if(!yuriWon)return false;\n  // Campaign progress is shared by seatIn; Yuri in seat 2 must retain his earned gate.\n  run._earnedUnlocks=run._earnedUnlocks||{};run._earnedUnlocks.lightningOrb=true;\n')
    s=replace(s, "if(P.w===8){run.pilot='yuri';yuriLightningOrbUnlocked=true;}", "if(P.w===8){run.pilot='yuri';yuriLightningOrbUnlocked=true;run._earnedUnlocks=Object.assign({},run._earnedUnlocks,{lightningOrb:true});}")
    s=replace(s, 'run._thunderStormUnlocked=!!s.thunderStormUnlocked;run._thunderCeremonyShown=!!s.thunderCeremonyShown;', 'run._thunderStormUnlocked=!!s.thunderStormUnlocked;run._chainLightningLevel=run._thunderStormUnlocked?2:1;run._thunderCeremonyShown=!!s.thunderCeremonyShown;')
    s=replace(s, 'if(chaingunUnlocked)return false;\n  chaingunUnlocked=true;', "if(chaingunIsUnlocked())return false;\n  if(run){run._earnedUnlocks=run._earnedUnlocks||{};run._earnedUnlocks.chaingun=true;}\n  chaingunUnlocked=true;")
    s=replace(s, 'forge:Object.assign({},run.forge||{}), forgeForms:', 'earnedUnlocks:Object.assign({},run._earnedUnlocks||{}),\n    forge:Object.assign({},run.forge||{}), forgeForms:')
    s=replace(s, "run.mode='campaign';run._missileBonus=null;run.ngplus=!!s.ngplus;", "run.mode='campaign';run._missileBonus=null;run.ngplus=!!s.ngplus;run.infusion=null;run._stageElements=[];run._chainSeeded=false;\n  // Old slots migrate from THEIR completed stages, never profile-wide unlocks.\n  run._earnedUnlocks=s.earnedUnlocks?Object.assign({},s.earnedUnlocks):{chaingun:!!s.rank?.[5],mist:!!s.rank?.[9],lightningOrb:s.pilot==='yuri'&&!!s.rank?.[4]};")
    s=replace(s, 'campaign._booted=false;campaign._introSeen=false;', 'campaign._booted=false;campaign._introSeen=false;campaign._l78Pending=0;campaign.rivalScattered=false;campaign.rivalDefeated=[false,false,false,false,false];')
    s=replace(s, "[5.5,'COLE','WHAT YOU FOUGHT", "[5.5,missionRadioWho('DECKER'),'WHAT YOU FOUGHT")
    s=replace(s, "[17,'DECKER','................']", "[17,missionRadioWho('DECKER'),'................']")
    s=replace(s, "[20,'COLE','LOOK OUT! STEALTH", "[20,missionRadioWho('DECKER'),'LOOK OUT! STEALTH")
    s=replace(s, "[11,'MAVERICK','HEY DECKER... DID YOU WORK ON CLOAKING FOR THE CONFEDERATION?']", "[11,missionRadioWho('MAVERICK'),missionRadioWho('DECKER')+'... DID YOU WORK ON CLOAKING FOR THE CONFEDERATION?']")
    s=replace(s, "const who=_pilotKey()==='cole'?'MAVERICK':'COLE';", "const who=missionRadioWho('COLE');")
    # Beam integration belongs to the shared renderer, used by gameplay AND Forge preview.
    s=replace(s, "if(b.kind==='beam'){   // held player laser\n", "if(b.kind==='beam'){   // held player laser\n      if(typeof missionBeamDraw==='function'&&missionBeamDraw(b))continue;\n")
    # Isolated probes / old index copies can still run the engine without the addon.
    marker='let s6Opening=null;'
    s=replace(s,marker,"function missionRadioWho(preferred){\n  const who=String(preferred||'DECKER').toUpperCase(),p=String(run.pilot||'').toUpperCase();\n  // In co-op either live seat can speak on the shared radio.\n  if(typeof coopActive==='function'&&coopActive())return who;\n  return who===p?(who==='DECKER'?'COLE':who==='COLE'?'DECKER':'COLE'):who;\n}\n"+marker)
    p.write_text(s,encoding='utf-8',newline='\n')
    p=root/'assets/furious_review_0927.js';s=p.read_text(encoding='utf-8')
    s=replace(s, "who:'DECKER'", "who:missionRadioWho('DECKER')") if s.count("who:'DECKER'")==1 else s
    # Escape dialogue has multiple Decker/Cole entries; replacement is intentionally global here.
    s=s.replace("who:'DECKER',text:","who:missionRadioWho('DECKER'),text:").replace("who:'COLE',text:","who:missionRadioWho('COLE'),text:")
    p.write_text(s,encoding='utf-8',newline='\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);patch(ap.parse_args().root)
