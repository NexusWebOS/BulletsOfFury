const fs=require('fs'),path=require('path');
/* 1001b - Mike's trailer notes: bomber flash, Falva's box, stage 9 entry/portals/asteroids, the stage 7
   portal run, Stage X's arena and the stage 6 turn. Pixel proof is _BUILD_SOURCE/scene1001.py; these
   pin the state and the source so the fixes cannot be quietly undone. */
module.exports=function(vm,ctxv,ok){
 console.log('=== 1001b. Trailer feedback ===');
 const ROOT=path.join(__dirname,'..');
 let loadErr=null;
 try{vm.runInContext(fs.readFileSync(path.join(ROOT,'assets/feedback_1001b.js'),'utf8'),ctxv,{filename:'feedback_1001b.js'});}
 catch(e){loadErr=String(e&&e.stack||e);}
 ok(!loadErr,'1001b: feedback_1001b.js loads after every other layer'+(loadErr?' - '+loadErr.slice(0,160):''));
 const html=fs.readFileSync(path.join(ROOT,'index.html'),'utf8');
 const iw=html.indexOf('assets/feedback_1001b.js'),ic=html.indexOf('assets/campaign_world_0930.js'),ih=html.indexOf('assets/widescreen_hud_0918.js');
 ok(iw>ic&&iw<ih,'1001b: index.html loads it after the campaign world and before the widescreen HUD');
 const png=f=>{const b=fs.readFileSync(path.join(ROOT,vm.runInContext('bofAssetPath('+JSON.stringify(f)+')',ctxv)));return [b.readUInt32BE(16),b.readUInt32BE(20)];};
 /* Falva: one 256x244 box on every frame (was 256 tall with the next cell's rail, or cut 11/22 rows low) */
 const falva=['idle','anger','crash','happy','laugh','sad','victory','talk-closed','talk-small','talk-medium','talk-wide','talk-o'];
 ok(falva.every(n=>{const s=png('assets/game/pilots_0922/portraits/falva-'+n+'.png');return s[0]===256&&s[1]===244;}),
   '1001b: all twelve Falva portrait frames are the same 256x244 box, with no slice of the next rail under it');
 ok(falva.every(n=>{const s=png('assets/game/pilots_0922/comm/comm_falva_'+n+'.png');return s[0]===128&&s[1]===122;}),
   '1001b: the compact comm set the dialogue box actually draws carries the same repair (128x122, every frame)');
 const out=JSON.parse(vm.runInContext(`(()=>{const o={};const saved={stage:run.stage,wing:typeof s6Wing!=='undefined'?s6Wing:null};
  try{
   o.flashHard=fb1001FlashAlpha({flash:.1})>=.999; o.flashFades=fb1001FlashAlpha({flash:0})<fb1001FlashAlpha({flash:.1});
   o.flashSolid=/xartTint\\(A\\.key,hitFlashColor\\(e,'#ffffff'\\),1\\)/.test(s67CellFlash.toString());
   run.stage=6;s6Wing={route:'left',routeFightT:10};o.left=Math.round(s6TurnOffset());
   s6Wing={route:'right',routeFightT:10};o.right=Math.round(s6TurnOffset());
   s6Wing={route:'left',routeFightT:0};o.start=Math.round(s6TurnOffset());
   s6Wing={route:null};o.none=Math.round(s6TurnOffset());
   o.arenaKey=XART._src.sx1001_arena;
   run._gp4StageX='left';o.arenaWrap=stageXArenaActive();run.stage=5;o.arenaWrap=o.arenaWrap&&!stageXArenaActive();delete run._gp4StageX;run.stage=6;
   const sp=[];for(let t=0;t<=8;t+=.05)sp.push(s7pSpeed(t));
   o.noBrake=sp.every((v,i)=>i===0||v>=sp[i-1]-1e-9); o.fullSpeed=Math.abs(s7pSpeed(S7P.SD+S7P.ACC+.01)-S7P.VMAX)<1e-6;
   o.pilotLine=fr27Exit.toString().indexOf('WHAT IS THIS?! WHAT IS HAPPENING TO ME?!')>=0;
   o.portalBeforeSwallow=S7P.OPEN<S7P.PULL&&S7P.PULL-S7P.SD<3;
   o.astKeys=S9AST_ROCK.concat(S9AST_WET).map(k=>XART._src[k+'_idle']);
   o.gateCloses=stage9PortalEscapeDraw.toString().indexOf('1-p*0.72')<0;
   o.s9clock=/run\\.stage===9\\)\\{ _stage9SpaceScroll \\+= dt\\*STAGE5_SPACE_CRUISE/.test(drawLevelMaster.toString());
  }catch(e){o.err=String(e&&e.stack||e);}finally{run.stage=saved.stage;if(saved.wing!==undefined)s6Wing=saved.wing;}
  return JSON.stringify(o);})()`,ctxv));
 ok(!out.err,'1001b: state checks ran'+(out.err?' - '+out.err.slice(0,200):''));
 ok(out.flashHard&&out.flashFades,'1001b: a bomber hit is a solid silhouette that fades with e.flash');
 ok(out.flashSolid,'1001b: the bomber flash is a FULL hit-colour flood of the plate, not a 74% wash');
 ok(out.left===340&&out.right===-340,'1001b: choosing LEFT slides the stage-6 world +340, RIGHT -340 ('+out.left+'/'+out.right+')');
 ok(out.start===0&&out.none===0,'1001b: the stage-6 turn is still before the choice and at the moment of it');
 ok(out.arenaKey==='assets/game/levels/stage_x/stage/stagex_coast_1004j/terrain.png'&&fs.existsSync(path.join(ROOT,out.arenaKey||'x')),'1001b: Stage X arena plate is registered and on disk');
 ok(out.arenaWrap,'1001b: the Stage X duel draws its own water-plateau arena, not stage 6');
 const a=png(out.arenaKey);
 ok(a[0]===680&&a[1]>=1024,'1001b: the arena plate is 680 wide and tall enough to circle the mountain ('+a.join('x')+')');
 ok(out.noBrake&&out.fullSpeed,'1001b: the stage 7 escape never decelerates once it reaches full speed');
 ok(out.pilotLine,'1001b: the pilot says "WHAT IS THIS?! WHAT IS HAPPENING TO ME?!" as the rift takes them');
 ok(out.portalBeforeSwallow,'1001b: the rift opens mid-flight and the pull follows it without a hold');
 ok(Array.isArray(out.astKeys)&&out.astKeys.length===6&&out.astKeys.every(k=>k&&fs.existsSync(path.join(ROOT,k))),'1001b: six new stage-9 asteroid plates (three clean, three watery) are registered and on disk');
 const gsrc=fs.readFileSync(path.join(ROOT,'assets/game.js'),'utf8');
 ok(/else if\(run\.stage===9\) stage9LaunchBackdropDraw\(drawLaunch\._bgScroll\);/.test(gsrc),'1001b: the stage 9 launch flies over the stage-9 void, not the water connector');
 ok(out.gateCloses,'1001b: the stage 9 exit gate closes instead of lingering at 28% alpha');
 ok(out.s9clock,'1001b: stage 9 scrolls on its own clock at stage 5 cruise speed');
};
