"""Update four stale suite expectations for approved new encounter content.

Retain CRLF and every unrelated test. These assertions still check concrete
wave counts and distinct ammunition; they no longer reject the new turrets or
the requested toxic center laser.
"""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'_BUILD_SOURCE/test_fl.js'
b=p.read_bytes()
def sub(a,c):
    global b
    x=a.encode();assert b.count(x)==1,(a,b.count(x))
    b=b.replace(x,c.encode(),1)
sub("STAGES[0].length===82 && buildStagePlan(1).length===19",
    "STAGES[0].length===82 && buildStagePlan(1).length===21 && buildStagePlan(1).filter(function(w){return w.fn._modGroundTurret;}).length===2")
sub("stage 1: the 19 map beats reach the dam arena at the 82-second boss trigger",
    "stage 1: 19 map beats and 2 grounded turret beats reach the dam at 82 seconds")
sub("ok(_p3.s3===17, 'stage 3 fields its complete authored native plan ('+_p3.s3+' waves)');",
    "ok(_p3.s3===10, 'stage 3 fields eight ice waves and two ground turrets ('+_p3.s3+' waves)');")
sub("ok(_p3.s1===19, 'stage 1 uses the 19 authored map beats rather than filler density ('+_p3.s1+')');",
    "ok(_p3.s1===21, 'stage 1 uses 19 authored map beats and two ground turrets ('+_p3.s1+')');")
sub("_shots270.skimmer.k.every(function(k){return k==='s7acid';})",
    "_shots270.skimmer.k.some(function(k){return k==='s7acid';})&&\r\n"
    "     _shots270.skimmer.k.some(function(k){return k==='s7laser';})&&\r\n"
    "     _shots270.skimmer.k.every(function(k){return k==='s7acid'||k==='s7laser';})")
sub("tank stitch and skimmer wake complete the remaining identities",
    "tank shards and skimmer acid/laser salvo keep distinct toxic roles")
assert b.count(b'\n')==b.count(b'\r\n')
p.write_bytes(b)
print('Updated CRLF-preserved assertions for wave additions and toxic jet')
