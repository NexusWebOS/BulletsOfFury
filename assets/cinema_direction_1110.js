'use strict';
/* Authored comic cinema. Rewards, campaign continuation, combat, and saves retain
   their native owners. Scaling/slide-ins are scoped to Mike's requested cinema. */
const D1110_SCENES={"opening":{"id":"opening","title":"01 / The day the sky changed","where":"Before Stage 1","purpose":"Establish peace, the crew, the takeover, and a pilot who can still act.","status":"Draft direction","shots":[{"id":"O01","duration":6,"art":"peace","speaker":"CAPTION","dialogue":"For a time, Earth was at peace.","readings":[],"layout":"plate","people":[],"frame":0,"bank":"city-takeover","clip":[0,1],"times":[1200,100000],"hold":1},{"id":"O02","duration":6,"art":"hangar","speaker":"CAPTION","dialogue":"In secret, Fury Division brought together the world’s best pilots.","readings":[],"layout":"plate","people":[],"frame":0},{"id":"O03","duration":8,"art":"concept","speaker":"COLE","dialogue":"That request came from outside the test rig.","readings":[],"layout":"panel","people":[],"frame":0,"bank":"command-work","clip":[0,1,0,1,2,3],"times":[250,150,250,150,250,100000]},{"id":"O04","duration":6,"art":"comic","speaker":"AXEL","dialogue":"Same check?","readings":[],"layout":"panel","people":["axel","freezer"],"frame":0,"bank":"axel-freezer-check","clip":[0,1,2,3,4,5]},{"id":"O05","duration":6,"art":"hangar","speaker":"LIZZIE","dialogue":"Together.","readings":[],"layout":"panel","people":["falva","lizzie"],"frame":0,"bank":"sisters-repair"},{"id":"O06","duration":3,"art":"lounge","speaker":"YURI","dialogue":"","readings":[],"layout":"panel","people":["maverick","juggernaut","yuri"],"frame":0,"bank":"yuri-maverick-preflight"},{"id":"O06B","duration":3,"art":"lounge","speaker":"JUGGERNAUT","dialogue":"","layout":"panel","bank":"juggernaut-help","readings":[],"clip":[0,1,2,3,4,5]},{"id":"O07","duration":8,"art":"collapse","speaker":"FURY RADIO","dialogue":"Emergency traffic. All sectors reporting control failures.","readings":[],"layout":"panel","people":[],"frame":0,"bank":"city-takeover","clip":[2,3,4,5],"times":[800,550,350,100000],"cue":"stage3AtomicSiren","cueAt":0.75},{"id":"O08","duration":7,"art":"command","speaker":"DECKER","dialogue":"Same command. Transport, utilities, defense.","readings":["REMOTE COMMAND: UNAUTHORIZED","MULTIPLE SYSTEMS: MATCH"],"layout":"radar","people":[],"frame":0,"bank":"radar-acquisition","clip":[0,1],"times":[1200,100000]},{"id":"O09","duration":7,"art":"concept","speaker":"COLE","dialogue":"Cut remote command authority. Confirm local flight control.","readings":["REMOTE AUTHORITY: DISCONNECTED","LOCAL FLIGHT CONTROL: READY"],"layout":"panel","people":[],"frame":0,"bank":"command-work","clip":[4,5],"times":[600,100000]},{"id":"O10","duration":7,"art":"comic","speaker":"COLE","dialogue":"Get people clear. Keep your controls local. Launch.","readings":[],"layout":"duo","people":["cole","decker"],"frame":0},{"id":"O11","duration":8,"art":"hangar","speaker":"FURY FLIGHT","dialogue":"","readings":[],"layout":"flight","people":["$pilot","$partner"],"frame":0,"ship":"board","cue":"crackle"},{"id":"O12","duration":8,"art":"sky","speaker":"COLE","dialogue":"Fury flight, report.","readings":[],"layout":"flight","people":[],"frame":0,"ship":"launch","cue":"jetDash"},{"id":"O13","duration":7,"art":"comic","speaker":"FURY SYSTEM","dialogue":"Squad channel lost. Local control responding.","readings":["SQUAD CHANNEL: LOST","LOCAL CONTROL: RESPONDING"],"layout":"duo","people":["$pilot"],"frame":0,"bank":null},{"id":"O14","duration":6,"art":"coast","speaker":"PILOT","dialogue":"Controls are mine. Heading into the city.","readings":["CLEAR THE COASTAL ROUTE"],"layout":"flight","people":[],"frame":0,"ship":"launch","title":true,"cue":"jetDash"}],"duration":96},"post1":{"id":"post1","title":"02 / Follow the transmission","where":"After Stage 1 → volcanic belt","purpose":"A captured transmission supplies a bearing while squad comms remain lost.","status":"Draft direction","shots":[{"id":"B101","duration":5,"art":"coast","speaker":"PILOT","dialogue":"The local battery’s quiet.","readings":[],"layout":"plate","people":[],"frame":0},{"id":"B102","duration":6,"art":"comic","speaker":"FURY RECORDER","dialogue":"Repeating transmission. Surface reply detected.","readings":["TRANSMISSION INTERVAL: MATCH","SURFACE REPLY: VOLCANIC BELT"],"layout":"duo","people":["$pilot"],"frame":0},{"id":"B103","duration":5,"art":"lava","speaker":"PILOT","dialogue":"Strongest return is over the volcanic belt.","readings":[],"layout":"plate","people":[],"frame":0},{"id":"B104","duration":6,"art":"lava","speaker":"PILOT","dialogue":"Following it.","readings":[],"layout":"flight","people":[],"frame":0,"ship":"launch"}],"duration":22},"post2":{"id":"post2","title":"03 / A voice on the channel","where":"After Stage 2 → dish → frozen region","purpose":"A physical service connection restores limited navigation and friendly tracks.","status":"Draft direction","shots":[{"id":"B201","duration":6,"art":"dish","speaker":"PILOT","dialogue":"That service dish still has power.","readings":[],"layout":"plate","people":[],"frame":0,"ship":null},{"id":"B202","duration":7,"art":"dish","speaker":"PILOT","dialogue":"Service port matches. Isolating the line.","readings":[],"layout":"panel","people":[],"frame":0,"bank":"service-connector","cue":"crackle","cueAt":1.25},{"id":"B203","duration":6,"art":"dish","speaker":"FURY SYSTEM","dialogue":"Navigation restored. Squad signals: partial.","readings":["LOCAL POWER: STABLE","NAV RESTORED / SQUAD SIGNALS: PARTIAL"],"layout":"radar","people":[],"frame":0,"bank":"radar-acquisition","clip":[0],"times":[100000]},{"id":"B204","duration":5,"art":"comic","speaker":"TECH","dialogue":"We’ve got you. The others are ahead, near the base.","readings":[],"layout":"duo","people":["$pilot","$tech"],"frame":0},{"id":"B205","duration":6,"art":"freeze","speaker":"PILOT","dialogue":"That ground was bare a moment ago.","readings":[],"layout":"flight","people":[],"frame":3,"ship":"launch"}],"duration":30},"post3":{"id":"post3","title":"04 / Twenty miles east","where":"After Stage 3 → HQ → airbase","purpose":"A powered base and a launch-time correlation become the next lead.","status":"Draft direction","shots":[{"id":"B301","duration":6,"art":"hangar","speaker":"COLE","dialogue":"Everyone accounted for. Bring up the recorder.","readings":[],"layout":"flight","people":[],"frame":0,"ship":"land"},{"id":"B302","duration":6,"art":"command","speaker":"DECKER","dialogue":"Flight computers isolated. Remote commands have no authority.","readings":["SQUAD CHANNELS: RESTORED","REMOTE AUTHORITY: DISCONNECTED"],"layout":"radar","people":[],"frame":0,"bank":"radar-acquisition","clip":[0],"times":[100000]},{"id":"B303","duration":7,"art":"concept","speaker":"COLE","dialogue":"Compare the launch time with the first outages.","readings":[],"layout":"panel","people":[],"frame":0,"bank":"command-work","clip":[0,1,2,3],"times":[200,150,250,100000]},{"id":"B304","duration":7,"art":"concept","speaker":"DECKER","dialogue":"Just before them. And the pad still has power.","readings":["AIRBASE: POWER PRESENT","LAUNCH EVENT: BEFORE FIRST OUTAGE"],"layout":"panel","people":[],"frame":1,"bank":"command-work","clip":[3],"times":[100000]},{"id":"B305","duration":6,"art":"concept","speaker":"COLE","dialogue":"Twenty miles east. We recover the launch records.","readings":[],"layout":"panel","people":[],"frame":2,"bank":"command-work","clip":[5],"times":[100000]}],"duration":32},"post4":{"id":"post4","title":"05 / The recovered recording","where":"After Stage 4 → Stage 5 orbit","purpose":"The archive reveals the satellite takeover; the Federation attachment supplies a way up.","status":"Draft direction","shots":[{"id":"B401","duration":6,"art":"pad","speaker":"TECH","dialogue":"Launch archive. Last satellite uplink. Open it locally.","readings":[],"layout":"duo","people":["$pilot","$tech"],"frame":0},{"id":"B402","duration":6,"art":"pad","speaker":"PILOT","dialogue":"Found the recorder. Sending the captured file.","readings":["ARCHIVE COPY: ISOLATED","ORBITAL CONTACT: RECORDED"],"layout":"plate","people":[],"frame":0},{"id":"B403","duration":6,"art":"orbital-relay","speaker":"ARCHIVE","dialogue":"","readings":["RELAY STATUS: NOMINAL","SOURCE: ISOLATED RECORDING"],"layout":"panel","people":[],"frame":2,"bank":"satellite-takeover","clip":[0,1,2,3,4],"times":[1000,900,900,1000,100000],"cue":"bossWeaponCharge","cueAt":1},{"id":"B404","duration":1.6,"art":"orbital-relay","speaker":"ARCHIVE","dialogue":"","readings":["CONTROL AUTHORITY: OVERRIDDEN","HOSTILE CODE: DOWNLINK ACTIVE"],"layout":"panel","people":[],"frame":3,"bank":"satellite-takeover","clip":[5],"times":[100000],"cue":"crackle","cueAt":0.08},{"id":"B404R","duration":2.4,"art":"command","speaker":"DECKER","dialogue":"","bank":"decker-reaction","layout":"panel","clip":[0,1,2,3,4,5],"times":[80,100,220,450,500,100000],"readings":[]},{"id":"B405","duration":7,"art":"comic","speaker":"DECKER","dialogue":"Symbiote code. It seized the satellite, then used its downlink to spread commands to Earth.","readings":[],"layout":"panel","people":["decker","cole"],"frame":0,"bank":"decker-reaction","clip":[5],"times":[100000]},{"id":"B406","duration":7,"art":"pad","speaker":"TECH","dialogue":"Federation prototype. It fits our fighters. Let’s check the seals.","readings":["ATTACHMENT LOCKED","LIFE SUPPORT: READY"],"layout":"flight","people":[],"frame":0,"ship":"board"},{"id":"B407","duration":8,"art":"earth","speaker":"COLE","dialogue":"Answers are up there. We’re going.","readings":[],"layout":"flight","people":[],"frame":0,"ship":"launch","cue":"jetDash"}],"duration":44.0},"post5":{"id":"post5","title":"06 / Home, for one night","where":"After Stage 5 → invasion scramble","purpose":"Let relief register; radar acquisitions then force the crew back into the sky.","status":"Draft direction","shots":[{"id":"B501","duration":6,"art":"earth","speaker":"PILOT","dialogue":"Chronos is down. Bringing the salvage home.","readings":[],"layout":"flight","people":[],"frame":0,"ship":"return"},{"id":"B502","duration":6,"art":"hangar","speaker":"COLE","dialogue":"Good to have you back.","readings":[],"layout":"flight","people":[],"frame":0,"ship":"land"},{"id":"B503","duration":7,"art":"forge","speaker":"DECKER","dialogue":"That rotary assembly survived? Leave it with me.","readings":[],"layout":"panel","people":[],"frame":0,"bank":"command-work","clip":[0,1,0,1,5],"times":[200,120,200,120,100000]},{"id":"B504","duration":5,"art":"forge","speaker":"JUGGERNAUT","dialogue":"Now that’s heavy metal.","readings":[],"layout":"duo","people":["juggernaut","decker"],"frame":0},{"id":"B505","duration":8,"art":"alarm","speaker":"DECKER","dialogue":"Those returns are real. They’re descending toward the city.","readings":["HOSTILE TRACKS: ACQUIRING","DESCENT VECTOR: CITY"],"layout":"panel","people":[],"frame":0,"bank":"radar-acquisition","clip":[0,1,2,3,4],"times":[700,700,1100,1200,100000],"cue":"stage3AtomicSiren","cueAt":4.7},{"id":"B506","duration":6,"art":"alarm","speaker":"COLE","dialogue":"[Guard names], hold HQ. Everyone else, launch. Now.","readings":[],"layout":"panel","people":[],"frame":3,"bank":"radar-acquisition","clip":[5],"times":[100000],"cue":"expBig","cueAt":0.08},{"id":"B507","duration":8,"art":"sky","speaker":"FURY FLIGHT","dialogue":"","readings":[],"layout":"flight","people":[],"frame":0,"ship":"launch","cue":"jetDash"}],"duration":46},"route":{"id":"route","title":"07 / A choice in the sky","where":"Stage 6 route decision","purpose":"Make the two threat vectors legible before the player chooses.","status":"Draft direction","shots":[{"id":"R01","duration":6,"art":"sky","speaker":"TECH","dialogue":"Harrier to the left. Rough Riders to the right.","readings":["LEFT: HARRIER / CARRIER","RIGHT: ROUGH RIDERS"],"layout":"plate","people":[],"frame":0},{"id":"R02","duration":6,"art":"comic","speaker":"PILOT","dialogue":"Mark both. We’re taking this approach.","readings":[],"layout":"duo","people":["$pilot","$tech"],"frame":0}],"duration":12},"post6":{"id":"post6","title":"08 / Below the streets","where":"After Stage 6 → river / sewer","purpose":"Confirm the chosen outcome, preserve optional pursuit, then locate a distinct underground source.","status":"Draft direction","shots":[{"id":"B601","duration":5,"art":"sky","speaker":"TECH","dialogue":"$routeReport","readings":[],"layout":"plate","people":[],"frame":0},{"id":"B602","duration":5,"art":"command","speaker":"COLE","dialogue":"Keep the remaining contacts marked. Show me the new signal.","readings":[],"layout":"plate","people":[],"frame":0},{"id":"B603","duration":6,"art":"command","speaker":"DECKER","dialogue":"No altitude match.","readings":["AIR SCAN: NO MATCH","SEARCH PLANE: SUBSURFACE"],"layout":"radar","people":[],"frame":0,"bank":"radar-acquisition","clip":[0],"times":[100000]},{"id":"B604","duration":6,"art":"river","speaker":"DECKER","dialogue":"There. Under the bridge. Inside the sewers.","readings":["SUBSURFACE SOURCE: RIVER ACCESS"],"layout":"plate","people":[],"frame":0},{"id":"B605","duration":6,"art":"sewer","speaker":"PILOT","dialogue":"Taking the river approach. Keep the channel open.","readings":[],"layout":"flight","people":[],"frame":0,"ship":"launch"}],"duration":28},"stagex":{"id":"stagex","title":"09 / The marked contact","where":"Optional Stage X","purpose":"Use the contact, wingmen, and encounter outcome actually selected.","status":"Draft direction","shots":[{"id":"X01","duration":5,"art":"sky","speaker":"TECH","dialogue":"Marked contact confirmed. Your wingmen are with you.","readings":[],"layout":"plate","people":[],"frame":0},{"id":"X02","duration":6,"art":"comic","speaker":"PILOT","dialogue":"Stand down. We can still end this.","readings":[],"layout":"duo","people":["$pilot","$tech"],"frame":0},{"id":"X03","duration":5,"art":"sky","speaker":"FURY SYSTEM","dialogue":"Contact resolved. Return vector held.","readings":[],"layout":"plate","people":[],"frame":0}],"duration":16},"post7":{"id":"post7","title":"10 / Leave the channel open","where":"After Stage 7 → Stage 8","purpose":"The portal separates the pilot from the crew. Silence provides the cliffhanger.","status":"Draft direction","shots":[{"id":"B701","duration":6,"art":"sewer","speaker":"PILOT","dialogue":"","readings":[],"layout":"flight","people":[],"frame":0,"portal":true,"ship":"launch"},{"id":"B702","duration":6,"art":"command","speaker":"DECKER","dialogue":"Beacon lost. No weapons telemetry.","readings":["FURY TRANSPONDER: NO SIGNAL"],"layout":"radar","people":[],"frame":0,"bank":"radar-acquisition","clip":[0],"times":[100000]},{"id":"B703","duration":6,"art":"comic","speaker":"COLE","dialogue":"Keep the recorder on that vector. Leave the channel open.","readings":[],"layout":"duo","people":["cole","decker"],"frame":0}],"duration":18},"bonus":{"id":"bonus","title":"11 / The detour","where":"Stage 9, when available","purpose":"Give the optional excursion an entry and a return without inventing a new finale.","status":"Draft direction","shots":[{"id":"Q01","duration":5,"art":"earth","speaker":"TECH","dialogue":"Detour marked. Holding your return vector.","readings":[],"layout":"plate","people":[],"frame":0},{"id":"Q02","duration":5,"art":"earth","speaker":"PILOT","dialogue":"Detour clear. Returning to course.","readings":["DETOUR CLEAR / RETURN VECTOR HELD"],"layout":"flight","people":[],"frame":0,"ship":"return"}],"duration":10},"milestone":{"id":"milestone","title":"12 / A mission completed","where":"Easy / Normal milestone ending","purpose":"Complete the Chronos achievement and offer the existing continuation route.","status":"Draft direction","shots":[{"id":"M01","duration":6,"art":"earth","speaker":"PILOT","dialogue":"Chronos is down. Salvage secured.","readings":[],"layout":"flight","people":[],"frame":0,"ship":"return"},{"id":"M02","duration":6,"art":"hangar","speaker":"COLE","dialogue":"Bring it home. We’ve got more work ahead.","readings":[],"layout":"plate","people":[],"frame":0},{"id":"M03","duration":6,"art":"lounge","speaker":"FURY COMMAND","dialogue":"Mission complete.","readings":[],"layout":"plate","people":[],"frame":0}],"duration":18},"ending":{"id":"ending","title":"13 / Everyone accounted for","where":"True victory → credits","purpose":"Resolve the attack and the crew’s interrupted human lives.","status":"Draft direction","shots":[{"id":"E01","duration":7,"art":"earth","speaker":"PILOT","dialogue":"Fury flight. Anyone receiving?","readings":["COMMAND UPLINK: SILENT"],"layout":"flight","people":[],"frame":0,"ship":"return"},{"id":"E02","duration":7,"art":"concept","speaker":"DECKER","dialogue":"We’ve got you.","readings":["FURY TRANSPONDER: RECEIVING"],"layout":"panel","people":[],"frame":0,"bank":"command-work","clip":[0,1,3],"times":[300,300,100000]},{"id":"E03","duration":9,"art":"hangar","speaker":"FURY FLIGHT","dialogue":"","readings":[],"layout":"flight","people":[],"frame":0,"ship":"land"},{"id":"E04","duration":8,"art":"peace","speaker":"DECKER","dialogue":"Command traffic has stopped. Bringing clean systems back locally.","readings":[],"layout":"panel","people":[],"frame":0,"bank":"city-takeover","clip":[1],"times":[100000]},{"id":"E05","duration":8,"art":"comic","speaker":"COLE","dialogue":"Everyone accounted for.","readings":[],"layout":"panel","people":["cole","decker"],"frame":0,"bank":"cole-decker-homecoming"},{"id":"E06","duration":8,"art":"lounge","speaker":"AXEL","dialogue":"Stand down.","readings":[],"layout":"panel","people":["axel","freezer"],"frame":0,"bank":"axel-freezer-check","clip":[4,5],"times":[350,100000]},{"id":"E07","duration":8,"art":"hangar","speaker":"LIZZIE","dialogue":"Think he’d have believed this?","readings":[],"layout":"panel","people":["falva","lizzie"],"frame":0,"bank":"sisters-home-hangar"},{"id":"E08","duration":8,"art":"lounge","speaker":"MAVERICK","dialogue":"Same time tomorrow?","readings":[],"layout":"panel","people":["maverick","juggernaut"],"frame":0,"bank":"juggernaut-guitar"},{"id":"E09","duration":9,"art":"command","speaker":"COLE","dialogue":"Get some sleep. We can fix the rest tomorrow.","readings":[],"layout":"panel","people":[],"frame":0,"bank":"cole-decker-homecoming","clip":[5],"times":[100000]}],"duration":72},"sting":{"id":"sting","title":"14 / An isolated echo","where":"Optional, after credits","purpose":"Retain the sequel hook while Earth’s victory remains real.","status":"Draft direction","shots":[{"id":"S01","duration":4,"art":"relay","speaker":"CAPTION","dialogue":"A severed relay. No uplink.","readings":[],"layout":"plate","people":[],"frame":0},{"id":"S02","duration":3,"art":"earth","speaker":"FEDERATION SENSOR","dialogue":"Unknown contact. Outer system.","readings":["EARTH COMMAND SIGNAL: SILENT","OUTER SYSTEM: UNKNOWN CONTACT"],"layout":"plate","people":[],"frame":0},{"id":"S03","duration":3,"art":"relay","speaker":"CAPTION","dialogue":"Bullets of Fury will return.","readings":[],"layout":"plate","people":[],"frame":0}],"duration":10}};
const D1110={version:1,revision:2,W:912,H:512,pilots:D1110_ART.pilots,events:[],last:null,paused:false,static:false,
 base:{introStart:campaignIntroStart,introFinish:campaignIntroFinish,introDraw:drawCampaignIntro,preview:C22.preview,storyPreview:S113.preview,
  script:s113Script,keys:s113Keys,play:s113Play,start:BOFCinematicDirector.start,
  tick:BOFCinematicDirector.tick,draw:BOFCinematicDirector.draw,bank:s113Bank,
  victory:drawVictory,trigger:triggerVictory,endingKeys:victoryEndingKeys,load:stageLoadBegin,battle:s113Battle,portalHandoff:cf4PortalHandoff},
 ending:null};
for(const a of Object.values(D1110_ART.banks))XART._src[a.key]=a.path;
Snd.prepare?.(['blip','crackle','jetDash','stage3AtomicSiren','dracodiaShriek','bossWeaponCharge','expBig']);
function d1110Event(kind,data={}){D1110.events.push({kind,...data});if(D1110.events.length>256)D1110.events.shift();}
function d1110Viewport(){s113Viewport();ctx.imageSmoothingEnabled=false;}
function d1110Active(p=run.pilot){return [...new Set([p,...(coopActive()?[p2Pilot().key]:[])])].filter(k=>D1110.pilots.includes(k));}
function d1110Tech(p=run.pilot){return d1110Active(p).includes('decker')?'cole':'decker';}
function d1110Crew(p=run.pilot){const active=d1110Active(p),guards=['decker','axel','freezer','juggernaut','lizzie','yuri','falva','maverick'].filter(k=>!active.includes(k)).slice(0,2);
 const flying=[...new Set([...active,'cole','axel','freezer','yuri','maverick','falva','lizzie','juggernaut','decker'])].filter(k=>!guards.includes(k)).slice(0,5);return {active,guards,flying};}
s113Crew=d1110Crew;
function d1110Resolve(s,p,route){return String(s||'').replace('[Guard names]',d1110Crew(p).guards.map(k=>k.toUpperCase()).join(' and ')).replace('$routeReport',route==='left'?'The Harrier is down. The remaining Rough Rider contacts are marked.':'The Rough Riders are down. The remaining Harrier threat is marked.');}
function d1110Who(k,p){return k==='PILOT'?p.toUpperCase():k==='TECH'?d1110Tech(p).toUpperCase():k;}
function d1110Clone(id,p=run.pilot,route=s113Route()){
 const scene=D1110_SCENES[id];if(!scene)return [];
 return scene.shots.map(raw=>{const b={...raw,d1110:true,who:d1110Who(raw.speaker,p),text:d1110Resolve(raw.dialogue,p,route),readings:[...(raw.readings||[])],people:[...(raw.people||[])],bg:'s113_'+({dish:'volcanic-dish',pad:'launch-pad',command:'command-bay'}[raw.art]||raw.art),_cueSet:new Set()};
  if(id==='post4'&&d1110Active(p).includes('decker')&&b.bank==='decker-reaction'){b.bank=null;b.art='pad';b.layout='duo';b.people=['decker','cole'];}
  if(id==='post4'&&d1110Active(p).includes('decker')&&d1110Active(p).includes('cole')&&b.layout==='duo')b.people=['cole','decker'];return b;});
}
function d1110Post(n,p=run.pilot,route=s113Route()){
 const id={1:'post1',2:'post2',3:'post3',4:'post4',5:'post5',6:'post6',7:'post7',9:'bonus'}[n];
 if(!id)return D1110.base.script(n,p,route);
 const rows=d1110Clone(id,p,route);
 // Preserve the established earned-loadout explanation without granting an item here.
 if([2,3,4,5,6,9].includes(n)){
  const upgrades=BOFCinematicDirector.upgrade(n,p).map((b,i)=>({...b,d1110:true,id:'upgrade-'+n+'-'+i,art:'forge',layout:'duo',duration:Math.max(4.5,b.text.length/38+1.8),readings:[],people:[p,d1110Tech(p)],_cueSet:new Set()}));
  const at=n===5?3:Math.max(1,rows.length-1);rows.splice(at,0,...upgrades);
 }
 return rows;
}
s113Script=d1110Post;BOFCinematicDirector.script=d1110Post;BOFCampaignStory.script=d1110Post;
function d1110Names(b,p=run.pilot){const names=[];if(b.bank)names.push(b.bank);
 if(b.bank){const context={
  'command-work':['radar-acquisition'], 'radar-acquisition':['command-work'], 'city-takeover':['city-takeover'],
  'satellite-takeover':['decker-reaction'],'decker-reaction':['satellite-takeover'],
  'juggernaut-guitar':['cole-decker-homecoming'],'sisters-home-hangar':['sisters-home-hangar']};names.push(...(context[b.bank]||[]));
  const pair={'axel-freezer-check':['axel','freezer'],'sisters-repair':['falva','lizzie'],'yuri-maverick-preflight':['yuri','maverick'],'juggernaut-help':['juggernaut']}[b.bank];
  if(pair)for(const pk of pair)names.push('native-'+pk+'-front');
  if(['service-connector','cole-decker-homecoming'].includes(b.bank))names.push(p+'-aircraft-landing');
 }
 if(b.layout==='duo'||b.layout==='trio')for(const k of b.people||[p,d1110Tech(p)]){const pk=k==='$pilot'?p:k==='$tech'?d1110Tech(p):k==='$partner'?(d1110Active(p)[1]||p):k;if(D1110.pilots.includes(pk))names.push('face-'+pk);}
 if(b.layout==='flight'||b.ship||b.art==='hangar')for(const pk of d1110Active(p))names.push(pk+'-aircraft-landing','native-'+pk+'-front','native-'+pk+'-rear','native-'+pk+'-top');
 if(b.layout==='radar')names.push('radar-acquisition');return [...new Set(names)];}
function d1110Keys(rows,p=run.pilot){const keys=['dlg_window','ui20_dialogue-a','nbl_logo_0916'];
 for(const b of rows){for(const name of d1110Names(b,p)){const a=D1110_ART.banks[name];if(a)keys.push(a.key);}
  {const name={dish:'volcanic-dish',pad:'launch-pad',command:'command-bay',cockpit:'cockpit-'+p,comic:'comic-backdrop'}[b.art]||b.art;
   const a=S113_ART.banks[name];if(a)keys.push(a.key);else if(C22_ART.images[{peace:'peace_city',collapse:'civilian_collapse',coast:'coast_invasion',lava:'lava_relay'}[b.art]])keys.push(C22_ART.images[{peace:'peace_city',collapse:'civilian_collapse',coast:'coast_invasion',lava:'lava_relay'}[b.art]].key);
  }
  if(b.bank==='command-work')keys.push(C22_ART.images.desert_airbase.key);
  if(['land','board'].includes(b.ship)||b.art==='hangar'||['O12','B507'].includes(b.id))keys.push(D1110_ART.banks['hq-overhead-bay'].key);
  if(b.art==='relay')keys.push(CE20_ART.relay.key);
  if(b.portal)keys.push(C22_ART.banks.blue_portal.key);
 }
 return [...new Set(keys)];}
s113Keys=function(rows){if(rows.some(b=>b.d1110))return d1110Keys(rows);const keys=D1110.base.keys(rows);
 if(rows.some(b=>b.battle||b.flight))for(const p of d1110Crew().flying)for(const name of ['native-'+p+'-front','native-'+p+'-rear',p+'-aircraft-landing'])keys.push(D1110_ART.banks[name].key);return [...new Set(keys)];};
function d1110Ready(keys){let ready=bmfReady('dialogue');for(const k of keys)if(!XART.rdy(k))ready=false;return ready;}
function d1110Play(id,rows,done){if(!rows.length)return false;const keys=d1110Keys(rows);d1110Ready(keys);
 const ok=BOFCinematicDirector.play(id,rows,done);if(ok){const s=BOFCinematicDirector.current;s.d1110Keys=keys;s.d1110Wait=0;s.md=!!Input.mouse.down;d1110Viewport();d1110Event('scene-start',{id,pilot:run.pilot});}return ok;}
s113Play=function(id,rows,done){return rows.some(b=>b.d1110)?d1110Play(id,rows,done):D1110.base.play(id,rows,done);};
BOFCinematicDirector.start=function(n,done){if(run.mode!=='campaign')return false;
 if([1,7,9].includes(n))return d1110Play('post-'+n,d1110Post(n),done);
 return D1110.base.start(n,done);
};
BOFCampaignStory.start=(n,done)=>BOFCinematicDirector.start(n,done);
// The Warden's live escape bypasses ordinary results/debrief hooks. Insert the
// authored portal beat before returning to its one native settlement/arrival.
cf4PortalHandoff=function(result){
 if(run.mode!=='campaign'||run.stage!==7||CF4.portal)return D1110.base.portalHandoff.apply(this,arguments);
 if(D1110.portalPending?.scene===BOFCinematicDirector.current)return;
 const pending={result,scene:null};D1110.portalPending=pending;
 const done=()=>{if(D1110.portalPending!==pending)return;D1110.portalPending=null;D1110.base.portalHandoff(result);};
 if(BOFCinematicDirector.start(7,done))pending.scene=BOFCinematicDirector.current;else done();
};
function d1110Bank(name,f=0,x=0,y=0,w,h){const a=D1110_ART.banks[name];if(!a||!XART.rdy(a.key))return false;
 f=clamp(Math.floor(f),0,a.frames-1);w=w??a.w;h=h??a.h;
 ctx.drawImage(XART.get(a.key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,Math.round(x),Math.round(y),Math.round(w),Math.round(h));
 return true;}
function d1110Native(pk,view,x,y,size){const name='native-'+pk+'-'+view,a=D1110_ART.banks[name];if(!a)return false;const k=size/Math.max(a.w,a.h);return d1110Bank(name,0,x-a.w*k/2,y-a.h*k/2,a.w*k,a.h*k);}
function d1110Plane(pk,f,x,y,size){return d1110Bank(pk+'-aircraft-landing',f,x-size/2,y-size/2,size,size);}
// Remove generated lookalike flight banks at the existing cinematic call sites.
s113Bank=function(name,f=0,x=456,y=256){const m=/^(landing|return|launch|flight)-(.+)$/.exec(name);
 if(m&&D1110.pilots.includes(m[2])){const [_,kind,p]=m;
  if(kind==='flight')return d1110Native(p,'front',x,y,240);
  const index=kind==='landing'?Math.min(5,Math.floor(f/5.34)):kind==='launch'?5-Math.min(5,Math.floor(f/8)):Math.min(3,Math.floor(f/8));
  return d1110Plane(p,index,x,y,kind==='landing'?128:256);
 }
 return D1110.base.bank.apply(this,arguments);
};
function d1110Frame(b,t){if(D1110.static)return b.hold??b.clip?.at(-1)??0;const a=D1110_ART.banks[b.bank],clip=b.clip||Array.from({length:a?.frames||1},(_,i)=>i);
 const times=b.times||clip.map((_,i)=>i===clip.length-1?100000:280);let ms=Math.max(0,t-(b.delay||.35))*1000;
 for(let i=0;i<clip.length;i++){if(ms<times[i])return clip[i];ms-=times[i];}return clip.at(-1);}
function d1110Plate(b,t){const H=D1110.visualH||392,name={dish:'volcanic-dish',pad:'launch-pad',command:'command-bay',cockpit:'cockpit-'+run.pilot,comic:'comic-backdrop'}[b.art]||b.art;
 if(['land','board'].includes(b.ship)||b.art==='hangar'||['O12','B507'].includes(b.id)){const a=D1110_ART.banks['hq-overhead-bay'];if(a&&XART.rdy(a.key)){ctx.drawImage(XART.get(a.key),0,0,a.w,a.h,0,0,912,608);return;}}
 if(b.art==='relay'&&XART.rdy(CE20_ART.relay.key)){const a=CE20_ART.relay,k=Math.max(912/a.w,392/a.h);ctx.drawImage(XART.get(a.key),Math.round((912-a.w*k)/2),Math.round((392-a.h*k)/2),Math.round(a.w*k),Math.round(a.h*k));return;}
 const a=S113_ART.banks[name];if(a){const f=b.frame||0,k=Math.max(912/a.w,H/a.h),w=a.w*k,h=a.h*k;
  if(XART.rdy(a.key))ctx.drawImage(XART.get(a.key),(f%a.cols)*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,Math.round((912-w)/2),Math.round((H-h)*.2),Math.round(w),Math.round(h));return;}
 const legacy=C22_ART.images[{peace:'peace_city',collapse:'civilian_collapse',coast:'coast_invasion',lava:'lava_relay'}[b.art]];
 if(legacy&&XART.rdy(legacy.key)){const k=Math.max(912/legacy.w,H/legacy.h);ctx.drawImage(XART.get(legacy.key),Math.round((912-legacy.w*k)/2),Math.round((H-legacy.h*k)/2),Math.round(legacy.w*k),Math.round(legacy.h*k));}
}
function d1110Inset(name,f=0,y=12,size=368){const a=D1110_ART.banks[name];if(!a)return;d1110Bank(name,f,532,y,size,size*a.h/a.w);}
function d1110Context(b,t,f){
 const p=run.pilot;
 if(b.bank==='command-work'){
  if(/^B30[3-5]$/.test(b.id)){const a=C22_ART.images.desert_airbase;if(XART.rdy(a.key))ctx.drawImage(XART.get(a.key),532,12,368,Math.round(368*a.h/a.w));}
  else d1110Inset('radar-acquisition',0,12,368);
 }else if(b.bank==='radar-acquisition'){
  const a=D1110_ART.banks['radar-acquisition'];if(XART.rdy(a.key))ctx.drawImage(XART.get(a.key),f%a.cols*a.w+62,Math.floor(f/a.cols)*a.h+70,384,264,532,16,368,253);
 }else if(b.bank==='satellite-takeover')d1110Bank('decker-reaction',f===5?2:0,574,12,284,284);
 else if(b.bank==='decker-reaction')d1110Inset('satellite-takeover',5);
 else if(b.bank==='city-takeover')d1110Inset('city-takeover',0);
 else if(b.bank==='sisters-home-hangar')d1110Inset('sisters-home-hangar',Math.min(4,f));
 else if(b.bank==='juggernaut-guitar')d1110Inset('cole-decker-homecoming',5);
 else if(['service-connector','cole-decker-homecoming'].includes(b.bank))d1110Plane(p,5,716,177,352);
 else{
  const pair={'axel-freezer-check':['axel','freezer'],'sisters-repair':['falva','lizzie'],'yuri-maverick-preflight':['yuri','maverick'],'juggernaut-help':['juggernaut']}[b.bank]||[p];
  pair.forEach((pk,i)=>d1110Native(pk,'front',716,pair.length===1?180:100+i*180,280));
 }
}
function d1110Face(pk,x,y,t,speaking,size=384){const f=D1110.static||!speaking?0:[0,1,2,1,3,1][Math.floor(t*8)%6];return d1110Bank('face-'+pk,f,x,y,size,size);}
function d1110People(b){const p=run.pilot;return [...new Set((b.people||[p,d1110Tech(p)]).map(k=>k==='$pilot'?p:k==='$tech'?d1110Tech(p):k==='$partner'?(d1110Active()[1]||p):k))].filter(k=>D1110.pilots.includes(k));}
function d1110Readings(b,t){if(!b.readings?.length)return;msgFaceUse('dialogue');const rows=b.readings;
 for(let i=0;i<rows.length;i++){let text=rows[i];if(b.id==='B505'&&i===0){const count=[0,1,3,12,37,96][d1110Frame(b,t)];text='HOSTILE TRACKS: '+String(count).padStart(2,'0');}
  if(b.id==='B403'&&i===0)text=['RELAY STATUS: NOMINAL','RECEIVER: UNKNOWN PAYLOAD','CORE: SYMBIOTE CODE','REPLICATION: ARRAY BUS','CONTROL AUTHORITY: LOST'][d1110Frame(b,t)];
  msgText(text,b.bank?716:456,(b.bank?316:340)+i*24,12,'#c6f5ea',1,1,.04);}
 msgFaceUse(null);
}
function d1110Visual(b,s){const t=s.t,p=run.pilot,slide=D1110.static?1:clamp(t/.4,0,1),ease=1-Math.pow(1-slide,3);ctx.save();ctx.imageSmoothingEnabled=false;ctx.fillStyle='#000';ctx.fillRect(0,0,912,512);
 const visualH=b.text?398:484;D1110.visualH=visualH;ctx.save();ctx.beginPath();ctx.rect(0,0,912,visualH);ctx.clip();
 if(b.bank){
  // Use complete new 512px scenes at native detail, with a separate contextual panel.
  const a=D1110_ART.banks[b.bank],f=d1110Frame(b,t),x=Math.round(-512+(512+10)*ease);
  d1110Bank(b.bank,f,x,-Math.max(0,(a?.h||512)-visualH)*.2);d1110Context(b,t,f);
 }else if(b.layout==='duo'||b.layout==='trio'){
  d1110Plate({...b,art:'comic'},t);const people=d1110People(b),trio=people.length>2;
  for(let i=0;i<people.length;i++){const width=trio?304:456,x=trio?i*304-40:i?510:10,offset=(1-ease)*(i?520:-520),pk=people[i];
   ctx.save();ctx.beginPath();ctx.rect(i*width,0,width,398);ctx.clip();d1110Face(pk,Math.round(x+offset),14,t,b.who===pk.toUpperCase()&&s.shown<b.text.length);ctx.restore();}
  if(S113_ART.banks['comic-border'])D1110.base.bank('comic-border',0,456,256);
 }else{
  d1110Plate(b,t);
  if(b.layout==='flight'||b.ship){const active=d1110Active(),u=D1110.static?.55:clamp(t/(b.duration||6),0,1);
   for(let i=0;i<active.length;i++){const pk=active[i],landing=b.ship==='land'||b.art==='hangar',size=landing?lerp(286,230,u):lerp(280,190,u),x=456+(i-(active.length-1)/2)*230,y=landing?lerp(320,226,u):lerp(285,-100,u);
    if(b.ship==='board')d1110Plane(pk,5-Math.min(2,Math.floor(u*3)),x,220,280);
    else if(b.ship==='launch')d1110Plane(pk,3-Math.min(3,Math.floor(u*5)),x,y,size);
    else if(landing)d1110Plane(pk,Math.min(5,Math.floor(u*6)),x,y,size);
    else d1110Native(pk,b.ship==='return'?'front':'rear',x,y,size);
   }
  }
  if(b.portal){const a=C22_ART.banks.blue_portal,f=Math.floor(t*a.fps)%a.frames;if(XART.rdy(a.key))ctx.drawImage(XART.get(a.key),f%a.columns*a.w,Math.floor(f/a.columns)*a.h,a.w,a.h,284,25,344,344);}
 }
 ctx.restore();d1110Readings(b,t);
 if(b.title&&XART.rdy('nbl_logo_0916')){const im=XART.get('nbl_logo_0916'),w=540,h=w*im.height/im.width;ctx.drawImage(im,Math.round((912-w)/2),22,w,Math.round(h));}
 if(b.text){msgFaceUse('dialogue');const r=ui20Panel(b.who,20,402,872,90,false);if(r){const content=ui20PanelContents(b.who,b.text,s.shown,null,r,14,13);D1110.caption={text:b.text,shown:s.shown,frame:r,content};}msgFaceUse(null);}
 msgFaceUse('dialogue');controlHintRow([['pad_a',s.shown<b.text.length?'REVEAL':'NEXT'],['pad_start','SKIP SCENE']],500,456,870,14);msgFaceUse(null);ctx.restore();
 D1110.last={id:s.id,shot:b.id,pilot:p,coOp:d1110Active(),bank:b.bank||null,frame:b.bank?d1110Frame(b,t):null,time:t,who:b.who,readings:b.readings,ship:b.ship||b.layout==='flight'};
}
function d1110Cue(s,b,name,at,previous){const key=name+':'+at;if(s.t>=at&&!b._cueSet.has(key)){b._cueSet.add(key);if(previous<=at&&s.t-previous<.25){Snd.play(name);d1110Event('cue',{id:s.id,shot:b.id,name,at});}}}
function d1110Step(s,dt,onAdvance,onFinish){
 if(D1110.paused)return;const b=s.beats[s.i];if(!b)return;
 s.age+=dt;s.d1110Wait=(s.d1110Wait||0)+dt;
 if(s.age>.15&&Input.menuStart()){onFinish();return;}
 const click=Input.mouse.down&&!s.md;s.md=!!Input.mouse.down;
 if(s.age>.15&&(Input.menuConfirm()||click)){if(s.shown<b.text.length){s.shown=b.text.length;s.t=Math.max(s.t,b.text.length/38);}else onAdvance();return;}
 if(!d1110Ready(s.d1110Keys)&&s.d1110Wait<15)return;
 const previous=s.t;s.t+=Math.max(0,dt);const before=s.shown;s.shown=Math.max(s.shown,Math.min(b.text.length,Math.floor(s.t*38)));dialogueLetterTicks(b.text,before,s.shown);
 if(b.cue)d1110Cue(s,b,b.cue,b.cueAt??.08,previous);
 if(b.layout==='radar'||b.id==='B505')for(const at of b.id==='B505'?[.1,.9,1.7,2.3,2.7,3,3.25,3.45,3.62,3.78,3.92,4.05,4.2,4.32]:[.25,1.3,2.35,3.4,4.45])d1110Cue(s,b,'blip',at,previous);
 if(s.t>=Math.max(b.duration||0,b.text.length/38+1.6)){s.shown=b.text.length;onAdvance();}
}
BOFCinematicDirector.tick=function(dt){const s=this.current;if(!s?.beats[s.i]?.d1110||s.live)return D1110.base.tick.call(this,dt);
 return d1110Step(s,dt,()=>this.advance(),()=>this.finish());};
BOFCinematicDirector.draw=function(){const s=this.current;if(!s?.beats[s.i]?.d1110||s.live)return D1110.base.draw.apply(this,arguments);d1110Viewport();d1110Visual(s.beats[s.i],s);};
function d1110NewScene(id,p,route){const beats=d1110Clone(id,p,route),keys=d1110Keys(beats,p);if(id==='ending')for(const pk of D1110.pilots)keys.push(D1110_ART.banks['face-'+pk].key);return {id,beats,i:0,t:0,age:0,shown:0,md:!!Input.mouse.down,d1110Wait:0,d1110Keys:[...new Set(keys)]};}
campaignIntroStart=function(done){const ok=D1110.base.introStart.apply(this,arguments);if(campaignIntro){campaignIntro.d1110=d1110NewScene('opening',campaignIntro.pilot,s113Route());run.pilot=campaignIntro.pilot;d1110Ready(campaignIntro.d1110.d1110Keys);d1110Viewport();d1110Event('intro-start',{pilot:run.pilot});}return ok;};
drawCampaignIntro=function(dt){if(!campaignIntro?.d1110)return D1110.base.introDraw(dt);const s=campaignIntro.d1110;d1110Viewport();
 const done=()=>{d1110Event('intro-complete',{pilot:run.pilot});D1110.base.introFinish();};
 d1110Step(s,dt,()=>{s.i++;s.t=0;s.shown=0;if(s.i>=s.beats.length)done();},done);
 if(campaignIntro?.d1110===s&&s.beats[s.i])d1110Visual(s.beats[s.i],s);
};
stageLoadBegin=function(n,keys){const rows=run.mode==='campaign'?d1110Post(n):[];return D1110.base.load.call(this,n,[...(keys||[]),...d1110Keys(rows)]);};
// A true victory is already recorded by triggerVictory. Only its presentation changes.
triggerVictory=function(){D1110.ending=null;return D1110.base.trigger.apply(this,arguments);};
function d1110Credits(){ctx.fillStyle='#000';ctx.fillRect(0,0,912,512);msgFaceUse('dialogue');msgText('THE FURY PILOTS',456,35,24,'#ffe082',1,1,.04);
 D1110.pilots.forEach((p,i)=>{const x=24+i%3*310,y=75+Math.floor(i/3)*118;d1110Face(p,x,y,0,false,90);msgText(p.toUpperCase(),x+175,y+48,14,'#ecf2ed',1,1,.04);});msgText('EARTH HAS A TOMORROW.',456,466,18,'#bde8d5',1,1,.04);msgFaceUse(null);}
function d1110FinalCard(age){ctx.fillStyle='#000';ctx.fillRect(0,0,912,512);msgFaceUse('dialogue');msgText('THE END',456,62,32,'#ffe082',1,1,.04);msgText('DRACODIA DEFEATED',456,110,17,'#bce8d1',1,1,.04);
 const active=d1110Active();for(let i=0;i<active.length;i++){const x=active.length===1?366:240+i*255;d1110Face(active[i],x,145,0,false,180);msgText(active[i].toUpperCase(),x+90,350,18,'#f0e4c7',1,1,.04);}
 const total=(run.score||0)+(coopActive()?(run2.score||0):0);msgText('FINAL SCORE '+pad(total,8),456,405,19,'#eef5ff',1,1,.04);msgText('THE SKY IS OURS.',456,447,16,'#bde8d5',1,1,.04);if(age>1)controlHintRow([['pad_start','TITLE']],490,456,870,14);msgFaceUse(null);}
const D1110_OLD_VICTORY=drawVictory;
drawVictory=function(dt){if(run.mode==='arcade'||!drawVictory._trueEnding)return D1110_OLD_VICTORY(dt);
 d1110Viewport();if(!D1110.ending){D1110.ending={scene:d1110NewScene('ending',run.pilot,s113Route()),phase:'ending',time:0};d1110Ready(D1110.ending.scene.d1110Keys);d1110Event('ending-start',{pilot:run.pilot});}
 const end=D1110.ending;
 if(end.phase==='ending'||end.phase==='sting'){
  const s=end.scene;d1110Step(s,dt,()=>{s.i++;s.t=0;s.shown=0;if(s.i>=s.beats.length){end.phase=end.phase==='ending'?'credits':'card';end.time=0;Input.clearTaps();}},()=>{end.phase=end.phase==='ending'?'credits':'card';end.time=0;Input.clearTaps();});
  if(s.beats[s.i]&&['ending','sting'].includes(end.phase))d1110Visual(s.beats[s.i],s);
 }else if(end.phase==='credits'){
  end.time+=dt;d1110Credits();if(end.time>7){end.phase='sting';end.scene=d1110NewScene('sting',run.pilot,s113Route());d1110Ready(end.scene.d1110Keys);Input.clearTaps();}
 }else{
  end.time+=dt;d1110FinalCard(end.time);const click=Input.mouse.down&&!end.md;end.md=!!Input.mouse.down;
  if(end.time>1&&(Input.menuStart()||Input.menuConfirm()||click)){D1110.ending=null;drawVictory._t=0;drawVictory._ready=false;setState(GS.TITLE);menuIndex=0;Audio.startMusic('title');}
 }
};
Object.assign(drawVictory,D1110_OLD_VICTORY);
S113.preview=async function(id,p=run.pilot,route='left',partner=null){BOFCinematicDirector.cancel();run.mode='campaign';run.pilot=D1110.pilots.includes(p)?p:'cole';coopOn=D1110.pilots.includes(partner)&&partner!==run.pilot;if(coopOn)run2.pilot=partner;Input.clearTaps();Input.mouse.down=false;
 if(id==='opening'){campaignIntroStart(()=>setState(GS.TITLE));return true;}
 if(id==='ending'){D1110.ending=null;setState(GS.VICTORY);drawVictory._trueEnding=true;drawVictory._ready=true;return true;}
 if(!id.startsWith('post-')&&!D1110_SCENES[id])return D1110.base.storyPreview(id,p,route);
 const rows=id.startsWith('post-')?d1110Post(Number(id.slice(5)),run.pilot,route):d1110Clone(id,run.pilot,route);return d1110Play('review-'+id,rows,()=>setState(GS.TITLE));};
C22.preview=(id,p)=>id==='opening'||id==='ending'||id.startsWith('post-')||D1110_SCENES[id]?S113.preview(id,p):D1110.base.preview(id,p);
D1110.preview=S113.preview;D1110.script=d1110Post;
window.BOF_CINEMA_1110=D1110;
