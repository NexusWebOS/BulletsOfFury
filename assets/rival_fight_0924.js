/* Optional Stage-6 Harrier-route consequence: five scattered rivals, two selected wingmen. */
const Rival24=(()=>{
  const STAGES_AT=[2,3,4,5,8];
  const KEYS=['voss','nyx','rook','kaia','jace'];
  const SHIPS=['voss_iron_vulture','nyx_ghostknife','rook_breachhammer','kaia_signal_wraith','jace_razorjack'];
  const COLORS=['#bc77ff','#53e6e0','#c8dcf2','#ff7087','#eced6e'];
  let mapFocus=false, mapCursor=0, mapMouse=false, mapPrevCursor=7, scatterT=null, select=null, active=null, wing=[];
  function available(){return campaign&&campaign.rivalScattered&&run.mode==='campaign'&&aliveIndices().length>0;}
  function aliveIndices(){return KEYS.map((_,i)=>i).filter(i=>!(campaign.rivalDefeated||[])[i]);}
  function pos(i){const p=sselFlagScreenXY(STAGES_AT[i]);return p?{x:clamp(p.x+24,30,VW-30),y:clamp(p.y-27,69,VH-126)}:null;}
  function mapDraw(dt){
    if(!available()||sselBoot>0)return;
    if(scatterT!=null)scatterT=Math.min(2.7,scatterT+(dt||0));
    const origin=sselFlagScreenXY(7),flying=scatterT!=null&&scatterT<2.7;
    for(const i of aliveIndices()){
      const dest=pos(i);if(!dest)continue;
      const k=flying?'rr_ship_'+SHIPS[i]:'rr_portrait_'+KEYS[i],chosen=mapFocus&&i===mapCursor;
      const f=clamp(((scatterT||0)-i*.14)/2,0,1),ease=f*f*(3-2*f);
      const p=flying&&origin?{x:lerp(origin.x,dest.x,ease),y:lerp(origin.y-25,dest.y,ease)-Math.sin(f*Math.PI)*(14+i*3)}:dest;
      ctx.save();ctx.globalAlpha=chosen?1:.86;
      ctx.shadowColor=COLORS[i];ctx.shadowBlur=chosen?16:6;
      ctx.strokeStyle=COLORS[i];ctx.lineWidth=chosen?2:1;
      ctx.strokeRect(p.x-16,p.y-14,32,28);
      if(XART.rdy(k)){const im=XART.get(k);ctx.drawImage(im,p.x-13,p.y-12,26,24);}
      ctx.restore();
      if(chosen)campText('RIVAL '+KEYS[i].toUpperCase()+' - LEVEL '+STAGES_AT[i],VW/2,VH-144,12,'#ffb6a5');
    }
    if(flying)campText('RIVAL CREW BREAKING FORMATION',VW/2,VH-128,10,'#ffb4a3');
    else if(!mapFocus)campText('RIVAL CONTACTS: DOWN TO SELECT',VW/2,VH-128,10,'#ff9d8a');
    else campText('LEFT/RIGHT: RIVAL   FIRE: FIGHT   UP: MAP',VW/2,VH-123,9,'#dceeff');
  }
  function mapInput(){
    if(!available())return false;
    if(scatterT!=null&&scatterT<2.7)return true;
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
    campText('UP/DOWN/LEFT/RIGHT: PILOT   FIRE: SELECT   BACK: CANCEL',VW/2,VH-25,9,'#a7c9da');
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
    select=null;active={rival,returnStage,chosen,music:false};
    /* Use Stage 6's neutral encounter setup, then draw the chosen contact's
       biome. Entering the destination stage outright would replay its story
       dialogue and scripted hazards over this optional duel. */
    beginStage(6);
    curStage=STAGES[STAGES_AT[rival]-1];stagePlan=[];waveIdx=0;
    s6Opening=null;s6Wing=null;
    enemies.length=0;eBullets.length=0;pBullets.length=0;
    subBossDone=true;subBossTriggered=true;subBossActive=false;subBoss=null;
    bossWarned=true;warnT=0;
    spawnBoss('rebelsquad');bossActive=true;bossDefeated=false;
    wing=chosen.map((key,i)=>({key,hp:45,maxhp:45,x:player.x+(i?70:-70),y:VH+35+i*14,t:0,cd:.4+i*.25,dead:false}));
    XART.rdy('r24_card');Audio.SFX.alertBossIncoming&&Audio.SFX.alertBossIncoming();
  }
  function cardDraw(dt){
    ctx.fillStyle='#000';ctx.fillRect(0,0,VW,VH);
    if(XART.rdy('r24_card')){const im=XART.get('r24_card');const w=VW,h=w*(im.naturalHeight||im.height)/(im.naturalWidth||im.width);ctx.drawImage(im,0,(VH-h)/2,w,h);}
    campText('3 FURY PILOTS VS 5 RIVALS',VW/2,VH-43,13,'#ccefff');
    if(stateT>3.5||stateT>.8&&Input.menuConfirm())proceedIntro();
  }
  function tick(dt){if(!active||state!==GS.PLAY)return;
    if(!active.music){active.music=true;Audio.startMusic('boss6');}
    for(let i=0;i<wing.length;i++){
      const q=wing[i];if(q.dead)continue;q.t+=dt;q.cd-=dt;
      const sx=i?1:-1,tx=clamp(player.x+sx*64+Math.sin(q.t*1.7+i)*13,camLeftX()+25,camRightX()-25),ty=clamp(player.y+22+Math.sin(q.t*2.1+i)*9,55,VH-34);
      q.x+=(tx-q.x)*Math.min(1,dt*3.4);q.y+=(ty-q.y)*Math.min(1,dt*3.5);
      for(let j=eBullets.length-1;j>=0;j--){const z=eBullets[j];if(!z||z.dead||Math.abs(z.x-q.x)>13||Math.abs(z.y-q.y)>15)continue;
        eBullets.splice(j,1);q.hp-=Math.max(1,z.dmg||3);q.flash=.18;
        if(q.hp<=0){q.dead=true;explode(q.x,q.y,45,'blue');break;}
      }
      if(q.dead)continue;q.flash=Math.max(0,(q.flash||0)-dt);
      if(q.cd<=0){q.cd=.25+i*.035;
        const targets=boss&&boss._rebels?boss._rebels.ships.filter(s=>!s.dead&&s.mode!=='entry'):[];
        const target=targets.reduce((best,s)=>!best||Math.hypot(s.x-q.x,s.y-q.y)<Math.hypot(best.x-q.x,best.y-q.y)?s:best,null);
        const dx=target?target.x-q.x:0,dy=target?target.y-q.y:-300,mag=Math.hypot(dx,dy)||1;
        pBullets.push({x:q.x,y:q.y-17,vx:dx/mag*10,vy:dy/mag*10,w:5,h:12,dmg:3,kind:'mg',ally:true,col:(PILOTS.find(p=>p.key===q.key)||{}).tint||'#adf5ff'});
        q._muzzle=.10;
      }
      q._muzzle=Math.max(0,(q._muzzle||0)-dt);
    }
  }
  function draw(){if(!active||state!==GS.PLAY)return;
    for(const q of wing){if(q.dead)continue;const k='ship_'+q.key;if(!XART.rdy(k))continue;
      const im=XART.get(k),h=39,w=h*(im.naturalWidth||im.width)/(im.naturalHeight||im.height);
      ctx.save();ctx.globalAlpha=q.flash>0?.56:1;ctx.drawImage(im,q.x-w/2,q.y-h/2,w,h);ctx.restore();
      ctx.fillStyle='#192536';ctx.fillRect(q.x-17,q.y+22,34,3);
      ctx.fillStyle='#53d9af';ctx.fillRect(q.x-17,q.y+22,34*q.hp/q.maxhp,3);
      if(q._muzzle>0&&XART.rdy('mfx_bmg_0'))ctx.drawImage(XART.get('mfx_bmg_0'),q.x-7,q.y-h/2-12,14,14);
    }
    campText('RIVAL FIGHT!   '+wing.filter(q=>!q.dead).length+' WINGMEN ACTIVE',VW/2,47,10,'#ffe0b5');
  }
  function finish(){if(!active)return false;
    const A=active;active=null;wing=[];
    if(!campaign.rivalDefeated)campaign.rivalDefeated=[false,false,false,false,false];
    /* This is a five-member fight, so a win removes the entire rival crew.
       The selected map contact decides the arena, not which pilot survived. */
    campaign.rivalDefeated=[true,true,true,true,true];
    run.stage=A.returnStage;
    try{const data=Object.assign(campSnapshot(),{mode:'campaign',stage:A.returnStage});localStorage.setItem(CAMP_AUTO_KEY,JSON.stringify(data));campSession=data;}catch(_e){}
    Audio.stopMusic();openStageSelect(A.returnStage,{});
    return true;
  }
  function scatterAfterHarrier(){
    if(run.mode!=='campaign'||!s6Wing||s6Wing.route!=='left')return;
    if(!campaign.rivalScattered)scatterT=0;
    campaign.rivalScattered=true;
    if(!Array.isArray(campaign.rivalDefeated))campaign.rivalDefeated=[false,false,false,false,false];
  }
  function save(){return {scattered:!!campaign.rivalScattered,defeated:(campaign.rivalDefeated||[]).slice(0,5)};}
  function load(s){campaign.rivalScattered=!!(s&&s.scattered);campaign.rivalDefeated=s&&Array.isArray(s.defeated)?s.defeated.slice(0,5):[false,false,false,false,false];}
  return {get active(){return active;},arenaStage(){return active?STAGES_AT[active.rival]:null;},mapDraw,mapInput,mapBack,selectDraw,cardDraw,tick,draw,finish,scatterAfterHarrier,save,load};
})();
