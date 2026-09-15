const fs=require('fs');const path=require('path');const file=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(file,'utf8');
if(s.includes('\r'))throw new Error('assets/game.js line-ending drift');
function once(from,to,label){const n=s.split(from).length-1;if(n!==1)throw new Error(label+' expected once, found '+n);s=s.replace(from,to);}
once(
"  ctx.drawImage(im,-size[0]/2,-size[1]/2,size[0],size[1]);ctx.restore();return true;",
"  ctx.drawImage(im,-size[0]/2,-size[1]/2,size[0],size[1]);\n  if(b._s3LaserBall){\n    /* Same authored pixels, fixed footprint: a stepped additive pulse makes the dark-blue ball\n       readable on ice without the orange missile exhaust that shootable rounds usually inherit. */\n    const pulse=[.10,.18,.28,.18][Math.floor((b.t||0)*12)&3];\n    ctx.globalCompositeOperation='lighter';ctx.globalAlpha=pulse;\n    ctx.drawImage(im,-size[0]/2,-size[1]/2,size[0],size[1]);\n  }\n  ctx.restore();return true;",
'add authored laser-ball pixel pulse');
once(
"      if(typeof addTrail==='function' && (b.t*60|0)%2===0) addTrail(b.x - Math.cos(b.ang||Math.PI/2)*b.h*0.4, b.y - Math.sin(b.ang||Math.PI/2)*b.h*0.4, null, 'missile');",
"      if(typeof addTrail==='function' && !b._s3LaserBall && (b.t*60|0)%2===0) addTrail(b.x - Math.cos(b.ang||Math.PI/2)*b.h*0.4, b.y - Math.sin(b.ang||Math.PI/2)*b.h*0.4, null, 'missile');",
'exclude laser balls from missile exhaust');
fs.writeFileSync(file,s,'utf8');if(fs.readFileSync(file,'utf8').includes('\r'))throw new Error('wrote CRLF');console.log('refined Stage-3 Hard laser-ball rendering');

