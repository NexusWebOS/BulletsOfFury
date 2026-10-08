const fs=require('fs'),path=require('path'),sharp=require('sharp'),crypto=require('crypto');
const root=path.resolve(__dirname,'../coastline'),out=path.join(root,'assets/v3'),motion=require(path.join(root,'map_motion_v3.js'));
const base=JSON.parse(fs.readFileSync(path.join(root,'manifest_v2.json'),'utf8'));
const records=base.assets.filter(a=>!['world_terrain','world_review','coast_detail_review'].includes(a.id));
const created=[];
function svg(w,h,body){return Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">${body}</svg>`);}
async function save(p,id,role,source){const file=path.join(out,id+'.png');await p.png().toFile(file);const bytes=fs.readFileSync(file),m=await sharp(bytes).metadata(),{data}=await sharp(bytes).ensureAlpha().raw().toBuffer({resolveWithObject:true});let transparent=0;for(let i=3;i<data.length;i+=4)if(data[i]===0)transparent++;const a={id,file:'assets/v3/'+id+'.png',width:m.width,height:m.height,transparentPixels:transparent,role,source,sha256:crypto.createHash('sha256').update(bytes).digest('hex')};records.push(a);created.push(a);}
async function sprite(source,id,rect,size,role){let p=sharp(path.join(root,source));if(rect)p=p.extract({left:rect[0],top:rect[1],width:rect[2],height:rect[3]});const crop=await p.png().toBuffer(),trim=await sharp(crop).trim({threshold:8}).png().toBuffer();await save(sharp(trim).resize(size[0]-16,size[1]-16,{fit:'contain',background:'#00000000',kernel:'nearest'}).extend({top:8,bottom:8,left:8,right:8,background:'#00000000'}),id,role,source);}
(async()=>{
fs.mkdirSync(out,{recursive:true});
await sprite('source/comet_island_v3.png','comet_island',null,[880,920],'Comet-struck coastal region');
const six=[['cloud_comet_storm',[300,210]],['cloud_ashen',[300,210]],['cloud_spores',[230,240]],['comet_reef',[150,150]],['corrupted_shipwreck',[200,145]],['dead_palm_islet',[155,165]]];
for(let i=0;i<six.length;i++){const [id,size]=six[i];await sprite('source/comet_surrounds_v3.png',id,[i%3*512,Math.floor(i/3)*512,512,512],size,i<3?'Independent ambient map object':'Corrupted coastal surround');}
const terrain=[...base.mapLayout.terrain,{id:'cometIsland',file:'assets/v3/comet_island.png',rect:[110,780,880,920]},
{id:'reefNorth',file:'assets/v3/comet_reef.png',rect:[165,660,135,135]},
{id:'reefSouth',file:'assets/v3/comet_reef.png',rect:[780,1700,125,125]},
{id:'shipwreck',file:'assets/v3/corrupted_shipwreck.png',rect:[1030,1510,165,120]},
{id:'deadIslet',file:'assets/v3/dead_palm_islet.png',rect:[185,1660,140,150]}];
const ambient=[
{id:'motorboat',sprite:'boat_motor',center:[490,1920],radius:[260,85],speed:.11,phase:.4,size:[38,64],type:'boat'},
{id:'patrolboat',sprite:'boat_patrol',center:[1060,1200],radius:[34,225],speed:-.095,phase:2.2,size:[38,70],type:'boat'},
{id:'cargoboat',sprite:'boat_cargo',center:[515,695],radius:[145,28],speed:.07,phase:2.8,size:[48,84],type:'boat'},
{id:'comet_scout',sprite:'drone_scout',center:[550,1140],radius:[440,285],speed:.19,phase:.1,size:[57,66],type:'drone'},
{id:'comet_manta',sprite:'drone_manta',center:[600,1270],radius:[480,375],speed:-.14,phase:3.7,size:[79,72],type:'drone'},
{id:'bridge_trident',sprite:'drone_trident',center:[1030,830],radius:[430,180],speed:.17,phase:2.5,size:[68,72],type:'drone'},
{id:'coastal_scout',sprite:'drone_scout',center:[1530,1230],radius:[290,345],speed:.23,phase:1.1,size:[57,66],type:'drone'},
{id:'southern_manta',sprite:'drone_manta',center:[1280,1920],radius:[430,220],speed:.14,phase:4.5,size:[79,72],type:'drone'},
{id:'city_trident',sprite:'drone_trident',center:[470,360],radius:[380,240],speed:-.12,phase:1.7,size:[62,66],type:'drone'},
...base.mapLayout.ambient.filter(a=>a.type==='cloud'&&a.id!=='cloud_c').map(a=>({...a,drift:90})),
{id:'north_ash',sprite:'cloud_ashen',center:[435,755],speed:4,phase:.6,drift:65,size:[310,217],type:'cloud'},
{id:'western_storm',sprite:'cloud_comet_storm',center:[155,1020],speed:3,phase:.8,drift:35,size:[260,182],type:'cloud'},
{id:'eastern_storm',sprite:'cloud_comet_storm',center:[1010,840],speed:-4,phase:2.2,drift:70,size:[260,182],type:'cloud'},
{id:'southern_ash',sprite:'cloud_ashen',center:[690,1720],speed:5,phase:1.5,drift:85,size:[260,182],type:'cloud'},
{id:'western_spores',sprite:'cloud_spores',center:[140,1400],speed:2,phase:2.1,drift:25,size:[180,188],type:'cloud'},
{id:'eastern_spores',sprite:'cloud_spores',center:[1030,1530],speed:-3,phase:.7,drift:35,size:[185,193],type:'cloud'},
{id:'southern_cumulus',sprite:'cloud_cumulus',center:[430,2000],speed:5,phase:.3,drift:100,size:[230,195],type:'cloud'}];
const [W,H]=base.mapLayout.canvas,layers=[],terrainLayers=[],ocean=await sharp(path.join(root,'reference/existing_ocean.png')).resize(256,256,{kernel:'nearest'}).toBuffer();
for(let y=0;y<H;y+=256)for(let x=0;x<W;x+=256)layers.push({input:ocean,left:x,top:y});
for(const t of terrain){const [x,y,w,h]=t.rect;terrainLayers.push({input:await sharp(path.join(root,t.file)).resize(w,h,{kernel:'nearest'}).toBuffer(),left:x,top:y});}
await save(sharp({create:{width:W,height:H,channels:4,background:'#031629'}}).composite([...layers,...terrainLayers]),'world_terrain','Layered terrain composite only','Version 3 terrain layout');
const {data:mask}=await sharp({create:{width:W,height:H,channels:4,background:'#00000000'}}).composite(terrainLayers).extractChannel(3).raw().toBuffer({resolveWithObject:true});
const collisions=[];
for(const a of ambient.filter(a=>a.type==='boat')){const radius=Math.hypot(...a.size)/2;for(let step=0;step<360;step++){const t=step*Math.PI*2/(360*Math.abs(a.speed)),p=motion.pose(a,t);for(let j=0;j<17;j++){const ang=j*Math.PI*2/16,r=j===16?0:radius,x=Math.round(p.x+Math.cos(ang)*r),y=Math.round(p.y+Math.sin(ang)*r);if(x<0||y<0||x>=W||y>=H||mask[y*W+x]>64){collisions.push({boat:a.id,phaseSample:step,point:[x,y]});break;}}}}
const nodeOverlay=base.mapLayout.nodes.map(n=>`<ellipse cx="${n.ground[0]}" cy="${n.ground[1]-38}" rx="${n.size*.38}" ry="23" fill="#001017" opacity=".58"/>`).join('');
const route=base.mapLayout.flightRoute,review=[{input:svg(W,H,`<path d="${route}" fill="none" stroke="#06203b" stroke-width="13"/><path d="${route}" fill="none" stroke="#80e7e8" stroke-width="4" stroke-dasharray="13 16"/>${nodeOverlay}`),left:0,top:0}];
for(const n of base.mapLayout.nodes){review.push({input:await sharp(path.join(root,n.file)).resize(n.size,n.size,{kernel:'nearest'}).toBuffer(),left:Math.round(n.center[0]-n.size/2),top:Math.round(n.center[1]-n.size/2)});review.push({input:await sharp(path.join(root,'assets/v2/nss_flag'+n.number+(n.number===1?'_hi0':'_av')+'.png')).resize(60,72,{kernel:'nearest'}).toBuffer(),left:n.flag[0]-30,top:n.flag[1]-72});}
for(const f of base.mapLayout.originalFlags)review.push({input:await sharp(path.join(root,'assets/v2/nss_flag'+f.number+'_av.png')).resize(40,48,{kernel:'nearest'}).toBuffer(),left:Math.round(f.at[0]-20),top:Math.round(f.at[1]-48)});
for(const a of ambient){const p=motion.pose(a,0),rec=records.find(r=>r.id===a.sprite);let s=sharp(path.join(root,rec.file)).resize(a.size[0],a.size[1],{kernel:'nearest'});if(a.radius)s=s.rotate(p.angle*180/Math.PI,{background:'#00000000'});const buf=await s.png().toBuffer(),m=await sharp(buf).metadata();review.push({input:buf,left:Math.max(0,Math.round(p.x-m.width/2)),top:Math.max(0,Math.round(p.y-m.height/2))});}
await save(sharp(path.join(out,'world_terrain.png')).composite(review),'world_review','Map review with object placement at time zero','Version 3 layers');
await save(sharp(path.join(out,'world_review.png')).extract({left:0,top:560,width:2050,height:1630}),'western_expansion_review','Comet island and surrounding expansion detail','world_review.png');
const manifest={...base,version:3,assets:records,mapLayout:{...base.mapLayout,terrain,ambient,baseImage:'assets/v3/world_terrain.png',regions:{...base.mapLayout.regions,cometIsland:[110,780,880,920]},focusBoxes:{full:[0,0,W,H],coast:[1060,840,1000,880],south:[760,1670,1450,634],city:[20,0,1320,960],comet:[0,620,2050,1170],expansion:[0,30,2110,2274]},ambientBehavior:'All three boats patrol western water. Six drones orbit the new expansion regions. Eleven cloud objects drift independently around coast and comet island.'},revisionNotes:['New comet-struck giant island placed in user-indicated western water below the bridge.','No new numbered level assigned to this geography. Sections 1 and 2 keep their separate hovering icons and original flags.','The existing green coast, northwest city/bridge, southern islands and original campaign remain in their previous positions.']};
fs.writeFileSync(path.join(root,'manifest_v3.json'),JSON.stringify(manifest,null,2)+'\n');fs.writeFileSync(path.join(root,'manifest_v3.js'),'window.COAST_MANIFEST='+JSON.stringify(manifest)+';\nwindow.COAST_STORY='+fs.readFileSync(path.join(root,'story.json'),'utf8')+';\n');
const issues=created.filter(a=>!a.width||!a.height||(a.role!=='Layered terrain composite only'&&!a.id.includes('review')&&!a.transparentPixels)).map(a=>a.id+' invalid dimensions/transparency');if(collisions.length)issues.push('Boat route intersects terrain: '+collisions.length+' sampled positions');for(const a of ambient)if(!records.some(r=>r.id===a.sprite))issues.push('Missing sprite '+a.sprite);
const report={newExports:created.length,totalManifestAssets:records.length,boats:3,drones:6,cloudPlacements:ambient.filter(a=>a.type==='cloud').length,boatRouteCheck:{stepsPerFullOrbit:360,pointsPerStep:17,method:'Conservative circumcircle of boat sprite against terrain alpha, including reefs and wreckage',collisions},issues};fs.writeFileSync(path.join(root,'verification_v3.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({...report,boatRouteCheck:{...report.boatRouteCheck,collisions:collisions.slice(0,5)}}));if(issues.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
