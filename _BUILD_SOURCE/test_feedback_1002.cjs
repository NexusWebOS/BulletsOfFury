const fs=require('fs'),path=require('path');
/* 1002 - Mike's Stage 5 / Stage 6 notes. Pixel and audio proof is in the real-Chromium probes:
   probe_hammer_1002.py (volley/flash/no early kill), probe_hammer_intro_1002.py (the in-play arrival),
   probe_stealth_1002.py (warned stealth flights), probe_hivewing_1002.py (the Harrier's squadron),
   probe_teamscene_1002.py ("who stayed behind" + Callisto), probe_turbulence_1002.py. These pin the state
   and the source so the fixes cannot quietly come undone. */
module.exports=function(vm,ctxv,ok){
 console.log('=== 1002. Stage 5 hammer, Stage 6 flights, squadron, team scene, turbulence ===');
 const ROOT=path.join(__dirname,'..');
 let loadErr=null;
 try{vm.runInContext(fs.readFileSync(path.join(ROOT,'assets/feedback_1002.js'),'utf8'),ctxv,{filename:'feedback_1002.js'});}
 catch(e){loadErr=String(e&&e.stack||e);}
 ok(!loadErr,'1002: feedback_1002.js loads after every other layer'+(loadErr?' - '+loadErr.slice(0,160):''));
 const html=fs.readFileSync(path.join(ROOT,'index.html'),'utf8');
 const i2=html.indexOf('assets/feedback_1002.js'),i1=html.indexOf('assets/feedback_1001b.js'),ih=html.indexOf('assets/widescreen_hud_0918.js');
 ok(i2>i1&&i2<ih,'1002: index.html loads it after feedback_1001b and before the widescreen HUD');
 const png=f=>{const b=fs.readFileSync(path.join(ROOT,f));return [b.readUInt32BE(16),b.readUInt32BE(20)];};
 const game=fs.readFileSync(path.join(ROOT,'assets/game.js'),'utf8');
 ok(/if\(b\.flash>0\)\{const wim=xartTint\(key,hitFlashColor\(b,'#ffffff'\),1\)/.test(game),
   '1002 A2: the Chromium hammer pose flashes a WHITE silhouette, not a re-blit of its own plain plate');
 const out=JSON.parse(vm.runInContext(`(()=>{const o={};const keep={pilot:run.pilot,mode:run.mode,stage:run.stage,coop:coopOn,p2:run2.pilot,rnd:Math.random,boss:boss};
  try{
   /* A3 - the floor: no kill before the recovery has started */
   const b={_hammer:{restorationSeen:false},maxhp:1000,hp:120};
   o.floor=fb2HammerFloor(b);o.notDone=!fb2HammerRageDone(b);
   b._hammer.restorationSeen=true;o.doneNoArmor=fb2HammerRageDone(b);
   /* A1 - the volley never selects the hammer piece */
   o.filter=/fb2NoHammerTarget\\?a\\.filter\\(t=>!\\(t&&t\\._retinaId==='hammer'\\)\\)/.test(spaceTargets.toString());
   /* B - dispatcher rules */
   coopOn=false;
   run.pilot='cole';o.dCole=fb2Dispatcher();run.pilot='decker';o.dDecker=fb2Dispatcher();
   run.pilot='lizzie';o.dLizzie=[fb2Dispatcher(()=>.1),fb2Dispatcher(()=>.9)];
   o.coopOk=typeof coopActive==='function';
   coopOn=true;run.pilot='cole';run2.pilot='decker';o.dCD=coopActive()?fb2Dispatcher():'nocoop';
   run.pilot='decker';run2.pilot='cole';o.dDC=coopActive()?fb2Dispatcher():'nocoop';
   run.pilot='axel';run2.pilot='decker';o.dAD=coopActive()?fb2Dispatcher():'nocoop';
   coopOn=false;
   const sA=fb2HammerIntroScript('cole','decker',false),sC=fb2HammerIntroScript('cole','decker',true);
   o.introFirst=sA[0].text;o.introSecond=sA[1].text;o.introHQ=sA.some(l=>l.kind==='hq'&&/DECKER - HQ/.test(l.who));
   o.arcadeSilent=sA.filter(l=>l.kind==='boss').every(l=>/^\\.+$/.test(l.text));o.campaignCronos=sC.some(l=>l.who==='CRONOS');
   o.holdT=FB2_HOLD_T;
   /* C - roles, replacements */
   o.roleBomb=fb2MissionRole({kind:'bomb',direction:'south'});o.roleSide=fb2MissionRole({kind:'lane',direction:'east'});
   o.roleMG=fb2MissionRole({kind:'lane',direction:'south',n:2,attack:1});o.roleBlue=fb2MissionRole({kind:'lane',direction:'south',n:0,attack:null});
   run.stage=6;fb2Flights.length=0;
   o.bomberNull=spawnEnemy('s6bomber',-105,200,{_side:1,_jetManeuver:'bomb'})===null;o.bomberPlanned=fb2Flights.length===1&&fb2Flights[0].direction==='east';
   s6StrikeSpawn('south');o.strikePlanned=fb2Flights.length===2&&fb2Flights[1].direction==='south';
   o.roles=fb2Flights.map(q=>q.role);fb2Flights.length=0;
   o.strikeWrapped=/_fb2Stealth/.test(s6StrikeTick.toString());
   /* D - the squadron */
   const e={};fb2HwFace(e,Math.PI/2);o.faceDown=Math.abs(e._faceAng-Math.PI)<1e-9&&Math.abs(e.spin)<1e-9;
   o.diveHeld=/D0\\.t=0/.test(hivewingTick.toString())&&/combatWarningTick\\(e,'fb2dive'/.test(hivewingTick.toString());
   o.plays=/'pincer','missile','bracket'/.test(fb2SquadTick.toString());
   /* E - the team scene */
   s6Wing=null;run.pilot='cole';const tc=fb2TeamScript();run.pilot='lizzie';const tl=fb2TeamScript();
   o.coleKinds=tc.filter(x=>x.kind).map(x=>x.kind);o.lizKinds=tl.filter(x=>x.kind).map(x=>x.kind);
   o.rage=tc.filter(x=>x.rage).length;o.firstLine=tc[0].text;
   o.teamNotCole=tc.filter(x=>x.who&&x.emo==='sad').every(x=>x.who!=='COLE');
   o.uniqueTeam=new Set(tc.filter(x=>x.who&&x.who!=='COLE').slice(0,6).map(x=>x.who)).size;
   o.shocked=tc.filter(x=>x.emo==='crash').length;
   o.callistoText=FB2_CALLISTO.join('');
  }catch(err){o.err=String(err&&err.stack||err);}
  finally{run.pilot=keep.pilot;run.mode=keep.mode;run.stage=keep.stage;coopOn=keep.coop;run2.pilot=keep.p2;}
  return JSON.stringify(o);})()`,ctxv));
 ok(!out.err,'1002: the state checks ran'+(out.err?' - '+out.err.slice(0,240):''));
 ok(out.notDone&&out.floor===80,'1002 A3: before the hammer recovery has played, his HP has a floor ('+out.floor+' of 1000) - no kill yet');
 ok(out.doneNoArmor===true,'1002 A3: once the recovery has started (and no twirl is owed) the floor lifts');
 ok(out.filter,'1002 A1: the passive volley rack filters the hammer out of its targets');
 ok(out.dCole==='decker'&&out.dDecker==='cole','1002 B: playing Cole, Decker dispatches; playing Decker, Cole does');
 ok(out.dLizzie&&['cole','decker'].includes(out.dLizzie[0])&&['cole','decker'].includes(out.dLizzie[1])&&out.dLizzie[0]!==out.dLizzie[1],
   '1002 B: anyone else gets Cole or Decker at random ('+out.dLizzie+')');
 if(out.dCD!=='nocoop'){
  ok(out.dCD==='axel'&&out.dDC==='axel','1002 B: Cole and Decker both flying - Axel dispatches ('+out.dCD+', '+out.dDC+')');
  ok(out.dAD==='cole','1002 B: a seated Decker is never the dispatcher ('+out.dAD+')');
 }
 ok(out.introFirst==='...Who are you?'&&out.introSecond==='.........','1002 B: the pilot asks "...Who are you?" and the hammer answers "........."');
 ok(out.introHQ,'1002 B: HQ chimes in under the dispatcher\'s own name');
 ok(out.arcadeSilent&&out.campaignCronos,'1002 B: arcade keeps him silent; the campaign keeps the Cronos reveal');
 ok(out.holdT<2,'1002 B: he holds the unfolded plate below 2.0 s, where the base makes him hittable');
 for(const f of ['hammer_avatar','dispatch_cole','dispatch_decker','dispatch_axel','dispatch_lizzie','dispatch_falva']){
  const s=png('assets/game/dispatch_1002/'+f+'.png');ok(s[0]>=126&&s[0]<=128&&s[1]>=122&&s[1]<=128,'1002 B: '+f+' is a comm-box sized plate ('+s.join('x')+')');}
 ok(out.roleBomb==='green'&&out.roleSide==='green'&&out.roleMG==='orange'&&out.roleBlue===null,
   '1002 C: the assault squadron wears its role - bombers green, a Furious gun gate orange, an unarmed gate blue');
 ok(out.bomberNull&&out.bomberPlanned,'1002 C: a stage-6 s6bomber spawns nothing and plans a warned stealth flight instead');
 ok(out.strikePlanned,'1002 C: the cardinal strike passes are planned stealth flights too');
 ok(new Set(out.roles).size===2,'1002 C: consecutive flights rotate their roles ('+out.roles+')');
 ok(out.strikeWrapped,'1002 C: the strike tick hands a stealth jet to its own role tick');
 for(const r of ['red','green','orange']){const s=png('assets/game/stealth_1002/'+r+'.png');ok(s[0]===512&&s[1]===128,'1002 C: the '+r+' stealth sheet is four 128px headings ('+s.join('x')+')');}
 ok(out.faceDown,'1002 D: the escort heading helper faces nose-south for a southward vector');
 ok(out.diveHeld,'1002 D: the escort dive is held for its own warned tell, not the base 0.4 s flash');
 ok(out.plays,'1002 D: the squadron brain rotates pincer, missile and bracket plays');
 ok(out.coleKinds.join()==='callisto,demo'&&out.lizKinds.length===0,'1002 E: Callisto and the demo play for Cole only ('+out.coleKinds+' / '+out.lizKinds+')');
 ok(out.rage===3&&/WHO STAYED BEHIND AT BASE/.test(out.firstLine),'1002 E: Cole asks who stayed behind, then three rage lines in the shouting frames');
 ok(out.teamNotCole&&out.uniqueTeam>=5,'1002 E: the heads-down lines come from the team, at least five different pilots ('+out.uniqueTeam+')');
 ok(out.shocked>=4,'1002 E: the team reacts in shock after the demo');
 ok(out.callistoText==='SECRET WEAPON CALLISTOWEAPON STATUS = ACTIVATED','1002 E: the banner reads SECRET WEAPON CALLISTO / WEAPON STATUS = ACTIVATED');
 for(let i=0;i<3;i++){const s=png('assets/game/dispatch_1002/cole_rage_'+i+'.png');ok(s[0]===128&&s[1]===128,'1002 E: cole_rage_'+i+' is 128x128');}
 for(const f of ['turbulence_carrier_1002.mp3','jetwash_1002.mp3'])ok(fs.statSync(path.join(ROOT,'assets/game/sounds',f)).size>4000,'1002 F: '+f+' ships');
 const src=fs.readFileSync(path.join(ROOT,'assets/feedback_1002.js'),'utf8');
 ok(/name==='carrierTurbine'\)FB2_LOOPON\.call\(this,'turbCarrier1002'/.test(src)&&/name==='carrierTurbine'\)FB2_LOOPOFF\.call\(this,'turbCarrier1002'\)/.test(src),
   '1002 F: the turbulence loop rides the carrier turbine\'s own on/off calls');
 ok(!/getImageData/.test(src.replace(/\/\*[\s\S]*?\*\//g,'')),'1002: nothing in this layer reads pixels at runtime (file:// refuses it)');
};
