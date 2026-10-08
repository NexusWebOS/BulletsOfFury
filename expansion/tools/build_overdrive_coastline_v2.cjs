const fs=require('fs'),path=require('path'),sharp=require('sharp'),crypto=require('crypto');
const root=path.resolve(__dirname,'../coastline'),out=path.join(root,'assets/v2');
const game='C:/Users/Mike/Desktop/Github Coding/BulletsOfFury';
const records=[];
async function save(p,name,role,source){const file=path.join(out,name+'.png');await p.png().toFile(file);const bytes=fs.readFileSync(file),m=await sharp(bytes).metadata(),{data}=await sharp(bytes).ensureAlpha().raw().toBuffer({resolveWithObject:true});let transparent=0;for(let i=3;i<data.length;i+=4)if(data[i]===0)transparent++;records.push({id:name,file:'assets/v2/'+name+'.png',width:m.width,height:m.height,transparentPixels:transparent,role,source,sha256:crypto.createHash('sha256').update(bytes).digest('hex')});}
async function sprite(source,name,rect,size,role){let p=sharp(path.join(root,source));if(rect)p=p.extract({left:rect[0],top:rect[1],width:rect[2],height:rect[3]});const crop=await p.png().toBuffer();const b=await sharp(crop).trim({threshold:8}).png().toBuffer();await save(sharp(b).resize(size[0]-16,size[1]-16,{fit:'contain',background:'#00000000',kernel:'nearest'}).extend({top:8,bottom:8,left:8,right:8,background:'#00000000'}),name,role,source);}
function svg(w,h,body){return Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">${body}</svg>`);}
(async()=>{
fs.mkdirSync(out,{recursive:true});
await save(sharp(path.join(root,'source/coast_terrain_v2.png')).resize(660,880,{kernel:'nearest'}),'coast_terrain','Terrain, no baked mission landmarks','source/coast_terrain_v2.png');
await save(sharp(path.join(root,'source/major_city_v2.png')).resize(680,544,{kernel:'nearest'}),'major_city','Northwest city region','source/major_city_v2.png');
await save(sharp(path.join(root,'source/city_bridge_v2.png')).resize(600,400,{kernel:'nearest'}),'city_bridge','Separate northwest causeway','source/city_bridge_v2.png');
const islands=[['island_beach',[0,70,512,440],[260,230]],['island_lagoon',[515,70,505,440],[280,240]],['island_ruins',[1030,60,506,450],[280,260]],['island_cove',[0,540,510,484],[280,240]],['central_plateau',[511,515,575,509],[340,320]]];
for(const [id,rect,size]of islands)await sprite('source/southern_islands_v2.png',id,rect,size,'Separate southern island');
const obj=[['cloud_long',[0,70,438,315],[256,160]],['cloud_cumulus',[443,65,370,325],[200,170]],['cloud_storm',[817,65,437,320],[256,170]],['boat_motor',[85,420,260,417],[72,120]],['boat_patrol',[495,420,264,417],[72,132]],['boat_cargo',[898,420,275,420],[80,140]],['drone_scout',[80,850,265,350],[96,112]],['drone_trident',[452,840,343,365],[112,120]],['drone_manta',[820,840,419,367],[132,120]]];
for(const [id,rect,size]of obj)await sprite('source/map_objects_v2.png',id,rect,size,'Independent ambient map object');
const manifestSource=fs.readFileSync(path.join(game,'assets/manifest.js'),'utf8');
const flagKeys=[];
for(let n=1;n<=8;n++)for(const state of ['av','done','lock','hi0','hi1'])flagKeys.push('nss_flag'+n+'_'+state);
for(let n=0;n<8;n++)flagKeys.push('nss_cursor_'+n);
for(const key of flagKeys){const match=manifestSource.match(new RegExp('"'+key+'":\\["([^"]+)",(\\d+),(\\d+),(\\d+),(\\d+)\\]'));if(!match)throw Error('Missing atlas key '+key);const [,atlas,x,y,w,h]=match;await save(sharp(path.join(game,'assets/game/atlas/'+atlas+'.png')).extract({left:+x,top:+y,width:+w,height:+h}),key,'Existing original campaign flag/cursor','Original game atlas '+atlas+' / '+key);}
const terrain=[{id:'city',file:'assets/v2/major_city.png',rect:[90,40,680,544]}, {id:'bridge',file:'assets/v2/city_bridge.png',rect:[674,490,600,400]}, {id:'coast',file:'assets/v2/coast_terrain.png',rect:[1145,770,660,880]},
{id:'beach',file:'assets/v2/island_beach.png',rect:[950,1730,260,230]},{id:'lagoon',file:'assets/v2/island_lagoon.png',rect:[1760,1760,280,240]},{id:'ruins',file:'assets/v2/island_ruins.png',rect:[890,2030,280,260]},{id:'cove',file:'assets/v2/island_cove.png',rect:[1820,2060,280,240]},{id:'plateau',file:'assets/v2/central_plateau.png',rect:[1370,1895,340,320]}];
const pos={1:[120,117],2:[286,80],3:[444,117],4:[517,255],5:[497,390],6:[322,401],7:[137,389],8:[91,252],9:[575,75],hub:[304,245]};
const original=[];
for(const k of Object.keys(pos).sort((a,b)=>pos[a][1]-pos[b][1])){const p=pos[k],d=Math.round((k==='hub'?240:k==='9'?130:190)*.9),x=Math.round(2330+(p[0]*1.45+10)*.9-d/2),y=Math.round(700+(p[1]*1.45+10)*.9-d/2);const t={id:'old_'+k,file:'reference/isl_'+k+'.png',rect:[x,y,d,d]};terrain.push(t);if(k!=='hub'&&k!=='9')original.push({number:+k,at:[x+d*.5,y+d*.7]});}
const nodes=[{id:'od01',number:1,name:'Military compound',file:'assets/level_01_compound.png',center:[1555,1385],size:244,ground:[1555,1515],flag:[1605,1445],hover:18},{id:'od02',number:2,name:'North gate / highway',file:'assets/level_02_gate_highway.png',center:[1400,1135],size:230,ground:[1400,1260],flag:[1450,1200],hover:18}];
const ambient=[
{id:'motorboat',sprite:'boat_motor',center:[1950,1640],radius:[160,80],speed:.11,phase:.4,size:[38,64],type:'boat'},
{id:'patrolboat',sprite:'boat_patrol',center:[1930,1100],radius:[120,235],speed:-.095,phase:2.2,size:[38,70],type:'boat'},
{id:'cargoboat',sprite:'boat_cargo',center:[870,1470],radius:[160,100],speed:.07,phase:2.8,size:[48,84],type:'boat'},
{id:'scout',sprite:'drone_scout',center:[1510,1100],radius:[330,180],speed:.23,phase:.1,size:[57,66],type:'drone'},
{id:'trident',sprite:'drone_trident',center:[1620,1390],radius:[280,165],speed:.18,phase:2.5,size:[68,72],type:'drone'},
{id:'manta',sprite:'drone_manta',center:[1550,1570],radius:[350,130],speed:-.14,phase:4.5,size:[79,72],type:'drone'},
{id:'cloud_a',sprite:'cloud_long',center:[1210,650],speed:8,phase:0,size:[340,212],type:'cloud'},
{id:'cloud_b',sprite:'cloud_cumulus',center:[2050,710],speed:-6,phase:0,size:[220,187],type:'cloud'},
{id:'cloud_c',sprite:'cloud_long',center:[620,1570],speed:5,phase:0,size:[285,178],type:'cloud'},
{id:'cloud_d',sprite:'cloud_storm',center:[1960,1990],speed:-4,phase:0,size:[300,199],type:'cloud'},
{id:'cloud_e',sprite:'cloud_cumulus',center:[680,2200],speed:7,phase:0,size:[235,200],type:'cloud'}];
const W=3328,H=2304,layers=[],ocean=await sharp(path.join(root,'reference/existing_ocean.png')).resize(256,256,{kernel:'nearest'}).toBuffer();
for(let y=0;y<H;y+=256)for(let x=0;x<W;x+=256)layers.push({input:ocean,left:x,top:y});
for(const t of terrain){const [x,y,w,h]=t.rect;layers.push({input:await sharp(path.join(root,t.file)).resize(w,h,{kernel:'nearest'}).toBuffer(),left:x,top:y});}
await save(sharp({create:{width:W,height:H,channels:4,background:'#031629'}}).composite(layers),'world_terrain','Layered terrain composite only','layout in manifest');
const routePath='M2440 1340 C2300 1520 2030 1580 1800 1520 S1690 1460 1610 1450';
const routeSvg=svg(W,H,`<path d="${routePath}" fill="none" stroke="#06203b" stroke-width="13"/><path d="${routePath}" fill="none" stroke="#80e7e8" stroke-width="4" stroke-dasharray="13 16"/>`);fs.writeFileSync(path.join(out,'flight_route.svg'),routeSvg);
const review=[{input:routeSvg,left:0,top:0}];
review.push({input:svg(W,H,nodes.map(n=>`<ellipse cx="${n.ground[0]}" cy="${n.ground[1]-38}" rx="${n.size*.38}" ry="23" fill="#001017" opacity=".58"/>`).join('')),left:0,top:0});
for(const n of nodes){review.push({input:await sharp(path.join(root,n.file)).resize(n.size,n.size,{kernel:'nearest'}).toBuffer(),left:Math.round(n.center[0]-n.size/2),top:Math.round(n.center[1]-n.size/2)});review.push({input:await sharp(path.join(out,'nss_flag'+n.number+(n.number===1?'_hi0':'_av')+'.png')).resize(60,72,{kernel:'nearest'}).toBuffer(),left:n.flag[0]-30,top:n.flag[1]-72});}
for(const f of original)review.push({input:await sharp(path.join(out,'nss_flag'+f.number+'_av.png')).resize(40,48,{kernel:'nearest'}).toBuffer(),left:Math.round(f.at[0]-20),top:Math.round(f.at[1]-48)});
for(const a of ambient){let x=a.center[0],y=a.center[1];if(a.radius){x+=a.radius[0]*Math.cos(a.phase);y+=a.radius[1]*Math.sin(a.phase);}const b=await sharp(path.join(out,a.sprite+'.png')).resize(a.size[0],a.size[1],{kernel:'nearest'}).toBuffer();review.push({input:b,left:Math.round(x-a.size[0]/2),top:Math.round(y-a.size[1]/2)});}
await save(sharp(path.join(out,'world_terrain.png')).composite(review),'world_review','Static review with independent icon, flag and ambient layers','Layer manifest');
await save(sharp(path.join(out,'world_review.png')).extract({left:950,top:860,width:1060,height:840}),'coast_detail_review','Review crop of hovering level icons','world_review.png');
const manifest={version:2,project:'Bullets of Fury — Overdrive',status:'Art and animated map preview; no game runtime integration',mapLayout:{canvas:[W,H],terrain,nodes,originalFlags:original,ambient,flightRoute:routePath,regions:{coast:[1145,770,660,880],northwestCity:[90,40,680,544],bridge:[674,490,600,400],southernArchipelago:[890,1730,1210,570]},iconBehavior:'Independent sprites hover over grass; original numbered flags remain attached to each sprite.',flagStates:{available:'av',selected:['hi0','hi1'],locked:'lock',completed:'done'},ambientBehavior:'Boat water patrols, drone ellipses and cloud drift; runtime coordinates are separate from PNG art'},assets:records};
fs.writeFileSync(path.join(root,'manifest_v2.json'),JSON.stringify(manifest,null,2)+'\n');fs.writeFileSync(path.join(root,'manifest_v2.js'),'window.COAST_MANIFEST='+JSON.stringify(manifest)+';\nwindow.COAST_STORY='+fs.readFileSync(path.join(root,'story.json'),'utf8')+';\n');
const issues=[];for(const a of records){if(!a.width||!a.height)issues.push(a.id+' invalid dimensions');if(!a.id.startsWith('world_')&&a.id!=='coast_detail_review'&&a.transparentPixels===0)issues.push(a.id+' missing transparency');}for(const t of terrain)if(!fs.existsSync(path.join(root,t.file)))issues.push('Missing '+t.file);
fs.writeFileSync(path.join(root,'verification_v2.json'),JSON.stringify({exports:records.length,terrainPieces:terrain.length,hoveringLevelIcons:nodes.length,ambientObjects:ambient.length,southernIslands:5,issues},null,2)+'\n');console.log(JSON.stringify({exports:records.length,issues}));
})().catch(e=>{console.error(e);process.exitCode=1;});
