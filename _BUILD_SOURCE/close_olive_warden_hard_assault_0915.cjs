const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const p=path.join(root,'docs','REQUEST_CHECKLIST_0914.json');
const data=JSON.parse(fs.readFileSync(p,'utf8'));
const row=data.items.find(x=>x.id==='S4-06');
if(!row)throw new Error('S4-06 missing');
if(row.status!=='pending')throw new Error('S4-06 status drift: '+row.status);
row.status='complete';
row.evidence='OLIVE_WARDEN_HARD_ASSAULT_0915.md';
data.updated='2026-09-15';
data.latestBatch={
  description:'Completed the Olive Warden Hard/Furious assault cycle: rapid mounted guns, continuous orbit and glide, committed three-color warned body ram, and collision-safe curved return.',
  evidence:'OLIVE_WARDEN_HARD_ASSAULT_0915.md'
};
fs.writeFileSync(p,JSON.stringify(data,null,2)+'\n','utf8');
fs.copyFileSync(path.join(root,'_shots','olive_warden_hard_assault_0915','results.json'),path.join(root,'docs','qa','olive_warden_hard_assault_0915.json'));
console.log('closed S4-06');
