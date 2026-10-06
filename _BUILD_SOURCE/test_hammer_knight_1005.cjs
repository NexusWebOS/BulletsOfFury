module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path');for(const n of ['hammer_knight_art_1005.js','hammer_knight_1005.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/'+n),'utf8'),c,{filename:n});
 console.log('=== Persistent Hammer copy, knight extension and committed Cronos lanes ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const o={};coopOn=false;run.pilot='cole';run.mode='campaign';
 for(const diff of ['normal','hard','furious'])for(const route of ['regular','hammer','hama']){
  diffKey=diff;DIFF=DIFFS[diff];beginStage(5);setState(GS.PLAY);player.reset();player.invuln=999;player.x=worldWidth()/2;player.y=VH-90;
  const b={x:worldWidth()/2,y:180,hp:1000,maxhp:1000,w:158,h:176,dead:false,enter:false,_noHit:false};hammerBossInit(b);b._hammer.balance0922=true;
  if(route==='hammer')b._hammerTime={mode:'attack',t:0};if(route==='hama')b._hama={mode:'attack',t:0};
  // Invoke the same underlying source tick that all three wrappers delegate to.
  hammerSpellStart(b);const targets=JSON.stringify(b._hammer.spellTargets.map(q=>q.x));player.x+=135;
  for(let i=0;i<90;i++)HT27_BASE.hammerTick(b,1/60);
  o[diff+' '+route+' lightning positions never chase pilot']=JSON.stringify(b._hammer.spellTargets.map(q=>q.x))===targets;
  o[diff+' '+route+' ground retinas fit bottom visible row']=hammerWarningFloorY()+36<bottomHudLayout().radar.y&&hammerWarningFloorY()>PLAY.y+200;
  hammerState(b,'mega_charge');const x=b.x;player.x-=180;camX+=30;hammerBossTick(b,.3);o[diff+' '+route+' super lane committed']=b.x===x;
 }
 diffKey='furious';DIFF=DIFFS.furious;beginStage(5);setState(GS.PLAY);player.invuln=999;
 const b={x:worldWidth()/2,y:180,hp:1000,maxhp:1000,w:158,h:176,dead:false,enter:false,_noHit:false};hammerBossInit(b);b._hammer.balance0922=true;
 hammerStormTarget(b);hammerStormImpact(b);const rows=b._hammer.stormWaves,order=rows.map(q=>q.delay);o['spikes ripple in readable lane order']=order.every((n,i)=>!i||n>order[i-1])||order.every((n,i)=>!i||n<order[i-1]);
 const q=rows[1],base=q.split+q.delay+q.warm,rise=.38/q.riseRate;q.t=base+rise+.10;const high=hammerStormSpikeShape(q);q.t=base+rise+.24+.30;const low=hammerStormSpikeShape(q);
 o['same visible spike and collision shaft retract']=high.height>low.height&&hammerStormSpikeHits(q,q.x,q.y-low.height*.5)&&!hammerStormSpikeHits(q,q.x,q.y-high.height*.9);
 q.t=base+q.active+.01;o['collapsed spike ceases drawing and damage']=!hammerStormSpikeShape(q)&&!hammerStormSpikeHits(q,q.x,q.y);
 beginStage(8);setState(GS.PLAY);player.reset();player.invuln=999;spawnBoss('vileexistence');BOFCinematicDirector.cancel();story=null;fb2Talk=null;const B=boss,S=B._r30,J=j3State(B);j3Encounter(B,2);on5FightStart(B);
 o['ninth copied Hammer pool added without fourth outer encounter']=J.max.length===9&&J.hp.length===9&&J.encounter===2;
 j3Mimic(B,8);on5FightStart(B);const D=gd4Create(B,8),h=D.p._hammer;o['source initialization preserves copied Hammer arena position']=D.p.x===B.x&&D.p.y===B.y;gd4Tick(B,.05);o['Hammer copy runs source chromium activation']=h.state==='fr_activation'&&!!h.frArmor;
 for(let i=0;i<72;i++)gd4Tick(B,.05);o['source activation finishes into combat']=!!h.frArmor.activated&&!B._noHit;
 h.throw={x:B.x-150,y:B.y+150};const grip=hammerGripPoint(D.p);o['thrown copied weapon returns to robot hand instead of itself']=Math.hypot(grip.x-h.throw.x,grip.y-h.throw.y)>100;h.throw=null;
 h.frArmor.hp=0;B.hp=J.hp[8]=B.maxhp*.6;B._lastPart=B.parts[0];const prior=B.hp;modularHit(10);o['copied core hit uses source damage and marks white flash']=B.hp<prior&&B.flash>0;
 const hp=B.hp;j3Home(B);j3Mimic(B,8);o['Hammer returns to its own damaged health pool']=B.hp===hp&&J.active===8;
 on5FightStart(B);h.frArmor.hp=h.frArmor.max*.4;D.p.hp=B.hp;fr27Restore(D.p,.1,false,true);const heal=h.recovery;
 const target=retinaBossTargets(B).find(t=>t.kind==='hammer');const saved=_dmgBullet;_dmgBullet={kind:'retinaMissile',tgt:target};if(target)target._retinaHit(25);_dmgBullet=saved;
 o['real copied hammer target interrupts source healing']=!!target&&heal.status==='cancelled'&&h.state==='fr_stun';
 // The source's earlier restoration/red-spin gate must complete before testing its LAST reserve.
 on5FightStart(B);h.frArmor.hp=0;h._fb2RageDone=h.restorationSeen=true;h.gp4FailsafeSeen=false;B.hp=J.hp[8]=B.maxhp*.081;D.p.hp=B.hp;B._lastPart=B.parts[0];modularHit(B.maxhp);
 o['large hit cannot skip Hammer eight-percent emergency']=Math.abs(B.hp-B.maxhp*.08)<.01;gd4Tick(B,.05);
 o['copied Hammer starts source emergency charge']=!!h.gp4Emergency;
 for(let i=0;i<62;i++)gd4Tick(B,.05);o['copied emergency heals to reserve then enters red source stance']=!h.gp4Emergency&&h.gp4FailsafeSeen&&h.frArmor.rage&&B.hp>=B.maxhp*.37;
 j3Mimic(B,5);on5FightStart(B);const D5=gd4Create(B,5);hk5AttackStart(B,'leapSlash');const K=S.hkKnight,tx=K.tx,ty=K.ty;player.x+=100;player.y-=100;
 const phases=new Set();for(let i=0;i<100;i++){phases.add(S.hkKnight?.phase);gd4Tick(B,.05);}o['jump then downward slash and warned rising slash complete']= ['tell','jump','land','followTell','rise','recover'].every(n=>phases.has(n));
 o['knight jump target stays committed']=K.tx===tx&&K.ty===ty;
 hk5AttackStart(B,'armageddon');for(let i=0;i<45;i++)gd4Tick(B,.05);const R=S.hkKnight.rows;
 o['Armageddon creates both side-edge retinas with inward lanes']=R.length===3&&R.some(q=>q.x===camLeftX()+36&&q.ex>q.x)&&R.some(q=>q.x===camRightX()-36&&q.ex<q.x);
 const r=R[0];r.t=r.tell+.55;const full=hk5EruptionShape(r);r.t=r.tell+.9;const tail=hk5EruptionShape(r);o['Armageddon eruptions burst then disintegrate']=full.f===4&&tail.f>=6&&Math.abs(tail.reach)<Math.abs(full.reach);
 r.t=r.tell+r.active+.01;o['no lingering Armageddon wall after collapse']=hk5EruptionShape(r)===null;
 hk5AttackStart(B,'shieldCode');for(let i=0;i<30;i++)gd4Tick(B,.05);o['charged shield fires authored code fireballs']=eBullets.some(q=>q._hkCodeFire&&q._hkOwner===B);
 j3Clear(B);o['form exit clears custom warnings and projectiles']=!S.hkKnight&&!eBullets.some(q=>q._hkOwner===B);
 J.hp=J.hp.map(()=>0);J.hp[8]=123;J.active=7;o['living ninth pool cannot be skipped']=j3Next(J)===8;J.cursor=7;J.mimic=null;S.mode='fight';j3Morph(B,0);o['form cycle selects ninth Hammer before wrap']=J.destination===8;
 J.hp=J.hp.map(()=>0);B.hp=0;j3Home(B);o['all nine exhausted pools enter sole finale death']=S.mode==='dr5Death'&&J.encounter===2;
 for(let i=0;i<630;i++)r30Tick(B,.05);o['nine-pool finale still awards exactly one original reunion reward']=state===GS.STAGECLEAR&&S.rewarded&&S.history.filter(q=>q.event==='complete').length===1;
 o['new copied Hammer password is pinned with its correct label']=pc5Pages().flatMap(p=>p.rows).some(r=>r[0]==='HAMR8'&&r[1]==='CODE HAMMER');
 return o;})())`,c));for(const [n,v]of Object.entries(out))ok(v,n);
};
