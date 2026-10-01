"use strict";
/* September 30: a single interactive world, with Fury HQ at its centre.
   Geography is decorative. The locked East Coast USA sector never adds an expansion unlock. */
const MAP30_ART={hq:'fury_hq',east:'eastern_ruins',north:'northern_coast',datawall:'east_coast_binary_rows_v6',home:'northern_hq_island',cove:'island_cove',ruins:'island_ruins'};
for(const [k,file] of Object.entries(MAP30_ART))XART._src['map30_'+k]='assets/game/campaign_0930/'+file+'.png';
const MAP30={westX:35,home:{x:385,y:185,w:205,h:190},ships:new Map(),land:[
 {key:'north',x:690,y:-148,w:1280,h:402},
 {key:'east',x:1395,y:640,w:280,h:570},
 {key:'cove',x:138,y:350,w:90,h:80},
 {key:'ruins',x:166,y:940,w:92,h:84},
 {key:'cove',x:510,y:1080,w:90,h:80},
 {key:'ruins',x:1260,y:968,w:83,h:76},
 {key:'cove',x:1300,y:254,w:85,h:75},
 {key:'ruins',x:1080,y:1170,w:110,h:100},
 {key:'cove',x:870,y:1160,w:64,h:57}
]};
const MAP30_WARM=cmap2Warm;
cmap2Warm=function(){MAP30_WARM();for(const k of Object.keys(MAP30_ART))XART.rdy('map30_'+k);};
/* These two headings are baked once from each pilot's approved hull. There is
   no animated pivot, bank frame or renderer rotation on the map. */
function map30ShipFrame(key,face){
 const id=key+':'+face;if(MAP30.ships.has(id))return MAP30.ships.get(id);
 if(!XART.rdy(key))return null;
 const im=XART.get(key),w=im.naturalWidth||im.width,h=im.naturalHeight||im.height;
 const c=document.createElement('canvas');c.width=h;c.height=w;
 const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.translate(h/2,w/2);g.rotate(face*Math.PI/2);g.drawImage(im,-w/2,-h/2);
 c.naturalWidth=c.width;c.naturalHeight=c.height;MAP30.ships.set(id,c);return c;
}
sselShipDraw=function(){
 if(!sselShip)return;const sh=sselShip,pk=typeof _pilotKey==='function'?_pilotKey():run.pilot||'cole';
 const im=map30ShipFrame('ship_'+pk,sh.face||1)||map30ShipFrame('ship_cole',sh.face||1);if(!im)return;
 const z=cmap2On()?Math.max(.25,cmap2.cam.z):1,w=29/z,h=w*im.height/im.width;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,sh.x-w/2,sh.y-h/2,w,h);ctx.restore();
};
function map30Overview(){
 const hub=cmap2World('hub');
 /* Keep the mission ring above the bottom briefing and below the clock.
    Portrait widths reduce horizontal space only on the widescreen HUD. */
 const wide=window.innerWidth>=1150&&campaignViewWidth()>VW;
 const available=Math.max(350,campaignViewWidth()-(wide?200:18));
 return {x:hub.x,y:hub.y,z:Math.min(.30,available/1460,(CM2_BAND_BOT-CM2_BAND_TOP-24)/1050)};
}
const MAP30_CAMERA=cmap2CameraTick;
cmap2CameraTick=function(dt,cine,selected){
 if(sselBoot>0||s9MapCine||riftReturn||selected===9||Rival24.mapFocused||Rival24.flying||cine){return MAP30_CAMERA(dt,cine,selected);}
 const target=map30Overview(),k=1-Math.exp(-dt*3.4),c=cmap2.cam;
 c.x+=(target.x-c.x)*k;c.y+=(target.y-c.y)*k;c.z+=(target.z-c.z)*k;
};
function map30Blit(key,x,y,w,h,alpha){
 if(!XART.rdy('map30_'+key))return;ctx.save();ctx.globalAlpha=alpha==null?1:alpha;
 ctx.drawImage(XART.get('map30_'+key),x-w/2,y-h/2,w,h);ctx.restore();
}
function map30Geography(){
 const H=MAP30.home;map30Blit('home',H.x,H.y,H.w,H.h,1);
 for(const q of MAP30.land)map30Blit(q.key,q.x,q.y,q.w,q.h,q.alpha);
}
function map30LockedBounds(){
 const c=cmap2.cam,z=Math.max(.05,c.z);
 return {left:c.x+(-campaignViewOffset()-CM2_VCX)/z-8,right:MAP30.westX,
  top:c.y-CM2_VCY/z-8,height:VH/z+16,z};
}
/* Four binary-row palette poses from one generated panel. Its ragged alpha
   edge composites over live ocean without scrolling or crystal geometry.
   Source: east_coast_binary_rows_v6.json / build_east_coast_binary_rows_0930.py. */
const MAP30_DATA={columns:4,count:4,width:512,height:1024,fps:3};
function map30DataLayout(B){
 const w=Math.max(B.right-B.left+120,B.height*MAP30_DATA.width/MAP30_DATA.height);
 const h=w*MAP30_DATA.height/MAP30_DATA.width;
 return {x:B.right-w*.9,y:B.top+(B.height-h)/2,w,h};
}
function map30DataWall(){
 const B=map30LockedBounds();if(B.left>=B.right)return;
 ctx.save();ctx.globalAlpha=1;
 /* Hidden land is never submitted. Keep the opaque backing behind the
    generated edge so the live ocean remains visible through its alpha. */
 const ready=XART.rdy('map30_datawall'),P=map30DataLayout(B);
 const backingRight=ready?P.x+P.w*.42:B.right;
 ctx.fillStyle='#060416';
 if(backingRight>B.left)ctx.fillRect(B.left,B.top,backingRight-B.left,B.height);
 if(ready){
  const f=Math.floor(cmap2.t*MAP30_DATA.fps)%MAP30_DATA.count;
  ctx.imageSmoothingEnabled=false;
  ctx.drawImage(XART.get('map30_datawall'),
   (f%MAP30_DATA.columns)*MAP30_DATA.width,
   Math.floor(f/MAP30_DATA.columns)*MAP30_DATA.height,
   MAP30_DATA.width,MAP30_DATA.height,P.x,P.y,P.w,P.h);
 }
 ctx.restore();
}

function map30Labels(){
 const z=Math.max(.25,cmap2.cam.z),hub=cmap2World('hub'),home=MAP30.home;
 const busy=Rival24.mapAvailable||Rival24.mapFocused;
 /* Fury HQ belongs to the northern jungle outpost. The center island remains
    the Harrier/rebel battleground and still hosts Stage X's orbit and plaque. */
 map30Blit('hq',home.x,home.y+8,27/z,25/z,1);
 if(!busy&&typeof campText==='function')campText('CENTRAL BATTLEGROUND',hub.x,hub.y+137,7/z,'#b9dcf0',.9);
 const B=map30LockedBounds(),visible=(B.right-B.left)*B.z;
 if(typeof campText==='function'&&visible>40){
  const labelX=(B.left+B.right)/2,labelY=cmap2.cam.y+20/B.z;
  const size=Math.min(9,(visible-16)/13);
  ctx.save();ctx.globalAlpha=.86;ctx.fillStyle='#08041b';
  ctx.fillRect(B.left+7/B.z,labelY-29/B.z,(visible-14)/B.z,62/B.z);ctx.restore();
  campText('EAST COAST USA',labelX,labelY-15/B.z,size/B.z,'#d9c0ff',1);
  campText('LOCKED',labelX,labelY+5/B.z,Math.min(14,(visible-18)/7.7)/B.z,'#f4eaff',1);
  campText('PASSAGE SEALED',labelX,labelY+22/B.z,size*.72/B.z,'#d9c0ff',1);
 }

}
const MAP30_WORLD=cmap2DrawWorld;
cmap2DrawWorld=function(dt,selected){
 ctx.save();ctx.imageSmoothingEnabled=false;map30Geography();ctx.restore();
 MAP30_WORLD(dt,selected);ctx.save();ctx.imageSmoothingEnabled=false;map30DataWall();map30Labels();ctx.restore();
};
/* Clicking the visible data barrier explains the locked border, and cannot
   select or deploy an expansion level. All existing stage hit tests stay live. */
cv.addEventListener('pointerdown',function(e){
 if(state!==GS.STAGESEL||campPause||sselBoot||sselZoom)return;
 const r=cv.getBoundingClientRect(),sx=(e.clientX-r.left)/r.width*campaignViewWidth()-campaignViewOffset(),sy=(e.clientY-r.top)/r.height*VH;
 if(sy<75||sy>CM2_BAND_BOT)return;
 const wx=cmap2.cam.x+(sx-CM2_VCX)/cmap2.cam.z;
 if(wx<=MAP30.westX+50){cmap2Toast('EAST COAST USA - PASSAGE SEALED');if(Audio.SFX.error)Audio.SFX.error();}
});
