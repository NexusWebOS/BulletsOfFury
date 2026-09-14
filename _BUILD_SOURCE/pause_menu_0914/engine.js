/* Mike 0914 pause rule: monochrome playfield, quiet music, green menu.
 * Menu/options/help never advance combat. Backspace cannot abandon a level.
 * Saved music preference is independent of the temporary pause duck.
 */
const PLAY_PAUSE_ROWS=['RESUME','RETURN TO MAIN MENU','RESTART LEVEL','OPTIONS','HELP','QUIT GAME'];
let playPause=null;
function pauseMusicDuck(){return state==='paused'?.28:1;}
function playPauseBegin(){playPause={sel:0,mode:'root',t:0,shown:0,msg:'',mouseDown:!!Input.mouse.down};}
function playPauseSubmenuReturn(){
  if(playPause){playPause.mode='root';playPause.t=.85;}
  Input.clearTaps();return true;
}
function playPauseSave(){
  if(run.mode!=='campaign')return {ok:true,name:null};
  try{
    campSuspend();const snap=Object.assign(campSnapshot(),{mode:'campaign'}),i=(Number(localStorage.getItem('bof_autosave_next'))||0)%3,
      name='Autosav0'+(i+1)+'.json',bytes=JSON.stringify(snap);
    localStorage.setItem(name,bytes);
    if(localStorage.getItem(name)!==bytes)throw new Error('Autosave verification failed');
    localStorage.setItem('bof_autosave_latest',name);
    localStorage.setItem('bof_autosave_next',String((i+1)%3));
    return {ok:true,name};
  }catch(_){return {ok:false,name:null};}
}
function playPauseExit(quit){
  const save=playPauseSave();
  if(!save.ok){playPause.msg='AUTOSAVE FAILED - TRY AGAIN';return;}
  playPause.exit={quit,save,t:0,over:false};playPause.mode='exit';Input.clearTaps();
  endSpecial();run.shield=0;player.invuln=0;
  if(!player.dead)playerHit();
}
function playPauseChoose(index){
  if(!playPause)return;
  if(Audio.SFX.select)Audio.SFX.select();
  if(index===0){setState(GS.PLAY);playPause=null;}
  else if(index===1||index===5)playPauseExit(index===5);
  else if(index===2){
    const n=run.stage;setState(GS.PLAY);playPause=null;beginStage(n);player.reset();setState(GS.PLAY);
    if(Audio.startMusic)Audio.startMusic(curStage.music);
  }else{
    playPause.mode=index===3?'options':'help';Input.clearTaps();
    if(index===3){optSnap=null;optSelIdx=0;optScroll=0;optSnapshot();}
    else{helpPage=0;helpT=0;}
  }
}
function playPauseExitTick(dt){
  const E=playPause.exit;E.t+=dt;updateDeathSpin(dt);updateEffects(dt);player.deathT-=dt;
  if(player.deathT<=0){
    E.t=0;E.over=true;setState(GS.GAMEOVER);Audio.stopMusic();Snd.loopStopAll();
    if(Audio.SFX.gameover)Audio.SFX.gameover();
  }
}
function playPauseGameOverDraw(dt){
  const E=playPause.exit;E.t+=dt;drawWorld(0);
  ctx.fillStyle='rgba(20,0,0,.75)';ctx.fillRect(0,0,VW,VH);
  msgText('GAME OVER',VW/2,VH/2-20,32,null,0,1,.10);
  campText('SCORE '+pad(run.score,8),VW/2,VH/2+20,13,'#ffd36b');
  if(E.save.name)campText(E.save.name+' SAVED',VW/2,34,12,'#2aff5a');
  if(!E.overVoice&&E.t>=2.1){E.overVoice=true;if(Audio.SFX.over)Audio.SFX.over();}
  if(E.t>4.4){ctx.fillStyle='rgba(0,0,0,'+clamp((E.t-4.4)/.8,0,1)+')';ctx.fillRect(0,0,VW,VH);}
  Input.clearTaps();
  if(E.t>=5.2){const quit=E.quit;playPause=null;player._spin=null;if(quit)tryExit();else{setState(GS.TITLE);menuIndex=0;}}
}
function playPauseWorldDraw(){
  drawWorld(0);
  if(!playPause)playPauseBegin();
  const P=playPause,screen=document.getElementById('screen');
  if(!P.frame){P.frame=document.createElement('canvas');P.frame.width=screen.width;P.frame.height=screen.height;}
  const g=P.frame.getContext('2d');g.clearRect(0,0,P.frame.width,P.frame.height);g.drawImage(screen,0,0);
  ctx.save();ctx.filter='grayscale(1) brightness(.82)';ctx.drawImage(P.frame,0,0,VW,VH);ctx.restore();
}
function playPauseDraw(dt){
  dt=Number.isFinite(dt)?dt:1/60;if(!playPause)playPauseBegin();
  const P=playPause;
  if(P.mode==='exit'){playPauseExitTick(dt);return;}
  if(P.mode!=='root'){
    if(Input.menuBack()){if(P.mode==='options')optCancel();else playPauseSubmenuReturn();return;}
    if(P.mode==='options')drawOptions(0);else drawHelp(0);
    return;
  }
  Input.tap('backspace');P.t+=dt;
  const keys=[];
  for(const seat of [1,2])for(const k of keybindFor(seat).start||[])if(k!=='enter')keys.push(k);
  if(keys.some(k=>Input.tap(k))){playPauseChoose(0);return;}
  if(P.t>.25){
    let change=0;if(Input.menuDown())change=1;if(Input.menuUp())change=-1;
    if(change){P.sel=(P.sel+change+PLAY_PAUSE_ROWS.length)%PLAY_PAUSE_ROWS.length;if(Audio.SFX.blip)Audio.SFX.blip();}
  }
  ctx.fillStyle='rgba(0,0,0,.56)';ctx.fillRect(0,0,VW,VH);
  msgText('PAUSED',VW/2,58,28,'#2aff5a',0,1,.12);
  const w=Math.min(300,VW-96),h=34,gap=48,y0=126,m=Input.mouse;
  for(let i=0;i<PLAY_PAUSE_ROWS.length;i++){
    const k=clamp((P.t-i*.085)/.28,0,1);if(k<=0)continue;
    if(i>=P.shown){P.shown=i+1;if(Audio.SFX.blip)Audio.SFX.blip();}
    const y=y0+i*gap-(1-k)*(1-k)*VH*.75,selected=i===P.sel;
    ctx.save();ctx.globalAlpha=k;octFill(VW/2-w/2,y-h/2,w,h,7,selected?'#133623':'#141b19');
    ctx.strokeStyle=selected?'#2aff5a':'#3c5550';ctx.lineWidth=selected?2:1;ctx.strokeRect(VW/2-w/2+4,y-h/2+3,w-8,h-6);
    campText(PLAY_PAUSE_ROWS[i],VW/2,y+4,12,selected?'#dfffe9':'#a0b2a8');
    if(selected)menuSelMark(VW/2,y,w/2,'green');ctx.restore();
    if(k===1&&m.inside&&Math.abs(m.x-VW/2)<=w/2&&Math.abs(m.y-y)<h/2){
      if(Input.consumeMouseMoved())P.sel=i;
      if(m.down&&!P.mouseDown&&P.t>.85){P.sel=i;playPauseChoose(i);return;}
    }
  }
  P.mouseDown=m.down;
  if(P.msg)campText(P.msg,VW/2,VH-25,10,'#ff7474');
  if(P.t>.85&&Input.menuConfirm())playPauseChoose(P.sel);
}
