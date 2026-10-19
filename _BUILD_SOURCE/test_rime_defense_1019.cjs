/* Real encounter state and weapon routing under a mocked renderer.
   Native pixel checks are separate: probe_rime_defense_1019.py. */
const fs=require('fs'),path=require('path'),vm=require('vm');
const ROOT=path.resolve(__dirname,'..');
const harness=fs.readFileSync(path.join(__dirname,'test_fl.js'),'utf8');
const boot=harness.slice(0,harness.indexOf("run('assets/asset_paths_1007.js'"));
const html=fs.readFileSync(path.join(ROOT,'index.html'),'utf8');
const scripts=[...html.matchAll(/^<script src="([^"]+)"/gm)].map(m=>m[1].split('?')[0]);
const context=vm.createContext({require,process,__dirname,console,Buffer,setTimeout,clearTimeout});
vm.runInContext(boot+`
 sandbox.URL=URL;sandbox.location={href:'http://127.0.0.1:8794/index.html',search:'',protocol:'http:',origin:'http://127.0.0.1:8794'};
 sandbox.document.querySelector=()=>null;sandbox.document.querySelectorAll=()=>[];
 const originalContext=mkCtx;mkCtx=()=>Object.assign(originalContext(),{getTransform:()=>({a:1,b:0,c:0,d:1,e:0,f:0}),setLineDash:()=>{}});
 const decorate=el=>Object.assign(el,{append:()=>{},setAttribute:()=>{},remove:()=>{},
  classList:el.classList||{add:()=>{},remove:()=>{},toggle:()=>{},contains:()=>false}});
 const originalGet=sandbox.document.getElementById,originalCreate=sandbox.document.createElement;
 sandbox.document.getElementById=id=>decorate(originalGet(id));
 sandbox.document.createElement=tag=>decorate(originalCreate(tag));
 sandbox.CanvasRenderingContext2D=function(){};Object.assign(sandbox.CanvasRenderingContext2D.prototype,mkCtx());
 sandbox.CanvasRenderingContext2D.prototype.getTransform=()=>({a:1,b:0,c:0,d:1,e:0,f:0});
 sandbox.fetch=()=>Promise.resolve({ok:false,json:async()=>({}),text:async()=>''});
 sandbox.__bofFit=()=>false;
 for(const file of ${JSON.stringify(scripts)})run(file,file);
 if(errors.length)throw Error(errors.join('\\n'));
 globalThis.rimeVm=ctxv;
`,Object.assign(context,{URL}),{filename:'rime-bootstrap'});
const game=context.rimeVm;
let passed=0,failed=0;
function check(name,ok,data){console.log((ok?'PASS ':'FAIL ')+name+(ok?'':' '+JSON.stringify(data)));if(ok)passed++;else failed++;}
function read(code){return JSON.parse(vm.runInContext(`JSON.stringify((()=>{${code}})())`,game));}
vm.runInContext(`
 window.rimeFixture=(difficulty='normal',mini=false)=>{
  coopOn=false;run.mode='arcade';run.stage=3;run.pilot='cole';curStage=STAGES[2];diffKey=difficulty;DIFF=DIFFS[diffKey];
  boss=null;subBoss=null;bossActive=subBossActive=false;enemies=[];eBullets=[];pBullets=[];polishLanes=[];
  player.dead=player.out=false;player.x=240;player.y=440;player.invuln=0;playerHit=()=>{};camX=0;groundTargetingReset();
  if(mini)spawnSubBoss__inner('frostcruiser');else spawnBoss('cryospear');
  const b=mini?subBoss:boss;b._be=null;b.enter=b._noHit=false;b._phaseInvuln=0;b.x=240;b.y=b._er26.home;b._drawY=b.y;
  b._er26.engaged=false;mr27Init(b);er26Tick(b,0);return b;
 };
 window.rimeDisarm=b=>{for(const p of b._mr27.parts){p.hp=0;p.dead=true;}er26Tick(b,0);};
`,game);
const timing=[];
module.exports={context:game,read,ROOT};
if(require.main!==module)return;
if(process.argv.includes('--trace')){
 console.log(read(`const b=rimeFixture('normal'),events=[],set=er26Set;
  er26Set=function(b,mode){events.push({mode,stack:new Error().stack});return set.apply(this,arguments);};
  er26Set(b,'rd19-lasers');b._er26.t=b._er26.warm+.02;er26Combat(b,1/60);
  const before={released:b._rd19.beam?.released,mode:b._er26.mode},errors=[];
  for(const name of ['mr27Draw','drawBoss','drawWorld'])try{window[name](name==='mr27Draw'||name==='drawBoss'?b:0);}catch(e){errors.push(name+':'+e.stack);}
  return{before,after:{released:b._rd19.beam?.released,beam:!!b._rd19.beam,mode:b._er26.mode},events,errors};`));
 process.exit(0);
}
for(const diff of ['normal','hard','furious']){
 const result=read(`const o={},b=rimeFixture('${diff}');
  o.form=b._er26.form;o.book=er26Book(b);o.parts=b._mr27.parts.length;
  er26Set(b,'sa14-mg');b._er26.t=b._er26.warm+.02;er26Combat(b,1/60);o.slug=eBullets.filter(q=>q._rd19IceSlug).map(q=>({proof:q._weaponProof,ice:q._coldTracer1002,speed:Math.hypot(q.vx,q.vy)}));
  er26Set(b,'rd19-lasers');const B=b._rd19.beam;o.beamWarm=B.warm;
  b._er26.t=B.warm*.7;er26Combat(b,1/60);o.noEarlyLaser=!B.released;
  b._er26.t=B.warm+.02;er26Combat(b,1/60);const angles=B.angles.slice();player.x+=140;
  for(let i=0;i<12;i++)er26Tick(b,1/60);
  o.beamReleased=B.released;o.beamFixed=B.angles.every((a,i)=>a===angles[i]);o.gunAligned=B.slots.every((s,i)=>Math.abs(mr27Part(b,s==='L'?'gunL':'gunR').rot-(B.angles[i]-Math.PI/2))<1e-6);
  mr27Part(b,'gunL').dead=true;mr27Part(b,'gunL').hp=0;er26Tick(b,1/60);o.brokenGunGone=B.slots.length===1&&B.slots[0]==='R';
  er26Set(b,'rd19-mortars');const c=rd19Cfg();o.mortarWarm=b._er26.warm;
  b._er26.t=b._er26.warm-.01;er26Combat(b,1/60);o.noEarlyMortar=groundTargetingFx.length===0;
  b._er26.t=b._er26.warm+.01;er26Combat(b,1/60);const q=groundTargetingFx[0];o.mortars=groundTargetingFx.length;o.source=JSON.stringify(q.launch)===JSON.stringify(rd19Port(b,q.side));
  o.fixed=!q.track&&!q.lane;o.fall=q.warn;o.radius=q.radius;const pos={x:q.x,y:q.y};player.x+=100;groundTargetingTick(.2);o.noHoming=q.x===pos.x&&q.y===pos.y;
  const hit=playerHit;let hits=0;playerHit=()=>{hits++;};player.x=q.x;player.y=q.y;
  groundTargetingTick(Math.max(0,q.warn-q.t-.02));o.noEarlyDamage=hits===0;groundTargetingTick(.14);o.impactDamage=hits>0;
  q.hitSeats={};hits=0;player.x=q.x+q.radius+3;player.y=q.y;groundTargetingStrikePlayers(q);o.radiusEscape=hits===0;playerHit=hit;
  groundTargetingReset();er26Set(b,'rd19-mortars');b._er26.t=b._er26.warm+.01;er26Combat(b,1/60);b.dead=true;groundTargetingTick(0);o.cancelled=groundTargetingFx.every(q=>q.dead);b.dead=false;
  rimeDisarm(b);o.exposed=b._rd19.exposed;o.finalBook=er26Book(b);const core=mr27Shape(b,'core');o.core=core;o.coreSolid=mr27At(b,core.x,core.y);
  o.multiplier=mr27Damage(b,5,core.x,core.y);
  const hp=b.hp;_lastHitX=core.x;_lastHitY=core.y;_dmgBullet={kind:'mg'};hitBoss(5);_dmgBullet=null;o.nativeCoreLoss=hp-b.hp;
  const targets=retinaBossTargets(b);o.targets=targets.map(t=>({id:t._retinaId,kind:t.kind,x:t.x,y:t.y}));o.criticalTarget=targets.some(t=>t._retinaId==='rd19-core'&&t.x===core.x&&t.y===core.y)&&!targets.includes(b);
  const h=b.hp,t=targets.find(t=>t._retinaId==='rd19-core');t._retinaHit(5);o.lockedLoss=h-b.hp;
  o.openConduit=false;o.physicalHull=false;
  for(let y=core.y+core.h/2+4;y<b.y+b.h*.5;y+=2)if(RD19.base.hull(b,core.x,y)&&!mr27At(b,core.x,y)){o.openConduit=true;o.physicalHull=target17BossContact(b,core.x,y);break;}
  er26Set(b,'rd19-ram');o.ramWarm=b._er26.warm;const home=b.y;
  b._er26.t=b._er26.warm-.02;er26Combat(b,1/60);o.noEarlyRam=Math.abs(b.y-home)<1;
  b._er26.t=b._er26.warm+c.dash;er26Combat(b,1/60);o.ramTravel=b.y-home;
  b._er26.t=b._er26.dur;er26Combat(b,1/60);o.returned=Math.abs(b.y-b._er26.home)<1;
  groundTargetingReset();RD19.events=[];for(let i=0;i<1800;i++)er26Tick(b,1/60);
  o.finalEvents=[...new Set(RD19.events.map(q=>q.event))];o.finite=Number.isFinite(b.x+b.y+b.hp)&&groundTargetingFx.every(q=>Number.isFinite(q.x+q.y));
  return o;`);
 timing.push({diff,laser:result.beamWarm,mortar:result.mortarWarm,fall:result.fall,ram:result.ramWarm});
 check(diff+' preserves ice identity and four native modules',result.form==='ice'&&result.parts===4,result);
 check(diff+' includes MG, ice lasers, missiles, mortars and ice-ball volleys',result.book.length===5&&['sa14-mg','rd19-lasers','sa14-rockets','rd19-mortars','sa14-ice'].every(x=>result.book.includes(x)),result.book);
 check(diff+' real MG bullets carry cold art and native interception protection',result.slug.length>0&&result.slug.every(q=>q.proof&&q.ice&&q.speed>0),result.slug);
 check(diff+' lasers wait through warning, release, hold their angle and keep guns aligned',result.noEarlyLaser&&result.beamReleased&&result.beamFixed&&result.gunAligned,result);
 check(diff+' a broken cannon stops its own laser immediately',result.brokenGunGone,result);
 check(diff+' both permanent shoulder sockets launch after the warning',result.noEarlyMortar&&result.mortars===2&&result.source,result);
 check(diff+' mortar target commits and has a circular escape radius',result.fixed&&result.noHoming&&result.radiusEscape,result);
 check(diff+' mortar cannot damage early but strikes its warned landing point',result.noEarlyDamage&&result.impactDamage,result);
 check(diff+' owner death cancels lingering shoulder attacks',result.cancelled,result);
 check(diff+' disarmament exposes the actual core and switches the attack book',result.exposed&&result.coreSolid==='core'&&result.finalBook.every(x=>['rd19-ram','rd19-mortars'].includes(x)),result);
 check(diff+' ordinary core damage is tripled through native hitBoss',result.multiplier===15&&result.nativeCoreLoss>=14.9,result);
 check(diff+' manual Retina targets the seated core and receives critical damage',result.criticalTarget&&result.lockedLoss>=14.9,result);
 check(diff+' primary shots can pass the retired nose while ramming hull stays solid',result.openConduit&&result.physicalHull,result);
 check(diff+' desperation ram warns, travels, then returns',result.noEarlyRam&&result.ramTravel>45&&result.returned,result);
 check(diff+' a 30-second final phase keeps attacking with finite state',result.finalEvents.includes('ram-release')&&result.finalEvents.includes('mortar-launch')&&result.finite,result);
}
check('Normal, Hard and Furious shorten reaction windows in order',timing.every((r,i)=>!i||['laser','mortar','fall','ram'].every(k=>r[k]<timing[i-1][k])),timing);
const other=read(`const o={};const mini=rimeFixture('furious',true);o.miniBook=JSON.stringify(er26Book(mini))===JSON.stringify(RD19.base.book(mini));o.miniIce=mini._er26.form==='ice'&&!mini._s3Nuclear;
 run.stage=4;curStage=STAGES[3];boss=null;subBoss=null;spawnSubBoss__inner('olivewarden');const b=subBoss;b.enter=b._noHit=false;mr27Init(b);o.wardenBook=JSON.stringify(er26Book(b))===JSON.stringify(RD19.base.book(b));o.wardenParts=b._mr27.parts.length;
 return o;`);
check('Frost Cruiser retains its independent ice encounter',other.miniBook&&other.miniIce,other);
check('Stage 4 Warden and its five weapons keep their own controller',other.wardenBook&&other.wardenParts===5,other);
const routes=read(`const b=rimeFixture(),o={};rimeDisarm(b);const c=mr27Shape(b,'core'),hit=q=>{const hp=b.hp;const n=q();return{count:n,loss:hp-b.hp};};
 o.beam=hit(()=>beamPiercePieces(b,{kind:'beam',x:c.x,top:c.y-80,bot:c.y+150,w:18,dmg:5,lv:2,seat:1}));
 const orb={kind:'orb',_el:'ice',x:c.x,y:c.y,w:30,h:30,dmg:5,lv:2,seat:1},orbExpected=elementalDamageResult(b,'boss',orb,5,c.x,c.y).dmg*3;
 o.orb={...hit(()=>fb10StrikePieces(orb,b,c.x,c.y,18,5,false)),expected:orbExpected};
 o.slug=!!XART._src[RD19_ART.bullet.key];o.sounds=['iceBreathStart','combatOrb0927','iceOrbImpact','enemyHeavyLaser','chargeDash','shieldBreak'].filter(k=>typeof Audio.SFX[k]!=='function');
 return o;`);
check('Player laser beam reaches exactly one critical core through native piece routing',routes.beam.count===1&&routes.beam.loss>=14.9,routes.beam);
check('Player orb reaches one critical core and retains authored elemental resistance',routes.orb.count===1&&Math.abs(routes.orb.loss-routes.orb.expected)<.01&&routes.orb.loss>0,routes.orb);
check('Cold bullet art and all new attack sounds resolve to registered assets',routes.slug&&routes.sounds.length===0,routes);
const out={passed,failed,timing,other,scope:'Mocked-renderer encounter state and native damage routing, not pixel verification'};
fs.writeFileSync(path.join(ROOT,'_shots/rime_defense_1019/state-report.json'),JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify(out));process.exitCode=failed?1:0;
