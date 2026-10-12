"use strict";
/* Approved Armored Command. Complete proportional authored bands; live seat state.
   The offscreen row remains [bottom, top] for the shared HUD splitter. */
const AC11={base:{load:stageLoadBegin,retire:bofDerivedCachesRetire},frame:null,draws:0,last:[]};
XART._src[AC11_ART.key]=AC11_ART.path;
PH8.row=AC11_ART.bottom;PH8.height=AC11_ART.bottom+AC11_ART.top;
FB9_HUD.ROW=PH8.height;FB9_HUD.HOUSE=PH8.row;
window.__bofHudSeatHeight=PH8.height;window.__bofHudHouseHeight=PH8.row;
stageLoadBegin=function(n,keys){return AC11.base.load.call(this,n,[...(keys||[]),AC11_ART.key]);};
bofDerivedCachesRetire=function(){AC11.frame=null;return AC11.base.retire.apply(this,arguments);};
ph8Frame=function(){
 if(AC11.frame)return AC11.frame;
 if(!XART.rdy(AC11_ART.key))return null;
 const source=XART.get(AC11_ART.key),canvas=document.createElement('canvas');
 canvas.width=VW*PH8.scale;canvas.height=PH8.height*PH8.scale;
 const g=canvas.getContext('2d');g.scale(PH8.scale,PH8.scale);g.imageSmoothingEnabled=false;
 const rect={};
 for(let i=0;i<2;i++){
  const band=AC11_ART.bands[i],sw=band[2]-band[0],sh=band[3]-band[1],k=VW/sw;
  const bh=i?PH8.row:AC11_ART.top,y=(i?0:PH8.row)+(bh-sh*k)/2;
  g.drawImage(source,band[0],band[1],sw,sh,0,y,VW,sh*k);
  for(const [key,r] of Object.entries(AC11_ART.wells))if(r[1]>=band[1]&&r[1]+r[3]<=band[3])
   rect[key]=[(r[0]-band[0])*k,y+(r[1]-band[1])*k,r[2]*k,r[3]*k];
 }
 return AC11.frame={canvas,source,a:AC11_ART,rect};
};
function ac11Meter(g,r,fraction,col){
 const a=PH8_ART[ph8Theme()]||PH8_ART.stage_01;if(!a||!XART.rdy(a.key))return;
 const k=clamp(Number(fraction)||0,0,1);if(!k)return;
 const src=col==='red'?a.special:a.roll;
 g.save();g.beginPath();g.rect(r[0],r[1],r[2]*k,r[3]);g.clip();
 g.drawImage(XART.get(a.key),col==='red'?a.redX:a.greenX,src[1]-a.sourceY,4,src[3],...r);g.restore();
}
function ac11Counter(g,r,label,key,count){
 const [x,y,w,h]=r,cy=y+h/2,n=String(Math.max(0,count|0)).padStart(2,'0');
 ph8Text(g,label,x+3,cy,11,w*.42,'left');ph8Icon(g,key,x+w*.57,cy,24);
 ph8Text(g,'X',x+w*.69,cy,10,w*.06);ph8Text(g,n,x+w-4,cy,24,w*.26,'right');
 if(count<=1){g.fillStyle=count<=0?'#ff4149':'#ffb345';g.fillRect(x+2,y+h-2,w-4,1);}
}
function ac11Maneuver(g,r,label,frac){
 ph8Text(g,label,r[0]+r[2]/2,r[1]+7,10,r[2]-6);
 ac11Meter(g,[r[0]+4,r[1]+r[3]-9,r[2]-8,6],frac,'green');
}
ph8Row=function(g,f,v){
 const r=f.rect;g.drawImage(f.canvas,0,0,VW,PH8.height);
 for(const [key,label,value] of [['score',(PH8.rows>1?'P'+v.seat+' ':'')+v.pilot+' SCORE',v.score],['high','HIGH SCORE',Math.max(v.score,highScore)]]){
  const q=r[key];ph8Text(g,label,q[0]+3,q[1]+q[3]/2,8,q[2]*.46,'left');
  ph8Text(g,ph8Score(value),q[0]+q[2]-3,q[1]+q[3]/2,14,q[2]*.51,'right');
 }
 const i={yuri:0,falva:1,cole:2,maverick:3,axel:4,juggernaut:5,lizzie:6,decker:7,freezer:8}[v.pilot]??0;
 ac11Counter(g,r.lives,'LIVES','nli_'+i,v.lives);ac11Counter(g,r.missiles,'MISSILES','nmi_'+i,v.missiles);
 ac11Maneuver(g,r.roll,v.rollAvailable?'ROLL':'ROLL LOCKED',v.rollAvailable?v.roll:0);
 ac11Maneuver(g,r.somer,v.somerAvailable?'SOMERSAULT':'SOMERSAULT --',v.somer);
 const w=r.weapon,wx=w[0]+w[2]/2,wy=w[1]+w[3]*.40;
 if(v.weapon.reel)cf1004Cell(v.weapon.reel,CF1004.clock,wx,wy,20,40,0,g);
 else p2HudWeaponIcon(g,v.weapon.key,wx,wy,40);
 const words=v.weapon.label?.split(' ');
 if(words?.length){for(let i=0;i<Math.min(2,words.length);i++)ph8Text(g,words[i],wx,w[1]+w[3]*.77+i*9,8,w[2]-3);}
 else ph8Text(g,'L'+v.weapon.lv,wx,w[1]+w[3]*.82,10,w[2]-3);
 const s=r.special;ph8Icon(g,specialArtKey('spicon_'+v.pilot),s[0]+9,s[1]+8,16);
 ph8Text(g,v.name,s[0]+22,s[1]+6,9,s[2]-25,'left');
 ph8Text(g,v.dead?'SHIP LOST':v.detail,s[0]+22,s[1]+16,8,s[2]-25,'left');
 ac11Meter(g,[s[0]+3,s[1]+s[3]-6,s[2]-6,4],v.resource,'red');
 const lk=r.lock;
 if(XART.rdy('retm_0')){const im=xartPalette('retm_0',v.lock?'#ff2929':'#b2c5d5')||XART.get('retm_0'),h=23,iw=h*im.width/im.height;
  g.drawImage(im,lk[0]+15-iw/2,lk[1]+lk[3]/2-h/2,iw,h);}
 ph8Text(g,v.lock?'LOCK-ON!':'NO LOCK',lk[0]+lk[2]-5,lk[1]+lk[3]/2,12,lk[2]-36,'right');
 if(v.lock&&Math.floor(performance.now()/130)%2===0){g.strokeStyle='#ff4a3e';g.lineWidth=1;g.strokeRect(lk[0]+1,lk[1]+1,lk[2]-2,lk[3]-2);}
 for(const [key,n,col] of [['speed',v.speed,'#ffb838'],['shield',v.shield,'#3df1ff']]){
  const q=r[key];ph8Text(g,key,q[0]+2,q[1]+q[3]/2,8,q[2]*.43,'left');
  const step=q[2]*.105;for(let j=0;j<5;j++){g.fillStyle=j<n?col:'#19202b';g.fillRect(q[0]+q[2]*.45+j*step,q[1]+2,step-2,q[3]-4);}
 }
 // Timed weapon loans retain their own badge and resource beside the native special.
 for(let j=0;j<v.loans.length;j++){const q=v.loans[j],x=w[0]+j*14;ph8Icon(g,q.icon,x+6,w[1]+w[3]-1,10);ac11Meter(g,[x+1,w[1]+w[3]+6,10,2],q.frac,'red');}
 AC11.draws++;AC11.last.push({seat:v.seat,lives:v.lives,missiles:v.missiles,score:v.score});if(AC11.last.length>2)AC11.last.shift();
};
ph8Sync();
