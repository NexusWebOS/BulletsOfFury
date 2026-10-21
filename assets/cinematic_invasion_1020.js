"use strict";
/* Mike's authored invasion ending. All artwork is PixelLab or the game's actual
   registered actors; no combat, score, reward or cinematic callback ownership changes. */
const INV20={base:{draw:drawVictory,keys:victoryEndingKeys,ceKeys:ce20Keys,flight:hc10Flight,geometry:hc10ShipGeometry,
 sample:hc10FlightSample,flightAssets:hc10FlightAssets,dialogue:dialogueFrameDraw,face:msgFaceUse,pilot:ce20Pilot,bmf:bmfDraw,name:pilotNameDraw},
 end:145,last:null,active:false,events:[],draws:{},fontInstalled:false,fontTints:new Map(),
 shots:[['report',26.4,34],['relief',34,39],['alarm',39,44],['federation',44,57],['horror',57,62],
 ['base',62,72],['waters',72,82],['earth',82,94],['solar',94,105],['growth',105,112],
 ['scream',112,119],['escape',119,127],['return',127,135],['credits',135,145],['card',145,Infinity]]};
for(const a of Object.values(INV20_ART.images))XART._src[a.key]=a.path;
for(const bank of Object.values(INV20_ART.banks))for(const a of bank)XART._src[a.key]=a.path;
const INV20_FLEET=['ns9e_wskim_idle','ns9e_pneedle_idle','ns9e_vmanta_idle','ns9x_dreadv',
 'nef_s1_missile_gunboat_intact_idle','nef_s1_river_patrol_boat_intact_idle'];
function inv20Keys(){return [...Object.values(INV20_ART.images).map(a=>a.key),...Object.values(INV20_ART.banks).flatMap(b=>b.map(a=>a.key)),
 ...PL11.keys('blue_rift'),...PL11.keys('black_void'),...INV20_FLEET,...DR21_ART.banks.jet.map(a=>a.key),
 'cut_furyhq_command_center','cinend_deep_space'];}
ce20Keys=function(pk=run.pilot){const retired=new Set([...Object.values(CE20_ART).map(a=>a.key),...AP10_CIN_ART.void.map(a=>a.key),'cinend_bof2_shadow']);return [...new Set([...INV20.base.ceKeys(pk).filter(k=>!retired.has(k)),...inv20Keys()])];};
victoryEndingKeys=function(){const old=new Set(AP10_CIN_ART.void.map(a=>a.key));return [...new Set([...INV20.base.keys().filter(k=>!old.has(k)),...inv20Keys()])];};
hc10FlightAssets=function(pk){const old=new Set(AP10_CIN_ART.void.map(a=>a.key));return [...INV20.base.flightAssets(pk).filter(a=>!old.has(a.key)),...PL11.keys('blue_rift').map(key=>({key}))];};
function inv20InstallFont(){if(INV20.fontInstalled||!XART.rdy('inv20_font'))return;
 BMF.invasion={img:XART.get('inv20_font'),map:INV20_ART.font};INV20.fontInstalled=true;}
// White master glyphs need an alpha-mask colour treatment: luminance-preserving
// sprite tinting correctly leaves white white, which hides pilot-name colours.
bmfDraw=function(k,text,x,y,h,alpha,color,tintA,outline){
 if(k!=='invasion'||!color)return INV20.base.bmf.apply(this,arguments);
 const r=BMF.invasion,original=r.img;let tinted=INV20.fontTints.get(color);
 if(!tinted){tinted=document.createElement('canvas');tinted.width=original.width;tinted.height=original.height;const g=tinted.getContext('2d');g.drawImage(original,0,0);g.globalCompositeOperation='source-in';g.fillStyle=color;g.fillRect(0,0,tinted.width,tinted.height);tinted.complete=true;tinted.naturalWidth=tinted.width;tinted.naturalHeight=tinted.height;if(INV20.fontTints.size>=16)INV20.fontTints.delete(INV20.fontTints.keys().next().value);INV20.fontTints.set(color,tinted);}
 r.img=tinted;try{return INV20.base.bmf(k,text,x,y,h,alpha,null,0,outline);}finally{r.img=original;}
};
function inv20Color(who,fallback='#98dcff'){const p=PILOTS.find(p=>p.key===String(who).toLowerCase()||p.name===String(who).toUpperCase());return p?.tint||dialogueNameColor(who,fallback);}
msgFaceUse=function(face){inv20InstallFont();const cinematic=INV20.active||state===GS.CUTSCENE||state===GS.CAMPAIGNINTRO||state===GS.VICTORY||
 (typeof boss!=='undefined'&&v18Owned(boss)&&boss._r30.mode==='dr5Monologue');
 return INV20.base.face(cinematic&&(face==='dialogue'||face==='cutscene')&&INV20.fontInstalled?'invasion':face);};
pilotNameDraw=function(name,cx,cy,h,color,alpha){if(INV20.fontInstalled&&(INV20.active||state===GS.CUTSCENE||state===GS.CAMPAIGNINTRO||state===GS.VICTORY)){
 const before=_msgFace;INV20.base.face('invasion');msgText(name,cx,cy,h,inv20Color(name,color),1,alpha);INV20.base.face(before);return;
 }return INV20.base.name.apply(this,arguments);};
function inv20Panel(x,y,w,h){if(!XART.rdy('inv20_panel'))return false;
 const im=XART.get('inv20_panel'),sx=[0,40,472,512],sy=[0,27,103,128],e=Math.min(25,w*.07),v=Math.min(18,h*.18),dx=[x,x+e,x+w-e,x+w],dy=[y,y+v,y+h-v,y+h];
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.fillStyle='#030911';ctx.fillRect(x+e,y+v,w-2*e,h-2*v);
 for(let r=0;r<3;r++)for(let c=0;c<3;c++)ctx.drawImage(im,sx[c],sy[r],sx[c+1]-sx[c],sy[r+1]-sy[r],dx[c],dy[r],dx[c+1]-dx[c],dy[r+1]-dy[r]);ctx.restore();
 INV20.draws.panel=(INV20.draws.panel||0)+1;return true;}
dialogueFrameDraw=function(who,tint,x,y,w,h){
 if(INV20.active||state===GS.CUTSCENE||state===GS.CAMPAIGNINTRO||state===GS.VICTORY||v18Owned(boss)&&boss._r30.mode==='dr5Monologue'){
  if(inv20Panel(x,y,w,h))return true;
 }return INV20.base.dialogue.apply(this,arguments);
};
function inv20Pose(pk,x,bottom,height,t=0,horror=false){
 const a=INV20_ART.images[pk+(horror?'_horror':'')];if(!a||!XART.rdy(a.key))return INV20.base.pilot(pk,x,bottom,height,t);
 const k=height/384;ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),x-128*k,bottom-384*k,256*k,384*k);ctx.restore();
 INV20.draws[a.key]=(INV20.draws[a.key]||0)+1;CE20.draws[a.key]=(CE20.draws[a.key]||0)+1;return {pilot:pk,key:a.key,x,bottom,height,horror};
}
ce20Pilot=function(pk,x,bottom,height,t=0,alpha=1){if(INV20.active||BOFCinematicDirector.active){ctx.save();ctx.globalAlpha*=alpha;const r=inv20Pose(pk,x,bottom,height,t,false);ctx.restore();return r;}return INV20.base.pilot.apply(this,arguments);};
function inv20Text(who,text,W,H,shown=text.length,alpha=1){
 const w=Math.min(W*.94,1120),h=H*(W/H<1?.27:.225),x=(W-w)/2,y=H-h-13,
 color=inv20Color(who);
 ctx.save();ctx.globalAlpha*=alpha;inv20Panel(x,y,w,h);msgFaceUse('dialogue');
 msgDrawBlock({text:who.toUpperCase(),x:x+22,y:y+10,w:w-44,h:22,maxH:16,minH:10,lineMul:1.12,color,alpha:1,tintA:1,outline:false,align:'left'});
 msgDrawBlock({text:text.toUpperCase(),budget:shown,x:x+24,y:y+37,w:w-48,h:h-49,maxH:15,minH:9,lineMul:1.23,color:'#f7f9ff',alpha:1,tintA:1,outline:false,align:'left',stableCenter:true});
 msgFaceUse(null);ctx.restore();INV20.caption={who,text,color,x,y,w,h,shown};
}
victoryCaption=function(who,text,W,H,alpha=1){return inv20Text(who,text,W,H,text.length,alpha);};
hc10ShipGeometry=function(pk,view){
 // A nose-first arrival stays nose-first through approach, touchdown and parking.
 if(state===GS.VICTORY&&drawVictory._t>=6&&drawVictory._t<26.4)view='front';
 return INV20.base.geometry(pk,view);
};
hc10FlightSample=function(t,pk){const s=INV20.base.sample(t,pk);if(t>=6){s.view='front';s.bank=hc10ShipKey(pk,'front');}return s;};
hc10Flight=function(t,pk,R){
 const s=hc10FlightSample(t,pk),width=R.w*s.width;
 if(t<2.75){const pose=PL11.sequence('blue_rift',t,{form:.65,loop:1.4,close:.7}),size=R.h*.76;
  PL11.draw(ctx,pose,R.x+R.w*.5,R.y+R.h*.37,size,k=>XART.get(k),1);
  HC10.portal={bank:'blue_rift',source:PL11_ART.blue_rift[pose.phase].frames[pose.from].key,phase:pose.phase,size,visible:true};
 }else HC10.portal=null;
 hc10StaticShip(pk,s.view,R.x+R.w*s.x,R.y+R.h*s.y,width);
 HC10.last={...s,rect:R,jet:{x:R.x+R.w*s.x,y:R.y+R.h*s.y,width,nativeWidth:width},portal:HC10.portal};return HC10.last;
};
function inv20Image(name,x,y,width,angle=0,alpha=1){
 const key=INV20_ART.images[name]?.key||name;if(!XART.rdy(key))return false;const im=XART.get(key),r=ce20Ink(key);if(!r)return false;
 const k=width/r[2];ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,...r,-width/2,-r[3]*k/2,width,r[3]*k);ctx.restore();INV20.draws[key]=(INV20.draws[key]||0)+1;return true;
}
function inv20Bank(bank,t,x,y,width,once=true){const rows=INV20_ART.banks[bank],i=once?Math.min(rows.length-1,Math.floor(clamp(t,0,1)*(rows.length-1))):Math.floor(t*12)%rows.length,a=rows[i];if(!a||!XART.rdy(a.key))return;
 const k=width/a.w;ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),x-a.pivot[0]*k,y-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();INV20.draws[a.key]=(INV20.draws[a.key]||0)+1;
 return {bank,index:i,key:a.key,x,y,width,pivot:a.pivot};}
function inv20Portal(bank,t,x,y,size,form=.8,loop=Infinity,close=.8){const pose=PL11.sequence(bank,t,{form,loop,close});PL11.draw(ctx,pose,x,y,size,k=>XART.get(k),1);return pose;}
function inv20Squad(W,H,t,horror=false){const order=CE20.pilots,cast=[],narrow=W/H<1.2;
 for(let i=0;i<order.length;i++){const row=narrow?Math.floor(i/5):0,col=narrow?i%5:i,
  x=W*(narrow?(row?.17:.10)+col*(row?.22:.20):.075+i*.106),bottom=H*(narrow?(row?.72:.49):.72),height=H*(narrow?.27:.43);
  cast.push(inv20Pose(order[i],x,bottom,height,t,horror));}return cast;
}
function inv20Alarm(W,H,t){ctx.save();ctx.fillStyle='rgba(225,0,15,'+(.11+.13*(.5+.5*Math.sin(t*5.8)))+')';ctx.fillRect(0,0,W,H);ctx.restore();}
function inv20AirFleet(W,H,q,orbit=false){const units=[];
 for(let i=0;i<28;i++){const col=i%7,row=(i/7)|0,progress=((q*.016+col*.137+row*.077)%1),x=W*(orbit?.12+progress*.76:progress),
  y=H*(orbit?.13+row*.14:.075+row*.105),key=i%5===0?'ns9x_dreadv':INV20_FLEET[i%3],w=H*(orbit?(i%5===0?.11:.042):.045+row*.018);
  inv20Image(key,x,y,w,Math.PI);units.push({key,x,y,w});}return units;
}
function inv20Boats(W,H,q,R){const units=[];
 for(let row=0;row<4;row++)for(let col=0;col<5;col++){const x=(.08+col*.11+row*.017+q*.002)*512,y=(.29+row*.13)*288,
  px=R.x+x*R.w/512,py=R.y+y*R.h/288,key=INV20_FLEET[4+(col+row)%2],w=R.w*(.045+row*.006);
  inv20Image(key,px,py,w,Math.PI/3);units.push({key,x:px,y:py,w});}return units;
}
function inv20Cue(S,id,t,name){const prior=S.inv20;if(!prior||t<prior.time-.01)S.inv20={time:t,cues:new Set()};const s=S.inv20;
 if(!s.cues.has(id)){s.cues.add(id);const play=s.smooth;
  if(play)Snd.play(name);INV20.events.push({id,name,t,played:!!play});if(INV20.events.length>90)INV20.events.shift();}
}
function inv20Draw(t,W,H,S){
 const shot=INV20.shots.find(a=>t>=a[1]&&t<a[2])||INV20.shots.at(-1),name=shot[0],q=t-shot[1],duration=shot[2]-shot[1],u=clamp(q/duration,0,1),pk=hl10Pilot(run.pilot),
 partner=coopActive()?p2Pilot().key:null;let cast=[],units=[],bank=null,dialogue=null;INV20.active=true;
 if(!S.inv20||t<S.inv20.time-.01)S.inv20={time:t,cues:new Set(),smooth:false};else S.inv20.smooth=t>S.inv20.time&&t-S.inv20.time<.25;
 const chain=['base','waters','earth','solar'];
 if(INV20.last?.scene!==name){INV20.transition=null;if(chain.includes(name)&&S.inv20.smooth){const image=document.createElement('canvas');image.width=cv.width;image.height=cv.height;image.getContext('2d').drawImage(cv,0,0);INV20.transition={image,scene:name};}}
 ctx.fillStyle='#01030b';ctx.fillRect(0,0,W,H);
 if(['report','relief','alarm','federation','horror'].includes(name)){
  ce20Cover('cut_furyhq_command_center',W,H,q,1.06);
  if(name==='report'){
   const entering=hl10Ease(q/1.3);cast.push(inv20Pose(pk,lerp(-W*.1,W*(partner?.34:.40),entering),H*.72,H*.58,q));
   if(partner)cast.push(inv20Pose(partner,lerp(W*1.1,W*.68,entering),H*.72,H*.55,q));
   dialogue=[cinPilotName(pk),partner?'We got him! Dracodia is down. We both made it back. Tell everyone - it is finally over!':'We got him! Dracodia is down. I made it back. Tell everyone - it is finally over!'];
  }else if(name==='relief'){
   cast=inv20Squad(W,H,q,false);dialogue=['AXEL','All pilots accounted for. You brought our people home. We can finally breathe.'];
  }else{
   const monitorW=Math.min(W*.58,H*.9),monitorH=H*.28,mx=(W-monitorW)/2,my=H*.05;
   inv20Panel(mx,my,monitorW,monitorH);ctx.save();ctx.beginPath();ctx.rect(mx+18,my+16,monitorW-36,monitorH-32);ctx.clip();
   ctx.translate(mx,my);ce20Cover(INV20_ART.images.earth.key,monitorW,monitorH,q,1);ctx.restore();
   cast=inv20Squad(W,H,q,true);inv20Alarm(W,H,q);
   if(name==='alarm'){dialogue=['FURY COMMAND','RED ALERT! Priority transmission from the Space Federation. Put it on the main screen!'];inv20Cue(S,'alarm',t,'stage3AtomicSiren');}
   if(name==='federation'){
    const line=Math.min(2,Math.floor(q/4.34));dialogue=['SPACE FEDERATION',[
     'Fury Command, this is the Space Federation. Digital black holes are opening across the orbital defense network!',
     'Alien drones are pouring through. They are hacking our systems and turning our own defenses against us!',
     'They have broken the Earth perimeter. They are swarming above your planet. They are coming for your skies!'][line]];inv20Cue(S,'federation-'+line,t,line?'crackle':'blip');
   }
   if(name==='horror'){dialogue=['DECKER','Those signals... they are multiplying. The skies, the sea, the entire planet. This was only the beginning.'];inv20Cue(S,'horror',t,'crackle');}
  }
 }else if(name==='base'){
  ce20Cover(INV20_ART.images.base.key,W,H,q,lerp(1.48,1,u));units=inv20AirFleet(W,H,q);inv20Alarm(W,H,q);
  dialogue=['FURY COMMAND','Air contacts over the base! Every altitude. Every approach. Scramble all remaining aircraft!'];inv20Cue(S,'air',t,'jetDash');
 }else if(name==='waters'){
  const R=ce20Cover(INV20_ART.images.coast.key,W,H,q,lerp(1.45,1,u));if(R)units=inv20Boats(W,H,q,R);
  dialogue=['COASTAL DEFENSE','Warboats approaching the peninsula! The entire coast is under siege!'];inv20Cue(S,'sea',t,'blip');
 }else if(name==='earth'){
  ce20Cover(INV20_ART.images.earth.key,W,H,q,lerp(1.4,1,u));
  for(let i=0;i<4;i++)inv20Portal('black_void',q+i*.7,W*(.15+i*.23),H*(i%2?.25:.54),H*.24);
  units=inv20AirFleet(W,H,q,true);dialogue=['SPACE FEDERATION','More rifts. More fleets. They are surrounding Earth. All surviving units, respond!'];inv20Cue(S,'earth',t,'warpGate');
 }else if(name==='solar'){
  ce20Cover(INV20_ART.images.solar.key,W,H,q,lerp(1.55,1,u));dialogue=q<5?['SPACE FEDERATION','The breach extends beyond Earth. We are detecting their signal across the solar system.']:null;inv20Cue(S,'solar',t,'warpGate');
 }else if(name==='growth'){
  ce20Cover('cinend_deep_space',W,H,q);bank=inv20Bank('emerge',u,W*.54,H*.45,H*lerp(.35,.62,u));inv20Cue(S,'growth',t,'crackle');
 }else if(name==='scream'){
  ce20Cover('cinend_deep_space',W,H,q);const zoom=hl10Ease(clamp((q-1.2)/4.8,0,1)),width=H*lerp(.62,2.4,zoom),
   rootY=H*.47+90*(width-H*.62)/288+H*.18*zoom;
  // Track the skull as it approaches; a cable-root zoom would put his face
  // above the screen and show only his chest at the exact scream climax.
  bank=inv20Bank('roar',clamp(q/2.6,0,1),W*.54,rootY,width);inv20Cue(S,'scream',t,'dracodiaShriek');
 }else if(name==='escape'){
  ce20Cover(INV20_ART.images.solar.key,W,H,q);const portal=inv20Portal('black_void',q,W*.72,H*.4,H*.60,1.1,4.4,1.5),p=hl10Ease(clamp((q-1.4)/4.2,0,1));
  if(q<5.8){ctx.save();ctx.globalAlpha=1-hl10Ease(clamp((q-4.2)/1.5,0,1));bank=inv20Bank('roar',1,lerp(W*.2,W*.72,p),lerp(H*.67,H*.4,p),H*lerp(.34,.035,p));ctx.restore();}
  if(q>6.2)hl10Fade(clamp((q-6.2)/1.2,0,1),W,H);inv20Cue(S,'escape',t,'warpGate');
 }else if(name==='return'){
  inv20Title('BULLETS OF FURY',W,H,.37,Math.min(W*.073,H*.10),'#ffe291');inv20Title('WILL RETURN!',W,H,.58,Math.min(W*.062,H*.08),'#ecf3ff');
 }else if(name==='credits'){
  inv20Title('THE FURY PILOTS',W,H,.12,Math.min(W*.045,H*.05),'#ffe291');
  for(let i=0;i<CE20.pilots.length;i++){const row=Math.floor(i/3),col=i%3,p=CE20.pilots[i];inv20Title(p.toUpperCase(),W,H,.33+row*.12,Math.min(H*.033,W*.032),inv20Color(p),W*(.18+col*.32));}
  inv20Title('THANK YOU FOR PLAYING',W,H,.80,Math.min(W*.043,H*.047),'#eff6ff');
 }else inv20Card(t,W,H);
 if(dialogue)inv20Text(...dialogue,W,H,Math.floor(Math.max(0,q-.12)*37));
 if(name!=='scream'&&name!=='escape'&&name!=='card'&&!chain.includes(name))hl10Fade(1-hl10Ease(q/.45),W,H);
 if(INV20.transition?.scene===name){
  if(q<.9){const v=hl10Ease(q/.9),target={base:[.50,.67,.18],waters:[.82,.60,.22],earth:[.50,.48,.12],solar:[.54,.55,.035]}[name],
   w=lerp(W,W*target[2],v),h=w*H/W,x=lerp(W/2,W*target[0],v),y=lerp(H/2,H*target[1],v);
   ctx.save();ctx.globalAlpha=1-v;ctx.imageSmoothingEnabled=false;ctx.drawImage(INV20.transition.image,x-w/2,y-h/2,w,h);ctx.restore();
  }else INV20.transition=null;
 }
 INV20.last={scene:name,t,q,u,pilot:pk,partner,cast,units,bank,dialogue};INV20.active=false;if(S.inv20)S.inv20.time=t;
}
function inv20Title(text,W,H,y,h,color,x=W/2){msgFaceUse('dialogue');msgText(text,x,H*y,h,color,1,1,.04);msgFaceUse(null);}
function inv20Card(t,W,H){const pk=hl10Pilot(run.pilot),other=coopActive()?p2Pilot().key:null,total=(run.score||0)+(other?(run2.score||0):0);
 inv20Title('MISSION COMPLETE',W,H,.13,Math.min(H*.06,W*.065),'#ffe291');inv20Title('BULLETS OF FURY WILL RETURN!',W,H,.25,Math.min(H*.03,W*.033),'#d4e3ff');
 ce20Portrait(pk,W*(other?.32:.5),H*.44,Math.min(H*.23,W*(other?.35:.6)));if(other)ce20Portrait(other,W*.68,H*.44,Math.min(H*.23,W*.35));
 inv20Title(other?cinPilotName(pk)+' + '+cinPilotName(other):cinPilotName(pk),W,H,.60,Math.min(H*.027,W*.035),dialogueNameColor(pk));
 inv20Title('FINAL SCORE '+pad(total,8),W,H,.72,Math.min(H*.034,W*.036),'#ffffff');if(t>INV20.end+5)controlHintRow([['pad_start','TITLE']],H-22,W/2,W-24);
}
drawVictory=function(dt){
 if(run.mode==='arcade'||!drawVictory._trueEnding||!drawVictory._ready||drawVictory._t<26.4)return INV20.base.draw.call(this,dt);
 victoryEndingWarm();drawVictory._t=(drawVictory._t||0)+dt;drawVictory._scroll=(drawVictory._scroll||0)+dt;
 const W=cutsceneViewWidth(),H=VH,S=drawVictory._sfx||(drawVictory._sfx={});inv20Draw(drawVictory._t,W,H,S);
 const click=!!Input.mouse.down&&!drawVictory._md;drawVictory._md=!!Input.mouse.down;
 if(drawVictory._t>INV20.end+5&&(Input.menuConfirm()||click)){drawVictory._t=0;drawVictory._scroll=0;drawVictory._sfx={};drawVictory._ready=false;setState(GS.TITLE);menuIndex=0;Audio.startMusic('title');}
};
globalThis.BOF_INVASION_ENDING=INV20;
