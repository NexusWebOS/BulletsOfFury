const fs=require('fs');const {load}=require('./run.js');
const D='/home/user/BulletsOfFury/mr_reduction/';const A=D+'src_art/';
const b64=f=>'data:image/png;base64,'+fs.readFileSync(A+f).toString('base64');
(async()=>{
 const sample=[];for(const f of fs.readdirSync('.').filter(f=>/SIG_.*\.pdf$/.test(f)&&!/Oct_12/.test(f))){const r=await load(f);
  sample.push({file:'sample',date:r.date,tour:r.tour.startsWith('06')?'AM':'PM',tourLabel:r.tour,headerSet:r.headerSet,rows:r.rows.map(x=>[x.borough,x.station,x.fcas.join(', '),x.set||0])});}
 const art={stand:b64('hero_a.png'),split:b64('kick_a.png'),barricade:b64('icon_barricade.png'),cone:b64('icon_cone.png'),arrow:b64('icon_arrow.png'),
  idle:{src:b64('idle_sheet.png'),cols:8,n:8,fw:256,fh:256},kick:{src:b64('kick_sheet.png'),cols:8,n:8,fw:204,fh:204}};
 const parser=fs.readFileSync('parser.js','utf8').replace(/if\(typeof module[^\n]*\n?/,'');
 let t=fs.readFileSync(D+'template.html','utf8');
 const rep=(k,v)=>{if(!t.includes(k))throw new Error('missing '+k);t=t.split(k).join(v);};
 rep('__BASELINE__',fs.readFileSync('baseline.json','utf8'));rep('__SAMPLE__',JSON.stringify(sample));rep('__ART__',JSON.stringify(art));
 rep('__PARSER__',parser);rep('__BG__',b64('bg_crop.png'));rep('__ICON_HARDHAT__',b64('icon_hardhat.png'));rep('__ICON_BARRICADE__',b64('icon_barricade.png'));rep('__ICON_CONE__',b64('icon_cone.png'));
 fs.writeFileSync(D+'mr_reduction_artifact.html',t);
 fs.writeFileSync(D+'MrReduction.html','<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>\n'+t+'\n</body></html>\n');
 console.log('built',fs.statSync(D+'MrReduction.html').size, sample.map(s=>s.tour+' '+s.date));
})();
