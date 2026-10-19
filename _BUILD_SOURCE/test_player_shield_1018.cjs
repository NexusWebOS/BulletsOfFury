module.exports=function(vm,ctxv,ok){
 /* 1018 - Mike: "why are the shields so big. I mainly wanted just a specific outline of each pilot's ship that pixel
    glows and lets you know they are protected internally with a shield that glows over them too."
    Real-Chromium proof with a busted arm: _BUILD_SOURCE/probe_player_shield_checks_1018.py (74/0). */
 const fs=require('fs'),path=require('path');
 console.log('=== 385. Player shields: a pixel-glow outline of the ship itself plus a sheen over it ===');
 for(const f of ['shield_fit_1018.js','shield_pixel_1018.js','player_shield_1018.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),ctxv,{filename:f});
 const strip=s=>s.replace(/\/\*[\s\S]*?\*\//g,'').replace(/(^|[^:'"])\/\/.*$/gm,'$1');
 const src=strip(fs.readFileSync(path.join(__dirname,'../assets/player_shield_1018.js'),'utf8'));
 ok(!/ctx.filter|shadowBlur|ctx\.arc|ctx\.rotate|ctx\.scale/.test(src),'pixel glow only: no blur, no rotating sweep, no runtime scaling');
 ok(!/SHIELD_PX_1018|ps18Fit/.test(src),'the oversized crystal-shell reel is no longer drawn');
 ok(/pf27PlaneThrustDraw=function\(g,key,x,y,w,h\)/.test(src)&&/somerFrameKey\(\)/.test(src)&&/rollFrameKey\(\)/.test(src),'the outline is traced from the exact hull frame and rect on screen, rolls included');
 ok(/for\(let k=lv;k>=2;k--\)/.test(src)&&/M\.ring\(1,M\.lit\)/.test(src),'one 1-px ring per shield level hugs the silhouette (level 5 = five rings)');
 ok(/lv>=5/.test(src)&&/PS18_GOLD/.test(src)&&/kind:'up'/.test(src)&&/ps18ShardBurst/.test(src),'level 5 gold edge; level up flares outward, level down throws shards');
 ok(/source-in/.test(src)&&/destination-out/.test(src)&&!/getImageData/.test(src),'masks built by compositing, no pixel read (file:// safe)');
 ok(vm.runInContext("typeof ps18HullInk==='function'&&!!ps18HullInk('cole')",ctxv),'ps18HullInk still serves the charge rings');
};
