module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 for(const f of ['original_warnings_1003e.js','herald_art_1003f.js','herald_1003f.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),ctxv,{filename:f});
 console.log('=== October 3f original enemy warnings and modular Herald restoration ===');
 const rows=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const o={};ht27Stop();debugFight=null;coopOn=false;run.mode='campaign';run.pilot='yuri';
 o['Stage 8 restores the archived Herald at its existing halfway gate']=SUBBOSS[8].kind==='heralddeath'&&SUBBOSS[8].afterScroll===1201&&ALTBOSS[8].kind==='heralddeath';
 for(const d of ['easy','normal','hard','furious']){
  diffKey=d;DIFF=DIFFS[d];beginStage(8);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;enemies=[];eBullets=[];boss=null;bossActive=false;spawnSubBoss('heralddeath');const b=subBoss,H=b._hd1003;b.enter=false;b.x=worldWidth()/2;b.y=b.ty;player.x=b.x;player.y=VH-100;
  o[d+' Herald has six separate generated components and the Stage 8 HP floor']=H.parts.length===6&&b.hp===b.maxhp&&b.hp>=MINIBOSS_HP_FLOOR[7]*encounterFloorDifficultyMul(8);
  o[d+' all six live parts have independent Retina targets']=retinaBossTargets(b).length===6;
  H.seq=0;hd1003Tell(b);const lanes=JSON.stringify(H.lanes);player.x+=70;hd1003Tick(b,.05);
  o[d+' warning locks its target instead of chasing the pilot']=JSON.stringify(H.lanes)===lanes;
  const guns=()=>['gunL','gunR'].map(id=>hd1003Part(b,id));
  const restore=()=>{for(const p of guns()){p.dead=false;p.hp=p.maxhp;p.flash=0;p.kick=0;}H.debris=[];H.fx=[];H.flashes=[];eBullets=[];};
  restore();H.seq=0;H.cannonTurn=0;hd1003Tell(b);const lead=H.lanes[0],follow=H.lanes[1],fan=3+H.rank*2;
  hd1003Tick(b,H.warm+.01);
  o[d+' cannon fans release on different beats']=eBullets.filter(q=>q._heraldPart1003===lead.id).length===fan&&!eBullets.some(q=>q._heraldPart1003===follow.id)&&!follow.issued;
  o[d+' fan shots share the warned socket before recoil']=eBullets.every(q=>Math.abs(q.x-lead.x)<.001&&Math.abs(q.y-lead.y)<.001);
  hd1003Tick(b,follow.delay);
  o[d+' second cannon completes its own full warning']=follow.issued&&eBullets.filter(q=>q._heraldPart1003===follow.id).length===fan;
  const other=eBullets.find(q=>q._heraldPart1003===follow.id),foreign={...other,_heraldOwner1003:null};eBullets.push(foreign);
  hd1003Break(b,hd1003Part(b,lead.id));
  o[d+' disarm clears released shots only for that owner']=!eBullets.some(q=>q._heraldOwner1003===b&&q._heraldPart1003===lead.id)&&eBullets.includes(other)&&eBullets.includes(foreign);
  restore();H.seq=0;H.cannonTurn=0;hd1003Tell(b);const waiting=H.lanes[1].id;hd1003Tick(b,H.warm+.01);hd1003Break(b,hd1003Part(b,waiting));hd1003Tick(b,.6);
  o[d+' pending cannon release is cancelled immediately']=!H.lanes.some(L=>L.id===waiting)&&!eBullets.some(q=>q._heraldPart1003===waiting);
  restore();H.seq=0;H.cannonTurn=0;hd1003Tell(b);const first=H.lanes[0].id;H.seq=0;hd1003Tell(b);
  o[d+' successive cannon attacks alternate the leading side']=first!==H.lanes[0].id;
  restore();H.seq=0;hd1003Tell(b);hd1003Tick(b,H.warm+.7);const count=eBullets.length;hd1003Tick(b,.05);
  o[d+' catch-up releases each scheduled fan exactly once']=count===fan*2&&eBullets.length===count;
  restore();for(const p of guns())hd1003Break(b,p);H.mode='rest';H.age=0;H.seq=1;hd1003Tick(b,1.1);
  o[d+' removing both cannons lengthens the punish interval']=H.mode==='rest';hd1003Tick(b,.41);
  restore();H.seq=0;hd1003Tell(b);
  const p=hd1003Part(b,'gunL'),target=retinaBossTargets(b).find(t=>t._retinaId==='herald-gunL'),hp=p.hp,center=hd1003Center(b,p);hitSubBoss(10,center.x,center.y);
  o[d+' cannon impact only flashes and damages that module']=p.hp<hp&&p.flash>0&&hd1003Part(b,'gunR').flash===0;
  hd1003Hit(b,p.hp+1,center.x,center.y,p.id);H.seq=0;hd1003Tell(b);
  o[d+' detached cannon loses collision, target and volley']=p.dead&&target.dead&&!retinaBossTargets(b).includes(target)&&!H.lanes.some(q=>q.id==='gunL')&&H.debris.length===1;
  const wing=hd1003Part(b,'wingL');hd1003Hit(b,wing.hp+1,0,0,wing.id);H.seq=1;hd1003Tell(b);
  o[d+' surviving weapons own the remaining attack lanes']=H.lanes.every(L=>!hd1003Part(b,L.id).dead);
  eBullets.push({_heraldOwner1003:b,_heraldPart1003:'head'});hitSubBoss(b.hp+1);o[d+' core stays killable before every module is removed']=b.dead&&H.mode==='dead';
  o[d+' defeat clears every pending lane and owned bullet']=!H.lanes.length&&!eBullets.some(q=>q._heraldOwner1003===b);
  for(let i=0;i<125;i++)updateSubBoss(1/60);
  o[d+' native death resolves the miniboss gate']=subBoss===null&&subBossDone&&!subBossActive;
 }
 return o;})())`,ctxv));
 for(const [name,pass]of Object.entries(rows))ok(pass,name);
 for(const p of ['assets/game/levels/stage_08/miniboss/herald_1003f/parts.png','assets/game/levels/stage_08/miniboss/herald_1003f/manifest.json','assets/game/shared/effects/contra_fx_1006/boss_signature_fx.png','assets/game/shared/effects/contra_fx_1006/manifest.json'])ok(fs.existsSync(path.join(__dirname,'..',p)),'Herald generated art is packaged: '+p);
};
