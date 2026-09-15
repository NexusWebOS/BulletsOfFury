const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const p=path.join(root,'docs','REQUEST_CHECKLIST_0914.json');
const data=JSON.parse(fs.readFileSync(p,'utf8'));
const row=data.items.find(x=>x.id==='S3-09');
if(!row)throw new Error('S3-09 missing');
if(row.status!=='pending')throw new Error('S3-09 status drift: '+row.status);
row.status='complete';
row.evidence='FROST_CRUISER_FURIOUS_CHARGE_0915.md';
data.updated='2026-09-15';
data.latestBatch={
  description:"Completed the Furious Frost Cruiser's six-rocket Retina volley into a late-committed, rotated body charge with a safe bounded offscreen return.",
  evidence:'FROST_CRUISER_FURIOUS_CHARGE_0915.md'
};
fs.writeFileSync(p,JSON.stringify(data,null,2)+'\n','utf8');
fs.copyFileSync(path.join(root,'_shots','frost_cruiser_furious_charge_0915','results.json'),path.join(root,'docs','qa','frost_cruiser_furious_charge_0915.json'));
console.log('closed S3-09');

