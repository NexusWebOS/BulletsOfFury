const fs=require('fs'),path=require('path'),file=path.resolve(__dirname,'../assets/game.js');let src=fs.readFileSync(file,'utf8');
if(src.includes('\r'))throw new Error('assets/game.js must remain LF-only');
const a=`  const z=e&&e._eshStun;if(!z)return false;z.t+=dt;
  const p=clamp(z.t/z.dur,0,1),ease=p*p*(3-2*p);`;
const b=`  const z=e&&e._eshStun;if(!z)return false;z.t+=dt;e.flash=Math.max(0,(e.flash||0)-dt);
  const p=clamp(z.t/z.dur,0,1),ease=p*p*(3-2*p);`;
if(src.includes(a))src=src.replace(a,b);else if(!src.includes(b))throw new Error('stun flash guard not found');
fs.writeFileSync(file,src,'utf8');console.log('Verified shield-stun hit-flash decay.');
