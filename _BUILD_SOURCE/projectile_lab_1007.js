/* Native-browser QA only. Not part of the game build. */
window.AP7={case:null,keys:{},errors:[],geometry:[],unready:[],seen:new WeakSet(),shots:{},frames:0};
const AP7_RAW={get:XART.get,draw:ctx.drawImage,bullets:drawBullets};
AP7.tags=new WeakMap();
XART.get=function(k){const im=AP7_RAW.get.apply(this,arguments);if(im&&typeof im==='object')AP7.tags.set(im,k);return im;};
drawBullets=function(){AP7.layer='projectile';try{return AP7_RAW.bullets.apply(this,arguments);}finally{AP7.layer=null;}};
ctx.drawImage=function(im,...a){
 const key=AP7.tags.get(im)||im?.src?.split('/').pop()||'cached',layer=AP7.layer||'scene';
 const name=layer+':'+key;AP7.keys[name]=(AP7.keys[name]||0)+1;
 const w=im?.naturalWidth||im?.width,h=im?.naturalHeight||im?.height;
 if(a.some(v=>!Number.isFinite(v))||!w||!h){if(AP7.geometry.length<80)AP7.geometry.push({case:AP7.case,key,layer,a,w,h,reason:'nonfinite-or-empty'});}
 else if(a.length===8&&(a[0]<-.01||a[1]<-.01||a[0]+a[2]>w+.01||a[1]+a[3]>h+.01)){
  if(AP7.geometry.length<80&&!AP7.geometry.some(e=>e.key===key&&e.case===AP7.case))AP7.geometry.push({case:AP7.case,key,layer,a,w,h,reason:'source-outside-image'});
 }
 return AP7_RAW.draw.call(this,im,...a);
};
AP7.begin=function(c){
 BAL7.setup(c);AP7.case=c.id;AP7.keys={};AP7.geometry=[];AP7.shots={};AP7.seen=new WeakSet();AP7.frames=0;
 player.invuln=99999;player2.invuln=99999;run.shield=999;
 if(c.slice){boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=false;subBossTriggered=false;
  beginStage(c.stage);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;player.reset();player.invuln=99999;run.shield=999;}
 return true;
};
AP7.step=function(n){
 for(let i=0;i<n;i++){
  if(state!==GS.PLAY)break;
  player.invuln=99999;player.dead=false;player.out=false;run.shield=999;
  // Observe real firing patterns without deleting the encounter through player damage.
  player.x=worldWidth()/2+Math.sin(AP7.frames/180)*Math.min(115,worldWidth()/4);player.y=VH-90;
  updatePlay(1/60);AP7.frames++;
  for(const b of eBullets)if(!AP7.seen.has(b)){AP7.seen.add(b);AP7.shots[b.kind]=(AP7.shots[b.kind]||0)+1;}
  if(AP7.frames%10===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/6);}
 }
 return {frames:AP7.frames,state,shots:AP7.shots,keys:AP7.keys,geometry:AP7.geometry,pattern:BAL7.pattern()};
};
AP7.frame=function(b,enemy=true){
 pBullets=enemy?[]:[b];eBullets=enemy?[b]:[];
 ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);drawBullets();
 const ox=(VW/2-96)*SS,oy=(VH/2-112)*SS,w=192*SS,h=224*SS,d=ctx.getImageData(ox,oy,w,h).data;
 let l=w,r=-1,t=h,bt=-1,n=0,hash=2166136261,alphaHash=2166136261;
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){
  const i=(y*w+x)*4,a=d[i+3];
  if(a){n++;l=Math.min(l,x);r=Math.max(r,x);t=Math.min(t,y);bt=Math.max(bt,y);}
  if(a){alphaHash=Math.imul(alphaHash^(a+i),16777619)>>>0;
   for(let c=0;c<4;c++)hash=Math.imul(hash^(d[i+c]+i+c),16777619)>>>0;}
 }
 return {bounds:n?[(l+ox)/SS,(t+oy)/SS,(r+1+ox)/SS,(bt+1+oy)/SS]:null,n,hash,alphaHash};
};
AP7.catalog=function(){
 const kinds=[...new Set([...Object.keys(FIRETYPES),...Object.keys(PROJ),'s8parasite'])];
 const out=[];for(const kind of kinds){
  const b={kind,x:VW/2,y:VH/2,vx:0,vy:3,ang:Math.PI/2,w:12,h:20,t:0,life:10,pal:'red',lv:3,szMul:1,_noArsenal:true};
  try{const frames=[];for(let i=0;i<8;i++){b.t=b._visualAge=i/16;frames.push(AP7.frame(b));}out.push({kind,frames});}
  catch(e){out.push({kind,error:String(e)});ctx.resetTransform();ctx.globalAlpha=1;}
 }
 pBullets=[];eBullets=[];return out;
};
