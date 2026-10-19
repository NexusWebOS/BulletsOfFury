module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path');
 console.log('=== October 11: earned Signature Mk II, normal pickups and no opening supplies ===');
 if(vm.runInContext('typeof FS11',c)==='undefined')vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/signature_specials_1011.js'),'utf8'),c,{filename:'signature_specials_1011.js'});
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={},sv={receipt:FS11.receipt,boxes:FS11.boxes,pending:FS11.pending};
  try{
   ht27Stop();BOFCinematicDirector.cancel();H3.ending=null;AP10_X.intro=null;H3.release=false;P2M.active=null;story=fb2Talk=s6Opening=null;
   coopOn=false;run.mode='arcade';run.stage=1;setState(GS.PLAY);player.reset();FS11.receipt=null;
   o['A stale boolean does not unlock enhanced specials']=!fs11ReceiptValid(true)&&!fs11ReceiptValid({version:1,stage:'X',earned:true})&&!fs11Enhanced();
   const receipt={version:1,stage:'X',route:'right',boss:'rebelsquad',earned:true,at:1};
   for(const pk of Object.keys(FS11_UPGRADES)){
    run.pilot=pk;run.bombs=3;run.shield=0;run._chainLightningLevel=1;special=null;FS11.receipt=null;startSpecial();
    o[pk+': base pickup grants the actual unenhanced fifteen-second ability']=special?.pilot===pk&&special.dur===15&&special._fs11Level===1;
    endSpecial();FS11.receipt=receipt;startSpecial();
    o[pk+': earned pickup grants its twenty-second Mk II ability']=special?.pilot===pk&&special.dur===20&&special._fs11Level===2&&pcSpecial(pk).name.includes('MK II');
    if(pk==='cole'||pk==='lizzie')o[pk+': Mk II carries two extra warheads without stealing standard ammunition']=special.strikes===5&&special.prevBombs===3;
    if(pk==='yuri'){o['Yuri gains an extra chain tier while active']=run._chainLightningLevel===2;endSpecial();o['Yuri cleanup restores the earned chain tier']=run._chainLightningLevel===1;}
    if(pk==='freezer')o['Freezer Mk II deepens time freeze outside Stage 6']=timeScale===.4;
    if(pk==='maverick'){pBullets=[];releaseHelix(MAV_FULL);o['Maverick boosts only his newly emitted charged ball']=pBullets.length===1&&pBullets[0]._fs11Level===2&&pBullets[0].dmg===(60+Math.max(1,run.wlevels[run.weapon]||1)*10)*1.25;}
    if(pk==='falva'){rollers=[];releaseRoller(FALVA_FULL);o['Falva Mk II increases real roller contact damage']=rollers.length===1&&rollers[0].dmg===15;}
    endSpecial();
   }
   run.pilot='freezer';run.stage=6;startSpecial();o['Stage 6 retains its authored full-speed sky while Freezer is enhanced']=timeScale===1;endSpecial();
   run.pilot='axel';run.stage=1;startSpecial();player.x=240;player.y=300;player._megaGrace=0;
   const shot={x:240,y:320,vx:0,vy:-6,w:6,h:6,dmg:4};axelMegaReflect(shot);
   o['Axel strengthens a physically reflected round without extra shield hits']=shot._megaReflected&&shot._megaDamage===6&&run.shield===4;endSpecial();
   FS11.receipt=null;run.pilot='cole';run.stage=6;run._gp4StageX='right';bossDefeated=false;
   spawnBoss('rebelsquad');const b=boss;const G=rg4Init(b);
   o['Only a real matching Stage X boss spawn records the reward proof']=FS11.proof?.ref===b&&FS11.proof.kind==='rebelsquad';
   o['Entering Stage X does not unlock the reward']=!fs11UnlockFromStageX();
   bossDefeated=true;o['A living Stage X boss cannot grant the reward even with a stale clear flag']=!fs11UnlockFromStageX();
   for(const q of b._rebels.ships){const kind=ra4AttackKind(q,G);o[q.key+': the first personal supply is its own signature']=kind===FS11_REBELS[q.key].kind&&!!q.rg4.signature;}
   const voss=b._rebels.ships.find(q=>q.key==='voss');b._rebels.rf.callouts=[];rg4Attack(voss,b._rebels,G,'fusion');
   o['Voss secondary Fusion keeps its correct single callout']=voss.rg4.act?._fs11Name==='FUSION CANNON'&&b._rebels.rf.callouts.length===1&&b._rebels.rf.callouts[0].text==='FUSION CANNON';
   b.dead=true;b.hp=0;o['Defeating the recorded Stage X boss earns the permanent reward']=fs11UnlockFromStageX()&&fs11Enhanced();
   o['Repeated exits do not award another unlock']=!fs11UnlockFromStageX()&&FS11.events.filter(q=>q.event==='signature-mk2-unlocked').length===1;
   const saved=campSnapshot();o['Campaign snapshots carry the versioned earned receipt']=fs11ReceiptValid(saved.signatureMk2);
   FS11.receipt=null;campApply(saved);o['Campaign restore recovers the earned upgrade']=fs11Enhanced();
   FS11.receipt=null;delete saved.signatureMk2;campApply(saved);o['An older campaign without a receipt stays unenhanced']=!fs11Enhanced();
   run.stage=6;run._gp4StageX='left';bossDefeated=false;spawnBoss('warhive');
   o['The left Stage X Harrier records its own proof without an arrival reward']=FS11.proof?.ref===boss&&FS11.proof.kind==='warhive'&&!fs11UnlockFromStageX();
   boss.dead=true;boss.hp=0;bossDefeated=true;ap10StageXReward();
   o['The left Stage X reward path also earns all-pilot Mk II']=fs11Enhanced()&&FS11.receipt.route==='left'&&FS11.receipt.boss==='warhive';
   FS11.receipt=null;FS11.proof=null;delete run._gp4StageX;spawnBoss('warhive');boss.dead=true;boss.hp=0;bossDefeated=true;ap10StageXReward();
   o['An ordinary Stage 6 boss clear cannot earn the Stage X upgrade']=!fs11Enhanced()&&FS11.proof===null;
   FS11.receipt=null;run.pilot='cole';run.mode='arcade';coopOn=false;
   for(let n=1;n<=9;n++){
    FS11.pending={stage:n,ready:true,seats:[{seat:1,delivered:false}]};FS11.boxes=[{seat:1}];
    startRun(n);
    o['Stage '+n+' starts without an opening delivery or stale flying box']=FS11.pending===null&&FS11.boxes.length===0;
   }
   FS11.pending={stage:2,ready:true};FS11.boxes=[{seat:1}];beginStage(2);
   o['A normal level transition also discards any stale delivery']=FS11.pending===null&&FS11.boxes.length===0;
   pilotIndex=PILOTS.findIndex(p=>p.key==='cole');startRun(1);setState(GS.PLAY);
   BOFCinematicDirector.cancel();story=fb2Talk=s6Opening=null;H3.release=false;AP10_X.intro=null;
   stagePlan=[];enemies=[];powerups=[];boss=subBoss=null;bossActive=subBossActive=false;player.invuln=999;
   for(let i=0;i<180;i++)updatePlay(1/60);
   o['Opening gameplay grants no free special']=!special&&FS11.pending===null&&FS11.boxes.length===0;
   applyPowerup({kind:'specialicon',x:player.x,y:player.y});
   o['Normal special pickups still activate the actual base ability']=special?.pilot==='cole'&&special.strikes>=3&&special._fs11Level===1;
   endSpecial();coopOn=true;pilotIndex=PILOTS.findIndex(p=>p.key==='cole');p2Index=PILOTS.findIndex(p=>p.key==='lizzie');startRun(1);
   o['Co-op starts without automatic boxes for either seat']=FS11.pending===null&&FS11.boxes.length===0&&!special&&!FS11.seat2.special;
   for(const seat of seatList())withSeat(seat,()=>applyPowerup({kind:'specialicon',x:player.x,y:player.y}));
   o['Normal co-op special pickups remain with their intended pilots']=special?.pilot==='cole'&&FS11.seat2.special?.pilot==='lizzie';
   const p1=special.t,p2=FS11.seat2.special.t;updateSpecial(.1);
   o['Both co-op ability windows tick exactly once']=Math.abs(special.t-p1+.1)<1e-8&&Math.abs(FS11.seat2.special.t-p2+.1)<1e-8;
  }finally{FS11.receipt=sv.receipt;FS11.boxes=sv.boxes;FS11.pending=sv.pending;coopOn=false;endSpecial();}
  return o;
 })())`,c));
 for(const [name,passed]of Object.entries(out))ok(passed,name);
};
