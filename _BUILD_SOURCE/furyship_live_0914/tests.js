console.log('\n=== 309. Furyship replacement, manual selection and pose contracts ===');
try {
  const saved309=vm.runInContext('furyLegacyShip',ctxv);
  vm.runInContext('furyLegacyShip=false;furyShipWarm();',ctxv);
  const files309=JSON.parse(vm.runInContext('JSON.stringify(FURY_KEYS.flatMap(k=>[XART._src["fury_"+k]].concat(furyTintedKey(k)?[XART._src["fury_"+k+"_blue"]]:[])))',ctxv));
  ok(files309.every(p=>p&&fs.existsSync(path.join(ROOT,p))),'every new flight, component and effect image/mask exists on disk');
  ok(fs.readFileSync(path.join(ROOT,'assets/game/furyship_0914/runtime_base.png')).equals(fs.readFileSync(path.join(ROOT,'assets/game/gravity_mode/furyship_somersault_13.png'))),'level-flight plate is the exact approved somersault frame 13');
  const pitch309=JSON.parse(vm.runInContext('JSON.stringify(Array.from({length:12},(_,i)=>furyShipPose({somer:{t:(i+.1)/12,dur:1}},null)))',ctxv));
  ok(new Set(pitch309.map(p=>p.key)).size===12&&pitch309.every(p=>p.key.startsWith('somersault_')),'a full pitch action selects twelve distinct somersault poses');
  for(const dir of [-1,1]){
    const keys=JSON.parse(vm.runInContext('JSON.stringify(Array.from({length:8},(_,i)=>furyShipPose({roll:{dir:'+dir+',t:(i+.1)/8,dur:1}},null).key))',ctxv));
    ok(new Set(keys).size===8&&keys.every(k=>k.startsWith('roll_')),'the complete roll visits all eight views in direction '+dir);
  }
  ok(vm.runInContext('furyShipPose({roll:{t:.2,dur:1,dir:1},somer:{t:.4,dur:1}},null).key.startsWith("roll_")',ctxv),'roll keeps priority if a restored state contains both evasions');
  const hp309=JSON.parse(vm.runInContext('JSON.stringify(spaceShipHardpoints(240,400,48))',ctxv));
  ok(hp309.laser[0].x===230.25&&hp309.laser[1].x===249.75&&hp309.laser[0].y===392.125,'new laser origins match the approved frame-13 gun mouths');
  vm.runInContext('pwInput="SPCBOY";submitPassword();',ctxv);
  ok(vm.runInContext('furyLegacyShip&&campSnapshot().unlocks.legacySpaceShip',ctxv),'SPCBOY selects the legacy fighter and campaign snapshot persists it');
  const old309=JSON.parse(vm.runInContext('JSON.stringify(spaceShipHardpoints(240,400,48))',ctxv));
  ok(Math.abs(old309.laser[0].x-225.888)<.001,'legacy selection retains its original cannon anchors');
  vm.runInContext('pwInput="SPCBOY";submitPassword();',ctxv);
  ok(vm.runInContext('!furyLegacyShip',ctxv),'repeating SPCBOY restores the replacement without removing old art');
  vm.runInContext('furyLegacyShip='+saved309,ctxv);
} catch(e){ok(false,'Furyship verification threw: '+e.stack);}
