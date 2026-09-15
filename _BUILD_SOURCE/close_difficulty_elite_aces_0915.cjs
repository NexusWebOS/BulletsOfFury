const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const p=path.join(root,'docs','REQUEST_CHECKLIST_0914.json');
const data=JSON.parse(fs.readFileSync(p,'utf8'));
const row=data.items.find(x=>x.id==='MODE-05');
if(!row)throw new Error('MODE-05 missing');
if(row.status!=='pending')throw new Error('MODE-05 status drift: '+row.status);
row.status='complete';
row.evidence='DIFFICULTY_ELITE_ACES_0915.md';
data.updated='2026-09-15';
data.latestBatch={
  description:'Completed authored Hard/Furious elite ace injection across all nine stages with stable scheduling, shielded Elite X behavior and exact renderer warmup.',
  evidence:'DIFFICULTY_ELITE_ACES_0915.md'
};
fs.writeFileSync(p,JSON.stringify(data,null,2)+'\n','utf8');
fs.copyFileSync(path.join(root,'_shots','difficulty_elite_aces_0915','results.json'),path.join(root,'docs','qa','difficulty_elite_aces_0915.json'));
console.log('closed MODE-05');
