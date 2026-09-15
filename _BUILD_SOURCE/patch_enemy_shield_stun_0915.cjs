const fs=require('fs'),path=require('path');
const file=path.resolve(__dirname,'../assets/game.js');let src=fs.readFileSync(file,'utf8');
if(src.includes('\r'))throw new Error('assets/game.js must remain LF-only');
if(src.includes('function enemyShieldStunStart(')){console.log('Enemy shield stun patch already applied.');process.exit(0);}
function rep(a,b,n){const c=src.split(a).length-1;if(c!==1)throw new Error(n+' expected once, found '+c);src=src.replace(a,b);}

rep(`function enemyShieldImpact(e,b,F,reflected){
  const a=enemyShieldFacing(e), x=b&&isFinite(b.x)?b.x:e.x+Math.cos(a)*(e.w||30)*0.55,
        y=b&&isFinite(b.y)?b.y:e.y+Math.sin(a)*(e.h||30)*0.55;
  enemyShieldFx.push({x,y,t:0,dur:0.20,base:F.hit,ang:reflected&&b?Math.atan2(b.vy,b.vx):a});
}
function enemyShieldIntercept(e,dmg,b){`,
`function enemyShieldImpact(e,b,F,reflected){
  const a=enemyShieldFacing(e), x=b&&isFinite(b.x)?b.x:e.x+Math.cos(a)*(e.w||30)*0.55,
        y=b&&isFinite(b.y)?b.y:e.y+Math.sin(a)*(e.h||30)*0.55;
  enemyShieldFx.push({x,y,t:0,dur:0.20,base:F.hit,ang:reflected&&b?Math.atan2(b.vy,b.vx):a});
}
/* A broken enemy shield buys a short, readable punish window. The hull itself owns the stun so
   every movement/weapon family pauses through the shared enemy loop. Splash is deliberately
   bounded by radius, damage and target count; a secondary shield can break and stun, but its
   shield-break round is tagged so it cannot start a chain reaction across the whole formation. */
const ENEMY_SHIELD_STUN_DUR=1.15,ENEMY_SHIELD_SPLASH_CAP=6;
function enemyShieldBreakSplash(e,s){
  const radius=clamp(Math.max(e.w||30,e.h||30)*2.15,78,124),base=clamp(Math.ceil((s.max||1)*.18),3,16);
  const near=enemies.filter(q=>q&&q!==e&&!q.dead&&q._dyingT==null&&!isSetPiece(q))
    .map(q=>({q,d:Math.hypot(q.x-e.x,q.y-e.y)})).filter(v=>v.d<=radius).sort((a,b)=>a.d-b.d).slice(0,ENEMY_SHIELD_SPLASH_CAP);
  const old=_dmgBullet;
  try{
    for(const v of near){const fall=.35+.65*(1-v.d/radius),amount=Math.max(2,Math.round(base*fall));
      _dmgBullet={kind:'shieldbreak',_shieldSplash:true,x:v.q.x,y:v.q.y,pierce:true};hitEnemy(v.q,amount);}
  }finally{_dmgBullet=old;}
  return{radius,base,count:near.length};
}
function enemyShieldStunStart(e,s,F,secondary){
  const dir=(((e._order||0)+Math.floor(e.x||0))&1)?-1:1;
  e._eshStun={t:0,dur:ENEMY_SHIELD_STUN_DUR,baseY:e.y,angle:0,dir,base:F?F.hit:0,frenzy:!!s.once};
  if(typeof floatText==='function')floatText(e.x,e.y-Math.max(22,(e.h||30)*.7),'SHIELD BREAK!','#ffe45c');
  for(let i=0;i<4;i++){const a=i*TAU/4,r=Math.max(20,Math.max(e.w||30,e.h||30)*.62);
    enemyShieldFx.push({x:e.x+Math.cos(a)*r,y:e.y+Math.sin(a)*r,t:0,dur:.34,base:F?F.hit:0,ang:a});}
  if(typeof fxBurst==='function')fxBurst(e.x,e.y,Math.max(30,Math.max(e.w||30,e.h||30)*.9),{color:'#9fe9ff',rings:1});
  if(!secondary)enemyShieldBreakSplash(e,s);
}
function enemyShieldStunTick(e,dt){
  const z=e&&e._eshStun;if(!z)return false;z.t+=dt;
  const p=clamp(z.t/z.dur,0,1),ease=p*p*(3-2*p);
  e.y=z.baseY-Math.sin(p*Math.PI)*14;z.angle=z.dir*TAU*1.15*ease;
  if(p>=1){e.y=z.baseY;const frenzy=z.frenzy;delete e._eshStun;if(frenzy&&typeof enemyFrenzyBegin==='function')enemyFrenzyBegin(e);return false;}
  return true;
}
function enemyShieldStunDraw(e){
  const z=e&&e._eshStun;if(!z||typeof XART==='undefined')return;
  const fi=Math.min(2,Math.floor((z.t*15)%3)),key='nes_hit_'+(z.base+fi);if(!XART.rdy(key))return;
  const top=e.y-(e.h||30)*.62,r=Math.max(20,(e.w||30)*.48);
  for(let i=0;i<3;i++){const a=z.t*7+i*TAU/3,x=e.x+Math.cos(a)*r,y=top+Math.sin(a)*6;
    ctx.save();ctx.translate(x,y);ctx.rotate(a);ctx.globalAlpha=.72;ctx.drawImage(XART.get(key),-15,-15,30,30);ctx.restore();}
}
function enemyShieldIntercept(e,dmg,b){`,'shield stun helpers');

rep(`  if(s.energy<=0){
    s.phase='broken'; s.breakT=s.breakDelay; s.animT=0; s.hitT=0;
    if(Audio.SFX.shieldBreakCombat) Audio.SFX.shieldBreakCombat();
    /* ⚠ ONE-WAY. See enemyFrenzyBegin: a \`once\` shield never comes back, so "break the shield
       first" is a real gate rather than a delay, and the hull panics for the rest of its life. */
    if(s.once) enemyFrenzyBegin(e);
  }`,
`  if(s.energy<=0){
    s.phase='broken'; s.breakT=s.breakDelay; s.animT=0; s.hitT=0;
    if(Audio.SFX.shieldBreakCombat) Audio.SFX.shieldBreakCombat();
    /* The stun owns the transition into frenzy. A one-way shield turns the hull red only after
       the dizzy punish window ends, so the two states remain readable instead of overlapping. */
    enemyShieldStunStart(e,s,F,!!(b&&b._shieldSplash));
  }`,'break transition');

rep(`    e.t+=dt;
    if(typeof enemyShieldTick==='function') enemyShieldTick(e,dt);
    if(typeof enemyFrenzyTick==='function') enemyFrenzyTick(e,dt);`,
`    e.t+=dt;
    if(typeof enemyShieldTick==='function') enemyShieldTick(e,dt);
    if(typeof enemyShieldStunTick==='function'&&enemyShieldStunTick(e,dt))continue;
    if(typeof enemyFrenzyTick==='function') enemyFrenzyTick(e,dt);`,'enemy update stun gate');

rep(`function drawEnemy(e){
  /* BAKED DAMAGE STATE FOLLOWS HP`,
`function drawEnemy(e){
  /* Rotate the complete authored hull during shield stun without touching its source art or
     teaching each enemy renderer a separate stun branch. The recursive guard makes every body
     family use the same transform, then the existing shield-impact plates orbit above it. */
  if(e&&e._eshStun&&!e._eshStunPaint&&e._dyingT==null){
    const z=e._eshStun;e._eshStunPaint=1;ctx.save();ctx.translate(e.x,e.y);ctx.rotate(z.angle||0);ctx.translate(-e.x,-e.y);
    try{drawEnemy(e);}finally{ctx.restore();delete e._eshStunPaint;}
    enemyShieldStunDraw(e);return;
  }
  /* BAKED DAMAGE STATE FOLLOWS HP`,'stun draw wrapper');

fs.writeFileSync(file,src,'utf8');console.log('Applied shared enemy shield break stun and bounded splash.');
