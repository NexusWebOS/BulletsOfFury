const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const sharp = require('sharp');
const root = path.resolve(__dirname, '../coastline');
const out = path.join(root, 'assets/v5');
const previous = JSON.parse(fs.readFileSync(path.join(root, 'manifest_v4.json'), 'utf8'));
const motion = require(path.join(root, 'map_motion_v3.js'));
const [W, H] = previous.mapLayout.canvas;
const bridgeRect = [210, 390, 400, 500];
const shieldRect = [375, 540, 100, 150];
const assets = previous.assets.filter(a => !['world_terrain', 'world_review'].includes(a.id));
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
  const record = { id, file: `assets/v5/${id}.png`, width: meta.width, height: meta.height,
    transparentPixels, role, source, sha256: crypto.createHash('sha256').update(bytes).digest('hex') };
  assets.push(record);
  made.push(record);
  return file;
}

async function main() {
  const source = 'source/portal_bridge_v5.png';
  const bridgeFile = await save(sharp(path.join(root, source)).resize(bridgeRect[2], bridgeRect[3], { kernel: 'nearest' }),
    'portal_bridge', 'Void portal bridge', source);
  const bridgeBuffer = fs.readFileSync(bridgeFile);
  const shieldSource = 'source/portal_shield_v5.png';
  const shieldFile = await save(sharp(path.join(root, shieldSource)).resize(shieldRect[2], shieldRect[3], { kernel: 'nearest' }),
    'portal_shield', 'Independent portal shield effect', shieldSource);
  const shieldBuffer = fs.readFileSync(shieldFile);
  const terrain = [...previous.mapLayout.terrain,
    { id: 'portalBridge', file: 'assets/v5/portal_bridge.png', rect: bridgeRect }];
  const ambient = previous.mapLayout.ambient.map(a => {
    if (a.id === 'cargoboat') return { ...a, center: [660, 650], radius: [60, 25] };
    if (a.id === 'north_ash') return { ...a, center: [760, 960] };
    if (a.id === 'city_trident') return { ...a, phase: .4 };
    return { ...a };
  });
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
  ]), 'world_terrain', 'Layered terrain composite only', 'Version 4 terrain plus void portal bridge');

  const svg = body => Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">${body}</svg>`);
  const route = previous.mapLayout.flightRoute;
  const shadows = previous.mapLayout.nodes.map(n => `<ellipse cx="${n.ground[0]}" cy="${n.ground[1] - 38}" rx="${n.size * .38}" ry="23" fill="#001017" opacity=".58"/>`).join('');
  const review = [
    { input: shieldBuffer, left: shieldRect[0], top: shieldRect[1] },
    { input: svg(`<path d="${route}" fill="none" stroke="#06203b" stroke-width="13"/><path d="${route}" fill="none" stroke="#80e7e8" stroke-width="4" stroke-dasharray="13 16"/>${shadows}`), left: 0, top: 0 }
  ];
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
  await save(sharp(path.join(out, 'world_terrain.png')).composite(review), 'world_review', 'Map review with object placement at time zero', 'Version 5 layers');
  await save(sharp(path.join(out, 'world_review.png')).extract({ left: 130, top: 330, width: 780, height: 660 }),
    'portal_bridge_review', 'Void portal bridge between city and comet shores', 'world_review.png');

  const manifest = { ...previous, version: 5, assets, mapLayout: { ...previous.mapLayout,
    terrain, ambient, baseImage: 'assets/v5/world_terrain.png',
    effects: [{ id: 'voidPortalShield', sprite: 'portal_shield', rect: shieldRect, type: 'shield', pulseSpeed: 2.3 }],
    regions: { ...previous.mapLayout.regions, portalBridge: bridgeRect },
    focusBoxes: { ...previous.mapLayout.focusBoxes, portal: [130, 330, 780, 660] } },
    revisionNotes: [...previous.revisionNotes, 'A second bridge links the northern city to the comet island through a giant void portal. Its cyan-violet protective shield is an independently exported pulsing map layer.'] };
  fs.writeFileSync(path.join(root, 'manifest_v5.json'), JSON.stringify(manifest, null, 2) + '\n');
  fs.writeFileSync(path.join(root, 'manifest_v5.js'), `window.COAST_MANIFEST=${JSON.stringify(manifest)};\nwindow.COAST_STORY=${fs.readFileSync(path.join(root, 'story.json'), 'utf8')};\n`);
  const issues = [];
  if (!assets.find(a => a.id === 'portal_bridge').transparentPixels) issues.push('Bridge export lacks transparency');
  if (!assets.find(a => a.id === 'portal_shield').transparentPixels) issues.push('Shield export lacks transparency');
  if (collisions.length) issues.push(`Boat patrol intersects terrain at ${collisions.length} sampled positions`);
  const report = { version: 5, bridgeRect, shieldRect, newExports: made.length, totalManifestAssets: assets.length,
    bridgeTransparency: assets.find(a => a.id === 'portal_bridge').transparentPixels,
    shieldTransparency: assets.find(a => a.id === 'portal_shield').transparentPixels,
    boatTerrainCollisionCheck: { stepsPerFullOrbit: 360, footprintPointsPerStep: 17, method: 'Boat circumcircle against full terrain alpha, including both new bridges', collisions: collisions.slice(0, 30), collisionCount: collisions.length }, issues };
  fs.writeFileSync(path.join(root, 'verification_v5.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report));
  if (issues.length) process.exitCode = 1;
}
main().catch(err => { console.error(err); process.exitCode = 1; });
