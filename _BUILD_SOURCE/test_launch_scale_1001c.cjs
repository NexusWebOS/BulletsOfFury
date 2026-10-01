const fs=require('fs'),path=require('path');
/* 1001c - Mike: "keep it at gameplay scale at all times and not do that or any sudden stops on any levels?
   always remain in motion but just slow down as we get to the intro's". The pixel proof is
   _BUILD_SOURCE/probe_launchscale_1001c.py (real Chromium, the hull's own blits); this drives the launch
   machine in the vm and records every height drawShipSprite is handed and every speed the launch holds. */
module.exports=function(vm,ctxv,ok){
 console.log('=== 1001c. One ship size and no stop from intro to play ===');
 const ROOT=path.join(__dirname,'..');
 const out=JSON.parse(vm.runInContext(`(()=>{const o={};const keep={dss:drawShipSprite,slr:typeof stageLoadReady==='function'?stageLoadReady:null,stage:run.stage,cs:curStage,st:state};
  /* the vm decodes no images, so the load gate would hold the launch for ever; the gate is not what is under test */
  stageLoadReady=function(){return true;};
  try{
   o.poseH=playShipPose().h; o.drawH=SHIP_DRAW_H;
   const sim=function(n){
     run.stage=n; curStage=STAGES[n-1]; beginStage(n); setState(GS.LAUNCH);
     drawLaunch._phase=undefined; drawLaunch._lastT=0;
     const hs=[],sp=[],ph=[]; let errs=0, played=false;
     drawShipSprite=function(x,y,h){hs.push(Math.round(h*10)/10);};
     for(let i=0;i<1600&&!played;i++){
       stateT=(stateT||0)+1/60;
       try{drawLaunch(1/60);}catch(e){errs++;}
       if(state===GS.PLAY)played=true;
       if(drawLaunch._phase){sp.push(drawLaunch._spd);ph.push(drawLaunch._phase);}
     }
     let drop=0;for(let i=1;i<sp.length;i++)drop=Math.max(drop,sp[i-1]-sp[i]);
     const after=sp.filter((v,i)=>ph[i]!=='run'||i>30);
     return {played,errs,hmin:Math.min.apply(null,hs),hmax:Math.max.apply(null,hs),n:hs.length,
       spdMin:Math.min.apply(null,after),spdEnd:sp[sp.length-1],drop:Math.round(drop),phases:Array.from(new Set(ph))};
   };
   o.s2=sim(2); o.s3=sim(3);
  }catch(e){o.err=String(e&&e.stack||e);}
  finally{drawShipSprite=keep.dss;if(keep.slr)stageLoadReady=keep.slr;run.stage=keep.stage;curStage=keep.cs;}
  return JSON.stringify(o);})()`,ctxv));
 ok(!out.err,'1001c: the launch simulation ran'+(out.err?' - '+out.err.slice(0,200):''));
 ok(out.poseH===out.drawH,'1001c: the play pose is the height PLAY draws the hull at ('+out.poseH+' vs SHIP_DRAW_H '+out.drawH+'), not the 76 px that popped at GO');
 for(const k of ['s2','s3']){
  const r=out[k]||{};
  ok(r.played&&r.n>200,'1001c: stage '+k.slice(1)+' launch runs to PLAY in the vm ('+r.n+' ship draws, '+r.errs+' draw errors, phases '+(r.phases||[]).join('>')+')');
  ok(r.hmin===out.drawH&&r.hmax===out.drawH,'1001c: stage '+k.slice(1)+' draws the ship at play size on every launch frame ('+r.hmin+'..'+r.hmax+')');
  ok(r.spdMin>=40,'1001c: stage '+k.slice(1)+' never stops - slowest launch speed '+Math.round(r.spdMin)+' px/s');
  ok(r.spdEnd===40,'1001c: stage '+k.slice(1)+' hands PLAY its own 40 px/s, so GO is not a speed change');
  ok(r.drop<40,'1001c: stage '+k.slice(1)+' slows down, never brakes in a frame (largest one-frame drop '+r.drop+' px/s)');
 }
 const g=fs.readFileSync(path.join(ROOT,'assets/game.js'),'utf8');
 ok(g.indexOf("size=SPACE_SHIP_SIZE;   // play size throughout (1001c)")>0 && g.indexOf('lerp(S.build?118:SPACE_SHIP_SIZE')<0,
   '1001c: stage 5 builds the fighter at its play size - no 118 px craft shrunk to 48 in the countdown');
 ok(g.indexOf("drawShipSprite(x,y,90,'')")<0,'1001c: stage 5 flies the plane at play size, not 90 px');
 ok(g.indexOf("o.py, 38, ''")<0,'1001c: the outbound routes climb out at play size, not 38 px');
 ok(g.indexOf('sh=lerp(6,pose.h,k)')<0,'1001c: the stage 8 rift arrival comes out at play size, not grown from 6 px');
 ok(g.indexOf('shipH=lerp(14,SPACE_SHIP_SIZE,pe)')<0,'1001c: the stage 9 launch holds the space fighter at play size');
 ok(g.indexOf('drawLaunch._spd=lerp(drawLaunch._brkV0,STAGE5_SPACE_CRUISE,_ease(p))')>0,
   '1001c: the space brake eases from the speed it is flying at (it halved 3200 -> 1750 in one frame)');
};
