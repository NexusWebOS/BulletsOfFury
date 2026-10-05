'use strict';
/* Mike's approved large stage regions now sit over a connected authored continent.
   Original flags, blue ocean and clouds remain the live navigation system. */
const MAP4E={w:3200,h:2320,landH:3200*2/3,hub:[1625,1110],hq:[475,350],last:null,focus:false,hover:-1,
 sizes:{1:630,2:640,3:640,4:650,5:630,6:635,7:630,8:640,9:570,hub:700,hq:500},
 keys:[1,2,3,4,5,6,7,8,9,'hub','hq','islets'],
 islets:[{x:3000,y:1960,s:290},{x:280,y:1920,s:210},{x:1900,y:2210,s:210}],
 readiness:false,xPreview:false,xMouse:false,ships:new Map()};
Object.assign(SSEL_POS,{1:[740,640],2:[1540,510],3:[2180,590],4:[2600,1110],
 5:[2610,1690],6:[1640,1840],7:[660,1580],8:[470,1030],9:[2890,270]});
cmap2Order._o=null;
XART._src.map4e_landscape='assets/game/campaign_landscape_1004e/landscape.png';
for(const k of MAP4E.keys)for(const v of ['','_lock','_shadow','_glow'])
 XART._src['map4e_region_'+k+v]='assets/game/campaign_landscape_1004e/region_'+k+v+'.png';
for(const v of ['','_lock','_shadow','_glow'])
 XART._src['map4e_region_hq'+v]='assets/game/campaign_landscape_1004f/region_hq'+v+'.png';
for(const v of ['','_lock','_shadow','_glow'])
 XART._src['map4e_region_hub'+v]='assets/game/campaign_stagex_1004g/region_hub'+v+'.png';
for(const v of ['','_lock'])XART._src['map4f_flagx'+v]='assets/game/campaign_landscape_1004f/flag_x'+v+'.png';
const MAP4F_FLAG_STATES=['av','lock','hi0','hi1','done_gold','done_silver','done_green','white'];
for(let n=1;n<=9;n++)for(const v of MAP4F_FLAG_STATES)
 XART._src['map4f_flag'+n+'_'+v]='assets/game/campaign_landscape_1004f/flag_'+n+'_'+v+'.png';
function map4eWarm(){XART.rdy('map4e_landscape');for(const k of MAP4E.keys)
 for(const v of ['','_lock','_shadow','_glow'])XART.rdy('map4e_region_'+k+v);XART.rdy('map4f_flagx');XART.rdy('map4f_flagx_lock');
 if(Rival24.mapAvailable)for(const key of ['gp4_ace_top',...REBEL_SHIPS.map(k=>'rr_ship_'+k)])XART.rdy(key);
 for(let n=1;n<=9;n++)for(const v of MAP4F_FLAG_STATES)XART.rdy('map4f_flag'+n+'_'+v);
}
const MAP4E_BASE={warm:cmap2Warm,reset:cmap2Reset,world:cmap2World};
cmap2Warm=function(){MAP4E_BASE.warm.apply(this,arguments);map4eWarm();};
cmap2World=function(k){return k==='hub'?{x:MAP4E.hub[0],y:MAP4E.hub[1]}:
 k==='hq'?{x:MAP4E.hq[0],y:MAP4E.hq[1]}:MAP4E_BASE.world(k);};
cmap2Size=function(k){return MAP4E.sizes[k]||630;};
// Favor landmarks along the horizontal travel direction. Pure nearest-distance
// selection bounced between the two eastern nodes and stranded the south coast.
sselMoveHorizontal=function(dir,lo,hi,from){const cur=from==null?sselCursor:from,p=SSEL_POS[cur];
 if(!p||!dir)return cur;let best=cur,score=Infinity;
 for(let k=lo;k<=hi;k++){const q=SSEL_POS[k];if(k===cur||!q)continue;
  const dx=q[0]-p[0],dy=q[1]-p[1];if(dx*dir<=0)continue;
  const distance=Math.hypot(dx,dy)+Math.abs(dy)*1.25;
  if(distance<score){best=k;score=distance;}}
 return best;
};
cmap2FitZ=function(){return map30Overview().z;};
cmap2Clamp=function(p,z){
 const hw=campaignViewWidth()/2/z,hh=(CM2_BAND_BOT-CM2_BAND_TOP)/2/z;
 return {x:MAP4E.w>2*hw?clamp(p.x,hw-100,MAP4E.w-hw+100):MAP4E.w/2,
  y:MAP4E.h>2*hh?clamp(p.y,hh-80,MAP4E.h-hh+80):MAP4E.h/2};
};
// The whole continent fits above progression and the briefing. It is visible
// after the boot zoom; a new selected region then pulls the camera closer.
map30Overview=function(){return {x:MAP4E.w/2,y:1135,
 z:Math.min((campaignViewWidth()-150)/MAP4E.w,(CM2_BAND_BOT-CM2_BAND_TOP-16)/MAP4E.landH)};};
cmap2Reset=function(opts){const r=MAP4E_BASE.reset.apply(this,arguments);
 MAP4E.last=sselCursor;MAP4E.focus=!!(opts?.unlock||opts?.bonusUnlock);MAP4E.readiness=false;MAP4E.xPreview=false;MAP4E.xMouse=false;
 cmap2.clouds=null;const t=map30Overview();cmap2.cam={...t,z:t.z*(opts?.boot ? .72 : 1)};return r;};
cmap2Frame=function(a,b){const p=cmap2World(a),q=cmap2World(b);if(!p||!q)return map30Overview();
 const margin=Math.max(cmap2Size(a),cmap2Size(b));
 return {x:(p.x+q.x)/2,y:(p.y+q.y)/2,z:Math.min(.34,
  (campaignViewWidth()-170)/(Math.abs(p.x-q.x)+margin+150),
  (CM2_BAND_BOT-CM2_BAND_TOP-24)/(Math.abs(p.y-q.y)+margin*.8+150))};
};
cmap2CameraTick=function(dt,cine,selected){
 map4eWarm();const ready=XART.rdy('map4e_landscape')&&MAP4E.keys.every(k=>XART.rdy('map4e_region_'+k));
 MAP4E.readiness=ready;
 if(selected!==MAP4E.last&&sselBoot===0){MAP4E.focus=true;MAP4E.last=selected;}
 let t=map30Overview();
 if(sselBoot>0){const u=clamp((sselBootT-1.7)/3.2,0,1),e=u*u*(3-2*u);t.z*=lerp(.72,1,e);}
 else if(s9MapCine||riftReturn)t=cmap2Frame(5,9);
 else if(Rival24.flying)t=cmap2Frame(6,'hub');
 else if(Rival24.mapFocused||MAP4E.xPreview){const p=cmap2World('hub');t={x:p.x,y:p.y-150,z:.31};}
 else if(Rival24.mapAvailable&&[6,7].includes(selected))t=cmap2Frame(selected,'hub');
 else if(cine||selected===9||MAP4E.focus){const p=cmap2World(cine?.stage||selected);
  if(p)t={...p,z:Math.min(.33,(CM2_BAND_BOT-CM2_BAND_TOP-42)/(cmap2Size(cine?.stage||selected)*.85))};}
 if(cmap2.focus==='bar'&&!cine&&!s9MapCine&&!riftReturn)t=map30Overview();
 const ease=1-Math.exp(-Math.max(0,dt)*(sselBoot>0?4:2.6));
 for(const k of ['x','y','z'])cmap2.cam[k]+=(t[k]-cmap2.cam[k])*ease;
};
function map4eBlit(key,x,y,s,alpha=1){if(!XART.rdy(key))return false;
 ctx.save();ctx.globalAlpha=alpha;ctx.drawImage(XART.get(key),x-s/2,y-s/2,s,s);ctx.restore();return true;}
// One live pose owns the floating city, its flag, pointer bounds and encounter
// orbits. The ground anchor remains fixed for campaign geography and cameras.
function map4eHubPose(){const p=cmap2World('hub'),lift=cmap2.lift.hub||0;
 return {x:p.x,y:p.y-110-28*lift+Math.sin(cmap2.t*.9)*9,s:cmap2Size('hub')};}
function map4eStageXAt(mx,my){if(my<CM2_BAND_TOP||my>=CM2_BAND_BOT)return false;
 const p=map4eHubPose(),q=cmap2ToScreen(p.x,p.y),s=p.s*cmap2.cam.z;
 return Math.abs(mx-q.x)<s*.44&&Math.abs(my-q.y)<s*.4;}
fr27CoreMapPosition=function(){const p=map4eHubPose();return cmap2ToScreen(p.x,p.y-80);};
function map4eRegion(k){const p=cmap2World(k),s=cmap2Size(k),lift=cmap2.lift[k]||0;
 if(k==='hub'){const q=map4eHubPose(),key='map4e_region_hub';
  if(XART.rdy(key+'_shadow')){ctx.save();ctx.globalAlpha=.52;ctx.drawImage(XART.get(key+'_shadow'),p.x-s/2,p.y+40-s*.14,s,s*.28);ctx.restore();}
  if(lift>.01)map4eBlit(key+'_glow',q.x,q.y,s,lift*.3);
  map4eBlit(key,q.x,q.y,s);return;
 }
 const y=p.y+cmap2Bob(k==='hq'?0:k)-4*lift,prefix='map4e_region_'+k;
 map4eBlit(prefix+'_shadow',p.x+8+4*lift,p.y+18+10*lift,s,.4-.1*lift);
 if(lift>.01)map4eBlit(prefix+'_glow',p.x,y,s,lift*.4);
 // Locked regions retain their authored biomes; the existing gray flag conveys
 // the lock. This makes the entire theater legible from the first map load.
 map4eBlit(prefix,p.x,y,s);
}
cmap2DrawWorld=function(dt,selected){
 ctx.save();ctx.imageSmoothingEnabled=false;
 if(XART.rdy('map4e_landscape'))ctx.drawImage(XART.get('map4e_landscape'),0,70,3200,3200*2/3);
 for(const q of MAP4E.islets)map4eBlit('map4e_region_islets',q.x,q.y+Math.sin(cmap2.t*.7+q.x)*3,q.s);
 const m=Input.mouse||{};MAP4E.hover=sselBoot===0&&m.active&&m.moved?
  (map4eStageXAt(m.x,m.y)?'hub':cmap2IslandAt(m.x,m.y,1,9)):-1;
 for(const k of CM2_ISLANDS){const want=(k===selected||k===MAP4E.hover||k==='hub'&&(Rival24.mapFocused||MAP4E.xPreview))&&sselBoot===0?1:0;
  cmap2.lift[k]=(cmap2.lift[k]||0)+(want-(cmap2.lift[k]||0))*Math.min(1,dt*7);}
 const order=[...CM2_ISLANDS,'hq'].sort((a,b)=>cmap2World(a).y-cmap2World(b).y);
 // The cosmic coast remains visible before the Stage 5 gate unlock. Only the
 // original portal navigation/cinematic controls allow its deployment.
 for(const k of order)map4eRegion(k);
 if(sselBoot===0)map4eStageXMarker();
 ctx.restore();cmap2DrawClouds(selected);
};
cmap2DrawClouds=function(selected){
 if(!cmap2.clouds)cmap2.clouds=Array.from({length:16},(_,i)=>({i:i%7,
  x:cmap2Rand(i*3+5)*(MAP4E.w+400)-200,y:80+cmap2Rand(i*7+9)*(MAP4E.h-80),sp:5+cmap2Rand(i*11+1)*6}));
 const c=cmap2.cam,span=MAP4E.w+400;ctx.save();ctx.imageSmoothingEnabled=false;
 const p=cmap2World(selected),size=cmap2Size(selected);
 for(const shadow of [true,false])for(const q of cmap2.clouds){
  const key='cm2_cloud_'+q.i+(shadow?'_shadow':'');if(!XART.rdy(key))continue;
  const im=XART.get(key),w=im.width*.85,h=im.height*.85;
  const x=((q.x+cmap2.t*q.sp+200)%span+span)%span-200,y=q.y;
  const hub=map4eHubPose(),near=(p?Math.hypot(x-p.x,(y-p.y)*1.2)<size*.5:false)||
   Math.hypot(x-hub.x,(y-hub.y)*1.2)<hub.s*.55;
  ctx.globalAlpha=shadow?.13:(near?.25:.75);
  ctx.drawImage(im,x-w/2+(shadow?26:0),y-h/2+(shadow?32:0),w,h);
 }ctx.restore();
};
// Island picking follows the live lifted landmark, rather than the terrain
// underlay. The Stage 9 unlock gate is still owned by the original input code.
cmap2IslandAt=function(mx,my,lo,hi){if(my<CM2_BAND_TOP||my>=CM2_BAND_BOT)return -1;
 for(let k=hi;k>=lo;k--){const p=cmap2World(k);if(!p)continue;
  const s=cmap2ToScreen(p.x,p.y+cmap2Bob(k)),w=cmap2Size(k)*cmap2.cam.z;
  if(Math.abs(mx-s.x)<w*.43&&Math.abs(my-s.y)<w*.31)return k;}
 return -1;
};
// Remove the obsolete western data barrier hit strip from the expanded local
// geography. It remains beyond this world, with no new expansion stage unlock.
MAP30.westX=-10000;

// A real flag plants Stage X in the city even before an encounter is available.
// Its lock is informational; neither visiting it nor confirming unlocks a fight.
function map4eStageXPoint(){const p=map4eHubPose();return {x:p.x,y:p.y+55};}
function map4eStageXMarker(){
 const p=map4eStageXPoint(),key='map4f_flagx'+(Rival24.mapAvailable?'':'_lock');
 if(!XART.rdy(key))return;const im=XART.get(key),z=Math.max(.05,cmap2.cam.z);
 const h=(Rival24.mapFocused||MAP4E.xPreview?31:25)/z,w=h*im.width/im.height;
 const anchor=typeof MAP4F_X_ANCHOR!=='undefined'?MAP4F_X_ANCHOR:[.5,1];
 ctx.drawImage(im,p.x-w*anchor[0],p.y-h*anchor[1],w,h);
}
const MAP4E_X={draw:Rival24.mapDraw,input:Rival24.mapInput,back:Rival24.mapBack};
const map4eXFocused=Object.getOwnPropertyDescriptor(Rival24,'mapFocused').get;
Object.defineProperty(Rival24,'mapFocused',{get(){return MAP4E.xPreview||map4eXFocused.call(Rival24);}});
Rival24.mapDraw=function(dt){const r=MAP4E_X.draw.apply(this,arguments);
 if(MAP4E.xPreview&&!Rival24.mapAvailable)mapgBriefingDraw({key:'map4f-x-locked',title:'STAGE X',
  body:'THE CENTRAL CITY. COMPLETE STAGE 6 TO PURSUE THE HARRIER OR CHALLENGE THE REBEL FIGHTERS HERE.'});return r;
};
Rival24.mapInput=function(){
 if(Rival24.mapAvailable){MAP4E.xPreview=false;return MAP4E_X.input.apply(this,arguments);}
 if(sselBoot>0)return MAP4E_X.input.apply(this,arguments);
 const m=Input.mouse||{},p=map4eStageXPoint(),q=cmap2ToScreen(p.x,p.y),hit=map4eStageXAt(m.x,m.y)||Math.abs(m.x-q.x)<19&&m.y>q.y-34&&m.y<q.y+7;
 const click=m.down&&!MAP4E.xMouse;MAP4E.xMouse=!!m.down;
 if(click&&hit){MAP4E.xPreview=true;Audio.SFX.blip();return true;}
 if(MAP4E.xPreview){
  if(Input.menuBack()||Input.menuUp()){MAP4E.xPreview=false;Audio.SFX.blip();return true;}
  if(Input.menuConfirm()){Audio.SFX.blip();return true;}
  if(Input.menuLeft()){MAP4E.xPreview=false;Input.injectTap(keybind.left[0]);return false;}
  if(Input.menuRight()){MAP4E.xPreview=false;Input.injectTap(keybind.right[0]);return false;}
  return true;
 }
 return MAP4E_X.input.apply(this,arguments);
};
Rival24.mapBack=function(){if(MAP4E.xPreview&&Input.menuBack()){MAP4E.xPreview=false;return true;}return MAP4E_X.back.apply(this,arguments);};

// Keep the approved pilot hull and bake each cardinal heading once. The three
// requested vertical legs hold their heading after arrival, so terrain bobbing
// never makes the hull pivot back and forth.
function map4eShipHeading(from,to,dx){
 if(from===4&&to===5)return Math.PI;
 if(from===7&&to===8||from===8&&to===1)return 0;
 return dx<0?-Math.PI/2:Math.PI/2;
}
sselShipUpdate=function(dt){
 if(sselBoot>0)return;const atX=typeof map4hXFocused==='function'&&map4hXFocused(),cursor=atX?'x':sselCursor;
 const dest=atX?map4eStageXPoint():sselFlagXY(sselCursor);if(!dest)return;
 if(!sselShip){const first=sselFlagXY(1)||dest;sselShip={x:-70,y:first.y,tx:first.x,ty:first.y,t:0,phase:'flyin',bank:0,trail:0,cur:1,head:Math.PI/2,face:1};}
 const sh=sselShip;sh.t+=dt;
 if(sh.cur!==cursor){
  sh.head=map4eShipHeading(sh.cur,cursor,dest.x-sh.x);
  if(sh.cur!=null&&Audio.SFX.mapMove)Audio.SFX.mapMove();sh.cur=cursor;
 }
 if(!Number.isFinite(sh.head))sh.head=Math.PI/2;
 sh.face=sh.head<0?-1:1;sh.tx=dest.x;sh.ty=dest.y;
 const dx=dest.x-sh.x,dy=dest.y-sh.y,d=Math.hypot(dx,dy),k=sh.phase==='flyin'?.055:.075;
 sh.x+=dx*Math.min(1,dt*60*k);sh.y+=dy*Math.min(1,dt*60*k);sh.bank=0;
 if(sh.phase==='flyin'&&d<4)sh.phase='idle';sh.moving=d>3;sh.trail-=dt;
 if(sh.moving&&sh.trail<=0){sh.trail=.03;
  const ux=Math.sin(sh.head),uy=-Math.cos(sh.head);
  particles.push({x:sh.x-ux*17,y:sh.y-uy*17,vx:-ux*.35+rnd(-.2,.2),vy:-uy*.35+rnd(-.2,.2),life:rnd(.18,.36),t:0,r:rnd(1,2.2),color:d>90?'#ffd27a':'#8fd0ff'});
 }
};
function map4eShipFrame(key,heading){
 const id=key+':'+heading;if(MAP4E.ships.has(id))return MAP4E.ships.get(id);if(!XART.rdy(key))return null;
 const im=XART.get(key),w=im.naturalWidth||im.width,h=im.naturalHeight||im.height,side=Math.abs(Math.sin(heading))>.5;
 const c=document.createElement('canvas');c.width=side?h:w;c.height=side?w:h;
 const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.translate(c.width/2,c.height/2);g.rotate(heading);g.drawImage(im,-w/2,-h/2,w,h);
 c.naturalWidth=c.width;c.naturalHeight=c.height;MAP4E.ships.set(id,c);return c;
}
sselShipDraw=function(){
 if(!sselShip)return;const sh=sselShip,pk=typeof _pilotKey==='function'?_pilotKey():run.pilot||'cole';
 const im=map4eShipFrame('ship_'+pk,sh.head)||map4eShipFrame('ship_cole',sh.head);if(!im)return;
 const size=29/(cmap2On()?Math.max(.25,cmap2.cam.z):1),scale=size/Math.max(im.width,im.height);
 const w=im.width*scale,h=im.height*scale;ctx.save();ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,sh.x-w/2,sh.y-h/2,w,h);ctx.restore();
};

// Authored Roman numerals share the approved X flag's chrome mast and frame.
// Locks, ranks and unlock timing retain their existing campaign state owners.
function map4fFlagDraw(st,dt,cine){
 const available=st===9?!!campaign.bonusUnlocked:st<=campaign.unlockedMax;
 const selected=available&&st===sselCursor&&sselBoot===0;
 const rank=campaign.rank[st];let v=!available?'lock':selected?'hi'+(((stateT*6)|0)%2):rank?'done_'+rankFlagColor(rank):'av';
 if(cine?.stage===st&&cine.phase==='ding'&&((cine.t*12)|0)%2)v='white';
 const key='map4f_flag'+st+'_'+v;if(!XART.rdy(key))return false;
 const p=sselFlagXY(st);if(!p)return false;const im=XART.get(key),z=cmap2On()?Math.max(.05,cmap2.cam.z):1;
 const h=28/z,w=h*im.width/im.height;
 let drop=0;if(sselBoot>0){const age=sselBootT-(4.05+(st-1)*.2);if(age>=0&&age<.18)drop=-(1-age/.18)*14/z;}
 const anchor=typeof MAP4F_FLAGS!=='undefined'?MAP4F_FLAGS[st].anchor:[.5,1];
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,p.x-w*anchor[0],p.y-h*anchor[1]+drop,w,h);ctx.restore();
 return true;
}
const MAP4F_BONUS_DRAW=s9MapDraw;
s9MapDraw=function(){const r=MAP4F_BONUS_DRAW.apply(this,arguments);
 if(sselBoot===0)map4fFlagDraw(9,0,s9MapCine&&{stage:9,phase:s9MapCine.ph==='flash'?'ding':s9MapCine.ph,t:s9MapCine.t});return r;
};
map4eWarm();
