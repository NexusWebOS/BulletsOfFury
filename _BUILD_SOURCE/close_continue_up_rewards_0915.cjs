const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');

const result=path.join(root,'_shots','continue_up_rewards_0915','results.json');
if(!fs.existsSync(result))throw new Error('missing native Chromium result');
const qa=JSON.parse(fs.readFileSync(result,'utf8'));
if(qa.errors.length||qa.checks.some(q=>!q.pass))throw new Error('native Chromium result is not green');
const qaOut=path.join(root,'docs','qa','continue_up_rewards_0915.json');
fs.mkdirSync(path.dirname(qaOut),{recursive:true});
fs.writeFileSync(qaOut,JSON.stringify(qa,null,2)+'\n','utf8');

const listPath=path.join(root,'docs','REQUEST_CHECKLIST_0914.json');
const list=JSON.parse(fs.readFileSync(listPath,'utf8'));
const items=Array.isArray(list)?list:list.items;
const item=items.find(q=>q.id==='MODE-07');
if(!item)throw new Error('MODE-07 missing from checklist');
item.status='complete';item.evidence='CONTINUE_UP_REWARDS_0915.md';
fs.writeFileSync(listPath,JSON.stringify(list,null,2).replace(/\n/g,'\r\n')+'\r\n','utf8');

function appendOnce(file,marker,text){
  const p=path.join(root,file),s=fs.readFileSync(p,'utf8');
  if(!s.includes(marker))fs.appendFileSync(p,'\n'+text.trim()+'\n','utf8');
}
appendOnce('CLAUDE.md','## 2026-09-15 Continue Up rewards',`
## 2026-09-15 Continue Up rewards
MODE-07 complete. Hard/Furious authored aces and deathless miniboss/boss encounter sections now drop one physical Continue Up. Either co-op seat dying invalidates a deathless encounter reward. Collection extends finite banks, persists in campaign saves and appears on the Continue screen. Current presentation composes the authored Life Up with a cyan C/ring; dedicated SpriteCook art remains MODE-08. Focused section 324 passes 18/18; Chromium passes 18/18 with zero errors; full suite retains the exact 57-name baseline. See docs/CONTINUE_UP_REWARDS_0915.md.
`);
appendOnce('HANDOFF_CODEX.md','## Codex update — 2026-09-15: Continue Up rewards',`
## Codex update — 2026-09-15: Continue Up rewards

- MODE-07 is complete: deathless miniboss/boss encounters and Hard/Furious authored aces drop a physical Continue Up exactly once.
- Either co-op seat dying blocks the deathless reward. The collected credit extends the shared finite bank, survives campaign save/load, and is shown on the Continue screen.
- Current art is a clearly marked composition of the authored Life Up; MODE-08 still owns the dedicated SpriteCook pickup art.
- Verification: focused 18/18, Chromium 18/18 with zero errors, full suite exact 57-name recorded baseline. Evidence: docs/CONTINUE_UP_REWARDS_0915.md.
`);
console.log('CLOSED_CONTINUE_UP_REWARDS_0915');
