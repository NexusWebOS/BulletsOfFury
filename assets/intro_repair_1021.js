"use strict";
/* Campaign opening only. Native campaign completion, aircraft and input remain
   authoritative; PixelLab plates never replace the selected live aircraft. */
const IP21={base:{keys:campaignIntroKeys,start:campaignIntroStart,visual:campaignIntroVisual},
 draws:{},last:null,caption:null,logo:null,jet:null,events:[],scrollRate:410*9};
IP21.base.viewport=_setCinematicViewport;
_setCinematicViewport=function(on){
 if(!on||state!==GS.CAMPAIGNINTRO)return IP21.base.viewport.apply(this,arguments);
 // The older 640px minimum is stretched into portrait CSS. This opening takes
 // the actual display aspect so aircraft, faces and glyphs retain proportions.
 CINEMA_VW=Math.max(2,Math.round(VH*window.innerWidth/Math.max(1,window.innerHeight)));
 if(cv.width!==CINEMA_VW*SS||cv.height!==VH*SS){cv.width=CINEMA_VW*SS;cv.height=VH*SS;}
 document.body.classList.add('cinematic-full');ctx.imageSmoothingEnabled=false;
 if(window.__bofFit)window.__bofFit();else fitCanvas();
};
for(const a of Object.values(IP21_ART.banks))XART._src[a.key]=a.path;
function ip21Keys(){return Object.values(IP21_ART.banks).map(a=>a.key);}
campaignIntroKeys=function(){return [...IP21.base.keys(),...ip21Keys(),'ui20_dialogue-a'];};
campaignIntroStart=function(){Snd.prepare(['bossWeaponCharge','hammerImpact','jetDash','warpGate']);return IP21.base.start.apply(this,arguments);};
function ip21Line(b,c){
 const voice=CAMPAIGN_SOLO_LINES[c.pilot]||CAMPAIGN_SOLO_LINES.axel;
 if(b.pilotLine==='resolve')return voice.resolve+' Whoever did this is going to pay.';
 return b.pilotLine?voice[b.pilotLine]:b.text||'';
}
IP21.beats=[];
for(const original of CAMPAIGN_INTRO_BEATS){
 const b={...original};
 if(b.bg==='cin_origin_radio'){delete b.bg;b.dispatch='dispatch';b.who='LIZZIE';b.text='Fury flight, report in. Every pilot channel is gone. Decker, something has taken over the network.';}
 if(b.bg==='cin_origin_tower'){delete b.bg;b.dispatch='turn';b.who='DECKER';b.text='We gotta get to the others, now!';}
 IP21.beats.push(b);
 if(b.dispatch==='turn')IP21.beats.push({dispatch:'run',text:''});
}
let ip21At=0;
for(const b of IP21.beats){
 const chars=b.pilotLine?Math.max(...Object.keys(CAMPAIGN_SOLO_LINES).map(p=>ip21Line(b,{pilot:p}).length)):ip21Line(b,{pilot:'axel'}).length;
 b.duration=Math.max(b.dispatch==='run'?4.1:b.federation?7:5.5,b.duration||0,chars/CAMPAIGN_INTRO_CPS+CAMPAIGN_INTRO_READ_HOLD);
 b.at=ip21At;b.to=ip21At+=b.duration;
}
IP21.finaleAt=ip21At;IP21.end=ip21At+14;
function ip21Blit(bank,index,x,y,w,h,alpha=1){
 const a=IP21_ART.banks[bank];if(!a||!XART.rdy(a.key))return false;
 const f=clamp(index|0,0,a.frames-1),k=Math.min(w/a.w,h/a.h),dw=a.w*k,dh=a.h*k;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=alpha;
 ctx.drawImage(XART.get(a.key),(f%a.columns)*a.w,Math.floor(f/a.columns)*a.h,a.w,a.h,x-dw/2,y-dh/2,dw,dh);ctx.restore();
 IP21.draws[bank]=(IP21.draws[bank]||0)+1;return true;
}
function ip21Cover(bank,index,W,H){
 const a=IP21_ART.banks[bank];if(!a)return false;const k=Math.max(W/a.w,H/a.h);
 ctx.save();ctx.beginPath();ctx.rect(0,0,W,H);ctx.clip();const drawn=ip21Blit(bank,index,W/2,H/2,a.w*k,a.h*k);ctx.restore();return drawn;
}
function ip21Cue(c,id,at,name,previous){
 if(c.t<at)return;const seen=c._ip21Cues||(c._ip21Cues=new Set());if(seen.has(id))return;seen.add(id);
 const played=previous<at&&c.t-previous<.75;if(played)Snd.play(name);
 IP21.events.push({id,name,time:c.t,played});if(IP21.events.length>80)IP21.events.shift();
}
function ip21Pilot(pilot,W,H){
 const key='cin_pilot_'+pilot+'_helmet';if(!XART.rdy(key))return false;const im=XART.get(key),k=Math.max(W/im.width,H/im.height),w=im.width*k,h=im.height*k;
 ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);ctx.save();ctx.beginPath();ctx.rect(0,0,W,H);ctx.clip();ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,(W-w)/2,Math.min(0,(H-h)*.16),w,h);ctx.restore();
 IP21.last={kind:'pilot',pilot,key,fullScreen:true,background:'#000',w:W,h:H};return true;
}
function ip21Visual(b,c,t,W,H){
 if(b.federation){
  cinCover('cinend_deep_space',W,H,.5);const progress=clamp((t-.8)/4.4,0,1),a=IP21_ART.banks.corruption;
  const bank=t<.8?'clean':'corruption',frame=bank==='clean'?0:Math.min(a.frames-1,Math.floor(progress*a.frames));
  ip21Blit(bank,frame,W*.5,H*.39,Math.min(W*.67,H*.68),H*.68);
  IP21.last={kind:'satellite',bank,frame,progress};return;
 }
 if(b.dispatch){
  const a=IP21_ART.banks[b.dispatch],frame=Math.min(a.frames-1,Math.floor(t*(b.dispatch==='dispatch'?8:9)));
  if(W/H<1.2){ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);ip21Blit(b.dispatch,frame,W/2,H*.35,W,H*.57);}
  else ip21Cover(b.dispatch,frame,W,H);
  IP21.last={kind:'dispatch',bank:b.dispatch,frame};return;
 }
 if(b.pilotCam){
  ip21Pilot(b.pilotCam,W,H);msgFaceUse('dialogue');msgText('NO SIGNAL',W/2,H*.64,Math.max(12,H*.028),'#ff6868',1,.85,.06);msgFaceUse(null);return;
 }
 if(b.comic){
  IP21.base.visual.call(this,b,c,t*9/1.75,W,H);IP21.last={kind:'comic',pilot:c.pilot,scrollRate:IP21.scrollRate};
  if(b.pilotLine==='resolve'&&c.t>=IP21.finaleAt-.85)ip21Logo(c,c.t-(IP21.finaleAt-.85),W,H);
  return;
 }
 IP21.base.visual.apply(this,arguments);IP21.last={kind:'native',bg:b.bg};
}
function ip21Caption(b,c,W,H,alpha){
 if(alpha<=0)return;const text=ip21Line(b,c),p=PILOTS.find(p=>p.key===c.pilot),who=b.who==='PILOT'?(p?.name||c.pilot):b.who;
 const w=Math.min(W*.91,960),h=Math.min(H*.27,145),x=(W-w)/2,y=H-h-38,shown=Math.min(text.length,Math.floor((c.t-b.at)*CAMPAIGN_INTRO_CPS));
 ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha*=alpha;msgFaceUse('dialogue');
 const r=ui20Panel(who,x,y,w,h,false),content=ui20PanelContents(who,text,shown,null,r,14,16);
 msgFaceUse(null);ctx.restore();IP21.caption={...content,who,text,shown,x,y,w,h,body:content.text};
}
function ip21Logo(c,age,W,H){
 if(!XART.rdy('nbl_logo_0916'))return;const im=XART.get('nbl_logo_0916'),u=clamp(age/.32,0,1),e=1-Math.pow(1-u,3),w=Math.min(W*.69,H*1.15),h=w*im.height/im.width;
 const rumble=Math.max(0,1-age/1.35),x=lerp(-w,W/2,e)+Math.sin(age*97)*rumble*2.2,y=H*.29+Math.sin(age*83)*rumble*1.7;
 const fade=clamp(age/.16,0,1)*clamp((4.4-age)/.7,0,1);ctx.save();ctx.globalAlpha*=fade;ctx.imageSmoothingEnabled=false;ctx.drawImage(im,x-w/2,y-h/2,w,h);ctx.restore();
 const frame=Math.floor(age*24);if(frame<IP21_ART.banks.logo.frames)ip21Blit('logo',frame,x,y,w*1.25,h*1.6,fade);
 IP21.logo={key:'nbl_logo_0916',age,x,y,w,h,alpha:fade,frame,rumble};
}
function ip21Jet(c,q,W,H){
 const u=clamp((q-.55)/1.75,0,1),power=clamp((q-.15)/.65,0,1),y=H*(.68-1.1*Math.pow(u,2.6)),h=H*(.25-.06*u),x=W*.5;
 if(q>2.4)return;pt11OpeningShip(c.pilot,c.t,x,y,h,power);const {key,w,plume}=PT11_UI.ship;
 IP21.jet={pilot:c.pilot,key,x,y,w,h,power,plume,progress:u};
}
function ip21Finale(c,q,W,H,previous){
 campaignIntroJungle(W,H,(c.t-IP21.finaleAt)*9);ip21Jet(c,q,W,H);ip21Logo(c,q+.85,W,H);
 ip21Cue(c,'logo',IP21.finaleAt-.82,'hammerImpact',previous);ip21Cue(c,'boost',IP21.finaleAt+.16,'jetDash',previous);
 const black=clamp((q-2.15)/.65,0,1);ctx.fillStyle='rgba(0,0,0,'+black+')';ctx.fillRect(0,0,W,H);
 if(q>=2.8){
  const pilot=PILOTS.find(p=>p.key===c.pilot),name=pilot?.name||c.pilot,pronoun=['lizzie','falva'].includes(c.pilot)?'her':'his';
  const text='Detecting anomalies over the mysterious jungle, '+name+' sets off to find answers while '+pronoun+' communications system is down.',last="Good luck Commander. You'll need it.";
  const age=q-2.8,budget=Math.min(text.length,Math.floor(age*34)),tail=Math.min(last.length,Math.max(0,Math.floor((q-9)*34)));
  msgFaceUse('dialogue');const r={x:W*.10,y:H*.29,w:W*.80,h:H*.23};
  const layout=msgDrawBlock({text,budget,...r,maxH:Math.min(22,H*.041),minH:12,lineMul:1.35,color:'#f3f6ff',align:'center',stableCenter:true,valign:'middle',outline:false});
  msgDrawBlock({text:last,budget:tail,x:r.x,y:H*.60,w:r.w,h:H*.13,maxH:Math.min(22,H*.041),minH:12,lineMul:1.3,color:'#ffd47d',align:'center',stableCenter:true,valign:'middle',outline:false});msgFaceUse(null);
  IP21.narration={text,last,budget,tail,body:r,layout};
 }
 const fade=clamp(q-13,0,1);if(fade){ctx.fillStyle='rgba(0,0,0,'+fade+')';ctx.fillRect(0,0,W,H);}
 IP21.last={kind:'finale',q,fade,bullets:false};
}
drawCampaignIntro=function(dt){
 const c=campaignIntro,W=cutsceneViewWidth(),H=VH;ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
 if(!c){openStageSelect(1,{boot:true});return;}
 if(stateT>.15&&Input.menuStart()){campaignIntroFinish();return;}
 const b=IP21.beats.find(b=>c.t>=b.at&&c.t<b.to),keys=b?.federation?['clean','corruption']:b?.dispatch?[b.dispatch]:[];
 if(!campaignIntroReady()||!XART.rdy('ui20_dialogue-a')||keys.some(k=>!XART.rdy(IP21_ART.banks[k].key))){campaignIntroWarm();return;}
 if(b?.bg&&!XART.rdy(b.bg)){campaignIntroWarm();return;}
 if(b?.pilotCam&&!XART.rdy('cin_pilot_'+b.pilotCam+'_helmet')){campaignIntroWarm();return;}
 if(c.t>=IP21.finaleAt&&(!XART.rdy(IP21_ART.banks.logo.key)||!XART.rdy('nbl_logo_0916'))){campaignIntroWarm();return;}
 if(stateT>.15&&Input.menuConfirm()){
  if(b){const end=b.at+ip21Line(b,c).length/CAMPAIGN_INTRO_CPS;c.t=c.t<end?Math.min(b.to-.02,end+.02):b.to+.001;}
  else if(c.t<IP21.finaleAt+8.9)c.t=IP21.finaleAt+8.9;else c.t=IP21.end-.5;
 }
 const click=Input.mouse.down&&!c.md;c.md=!!Input.mouse.down;if(stateT>.35&&click){Input.mouse.down=false;campaignIntroFinish();return;}
 const previous=c.t;c.ready=true;c.t+=dt;const beat=IP21.beats.find(b=>c.t>=b.at&&c.t<b.to);
 if(beat){
  const line=ip21Line(beat,c),shown=Math.min(line.length,Math.floor((c.t-beat.at)*CAMPAIGN_INTRO_CPS));
  if(c.lastBeat!==beat){c.lastBeat=beat;c.lastShown=0;}dialogueLetterTicks(line,c.lastShown,shown);c.lastShown=shown;
  ip21Visual(beat,c,c.t-beat.at,W,H);
  if(beat.dispatch==='run')IP21.caption=null;else ip21Caption(beat,c,W,H,Math.min(clamp((c.t-beat.at)/.25,0,1),clamp((beat.to-c.t)/.25,0,1)));
  if(beat.federation)ip21Cue(c,'corruption',beat.at+.85,'bossWeaponCharge',previous);
  if(beat.pilotLine==='resolve')ip21Cue(c,'logo',IP21.finaleAt-.82,'hammerImpact',previous);
 }else ip21Finale(c,c.t-IP21.finaleAt,W,H,previous);
 if(c.t<IP21.end-1){msgFaceUse('dialogue');controlHintRow([['pad_a','NEXT'],['pad_start','SKIP SCENE']],H-20,W/2,W-24);msgFaceUse(null);}
 if(c.t>=IP21.end)campaignIntroFinish();
};
window.BOF_INTRO_REPAIR=IP21;
