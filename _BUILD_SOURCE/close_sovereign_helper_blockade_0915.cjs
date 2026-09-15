const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const result=path.join(root,'_shots','sovereign_helper_blockade_0915','results.json');
if(!fs.existsSync(result))throw new Error('missing Chromium evidence');
const qa=JSON.parse(fs.readFileSync(result,'utf8'));
if((qa.errors||[]).length||(qa.checks||[]).some(x=>!x.pass))throw new Error('Chromium evidence is not green');
const qaOut=path.join(root,'docs','qa','sovereign_helper_blockade_0915.json');
fs.mkdirSync(path.dirname(qaOut),{recursive:true});fs.writeFileSync(qaOut,JSON.stringify(qa,null,2)+'\n');
const listPath=path.join(root,'docs','REQUEST_CHECKLIST_0914.json'),list=JSON.parse(fs.readFileSync(listPath,'utf8'));
const items=Array.isArray(list)?list:list.items,item=items.find(x=>x.id==='S4-11');
if(!item)throw new Error('S4-11 missing');item.status='complete';item.evidence='SOVEREIGN_HELPER_BLOCKADE_0915.md';
fs.writeFileSync(listPath,JSON.stringify(list,null,2).replace(/\n/g,'\r\n')+'\r\n');
function appendOnce(file,marker,text){const p=path.join(root,file),s=fs.readFileSync(p,'utf8');if(!s.includes(marker))fs.appendFileSync(p,'\n'+text.trim()+'\n');}
appendOnce('CLAUDE.md','## 2026-09-15 Sovereign helper blockade',`
## 2026-09-15 Sovereign helper blockade
S4-11 complete. Hard/Furious Storm Sovereign helpers have 50% more shield capacity, progressively faster turns/fire/rounds, and a timed forward horizontal row that tracks the player inside safe camera edges before withdrawing. Normal remains unchanged. Focused section 325 passes 14/14; Chromium passes 17/17 with zero errors; full suite retains the exact 57-name baseline. See docs/SOVEREIGN_HELPER_BLOCKADE_0915.md.
`);
appendOnce('HANDOFF_CODEX.md','## Codex update — 2026-09-15: Sovereign helper blockade',`
## Codex update — 2026-09-15: Sovereign helper blockade

- S4-11 is complete: Hard/Furious Sovereign helpers get 50% more shield capacity, faster attack handling and a timed forward blocking row that follows the player before returning to its generator stations.
- Normal remains unchanged. S4-12 and S4-13 still own the generator-hit enrage and side-stream follow-up.
- Verification: focused 14/14, Chromium 17/17 with zero errors, and the exact established 57-name full-suite baseline. Evidence: docs/SOVEREIGN_HELPER_BLOCKADE_0915.md.
`);
console.log('CLOSED_SOVEREIGN_HELPER_BLOCKADE_0915');
