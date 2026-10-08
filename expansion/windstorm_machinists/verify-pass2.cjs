const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const ROOT=__dirname,read=f=>JSON.parse(fs.readFileSync(path.join(ROOT,f),'utf8').replace(/^\uFEFF/,''));
const M=read('manifest.json'),Q=read('verification.json'),G=read('passes-2-generation.json');
const sources=new Set(G.jobs.map(j=>'source/'+j.name+'.png'));
const frames=Object.entries(M.frames).filter(([id,f])=>sources.has(f.source));
const sequences=Object.entries(M.sequences).filter(([id,s])=>/_(crouch_walk|prone_fire|run_west)/.test(id)||id.startsWith('enemy_'));
assert.equal(G.jobs.length,12);assert.equal(sequences.length,66);
for(const j of G.jobs)assert.ok(fs.existsSync(path.join(ROOT,'source/'+j.name+'.png')));
const checks=Q.frameChecks.filter(f=>frames.some(([id])=>id===f.id));
assert.ok(checks.every(c=>c.nonzeroAlphaPixels>0&&c.borderAlphaPixels===0),'New sprite/UI export has empty alpha or edge clipping');
const details=[];for(const [id,s]of sequences){const distinct=new Set(s.frames.map(f=>M.frames[f]?.sha256));assert.ok(!distinct.has(undefined),'Missing frame '+id);assert.equal(distinct.size,s.frames.length,'Duplicate animation phase '+id);assert.equal(s.frames.length,/^phoenix_crouch_walk_(east|south)$/.test(id)?5:6);details.push({id,frames:s.frames.length,distinctHashes:distinct.size});}
assert.ok(Q.machinistsUi.every(p=>p.frameAlphaUnchanged));
Q.pass2={date:'2026-10-07',sourceMasters:12,newSourceExports:frames.length,newSequences:sequences.length,allNewExportsNonempty:true,allNewExportsClearBorders:true,allNewSequencePhasesDistinct:true,portraitFrameAlphaUnchanged:true,sequenceChecks:details,visualReview:['Three generated contact sheets inspected at output size','North enemy correction shows helmet backs and rear spine panels','Phoenix east/south crouch phase with wrong facing excluded','Machinist approved faces retained in exact canonical frame'],limitations:['Generated pose/scale drift and roots need final pixel cleanup','Some crouch phases read as low walking','Enemy south patrol carries weapon up; aimed south fire still needs separate art','Not an eight-direction production set; gameplay remains unimplemented']};
fs.writeFileSync(path.join(ROOT,'verification.json'),JSON.stringify(Q,null,2)+'\n');console.log(JSON.stringify({totals:Q.totals,pass2:{masters:12,sourceExports:frames.length,sequences:sequences.length,nonempty:true,clearBorders:true,distinctPhases:true,canonicalPortraitAlpha:true}},null,2));
