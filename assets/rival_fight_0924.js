/* Optional Stage-6 Harrier-route consequence: five scattered rivals, two selected wingmen. */
// Mike's Stage X score. Keep the regular Stage 6 boss music independently mapped.
BOFA.music.stagex='assets/game/levels/stage_x/audio/music/LevelX.mp3';
if(Snd){const m=new window.Audio();m.preload='none';m.src=BOFA.music.stagex;m.loop=true;Snd.music.stagex=m;}
const Rival24=(()=>{
  const STAGES_AT=[6,6,6,6,6];
  const KEYS=['voss','nyx','rook','kaia','jace'];
  const SHIPS=['voss_iron_vulture','nyx_ghostknife','rook_breachhammer','kaia_signal_wraith','jace_razorjack'];
  const COLORS=['#bc77ff','#53e6e0','#c8dcf2','#ff7087','#eced6e'];
  let mapFocus=false, mapCursor=0, mapMouse=false, mapPrevCursor=7, scatterT=null, select=null, active=null, wing=[];
  function available(){return campaign&&campaign.rivalScattered&&run.mode==='campaign'&&aliveIndices().length>0;}
  function aliveIndices(){return KEYS.map((_,i)=>i).filter(i=>!(campaign.rivalDefeated||[])[i]);}
  /* 0928 - Mike: "if we dont face them, when we go back to the campaign map, they will fly out from
     stage 6 and go to the middle and spiral around it all 5 of them. We then can either go to Stage 7,
     or Stage X aka 10." They launch from the STAGE 6 flag (the old code launched from 7's), bank in
     along curved paths nose-first, then orbit the hub in a breathing spiral around the STAGE X plaque.
     The authored rr_ship plates face south, so a heading theta is drawn rotated by theta - PI/2. */
  let orbitT=0;
  function hub(){const p=typeof fr27CoreMapPosition==='function'?fr27CoreMapPosition():null;return p||(sselFlagScreenXY(6)||null);}
  function orbitAt(i,t){
    const h=hub();if(!h)return null;const idx=aliveIndices(),k=Math.max(0,idx.indexOf(i)),N=Math.max(1,idx.length);
    const a=t*.8+k*TAU/N,r=92+Math.sin(t*1.5+k*1.3)*10,ry=.55;
    return {x:h.x+Math.cos(a)*r,y:h.y+Math.sin(a)*r*ry,heading:Math.atan2(Math.cos(a)*r*ry,-Math.sin(a)*r)};
  }
  function pos(i){const p=orbitAt(i,orbitT);return p?{x:clamp(p.x,30,VW-30),y:clamp(p.y,40,VH-40)}:null;}
  function shipDraw(i,x,y,heading,size,alpha){
    const k='rr_ship_'+SHIPS[i];if(!XART.rdy(k))return;const im=XART.get(k),h=size,w=h*im.width/im.height;
    ctx.save();ctx.globalAlpha=alpha==null?1:alpha;ctx.translate(x,y);ctx.rotate(heading-Math.PI/2);ctx.imageSmoothingEnabled=false;
    ctx.drawImage(im,-w/2,-h/2,w,h);ctx.restore();
  }
  function mapDraw(dt){
    if(!available()||sselBoot>0)return;
    dt=dt||0;orbitT+=dt;
    if(scatterT!=null)scatterT=Math.min(3.2,scatterT+dt);
    const origin=sselFlagScreenXY(6),flying=scatterT!=null&&scatterT<3.2,h=hub();
    const idx=aliveIndices();
    const order=idx.map(i=>({i,p:orbitAt(i,orbitT)})).filter(o=>o.p).sort((a,b)=>a.p.y-b.p.y);
    const drawShips=front=>{for(const {i,p} of order){
      if((p.y>=(h?h.y:0))!==front)continue;
      let x=p.x,y=p.y,heading=p.heading;
      if(flying&&origin){
        /* launched one after another from the stage 6 flag, curving out to their slot in the orbit */
        const f=clamp((scatterT-i*.16)/2.2,0,1),e=f*f*(3-2*f);
        if(f<=0)continue;
        const c={x:(origin.x+p.x)/2+(i-2)*34,y:Math.min(origin.y,p.y)-60-i*6};
        const bx=(1-e)*(1-e)*origin.x+2*(1-e)*e*c.x+e*e*p.x,by=(1-e)*(1-e)*origin.y+2*(1-e)*e*c.y+e*e*p.y;
        const tx=2*(1-e)*(c.x-origin.x)+2*e*(p.x-c.x),ty=2*(1-e)*(c.y-origin.y)+2*e*(p.y-c.y);
        x=bx;y=by;if(f<1)heading=Math.atan2(ty,tx);
      }
      const chosen=mapFocus&&i===mapCursor;
      if(chosen){ctx.save();ctx.globalAlpha=.7+.3*Math.sin(orbitT*9);ctx.strokeStyle=COLORS[i];ctx.lineWidth=2;ctx.shadowColor=COLORS[i];ctx.shadowBlur=12;
        ctx.beginPath();ctx.arc(x,y,21,0,TAU);ctx.stroke();ctx.restore();}
      shipDraw(i,x,y,heading,chosen?40:34,mapFocus&&!chosen?.8:1);
    }};
    drawShips(false);   // the far side of the orbit passes behind the plaque
    /* the STAGE X plaque sits in the middle of the orbit - this is the node the pilot chooses */
    if(typeof map4eStageXMarker!=='function'&&h&&XART.rdy('fr27_stagex_card')){const im=XART.get('fr27_stagex_card'),w=mapFocus?118:98,hh=w*im.height/im.width,
      pulse=mapFocus?1:.86+.14*Math.sin(orbitT*3);ctx.save();ctx.globalAlpha=(flying?clamp(scatterT/2.2,0,1):1)*pulse;ctx.imageSmoothingEnabled=false;
      if(mapFocus){ctx.shadowColor='#ff5a4a';ctx.shadowBlur=14;}ctx.drawImage(im,h.x-w/2,h.y-hh/2,w,hh);ctx.restore();}
    else XART.rdy('fr27_stagex_card');
    drawShips(true);    // and the near side in front of it
    if(mapFocus&&idx.includes(mapCursor))stageXCard(mapCursor);
    if(flying)campText('REBEL FURY BREAKING FORMATION',VW/2,VH-212,10,'#ffb4a3');
    else if(!mapFocus)controlHintRow([['pad_dpad','STAGE X']],VH-212,VW/2,VW-24,20);
    else controlHintRow([['pad_dpad','RIVAL'],['pad_a','FIGHT'],['pad_b','MAP']],stageXCardTop()-86,VW/2,VW-24,20);
  }
  /* Stage X borrows Stage 6's cursor but owns its own centered, live rival briefing. */
  function stageXCardH(){return typeof MAPG!=='undefined'?MAPG.rect.h:98;}
  function stageXCardTop(){return VH-stageXCardH()-24;}
  function stageXCard(i){
    if(typeof mapgBriefingDraw==='function')mapgBriefingDraw({key:'x-'+i,
      title:'STAGE X - FRACTURED FURY',body:'RIVAL '+KEYS[i].toUpperCase()+'. FLY WITH TWO ALLIED PILOTS.'});
  }

  function mapInput(){
    if(!available())return false;
    if(scatterT!=null&&scatterT<3.2)return true;
    const m=Input.mouse||{},idx=aliveIndices();
    if(!idx.length)return false;
    let hit=-1;
    for(const i of idx){const p=pos(i);if(p&&Math.abs(m.x-p.x)<=18&&Math.abs(m.y-p.y)<=17){hit=i;break;}}
    if(hit>=0&&m.down&&!mapMouse&&stateT>.4){mapFocus=true;mapCursor=hit;startSelect(hit);mapMouse=true;return true;}
    mapMouse=!!m.down;
    if(!mapFocus){if(Input.menuDown()){mapFocus=true;mapPrevCursor=sselCursor;mapCursor=idx[0];sselCursor=STAGES_AT[mapCursor];Audio.SFX.blip();return true;}return false;}
    if(Input.menuUp()){mapFocus=false;sselCursor=mapPrevCursor;Audio.SFX.blip();return true;}
    const n=idx.indexOf(mapCursor);
    if(Input.menuLeft()){mapCursor=idx[(n+idx.length-1)%idx.length];sselCursor=STAGES_AT[mapCursor];Audio.SFX.blip();}
    if(Input.menuRight()){mapCursor=idx[(n+1)%idx.length];sselCursor=STAGES_AT[mapCursor];Audio.SFX.blip();}
    if(Input.menuConfirm()){startSelect(mapCursor);return true;}
    return true;
  }
  function mapBack(){if(!mapFocus||!Input.menuBack())return false;mapFocus=false;sselCursor=mapPrevCursor;Audio.SFX.blip();return true;}
  function startSelect(i){
    mapFocus=false;select={rival:i,chosen:[],cursor:0,mouse:false,t:0};
    for(const p of PILOTS)XART.rdy('pav_'+p.key);
    XART.rdy('r24_panel');XART.rdy('r24_card');
    Audio.SFX.select();setState(GS.RIVALALLY);
  }
  function pool(){return PILOTS.filter(p=>p.key!==run.pilot);}
  function selectDraw(dt){
    if(!select){openStageSelect(campaign.unlockedMax||7,{});return;}
    const S=select;S.t+=dt||0;
    ctx.fillStyle='#030912';ctx.fillRect(0,0,VW,VH);
    const y=84,h=320;
    if(XART.rdy('r24_panel'))ctx.drawImage(XART.get('r24_panel'),0,y,VW,h);
    campText('RIVAL FIGHT!',VW/2,y+24,20,'#ffb4a7');
    campText('CHOOSE TWO ALLY PILOTS',VW/2,y+43,12,'#bfefff');
    const P=pool(),cells=[];
    P.forEach((p,i)=>{
      const x=83+(i%3)*156,cy=y+84+Math.floor(i/3)*55,chosen=S.chosen.includes(p.key),focus=i===S.cursor;
      cells.push({x:x-49,y:cy-26,w:98,h:52});
      ctx.save();ctx.globalAlpha=chosen?.65:1;
      ctx.fillStyle=chosen?'rgba(35,104,89,.55)':focus?'rgba(53,110,140,.72)':'rgba(4,17,25,.88)';
      ctx.fillRect(x-49,cy-26,98,52);
      ctx.strokeStyle=chosen?'#6affbc':focus?'#ffe28d':'#39667b';ctx.lineWidth=focus?2:1;ctx.strokeRect(x-49,cy-26,98,52);
      const k='pav_'+p.key;if(XART.rdy(k))ctx.drawImage(XART.get(k),x-17,cy-24,34,34);
      ctx.restore();
      campText(p.name,x,cy+19,8,chosen?'#84ffc5':'#dceaf4');
    });
    S.cells=cells;
    const labels=[S.chosen[0]||'ALLY 1',S.chosen[1]||'ALLY 2','DEPLOY'];
    for(let i=0;i<3;i++)campText(labels[i].toUpperCase(),80+i*160,y+273,11,i===2&&S.chosen.length===2?'#fff1a3':'#9fd7ee');
    controlHintRow([['pad_dpad','PILOT'],['pad_a',S.chosen.length===2?'DEPLOY':'SELECT'],['pad_b','CANCEL']],VH-25);
    const m=Input.mouse||{};let hit=-1;
    for(let i=0;i<cells.length;i++){const r=cells[i];if(m.x>=r.x&&m.x<r.x+r.w&&m.y>=r.y&&m.y<r.y+r.h){hit=i;break;}}
    if(hit>=0&&m.down&&!S.mouse&&S.t>.15){S.cursor=hit;choose();}
    if(m.down&&!S.mouse&&S.chosen.length===2&&m.y>=y+238&&m.y<=y+299&&m.x>320)deploy();
    S.mouse=!!m.down;
    if(Input.menuLeft()){S.cursor=(S.cursor+P.length-1)%P.length;Audio.SFX.blip();}
    if(Input.menuRight()){S.cursor=(S.cursor+1)%P.length;Audio.SFX.blip();}
    if(Input.menuUp()){S.cursor=(S.cursor+P.length-3)%P.length;Audio.SFX.blip();}
    if(Input.menuDown()){S.cursor=(S.cursor+3)%P.length;Audio.SFX.blip();}
    if(Input.menuBack()){select=null;openStageSelect(campaign.unlockedMax||7,{});return;}
    if(Input.menuConfirm()){if(S.chosen.length===2)deploy();else choose();}
  }
  function choose(){const p=pool()[select.cursor];if(!p)return;
    const j=select.chosen.indexOf(p.key);
    if(j>=0)select.chosen.splice(j,1);else if(select.chosen.length<2)select.chosen.push(p.key);
    Audio.SFX.select();
  }
  function deploy(){if(!select||select.chosen.length!==2)return;
    const chosen=select.chosen.slice(),rival=select.rival,returnStage=clamp(campaign.unlockedMax||7,1,8);
    select=null;
    /* Use Stage 6's neutral encounter setup, then draw the chosen contact's
       biome. Entering the destination stage outright would replay its story
       dialogue and scripted hazards over this optional duel. */
    beginStage(6);
    active={rival,returnStage,chosen,music:false};
    curStage=STAGES[STAGES_AT[rival]-1];stagePlan=[];waveIdx=0;
    s6Opening=null;s6Wing=null;
    enemies.length=0;eBullets.length=0;pBullets.length=0;
    subBossDone=true;subBossTriggered=true;subBossActive=false;subBoss=null;
    bossWarned=true;warnT=0;
    spawnBoss('rebelsquad');bossActive=true;bossDefeated=false;
    const R=boss._rebels;R.frStageX=true;
    for(const q of R.ships){q.dead=q.i!==rival;if(!q.dead){q.hp=q.max*=2.4;q.homeX=worldWidth()/2;q.homeY=VH*.25;}}
    boss.hp=boss.maxhp=R.ships[rival].max;
    wing=chosen.map((key,i)=>({key,slot:i,phase:'arrive',hp:45,maxhp:45,x:player.x+(i?70:-70),y:VH+35+i*14,t:0,cd:.4+i*.25,dead:false}));
    for(const key of chosen)for(let f=0;f<8;f++){XART.rdy('ship_'+key+'_br'+f);XART.rdy('ship_'+key+'_so'+f);}
    XART.rdy('r24_card');Audio.SFX.alertBossIncoming&&Audio.SFX.alertBossIncoming();
  }
  function cardDraw(dt){
    ctx.fillStyle='#000';ctx.fillRect(0,0,VW,VH);
    if(XART.rdy('r24_card')){const im=XART.get('r24_card');const w=VW,h=w*(im.naturalHeight||im.height)/(im.naturalWidth||im.width);ctx.drawImage(im,0,(VH-h)/2,w,h);}
    if(stateT>3.5||stateT>.8&&Input.menuConfirm())proceedIntro();
  }
  function tick(dt){if(!active||state!==GS.PLAY)return;
    if(!active.music){active.music=true;Audio.startMusic('stagex');}
    const formation={ships:wing,boxes:[]};
    for(let i=0;i<wing.length;i++){
      const q=wing[i];if(q.dead)continue;q.t+=dt;q.cd-=dt;
      ally27Tick(q,dt);s6WingNavigate(q,formation,dt);
      if(q.phase==='arrive'&&q.y<VH-75)q.phase='fight';
      if(q.phase==='fight')q.y=Math.min(q.y,bottomHudLayout().rail.y-26);
      for(let j=eBullets.length-1;j>=0;j--){const z=eBullets[j];if(q.dodgeT>0||!z||z.dead||Math.abs(z.x-q.x)>13||Math.abs(z.y-q.y)>15)continue;
        eBullets.splice(j,1);q.hp-=Math.max(1,z.dmg||3);q.flash=.18;
        if(q.hp<=0){q.dead=true;q.phase='leave';unitDeathFX({x:q.x,y:q.y,w:39,h:39},'jet','blue');break;}
      }
      if(q.dead)continue;q.flash=Math.max(0,(q.flash||0)-dt);
      if(q.cd<=0&&!q.dodgeT&&q.phase==='fight'){q.cd=.25+i*.035;
        const targets=boss&&boss._rebels?boss._rebels.ships.filter(s=>!s.dead&&s.mode!=='entry'):[];
        const target=targets.reduce((best,s)=>!best||Math.hypot(s.x-q.x,s.y-q.y)<Math.hypot(best.x-q.x,best.y-q.y)?s:best,null);
        const dx=target?target.x-q.x:0,dy=target?target.y-q.y:-300,mag=Math.hypot(dx,dy)||1;
        pBullets.push({x:q.x,y:q.y-17,vx:dx/mag*10,vy:dy/mag*10,w:5,h:12,dmg:3,kind:'mg',ally:true,col:(PILOTS.find(p=>p.key===q.key)||{}).tint||'#adf5ff'});
        q._muzzle=.10;
        if(Audio.SFX.machineGun)Audio.SFX.machineGun();
      }
      q._muzzle=Math.max(0,(q._muzzle||0)-dt);
    }
  }
  function draw(){if(!active||state!==GS.PLAY)return;
    for(const q of wing){if(q.dead)continue;const k='ship_'+q.key;if(!XART.rdy(k))continue;
      let art=k;
      if(q.dodgeT>0){const f=clamp(Math.floor((1-q.dodgeT/q.dodgeDuration)*8),0,7),pose=k+'_'+(q.dodgeMode==='somer'?'so':'br')+f;if(XART.rdy(pose))art=pose;}
      const im=XART.get(art),h=39,w=h*(im.naturalWidth||im.width)/(im.naturalHeight||im.height);
      ctx.save();ctx.globalAlpha=q.flash>0?.56:1;ctx.drawImage(im,q.x-w/2,q.y-h/2,w,h);ctx.restore();
      ctx.fillStyle='#192536';ctx.fillRect(q.x-17,q.y+22,34,3);
      ctx.fillStyle='#53d9af';ctx.fillRect(q.x-17,q.y+22,34*q.hp/q.maxhp,3);
      if(q._muzzle>0&&typeof wm26Draw==='function')wm26Draw(ctx,'mg',q.x,q.y-17,-Math.PI/2,1-q._muzzle/.10,22);
    }
    campText('RIVAL FIGHT!   '+wing.filter(q=>!q.dead).length+' WINGMEN ACTIVE',camLeftX()+viewW()/2,47,10,'#ffe0b5');
  }
  function finish(){if(!active)return false;
    const A=active;active=null;wing=[];
    if(!campaign.rivalDefeated)campaign.rivalDefeated=[false,false,false,false,false];
    campaign.rivalDefeated[A.rival]=true;
    run.stage=A.returnStage;
    try{const data=Object.assign(campSnapshot(),{mode:'campaign',stage:A.returnStage});localStorage.setItem(CAMP_AUTO_KEY,JSON.stringify(data));campSession=data;}catch(_e){}
    Audio.stopMusic();openStageSelect(A.returnStage,{});
    return true;
  }
  function reset(){active=null;wing=[];select=null;mapFocus=false;mapMouse=false;}
  function restart(){
    if(!active)return false;
    select={rival:active.rival,chosen:active.chosen.slice()};deploy();return true;
  }
  function scatterAfterHarrier(){
    if(run.mode!=='campaign'||!s6Wing||s6Wing.route!=='left')return;
    if(!campaign.rivalScattered)scatterT=0;
    campaign.rivalScattered=true;
    if(!Array.isArray(campaign.rivalDefeated))campaign.rivalDefeated=[false,false,false,false,false];
  }
  function save(){return {scattered:!!campaign.rivalScattered,defeated:(campaign.rivalDefeated||[]).slice(0,5)};}
  function load(s){reset();campaign.rivalScattered=!!(s&&s.scattered);campaign.rivalDefeated=s&&Array.isArray(s.defeated)?s.defeated.slice(0,5):[false,false,false,false,false];}
  return {get active(){return active;},get mapFocused(){return mapFocus;},get mapAvailable(){return available();},get flying(){return available()&&scatterT!=null&&scatterT<3.2;},arenaStage(){return active?STAGES_AT[active.rival]:null;},mapDraw,mapInput,mapBack,selectDraw,cardDraw,tick,draw,finish,reset,restart,scatterAfterHarrier,save,load};
})();
