const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const sharp = require('sharp');
const root = path.resolve(__dirname, '../coastline');
const out = path.join(root, 'assets/v4');
const previous = JSON.parse(fs.readFileSync(path.join(root, 'manifest_v3.json'), 'utf8'));
const motion = require(path.join(root, 'map_motion_v3.js'));
const [W, H] = previous.mapLayout.canvas;
const bridgeRect = [800, 1105, 560, 215];
const assets = [...previous.assets];
const made = [];
fs.mkdirSync(out, { recursive: true });

async function save(pipeline, id, role, source) {
  const file = path.join(out, `${id}.png`);
  await pipeline.png().toFile(file);
  const bytes = fs.readFileSync(file);
  const meta = await sharp(bytes).metadata();
  const raw = await sharp(bytes).ensureAlpha().raw().toBuffer();
  let transparentPixels = 0;
  for (let i = 3; i < raw.length; i += 4) if (raw[i] === 0) transparentPixels++;
  const record = { id, file: `assets/v4/${id}.png`, width: meta.width, height: meta.height,
    transparentPixels, role, source, sha256: crypto.createHash('sha256').update(bytes).digest('hex') };
  assets.push(record);
  made.push(record);
  return file;
}

async function main() {
  const source = 'source/collapsed_bridge_v4.png';
  const bridgeFile = await save(sharp(path.join(root, source)).resize(bridgeRect[2], bridgeRect[3], { kernel: 'nearest' }),
    'collapsed_bridge', 'Collapsed coastal crossing', source);
  const bridgeBuffer = fs.readFileSync(bridgeFile);
  const terrain = [...previous.mapLayout.terrain,
    { id: 'collapsedBridge', file: 'assets/v4/collapsed_bridge.png', rect: bridgeRect }];
  const ambient = previous.mapLayout.ambient.map(a => a.id === 'patrolboat'
    ? { ...a, center: [1055, 1405], radius: [20, 45] } : { ...a });
  const terrainLayers = [];
  for (const t of terrain) {
    const [x, y, w, h] = t.rect;
    terrainLayers.push({ input: await sharp(path.join(root, t.file)).resize(w, h, { kernel: 'nearest' }).toBuffer(), left: x, top: y });
  }
  const { data: terrainAlpha } = await sharp({ create: { width: W, height: H, channels: 4, background: '#00000000' } })
    .composite(terrainLayers).extractChannel(3).raw().toBuffer({ resolveWithObject: true });
  const collisions = [];
  for (const a of ambient.filter(a => a.type === 'boat')) {
    const radius = Math.hypot(...a.size) / 2;
    for (let step = 0; step < 360; step++) {
      const time = step * Math.PI * 2 / (360 * Math.abs(a.speed));
      const p = motion.pose(a, time);
      for (let j = 0; j < 17; j++) {
        const angle = j * Math.PI * 2 / 16;
        const rr = j === 16 ? 0 : radius;
        const x = Math.round(p.x + Math.cos(angle) * rr);
        const y = Math.round(p.y + Math.sin(angle) * rr);
        if (x < 0 || y < 0 || x >= W || y >= H || terrainAlpha[y * W + x] > 64) {
          collisions.push({ boat: a.id, phaseSample: step, point: [x, y] });
          break;
        }
      }
    }
  }

  await save(sharp(path.join(root, previous.mapLayout.baseImage)).composite([
    { input: bridgeBuffer, left: bridgeRect[0], top: bridgeRect[1] }
  ]), 'world_terrain', 'Layered terrain composite only', 'Version 3 terrain plus collapsed bridge');

  const svg = body => Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">${body}</svg>`);
  const route = previous.mapLayout.flightRoute;
  const shadows = previous.mapLayout.nodes.map(n => `<ellipse cx="${n.ground[0]}" cy="${n.ground[1] - 38}" rx="${n.size * .38}" ry="23" fill="#001017" opacity=".58"/>`).join('');
  const review = [{ input: svg(`<path d="${route}" fill="none" stroke="#06203b" stroke-width="13"/><path d="${route}" fill="none" stroke="#80e7e8" stroke-width="4" stroke-dasharray="13 16"/>${shadows}`), left: 0, top: 0 }];
  for (const n of previous.mapLayout.nodes) {
    review.push({ input: await sharp(path.join(root, n.file)).resize(n.size, n.size, { kernel: 'nearest' }).toBuffer(), left: Math.round(n.center[0] - n.size / 2), top: Math.round(n.center[1] - n.size / 2) });
    review.push({ input: await sharp(path.join(root, `assets/v2/nss_flag${n.number}${n.number === 1 ? '_hi0' : '_av'}.png`)).resize(60, 72, { kernel: 'nearest' }).toBuffer(), left: n.flag[0] - 30, top: n.flag[1] - 72 });
  }
  for (const f of previous.mapLayout.originalFlags) review.push({ input: await sharp(path.join(root, `assets/v2/nss_flag${f.number}_av.png`)).resize(40, 48, { kernel: 'nearest' }).toBuffer(), left: Math.round(f.at[0] - 20), top: Math.round(f.at[1] - 48) });
  for (const a of ambient) {
    const p = motion.pose(a, 0);
    const rec = assets.find(r => r.id === a.sprite);
    let sprite = sharp(path.join(root, rec.file)).resize(a.size[0], a.size[1], { kernel: 'nearest' });
    if (a.radius) sprite = sprite.rotate(p.angle * 180 / Math.PI, { background: '#00000000' });
    const buffer = await sprite.png().toBuffer();
    const meta = await sharp(buffer).metadata();
    review.push({ input: buffer, left: Math.max(0, Math.round(p.x - meta.width / 2)), top: Math.max(0, Math.round(p.y - meta.height / 2)) });
  }
  await save(sharp(path.join(out, 'world_terrain.png')).composite(review), 'world_review', 'Map review with object placement at time zero', 'Version 4 layers');
  await save(sharp(path.join(out, 'world_review.png')).extract({ left: 660, top: 930, width: 930, height: 650 }),
    'collapsed_crossing_review', 'Collapsed bridge and both island shores detail', 'world_review.png');

  const manifest = { ...previous, version: 4, assets, mapLayout: { ...previous.mapLayout,
    terrain, ambient, baseImage: 'assets/v4/world_terrain.png',
    regions: { ...previous.mapLayout.regions, collapsedBridge: bridgeRect },
    focusBoxes: { ...previous.mapLayout.focusBoxes, crossing: [660, 930, 930, 650] } },
    revisionNotes: [...previous.revisionNotes, 'A separately exported, visibly impassable collapsed crossing now links the comet island and Miami coast. The intact northern city bridge and both level icons are unchanged.'] };
  fs.writeFileSync(path.join(root, 'manifest_v4.json'), JSON.stringify(manifest, null, 2) + '\n');
  fs.writeFileSync(path.join(root, 'manifest_v4.js'), `window.COAST_MANIFEST=${JSON.stringify(manifest)};\nwindow.COAST_STORY=${fs.readFileSync(path.join(root, 'story.json'), 'utf8')};\n`);
  const issues = [];
  if (!assets.find(a => a.id === 'collapsed_bridge').transparentPixels) issues.push('Bridge export lacks transparency');
  if (collisions.length) issues.push(`Boat patrol intersects bridge at ${collisions.length} sampled positions`);
  const report = { version: 4, bridgeRect, newExports: made.length, totalManifestAssets: assets.length,
    bridgeTransparency: assets.find(a => a.id === 'collapsed_bridge').transparentPixels,
    boatTerrainCollisionCheck: { stepsPerFullOrbit: 360, footprintPointsPerStep: 17, method: 'Boat circumcircle against full terrain alpha, including collapsed bridge', collisions: collisions.slice(0, 30), collisionCount: collisions.length }, issues };
  fs.writeFileSync(path.join(root, 'verification_v4.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report));
  if (issues.length) process.exitCode = 1;
}
main().catch(err => { console.error(err); process.exitCode = 1; });
