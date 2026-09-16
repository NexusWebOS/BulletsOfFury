const fs=require('fs'),path=require('path'),root=path.resolve(__dirname,'..');
const checklist=path.join(root,'docs','REQUEST_CHECKLIST_0914.json'),data=JSON.parse(fs.readFileSync(checklist,'utf8'));
const item=data.items.find(x=>x.id==='SPACE-23');if(!item||item.status!=='complete')throw new Error('SPACE-23 complete row missing');
item.request='Chrome Hammer Archmage one-hand boomerang: rapidly spin and charge the authored hammer, warn its committed vertical player lane, throw it downfield, turn below the playfield, then visibly retract it to the raised hand at medium magnetic speed with sounds.';
const eng=data.items.find(x=>x.id==='ENG-02');if(!eng||eng.status!=='partial')throw new Error('ENG-02 partial row missing');
eng.request='Migrate all dangerous non-laser boss/miniboss attacks to the shared warning rule. Covered families now include the Stage-5 Chrome Hammer Archmage vertical boomerang, Stage-6 Thunderhead, Stage-9 Event Horizon, independent Warp Sentinel radial/aimed volleys, and every row of the Tidal Sovereign cascade; remaining encounter families need review.';
item.evidence='ARCHMAGE_BOOMERANG_VISUAL_0916.md';data.updated='2026-09-16';data.latestBatch={description:'active Stage-5 Chrome Hammer Archmage boomerang warning, authored one-hand twirl, cleaned motion echoes and verified magnetic catch',evidence:'ARCHMAGE_BOOMERANG_VISUAL_0916.md'};
fs.writeFileSync(checklist,JSON.stringify(data,null,2).replace(/\n/g,'\r\n')+'\r\n','utf8');
const appendOnce=(rel,mark,body)=>{const p=path.join(root,rel),s=fs.readFileSync(p,'utf8');if(!s.includes(mark))fs.writeFileSync(p,s.replace(/\s*$/,'')+'\r\n\r\n'+body.trim()+'\r\n','utf8');};
appendOnce('docs/SHARED_NONLASER_WARNING_0915.md','## Stage 5 Archmage boomerang follow-up',`## Stage 5 Archmage boomerang follow-up

The active Chrome Hammer Archmage one-hand twirl now preserves the boomerang controller's committed vertical lane and floor reticle through the shared green/yellow/red warning. The alert is placed beside the boss to clear its destructible-module labels. Chromium passes 19/19 and focused active-render section 342 passes 6/6. See [ARCHMAGE_BOOMERANG_VISUAL_0916.md](ARCHMAGE_BOOMERANG_VISUAL_0916.md).`);
appendOnce('CLAUDE.md','## 2026-09-16 active Archmage boomerang visual repair',`## 2026-09-16 active Archmage boomerang visual repair
SPACE-23 remains complete against the current Chrome Hammer Archmage controller. The Archmage art merge had preserved mechanics but bypassed the shared warning draw; the active authored one-hand twirl now restores its committed green/yellow/red lane and floor reticle. The alert clears the CHAINGUN label, and the outbound/return reel uses one solid hammer plus three faint authored motion echoes instead of six opaque clones. Focused sections 304e and 342 pass 12/12 and 6/6. Chromium passes 19/19 with zero errors. Full suite: 4,364 passes, the established 56 failures plus the known intermittent sand-tank fixture. See docs/ARCHMAGE_BOOMERANG_VISUAL_0916.md.`);
appendOnce('HANDOFF_CODEX.md','## Codex update — 2026-09-16: active Archmage boomerang repair',`## Codex update — 2026-09-16: active Archmage boomerang repair

- The current Chrome Hammer Archmage again shows the committed green/yellow/red lane and floor reticle during its authored one-hand twirl. The alert no longer overlaps the CHAINGUN module label.
- The detached authored hammer descends vertically, turns below the screen, returns at the capped medium magnetic speed and catches in the raised hand. One solid weapon plus three faint motion echoes replaces the accidental row of opaque hammer clones.
- Focused 12/12 mechanics and 6/6 active-render checks; Chromium 19/19 with zero errors; full suite 4,364 passes with the established 56 failures plus the intermittent Stage-1 sand-tank fixture. Evidence: docs/ARCHMAGE_BOOMERANG_VISUAL_0916.md. Tally remains 128 complete / 7 partial / 16 pending.`);
console.log('CLOSED_ARCHMAGE_BOOMERANG_VISUAL_0916');
