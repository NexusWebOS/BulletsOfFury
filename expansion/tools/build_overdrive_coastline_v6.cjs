const fs=require('fs');
const path=require('path');
const crypto=require('crypto');
const sharp=require('sharp');
const root=path.resolve(__dirname,'../coastline');
const out=path.join(root,'assets/v6');
const previous=JSON.parse(fs.readFileSync(path.join(root,'manifest_v5.json'),'utf8'));
const motion=require(path.join(root,'map_motion_v3.js'));
const weather=require(path.join(root,'map_weather_v6.js'));
const [W,H]=previous.mapLayout.canvas;
const assets=previous.assets.filter(a=>!['world_terrain','world_review'].includes(a.id));
const made=[];
fs.mkdirSync(out,{recursive:true});

async function save(pipeline,id,role,source){
  const file=path.join(out,`${id}.png`);
  await pipeline.png().toFile(file);
  const bytes=fs.readFileSync(file),meta=await sharp(bytes).metadata();
  const raw=await sharp(bytes).ensureAlpha().raw().toBuffer();
  let transparentPixels=0;for(let i=3;i<raw.length;i+=4)if(raw[i]===0)transparentPixels++;
  const rec={id,file:`assets/v6/${id}.png`,width:meta.width,height:meta.height,transparentPixels,role,source,sha256:crypto.createHash('sha256').update(bytes).digest('hex')};
  assets.push(rec);made.push(rec);return file;
}
function hsv(r,g,b){
  r/=255;g/=255;b/=255;
  const max=Math.max(r,g,b),min=Math.min(r,g,b),d=max-min;
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
    const [r,g,b]=rgb(newHue,newSat,newValue);
    data[i]=r;data[i+1]=g;data[i+2]=b;swapped++;
  }
  return{buffer:await sharp(data,{raw:{width:info.width,height:info.height,channels:4}}).png().toBuffer(),swapped};
}
function svg(body){return Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">${body}</svg>`);}

async function main(){
  const ocean=await sludge(path.join(root,'reference/existing_ocean.png'));
  await save(sharp(ocean.buffer),'sludge_ocean','Sludge water palette tile','reference/existing_ocean.png');
  const base=await sludge(path.join(root,previous.mapLayout.baseImage));
  const protectedTerrain=previous.mapLayout.terrain.filter(t=>t.id==='portalBridge'||t.id.startsWith('old_'));
  const protectedLayers=[];
  for(const t of protectedTerrain){const [x,y,w,h]=t.rect;protectedLayers.push({input:await sharp(path.join(root,t.file)).resize(w,h,{kernel:'nearest'}).toBuffer(),left:x,top:y});}
  const terrainFile=await save(sharp(base.buffer).composite(protectedLayers),
    'world_terrain','Layered terrain composite only','Version 5 terrain with sludge water; original islands and portal restored');
  const shield=previous.mapLayout.effects.find(e=>e.id==='voidPortalShield');
  const [sx,sy,sw,sh]=shield.rect;
  const shieldBuffer=await sharp(path.join(root,assets.find(a=>a.id===shield.sprite).file)).resize(sw,sh,{kernel:'nearest'}).toBuffer();
  const route=previous.mapLayout.flightRoute;
  const shadows=previous.mapLayout.nodes.map(n=>`<ellipse cx="${n.ground[0]}" cy="${n.ground[1]-38}" rx="${n.size*.38}" ry="23" fill="#001017" opacity=".58"/>`).join('');
  const review=[{input:shieldBuffer,left:sx,top:sy},{input:svg(`<path d="${route}" fill="none" stroke="#14261d" stroke-width="13"/><path d="${route}" fill="none" stroke="#a6dcc0" stroke-width="4" stroke-dasharray="13 16"/>${shadows}`),left:0,top:0}];
  for(const n of previous.mapLayout.nodes){
    review.push({input:await sharp(path.join(root,n.file)).resize(n.size,n.size,{kernel:'nearest'}).toBuffer(),left:Math.round(n.center[0]-n.size/2),top:Math.round(n.center[1]-n.size/2)});
    review.push({input:await sharp(path.join(root,`assets/v2/nss_flag${n.number}${n.number===1?'_hi0':'_av'}.png`)).resize(60,72,{kernel:'nearest'}).toBuffer(),left:n.flag[0]-30,top:n.flag[1]-72});
  }
  for(const f of previous.mapLayout.originalFlags)review.push({input:await sharp(path.join(root,`assets/v2/nss_flag${f.number}_av.png`)).resize(40,48,{kernel:'nearest'}).toBuffer(),left:Math.round(f.at[0]-20),top:Math.round(f.at[1]-48)});
  for(const a of previous.mapLayout.ambient){
    const p=motion.pose(a,0),rec=assets.find(r=>r.id===a.sprite);
    let sprite=sharp(path.join(root,rec.file)).resize(a.size[0],a.size[1],{kernel:'nearest'});
    if(a.radius)sprite=sprite.rotate(p.angle*180/Math.PI,{background:'#00000000'});
    const buf=await sprite.png().toBuffer(),meta=await sharp(buf).metadata();
    review.push({input:buf,left:Math.max(0,Math.round(p.x-meta.width/2)),top:Math.max(0,Math.round(p.y-meta.height/2))});
  }
  const rain=weather.drops(1250,W,H).map(d=>{const p=weather.pose(d,0,W,H);return`<path d="M${Math.round(p.x)} ${Math.round(p.y)} l-4 ${d.length}" stroke="#d8ead4" stroke-width="1.5" opacity="${d.opacity.toFixed(2)}"/>`;}).join('');
  review.push({input:svg(rain),left:0,top:0});
  await save(sharp(terrainFile).composite(review),'world_review','Rainy sludge map review at time zero','Version 6 layers');
  await save(sharp(path.join(out,'world_review.png')).extract({left:90,top:320,width:1100,height:850}),
    'sludge_portal_review','Rainy sludge water around portal and coast','world_review.png');
  const manifest={...previous,version:6,assets,mapLayout:{...previous.mapLayout,
    baseImage:'assets/v6/world_terrain.png',waterPalette:{type:'sludge',source:'reference/existing_ocean.png',tile:'assets/v6/sludge_ocean.png',method:'Blue and cyan water hues shifted to deep moss and toxic olive while retaining pixel texture'},
    weather:{type:'rain',count:1250,wind:-42,speed:[185,320],toggleDefault:true}},
    revisionNotes:[...previous.revisionNotes,'The world water is palette-swapped to dark moss and toxic olive sludge. Animated diagonal rain covers the map, with a preview toggle.']};
  fs.writeFileSync(path.join(root,'manifest_v6.json'),JSON.stringify(manifest,null,2)+'\n');
  fs.writeFileSync(path.join(root,'manifest_v6.js'),`window.COAST_MANIFEST=${JSON.stringify(manifest)};\nwindow.COAST_STORY=${fs.readFileSync(path.join(root,'story.json'),'utf8')};\n`);
  const oldAlpha=await sharp(path.join(root,previous.mapLayout.baseImage)).extractChannel(3).raw().toBuffer();
  const newAlpha=await sharp(terrainFile).extractChannel(3).raw().toBuffer();
  let alphaDifferences=0;for(let i=0;i<oldAlpha.length;i++)if(oldAlpha[i]!==newAlpha[i])alphaDifferences++;
  const issues=[];if(base.swapped<1000000)issues.push('Too few map pixels palette swapped');if(alphaDifferences)issues.push(`Terrain alpha changed at ${alphaDifferences} pixels`);
  for(const a of assets)if(!fs.existsSync(path.join(root,a.file)))issues.push(`Missing ${a.id}`);
  const report={version:6,swappedMapPixels:base.swapped,swappedOceanTilePixels:ocean.swapped,rainDrops:1250,terrainAlphaDifferences:alphaDifferences,totalManifestAssets:assets.length,newExports:made.length,issues};
  fs.writeFileSync(path.join(root,'verification_v6.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report));if(issues.length)process.exitCode=1;
}
main().catch(e=>{console.error(e);process.exitCode=1;});
