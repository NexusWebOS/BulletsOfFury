module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path');for(const n of ['finale_motion_art_1006.js','finale_ai_1006.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/'+n),'utf8'),c,{filename:n});
 console.log('=== Stage 8 authored motion coverage and difficulty-aware form AI ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const o={};coopOn=false;run.pilot='yuri';run.mode='campaign';diffKey='furious';DIFF=DIFFS.furious;
 beginStage(8);setState(GS.PLAY);player.reset();player.invuln=999;spawnBoss('vileexistence');story=null;BOFCinematicDirector.cancel();fb2Talk=null;
 const b=boss,S=b._r30,J=j3State(b);j3Encounter(b,2);j3Mimic(b,8);on5FightStart(b);const D=gd4Create(b,8),h=D.p._hammer;
 o['all 16 additional authored cells registered and measured']=F6_MOTION.length===16&&F6_MOTION.every(a=>XART._src[a.key]===a.path&&a.px>0&&a.px<1&&a.py>0&&a.py<1);
 const states={curl:0,ball:2,uncurl:2,giant_idle:4,giant_dive:5,giant_sweep:6,giant_recover:7,whirlwind:8,hammer_stun:12,storm_rebuild:14,throw:15};
 for(const [state,f]of Object.entries(states)){hammerState(D.p,state);h.t=0;const rig=fmcRig(b);o[state+' uses its own generated pose']=rig[0].key===F6_MOTION[f].key&&rig[0].p.id==='core';}
 h.state='whirlwind';const frames=[0,.12,.24,.36].map(t=>{h.t=t;return fmcRig(b)[0].key;});o['whirlwind turns through four authored views']=new Set(frames).size===4;
 h.state='giant_dive';h.t=0;const small=fmcRig(b)[0].w;h.t=.52;o['giant strike scales from distant descent into its source impact']=fmcRig(b)[0].w>small*5;
 h.state='ball';h.angle=.7;o['curl ball rotates with its native controller']=fmcRig(b)[0].rot===.7;
 h.throw={x:b.x-150,y:b.y+100};h.state='hammer';o['any active throw keeps robot empty handed']=fmcRig(b)[0].key===F6_MOTION[15].key&&!fmcRig(b).some(v=>v.p.id==='hammer');h.throw=null;
 h.hammerDestroyed=true;o['destroyed hammer cannot remain baked into robot pose']=fmcRig(b)[0].key===F6_MOTION[13].key&&!fmcRig(b).some(v=>v.p.id==='hammer');h.hammerDestroyed=false;
 h.state='hkSideHit';h.gp4Emergency=null;h.f6Sides=0;h.hkSide=1;hammerState(D.p,'hammer');o['Furious side strike gets an opposite independently warned followup']=h.state==='hkSideTell'&&h.hkSide===-1;
 h.state='hkSideHit';hammerState(D.p,'hammer');o['second side strike ends its combo rather than looping']=h.state==='hammer'&&h.f6Sides===0;
 diffKey='normal';h.state='hkSideHit';hammerState(D.p,'hammer');o['normal side strike remains one readable attack']=h.state==='hammer';
 j3Mimic(b,5);on5FightStart(b);const DK=gd4Create(b,5);diffKey='furious';player.x=camLeftX()+90;player.y=hammerWarningFloorY();
 hk5AttackStart(b,'leapSlash');const K=S.hkKnight,tx=K.tx,ty=K.ty;player.x+=120;player.y-=80;hk5KnightTick(b,DK,.3);o['Furious initial leap warning never chases pilot']=K.tx===tx&&K.ty===ty;
 hk5Phase(K,'recover');hk5KnightTick(b,DK,.01);o['Furious leap adds a newly warned shield followup']=K.phase==='tell'&&K.kind==='shieldSmite'&&K.f6.followed&&K.tx!==tx;
 hk5AttackStart(b,'shieldCode');const C=S.hkKnight;eBullets=[];for(let i=0;i<190;i++)hk5KnightTick(b,DK,.03);
 o['Furious code shield fires three discrete warned bursts']=C.f6.bursts===3&&F6.events.filter(q=>q.event==='knightCodeBurst').length===3;
 o['code shield alternates aim and split volleys with authored effects']=eBullets.filter(q=>q._hkCodeFire).length===10;
 hk5AttackStart(b,'armageddon');const A=S.hkKnight;A.phase='active';A.rows=[{t:0}];b.parts.find(p=>p.id==='sword').destroyed=true;hk5KnightTick(b,DK,.01);
 o['breaking sword cancels Armageddon and its damage rows']=A.phase==='recover'&&A.rows.length===0;
 b.parts.find(p=>p.id==='shield').destroyed=true;o['fully disarmed knight chooses its core fallback']=f6KnightChoice(b)==='coreCode';
 for(const i of [1,2,3,4,6,7]){j3Mimic(b,i);on5FightStart(b);const N=gd4Create(b,i),V={n:0,tx:player.x,ty:player.y};const lanes=f6SalvoLanes(b,N,V);
  o['copy '+i+' has its own finite module-bound warning pattern']=lanes.length>0&&lanes.every(L=>[L.x,L.y,L.ex,L.ey,L.a].every(Number.isFinite)&&fmcAlive(b,L.module));
  const victim=b.parts.find(p=>p.id===lanes[0].module);victim.destroyed=true;o['copy '+i+' cannot emit followups from a destroyed module']=!f6SalvoLanes(b,N,V).some(L=>L.module===victim.id);
 }
 o['all six copied donor followups use separate named patterns']=new Set(Object.values(F6_PATTERNS).map(p=>p.name)).size===6;
 o['Furnace cannon tells do not starve its relay while live beams still defer it']=!f6Busy({p:{_fz:{attack:'cannon',tells:[{}],beams:[]}}})&&f6Busy({p:{_fz:{attack:'cannon',tells:[],beams:[{}]}}})&&f6Busy({p:{_fz:{attack:'sweep',tells:[{}],beams:[]}}});
 j3Mimic(b,3);on5FightStart(b);const CR=gd4Create(b,3);CR.aa5Salvo={f6:true};eBullets.push({_f6Owner:b});j3Clear(b);
 o['transform clears pending difficulty volleys and owned shots']=!CR.aa5Salvo&&!eBullets.some(q=>q._f6Owner===b);
 j3Encounter(b,1);on5FightStart(b);S.seq=0;S.f6OuterSeq=0;const types=[];for(let i=0;i<10;i++){r30Attack(b);types.push(S.attack.type);S.attack=null;}
 o['Furious ghost rotates through rails, warp, claws and source attacks']=new Set(types).size===8&&types.filter(t=>t==='ghostWarp').length===2&&S.seq===10;
 j3Encounter(b,2);on5FightStart(b);S.cd=0;aa5DraculaTick(b,.01);const P=S.attack;P.t=P.tell+.5;aa5DraculaTick(b,.01);
 const E=P.f6Echo,target=E.tx;player.x+=80;for(let i=0;i<130;i++)aa5DraculaTick(b,.01);
 o['Furious colossus fires a committed newly warned claw echo']=!!E&&E.tx===target&&E.fired&&F6.events.some(q=>q.event==='colossusEcho');
 o['AI pass preserves nine independent pools and three outer encounters']=J.max.length===9&&J.hp.length===9&&J.encounter===2;
 return o;})())`,c));for(const[n,v]of Object.entries(out))ok(v,n);
};
