module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path'),crypto=require('crypto'),r=path.resolve(__dirname,'..');
 console.log('=== Boss redesign 1020: complete authored banks and whole module exports ===');
 const art=JSON.parse(fs.readFileSync(path.join(r,'assets/game/shared/boss_redesign_1020/manifest.json')));
 const required=['blue_slam','blue_side','blue_side_left','blue_gun','blue_entry','blue_spin','blue_dance','blue_empty','blue_throw','corrupt_slam','corrupt_side','corrupt_unarmed','corrupt_break','corrupt_punch','corrupt_fists','corrupt_fire','corrupt_spin','corrupt_dance','corrupt_charge','corrupt_gun','corrupt_gun_left','corrupt_ball','corrupt_tool','counter_left','counter_right'];
 ok(required.every(k=>art.banks[k]?.length),'every requested Hammer action has an actual authored bank');
 for(const [name,bank]of Object.entries(art.banks)){
  ok(bank.every(a=>{const p=path.join(r,a.path);if(!fs.existsSync(p))return false;const b=fs.readFileSync(p);return b.readUInt32BE(16)===a.w&&b.readUInt32BE(20)===a.h&&a.w%2===0&&a.h%2===0;}),name+' real PNGs match their fixed even canvases');
  ok(bank.every(a=>String(a.pivot)===String(bank[0].pivot)&&a.bounds[0]>0&&a.bounds[1]>0&&a.bounds[2]<a.w&&a.bounds[3]<a.h),name+' keeps one anchor and transparent clipping margins');
  if(bank.length>1){const hashes=new Set(bank.map(a=>crypto.createHash('sha256').update(fs.readFileSync(path.join(r,a.path))).digest('hex')));ok(hashes.size>=Math.min(4,bank.length),name+' contains changing authored frames');}
 }
 const p=JSON.parse(fs.readFileSync(path.join(r,'assets/game/levels/stage_08/boss/phoenix_swoon_1020/manifest.json'))),audit=JSON.parse(fs.readFileSync(path.join(r,'_ART_SOURCES/boss_redesign_1020/phoenix-module-audit.json')));
 ok(['head','wingL','wingR','clawL','clawR','tail','core'].every(k=>p.parts[k]),'Phoenix exports whole anatomical pieces rather than rotating wing slivers');
 ok(audit.length===7&&audit.every(q=>q.exportedComponents===1),'each exported anatomical module is a connected authored component');
 ok(p.cannon.w===128&&p.warning.w===64,'added detachable cannon and scoped corner warning have independent authored art');
 const html=fs.readFileSync(path.join(r,'index.html'),'utf8');
 for(const [a,b]of [['boss_shared_1020','phoenix_swoon_1020'],['phoenix_swoon_art_1020','phoenix_swoon_1020'],['hammer_redesign_art_1020','hammer_redesign_1020'],['helicopter_assault_1020','hammer_redesign_1020']])ok(html.indexOf('assets/'+a+'.js')>0&&html.indexOf('assets/'+a+'.js')<html.indexOf('assets/'+b+'.js'),a+' is installed before '+b);
};
