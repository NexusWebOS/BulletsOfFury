/* Isolated live attack trials with ordinary movement, no shields/evasions/fire. */
BAL7.attackStart=function(c){
 const q=BAL7.q;let dir=[1,0],duration=10;
 if(c.attack==='rift'){
  const C=hc7RiftStart(B);if(!C)throw new Error('Rift did not start');
  player.x=C.x+(c.position==='left'?-100:c.position==='right'?100:0);player.y=C.y+75;dir=[c.position==='left'?-1:1,0];duration=C.tell+C.active+.1;
  q.attackMeta={tell:C.tell,radius:C.radius,active:C.active,force:hammerFurious()?176:hammerHard()?165:148,baseSpeed:playerBaseSpeed()*60};
 }else if(c.attack==='hook'){
  const R=B._rebels,G=rg4Init(B);G.scene=null;G.rescueDone=true;G.releaseAt=G.age+999;
  for(const s of R.ships){s.rg4.cd=999;s.rg4.gunCd=999;s.rg4.act=null;s.rg4.armed=null;s.rg4.supply=null;}
  const rook=R.ships[2];rook.x=worldWidth()/2;rook.y=170;player.x=worldWidth()/2+(c.position==='left'?-150:c.position==='right'?150:0);player.y=VH-110;
  dir=[c.position==='right'?-1:1,0];rg4Attack(rook,R,G,'rookhook');q.attackOwner=rook;duration=4.8;
  if(rook.rg4.act?.kind!=='rookhook')throw new Error('Hook did not start');
  q.attackMeta={tell:rook.rg4.act.warm,commitAt:rook.rg4.act.warm*.46,speed:diffKey==='easy'?410:500};
 }else if(c.attack==='cross'){
  B._bomber.mode='recover';B._hc1007={clock:0,seq:0};hc1007BomberSet(B,'cross');const C=B._hc1007.cross;
  C.age=C.warm+C.on;const L=hc1007CrossState(B).rays[0],a=L.angle,range=c.position==='left'?115:c.position==='right'?195:155;
  dir=[-Math.sin(a),Math.cos(a)];const px=L.x+Math.cos(a)*range,py=L.y+Math.sin(a)*range;
  player.x=px-dir[0]*30;player.y=py-dir[1]*30;q.crossTarget={x:px+dir[0]*30,y:py+dir[1]*30};duration=C.cycle-C.on+.1;
  q.attackMeta={cycle:C.cycle,active:C.on,harmless:C.cycle-C.on,empty:C.cycle-C.on-C.fade-C.rewarn,width:C.width,baseSpeed:playerBaseSpeed()*60,crossingDistance:60};
 }else throw new Error('Unknown attack');
 if(c.positive){
  if(c.attack==='rift'){const C=B._r30.hc7Rift;player.x=C.x;player.y=C.y;}
  if(c.attack==='cross'){B._hc1007.cross.age=B._hc1007.cross.warm+.03;const L=hc1007CrossState(B).rays[0];player.x=L.x+(L.ex-L.x)*.2;player.y=L.y+(L.ey-L.y)*.2;duration=.3;}
 }
 camX=clamp(player.x-VW/2,0,worldWidth()-VW);q.attackStart={x:player.x,y:player.y};q.attackDir=dir;q.attackDuration=duration;q.attackDistance=0;q.c.fire=false;
 player.invuln=0;run.shield=0;eBullets=[];pBullets=[];Input.clearTaps?.();return q.attackMeta;
};
BAL7.step=function(n){const Q=BAL7.q,dt=1/(Q.c.fps||60);
 for(let i=0;i<n&&!Q.done;i++){
  Q.t+=dt;Q.frames++;for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.clearTaps?.();
  const hold=a=>(keybindFor(1)[a]||[]).filter(k=>!k.startsWith('pad_')).forEach(k=>Input.keys[k]=true);
  if(Q.t>=Q.c.reaction&&!player.dead){const [dx,dy]=Q.attackDir;
   if(Q.c.attack!=='cross'||Q.attackDistance<62){if(dx<-.1)hold('left');if(dx>.1)hold('right');if(dy<-.1)hold('up');if(dy>.1)hold('down');}
  }
  updatePlay(dt);if(Q.frames%3===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(dt*3);}
  Q.attackDistance=Math.hypot(player.x-Q.attackStart.x,player.y-Q.attackStart.y);
  if(player.dead){Q.done=true;Q.outcome='hit';}
  if(Q.t>=Q.attackDuration){Q.done=true;Q.outcome='survived';}
  if(Q.c.attack==='rift'){const C=B._r30.hc7Rift;if(C&&Math.hypot(player.x-C.x,player.y-C.y)>C.radius+10&&Q.reachedSafeAt==null)Q.reachedSafeAt=Q.t;}
 }
 return{t:Q.t,done:Q.done,outcome:Q.outcome};
};
