const fs=require('fs');const path=require('path');const root=path.resolve(__dirname,'..');
const p=path.join(root,'docs','REQUEST_CHECKLIST_0914.json');const data=JSON.parse(fs.readFileSync(p,'utf8'));
const row=data.items.find(x=>x.id==='S3-11');if(!row)throw new Error('S3-11 missing');if(row.status!=='pending')throw new Error('S3-11 status drift: '+row.status);
row.status='complete';row.evidence='RIME_WALL_HARD_LASER_BALLS_0915.md';data.updated='2026-09-15';
data.latestBatch={description:"Completed the below-half Hard/Furious Rime Wall laser-ball pressure: one Retina, two physical cannon releases, shoot-down collision, shared evasion break and clean offscreen commitment.",evidence:'RIME_WALL_HARD_LASER_BALLS_0915.md'};
fs.writeFileSync(p,JSON.stringify(data,null,2)+'\n','utf8');
fs.copyFileSync(path.join(root,'_shots','stage3_hard_laser_balls_0915','results.json'),path.join(root,'docs','qa','stage3_hard_laser_balls_0915.json'));
console.log('closed S3-11');

