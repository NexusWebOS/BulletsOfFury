const fs=require('fs'),path=require('path'),Module=require('module');
const ROOT=path.resolve(__dirname,'..');
const harness=fs.readFileSync(path.join(ROOT,'_BUILD_SOURCE/test_fl.js'),'utf8');
const boot=harness.slice(0,harness.indexOf('/* top-level const/let'));
const test=`
const result=vm.runInContext(\`(()=>{
 const checks=[];const check=(v,n)=>{checks.push({name:n,ok:!!v});if(!v)throw Error(n);};
 const tiers=['super','ultra','uber'];
 for(const tier of tiers){
  check(XART._src['missile_'+tier+'_icon_0915']==='assets/game/ui/missile_tiers_0915/'+tier+'_icon.png',tier+' upgrade icon registered');
  check(XART._src['missile_'+tier+'_box_0915']==='assets/game/ui/missile_tiers_0915/'+tier+'_box.png',tier+' missile box registered');
 }
 const oldR=XART.rdy,oldG=XART.get,oldD=ctx.drawImage,calls=[];
 XART.rdy=k=>/^missile_(super|ultra|uber)_(icon|box)_0915$/.test(k);
 XART.get=k=>({naturalWidth:k.includes('_box_')?300:260,naturalHeight:k.includes('_box_')?290:330,_key:k});
 ctx.drawImage=(im,x,y,w,h)=>calls.push({key:im._key,x,y,w,h});
 for(const tier of tiers)check(drawMissileTierPickup({kind:'missileup_'+tier,x:100,t:1},150),tier+' icon uses dedicated renderer');
 for(const tier of tiers)check(drawMissileTierPickup({kind:'missileupbox_'+tier,x:100,t:1},150),tier+' box uses dedicated renderer');
 check(calls.length===6&&new Set(calls.map(c=>c.key)).size===6,'all six art files render independently');
 const ih=calls.slice(0,3).map(c=>c.h),bh=calls.slice(3).map(c=>c.h);
 check(ih[0]<ih[1]&&ih[1]<ih[2]&&bh[0]<bh[1]&&bh[1]<bh[2],'Super Ultra Uber scale rises in both families');
 check(!drawMissileTierPickup({kind:'missilepack10',x:0,t:0},0),'quantity missile boxes retain their existing renderer');
 XART.rdy=oldR;XART.get=oldG;ctx.drawImage=oldD;
 return {passed:checks.length,failed:0,checks};
})()\`,ctxv);console.log(JSON.stringify(result,null,2));`;
const m=new Module(__filename,module);m.filename=__filename;m.paths=module.paths;m._compile(boot+test,__filename);
