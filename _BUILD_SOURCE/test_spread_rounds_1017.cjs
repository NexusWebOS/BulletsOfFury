module.exports=function(vm,ctxv,ok){
 /* 1017 - Mike: "spread fire, should no longer be the large slugs. should be our actual bullet graphics, but spread
    style. and the speed is too fast by level 2/3." Real-Chromium proof with a busted arm:
    _BUILD_SOURCE/probe_spread_rounds_1017.py (16/0). */
 const fs=require('fs'),path=require('path');
 console.log('=== 384. Spread fire flies the gun rounds and slows its volleys as the fan widens ===');
 const c=JSON.parse(vm.runInContext(`JSON.stringify((()=>{const s={w:run.weapon,l:run.wlevel},o=[];run.weapon=1;
  for(let lv=1;lv<=5;lv++){run.wlevel=lv;o.push(_weaponCadence());}run.weapon=s.w;run.wlevel=s.l;return {o,base:WEAPON_CADENCE[1],k:SPREAD_LV_SLOW};})())`,ctxv));
 ok(Math.abs(c.o[0]-c.base)<1e-9,'level 1 spread keeps the balance-table cadence');
 ok(c.o.every((v,i)=>i===0||v>c.o[i-1]),'each spread level fires its volleys a little slower ('+c.o.map(v=>v.toFixed(3)).join(' / ')+')');
 const pps=c.o.map((v,i)=>(i+3)/v);
 ok(pps[2]<=pps[0]*1.45&&pps[4]<=pps[0]*1.7,'pellets per second grow gently ('+pps.map(v=>v.toFixed(1)).join(' / ')+')');
 const strip=s=>s.replace(/\/\*[\s\S]*?\*\//g,'').replace(/(^|[^:'"])\/\/.*$/gm,'$1');
 const sd=strip(fs.readFileSync(path.join(__dirname,'../assets/spread_1001.js'),'utf8'));
 const body=sd.slice(sd.indexOf('function spreadDraw1001'));
 ok(/'mgcf_'\+lv\+'_'\+mgcfFrame\(b\)/.test(body)&&/drawMfx\(key,b\.x,b\.y,Math\.atan2\(b\.vy\|\|-1,b\.vx\|\|0\)\+Math\.PI\/2/.test(body),'a plain spread pellet draws the gun round, turned along its line');
 ok(!/SPREAD1001_ART\[/.test(body),'spreadDraw1001 no longer flies the slug reels');
};
