const fs=require('fs'),path=require('path');const root=path.resolve(__dirname,'..');
const src=fs.readFileSync(path.join(root,'assets/game.js'),'utf8'),meta=JSON.parse(fs.readFileSync(path.join(root,'assets/game/stage5_hammer/reticle_ground_0915.json'),'utf8'));
let passed=0,failed=0,checks=[];function ok(name,v){checks.push({name,ok:!!v});v?passed++:failed++;}
for(const f of ['reticle.png','reticle_ground_source_0915.png','reticle_topdown_original_0915.png','reticle_ground_0915.json'])ok(f+' exists',fs.existsSync(path.join(root,'assets/game/stage5_hammer',f)));
ok('ground reticle is a wide floor ellipse',meta.aspect>1.8);
ok('runtime uses preserved source aspect',src.includes('const hh=w*im.height/Math.max(1,im.width)'));
ok('leap warning uses ground reticle helper',src.includes('hammerGroundReticleDraw(ri,h.tx,h.ty,126'));
ok('boomerang warning uses ground reticle helper',src.includes('hammerGroundReticleDraw(ri,h.throwX,h.throwY,122'));
ok('square 100x100 leap-reticle draw removed',!src.includes('ctx.drawImage(ri,h.tx-50,h.ty-50,100,100)'));
ok('green yellow red warning progression remains',src.includes("h.t<.4?null:h.t<.8?'yellow':'red'"));
console.log(JSON.stringify({passed,failed,checks},null,2));process.exitCode=failed?1:0;
