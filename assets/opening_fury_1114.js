"use strict";
/* Mike's November14 opening: one readable crawl, then a selected-pilot Stage1 comic.
   This owner only wraps presentation and retains the original launch continuation. */
const FURY14={version:1,last:null,map:null,pending:false,cache:null,events:[],base:{
 introStart:campaignIntroStart,introDraw:drawCampaignIntro,deploy:sselDeploy,keys:d1110Keys,
 visual:d1110Visual,step:d1110Step,mapReset:cmap2Reset,mapCam:cmap2CameraTick,mapDraw:drawStageSelect,
 mapWorld:cmap2DrawWorld,ship:sselShipUpdate,cardDraw:drawIntro}};
XART._src.fury14_logo='assets/game/shared/cinematics/opening_1114/fury-division.png';
XART._src.fury14_boom='assets/game/shared/cinematics/opening_1114/boom.png';
const FURY14_TEXT=[
 ['2026. PLANET EARTH.',''],
 ['After the Cold War, peace returned.','But the world still needed guardians.',''],
 ['The United States Government and Air Force','formed a secret unit of elite pilots','from around the globe: the FURY DIVISION.',''],
 ['Their mission: defend Earth against','unforeseen attacks and unknown threats.',''],
 ['Generations came and went. Rivalries divided','the ranks. Nine pilots remained.',''],
 ['COLE. AXEL. FREEZER. YURI. MAVERICK.','FALVA. LIZZIE. DECKER. JUGGERNAUT.',''],
 ['Cole led the team. Decker kept them flying.','Their converted fighters used manual controls,','old machines built to answer to their pilots.',''],
 ['Then, without warning, everything changed.','Computers failed. Vehicles turned on their','drivers. Aircraft fell from peaceful skies.',''],
 ['Fighter jets attacked cities. Tanks rolled','into neighborhoods. Ships launched strikes','against one another. Earth descended into war.',''],
 ['Fury HQ lost contact with its scattered pilots.','No orders. No answers. No way to know','who was still out there.',''],
 ['Nine fighters. One chance to turn the tide.',''],
 ['Nobody knows for sure what will happen.','All we know is we must have hope.','Hope that the Fury Division can save us all...']
].flat();
FURY14.finalLine=FURY14_TEXT.length-3;
FURY14.scrollStop=(540+FURY14.finalLine*36-292)/17;
FURY14.total=6+FURY14.scrollStop+11;
FURY14.openKeys=['fury14_logo','cin_war_earth_peace','cin_war_civilian_collapse','cin_war_city_air_attack','cin_war_suburban_tanks','cin_war_naval_exchange'];
function fury14Ready(keys){let ok=bmfReady('dialogue');for(const k of keys)if(!XART.rdy(k))ok=false;return ok;}
function fury14Warm(p=run.pilot){
 const keys=[...FURY14.openKeys,'fury14_boom','cin_terrain_jungle_loop','ship_'+p,'ship_'+p+'_g1','ship_'+p+'_g2',
 C16_ART.banks['talk-'+p].key,'system_avatar_1109','cin_cockpit_front_fighter','scard_1'];
 fury14Ready(keys);map4eWarm();cmap2Warm();Snd.prepare?.(['expBig','jetDash','crackle']);return keys;
}
function fury14Line(text){
 const id=text;if(FURY14.cache?.has(id))return FURY14.cache.get(id);
 FURY14.cache??=new Map();const c=document.createElement('canvas');c.width=824;c.height=36;
 const g=c.getContext('2d');g.imageSmoothingEnabled=false;
 if(typeof pm27Draw==='function'&&pm27Live())pm27Draw(g,text,412,18,24,{family:'command',palette:'gold',width:810});
 else bmfDrawOn(g,'dialogue',text,412,3,24,'center');
 FURY14.cache.set(id,c);return c;
}
function fury14PixelReveal(next,progress,W=912,H=512){
 // Eight-pixel Venetian columns progress in a fixed diagonal pattern.
 if(progress>=1){next();return;}if(progress<=0)return;
 ctx.save();ctx.beginPath();for(let x=0;x<W;x+=24)for(let y=0;y<H;y+=24){
  const rank=((x/24)*7+(y/24)*11)%23;if(rank/23<progress)ctx.rect(x,y,24,24);
 }ctx.clip();next();ctx.restore();
}
function fury14Earth(key,t){
 cinCover(key,912,512,.5);if(key!=='cin_war_earth_peace'){
  const age=t%4.5;campaignIntroWarImpact(key,912,512,.5,age);
  if(key==='cin_war_civilian_collapse')campaignIntroWarVehicle(key,912,512,.5,Math.min(age,3.3));
 }
}
campaignIntroStart=function(done){
 const pilot=campaignIntroPickPilot();run.pilot=pilot;fury14Warm(pilot);FURY14.cache=null;
 campaignIntroPilot=pilot;campaignIntro={t:0,onDone:done||null,pilot,ready:false,finished:false,md:!!Input.mouse.down,fury14:true};
 Audio.startMusic('cinematics');setState(GS.CAMPAIGNINTRO);d1110Viewport();return true;
};
drawCampaignIntro=function(dt){
 const C=campaignIntro;if(!C?.fury14)return FURY14.base.introDraw.apply(this,arguments);
 d1110Viewport();ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#000';ctx.fillRect(0,0,912,512);
 if(!fury14Ready(FURY14.openKeys)){msgFaceUse('dialogue');msgText('FURY DIVISION',456,256,22,'#ffd681',1,1);msgFaceUse(null);ctx.restore();return;}
 C.ready=true;C.t+=Math.max(0,dt||0);const t=C.t;
 if(t>.4&&Input.menuStart()){ctx.restore();campaignIntroFinish();return;}
 const phases=[{at:0,key:'cin_war_earth_peace'},{at:43,key:'cin_war_civilian_collapse'},
 {at:57,key:'cin_war_city_air_attack'},{at:70,key:'cin_war_suburban_tanks'},{at:82,key:'cin_war_naval_exchange'}];
 const phase=phases.findLastIndex(q=>t>=q.at),shot=phases[phase],previous=phases[Math.max(0,phase-1)];
 fury14Earth(previous.key,t);fury14PixelReveal(()=>fury14Earth(shot.key,t),clamp((t-shot.at)/2.6,0,1));
 ctx.fillStyle='rgba(0,3,12,.70)';ctx.fillRect(0,0,912,512);
 let visible=[];
 if(t<6){const im=XART.get('fury14_logo'),w=638,h=w*im.height/im.width;ctx.globalAlpha=clamp(t/.9,0,1)*clamp((6-t)/1,0,1);ctx.drawImage(im,Math.round((912-w)/2),Math.round((512-h)/2),w,h);ctx.globalAlpha=1;}
 else{
  const q=Math.min(FURY14.scrollStop,t-6),fade=t>6+FURY14.scrollStop+8?1-(t-6-FURY14.scrollStop-8)/3:1;
  for(let i=0;i<FURY14_TEXT.length;i++){
   const y=540+i*36-q*17;if(y<92||y>540||!FURY14_TEXT[i])continue;
   const k=.56+.44*clamp((y-90)/422,0,1),line=fury14Line(FURY14_TEXT[i]);
   ctx.globalAlpha=clamp((y-92)/40,0,1)*clamp(fade,0,1);ctx.drawImage(line,Math.round(456-line.width*k/2),Math.round(y),Math.round(line.width*k),Math.round(36*k));visible.push(i);
  }ctx.globalAlpha=1;
 }
 if(t>FURY14.total-3){ctx.fillStyle='rgba(0,0,0,'+clamp((t-FURY14.total+3)/3,0,1)+')';ctx.fillRect(0,0,912,512);}
 if(t<FURY14.total-4){msgFaceUse('dialogue');controlHintRow([['pad_start','SKIP INTRO']],720,490,880,11);msgFaceUse(null);}
 FURY14.last={kind:'crawl',pilot:C.pilot,t,total:FURY14.total,background:shot.key,lines:visible,closing:t>=6+FURY14.scrollStop};ctx.restore();
 if(t>=FURY14.total)campaignIntroFinish();
};
function fury14Rows(p=run.pilot){
 return [
 ['F1-01',6.5,'flight',"I've just lost comms with the team."],
 ['F1-02',5.7,'pilot',"Dammit, where did everyone go?!"],
 ['F1-03',4.2,'boom',''],
 ['F1-04',7.6,'orders','Flight systems, head for that jungle over there, stat!'],
 ['F1-05',6.8,'resolve','I wonder if any of the others are over there...'],
 ['F1-06',1.5,'fade','']
 ].map(([id,duration,shot,text])=>({id,duration,shot,text,who:p.toUpperCase(),people:[p],fury14:true,d1110:true,readings:[],art:'comic',_cueSet:new Set()}));
}
d1110Keys=function(rows,p=run.pilot){const keys=FURY14.base.keys.apply(this,arguments);if(rows.some(b=>b.fury14))keys.push(...fury14Warm(p));return [...new Set(keys)];};
function fury14Panel(x,t,pk,right,talking=false){
 c16Clip([x,0,912,350],()=>{
  ctx.save();ctx.translate(x,0);campaignIntroJungle(912,350,t*.72);ctx.fillStyle='rgba(1,11,13,.13)';ctx.fillRect(0,0,912,350);
  if(!right)pt11OpeningShip(pk,t,456,172,185,.70);
  else{
   // The forward view remains visible on the right of the selected pilot.
   const a=C16_ART.banks['talk-'+pk],f=talking?Math.floor(t*9)%7:0,im=XART.get(a.key);
   if(im)ctx.drawImage(im,f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,98,28,236,278);
   const cockpit=XART.get('cin_cockpit_front_fighter');if(cockpit)ctx.drawImage(cockpit,0,0,432,350);
   const u=t-13.35;if(u>=0&&u<.62)cinFx('airburst',677,150,105,u);
  }
  ctx.restore();
 });
 ctx.strokeStyle='#f1dfae';ctx.lineWidth=6;ctx.strokeRect(x+4,4,904,342);
}
d1110Visual=function(b,s){
 if(!b.fury14)return FURY14.base.visual.apply(this,arguments);
 const index=s.i,pk=run.pilot,time=s.beats.slice(0,index).reduce((v,q)=>v+q.duration,0)+s.t;
 const pan=index<2?0:index===2?912*clamp(s.t/2.4,0,1)**2*(3-2*clamp(s.t/2.4,0,1)):912;
 ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#05080c';ctx.fillRect(0,0,912,512);
 c16Clip([0,0,912,350],()=>{ctx.save();ctx.translate(-Math.round(pan),0);fury14Panel(0,time,pk,false);fury14Panel(912,time,pk,true,s.shown<b.text.length);ctx.restore();});
 if(index===2&&s.t>=1.15){const im=XART.get('fury14_boom'),w=365,h=w*im.height/im.width;ctx.globalAlpha=clamp((s.t-1.15)/.12,0,1)*clamp((4.2-s.t)/.45,0,1);if(im)ctx.drawImage(im,Math.round(912-pan+480),42,w,h);ctx.globalAlpha=1;}
 if(index===2&&s.t>=1.15&&s.t<1.48){const a=.65*(1-(s.t-1.15)/.33);ctx.fillStyle='rgba(255,241,193,'+a+')';ctx.fillRect(440,8,464,334);}
 const caption={...b,who:pk.toUpperCase()};cb1110Caption(caption,s);
 if(index===0&&s.t<.7||b.shot==='fade'){ctx.fillStyle='rgba(0,0,0,'+(b.shot==='fade'?clamp(s.t/b.duration,0,1):1-clamp(s.t/.7,0,1))+')';ctx.fillRect(0,0,912,512);}
 FURY14.last={kind:'stage1-comic',pilot:pk,shot:b.shot,i:index,t:s.t,pan,visiblePanel:pan<456?'left':'right',text:b.text,shown:s.shown};ctx.restore();
};
d1110Step=function(s,dt,next,finish){
 const b=s.beats[s.i];if(!b?.fury14)return FURY14.base.step.apply(this,arguments);
 if(D1110.paused)return;s.age+=dt;s.d1110Wait=(s.d1110Wait||0)+dt;
 if(s.age>.3&&Input.menuStart()){finish();return;}
 if(!fury14Ready(s.d1110Keys||[]))return;
 const click=Input.mouse.down&&!s.md;s.md=!!Input.mouse.down;
 if(s.age>.3&&(Input.menuConfirm()||click)&&b.text){if(s.shown<b.text.length)s.shown=b.text.length;else if(s.t>1)next();return;}
 const before=s.shown,previous=s.t;s.t+=Math.max(0,dt);s.shown=Math.max(s.shown,Math.min(b.text.length,Math.floor(Math.max(0,s.t-.6)*28)));dialogueLetterTicks(b.text,before,s.shown);
 if(b.shot==='boom')d1110Cue(s,b,'expBig',1.15,previous);
 if(s.t>=b.duration)next();
};
sselDeploy=function(stage,after){
 if(stage!==1||run.mode!=='campaign'||debugFight||FURY14.pending)return FURY14.base.deploy.apply(this,arguments);
 FURY14.pending=true;fury14Warm();
 return FURY14.base.deploy.call(this,stage,()=>{FURY14.pending=false;
  if(!d1110Play('stage1-lost-comms',fury14Rows(),()=>{FURY14.card=true;after?.();}))after?.();
 });
};
// Map boot: assets decode before clocks run; hold the HQ-to-jungle flight for twelve seconds.
cmap2Reset=function(opts){const out=FURY14.base.mapReset.apply(this,arguments);FURY14.map=opts?.boot?{t:0,ready:false,done:false}:null;
 if(FURY14.map){const hq=cmap2World('hq'),dest=sselFlagXY(1);cmap2.cam={x:(hq.x+dest.x)/2,y:(hq.y+dest.y)/2,z:.48};CF9.detail=0;}
 return out;
};
function fury14MapReady(){const keys=['map4e_landscape',...MAP4E.keys.map(k=>'map4e_region_'+k),'ship_'+run.pilot,'cm2_ocean'];return fury14Ready(keys);}
drawStageSelect=function(dt){
 const M=FURY14.map;if(!M||M.done)return FURY14.base.mapDraw.apply(this,arguments);
 M.ready=fury14MapReady();if(M.ready)M.t+=Math.max(0,dt);const lock=window.sselCommitted;window.sselCommitted=true;
 let out;try{out=FURY14.base.mapDraw.call(this,M.ready?dt:0);}finally{window.sselCommitted=lock;}
 if(!M.ready){ctx.save();ctx.fillStyle='#050c16';ctx.fillRect(-campaignViewOffset(),0,campaignViewWidth(),512);msgText('ACQUIRING EARTH FEED',240,240,17,'#efd390',1,1);ctx.restore();}
 if(M.t>=12){M.done=true;window.sselCommitted=false;}
 return out;
};
cmap2CameraTick=function(dt,cine,selected){
 const M=FURY14.map;if(!M||M.done||!cf9Standard())return FURY14.base.mapCam.apply(this,arguments);
 const h=cmap2World('hq'),d=sselFlagXY(1),u=clamp((M.t-1.7)/8,0,1),e=u*u*(3-2*u),z=.48+(CF9.zoom()-.48)*(1-Math.cos(clamp((M.t-2)/10,0,1)*Math.PI))*.5;
 sselShip??={x:h.x,y:h.y+40,tx:d.x,ty:d.y,t:0,phase:'flyin',bank:0,trail:0,cur:1,head:0,face:1,cf9:true};
 Object.assign(sselShip,{x:lerp(h.x,d.x,e),y:lerp(h.y+40,d.y,e),t:M.t,moving:u>0&&u<1,phase:u>=1?'idle':'flyin',head:0,bank:0});CF9.detail=clamp(M.t/10,0,1);
 const lead=clamp(M.t/12,0,1);cmap2.cam={x:lerp((h.x+d.x)/2,d.x,lead),y:lerp((h.y+d.y)/2,d.y-12/z,lead),z};
};
sselShipUpdate=function(dt){if(FURY14.map&&!FURY14.map.done)return;return FURY14.base.ship.apply(this,arguments);};
cmap2DrawWorld=function(dt,selected){const out=FURY14.base.mapWorld.apply(this,arguments),M=FURY14.map;
 if(M&&!M.done&&M.ready){const d=cmap2World(1),age=M.t;for(let i=0;i<3;i++){const q=(age-i*.8)%2.6;if(q>=0&&q<.62)cinFx('airburst',d.x+[-70,90,40][i],d.y+[-85,-40,40][i],80,q);}
}
 return out;
};
FURY14.preview=function(part='opening',p=run.pilot){BOFCinematicDirector.cancel();run.pilot=p;pilotIndex=PILOTS.findIndex(q=>q.key===p);run.mode='campaign';coopOn=false;Input.clearTaps();
 if(part==='opening')return campaignIntroStart(()=>openStageSelect(1,{boot:true}));
 return d1110Play('stage1-lost-comms',fury14Rows(p),()=>{FURY14.card=true;beginStage(1);});};
window.BOF_FURY_OPENING_1114=FURY14;

// This arrival fades its entire card in/out; native proceedIntro owns the stage launch.
drawIntro=function(dt){
 if(!FURY14.card||run.stage!==1)return FURY14.base.cardDraw.apply(this,arguments);
 const ready=XART.rdy('scard_1');if(!ready){stateT=0;return;}
 const im=XART.get('scard_1'),W=cv.width/SS,H=VH,t=stateT,ratio=im.width/im.height,h=Math.min(H-62,(W-52)/ratio),w=h*ratio;
 ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
 ctx.globalAlpha=clamp(t/.85,0,1)*clamp((3.8-t)/.8,0,1);ctx.imageSmoothingEnabled=false;ctx.drawImage(im,Math.round((W-w)/2),Math.round((H-h)/2),Math.round(w),Math.round(h));ctx.restore();
 FURY14.last={kind:'stage1-card',t,alpha:clamp(t/.85,0,1)*clamp((3.8-t)/.8,0,1),rect:[(W-w)/2,(H-h)/2,w,h]};
 if(t>=3.8){FURY14.card=false;proceedIntro();}
};
