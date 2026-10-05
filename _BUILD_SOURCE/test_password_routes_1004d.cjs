module.exports=function(vm,ctxv,ok){
 console.log('=== Thirteen stage and direct-encounter passwords ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={},codes={FURY:1,IRON:2,DAM5:3,STRM:4,ORBT:5,TURB:6,SEWR:7,DETH:8,RIFT9:9,XHARR:6,XREBEL:6,HARR6:6,REBEL6:6};
 ht27Stop();debugFight=null;coopOn=false;diffKey='furious';DIFF=DIFFS.furious;run.pilot='yuri';
 out['exactly thirteen stage/encounter passwords are registered']=Object.keys(PASSWORDS).length===13;
 out['every stage/encounter password fits the actual six-character input']=Object.keys(codes).every(k=>k.length<=6);
 for(const [code,stage]of Object.entries(codes)){setState(GS.PASSWORD);pwInput=code;submitPassword();
  out[code+' selects its starting stage through the real password handler']=state===GS.DIFF&&PENDING_STAGE===stage&&run.mode==='arcade'&&passwordDifficulty;
 }
 for(const [code,kind,x,route]of [['HARR6','warhive',false,'left'],['REBEL6','rebelsquad',false,'right'],['XHARR','warhive',true,'left'],['XREBEL','rebelsquad',true,'right']]){
  setState(GS.PASSWORD);pwInput=code;submitPassword();beginStage(PENDING_STAGE);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;gp4QuickEncounter();
  out[code+' jumps past the level waves to the selected full boss fight']=bossActive&&boss.kind===kind&&subBossDone&&subBossTriggered&&enemies.length===0&&s6Wing.ships.length===4&&s6Wing.route===route;
  out[code+' distinguishes Stage 6 from the Stage X rematch']=x?run._gp4StageX===route:!run._gp4StageX;
  out[code+' consumes its shortcut once']=!GP4.routeReady&&!GP4.route&&!GP4.stage6Only;
 }
 setState(GS.PASSWORD);pwInput='HARR6';submitPassword();pwInput='TURB';submitPassword();beginStage(6);
 out['ordinary TURB clears a previously selected boss shortcut']=!GP4.route&&!GP4.routeReady&&!GP4.stage6Only&&!run._gp4StageX;
 GP4.stage6Only=true;campaign.unlockedMax=7;campaign.stageX1004={route:'right',done:false};cf4LaunchX();
 out['campaign Stage X launch cannot inherit a canceled Stage 6 shortcut']=run._gp4StageX==='right'&&boss.kind==='rebelsquad';
 beginStage(1);setState(GS.TITLE);return out;
})())`,ctxv));
 for(const [name,pass]of Object.entries(out))ok(pass,name);
};
