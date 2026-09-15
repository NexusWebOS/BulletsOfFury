const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p,'utf8');
if(s.includes('\r\n'))throw new Error('game.js must remain LF');
function one(a,b,label){const n=s.split(a).length-1;if(n!==1)throw new Error(label+' matches '+n);s=s.replace(a,b);}
one("function rzbWorld(b,lx,ly){ const a=b._rzb.a, c=Math.cos(a), s=Math.sin(a);\n  return {x:b.x+(lx*c-ly*s)*RZB_S, y:b.y+(lx*s+ly*c)*RZB_S}; }\nfunction rzbPxFrame(spdPack){ return spdPack*RZB_S*RZB_PFAST/60; }",
`function rzbScale(b){return RZB_S*((b&&b._rzb&&b._rzb.scale)||1);}
function rzbWorld(b,lx,ly){ const a=b._rzb.a, c=Math.cos(a), s=Math.sin(a), z=rzbScale(b);
  return {x:b.x+(lx*c-ly*s)*z, y:b.y+(lx*s+ly*c)*z}; }
function rzbPxFrame(spdPack,b){ return spdPack*RZB_S*RZB_PFAST*((b&&b._rzb&&b._rzb.furious)?1.22:1)/60; }`,'scaled transforms');
one("    trans:0, ramX:W/2, pid:0, ppx:player?player.x:W/2, pvx:0, shake:0, clankT:0};\n  try{ if(typeof XART!=='undefined')",
`    trans:0, ramX:W/2, pid:0, ppx:player?player.x:W/2, pvx:0, shake:0, clankT:0};
  if(typeof diffKey!=='undefined'&&diffKey==='furious'){
    const R=b._rzb;R.furious=true;R.scale=1.5;R.speedMul=1.62;R.turnMul=1.55;R.rate=1.30;
    b.name='FURIOUS RAZORBACK';b.w=Math.round(270*RZB_S*R.scale);b.h=Math.round(270*RZB_S*R.scale);
  }
  try{ if(typeof XART!=='undefined')`,'furious init');
one("      if((x-g.x)*(x-g.x)+(y-g.y)*(y-g.y) < RZB_R.gun*RZB_R.gun) return k; }",
"      const rr=RZB_R.gun*(R.scale||1);if((x-g.x)*(x-g.x)+(y-g.y)*(y-g.y) < rr*rr) return k; }",'gun hit scale');
one("  const r=R.state==='turret'?RZB_R.turret:RZB_R.hull;",
"  const r=(R.state==='turret'?RZB_R.turret:RZB_R.hull)*(R.scale||1);",'part hit scale');
one("  const v=rzbPxFrame(spdPack), r=Math.max(6,Math.round(rPack*2*RZB_S)), ga=rzbGameAng(a);\n  eBullets.push({x:p.x,y:p.y,vx:Math.cos(ga)*v,vy:Math.sin(ga)*v,w:r,h:r,kind:kind,t:0,_rzb:true,_rzbOwner:b,ang:ga,spin:Math.random()*6});",
"  const v=rzbPxFrame(spdPack,b), r=Math.max(6,Math.round(rPack*2*rzbScale(b))), ga=rzbGameAng(a);\n  eBullets.push({x:p.x,y:p.y,vx:Math.cos(ga)*v,vy:Math.sin(ga)*v,w:r,h:r,kind:kind,t:0,_rzb:true,_rzbOwner:b,_rzbFurious:!!b._rzb.furious,ang:ga,spin:Math.random()*6});",'furious shot');
one("  const ga=rzbGameAng(a), v=rzbPxFrame(160);\n  eBullets.push({x:p.x,y:p.y,vx:Math.cos(ga)*v,vy:Math.sin(ga)*v,ang:ga,w:10,h:16,kind:'rzbMissile',hp:1,\n    _shootable:true,spd:v,_accel:0.0264,_maxspd:5.04,t:0,_rzb:true,_rzbOwner:b});",
"  const ga=rzbGameAng(a), v=rzbPxFrame(160,b),furious=!!b._rzb.furious;\n  eBullets.push({x:p.x,y:p.y,vx:Math.cos(ga)*v,vy:Math.sin(ga)*v,ang:ga,w:furious?15:10,h:furious?24:16,kind:'rzbMissile',hp:1,\n    _shootable:true,spd:v,_accel:furious?0.034:0.0264,_maxspd:furious?6.25:5.04,t:0,_rzb:true,_rzbOwner:b,_rzbFurious:furious});",'furious missile');
one("  const R=b._rzb, dx=R.tgt.x-b.x, dy=R.tgt.y-b.y, d=Math.hypot(dx,dy), oldA=R.a;\n  const top=((R.attack==='ram' && R.at>1)?330:92)*RZB_S*RZB_MOVE;\n  const speed=Math.min(d*1.7*RZB_MOVE,top);",
"  const R=b._rzb, dx=R.tgt.x-b.x, dy=R.tgt.y-b.y, d=Math.hypot(dx,dy), oldA=R.a,hyper=R.speedMul||1;\n  const top=((R.attack==='ram' && R.at>1)?330:92)*RZB_S*RZB_MOVE*hyper;\n  const speed=Math.min(d*1.7*RZB_MOVE*hyper,top);",'hyper movement');
one("    if(speed>8*RZB_S) R.a+=clamp(rzbWrap(rzbAim({x:0,y:0},{x:dx,y:dy})-R.a), -1.65*RZB_TURN*dt, 1.65*RZB_TURN*dt);",
"    if(speed>8*RZB_S) R.a+=clamp(rzbWrap(rzbAim({x:0,y:0},{x:dx,y:dy})-R.a), -1.65*RZB_TURN*(R.turnMul||1)*dt, 1.65*RZB_TURN*(R.turnMul||1)*dt);",'hyper turn');
one("  R.turret+=clamp(rzbWrap(ta-R.turret), -1.85*dt, 1.85*dt);",
"  R.turret+=clamp(rzbWrap(ta-R.turret), -1.85*(R.turnMul||1)*dt, 1.85*(R.turnMul||1)*dt);",'hyper turret');
one("  if(R.trans<=0){ R.at+=dt; razorbackCombat(b); }",
"  if(R.trans<=0){ R.at+=dt*(R.rate||1); razorbackCombat(b); }",'hyper attack clock');
one("      if(Math.abs(dd-w.r)<w.width+7*RZB_S && Math.abs(rzbWrap(aa-w.a))<w.arc && typeof playerHit==='function') playerHit(); }",
"      if(Math.abs(dd-w.r)<w.width+7*rzbScale(b) && Math.abs(rzbWrap(aa-w.a))<w.arc && typeof playerHit==='function') playerHit(); }",'wave collision scale');
one("  if(!P.dead && Math.hypot(b.x-P.x,b.y-P.y)<105*RZB_S && typeof playerHit==='function') playerHit();   // the hull runs you over",
"  if(!P.dead && Math.hypot(b.x-P.x,b.y-P.y)<105*rzbScale(b) && typeof playerHit==='function') playerHit();   // the hull runs you over",'body collision scale');
one("  const R=b._rzb, t=R.at, m=rzbFwd(b,R.turret,(142-R.recoil)*RZB_S);",
"  const R=b._rzb, t=R.at, S=rzbScale(b),m=rzbFwd(b,R.turret,(142-R.recoil)*S);",'combat scale');
one("        const g=rzbWorld(b,k==='left'?-57:57,96), a=R.guns[k].a, mz=rzbFwd(g,a,49*RZB_S);\n        const n0=eBullets.length;\n        eShootT(mz.x,mz.y,eAimDown(rzbGameAng(a+Math.sin(beat*1.9)*0.07)),rzbPxFrame(380),'mg',{w:4,h:14,silent:true});",
"        const g=rzbWorld(b,k==='left'?-57:57,96), a=R.guns[k].a, mz=rzbFwd(g,a,49*S);\n        const n0=eBullets.length;\n        eShootT(mz.x,mz.y,eAimDown(rzbGameAng(a+Math.sin(beat*1.9)*0.07)),rzbPxFrame(380,b),'mg',{w:R.furious?6:4,h:R.furious?19:14,silent:true});",'furious machine rounds');
one("        for(let i=n0;i<eBullets.length;i++){eBullets[i]._rzb=true;eBullets[i]._rzbOwner=b;}",
"        for(let i=n0;i<eBullets.length;i++){eBullets[i]._rzb=true;eBullets[i]._rzbOwner=b;eBullets[i]._rzbFurious=!!R.furious;}",'tag machine rounds');
one("        for(const off of [-0.28,-0.14,0,0.14,0.28]) rzbShot(b,m,R.turret+off,240,18,'rzbSonic');\n        R.waves.push({x:m.x,y:m.y,r:10*RZB_S,a:R.turret,arc:0.65,speed:180*RZB_S*RZB_WFAST,width:15*RZB_S,life:5});",
"        const offs=R.furious?[-0.56,-0.42,-0.28,-0.14,0,0.14,0.28,0.42,0.56]:[-0.28,-0.14,0,0.14,0.28];\n        for(const off of offs)rzbShot(b,m,R.turret+off,R.furious?300:240,R.furious?22:18,'rzbSonic');\n        R.waves.push({x:m.x,y:m.y,r:10*S,a:R.turret,arc:R.furious?1.05:0.65,speed:(R.furious?270:180)*S*RZB_WFAST,width:(R.furious?24:15)*S,life:R.furious?6:5,furious:!!R.furious});",'furious sonic wave');
one("      R.beat=0; const N=R.state==='hull'?8:10, pid=R.pid;",
"      R.beat=0; const N=R.furious?14:(R.state==='hull'?8:10), pid=R.pid;",'furious missile count');
one("      R.waves.push({x:b.x,y:b.y,r:35*RZB_S,a:R.a,arc:2.66,speed:200*RZB_S*RZB_WFAST,width:17*RZB_S,life:5.6});\n      for(let i=0;i<16;i++) rzbShot(b,{x:b.x,y:b.y},i*Math.PI*2/16,145,12,'rzbSonic');",
"      R.waves.push({x:b.x,y:b.y,r:35*S,a:R.a,arc:R.furious?2.92:2.66,speed:(R.furious?260:200)*S*RZB_WFAST,width:(R.furious?25:17)*S,life:R.furious?6.4:5.6,furious:!!R.furious});\n      const n=R.furious?28:16;for(let i=0;i<n;i++)rzbShot(b,{x:b.x,y:b.y},i*Math.PI*2/n,R.furious?205:145,R.furious?15:12,'rzbSonic');",'furious nova');
one("function rzbSprite(key,x,y,a,s,alpha,px,py){\n  const im=rzbImg(key); if(!im) return false;\n  const w=im.width||im.naturalWidth, h=im.height||im.naturalHeight;\n  const ox=(px!=null?px:w/2), oy=(py!=null?py:h/2), sc=s*RZB_S;",
"function rzbSprite(key,x,y,a,s,alpha,px,py,mul,tint){\n  const im=(tint&&typeof xartPalette==='function'&&xartPalette(key,tint))||rzbImg(key); if(!im) return false;\n  const w=im.width||im.naturalWidth, h=im.height||im.naturalHeight;\n  const ox=(px!=null?px:w/2), oy=(py!=null?py:h/2), sc=s*RZB_S*(mul||1);",'scaled tinted sprite');
one("function rzbFlash(key,x,y,a,s,px,py,amt){",
"function rzbFlash(key,x,y,a,s,px,py,amt,mul){",'flash signature');
one("  const w=t.width, h=t.height, ox=(px!=null?px:w/2), oy=(py!=null?py:h/2), sc=s*RZB_S;",
"  const w=t.width, h=t.height, ox=(px!=null?px:w/2), oy=(py!=null?py:h/2), sc=s*RZB_S*(mul||1);",'flash scale');
one("  const S=RZB_S;\n  ctx.save(); ctx.imageSmoothingEnabled=false;",
"  const mul=R.scale||1,S=rzbScale(b),bodyTint=R.furious?'#d51f3b':null;\n  ctx.save(); ctx.imageSmoothingEnabled=false;",'draw scale palette');
one("    rzbSprite('rzb_wreck',b.x,b.y,R.a,1,1-k*0.85);",
"    rzbSprite('rzb_wreck',b.x,b.y,R.a,1,1-k*0.85,null,null,mul,bodyTint);",'death scale');
one("    rzbSprite('rzb_dust',p.x,p.y,(b.t||0)*0.12,0.36+Math.sin((b.t||0)*10+side)*0.08,0.25); } }",
"    rzbSprite('rzb_dust',p.x,p.y,(b.t||0)*0.12,0.36+Math.sin((b.t||0)*10+side)*0.08,0.25,null,null,mul); } }",'dust scale');
one("  rzbSprite(hk,b.x,b.y,ha,1);\n  if(R.state==='hull') rzbFlash(hk,b.x,b.y,ha,1,null,null,R.flash.hull);",
"  rzbSprite(hk,b.x,b.y,ha,1,null,null,null,mul,bodyTint);\n  if(R.state==='hull') rzbFlash(hk,b.x,b.y,ha,1,null,null,R.flash.hull,mul);",'hull scale palette');
one("  const tr=rzbImg('rzb_tread');",
"  const tr=(bodyTint&&typeof xartPalette==='function'&&xartPalette('rzb_tread',bodyTint))||rzbImg('rzb_tread');",'tread palette');
one("    rzbSprite('rzb_rotor',p.x,p.y,R.a+R.travel[side]/25,0.43);",
"    rzbSprite('rzb_rotor',p.x,p.y,R.a+R.travel[side]/25,0.43,null,null,null,mul,bodyTint);",'rotor scale palette');
one("  for(const s of [-1,1]){ const p=rzbWorld(b,s*105,10); rzbSprite('rzb_missile_pod',p.x,p.y,R.a,0.55);\n    if(R.pods[s<0?0:1]>0){ const q=rzbFwd(p,R.turret+s*0.6,26*S); rzbSprite('rzb_muzzle',q.x,q.y,R.turret,0.2); } }",
"  for(const s of [-1,1]){ const p=rzbWorld(b,s*105,10); rzbSprite('rzb_missile_pod',p.x,p.y,R.a,0.55,null,null,null,mul,bodyTint);\n    if(R.pods[s<0?0:1]>0){ const q=rzbFwd(p,R.turret+s*0.6,26*S); rzbSprite('rzb_muzzle',q.x,q.y,R.turret,0.2,null,null,null,mul); } }",'pod scale palette');
one("    rzbSprite('rzb_machinegun',p.x,p.y,g.a,1,null,64,65);\n    rzbFlash('rzb_machinegun',p.x,p.y,g.a,1,64,65,R.flash[k]);\n    if(g.flash>0){ const m=rzbFwd(p,g.a,49*S); rzbSprite('rzb_muzzle',m.x,m.y,g.a,0.34); }",
"    rzbSprite('rzb_machinegun',p.x,p.y,g.a,1,null,64,65,mul,bodyTint);\n    rzbFlash('rzb_machinegun',p.x,p.y,g.a,1,64,65,R.flash[k],mul);\n    if(g.flash>0){ const m=rzbFwd(p,g.a,49*S); rzbSprite('rzb_muzzle',m.x,m.y,g.a,0.34,null,null,null,mul); }",'gun scale palette');
one("    rzbSprite(tk,p.x,p.y,R.turret,1,null,128,128);\n    if(R.state==='turret') rzbFlash(tk,p.x,p.y,R.turret,1,128,128,R.flash.turret);",
"    rzbSprite(tk,p.x,p.y,R.turret,1,null,128,128,mul,bodyTint);\n    if(R.state==='turret') rzbFlash(tk,p.x,p.y,R.turret,1,128,128,R.flash.turret,mul);",'turret scale palette');
one("    rzbSprite('rzb_sonic_charge',m.x,m.y,(b.t||0)*0.8,0.16+R.charge*0.5);",
"    rzbSprite('rzb_sonic_charge',m.x,m.y,(b.t||0)*(R.furious?1.7:0.8),0.16+R.charge*(R.furious?0.78:0.5),null,null,null,mul,R.furious?'#ff1838':null);",'furious charge');
one("      ctx.strokeStyle='rgba(184,238,94,0.5)';",
"      ctx.strokeStyle=R.furious?'rgba(255,32,58,0.72)':'rgba(184,238,94,0.5)';",'furious aim line');
one("    rzbSprite(e.key,e.x,e.y,(e.spin?u*3:0),e.s*(0.7+u*0.6),1-u, e.key==='rzb_turret_damaged'?128:null, e.key==='rzb_turret_damaged'?128:null); }",
"    rzbSprite(e.key,e.x,e.y,(e.spin?u*3:0),e.s*(0.7+u*0.6),1-u, e.key==='rzb_turret_damaged'?128:null, e.key==='rzb_turret_damaged'?128:null,mul,bodyTint); }",'effect scale');
one("  const im=rzbImg('rzb_sonic_ring');",
"  const im=(w.furious&&typeof xartPalette==='function'&&xartPalette('rzb_sonic_ring','#ff1838'))||rzbImg('rzb_sonic_ring');",'furious ring palette');
one("  ctx.save(); ctx.strokeStyle='rgba(202,255,119,0.5)';",
"  ctx.save(); ctx.strokeStyle=w.furious?'rgba(255,40,65,0.72)':'rgba(202,255,119,0.5)';",'furious ring edge');
one("  const key=q.kind==='rzbMissile'?'rzb_razor_missile':'rzb_sonic_bullet', im=rzbImg(key);",
"  const key=q.kind==='rzbMissile'?'rzb_razor_missile':'rzb_sonic_bullet', im=(q._rzbFurious&&typeof xartPalette==='function'&&xartPalette(key,'#ff1838'))||rzbImg(key);",'furious ordnance palette');
one("  const sz=q.kind==='rzbMissile'?34:Math.max(20,q.w*1.9);",
"  const sz=q.kind==='rzbMissile'?(q._rzbFurious?51:34):Math.max(20,q.w*1.9);",'furious missile draw size');
one("    const r=R.state==='guns'?RZB_R.gun:R.state==='turret'?RZB_R.turret:RZB_R.hull;",
"    const r=(R.state==='guns'?RZB_R.gun:R.state==='turret'?RZB_R.turret:RZB_R.hull)*(R.scale||1);",'beam scale');
one("        a.push(retinaImpactTarget(b,rid,'razorback '+(ai+1)+' '+id,state,(RZB_R[id==='left'||id==='right'?'gun':id]||34)*2,(RZB_R[id==='left'||id==='right'?'gun':id]||34)*2));}",
"        const rr=(RZB_R[id==='left'||id==='right'?'gun':id]||34)*(R.scale||1)*2;a.push(retinaImpactTarget(b,rid,'razorback '+(ai+1)+' '+id,state,rr,rr));}",'pair retina scale');
one("      a.push(retinaImpactTarget(b,id,'razorback '+id,state,(RZB_R[id==='left'||id==='right'?'gun':id]||34)*2,(RZB_R[id==='left'||id==='right'?'gun':id]||34)*2));",
"      const rr=(RZB_R[id==='left'||id==='right'?'gun':id]||34)*(R.scale||1)*2;a.push(retinaImpactTarget(b,id,'razorback '+id,state,rr,rr));",'single retina scale');
fs.writeFileSync(p,s,'utf8');console.log('PATCHED_RAZORBACK_FURIOUS_0915');
