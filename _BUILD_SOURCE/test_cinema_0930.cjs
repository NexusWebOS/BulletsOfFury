module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/cinematic_director_0930.js'),'utf8'),ctxv,{filename:'cinematic_director_0930.js'});
 console.log('=== 381. Cinematic mission continuity, individual upgrades, and skippable encounters ===');
 const result=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={},D=BOFCinematicDirector;ht27Stop();debugFight=null;run.mode='campaign';run.pilot='axel';
  for(const pk of PILOTS.map(p=>p.key)){
   for(let stage=1;stage<=9;stage++)o[pk+' stage '+stage+' has nonempty story beats']=D.script(stage,pk).every(b=>b.who&&b.text&&b.text.length<260)&&D.script(stage,pk).length>=3;
   const upgrade=D.upgrade(5,pk),text=upgrade.map(b=>b.text).join(' ');
   o[pk+' has its own upgrade response']=upgrade.some(b=>b.who===pk.toUpperCase())&&upgrade.some(b=>b.who===(pk==='decker'?'COLE':'DECKER'));
   o[pk+' hears the recovered chaingun origin']=text.includes('chaingun we acquired in space');
  }
  o['Freezer and Maverick retain their special loadout briefings']=D.upgrade(1,'freezer').some(b=>b.text.includes('Ice Breath'))&&D.upgrade(1,'maverick').some(b=>b.text.includes('Laser Beam'));
  o['Cole retains his prototype weapon branch']=D.upgrade(5,'cole').some(b=>b.text.includes('prototype gun and Fusion Cannon'));
  o['Yuri Thunder Storm gets a dedicated upgrade explanation']=D.upgrade(4,'yuri').some(b=>b.text.includes('Thunder Storm'));
  const left=D.script(6,'yuri','left').map(b=>b.text).join(' '),right=D.script(6,'yuri','right').map(b=>b.text).join(' ');
  o['Harrier aftermath opens optional Stage X while rebel aftermath closes pursuit']=left.includes('Stage X is optional')&&right.includes('no Stage X pursuit');
  o['lost expansion pilots stay missing, not declared dead']=left.includes('HotWire and Phoenix')&&left.includes('Still missing');
  const words=D.cronos('axel').map(b=>b.text).join(' ');
  o['Cronos identifies himself and the other dimension, offers mercy, targets Earth']=words.includes('Cronos')&&words.includes('another dimension')&&words.includes('will not hurt you')&&words.includes('Your planet')&&words.includes('palm of my hands');
  o['Stage X Nyx dialogue is specific to Nyx']=D.rebelScript('axel','nyx').some(b=>b.who==='NYX')&&!D.rebelScript('axel','nyx').some(b=>b.who==='VOSS');
  let done=0;const before=JSON.stringify({forge:run.forge,lives:run.lives,score:run.score});
  D.play('test',[{who:'AXEL',text:'Hello there.'},{who:'DECKER',text:'Second line.'}],()=>done++,true);
  D.advance();o['first A only reveals current line']=D.current.i===0&&D.current.shown===12;
  D.advance();o['second A moves to exactly next beat']=D.current.i===1&&D.current.shown===0;
  D.finish();D.finish();o['skip callback fires exactly once']=done===1;
  o['dialogue never changes earned weapons, lives or score']=before===JSON.stringify({forge:run.forge,lives:run.lives,score:run.score});
  D.play('cancel',[{who:'AXEL',text:'Aborted.'}],()=>done++,true);D.cancel();o['cancel does not commit a route or reward']=done===1&&!D.active;
  return o;
 })())`,ctxv));
 for(const [n,p]of Object.entries(result))ok(p,n);
};
