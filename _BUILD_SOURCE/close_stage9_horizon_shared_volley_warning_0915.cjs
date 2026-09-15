const fs=require('fs'),p='docs/REQUEST_CHECKLIST_0914.json',d=JSON.parse(fs.readFileSync(p,'utf8')),i=d.items.find(x=>x.id==='ENG-02');
i.request='Migrate all dangerous non-laser boss/miniboss attacks to the shared warning rule. Covered families now include the Stage-9 Event Horizon and independent Warp Sentinel radial/aimed volleys; remaining encounter families need review.';
d.updated='2026-09-15';d.latestBatch={description:'Stage-9 Event Horizon and twin Warp Sentinel radial/aimed volleys with independent committed 0.62-second shared warnings',evidence:'STAGE9_HORIZON_SHARED_VOLLEY_WARNING_0915.md'};
fs.writeFileSync(p,JSON.stringify(d,null,2).replace(/\n/g,'\r\n')+'\r\n');
