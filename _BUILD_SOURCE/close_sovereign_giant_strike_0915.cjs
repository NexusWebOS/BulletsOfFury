const fs=require('fs'),path=require('path'),root=path.resolve(__dirname,'..'),src=path.join(root,'_shots','sovereign_giant_strike_0915','results.json');
if(!fs.existsSync(src))throw new Error('missing Chromium evidence');const qa=JSON.parse(fs.readFileSync(src,'utf8'));if((qa.errors||[]).length||(qa.checks||[]).some(x=>!x.pass))throw new Error('Chromium evidence is not green');
const qout=path.join(root,'docs','qa','sovereign_giant_strike_0915.json');fs.mkdirSync(path.dirname(qout),{recursive:true});fs.writeFileSync(qout,JSON.stringify(qa,null,2)+'\n');
const p=path.join(root,'docs','REQUEST_CHECKLIST_0914.json'),list=JSON.parse(fs.readFileSync(p,'utf8')),items=list.items,item=items.find(x=>x.id==='S4-15');if(!item)throw new Error('S4-15 missing');
item.status='complete';item.evidence='SOVEREIGN_GIANT_LIGHTNING_0915.md';list.updated='2026-09-15';list.latestBatch={description:'Furious Storm Sovereign five-second giant lightning strike with shared yellow/red warnings, authored charge art, red release flash, suspended helper fire, and two measured safe corner lanes',evidence:'SOVEREIGN_GIANT_LIGHTNING_0915.md'};fs.writeFileSync(p,JSON.stringify(list,null,2).replace(/\n/g,'\r\n')+'\r\n');
function appendOnce(file,mark,text){const p=path.join(root,file),s=fs.readFileSync(p,'utf8');if(!s.includes(mark))fs.appendFileSync(p,'\n'+text.trim()+'\n');}
appendOnce('CLAUDE.md','## 2026-09-15 Sovereign giant lightning strike',`
## 2026-09-15 Sovereign giant lightning strike
S4-15 complete. Furious now follows its expanded chain phase with an exact five-second giant-lightning tell: shared yellow/red FOV and alert art, darkened screen, authored crackling core, final red flash, central seven-column strike, and 17% safe lanes at both camera edges. Helpers/final guns pause during the event; Normal/Hard are unchanged. Focused 13/13, Chromium 15/15 zero errors, full suite exact 57-name baseline. Tally 120 complete / 9 partial / 20 pending. See docs/SOVEREIGN_GIANT_LIGHTNING_0915.md.
`);
appendOnce('HANDOFF_CODEX.md','## Codex update — 2026-09-15: Sovereign giant lightning strike',`
## Codex update — 2026-09-15: Sovereign giant lightning strike

- S4-15 is complete: Furious Sovereign follows chain lightning with an exact five-second yellow/red warning, darkened authored core charge, red release flash, and seven-column central lightning field. Both 17% camera-edge lanes remain safe and helper/final-gun fire pauses for readability.
- Normal/Hard routing is unchanged. Focused 13/13, Chromium 15/15 with zero errors, full suite exact 57-name baseline. Evidence: docs/SOVEREIGN_GIANT_LIGHTNING_0915.md. Tally: 120 complete / 9 partial / 20 pending.
`);
console.log('CLOSED_SOVEREIGN_GIANT_STRIKE_0915');
