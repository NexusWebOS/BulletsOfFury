module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 for(const f of ['pilot_feedback_art_0927.js','pilot_feedback_0927.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),ctxv,{filename:f});
 console.log('=== One player emitter, lance colors, ice animation and acceleration ===');
 const result=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const out={};run.stage=1;run.spaceMode=false;run.gravityShipReady=false;gravityMode=null;special=null;run.sonicT=run.dkT=0;run.forge={};run.infusion=null;run.wvars=[];run.pilot='cole';player.dead=player.out=false;player.x=240;player.y=360;
  for(const w of [0,1,2,7]){wm26Releases=[];let pass=true;
   for(let lv=1;lv<=5;lv++){run.weapon=w;run.wlevel=lv;run.wlevels=WEAPONS.map(()=>lv);pBullets=[];wm26Releases=[];pShoot();pass=pass&&wm26Releases.length===1&&wm26Releases[0].x===player.x;
    wm26Tick(.03);pShoot();pass=pass&&wm26Releases.length===1;}
   out['weapon '+w+' has one centered emitter across all five tiers and rapid volleys']=pass;}
  run.pilot='maverick';run.weapon=3;run.wvars[3]='mavhoming';
  for(let lv=1;lv<=5;lv++){run.wlevels[3]=lv;run.wlevel=1;pBullets=[];wm26Releases=[];pShoot();out['lance color tier '+lv+' keeps fixed combat stats']=wm26Releases.length===1&&wm26Releases[0].color===wlvGlow(lv)&&pBullets.length===3&&pBullets.every(b=>b.colorLv===lv&&b.lv===1&&Math.abs(b.dmg-.62)<.001);}
  const p={};pf27ThrustTick(p,.1,0,-1,false);const climb=p._thrustPower;
  out['forward input ramps thrust promptly']=climb>.7&&climb<1;
  pf27ThrustTick(p,.1,0,0,false);out['released movement eases exhaust down']=p._thrustPower>0&&p._thrustPower<climb;
  for(let i=0;i<100;i++)pf27ThrustTick(p,1/60,0,0,false);out['idle returns to ordinary exhaust']=p._thrustPower===0;
  out['twelve unique ice cells with stable root metadata']=PILOT_FEEDBACK_ART.frames.length===12&&new Set(PILOT_FEEDBACK_ART.frames.map(r=>r[0]+','+r[1])).size===12&&PILOT_FEEDBACK_ART.frames.every(r=>r[4]>85&&r[4]<175&&r[5]>450);
  return out;
 })())`,ctxv));
 for(const [name,value]of Object.entries(result))ok(value,name);
};
