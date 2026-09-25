/* Campaign aftermaths. These authored plates and the shared dialogue window keep
   the origin reveal after Stage 1; no pilot radio exchanges play in Stage 1. */
(function(){
  'use strict';
  let cut=null;
  function pilot(){return (run&&run.pilot)||_pilotKey()||'axel';}
  function support(){return pilot()==='decker'?'cole':'decker';}
  function b(bg,who,text,extra){
    const shot=bg==='cinintro_team'?'reaction':bg==='cinintro_command'?'command':bg==='cinintro_lab'?'lab':null;
    const plate=shot?(shot==='lab'?'cin_story_lab_empty':'cin_story_hq_empty'):bg;
    return Object.assign({bg:plate,who:who,text:text,shot:shot,duration:Math.max(4.1,text.length/34+1.15)},extra||{});
  }
  function script(stage){
    const pk=pilot(), tech=support(), p=(PILOTS.find(q=>q.key===pk)||{}).name||pk.toUpperCase();
    if(stage===1)return [
      b('cinintro_team',p,'We made it home. I could see your ships, but every channel was dead. What happened out there?',{pilot:pk}),
      b('cinintro_command',tech.toUpperCase(),'The flight grid was hacked. The command arrived through our own satellites.'),
      b('cin_origin_blackhole_0924','FURY RECORDING','The last orbital frame shows a black hole opening beside the relay array.',{pan:.25,origin:true,duration:4.2}),
      b('cin_origin_emerges_0924',tech.toUpperCase(),'Something came through it. Look at that shape moving toward our satellite.',{pan:.47,origin:true,duration:4.3}),
      b('cin_origin_contact_0924','FURY RECORDING','First contact. Its tendrils reached the relay dish before the warning system could react.',{pan:.64,origin:true,duration:4.4}),
      b('cin_origin_arrival',tech.toUpperCase(),'The whole relay is being swallowed. The signal is no longer ours.',{pan:.66,origin:true,duration:4.2}),
      b('cin_origin_satellite',tech.toUpperCase(),'It filled the uplink with code I cannot read and sent the infection down to Earth.',{pan:.58,origin:true,duration:4.3}),
      b('cin_origin_land','FURY RECORDING','That signal reached aircraft, armor, ships, homes, and every connected system on Earth.'),
      b('cinintro_command',tech.toUpperCase(),'Fury survived because we rebuilt old eighties and nineties fighters for manual flight. No remote steering, no helpful sensors to turn against us.'),
      b('cinbg_jungle','SHIP SYSTEM','High-threat movement detected at a volcano beyond the jungle coast. That is our next lead.')
    ];
    if(stage===2)return [
      b('cinbg_hq_aerial',tech.toUpperCase(),'Perfect timing. Fire control is responding again. I have the radar back online.'),
      b('cinbg_hq_aerial',p,'I hear you clearly. Fury flight, sound off.',{pilot:pk,ship:true}),
      b('cinbg_hq_aerial','FURY FLIGHT','All pilots responding. Formation restored. Keep those red contacts in sight.',{ship:true})
    ];
    if(stage===3){
      const rows=[
        b('cinintro_command','COLE','Everyone around the map. The threat has spread from the jungle to the volcanic belt. We need a way through.',{shot:'table'}),
        b('cinintro_command',tech.toUpperCase(),'The signal keeps changing. I am staying on repairs and comms while the squad moves. Stage Six will need every pilot airborne.'),
        b('cinintro_lab','COLE','Decker, show me those prototypes you have been hiding. Just us.',{pilot:'cole'}),
        b('cinintro_lab','DECKER','Level Six laser array. Then the Level Seven emitter that becomes your Photon Cannon. I have not cleared either for field use.'),
        b('cinintro_lab','COLE','Put them on my ship. Quietly. Nobody else needs to know yet.',{pilot:'cole'}),
        b('cinintro_lab','COLE','You built the Photon Cannon? Decker, this is incredible!',{pilot:'cole',fx:'coleHug'}),
        b('cinintro_lab','DECKER','You are hugging me over a weapon schematic? If I showed you the rest of my designs, I would need a restraining order.',{fx:'coleHug'}),
        b('cinintro_lab','COLE','I am taking that as a yes.',{pilot:'cole'})
      ];
      if(pk==='cole')rows[4].text='Install them on my ship, Decker. Quietly. I want the Photon Cannon ready.';
      if(pk==='decker')rows[2].text='Decker, show me the prototypes. I want to learn how you built that Photon Cannon.';
      return rows;
    }
    if(stage===4){
      const rows=[
        b('cinintro_command',tech.toUpperCase(),'Bring that lightning system home. It can restore enough power to read the last satellite feed.'),
        b('cinintro_lab',tech.toUpperCase(),'The code is not human. I cannot parse one line of it. This is alien intelligence.',{fx:'typing'}),
        b('cinintro_lab',tech.toUpperCase(),'Wait. The final frame... what is looking back at us?',{fx:'shock',duration:4.2}),
        b('cin_war_symbiote_reveal','FURY RECORDING','LAST ORBITAL FRAME: SIGNAL SOURCE IDENTIFIED.',{fx:'warcry',duration:6}),
        b('cinintro_team','FURY FLIGHT','That thing was inside our own satellite? We were fighting its signal all this time.',{duration:5.3}),
        b('cinintro_team',p,'Cut it off! Nobody say a word. Just... tell me what we do now.',{pilot:pk}),
        b('cinintro_command',tech.toUpperCase(),'The Federation left us a prototype hull that can carry our fighters through gravity and into space. Our relay is gone. We go up for answers.')
      ];
      if(pk==='yuri')rows.splice(1,0,b('cinintro_lab','DECKER','Yuri, I upgraded your chain lightning to Level II. Take the new arc spread into the next fight.',{upgrade:true}));
      return rows;
    }
    if(stage===5)return [
      b('bg_stage05_loop_0923','FURY FLIGHT','The hammer is gone. I can see the blast from the edge of the debris field.',{fx:'hammerBurst',duration:5.2}),
      b('bg_stage05_loop_0923','NARRATOR','And on that day, '+p+' defeated the only known answer to the threat. For a moment, peace seemed possible.',{fx:'monochrome',duration:5.8}),
      b('cinend_deep_space','FURY FLIGHT','We did it! Fury flight, come back to Earth. We meet at the base.',{ship:true}),
      b('cinend_deep_space',p,'Copy. Set a course for home.',{ship:true,pilot:pk}),
      b('cinend_deep_space','SHIP SYSTEM','Federation hull disengaging. Manual controls restored.',{fx:'hull',ship:true,duration:5.2}),
      b('cinbg_hq_aerial','SHIP SYSTEM','Atmospheric entry confirmed. Fury is returning to Earth.',{ship:true})
    ];
    if(stage===6)return [
      b('cin_story_city_descent','SHIP SYSTEM','Descending toward the city. Surface radar has found a high-threat signature below the riverbank.',{ship:true,flight:'descent',duration:5.1}),
      b('cin_story_river_high','SHIP SYSTEM','Low-altitude flight confirmed. Follow the river channel toward the iron bridge.',{ship:true,flight:'riverHigh',duration:4.8}),
      b('cin_story_river_bridge',tech.toUpperCase(),'I have the bridge on radar. Stay low. The threat signal is ahead on the far bank.',{ship:true,flight:'bridgePass',duration:5.0}),
      b('cin_story_riverbank_sewer',tech.toUpperCase(),'We never searched underground. The old riverbank tunnel is where that signal disappears.',{ship:true,flight:'approach',duration:5.1}),
      b('cin_story_riverbank_sewer',p,'That entrance is large enough to fly through. I am taking us inside.',{ship:true,pilot:pk,flight:'enter',duration:4.6}),
      b('cin_story_sewer_gate','SHIP SYSTEM','Entering underground. Exterior signal lost.',{ship:true,flight:'gate',duration:5.2}),
      b('cin_stage07_approach','SHIP SYSTEM','Underground threat confirmed. Radar contact is moving deeper into the sewer.',{ship:true,flight:'underground',duration:4.8}),
      b('cin_stage07_topdown',p,'I see the access tunnel. Going down to find out what is hiding there.',{ship:true,pilot:pk})
    ];
    return null;
  }
  function start(stage,onDone){
    if(!run||run.mode!=='campaign')return false;
    const beats=script(stage);if(!beats||!beats.length)return false;
    cut={stage:stage,beats:beats,i:0,t:0,shown:0,md:!!Input.mouse.down,played:false};
    hqMode='campaignStory';hqSc={beats:beats};hqDone=onDone||null;
    for(const beat of beats)XART.rdy(beat.bg);
    if(beats.some(beat=>beat.ship)){
      XART.rdy(cinShipKey(pilot(),1));
      for(let f=0;f<4;f++)XART.rdy('nthp_'+pilot()+'_'+f);
    }
    for(const beat of beats)if(beat.shot||beat.fx==='warcry'){
      for(const pk of ['axel','freezer','lizzie','falva','yuri','maverick','cole','decker','juggernaut'])
        for(const pose of [1,2,3,4,5,6])XART.rdy('cinpose_'+pk+'_'+pose);
      break;
    }
    if(beats.some(beat=>beat.fx==='warcry')){
      XART.rdy('cin_war_symbiote_twoeyes');
    }
    if(beats.some(beat=>beat.fx==='hammerBurst'||beat.fx==='monochrome'))XART.rdy('arch_death');
    if(beats.some(beat=>beat.fx==='coleHug'))XART.rdy('cin_cole_decker_hug_0924');
    if(beats.some(beat=>beat.fx==='typing'||beat.fx==='shock')){
      XART.rdy(support()==='cole'?'cin_cole_typing_0924':'cin_decker_typing_0924');
      XART.rdy(support()==='cole'?'cin_cole_shocked_0924':'cin_decker_shocked_0924');
    }
    XART.rdy('dlg_window');if(typeof bmfReady==='function')bmfReady('dialogue');
    try{if(Audio&&Audio.startMusic)Audio.startMusic('cinematics');}catch(_e){}
    setState(GS.CUTSCENE);return true;
  }
  function next(){
    cut.i++;cut.t=0;cut.shown=0;cut.played=false;
    if(cut.i>=cut.beats.length){cut=null;hqEnd();}
  }
  function drawPose(pk,pose,cx,bottom,height){
    const key='cinpose_'+pk+'_'+pose;
    if(!XART.rdy(key))return;
    const im=XART.get(key),w=height*(im.naturalWidth||im.width)/(im.naturalHeight||im.height);
    ctx.drawImage(im,cx-w*.5,bottom-height,w,height);
  }
  function drawStoryCast(beat,W,H){
    const selected=pilot(),tech=support(),shot=beat.fx==='warcry'?'reveal':beat.shot;
    if(!shot)return;
    ctx.save();ctx.imageSmoothingEnabled=false;
    if(beat.fx==='coleHug'&&XART.rdy('cin_cole_decker_hug_0924')){
      const im=XART.get('cin_cole_decker_hug_0924'),dh=H*.62,dw=dh*(im.naturalWidth||im.width)/(im.naturalHeight||im.height);
      ctx.drawImage(im,W*.5-dw*.5,H*.70-dh,dw,dh);
      ctx.restore();return;
    }
    if(beat.fx==='typing'||beat.fx==='shock'){
      const shocked=beat.fx==='shock'&&cut.t>.43;
      const key=tech==='cole'?(shocked?'cin_cole_shocked_0924':'cin_cole_typing_0924'):
        (shocked?'cin_decker_shocked_0924':'cin_decker_typing_0924');
      if(XART.rdy(key)){
        const im=XART.get(key),dh=H*.57,dw=dh*(im.naturalWidth||im.width)/(im.naturalHeight||im.height);
        ctx.drawImage(im,W*.5-dw*.5,H*.70-dh,dw,dh);
        ctx.restore();return;
      }
    }
    if(shot==='table'||shot==='reveal'){
      const cast=['axel','freezer','lizzie','falva','yuri','maverick','cole','decker','juggernaut'].filter(pk=>pk!==selected);
      cast.splice(4,0,selected);
      cast.forEach((pk,i)=>drawPose(pk,i<4?6:i>4?5:4,W*(.075+i*.106),H*.695,H*(pk===selected ? .25 : .22)));
    }else if(shot==='lab'){
      const speaker=beat.who.toLowerCase();
      drawPose('cole',speaker==='cole'?3:6,W*.20,H*.695,H*.41);
      drawPose('decker',speaker==='decker'?2:5,W*.80,H*.695,H*.41);
    }else if(shot==='command'){
      const speaker=beat.who.toLowerCase();
      drawPose(tech,speaker===tech?3:6,W*.24,H*.695,H*.40);
      drawPose(selected,speaker===selected?2:5,W*.76,H*.695,H*.40);
    }else if(shot==='reaction'){
      const side=['lizzie','juggernaut','axel','yuri'].filter(pk=>pk!==selected&&pk!==tech);
      drawPose(side[0],3,W*.12,H*.695,H*.34);
      drawPose(selected,2,W*.38,H*.695,H*.43);
      drawPose(tech,3,W*.64,H*.695,H*.41);
      drawPose(side[1],2,W*.88,H*.695,H*.34);
    }
    ctx.restore();
  }
  function beatArtReady(beat){
    const selected=pilot(),tech=support(),shot=beat.fx==='warcry'?'reveal':beat.shot;
    const keys=[beat.bg];
    if(beat.ship)keys.push(cinShipKey(selected,1));
    if(beat.fx==='hammerBurst'||beat.fx==='monochrome')keys.push('arch_death');
    if(beat.fx==='hull')keys.push('cin_hull_release');
    if(beat.fx==='warcry')keys.push('cin_war_symbiote_twoeyes');
    if(beat.fx==='coleHug')keys.push('cin_cole_decker_hug_0924');
    if(beat.fx==='typing'||beat.fx==='shock'){
      keys.push(tech==='cole'?'cin_cole_typing_0924':'cin_decker_typing_0924');
      if(beat.fx==='shock')keys.push(tech==='cole'?'cin_cole_shocked_0924':'cin_decker_shocked_0924');
    }
    if(shot==='table'||shot==='reveal'){
      const cast=['axel','freezer','lizzie','falva','yuri','maverick','cole','decker','juggernaut'].filter(pk=>pk!==selected);
      cast.splice(4,0,selected);
      cast.forEach((pk,i)=>keys.push('cinpose_'+pk+'_'+(i<4?6:i>4?5:4)));
    }else if(shot==='lab'){
      const speaker=beat.who.toLowerCase();
      keys.push('cinpose_cole_'+(speaker==='cole'?3:6),'cinpose_decker_'+(speaker==='decker'?2:5));
    }else if(shot==='command'){
      const speaker=beat.who.toLowerCase();
      keys.push('cinpose_'+tech+'_'+(speaker===tech?3:6),'cinpose_'+selected+'_'+(speaker===selected?2:5));
    }else if(shot==='reaction'){
      const side=['lizzie','juggernaut','axel','yuri'].filter(pk=>pk!==selected&&pk!==tech);
      keys.push('cinpose_'+side[0]+'_3','cinpose_'+selected+'_2','cinpose_'+tech+'_3','cinpose_'+side[1]+'_2');
    }
    let ready=true;
    for(const key of keys)if(!XART.rdy(key))ready=false;
    return ready;
  }
  const APPROACH_FLIGHTS=new Set(['descent','riverHigh','bridgePass','approach','enter']);
  function flightApproachProgress(){
    let elapsed=cut.t,total=0;
    cut.beats.forEach((b,i)=>{
      if(!APPROACH_FLIGHTS.has(b.flight))return;
      total+=b.duration;
      if(i<cut.i)elapsed+=b.duration;
    });
    return Math.min(1,elapsed/Math.max(.01,total));
  }
  function drawFlightPlate(beat,u,W,H){
    const entering=beat.flight==='enter';
    const zoom=(entering?1.25:1.02)+Math.min(1,u)*(entering?.34:.23);
    ctx.save();ctx.translate(W*.5,H*.5);ctx.scale(zoom,zoom);ctx.translate(-W*.5,-H*.5);
    cinCover(beat.bg,W,H,.5);ctx.restore();
  }
  function draw(dt){
    if(!cut){hqEnd();return;}
    const W=cutsceneViewWidth(),H=VH,beat=cut.beats[cut.i];
    // A scene starts only when its visible layers are decoded. This matters on
    // first play, when later orbital and cast plates are still loading.
    if(!beatArtReady(beat))return;
    cut.t+=dt;
    ctx.save();ctx.fillStyle='#02060b';ctx.fillRect(0,0,W,H);
    ctx.filter=beat.fx==='monochrome'?'grayscale(1)':'none';
    if(beat.flight==='gate'&&XART.rdy(beat.bg)){
      const im=XART.get(beat.bg),dw=Math.min(W,H*(im.naturalWidth||im.width)/(im.naturalHeight||im.height));
      ctx.drawImage(im,W*.5-dw*.5,0,dw,H);
    }else if(APPROACH_FLIGHTS.has(beat.flight)&&cut.i>0&&APPROACH_FLIGHTS.has(cut.beats[cut.i-1].flight)&&cut.t<.62){
      const previous=cut.beats[cut.i-1];
      drawFlightPlate(previous,1,W,H);
      ctx.save();ctx.globalAlpha=Math.min(1,cut.t/.62);
      drawFlightPlate(beat,cut.t/beat.duration,W,H);ctx.restore();
    }else if(beat.flight){
      drawFlightPlate(beat,cut.t/beat.duration,W,H);
    }else if(beat.origin&&cut.i>0&&cut.beats[cut.i-1].origin&&cut.t<.68){
      const prev=cut.beats[cut.i-1];
      cinCover(prev.bg,W,H,prev.pan==null?.5:prev.pan,prev.duration/7);
      ctx.save();ctx.globalAlpha=Math.min(1,cut.t/.68);
      cinCover(beat.bg,W,H,beat.pan==null?.5:beat.pan,cut.t/7);ctx.restore();
    }else cinCover(beat.bg,W,H,beat.pan==null?.5:beat.pan,cut.t/7);
    ctx.filter='none';
    if(beat.fx==='warcry'){
      if(XART.rdy('cin_war_symbiote_twoeyes')){
        const im=XART.get('cin_war_symbiote_twoeyes');
        const sx=im.width*.12,sy=im.height*.05,sw=im.width*.76,sh=im.height*.53;
        const dh=H*.42,dw=dh*sw/sh;
        ctx.save();ctx.beginPath();ctx.rect(W*.15,H*.02,W*.70,H*.43);ctx.clip();
        ctx.globalAlpha=.82+.15*Math.sin(cut.t*14);
        ctx.drawImage(im,sx,sy,sw,sh,W*.5-dw*.5,H*.015,dw,dh);
        ctx.restore();
      }
    }
    drawStoryCast(beat,W,H);
    if(beat.fx==='shock'&&cut.t>.43&&cut.t<1.15){
      const alpha=.70*(1-(cut.t-.43)/.72);
      ctx.fillStyle='rgba(210,240,255,'+Math.max(0,alpha)+')';
      ctx.fillRect(W*.16,H*.09,W*.68,H*.47);
    }
    if(beat.fx==='hull'&&XART.rdy('cin_hull_release')){
      const im=XART.get('cin_hull_release'),half=im.width/2;
      const dh=H*.43,dw=H*.34,shift=H*.15*Math.min(1,cut.t/3.5);
      ctx.save();ctx.globalAlpha=Math.min(1,Math.max(0,(5.2-cut.t)/1.3));
      ctx.drawImage(im,0,0,half,im.height,W*.5-dw-shift,H*.43-dh*.5,dw,dh);
      ctx.drawImage(im,half,0,half,im.height,W*.5+shift,H*.43-dh*.5,dw,dh);
      ctx.restore();
    }
    if(beat.ship){
      const u=Math.min(1,cut.t/beat.duration);
      const gate=beat.flight==='gate';
      const approach=APPROACH_FLIGHTS.has(beat.flight),progress=approach?flightApproachProgress():0;
      const py=gate?H*(.50-.29*u):approach?H*(.59-.13*progress):beat.flight?H*(.53-.23*u):H*(.43-.04*Math.min(1,cut.t/4));
      const sh=gate?H*(.18-.11*u):approach?H*(.24-.09*progress):beat.flight?H*(.23-.12*u):H*.17;
      cinDrawShip(pilot(),1,W*.5,py,sh,false,gate?1-Math.max(0,(u-.70)/.22):1,0);
    }
    if(beat.flight==='gate'){
      const a=Math.min(1,Math.max(0,(cut.t/beat.duration-.77)/.23));
      ctx.fillStyle='rgba(0,0,0,'+a+')';ctx.fillRect(0,0,W,H*.70);
    }
    if(beat.fx==='hammerBurst'||beat.fx==='monochrome'){
      const after=beat.fx==='monochrome',f=after?14:Math.min(15,Math.floor(cut.t*3.2));
      ctx.save();if(after)ctx.filter='grayscale(1)';
      archBlit('death',f,W*.5,H*.28,H*.23,null,0,after?Math.max(0,.82-cut.t/beat.duration*.82):1);
      ctx.restore();
      if(!after&&f>=8&&!cut.played){
        cut.played=true;
        try{(Audio.SFX.explosionPlasma||Audio.SFX.explosionAirMedium||Audio.SFX.boom||function(){})();}catch(_e){}
      }
    }
    if(beat.fx==='warcry'&&!cut.played){
      cut.played=true;
      try{(Audio.SFX.symbioteWarcry||Audio.SFX.mechScream||Audio.SFX.enemyApproach||function(){})();}catch(_e){}
    }
    if(beat.upgrade&&run&&run.pilot==='yuri'){
      msgFaceUse('dialogue');msgText('CHAIN LIGHTNING LEVEL II',W/2,H*.12,Math.max(15,H*.039),'#8fdcff',1,1,.07);msgFaceUse(null);
    }
    // Several HQ room masters carry an old baked caption along their lower edge.
    // The dedicated dialogue rail masks that caption before the live text is set.
    ctx.fillStyle='#02060b';ctx.fillRect(0,H*.70,W,H*.30);
    const full=beat.text,was=cut.shown;
    cut.shown=Math.min(full.length,Math.floor(cut.t*38));
    dialogueLetterTicks(full,was,cut.shown);
    const tint=dialogueNameColor(beat.who,'#a9dcfa');
    dlgBox({who:beat.who,portrait:beat.pilot||false,full:full,shown:full.slice(0,cut.shown),fade:Math.min(1,cut.t*5),tint:tint,
      pw:Math.min(W*.82,940),ph:Math.min(H*.26,146),screenSpace:false});
    msgFaceUse('dialogue');controlHintRow([['pad_start','SKIP']],H-20,W/2,W-24);msgFaceUse(null);
    ctx.restore();
    const click=Input.mouse.down&&!cut.md;cut.md=!!Input.mouse.down;
    if(cut.t>=beat.duration||(cut.t>.35&&(click||(typeof anyTap==='function'&&anyTap())))){
      Input.mouse.down=false;next();
    }
  }
  let gateLaunch=null;
  function drawGateLaunch(dt,W,H){
    if(!gateLaunch)gateLaunch={t:0};
    ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);
    if(!XART.rdy('cin_story_sewer_gate')||!XART.rdy(cinShipKey(pilot(),1)))return true;
    gateLaunch.t+=Math.max(0,dt||0);
    const im=XART.get('cin_story_sewer_gate'),dw=Math.min(W,H*(im.naturalWidth||im.width)/(im.naturalHeight||im.height));
    ctx.drawImage(im,W*.5-dw*.5,0,dw,H);
    const u=Math.min(1,gateLaunch.t/4.4),alpha=1-Math.min(1,Math.max(0,(u-.72)/.22));
    cinDrawShip(pilot(),1,W*.5,H*(.82-.54*u),H*(.27-.20*u),false,alpha,0);
    const dark=Math.min(1,Math.max(0,(u-.78)/.22));
    if(dark>0){ctx.fillStyle='rgba(0,0,0,'+dark+')';ctx.fillRect(0,0,W,H);}
    if(gateLaunch.t>=4.4&&stageLoadReady(7)){gateLaunch=null;return false;}
    if(gateLaunch.t>=4.4)drawStageLoadOverlay();
    return true;
  }
  window.BOFCampaignStory={start:start,draw:draw,script:script,drawGateLaunch:drawGateLaunch,
    seek:function(i){if(cut&&i>=0&&i<cut.beats.length){cut.i=i;cut.t=0;cut.shown=0;cut.played=false;}},
    get active(){return !!cut;}};
})();
