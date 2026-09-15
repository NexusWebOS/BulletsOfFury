const fs=require('fs'),path=require('path'),root=path.resolve(__dirname,'..');
const src=path.join(root,'_shots','sovereign_helper_enrage_0915','results.json');if(!fs.existsSync(src))throw new Error('missing Chromium evidence');
const qa=JSON.parse(fs.readFileSync(src,'utf8'));if((qa.errors||[]).length||(qa.checks||[]).some(x=>!x.pass))throw new Error('Chromium evidence is not green');
const qout=path.join(root,'docs','qa','sovereign_helper_enrage_0915.json');fs.mkdirSync(path.dirname(qout),{recursive:true});fs.writeFileSync(qout,JSON.stringify(qa,null,2)+'\n');
const p=path.join(root,'docs','REQUEST_CHECKLIST_0914.json'),list=JSON.parse(fs.readFileSync(p,'utf8')),items=Array.isArray(list)?list:list.items,item=items.find(x=>x.id==='S4-12');
if(!item)throw new Error('S4-12 missing');item.status='complete';item.evidence='SOVEREIGN_HELPER_ENRAGE_0915.md';fs.writeFileSync(p,JSON.stringify(list,null,2).replace(/\n/g,'\r\n')+'\r\n');
function appendOnce(file,mark,text){const p=path.join(root,file),s=fs.readFileSync(p,'utf8');if(!s.includes(mark))fs.appendFileSync(p,'\n'+text.trim()+'\n');}
appendOnce('CLAUDE.md','## 2026-09-15 Sovereign helper enrage',`
## 2026-09-15 Sovereign helper enrage
S4-12 complete. A Hard/Furious generator hit enrages the surviving Sovereign helpers once per node cycle: true red palette, glowing asterisk, opposite side stations, inward hull aim and staggered six-round rapid streams with repeated traversable gaps. The boss holds and pauses unrelated orb/final-gun pressure during the 5.6s Hard / 6.8s Furious phase. Focused section 326 passes 12/12; Chromium 19/19 with zero errors; repeat full suite exact 57-name baseline. See docs/SOVEREIGN_HELPER_ENRAGE_0915.md.
`);
appendOnce('HANDOFF_CODEX.md','## Codex update — 2026-09-15: Sovereign helper enrage',`
## Codex update — 2026-09-15: Sovereign helper enrage

- S4-12 is complete: real Hard/Furious generator damage sends surviving helpers red to opposite edges with glowing asterisks, inward hull aim, and staggered six-round streams separated by recurring dodge gaps.
- The dedicated phase lasts 5.6s on Hard and 6.8s on Furious; unrelated boss orb/final-gun pressure pauses so the intended route remains visible. Normal is unchanged, and S4-13 still owns the later spider-walk tracking response.
- Verification: focused 12/12, Chromium 19/19 with zero errors, repeat full suite exact 57-name baseline. Evidence: docs/SOVEREIGN_HELPER_ENRAGE_0915.md.
`);
console.log('CLOSED_SOVEREIGN_HELPER_ENRAGE_0915');
