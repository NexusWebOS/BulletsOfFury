"""Update expectations explicitly superseded by Mike's October 11 recording.
Byte replacements preserve each existing test file's line endings.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
patches={
 '_BUILD_SOURCE/test_part2_1010.cjs':[("includes('p2-rockets')&&er26Book({_ship:'stormsovereign'}).includes('p2-core-laser')","includes('p2-rockets')&&er26Book({_ship:'stormsovereign'}).includes('ap10-stormburst')")],
 '_BUILD_SOURCE/test_fl.js':[("run('assets/game.js', 'game');","run('assets/game.js', 'game');\r\nrun('assets/playthrough_ui_1011.js', 'playthrough_ui');"),
 ("ok(save302.can&&save302.loaded,'Continue restores the completed-stage checkpoint after the session is lost');","ok(!save302.can&&!save302.loaded,'Continue requires the current session; saved checkpoints remain in Load');"),
 ("require('./test_element_arsenal_1011.cjs')(vm,ctxv,ok);","require('./test_element_arsenal_1011.cjs')(vm,ctxv,ok);\r\nrequire('./test_playthrough_1011.cjs')(vm,ctxv,ok);")],
 '_BUILD_SOURCE/test_polish_0927b.cjs':[("out['laser pickups equip and upgrade beams instead of lances']=run._mavBeamUnlocked&&heldVariant(3)==='laserbeam'&&run.wlevel===2&&pBullets.some(q=>q.kind==='beam');","out['laser pickups preserve fixed lances and store separate beam levels']=run._mavBeamUnlocked&&heldVariant(3)==='mavhoming'&&run.wlevels[3]===2&&pBullets.length===3&&pBullets.every(q=>q.kind==='mavlaser'&&q.lv===1);")],
 '_BUILD_SOURCE/test_feedback_1002.cjs':[("o['Furious rain has three groups of nine']=groundTargetingFx.length===27&&[0,1,2].every(z=>groundTargetingFx.filter(q=>q._meteor1002.zone===z).length===9);","o['Furious rain has three separated groups of six']=groundTargetingFx.length===18&&[0,1,2].every(z=>groundTargetingFx.filter(q=>q._meteor1002.zone===z).length===6&&groundTargetingFx.filter(q=>q._meteor1002.zone===z).every(q=>q.warn>=1.8));")],
 '_BUILD_SOURCE/test_hammer_chromium_1011.cjs':[("half-screen beams and anchored jump counter","half-screen beams and anchored slide counter"),
 ("crossing above halfway starts a committed jump","crossing above halfway starts a committed side slide"),
 ("airborne boss shrinks and cannot make body contact']=Math.abs(C.scale-.30)<1e-8","sliding boss stays full-size and cannot make unwarned body contact']=C.scale>=1&&C.scale<=1.1"),
 ("full locked warning and dive remain harmless","full locked warning and slide remain harmless"),
 ("Leaving the warned anchor avoids the full jump and side strike","Leaving the warned anchor avoids the full slide and side strike"),
 ("Hammer depletion queues the break through the jump","Hammer depletion queues the break through the side slide")]
}
for name,pairs in patches.items():
 p=ROOT/name;b=p.read_bytes()
 for old,new in pairs:
  old=old.encode();new=new.encode()
  if new in b:continue
  assert b.count(old)==1,(name,old,b.count(old));b=b.replace(old,new)
 p.write_bytes(b)
print('Updated only superseded expectations; line endings retained.')
