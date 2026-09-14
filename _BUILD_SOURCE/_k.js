global.window=global;eval(require('fs').readFileSync('assets/manifest.js','utf8'));
const P=["axel", "cole", "decker", "falva", "freezer", "juggernaut", "lizzie", "maverick", "yuri"];const o={};for(const k in BOFX.ships){for(const p of P){if(k==='ship_'+p||k.indexOf('ship_'+p+'_')===0){o[k]=BOFX.ships[k];break;}}}
process.stdout.write(JSON.stringify(o));
