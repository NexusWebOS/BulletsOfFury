/* Compact Genesis-style ground HUD. Boss bars/dialogue retain their owners. */
(function(root){
 'use strict';
 const TD=root.TD,M=TD.M,KEY='bof_od_onfoot_high_score';
 const valid=n=>Number.isFinite(Number(n))?Math.max(0,Math.floor(Number(n))):0;
 let best=0;try{best=valid(localStorage.getItem(KEY));}catch(e){}
 const api=TD.CornerHUD26={last:null,storageKey:KEY};
 api.status=function(G,pseudo){
  const p=G.player;
  if(p.dead)return 'DOWN';
  if(p.reviveT>0)return 'RECOVERING';
  if(p.roll>0)return p.rollFromProne39?'PRONE ROLL':p.rollProne?'ROLL TO PRONE':'ROLLING';
  if(p.jump>0)return 'JUMPING';
  if(p.stunned>0||p.stun>0)return 'STUNNED';
  if(p.throwT>0||p.action==='grenade'||p.action?.kind==='grenade')return 'GRENADE';
  if(p.reload>0)return 'RELOADING';
  if(p.blindfire)return 'BLINDFIRE';
  if(p.quickSide)return 'SIDE FIRE';
  if(p.prone)return p.moving?'CRAWLING':p.cover||pseudo&&TD.Bastion.coverAt(G,p.x)?.hp>0?'WALL PRONE':'PRONE';
  if(p.scripted)return 'STANDOFF';
  if(p.freeAim||TD.Input.down('retina'))return 'FREE AIM';
  if(p.firing>0)return 'FIRING';
  if(p.cover&&!p.peekExposed||pseudo&&p.rise<.35&&TD.Bastion.coverAt(G,p.x)?.hp>0)return 'IN COVER';
  if(p.moving)return p.stance==='crouch'?'CROUCH WALK':'RUNNING';
  return p.stance==='crouch'?'CROUCHING':'READY';
 };
 api.model=function(G,pseudo){
  const p=G.player,gun=p.weapons?.[p.wi||0],ammo=pseudo?(p.groundGun==='rifle'||!p.groundGun?Infinity:p.gunAmmo):gun?.ammo;
  const score=valid(G.score);if(score>best){best=score;try{localStorage.setItem(KEY,String(best));}catch(e){}}
  return{pilot:p.pilot||TD.pilot||'yuri',lives:valid(G.lives),hp:M.clamp(Number(p.hp)||0,0,p.max||1),max:Math.max(1,p.max||1),ammo:ammo===Infinity?'∞':String(valid(ammo)),status:api.status(G,pseudo),score,highScore:best};
 };
 const plate=(ctx,key,x,y)=>TD.AssaultArt.draw(ctx,key,x,y);
 const digits=n=>String(n).padStart(7,'0');
 api.draw=function(ctx,text,G,pseudo){
  const v=api.model(G,pseudo),w=TD.VW,pack=root.TD_CORNER26_ART;ctx.save();ctx.imageSmoothingEnabled=false;
  // Existing selected-pilot portrait is drawn locally; no private source upload.
  plate(ctx,'corner26_portrait',8,8);
  const key='pav_'+v.pilot,g=ART.get(key)||ART.get('pav_yuri');
  if(g){const inset=Math.round(g.sw*.105),side=g.sw-inset*2;ctx.drawImage(g.im,g.sx+inset,g.sy+inset,side,side,14,14,44,44);}
  text('X '+v.lives,68,21,13,'#ffffff');
  plate(ctx,'corner26_health',68,36);
  const fill=pack.fill,frac=v.hp/v.max,fillWidth=Math.floor(fill.w*frac),fillKey=frac<=.3?'corner26_fill_low':'corner26_fill';
  ctx.save();ctx.beginPath();ctx.rect(68+fill.x,36+fill.y,fillWidth,fill.h);ctx.clip();plate(ctx,fillKey,68+fill.x,36+fill.y);ctx.restore();
  const cx=Math.round(w/2),scoreX=cx-51,highX=cx+51;
  text('SCORE',scoreX,14,8,'#ffdd72','center');text(digits(v.score),scoreX,30,11,'#ffffff','center');
  text('HIGH SCORE',highX,14,8,'#ffdd72','center');text(digits(v.highScore),highX,30,11,'#ffffff','center');
  const right=w-8;plate(ctx,'corner26_ammo',right-128,8);
  text('AMMO = '+v.ammo,right-7,21,11,'#ffffff','right');
  text(v.status,right-7,42,8,'#8cffe5','right');
  api.last={...v,healthFillPixels:fillWidth,regions:{left:[8,8,208,56],center:[cx-100,8,200,36],right:[right-128,8,128,48]}};
  ctx.restore();
 };
})(window);
