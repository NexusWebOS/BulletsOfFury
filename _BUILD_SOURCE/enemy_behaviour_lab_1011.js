/* Verification only: never loaded by index.html. */
(()=>{
   window.EA11={rows:[],specs:{},serial:0,base:{begin:ai27Begin,end:ai27End,spawn:spawnEnemy}};
   spawnEnemy=function(type,x,y,opt){const n=enemies.length,r=EA11.base.spawn.apply(this,arguments);for(const e of enemies.slice(n))e._eaSpawnOpt={...opt};return r;};
   ai27Begin=function(e,dt){const previous=EA11.base.begin.apply(this,arguments);
    if(!e._ea11)e._ea11={id:++EA11.serial,type:e.type,pattern:e.pattern,shots:0,beams:0,visible:0,age:0,minY:e.y,maxY:e.y,minX:e.x,maxX:e.x,blocked:0,actions:[]};
    const q=e._ea11;q.age+=dt;if(e._ai27?.visible)q.visible+=dt;q.minY=Math.min(q.minY,e.y);q.maxY=Math.max(q.maxY,e.y);q.minX=Math.min(q.minX,e.x);q.maxX=Math.max(q.maxX,e.x);
    q._bullets=eBullets.length;q._beams=orbBeams.length+(typeof S81003==='undefined'?0:S81003.beams.length);q._ground=groundTargetingFx.length;return previous;};
   ai27End=function(e,prev){const q=e._ea11;if(q){q.shots+=Math.max(0,eBullets.length-q._bullets);q.beams+=Math.max(0,orbBeams.length+S81003.beams.length-q._beams);
    q.ground=(q.ground||0)+Math.max(0,groundTargetingFx.length-q._ground);q.blocked=e._ai27?.blocked||0;for(const key of ['_ac10Ram','_ram','_phase','_orbit1003','_frRealmAI','_s2Act','_s3Act','_s4Act','_s5Act','_s6Act','_s7Act','_s9Act']){const a=e[key];if(a){const s=key+':'+(typeof a==='string'?a:a.phase||a.mode||a.state||(a.fired?'fired':'pending'));if(!q.actions.includes(s))q.actions.push(s);}}}
    return EA11.base.end.apply(this,arguments);};
   EA11.setup=function(stage,diff){ht27Stop();coopOn=false;diffKey=diff;run.mode='arcade';DIFF=difficultyForRun(run.mode,diff);
    run.pilot='yuri';pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');PILOTMOD={...PILOTS[pilotIndex]};run.lives=20;run.contUsed=0;run.shield=0;
    beginStage(stage);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=special=thunderStorm=s6Opening=null;H3.ending=null;H3.release=false;AP10_X.intro=null;P2M.active=null;FS11.pending=null;FS11.boxes=[];
    boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=subBossTriggered=bossWarned=true;warnT=0;warnKind=null;
    enemies=[];eBullets=[];pBullets=[];powerups=[];l5Rocks=[];l5RockT=99999;spawnClock=9999;
    player.dead=player.out=false;player.alive=true;player.invuln=40002;player.x=worldWidth()/2;player.y=VH*.80;camX=player.x-VW/2;
    player.roll=player.somer=player._spin=player._voidDeath=null;for(const k of Object.keys(Input.keys))Input.keys[k]=false;
    if(window.BOFOnline)window.BOFOnline.submitScore=()=>{};};
   EA11.collect=function(){const plan=[...stagePlan],found={},delay=aiDelay;aiDelay=(t,fn)=>fn();for(const w of plan){
    stageTimer=w.t;mapScroll=w.fn._s1MapScroll??w.t*40;enemies=[];aiQueue=[];try{w.fn();}catch(err){EA11.rows.push({waveError:String(err),t:w.t});}
    for(const e of enemies){if(e.prop||e._prop||e.pattern==='prop'||isSetPiece(e)||e._mini)continue;
     const key=e.type+'|'+e.pattern+'|'+(e._s9Role||'')+'|'+!!e._s1Kamikaze+'|'+(e._modTurret?.weapon||'');if(!found[key])found[key]={type:e.type,pattern:e.pattern,opt:{...e._eaSpawnOpt,pattern:e.pattern,_side:e._side,phase:e.phase,_s9Role:e._s9Role,_s1Kamikaze:e._s1Kamikaze,_s1Rush:e._s1Rush,_modStage:e._modTurret?.stage,_modWeapon:e._modTurret?.weapon},x:e.x,y:e.y,map:mapScroll,flags:Object.keys(e).filter(k=>/^_(s[2-9]|alien|volc|orb|dr|l6x|droid|jet|mission|fb2Stealth)/.test(k)),shoots:e.shoots,fk:e.fk};}
   }aiDelay=delay;aiQueue=[];stagePlan=[];stageTimer=0;enemies=[];EA11.specs[run.stage]=Object.values(found);return EA11.specs[run.stage];};
   EA11.case=function(spec){enemies=[];eBullets=[];pBullets=[];orbBeams=[];S81003.beams=[];groundTargetingFx=[];
    let seed=1011;Math.random=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};
    mapScroll=spec.map;_prevMapScroll=mapScroll;_lastScrollDy=0;_tsPrev=null;_tsPx=.34;_tsSeen=false;_tsScrollFrame=-1;camX=(worldWidth()-VW)/2;EB11.clock=0;EB11.nextTell=0;
    const physical=['s1tank','naval','ground'].includes(spec.pattern);
    const x=physical||spec.type==='s7pipe'?spec.x:spec.x<0?camLeftX()-70:spec.x>worldWidth()?camRightX()+70:worldWidth()*.5;
    if(physical||spec.type==='s7pipe'){player.x=clamp(spec.type==='s7pipe'?100:x,40,worldWidth()-40);camX=clamp(player.x-VW/2,0,worldWidth()-viewW());}else player.x=worldWidth()/2;
    ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);_prevMapScroll=mapScroll;_lastScrollDy=0;
    spawnEnemy(spec.type,x,spec.y,spec.opt);
    window.E=enemies.at(-1);stagePlan=[];waveIdx=999;stageTimer=0;return !!E;};
   EA11.step=function(n){for(let i=0;i<n;i++){player.invuln=40002;if(E&&['naval','s1tank'].includes(E.pattern)){player.x=clamp(E.x,40,worldWidth()-40);camX=clamp(player.x-VW/2,0,worldWidth()-viewW());}updatePlay(1/60);if(i%12===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}if(!E||E.dead||E._dyingT!=null)break;}return E?{...E._ea11,dead:E.dead,x:E.x,y:E.y,hp:E.hp,shoots:E.shoots,fk:E.fk,phase:E._phase,beached:E._beached,ram:!!(E._ac10Ram||E._ram||E._s1Kamikaze||E.impact),support:E._s5space==='s5repair',ai:E._ai27?.seen,gate:state,story:!!story,finite:[E,...eBullets].every(q=>Number.isFinite(q.x)&&Number.isFinite(q.y))}:null;};
  })();
