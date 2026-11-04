window.menu113Review=function(key){
 Input.clearTaps();Input.mouse.down=false;coopOn=false;for(const k of Object.keys(Input.keys))Input.keys[k]=false;menuIndex=0;modeIndex=0;pilotPending=null;diffPending=null;diffFlash=0;campPick=null;P2M.choice=null;
 if(key==='coop-choice'){run.mode='arcade';setState(GS.MODESEL);P2M.choice='coop';P2M.row=0;}
 else if(key==='roster'){coopOn=true;p2Index=PILOTS.findIndex(p=>p.key==='axel');setState(GS.COOPROSTER);}
 else if(key==='forge'){run.mode='arcade';run.stage=6;run.spaceMode=false;run.loadout=[0,1,2,3,4,5];run.wlevels=WEAPONS.map(()=>3);run.wlevel=3;forgeStart(()=>setState(GS.TITLE));forge.t=3;}
 else if(key==='armory'){armoryOpen('title');setState(GS.ARMORY);}
 else if(key==='achievements'){awardsOpen();setState(GS.ACHIEVEMENTS);}
 else if(key==='vault'){vaultOpen();setState(GS.VAULT);}
 else{const map={title:GS.TITLE,modes:GS.MODESEL,difficulty:GS.DIFF,pilot:GS.PILOT,campaign:GS.CAMPHUB,options:GS.OPTIONS,password:GS.PASSWORD,credits:GS.CREDITS,help:GS.HELP};run.mode=key==='campaign'?'campaign':'arcade';if(key==='pilot'){pilotIndex=PILOTS.findIndex(p=>p.key==='cole');coleUnlocked=true;PILOTMOD={...PILOTS[pilotIndex]};run.pilot='cole';}setState(map[key]||GS.TITLE);}
 stateT=2;return{state,scene:ms113Scene()};
};
window.addEventListener('message',e=>{if(e.origin===location.origin&&e.data?.menu113Scene)window.menu113Review(e.data.menu113Scene);});
