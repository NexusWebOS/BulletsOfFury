module.exports=function(vm,ctxv,ok){
 console.log('=== September 27 video regression repairs ===');
 // The older harness deliberately tests pre-finale compatibility earlier.
 // Load the shipped finale now for its current collision behavior.
 vm.runInContext(require('fs').readFileSync(require('path').join(__dirname,'../assets/vile_finale_0924.js'),'utf8'),ctxv);
 if(vm.runInContext("typeof Rival24==='undefined'",ctxv))vm.runInContext(require('fs').readFileSync(require('path').join(__dirname,'../assets/rival_fight_0924.js'),'utf8'),ctxv);
 // An early legacy harness section leaves playerHit stubbed. Restore the real
 // death path only for the respawn regression, then put its prior binding back.
 const gameSource=require('fs').readFileSync(require('path').join(__dirname,'../assets/game.js'),'utf8');
 const hitStart=gameSource.indexOf('function playerHit(source){');
 ctxv.__overnightRealPlayerHit=vm.runInContext('('+gameSource.slice(hitStart,gameSource.indexOf('\nfunction triggerGameOver()',hitStart))+')',ctxv);
 const out=JSON.parse(vm.runInContext(`(()=>{
  const o={};
  run.mode='arcade';diffKey='normal';DIFF=DIFFS.normal;run.pilot='cole';beginStage(4);player.reset();boss=null;bossActive=false;
  const zoom=viewZoom();spawnBoss('stormsovereign');o['Stage 4 boss does not change framing']=viewZoom()===zoom;
  for(const d of ['normal','hard','furious'])for(let s=1;s<=9;s++){
   diffKey=d;DIFF=DIFFS[d];const plan=[];difficultyElitePlan(plan,s);o[d+' stage '+s+' adds no elite helpers']=plan.length===0;
  }
  beginStage(5);setState(GS.PLAY);player.reset();player.invuln=999;run.spaceMode=true;run.spaceWeapon=1;run.spaceLevels=[3,3,3];run.sonicT=run.dkT=0;lzMount=null;run.weapon=0;
  for(const k of ['maverick','yuri','falva']){run.pilot=k;special={pilot:k,t:10};run._spaceShadowHeld=true;run._spaceShadowCharge=.8;
   o[k+' special owns trigger instead of Shadow Orb']=!spaceShadowTick(1/60,true)&&!run._spaceShadowHeld&&run._spaceShadowCharge===0;
  }
  for(const k of ['cole','decker','freezer']){run.pilot=k;special={pilot:k,t:10};spaceShadowCancel();o[k+' non-primary special keeps Shadow Orb firing']=spaceShadowTick(.1,true)&&run._spaceShadowCharge>.09;}
  special=null;run.pilot='cole';pBullets=[];spaceShadowRelease(SPACE_SHADOW_FULL_CHARGE);o['Shadow Orb full charge matches reduced damage']=Math.abs(pBullets[0].dmg-SPACE_SHADOW_TIER[2].base*1.5*.78)<1e-8;
  const snd=Audio.SFX.missile;let launches=0;Audio.SFX.missile=()=>launches++;run.bombs=2;player.dead=false;retina.target=null;pBullets=[];useBomb();o['unlocked manual missile has a launch cue']=launches===1&&pBullets[0].kind==='gmiss'&&!pBullets[0].tgt;Audio.SFX.missile=snd;
  for(const d of ['normal','hard','furious']){
   diffKey=d;DIFF=DIFFS[d];beginStage(5);setState(GS.PLAY);player.reset();player.invuln=999;spawnBoss('chromehammer');const b=boss,h=b._hammer;b.enter=false;b._noHit=false;h.balance0922=true;h.mode='hammer';b.hp=b.maxhp*.45;hammerState(b,'hammer');
   const seen=[];for(let i=0;i<1800&&!h.phaseTwo;i++){hammerBossTick(b,1/60);if(!seen.includes(h.state))seen.push(h.state);}
   o[d+' low health still performs ball before cannon phase']=seen.includes('ball')&&h.ballSeen&&h.phaseTwo;
   h.mode='hammer';h.phasePending=false;b.hp=b.maxhp;h.tx=b.x;h.ty=b.y;eBullets=[];hammerState(b,'leap');hammerBossTick(b,1);
   o[d+' impact lasers use difficulty speed']=eBullets.length===8&&eBullets.every(q=>Math.abs(Math.hypot(q.vx,q.vy)-(d==='furious'?7.4:d==='hard'?5.7:3.5))<1e-8);
   hammerStormStart(b);hammerStormTarget(b);hammerStormImpact(b);const q=h.stormWaves[0];q.t=q.split+q.delay+q.warm-.01;o[d+' warning remains before eruption']=!!hammerStormRedZone(q)&&!!hammerStormRowAlert(q);
   q.t+=.02;o[d+' red field and sign clear on eruption']=hammerStormRedZone(q)===null&&hammerStormRowAlert(q)===null;
  }
  beginStage(6);enemies=[];spawnBoss('warhive');boss.enter=false;boss.x=worldWidth()/2;boss.y=VH*.4;boss._whv.cx=boss.x;boss._whv.cy=boss.y;whvLaunchJet(boss);const jet=enemies.at(-1),y=jet.y;eBullets=[];
  hivewingTick(jet,.55,ELITEX.hivewing);o['Harrier launch grows north with correct sprite heading']=jet.y<y&&jet._scale>.18&&jet._scale<1&&jet.spin===-Math.PI&&eBullets.length===0;
  hivewingTick(jet,.56,ELITEX.hivewing);hivewingTick(jet,.9,ELITEX.hivewing);o['escort smoothly finishes turn at full scale']=jet._scale===1&&Math.abs(jet.spin)<1e-8&&!jet._hwLaunch&&!jet._hwPeel&&!jet._noHit;
  diffKey='normal';DIFF=DIFFS.normal;beginStage(8);enemies=[];eBullets=[];pBullets=[];run.distance=0;s8VolleyNext=0;const a=spawnEnemy('s8leech',240,100,{}),b=spawnEnemy('s8leech',330,100,{});a._fcd=b._fcd=0;
  let first=null,second=null,prior=0;
  for(let i=0;i<90;i++){run.distance+=40/60;s8MegaTick(a,1/60);s8MegaTick(b,1/60);if(eBullets.length>prior){if(first===null)first=i/60;else if(second===null)second=i/60;prior=eBullets.length;}}
  o['Stage 8 simultaneous ships keep visible charge time']=first>=.46;
  o['Stage 8 volley releases are spaced apart']=second-first>=.43;
  beginStage(8);enemies=[];eBullets=[];pBullets=[];run.distance=0;s8VolleyNext=0;const unseen=spawnEnemy('s8leech',240,-200,{});unseen._fcd=0;
  for(let i=0;i<60;i++){run.distance+=40/60;s8MegaTick(unseen,1/60);}o['Stage 8 cannot start an attack before entering view']=eBullets.length===0&&!unseen._s8Act;
  o['heavy fleet keeps five / six / seven hull pressure limits']=['normal','hard','furious'].every((d,i)=>{diffKey=d;return stageAiProfile(8).cap===5+i;});
  diffKey='normal';DIFF=DIFFS.normal;beginStage(3);spawnSubBoss__inner('frostcruiser');subBoss.enter=false;subBoss.x=240;subBoss.y=130;const arrival={x:subBoss.x,y:subBoss.y};er26Tick(subBoss,1/60);
  o['Frost Cruiser recovery starts at its arrival, not its spawn']=Math.hypot(subBoss.x-arrival.x,subBoss.y-arrival.y)<1;
  beginStage(9);spawnSubBoss__inner('voidhorizon');for(let i=0;i<103;i++)late27Horizon(subBoss,1/60);const settled={x:subBoss.x,y:subBoss.y};late27Horizon(subBoss,1/60);
  o['Horizon recovery cannot teleport back to the entry origin']=!subBoss.enter&&Math.hypot(subBoss.x-settled.x,subBoss.y-settled.y)<1;
  beginStage(9);spawnBoss('tidalfusion');const fb=boss,F=fb._s9fusion;fb.enter=false;
  o['Sentinel fusion starts at world centre']=fb.x===worldWidth()/2;
  for(const w of [F.left,F.right]){w._s9VolleyWarn={t:.3};F.hit=w;s9FusionHit(fb,w.hp);}
  o['Disabled Sentinels clear their pending warning fields']=!F.left._s9VolleyWarn&&!F.right._s9VolleyWarn&&F.phase==='fuse';
  for(let i=0;i<146;i++)s9FusionBossTick(fb,1/60);
  o['Fused hull emerges at the portal world position']=F.phase==='tidal'&&Math.abs(fb.x-worldWidth()/2)<1;
  beginStage(8);camX=0;spawnBoss('vileexistence');const vb=boss;player.dead=false;player.somer=null;player.roll=null;player.x=camLeftX()+35;player.y=VH*.8;
  const P={type:'box',t:0};vile25Start(vb,P);let maxPush=0;
  for(let i=0;i<125;i++){const x=player.x;camX=Math.max(0,camX+.8);vile25Tick(vb,P,1/60);maxPush=Math.max(maxPush,Math.abs(player.x-x));}
  o['Ghost walls remain anchored while camera pans']=P.boxLeft===0&&Math.abs(P.walls.lx-(-VW/3*.60+P.left*(VW*.30+VW/3*.60)))<.001;
  o['Ghost walls push continuously without entry teleport']=maxPush<4;
  player.somer={t:.2,y0:VH*.8,dur:.62};player.y=VH*.8-100;player.x=P.walls.lx;
  vile25Tick(vb,P,1/60);o['Somersault stays boxed horizontally without a vertical snap']=player.x>P.walls.lx&&Math.abs(player.y-(VH*.8-100))<.001;
  const owner={},savedCue=Audio.SFX.combatOrb0927;let count=0;Audio.SFX.combatOrb0927=()=>count++;stageTimer=30;
  combatAudio0927(owner,'combatOrb0927',.25);combatAudioTick0927(.10);combatAudio0927(owner,'combatOrb0927',.25);combatAudioTick0927(.20);combatAudio0927(owner,'combatOrb0927',.25);
  o['Attack audio repeats while miniboss freezes stage timer']=stageTimer===30&&count===2;Audio.SFX.combatOrb0927=savedCue;
  beginStage(6);setState(GS.PLAY);s6Opening=null;stageTimer=30;bossActive=false;subBossActive=true;s6Wing={combatTime:0,ships:[],reinforce:10};
  const ally={key:'cole',slot:0,x:240,y:500,target:{x:240,y:150},missileCd:0,specialCd:10};pBullets=[];
  s6WingArsenal(ally,0);const firstAllies=pBullets.length;s6OnslaughtTick(s6Wing,.35);
  o['Ally heavy weapons keep the shared release gap']=firstAllies===2&&!ally27ArsenalTurn({key:'decker'});
  s6OnslaughtTick(s6Wing,.36);o['Ally release clock advances during a frozen miniboss timer']=stageTimer===30&&ally27ArsenalTurn({key:'decker'});
  s6OnslaughtTick(s6Wing,5.6);s6WingArsenal(ally,6.31);o['Ally missiles recharge after their full cooldown during miniboss']=pBullets.length===4&&ally.missileCd===6.2;
  beginStage(6);s6Opening=null;bossActive=false;spawnSubBoss__inner('tempestbrothers');enemies=[];const duo=subBoss._tempestDuo;duo.ai.black.phase='chase';duo.ai.black.vulnerable=true;duo.ai.black.boss.y=230;tempestBrothersSync(subBoss);s6Wing={ships:[],boxes:[]};
  const support={key:'cole',slot:0,x:240,y:400,t:2,phase:'fight'};s6WingNavigate(support,s6Wing,1/60);
  o['Ally targeting includes vulnerable miniboss modules']=!!support.target&&support.target._retinaOwner===subBoss;
  o['Tempest committed charge interval scales with difficulty']=['normal','hard','furious'].every((d,i)=>{diffKey=d;return Math.abs(tempestJetChargeDuration()-[1.20,1.10,1.0][i])<1e-8;});
  diffKey='normal';DIFF=DIFFS.normal;
  beginStage(7);spawnBoss('sludgeemperor');const wb=boss,M=s7mInit(wb);wb.y=175;
  for(const part of M.parts)part.hp=0;M.shield=0;s7mSet(wb,'laser');s7mTick(wb,.5);o['Toxic faceplate opens during laser windup']=M.mask===1&&M.shot===0;
  const warnings=[],drawWarning=combatWarningDraw;combatWarningDraw=(b,q)=>warnings.push(q);s7mWarnings(false);combatWarningDraw=drawWarning;
  const nozzle=s7mMuzzle(wb,'emitter');o['Exposed laser warning starts at its real emitter']=warnings.length===1&&warnings[0].x===nozzle.x&&warnings[0].y===nozzle.y&&warnings[0].width>100;
  beginStage(4);setState(GS.PLAY);spawnBoss('stormsovereign');const sb=boss;sb.enter=false;sb.x=worldWidth()/2;sb.y=sb._er26.home;sb._drawY=sb.y;stage4ShieldSyncNodes(sb);
  const nodes=sb._s4war.shield.nodes;
  o['Sovereign generators clear the shield and bottom HUD']=nodes.every(n=>Math.abs(n.x-sb.x)>sb.w*.67&&n.y-34>77&&n.y+34<bottomHudLayout().rail.y);
  o['Sovereign shield phase holds a station that fits both columns']=Math.abs(er26Station(sb,-1)-er26Station(sb,1))<=4;
  o['Ordinary upward shots can approach every live generator']=nodes.every(n=>!bossHitTest(n.x,n.y+60)&&bossHitTest(n.x,n.y));
  sb._er26.mode='sovereign-battery';sb._er26.t=.4;sb._er26.warm=1;sb._er26.warnings=[{slot:'L',angle:Math.PI/2,width:30},{slot:'R',angle:Math.PI/2,width:30}];
  const sharedWarn=combatWarningDraw,drawn=[];combatWarningDraw=(b,q)=>drawn.push(q);er26Draw(sb);combatWarningDraw=sharedWarn;
  o['Sovereign draws one warning sign below its shield gauge']=drawn.filter(q=>q.fieldOnly).length===2&&drawn.filter(q=>q.alertOnly).length===1&&drawn.find(q=>q.alertOnly).alertY>=82;
  for(const d of ['normal','hard','furious']){
    diffKey=d;DIFF=DIFFS[d];beginStage(9);spawnSubBoss__inner('voidhorizon');const hb=subBoss,spawnHP=hb.hp;late27Horizon(hb,1/60);
    o[d+' Horizon retains the scaled spawn health on its first tick']=hb.hp===spawnHP&&hb.maxhp===spawnHP&&hb._s9rift.core.hp===spawnHP;
    beginStage(6);spawnSubBoss__inner('tempestbrothers');const tb=subBoss,pp=tb._tempestDuo.ships[0],jj=pp._jet,ss=pp._ai;
    tb._tempestDuo.striker=pp;jj.active=true;jj.state='offscreen-turn';jj.t=0;jj.returnFrom={x:300,y:1150};jj.reentry={x:500,y:300};
    ss.boss.x=300;ss.boss.y=1150;jj.angle=Math.atan2(-850*TLV_KY,200*TLV_KX)+Math.PI/2;
    const duration=tempestJetReturnDuration();tempestJetTick(tb,pp,duration-.01);const priorMode=jj.state,warning=tempestJetReturnWarning(pp);tempestJetTick(tb,pp,.02);
    o[d+' Tempest return waits for its committed warning']=priorMode==='offscreen-turn'&&jj.state==='return'&&warning&&warning.alertY+42<bottomHudLayout().rail.y;
  }
  diffKey='normal';DIFF=DIFFS.normal;beginStage(5);spawnSubBoss__inner('siegebomber');const bomber=subBoss;bomber.enter=false;
  siegeBomberHit(bomber,bomber._bomber.core,bomber.x,bomber.y,'core');
  o['Bomber destroyed core empties the health gauge even with surviving engines']=bomber.dead&&bomber.hp===0&&bomber._bomber.parts.some(p=>p.hp>0);
  beginStage(8);setState(GS.PLAY);spawnBoss('vileexistence');const final=boss;final._symEntry=null;final.enter=false;vile24BuildForm(final,3);final.flash=0;final.x=worldWidth()/2;final.y=140;
  const fp={type:'phantom',t:0};vile25Start(final,fp);final._v24.pattern=fp;fp.t=.8;fp.cycle=0;fp.tx=final.x+150;fp.ty=400;
  o['Phantom underground has no invisible body, shield or lock target']=!bossHitTest(final.x,final.y)&&!vile25ShieldContact(final,{x:final.x,y:final.y})&&retinaBossTargets(final).length===0;
  fp.t=1.3;const pose=vile25BodyPose(final),target=retinaBossTargets(final)[0];
  o['Phantom emerging body, shield and Retina use the visible position']=!!pose&&target.x===pose.x&&target.y===pose.y&&bossHitTest(pose.x,pose.y)&&vile25ShieldContact(final,{x:pose.x,y:pose.y})&&!bossHitTest(final.x,final.y);
  final._v24.pattern=null;o['Lock on an emerged phantom expires when it vanishes']=!retinaTargetValid(target);
  const kp={type:'knight',t:0};vile25Start(final,kp);final._v24.pattern=kp;kp.t=1.37;kp.cycle=0;kp.tx=final.x+160;kp.ty=400;
  const kt=retinaBossTargets(final)[0];o['Knight Retina follows its leaping body']=kt.x===kp.tx&&kt.y===kp.ty&&bossHitTest(kt.x,kt.y)&&!bossHitTest(final.x,final.y);
  const mp={type:'mirror',t:0};vile25Start(final,mp);final._v24.pattern=mp;mp.t=1;final._v24.shield=0;
  const echoes=retinaBossTargets(final),fake=(mp.real+1)%4,priorHP=final.hp;retinaMissileDamage(echoes[fake],20,{kind:'gmiss',x:echoes[fake].x,y:echoes[fake].y});
  o['All four echoes can be locked without exposing which is real']=echoes.length===4&&echoes.every(t=>t.kind==='echo');
  o['Missile against a fake echo enrages it without damaging real boss']=mp.clones[fake].rage>0&&final.hp===priorHP;
  retinaMissileDamage(echoes[mp.real],20,{kind:'gmiss',x:echoes[mp.real].x,y:echoes[mp.real].y});
  o['Missile against the real echo uses ordinary boss damage']=final.hp<priorHP&&mp.realDamage>0;
  final._v24.shield=200;o['Mirror cannot reflect fire from an invisible central shield']=!vile25ShieldContact(final,{x:final.x,y:final.y});
  const warns=[],reticles=[],savedWarn=combatWarningDraw,savedReticle=groundTargetReticleDraw;
  combatWarningDraw=(b,q)=>warns.push(q);groundTargetReticleDraw=(...args)=>reticles.push(args);
  vile25Warn(final,'phantom',final.x,final.y,300,380,.8,102);combatWarningDraw=savedWarn;groundTargetReticleDraw=savedReticle;
  o['Portal warning is a local ground retina and authored sign, not a beam cone']=reticles.length===1&&reticles[0][0]===300&&reticles[0][1]===380&&warns.length===1&&warns[0].alertOnly;
  o['Final subforms own their timed contact, avoiding early generic hull hits']=['box','phantom','knight','mirror','mirrorball'].every(type=>vile25PatternOwnsContact({_v24:{pattern:{type}}}))&&!vile25PatternOwnsContact({_v24:{pattern:{type:'hyperlaser'}}});
  const savedPlayerHit=playerHit;if(typeof __overnightRealPlayerHit==='function')playerHit=__overnightRealPlayerHit;
  beginStage(5);setState(GS.PLAY);player.reset();special=null;run._megaShield=null;run.shield=0;player.x=211;player.y=398;player.invuln=0;playerHit();
  const deathAnchor=player._deathAnchor;player.x=237;player.y=482;player._px=237;player._py=482;player.somer={t:0};player.reset(true);
  o['Respawn returns to the hit position, not the falling wreck position']=deathAnchor.x===211&&deathAnchor.y===398&&player.x===211&&player.y===398&&!player._deathAnchor;
  o['Respawn clears stale movement prediction and flip state']=player._px===211&&player._py===398&&player._vx===0&&player._vy===0&&!player.somer;
  player._deathAnchor={x:23,y:27};player.reset();o['Fresh stage spawn ignores and clears a previous death anchor']=player.x===worldWidth()/2&&player.y===VH*.78&&!player._deathAnchor;
  playerHit=savedPlayerHit;
  beginStage(6);setState(GS.PLAY);spawnBoss('rebelsquad');const rb=boss,rs=rb._rebels.ships;
  o['Entering Rival ships are not lockable']=retinaBossTargets(rb).length===0;
  for(const q of rs){q.mode='fight';q.y=q.homeY;}
  const rt=retinaBossTargets(rb);o['Rival formation exposes five individual ship targets']=rt.length===5&&rt.every((t,i)=>t.x===rs[i].x&&t.y===rs[i].y);
  const hpBefore=rs.map(q=>q.hp);retinaMissileDamage(rt[3],25,{kind:'gmiss',x:rt[3].x,y:rt[3].y});
  o['Rival missile lock damages the selected moving ship only']=rs.every((q,i)=>Math.abs(q.hp-(hpBefore[i]-(i===3?25:0)))<1e-8);
  rs[3].warp=1;o['Warping Rival invalidates its existing lock']=!retinaTargetValid(rt[3]);rs[3].warp=0;rs[3].dead=true;o['Destroyed Rival disappears from missile targets']=!retinaTargetValid(rt[3])&&retinaBossTargets(rb).length===4;
  run.mode='campaign';run.pilot='cole';campaign.unlockedMax=8;campaign.rivalScattered=true;campaign.rivalDefeated=[false,false,false,false,false];openStageSelect(8,{});stateT=2;
  Input.injectTap('arrowdown');Rival24.mapInput();Input.injectTap('enter');Rival24.mapInput();
  Input.injectTap('enter');Rival24.selectDraw(.1);Input.injectTap('arrowright');Rival24.selectDraw(.1);Input.injectTap('enter');Rival24.selectDraw(.1);Input.injectTap('enter');Rival24.selectDraw(.1);
  o['Optional Rival fight saves its campaign return point']=!!Rival24.active&&campSnapshot().stage===8;
  const oldRival=boss;setState('paused');playPauseChoose(2);
  o['Restart rebuilds Rival encounter with the two selected allies']=!!Rival24.active&&Rival24.active.chosen.join(',')==='axel,decker'&&boss!==oldRival&&boss.kind==='rebelsquad'&&state===GS.INTRO;
  beginStage(4);o['A normal stage clears temporary Rival arena and allies']=!Rival24.active&&Rival24.arenaStage()===null&&campaign.rivalDefeated.every(x=>!x);
  campBeginFresh();o['A new campaign clears the previous Rival Crew progression']=!campaign.rivalScattered&&campaign.rivalDefeated.every(x=>!x);
  return JSON.stringify(o);
 })()`,ctxv));
 delete ctxv.__overnightRealPlayerHit;
 for(const [k,v] of Object.entries(out))ok(v,'0927 video: '+k);
};
