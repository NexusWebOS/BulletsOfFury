module.exports=function testArchmageStormRecovery(vm,ctxv,ok){
  console.log('=== 358. Archmage cannon loss restores charged hammer (0926) ===');
  const out=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,diffKey,DIFF,powerups,eBullets,hit:playerHit,charge:Audio.SFX.bossWeaponCharge,stage:run.stage,curStage,camX,fit:VIEW_FIT};
    const o={};let cues=0;
    try{
      Audio.SFX.bossWeaponCharge=()=>cues++;powerups=[];eBullets=[];run.stage=5;curStage=STAGES[4];VIEW_FIT=0;camX=100;
      for(const d of ['normal','hard','furious']){
        diffKey=d;DIFF=DIFFS[d];player={x:240,y:410,dead:false,invuln:999};
        boss={x:104,y:286,w:158,h:176,hp:350,maxhp:1000,flash:0,enter:false,dead:false,_noHit:false};hammerBossInit(boss);
        boss.x=104;boss.y=286;boss.enter=false;boss._noHit=false;const h=boss._hammer;h.balance0922=true;h.mode='chaingun';h.state='chaingun';h.chainHP=1;boss._hammerModuleHit='chaingun';
        hammerBossDamage(boss,2);
        o[d+' cannon break restores weapon']=h.chainDestroyed&&!h.hammerDestroyed&&h.mode==='storm'&&h.state==='storm_raise'&&h.hammerHP===h.hammerMax;
        hammerBossTick(boss,1.3);o[d+' lightning charges hammer']=h.charged&&h.lightningCue;
        for(let i=0;i<500&&h.state==='storm_raise';i++)hammerBossTick(boss,1/60);o[d+' lowered idle after charge']=h.state==='storm_idle';
        hammerStormTarget(boss);const target=JSON.stringify(h.stormTarget);player.x=70;player.y=250;hammerBossTick(boss,.3);
        o[d+' committed slam target']=JSON.stringify(h.stormTarget)===target&&h.state==='storm_warn';
        hammerBossTick(boss,1);hammerBossTick(boss,.7);
        const count=Math.ceil((worldWidth()-PLAY.x*2)/96)+1;
        o[d+' complete world row']=h.state==='storm_split'&&h.stormWaves.length===count&&h.stormWaves.every(q=>q.ox===h.stormTarget.x&&q.oy===h.stormTarget.y&&!q.started);
        o[d+' single bottom row']=h.stormWaves.every(q=>q.y===hammerStormFloorY()&&q.height===VH*.75);
        o[d+' randomized permutation']=new Set(h.stormWaves.map(q=>q.delay)).size===count&&h.stormOrder.slice().sort((a,b)=>a-b).every((v,i)=>v===i);
        o[d+' original Retina size']=h.stormWaves.every(q=>q.retinaWidth===96&&q.radius===20);
        const rate=d==='furious'?2.8:d==='hard'?1.8:1;
        o[d+' faster authored rise']=h.stormWaves.every(q=>q.riseRate===rate&&Math.abs(hammerStormSpikeTime(q,.38)-.38/rate)<1e-9);
        o[d+' faster ripple cadence']=Math.abs(Math.max(...h.stormWaves.map(q=>q.delay))/(count-1)-(d==='furious'?.20:d==='hard'?.30:.50))<1e-9;
        o[d+' both map edges covered']=h.stormWaves[0].x===PLAY.x&&h.stormWaves[count-1].x===worldWidth()-PLAY.x;
        o[d+' includes offscreen positions']=h.stormWaves[0].x<camLeftX()&&h.stormWaves[count-1].x>camRightX();
        const geometry=h.stormWaves.map(q=>[q.x,q.y,q.delay]);
        for(const x of [0,worldWidth()-viewW(),100]){camX=x;hammerStormWaveTick(boss,.001);}
        o[d+' camera cannot relocate row']=JSON.stringify(geometry)===JSON.stringify(h.stormWaves.map(q=>[q.x,q.y,q.delay]));
        let hits=0;playerHit=()=>hits++;player.invuln=0;const q=h.stormWaves[0];player.x=q.x;player.y=q.y;h.hitCd=0;
        q.t=q.split+q.delay+q.warm-1.01;o[d+' no early red zone']=hammerStormRedZone(q)===null;
        q.t+=.02;const zone=hammerStormRedZone(q);o[d+' one second red window']=!!zone&&zone.fire<-.98&&zone.top===q.y-q.height;
        o[d+' full Retina diameter warning']=zone.width===q.retinaWidth;
        const colors=[];for(const age of [.4,1.4,2.4]){q.t=q.split+q.delay+age;colors.push(hammerStormRowAlert(q).key);}
        o[d+' framed warning sign colors']=colors.join(',')===['green','yellow','red'].map(c=>'bmfx_badge_'+c).join(',');
        const alert=hammerStormRowAlert(q);
        o[d+' asterisk clears gauge and world edge']=alert.y>=L23_WARN_MINY&&alert.x-alert.size/2>=PLAY.x;
        q.t=q.split+q.delay+q.warm;o[d+' asterisk ends at eruption']=hammerStormRowAlert(q)===null;
        let safe=true;for(let t=q.warm-1;t<q.warm+hammerStormSpikeTime(q,.14)-.001;t+=.01){q.t=q.split+q.delay+t;safe=safe&&!hammerStormSpikeHits(q,q.x,q.y);}
        o[d+' red warning and initial glow harmless']=safe;
        q.t=q.split+q.delay+q.warm-.1;hammerStormWaveTick(boss,.01);o[d+' warning harmless']=hits===0;
        q.t=q.split+q.delay+q.warm+.4;player.y=q.y-q.height*.8;hammerStormWaveTick(boss,.01);o[d+' tall shaft damaging']=hits===1&&q.started;
        player.y=q.y-q.height-5;h.hitCd=0;hammerStormWaveTick(boss,.01);o[d+' above visible tip safe']=hits===1;
        q.t=q.split+q.delay+q.warm+hammerStormSpikeTime(q,.20);player.y=q.y-q.height*.8;hammerStormWaveTick(boss,.001);o[d+' not yet risen safe']=hits===1;
        h.hitCd=0;player.x=q.x+q.radius+15;player.y=q.y;const previous=hits;hammerStormWaveTick(boss,.01);o[d+' outside spike safe']=hits===previous;
        q.t=q.split+q.delay+q.warm+1.35;player.x=q.x;hammerStormWaveTick(boss,.01);o[d+' residue harmless']=hits===previous;
        const order=h.stormOrder.join(',');player.invuln=999;boss.x=80;boss.y=350;hammerStormImpact(boss);
        o[d+' new committed order each slam']=h.stormOrder.join(',')!==order;
        const poseFrames=new Set();let maxStep=0,previousPoint={x:boss.x,y:boss.y};
        for(let i=0;i<180;i++){camX=i%60<30?0:worldWidth()-viewW();hammerBossTick(boss,1/60);poseFrames.add(hammerStormPoseFrame(boss));maxStep=Math.max(maxStep,Math.hypot(boss.x-previousPoint.x,boss.y-previousPoint.y));previousPoint={x:boss.x,y:boss.y};}
        o[d+' full authored recovery poses']=[7,8,9,10,11].every(f=>poseFrames.has(f));
        o[d+' return ignores scrolling']=h.stormRecovery.done&&Math.abs(boss.x-worldWidth()/2)<.001&&Math.abs(boss.y-VH*.34)<.001;
        o[d+' smooth return without position snap']=maxStep<7&&h.state==='storm_split';camX=100;
        player.invuln=999;const seen=new Set();for(let i=0;i<2100;i++){seen.add(h.state);hammerBossTick(boss,1/60);}
        o[d+' hammer loop without akimbo']=['storm_idle','storm_warn','storm_slam','storm_split','spin','throw','hammer_catch'].every(x=>seen.has(x))&&!['uzi','enrage','core_orbit','chaingun'].some(x=>seen.has(x));
      }
      o['charge cue each break']=cues===3;
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;diffKey=save.diffKey;DIFF=save.DIFF;powerups=save.powerups;eBullets=save.eBullets;playerHit=save.hit;Audio.SFX.bossWeaponCharge=save.charge;run.stage=save.stage;curStage=save.curStage;camX=save.camX;VIEW_FIT=save.fit;}
  })()`,ctxv));
  for(const [k,v] of Object.entries(out))ok(v,'Archmage storm recovery: '+k);
};
