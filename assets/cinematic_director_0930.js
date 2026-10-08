"use strict";
/* Authored mission bridges and pilot-specific upgrade conversations. Rewards remain
   owned by the engine: A/Start can never grant, erase or duplicate an upgrade. */
const BOFCinematicDirector=(()=>{
 const pilots=['axel','freezer','lizzie','falva','yuri','maverick','cole','decker','juggernaut'];
 const root='assets/game/shared/cinematics/cinema_0930/';
 for(const key of ['cronos','decker','yuri'])XART._src['cin30_'+key]=root+key+'.png';
 XART._src.cin_stage08_approach='assets/game/levels/stage_08/cinematics/cinematic_level_approaches/stage08_furious_death_approach.png';
 XART._src.cin30_bonus='assets/game/levels/stage_09/cinematics/cinematic_level_approaches/stage09_the_velocity_void_bonus_approach.png';
 let scene=null;
 const oldStory=window.BOFCampaignStory;
 const originalScript=oldStory&&oldStory.script;
 const lead=()=>run.pilot||_pilotKey()||'axel';
 const contact=p=>p==='decker'?'cole':'decker';
 const line=(who,text,extra={})=>Object.assign({who:who.toUpperCase(),text},extra);
 const pilotLines={
  axel:['Keep the ship responsive. I want the gun ready the instant I break formation.','Fast feed, clean recoil. I can work with that.'],
  freezer:['Keep my thermal circuits isolated. I need fire and ice available when I switch.','Hot barrels, cold nerves. That should do nicely.'],
  lizzie:['Balance both mounts. I am not fighting the recoil while I line up my next shot.','Now that is a proper upgrade. Leave me something to aim at.'],
  falva:['Keep the firing line clean. I need room for my elemental systems to breathe.','Then let us see how their armor likes the new rhythm.'],
  yuri:['Keep the feed insulated from my lightning. I would rather charge the enemy than the magazine.','Steel and lightning. They are going to hear us coming.'],
  maverick:['My homing lasers stay on their own circuit. I want a clean switch between both systems.','Good. Precision when I need it. Volume when I do not.'],
  cole:['Get the squad equipped first. Keep my prototype machine-gun and Fusion Cannon line intact.','Bring everyone home, Decker. Then we will see what else that salvage can do.'],
  decker:['That chaingun we acquired in space is exactly what I need to upgrade our bullet systems.','Faster feed, heavier rounds, and the elemental cartridges still fit. That is our new chaingun.'],
  juggernaut:['Reinforce the mounts. If it shakes loose the first time I charge, I am bringing it back.','A little more kick. Now you are speaking my language.']
 };
 function upgrade(stage,p){
  const c=contact(p),rows=[];
  const say=(who,text,extra)=>rows.push(line(who,text,Object.assign({location:'lab',art:who==='yuri'&&stage>=4?'cin30_yuri':undefined},extra)));
  if(stage===1){
   say(c,'The recovered system gives us our first elemental upgrade. Keep these combinations inside this campaign; every new sortie starts with what we actually recover.');
   if(p==='freezer'){
    say('freezer','That volcanic front will cook a normal approach. Let me take Ice Breath in.');
    say(c,'Ice Breath is fitted for Stage Two. It is your starting loadout there. We will reopen the choice after the Furnace Tyrant falls.');
   }else if(p==='maverick'){
    say('maverick','I want a straight beam option alongside my homing lasers.');
    say(c,'You can select Laser Beam in the loadout. Your homing array stays yours; choose the tool for the target.');
   }else{
    say(p,{axel:'I will test the new combination on the way to the volcanic front.',lizzie:'New element, same rule: know where every shot is going.',falva:'I can feel the new energy. Let us find a useful shape for it.',yuri:'Keep the electrical circuits clear. I want this upgrade stable.',cole:'Record the combinations, but only issue what this run has earned.',decker:'I will match the recovered element to the guns we actually have.',juggernaut:'If it hits harder, mount it. I will handle the rest.'}[p]);
   }
  }else if(stage===2){
   say(c,'Fire Orb is ready. We are heading into ice units next: fire deals fifty percent more damage to them. Ice against ice deals fifty percent less.');
   say(p,p==='freezer'?'Switch me back to Flamethrower for the ice front. Keep Ice Breath selectable; I still want the choice.':'Fit the fire option before we launch. No point feeding an enemy its own element.');
   say(c,'Use the loadout to choose your weapon and its element. The same resistance rule applies to fire weapons against fire units.');
  }else if(stage===3){
   say(c,'The ice core is recovered. We can now carry its properties into the weapon combinations you have unlocked.');
   if(p==='freezer'){
    say('freezer','Now combine that control with our fire system. A sudden thermal change should crack their armor.');
    say(c,'Thermoshock is your default orb from here. Fire Orb and Ice Orb remain selectable.');
   }else say(p,'Good. Keep the elemental options ready. The airbase will have more than one kind of armor.');
  }else if(stage===4){
   if(p==='yuri'){
    say('decker','The boss capacitor can strengthen your lightning, Yuri. I have matched the new blue arc to your ship.');
    say('yuri','I can feel it building. A tap for chain lightning... a held charge for something much bigger.');
    say('decker','Thunder Storm. Charge, choose your moment, then release. The bolts volley out from your ship and bring the sky down on them.');
   }else{
    say(c,'The recovered electrical system is stable. Your loadout now has the combinations earned from this airbase.');
    say(p,'Check the Federation hull as well. Those guns need to survive the trip into space.');
   }
  }else if(stage===5){
   if(p==='decker'){
    say('cole','Decker, tell me the parts we recovered were worth dragging through reentry.');
    say('decker',pilotLines[p][0],{art:'cin30_decker'});
    say('cole','Then build it. The squad will need more firepower before we reach home.');
   }else{
    say('decker','That chaingun we acquired in space is exactly what I need to upgrade our bullet systems.',{art:'cin30_decker'});
    say(p,pilotLines[p][0]);
    say('decker',p==='cole'?'Understood. The squad gets the chaingun conversion. Your prototype gun and Fusion Cannon progression stay intact.':'I have fitted rotary mounts to your ship. Faster, heavier rounds, with the elemental upgrades from your machine gun carried across.',{art:'cin30_decker'});
   }
   say(p,pilotLines[p][1]);
   if(p!=='cole')say(p==='decker'?'cole':'decker','The chaingun is ready for the next ground sortie. Check it in the loadout before Stage Six.');
  }else if(stage===6){
   say(c,'Check the new combinations before we go underground. The toxic signature below the city is unlike the aircraft we just fought.');
   say(p,'A narrow tunnel, contaminated air, and no room to turn back. Make every shot count.');
  }else if(stage===9){
   say(c,'Laser Mist survived the detour. The weapon is unlocked; return to the campaign map and choose where we take it next.');
   say(p,'One more answer in the arsenal. Back to the mission.');
  }
  return rows;
 }
 function script(stage,p=lead(),route){
  const c=contact(p),L=(who,text,extra)=>line(who,text,extra),U=upgrade(stage,p);
  const r=route||(typeof s6Wing!=='undefined'&&s6Wing&&s6Wing.route)||(campaign.rivalScattered?'left':'right');
  if(stage===1){
   const origin=originalScript?originalScript(1).filter(b=>b.origin||['cin_origin_arrival','cin_origin_satellite','cin_origin_land'].includes(b.bg)).map(b=>L(['COLE','DECKER'].includes(b.who)?c:b.who,b.text,{bg:b.bg})):[];
   return [L(p,'The dam is down. The runway is open, but those machines were coordinating through the same signal.'),L(c,'We recovered part of the transmission. Watch the orbital relay.'),...origin,
    L(c,'The signal came down through our satellites. Fury survived because our rebuilt fighters still answer manual controls.'),...U,
    L(c,'The strongest relay on the surface is inside the volcanic belt. Cut its power before it spreads further.'),L(p,'Set a course for the volcano. We follow the signal to its source.')];
  }
  if(stage===2)return [L(p,'The Furnace Tyrant is down. That should take some heat off the network.'),L(c,'It has. Our radar and squad channels are returning. But a second relay is answering from the frozen region.'),...U,L(c,'That relay is using the cold to protect its systems. Break the ice front, and we can trace its connection to the missile airbase.'),L(p,'Fire systems checked. Heading for the ice.')];
  if(stage===3){const privateLab=originalScript?originalScript(3).slice(2).map(b=>L(b.who,b.text,{location:'lab',art:b.fx==='coleHug'?'cin_cole_decker_hug_0924':undefined})):[];
   return [L(p,'The ice relay is finished. I recovered its last transmission.'),L(c,'The coordinates lead to a missile airbase. Its launch batteries are protecting an uplink to orbit.'),...U,...privateLab,L(c,'Silence those batteries and recover the electrical core. I need that power to decode the satellite recording.'),L(p,'Then we take the airbase. No missiles reach the cities.')];}
  if(stage===4)return [L(p,'The airbase is ours. Tell me that core was worth the trouble.'),...U,L(c,'It was. The last orbital frame is finally clear. This is what touched our satellite.',{location:'lab'}),
   L('FURY RECORDING','ORBITAL RELAY: FOREIGN INTELLIGENCE CONFIRMED.',{bg:'cin_war_symbiote_reveal'}),L(p,'That is what has been steering every machine down here?'),L(c,'It is the source of the transmission we traced. The Federation hull can get your fighter into orbit. We need answers before it sends anything else down.'),L(p,'Fit the space systems. I am going up.')];
  if(stage===5)return [L(p,'Cronos is down. Recover anything we can use, then disengage the Federation hull.',{bg:'bg_stage05_loop_0923'}),L(c,'His local signal is gone. That does not prove the infection on Earth is gone with it.'),...U,
   L(c,'Fury flight is forming up for the return. Keep your new guns ready; we have lost contact with the base.'),L(p,'All pilots, stay close on reentry. Nobody flies home alone.')];
  if(stage===6)return [L(p,r==='left'?'The Harrier is finished. What happened to the rebel squad?':'Rebel Fury is down. I wish they had listened.'),
   L(c,r==='left'?'They scattered toward the central core while we took the carrier. Their signals are marked on the map as Stage X contacts.':'All five rebel signals are gone. There will be no Stage X pursuit of this squad.'),
   ...(r==='left'?[L(c,'Stage X is optional. Choose a contact and two wingmen at the central core. They kept the stolen gear, so expect an upgraded fight.'),L(p,'Keep those contacts marked. First tell me what is moving beneath the city.')]:[L(c,'The other threat has not stopped. I am reading a separate signature beneath the city.')]),
   L(p,'And HotWire and Phoenix?'),L(c,'Still missing. They warned us about this squad before their mission. We have no confirmed transmission from either pilot since.'),...U,
   L(c,'Follow the river under the iron bridge. The old sewer access leads toward that signature.',{bg:'cin_story_city_descent'}),L(p,'Taking the lower approach. Keep listening for us.',{bg:'cin_stage07_topdown'})];
  if(stage===7){const second=c==='decker'?'cole':'decker';return [L(c,'The portal closed behind '+p.toUpperCase()+'. No beacon, no weapons telemetry. The sewer is gone.'),L(second,'Keep the last vector on the recorder. Leave every channel open. We are not giving up on them.'),L('FURY RELAY','LAST TRANSMISSION LOST. UNKNOWN SPACE AHEAD.',{bg:'cin_stage08_approach'})];}
  if(stage===8)return [L(p,'The signal is breaking apart. Fury flight, can anyone hear me?',{bg:'cinend_deep_space'}),L(c,'We have you. Hold that channel. We are bringing you home.'),L(p,'Copy. I have had enough of other dimensions for one day.')];
  if(stage===9)return [L(p,'The detour is clear. Space systems intact.',{bg:'cin30_bonus'}),...U];
  return [];
 }
 function cronos(p=lead()) {return [
  line('cronos','Leave now, pilot, and I promise I will not hurt you. I have no quarrel with one small ship.'),
  line(p,'Then why attack us? Who are you, and what do you want?'),
  line('cronos','I am Cronos. An artificial intelligence from another dimension. The details are not important.'),
  line(p,'You turned our machines against us. Those details matter to everyone on our planet.'),
  line('cronos','Your planet is precisely what interests me. Soon enough, I will control everything from the palm of my hands.'),
  line(p,'You are not getting past me.'),line('cronos','A generous offer, refused. Very well. Show me how long your defiance lasts.')
 ];}
 function routeScript(side,p=lead()) {const c=contact(p);return side==='left'?[
  line(c,'The Harrier is heading left. That carrier can keep launching fighters until we bring it down.'),line(p,'I am taking the carrier. Keep the rebels on radar.'),line(c,'If they escape this fight, we can pursue their Stage X contacts at the central core. Choose two wingmen when you go.'),line(p,'Understood. Fury flight, split formation. Left wing, on me.')]:[
  line(c,'Right side: Voss and his old unit. They took the gear from our forward depot.'),line(p,'They called us the Fury crew like we were strangers. What happened to them?'),line(c,'HotWire and Phoenix warned us before their last mission. Neither has checked in since.'),line(p,'Then we get answers here. Right wing, on me.')];}
 function rebelScript(p=lead(),key){const c=contact(p);if(key)return [
  line(c,'Stage X contact confirmed: '+key.toUpperCase()+'. Your two wingmen are with you. This is the signal we marked after the Harrier fight.'),
  line(key,'You chose the carrier. You should have left us out of this.'),line(p,'You took our weapons and threatened our people. Stand down. We can still end this.'),
  line(key,'We improved those weapons while you were busy. Come and see how much.')];
  return [line('voss','Thanks for the free gear, Fury crew. You always did take good care of your machines.'),line(p,'We were one unit once. It does not have to be like this.'),line('voss','The Division betrayed every one of us. There are no orders left worth following.'),line(p,'Then help us stop this. Burning the world will not undo what happened.'),line('nyx','That world was built on our bones. We owe it nothing.'),line('voss','Get out of our way, or burn with it.')];}
 function artFor(b){
  if(b.art)return b.art;
  const p=b.who.toLowerCase();
  if(p==='cronos')return 'cin30_cronos';
  if(pilots.includes(p))return 'cin_pilot_'+p+'_open';
  if(['voss','nyx','rook','kaia','jace'].includes(p))return 'rr_portrait_'+p;
  return null;
 }
 function warm(b){let ready=true;for(const k of [artFor(b),b.bg||'cin_story_lab_empty','dlg_window'])if(k&&!XART.rdy(k))ready=false;bmfReady('dialogue');return ready;}
 function play(id,beats,done,live=false){
  if(scene||!beats.length)return false;
  scene={id,beats,i:0,t:0,shown:0,age:0,readyWait:0,done,live,md:!!Input.mouse.down};
  if(live){eBullets.length=0;pBullets.length=0;}
  for(const b of beats)warm(b);
  Input.clearTaps();
  if(!live){hqMode='director0930';hqSc={beats};hqDone=null;Audio.startMusic('cinematics');setState(GS.CUTSCENE);}
  return true;
 }
 function finish(){if(!scene)return;const s=scene;scene=null;Input.clearTaps();Input.mouse.down=false;
  if(!s.live){hqSc=null;hqDone=null;Audio.startMusic('neonvelocity');}
  if(s.done)s.done();else if(!s.live)setState(GS.CAMPHUB);
 }
 function advance(){if(!scene)return;const s=scene,b=s.beats[s.i];
  if(s.shown<b.text.length){s.shown=b.text.length;s.t=Math.max(s.t,b.text.length/38);return;}
  s.i++;s.t=0;s.shown=0;s.readyWait=0;if(s.i>=s.beats.length)finish();
 }
 function tick(dt){
  if(!scene)return;const s=scene;s.age+=dt;s.frameDt=dt;
  // Read Start before menuConfirm, which includes Start in the shared input API.
  if(s.age>.15&&Input.menuStart()){finish();return;}
  const b=s.beats[s.i];s.readyWait+=dt;const ready=warm(b);
  const click=Input.mouse.down&&!s.md;s.md=!!Input.mouse.down;
  if(s.age>.15&&(Input.menuConfirm()||click)){advance();return;}
  if(!ready&&s.readyWait<4)return; // missing art never traps Start/A or the campaign
  s.t+=dt;const n=Math.min(b.text.length,Math.floor(s.t*38));dialogueLetterTicks(b.text,s.shown,n);s.shown=Math.max(s.shown,n);
  if(s.t>=b.text.length/38+2.7){s.shown=b.text.length;advance();}
 }
 function fit(key,x,y,w,h){if(!key||!XART.rdy(key))return false;const im=XART.get(key),k=Math.min(w/im.width,h/im.height),dw=im.width*k,dh=im.height*k;ctx.drawImage(im,Math.round(x+(w-dw)/2),Math.round(y+(h-dh)/2),Math.round(dw),Math.round(dh));return true;}
 function draw(){if(!scene)return;const s=scene,b=s.beats[s.i],W=s.live?VW:cutsceneViewWidth(),H=VH,key=artFor(b);
  ctx.save();ctx.imageSmoothingEnabled=false;
  if(s.live){worldXformEscape();ctx.fillStyle='rgba(2,5,14,.40)';ctx.fillRect(0,0,W,H);}
  else{
   ctx.fillStyle='#030912';ctx.fillRect(0,0,W,H);
   const cockpit=key&&key.startsWith('cin_pilot_')&&!b.bg;
   const bg=cockpit?key:(b.bg||(b.who==='CRONOS'?'bg_stage05_loop_0923':'cin_story_lab_empty'));
   // Anchor cockpit crops at the top so a wide display never trims a pilot's head.
   if(XART.rdy(bg))cinCover(bg,W,H,.5,cockpit?1:0);
   if(!cockpit){ctx.fillStyle='rgba(2,6,12,.24)';ctx.fillRect(0,0,W,H);}
   // A location plate is an establishing shot; cockpit reverse shots fill the view.
   // New transparent busts retain their complete head and shoulders over the lab.
   if(key&&!cockpit&&!b.bg)fit(key,W*.08,H*.035,W*.84,H*.655);
  }
  const pw=s.live?W*.94:Math.min(W*.92,1020),ph=s.live?H*.29:H*.245,x=(W-pw)/2,y=s.live?H*.64:H*.70;
  const pk=b.who.toLowerCase(),hasPilot=pilots.includes(pk),portrait=hasPilot?pk:false;
  // dlgBox's legacy wall-clock typing must not restart when A reveals a new line.
  dlgBox._tw={key:String(state)+'|'+b.who+'|'+b.text,count:s.shown,at:performance.now(),auto:false};
  dlgBox({who:b.who,portrait,portraitKey:!hasPilot?key:undefined,full:b.text,shown:b.text.slice(0,s.shown),fade:1,tint:b.who==='CRONOS'?'#c6a6ff':'#a9dcfa',pw,ph,x,y,maxBottom:H*.94,screenSpace:false});
  if(s.live&&b.who==='CRONOS')fit(key,W*.67,H*.27,W*.30,H*.34);
  msgFaceUse('dialogue');controlHintRow([['pad_a',s.shown<b.text.length?'REVEAL':'NEXT'],['pad_start','SKIP SCENE']],H*.972,W/2,W*.92,16);msgFaceUse(null);ctx.restore();
 }
 function start(stage,done){if(run.mode!=='campaign')return false;return play('post-'+stage,script(stage),done);}
 function cancel(){scene=null;}
 function preview(id,p){
  cancel();run.pilot=pilots.includes(p)?p:'axel';
  const beats=id.startsWith('post-')?script(Number(id.slice(5)),run.pilot):id==='cronos'?cronos():id==='left'||id==='right'?routeScript(id):rebelScript(lead(),id.startsWith('x-')?id.slice(2):null);
  return play('preview-'+id,beats,()=>setState(GS.TITLE));
 }
 return {script,upgrade,cronos,routeScript,rebelScript,play,start,tick,draw,finish,advance,artFor,cancel,preview,
  get active(){return !!scene;},get live(){return !!scene?.live;},get current(){return scene;}};
})();
window.BOFCinematicDirector=BOFCinematicDirector;
// The old entry point is the actual post-stats/post-unlock continuation.
if(window.BOFCampaignStory){
 window.BOFCampaignStory.start=BOFCinematicDirector.start;
 window.BOFCampaignStory.script=BOFCinematicDirector.script;
 window.BOFCampaignStory.draw=dt=>{BOFCinematicDirector.tick(dt);BOFCinematicDirector.draw();};
 Object.defineProperty(window.BOFCampaignStory,'active',{get:()=>BOFCinematicDirector.active});
}
const CIN30_CUT=drawCutsceneState;
drawCutsceneState=function(dt){
 if(hqMode==='director0930'&&BOFCinematicDirector.active){BOFCinematicDirector.tick(dt);BOFCinematicDirector.draw();return;}
 if(stateT>.15&&Input.menuStart()){hqEnd();return;}
 if(stateT>.15&&hqMode==='beats'&&hqSc&&Input.menuConfirm()){
  const n=(hqSc.beats[hqLine]?.text||'').length;
  if(hqChars<n)hqChars=n;else if(!hqAdvance())return;
 }
 if(stateT>.15&&hqMode==='ens'&&hqSc&&Input.menuConfirm()){
  const n=(hqSc.lines[hqLine]?.[2]||'').length;
  if(hqChars<n)hqChars=n;
  else{hqLine++;if(hqLine>=hqSc.lines.length){hqEnd();return;}hqChars=0;hqHoldT=0;hqSeat(hqLine);}
 }
 return CIN30_CUT(dt);
};
const CIN30_PLAY=updatePlay;
updatePlay=function(dt){if(BOFCinematicDirector.live){BOFCinematicDirector.tick(dt);return;}return CIN30_PLAY(dt);};
const CIN30_WORLD=drawWorld;
drawWorld=function(dt){const r=CIN30_WORLD(BOFCinematicDirector.live?0:dt);if(BOFCinematicDirector.live)BOFCinematicDirector.draw();return r;};
// Keep the Stage 6 sky moving throughout contact dialogue; only combat waits.
const CIN30_BG=drawBG;
drawBG=function(dt){return CIN30_BG(BOFCinematicDirector.live&&run.stage===6?(BOFCinematicDirector.current.frameDt||0):dt);};
const CIN30_CHOICE=s6WingChoiceDraw;
s6WingChoiceDraw=function(){if(!BOFCinematicDirector.live)return CIN30_CHOICE();};
const CIN30_ROUTE=fr27ChooseRoute;
fr27ChooseRoute=function(W,route){if(run.mode!=='campaign')return CIN30_ROUTE(W,route);
 BOFCinematicDirector.play('route-'+route,BOFCinematicDirector.routeScript(route),()=>{W.frStory=3;CIN30_ROUTE(W,route);W.frStory=3;},true);
};
const CIN30_HAMMER=hammerBossTick;
hammerBossTick=function(b,dt){
 if(run.mode==='campaign'&&!b._hammerTime&&!b._cin30Spoke&&b._hammer.state==='unfold'&&b._hammer.t>=.6){
  b._cin30Spoke=true;b.name='CRONOS';storySkip();
  BOFCinematicDirector.play('cronos',BOFCinematicDirector.cronos(),()=>{},true);return;
 }
 return CIN30_HAMMER(b,dt);
};
const CIN30_REBEL=rebelSquadTick;
rebelSquadTick=function(b,dt){const R=b._rebels;
 if(run.mode==='campaign'&&!R.frIntro?.done&&!R._cin30Spoke){
  const I=R.frIntro||(R.frIntro={t:0,beat:0,done:false});I.t+=dt;b._noHit=true;eBullets.length=0;pBullets.length=0;
  for(const q of R.ships){q.x+=clamp(q.homeX-q.x,-100*dt,100*dt);q.y+=clamp(q.homeY-q.y,-95*dt,95*dt);q.mode='entry';}
  if(I.t>=2.5){R._cin30Spoke=true;const key=R.frStageX?R.ships.find(q=>!q.dead)?.key:null;
   BOFCinematicDirector.play(key?'stage-x-'+key:'rebel-contact',BOFCinematicDirector.rebelScript(run.pilot,key),()=>{I.done=true;I.t=29;b._noHit=false;R.t=0;R.releaseAt=1.6;if(s6Wing)s6Wing.line=null;for(const q of R.ships){q.mode='fight';q.t=0;q.cd=1.6+q.i*.4;}},true);
  }return;
 }return CIN30_REBEL(b,dt);
};
// Stages 7/8 and the bonus used separate exits that bypassed hqTrigger entirely.
const CIN30_LEAVE=scLeaveStage;
scLeaveStage=function(R){if(run.mode==='campaign'&&[7,8,9].includes(run.stage)&&!R._cin30Done){R._cin30Done=true;if(BOFCinematicDirector.start(run.stage,()=>CIN30_LEAVE(R)))return;}return CIN30_LEAVE(R);};
// Leaving/resetting a run must not retain an encounter conversation.
const CIN30_BEGIN=beginStage;
beginStage=function(){BOFCinematicDirector.cancel();return CIN30_BEGIN.apply(this,arguments);};
const CIN30_STATE=setState;
setState=function(s){if(BOFCinematicDirector.active&&((BOFCinematicDirector.live&&s!==GS.PLAY)||(!BOFCinematicDirector.live&&s!==GS.CUTSCENE)))BOFCinematicDirector.cancel();return CIN30_STATE(s);};
// Match A/Start semantics in the existing authored opening without replacing it.
const CIN30_OPENING=drawCampaignIntro;
drawCampaignIntro=function(dt){
 if(campaignIntro&&stateT>.15){
  if(Input.menuStart()){campaignIntroFinish();return;}
  if(Input.menuConfirm()){
   const C=campaignIntro,B=CAMPAIGN_INTRO_BEATS.find(b=>C.t>=b.at&&C.t<b.to);
   if(B){const text=B.pilotLine?(CAMPAIGN_SOLO_LINES[C.pilot]||CAMPAIGN_SOLO_LINES.axel)[B.pilotLine]:B.text;
    const end=B.at+(text||'').length/CAMPAIGN_INTRO_CPS;C.t=C.t<end?Math.min(B.to-.02,end+.02):B.to+.001;
   }else campaignIntroFinish();
  }
 }
 return CIN30_OPENING(dt);
};
