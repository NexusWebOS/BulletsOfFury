const fs=require('fs'),path=require('path'),Module=require('module');
const game=path.resolve(__dirname,'../../..'),file=path.join(__dirname,'verify_combat39.cjs');
let src=fs.readFileSync(file,'utf8').replace('env.window=env;','const handlers={};env.addEventListener=(n,f)=>(handlers[n]??=[]).push(f);env.window=env;');
src=src.slice(0,src.indexOf('async function main(){'))+'module.exports={env,start,hydrate,shot,images,wanted,loadImage,BASE,GROOT,cv,handlers};';
const mod=new Module(file,module);mod.filename=file;mod.paths=module.paths;mod._compile(src,file);
const h=mod.exports,{env,start}=h,TD=env.TD;
async function load(keys){for(const k of keys)env.ART.get(k);for(const [file,c]of h.images)if(!c.loaded){try{const im=await h.loadImage(file);c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);c.loaded=true;}catch(e){console.log('LOAD ERROR',file,e.message);}}}
function key(k,down=true){for(const f of h.handlers[down?'keydown':'keyup']||[])f({key:k,repeat:false,preventDefault(){}});TD.Input.update();}
async function main(){
 TD.Audio.on=false;const cues=[];TD.Audio.play=(...a)=>cues.push(a);
 console.log('WORLD',Object.keys(TD.World));
 let g=start(3);await load(Object.keys(env.TD_COMBAT39_ART.assets));
 const ray=TD.World.rayBlock;TD.World.rayBlock=()=>false;const collide=TD.World.collide;TD.World.collide=()=>{};g.structures=[];g.props=[];g.player.x=400;g.player.y=2450;
 key('f');TD.footTick(g.player,g,1/60);console.log('PRONE',g.player.prone,g.player.stance,TD.Input.state.prone,TD.BIND.prone);key('f',false);
 for(const kind of Object.keys(TD.Depth35.profiles)){
  const u=TD.makeUnit('c35_'+kind,400,2250,{a:0});g.units=[u];g.eshots=[];const states={},frames=new Set();let shots=0;
  for(let i=0;i<1800;i++){g.time+=1/60;g.t++;TD.unitTick(u,g,1/60);states[(u.tactic36?.state||'air')+'/'+u.attack35?.phase]=(states[(u.tactic36?.state||'air')+'/'+u.attack35?.phase]||0)+1;frames.add(TD.Depth35.groundPose(u).key);shots+=g.eshots.length;g.eshots=[];}
  console.log('L3',kind,{shots,frames:frames.size,states,at:[u.x,u.y],attack:u.attack35});
 }
 TD.World.rayBlock=ray;TD.World.collide=collide;
 g=start(7);TD.Bastion.wave(g);await load(Object.keys(env.TD_PIXELLAB38_ART.assets));g.player.inv=999999;g.player.hp=g.player.max=999999;g.bastion.battle=0;const counts={},phases={};
 for(let i=0;i<2400;i++){TD.Bastion.step(g,1/60);for(const u of g.units){const k=u.kind+'/'+u.phase+'/'+u.attack35?.phase;phases[k]=(phases[k]||0)+1;}for(const s of g.bastion.enemyShots){if(!s.counted40){s.counted40=true;counts[s.kind]=(counts[s.kind]||0)+1;}}}
 console.log('L4',{counts,phases,turrets:g.bastion.turrets,cues:cues.length});
 await h.shot('playtest40-before-base');
}
if(require.main===module)main().catch(e=>{console.error(e);process.exitCode=1;});
module.exports={...h,load,key};
