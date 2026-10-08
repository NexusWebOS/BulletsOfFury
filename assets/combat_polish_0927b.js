"use strict";
/* Mike's September 27 gameplay/Armory pass. Authored art, shared strike warnings. */
const POLISH_ART={armory:'assets/game/shared/combat/polish_0927b/armory.png',bomber:'assets/game/shared/combat/polish_0927b/bomber.png',warning:'assets/game/shared/combat/polish_0927b/warning.png',ordnance:'assets/game/levels/stage_04/projectiles/projectiles_0927/stage4_ordnance.png'};
for(const [k,v] of Object.entries(POLISH_ART))XART._src['polish_'+k]=v;
XART._src.polish_ice_ordnance='assets/game/levels/stage_03/projectiles/projectiles_0927/stage3_ordnance.png';
const POLISH_CELLS={armory:[[225,48,422,406],[892,47,424,409],[225,564,422,402],[895,565,417,403]],bomber:[[8,4,977,601],[1047,28,206,574],[351,615,237,535],[790,685,322,429]],warning:[[196,88,274,679],[750,88,274,679],[1304,88,274,679]]};
const POLISH_CACHE={};
function polishStage4Projectile(b,role){
  if(!XART.rdy('polish_ordnance'))return false;
  const rows={steel:0,brass:1,rocket:2,missile:3,bomb:4,rail:5},row=rows[role];if(row==null)return false;
  const im=XART.get('polish_ordnance'),frame=Math.floor((b.t||0)*18+(b._ph||0))%4,
    h=({steel:36,brass:30,rocket:46,missile:50,bomb:48,rail:42}[role])*(b.szMul||1),scale=h/256;
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(Math.round(b.x),Math.round(b.y));
  ctx.rotate(Math.atan2(b.vy??1,b.vx??0)-Math.PI/2);
  ctx.drawImage(im,frame*256,row*320,256,320,-128*scale,-230*scale,h,320*scale);ctx.restore();return true;
}
function polishStage3Projectile(b,role){
  if(!XART.rdy('polish_ice_ordnance'))return false;
  const row={shard:0,lance:1,tracer:2,mortar:3,shell:4,wave:5}[role];if(row==null)return false;
  const frame=Math.floor((b.t||0)*18+(b._ph||0))%4,im=XART.get('polish_ice_ordnance'),
    scale=({shard:44,lance:48,tracer:34,mortar:40,shell:48,wave:42}[role])*(b.szMul||1)/256;
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(Math.round(b.x),Math.round(b.y));
  ctx.rotate(Math.atan2(b.vy??1,b.vx??0)-Math.PI/2);
  ctx.drawImage(im,frame*256,row*320,256,320,-128*scale,-230*scale,256*scale,320*scale);ctx.restore();return true;
}
function polishCell(name,i){
  const id=name+i;if(POLISH_CACHE[id])return POLISH_CACHE[id];if(!XART.rdy('polish_'+name))return null;
  const im=XART.get('polish_'+name),r=POLISH_CELLS[name]?.[i]||[i*im.width/3,0,im.width/3,im.height];
  const c=document.createElement('canvas');c.width=Math.ceil(r[2]);c.height=Math.ceil(r[3]);c.getContext('2d').drawImage(im,...r,0,0,c.width,c.height);return POLISH_CACHE[id]=c;
}
function polishBlit(name,i,x,y,w,h,flash){const im=polishCell(name,i);if(!im)return;ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,x-w/2,y-h/2,w,h);if(flash){
  const id=name+i+'white';let c=POLISH_CACHE[id];if(!c){c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);g.globalCompositeOperation='source-in';g.fillStyle='#fff';g.fillRect(0,0,c.width,c.height);POLISH_CACHE[id]=c;}
  ctx.globalAlpha=Math.min(1,flash*9);ctx.drawImage(c,x-w/2,y-h/2,w,h);}ctx.restore();}
function polishPanel(x,y,w,h){const im=polishCell('armory',3);if(!im)return;const s=90,d=Math.min(17,h/3),xs=[0,s,im.width-s],ys=[0,s,im.height-s],ws=[s,im.width-2*s,s],hs=[s,im.height-2*s,s],dx=[x,x+d,x+w-d],dy=[y,y+d,y+h-d],dw=[d,w-2*d,d],dh=[d,h-2*d,d];for(let a=0;a<3;a++)for(let b=0;b<3;b++)ctx.drawImage(im,xs[a],ys[b],ws[a],hs[b],dx[a],dy[b],dw[a],dh[b]);}
function polishBaseIcon(w){return ['micon_mg_1','micon_spread_1','micon_missile_1','micon_laser_1','micon_firewall_1','micon_iceorb_1','micon_lasermist_1','micon_chaingun_1','micon_lightningorb_1'][w];}
function polishMapFlash(F){
  const st=F.rect.stage,p=clamp(F.t/F.dur,0,1),pulse=Math.sin(p*Math.PI);ctx.save();ctx.translate(campaignViewOffset(),0);ctx.globalAlpha=pulse*.85;
  if(cmap2On()){const w=cmap2World(st),s=cmap2Size(st),y=w.y+cmap2Bob(st)-4*(cmap2.lift[st]||0);cmap2ApplyCamera();const im=xartTint('cm2_isl_'+st,'#ffffff',.94);if(im)ctx.drawImage(im,w.x-s/2,y-s/2,s,s);}
  else {const p=sselFlagScreenXY(st),key='nss_flag'+st+'_av',im=xartTint(key,'#ffffff',.94);if(im&&p)ctx.drawImage(im,p.x-22,p.y-22,44,44);}
  ctx.restore();
}

/* A profile-wide collection records what was actually acquired, not everything
   purchasable after an element unlock. Existing run/save forms migrate on entry. */
function polishRememberItem(key){const O=achievementState.owned||(achievementState.owned={}),id='arsenal_'+key;if(!O[id]){O[id]={at:Date.now()};achievementSave();}}
function polishRememberWeapon(w){if(WEAPONS[w])polishRememberItem('base_'+w);}
function polishRememberForm(w,e){const O=achievementState.owned||(achievementState.owned={}),id=forgeComboId(e,w);if(!O[id]){O[id]={at:Date.now(),earned:true};achievementSave();}}
function polishCollection(){
  const O=achievementState.owned||{},forms=run&&run.forgeForms||{};const result=[];
  for(const w of FORGE_WEAPONS){
    const base=w===0||!!O['arsenal_base_'+w]||!!(run.wlevels&&run.wlevels[w]>0)||w===6&&laserMistIsUnlocked()||w===7&&chaingunIsUnlocked()||w===8&&yuriLightningOrbIsUnlocked();
    result.push({w,elem:null,name:WEAPONS[w],owned:!!base,key:polishBaseIcon(w)});
    for(const e of Object.keys(INFUSIONS))result.push({w,elem:e,name:forgeComboName(e,w),owned:!!(forms[w]?.[e]||O[forgeComboId(e,w)]),key:forgeBadgeKey(e,w,1)});
  }
  const variants=[['laserbeam',3,'cole'],['mavhoming',3,'maverick'],['flamethrower',4,'cole'],['icebreath',4,'freezer'],['iceorb',5,'cole'],['fireorb',5,'cole'],['fireice',5,'freezer']];
  for(const [v,w,pilot] of variants)result.push({w,elem:null,variant:v,pilot,name:WVAR_NAME[v],owned:!!O['arsenal_variant_'+v]||result.some(c=>c.w===w&&!c.elem&&c.owned&&(v==='laserbeam'||v==='flamethrower'||v==='iceorb'))||!!(v==='fireorb'&&forms[5]?.fire),key:v==='mavhoming'?'micon_maverick_laser_1':WVAR_ICON[v]?WVAR_ICON[v]+'1':polishBaseIcon(w)});
  for(let i=0;i<3;i++)result.push({w:0,elem:null,space:i,name:['SPACE LASER CANNON','SHADOW ORB','VOLLEY MISSILES'][i],owned:!!O['arsenal_space_'+i]||!!(run.spaceMode&&run.spaceLevels?.[i]>0),key:['space_laser_icon_1','space_shadow_icon_1','space_volley_icon_1'][i]});
  return result;
}
function polishArmoryDraw(dt){
  if(!armory)armoryOpen('title');const A=armory;A.t+=dt;A.msgT=Math.max(0,A.msgT-dt);const art=curFontArt();
  if(!A.collected){for(const w of FORGE_WEAPONS)if(run.wlevels?.[w]>0)polishRememberWeapon(w);for(const [w,forms]of Object.entries(run.forgeForms||{}))for(const e of Object.keys(forms))polishRememberForm(+w,e);A.collected=true;}
  const cells=polishCollection(),cols=1+Object.keys(INFUSIONS).length,rows=Math.ceil(cells.length/cols);
  A.cell=clamp(A.cell||0,0,cells.length-1);const side=Math.min((VW-54)/cols,(VH-173)/rows),x0=(VW-side*cols)/2+12,y0=62;
  ctx.fillStyle='#060c16';ctx.fillRect(0,0,VW,VH);
  const label=(text,x,y,h,col='#dcecff')=>{if(art)stageText(art,text,x,y,Math.min(h,stageFitH(art,text,VW-25,h,5,.04)),col,.95,1,.04);};
  label('FURY ARMORY',VW/2,19,18,'#ffda72');label(cells.filter(c=>c.owned).length+' / '+cells.length+' COLLECTED',VW/2,39,9);
  const els=[null,...Object.keys(INFUSIONS)];els.forEach((e,i)=>{if(e)iconBlit(ctx,'inf_'+e,x0+(i+.5)*side,y0-10,13,true);else label('BASE',x0+side/2,y0-10,6);});
  A.rects=[];
  cells.forEach((c,i)=>{const x=x0+(i%cols+.5)*side,y=y0+(Math.floor(i/cols)+.5)*side,sel=i===A.cell;
    polishBlit('armory',c.owned?(sel?1:0):2,x,y,side-2,side-2);
    if(c.owned){if(!iconBlit(ctx,c.key,x,y,side*.63,true))iconBlit(ctx,polishBaseIcon(c.w),x,y,side*.63,true);}
    if(sel&&!c.owned){ctx.strokeStyle='#ffcf51';ctx.lineWidth=1.5;ctx.strokeRect(x-side/2+2,y-side/2+2,side-4,side-4);}
    if(i%cols===0&&i<90)iconBlit(ctx,polishBaseIcon(c.w),x0-15,y,20,true);
    if(i===90)label('+',x0-15,y,11);
    A.rects.push({x:x-side/2,y:y-side/2,w:side,h:side,i});
  });
  const c=cells[A.cell],dy=y0+rows*side+8,dh=VH-dy-28;
  polishPanel(13,dy,VW-26,dh);
  label(c.owned?c.name:'UNDISCOVERED',VW*.35,dy+18,11,c.owned?'#ffda72':'#b8c4d4');
  label(c.owned?'COLLECTED':'ACQUIRE AND FORGE TO REVEAL',VW*.35,dy+37,7);
  if(c.owned){const id=c.w+'|'+c.elem+'|'+c.variant+'|'+c.space;if(A.previewId!==id){A.previewId=id;A.preview=forgePreviewNew(c.w,c.elem,1);A.preview.pilot=c.pilot;A.preview.space=c.space;if(c.variant)A.preview.variant=c.variant;else if(c.w===3&&!c.elem)A.preview.variant='laserbeam';}
    forgePreviewTick(A.preview,95,dh-20,dt);forgePreviewDraw(A.preview,VW-122,dy+10,95,dh-20);
  }
  controlHintRow([['pad_dpad','BROWSE'],['pad_a','PREVIEW'],['pad_b','BACK']],VH-12,VW/2,VW-24);
  const lf=Input.menuLeft(),rt=Input.menuRight(),up=Input.menuUp(),dn=Input.menuDown(),go=Input.menuConfirm();
  const col=A.cell%cols,row=Math.floor(A.cell/cols);let next=A.cell;
  if(lf||rt)next=row*cols+clamp(col+(rt?1:-1),0,cols-1);if(up||dn)next=clamp(row+(dn?1:-1),0,rows-1)*cols+col;
  if(next!==A.cell){A.cell=next;Audio.SFX.blip?.();}if(go){(c.owned?Audio.SFX.select:Audio.SFX.blocked)?.();if(c.owned&&A.preview)A.preview.cd=0;}
  const md=!!Input.mouse.down;if(md&&!A.md&&Input.mouse.inside){const r=A.rects.find(r=>Input.mouse.x>=r.x&&Input.mouse.x<r.x+r.w&&Input.mouse.y>=r.y&&Input.mouse.y<r.y+r.h);if(r)A.cell=r.i;}A.md=md;
  if(Input.menuBack()){if(A.back==='forge')setState(GS.FORGE);else if(A.back==='title'){setState(GS.TITLE);menuIndex=TITLE_ITEMS.indexOf('ARMORY');}else{setState(GS.VAULT);vaultOpen();}}
}

/* Committed, color-staged incoming missile lanes. Same FOV and strike engine
   for boss ordnance and ordinary bomber runs. Direction arrow is authored art. */
let polishLanes=[],polishDeaths=[];
function polishReset(){polishLanes=[];polishDeaths=[];}
function polishEncounterAttack(b,dt){
  const R=b._er26,mode=R.mode,n=R.level;
  if(!/mortar|charred-battery/.test(mode))return false;
  if(b._mr27&&b._mr27.parts.filter(p=>p.id.startsWith('rocket')&&!p.dead).length===0){er26Set(b,'recover');return true;}
  R.warnings=[];b.x+=(er26Station(b,0)-b.x)*Math.min(1,dt*2);b.y+=(R.home-b.y)*Math.min(1,dt*3);b._drawY=b.y;
  if(!R.groundCast){R.groundCast=true;R.dur=3.6;const count=mode==='charred-battery'?6:4+n,gap=Math.floor(Math.random()*count),W=camRightX()-camLeftX();
    for(let i=0;i<count;i++){
      if(i===gap)continue;const x=camLeftX()+W*(i+.5)/count,y=clamp(R.target.y+(i%2?24:-20),240,VH-65);
      const q=groundTargetingSpawn({kind:'missile',owner:b,x,y,warn:[1.25,1.05,.88][n]+i*.09,active:.5,radius:29,size:82,track:false,shake:3,onImpact:q=>{
        const a=aimPlayer(q.x,q.y);for(let k=0;k<6+n;k++){const angle=k*TAU/(6+n);if(Math.abs(Math.atan2(Math.sin(angle-a),Math.cos(angle-a)))<.5)continue;if(b._s4war)stage4WarfareShot(b,q,angle,2.35+n*.23,'mg');else er26Shot(b,q,angle,2.35+n*.23);}
        explode(q.x,q.y,72,b._ship==='magmaward'||b._s4war?'red':'blue');}});q._polishBomb={x:b.x,y:b.y+b.h*.30};
    }
    if(mode==='charred-battery')for(const slot of ['L','R']){const p=shipBossMount(b,slot);polishLane(b,p.x,p.y,R.angles[slot==='L'?0:2],{mount:slot,warn:1.55,speed:5.6,fire:q=>{for(let j=-2;j<=2;j++)er26Shot(b,q,q.angle+j*.095,5.6);er26Muzzle(b,slot);}});}
    er26Sound('bossWeaponCharge','enemyBossCannon');
  }
  return true;
}
function polishLane(owner,x,y,angle,opt={}){const q={owner,x,y,angle,t:0,warn:opt.warn||1.25,speed:opt.speed||5,width:opt.width||34,fire:opt.fire,mount:opt.mount,
  offset:owner&&Number.isFinite(owner.x+owner.y)?{x:x-owner.x,y:y-owner.y}:null};polishLanes.push(q);XART.rdy('polish_warning');return q;}
function polishLaneOrigin(q){
  // The direction is committed, but the physical launcher travels with its hull.
  // Use this in both update and draw so the last warning matches the release.
  const p=q.mount?shipBossMount(q.owner,q.mount):q.offset?{x:q.owner.x+q.offset.x,y:q.owner.y+q.offset.y}:q;
  q.x=p.x;q.y=p.y;
}
function polishCombatTick(dt){
  for(const b of [boss,subBoss])if(b&&b.dead&&!b._polishDeath){b._polishDeath=true;polishDeaths.push({x:b.x,y:b.y,w:b.w,h:b.h,t:0,cd:0,mini:b===subBoss});}
  for(const D of polishDeaths){D.t+=dt;D.cd-=dt;if(D.cd<=0&&D.t<2.3){D.cd=.13;explode(D.x+rnd(-D.w*.4,D.w*.4),D.y+rnd(-D.h*.35,D.h*.35),Math.max(35,D.w*.30),'red');if(D.t>.65&&D.t<1.8)atomFlash=Math.max(atomFlash,Math.sin((D.t-.65)/1.15*Math.PI)*.78);}}
  polishDeaths=polishDeaths.filter(q=>q.t<2.8);
  if(bossActive||subBossActive){for(const e of enemies)e._polishBomberCD=4;}
  else if(run.stage>=3)for(const e of enemies){
    if(e.dead||!/(bomber|missilejet|rocketjet)/i.test(e.type||''))continue;
    e._polishBomberCD=(e._polishBomberCD==null?3:e._polishBomberCD)-dt;
    if(e._polishBomberCD<=0&&e.y>25&&e.y<VH*.48&&Math.abs(e.x-player.x)<VW){e._polishBomberCD=7;polishLane(e,e.x,e.y+20,Math.PI/2,{warn:1.4,speed:4.5});}
  }
  for(const q of polishLanes){q.t+=dt;if(q.owner?.dead){q.dead=true;continue;}polishLaneOrigin(q);combatWarningTick(q,'incoming',q.t,q.warn);
    if(q.t>=q.warn){q.dead=true;if(q.fire)q.fire(q);else{const p=eShootT(q.x,q.y,q.angle,q.speed,'emissile',{w:12,h:25,silent:true});p._shootable=true;p.hp=2;p._noArsenal=true;p.spd=q.speed;p.ang=q.angle;p._committed=true;p.homing=false;Audio.SFX.missile?.();}}
  }polishLanes=polishLanes.filter(q=>!q.dead);
}
function polishCombatDraw(){
  // This hook is after world restore; warnings convert world positions explicitly.
  ctx.save();ctx.translate(-camLeftX(),0);
  for(const q of groundTargetingFx)if(q._polishBomb&&!q.owner?._bomber&&q.t>0&&q.t<q.warn&&XART.rdy('lz_bomb')){const p=clamp(q.t/q.warn,0,1),im=XART.get('lz_bomb');ctx.save();ctx.translate(lerp(q._polishBomb.x,q.x,p),lerp(q._polishBomb.y,q.y,p));ctx.rotate(Math.PI);ctx.drawImage(im,-7,-17,14,34);ctx.restore();}
  for(const q of polishLanes){polishLaneOrigin(q);const p=clamp(q.t/q.warn,0,1);combatWarningDraw(q,{x:q.x,y:q.y,ex:q.x+Math.cos(q.angle)*VH,ey:q.y+Math.sin(q.angle)*VH,progress:p,width:q.width});
    const im=(enemyWarningOwner(q)||run.stage===6||(run.stage===5&&q.owner===subBoss))?null:polishCell('warning',p<L23_FOV_YEL?0:p<L23_FOV_RED?1:2);if(im){ctx.save();ctx.translate(q.x,q.y+30);ctx.rotate(q.angle-Math.PI/2);ctx.globalAlpha=.62+.38*Math.abs(Math.sin(q.t*18));ctx.drawImage(im,-12,-26,24,52);ctx.restore();}}
  const b=subBoss;if(b?._bomber&&!b.dead){const B=b._bomber;if(B.mode==='charge'||B.mode==='beam'){ctx.restore();ctx.save();ctx.fillStyle='rgba(0,0,12,'+(B.mode==='beam'?.56:clamp(B.t/B.dur,0,1)*.62)+')';ctx.fillRect(0,0,VW,VH);ctx.translate(-camLeftX(),0);siegeBomberBeamDraw(b);}}
  ctx.restore();
}

/* Stage 5 pursuit: two engines, two forward cannons, and a rear bomb bay. */
function siegeBomberInit(b){
  const n=diffKey==='furious'?2:diffKey==='hard'?1:0;b.name='ECLIPSE SIEGE BOMBER';b.w=VW*.50;b.h=b.w*.62;b.x=worldWidth()/2;b.y=-b.h;b.ty=VH*.27;b.enter=true;b._ship=null;
  const hp=diffKey==='easy'?600:[1050,1250,1450][n];b._bomber={n,mode:'entry',t:0,dur:2.1,seq:0,cd:0,clock:0,bombs:[],history:['entry'],core:hp,coreMax:hp,parts:[]};
  for(const id of ['engineL','engineR','laserL','laserR'])b._bomber.parts.push({id,hp:diffKey==='easy'?140:250+n*40,max:diffKey==='easy'?140:250+n*40,flash:0});
  b.hp=b.maxhp=hp+b._bomber.parts.reduce((a,p)=>a+p.hp,0);if(typeof mr27BomberSetup==='function')mr27BomberSetup(b);XART.rdy('polish_bomber');for(let i=0;i<8;i++){XART.rdy('l23fx_inferno_laser_'+i);XART.rdy('l23fx_inferno_mg_'+i);XART.rdy('laser_round_muzzle_'+i);}XART.rdy('lz_bomb');
}
function siegeBomberParts(b){
  if(b._bomber.space)return mr27SpaceParts(b);const W=b.w;return [{id:'core',cell:0,x:b.x,y:b.y,w:W,h:b.h},...[-1,1].flatMap(s=>[{id:s<0?'engineL':'engineR',cell:1,x:b.x+s*W*.30,y:b.y+W*.12,w:W*.15,h:W*.43},{id:s<0?'laserL':'laserR',cell:2,x:b.x+s*W*.17,y:b.y-W*.015,w:W*.13,h:W*.36}])];}
function siegeBomberAt(b,x,y,pad=0){if(b.dead||b.enter||!Number.isFinite(x)||!Number.isFinite(y))return null;for(const p of siegeBomberParts(b).reverse()){const m=b._bomber.parts.find(q=>q.id===p.id);if(m&&m.hp<=0)continue;const core=p.id==='core',w=core?p.w*.48:p.w,h=core?p.h*.82:p.h;if(Math.abs(x-p.x)<w/2+pad&&Math.abs(y-p.y)<h/2+pad)return p.id;}return null;}
function siegeBomberBeam(b,beam){const bottom=Math.min(beam.bot??player.y,b.y+b.h),top=Math.max(beam.top||0,b.y-b.h);
  /* The laser plates are painted over their adjacent engines. A held beam aimed at a turret's
     centre must hit that visible plate even where its lower edge overlaps an engine box. */
  for(const p of siegeBomberParts(b).filter(q=>q.id.startsWith('laser'))){
    const m=b._bomber.parts.find(q=>q.id===p.id);
    if(m?.hp>0&&Math.abs(beam.x-p.x)<p.w*.5+(beam.w||6)*.5&&p.y+p.h*.5>=top&&p.y-p.h*.5<=bottom)
      return {x:beam.x,y:Math.min(bottom,p.y+p.h*.5),id:p.id};
  }
  for(let y=bottom;y>top;y-=3)for(const x of [beam.x,beam.x-(beam.w||6)*.4,beam.x+(beam.w||6)*.4]){const id=siegeBomberAt(b,x,y,2);if(id)return{x,y,id};}return null;}
function siegeBomberTargets(b){return siegeBomberParts(b).map(p=>retinaDynamicPiece(b,'bomber-'+p.id,p.id==='core'?'boss':'module',()=>{const q=siegeBomberParts(b).find(q=>q.id===p.id),m=b._bomber.parts.find(q=>q.id===p.id);return{x:q.x,y:q.y,hp:m?m.hp:b._bomber.core,dead:b.dead||b.enter||!!(m&&m.hp<=0)};},d=>siegeBomberHit(b,d,p.x,p.y,p.id),p.w,p.h));}
function siegeBomberHit(b,dmg,x,y,id){if(b.enter||b.dead||dmg<=0||b._bomber.mode==='overdrive')return;const B=b._bomber,target=id||siegeBomberAt(b,x,y,Math.max(2,(_dmgBullet?.w||0)*.35))||(!Number.isFinite(x)||!Number.isFinite(y)?'core':null),p=B.parts.find(p=>p.id===target);if(!p&&target!=='core')return;
  if(p&&p.hp<=0)return;
  if(p){p.hp=Math.max(0,p.hp-dmg);p.flash=.2;if(!p.hp){const shape=siegeBomberParts(b).find(q=>q.id===p.id);if(typeof d27ModuleRupture==='function')d27ModuleRupture(b,p,{...shape,debrisImage:B.space?mr27Cell('space',shape.cell,typeof d27FuriousBomber==='function'&&d27FuriousBomber(b)?'fury':null):polishCell('bomber',shape.cell)},'red');explode(shape.x,shape.y,b.w*.24,'red');Audio.SFX.expBig?.();if(p.id.startsWith('laser')&&['charge','beam'].includes(B.mode))siegeBomberSet(b,'recover');}}
  else {B.core=Math.max(0,B.core-dmg);b.flash=.18;}
  b.hp=B.core+B.parts.reduce((s,p)=>s+p.hp,0);
  if(B.core<=0){b.hp=0;b.dead=true;b.dying=0;groundTargetingCancel(b);polishLanes=polishLanes.filter(q=>q.owner!==b);achievementEncounterDefeat(b,'miniboss');continueRewardResolve(b,b.x,b.y,'miniboss');Audio.SFX.expBig?.();}
}
function siegeBomberSet(b,mode){const B=b._bomber;B.mode=mode;B.t=0;B.cd=0;B.dur=({bombs:diffKey==='easy'?3.1:4.2,charge:diffKey==='easy'?3.4:2.7,beam:1.5,crossfire:diffKey==='easy'?3.1:3.8,missiles:diffKey==='easy'?2.4:3.3,recover:diffKey==='easy'?2.0:diffKey==='normal'?1.55:1.25})[mode]||2;if(typeof d27FuriousBomber==='function'&&d27FuriousBomber(b)){B.dur=({bombs:3.6,charge:1.65,beam:1.25,crossfire:3.2,missiles:2.7,recover:.85})[mode]||B.dur;B.safeLane=Math.floor(Math.random()*5);B.volley=0;}if(mode==='lob'){B.dur=[1.1,.95,.85][B.n]*(diffKey==='easy'?1.3:1)+(2+B.n)*.34+1.5;B.lobCast=false;}
  if(mode==='carpet'){B.dur=3.6;B.carpetCast=false;}
  if(mode==='overdrive'){B.dur=1.6;B.odFx=false;}
  if(B.od&&mode!=='overdrive')B.dur*=mode==='recover'?.75:.9;
  B.history.push(mode);B.target={x:player.x,y:player.y};if(mode==='charge'){(Audio.SFX.bossWeaponCharge||Audio.SFX.laserBeamStart)?.();arcadeBanner('ALLIED WING UNDER FIRE');}if(mode==='beam')(Audio.SFX.quadFire||Audio.SFX.laserBeamStart)?.();}
function siegeBomberTick(b,dt){const B=b._bomber;B.clock+=dt;B.t+=dt;b.flash=Math.max(0,(b.flash||0)-dt);for(const p of B.parts)p.flash=Math.max(0,p.flash-dt);
  if(b.dead){b.dying+=dt;if(b.dying>2.8){subBossActive=false;subBossDone=true;subBoss=null;run.score+=9000;stageScoreOffer(9000);dropPowerup(b.x,b.y,'weapon');}return;}
  if(B.mode==='entry'){b.y=lerp(-b.h,b.ty,1-Math.pow(1-clamp(B.t/B.dur,0,1),3));if(B.t>=B.dur){b.enter=false;siegeBomberSet(b,B.space?'crossfire':'bombs');}return;}
  const engines=B.parts.filter(p=>p.id.startsWith('engine')&&p.hp>0).length,furious=typeof d27FuriousBomber==='function'&&d27FuriousBomber(b);
  const tx=worldWidth()/2+Math.sin(B.clock*(furious?1.7:diffKey==='easy'?.48:.78+B.n*.18))*Math.max(35,worldWidth()*(furious?.29:.25))*engines/2;b.x+=(tx-b.x)*Math.min(1,dt*(furious?5:diffKey==='easy'?1.25:2.1));const ty=b.ty+(furious?Math.sin(B.clock*2.9)*22:0);b.y+=(ty-b.y)*Math.min(1,dt*(furious?4:2));
  B.cd-=dt;
  if(B.mode==='charge')combatWarningTick(b,'siege-beam',Math.min(B.t,B.dur),B.dur);
  if(B.mode==='beam')for(const p of siegeBomberParts(b).filter(p=>p.id.startsWith('laser')))if(B.parts.find(q=>q.id===p.id).hp>0&&Math.abs(player.x-p.x)<27&&player.y>=p.y+p.h*.46)playerHit();
  if(B.mode==='crossfire'&&B.cd<=0){B.cd=diffKey==='easy'?.72:B.n===2?.31:.47;for(const p of siegeBomberParts(b).filter(p=>p.id.startsWith('laser')&&B.parts.find(q=>q.id===p.id).hp>0)){const tip=p.y+p.h*.46,a=Math.atan2(player.y-tip,player.x-p.x);for(const off of (B.n===2?[-.13,0,.13]:[-.08,.08]))siegeBomberShot(b)(p.x,tip,a+off,diffKey==='easy'?3.9:5.1+B.n*.35);if(typeof wm26Emit==='function')wm26Emit(b,p.x,tip,a,'laser',null,{size:29});}Audio.SFX.laser?.();}
  if(B.mode==='bombs'&&B.cd<=0){B.cd=furious?.38:diffKey==='easy'?1.3:[.62,.49,.40][B.n];
    const slot=(B.volley||0)%5;B.volley=(B.volley||0)+1;
    const target={x:furious?(slot+.5)*worldWidth()/5:clamp(player.x+Math.sin(B.clock*2.1)*55,camLeftX()+35,camRightX()-35),y:clamp(player.y,220,VH-65)};
    if(!furious||slot!==B.safeLane){
      const q=groundTargetingSpawn({kind:'missile',owner:b,...target,warn:furious?.84:diffKey==='easy'?1.65:1.18-B.n*.14,active:.40,radius:furious?27:32,size:88,track:false,shake:3,onImpact:q=>explode(q.x,q.y,68,'red')});q._polishBomb={x:b.x,y:b.y+b.h*.34};B.bombs.push(q);Audio.SFX.missile?.();
      if(typeof wm26Emit==='function')wm26Emit(b,b.x,b.y+b.h*.34,Math.PI/2,'missile',null,{size:30});
    }
  }
  if(B.mode==='lob'||B.mode==='carpet'||B.mode==='overdrive')siegeBomber28Tick(b,B);
  if(B.mode==='missiles'&&B.cd<=0){B.cd=furious?.62:diffKey==='easy'?1.1:[.76,.68,.62][B.n];for(const s of [-1,1])for(const offset of (furious?[-.17,.17]:[0]))polishLane(b,b.x+s*b.w*.42,b.y+15,Math.PI/2+offset,{warn:furious?.90:diffKey==='easy'?1.65:1.1-B.n*.08,speed:furious?7.2:diffKey==='easy'?4.6:5.8+B.n*.65});}
  if(B.t>=B.dur){if(B.mode==='charge')siegeBomberSet(b,'beam');else if(B.mode==='beam')siegeBomberSet(b,'recover');else{
    /* 0928: Furious crosses into its overdrive once, between attacks, at half the pool */
    if(B.n===2&&!B.od&&b.hp<=b.maxhp*.5){B.od=true;siegeBomberSet(b,'overdrive');}
    else{const book=B.space?(B.od?['charge','crossfire','missiles','charge','crossfire']:['crossfire','charge','missiles','crossfire']):(B.od?['charge','carpet','missiles','lob','bombs']:['bombs','charge','missiles','lob']),next=book[B.seq++%book.length];
      siegeBomberSet(b,['charge','crossfire'].includes(next)&&!B.parts.some(p=>p.id.startsWith('laser')&&p.hp>0)?(B.space?'missiles':'bombs'):next);}}}
  B.bombs=B.bombs.filter(q=>!q.dead);
}
function siegeBomberDraw(b){
  if(b.dead)return;
  /* 0928: lanes and the overdrive glow draw behind the hull, for both the Earth and space skins */
  siegeBomberLaneDraw(b);
  {const B0=b._bomber;if(B0.mode==='overdrive'){const k=clamp(B0.t/B0.dur,0,1),key='l23fx_inferno_mg_'+(Math.floor(B0.clock*16)%8);if(XART.rdy(key)){ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.6*(1-k);const s=b.w*(.5+k);ctx.drawImage(XART.get(key),b.x-s/2,b.y-s/2,s,s);ctx.restore();}}}
  if(b._bomber.space&&mr27SpaceDraw(b))return;const B=b._bomber;if(b.dead)return;for(const p of siegeBomberParts(b)){const m=B.parts.find(q=>q.id===p.id);if(m?.hp<=0)continue;
  if(p.id.startsWith('engine')&&typeof d27MuzzleDraw==='function')d27MuzzleDraw(ctx,'exhaust',p.x,p.y+p.h*.43,Math.PI/2,(B.clock*12)%1,82);
  polishBlit('bomber',p.cell,p.x,p.y,p.w,p.h,m?m.flash:b.flash);}
  if(B.mode==='bombs')polishBlit('bomber',3,b.x,b.y+b.h*.23,b.w*.12,b.h*.30);
  for(const q of B.bombs)if(q.t>0&&q.t<q.warn&&XART.rdy('lz_bomb')){const p=clamp(q.t/q.warn,0,1),im=XART.get('lz_bomb');ctx.save();ctx.translate(lerp(q._polishBomb.x,q.x,p),lerp(q._polishBomb.y,q.y,p));ctx.rotate(Math.PI);ctx.drawImage(im,-8,-20,16,40);ctx.restore();}
}
function siegeBomberBeamDraw(b){if(b.dead)return;const B=b._bomber;
  for(const p of siegeBomberParts(b).filter(p=>p.id.startsWith('laser'))){if(B.parts.find(q=>q.id===p.id).hp<=0)continue;const tip=p.y+p.h*.46;
    if(B.mode==='charge'){const s=18+Math.min(1,B.t/B.dur)*45;wm26Draw(ctx,'laser',p.x,tip,Math.PI/2,(B.clock*13)%1,s,d27FuriousBomber(b)?'#ff3922':null);combatWarningDraw(b,{x:p.x,y:tip,ex:p.x,ey:VH+20,progress:B.t/B.dur,width:45});}
    else if(B.mode==='beam'){const k=B.space?'tlv_beam':'l23fx_inferno_laser_'+Math.floor(B.clock*16)%8;if(XART.rdy(k)){const im=XART.get(k);ctx.save();ctx.translate(p.x,tip);ctx.drawImage(im,-27,0,54,VH-tip+20);ctx.restore();}if(typeof d27MuzzleDraw==='function')d27MuzzleDraw(ctx,'laser',p.x,tip,Math.PI/2,(B.clock*13)%1,40);}
  }
}

/* ============================================================================
   0928 — the Stage 5/6 pursuit bombers (Mike: "better FOV warnings ... only that the ball is
   coming where its targeted", and Furious "extra abilities, attacks, patterns, phases").
   * The bomb bay's bombs already fell onto floor reticles; each now also shows its lane from the
     bay to the reticle while it falls, so the reticle says where it is coming FROM.
   * Every difficulty gains a FLAK LOB: 2+n targeted rounds from the bay (tb28), bursting on arrival.
   * Furious crosses into OVERDRIVE at half its pool: an invulnerable beat, faster turns, and a
     CARPET RUN - a line of lobbed bombs walking across the pilot's row with one cell always open.
   ============================================================================ */
function siegeBomberBay(b){return {x:b.x,y:b.y+b.h*(b._bomber.space?.30:.34)};}
function siegeBomberShot(b){
  const space=b._bomber.space;
  return (x,y,a,s)=>{const q=eShootT(x,y,a,s,space?'s5split':'s6orb',{w:14,h:14,silent:true,noMuzzle:true});q._noArsenal=true;q._boss=true;return q;};
}
function siegeBomber28Tick(b,B){
  const n=B.n,space=B.space;
  if(B.mode==='overdrive'){
    b.flash=Math.max(b.flash||0,.05);
    if(!B.odFx&&B.t>=.3){B.odFx=true;shake=Math.max(shake,11);flashScreen=Math.max(flashScreen||0,.4);
      if(typeof spawnShockRing==='function'){spawnShockRing(b.x,b.y,b.w*.5,'fire');spawnShockRing(b.x,b.y,b.w*.8,'fire');}
      explode(b.x,b.y,b.w*.3,'red');(Audio.SFX.bossRoar||Audio.SFX.expBig||function(){})();
      if(typeof arcadeBanner==='function')arcadeBanner(space?'ECLIPSE BURN':'CARPET RUN');}
    return;
  }
  if(B.mode==='lob'&&!B.lobCast){B.lobCast=true;const count=2+n;
    for(let i=0;i<count;i++){const off=i===0?0:((i&1)?84:-84)*Math.ceil(i/2);
      tb28Fire(b,{from:()=>b.dead?null:siegeBomberBay(b),target:{x:player.x+off,y:player.y-(i&1?14:0)},warm:[1.1,.95,.85][n]*(diffKey==='easy'?1.3:1)+i*.34,
        flight:.8,mode:'direct',art:space?'antimatter':'molten',size:28,hp:2,silent:i>0,shot:siegeBomberShot(b),burst:{n:6,speed:2.4+.25*n,gap:.5},
        onArrive:(q,x,y)=>{explode(x,y,30,space?'blue':'red');(Audio.SFX.expSmall||function(){})();}});}
    (Audio.SFX.bossWeaponCharge||function(){})();
  }
  if(B.mode==='carpet'&&!B.carpetCast){B.carpetCast=true;
    const L=camLeftX()+34,W=camRightX()-camLeftX()-68,cols=7,dir=Math.random()<.5?-1:1,gap=1+Math.floor(Math.random()*(cols-2));let i=0;
    for(let k=0;k<cols;k++){const c=dir<0?cols-1-k:k;if(c===gap)continue;
      tb28Fire(b,{from:()=>b.dead?null:siegeBomberBay(b),target:{x:L+W*c/(cols-1),y:player.y+((k&1)?-22:18)},warm:.8+i*.2,flight:.8,mode:'lob',arc:90,
        art:space?'void':'molten',size:30,splash:34,reticle:80,width:26,laneAlpha:.4,silent:i>0,onArrive:(q,x,y)=>explode(x,y,44,space?'blue':'red')});i++;}
    (Audio.SFX.bossWeaponCharge||function(){})();
  }
}
function siegeBomberLaneDraw(b){
  const B=b._bomber,bay=siegeBomberBay(b);
  for(const q of B.bombs){if(q.dead||q.impact||!(q.t>0))continue;const k=clamp(q.t/q.warn,0,1);
    combatWarningDraw(b,{x:bay.x,y:bay.y,ex:q.x,ey:q.y,progress:k,width:26,len:Math.hypot(q.x-bay.x,q.y-bay.y),fieldOnly:true,alpha:.34});}
}
