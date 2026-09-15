const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const p=path.join(root,'docs','REQUEST_CHECKLIST_0914.json');
const data=JSON.parse(fs.readFileSync(p,'utf8'));
const row=data.items.find(x=>x.id==='S3-13');
if(!row)throw new Error('S3-13 missing');
if(row.status!=='pending')throw new Error('S3-13 status drift: '+row.status);
row.status='complete';
row.evidence='RIME_WALL_FURIOUS_SIMON_0915.md';
data.updated='2026-09-15';
data.latestBatch={
  description:'Completed the Furious Rime Wall Simon-Says side-cannon sequence: yellow/red/yellow/red/red-flash, no green or overhead marker, then one fixed committed beam. Also repaired the live Hard laser-ball route.',
  evidence:'RIME_WALL_FURIOUS_SIMON_0915.md'
};
fs.writeFileSync(p,JSON.stringify(data,null,2)+'\n','utf8');
fs.copyFileSync(path.join(root,'_shots','rime_furious_simon_0915','results.json'),path.join(root,'docs','qa','rime_furious_simon_0915.json'));
console.log('closed S3-13');
