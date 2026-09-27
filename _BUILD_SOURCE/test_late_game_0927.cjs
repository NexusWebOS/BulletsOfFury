module.exports=function(vm,ctxv,ok){
  const fs=require('fs'),path=require('path');
  console.log('=== 307. Field reactions, ally recharge, Stage 7/9 attack turns ===');
  for(const f of ['combat_ai_0927.js','late_encounters_0927.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),ctxv);
  const result=JSON.parse(vm.runInContext(`(()=>{
    const out={};diffKey='normal';DIFF=DIFFS.normal;run.stage=1;run.mode='arcade';camX=0;
    player.dead=false;player.x=240;player.y=410;enemies=[];pBullets=[];eBullets=[];
    const e={type:'jet',x:200,y:-60,w:34,h:34,hp:10},old=ai27Begin(e,.016);
    eShootT(e.x,e.y,Math.PI/2,3,'bolt');ai27End(e,old);
    out['unseen field enemies cannot fire into the camera']=eBullets.length===0&&e._ai27.blocked>0;
    e.y=150;for(let i=0;i<40;i++){const p=ai27Begin(e,1/60);ai27End(e,p);}
    let p=ai27Begin(e,1/60);eShootT(e.x,e.y,Math.PI/2,3,'bolt');ai27End(e,p);
    out['established visible enemies can release rounds']=eBullets.length===1;
    e.hp=9;p=ai27Begin(e,1/60);const count=eBullets.length;eShootT(e.x,e.y,Math.PI/2,3,'bolt');ai27End(e,p);
    out['damage briefly interrupts a field volley']=eBullets.length===count&&e._ai27.flinch>0;
    out['field emitter context restores after update']=ai27Context===null;
    eShootT(150,150,Math.PI/2,3,'bolt');out['boss and detached rounds bypass field visibility gate']=eBullets.length===count+1;
    out['anchored turrets cannot acquire a lateral dodge']=!ai27Air({type:'turret',_tur:{},_dr:true})&&!ai27Air({type:'tank',_vkind:'tank',_dr:true});
    const q={x:240,y:360,slot:1},events=[];
    for(let i=0;i<1800;i++){ally27Tick(q,1/60);if(ally27Dodge(q,{x:241,y:360},25,455,90,440))events.push({t:i/60,m:q.dodgeMode,d:q.dodgeDuration});}
    for(const mode of ['roll','somer']){
      const ev=events.filter(e=>e.m===mode),cool=mode==='roll'?BR_COOL:SS_COOL,dur=mode==='roll'?BR_DUR:SS_DUR;
      out[mode+' uses player duration and full post-maneuver recharge']=ev.length>=3&&ev.every(e=>e.d===dur)&&ev.slice(1).every((e,i)=>e.t-ev[i].t>=cool+dur-.001);
    }
    out['roll and somersault never overlap']=events.slice(1).every((e,i)=>e.t-events[i].t>=events[i].d-.001);
    run.stage=6;s6Wing={ships:[]};const without=s6PressureMultiplier();s6Wing.ships=Array.from({length:8},()=>({phase:'fight'}));
    out['wing support decreases rather than multiplies enemy pressure']=s6PressureMultiplier()<without;
    stageTimer=10;s6Wing.combatTime=10;const a=ally27ArsenalTurn({key:'cole'}),secondRelease=ally27ArsenalTurn({key:'yuri'});s6Wing.combatTime+=.71;
    out['wing heavy releases are separated']=a&&!secondRelease&&ally27ArsenalTurn({key:'yuri'});
    s6Wing=null;
    for(const difficulty of ['normal','hard','furious']){
      diffKey=difficulty;DIFF=DIFFS[difficulty];run.stage=7;
      const b={x:240,y:145,w:200,h:160,hp:100,maxhp:100,_ship:'dualscoopdredger'};
      late27Init(b,'dredger');late27Set(b,'bucket-run');const landing=b._late27.landing;
      out[difficulty+' landing warning commits to actual feet']=landing.x===b._late27.to.x&&landing.y===b._late27.to.y+65&&landing.warn===b._late27.dur&&!landing.track;
      const x=player.x;player.x+=100;late27Step(b,.2);
      out[difficulty+' leap cannot retarget after warning']=landing.x===b._late27.to.x&&landing.t===0;
      player.x=x;late27Suspend(b);out[difficulty+' interrupted landing cancels its strike']=landing.dead&&b._late27.suspended;
      late27Set(b,'recover');out[difficulty+' recovery has its own bounded duration']=b._late27.dur<1.3;
      late27Set(b,'mine-gate');const A=b._late27;
      out[difficulty+' mine gate preserves an escape lane']=A.paths.length===(difficulty==='normal'?4:6)&&A.paths.every(p=>p.anchor&&Math.abs(Math.floor(p.anchor.x/worldWidth()*7)-A.gapLane)>=(difficulty==='normal'?2:1));
    }
    run.stage=7;const cancelledBoss={x:240,y:145,w:200,h:160,hp:100,maxhp:100,_ship:'dualscoopdredger'};
    late27Init(cancelledBoss,'dredger');late27Set(cancelledBoss,'bucket-run');const landing=cancelledBoss._late27.landing;
    cancelledBoss.dead=true;groundTargetingTick(.02);
    out['killing a leaping miniboss cancels its pending impact']=landing.dead&&!landing.impact;
    run.stage=3;const drone=spawnEnemy('sharddart',200,-72,{_adaptiveReinforcement:true});
    out['reinforcement drone has a finite native flight amplitude']=Number.isFinite(drone.amp)&&drone.amp>0;
    run.stage=9;const b={x:240,y:140,w:200,h:200,hp:100,maxhp:100,_ship:'tidalsovereign'};late27Init(b,'tidal');late27Set(b,'torpedo-hunt');
    eBullets=[];late27Step(b,.2);out['Tidal windup cannot release early']=eBullets.length===0;
    late27Step(b,1);out['Tidal torpedoes have authored art and can be shot down']=eBullets.length>0&&eBullets.every(p=>p._s9a==='tidaltorp'&&p._shootable&&p.hp===1);
    const h={x:240,y:145,w:200,h:160,hp:100,maxhp:100,_s9rift:{core:{x:240,y:145,w:200,h:160}}};
    late27Init(h,'horizon');late27Set(h,'horizon-orbit');const H=h._late27;
    out['Horizon radial attack leaves committed player-facing opening']=H.paths.length>=6&&H.paths.every(p=>Math.abs(Math.atan2(Math.sin(p.a-H.aim),Math.cos(p.a-H.aim)))>.58);
    return JSON.stringify(out);
  })()`,ctxv));
  for(const [name,pass]of Object.entries(result))ok(pass,'Late combat: '+name);
};
