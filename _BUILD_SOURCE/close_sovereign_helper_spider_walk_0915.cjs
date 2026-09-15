const fs=require('fs'),path=require('path'),root=path.resolve(__dirname,'..'),src=path.join(root,'_shots','sovereign_helper_spider_walk_0915','results.json');
if(!fs.existsSync(src))throw new Error('missing Chromium evidence');const qa=JSON.parse(fs.readFileSync(src,'utf8'));if((qa.errors||[]).length||(qa.checks||[]).some(x=>!x.pass))throw new Error('Chromium evidence is not green');
const qout=path.join(root,'docs','qa','sovereign_helper_spider_walk_0915.json');fs.mkdirSync(path.dirname(qout),{recursive:true});fs.writeFileSync(qout,JSON.stringify(qa,null,2)+'\n');
const p=path.join(root,'docs','REQUEST_CHECKLIST_0914.json'),list=JSON.parse(fs.readFileSync(p,'utf8')),items=Array.isArray(list)?list:list.items,item=items.find(x=>x.id==='S4-13');
if(!item)throw new Error('S4-13 missing');item.status='complete';item.evidence='SOVEREIGN_HELPER_SPIDER_WALK_0915.md';fs.writeFileSync(p,JSON.stringify(list,null,2).replace(/\n/g,'\r\n')+'\r\n');
function appendOnce(file,mark,text){const p=path.join(root,file),s=fs.readFileSync(p,'utf8');if(!s.includes(mark))fs.appendFileSync(p,'\n'+text.trim()+'\n');}
appendOnce('CLAUDE.md','## 2026-09-15 Sovereign helper spider walk',`
## 2026-09-15 Sovereign helper spider walk
S4-13 complete. Continued generator damage during the red side-stream phase synchronizes a bounded upward-and-back helper walk: 58px Hard, 72px Furious, one response per trigger without damage-tick resets, retriggerable after return. Edge stations, separated lanes and pause windows remain intact; Normal is unchanged. Focused section 327 passes 9/9; Chromium 13/13 zero errors; full suite has 56 established names and no new failures, with only the known flaky sand-tank spawn assertion absent. See docs/SOVEREIGN_HELPER_SPIDER_WALK_0915.md.
`);
appendOnce('HANDOFF_CODEX.md','## Codex update — 2026-09-15: Sovereign helper spider walk',`
## Codex update — 2026-09-15: Sovereign helper spider walk

- S4-13 is complete: generator damage during the red side phase makes both helpers walk upward and back within explicit 58px Hard / 72px Furious limits, while preserving the edge route, separated streams, and pause windows.
- Different nodes are recognized, repeated damage cannot pin the motion at its start, and a new response can begin after the pair returns. Normal is unchanged.
- Verification: focused 9/9, Chromium 13/13 with zero errors, full suite no new failure names. Evidence: docs/SOVEREIGN_HELPER_SPIDER_WALK_0915.md.
`);
console.log('CLOSED_SOVEREIGN_HELPER_SPIDER_WALK_0915');
