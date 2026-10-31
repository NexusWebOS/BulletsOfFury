/* Asset and actual Canvas2D drawing-path checks. No browser is launched. */
const fs=require('fs'),path=require('path'),vm=require('vm');
const {createCanvas,loadImage}=require('C:/Users/Mike/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@napi-rs/canvas');
async function main(){
const R=process.argv[2]||'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury',O=path.join(R,'_shots/pixellab38');fs.mkdirSync(O,{recursive:true});
const P=JSON.parse(fs.readFileSync(path.join(R,'expansion/topdown/art/pixellab38/manifest.json'))),checks=[],errors=[],captures=[];
function check(name,value){checks.push({name,passed:!!value});if(!value)console.log('FAIL '+name);}
function read(n){return fs.readFileSync(path.join(R,n),'utf8');}
const TD={M:{clamp:(x,a,b)=>Math.max(a,Math.min(b,x)),wrap:x=>Math.atan2(Math.sin(x),Math.cos(x)),fwd:a=>[-Math.sin(a),Math.cos(a)]},AssaultArt:{},Contra34:{frontPose:()=> 'legacy',corePose:()=> 'legacy-core',turretPose:()=> 'legacy-turret',frontShot:()=>false,heliosPose:()=>({key:'legacy-boss'})},Depth35:{attacks:{},role:u=>({rifle:'machine_gunner',heavy:'minigunner',laser:'sniper',rocket:'rocket_launcher',shotgun:'shotgunner',double:'double_barrel',flame:'flamethrower',flyer:'flying_alien',roller:'roller_alien'})[u.kind],attack:()=>{},drawShot:()=>{},drawCover:()=>false},Audio:{play:(cue)=>audio.push(cue)},Escape29:{pose:()=> 'legacy-yuri',step:()=>{}},Base33:{drawForeground:()=>{}},MISSIONS:[{id:3,map:{}}],footPose:()=>({key:'legacy-yuri'}),gosferPose:()=>({key:'legacy-gosfer'}),game:{bastion:{},player:{x:320,y:448},time:1}};
const decoded=new Map();await Promise.all([...new Set(Object.values(P.assets).map(a=>a.file))].map(async f=>decoded.set(f,await loadImage(path.join(R,f)))));
// Native Canvas PNG decoder bridge; the production ART lookup/draw code below
// is unchanged. This is a drawing-path check, not a browser integration claim.
const audio=[];const context={TD,TD_PIXELLAB38_ART:P,TD_ASSAULT_ART:{assets:P.assets,sequences:{}},BOFX:{cells:{},img:{}},location:{search:''},URLSearchParams,console,Image:function(){const cv=createCanvas(1,1);Object.defineProperties(cv,{naturalWidth:{get:()=>cv.width},naturalHeight:{get:()=>cv.height},complete:{get:()=>true},src:{set(v){const im=decoded.get(v.replace(/^\.\.\/\.\.\//,''));if(!im){errors.push('Missing PNG '+v);return;}cv.width=im.width;cv.height=im.height;cv.getContext('2d').drawImage(im,0,0);}}});return cv;},document:{createElement:()=>createCanvas(1,1)}};context.window=context;vm.createContext(context);
function run(code,name){try{return vm.runInContext(code,context,{filename:name});}catch(e){throw new Error(name+': '+e.message);}}
run(read('expansion/topdown/js/art.js'),'art.js');
const infantry=read('expansion/topdown/js/infantry_1013.js');context.PACK=context.TD_ASSAULT_ART;context.direction=()=> 'south';run(infantry.slice(infantry.indexOf('TD.AssaultArt={'),infantry.indexOf('const art=TD.AssaultArt;')),'native AssaultArt.draw');
const depth=read('expansion/topdown/js/depth35.js');context.D=TD.Depth35;run(depth.slice(depth.indexOf('D.profiles='),depth.indexOf('D.role=')),'attack profiles');
run(read('expansion/topdown/js/pixellab38.js'),'pixellab38.js');
const api=TD.PixelLab38,ART=context.ART;
let geometry=true,hard=true,anchors=true,opaque=true,loaded=0;const files=new Map();
for(const [k,m]of Object.entries(P.assets)){
 const g=ART.get(k);if(!g){geometry=false;continue;}loaded++;const r=m.rect||[0,0,...m.size];geometry&&=m.size.every(n=>n%2===0)&&r[0]+r[2]<=g.im.width&&r[1]+r[3]<=g.im.height;
 if(!files.has(m.file)){const c=createCanvas(g.im.width,g.im.height),x=c.getContext('2d');x.drawImage(g.im,0,0);files.set(m.file,x.getImageData(0,0,c.width,c.height));}
 const p=files.get(m.file);for(let y=r[1];y<r[1]+r[3];y++)for(let x=r[0];x<r[0]+r[2];x++){const a=p.data[(y*p.width+x)*4+3];if(a!==0&&a!==255)hard=false;}
 for(const v of Object.values(m.muzzles||{})){if(!p.data[((r[1]+v[1])*p.width+r[0]+v[0])*4+3])opaque=false;}
}
for(const q of Object.values(P.banks))for(const k of q.frames){const m=P.assets[k];anchors&&=m.anchor.join()===(q.origin||m.anchor).join()&&m.drawScale===1;}
check('Every registered PNG decodes through the production ART loader',loaded===Object.keys(P.assets).length);
check('Atlas rectangles stay inside even-sized sheets and cells',geometry);check('Frames have binary alpha',hard);check('All banks use fixed origins and baked display units',anchors);check('Every barrel socket sits on opaque hardware',opaque);
const rows=[];
for(const kind of ['rifle','heavy','laser','rocket','shotgun','double','flame','flyer','roller']){
 const u={kind,x:320,y:338,phase:'peek',duck:0,age:0,attack35:{phase:'wait',t:0}},shots=[];let observed=new Set(),t=0;
 for(let i=0;i<900;i++){
  api.stats.releases=0;TD.Depth35.attack(u,1/60,true,(shot,off,speed,index)=>shots.push({t,frame:P.assets[TD.Contra34.frontPose(u)]?.phase,action:u.action35,index,off,speed,port:api.unitSocket(u,1)}));
  observed.add(u.action35);t+=1/60;if(u.attack35.phase==='recover'&&shots.length)break;
 }
 const d=TD.Depth35.profiles[kind];check(kind+' releases the authored projectile count',shots.length===d.count*d.fan.length);check(kind+' releases forward from the displayed weapon',shots.every(s=>s.port&&Number.isFinite(s.port.x)&&s.action==='fire_forward'));
 if(kind==='shotgun')check('Pump shot occurs on native recoil frame 2',shots[0]?.frame===2);
 if(kind==='double')check('Double barrel fires its two banks on frames 2 and 10',shots[0]?.frame===2&&shots[7]?.frame===10);
 if(kind==='heavy')check('Minigun completes spin-up, native firing and spin-down',observed.has('spin_up')&&observed.has('spin_down'));
 rows.push({kind,u,shots,observed:[...observed]});
}
const interrupted={kind:'heavy',phase:'peek',x:320,y:338,attack35:{phase:'wait',t:0}},cancel=[];
for(let i=0;i<50;i++)TD.Depth35.attack(interrupted,1/60,true,()=>cancel.push(i));const before=cancel.length;
for(let i=0;i<180;i++)TD.Depth35.attack(interrupted,1/60,false,()=>cancel.push(i));check('Interrupted attacks cancel future rounds',cancel.length===before);
const turret={kind:'gun',x:254,y:159,hp:20,cd:0,age:0,flash:0},tshots=[];
for(let i=0;i<90;i++)api.stepTurret(TD.game,turret,1/60,1/60,(G,x,y,k)=>tshots.push({x,y,k,frame:P.assets[TD.Contra34.turretPose(turret)].phase}));
check('Turret releases only two alternating native barrel events',tshots.length===2&&tshots[0].frame===2&&tshots[1].frame===10&&tshots[0].x<tshots[1].x);
turret.hp=0;for(let i=0;i<240;i++)api.stepTurret(TD.game,turret,1/60,1/60,()=>tshots.push({}));check('Destroyed turret cancels queued gunfire',tshots.length===2);
check('Destroyed door cores use the inactive material bank',TD.Contra34.corePose({age:1},{hp:0}).includes('inactive'));
const core=api.bank('door_core_pseudo3d','active');check('Native 80ms material timing is retained',core.fps===12.5&&api.frame(core,.079)===core.frames[0]&&api.frame(core,.08)===core.frames[1]);
const boss=P.assets[api.bank('fire_prism_topdown','prism_lightning','south').frames[0]];check('Prism lightning retains the existing 240-pixel boss body unit',Math.abs(boss.bounds[3]-boss.bounds[1]-240)<12);
const SG=api.bank('shotgunner_pseudo3d','fire');check('Rejected pump reload is absent from the import',!api.bank('shotgunner_pseudo3d','reload'));check('Clipped prism volleys are absent from the import',!Object.keys(P.banks).some(k=>k.includes('prism_volley')));
const cv=createCanvas(960,630),cx=cv.getContext('2d');cx.imageSmoothingEnabled=false;cx.fillStyle='#17222c';cx.fillRect(0,0,960,630);cx.font='14px monospace';
rows.forEach(({kind},i)=>{const u={kind,x:160+i%3*320,y:180+Math.floor(i/3)*210,phase:'peek',action35:'fire_forward',actionT35:kind==='double'?.8:.18};const k=TD.Contra34.frontPose(u);api.blit(cx,k,u.x,u.y,1);cx.fillStyle='#d6e4df';cx.fillText(kind,u.x-75,u.y+26);const q=api.unitSocket(u,1);cx.fillStyle='#63eeab';cx.fillRect(q.x,q.y,2,2);});
fs.writeFileSync(path.join(O,'native-firing.png'),cv.toBuffer('image/png'));captures.push('native-firing.png');
const hit=createCanvas(300,300),hc=hit.getContext('2d'),key=SG.frames[0];function pixels(f){hc.clearRect(0,0,300,300);TD.AssaultArt.draw(hc,key,150,260,{s:1,flash:f});return hc.getImageData(0,0,300,300).data;}const normal=Buffer.from(pixels(0)),white=Buffer.from(pixels(1)),restored=Buffer.from(pixels(0));check('Hit flash changes actual damaged pixels and fully expires',!normal.equals(white)&&normal.equals(restored));
check('Native hatch reaches the fully open frame before the chute',api.hatchDuration===16/12.5&&api.hatchKey({escape29:{phase:'hinge',t:api.hatchDuration}}).endsWith('_15'));
const noImage=ART.get,blocked=SG.frames[0];ART.get=k=>k===blocked?null:noImage(k);check('Incomplete lazy bank preserves the current art fallback',TD.Contra34.frontPose({kind:'shotgun',phase:'peek',action35:'fire_forward',actionT35:0})==='legacy');ART.get=noImage;
check('No image decode or draw errors',errors.length===0);
const inFlight={kind:'rifle',phase:'peek',attack35:{phase:'burst',sent:1},action35:'fire_forward'};TD.Depth35.attack(inFlight,1/60,true,()=>{});check('A bank finishing its lazy load cannot replace an in-flight legacy controller',inFlight.artMode38==='legacy');
const proofDir=path.join(O,'motion-frames');fs.mkdirSync(proofDir,{recursive:true});
const actors=[{kind:'heavy',x:150,y:202,phase:'peek',attack35:{phase:'wait',t:0}},{kind:'double',x:400,y:202,phase:'peek',attack35:{phase:'wait',t:0}}],mount={kind:'gun',x:650,y:128,hp:20,cd:0,age:0,flash:0};
let stopTurret=false;
for(let i=0;i<360;i++){
 for(const u of actors){TD.Depth35.attack(u,1/60,!u.done38,()=>{});if(u.attack35.phase==='recover')u.done38=true;}
 if(!stopTurret){api.stepTurret(TD.game,mount,1/60,1/60,()=>{});if(mount.sent38===2&&!mount.fire38)stopTurret=true;}
 if(i%2)continue;
 const c=createCanvas(768,240),x=c.getContext('2d');x.imageSmoothingEnabled=false;x.fillStyle='#17222c';x.fillRect(0,0,768,240);x.fillStyle='#34414b';x.fillRect(0,203,530,1);x.fillStyle='#d6e4df';x.font='14px monospace';x.fillText('MINIGUN',112,27);x.fillText('DOUBLE BARREL',336,27);x.fillText('WALL TURRET',604,27);
 for(const u of actors){api.blit(x,TD.Contra34.frontPose(u),u.x,u.y,1);api.drawUnitMuzzle(x,u,1);}
 api.blit(x,TD.Contra34.turretPose(mount),mount.x,mount.y,1);api.drawTurretMuzzle(x,mount);
 fs.writeFileSync(path.join(proofDir,String(i/2).padStart(3,'0')+'.png'),c.toBuffer('image/png'));
}
const result={build:P.build,environment:'Node + native Canvas2D; production ART and draw functions. Chromium/browser testing is blocked by Work settings.',passed:checks.filter(x=>x.passed).length,total:checks.length,errors,checks,measurements:{counts:P.counts,attacks:rows.map(({kind,shots,observed})=>({kind,shots,observed})),turret:tshots},captures};
fs.writeFileSync(path.join(O,'verification.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({passed:result.passed,total:result.total,errors}));process.exitCode=result.passed===result.total?0:1;
}
main().catch(e=>{console.error(e.message);process.exitCode=1;});
