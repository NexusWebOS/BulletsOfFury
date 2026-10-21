"use strict";
/* A resolved victory before the optional sequel sting. Native encounter,
   campaign rewards, pilot art, aircraft, input and ending branches keep ownership. */
const CE20={base:{keys:victoryEndingKeys,load:stageLoadBegin,portrait:dr5Portrait,rigDraw:dr5RigDraw,
  drawBoss:r30DrawBoss,card:victoryFinalCard,stinger:victoryStinger,trigger:triggerVictory,
  directorDraw:BOFCinematicDirector.draw,directorTick:BOFCinematicDirector.tick,caption:victoryCaption,ship:hc10StaticShip,actor:hl10Actor,tick:r30Tick,world:drawWorld,survivorAssets:sv10Assets},
  pilots:HC10.pilots,draws:{},events:[],scenes:new WeakSet(),portraits:new Map(),bounds:new Map(),last:null};
for(const a of Object.values(CE20_ART))XART._src[a.key]=a.path;
const CE20_EPILOGUES={
 cole:['COLE - EVERYONE COMES HOME','We broke his hold. Now we get every pilot home, restore the cities, and make sure nobody hands a machine the keys to our world again.'],
 axel:['AXEL - THE NEXT WATCH','The attack is over. Keep the rescue lanes open and the defenses under manual control. We stand down when the last civilian is safe.'],
 freezer:['FREEZER - A WORLD ALLOWED TO HEAL','The reactors are stable. The emergency shelters have power. For the first time since this began, nobody needs another weapon from me tonight.'],
 yuri:['YURI - LIGHTS ACROSS THE CITY','One district at a time, the lights are coming back. Listen to that channel. Those are people calling their families, not another distress signal.'],
 maverick:['MAVERICK - SOMETHING WORTH SAVING','Call the contract closed. Keep the bonus. Put it into the rescue crews and the people rebuilding down there. I have had enough targets for one day.'],
 falva:['FALVA - THE LINE HELD','Every evacuation flight made it through the last corridor. We held the line together. Now let the people we protected have their sky back.'],
 lizzie:['LIZZIE - TOOLS FOR REBUILDING','The defense grid is ours again. Tomorrow these hands help rebuild what it destroyed. Tonight, I want to hear the hangar without an alarm.'],
 decker:['DECKER - NO MASTER SIGNAL','His command lattice is gone. I am restoring each system from clean local copies. Nothing reconnects until we know who is holding the controls.'],
 juggernaut:['JUGGERNAUT - THE QUIET AFTER','That is it. No more running from the next alarm. Get the wounded inside, clear a place for the rescue crews, and tell the city we are still here.']
};
DR5.intro.splice(0,DR5.intro.length,
 ['Your machines called across the dark. I answered.',3],
 ['I was a will without a body. Your networks gave me hands. Your weapons gave me a voice.',4],
 ['You named the intrusion a virus. You mistook a doorway for its master.',0],
 ['I am the thing that learned to live inside your code.',4],
 ['Every stolen machine carried a piece of my will. Every battle taught me your fear.',3],
 ['But you kept flying. No command to obey. No network for me to seize.',0],
 ['Then I will break you myself.',5],
 ['I AM DRACODIA. MASTER OF DESTRUCTION!',5]);
function ce20Keys(pk=run.pilot){
 const partner=typeof coopActive==='function'&&coopActive()?hl10Assets(p2Pilot().key).map(a=>a.key):[];
 return [...new Set([...hl10Assets(pk).map(a=>a.key),...partner,...Object.values(CE20_ART).map(a=>a.key),
  ...CE20.pilots.flatMap(p=>[campaignIntroPortraitKey(p),'comm_'+p+'_idle','comm_'+p+'_victory',...hc10ShipAssets(p).map(a=>a.key)]),
  ...DR21_ART.banks.symbiote.map(a=>a.key),...Object.values(V18_ART.models.colossus.frames[0]).map(a=>a.key),
  'cinend_deep_space','cinend_bof2_shadow','cut_furyhq_command_center','dlg_window','nbl_logo_0916'])];
}
function ce20Warm(pk=run.pilot){let ready=true;for(const key of ce20Keys(pk))if(!XART.rdy(key))ready=false;bmfReady('dialogue');return ready;}
victoryEndingKeys=function(){return ce20Keys();};
// Preserve archived previews, but do not enqueue the retired organic infection
// family through its older loading wrapper during a current campaign launch.
sv10Assets=function(){return CE20.retiredLoading?[]:CE20.base.survivorAssets.apply(this,arguments);};
stageLoadBegin=function(n,keys){const before=CE20.retiredLoading;CE20.retiredLoading=n>=7;
 try{return CE20.base.load.call(this,n,[...(keys||[]),...(n>=7?ce20Keys():[])]);}
 finally{CE20.retiredLoading=before;}
};
function ce20Cue(S,key,at,q,name){
 const state=S.ce20||(S.ce20={time:q,cues:new Set()});
 if(q<state.time-.01){state.time=q;state.cues.clear();}
 if(q>=at&&!state.cues.has(key)){state.cues.add(key);const play=state.time<at&&q-state.time<.75;
  if(play)Snd.play(name);CE20.events.push({key,name,q,played:play});if(CE20.events.length>100)CE20.events.shift();}
}
function ce20Cover(key,W,H,t=0,zoom=1){
 if(!XART.rdy(key))return null;const im=XART.get(key),k=Math.max(W/im.width,H/im.height)*zoom,
  w=im.width*k,h=im.height*k,x=(W-w)/2,y=(H-h)/2;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,x,y,w,h);ctx.restore();CE20.draws[key]=(CE20.draws[key]||0)+1;
 return {x,y,w,h};
}
function ce20Ink(key){if(CE20.bounds.has(key))return CE20.bounds.get(key);if(!XART.rdy(key))return null;
 const im=XART.get(key),c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d',{willReadFrequently:true});g.drawImage(im,0,0);
 const a=g.getImageData(0,0,c.width,c.height).data;let x0=c.width,y0=c.height,x1=0,y1=0;
 for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++)if(a[(y*c.width+x)*4+3]>24){x0=Math.min(x0,x);y0=Math.min(y0,y);x1=Math.max(x1,x+1);y1=Math.max(y1,y+1);}
 const box=[x0,y0,Math.max(1,x1-x0),Math.max(1,y1-y0)];CE20.bounds.set(key,box);return box;
}
function ce20Pilot(pk,x,bottom,height,t=0,alpha=1){
 const key=campaignIntroPortraitKey(pk),r=ce20Ink(key);if(!r)return false;const k=height/r[3],w=r[2]*k;
 ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(key),...r,x-w/2,bottom-height+Math.sin(t*1.8)*.35,w,height);ctx.restore();
 CE20.draws[key]=(CE20.draws[key]||0)+1;return {pilot:pk,key,x,bottom,height};
}
function ce20Label(text,x,y,size,color='#f4e8c3',alpha=1){
 msgFaceUse('dialogue');msgText(text,x,y,size,color,1,alpha,.045);msgFaceUse(null);
}
victoryCaption=function(head,body,W,H,alpha=1){
 if(alpha<=0)return;const x=W*.055,w=W*.89,y=H*.72,narrow=W/H<1.2,headH=narrow?34:27;
 ctx.save();ctx.globalAlpha*=alpha;const g=ctx.createLinearGradient(0,y-20,0,H);
 g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(.3,'rgba(0,0,0,.78)');g.addColorStop(1,'rgba(0,0,0,.95)');ctx.fillStyle=g;ctx.fillRect(0,y-20,W,H-y+20);
 msgFaceUse('dialogue');
 msgDrawBlock({text:head,x,y:y+4,w,h:headH,maxH:narrow?12:18,minH:narrow?9:12,lineMul:1.15,spacing:.04,color:'#ffe082',tintA:1,alpha:1,outline:1});
 msgDrawBlock({text:body,x,y:y+headH+7,w,h:H-y-headH-16,maxH:narrow?12:15,minH:9,lineMul:1.25,spacing:.04,color:DIALOGUE_BODY_COLOR,tintA:1,alpha:1,outline:1});
 msgFaceUse(null);ctx.restore();CE20.caption={head,body,x,w,y,headH,narrow};
};
function ce20Portrait(pk,x,y,size,emotion='victory'){
 const key='comm_'+pk+'_'+emotion,k=XART.rdy(key)?key:'comm_'+pk+'_idle';if(!XART.rdy(k))return;
 const im=XART.get(k),s=Math.min(size/im.width,size/im.height);ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,x-im.width*s/2,y-im.height*s/2,im.width*s,im.height*s);ctx.restore();CE20.draws[k]=(CE20.draws[k]||0)+1;
}
hc10StaticShip=function(pk,view,x,y,width){
 const result=CE20.base.ship.apply(this,arguments);
 if(state===GS.VICTORY&&run.mode!=='arcade'&&coopActive()&&pk===run.pilot&&drawVictory._t<VICTORY_DISH_AT){
  const other=p2Pilot().key,a=hc10ShipGeometry(pk,view),p=hc10ShipGeometry(other,view),ground=drawVictory._t>=HL10.times.pad;
  const h=width*a.h/a.w,ph=width*p.h/p.w,px=x+width*.95,py=ground?y+h/2-ph/2:y+h*.28;
  CE20.base.ship(other,view,px,py,width);CE20.partnerShip={pilot:other,key:p.key,x:px,y:py,width,ground};
 }return result;
};
hl10Actor=function(s,R){
 const result=CE20.base.actor.apply(this,arguments);
 if(state===GS.VICTORY&&coopActive()&&s.pilot===run.pilot){
  const other=p2Pilot().key,t=s.t-1.0,q=hl10Sample(t,other),u=hl10Ease((t-HL10.times.walk)/(HL10.times.entered-HL10.times.walk)),offset=R.w*.19*(1-u);
  CE20.partnerActor=CE20.base.actor(q,{...R,x:R.x+offset});
 }return result;
};
victoryDish=function(t,W,H,S){
 const q=t-VICTORY_DISH_AT,pk=hl10Pilot(run.pilot),phase=q<5.2?'debrief':q<11.2?'pilot':'squad',
  fade=Math.min(clamp(q/.6,0,1),clamp((VICTORY_WARNING_AT-t)/.6,0,1));
 ctx.save();ctx.globalAlpha=fade;ce20Cover(CE20_ART.debrief.key,W,H,q,1+q*.0014);
 const cast=[];
 if(phase==='squad'){
  const narrow=W/H<1.2;
  const others=CE20.pilots.filter(p=>p!==pk),order=narrow?[...others.slice(0,5),others[5],pk,others[6],others[7]]:[...others.slice(0,4),pk,...others.slice(4)];
  for(let i=0;i<order.length;i++){const back=narrow&&i<5,x=narrow?W*(back?.10+i*.20:.17+(i-5)*.22):W*(.10+i*.10),bottom=H*(back?.615:.70),height=H*(narrow?(back?.19:order[i]===pk?.26:.22):(order[i]===pk?.39:.32));cast.push(ce20Pilot(order[i],x,bottom,height,q+i));}
 }else{
  const tech=pk==='decker'?'cole':'decker';cast.push(ce20Pilot(tech,W*.24,H*.70,H*.43,q));cast.push(ce20Pilot(pk,W*.72,H*.70,H*.48,q+.7));
 }
 const ep=CE20_EPILOGUES[pk],coop=typeof coopActive==='function'&&coopActive();
 const caption=phase==='debrief'?['FURY COMMAND - SIGNAL TERMINATED','Dracodia\'s core is destroyed. The invasion command signal is dead. Rescue channels are open. Earth is under human control again.']:
  phase==='pilot'?ep:['FURY FLIGHT - THE SKY IS OURS',coop?'Two pilots broke through. An entire squad held the way home. The survivors return to a world that finally has a tomorrow.':'One pilot broke through. An entire squad held the way home. The survivors return to a world that finally has a tomorrow.'];
 victoryCaption(...caption,W,H,1);ctx.restore();
 ce20Cue(S,'debrief',.10,q,'blip');ce20Cue(S,'epilogue',5.22,q,'select');ce20Cue(S,'reunion',11.22,q,'blip');if(S.ce20)S.ce20.time=q;
 CE20.last={scene:phase,q,pilot:pk,cast:cast.filter(Boolean),caption,fade};
};
victoryWarning=function(t,W,H,S){
 const q=t-VICTORY_WARNING_AT,fade=Math.min(clamp(q/.55,0,1),clamp((VICTORY_SPACE_AT-t)/.55,0,1));
 ctx.save();ctx.globalAlpha=fade;ce20Cover(CE20_ART.debrief.key,W,H,q,1.035);ctx.fillStyle='rgba(1,5,12,.83)';ctx.fillRect(0,0,W,H);
 const h=Math.min(H*.038,W*.037);
 ce20Label('BULLETS OF FURY',W/2,H*.14,h*1.45,'#ffe082');ce20Label('THE FURY PILOTS',W/2,H*.27,h,'#a9dcfa');
 const names=[['AXEL','COLE','DECKER'],['FALVA','FREEZER','JUGGERNAUT'],['LIZZIE','MAVERICK','YURI']];
 for(let r=0;r<3;r++)for(let c=0;c<3;c++)ce20Label(names[r][c],W*(.20+c*.30),H*(.39+r*.085),Math.min(h,W*.035));
 ce20Label('THANK YOU FOR PLAYING',W/2,H*.79,h*1.06,'#ffe082');
 ce20Label('EARTH HAS A TOMORROW.',W/2,H*.88,h*.72,'#b8dbc8');ctx.restore();CE20.last={scene:'credits',q,fade};
};
victorySpaceLaunch=function(t,W,H,S){
 const q=t-VICTORY_SPACE_AT;
 ctx.save();ctx.globalAlpha*=Math.min(clamp(q/.4,0,1),clamp((VICTORY_STINGER_AT-t)/.35,0,1));
 if(q<3.5){
  const R=ce20Cover(CE20_ART.relay.key,W,H,q,1.025+q*.006);
  if(R){const at={x:R.x+R.w*.77,y:R.y+R.h*.66};dr21Art('symbiote',q,at.x,at.y,Math.min(W*.075,H*.15),.75);}
  victoryCaption('POST-CREDITS - AN ISOLATED ECHO','Far above Earth, a severed relay drifts in silence. One fragment still moves. It has no uplink. Nobody is listening.',W,H,Math.min(clamp(q/.35,0,1),clamp((3.5-q)/.35,0,1)));
 }else{
  ce20Cover('cinend_deep_space',W,H,q);
  victoryCaption('SPACE FEDERATION - UNIDENTIFIED CONTACT','Earth\'s invasion signal is gone. Beyond the outer system, a different contact turns toward the light. Origin unknown.',W,H,Math.min(clamp((q-3.5)/.35,0,1),clamp((VICTORY_STINGER_AT-t)/.35,0,1)));
 }
 ce20Cue(S,'echo',.20,q,'crackle');ce20Cue(S,'contact',3.55,q,'blip');if(S.ce20)S.ce20.time=q;
 if(q>=5.6&&!S.ce20MusicOut){S.ce20MusicOut=true;if(Audio.fadeOutMusic)Audio.fadeOutMusic(.5);}
 ctx.restore();
 CE20.last={scene:q<3.5?'isolated-echo':'unknown-contact',q};
};
victoryStinger=function(t,W,H,S){const q=t-VICTORY_STINGER_AT,prev=S.ce20StingerAt??q;
 if(q<prev-.01)S.scream=false;
 if(q>=1.06&&(prev>=1.06||q-prev>.75))S.scream=true;
 const r=CE20.base.stinger.apply(this,arguments);S.ce20StingerAt=q;CE20.last={scene:'sequel-stinger',q};return r;};
victoryFinalCard=function(t,W,H){
 if(run.mode==='arcade')return CE20.base.card.apply(this,arguments);
 const q=t-VICTORY_CARD_AT,pk=hl10Pilot(run.pilot),fade=clamp(q/.6,0,1);ctx.fillStyle='#02050a';ctx.fillRect(0,0,W,H);
 ctx.save();ctx.globalAlpha=fade;ce20Label('THE END',W/2,H*.14,Math.min(H*.063,W*.075),'#ffe082');
 ce20Label(drawVictory._trueEnding?'DRACODIA DEFEATED':'MISSION COMPLETE',W/2,H*.25,Math.min(H*.030,W*.033),'#c9e8de');
 const coop=typeof coopActive==='function'&&coopActive();
 ce20Portrait(pk,W*(coop?.32:.5),H*.43,Math.min(H*.24,W*(coop?.36:.62)));
 if(coop)ce20Portrait(p2Pilot().key,W*.68,H*.43,Math.min(H*.24,W*.36));
 ce20Label(coop?cinPilotName(pk)+' + '+cinPilotName(p2Pilot().key):cinPilotName(pk),W/2,H*.58,Math.min(H*.027,W*(coop?.035:.06)),'#f5e8c5');
 const total=(run.score||0)+(typeof coopActive==='function'&&coopActive()?run2.score||0:0);
 ce20Label('FINAL SCORE  '+pad(total,8),W/2,H*.68,Math.min(H*.03,W*.035),'#eef5ff');
 ce20Label('THE SKY IS OURS.',W/2,H*.78,H*.025,'#a9dcfa');
 if(drawVictory._trueEnding)ce20Label('BULLETS OF FURY WILL RETURN',W/2,H*.85,Math.min(H*.018,W*.025),'#a9a4b9');
 if(q>5)controlHintRow([['pad_start','TITLE']],H-22,W/2,W-24);ctx.restore();CE20.last={scene:'final-card',q,pilot:pk,total};
};
function ce20Body(t,x,y,size,roar=false){
 const m=V18_ART.models.colossus,acting=roar?v19ClipFrame('colossus_roar',t,2.5)?.layers:null,
  frame=acting||m.frames[Math.floor(t*m.fps)%m.frames.length],k=size/320;
 for(const id of ['left','right','core']){const a=frame[id];if(!a||!XART.rdy(a.key))continue;
  const joint=acting?[160,160]:V19_LIMBS.colossus[id]?.[0]||[160,160],sign=id==='left'?-1:1,rot=acting||id==='core'?0:sign*(Math.sin(t*2.3)*.065+.025);
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(x+(joint[0]-160)*k,y+(joint[1]-160)*k);ctx.rotate(rot);ctx.drawImage(XART.get(a.key),-joint[0]*k,-joint[1]*k,size,size);ctx.restore();CE20.draws[a.key]=(CE20.draws[a.key]||0)+1;
 }
}
dr5RigDraw=function(b){if(!v18Owned(b)||b._r30.mode!=='dr5Monologue')return CE20.base.rigDraw.apply(this,arguments);
 const R=dr5State(b).radio;ce20Body(R?.face===5?R.t:b._r30.clock,b.x,b.y,v18Size(b),R?.face===5);
};
r30DrawBoss=function(b){if(v18Owned(b)&&b._r30.mode==='dr5Monologue'){
 const R=dr5State(b).radio;ce20Body(R?.face===5?R.t:b._r30.clock,b.x,b.y,v18Size(b),R?.face===5);dr5EffectsDraw(b);return;
 }return CE20.base.drawBoss.apply(this,arguments);};
r30Tick=function(b,dt){
 if(v18Owned(b)&&b._r30.mode==='dr5Monologue'&&b._r30.t>.25){
  const D=dr5State(b),R=D.radio;
  if(R&&Input.menuStart()){
   D.line=DR5.intro.length-1;R.t=dr5TalkDuration(R.text)+.01;Snd.stopCue('dracodiaShriek');
  }else if(R&&Input.menuConfirm()){
   const typed=R.text.length/34;R.t=R.t<typed?typed:dr5TalkDuration(R.text)+.01;
  }
 }
 return CE20.base.tick.apply(this,arguments);
};
drawWorld=function(dt){const out=CE20.base.world.apply(this,arguments);
 if(v18Owned(boss)&&boss._r30.mode==='dr5Monologue'){
  const R=dr5State(boss).radio,label=R&&R.t<R.text.length/34?'REVEAL':'NEXT';
  ctx.save();ctx.setTransform(SS,0,0,SS,0,0);msgFaceUse('dialogue');controlHintRow([['pad_a',label],['pad_start','SKIP SPEECH']],VH*.925,VW/2,VW*.94,14);msgFaceUse(null);ctx.restore();
 }return out;
};
dr5Portrait=function(face,talk=0){
 if(!v18Owned(boss))return CE20.base.portrait.apply(this,arguments);
 const R=dr5State(boss).radio,f=talk?Math.floor((R?.t||0)*12)%V18_ART.models.colossus.frames.length:0,
  a=(face===5?v19ClipFrame('colossus_roar',R?.t||0,2.5)?.layers?.core:null)||V18_ART.models.colossus.frames[f].core,key=a.key;
 if(CE20.portraits.has(key))return CE20.portraits.get(key);if(!XART.rdy(a.key))return null;
 const old=DR5_ART.portrait[0],c=document.createElement('canvas');c.width=old.w;c.height=old.h;const g=c.getContext('2d');g.imageSmoothingEnabled=false;
 if(XART.rdy(old.key))g.drawImage(XART.get(old.key),0,0);g.clearRect(38,40,c.width-76,c.height-78);g.fillStyle='#060713';g.fillRect(38,40,c.width-76,c.height-78);
 const crop=[117,36,86,124],w=c.width-84,h=c.height-88,k=Math.min(w/crop[2],h/crop[3]);g.drawImage(XART.get(a.key),...crop,42+(w-crop[2]*k)/2,44+(h-crop[3]*k)/2,crop[2]*k,crop[3]*k);
 c.complete=true;c.naturalWidth=c.width;c.naturalHeight=c.height;if(CE20.portraits.size>=16)CE20.portraits.delete(CE20.portraits.keys().next().value);CE20.portraits.set(key,c);return c;
};
function ce20Story(s){if(!s||CE20.scenes.has(s))return;CE20.scenes.add(s);
 for(const b of s.beats){
  b._ce20Hug=b.art==='cin_cole_decker_hug_0924';
  if(b.bg==='cin_war_symbiote_reveal'){b._ce20Reveal=true;b.text='RELAY RECORDING: A FOREIGN WILL INSIDE THE MACHINE. Its body is woven from stolen circuitry and armor.';b.bg='cin_story_lab_empty';}
  if(/symbiote/i.test(b.text))b.text=b.text.replace(/alien symbiote/gi,'demonic machine parasite').replace(/symbiote/gi,'machine parasite');
  if(b.text.includes('That is what has been steering'))b.text='That thing did not just infect the satellite. It used it to reach inside our machines.';
  if(b.bg==='cin_stage08_approach')b._ce20Approach=true;
  if(b._ce20Reveal)for(const f of V18_ART.models.colossus.frames)for(const a of Object.values(f))XART.rdy(a.key);
  if(b._ce20Approach)for(const a of DR21_ART.banks.symbiote)XART.rdy(a.key);
  const pk=b.who.toLowerCase();if(CE20.pilots.includes(pk)){if(!b._ce20Hug)b.art=campaignIntroPortraitKey(pk);XART.rdy(b.art);for(const e of ['idle','talk-closed','talk-small','talk-medium','talk-wide','talk-o'])XART.rdy('comm_'+pk+'_'+e);}
 }
}
BOFCinematicDirector.tick=function(dt){ce20Story(BOFCinematicDirector.current);return CE20.base.directorTick.call(this,dt);};
BOFCinematicDirector.draw=function(){
 const s=BOFCinematicDirector.current;if(!s)return;ce20Story(s);const b=s.beats[s.i];
 if(s.live||b.interactive||b.who==='CRONOS')return CE20.base.directorDraw.call(this);
 const W=cutsceneViewWidth(),H=VH,pk=b.who.toLowerCase(),person=CE20.pilots.includes(pk),
  selected=hl10Pilot(run.pilot),contact=selected==='decker'?'cole':'decker';
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.fillStyle='#030711';ctx.fillRect(0,0,W,H);
 const bg=b._ce20Approach?'cinend_deep_space':b.bg||'cin_story_lab_empty';ce20Cover(bg,W,H,s.t,1);
 if(b._ce20Hug&&XART.rdy(b.art)){
  const im=XART.get(b.art),src=[0,0,im.width,Math.floor(im.height*.60)],k=Math.min(W*.78/src[2],H*.66/src[3]),w=src[2]*k,h=src[3]*k;
  ctx.drawImage(im,...src,(W-w)/2,H*.02,w,h);CE20.draws[b.art]=(CE20.draws[b.art]||0)+1;
 }else if(b._ce20Reveal){ce20Body(s.t,W*.5,H*.36,Math.min(W*.55,H*.77),false);ce20Label('FOREIGN SIGNAL / MACHINE HOST',W*.5,H*.10,Math.min(W*.025,H*.026),'#e4c2ff');}
 else if(person&&!b.bg){
  // These authored portraits end at the thighs. Bury that source edge behind
  // the opaque dialogue panel, keeping the complete heads above it.
  CE20.storyCast=[ce20Pilot(pk===contact?selected:contact,W*.23,H*.91,H*.75,s.t),ce20Pilot(pk,W*.72,H*.91,H*.79,s.t+.4)];
 }
 else if(b._ce20Approach){dr21Art('symbiote',s.t,W*.5,H*.36,H*.34,.88);}
 else if(b.bg&&/deep_space|city_descent|river|sewer|topdown|stage07|stage08/.test(b.bg)){
  const front=/stage08/.test(b.bg),view=front?'front':'rear';hc10StaticShip(selected,view,W*.5,H*(.45-.06*clamp(s.t/8,0,1)),H*.25);
 }
 const pw=Math.min(W*.92,1020),ph=H*.245,x=(W-pw)/2,y=H*.70;
 dlgBox._tw={key:String(state)+'|'+b.who+'|'+b.text,count:s.shown,at:performance.now(),auto:false};
 dlgBox({who:b.who,portrait:person?pk:false,full:b.text,shown:b.text.slice(0,s.shown),forceShown:true,fade:1,tint:b._ce20Reveal?'#d9a9ff':'#a9dcfa',pw,ph,x,y,maxBottom:H*.94,screenSpace:false});
 msgFaceUse('dialogue');controlHintRow([['pad_a',s.shown<b.text.length?'REVEAL':'NEXT'],['pad_start','SKIP SCENE']],H*.972,W/2,W*.92,16);msgFaceUse(null);ctx.restore();
 CE20.story={id:s.id,index:s.i,who:b.who,bg,body:person?campaignIntroPortraitKey(pk):null,reveal:!!b._ce20Reveal};
};
globalThis.BOF_CINEMATIC_ENDING={state:CE20,warm:ce20Warm,keys:ce20Keys};
