const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const sharp = require('sharp');

const root = path.resolve(__dirname, '../coastline');
const out = path.join(root, 'assets/v8');
const prior = JSON.parse(fs.readFileSync(path.join(root, 'manifest_v7.json'), 'utf8'));
const [W, H] = prior.mapLayout.canvas;
const assets = prior.assets.filter(a => !['world_terrain', 'world_review'].includes(a.id));
const created = [];
fs.mkdirSync(out, { recursive: true });

async function save(pipeline, id, role, source) {
  const file = path.join(out, `${id}.png`);
  await pipeline.png().toFile(file);
  const bytes = fs.readFileSync(file);
  const meta = await sharp(bytes).metadata();
  const raw = await sharp(bytes).ensureAlpha().raw().toBuffer();
  let transparentPixels = 0;
  for (let i = 3; i < raw.length; i += 4) if (raw[i] === 0) transparentPixels++;
  const record = { id, file: `assets/v8/${id}.png`, width: meta.width, height: meta.height,
    transparentPixels, role, source, sha256: crypto.createHash('sha256').update(bytes).digest('hex') };
  assets.push(record);
  created.push(record);
  return file;
}

async function cropAlpha(file) {
  const { data, info } = await sharp(file).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  let x0 = info.width, y0 = info.height, x1 = -1, y1 = -1;
  for (let y = 0; y < info.height; y++) for (let x = 0; x < info.width; x++) {
    if (data[(y * info.width + x) * 4 + 3] > 12) {
      x0 = Math.min(x0, x); y0 = Math.min(y0, y);
      x1 = Math.max(x1, x); y1 = Math.max(y1, y);
    }
  }
  if (x1 < x0) throw Error(`Empty alpha in ${file}`);
  return sharp(file).extract({ left: x0, top: y0, width: x1 - x0 + 1, height: y1 - y0 + 1 }).png().toBuffer();
}

function hsv(r, g, b) {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b), d = max - min;
  let h = 0;
  if (d) {
    if (max === r) h = ((g - b) / d) % 6;
    else if (max === g) h = (b - r) / d + 2;
    else h = (r - g) / d + 4;
    h = (h * 60 + 360) % 360;
  }
  return [h, max ? d / max : 0, max];
}
function rgb(h, s, v) {
  const c = v * s, x = c * (1 - Math.abs((h / 60) % 2 - 1)), m = v - c;
  const q = h < 60 ? [c, x, 0] : h < 120 ? [x, c, 0] : h < 180 ? [0, c, x]
    : h < 240 ? [0, x, c] : h < 300 ? [x, 0, c] : [c, 0, x];
  return q.map(n => Math.round((n + m) * 255));
}
async function paletteSludge(input) {
  const { data, info } = await sharp(input).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  for (let i = 0; i < data.length; i += 4) {
    if (data[i + 3] < 32) continue;
    const [h, s, v] = hsv(data[i], data[i + 1], data[i + 2]);
    if (h < 160 || h > 255 || s < .22 || v < .12 || data[i + 2] < data[i] * 1.2) continue;
    const [r, g, b] = rgb(Math.max(70, Math.min(105, h - 125)), Math.max(.36, Math.min(.56, s * .43 + .07)), Math.min(1, v * (v > .52 ? .82 : .65)));
    data[i] = r; data[i + 1] = g; data[i + 2] = b;
  }
  return sharp(data, { raw: { width: info.width, height: info.height, channels: 4 } }).png().toBuffer();
}
async function icon(source, id, role) {
  const cropped = await cropAlpha(path.join(root, source));
  const resized = await sharp(cropped).resize(380, 380, { fit: 'contain', background: '#00000000', kernel: 'nearest' }).png().toBuffer();
  return save(sharp(await paletteSludge(resized)), id, role, source);
}
async function terrain(excludePlateau, fortressFile) {
  const layers = [];
  for (const t of prior.mapLayout.terrain) {
    if (excludePlateau && t.id === 'plateau') continue;
    const [x, y, w, h] = t.rect;
    layers.push({ input: await sharp(path.join(root, t.file)).resize(w, h, { kernel: 'nearest' }).png().toBuffer(), left: x, top: y });
  }
  const rawBase = await sharp({ create: { width: W, height: H, channels: 4, background: '#00000000' } }).composite(layers).png().toBuffer();
  const swapped = await paletteSludge(rawBase);
  const protectedLayers = [];
  for (const t of prior.mapLayout.terrain.filter(t => t.id === 'portalBridge' || t.id.startsWith('old_'))) {
    const [x, y, w, h] = t.rect;
    protectedLayers.push({ input: await sharp(path.join(root, t.file)).resize(w, h, { kernel: 'nearest' }).png().toBuffer(), left: x, top: y });
  }
  const { data } = await sharp(swapped).composite(protectedLayers).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const original = await sharp(rawBase).ensureAlpha().raw().toBuffer();
  for (let i = 3; i < data.length; i += 4) data[i] = original[i];
  let overlay = await sharp(data, { raw: { width: W, height: H, channels: 4 } }).png().toBuffer();
  if (fortressFile) overlay = await sharp(overlay).composite([{ input: fs.readFileSync(fortressFile), left: 1260, top: 1585 }]).png().toBuffer();
  return overlay;
}
async function tileUnder(overlayFile) {
  const frame = fs.readFileSync(path.join(root, prior.mapLayout.waterAnimation.frames[0]));
  const tiles = [];
  for (let y = 0; y < H; y += 256) for (let x = 0; x < W; x += 256) tiles.push({ input: frame, left: x, top: y });
  return sharp({ create: { width: W, height: H, channels: 4, background: '#00000000' } }).composite([...tiles, { input: fs.readFileSync(overlayFile), left: 0, top: 0 }]).png().toBuffer();
}
function node(number, name, file, center, size, ground, flag) {
  return { id: `od0${number}`, number, name, file, center, size, ground, flag, hover: 18 };
}
async function skyMap(fortressFile) {
  const bands = ['#101b3b','#14234c','#192b58','#223666','#294371','#36517b','#506887','#637b96','#7e92a9','#9aabba','#b6bec6','#c9c6cc'];
  const stops = bands.map((c, i) => `<rect x="0" y="${i * H / bands.length}" width="${W}" height="${H / bands.length + 2}" fill="${c}"/>`).join('');
  const stars = Array.from({ length: 90 }, (_, i) => {
    const x = (i * 1319 + 53) % W, y = (i * 487 + 29) % 1000;
    return `<rect x="${x}" y="${y}" width="${i % 5 === 0 ? 5 : 2}" height="${i % 5 === 0 ? 5 : 2}" fill="#d9e4e8" opacity="${i % 4 === 0 ? .85 : .45}"/>`;
  }).join('');
  const svg = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">${stops}${stars}</svg>`);
  const layers = [];
  const cloudSpecs = [
    ['cloud_long',80,980,650,250],['cloud_cumulus',510,1370,440,290],['cloud_long',2390,1110,720,275],
    ['cloud_cumulus',2650,1610,550,355],['cloud_storm',60,1660,800,390],['cloud_long',30,1970,1100,330],
    ['cloud_cumulus',700,1940,660,390],['cloud_cumulus',2260,1930,860,430],['cloud_long',1130,2070,1140,260]
  ];
  for (const [id,x,y,w,h] of cloudSpecs) {
    const rec = assets.find(a => a.id === id);
    layers.push({ input: await sharp(path.join(root, rec.file)).resize(w,h,{kernel:'nearest'}).png().toBuffer(), left:x, top:y });
  }
  const fortress = await sharp(fortressFile).resize(1030,1160,{fit:'contain',background:'#00000000',kernel:'nearest'}).png().toBuffer();
  layers.splice(5,0,{ input: fortress, left: 1150, top: 930 });
  return sharp(svg).composite(layers).png().toBuffer();
}

async function main() {
  const bridgeFile = await icon('source/level_03_bridge_v8.png','level_03_bridge','Floating section 03 bridge icon');
  const cityFile = await icon('source/level_04_miami_v8.png','level_04_miami_center','Floating section 04 city-center icon');
  const plateauFile = await icon('source/level_05_plateau_v8.png','level_05_plateau','Floating section 05 plateau boss icon');
  const fortressCropped = await cropAlpha(path.join(root,'source/plateau_fortress_v8.png'));
  const fortressResized = await sharp(fortressCropped).resize(560,630,{fit:'contain',background:'#00000000',kernel:'nearest'}).png().toBuffer();
  const fortressFile = await save(sharp(await paletteSludge(fortressResized)),'plateau_fortress','Post-level-5 shattered plateau and sky fortress','source/plateau_fortress_v8.png');
  const postOverlayFile = await save(sharp(await terrain(true,fortressFile)),'poststorm_terrain_overlay','Transparent post-level-5 terrain overlay','Version 7 terrain without plateau plus fortress');
  const postBaseFile = await save(sharp(await tileUnder(postOverlayFile)),'poststorm_world_terrain','Post-level-5 world first water frame','poststorm_terrain_overlay plus water_frame_00');
  await save(sharp(await skyMap(fortressFile)),'sky_map_base','Above-cloud campaign map vista','plateau_fortress plus existing cloud sprites');

  const newNodes = [
    node(3,'Bridge to Miami','assets/v8/level_03_bridge.png',[1020,670],236,[1020,800],[1080,705]),
    node(4,'Center of Miami','assets/v8/level_04_miami_center.png',[420,280],242,[420,430],[485,330]),
    node(5,'The Plateau','assets/v8/level_05_plateau.png',[1540,1910],245,[1540,2060],[1600,1970])
  ];
  const nodes = [...prior.mapLayout.nodes,...newNodes];
  const preLayers = [];
  for (const n of newNodes) {
    preLayers.push({input:await sharp(path.join(root,n.file)).resize(n.size,n.size,{kernel:'nearest'}).png().toBuffer(),left:Math.round(n.center[0]-n.size/2),top:Math.round(n.center[1]-n.size/2)});
    preLayers.push({input:await sharp(path.join(root,`assets/v2/nss_flag${n.number}_av.png`)).resize(52,64,{kernel:'nearest'}).png().toBuffer(),left:n.flag[0]-26,top:n.flag[1]-64});
  }
  await save(sharp(path.join(root,'assets/v7/world_review.png')).composite(preLayers),'world_review','Five-section ground map review','Version 7 map plus sections 03–05');
  const postLayers = [];
  for (const n of nodes.filter(n=>n.number<=4)) {
    postLayers.push({input:await sharp(path.join(root,n.file)).resize(n.size,n.size,{kernel:'nearest'}).png().toBuffer(),left:Math.round(n.center[0]-n.size/2),top:Math.round(n.center[1]-n.size/2)});
    postLayers.push({input:await sharp(path.join(root,`assets/v2/nss_flag${n.number}_av.png`)).resize(52,64,{kernel:'nearest'}).png().toBuffer(),left:n.flag[0]-26,top:n.flag[1]-64});
  }
  postLayers.push({input:await sharp(path.join(root,'assets/v2/nss_flag5_done.png')).resize(65,78,{kernel:'nearest'}).png().toBuffer(),left:1570,top:1910});
  await save(sharp(postBaseFile).composite(postLayers),'poststorm_world_review','Fortress aftermath map review','Poststorm terrain plus section flags');

  const manifest = {...prior,version:8,assets,mapLayout:{...prior.mapLayout,nodes,
    postStormTerrainOverlay:'assets/v8/poststorm_terrain_overlay.png',
    postStormBaseImage:'assets/v8/poststorm_world_terrain.png',
    skyMap:{baseImage:'assets/v8/sky_map_base.png',anchor:'assets/v8/plateau_fortress.png',futureNodesDefined:false},
    focusBoxes:{...prior.mapLayout.focusBoxes,bridgeMiami:[720,400,700,610],downtown:[70,50,760,650],plateau:[1210,1550,730,700],fortress:[1160,1430,790,820],sky:[850,550,1600,1550]}},
    revisionNotes:[...prior.revisionNotes,'Sections 03–05: bridge to Miami, center of Miami, plateau. After section 05 a lightning storm destroys the plateau, raises an alien fortress, and shifts the campaign-map preview above the clouds.']};
  fs.writeFileSync(path.join(root,'manifest_v8.json'),JSON.stringify(manifest,null,2)+'\n');
  fs.writeFileSync(path.join(root,'manifest_v8.js'),`window.COAST_MANIFEST=${JSON.stringify(manifest)};\nwindow.COAST_STORY=${fs.readFileSync(path.join(root,'story_v8.json'),'utf8')};\n`);
  const issues=[];
  for (const a of assets) if (!fs.existsSync(path.join(root,a.file))) issues.push(`Missing ${a.file}`);
  const ids=assets.map(a=>a.id);if(new Set(ids).size!==ids.length)issues.push('Duplicate asset ID');
  for(const n of nodes)if(!fs.existsSync(path.join(root,n.file)))issues.push(`Missing node ${n.id}`);
  for(const n of nodes)if(n.center[0]<0||n.center[0]>=W||n.center[1]<0||n.center[1]>=H)issues.push(`Node outside canvas ${n.id}`);
  const story=JSON.parse(fs.readFileSync(path.join(root,'story_v8.json'),'utf8'));
  if(story.missions.length!==nodes.length||story.missions.some((m,i)=>m.number!==nodes[i].number))issues.push('Story and map section sequence differ');
  const plateauRegion={left:1200,top:1500,width:700,height:750};
  const before=await sharp(path.join(root,prior.mapLayout.terrainOverlay)).extract(plateauRegion).ensureAlpha().raw().toBuffer();
  const after=await sharp(postOverlayFile).extract(plateauRegion).ensureAlpha().raw().toBuffer();
  let changedPixels=0;for(let i=0;i<before.length;i+=4)if(before[i]!==after[i]||before[i+1]!==after[i+1]||before[i+2]!==after[i+2]||before[i+3]!==after[i+3])changedPixels++;
  if(changedPixels<20000)issues.push('Poststorm plateau replacement is missing or too small');
  if(prior.mapLayout.waterAnimation.frameCount!==6)issues.push('Six-frame water animation was not preserved');
  const report={version:8,sections:nodes.map(n=>({number:n.number,name:n.name,center:n.center})),
    postLevel5:'lightning storm > shattered plateau > fortress > sky map',skyFutureNodesDefined:false,
    poststormChangedPixels:changedPixels,waterFramesPreserved:prior.mapLayout.waterAnimation.frameCount,
    assets:assets.length,newExports:created.length,issues};
  fs.writeFileSync(path.join(root,'verification_v8.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report));if(issues.length)process.exitCode=1;
}
main().catch(e=>{console.error(e);process.exitCode=1});
