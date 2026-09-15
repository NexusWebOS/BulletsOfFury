const fs=require('fs'),path=require('path'),root=path.resolve(__dirname,'..'),src=path.join(root,'_shots','razorback_furious_0915','results.json');
if(!fs.existsSync(src))throw new Error('missing Chromium evidence');const qa=JSON.parse(fs.readFileSync(src,'utf8'));if((qa.errors||[]).length||(qa.checks||[]).some(x=>!x.pass))throw new Error('Chromium evidence is not green');
const qout=path.join(root,'docs','qa','razorback_furious_0915.json');fs.mkdirSync(path.dirname(qout),{recursive:true});fs.writeFileSync(qout,JSON.stringify(qa,null,2)+'\n');
const p=path.join(root,'docs','REQUEST_CHECKLIST_0914.json'),list=JSON.parse(fs.readFileSync(p,'utf8')),item=list.items.find(x=>x.id==='S1-06');if(!item)throw new Error('S1-06 missing');
item.status='complete';item.evidence='RAZORBACK_FURIOUS_0915.md';list.updated='2026-09-15';list.latestBatch={description:'Furious Stage-1 Razorback hyper tank with an exact 150% authored silhouette, crimson palette, accelerated drivetrain and expanded sonic, nova and missile pressure',evidence:'RAZORBACK_FURIOUS_0915.md'};fs.writeFileSync(p,JSON.stringify(list,null,2).replace(/\n/g,'\r\n')+'\r\n');
function appendOnce(file,mark,text){const p=path.join(root,file),s=fs.readFileSync(p,'utf8');if(!s.includes(mark))fs.appendFileSync(p,'\n'+text.trim()+'\n');}
appendOnce('CLAUDE.md','## 2026-09-15 Furious Razorback hyper tank',`
## 2026-09-15 Furious Razorback hyper tank
S1-06 complete. Furious Stage 1 now fields one 150%-scale crimson Razorback with scaled hardpoints/hit geometry, a 62%-faster drivetrain, 55%-faster turning, 30%-faster attack clock, nine-round sonic fan, giant pressure wave, 28-round nova and fourteen-missile Razor Rack. Normal and the Hard duo remain unchanged. Focused 14/14, Chromium 17/17 zero errors, full suite exact 57-name baseline. Tally 122 complete / 9 partial / 18 pending. See docs/RAZORBACK_FURIOUS_0915.md.
`);
appendOnce('HANDOFF_CODEX.md','## Codex update — 2026-09-15: Furious Razorback hyper tank',`
## Codex update — 2026-09-15: Furious Razorback hyper tank

- S1-06 is complete: Furious Stage 1 fields one exact 150%-scale crimson Razorback with matching hardpoints/collision, faster movement/turn/attack clocks and expanded sonic, resonance-nova and Razor Rack pressure.
- Normal remains the original single tank and Hard remains the independent two-tank fight. Focused 14/14, Chromium 17/17 with zero errors, full suite exact 57-name baseline. Evidence: docs/RAZORBACK_FURIOUS_0915.md. Tally: 122 complete / 9 partial / 18 pending; S2-08 is the next unfinished queue item.
`);
console.log('CLOSED_RAZORBACK_FURIOUS_0915');
