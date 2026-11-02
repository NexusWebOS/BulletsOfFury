'use strict';
/* Normal ends at the real Chronos defeat. Existing tally/Forge run first;
   verified completion survives a fresh operation in an independent archive.
   1101 (Mike): Easy ends there too. Its clear offers Normal (normal enemy health and fire,
   still Stages 1-5 only), Hard or Furious; only Hard and Furious go past Stage 5. */
const NF100={key:'bof_normal_complete_1031',state:'normal-finale-1031',current:null,resume:null,events:[],
 base:{die:bossDie,leave:scLeaveStage,scene:drawScene,snapshot:campSnapshot,apply:campApply,map:openStageSelect,
 begin:beginStage,fresh:campBeginFresh,start:startRun,readAuto:campReadAuto,label:campAutoLabel,reset:bofStorageResetKeepSaves}};
for(const a of Object.values(NF100_ART.banks))for(const p of a.pages)XART._src[p.key]=p.path;
function nf100Warm(){let ok=true;for(const a of Object.values(NF100_ART.banks))for(const p of a.pages)ok=XART.rdy(p.key)&&ok;return ok;}
function nf100Blit(n,f,x,y){const a=NF100_ART.banks[n];if(!a)return false;f=clamp(f|0,0,a.frames-1);const p=a.pages.find(p=>f>=p.start&&f<p.start+p.frames);if(!p||!XART.rdy(p.key))return false;
 const j=f-p.start;ctx.drawImage(XART.get(p.key),j%a.cols*a.w,Math.floor(j/a.cols)*a.h,a.w,a.h,Math.round(x),Math.round(y),a.w,a.h);return true;}
function nf100Ends(k=diffKey){return k==='easy'||k==='normal';}
function nf100Eligible(){return nf100Ends()&&run.stage===5&&!debugFight&&!run._gp4StageX;}
function nf100Log(event,data={}){NF100.events.push({event,...data});}
function nf100Save(phase,rank){
 if(debugFight)return false;
 if(rank)campaign.rank[5]=rank;
 if(typeof hf23Grant==='function')hf23Grant(5);
 const old=run._normalComplete100,meta={version:1,phase,diff:diffKey,mode:old?.mode||run.mode,completedAt:old?.completedAt||Date.now(),pilot:run.pilot,coop:coopActive(),p2:coopActive()?{pilot:run2.pilot,score:run2.score,lives:run2.lives,weapon:run2.weapon,wlevel:run2.wlevel}:null};
 run._normalComplete100=meta;
 const snap=Object.assign(campSnapshot(),{mode:'campaign',diff:nf100Ends()?diffKey:'normal',stage:5,completed:true,unlockedMax:Math.min(5,campaign.unlockedMax||5),normalComplete100:meta});
 try{const bytes=JSON.stringify(snap);localStorage.setItem(NF100.key,bytes);if(localStorage.getItem(NF100.key)!==bytes)throw Error('completion readback');
  localStorage.setItem(CAMP_AUTO_KEY,bytes);if(localStorage.getItem(CAMP_AUTO_KEY)!==bytes)throw Error('auto readback');
  campSession=snap;nf100Log('saved',{phase,score:run.score,pilot:run.pilot});return true;
 }catch(e){nf100Log('save-failed',{phase,reason:String(e)});return false;}
}
bossDie=function(){const eligible=nf100Eligible()&&boss?._hammer&&!boss.dead;const out=NF100.base.die.apply(this,arguments);
 if(eligible&&boss?.dead){run._normalComplete100={version:1,phase:'defeated',mode:run.mode,completedAt:Date.now(),pilot:run.pilot};run._normalSaved100=nf100Save('defeated');nf100Warm();}return out;};
campSnapshot=function(){const s=NF100.base.snapshot.apply(this,arguments);if(run._normalComplete100&&nf100Ends())s.normalComplete100={...run._normalComplete100};return s;};
campApply=function(s){const out=NF100.base.apply.apply(this,arguments);if(!out)return out;
 const done=s.normalComplete100||(nf100Ends(s.diff)&&s.stage>=6&&s.stage<=8?{version:1,phase:'legacy',mode:'campaign',completedAt:s.t,pilot:s.pilot}:null);
 run._normalComplete100=done?{...done}:null;NF100.resume=done;
 if(done){run.stage=5;run.mode=done.mode||'campaign';coopOn=!!done.coop;if(coopOn&&done.p2){for(const k of ['pilot','score','lives','weapon','wlevel'])if(done.p2[k]!=null)run2[k]=done.p2[k];const i=PILOTS.findIndex(p=>p.key===run2.pilot);if(i>=0)p2Index=i;}}return out;};
campAutoLabel=function(){const a=campReadAuto();return a?.normalComplete100?(a.diff==='easy'?'AUTO  EASY COMPLETE':'AUTO  NORMAL COMPLETE'):NF100.base.label.apply(this,arguments);};
openStageSelect=function(){if(NF100.resume){NF100.resume=null;return nf100Open(false);}return NF100.base.map.apply(this,arguments);};
beginStage=function(n){if(n>=6&&n<=8&&nf100Ends()&&!debugFight&&!run._gp4StageX){nf100Log('normal-stage-blocked',{stage:n,diff:diffKey});return nf100Open(false);}return NF100.base.begin.apply(this,arguments);};
campBeginFresh=function(){NF100.resume=null;run._normalComplete100=null;return NF100.base.fresh.apply(this,arguments);};
startRun=function(){NF100.current=null;NF100.resume=null;run._normalComplete100=null;return NF100.base.start.apply(this,arguments);};
bofStorageResetKeepSaves=function(){let bytes;try{bytes=localStorage.getItem(NF100.key);}catch(_){}const out=NF100.base.reset.apply(this,arguments);if(bytes)try{localStorage.setItem(NF100.key,bytes);}catch(_){}return out;};
scLeaveStage=function(R){if(!nf100Eligible()&&!run._normalComplete100)return NF100.base.leave.apply(this,arguments);
 if(!nf100Ends()||run.stage!==5||debugFight)return NF100.base.leave.apply(this,arguments);
 if(!R._normalSettled100){R._normalSettled100=true;run.score=(run.score|0)+(R.bonus||0);run.lives=clamp(run.lives,0,9);
  if(R.seats){run2.score=(run2.score|0)+(R.seats[1]?.bonus||0);run2.lives=clamp(run2.lives,0,9);}}
 drawStageClear._init=false;drawStageClear._res=null;Audio.stopMusic();run._normalSaved100=nf100Save('settled',R.rank);return nf100Open(true);
};
function nf100Open(flight=true,preview=false){
 if(!preview){BOFCinematicDirector.cancel();storySkip();}
 NF100.current={phase:flight?'flight':'menu',t:0,sel:0,from:diffKey==='easy'?'easy':'normal',preview,pilot:run.pilot,second:coopActive()?run2.pilot:null,mode:run.mode,saved:preview||nf100Save('settled'),md:!!Input.mouse.down};
 nf100Warm();setState(NF100.state);Input.clearTaps();Audio.startMusic(flight?'cinematics':'stageclear');nf100Log('opened',{flight,preview,mode:run.mode,pilot:run.pilot});
}
function nf100Choose(i){const A=NF100.current;if(!A||A.phase!=='menu')return false;
 if(!A.preview&&!nf100Save('settled')){A.saved=false;Audio.SFX.blip();return false;}
 A.saved=true;A.sel=i;A.chosen=nf100Options(A)[i].key;A.phase='fade';A.t=0;Input.clearTaps();Audio.SFX.select();nf100Log('difficulty-chosen',{difficulty:A.chosen});return true;
}
function nf100Text(s,r,size,color){return mw21Text(s,r,size,color);}
// Choice rows: the graphical Pixelmap Fury Strike face, as the main menus use; dim plane when unselected.
function nf100Choice(o,x,y,on,O){
 // One shared size: the largest Fury Strike bank in which every row fits, so rows never differ in height.
 if(typeof pm27Draw==='function'&&pm27Live()){const h=Math.min(...O.map(q=>pm27Fit(q.label,18,372,'fury_strike').height));
  pm27Draw(ctx,o.label,x,y,h,{family:'fury_strike',palette:on?o.pal:'chrome',alpha:on?1:.5});return;}
 ui20Text(ctx,o.label,x,y,14,350,'center',on?o.on:'#9daabb');
}
function nf100Stock(A,k){const D=difficultyForRun(A.mode,k),L=D.startLives,C=D.continues;return L+' LIVES / '+(C<0?'UNLIMITED CONTINUES':C+(C===1?' CONTINUE':' CONTINUES'));}
function nf100Options(A){
 const hard={key:'hard',label:'HARD - THE NEXT CHALLENGE',on:'#ffe098',pal:'gold',tone:'#c1def7',detail:'HIGHER HEALTH BUDGETS. FASTER FIRE AND DENSER WAVES. HARD BOSS PATTERNS. '+nf100Stock(A,'hard')+'. START AGAIN AT STAGE 1.'},
  furious={key:'furious',label:'FURIOUS - THE TRUE WAR',on:'#ffbcb9',pal:'ember',tone:'#ffcbc5',detail:'THE INTENDED BOF EXPERIENCE. FASTER, DENSER ASSAULTS AND UPGRADED BOSS PATTERNS. '+nf100Stock(A,'furious')+'. FINISH THE CAMPAIGN FOR THE TRUE ENDING.'};
 if(A.from!=='easy')return [hard,furious];
 return [{key:'normal',label:'NORMAL - STANDARD FURY',on:'#bfe8ff',pal:'ice',tone:'#d6ecff',detail:'BOSSES AND ENEMIES HAVE NORMAL HEALTH AND FIRING SPEED. '+nf100Stock(A,'normal')+'. STAGES 1-5 ONLY - CLEAR HARD OR FURIOUS TO GO BEYOND STAGE 5.'},hard,furious];
}
function nf100Menu(A){
 nf100Blit('hq',0,0,0);nf100Blit('window',0,12,58);
 const O=nf100Options(A),n=O.length,gap=n>2?28:34,top=n>2?224:234;
 ui20Text(ctx,A.from==='easy'?'EASY COMPLETE':'NORMAL COMPLETE',VW/2,29,20,VW-30,'center','#f5e3a4');
 ui20Text(ctx,'THE WAR IS NOT OVER',VW/2,93,14,342,'center','#ffd47d');
 A.copy=nf100Text("YOU MAY HAVE WON THE BATTLE, BUT YOU DIDN'T WIN THE WAR. ONLY THE STRONGEST WILL MAKE IT TO THE END, COMMANDER. DO YOU HAVE WHAT IT TAKES?",{x:44,y:123,w:392,h:85},13,'#eaf3ff');
 const moved=Input.consumeMouseMoved(),click=Input.mouse.down&&!A.md;A.md=!!Input.mouse.down;
 for(let i=0;i<n;i++){const y=top+i*gap,over=Input.mouse.inside&&Input.mouse.x>=48&&Input.mouse.x<=432&&Math.abs(Input.mouse.y-y)<16;
  if(A.phase==='menu'&&moved&&over)A.sel=i;nf100Choice(O[i],VW/2+4,y,A.sel===i,O);
  if(A.sel===i)drawSelArrow(40,y-4,18,false,'g');if(A.phase==='menu'&&click&&over&&A.t>.35)nf100Choose(i);
 }
 const pick=O[clamp(A.sel,0,n-1)],dy=n>2?16:0;
 A.detail=nf100Text(pick.detail,{x:44,y:298+dy,w:392,h:94-dy},12,pick.tone);
 ui20Text(ctx,A.saved?(A.from==='easy'?'EASY CLEAR AUTO-SAVED':'NORMAL CLEAR AUTO-SAVED'):'SAVE FAILED - CONFIRM TO RETRY',VW/2,419,11,370,'center',A.saved?'#a9f1af':'#ff9090');
 controlHintRow([['pad_dpad','CHOOSE'],['pad_a','NEW RUN']]);
}
function nf100Draw(dt){const A=NF100.current;if(!A)return;A.t+=Math.min(.05,Math.max(0,dt));if(!nf100Warm())return;
 if(A.phase==='flight'){
  const earth=A.t<3.4,u=clamp(earth?A.t/3.4:(A.t-3.4)/3.8,0,1);nf100Blit(earth?'earth':'hq',0,0,0);
  let f,y,x0,x1,y1;
  if(earth){f=Math.floor(u*47);y=400-u*205;x0=A.second?122:176;x1=272;y1=y+18;}
  else{
   // Nose-first from beside the camera up the runway to the hangar apron: ease-out ground run,
   // size from the plate's perspective (horizon ~260, runway centre 285 -> 296).
   const e=1-Math.pow(1-u,3),cy=590-e*272,cx=285+e*11,size=Math.max(14,108*(cy-260)/330),off=A.second?size*.55:0;
   f=clamp(Math.round((108-size)/94*47),0,47);y=cy-48;x0=cx-off-64;x1=cx+off-64;y1=y+size*.18;
  }
  if(A.second)nf100Blit('ship_'+A.second,f,x1,y1);nf100Blit('ship_'+A.pilot,f,x0,y);
  ui20Text(ctx,earth?'CHRONOS DEFEATED':'FURY HQ - EARTH',VW/2,40,18,VW-30,'center','#f0f6ff');
  ui20Text(ctx,'RETURNING HOME',VW/2,462,14,VW-36,'center','#aaddff');
  const edge=earth?Math.min(A.t,3.4-A.t):Math.min(A.t-3.4,7.2-A.t);if(edge<.3)nf100Blit('fade',Math.floor(15*(1-clamp(edge/.3,0,1))),0,0);
  if(A.t>=7.2){A.phase='menu';A.t=0;Input.clearTaps();Audio.startMusic('stageclear');nf100Log('home-arrival');}return;
 }
 nf100Menu(A);
 if(A.phase==='fade'){nf100Blit('fade',Math.min(15,Math.floor(A.t/.65*15)),0,0);if(A.t>=.7){
  diffKey=A.chosen;DIFF=difficultyForRun(A.mode,diffKey);run.mode=A.mode;run.stage=1;run.ngplus=false;run._normalComplete100=null;campSession=null;
  if(coopActive()){coopPick=0;coopP1Index=pilotIndex;}pilotPending=null;pilotSlide=0;pilotRot=0;drawPilot._entered=false;drawPilot._pcFor=null;NF100.current=null;NF100.pilotFade=.65;setState(GS.PILOT);Input.clearTaps();nf100Log('pilot-select',{difficulty:diffKey,mode:run.mode});}return;}
 if(A.t<.35)return;{const n=nf100Options(A).length;if(Input.menuUp()){A.sel=(A.sel+n-1)%n;Audio.SFX.blip();}else if(Input.menuDown()){A.sel=(A.sel+1)%n;Audio.SFX.blip();}}if(Input.menuConfirm())nf100Choose(A.sel);
}
drawScene=function(dt){if(state===NF100.state){window.__bofFrames=(window.__bofFrames||0)+1;nf100Draw(dt);return;}const out=NF100.base.scene.apply(this,arguments);
 if(state===GS.PILOT&&NF100.pilotFade>0){NF100.pilotFade=Math.max(0,NF100.pilotFade-dt);const w=cv.width/SS,h=cv.height/SS;
  // Tile the fixed authored veil to the pilot viewport; never stretch a sprite.
  for(let y=0;y<h;y+=512)for(let x=0;x<w;x+=480)nf100Blit('fade',Math.ceil(15*NF100.pilotFade/.65),x,y);Input.clearTaps();}return out;};
globalThis.BOF_NORMAL_FINALE=NF100;

for(const name of ['menuConfirm','menuBack','menuUp','menuDown','menuLeft','menuRight']){const base=Input[name];if(base)Input[name]=function(){if(state===GS.PILOT&&NF100.pilotFade>0)return false;return base.apply(this,arguments);};}

campReadAuto=function(){const current=NF100.base.readAuto.apply(this,arguments);if(current)return current;try{const s=JSON.parse(localStorage.getItem(NF100.key)||'null');return s?.v===CAMP_SAVE_VER&&s?.normalComplete100?s:null;}catch(_){return null;}};
DIFF_META.normal.desc='STAGES 1-5 / THEN HARD OR FURIOUS';
DIFF_META.easy.desc='STAGES 1-5 / SLOWER ENEMIES / MORE DROPS';
