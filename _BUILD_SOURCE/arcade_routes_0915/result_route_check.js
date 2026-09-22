(()=>{
  const saved={run:{...run},state,stateT,curStage,beginStage,tap:Input.tap,
    clear:{...drawStageClear},supplies:supplyScr,mouse:Input.mouse.down};
  try{
    run.mode='arcade';run.stage=1;curStage=STAGES[0];state=GS.STAGECLEAR;stateT=10;
    computeStageResults();drawStageClear._init=true;drawStageClear._stamp=1;
    drawStageClear._pwChars=(drawStageClear._res.pw||'').length;
    const score=run.score+drawStageClear._res.bonus;
    let destination=0;
    beginStage=function(n){destination=n;};
    Input.mouse.down=false;Input.tap=function(k){return k==='enter';};
    drawStageClear(0);
    if(state!==GS.SUPPLIES||destination!==0)return false;
    supplyChoose(supplyRows().find(r=>r.kind==='launch'));
    return destination===2&&run.score===score&&state!==GS.OUTBOUND&&state!==GS.STAGESEL;
  }finally{
    Object.assign(run,saved.run);state=saved.state;stateT=saved.stateT;curStage=saved.curStage;
    beginStage=saved.beginStage;supplyScr=saved.supplies;Input.tap=saved.tap;Input.mouse.down=saved.mouse;
    for(const k of Object.keys(drawStageClear))delete drawStageClear[k];
    Object.assign(drawStageClear,saved.clear);
  }
})()
