"""Targeted, guarded engine edits. Preserve incoming work and UTF-8/LF."""
from pathlib import Path
import hashlib
ROOT=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
def edit(path, edits):
    p=ROOT/path; raw=p.read_bytes(); s=raw.decode('utf-8')
    for old,new in edits:
        assert s.count(old)==1,(path,old[:100],s.count(old))
        s=s.replace(old,new,1)
    p.write_bytes(s.encode('utf-8'))
    print(path,hashlib.sha256(raw).hexdigest()[:12],'=>',hashlib.sha256(p.read_bytes()).hexdigest()[:12])

CACHE=r'''/* 0929: bounded sprite-layer cache. Gaussian blurs and static filters belong on
   small offscreen plates, not on every projectile. Alpha remains per layer. */
const _lateSpriteCache=new Map(),_lateSpriteIds=new WeakMap();
let _lateSpriteSerial=0,_lateSpriteBytes=0;
const LATE_SPRITE_BYTES=8*1024*1024,LATE_SPRITE_CAP=192;
function lateSpriteBake(src,rc,w,h,glow,blur,filter,additive){
  let id=_lateSpriteIds.get(src);if(!id){id=++_lateSpriteSerial;_lateSpriteIds.set(src,id);}
  const scale=SS||1,key=[id,rc.join(','),w,h,glow||'',blur||0,filter||'',!!additive,scale].join('|');
  const hit=_lateSpriteCache.get(key);
  if(hit){_lateSpriteCache.delete(key);_lateSpriteCache.set(key,hit);return hit;}
  const pad=Math.ceil((blur||0)*1.8)+2,c=document.createElement('canvas');
  c.width=Math.ceil(w*scale)+2*pad;c.height=Math.ceil(h*scale)+2*pad;
  const g=c.getContext('2d');g.imageSmoothingEnabled=false;
  if(additive)g.globalCompositeOperation='lighter';
  if(filter)g.filter=filter;
  if(glow&&blur){g.shadowColor=glow;g.shadowBlur=blur;}
  g.drawImage(src,...rc,pad,pad,w*scale,h*scale);
  c._latePad=pad/scale;c._lateScale=scale;
  const bytes=c.width*c.height*4;
  while(_lateSpriteCache.size&&(_lateSpriteCache.size>=LATE_SPRITE_CAP||_lateSpriteBytes+bytes>LATE_SPRITE_BYTES)){
    const oldest=_lateSpriteCache.keys().next().value,plate=_lateSpriteCache.get(oldest);
    _lateSpriteBytes-=plate.width*plate.height*4;_lateSpriteCache.delete(oldest);
  }
  if(bytes<=LATE_SPRITE_BYTES){_lateSpriteCache.set(key,c);_lateSpriteBytes+=bytes;}
  return c;
}
function lateSpriteBlit(c,x,y){
  ctx.drawImage(c,x-c._latePad,y-c._latePad,c.width/c._lateScale,c.height/c._lateScale);
}
const _glowOrder=new Map(),_blobOrder=new Map();
function glowCacheTouch(order,key,cache,cap){
  if(order.has(key))order.delete(key);order.set(key,1);
  while(order.size>cap){const k=order.keys().next().value;order.delete(k);delete cache[k];}
}
'''
oldhalo='''    ctx.shadowColor=glow; ctx.shadowBlur=16;
    ctx.globalAlpha=(alpha!=null?alpha:1)*0.85;
    ctx.drawImage(src, sx, sy, P87_CELL, P87_CELL, -h/2, -h*P87_BODY_Y, h, h);
    ctx.shadowBlur=7;                                    // a tighter, hotter inner ring
    ctx.drawImage(src, sx, sy, P87_CELL, P87_CELL, -h/2, -h*P87_BODY_Y, h, h);'''
newhalo='''    ctx.shadowBlur=0;
    ctx.globalAlpha=(alpha!=null?alpha:1)*0.85;
    const rc=[sx,sy,P87_CELL,P87_CELL];
    lateSpriteBlit(lateSpriteBake(src,rc,h,h,glow,16,null,false),-h/2,-h*P87_BODY_Y);
    lateSpriteBlit(lateSpriteBake(src,rc,h,h,glow,7,null,false),-h/2,-h*P87_BODY_Y);'''
oldrain='''    for(let i=0;i<count;i++){
      const seed=((i*(near?83.17:97.31))%101)/101;
      const x0=((i*(near?61.73:67.73)+seed*W+t*wind)%W+W)%W;
      const y0=top+(((i*(near?37.11:43.17)+seed*hgt+t*fall)%hgt+hgt)%hgt);
      const len=(near?14:8)+wet*(near?22:15)+(i%6);
      ctx.globalAlpha=(near?0.38:0.25)+wet*(near?0.42:0.30);
      ctx.lineWidth=near?((i%6===0)?2:1.25):1;
      ctx.beginPath();ctx.moveTo(x0,y0);ctx.lineTo(x0-wind/fall*len,y0+len);ctx.stroke();
    }'''
newrain='''    ctx.globalAlpha=(near?0.38:0.25)+wet*(near?0.42:0.30);
    // Same rain positions, lengths and widths; three strokes replace hundreds.
    for(let group=0;group<(near?2:1);group++){
      ctx.lineWidth=near?(group===1?2:1.25):1;ctx.beginPath();
      for(let i=0;i<count;i++){
        if(near&&((i%6===0)!==(group===1)))continue;
        const seed=((i*(near?83.17:97.31))%101)/101;
        const x0=((i*(near?61.73:67.73)+seed*W+t*wind)%W+W)%W;
        const y0=top+(((i*(near?37.11:43.17)+seed*hgt+t*fall)%hgt+hgt)%hgt);
        const len=(near?14:8)+wet*(near?22:15)+(i%6);
        ctx.moveTo(x0,y0);ctx.lineTo(x0-wind/fall*len,y0+len);
      }
      ctx.stroke();
    }'''
oldvent='''    // One fixed vent/pipe plate: attack frames animate only the toxic exhaust.
    const split=fw*.425;ctx.drawImage(sheet,0,0,split,fh,0,y-sizeY*.5,sizeX*.425,sizeY);'''
newvent='''    // The last column shifts left 33 source pixels; the lower row shifts up 31.
    // Keep the authored pipe fixed and register each exhaust frame to its mouth.
    const split=213,originY=y-sizeY*265/fh;
    ctx.drawImage(sheet,0,0,split,fh,0,originY,sizeX*split/fw,sizeY);'''
oldjet='''      const age=e.t-warn,f=age<.78?3+(Math.floor(age*12)%2):5+Math.min(1,Math.floor((age-.78)/.32*2));
      const jetY=fh*.33,jetH=fh*.37;
      ctx.drawImage(sheet,(f%4)*fw+split,Math.floor(f/4)*fh+jetY,fw-split,jetH,sizeX*.425,y-sizeY*.5+sizeY*.33,sizeX*.575,sizeY*.37);'''
newjet='''      const age=e.t-warn,f=stage7SluiceFrame(age);
      const dx=f%4===3?-33:0,dy=f>=4?-31:0,jetY=160,jetH=240;
      ctx.drawImage(sheet,(f%4)*fw+split+dx,Math.floor(f/4)*fh+jetY+dy,fw-split,jetH,
        sizeX*split/fw,originY+sizeY*jetY/fh,sizeX*(fw-split)/fw,sizeY*jetH/fh);'''
edit('assets/game.js',[
 ('function bakeGlow(key, w, h, tint, tintA, glow, blur, additive, bakeA){',CACHE+'\nfunction bakeGlow(key, w, h, tint, tintA, glow, blur, additive, bakeA){'),
 ('  if(hit){ _glowHits++; return hit; }\n  if(_glowBakes>=_GLOW_CAP) return null;     // pathological variety: fall back to the live path',
  '  if(_GLOW_CAP<=0)return null;\n  if(hit){ _glowHits++;glowCacheTouch(_glowOrder,ck,_glowc,_GLOW_CAP);return hit; }'),
 ('  _glowc[ck]=c; _glowBakes++;','  _glowc[ck]=c; _glowBakes++;glowCacheTouch(_glowOrder,ck,_glowc,_GLOW_CAP);'),
 ('  const hit=_blobc[ck]; if(hit){ _glowHits++; return hit; }\n  if(_blobBakes>=_BLOB_CAP) return null;',
  '  const hit=_blobc[ck];if(_BLOB_CAP<=0)return null;\n  if(hit){ _glowHits++;glowCacheTouch(_blobOrder,ck,_blobc,_BLOB_CAP);return hit; }'),
 ('  _blobc[ck]=c; _blobBakes++; return c;','  _blobc[ck]=c; _blobBakes++;glowCacheTouch(_blobOrder,ck,_blobc,_BLOB_CAP);return c;'),
 (oldhalo,newhalo),
 ("    ctx.globalAlpha=0.92; ctx.filter='brightness(0.18)';\n    ctx.drawImage(im,-w/2,-h/2,w,h);",
  "    ctx.globalAlpha=0.92;\n    lateSpriteBlit(lateSpriteBake(im,[0,0,im.width,im.height],w,h,null,0,'brightness(0.18)',false),-w/2,-h/2);"),
 ("    ctx.filter='brightness(2.4) saturate(0)';\n    ctx.drawImage(im,-w*0.28, -h*0.28+cy, w*0.56, h*0.56);",
  "    lateSpriteBlit(lateSpriteBake(im,[0,0,im.width,im.height],w*.56,h*.56,null,0,'brightness(2.4) saturate(0)',false),-w*.28,-h*.28+cy);"),
 ("    ctx.shadowColor='#ffc23a'; ctx.shadowBlur=8;\n    ctx.drawImage(im,-w/2,-h/2,w,h);",
  "    ctx.shadowBlur=0;\n    lateSpriteBlit(lateSpriteBake(im,[0,0,im.width,im.height],w,h,'#ffc23a',8,null,true),-w/2,-h/2);"),
 (oldrain,newrain),
 ("function l23WarnSymbolDraw(b,B){\n  if(!b", "function enemyWarningOwner(owner){return !!owner&&(enemies.includes(owner)||enemies.includes(owner.owner));}\nfunction l23WarnSymbolDraw(b,B){\n  if(enemyWarningOwner(b))return false; // Ordinary enemies retain lane/ground tells, not floating triangles.\n  if(!b"),
 ("    if(e.dead) continue;\n    if(e._fromBehind || e._crosser", "    if(e.dead||run.stage>=6&&run.stage<=8) continue;\n    if(e._fromBehind || e._crosser"),
 ('function stage7SluiceDraw(){', 'function stage7SluiceFrame(age){return age<.14?2:age<.78?3+(Math.floor((age-.14)*10)%2):age<.96?5:6;}\nfunction stage7SluiceDraw(){'),
 (oldvent,newvent),(oldjet,newjet),
 ('    const W=worldWidth(),lo=e.side<0?W*.19:W-350,hi=e.side<0?350:W-W*.19;',
  '    const W=worldWidth(),mouth=350*213/(1774/4),reach=e.t-warn<.14?252:350;\n    const lo=e.side<0?mouth:W-reach,hi=e.side<0?reach:W-mouth;'),
])
edit('assets/combat_polish_0927b.js',[("const im=(run.stage===6||(run.stage===5&&q.owner===subBoss))?null:polishCell('warning'", "const im=(enemyWarningOwner(q)||run.stage===6||(run.stage===5&&q.owner===subBoss))?null:polishCell('warning'")])
