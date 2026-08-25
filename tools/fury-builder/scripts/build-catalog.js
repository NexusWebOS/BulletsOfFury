"use strict";

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..", "..", "..");
const builderRoot = path.resolve(__dirname, "..");
const assetsRoot = path.join(root, "assets");
const referenceRoot = path.join(builderRoot, "library", "reference");
const outputDir = path.resolve(__dirname, "..", "data");
const imageExt = new Set([".png", ".jpg", ".jpeg", ".webp", ".gif"]);

function walk(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, out);
    else out.push(full);
  }
  return out;
}

function slash(value) { return value.split(path.sep).join("/"); }
function title(value) {
  return value.replace(/\.[^.]+$/, "").replace(/[_-]+/g, " ").replace(/\b\w/g, c => c.toUpperCase());
}

const sourceText = ["game.js", "assets/manifest.js"].map(file => {
  const full = path.join(root, file); return fs.existsSync(full) ? fs.readFileSync(full, "utf8") : "";
}).join("\n");

const scanRoots = [assetsRoot, referenceRoot].filter(fs.existsSync);
const files = scanRoots.flatMap(scanRoot => walk(scanRoot));
const assets = files.filter(file => imageExt.has(path.extname(file).toLowerCase())).map(file => {
  const rel = slash(path.relative(root, file));
  const normalized = rel.replace(/\\/g, "/");
  return {
    id: normalized.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, ""),
    name: title(path.basename(file)), path: normalized, bytes: fs.statSync(file).size,
    wired: sourceText.includes(normalized) || sourceText.includes(`./${normalized}`),
    group: file.startsWith(referenceRoot)
      ? `reference/${slash(path.relative(referenceRoot, path.dirname(file))) || "root"}`
      : slash(path.relative(assetsRoot, path.dirname(file))) || "root"
  };
}).sort((a, b) => a.path.localeCompare(b.path));

const frameSets = files.filter(file => file.endsWith(".frames.json")).map(file => {
  const frames = JSON.parse(fs.readFileSync(file, "utf8"));
  const imageFile = file.replace(/\.frames\.json$/, ".png");
  return {
    id: path.basename(file, ".frames.json"),
    manifest: slash(path.relative(root, file)),
    image: slash(path.relative(root, imageFile)),
    wired: sourceText.includes(slash(path.relative(root, imageFile))),
    frames
  };
});

const catalog = {
  version: 3, generatedAt: new Date().toISOString(), roots: ["assets", "tools/fury-builder/library/reference"],
  counts: { images: assets.length, wiredImages: assets.filter(a => a.wired).length, unwiredImages: assets.filter(a => !a.wired).length, frameSets: frameSets.length, frames: frameSets.reduce((n, s) => n + Object.keys(s.frames).length, 0) },
  assets, frameSets
};

fs.mkdirSync(outputDir, { recursive: true });
fs.writeFileSync(path.join(outputDir, "catalog.json"), JSON.stringify(catalog, null, 2));
fs.writeFileSync(path.join(outputDir, "catalog.js"), `window.FURY_CATALOG = ${JSON.stringify(catalog)};\n`);
console.log(`Fury Forge catalog: ${catalog.counts.images} images, ${catalog.counts.unwiredImages} unwired, ${catalog.counts.frames} atlas frames.`);
