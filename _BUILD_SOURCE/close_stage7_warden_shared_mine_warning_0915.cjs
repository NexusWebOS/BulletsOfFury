const fs=require('fs');
const p='docs/REQUEST_CHECKLIST_0914.json';
const list=JSON.parse(fs.readFileSync(p,'utf8'));
const item=list.items.find(x=>x.id==='ENG-02');
item.request='Migrate all dangerous non-laser boss/miniboss attacks to the shared warning rule. Chrome Hammer, Xeno Regent, Furnace eyes and rollerball, Stage-3 central pulse, Jungle Overlord-X charge, Storm Sovereign ram, Razorback rams, Chrome Hammer leap, and Toxic Portal Warden rail/minefield are covered; remaining encounter families need review.';
list.updated='2026-09-15';
list.latestBatch={description:'Stage-7 Toxic Portal Warden minefield with a charge-start safe-column commitment, six shared green/yellow/red lane fields, one unobscured alert and exact preview-to-release anchors',evidence:'STAGE7_WARDEN_SHARED_MINE_WARNING_0915.md'};
fs.writeFileSync(p,JSON.stringify(list,null,2).replace(/\n/g,'\r\n')+'\r\n');
