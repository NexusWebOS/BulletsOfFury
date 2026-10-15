"use strict";
/* October 10 audio: raised counters, generous wells, radar beside the score.
   UI reads seat state; it does not advance combat or replace weapon geometry. */
const AP10_UI={base:{frame:ph8Frame,row:ph8Row,fill:ph8Fill,load:stageLoadBegin},cache:new Map()};
XART._src[AP10_HUD_ART.key]=AP10_HUD_ART.path;
PH8.row=96;PH8.height=136;
FB9_HUD.ROW=136;FB9_HUD.HOUSE=96;
window.__bofHudSeatHeight=PH8.height;window.__bofHudHouseHeight=PH8.row;
stageLoadBegin=function(n,keys){return AP10_UI.base.load.call(this,n,[...(keys||[]),AP10_HUD_ART.key]);};
ph8Frame=function(theme){
 if(AP10_UI.cache.has(theme))return AP10_UI.cache.get(theme);
 if(!XART.rdy(AP10_HUD_ART.key))return null;
 const source=XART.get(AP10_HUD_ART.key),canvas=document.createElement('canvas');
 canvas.width=VW*PH8.scale;canvas.height=PH8.row*PH8.scale;
 const g=canvas.getContext('2d');g.imageSmoothingEnabled=false;g.drawImage(source,0,0,canvas.width,canvas.height);
 const rect={lives:[20,12,66,14],missiles:[388,12,67,14],rollLabel:[24,37,72,8],roll:[22,45,73,7],
  somerLabel:[24,61,72,8],somer:[22,69,73,7],weapon:[113,30,46,48],name:[176,35,180,13],
  specialIcon:[178,36,12,12],special:[177,55,180,9],speed:[176,71,78,10],shield:[276,71,78,10],
  lock:[377,34,81,40],radar:[VW/2-15,PH8.row+4,30,30]};
 const f={canvas,source,a:AP10_HUD_ART,rect};AP10_UI.cache.set(theme,f);return f;
};
ph8Fill=function(g,f,well,frac,col){
 if(f.a!==AP10_HUD_ART)return AP10_UI.base.fill.apply(this,arguments);
 const r=f.rect[well],k=Number.isFinite(frac)?clamp(frac,0,1):0;if(!k)return;
 // Meter pixels come from the existing authored HUD; no illustrative values.
 const a=PH8_ART[ph8Theme()]||PH8_ART.stage_01;if(!XART.rdy(a.key))return;
 const src=well==='special'?a.special:well==='somer'?a.somer:a.roll;
 g.save();g.beginPath();g.rect(r[0],r[1],r[2]*k,r[3]);g.clip();
 g.drawImage(XART.get(a.key),col==='red'?a.redX:a.greenX,src[1]-a.sourceY,4,src[3],...r);g.restore();
};
ph8Row=function(g,f,v){
 if(f.a!==AP10_HUD_ART)return AP10_UI.base.row.apply(this,arguments);
 const r=f.rect;g.drawImage(f.canvas,0,0,VW,PH8.row);
 ph8Counter(g,r.lives,'LIVES','nli_'+({yuri:0,falva:1,cole:2,maverick:3,axel:4,juggernaut:5,lizzie:6,decker:7,freezer:8}[v.pilot]??0),v.lives);
 ph8Counter(g,r.missiles,'MISSILES','nmi_'+({yuri:0,falva:1,cole:2,maverick:3,axel:4,juggernaut:5,lizzie:6,decker:7,freezer:8}[v.pilot]??0),v.missiles);
 ph8Centered(g,v.rollAvailable?'ROLL':'ROLL LOCKED',r.rollLabel,8);ph8Fill(g,f,'roll',v.rollAvailable?v.roll:0,'green');
 ph8Centered(g,v.somerAvailable?'SOMERSAULT':'SOMERSAULT --',r.somerLabel,8);ph8Fill(g,f,'somer',v.somer,'green');
 const wx=r.weapon[0]+r.weapon[2]/2,wy=r.weapon[1]+r.weapon[3]*.42;
 if(v.weapon.reel)cf1004Cell(v.weapon.reel,CF1004.clock,wx,wy,14,26,0,g);
 else if(typeof p2HudWeaponIcon==='function')p2HudWeaponIcon(g,v.weapon.key,wx,wy,27);
 else ph8Icon(g,v.weapon.key,wx,wy,27);
 ph8Text(g,v.weapon.label||'L'+v.weapon.lv,wx,r.weapon[1]+r.weapon[3]*.87,8,r.weapon[2]-2);
 ph8Text(g,v.name,r.name[0]+r.name[2]/2+5,r.name[1]+r.name[3]/2,9,r.name[2]-22);
 ph8Icon(g,specialArtKey('spicon_'+v.pilot),r.specialIcon[0]+6,r.specialIcon[1]+6,10);
 ph8Fill(g,f,'special',v.resource,'red');
 ph8Pips(g,f,'speed','SPEED',v.speed,'#ffb838');ph8Pips(g,f,'shield','SHIELD',v.shield,'#3df1ff');
 if(XART.rdy('retm_0')){const im=xartPalette('retm_0',v.lock?'#ff2929':'#b2c5d5')||XART.get('retm_0');
  const h=15,w=h*im.width/im.height;g.drawImage(im,r.lock[0]+r.lock[2]/2-w/2,r.lock[1]+4,w,h);}
 ph8Text(g,v.lock?'LOCK-ON!':'NO LOCK',r.lock[0]+r.lock[2]/2,r.lock[1]+30,9,r.lock[2]-4);
 if(v.lock&&Math.floor(performance.now()/130)%2===0){g.strokeStyle='#ff4a3e';g.lineWidth=1;g.strokeRect(...r.lock);}
 g.fillStyle='#07101a';g.fillRect(0,PH8.row,VW,PH8.height-PH8.row);
 ph8Text(g,(PH8.rows>1?'P'+v.seat+' ':'')+v.pilot+' SCORE',6,PH8.row+10,8,160,'left');
 ph8Text(g,ph8Score(v.score),6,PH8.row+27,13,160,'left');
 // The exact existing radar mapping follows each seat, now in the top strip.
 ph8Radar(g,r.radar);
 ph8Text(g,'HIGH SCORE',VW-6,PH8.row+10,8,150,'right');
 ph8Text(g,ph8Score(Math.max(v.score,highScore)),VW-6,PH8.row+27,13,150,'right');
 ph8Text(g,v.dead?'SHIP LOST':v.detail,180,PH8.row+28,7,80,'center');
 if(v.loans.length)for(let i=0;i<v.loans.length;i++){
  const loan=v.loans[i],x=r.name[0]+i*28;ph8Icon(g,loan.icon,x+5,r.special[1]+r.special[3]/2,9);
 }
};
ph8Sync();
