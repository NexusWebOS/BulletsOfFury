// ===== 302. GREEN PAUSE MENU AND VERIFIED AUTOSAVE, 0914 =====
console.log('=== 302. green pause menu and verified autosave ===');
{
 var pause302=JSON.parse(vm.runInContext(`(function(){
  var oldState=state,oldP=playPause,oldMusic=Audio.getVol('music'),oldCur=Snd.cur,oldMode=run.mode;
  Snd.cur={volume:0};Audio.setVol('music',.60);state=GS.PLAY;setState('paused');
  var o={music:Audio.getVol('music'),volume:Snd.cur.volume,duck:pauseMusicDuck(),sel:playPause.sel,master:Audio.getVol('master')};
  playPause.t=1;Input.injectTap('arrowdown');drawPaused(1/60);o.down=playPause.sel;
  Input.injectTap('backspace');drawPaused(1/60);o.backState=state;
  playPauseChoose(3);o.options=playPause.mode;optApply();o.optionsBack=state+'/'+playPause.mode;
  playPauseChoose(4);o.help=playPause.mode;setState(GS.TITLE);o.helpBack=state+'/'+playPause.mode;
  playPauseChoose(0);o.resume=state;o.resumedMusic=Audio.getVol('music');o.resumedDuck=pauseMusicDuck();
  Snd.cur=oldCur;Audio.setVol('music',oldMusic);state=oldState;playPause=oldP;run.mode=oldMode;Input.clearTaps();
  return JSON.stringify(o);
 })()`,ctxv));
 ok(pause302.sel===0&&pause302.down===1,'pause defaults to the top resume row and keyboard navigation selects the next action');
 ok(pause302.music===.60&&pause302.duck===.28&&Math.abs(pause302.volume-.60*.28*pause302.master)<1e-6,'paused music is quieter without changing its saved preference');
 ok(pause302.backState==='paused','Backspace cannot escape the pause menu into the title');
 ok(pause302.options==='options'&&pause302.optionsBack==='paused/root','applying real Options returns to the frozen fight menu');
 ok(pause302.help==='help'&&pause302.helpBack==='paused/root','real Help back routes to pause rather than abandoning the stage');
 ok(pause302.resume==='play'&&pause302.resumedMusic===.60&&pause302.resumedDuck===1,'resume removes the temporary duck while retaining the selected music volume');
 var save302=JSON.parse(vm.runInContext(`(function(){
  var get=localStorage.getItem,set=localStorage.setItem,clear=localStorage.clear,oldMode=run.mode,oldSession=campSession,oldP=playPause;
  var store={bof_campaign_slot0:'manual-save'};localStorage.getItem=k=>store[k]||null;localStorage.setItem=(k,v)=>store[k]=String(v);localStorage.clear=()=>{store={};};
  run.mode='campaign';playPauseBegin();var s=playPauseSave(),written=JSON.parse(store[s.name]),manual=store.bof_campaign_slot0;
  campSession=null;var can=campCanContinue(),loaded=campSession&&campSession.stage===written.stage;
  bofStorageResetKeepSaves();var kept=store[s.name]&&store.bof_campaign_slot0===manual;
  localStorage.setItem=()=>{throw new Error('quota');};var failed=playPauseSave();
  localStorage.getItem=get;localStorage.setItem=set;localStorage.clear=clear;run.mode=oldMode;campSession=oldSession;playPause=oldP;
  return JSON.stringify({ok:s.ok,name:s.name,pilot:written.pilot,manual,can,loaded,kept:!!kept,failed:failed.ok});
 })()`,ctxv));
 ok(save302.ok&&save302.name==='Autosav01.json'&&save302.pilot,'campaign autosave serializes and reads back a real named JSON record');
 ok(save302.manual==='manual-save','autosave uses separate records and preserves an existing manual slot');
 ok(save302.can&&save302.loaded,'Continue can recover the latest verified campaign autosave after the session is lost');
 ok(save302.kept,'controls reset preserves new autosave data together with manual saves');
 ok(!save302.failed,'failed storage cannot be advertised as a successful autosave');
}
