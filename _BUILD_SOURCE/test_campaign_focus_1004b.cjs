module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/campaign_focus_1004b.js'),'utf8'),ctxv,{filename:'campaign_focus_1004b.js'});
 console.log('=== Stage 6 / 8 recording follow-up: routes, real exit, articulated combat ===');
 const result=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const out={};ht27Stop();debugFight=null;coopOn=false;run.mode='campaign';diffKey='furious';DIFF=DIFFS.furious;
  const setup=(stage,kind)=>{beginStage(stage);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;stagePlan=[];enemies=[];pBullets=[];eBullets=[];powerups=[];
   if(!kind)return;spawnBoss(kind);const b=boss;b._be=null;b.enter=false;b._noHit=false;b.x=worldWidth()/2;b.y=200;return b;};
  const tap=Input.tapSeat;Input.tapSeat=(seat,k)=>seat===1&&k==='right';let wing=true;
  for(const pilot of PILOTS){run.pilot=pilot.key;setup(6);s6WingInit();s6WingLaunch(8,true);Object.assign(s6Wing,{all:true,fakeDone:true,beats:3,choice:true,choiceT:1});s6WingTick(.02);
   wing=wing&&s6Wing.route==='right'&&s6Wing.ships.filter(q=>q.phase!=='leave').length===4&&!s6Wing.ships.some(q=>q.key===pilot.key);}
  Input.tapSeat=tap;out['route selection retains four allies for all nine pilots']=wing;
  for(const route of ['left','right']){setup(6);s6WingInit();s6Wing.route=route;scLeaveStage({bonus:0,rank:'B'});const saved=Rival24.save();campaign.stageX1004=null;Rival24.load(saved);
   out['unchosen '+route+' route persists as the opposite Stage X fight']=cf4Pending()&&campaign.stageX1004.route===(route==='left'?'right':'left');
   cf4LaunchX();out['Stage X '+route+' branch launches a full encounter']=run.stage===6&&run._gp4StageX===(route==='left'?'right':'left')&&s6Wing.ships.length===4;
   scLeaveStage({bonus:0,rank:'A'});out['Stage X '+route+' victory returns to map and clears only that pending fight']=state===GS.STAGESEL&&campaign.stageX1004.done;
  }
  let b=setup(7,'sludgeemperor');run.weapon=7;run.lives=4;const score=run.score;s7mInit(b);b._s7warden.final={};fr27Exit(b,1/60);
  Object.assign(b._s7mod.frExit,{entry:{gone:true,goneAt:0,t0:0},flame:{t0:0,k:1,fx:1},t:100});fr27Exit(b,1/60);
  out['live Warden exit bypasses results, campaign and cutscene screens']=run.stage===8&&state===GS.WARPENTRY&&!!l78entry;
  out['direct portal keeps loadout, lives, earned rank and score']=run.weapon===7&&run.lives===4&&campaign.rank[7]&&run.score>score;
  run.stage=6;const six=forgeComboRoll().elem;run.stage=8;
  out['Prism is Stage 6; Dark Matter is Stage 8']=six==='prism'&&forgeComboRoll().elem==='dark';
  b=setup(8,'vileexistence');j3Encounter(b,2);b._r30.mode='fight';b.enter=false;b._r30.cd=0;const types=new Set();
  for(let i=0;i<300;i++){r30Tick(b,.05);if(b._r30.attack)types.add(b._r30.attack.type);}
  out['Dracula performs swipes, crush and flanking court before morphing']=['cf4Sweep','cf4Crush','cf4Court'].every(k=>types.has(k));
  out['finale projectiles stay finite']=eBullets.every(q=>Number.isFinite(q.x+q.y+q.vx+q.vy));
  j3Clear(b);j3Mimic(b,5);b._r30.mode='fight';b.enter=false;const D=gd4Create(b,5),h=D.p._hammer;
  const pose=new Set();for(let i=0;i<230;i++){r30Tick(b,.05);pose.add(cf4KnightFrame(h));}
  out['actual Hammer timing selects four generated component poses']=pose.size===4;
  hammerBoomerangStart(D.p);hammerBoomerangRelease(D.p);const sword=fmcRig(b).find(v=>v.p.id==='sword');
  out['returning sword draws at its damaging projectile position']=sword&&Math.hypot(sword.x-h.throw.x,sword.y-h.throw.y)<.001;
  b.parts.find(p=>p.id==='sword').destroyed=true;gd4Tick(b,.02);
  out['destroying sword cancels its projectile and switches to surviving arsenal']=!h.throw&&h.mode==='chaingun';
  return out;
 })())`,ctxv));
 for(const [name,pass]of Object.entries(result))ok(!!pass,name);
};
