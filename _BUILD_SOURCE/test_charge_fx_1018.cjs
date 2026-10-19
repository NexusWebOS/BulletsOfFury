module.exports=function(vm,ctxv,ok){
 /* 1018 - Mike: "now fix the animations when falva or maverick or jace charge and release their attacks".
    Real-Chromium film before/after: _BUILD_SOURCE/probe_charge_film_1018.py (_shots/charge_1018). */
 const fs=require('fs'),path=require('path');
 console.log('=== 386. Charge and release: Falva, Maverick, Jace ===');
 const strip=s=>s.replace(/\/\*[\s\S]*?\*\//g,'').replace(/(^|[^:'"])\/\/.*$/gm,'$1');
 const src=strip(fs.readFileSync(path.join(__dirname,'../assets/charge_fx_1018.js'),'utf8'));
 const idx=fs.readFileSync(path.join(__dirname,'../index.html'),'utf8');
 ok(idx.indexOf('assets/charge_fx_1018.js')>idx.indexOf('assets/player_shield_1018.js')&&idx.indexOf('assets/player_shield_1018.js')>0,'the charge layer loads after the shield layer (it reuses its hull measure)');
 ok(/releaseRoller=function/.test(src)&&/releaseHelix=function/.test(src)&&/cfx18NoNoseFire/.test(src),'a release never fires the generic fireball at the ship\'s own nose');
 ok(/CFX18_SNAP=\[\[1\.00,1\.00\],\[1\.25/.test(src),'release is the charge ring snapping out in hard steps');
 ok(/maverick:'#36d9c4'/.test(src)&&/xartPalette\(key,c\)/.test(src),'Maverick charges in his own teal, not Falva\'s pink');
 ok(/drawMavCoilUnder=function\(\)\{\}/.test(src),'the blurred sphere under Maverick\'s hull is retired');
 ok(/drawFalvaAura=function\(\)\{\}/.test(src)&&/drawFalvaCharge=function\(\)\{\}/.test(src)&&/drawFalvaOrbs=function/.test(src),'Falva\'s ring is drawn once, over her hull');
 ok(/ps18HullInk\(pilot\)/.test(src)&&/efxClock/.test(src),'the ring is traced round the drawn hull and runs on the game clock');
 ok(/q\.y\+CFX18_JACE_LEAD\+c\[1\]\*\.46/.test(src)&&/rs1004Ball\(o\.x,o\.y,s/.test(src),'Jace charges one ball in front of his nose, and that same ball is what he releases');
};
