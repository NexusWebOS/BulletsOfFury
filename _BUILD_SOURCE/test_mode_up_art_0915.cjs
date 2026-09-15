const fs=require('fs'),path=require('path'),Module=require('module');
const ROOT=path.resolve(__dirname,'..');
const harness=fs.readFileSync(path.join(ROOT,'_BUILD_SOURCE/test_fl.js'),'utf8');
const boot=harness.slice(0,harness.indexOf('/* top-level const/let'));
const test=`
const result=vm.runInContext(\`(()=>{
 const checks=[];const check=(v,n)=>{checks.push({name:n,ok:!!v});if(!v)throw Error(n);};
 check(XART._src.mode_life_up_0915==='assets/game/ui/pickups_0915/life_up_wings.png','Life Up source registered');
 check(XART._src.mode_continue_up_0915==='assets/game/ui/pickups_0915/continue_up.png','Continue Up source registered');
 const oldR=XART.rdy,oldG=XART.get,oldD=ctx.drawImage,calls=[];
 XART.rdy=k=>k==='mode_life_up_0915'||k==='mode_continue_up_0915';
 XART.get=k=>({naturalWidth:442,naturalHeight:546,_key:k});
 ctx.drawImage=(im,x,y,w,h)=>calls.push({key:im._key,x,y,w,h});
 check(drawModeUpPickup({kind:'life',x:120,t:0},150),'Life Up takes dedicated renderer');
 check(drawModeUpPickup({kind:'continueup',x:220,t:0},150),'Continue Up takes dedicated renderer');
 check(calls.length===2&&calls[0].key==='mode_life_up_0915'&&calls[1].key==='mode_continue_up_0915','each pickup uses its own authored plate');
 check(calls.every(c=>c.h>=48&&c.h<=50&&Math.abs(c.w/c.h-442/546)<.001),'both badges share readable proportional pickup scale');
 check(!drawModeUpPickup({kind:'bomb',x:0,t:0},0),'unrelated pickups stay on their existing renderer');
 XART.rdy=oldR;XART.get=oldG;ctx.drawImage=oldD;
 return {passed:checks.length,failed:0,checks};
})()\`,ctxv);console.log(JSON.stringify(result,null,2));`;
const m=new Module(__filename,module);m.filename=__filename;m.paths=module.paths;m._compile(boot+test,__filename);
