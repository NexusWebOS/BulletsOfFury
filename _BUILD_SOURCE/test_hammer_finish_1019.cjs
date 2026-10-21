module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path'),r=path.resolve(__dirname,'..');
 console.log('=== Hammer finish 1019: PixelLab banks and physical registration ===');
 const a=JSON.parse(fs.readFileSync(path.join(r,'assets/game/levels/stage_05/boss/hammer_finish_1019/manifest.json'),'utf8'));
 for(const [name,bank]of Object.entries(a.banks)){
  ok(bank.length===(name==='chaingun'?9:5),name+' has the complete accepted bank');
  ok(bank.every(a=>{const p=path.join(r,a.path);if(!fs.existsSync(p))return false;const b=fs.readFileSync(p);return b.readUInt32BE(16)===256&&b.readUInt32BE(20)===256;}),name+' real PNG dimensions match the even fixed canvas');
  ok(bank.every(a=>String(a.pivot)===String(bank[0].pivot)&&a.bounds[0]>0&&a.bounds[1]>0&&a.bounds[2]<256&&a.bounds[3]<256),name+' preserves a common pivot and uncropped transparent margins');
  ok(new Set(bank.map(a=>a.sha256)).size===bank.length,name+' contains distinct source poses');
 }
 const html=fs.readFileSync(path.join(r,'index.html'),'utf8');
 ok(html.indexOf('assets/hammer_finish_art_1019.js')<html.indexOf('assets/hammer_finish_1019.js')&&html.indexOf('assets/hammer_finish_1019.js')>html.indexOf('assets/harrier_fan_1019.js'),'new Hammer art loads before its controller and after the native donor rig');
};
