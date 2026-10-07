module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 if(vm.runInContext('typeof HC1007',ctxv)==='undefined')vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/hardcorps_bosses_1007.js'),'utf8'),ctxv,{filename:'hardcorps_bosses_1007.js'});
 console.log('=== October 7 Hard Corps boss choreography ===');
 const rows=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();debugFight=null;coopOn=false;run.mode='campaign';run.pilot='yuri';
 function setup(stage,kind,mini=true){beginStage(stage);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=null;thaw=null;boss=null;subBoss=null;
  if(mini)spawnSubBoss__inner(kind);else spawnBoss(kind);const b=mini?subBoss:boss;b.enter=false;b._noHit=false;b.x=worldWidth()/2;b.y=b._er26?.home||b.ty||160;b._drawY=b.y;
  if(b._bomber){b._bomber.mode='recover';b._hc1007={clock:0,seq:0,lines:[]};}player.invuln=1e9;return b;}
 for(const diff of ['easy','normal','hard','furious']){
  diffKey=diff;DIFF=DIFFS[diff];const b=setup(5,'spacebomber'),hp=b.hp;
  hc1007BomberSet(b,'cross');const C=b._hc1007.cross;
  out[diff+' cross starts with all four warned rays']=hc1007CrossState(b).rays.length===4&&hc1007CrossState(b).mode==='tell'&&C.warm>=1.4;
  C.age=C.warm+.1;const live=hc1007CrossState(b);out[diff+' four rays are orthogonal']=live.mode==='live'&&live.rays.every((q,i)=>Math.abs(q.angle-live.rays[0].angle-i*Math.PI/2)<1e-8);
  C.age=C.warm+C.on+C.fade+.01;out[diff+' dissolving beam has a fully absent crossing']=hc1007CrossState(b).mode==='gap'&&C.cycle-C.on-C.fade>.8;
  C.age=C.warm+C.duration;out[diff+' rotation ends after one complete revolution']=Math.abs(hc1007CrossState(b).angle-C.angle-TAU)<1e-8;
  hc1007CrossTick(b,0);out[diff+' complete revolution clears its collider']=b._hc1007.cross===null&&b.hp===hp;
  hc1007BomberSet(b,'lances');const target=b._hc1007.lines.map(q=>q.angle);player.x+=99;player.y-=50;hc1007BomberTick(b,.01);
  out[diff+' cannon aim stays committed after pilot moves']=b._hc1007.lines.every((q,i)=>q.angle===target[i]);
  siegeBomberHit(b,1e6,null,null,'laserL');out[diff+' cannon destruction cancels its pending tell']=b._hc1007.lines.every(q=>q.id!=='laserL');
  const e=setup(6,'siegebomber');hc1007BomberSet(e,'flak');const H=e._hc1007;
  out[diff+' flak grid reserves one fixed safe column']=H.flakCount-H.lines.length===1&&H.lines.every(q=>q.id==='core')&&H.warm>=1;
 }
 diffKey='furious';DIFF=DIFFS.furious;const b=setup(4,'stormsovereign',false),H=b._s4war.shield;H.rearming=false;
 out['Sovereign book includes both new authored beats']=er26Book(b).includes('hc-relay1007')&&er26Book(b).includes('hc-cross1007');
 er26Set(b,'hc-cross1007');const p=b._mr27.parts.find(p=>p.id==='lightning'),q=mr27Shape(b,'lightning');mr27Damage(b,p.hp+1,q.x,q.y);hc1007CrossTick(b,.01);
 out['Sovereign lightning destruction cancels all rays']=p.dead&&!b._hc1007.cross;
 const h=setup(8,'heralddeath');h._hd1003.seq=0;hd1003Tell(h);out['Herald preserves its first taught cannon attack']=h._hd1003.attack==='skulls';
 h._hd1003.seq=3;hd1003Tell(h);out['Herald gains eclipse cross after taught attacks']=h._hd1003.attack==='eclipse-cross'&&hc1007CrossState(h).rays.length===4;
 hd1003Break(h,hd1003Part(h,'wingL'));out['Herald missing wing removes its opposite pair']=hc1007CrossState(h).rays.length===2&&hc1007CrossState(h).rays.every(q=>q.id==='wingR');
 h.dead=true;hc1007CrossTick(h,.01);out['Herald death removes cross immediately']=h._hc1007.cross===null;
 return out;
})())`,ctxv));for(const [name,value]of Object.entries(rows))ok(value,name);
};
