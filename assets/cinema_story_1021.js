'use strict';
/* Authored PixelLab mission bridges. Native progression, rewards, dialogue input,
   ship identity, music mixer and final-death clocks retain their owners. */
const C22={base:{script:BOFCinematicDirector.script,start:BOFCinematicDirector.start,
 preview:BOFCinematicDirector.preview,draw:BOFCinematicDirector.draw,tick:BOFCinematicDirector.tick,
 intro:ip21Visual,keys:campaignIntroKeys,end:inv20Draw,cinKeys:ce20Keys,
 boss:r30DrawBoss,burst:dr5Burst,disintegrate:dr5Disintegrate,ship:hc10StaticShip,portal:inv20Portal,flight:hc10Flight,tickBoss:r30Tick,campaignPortrait:campaignIntroPortraitKey},draws:{},events:[],last:null};
for(const a of Object.values(C22_ART.images))XART._src[a.key]=a.path;
for(const a of Object.values(C22_ART.banks||{}))XART._src[a.key]=a.path;
// Match Maverick's green aviators across legacy speaking/arrival shots too.
// Native body sizes, expressions, pose placement and dialogue clocks remain owned
// by the existing cinematic renderers; these are identity-only artwork variants.
for(const [name,variant] of [['maverick','maverick_report_pose'],['maverick_horror','maverick_horror_pose']]){
 const a=C22_ART.images[variant];if(a&&INV20_ART.images[name])INV20_ART.images[name]={...INV20_ART.images[name],...a};
}
campaignIntroPortraitKey=function(pk){return pk==='maverick'&&C22_ART.images.maverick_standing_pose?C22_ART.images.maverick_standing_pose.key:C22.base.campaignPortrait.apply(this,arguments);};
Snd.prepare(['stage3AtomicSiren','crackle','jetDash','warpGate','expBig']);
function c22Keys(){return [...Object.values(C22_ART.images),...Object.values(C22_ART.banks||{})].map(a=>a.key).concat(['cin_cole_decker_hug_0924'],CE20.pilots.flatMap(pk=>['idle','talk-closed','talk-small','talk-medium','talk-wide','talk-o'].map(e=>'comm_'+pk+'_'+e)));}
function c22Warm(){let ok=true;for(const k of c22Keys())if(!XART.rdy(k))ok=false;return ok;}
campaignIntroKeys=function(){return [...C22.base.keys(),...c22Keys()];};
ce20Keys=function(pk){return [...C22.base.cinKeys(pk),...c22Keys()];};
function c22Plate(name,W,H,t=0,zoom=1.015){const a=C22_ART.images[name];if(!a||!XART.rdy(a.key))return false;
 const im=XART.get(a.key),k=Math.max(W/a.w,H/a.h)*zoom,w=a.w*k,h=a.h*k;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,(W-w)/2,(H-h)*.35,w,h);
 for(const [name,bank] of Object.entries(C22_ART.banks)){if(bank.patch?.image!==a.key.slice(4))continue;const [px,py,pw,ph]=bank.patch.rect;c22Bank(name,t,(W-w)/2+(px+pw/2)*k,(H-h)*.35+(py+ph/2)*k,pw*k);}
 ctx.restore();
 C22.draws[name]=(C22.draws[name]||0)+1;return true;
}
function c22Bank(name,t,x,y,size,once=false,alpha=1){const a=C22_ART.banks[name];if(!a||!XART.rdy(a.key))return false;
 const f=once?clamp(Math.floor(t*a.fps),0,a.frames-1):Math.floor(Math.max(0,t)*a.fps)%a.frames,k=size/a.w;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=alpha;
 ctx.drawImage(XART.get(a.key),(f%a.columns)*a.w,Math.floor(f/a.columns)*a.h,a.w,a.h,x-a.pivot[0]*k,y-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();
 C22.draws[name]=(C22.draws[name]||0)+1;C22.lastBank={name,f,x,y,size};return true;
}
function c22Line(who,text,shot,extra={}){return {who:who.toUpperCase(),text,bg:C22_ART.images[shot]?.key,c22:shot,...extra};}
function c22Upgrade(stage,p,shot){return BOFCinematicDirector.upgrade(stage,p).map(b=>({...b,bg:C22_ART.images[shot].key,c22:shot}));}
function c22Script(stage,p=run.pilot,route){const old=C22.base.script(stage,p,route),L=c22Line,contact=p==='decker'?'cole':'decker';
 if(stage===1)return old.map((b,i)=>({...b,c22:/ORBITAL|satellite|transmission|stolen|signal came/i.test(b.text)?'satellite_infected':i<2?'peace_city':'forge_upgrade',bg:C22_ART.images[/ORBITAL|satellite|transmission|stolen|signal came/i.test(b.text)?'satellite_infected':i<2?'peace_city':'forge_upgrade'].key}));
 if(stage===2)return old.map(b=>({...b,text:b.text.replace('Our radar and squad channels are returning.','The interference is weakening, but the squad channels are still blocked.'),bg:C22_ART.images.lava_relay.key,c22:'lava_relay'}));
 if(stage===3){const rows=[
  L(p,'Ice relay destroyed. Fury flight, does anyone read me?','ice_relay'),
  L('lizzie','Loud and clear! All squad channels are back. Everyone, return to Fury HQ.','ice_relay'),
  L(p,'Fury HQ in sight. Bringing the squad home to regroup.','hq_hangar',{c22Flight:'land'}),
  L('cole','Good to see everyone in one piece. Gather around. Decker, tell us what we have.','hq_regroup'),
  L('decker','The Forge can combine the systems we recover with our weapons. Fire, ice, then electricity. We keep every circuit isolated from the infected network.','hq_regroup'),
  ...c22Upgrade(3,p,'forge_upgrade'),
  L('decker','There is an electrical power cell in the abandoned desert airbase. We need it to restart our launch-pad generator.','desert_airbase'),
  L('cole','So we secure the cell, get the pad running, and take this fight into space.','hq_regroup'),
  L('decker','Exactly. I recovered video from the satellite as it was taken over, but the orbital recorder needs the launch generator online before I can decode the entire stream.','hq_regroup')];
  if(p==='cole')for(const b of old.slice(4,10))rows.push({...b,bg:C22_ART.images.forge_upgrade.key,c22:'forge_upgrade',c22Private:true});
  rows.push(L(p,'Set course for the lost airbase. Bring that power cell back intact.','desert_airbase'));return rows;
 }
 if(stage===4)return [L(p,'Airbase secured. We have the electrical power cell.','power_cell'),
  L('decker','That is the one. Bring it into the generator cradle.','launch_generator'),
  L('decker','Launch-pad power restored. The orbital recorder is coming online. Watch this.','launch_generator'),
  L('FURY RECORDING','SATELLITE SECURITY RECORDING. A foreign machine entered the relay array.','satellite_clean'),
  L('decker','Dracodia took over the satellite, then infected Earth\'s entire infrastructure through it. Our cities, defenses, aircraft. Everything linked to that network.','satellite_infected'),
  L(p,'Then the signal in orbit is where we strike next.','satellite_infected'),...c22Upgrade(4,p,'forge_upgrade'),
  L('decker','The Federation space systems are ready. With the generator restored, I can launch your fighter beyond the atmosphere.','launch_generator'),
  L(p,'Power the pad. I am going up.','hq_hangar',{c22Flight:'launch'})];
 if(stage===5){const flying=[p,...(coopActive()?[p2Pilot().key]:[])],guards=['decker','axel','juggernaut','freezer','lizzie'].filter(k=>!flying.includes(k)).slice(0,2),names=guards.map(k=>k.toUpperCase()).join(' and ');return [
  L(p,'Chronos is down. Recover that massive chaingun, disengage the space systems, and take us home.','orbital_return',{c22Flight:'land'}),
  L(p,'Fury HQ, the runway is in sight. Bringing the salvage down.','hq_hangar',{c22Flight:'land'}),
  L('decker','Look at this rotary assembly! That hammer-wielding monster left us exactly what we need.','forge_upgrade'),
  ...c22Upgrade(5,p,'forge_upgrade'),
  L('decker','Paired chaingun turrets and massive .50 caliber slugs. Reinforced mounts, insulated feeds. Your earned elemental cartridges still fit.','forge_upgrade'),
  L('FURY COMMAND','RED ALERT! Invasion force inbound from space. Heading straight for the city!','hq_alarm',{c22Cue:'stage3AtomicSiren'}),
  L('decker','The radar is going crazy. Those contacts are multiplying faster than I can track them!','hq_alarm',{c22Cue:'crackle'}),
  L('cole','Two of you, stay behind and defend the base! '+names+', hold HQ. Everyone else, scramble!','hq_alarm'),
  L('cole','','hq_sprint',{duration:1.65,c22Action:true,c22Cue:'jetDash'}),
  L(p,'Hangar crew, clear my fighter. We are launching now!','hq_hangar',{c22Flight:'board',duration:5.8}),
  L(p,'Fury flight, on my wing. We stop them before they reach the city.','hq_hangar',{c22Flight:'launch',duration:4.8})];}
 if(stage===6){const rows=old.filter(b=>!(/I traced the alien|code is coming|Taking the lower|Check the new combinations|narrow tunnel/i.test(b.text))).map(b=>({...b,bg:C22_ART.images.hq_regroup.key,c22:'hq_regroup'}));
  return [L(p,'Fury HQ, we are coming home. Get the squad together.','hq_hangar',{c22Flight:'land'}),...rows,
   L('decker','A new signal just appeared. It is not in the skies. It is underground, by the river.','hq_river'),
   L('cole','Show us exactly where.','hq_river'),L('decker','Under the iron bridge. The signal leads into the sewers themselves. We never searched beneath the city.','hq_river'),
   ...c22Upgrade(6,p,'forge_upgrade'),L(p,'Then we head there immediately. Fury flight, take the river approach.','river_sewer',{c22Flight:'river'})];}
 if(stage===9)return old.map(b=>({...b,bg:C22_ART.images.orbital_return.key,c22:'orbital_return',c22Flight:'land'}));
 return old;
}
BOFCinematicDirector.script=c22Script;
BOFCinematicDirector.start=function(stage,done){if(run.mode!=='campaign')return false;
 // Stage-clear rewards/Forge have already completed. The authored scramble now
 // leads straight to the native Stage 6 card, rather than returning to the map.
 const continuation=stage===5?()=>{Input.clearTaps();beginStage(6);}:done;
 return this.play('post-'+stage,c22Script(stage),continuation);};
BOFCinematicDirector.preview=function(id,p){if(!id.startsWith('post-'))return C22.base.preview.apply(this,arguments);this.cancel();run.pilot=CE20.pilots.includes(p)?p:'axel';return this.play('preview-'+id,c22Script(Number(id.slice(5)),run.pilot),()=>setState(GS.TITLE));};
if(window.BOFCampaignStory){window.BOFCampaignStory.script=c22Script;window.BOFCampaignStory.start=(stage,done)=>BOFCinematicDirector.start(stage,done);}
function c22Actor(pk,t,W,H){const bank=HL10_ART[pk+'_walk'],frame=bank?.[Math.floor(t*22)%bank.length];if(!frame||!XART.rdy(frame.key))return;
 const u=clamp(t/2.2,0,1),height=H*.19,k=height/(frame.opaque_bounds[3]-frame.opaque_bounds[1]),x=lerp(W*.85,W*.54,u),y=H*.67;
 hl10Cell(pk+'_walk',Math.floor(t*22)%bank.length,x,y,height*frame.w/(frame.opaque_bounds[3]-frame.opaque_bounds[1]));
 if(t>=2.2&&t<3.8){const exit=HL10_ART[pk+'_exit'],f=7-Math.min(7,Math.floor((t-2.2)/1.6*8));
  hl10Cell(pk+'_exit',f,W*.54,H*lerp(.67,.49,clamp((t-2.2)/1.6,0,1)),exit[0].w*k);}
}
function c22Front(pk,x,y,width){const a=C22_ART.images[pk+'_front'];if(!a||!XART.rdy(a.key))return C22.base.ship(pk,'front',x,y,width);
 const r=ce20Ink(a.key);if(!r)return;const h=width*r[3]/r[2];ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),...r,x-width/2,y-h/2,width,h);ctx.restore();C22.draws[pk+'_front']=(C22.draws[pk+'_front']||0)+1;
}
hc10StaticShip=function(pk,view,x,y,width){const front=view==='front'||state===GS.VICTORY&&drawVictory._t>=6&&drawVictory._t<26.4;
 if(!front||!C22_ART.images[pk+'_front'])return C22.base.ship.apply(this,arguments);
 c22Front(pk,x,y,width);if(state===GS.VICTORY&&coopActive()&&pk===run.pilot)c22Front(p2Pilot().key,x+width*.95,y,width);return true;
};
function c22Flight(kind,t,W,H){const pk=hl10Pilot(run.pilot);for(const a of [...hc10ShipAssets(pk),...hl10Assets(pk)])XART.rdy(a.key);
 if(kind==='board'){c22Front(pk,W*.45,H*.51,H*.62);if(t<2.2)c22Actor(pk,t,W,H);else if(t<3.8){const list=HL10_ART[pk+'_exit'],f=7-Math.min(7,Math.floor((t-2.2)*5));hl10Cell(pk+'_exit',f,W*.53,H*lerp(.67,.48,clamp((t-2.2)/1.6,0,1)),H*.24);} }
 else if(kind==='launch'){const u=hl10Ease(clamp((t-.35)/3,0,1)),width=H*lerp(.62,.045,u);hc10StaticShip(pk,'rear',W*.5,H*lerp(.52,.29,u),width);}
 else if(kind==='land'){const u=hl10Ease(clamp(t/4,0,1));c22Front(pk,W*.5,H*lerp(.28,.49,u),H*lerp(.12,.54,u));}
 else hc10StaticShip(pk,'rear',W*.48,H*.51,H*.18);
 C22.flight={pk,kind,t};
}
BOFCinematicDirector.tick=function(dt){const s=this.current,b=s?.beats[s.i];if(b?.c22&&b.c22Cue&&!b._c22Cue){b._c22Cue=true;Snd.play(b.c22Cue);C22.events.push({cue:b.c22Cue,id:s.id,index:s.i});}
 const before=s?.i;const out=C22.base.tick.call(this,dt);if(s===this.current&&s.i===before&&b?.c22Action&&s.t>=b.duration)this.advance();return out;};
BOFCinematicDirector.draw=function(){const s=this.current,b=s?.beats[s.i];if(!b?.c22||s.live)return C22.base.draw.apply(this,arguments);ce20Story(s);
 const W=cutsceneViewWidth(),H=VH;ctx.save();ctx.imageSmoothingEnabled=false;c22Plate(b._ce20Hug?'hq_hangar':b.c22,W,H,s.t);
 if(b._ce20Hug&&XART.rdy(b.art)){const im=XART.get(b.art),src=[0,0,im.width,Math.floor(im.height*.60)],k=Math.min(W*.78/src[2],H*.66/src[3]);ctx.drawImage(im,...src,(W-src[2]*k)/2,H*.02,src[2]*k,src[3]*k);}
 if(b.c22==='hq_sprint'){/* Native PixelLab run reel preserves the real full-body articulation. */ip21Cover('run',Math.min(IP21_ART.banks.run.frames-1,Math.floor(s.t*24)),W,H);}
 if(b.c22Flight)c22Flight(b.c22Flight,s.t,W,H);
 if(b.c22==='hq_alarm')inv20Alarm(W,H,s.t);
 const person=CE20.pilots.includes(b.who.toLowerCase());
 if(!b.c22Action){const pw=Math.min(W*.92,1020),ph=H*.245,x=(W-pw)/2,y=H*.70;
  dlgBox._tw={key:String(state)+'|'+b.who+'|'+b.text,count:s.shown,at:performance.now(),auto:false};
  dlgBox({who:b.who,portrait:person?b.who.toLowerCase():false,full:b.text,shown:b.text.slice(0,s.shown),forceShown:true,fade:1,pw,ph,x,y,maxBottom:H*.94,screenSpace:false});}
 msgFaceUse('dialogue');controlHintRow([['pad_a',s.shown<b.text.length?'REVEAL':'NEXT'],['pad_start','SKIP SCENE']],H*.972,W/2,W*.92,16);msgFaceUse(null);ctx.restore();
 C22.last={id:s.id,index:s.i,shot:b.c22,who:b.who,text:b.text};
};
// Compress the wordless departure and play the authored run at a brisk cadence.
{let at=0;for(const b of IP21.beats){if(b.dispatch==='run')b.duration=1.65;b.at=at;b.to=at+=b.duration;}IP21.finaleAt=at;IP21.end=at+14;}
ip21Visual=function(b,c,t,W,H){if(b.dispatch==='run'){ip21Cover('run',Math.min(IP21_ART.banks.run.frames-1,Math.floor(t*24)),W,H);IP21.last={kind:'dispatch',bank:'run',frame:Math.min(IP21_ART.banks.run.frames-1,Math.floor(t*24))};return;}
 const introMap={cin_war_earth_peace:'peace_city',cin_war_civilian_collapse:'civilian_collapse',cin_war_city_air_attack:'air_invasion',cin_war_suburban_tanks:'suburban_tanks',cin_war_naval_exchange:'naval_exchange',cin_origin_land:'civilian_collapse',cin_origin_hq_iso:'hq_alarm'};
 const name=b.federation?(t<.8?'satellite_clean':'satellite_infected'):b.dispatch==='dispatch'?'hq_regroup':b.dispatch==='turn'?'hq_alarm':introMap[b.bg]||null;
 if(name&&c22Plate(name,W,H,t)){IP21.last={kind:'c22',name};return;}return C22.base.intro.apply(this,arguments);};
// Dimensional fleet scenes replace the old repeated top-down sprite grids.
inv20Draw=function(t,W,H,S){const shot=INV20.shots.find(a=>t>=a[1]&&t<a[2]),name=shot?.[0],q=t-(shot?.[1]||0),map={report:'hq_regroup',relief:'hq_regroup',alarm:'hq_alarm',federation:'earth_invasion',horror:'hq_alarm',base:'air_invasion',waters:'coast_invasion',earth:'earth_invasion',solar:'solar'};
 if(['growth','scream','escape'].includes(name)&&C22_ART.banks.remnant&&C22_ART.banks.void_portal){
  const a=C22_ART.banks.remnant,u=clamp(q/(shot[2]-shot[1]),0,1);c22Plate('solar',W,H,q);
  if(name==='growth')c22Bank('remnant',u*4/a.fps,W*.52,H*.49,H*lerp(.35,.68,u),true);
  if(name==='scream'){const v=hl10Ease(clamp((q-.8)/5,0,1));c22Bank('remnant',(4+u*(a.frames-5))/a.fps,W*.52,H*.51,H*lerp(.68,1.9,v),true);}
  if(name==='escape'){inv20Portal('black_void',q,W*.72,H*.4,H*.60,1.1,4.4,1.5);const v=hl10Ease(clamp((q-1.4)/4.2,0,1));if(q<5.8)c22Bank('remnant',(a.frames-1)/a.fps,lerp(W*.2,W*.72,v),lerp(H*.67,H*.4,v),H*lerp(.34,.025,v),true);}
  if(S._c22Shot!==name){if(S._c22Time!=null&&t-S._c22Time<.25)Snd.play(name==='scream'?'dracodiaShriek':name==='escape'?'warpGate':'crackle');S._c22Shot=name;}
  S._c22Time=t;INV20.last={scene:name,t,q,pilot:run.pilot,units:[],cast:[],dimensional:true};return;
 }
 if(!map[name])return C22.base.end.apply(this,arguments);
 const smooth=S._c22Time!=null&&t>S._c22Time&&t-S._c22Time<.25;S._c22Time=t;
 c22Plate(map[name],W,H,q,lerp(1.04,1,clamp(q/Math.max(1,shot[2]-shot[1]),0,1)));
 let dialogue=null,cue=null;if(name==='report')dialogue=[cinPilotName(run.pilot),'We got him! Dracodia is down. Tell everyone - it is finally over!'];
 if(name==='relief')dialogue=['AXEL','All pilots accounted for. You brought our people home. We can finally breathe.'];
 if(name==='alarm'){dialogue=['FURY COMMAND','RED ALERT! Priority transmission from the Space Federation. Put it on the main screen!'];cue='stage3AtomicSiren';}
 if(name==='federation'){const i=Math.min(2,Math.floor(q/4.34));dialogue=['SPACE FEDERATION',['Digital black holes are opening across the orbital defense network!','Alien drones are pouring through. They are hacking our systems and swarming above Earth!','They have broken the perimeter. They are coming for your skies!'][i]];cue='crackle';}
 if(name==='horror')dialogue=['DECKER','Those signals... the skies, the sea, the entire planet. This was only the beginning.'];
 if(name==='base'){dialogue=['FURY COMMAND','Air contacts over the base! Every altitude. Every approach. Scramble all remaining aircraft!'];cue='jetDash';}
 if(name==='waters'){dialogue=['COASTAL DEFENSE','Warboats approaching the peninsula! The entire coast is under siege!'];cue='blip';}
 if(name==='earth'){dialogue=['SPACE FEDERATION','More rifts. More fleets. They are surrounding Earth. All surviving units, respond!'];cue='warpGate';}
 if(name==='solar'){dialogue=q<5?['SPACE FEDERATION','The breach extends beyond Earth. Their signal is spreading across the solar system.']:null;cue='warpGate';}
 if(['alarm','horror'].includes(name))inv20Alarm(W,H,q);
 if(S._c22Shot!==name){S._c22Shot=name;if(cue&&smooth)Snd.play(cue);}
 if(dialogue)inv20Text(...dialogue,W,H,Math.floor(Math.max(0,q-.12)*37));
 INV20.last={scene:name,t,q,pilot:run.pilot,units:[],cast:[],dialogue,dimensional:true};C22.ending=INV20.last;
};
// Data erasure precedes the existing native explosion / escape callback.
dr5Burst=function(b){if(v18Owned(b)&&b._r30.mode==='dr5Death'&&b._r30.t<4.2)return;return C22.base.burst.apply(this,arguments);};
dr5Disintegrate=function(b){if(!v18Owned(b)||b._r30.mode!=='dr5Death')return C22.base.disintegrate.apply(this,arguments);
 const D=dr5State(b);D.bodyGone=true;D.bits.length=0;dr5Burst(b,b.x,b.y,430,true);r30Sound('expBig');C22.events.push({event:'digital-disintegration-complete',time:b._r30.t});
};
r30DrawBoss=function(b){if(v18Owned(b)&&C22_ART.banks.blue_portal){const S=b._r30,D=dr5State(b);
  if(S.mode==='dr5Portal'){const size=290+Math.sin(Math.min(S.t,2)/2*Math.PI/2)*50,u=S.t<.7?hl10Ease(S.t/.7):S.t>6.2?1-hl10Ease((S.t-6.2)/1.4):1;c22Bank('blue_portal',S.t,worldWidth()/2,PLAY.y+150,size*u);dr5EffectsDraw(b);return;}
  if(S.mode==='reunion'&&D.deathStarted&&S.t<2.8){c22Bank('blue_portal',S.t,worldWidth()/2,112,310*(1-hl10Ease(S.t/2.8)));return;}
 }
 if(!v18Owned(b)||b._r30.mode!=='dr5Death')return C22.base.boss.apply(this,arguments);
 const t=b._r30.t;if(t<3.25)return C22.base.boss.apply(this,arguments);
 if(t<4.2){const a=C22_ART.banks.data_disintegrate;if(!a||!c22Bank('data_disintegrate',(t-3.25)/.95*(a.frames-1)/a.fps,b.x,b.y,422,true))C22.base.boss.apply(this,arguments);}
 else {dr5EffectsDraw(b);const a=C22_ART.banks.data_blast;if(a)for(const f of dr5State(b).fx.filter(f=>f.kind==='blast').slice(-8))if(f.t<a.frames/a.fps)c22Bank('data_blast',f.t,f.x,f.y,f.size*1.3,true);
  if(C22_ART.banks.code_fragments){const q=t-4.2;if(q<2.2)c22Bank('code_fragments',Math.min(q*.4,.65),b.x,b.y,lerp(400,1050,clamp(q/2.2,0,1)),true,1-clamp((q-1.2),0,1));}}
};
inv20Portal=function(bank,t,x,y,size,form=.8,loop=Infinity,close=.8){const name=bank==='blue_rift'?'blue_portal':bank==='black_void'?'void_portal':null,a=C22_ART.banks[name];
 if(!a)return C22.base.portal.apply(this,arguments);const end=form+loop+close,u=clamp(t/form,0,1)*(Number.isFinite(end)?clamp((end-t)/close,0,1):1);
 c22Bank(name,t,x,y,size*hl10Ease(u));return {phase:t<form?'form':t<form+loop?'loop':'close',from:Math.floor(t*a.fps)%a.frames};
};
hc10Flight=function(t,pk,R){if(t>=2.75)return C22.base.flight.apply(this,arguments);const a=C22_ART.banks.blue_portal;if(!a)return C22.base.flight.apply(this,arguments);
 const s=hc10FlightSample(t,pk),u=t<.6?hl10Ease(t/.6):t>2.05?1-hl10Ease((t-2.05)/.7):1;
 c22Bank('blue_portal',t,R.x+R.w*.5,R.y+R.h*.37,R.h*.76*u);c22Front(pk,R.x+R.w*s.x,R.y+R.h*s.y,R.w*s.width);
 HC10.portal={bank:'blue_rift',source:a.key,visible:t<2.75,phase:t<.6?'form':t>2.05?'close':'loop'};HC10.last={...s,rect:R,portal:HC10.portal};return HC10.last;
};
C22.preview=async function(id,pk){this.deathPreview=false;BOFCinematicDirector.cancel();Audio.stopMusic();Snd.loopStopAll();run.pilot=hl10Pilot(pk);run.mode='campaign';coopOn=false;Input.clearTaps();Input.mouse.down=false;
 const started=performance.now();while(!c22Warm()){if(performance.now()-started>90000)throw Error('Cinematic art did not finish loading. Reload the preview.');await new Promise(r=>setTimeout(r,50));}
 if(id.startsWith('post-')){BOFCinematicDirector.play('review-'+id,c22Script(Number(id.slice(5)),run.pilot),()=>setState(GS.TITLE));return;}
 if(id==='opening'){campaignIntroPilot=run.pilot;campaignIntroStart(()=>setState(GS.TITLE));return;}
 if(id==='ending'){run.stage=8;setState(GS.VICTORY);drawVictory._trueEnding=true;drawVictory._ready=true;drawVictory._t=0;drawVictory._scroll=0;drawVictory._sfx={};Audio.startMusic('finalCinematic');return;}
 if(id==='death'){beginStage(8);setState(GS.TITLE);player.reset();stagePlan=[];spawnClock=99999;enemies=[];eBullets=[];pBullets=[];boss=null;spawnBoss('vileexistence');
  while(!stageLoadReady(8)||!v18Warm()||!dr21Warm()){if(performance.now()-started>90000)throw Error('Final cinematic assets did not finish loading.');stageLoadTick();await new Promise(r=>setTimeout(r,50));}
  v18Clear(boss);v18Budget(boss);v18Enter(boss,2,0);v18Fight(boss);boss._r30.v18.arenaPhase=2;boss.x=worldWidth()/2;boss.y=viewTopY()+190;boss._r30.v18.home={x:boss.x,y:boss.y};boss._noHit=boss.enter=false;player.x=worldWidth()/2;player.y=VH-100;player.dead=false;
  setState(GS.PLAY);_setCinematicViewport(false);camX=clamp(player.x-VW/2,0,Math.max(0,worldWidth()-VW));ctx.setTransform(SS,0,0,SS,0,0);this.deathPreview=true;j3FinalDeath(boss);return;}
};
r30Tick=function(b,dt){const out=C22.base.tickBoss.apply(this,arguments);if(C22.deathPreview&&b?._r30?.mode==='dr5Portal'){C22.deathPreview=false;setState(GS.TITLE);}return out;};
globalThis.BOF_CINEMA_REBUILD=C22;
