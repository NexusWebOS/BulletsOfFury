/* Development-only access to exact retired reference artwork. Not loaded by index.html. */
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=process.env.BOF_REAL_GAME_ROOT||path.resolve(__dirname,'..');
const archive=path.resolve(__dirname,'../UNUSED_ASSETS/retired_art_1022');
const read=fs.readFileSync.bind(fs),exists=fs.existsSync.bind(fs);
const entries=JSON.parse(read(path.join(archive,'manifest.json'),'utf8'));
const allowed=new Set(entries.map(x=>x.path));
for(const x of entries){const p=path.join(archive,x.path);if(crypto.createHash('sha256').update(read(p)).digest('hex')!==x.sha256)throw Error('Archived reference hash mismatch: '+x.path);}
function retiredPath(p){if(typeof p!=='string')return p;const rel=path.relative(root,path.resolve(p)).split(path.sep).join('/');return allowed.has(rel)?path.join(archive,rel):p;}
fs.readFileSync=(p,...args)=>read(retiredPath(p),...args);
fs.existsSync=p=>exists(retiredPath(p));
