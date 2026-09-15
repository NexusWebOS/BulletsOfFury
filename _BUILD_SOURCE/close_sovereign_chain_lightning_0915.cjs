const fs=require('fs'),path=require('path'),root=path.resolve(__dirname,'..'),src=path.join(root,'_shots','sovereign_chain_lightning_0915','results.json');
if(!fs.existsSync(src))throw new Error('missing Chromium evidence');const qa=JSON.parse(fs.readFileSync(src,'utf8'));if((qa.errors||[]).length||(qa.checks||[]).some(x=>!x.pass))throw new Error('Chromium evidence is not green');
const qout=path.join(root,'docs','qa','sovereign_chain_lightning_0915.json');fs.mkdirSync(path.dirname(qout),{recursive:true});fs.writeFileSync(qout,JSON.stringify(qa,null,2)+'\n');
const p=path.join(root,'docs','REQUEST_CHECKLIST_0914.json'),list=JSON.parse(fs.readFileSync(p,'utf8')),items=Array.isArray(list)?list:list.items,item=items.find(x=>x.id==='S4-14');if(!item)throw new Error('S4-14 missing');
item.status='complete';item.evidence='SOVEREIGN_CHAIN_LIGHTNING_0915.md';fs.writeFileSync(p,JSON.stringify(list,null,2).replace(/\n/g,'\r\n')+'\r\n');
function appendOnce(file,mark,text){const p=path.join(root,file),s=fs.readFileSync(p,'utf8');if(!s.includes(mark))fs.appendFileSync(p,'\n'+text.trim()+'\n');}
appendOnce('CLAUDE.md','## 2026-09-15 Sovereign chain lightning',`
## 2026-09-15 Sovereign chain lightning
S4-14 complete. Normal retains 5 bolts/1 ball; Hard fires nine wider chain bolts; Furious widens and accelerates the nine-bolt cycle and launches three separately timed shootable balls from alternating L/R/L authored racks. Focused section 328 passes 10/10; Chromium 13/13 zero errors; full suite exact 57-name baseline. See docs/SOVEREIGN_CHAIN_LIGHTNING_0915.md.
`);
appendOnce('HANDOFF_CODEX.md','## Codex update — 2026-09-15: Sovereign chain lightning',`
## Codex update — 2026-09-15: Sovereign chain lightning

- S4-14 is complete: Hard doubles and widens both chain-lightning side volleys for nine total bolts; Furious accelerates and widens the cycle and adds three distinct shootable balls from alternating authored racks. Normal preserves its original 5-bolt/1-ball pattern.
- Verification: focused 10/10, Chromium 13/13 with zero errors, full suite exact 57-name baseline. Evidence: docs/SOVEREIGN_CHAIN_LIGHTNING_0915.md.
`);
console.log('CLOSED_SOVEREIGN_CHAIN_LIGHTNING_0915');
