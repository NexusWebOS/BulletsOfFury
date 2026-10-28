'use strict';
/* Approved Command Armor. State is read-only; source templates remain reusable. */
const UI20={style:'a',base:{dlg:dlgBox,frame:dialogueFrameDraw,load:stageLoadBegin,touch:XART._touch},draws:0,last:[],cache:new Map(),dirty:true};
const UI20_ROOT='assets/game/shared/ui/command_1020/';
for(const n of ['hud-a-left','hud-a-right','dialogue-a'])XART._src['ui20_'+n]=UI20_ROOT+n+'.webp';
for(const n of ['neutral','report','horror','talk'])XART._src['ui20_cole-'+n]='assets/game/pilots/cole/body_frames/front_identity_1020/cole-'+n+'.webp';
const UI20_KEYS=['hud-a-left','hud-a-right','dialogue-a'].map(n=>'ui20_'+n);
UI20.pilot=k=>PILOTS.find(p=>p.key===String(k).toLowerCase()||p.name===String(k).toUpperCase());
UI20.color=k=>UI20.pilot(k)?.tint||dialogueNameColor(k,'#b98cff');
UI20.warm=()=>{for(const k of UI20_KEYS)XART.rdy(k);};
UI20.base.pose=inv20Pose;
inv20Pose=function(pk,x,bottom,height,t=0,horror=false){if(pk!=='cole')return UI20.base.pose.apply(this,arguments);const key='ui20_cole-'+(horror?'horror':'report');if(!XART.rdy(key))return UI20.base.pose.apply(this,arguments);const k=height/704,cx=Math.max(x,256*k+6);ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(key),0,0,512,704,cx-256*k,bottom-height,512*k,height);ctx.restore();INV20.draws[key]=(INV20.draws[key]||0)+1;CE20.draws[key]=(CE20.draws[key]||0)+1;return {pilot:pk,key,x:cx,bottom,height,horror};};
stageLoadBegin=function(n,keys){return UI20.base.load.call(this,n,[...new Set([...(keys||[]),...UI20_KEYS,'ui20_cole-neutral'])]);};
XART._touch=function(k){if(k==='cole_body_0922'||k==='cole_body_0'||k==='cinseat_cole'||/^pose_cole_/.test(k||''))return UI20.base.touch.call(this,'ui20_cole-neutral');
 if(k==='inv20_cole'||k==='inv20_cole_horror'){
  const id=k==='inv20_cole'?'report':'horror',raw='ui20_cole-'+id;if(!XART.rdy(raw))return null;const ck='cinematic-'+id;if(!UI20.cache.has(ck)){const c=document.createElement('canvas');c.width=256;c.height=384;const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.drawImage(XART.get(raw),0,0,512,768,0,0,256,384);c.complete=true;c.naturalWidth=256;c.naturalHeight=384;UI20.cache.set(ck,c);}return UI20.cache.get(ck);
 }return UI20.base.touch.apply(this,arguments);};
function ui20Text(g,s,x,y,h,w,align='center',color){
 const face=window.BOF_UI_FACE||'game';s=String(s??'').toUpperCase();if(!s)return;
 const id=['text',s,h,color].join('|');let c=UI20.cache.get(id);
 if(!c){const raw=document.createElement('canvas');raw.width=Math.ceil(bmfMeasure(face,s,h)+h*2+40);raw.height=Math.ceil(h*3+16);const q=raw.getContext('2d');bmfDrawOn(q,face,s,raw.width/2,raw.height/2,h,'center');if(color){q.globalCompositeOperation='source-in';q.fillStyle=color;q.fillRect(0,0,raw.width,raw.height);}const p=q.getImageData(0,0,raw.width,raw.height).data;let l=raw.width,t=raw.height,r=0,b=0;for(let yy=0;yy<raw.height;yy++)for(let xx=0;xx<raw.width;xx++)if(p[(yy*raw.width+xx)*4+3]>0){l=Math.min(l,xx);t=Math.min(t,yy);r=Math.max(r,xx+1);b=Math.max(b,yy+1);}if(r<=l)return;c=document.createElement('canvas');c.width=r-l;c.height=b-t;c.getContext('2d').drawImage(raw,l,t,r-l,b-t,0,0,r-l,b-t);if(UI20.cache.size>240)UI20.cache.delete(UI20.cache.keys().next().value);UI20.cache.set(id,c);}
 const k=Math.min(w/c.width,h/c.height),cw=c.width*k,ch=c.height*k,dx=align==='left'?x:align==='right'?x-cw:x-cw/2;g.drawImage(c,dx,y-ch/2,cw,ch);
}
function ui20Icon(g,key,x,y,size){g.save();g.beginPath();g.rect(0,0,0,0);g.clip();p2HudWeaponIcon(g,key,x,y,size);g.restore();const a=P2_HUD_ICONS.get(key);if(!a)return;const k=size/Math.max(a.rect[2],a.rect[3]);g.drawImage(a.canvas,...a.rect,x-a.rect[2]*k/2,y-a.rect[3]*k/2,a.rect[2]*k,a.rect[3]*k);}
function ui20Fill(g,r,f,color){const q=clamp(Number(f)||0,0,1);if(!q)return;const [x,y,w,h]=r;
 const grad=g.createLinearGradient(0,y,0,y+h);grad.addColorStop(0,'#f2ffe5');grad.addColorStop(.2,color);grad.addColorStop(.75,color);grad.addColorStop(1,'#13201b');g.fillStyle=grad;g.fillRect(x,y,Math.floor(w*q),h);g.fillStyle='#ffffff70';g.fillRect(x,y,Math.floor(w*q),Math.max(1,h*.12));}
function ui20Lines(g,s,x,y,h,w,step){let words=String(s).split(/\s+/),rows=[],line='';for(const word of words){const next=line?line+' '+word:word;if(line&&bmfMeasure(window.BOF_UI_FACE||'game',next,h)>w){rows.push(line);line=word;}else line=next;}if(line)rows.push(line);rows.forEach((v,i)=>ui20Text(g,v,x,y+i*step,h,w));return rows.length;}
function ui20Radio(){if(state!==GS.PLAY)return null;
 // Use the director's current beat and clock, including the trap intro, pilot
 // replies and tactical announcements. Both HUD layouts stay outside the field.
 const s=BOFCinematicDirector.current,b=s?.beats[s.i];
 if(s?.live&&s.combatLive&&b)return {who:b.who,text:b.text,age:s.t,duration:Math.max(b.text.length/38+2.7,b.duration||0)};
 if(fb2IntroActive()){const I=fb2Intro,L=I.lines[I.i];if(L)return {who:L.who,text:L.text,age:I.t,duration:L.text.length/38+(L.text.replace(/\./g,'').length?1.7:1.25)};}
 if(run.stage===6&&s6WingRadioVisible()&&s6Wing?.line){const L=s6Wing.line,pages=s6r18Pages(L);let age=L.t,i=0;while(i<pages.length-1&&age>=pages[i].dur)age-=pages[i++].dur;return {who:L.who,text:pages[i].rows.join(' '),age,duration:pages[i].dur};}if(sa14Storm(boss)&&bossActive&&boss?._st18?.radio){const q=boss._st18.radio;return {who:q.who,text:q.text,age:q.t,duration:q.duration};}return null;}
function ui20RadioRows(q,width,size,count){const words=(q.who.toUpperCase()+': '+q.text).toUpperCase().split(/\s+/),rows=[];let row='';for(const word of words){const next=row?row+' '+word:word;if(row&&bmfMeasure(window.BOF_UI_FACE||'game',next,size)>width){rows.push(row);row=word;}else row=next;}if(row)rows.push(row);const pages=Math.max(1,Math.ceil(rows.length/count)),page=clamp(Math.floor((q.age||0)/Math.max(.01,q.duration/pages)),0,pages-1);return rows.slice(page*count,page*count+count);}
function ui20Seat(seat){return withSeat(seat,()=>{
 const v=ph8Values(),active=specialActive()&&special.pilot===v.pilot;v.ship='ship_'+v.pilot;
 v.color=UI20.color(v.pilot);v.portrait=commPortrait(v.pilot,v.dead?'crash':'idle');v.weapon.label=v.weapon.label||(spaceWeaponsActive()?spaceWeaponName():(WVAR_NAME[heldVariant(run.weapon)]||WEAPONS[run.weapon]||'WEAPON'));
 v.secondary={cole:'NUCLEAR WARHEADS',lizzie:'HEAVY TURRET',decker:'INCENDIARY SHOTGUN',freezer:'THERMOSHOCK',juggernaut:'CHARGE DASH'}[v.pilot]||'RETINA LOCK';
 v.primary={cole:'SONIC BOOM',lizzie:'ATOM BOMB',decker:'CLOAKING SYSTEM',freezer:'TIME FREEZE',juggernaut:'WRECKING BALL'}[v.pilot]||v.name;
 const loan=v.loans.find(q=>v.pilot==='cole'?/SONIC/.test(q.label):v.pilot==='lizzie'?/HEAVY/.test(q.label):v.pilot==='decker'?/SHOTGUN/.test(q.label):false);
 v.primaryFrac=v.pilot==='cole'?(loan?.frac||0):(active?v.resource:0);
 v.primaryDetail=v.dead?'SHIP LOST':v.pilot==='cole'?(loan?Math.ceil(run.sonicT)+'S / CHARGE '+Math.round(clamp((run._sonicChg||0)/SONIC_MAX,0,1)*100)+'%':'COLLECT SPECIAL'):(active?v.detail:'COLLECT SPECIAL');
 v.secondaryValue=v.pilot==='cole'?(active?'X '+special.strikes:'INACTIVE'):v.pilot==='lizzie'?(lzMount?(lzMount.docked?Math.ceil(lzMount.life)+'S':'DOCKING'):'INACTIVE'):v.pilot==='decker'?((run.dkT||0)>0?Math.ceil(run.dkT)+'S':'INACTIVE'):v.pilot==='freezer'?(orbIsFireIce()?'EQUIPPED':'VIA LOADOUT'):v.pilot==='juggernaut'?(active?'CHARGE '+Math.round(chargeLevel()*100)+'%':'INACTIVE'):(v.lock?'LOCKED':'NO LOCK');
 return v;
 });}
function ui20Rail(g,side,v){const source=XART.get(side?'hud28_right':'ui20_hud-a-left');g.drawImage(source,0,0,376,1024);const T=(s,x,y,h=26,w=260,a='center',c)=>ui20Text(g,s,x,y,h,w,a,c),I=(k,x,y,h)=>ph8Icon(g,k,x,y,h),pk={yuri:0,falva:1,cole:2,maverick:3,axel:4,juggernaut:5,lizzie:6,decker:7,freezer:8}[v.pilot]??0;
 if(!side){
  for(const [label,y,key,available] of [['ROLL',108,'roll',v.rollAvailable],['SOMERSAULT',268,'somer',v.somerAvailable]]){T(label,188,y,29);ui20Fill(g,[75,y+31,234,21],available?v[key]:0,'#35f837');T(v.dead?'SHIP LOST':!available?'LOCKED':v[key]>=.999?'READY':Math.round(v[key]*100)+'%',188,y+87,30,230,'center',v.dead?'#ff7864':v.color);}
  T('LIVES',107,433,25,126);T('MISSILES',263,433,24,120);ui20Icon(g,v.ship,104,503,74);I('nmi_'+pk,261,503,68);T('X '+Math.max(0,v.lives),108,555,40,119);T('X '+Math.max(0,v.missiles),269,555,40,130);
  T('SPECIAL ABILITY',188,640,25);I(specialArtKey('spicon_'+v.pilot),100,727,78);ui20Lines(g,v.primary,239,690,24,171,27);ui20Fill(g,[170,735,139,21],v.primaryFrac,'#ffb01e');T(v.primaryDetail,210,786,19,216,'center',v.primaryFrac?'#ffd26c':'#9ca8b5');
  if(UI20.radio){T(v.secondary+' '+v.secondaryValue,188,854,15,260);const rows=ui20RadioRows(UI20.radio,260,15,4);rows.forEach((s,i)=>T(s,188,886+i*18,15,260,'center',i?'#eef2f8':UI20.color(UI20.radio.who)));}
  else{T(v.secondary,188,859,21,260);I(v.pilot==='cole'?'special_icon_cole_nuclear_warheads':v.pilot==='lizzie'?'nsw_icon_lizzie':v.pilot==='decker'?'nsw_icon_decker':'retm_0',96,912,58);T(v.secondaryValue,235,914,30,171,'center',v.color);}
 }else{
  ui20Portrait(g,v.portrait,{x:70,y:74,w:228,h:228});
  g.fillStyle=v.color+'35';g.fillRect(82,329,216,39);T((seatList().length>1?'P'+v.seat+' ':'')+v.pilot,190,351,36,198,'center',v.color);
  T('SCORE',69,417,25,240,'left');T(ph8Score(v.score),188,464,60,278);T('HIGH SCORE',188,531,24);T(ph8Score(Math.max(highScore,v.score)),188,568,39,278);
  T('WEAPON EQUIPPED',188,641,24);if(v.weapon.reel)cf1004Cell(v.weapon.reel,CF1004.clock,104,720,70,100,0,g);else ui20Icon(g,v.weapon.key,105,719,78);
  ui20Lines(g,v.weapon.label,247,700,23,168,27);T('LEVEL '+String(v.weapon.lv).padStart(2,'0'),246,756,22,167);
  for(const [label,y,key,color] of [['SPEED',826,'speed','#14bcff'],['ARMOR',915,'shield','#1cffe6']]){T(label,69,y,24,148,'left');T(v[key]+' / 5',307,y,24,110,'right');ui20Fill(g,[69,y+28,242,21],v[key]/5,color);}
 }
}
function ui20IconReady(key){key=specialArtKey(key);const cell=BOFX.icons?.[key];return XART.rdy(cell?(cell[4]||'nia_icons'):key);}
function ui20Compact(values){const c=SC12.compact,w=960,h=392;if(c.width!==w||c.height!==h*values.length){c.width=w;c.height=h*values.length;}const g=c.getContext('2d');g.clearRect(0,0,c.width,c.height);g.imageSmoothingEnabled=false;
 values.forEach((v,i)=>withSeat(v.seat,()=>{g.save();g.translate(0,i*h);const im=XART.get('ui20_dialogue-a');ui20Nine(g,im,[470,0,im.width-470,im.height],0,0,w,h,[80,60,100,58]);
 const T=(s,x,y,sz=24,m=270,col)=>ui20Text(g,s,x,y,sz,m,'center',col),pk={yuri:0,falva:1,cole:2,maverick:3,axel:4,juggernaut:5,lizzie:6,decker:7,freezer:8}[v.pilot]??0;
 for(const [label,x,key,a] of [['ROLL',160,'roll',v.rollAvailable],['SOMERSAULT',480,'somer',v.somerAvailable]]){T(label,x,36);ui20Fill(g,[x-128,58,256,17],a?v[key]:0,'#35f837');T(v.dead?'SHIP LOST':!a?'LOCKED':v[key]>=.999?'READY':Math.round(v[key]*100)+'%',x,98,23,270,v.color);}
 T(v.primary,800,36,22);ui20Fill(g,[672,58,256,17],v.primaryFrac,'#ffb01e');T(v.primaryDetail,800,98,20);
 ui20Icon(g,v.ship,55,163,48);T('LIVES X '+v.lives,190,163,26,230);ph8Icon(g,'nmi_'+pk,365,163,48);T('MISSILES X '+v.missiles,510,163,26,230);T(v.secondary,800,144,20);T(v.secondaryValue,800,178,24,260,v.color);
 if(XART.rdy(v.portrait))g.drawImage(XART.get(v.portrait),26,225,106,106);T(v.pilot,80,354,24,112,v.color);T('SCORE '+ph8Score(v.score),298,245,UI20.radio?20:30,290);if(UI20.radio){ui20RadioRows(UI20.radio,280,17,3).forEach((s,j)=>T(s,298,278+j*24,17,280));T('HIGH '+ph8Score(Math.max(highScore,v.score)),298,364,17,290);}else T('HIGH '+ph8Score(Math.max(highScore,v.score)),298,291,24,310);
 T(v.weapon.label,568,240,22,210);T('LEVEL '+v.weapon.lv,568,282,22,210);ph8Icon(g,v.weapon.key,568,335,50);
 for(const [label,y,k,col] of [['SPEED',249,'speed','#14bcff'],['ARMOR',326,'shield','#1cffe6']]){T(label+' '+v[k]+'/5',802,y,24,220);ui20Fill(g,[690,y+21,224,17],v[k]/5,col);}g.restore();}));}
function ui20Render(values){UI20.warm();if(!UI20_KEYS.every(k=>XART.rdy(k)))return false;
 values=seatList().map(ui20Seat);UI20.last=values;UI20.radio=ui20Radio();const radioSignature=UI20.radio?JSON.stringify([UI20.radio.who,UI20.radio.text,Math.floor(UI20.radio.age*4)]):'';
 const stable=v=>({...v,roll:Math.round(v.roll*234),somer:Math.round(v.somer*234),resource:Math.round(v.resource*139),primaryFrac:Math.round(v.primaryFrac*139),loans:v.loans.map(q=>({...q,frac:Math.round(q.frac*139)}))});
 if(SC12.mode==='compact'){const sig=JSON.stringify(values.map(stable))+highScore+values.map(v=>XART.rdy(v.portrait))+values.map(v=>[v.ship,v.weapon.key,'spicon_'+v.pilot].filter(Boolean).map(ui20IconReady))+radioSignature;if(UI20.dirty||SC12.compact._ui20Signature!==sig){ui20Compact(values);SC12.compact._ui20Signature=sig;UI20.draws++;}UI20.dirty=false;return true;}
 for(const [side,c] of SC12.panels.entries()){if(c.width!==376||c.height!==1024*values.length){c.width=376;c.height=1024*values.length;UI20.dirty=true;}const g=c.getContext('2d');g.imageSmoothingEnabled=false;
 const sig=JSON.stringify(values.map(v=>[stable(v), XART.rdy(v.portrait),[v.ship,v.weapon.key,'spicon_'+v.pilot,'retm_0','nli_'+({yuri:0,falva:1,cole:2,maverick:3,axel:4,juggernaut:5,lizzie:6,decker:7,freezer:8}[v.pilot]??0),'nmi_'+({yuri:0,falva:1,cole:2,maverick:3,axel:4,juggernaut:5,lizzie:6,decker:7,freezer:8}[v.pilot]??0)].filter(Boolean).map(ui20IconReady),v.weapon.reel?Math.floor(CF1004.clock*12):0]))+highScore;
  const finalSig=sig+radioSignature;if(!UI20.dirty&&c._ui20Signature===finalSig)continue;g.clearRect(0,0,c.width,c.height);values.forEach((v,i)=>withSeat(v.seat,()=>{g.save();g.translate(0,i*1024);ui20Rail(g,side,v);g.restore();}));c._ui20Signature=finalSig;}
 UI20.dirty=false;UI20.draws++;return true;}
// The existing console remains the sole scheduled renderer and state reader.
SC12.render=ui20Render;
UI20.oldFit=SC12.fit;SC12.fit=function(vw=innerWidth,vh=innerHeight){const result=UI20.oldFit(vw,vh);if(result&&SC12.mode==='sides'){
 const rows=seatList().length,field=SC12.layout.field,roomW=(vw-field.w)/2-12,k=Math.min(vh/(1024*rows),roomW/376),w=376*k,h=1024*rows*k;SC12.panels.forEach((c,i)=>Object.assign(c.style,{width:w+'px',height:h+'px',top:(vh-h)/2+'px',left:(i?field.x+field.w+6:field.x-w-6)+'px'}));}
 else if(result){const rows=seatList().length,k=Math.min(vw/VW,vh/(VH+196*rows)),w=VW*k,h=VH*k,x=(vw-w)/2,y=(vh-(VH+196*rows)*k)/2;for(const el of [document.getElementById('game-frame'),document.getElementById('screen-area'),cv])Object.assign(el.style,{width:w+'px',height:h+'px'});Object.assign(document.getElementById('game-frame').style,{left:x+'px',top:y+'px'});Object.assign(SC12.compact.style,{left:x+'px',top:y+h+'px',width:w+'px',height:196*rows*k+'px'});SC12.layout.field={x,y,w,h};}return result;};
SC12.invalidate=()=>{UI20.dirty=true;};
// Map content through the very same rounded nine-slice edges as its housing.
// Source coordinates describe the authored apertures, not estimated percentages.
function ui20NineLayout(r,x,y,w,h,b){const [sx,sy,sw,sh]=r,[l,t,rr,bb]=b,k=Math.min(h/sh,w/(l+rr+1)),xs=[sx,sx+l,sx+sw-rr,sx+sw],ys=[sy,sy+t,sy+sh-bb,sy+sh],dx=[x,x+l*k,x+w-rr*k,x+w].map(Math.round),dy=[y,y+t*k,y+h-bb*k,y+h].map(Math.round);
 const axis=(v,src,dst)=>{const i=v<src[1]?0:v<src[2]?1:2;return dst[i]+(v-src[i])*(dst[i+1]-dst[i])/(src[i+1]-src[i]);};
 const point=(a,b)=>[axis(a,xs,dx),axis(b,ys,dy)],rect=(a,b,c,d)=>{const p=point(a,b),q=point(a+c,b+d);return {x:p[0],y:p[1],w:q[0]-p[0],h:q[1]-p[1]};};return {xs,ys,dx,dy,point,rect};}
function ui20Nine(g,im,r,x,y,w,h,b){const q=ui20NineLayout(r,x,y,w,h,b),{xs,ys,dx,dy}=q;g.save();for(let a=0;a<3;a++)for(let c=0;c<3;c++)g.drawImage(im,xs[c],ys[a],xs[c+1]-xs[c],ys[a+1]-ys[a],dx[c],dy[a],dx[c+1]-dx[c],dy[a+1]-dy[a]);g.restore();return q;}
function ui20PanelLayout(x,y,w,h,portrait){const bw=portrait?Math.min(h*1.13,w*.27):0,bodySource=[portrait?470:380,0,portrait?1690:1780,394],bodyBorder=[portrait?440:90,132,100,58],body=ui20NineLayout(bodySource,x+bw,y,w-bw,h,bodyBorder),bay=bw?ui20NineLayout([0,0,470,394],x,y,bw,h,[100,60,84,64]):null;
 const name=body.rect(505,51,320,52),text=body.rect(490,151,1586,175),portraitRect=bay?.rect(84,59,308,278),namePoint=(a,b)=>a<470&&bay?bay.point(a,b):body.point(Math.max(portrait?0:380,a),b),namePolygon=[[450,44],[839,44],[872,77],[872,87],[842,112],[482,112],[450,80]].map(p=>namePoint(...p)),nameHardware=[[467,64,23,25],[832,54,6,6],[841,103,7,7]].map(([a,b,rx,ry])=>{const c=namePoint(a,b),p=namePoint(a+rx,b+ry);return {x:c[0],y:c[1],rx:Math.abs(p[0]-c[0]),ry:Math.abs(p[1]-c[1])};});
 return {bw,body,bay,bodySource,bodyBorder,name,text,portraitRect,namePolygon,nameHardware};}
function ui20Polygon(g,points){g.beginPath();points.forEach((p,i)=>i?g.lineTo(...p):g.moveTo(...p));g.closePath();}
function ui20Panel(who,x,y,w,h,portrait){if(!XART.rdy('ui20_dialogue-a'))return null;const im=XART.get('ui20_dialogue-a'),r=ui20PanelLayout(x,y,w,h,portrait);
 if(r.bw)ui20Nine(ctx,im,[0,0,470,394],x,y,r.bw,h,[100,60,84,64]);ui20Nine(ctx,im,r.bodySource,x+r.bw,y,w-r.bw,h,r.bodyBorder);
 // Tint the entire inner plate through its angled nose; keep its lamp and bolts intact.
 ctx.save();ui20Polygon(ctx,r.namePolygon);ctx.clip();for(const q of r.nameHardware){ctx.moveTo(q.x+q.rx,q.y);ctx.ellipse(q.x,q.y,q.rx,q.ry,0,0,Math.PI*2);}ctx.fillStyle=UI20.color(who)+'50';ctx.fill('evenodd');ctx.restore();return r;}
function ui20Portrait(g,key,r){if(!r||!key||!XART.rdy(key))return null;const im=XART.get(key),k=Math.min(r.w/im.width,r.h/im.height),w=im.width*k,h=im.height*k,x=r.x+(r.w-w)/2,y=r.y+(r.h-h)/2;g.save();g.beginPath();g.rect(r.x,r.y,r.w,r.h);g.clip();g.drawImage(im,x,y,w,h);g.restore();return {x,y,w,h};}
function ui20PanelContents(who,full,shown,port,r,maxH=14,nameH=16){const portraitDraw=ui20Portrait(ctx,port,r.portraitRect),n=r.name,t=r.text;
 ctx.save();ui20Polygon(ctx,r.namePolygon);ctx.clip();ui20Text(ctx,who,n.x+n.w/2,n.y+n.h/2,Math.min(nameH,n.h*.86),n.w,'center',UI20.color(who));ctx.restore();
 const layout=msgDrawBlock({text:full,budget:shown,x:t.x,y:t.y,w:t.w,h:t.h,maxH,minH:8,lineMul:1.25,color:'#fff9eb',alpha:1,outline:false,align:'center',stableCenter:true,valign:'middle'});
 return {portrait:port,name:n,text:t,portraitRect:r.portraitRect,portraitDraw,namePolygon:r.namePolygon,layout};}
dialogueFrameDraw=function(who,tint,x,y,w,h){return !!ui20Panel(who,x,y,w,h,true)||UI20.base.frame.apply(this,arguments);};
dlgBox=function(o){if(!XART.rdy('ui20_dialogue-a'))return UI20.base.dlg.apply(this,arguments);
 const fade=o.fade??1;if(fade<=0)return;const who=o.who||'',full=o.full||'',key=String(state)+'|'+who+'|'+full,now=performance.now(),prior=dlgBox._tw,first=!prior||prior.key!==key,auto=o.forceShown!==true&&(o.shown==null||(o.shown===full&&(first||prior.auto)));let shown;
 if(auto){const count=first?0:Math.min(full.length,prior.count+(now-prior.at)*.034);shown=full.slice(0,Math.floor(count));dialogueLetterTicks(full,first?0:Math.floor(prior.count),Math.floor(count));dlgBox._tw={key,count,at:now,auto:true};}else{shown=String(o.shown??full);dialogueLetterTicks(full,first?0:Math.min(full.length,Math.floor(prior.count)),shown.length);dlgBox._tw={key,count:shown.length,at:now,auto:false};}
 const pk=String(o.portrait||who).toLowerCase(),talking=shown.length<full.length&&(!o.emo||o.emo==='idle'),port=o.portraitKey||(o.portrait!==false&&UI20.pilot(pk)?commPortrait(pk,talking?'talk':o.emo||'idle'):null),inPlay=state===GS.PLAY,viewW=(state===GS.CAMPAIGNINTRO||state===GS.CUTSCENE)?cutsceneViewWidth():VW;
 const w=Math.min(viewW-20,o.pw||(inPlay?VW*.72:viewW-20)),maxHeight=VH*(inPlay?.34:.44),x=o.x??(inPlay?PLAY.x+8:(viewW-w)/2),bottom=Math.min(VH-10,o.maxBottom??VH-10);let h=Math.min(maxHeight,o.fixedHeight===true?(o.ph||84):Math.max(o.ph||126,90));msgFaceUse(o.face||'dialogue');
 // Fit the complete sentence before revealing characters, so typing never shifts rows.
 const sizeKey=['dialogue-height',full,x,w,h,maxHeight,!!port,o.face||'dialogue',bmfReady(o.face||'dialogue')].join('|');if(o.fixedHeight===true){/* Caller owns a uniform cinematic window; text fits its aperture. */}else if(UI20.cache.has(sizeKey))h=UI20.cache.get(sizeKey);else{
  for(;h<maxHeight;h=Math.min(maxHeight,h+2)){const t=ui20PanelLayout(x,0,w,h,port).text;if(msgBlockLayout(full,t.w,1000,14,14,1.25).height<=t.h)break;}
  if(UI20.cache.size>240)UI20.cache.delete(UI20.cache.keys().next().value);UI20.cache.set(sizeKey,h);
 }
 const desired=o.y??(inPlay?Math.min(PLAY.y+PLAY.h-67-h,(player?.y||VH)-h-25):bottom-h),y=clamp(desired,8,bottom-h);
 ctx.save();ctx.globalAlpha*=fade;if(o.screenSpace!==false)worldXformEscape();const r=ui20Panel(who,x,y,w,h,port),content=ui20PanelContents(who,full,shown.length,port,r);msgFaceUse(null);ctx.restore();UI20.dialogue={who,color:UI20.color(who),portrait:port,x,y,w,h,shown:shown.length,full:full.length,...content};};
inv20Text=function(who,text,W,H,shown=text.length,alpha=1){const w=Math.min(W*.94,1120),h=H*(W/H<1?.27:.225),p=UI20.pilot(who),dr=/DRACODIA/i.test(who),port=p?commPortrait(p.key,shown<text.length?'talk':'idle'):dr?DP20.key:null;
 ctx.save();ctx.globalAlpha*=alpha;const x=(W-w)/2,y=H-h-13;msgFaceUse('dialogue');const r=ui20Panel(who,x,y,w,h,port);
 if(!r){msgFaceUse(null);ctx.restore();return;}const content=ui20PanelContents(who,text.toUpperCase(),shown,port,r,Math.min(27,H*.032),Math.min(25,H*.03));msgFaceUse(null);ctx.restore();INV20.caption={who,text,color:UI20.color(who),x,y,w,h,shown,...content};};
// Keep the Stage 4/6 radio timings and pages, while drawing their dialogue in
// the new frame rather than into coordinates belonging to the retired rail.
UI20.base.radio4=st18RadioDraw;UI20.base.radio6=s6r18RadioDraw;
st18RadioDraw=function(){if(!UI20_KEYS.every(k=>XART.rdy(k)))return UI20.base.radio4.apply(this,arguments);};
s6r18RadioDraw=function(){if(!UI20_KEYS.every(k=>XART.rdy(k)))return UI20.base.radio6.apply(this,arguments);};
UI20.warm();window.__bofFit();
