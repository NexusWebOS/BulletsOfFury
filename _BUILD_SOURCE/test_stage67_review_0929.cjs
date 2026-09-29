module.exports=function(vm,ctxv,ok){
 /* 0929 - Mike's Stage 6/7 list (assets/stage67_review_0929.js). Behaviour only; the pixel proof is
    _BUILD_SOURCE/probe_s67_0929.py in real Chromium (carrier, ace, escape, warden, triangles, bombers,
    supply, warhive). */
 const fs=require('fs'),path=require('path');
 for(const f of ['mission_art_0929.js','mission_repair_0929.js','stage67_review_0929.js']){
  const probe={'mission_art_0929.js':'MISSION29_ART','mission_repair_0929.js':'MISSION29_BASE','stage67_review_0929.js':'s67LaneBand'}[f];
  if(vm.runInContext('typeof '+probe,ctxv)==='undefined')vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),ctxv,{filename:f});}
 console.log('=== 379. Stage 6/7 review: no enemy triangles, the atomic bomb run, the escape, the Furious Warden ===');
 const result=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={};const realHit=playerHit;playerHit=function(){};
  if(typeof ht27Stop==='function')ht27Stop();debugFight=null;coopOn=false;
  function stage(n,diff){diffKey=diff;DIFF=DIFFS[diff];run.mode='campaign';run.pilot='cole';bossDefeated=false;
    beginStage(n);setState(GS.PLAY);story=null;special=null;enemies=[];eBullets=[];pBullets=[];powerups=[];stagePlan=[];waveIdx=999;spawnClock=9999;}
  /* triangles */
  o['the stage 4/6/7 procedural damage overlays draw nothing']=[drawS4DamageOverlay,drawS6DamageOverlay,drawS7DamageOverlay].every(f=>f.toString().replace(/\\s/g,'')==='function(){}');
  stage(7,'normal');
  const e=spawnEnemy('s7tank',camLeftX()+200,200,{});let cones=0,bands=0;const f=l23FovDraw,g=s67LaneBand;
  l23FovDraw=function(){cones++;return false;};s67LaneBand=function(){bands++;};
  try{combatWarningDraw(e,{x:e.x,y:e.y,ex:e.x,ey:VH,progress:.5,width:30});combatWarningDraw({x:1,y:1,t:0},{x:1,y:1,ex:1,ey:VH,progress:.5,width:30});}catch(_e){}
  l23FovDraw=f;s67LaneBand=g;
  o['an ordinary enemy warning is a straight band, never the cone']=bands===1;
  o['a boss warning keeps the FOV cone']=cones===1;
  /* the escape distance is analytic, monotonic, fast, and ends where the portal waits */
  let prev=-1,mono=true,vmax=0;for(let t=0;t<14;t+=.05){const s=s67EscS(t);if(s<prev-1e-9)mono=false;prev=s;vmax=Math.max(vmax,s67EscV(t));}
  o['the escape flies fast (880 px/s) and never backs up']=mono&&vmax===S67E.VMAX&&S67E.VMAX>=800;
  o['the flight lands exactly on the portal distance']=Math.abs(s67EscS(S67E.ARRIVE+1)-S67E.TOTAL)<1e-6&&s67EscS(S67E.SD)===0;
  /* anchoring moves only what the escape spawned */
  const ex0=explosions.length;explosions.push({x:0,y:100});s67Anchor(()=>explosions.push({x:0,y:100}));s67ShiftAnchored(50);
  o['anchored effects ride the terrain; the rest do not']=explosions[ex0].y===100&&explosions[ex0+1].y===150;explosions.length=ex0;
  /* the Furious Warden */
  spawnBoss('sludgeemperor');bossActive=true;const M=s7mInit(boss);M._mission29IntroDone=true;
  const fur=[];diffKey='furious';M.n=2;for(let i=0;i<12;i++){s7mNext(boss);fur.push(M.mode);}
  o['Furious weaves chaingun, stomp and toxic mortar into the rotation']=['chaingun','stomp','toxic-mortar'].every(m=>fur.includes(m));
  M.n=1;const hard=[];for(let i=0;i<12;i++){s7mNext(boss);hard.push(M.mode);}
  o['Hard never picks them']=!hard.some(m=>['chaingun','stomp','toxic-mortar'].includes(m));
  M.n=2;s7mSet(boss,'chaingun');for(let i=0;i<80;i++)s7mTick(boss,1/60);
  const mg=eBullets.filter(q=>q.kind==='mg'&&q._s7modOwner===boss);
  o['the chaingun fires real mg rounds from the barrels']=mg.length>=10;
  s7mSet(boss,'stomp');let air=0;for(let i=0;i<150;i++){s7mTick(boss,1/60);air=Math.max(air,M.height);if(M.mode!=='stomp')break;}
  o['the stomp hops and ends in the claw swats']=air>60&&M.mode==='swipeL'&&M.warn<.5;
  bossActive=false;boss=null;
  /* stage 6 */
  for(const [d,n] of [['normal',4],['hard',5],['furious',5]]){stage(6,d);s6Opening=null;spawnBoss('warhive');bossActive=true;o['the Warhive launches '+n+' escorts on '+d]=boss._whv.jetN===n;}
  stage(6,'normal');s6Opening=null;s6WingInit();const W=s6Wing;W.boxes=[{key:'axel',x:1,y:1},{key:_pilotKey(),x:1,y:1}];
  s6SupplyTick(W,1/60);
  o['supply boxes are never left on the field; each becomes a random grant']=W.boxes.length===0&&W.s67Grants.length===2;
  o['the stage 7 launch no longer takes the painted gate still']=!(window.BOFCampaignStory&&window.BOFCampaignStory.drawGateLaunch);
  bossActive=false;boss=null;playerHit=realHit;
  return o;
 })())`,ctxv));
 for(const [label,passed]of Object.entries(result))ok(passed,label);
};
