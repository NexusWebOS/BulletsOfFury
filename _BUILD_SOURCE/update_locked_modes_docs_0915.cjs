const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),p=path.join(root,'docs','REQUEST_CHECKLIST_0914.json');
const data=JSON.parse(fs.readFileSync(p,'utf8'));
function finish(id){const x=data.items.find(q=>q.id===id);if(!x)throw new Error('missing '+id);x.status='complete';x.evidence='LOCKED_MODES_0915.md';x.dependency='';}
finish('ACH-12');finish('ACH-13');
data.updated='2026-09-15';
data.latestBatch={description:'Added the five-mode New Game roster plus generated Boss Rush and Time Attack plates, exact Nexus II chain locks, blocked-alert denial and a persistent final-Campaign-clear reveal gate.',evidence:'LOCKED_MODES_0915.md'};
fs.writeFileSync(p,JSON.stringify(data,null,2)+'\n','utf8');
console.log('completed ACH-12 and ACH-13 in request ledger');
