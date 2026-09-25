"""Check the current fire/ice/alien encounter casts rather than retired exact rosters."""
from pathlib import Path

p=Path('_BUILD_SOURCE/test_fl.js');b=p.read_bytes()
assert b'\r\n' in b
def one(a,z):
 global b
 a,z=a.encode(),z.encode()
 assert b.count(a)==1,(a[:90],b.count(a))
 b=b.replace(a,z)

one('buildStagePlan.toString().indexOf(\\"all twelve unique volcanic hulls\\")>0',
    'buildStagePlan.toString().indexOf(\\"type:\'cinderwasp\'\\")>0&&buildStagePlan.toString().indexOf(\\"type:\'basaltbomber\'\\")>0')
one('stage-2 roster rebuilt around all twelve unique volcanic hulls',
    'stage-2 plan includes the new cinder-wasp and basalt fire jets')
one("['s3mine','s3interceptor','s3sled','s3snowmobile','s3crawler','s3tank','s3barge','s3artillery'].every(function(k){\r\n       return _s3.indexOf(\"'\"+k+\"'\")>0;\r\n     }), 'all eight native ice-field hulls have explicit Stage-3 rows'",
    "['s3mine','s3interceptor','sharddart','glaciercarrier','cryoeye'].every(function(k){\r\n       return _s3.indexOf(\"type:'\"+k+\"'\")>0;\r\n     }), 'Stage 3 schedules its ice jets, support craft and new shard-mine drone'")
one('Object.keys(S8MEGA).length===12 && buildStagePlan.toString().indexOf',
    'Object.keys(S8MEGA).length>=12 && buildStagePlan.toString().indexOf')
one('stage-8 roster includes the native twelve-hull mega fleet',
    'stage-8 roster includes every native mega hull and its expanded fleet')
one("ok(_sv8.length===12, 'all 12 native mega enemies appeared in the finale ('+_sv8.length+'/12)');",
    "ok(_sv8.length===_fleet8.length, 'all '+_fleet8.length+' native mega enemies appeared in the finale ('+_sv8.length+'/'+_fleet8.length+')');")
one("fleet:['ash','skim','eye','lance','disc','cruc','carrier','miner','lavamaw','crawl','pod','golem'].every(function(k){return _s2plan266.indexOf(\"spawnEnemy('"+"\"+k+\"'\")>=0;})",
    "fleet:['ash','skim','cinderwasp','magmaorb','basaltbomber','eye','lance','disc','cruc','carrier','miner','lavamaw','crawl','pod','golem'].every(function(k){return _s2plan266.indexOf(\"type:'"+"\"+k+\"'\")>=0;})")
one('Stage 2 fields all 12 unique volcanic hulls and none of the rejected art aliases',
    'Stage 2 fields its fifteen volcanic and new fire-jet types without rejected aliases')
one("ok(_p3.s3===10, 'stage 3 fields eight ice waves and two ground turrets ('+_p3.s3+' waves)');",
    "ok(_p3.s3===12, 'stage 3 fields eight ice waves, two new drone waves and two ground turrets ('+_p3.s3+' waves)');")
one("ok(_fleet267.every(function(k){return _s3plan267.indexOf(\"spawnEnemy('"+"\"+k+\"'\")>=0;}),\r\n     'Stage 3 schedules every one of its eight native ice-field hulls');",
    "ok(['s3mine','s3interceptor','sharddart','glaciercarrier','cryoeye'].every(function(k){return _s3plan267.indexOf(\"type:'"+"\"+k+\"'\")>=0;}),\r\n     'Stage 3 schedules both ice jet plates, support craft and the new ice drone');")
p.write_bytes(b)
