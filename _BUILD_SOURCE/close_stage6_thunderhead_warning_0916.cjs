const fs=require('fs'),path=require('path'),root=path.resolve(__dirname,'..');
const checklist=path.join(root,'docs','REQUEST_CHECKLIST_0914.json'),data=JSON.parse(fs.readFileSync(checklist,'utf8'));
const item=data.items.find(x=>x.id==='ENG-02');if(!item||item.status!=='partial')throw new Error('ENG-02 partial row missing');
item.request='Migrate all dangerous non-laser boss/miniboss attacks to the shared warning rule. Covered families now include the Stage-6 Thunderhead, Stage-9 Event Horizon, independent Warp Sentinel radial/aimed volleys, and every row of the Tidal Sovereign cascade; remaining encounter families need review.';
data.updated='2026-09-16';data.latestBatch={description:'all four live Stage-6 Thunderhead rows with committed two-column openings and 0.66-second shared warnings',evidence:'STAGE6_THUNDERHEAD_WARNING_0916.md'};
fs.writeFileSync(checklist,JSON.stringify(data,null,2).replace(/\n/g,'\r\n')+'\r\n','utf8');
const appendOnce=(rel,mark,body)=>{const p=path.join(root,rel),s=fs.readFileSync(p,'utf8');if(!s.includes(mark))fs.writeFileSync(p,s.replace(/\s*$/,'')+'\r\n\r\n'+body.trim()+'\r\n','utf8');};
appendOnce('docs/SHARED_NONLASER_WARNING_0915.md','## Stage 6 Thunderhead follow-up',`## Stage 6 Thunderhead follow-up

All four live Doomsday Carrier Mk II Thunderhead rows now commit their two-column opening, preview the other six exact release columns through shared green/yellow/red fields, then move the opening one column for the next warned row. Chromium passes 19/19 and focused section 341 passes 12/12. See [STAGE6_THUNDERHEAD_WARNING_0916.md](STAGE6_THUNDERHEAD_WARNING_0916.md).`);
appendOnce('CLAUDE.md','## 2026-09-16 Stage-6 Thunderhead shared row warnings',`## 2026-09-16 Stage-6 Thunderhead shared row warnings
ENG-02 advances: every live Thunderhead row on the Doomsday Carrier Mk II now uses a committed 0.66-second shared green/yellow/red warning over its exact six dangerous columns and two-column opening. Focused 12/12, Chromium 19/19 with zero errors, and full suite 4,358 passes with the exact 57-name baseline. ENG-02 remains partial. See docs/STAGE6_THUNDERHEAD_WARNING_0916.md.`);
appendOnce('HANDOFF_CODEX.md','## Codex update — 2026-09-16: Stage-6 Thunderhead row warnings',`## Codex update — 2026-09-16: Stage-6 Thunderhead row warnings

- ENG-02 advances: all four live Doomsday Carrier Mk II Thunderhead rows now own a 0.66-second shared green/yellow/red warning. Six fields match the twelve released projectiles while two adjacent columns remain open; the opening moves one column only after release.
- Fields render behind the giant carrier and its storm nodes; the matching alert remains visible above them and below the boss gauge. Focused 12/12, Chromium 19/19 with zero errors, full suite 4,358 passes with the exact 57-name baseline. Evidence: docs/STAGE6_THUNDERHEAD_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.`);
console.log('CLOSED_STAGE6_THUNDERHEAD_WARNING_0916');
