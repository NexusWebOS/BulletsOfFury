module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path');for(const n of ['alien_arena_art_1005.js','alien_arena_1005.js','pellet_warnings_1005.js'])
  vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/'+n),'utf8'),c,{filename:n});
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};diffKey='furious';DIFF=DIFFS.furious;run.pilot='cole';run.mode='campaign';coopOn=false;
 beginStage(8);setState(GS.PLAY);story=null;BOFCinematicDirector.cancel();fb2Talk=null;s6Opening=null;player.reset();spawnBoss('vileexistence');
 const b=boss,J=j3State(b),S=b._r30;j3Encounter(b,1);on5FightStart(b);
 out['ghost has eight real destructible modules']=b.parts.length===8&&b.parts.every(p=>p.hp>0);
 out['ghost keeps complete head attached to reactor']=aa5GhostRig(b).filter(v=>v.p.id==='core').length===2;
 out['every ghost module is exposed to Retina']=new Set(retinaBossTargets(b).map(t=>t._retinaId)).size===9;
 const arm=b.parts.find(p=>p.id==='armL'),hp=b.hp;b._lastPart=arm;modularHit(arm.hp+1);
 out['breaking ghost arm breaks attached claw without healing']=arm.destroyed&&b.parts.find(p=>p.id==='clawL').destroyed&&b.hp<hp;
 out['ghost breakup creates opaque spinning debris']=D27_MODULE_DEBRIS.length>=2;
 out['broken limbs are absent from live geometry']=!aa5GhostRig(b).some(v=>['armL','clawL'].includes(v.p.id));
 const head=aa5GhostRig(b).find(v=>v.key===AA5_ART.ghost[1].key);out['disarm never removes ghost head']=!!head;
 S.seq=4;r30Attack(b);out['ghost has physical pincer followup']=S.attack.type==='ghostPinch';S.attack=null;
 b.hp=b.maxhp*.49;r30Tick(b,.01);out['Furious ghost unlocks alternate reactor below half health']=S.aa5Unbound===true;
 j3Encounter(b,2);S.mode='fight';b.enter=false;S.cd=0;const types=[];
 for(let i=0;i<5;i++){S.attack=null;S.cd=0;r30Tick(b,.01);types.push(S.attack?.type);S.attack=null;}
 out['Dracula has five committed Furious signatures before transforming']=J.attacks===5&&types.includes('aa5Void')&&types.filter(t=>t==='cf4Crush').length===2;
 const hp0=b.hp;b.hp-=50;j3Save(b);j3Mimic(b,5);j3Home(b);
 out['arena survives form changes with exact saved host health']=aa5Arena(b)&&b.hp===hp0-50;
 const clock=J.aa5Clock;drawBG(0);drawBG(0);out['render calls do not advance arena clock']=J.aa5Clock===clock;
 beginStage(1);out['alien arena cannot leak into another stage']=!aa5Arena(b);
 const ship={x:100,y:300},p={x:100,y:150,vx:0,vy:5,w:7,h:7};
 out['approaching pellet receives time-to-impact warning']=Math.abs(pw5Impact(p,ship).t-.5)<.001;
 out['receding pellet receives no warning']=pw5Impact({...p,vy:-5},ship)===null;
 out['nearby pellet on a safe parallel lane receives no warning']=pw5Impact({...p,x:155},ship)===null;
 out['dead pellet receives no warning']=pw5Impact({...p,dead:true},ship)===null;
 out['slow ordnance uses its own seconds-based velocity']=Math.abs(pw5Impact({...p,vy:300},ship,1).t-.5)<.001;
 return out;})())`,c));
 for(const [name,v]of Object.entries(out))ok(v,name);
};
