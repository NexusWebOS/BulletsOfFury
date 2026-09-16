const fs=require('fs'),path=require('path'),root=path.resolve(__dirname,'..');
function read(rel){return fs.readFileSync(path.join(root,rel),'utf8');}
function writeCRLF(rel,s){fs.writeFileSync(path.join(root,rel),String(s).replace(/\r?\n/g,'\r\n'),'utf8');}
function replaceOne(rel,from,to){let s=read(rel);const n=s.split(from).length-1;if(n!==1)throw new Error(`${rel}: expected one match, got ${n}`);fs.writeFileSync(path.join(root,rel),s.replace(from,to),'utf8');}
function appendOnce(rel,heading,body){let s=read(rel);if(s.includes(heading))return;const cr=(s.match(/\r\n/g)||[]).length,lf=(s.match(/(?<!\r)\n/g)||[]).length,eol=cr>lf?'\r\n':'\n';const clean=body.trim().replace(/\r?\n/g,eol);fs.writeFileSync(path.join(root,rel),s.replace(/\s*$/,'')+eol+eol+clean+eol,'utf8');}

const qa=JSON.parse(read('_shots/archmage_core_recovery_0916/results.json'));
writeCRLF('docs/qa/archmage_core_recovery_0916.json',JSON.stringify(qa,null,2)+'\n');

const checklistPath='docs/REQUEST_CHECKLIST_0914.json',data=JSON.parse(read(checklistPath));
const eng=data.items.find(q=>q.id==='ENG-02');if(!eng)throw new Error('ENG-02 missing');
eng.request='Migrate all dangerous non-laser boss/miniboss attacks to the shared warning rule. Covered families now include the Stage-5 Chrome Hammer Archmage vertical boomerang, committed spiked-ball launch and fused mega-wave corridor, Stage-6 Doomsday Carrier twin-battery cyclone fan, alternating storm-node fans, four-barrel prism crossfire, paired gravity mines, accelerating omega bombs, mirrored cluster fan, chrome flak fan and Thunderhead, Stage-7 DUAL SCOOP DREDGER minefield and Toxic Portal Warden cripple-phase rail groups, Stage-8 BLACK COCOON crescent wall, RAVENOUS ASCENDANT five-needle fan, ABYSSAL LEVIATHAN nine-lane solar wheel, FURIOUS DEATH seven-gunship fan and four-lane straight-missile salvo, Stage-9 Event Horizon, independent Warp Sentinel radial/aimed volleys, and every row of the Tidal Sovereign cascade; remaining encounter families need review.';
data.updated='2026-09-16';data.latestBatch={description:'Stage-5 Chrome Hammer Archmage Easy/Normal core recovery and fused mega-wave warning',evidence:'ARCHMAGE_CORE_RECOVERY_0916.md'};
writeCRLF(checklistPath,JSON.stringify(data,null,2)+'\n');

const oldEng='Covered families now include the Stage-5 Chrome Hammer Archmage vertical boomerang and committed spiked-ball launch,';
const newEng='Covered families now include the Stage-5 Chrome Hammer Archmage vertical boomerang, committed spiked-ball launch and fused mega-wave corridor,';
replaceOne('docs/REQUEST_CHECKLIST_0914.md',oldEng,newEng);
replaceOne('docs/REQUEST_CHECKLIST_0914.md','Just verified: Stage-5 Chrome Hammer Archmage committed spiked-ball launch and camera-stable first bounce [Proof](ARCHMAGE_SPIKED_BALL_WARNING_0916.md).','Just verified: Stage-5 Chrome Hammer Archmage Easy/Normal core recovery and fused mega-wave warning [Proof](ARCHMAGE_CORE_RECOVERY_0916.md).');
replaceOne('docs/WORK_ORDER_0914.md',oldEng,newEng);

appendOnce('docs/SHARED_NONLASER_WARNING_0915.md','## Stage 5 Archmage fused mega-wave follow-up',`## Stage 5 Archmage fused mega-wave follow-up

The restored Easy/Normal post-chaingun form now previews the complete fused mega-wave damage corridor through the shared green/yellow/red system for 1.65 seconds. The beam remains harmless until red completes. The same batch repairs the missing \`core_orbit\` controller with authored blue core effects and prevents destroyed module targets from returning. Chromium passes 22/22 and focused section 358 passes 10/10. See [ARCHMAGE_CORE_RECOVERY_0916.md](ARCHMAGE_CORE_RECOVERY_0916.md).`);

appendOnce('HANDOFF_CODEX.md','## Codex update — 2026-09-16: Stage-5 Archmage core recovery',`## Codex update — 2026-09-16: Stage-5 Archmage core recovery

- Easy/Normal no longer freezes after the Archmage chaingun breaks. A 2.15-second authored blue core conversion returns the boss to its anchor and releases into the dual-Uzi/mega-wave loop.
- Both obsolete module targets retire at the final break, so invisible hammer hits cannot resurrect the destroyed chaingun phase. The fused mega-wave now shows the shared green/yellow/red corridor for its exact damage width before release.
- Focused section 358 passes 10/10; Chromium passes 22/22 with zero errors; full suite reaches 4,530 passes and the established 56 failures plus the intermittent Stage-1 sand-tank fixture. Evidence: docs/ARCHMAGE_CORE_RECOVERY_0916.md. Tally remains 128 complete / 7 partial / 16 pending.`);

appendOnce('CLAUDE.md','## 2026-09-16 Stage-5 Archmage core recovery',`## 2026-09-16 Stage-5 Archmage core recovery

The Chrome Hammer Archmage's Easy/Normal post-chaingun route no longer stalls in the previously unimplemented \`core_orbit\` state. It now runs a finite authored blue core convergence into the existing dual-Uzi/mega-wave loop, retires both old module targets, and gives the fused mega-wave a 1.65-second shared green/yellow/red corridor before damage. Hard/Furious retain their red enrage branch. Focused section 358 passes 10/10; Chromium passes 22/22 with zero errors; full suite reaches 4,530 passes and 57 failures, the established 56 plus the intermittent Stage-1 sand-tank fixture. See docs/ARCHMAGE_CORE_RECOVERY_0916.md.`);

console.log('CLOSED_ARCHMAGE_CORE_RECOVERY_0916');
