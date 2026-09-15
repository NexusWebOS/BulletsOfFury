const fs=require('fs');
const p='docs/REQUEST_CHECKLIST_0914.json';
const list=JSON.parse(fs.readFileSync(p,'utf8'));
const item=list.items.find(x=>x.id==='ENG-02');
item.request='Migrate all dangerous non-laser boss/miniboss attacks to the shared warning rule. Chrome Hammer, Xeno Regent, Furnace eyes and rollerball, Stage-3 central pulse, Jungle Overlord-X charge, Storm Sovereign ram, Razorback rams, Chrome Hammer leap, Toxic Portal Warden rail/minefield/cannon burst, and Stage-8 Vile Annihilation are covered; remaining encounter families need review.';
list.updated='2026-09-15';
list.latestBatch={description:'Stage-8 Furious Death Annihilation with a committed cross center, four exact converging green/yellow/red fields, an unobscured alert, retained target reticle and exact eight-round first-wave paths',evidence:'STAGE8_VILE_SHARED_ANNIHILATION_WARNING_0915.md'};
fs.writeFileSync(p,JSON.stringify(list,null,2).replace(/\n/g,'\r\n')+'\r\n');
