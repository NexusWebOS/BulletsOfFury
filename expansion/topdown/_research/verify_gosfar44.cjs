/* Actual modules and native pixels. Browser evidence is recorded separately. */
const h=require('./combat40_fixture.cjs'),fs=require('fs'),path=require('path');
const {env,start,load}=h,TD=env.TD,P=env.TD_GOSFAR43_ART,OUT=h.GROOT+'/_shots/gosfar44';fs.mkdirSync(OUT,{recursive:true});
env.CustomEvent=function(type,options){this.type=type;this.detail=options?.detail;};env.dispatchEvent=()=>true;
const checks=[],cues=[],music=[],frames={};let g;function check(name,v){checks.push({name,passed:!!v});if(!v)console.log('FAIL',name);}function step(n=1){env.TDGAME.step(n);}function dispatch(k,down){for(const f of h.handlers[down?'keydown':'keyup']||[])f({key:k,repeat:false,preventDefault(){}});}async function shot(name){TD.Achievements.queue=[];await h.hydrate();fs.writeFileSync(OUT+'/'+name+'.png',h.cv.toBuffer('image/png'));}
function bodyPixels43(b){const c=env.document.createElement('canvas');c.width=c.height=256;const x=c.getContext('2d');x.translate(128-b.x,248-b.y);b.draw(x);return x.getImageData(0,0,256,256).data;}
async function main(){
 TD.pilot='yuri';TD.Audio.on=false;TD.Audio.play=(k)=>cues.push(k);TD.Audio.playMusic=(k)=>music.push(k);g=start(3);step();
 check('Three original relay objectives retained',g.structures.filter(s=>s.kind==='od_relay').length===3);
 check('Route columns remain outside the new arena',g.structures.filter(s=>s.column36).length===4&&g.structures.filter(s=>s.column36).every(s=>s.y>560));
 check('Arena contains one aligned wall and no extra obstacles',g.structures.filter(s=>s.y<560).every(s=>s.gosfarWall43)&&g.structures.filter(s=>s.gosfarWall43).every(s=>s.y===365));
 const m=TD.MISSIONS.find(m=>m.id===3);check('Boss stays gated behind the relays',!m.canSpawnBoss(g));for(const s of g.structures.filter(s=>s.kind==='od_relay'))TD.hitStructure(g,s,999);step();check('Three relay destructions unlock the encounter',m.canSpawnBoss(g));
 g.player.y=550;g.player.x=540;step();check('Arena entry starts Hotwire hack with hidden boss',g.gosfar43?.phase==='hack'&&g.boss.hidden);g.msgs=[];
 const q=g.gosfar43,b=g.boss;await load(Object.keys(P.assets));
 const wallBank=P.banks.wall,slab=q.wall[1],savedHP=slab.hp;
 check('Every new boss and wall frame is PixelLab-authored',Object.values(P.assets).filter(a=>a.bank.startsWith('gosfar/')||a.bank==='wall').every(a=>a.provider==='PixelLab'));
 check('Tall wall has four distinct registered damage states',wallBank.frames.length===4&&new Set(wallBank.frames).size===4);
 const wa=P.assets[wallBank.frames[0]];check('Tall wall hides the crouched body height',wa.bounds[3]-wa.bounds[1]>=80&&381-wallBank.origin[1]+wa.bounds[1]<411-82);
 check('Six wall modules share flush physical edges',q.wall.every((s,i)=>!i||s.rect.x0===q.wall[i-1].rect.x1));
 function wallPixels(){const c=env.document.createElement('canvas');c.width=100;c.height=140;const x=c.getContext('2d');x.translate(50-slab.x,132-slab.y-slab.type.hh);TD.Depth35.drawCover(x,slab);return x.getImageData(0,0,100,140).data;}
 slab.flash=0;const wNormal=wallPixels();TD.hitStructure(g,slab,1);const wLit=wallPixels();let wallLit=0;for(let i=0;i<wLit.length;i+=4)if(wLit[i]+wLit[i+1]+wLit[i+2]>wNormal[i]+wNormal[i+1]+wNormal[i+2]+100)wallLit++;check('Tall authored wall visibly flashes on real damage',wallLit>200&&slab.flash>0);slab.hp=savedHP;slab.flash=0;
 let prev=q.phase,earlyDamage=false,locked=true;for(let i=0;i<3200&&q.phase!=='combat';i++){
  dispatch('j',true);dispatch('d',true);const hp=b.hp; b.hit(b.x,b.y-65,3,10);earlyDamage||=b.hp!==hp;step();locked&&=g.player.scripted||q.phase==='combat';
  if(q.phase!==prev){await shot('phase-'+prev);prev=q.phase;}
 }
 dispatch('j',false);dispatch('d',false);step();check('Every cinematic phase locks input until rally completes',locked&&!earlyDamage&&q.controlReleased&&!g.player.scripted);
 check('Boss music starts exactly at the health-bar reveal',music.filter(k=>k==='gosfar43').length===1&&q.log.find(x=>x.phase==='bar').at>q.log.find(x=>x.phase==='spotted').at);
 check('Alarm clears and power restores before the taunt',q.power&&q.alarm===0&&q.log.find(x=>x.phase==='taunt').at>q.log.find(x=>x.phase==='entrance').at);
 check('Opening volley contains more than 500 real projectiles',q.shots>=500);
 check('Five wall slabs destroyed, permanent Hotwire cover survives',q.wall.filter(s=>s.dead).length===5&&q.wall[0].hp===Infinity&&!q.wall[0].dead);
 check('Destroyed slabs remove physical collisions',q.wall.filter(s=>s.dead).every(s=>s.rect.dead&&!TD.World.solidAt(s.x,s.y)));
 const permanent=q.wall[0];TD.hitStructure(g,permanent,1e8);check('Hotwire wall cannot be destroyed by combat',!permanent.dead&&permanent.hp===Infinity);
 check('Hotwire remains left and Yuri right at release',q.hot.x<250&&g.player.x>450&&q.hot.y===411);
 check('Crew crouches outside the wall footprint',!TD.World.solidAt(q.hot.x,q.hot.y)&&!TD.World.solidAt(g.player.x,g.player.y));
 check('First controllable window is an overheated recovery',b.state==='overheat'&&b.hp===b.max);
 const x=g.player.x;dispatch('d',true);step(12);dispatch('d',false);step();check('Actual movement resumes after overheat call',g.player.x>x+5);
 const hp=b.hp;b.flash=0;const normal=bodyPixels43(b);b.hit(b.x,b.y-65,3,10);const bright=bodyPixels43(b);let lit=0;for(let i=0;i<bright.length;i+=4)if(bright[i]+bright[i+1]+bright[i+2]>normal[i]+normal[i+1]+normal[i+2]+100)lit++;check('Real authored boss pixels brighten when damaged',lit>200);check('Boss damage and visible flash enable after reveal',b.hp===hp-10&&b.flash>0);await shot('combat-hit');step(12);check('Boss flash expires without palette pulsing',b.flash===0);
 g.player.inv=999999;let bullets=0,states=new Set();for(let i=0;i<700;i++){g.player.inv=99999;step();states.add(b.state);bullets=Math.max(bullets,q.shots);}
 check('Combat alternates movement, rev, fire and overheat', ['move','windup','shoot','overheat'].every(s=>states.has(s))&&bullets>528);
 check('Hotwire throws multiple collectable weapons',q.throws>=2&&g.pickups.some(s=>s.kind==='flamethrower')&&g.pickups.some(s=>s.kind==='cryo_lance'));
 b.hp=b.max*.49;step();check('Half health summons four real flamethrower helpers',g.units.filter(u=>u.reinforcement39&&u.kind35==='flame').length===4);
 const enemy=g.units.find(u=>u.reinforcement39),oldHealth=g.units.map(u=>u.hp);Object.assign(enemy,{x:96,y:280,hp:3});let seenFire=false;for(let i=0;i<120;i++){g.player.inv=99999;step();seenFire||=q.hot.action==='fire';}check('Hotwire pistol fires travelling rounds and damages flamers',seenFire&&(q.helpKills>0||g.units.some((u,i)=>u.hp<oldHealth[i]&&u!==enemy)||enemy.hp<3));await shot('hotwire-support');
 const saved={x:b.x,y:b.y,px:g.player.x,py:g.player.y};
 for(const [dir,bx,by,px,py]of [['south',400,260,400,480],['east',400,260,650,260],['west',400,260,150,260],['north',400,400,400,180]]){b.x=bx;b.y=by;g.player.x=px;g.player.y=py;b.state='shoot';b.actionT=0;b.sent=0;b.target={x:px,y:py};b.tick(1/60);const z=TD.gosferPose(b),socket=TD.gosferSocket(b),round=g.eshots.at(-1);check('Gosfar '+dir+' uses its generated minigun firing bank',z.dir===dir&&z.bank==='gosfar/fire'+(dir==='south'?'':'/'+dir));check('Gosfar '+dir+' projectile starts at the drawn muzzle',round&&Math.hypot(round.x-socket.x,round.y-round.liftStart-socket.y)<.01);}
 Object.assign(b,{x:saved.x,y:saved.y,state:'overheat',actionT:0});Object.assign(g.player,{x:saved.px,y:saved.py});g.eshots=[];
 check('All new cue routes resolve to media files', [...new Set(cues)].every(k=>{const a=TD.Audio.sounds[TD.Audio.resolve(k)];return a&&fs.existsSync(path.join(h.GROOT,a.file));}));
 const oldLives=g.lives,oldPhaseCount=q.log.length;g.playerDied();step(115);check('Death respawns Yuri in the live arena without replaying the hack',!g.player.dead&&g.lives===oldLives-1&&q.log.length===oldPhaseCount&&q.phase==='combat'&&g.player.y>400);g.player.inv=99999;
 b.hit(b.x,b.y-65,4,99999);check('Boss death starts protected shared escape',b.dead&&q.phase==='victory'&&!g.escape29);let reached=false,corpseGone=true;for(let i=0;i<1000&&g.state!=='clear';i++){step();if(['exit','close'].includes(q.phase))corpseGone&&=b.deathT>=2.3&&b.flash===0; if(q.phase==='close')reached=g.player.y<170&&q.hot.y<170;}check('Both characters reach elevator before doors close',reached);check('Boss remains faded throughout elevator exit',corpseGone);check('Elevator fade reaches actual Overdrive stats',g.state==='clear'&&!!g.results&&!g.escape29);await shot('stats');
 for(const [name,bank] of Object.entries(P.banks)){check(name+' fixed even canvas and root',bank.size.every(n=>n%2===0)&&bank.frames.every(k=>P.assets[k].anchor.join()===bank.origin.join()&&P.assets[k].size.join()===bank.size.join()));if(bank.frames.length>1){const im=env.ART.get(bank.frames[0]);check(name+' uses authored frame rectangles',new Set(bank.frames.map(k=>P.assets[k].rect.join())).size===bank.frames.length&&!!im);}}
 g=start(7);step();check('Switching levels cleans the encounter owner',g.gosfar43===null);g=start(6);step();check('Truck mission still starts on foot with three companions',g.night39.phase==='onfoot'&&g.night39.crew.length===3);
 const report={build:TD.Gosfar43.build,passed:checks.filter(c=>c.passed).length,failed:checks.filter(c=>!c.passed).length,checks,phases:q.log,cues:[...new Set(cues)],shots:q.shots};fs.writeFileSync(OUT+'/native-report.json',JSON.stringify(report,null,2));console.log(JSON.stringify({passed:report.passed,failed:report.failed}));if(report.failed)process.exitCode=1;
}
main().catch(e=>{console.error(e);process.exitCode=1;});
