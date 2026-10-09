'use strict';
/* Mike's five-panel authored top HUD. UI reads state; drawing never changes combat. */
const PH8={height:104,row:70,scale:2,cache:new Map(),rows:1,last:[],draws:0};
const PH8_BASE={strip:drawHUDStrip,overlay:drawHUDOverlay,special:drawSpecialHUD,loans:drawHeavyTurretHUD,
 load:stageLoadBegin,retire:bofDerivedCachesRetire,state:setState,begin:beginStage,start:startRun,bar:drawHealthBarV2};
for(const a of Object.values(PH8_ART))XART._src[a.key]=a.path;
function ph8Theme(){return run.stage===6&&run._gp4StageX?'stage_x':'stage_'+String(clamp(run.stage||1,1,9)).padStart(2,'0');}
function ph8Keys(n){return [PH8_ART['stage_'+String(n).padStart(2,'0')]?.key,...(n===6?[PH8_ART.stage_x.key]:[]),...(n===8?['bmbar_fill_solid']:[])].filter(Boolean);}
stageLoadBegin=function(n,keys){return PH8_BASE.load.call(this,n,[...new Set([...(keys||[]),...ph8Keys(n)])]);};
bofDerivedCachesRetire=function(){PH8.cache.clear();PH8.last=[];return PH8_BASE.retire.apply(this,arguments);};
function ph8Sync(){const rows=seatList().length,h=PH8.height*rows;PH8.rows=rows;
 if(hudcv&&(hudcv.height!==h*PH8.scale||hudcv.width!==VW*PH8.scale)){hudcv.height=h*PH8.scale;hudcv.width=VW*PH8.scale;}
 if(window.__bofHudHeight!==h){window.__bofHudHeight=h;if(window.__bofFit)window.__bofFit();}
}
setState=function(){const r=PH8_BASE.state.apply(this,arguments);ph8Sync();return r;};
beginStage=function(){const r=PH8_BASE.begin.apply(this,arguments);ph8Sync();return r;};
startRun=function(){const r=PH8_BASE.start.apply(this,arguments);ph8Sync();return r;};
function ph8Frame(theme){if(PH8.cache.has(theme))return PH8.cache.get(theme);const a=PH8_ART[theme];if(!a||!XART.rdy(a.key))return null;
 const source=XART.get(a.key),canvas=document.createElement('canvas');canvas.width=VW*PH8.scale;canvas.height=PH8.row*PH8.scale;
 const g=canvas.getContext('2d');g.scale(PH8.scale,PH8.scale);g.imageSmoothingEnabled=true;g.drawImage(source,0,0,VW,PH8.row);
 const sx=VW/a.w,sy=PH8.row/a.h,local=r=>[r[0]*sx,(r[1]-a.sourceY)*sy,r[2]*sx,r[3]*sy];
 const empty=r=>{const q=local(r);g.clearRect(...q);g.drawImage(source,a.emptyX,a.special[1]-a.sourceY,4,a.special[3],...q);return q;};
 const d=a.offset;
 // Remove all illustration values/names/icons with the authored dark recess.
 const boxes={rollLabel:[80,a.rollLabelTop-10,282,26],somerLabel:[80,a.somerLabelTop-10,282,26],
  weapon:[417,130+d,112,123],name:[653,108+d,390,45],specialIcon:[609,116+d,29,29],
  radar:[1097,132+d,133,124],lock:[1329,147+d,241,56],
  lives:[137,253+d,204,43],missiles:[1325,253+d,268,43],
  speed:[592,238+d,215,36],shield:[826,238+d,217,36]};
 const rect={};for(const [k,r] of Object.entries(boxes))rect[k]=empty(r);
 rect.roll=empty(a.roll);rect.somer=empty(a.somer);rect.special=empty(a.special);
 const f={canvas,source,a,rect,local};PH8.cache.set(theme,f);return f;
}
function ph8Text(g,s,x,y,size,max,align='center'){
 if(!s)return;const face=window.BOF_UI_FACE||'game',text=String(s).toUpperCase();
 const measure=bmfMeasure(face,text,size),fs=Math.min(size,size*max/Math.max(1,measure));
 // Let the bitmap renderer round on the denser HUD grid, not the
 // 480px playfield grid: small outlined letters keep their strokes.
 const d=PH8.scale;g.save();g.scale(1/d,1/d);
 bmfDrawOn(g,face,text,Math.round(x*d),Math.round(y*d),fs*d,align);g.restore();
}
function ph8Centered(g,text,r,size=7){ph8Text(g,text,r[0]+r[2]/2,r[1]+r[3]/2,size,r[2]-2);}
function ph8Fill(g,f,well,frac,col){const r=f.rect[well],a=f.a,src=well==='special'?a.special:well==='somer'?a.somer:a.roll;
 const k=Number.isFinite(frac)?clamp(frac,0,1):0;if(!k)return;
 g.save();g.beginPath();g.rect(r[0],r[1],r[2]*k,r[3]);g.clip();
 g.drawImage(f.source,col==='red'?a.redX:a.greenX,src[1]-a.sourceY,4,src[3],...r);g.restore();
}
function ph8Weapon(){const lv=spaceWeaponsActive()?spaceWeaponLevel():clamp(run.wlevel||1,1,8);
 if(cf1004Primary()&&lv>=6){const label=lv>=8?'FUSION':lv>=7?'BLACK/HOMING':'YELLOW LASER';return{reel:lv>=8?'fusion':lv>=7?'black':'yellow',lv,label};}
 return{key:weaponIconKey(run.weapon,lv),lv,label:spaceWeaponsActive()?spaceWeaponName():''};}
function ph8Values(){const active=!!(special&&special.pilot===run.pilot&&specialActive()),w=ph8Weapon();
 let name=pcSpecial(run.pilot).name,resource=active?clamp(special.t/Math.max(.001,special.dur),0,1):0,detail=active?Math.ceil(special.t)+'S':'NO SPECIAL';
 if(run.pilot==='yuri'&&run._thunderStormUnlocked)name='THUNDER STORM';
 if(active&&run.pilot==='falva')detail='BALL '+Math.round(clamp((special.charge||0)/FALVA_FULL,0,1)*100)+'%';
 if(active&&run.pilot==='juggernaut')detail='CHARGE '+Math.round(chargeLevel()*100)+'%';
 if(active&&(run.pilot==='cole'||run.pilot==='lizzie'))detail=(run.pilot==='cole'?'NUKES ':'A-BOMBS ')+(special.strikes||0);
 const loans=timedWeaponHUDRows().filter(q=>q.icon!=='nsw_icon_lizzie'||run.pilot==='lizzie');
 if(!active&&loans.length){name=loans[0].label||loans[0].name||'LOAN';resource=loans[0].frac;detail='TIMED WEAPON';}
 const lock=playerLocks.some(l=>(l.seat==null||l.seat===_seat)&&['arming','locked'].includes(l.state));
 return{seat:_seat,pilot:run.pilot,roll:clamp(1-(player._rollCool||0)/BR_COOL,0,1),
  rollAvailable:!(typeof lzMountActive==='function'&&lzMountActive()),somer:somersaultAvailable()?clamp(1-(player._somerCool||0)/SS_COOL,0,1):0,
  somerAvailable:somersaultAvailable(),name,resource,detail,weapon:w,lock,lives:run.lives,missiles:run.bombs,
  speed:clamp(run.speedLevel||0,0,5),shield:clamp(run.shield||0,0,5),dead:!!player.dead,score:run.score||0,loans};
}
function ph8Icon(g,key,x,y,h){if(!key)return;iconBlit(g,key,x,y,h,true);}
function ph8Pips(g,f,r,label,n,color){const q=f.rect[r];ph8Text(g,label,q[0]+1,q[1]+q[3]/2,6,q[2]*.44,'left');
 const start=q[0]+q[2]*.49,step=q[2]*.097,size=q[3]*.58;
 for(let i=0;i<5;i++){g.fillStyle=i<n?color:'#19202b';g.fillRect(Math.round(start+i*step),Math.round(q[1]+(q[3]-size)/2),Math.max(2,Math.floor(step-2)),size);}
}
function ph8Counter(g,r,label,key,count){const y=r[1]+r[3]/2;ph8Text(g,label,r[0]+1,y,7,r[2]*.48,'left');
 ph8Icon(g,key,r[0]+r[2]*.60,y,10);ph8Text(g,'X'+Math.max(0,count),r[0]+r[2]-1,y,7,r[2]*.29,'right');}
function ph8Radar(g,r){const x=r[0],y=r[1],w=r[2],h=r[3];g.save();g.beginPath();g.rect(x,y,w,h);g.clip();
 // UI reticles use the existing radar's world mapping, with actual units only.
 g.strokeStyle='#1e7937';g.lineWidth=.5;g.beginPath();g.moveTo(x+w/2,y);g.lineTo(x+w/2,y+h);g.moveTo(x,y+h/2);g.lineTo(x+w,y+h/2);g.stroke();
 const plot=(px,py,col,size)=>{if(!Number.isFinite(px)||!Number.isFinite(py))return;
  const dx=x+2+clamp((px-camLeftX())/Math.max(1,camRightX()-camLeftX()),0,1)*(w-4),dy=y+2+clamp((py-PLAY.y)/PLAY.h,0,1)*(h-4);
  g.fillStyle=col;g.fillRect(Math.round(dx-size/2),Math.round(dy-size/2),size,size);};
 for(const e of enemies)if(e&&!e.dead)plot(e.x,e.y,'#f95747',1.5);
 if(subBossActive&&subBoss&&!subBoss.dead)plot(subBoss.x,subBoss.y,'#ffa26a',2);
 if(bossActive&&boss&&!boss.dead){if(boss._rebels){for(const q of boss._rebels.ships)if(!q.dead&&q.hp>0&&!q.frCloak)plot(q.x,q.y,'#ff4444',2);}else plot(boss.x,boss.y,'#ff4444',2.5);}
 for(const seat of seatList()){const p=seatShip(seat);if(p&&!p.dead)plot(p.x,p.y,seat===_seat?'#8dff68':'#63dfff',2);}
 g.restore();
}
function ph8Score(n){return String(Math.max(0,Math.floor(Number(n)||0))).replace(/\B(?=(\d{3})+(?!\d))/g,',');}
function ph8Row(g,f,v){g.drawImage(f.canvas,0,0,VW,PH8.row);const r=f.rect;
 ph8Centered(g,v.rollAvailable?'ROLL':'ROLL LOCKED',r.rollLabel,7);ph8Fill(g,f,'roll',v.rollAvailable?v.roll:0,'green');
 ph8Centered(g,v.somerAvailable?'SOMERSAULT':'SOMERSAULT --',r.somerLabel,7);ph8Fill(g,f,'somer',v.somer,'green');
 ph8Centered(g,v.name,r.name,8);ph8Fill(g,f,'special',v.resource,'red');
 ph8Icon(g,specialArtKey('spicon_'+v.pilot),r.specialIcon[0]+r.specialIcon[2]/2,r.specialIcon[1]+r.specialIcon[3]/2,8);
 const wx=r.weapon[0]+r.weapon[2]/2,wy=r.weapon[1]+r.weapon[3]*.43;
 if(v.weapon.reel)cf1004Cell(v.weapon.reel,CF1004.clock,wx,wy,v.weapon.lv>=8?13:9,23,0,g);
 else ph8Icon(g,v.weapon.key,wx,wy,23);
 ph8Text(g,v.weapon.label||'L'+v.weapon.lv,r.weapon[0]+r.weapon[2]/2,r.weapon[1]+r.weapon[3]*.88,6,r.weapon[2]-1);
 ph8Pips(g,f,'speed','SPEED',v.speed,'#ffb838');ph8Pips(g,f,'shield','SHIELD',v.shield,'#3df1ff');
 const i={yuri:0,falva:1,cole:2,maverick:3,axel:4,juggernaut:5,lizzie:6,decker:7,freezer:8}[v.pilot]??0;
 ph8Counter(g,r.lives,'LIVES','nli_'+i,v.lives);ph8Counter(g,r.missiles,'MISSILES','nmi_'+i,v.missiles);
 ph8Radar(g,r.radar);
 const blink=v.lock&&Math.floor(performance.now()/(Math.max(.055,_lockHudGap)*1000))%2===0;
 // Keep the authored crosshair visible at rest; the live lock turns it red.
 if(XART.rdy('retm_0')){
  const ret=xartPalette('retm_0',v.lock?'#ff2929':'#b2c5d5')||XART.get('retm_0');
  const h=Math.min(12,r.lock[3]-2),w=h*ret.width/ret.height;
  g.drawImage(ret,r.lock[0]+8-w/2,r.lock[1]+(r.lock[3]-h)/2,w,h);
 }
 ph8Text(g,v.lock?'LOCK-ON!':'NO LOCK',r.lock[0]+r.lock[2]/2+8,r.lock[1]+r.lock[3]/2,8,r.lock[2]-20);
 if(blink){g.strokeStyle='#ff4a3e';g.lineWidth=1;g.strokeRect(r.lock[0],r.lock[1],r.lock[2],r.lock[3]);}
 g.fillStyle='#07101a';g.fillRect(0,PH8.row,VW,PH8.height-PH8.row);
 g.fillStyle='#263e50';g.fillRect(0,PH8.row,VW,.5);
 ph8Text(g,(PH8.rows>1?'P'+v.seat+' ':'')+v.pilot.toUpperCase()+' SCORE',6,79,7,150,'left');
 ph8Text(g,ph8Score(v.score),6,94,12,150,'left');
 ph8Text(g,'SPECIAL',VW/2,79,7,150);
 ph8Text(g,v.dead?'SHIP LOST':v.detail,VW/2,94,12,150);
 // Loans remain visible even while the native special is active: miniature
 // approved badges and independently draining strips inside its title window.
 if(v.loans.length){const width=Math.min(22,r.name[2]/v.loans.length);
  for(let i=0;i<v.loans.length;i++){const loan=v.loans[i],x=r.name[0]+i*width;
   ph8Icon(g,loan.icon,x+3,r.name[1]+r.name[3]-3,5);
   g.save();g.beginPath();g.rect(x+7,r.name[1]+r.name[3]-4,(width-8)*clamp(loan.frac,0,1),2);g.clip();
   g.drawImage(f.source,f.a.redX,f.a.special[1]-f.a.sourceY,4,f.a.special[3],x+7,r.name[1]+r.name[3]-4,width-8,2);g.restore();}}
 ph8Text(g,'HIGH SCORE',VW-6,79,7,150,'right');
 ph8Text(g,ph8Score(Math.max(v.score,highScore)),VW-6,94,12,150,'right');
}
drawHUDStrip=function(g){ph8Sync();g.save();g.setTransform(1,0,0,1,0,0);
 g.clearRect(0,0,VW*PH8.scale,PH8.height*PH8.rows*PH8.scale);g.scale(PH8.scale,PH8.scale);g.imageSmoothingEnabled=false;PH8.last=[];
 const f=ph8Frame(ph8Theme());if(!f){g.restore();return;}
 for(const seat of seatList())withSeat(seat,()=>{const v=ph8Values();g.save();g.translate(0,(seat-1)*PH8.height);ph8Row(g,f,v);g.restore();PH8.last.push(v);});PH8.draws++;g.restore();
};
drawHUDOverlay=function(){
 if(boss&&bossActive&&bossHealthVisible(boss))drawHealthBarV2('boss',bossHealthFraction(boss),VW/2,27,VW-44);
};
drawHealthBarV2=function(kind,frac,cx,cy,w,inWorld,lagKey){
 let frame=null;
 if(kind==='boss'||kind==='mini'){
  const b=kind==='boss'?boss:subBoss,sf=b?bossShieldFrac(b):null;
  frame=eh7Frame(eh7Theme(b),kind+(sf==null?'':'Shield'),w);
  // Keep the complete miniboss nameplate directly under the top assembly,
  // instead of the obsolete legacy tab offset that put it inside the fight.
  if(frame&&kind==='mini')cy=2+frame.h/2;
  if(frame&&kind==='mini'&&bossActive&&boss&&bossHealthVisible(boss)&&!boss._rebels)cy+=eh7Frame(eh7Theme(boss),'boss'+(bossShieldFrac(boss)==null?'':'Shield'),VW-44)?.h||0;
 }
 const result=PH8_BASE.bar.call(this,kind,frac,cx,cy,w,inWorld,lagKey);
 // The new housing still carries Dracodia's successive colored coronation
 // fills and the selected form's live pool. Reuse the authored legacy fill.
 if(result&&frame&&kind==='boss'&&j3State(boss)&&XART.rdy('bmbar_fill_solid')){
  const gauge=fmcGauge(boss),bar=EH7.lastBoss,well=frame.hp;
  const fill=(color,value)=>{if(!color||!(value>0))return;const im=xartPalette('bmbar_fill_solid',color);if(!im)return;
   ctx.save();ctx.beginPath();ctx.rect(bar.x+well[0],bar.y+well[1],well[2]*clamp(value,0,1),well[3]);ctx.clip();
   ctx.drawImage(im,bar.x+well[0],bar.y+well[1],well[2],well[3]);ctx.restore();};
  ctx.save();if(inWorld===true)ctx.translate(camX,0);fill(gauge.under,1);fill(gauge.color,gauge.frac);ctx.restore();
 }
 return result;
};
// The native-special and borrowed-weapon resource readouts now belong to the top row.
drawSpecialHUD=function(){};
drawHeavyTurretHUD=function(){};
// No HUD covers the ground anymore; the ordinary world pass owns those hazards.
hammerStormHudHazardDraw=function(){};
ph8Sync();window.BOFPlayerHUD=PH8;
