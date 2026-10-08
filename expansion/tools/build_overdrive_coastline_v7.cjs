const fs=require('fs');
const path=require('path');
const crypto=require('crypto');
const sharp=require('sharp');
const root=path.resolve(__dirname,'../coastline');
const out=path.join(root,'assets/v7');
const previous=JSON.parse(fs.readFileSync(path.join(root,'manifest_v6.json'),'utf8'));
const motion=require(path.join(root,'map_motion_v3.js'));
const weather=require(path.join(root,'map_weather_v6.js'));
const [W,H]=previous.mapLayout.canvas;
const S=256,FRAMES=6,FPS=8;
const assets=previous.assets.filter(a=>!['world_terrain','world_review'].includes(a.id));
const made=[];
fs.mkdirSync(out,{recursive:true});

async function save(pipeline,id,role,source){
  const file=path.join(out,`${id}.png`);
  await pipeline.png().toFile(file);
  const bytes=fs.readFileSync(file),meta=await sharp(bytes).metadata();
  const raw=await sharp(bytes).ensureAlpha().raw().toBuffer();
  let transparentPixels=0;for(let i=3;i<raw.length;i+=4)if(raw[i]===0)transparentPixels++;
  const rec={id,file:`assets/v7/${id}.png`,width:meta.width,height:meta.height,transparentPixels,role,source,sha256:crypto.createHash('sha256').update(bytes).digest('hex')};
  assets.push(rec);made.push(rec);return file;
}
const clamp=(n,lo=0,hi=255)=>Math.max(lo,Math.min(hi,n));
function repairSeam(data,size,margin){
  for(let y=0;y<size;y++)for(let d=0;d<margin;d++){
    const a=(y*size+d)*4,b=(y*size+size-1-d)*4,weight=1-d/margin;
    for(let c=0;c<3;c++){const avg=(data[a+c]+data[b+c])/2;data[a+c]=Math.round(data[a+c]*(1-weight)+avg*weight);data[b+c]=Math.round(data[b+c]*(1-weight)+avg*weight);}
  }
  for(let x=0;x<size;x++)for(let d=0;d<margin;d++){
    const a=(d*size+x)*4,b=((size-1-d)*size+x)*4,weight=1-d/margin;
    for(let c=0;c<3;c++){const avg=(data[a+c]+data[b+c])/2;data[a+c]=Math.round(data[a+c]*(1-weight)+avg*weight);data[b+c]=Math.round(data[b+c]*(1-weight)+avg*weight);}
  }
}
function frame(base,k){
  const out=Buffer.alloc(base.length),phase=2*Math.PI*k/FRAMES;
  for(let y=0;y<S;y++)for(let x=0;x<S;x++){
    const dx=Math.round(1.7*Math.sin(2*Math.PI*y/64+phase)+.7*Math.sin(2*Math.PI*(x+y)/128-phase));
    const dy=Math.round(1.1*Math.cos(2*Math.PI*x/64-phase));
    const sx=(x+dx+S)%S,sy=(y+dy+S)%S,src=(sy*S+sx)*4,dst=(y*S+x)*4;
    const shine=4.6*Math.sin(2*Math.PI*(x/64+y/32)-phase)+2.4*Math.sin(2*Math.PI*(x/32-y/64)-phase);
    const strength=.45+base[src+1]/260;
    out[dst]=clamp(Math.round(base[src]+shine*strength*.78));
    out[dst+1]=clamp(Math.round(base[src+1]+shine*strength));
    out[dst+2]=clamp(Math.round(base[src+2]+shine*strength*.58));
    out[dst+3]=255;
  }
  repairSeam(out,S,9);
  return out;
}
function hsv(r,g,b){
  r/=255;g/=255;b/=255;const max=Math.max(r,g,b),min=Math.min(r,g,b),d=max-min;
  let h=0;if(d){if(max===r)h=((g-b)/d)%6;else if(max===g)h=(b-r)/d+2;else h=(r-g)/d+4;h=(h*60+360)%360;}
  return[h,max===0?0:d/max,max];
}
function rgb(h,s,v){
  const c=v*s,x=c*(1-Math.abs((h/60)%2-1)),m=v-c;
  const q=h<60?[c,x,0]:h<120?[x,c,0]:h<180?[0,c,x]:h<240?[0,x,c]:h<300?[x,0,c]:[c,0,x];
  return q.map(n=>Math.round((n+m)*255));
}
async function sludge(input){
  const {data,info}=await sharp(input).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  let swapped=0;
  for(let i=0;i<data.length;i+=4){
    if(data[i+3]<32)continue;
    const [h,s,v]=hsv(data[i],data[i+1],data[i+2]);
    if(h<160||h>255||s<.22||v<.12||data[i+2]<data[i]*1.2)continue;
    const newHue=Math.max(70,Math.min(105,h-125));
    const newSat=Math.max(.36,Math.min(.56,s*.43+.07));
    const newValue=Math.min(1,v*(v>.52?.82:.65));
    const [r,g,b]=rgb(newHue,newSat,newValue);data[i]=r;data[i+1]=g;data[i+2]=b;swapped++;
  }
  return{buffer:await sharp(data,{raw:{width:info.width,height:info.height,channels:4}}).png().toBuffer(),swapped};
}
function meanDifference(a,b){let sum=0;for(let i=0;i<a.length;i+=4)for(let c=0;c<3;c++)sum+=Math.abs(a[i+c]-b[i+c]);return sum/(S*S*3);}
function edgeDifference(a){let sum=0;for(let i=0;i<S;i++)for(let c=0;c<3;c++){sum+=Math.abs(a[(i*S)*4+c]-a[(i*S+S-1)*4+c]);sum+=Math.abs(a[i*4+c]-a[((S-1)*S+i)*4+c]);}return sum/(S*6);}
function svg(body){return Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">${body}</svg>`);}

async function main(){
  const base=await sharp(path.join(root,'assets/v6/sludge_ocean.png')).resize(S,S,{kernel:'nearest'}).ensureAlpha().raw().toBuffer();
  repairSeam(base,S,12);
  const frames=[],frameFiles=[];
  for(let k=0;k<FRAMES;k++){
    const pixels=frame(base,k);frames.push(pixels);
    const file=await save(sharp(pixels,{raw:{width:S,height:S,channels:4}}),`water_frame_${String(k).padStart(2,'0')}`,'Animated sludge water frame','assets/v6/sludge_ocean.png');
    frameFiles.push(file);
  }
  const sheetLayers=await Promise.all(frameFiles.map(async(file,k)=>({input:fs.readFileSync(file),left:k*S,top:0})));
  await save(sharp({create:{width:S*FRAMES,height:S,channels:4,background:'#00000000'}}).composite(sheetLayers),
    'sludge_water_6f','Six-frame animated water spritesheet','water_frame_00 through water_frame_05');
  const contactLayers=await Promise.all(frameFiles.map(async(file,k)=>({input:fs.readFileSync(file),left:(k%3)*S,top:Math.floor(k/3)*S})));
  await save(sharp({create:{width:S*3,height:S*2,channels:4,background:'#00000000'}}).composite(contactLayers),
    'water_frame_contact','Six-frame water contact sheet','water_frame_00 through water_frame_05');
  const seamLayers=[];for(let y=0;y<3;y++)for(let x=0;x<3;x++)seamLayers.push({input:fs.readFileSync(frameFiles[0]),left:x*S,top:y*S});
  await save(sharp({create:{width:S*3,height:S*3,channels:4,background:'#00000000'}}).composite(seamLayers),
    'water_tiling_review','Frame zero repeated 3 by 3 for seam review','water_frame_00.png');

  const terrainLayers=[];
  for(const t of previous.mapLayout.terrain){const [x,y,w,h]=t.rect;terrainLayers.push({input:await sharp(path.join(root,t.file)).resize(w,h,{kernel:'nearest'}).toBuffer(),left:x,top:y});}
  const landOriginal=await sharp({create:{width:W,height:H,channels:4,background:'#00000000'}}).composite(terrainLayers).png().toBuffer();
  const landSludge=await sludge(landOriginal);
  const protectedTerrain=previous.mapLayout.terrain.filter(t=>t.id==='portalBridge'||t.id.startsWith('old_'));
  const protectedLayers=[];for(const t of protectedTerrain){const [x,y,w,h]=t.rect;protectedLayers.push({input:await sharp(path.join(root,t.file)).resize(w,h,{kernel:'nearest'}).toBuffer(),left:x,top:y});}
  const {data:overlayRaw}=await sharp(landSludge.buffer).composite(protectedLayers).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  const originalRaw=await sharp(landOriginal).ensureAlpha().raw().toBuffer();
  for(let i=3;i<overlayRaw.length;i+=4)overlayRaw[i]=originalRaw[i];
  const overlayFile=await save(sharp(overlayRaw,{raw:{width:W,height:H,channels:4}}),
    'terrain_overlay','Transparent terrain over animated water','Version 6 terrain layout, shoreline palette');
  const waterTiles=[];for(let y=0;y<H;y+=S)for(let x=0;x<W;x+=S)waterTiles.push({input:fs.readFileSync(frameFiles[0]),left:x,top:y});
  const firstWorld=await sharp({create:{width:W,height:H,channels:4,background:'#00000000'}}).composite([...waterTiles,{input:fs.readFileSync(overlayFile),left:0,top:0}]).png().toBuffer();
  const worldFile=await save(sharp(firstWorld),'world_terrain','First-frame layered terrain composite','Animated frame zero plus terrain_overlay');

  const shield=previous.mapLayout.effects.find(e=>e.id==='voidPortalShield'),[sx,sy,sw,sh]=shield.rect;
  const shieldBuffer=await sharp(path.join(root,assets.find(a=>a.id===shield.sprite).file)).resize(sw,sh,{kernel:'nearest'}).toBuffer();
  const route=previous.mapLayout.flightRoute;
  const shadows=previous.mapLayout.nodes.map(n=>`<ellipse cx="${n.ground[0]}" cy="${n.ground[1]-38}" rx="${n.size*.38}" ry="23" fill="#001017" opacity=".58"/>`).join('');
  const review=[{input:shieldBuffer,left:sx,top:sy},{input:svg(`<path d="${route}" fill="none" stroke="#14261d" stroke-width="13"/><path d="${route}" fill="none" stroke="#a6dcc0" stroke-width="4" stroke-dasharray="13 16"/>${shadows}`),left:0,top:0}];
  for(const n of previous.mapLayout.nodes){
    review.push({input:await sharp(path.join(root,n.file)).resize(n.size,n.size,{kernel:'nearest'}).toBuffer(),left:Math.round(n.center[0]-n.size/2),top:Math.round(n.center[1]-n.size/2)});
    review.push({input:await sharp(path.join(root,`assets/v2/nss_flag${n.number}${n.number===1?'_hi0':'_av'}.png`)).resize(60,72,{kernel:'nearest'}).toBuffer(),left:n.flag[0]-30,top:n.flag[1]-72});
  }
  for(const f of previous.mapLayout.originalFlags)review.push({input:await sharp(path.join(root,`assets/v2/nss_flag${f.number}_av.png`)).resize(40,48,{kernel:'nearest'}).toBuffer(),left:Math.round(f.at[0]-20),top:Math.round(f.at[1]-48)});
  for(const a of previous.mapLayout.ambient){const p=motion.pose(a,0),rec=assets.find(r=>r.id===a.sprite);let sprite=sharp(path.join(root,rec.file)).resize(a.size[0],a.size[1],{kernel:'nearest'});if(a.radius)sprite=sprite.rotate(p.angle*180/Math.PI,{background:'#00000000'});const buf=await sprite.png().toBuffer(),meta=await sharp(buf).metadata();review.push({input:buf,left:Math.max(0,Math.round(p.x-meta.width/2)),top:Math.max(0,Math.round(p.y-meta.height/2))});}
  const rain=weather.drops(previous.mapLayout.weather.count,W,H).map(d=>{const p=weather.pose(d,0,W,H);return`<path d="M${Math.round(p.x)} ${Math.round(p.y)} l-4 ${d.length}" stroke="#d8ead4" stroke-width="1.5" opacity="${d.opacity.toFixed(2)}"/>`;}).join('');
  review.push({input:svg(rain),left:0,top:0});
  await save(sharp(worldFile).composite(review),'world_review','Animated water frame zero with map objects and rain','Version 7 layers');
  await save(sharp(path.join(out,'world_review.png')).extract({left:90,top:320,width:1100,height:850}),
    'animated_water_review','Six-frame sludge water in the western expansion','world_review.png');

  const animation={frameWidth:S,frameHeight:S,frameCount:FRAMES,fps:FPS,frameDurationMs:1000/FPS,loop:true,spritesheet:'assets/v7/sludge_water_6f.png',frames:frameFiles.map((_,i)=>`assets/v7/water_frame_${String(i).padStart(2,'0')}.png`),sheetLayout:'horizontal, left to right',terrainOverlay:'assets/v7/terrain_overlay.png'};
  fs.writeFileSync(path.join(root,'water_animation_v7.json'),JSON.stringify(animation,null,2)+'\n');
  const manifest={...previous,version:7,assets,mapLayout:{...previous.mapLayout,
    baseImage:'assets/v7/world_terrain.png',terrainOverlay:animation.terrainOverlay,waterAnimation:animation},
    revisionNotes:[...previous.revisionNotes,'The sludge ocean now animates with six seamless 256x256 frames at eight frames per second beneath a static transparent land overlay.']};
  fs.writeFileSync(path.join(root,'manifest_v7.json'),JSON.stringify(manifest,null,2)+'\n');
  fs.writeFileSync(path.join(root,'manifest_v7.js'),`window.COAST_MANIFEST=${JSON.stringify(manifest)};\nwindow.COAST_STORY=${fs.readFileSync(path.join(root,'story.json'),'utf8')};\n`);
  const pairDifferences=frames.map((f,i)=>meanDifference(f,frames[(i+1)%FRAMES]));
  const seamDifferences=frames.map(edgeDifference);
  const uniqueHashes=new Set(frames.map(f=>crypto.createHash('sha256').update(f).digest('hex')));
  const originalAlpha=await sharp(landOriginal).extractChannel(3).raw().toBuffer();
  const overlayAlpha=await sharp(overlayFile).extractChannel(3).raw().toBuffer();
  let alphaDifferences=0;for(let i=0;i<originalAlpha.length;i++)if(originalAlpha[i]!==overlayAlpha[i])alphaDifferences++;
  const issues=[];
  if(uniqueHashes.size!==FRAMES)issues.push('Water frames are not unique');
  if(Math.max(...seamDifferences)>0)issues.push('A water frame has a nonmatching tile edge');
  if(Math.min(...pairDifferences)<1)issues.push('Water motion too subtle');
  if(Math.max(...pairDifferences)>Math.min(...pairDifferences)*1.7)issues.push('Uneven frame-to-frame or frame-six-to-one motion');
  if(alphaDifferences)issues.push(`Terrain overlay alpha changed at ${alphaDifferences} pixels`);
  for(const a of assets)if(!fs.existsSync(path.join(root,a.file)))issues.push(`Missing asset ${a.id}`);
  const report={version:7,frameCount:FRAMES,frameSize:[S,S],fps:FPS,frameDurationMs:1000/FPS,uniqueFrames:uniqueHashes.size,pairDifferences,seamDifferences,terrainAlphaDifferences:alphaDifferences,shorelinePixelsPaletteSwapped:landSludge.swapped,totalManifestAssets:assets.length,newExports:made.length,issues};
  fs.writeFileSync(path.join(root,'verification_v7.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report));if(issues.length)process.exitCode=1;
}
main().catch(e=>{console.error(e);process.exitCode=1;});
