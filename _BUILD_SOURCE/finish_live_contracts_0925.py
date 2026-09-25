"""Exercise current furnace, naval and cinematic behavior in the headless suite."""
from pathlib import Path

path = Path('_BUILD_SOURCE/test_fl.js')
text = path.read_bytes().decode('utf-8').replace('\r\n', '\n')

def swap(old, new):
    global text
    assert text.count(old) == 1, (old[:100], text.count(old))
    text = text.replace(old, new)

swap("Object.keys(ENEMY_SHIELD_FAMILY).length===6 && Object.keys(ENEMY_SHIELD_LOADOUT).length>0",
     "Object.keys(ENEMY_SHIELD_FAMILY).filter(function(k){return k.indexOf('bubble_')===0;}).length===6 && Object.keys(ENEMY_SHIELD_LOADOUT).length>0")
swap("shipBossActionTick(b,tell*0.31);var after=eBullets.length,P=shipBossVisualPose(b),M=shipBossMount(b,'L');",
     "shipBossActionTick(b,tell*0.31);var fired=!!(b._sba&&b._sba.fired),action=b._mwAttack&&b._mwAttack.kind;magmaWardTick(b,0.60);var after=eBullets.length,P=shipBossVisualPose(b),M=shipBossMount(b,'L');")
swap("return JSON.stringify({q:q,before:before,early:early,after:after,slots:slots,kick:b._sbaKick,",
     "return JSON.stringify({q:q,before:before,early:early,after:after,fired:fired,action:action,slots:slots,kick:b._sbaKick,")
swap("  ok(_boss245.q && _boss245.before===0 && _boss245.early===0 && _boss245.after>0,",
     "  ok(_boss245.q && _boss245.before===0 && _boss245.early===0 && _boss245.fired &&\n     _boss245.action==='magmaflame' && _boss245.after>0,")
swap("  ok(_phase245.phase===2 && _phase245.t>0 && _phase245.step===0 && !_phase245.queued && _phase245.cd>=0.5,",
     "  ok(_phase245.phase>=2 && _phase245.t>0 && _phase245.step===0 && !_phase245.queued && _phase245.cd>=0.5,")
swap("run.stage=1;curStage=STAGES[0];player.x=240;player.y=430;eBullets.length=0;enemies.length=0;",
     "run.stage=1;curStage=STAGES[0];mapScroll=0;player.x=240;player.y=430;eBullets.length=0;enemies.length=0;")
swap("var mg=eBullets.filter(function(q){return q.kind==='mg';}),xs={};",
     "var mg=eBullets.filter(function(q){return q.kind==='s1bullet';}),xs={};")
swap("_motion246.indexOf(\"cinDrawShip(p,1\")>0",
     "_motion246.indexOf(\"cinDrawShip(p,7\")>0")

path.write_bytes(text.replace('\n', '\r\n').encode('utf-8'))
assert path.read_bytes().count(b'\r\n') == path.read_bytes().count(b'\n')
