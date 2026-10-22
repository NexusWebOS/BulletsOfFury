module.exports=function(vm,ctxv,ok){
 /* 1021b - Boss Mode STATIONS + starter bosses. A looping scene phase used to own the boss for ever, so a
    later phase keyed to HP (or the boss's own phase) could never start; the Charger template's 66% / 33%
    phases depend on the handoff. Real-Chromium proof, editor and engine, with a busted arm:
    _BUILD_SOURCE/probe_stations_1021b.py. */
 console.log('=== 389. Scene phases hand over on HP: a looping track yields to a later hp/phase trigger ===');
 const r=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={}; const b={x:200,y:120,hp:100,maxhp:100,w:160,h:120};
  const K=(x,y)=>({x:x,y:y,t:0.2,hold:0,ease:'linear',actions:[]});
  const def={grid:{cell:32},ownFire:true,zones:[],tracks:[
    {name:'teach',trigger:{type:'start'},mode:'loop',keys:[K(3,3),K(10,3)]},
    {name:'mid',trigger:{type:'hp',hp:0.66},mode:'loop',keys:[K(7,5),K(7,2)]},
    {name:'late',trigger:{type:'hp',hp:0.33},mode:'loop',keys:[K(2,2)]}]};
  sceneAttach(b,def);
  const step=(n)=>{ for(let i=0;i<n;i++) sceneDirectorTick(b,1/60); };
  step(120); o.a=b._scene.track&&b._scene.track.name;
  b.hp=60; step(60); o.b=b._scene.track&&b._scene.track.name;
  b.hp=30; step(60); o.c=b._scene.track&&b._scene.track.name;
  /* a later trigger that was ALREADY true when a track started does not cut it short */
  const b2={x:200,y:120,hp:20,maxhp:100,w:160,h:120};
  sceneAttach(b2,{grid:{cell:32},zones:[],tracks:[{name:'one',trigger:{type:'start'},mode:'loop',keys:[K(3,3),K(10,3)]},{name:'two',trigger:{type:'hp',hp:0.5},mode:'loop',keys:[K(7,5)]}]});
  for(let i=0;i<180;i++) sceneDirectorTick(b2,1/60); o.d=b2._scene.track&&b2._scene.track.name;
  /* a later START track never interrupts (only hp / phase triggers hand over) */
  const b3={x:200,y:120,hp:100,maxhp:100,w:160,h:120};
  sceneAttach(b3,{grid:{cell:32},zones:[],tracks:[{name:'one',trigger:{type:'start'},mode:'loop',keys:[K(3,3),K(10,3)]},{name:'two',trigger:{type:'start'},mode:'loop',keys:[K(7,5)]}]});
  for(let i=0;i<180;i++) sceneDirectorTick(b3,1/60); o.e=b3._scene.track&&b3._scene.track.name;
  return o;})())`,ctxv));
 ok(r.a==='teach','the opening phase loops while HP is full ('+r.a+')');
 ok(r.b==='mid','HP 60%: the looping phase hands over to the 66% phase ('+r.b+')');
 ok(r.c==='late','HP 30%: and on to the 33% phase ('+r.c+')');
 ok(r.d==='one','a trigger already true at the start does not cut the running phase short ('+r.d+')');
 ok(r.e==='one','a later START phase never interrupts a looping one ('+r.e+')');
};
