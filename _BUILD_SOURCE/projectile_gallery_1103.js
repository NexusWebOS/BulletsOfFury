/* Native-browser QA only. Not part of the game build.
   PG3 harvests every distinct projectile the real encounters and weapons fire, then films each one
   through the shipping drawBullets() — one round on an otherwise empty canvas, centred, for a fixed
   number of frames while the real updatePlay() keeps moving, spinning and ageing it. */
window.PG3={caps:{},order:[],live:[],errors:[],N:24,STEP:2,CROP:128,prime:false,ctxStat:null,enc:null};
const PG3_HOOKS=['_v24Kind','_ch23Round','_archBlaster','_hammerLaser','_frostNoseLaser','_rzb','_fzt','_tlv','_tb28','_er26Art',
 '_s4wKind','_s3ThermoArt','_l23fx','_mwKind','_s9a','_chKind','_carrierWarhead','_jcHelix','_heraldProjectile','_bfam','_fx',
 '_cal50','_inf','_ts','_charged','_full','_child','variant','tag','blast','mg','_el','_isBall','_burstVolley','_fire','_ice','pal'];
/* draw-route flags no fixed list knows about yet: later refits (S911, S811, CB112 ...) tag rounds with
   their own short string keys, and those keys pick the art */
const PG3_ROUTE=/kind|art|fam|fx|type|form|variant|pal|elem|el$|skin|look|tier/i;
PG3.sig=function(b,player){
 /* an enemy round belongs to its stage: an `mg` from a Stage 9 water jet is not a Stage 1 jungle `mg` */
 const parts=[player?'P':'E'+(run.stage||0),b.kind];
 for(const k of Object.keys(b)){if(k[0]!=='_'||PG3_HOOKS.includes(k)||!PG3_ROUTE.test(k))continue;const v=b[k];
  if(typeof v==='string'&&v.length<=28)parts.push(k+'='+v);}
 for(const h of PG3_HOOKS){const v=b[h];if(v==null||v===false||v===0||v==='')continue;
  let s=v;if(typeof v==='object')s=v.art||v.id||v.kind||v.name||'obj';if(typeof s==='number')s=Math.round(s*100)/100;
  if(h==='pal'&&!player)continue;parts.push(h+'='+String(s).slice(0,40));}
 if(!player&&b._boss&&typeof _bossProjKey==='function'){try{const k=_bossProjKey(b);if(k)parts.push('boss='+String(k).replace(/_\d+$/,''));}catch(e){}}
 if(player)parts.push('lv'+(b.lv||run.wlevel||1));
 /* enemy clips are per encounter: the same kind from two owners can draw different art, and fights
    are not deterministic, so a per-kind clip compared before/after from different sources */
 else if(PG3.enc)parts.push('@'+String(PG3.enc).replace(/^[epr]\d+-/,''));
 return parts.join('|');
};
/* instrumentation for the jank classifier: what kind of draw produced the pixels */
(function(){
 /* chain onto an instance hook (projectile_fx_1103 converts blur into pixel rings) so the stat
    records the blur that actually reaches the canvas, not the blur a renderer asked for */
 const P=CanvasRenderingContext2D.prototype,blur=Object.getOwnPropertyDescriptor(ctx,'shadowBlur')||Object.getOwnPropertyDescriptor(P,'shadowBlur'),gco=Object.getOwnPropertyDescriptor(ctx,'globalCompositeOperation')||Object.getOwnPropertyDescriptor(P,'globalCompositeOperation');
 Object.defineProperty(ctx,'shadowBlur',{configurable:true,get(){return blur.get.call(this);},set(v){if(PG3.noBlur)v=0;blur.set.call(this,v);const real=blur.get.call(this);if(PG3.ctxStat&&real>0)PG3.ctxStat.blur=Math.max(PG3.ctxStat.blur,real);}});
 Object.defineProperty(ctx,'globalCompositeOperation',{configurable:true,get(){return gco.get.call(this);},set(v){if(PG3.ctxStat&&v==='lighter')PG3.ctxStat.lighter++;gco.set.call(this,v);}});
 for(const m of ['drawImage','fillRect','arc','ellipse','fill','stroke','lineTo','createRadialGradient','createLinearGradient']){
  const raw=ctx[m];ctx[m]=function(){if(PG3.ctxStat)PG3.ctxStat[m]=(PG3.ctxStat[m]||0)+1;return raw.apply(this,arguments);};
 }
})();
PG3.snapshot=function(b,player){
 const P=pBullets,E=eBullets,C=PG3.CROP;
 pBullets=player?[b]:[];eBullets=player?[]:[b];
 const st={blur:0,lighter:0};PG3.ctxStat=st;
 ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.clearRect(0,0,cv.width,cv.height);ctx.restore();
 ctx.setTransform(SS,0,0,SS,(VW/2-b.x)*SS,(VH/2-b.y)*SS);
 const KG=XART.get,KR=XART.rdy,keys=new Set(),note=k=>{if(typeof k==='string')keys.add(k.replace(/(_\d+)+$/,''));};
 XART.get=function(k){note(k);return KG.apply(this,arguments);};XART.rdy=function(k){const v=KR.apply(this,arguments);if(v)note(k);return v;};
 try{drawBullets();}catch(e){st.err=String(e).slice(0,200);}
 finally{XART.get=KG;XART.rdy=KR;}
 st.keys=keys;
 PG3.ctxStat=null;ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.shadowBlur=0;
 pBullets=P;eBullets=E;
 const ox=(VW/2-C/2)*SS,oy=(VH/2-C/2)*SS,w=C*SS,h=C*SS,im=ctx.getImageData(ox,oy,w,h),d=im.data;
 let n=0,hash=2166136261,l=w,r=-1,t=h,bt=-1,lum=0,soft=0;
 /* the game canvas is alpha:false, so "lit" means brighter than the black clear, not alpha */
 for(let i=0;i<d.length;i+=4){const m=Math.max(d[i],d[i+1],d[i+2]);if(m<13)continue;n++;const px=(i>>2)%w,py=(i>>2)/w|0;
  if(px<l)l=px;if(px>r)r=px;if(py<t)t=py;if(py>bt)bt=py;lum+=m;if(m<90)soft++;
  hash=Math.imul(hash^(d[i]*7+d[i+1]*3+d[i+2]+i),16777619)>>>0;}
 return {im,n,hash,bounds:n?[l,t,r+1,bt+1]:null,lum:n?lum/n:0,soft:n?soft/n:0,st};
};
/* warm-up draws exist only to make the game request art; their pixels are discarded, so they skip
   blur (the shipping path costs ~100 ms a draw on Stage 5 with it, which stalled the before pass) */
PG3.warmDraw=function(){if(AP7.frames%4)return;PG3.noBlur=true;try{ctx.save();ctx.setTransform(SS,0,0,SS,0,0);drawBullets();}catch(e){}finally{ctx.restore();PG3.noBlur=false;}};
PG3.touchDraw=function(b,player){
 const P=pBullets,E=eBullets;pBullets=player?[b]:[];eBullets=player?[]:[b];
 PG3.noBlur=true;try{ctx.save();ctx.setTransform(SS,0,0,SS,(VW/2-b.x)*SS,(VH/2-b.y)*SS);drawBullets();}catch(e){}finally{ctx.restore();pBullets=P;eBullets=E;PG3.noBlur=false;}
};
PG3.track=function(list,player){
 for(const b of list){
  if(!b||b.dead||b.__pg3)continue;b.__pg3=1;
  const s=PG3.sig(b,player);
  /* prime/unfilmed: draw the round once, off the record, so the art it draws lazily gets requested
     (stepping never draws, so a reel that is only asked for at draw time would never load) */
  if(PG3.prime){if(!PG3.caps[s]){PG3.caps[s]={sig:s,primed:true};}PG3.touchDraw(b,player);continue;}
  const cap=PG3.caps[s];if(cap&&cap.frames)continue;if(PG3.live.some(L=>L.sig===s))continue;
  PG3.live.push({sig:s,b,player,frames:[],stats:[],skipped:0,age:0,enc:PG3.enc,vx:b.vx,vy:b.vy,w:b.w,h:b.h,kind:b.kind});
 }
};
PG3.film=function(){
 for(const L of PG3.live){
  if(L.done)continue;L.age++;
  if(L.age%PG3.STEP)continue;
  const b=L.b;
  if(b.dead||L.frames.length>=PG3.N){L.done=true;continue;}
  const f=PG3.snapshot(b,L.player);
  if(!f.n&&!L.frames.length){if(++L.skipped>40)L.done=true;continue;}   // launch delay: wait for the first lit frame
  for(const k of f.st.keys)(L.keys=L.keys||new Set()).add(k);
  L.frames.push(f.im);L.stats.push({n:f.n,hash:f.hash,bounds:f.bounds,lum:f.lum,soft:f.soft,blur:f.st.blur,lighter:f.st.lighter,
   img:f.st.drawImage||0,prim:(f.st.fillRect||0)+(f.st.arc||0)+(f.st.ellipse||0)+(f.st.lineTo||0)+(f.st.stroke||0),grad:(f.st.createRadialGradient||0)+(f.st.createLinearGradient||0),err:f.st.err});
  if(L.frames.length>=PG3.N)L.done=true;
 }
 for(const L of PG3.live.filter(L=>L.done)){if(L.frames.length>=4)PG3.store(L);}
 PG3.live=PG3.live.filter(L=>!L.done);
};
PG3.store=function(L){
 const C=PG3.CROP*SS,n=L.frames.length,c=document.createElement('canvas');c.width=C*n;c.height=C;const g=c.getContext('2d');
 L.frames.forEach((im,i)=>g.putImageData(im,i*C,0));
 const hashes=new Set(L.stats.map(s=>s.hash));
 PG3.caps[L.sig]={sig:L.sig,kind:L.kind,art:[...(L.keys||[])].sort(),stage:run.stage,player:L.player,enc:L.enc,frames:n,unique:hashes.size,vx:L.vx,vy:L.vy,w:L.w,h:L.h,stats:L.stats,strip:c.toDataURL('image/webp',0.92)};
 PG3.order.push(L.sig);
};
PG3.flush=function(){const out=[];for(const s of PG3.order){const c=PG3.caps[s];if(c&&c.strip&&!c.sent){c.sent=true;out.push(c);}}
 const r=out.map(c=>({...c}));for(const c of out)c.strip='sent';return r;};
/* ---- drivers ---- */
PG3.enemyCase=function(c){
 PG3.enc=c.id;AP7.begin(c);
 if(c.slice){/* AP7.begin already restarts the stage with its real wave table */}
 return true;
};
PG3.enemySteps=function(n){
 for(let i=0;i<n;i++){
  if(state!==GS.PLAY)break;
  player.invuln=99999;player.dead=false;player.out=false;run.shield=999;
  player.x=worldWidth()/2+Math.sin(AP7.frames/180)*Math.min(115,worldWidth()/4);player.y=VH-90;
  updatePlay(1/60);AP7.frames++;
  PG3.track(eBullets,false);if(!PG3.prime)PG3.film();else PG3.warmDraw();
 }
 return {live:PG3.live.length,caps:Object.keys(PG3.caps).length};
};
PG3.playerCase=function(c){
 PG3.enc=c.id;AP7.begin(c);
 boss=null;bossActive=false;subBoss=null;subBossActive=false;bossDefeated=false;stagePlan=[];enemies=[];spawnClock=9999;run.missileLevel=c.missileLevel||0;
 if(c.space!=null){run.spaceWeapon=c.space;}
 try{yuriLightningOrbUnlocked=true;run._earnedUnlocks={lightningOrb:true};}catch(e){}
 player.fireCd=0;run._chainHeat=0;run._chainOverheat=false;
 for(const k in Input.keys)Input.keys[k]=false;
 for(const k of keybindFor(1).fire||[])if(!k.startsWith('pad_'))Input.keys[k]=true;
 return true;
};
PG3.playerSteps=function(n,charge){
 for(let i=0;i<n;i++){
  if(state!==GS.PLAY)break;
  player.invuln=99999;player.dead=false;run.shield=999;player.x=worldWidth()/2;player.y=VH-90;
  if(charge){const held=(AP7.frames%150)<120;for(const k of keybindFor(1).fire||[])if(!k.startsWith('pad_'))Input.keys[k]=held;}
  updatePlay(1/60);AP7.frames++;
  PG3.track(pBullets,true);if(!PG3.prime)PG3.film();else PG3.warmDraw();
 }
 return {live:PG3.live.length,caps:Object.keys(PG3.caps).length};
};
/* every REGISTERED enemy kind, fired alone down the middle of its own stage, so a type that no
   natural slice happened to reach in its window is still filmed (labelled "registry") */
PG3.registryKinds=function(stage){
 const all=[...new Set([...Object.keys(FIRETYPES||{}),...Object.keys(PROJ||{}),...Object.keys(typeof CFX_STAGE_PROJECTILE!=='undefined'?CFX_STAGE_PROJECTILE:{})])];
 /* stage-prefixed kinds on their own stage; everything else on every stage, because shared fire
    types take their palette and family from run.stage (the gallery folds exact duplicates) */
 return all.filter(k=>{const m=/^s(\d)/.exec(k);return m?+m[1]===stage:true;});
};
PG3.registryCase=function(c){
 PG3.enc=c.id;AP7.begin(c);
 boss=null;bossActive=false;subBoss=null;subBossActive=false;stagePlan=[];enemies=[];spawnClock=9999;eBullets=[];
 return PG3.registryKinds(c.stage);
};
PG3.registryFire=function(kind,frames){
 const b={kind,x:worldWidth()/2,y:110,vx:0,vy:2.4,ang:Math.PI/2,w:12,h:20,t:0,life:12,pal:'red',lv:3,szMul:1,dmg:0,_registry:1};
 eBullets.push(b);
 for(let i=0;i<frames;i++){player.invuln=99999;player.dead=false;run.shield=999;player.x=40;player.y=VH-60;
  if(!b.dead){b.y=Math.min(b.y,VH*0.55);}
  updatePlay(1/60);AP7.frames++;PG3.track(eBullets,false);if(!PG3.prime)PG3.film();else PG3.warmDraw();}
 eBullets=[];return true;
};
PG3.end=function(){for(const L of PG3.live){if(L.frames.length>=4)PG3.store(L);}PG3.live=[];for(const k in Input.keys)Input.keys[k]=false;};
