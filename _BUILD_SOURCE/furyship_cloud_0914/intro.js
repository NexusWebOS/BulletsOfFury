/* Mike's revised Stage-5 approach: sustained fast sky -> broken cloud deck ->
   cloud clearing / assembly -> full white -> space. This replaces the earlier
   brake/cruise and exposed sky/space band for the new fighter. */
const FURY_INTRO_SPEED=420,FURY_INTRO_SKY_SECONDS=12;
function furyIntroWhite(G){
 if(!G)return 0;
 if(G.phase==='pixelglow')return _ease(clamp(G.t/GRAVITY_PIXEL_DUR,0,1));
 if(G.phase==='whiteout')return 1;
 if(G.phase==='reveal')return 1-_ease(clamp(G.t/GRAVITY_REVEAL_DUR,0,1));
 return 0;
}
function furyIntroClouds(S){
 if(S.space)return;
 const deck=_ease(clamp((S.t-2.4)/1.8,0,1)),clear=_ease(clamp((S.t-8.5)/3.5,0,1));
 const draw=(i,x,y,w,a)=>{
  const key='cm2_cloud_'+(i%7);if(!XART.rdy(key)||a<=0)return;
  const im=XART.get(key),h=w*(im.height/im.width);
  ctx.save();ctx.globalAlpha=a;ctx.drawImage(im,x-w/2,y-h/2,w,h);ctx.restore();
 };
 // Natural alpha holes between the moving authored banks reveal the aircraft.
 for(let row=0;row<6;row++)for(let col=0;col<3;col++){
  const x=(col+.5)*VW/3+Math.sin(row*2.3+col)*38;
  const y=((row*157+S.scroll*.9+col*61)%(VH+340))-170;
  draw(row*3+col,x,y,235,deck*(1-clear)*.97);
 }
 // The banks keep rushing past the clearing; no stationary cloud frame or
 // clipped geometric hole. Their irregular authored edges frame the assembly.
 for(let row=0;row<5;row++){
  const y=((row*190+S.scroll*.9)%(VH+380))-190;
  for(const side of [-1,1])draw(row+(side>0?2:0),side<0?-38:VW+38,y,300,deck*.98);
  if(Math.abs(y-VH*.59)>194)draw(row+4,VW/2+Math.sin(row)*45,y,290,deck*clear*.94);
 }
}
function furyIntroDialogue(G){
 if(!G||G.phase==='active'||G.dialogueT<=G.dialogueDelay)return;
 const full=G.line||'',shown=G.phase==='drift'?full.slice(0,Math.max(0,Math.floor((G.dialogueT-G.dialogueDelay)*GRAVITY_DIALOGUE_CPS))):full;
 dlgBox({who:'FURY HQ',tint:'#ffb347',full,shown,fade:clamp((G.dialogueT-G.dialogueDelay)/.28,0,1),portrait:false,pw:Math.min(VW-20,460),ph:Math.min(138,Math.round(VH*.26)),x:10,y:10,screenSpace:false});
}
function furyIntroDraw(dt){
 let S=drawLaunch._furyIntro;
 if(!S||stateT<(S.lastT||0)-.001||drawLaunch._phase===undefined){
  S=drawLaunch._furyIntro={t:0,scroll:0,phase:'sky',pt:0,lastT:stateT,build:!run.gravityShipReady,space:false,num:99,go:false};
  drawLaunch._phase='run';drawLaunch._pt=0;drawLaunch._dist=0;drawLaunch._bgScroll=0;drawLaunch._build=S.build;
  drawLaunch._mus=true;Audio.startMusic((curStage&&curStage.music)||'stage');
  furyShipWarm();for(let i=0;i<7;i++)XART._touch('cm2_cloud_'+i);XART._touch(STAGE6_TRANSITION_SKY);
  if(S.build)gravityModeStart();else{gravityModeRetain();S.space=true;S.phase='load';}
 }
 S.lastT=stateT;S.t+=dt;S.pt+=dt;S.scroll+=FURY_INTRO_SPEED*dt;furyFlightTime+=dt;
 drawLaunch._spd=FURY_INTRO_SPEED;drawLaunch._bgScroll=S.scroll;drawLaunch._dist=S.scroll;
 if(S.phase==='sky'){
  gravityModeTick(dt);
  if(S.t>=FURY_INTRO_SKY_SECONDS&&gravityMode.dialogueDone&&furyShipReady()&&Array.from({length:7},(_,i)=>XART.rdy('cm2_cloud_'+i)).every(Boolean)){
   gravityModeBeginCharge();S.phase='assembly';S.pt=0;
  }
 }else if(S.phase==='assembly'){
  const running=gravityModeTick(dt);
  // Swap the backdrop only under opaque white, before its fade reveals space.
  if(gravityMode.phase==='reveal'||gravityMode.phase==='active')S.space=true;
  if(!running){S.phase='load';S.pt=0;}
 }else if(S.phase==='load'){
  if(furyShipReady()&&(typeof stageLoadReady!=='function'||stageLoadReady(5))){S.phase='countdown';S.pt=0;}
 }
 drawLaunch._phase=S.phase==='assembly'?'gravity':S.phase==='countdown'?'cd':S.phase==='load'?'load':'run';
 drawLaunch._pt=S.pt;
 shake=Math.max(0,shake-dt*30);flashScreen=Math.max(0,flashScreen-dt*3);
 const G=gravityMode,pose=playShipPose(),k=S.phase==='countdown'?_ease(clamp(S.pt/3,0,1)):0;
 const x=lerp(VW/2,pose.x,k),y=lerp(S.build?VH*.59:pose.y,pose.y,k),size=lerp(S.build?118:SPACE_SHIP_SIZE,SPACE_SHIP_SIZE,k);
 S.ship={x,y,size};
 if(S.space){_stage5SpaceScroll=S.scroll;entryConnectorDraw(5,0);}
 else stage6TransitionBackgroundDraw(S.scroll);
 if(S.build&&S.phase==='sky'&&S.t<6){drawShipSprite(x,y,90,'');}
 else if(furyShipReady())furyShipDrawPhase(G,x,y,size,90,_pilotKey());
 else drawShipSprite(x,y,90,'');
 furyIntroClouds(S);
 furyIntroDialogue(G);
 if(S.phase==='assembly'&&G.phase!=='drift'){
  ctx.save();ctx.textAlign='center';ctx.font='bold 15px "BOFmil", monospace';ctx.fillStyle='#f5fbff';ctx.shadowColor='#153748';ctx.shadowBlur=5;
  ctx.fillText(spaceFighterName(_pilotKey()),x,VH*.90);ctx.restore();
 }
 if(typeof drawScanlines==='function')drawScanlines();
 // Last in the composite: even HQ and scanlines disappear in the full white.
 const white=furyIntroWhite(G);S.white=white;gravityWhite(white);
 if(S.phase==='load')drawStageLoadOverlay();
 if(S.phase==='countdown'){
  const art=typeof curArt==='function'&&curArt();
  if(S.pt<3){
   const n=3-Math.floor(S.pt);if(S.num!==n){S.num=n;if(Audio.SFX.getready)Audio.SFX.getready();}
   if(art){stageText(art,'GET READY',VW/2,VH*.34,20,null,null,1,.12);stageText(art,String(n),VW/2,VH*.48,52,null,null,1,.1);}
   else{ctx.save();ctx.textAlign='center';ctx.fillStyle='#fff';ctx.font='bold 20px "BOFmil", monospace';ctx.fillText('GET READY',VW/2,VH*.34);ctx.font='bold 52px "BOFmil", monospace';ctx.fillText(String(n),VW/2,VH*.48);ctx.restore();}
  }else{
   if(!S.go){S.go=true;if(Audio.SFX.go)Audio.SFX.go();}
   msgText('GO!',VW/2,VH*.46,64,'#fff',0,1,.08);
   if(S.pt>=3.85)finishLaunch();
  }
 }
 return true;
}
