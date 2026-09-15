const fs=require('fs'),path=require('path'),root=path.resolve(__dirname,'..'),src=path.join(root,'_shots','razorback_duo_0915','results.json');
if(!fs.existsSync(src))throw new Error('missing Chromium evidence');const qa=JSON.parse(fs.readFileSync(src,'utf8'));if((qa.errors||[]).length||(qa.checks||[]).some(x=>!x.pass))throw new Error('Chromium evidence is not green');
const qout=path.join(root,'docs','qa','razorback_duo_0915.json');fs.mkdirSync(path.dirname(qout),{recursive:true});fs.writeFileSync(qout,JSON.stringify(qa,null,2)+'\n');
const p=path.join(root,'docs','REQUEST_CHECKLIST_0914.json'),list=JSON.parse(fs.readFileSync(p,'utf8')),item=list.items.find(x=>x.id==='S1-05');if(!item)throw new Error('S1-05 missing');
item.status='complete';item.evidence='RAZORBACK_DUO_0915.md';list.updated='2026-09-15';list.latestBatch={description:'Hard Stage-1 Razorback duo with two complete authored tanks, independent component pools and attacks, camera-safe lanes, actor-specific damage and two-kill completion',evidence:'RAZORBACK_DUO_0915.md'};fs.writeFileSync(p,JSON.stringify(list,null,2).replace(/\n/g,'\r\n')+'\r\n');
function appendOnce(file,mark,text){const p=path.join(root,file),s=fs.readFileSync(p,'utf8');if(!s.includes(mark))fs.appendFileSync(p,'\n'+text.trim()+'\n');}
appendOnce('CLAUDE.md','## 2026-09-15 Hard Razorback duo',`
## 2026-09-15 Hard Razorback duo
S1-05 complete. Hard Stage 1 now fields two complete Razorback siege tanks under one combined miniboss gauge. Each actor owns its authored rig, component pools, attack book, ordnance, locks and death; camera-relative lanes keep both readable and one tank continues after its partner dies. Normal and Furious remain single. Focused 14/14, Chromium 17/17 zero errors, full suite exact 57-name baseline. Tally 121 complete / 9 partial / 19 pending. See docs/RAZORBACK_DUO_0915.md.
`);
appendOnce('HANDOFF_CODEX.md','## Codex update — 2026-09-15: Hard Razorback duo',`
## Codex update — 2026-09-15: Hard Razorback duo

- S1-05 is complete: Hard Stage 1 fields two full Razorbacks at once with independent destructible components, offset attack books, owned ordnance/locks, camera-safe movement and a combined gauge that requires both kills.
- Normal and Furious remain single for their distinct designs. Focused 14/14, Chromium 17/17 with zero errors, full suite exact 57-name baseline. Evidence: docs/RAZORBACK_DUO_0915.md. Tally: 121 complete / 9 partial / 19 pending; S1-06 is the next ready encounter.
`);
console.log('CLOSED_RAZORBACK_DUO_0915');
