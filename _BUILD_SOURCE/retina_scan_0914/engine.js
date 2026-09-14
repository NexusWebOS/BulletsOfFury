/* Directional Retina Scan upgrade: four independent authored retinas, each with a
   five-second firing window. Manual missile queues never spend passive ammo. */
const RETINA_SCAN_CAP=4,RETINA_SCAN_LIFE=5,RETINA_SCAN_GAP=.05;
function retinaScanState(){
  if(!player._retinaScan)player._retinaScan={marks:[],queue:null};
  return player._retinaScan;
}
function retinaScanClear(){player._retinaScan=null;}
function retinaScanAdd(t){
  if(!run.retinaScan||!retinaTargetValid(t))return false;
  const S=retinaScanState();if(S.queue||S.marks.length>=RETINA_SCAN_CAP||S.marks.some(m=>m.target===t))return false;
  S.marks.push({target:t,phase:'seek',seekT:0,ox:player.x,oy:player.y-10,x:player.x,y:player.y-10,scale:2.2,spin:0,_tick:0,animT:0,lockT:RETINA_SCAN_LIFE});
  if(Audio.SFX.retinaCharge)Audio.SFX.retinaCharge();return true;
}
function retinaScanDirection(dx,dy){
  if(!run.retinaScan||run.bombs<=0||player.dead)return false;
  const S=retinaScanState();if(S.queue)return false;
  if(!S.marks.length&&_seat===1&&retinaTargetValid(retina.target)){retinaScanAdd(retina.target);retina.target=null;retina.phase=null;}
  const candidates=_lockTargets().filter(t=>{
    if(S.marks.some(m=>m.target===t)||t.x<camLeftX()+8||t.x>camRightX()-8)return false;
    const x=t.x-player.x,y=(t._drawY!=null?t._drawY:t.y)-player.y,len=Math.hypot(x,y);
    return len>1&&(x*dx+y*dy)/len>.35;
  });
  candidates.sort((a,b)=>Math.hypot(a.x-player.x,a.y-player.y)-Math.hypot(b.x-player.x,b.y-player.y));
  if(!candidates.length){if(Audio.SFX.hit)Audio.SFX.hit();return false;}
  return retinaScanAdd(candidates[0]);
}
function retinaScanInput(){
  if(!run.retinaScan||player.dead)return;
  const keys=keybindFor(_seat),held=(keys.retina||[]).some(k=>Input.down(k));if(!held)return;
  for(const [name,x,y]of [['left',-1,0],['right',1,0],['up',0,-1],['down',0,1]]){
    if((keys[name]||[]).some(k=>Input.tap(k)))retinaScanDirection(x,y);
  }
}
function retinaScanHeldFire(){
  const S=player._retinaScan,K=keybindFor(_seat);
  if(S&&S.marks.length&&S.marks.every(m=>m.phase==='locked')&&(K.retina||[]).some(k=>Input.down(k))&&[...(K.fire||[]),...(K.bomb||[])].some(k=>Input.down(k)))retinaScanFire();
}
function retinaScanFire(){
  if(!run.retinaScan||player.dead||specialActive('cole')||specialActive('lizzie'))return false;
  const S=retinaScanState();if(S.queue)return true;
  const ready=S.marks.filter(m=>m.phase==='locked'&&m.lockT>0&&retinaTargetValid(m.target));
  if(!ready.length)return S.marks.length>0; // acquiring marks cannot silently spend a free missile
  if(run.bombs<=0){if(Audio.SFX.hit)Audio.SFX.hit();return true;}
  S.queue={targets:ready.map(m=>m.target),next:0};return true;
}
function retinaScanTick(dt){
  const S=player._retinaScan;if(!S)return;
  if(player.dead||!run.retinaScan){retinaScanClear();return;}
  let expired=false,acquired=false;S.cueCd=Math.max(0,(S.cueCd||0)-dt);
  for(const m of S.marks){
    m.animT+=dt;m.spin+=dt*(m.phase==='seek'?14:Math.max(0,m.lockSpin||0));
    if(!retinaTargetValid(m.target)){m.phase=null;continue;}
    const t=m.target,y=t._drawY!=null?t._drawY:t.y;
    if(m.phase==='seek'){
      m.seekT+=dt;const p=clamp(m.seekT/.45,0,1),e=1-Math.pow(1-p,3);
      m.x=lerp(m.ox,t.x,e);m.y=lerp(m.oy,y,e);m.scale=lerp(2.2,1,e);
      if(p>=1){m.phase='locked';m.lockT=RETINA_SCAN_LIFE;m.lockSpin=7;acquired=true;}
    }else if(m.phase==='locked'){
      m.x=t.x;m.y=y;m.lockSpin=Math.max(0,(m.lockSpin||0)-dt*14);m.lockT-=dt;
      if(m.lockT<=0){m.phase=null;expired=true;}
    }
  }
  if(acquired&&S.cueCd<=0){if(Audio.SFX.select)Audio.SFX.select();S.cueCd=.14;}
  S.marks=S.marks.filter(m=>m.phase);
  if(expired&&Audio.SFX.hit)Audio.SFX.hit();
  if(S.queue){
    const Q=S.queue;Q.next-=dt;
    if(Q.next<=1e-9){
      const t=Q.targets.shift();
      if(t&&S.marks.some(m=>m.target===t&&m.phase==='locked'&&m.lockT>0)&&retinaTargetValid(t)&&run.bombs>0){
        const first=pBullets.length;
        if(useBomb(t)){for(let i=first;i<pBullets.length;i++)pBullets[i].seat=_seat;}
      }
      S.marks=S.marks.filter(m=>m.target!==t);Q.next=RETINA_SCAN_GAP;
      if(!Q.targets.length||run.bombs<=0){S.queue=null;S.marks=[];}
    }
  }
}
function drawRetinaScans(){
  for(const seat of seatList())withSeat(seat,()=>{
    const S=player._retinaScan;if(!S)return;const old=retina;
    try{for(const m of S.marks){retina=m;drawRetina();}}
    finally{retina=old;}
  });
}
function retinaScanPickupDraw(p,y){
  const fi=Math.floor((p.t||0)*9)%4,im=retinaTinted('retA',fi,_pilotKey());if(!im)return;
  const w=im.width||im.naturalWidth,h=im.height||im.naturalHeight,scale=42/Math.max(w,h);
  ctx.save();ctx.translate(p.x,y);ctx.rotate((p.t||0)*2.2);ctx.drawImage(im,-w*scale/2,-h*scale/2,w*scale,h*scale);ctx.restore();
}
function retinaScanSupply(p){
  if(p.kind!=='mcrate'||run.stage<2||run.retinaScan||powerups.some(q=>!q.dead&&q.kind==='retinascan'))return;
  powerups.push({x:clamp(p.x+35,camLeftX()+24,camRightX()-24),y:p.y,vy:.7,t:0,kind:'retinascan',w:32,h:32,bob:0});
}
