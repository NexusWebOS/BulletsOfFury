'use strict';
/* Earned gate-eight warp presentation. Native warp-white/map unlock, Stage9
   selection, launch, armor, rift snapshot and failure return keep their owners. */
const WP1110={version:1,base:{start:s9WarpStart,tick:s9WarpTick,draw:s9WarpDraw,keys:d1110Keys,primary:cb1110Primary,secondary:cb1110Secondary,readings:cb1110Readings,load:stageLoadBegin,launch:drawLaunch,begin:beginStage,cancel:BOFCinematicDirector.cancel,preview:D1110.preview},pending:null,last:null,events:[]};
for(const[n,a]of Object.entries(WP1110_ART.banks)){D1110_ART.banks[n]=a;XART._src[a.key]=a.path;}
Snd.prepare(['warpCharge','warpBurst','blip']);
function wp1110Ship(p=run.pilot){return 'space-'+p+'-warp';}
function wp1110Beat(p,id,duration,who,text,extra={}){return{id,duration,who:d1110Who(who,p),text,d1110:true,warp1110:true,art:'comic',layout:'panel',people:[],readings:[],comic:'vertical',_cueSet:new Set(),delay:.2,...extra};}
function wp1110Rows(kind,p=run.pilot){const L=(...v)=>wp1110Beat(p,...v);return kind==='departure'?[
 L('W5901',4.6,'SYSTEM','',{bank:wp1110Ship(p),clip:[0],times:[100000],comic:'stack',screen:true,readings:['GATES: 08 / 08','DRIVE COILS: CHARGING'],cue:'warpCharge',cueAt:.12}),
 L('W5902',4.2,'PILOT','Vector locked. Taking the jump.',{bank:wp1110Ship(p),clip:[1,2],times:[900,100000],comic:'vertical',readings:['LOCAL NAV: LOCKED','WARP DRIVE: ENGAGED']}),
 L('W5903',4.4,'SYSTEM','',{bank:wp1110Ship(p),clip:[2,3,4,5],times:[900,950,1050,100000],comic:'impact',screen:true,readings:['JUMP VECTOR: COMMITTED','DRIVE: MAXIMUM'],cue:'warpBurst',cueAt:.08})
 ]:[
 L('A901',4.8,'PILOT','Jump complete. Checking the other side.',{bank:'warp-arrival',times:[180,200,250,300,350,100000],flight:true,comic:'slash',readings:['WARP DRIVE: DISENGAGED','LOCAL SENSORS: RESTORED']}),
 L('A902',4.2,'TECH','Stay on local controls. We are off the main route.',{bank:'warp-arrival',clip:[5],times:[100000],flight:true,comic:'vertical',readings:['NAVIGATION: LOCAL CONTROL','SECTOR: UNCHARTED']})
 ];}
function wp1110ScreenFrame(b,t){return b.id==='W5901'?d1110Frame({bank:'warp-drive',delay:.2,times:WP1110_ART.banks['warp-drive'].durations.map((n,i)=>i===5?100000:n)},t):5;}
d1110Keys=function(rows,p=run.pilot){const keys=WP1110.base.keys(rows,p);for(const b of rows){if(!b.warp1110)continue;keys.push(WP1110_ART.banks['warp-drive'].key);for(const pk of d1110Active(p))keys.push(WP1110_ART.banks[wp1110Ship(pk)].key,WP1110_ART.banks['warp-native-'+pk].key);}return [...new Set(keys)];};
cb1110Primary=function(b,s,box){if(!b.warp1110)return WP1110.base.primary(b,s,box);
 const f=d1110Frame(b,s.t);cb1110Cover(b.bank,f,box,b.flight?0:.16);
 if(b.flight&&f>=2){const a=WP1110_ART.banks[b.bank],r=br1110Rect(a,box,0),u=clamp((s.t-.8)/3.6,0,1),active=d1110Active();active.forEach((pk,i)=>{const x=r.x+256*r.k+(i-(active.length-1)/2)*150,y=r.y+(b.id==='A902'?210:lerp(338,238,u))*r.k;d1110Bank('warp-native-'+pk,0,Math.round(x-64),Math.round(y-64));});}
 WP1110.last={shot:b.id,bank:b.bank,frame:f,pilot:run.pilot,pilots:d1110Active(),arrival:!!b.flight};
};
function wp1110Insert(name,f,box){const[x,y,w,h]=box,size=Math.min(w,h);d1110Bank(name,f,Math.round(x+(w-size)/2),Math.round(y+(h-size)/2),Math.round(size),Math.round(size));}
cb1110Secondary=function(b,s,box,index=1){if(!b.warp1110)return WP1110.base.secondary(b,s,box,index);
 const partner=d1110Active().find(pk=>pk!==run.pilot);
 if(b.screen&&index===1){wp1110Insert('warp-drive',wp1110ScreenFrame(b,s.t),box);return;}
 if(partner&&!b.flight){wp1110Insert(wp1110Ship(partner),d1110Frame(b,s.t),box);return;}
 cb1110Face(index===2?run.pilot:b.flight?d1110Tech():run.pilot,box,s.t,b.who===run.pilot.toUpperCase()&&s.shown<b.text.length);
};
cb1110Readings=function(b,t){if(!b.warp1110)return WP1110.base.readings(b,t);let rows=b.readings;
 if(b.id==='W5901')rows=['GATES: 08 / 08','DRIVE COILS: '+[20,40,70,100,100,100][wp1110ScreenFrame(b,t)]+'%'];
 if(b.id==='W5903'){const f=d1110Frame(b,t);rows=f<3?['VELOCITY: CLIMBING','JUMP VECTOR: LOCKED']:f<5?['DRIVE: MAXIMUM','JUMP: COMMITTED']:['WARP SIGNAL: IN TRANSIT','NAVIGATION: HOLD VECTOR'];}
 if(!rows?.length)return;const x=b.comic==='impact'?600:b.comic==='stack'?552:532,y=b.comic==='impact'?142:b.comic==='stack'?150:300,w=b.comic==='impact'?300:b.comic==='stack'?352:368,h=b.comic==='impact'?76:b.comic==='stack'?84:90;
 ui20Panel('',x,y,w,h,false);msgFaceUse('dialogue');rows.forEach((text,i)=>msgText(text,x+w/2,y+36+i*22,11,'#c6f5ea',1,1,.04));msgFaceUse(null);
};
function wp1110Resume(P){if(WP1110.pending!==P||P.released)return;P.released=true;WP1110.pending=null;
 if(s9warp!==P.w)return;setState(GS.PLAY);WP1110.base.tick.call(this,Math.max(0,S9W_DRAW-P.w.t)+.001);WP1110.events.push({event:'native-white',pilot:run.pilot});
}
s9WarpStart=function(){if(WP1110.pending||s9warp?.wp1110)return;
 if(run.stage!==5||debugFight)return WP1110.base.start.apply(this,arguments);
 // The native burst starts immediately. Defer its one report to the actual
 // acceleration beat, through the same shared sound owner used by the cinema.
 const burst=Audio.SFX?.warpBurst;let result;if(burst)Audio.SFX.warpBurst=()=>{};
 try{result=WP1110.base.start.apply(this,arguments);}finally{if(burst)Audio.SFX.warpBurst=burst;}
 if(!s9warp)return result;const P={w:s9warp,scene:null,released:false};WP1110.pending=P;
 if(d1110Play('stage5-9-warp',wp1110Rows('departure'),()=>wp1110Resume(P))){P.scene=BOFCinematicDirector.current;P.w.wp1110=true;WP1110.events.push({event:'start',pilot:run.pilot});}
 else{WP1110.pending=null;if(burst)burst();}return result;
};
s9WarpTick=function(dt){if(WP1110.pending?.w===s9warp)return;return WP1110.base.tick.apply(this,arguments);};
s9WarpDraw=function(){const W=s9warp;if(!W?.wp1110)return WP1110.base.draw.apply(this,arguments);
 if(WP1110.pending?.scene===BOFCinematicDirector.current){const s=WP1110.pending.scene;d1110Viewport();d1110Visual(s.beats[s.i],s);return;}
 if(W.ph==='white'){const a=WP1110_ART.banks[wp1110Ship()],im=XART.get(a.key),w=cv.width/SS,h=cv.height/SS,size=Math.max(w,h);ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;ctx.drawImage(im,1026,514,508,508,Math.round((w-size)/2),Math.round((h-size)/2),size,size);ctx.restore();WP1110.last={shot:'native-warp-white',pilot:run.pilot};return;}
 return WP1110.base.draw.apply(this,arguments);
};
BOFCinematicDirector.cancel=function(){const P=WP1110.pending;if(P?.scene&&P.scene===this.current){WP1110.pending=null;P.cancelled=true;if(s9warp===P.w)s9warp=null;try{Audio.warpAmbienceStop?.();Audio.setWarpMix?.(0);}catch(_e){}}return WP1110.base.cancel.apply(this,arguments);};
drawLaunch=function(dt){if(run.stage===9&&state===GS.LAUNCH&&!run._warpArrival9&&!debugFight&&!tutLive()){
 run._warpArrival9=true;if(d1110Play('stage9-approach',wp1110Rows('arrival'),()=>setState(GS.LAUNCH))){WP1110.events.push({event:'arrival',pilot:run.pilot});return;}run._warpArrival9=false;
 }return WP1110.base.launch.apply(this,arguments);};
beginStage=function(n){const result=WP1110.base.begin.apply(this,arguments);if(n===9)run._warpArrival9=false;return result;};
stageLoadBegin=function(n,keys){const rows=n===5?wp1110Rows('departure'):n===9?wp1110Rows('arrival'):[];return WP1110.base.load.call(this,n,[...(keys||[]),...(rows.length?d1110Keys(rows):[])]);};
D1110.preview=S113.preview=async function(id,p='cole',route='left',partner=null){if(id==='warp-5-9'||id==='arrival-9'){
 BOFCinematicDirector.cancel();run.pilot=p;pilotIndex=PILOTS.findIndex(q=>q.key===p);run.mode='campaign';coopOn=D1110.pilots.includes(partner)&&partner!==p;if(coopOn){run2.pilot=partner;p2Index=PILOTS.findIndex(q=>q.key===partner);}Input.clearTaps();return d1110Play('review-'+id,wp1110Rows(id==='warp-5-9'?'departure':'arrival',p),()=>setState(GS.TITLE));
 }return WP1110.base.preview(id,p,route,partner);};
WP1110.rows=wp1110Rows;window.BOF_WARP_1110=WP1110;
