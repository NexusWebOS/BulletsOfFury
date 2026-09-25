"""Align old assertions with explicit later design changes, preserving CRLF."""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'_BUILD_SOURCE/test_fl.js'
b=p.read_bytes()
def sub(a,c):
    global b
    x=a.encode();assert b.count(x)==1,(a,b.count(x))
    b=b.replace(x,c.encode(),1)
sub("ok(vm.runInContext(\"drawUnitShadow.toString().indexOf('ctx.ellipse')<0\", ctxv), 'the drop-shadow ellipse is gone');",
    "ok(vm.runInContext(\"drawUnitShadow.toString().indexOf('if(!e || !e._bodShadow) return')>0\", ctxv), 'the shadow remains editor opt-in only');")
sub("ok(vm.runInContext(\"drawUnitShadow.toString().indexOf('intentionally does nothing')>0\", ctxv), 'kept as a no-op so its call sites stay harmless');",
    "ok(vm.runInContext(\"drawUnitShadow.toString().indexOf('ctx.ellipse')>0\", ctxv), 'the editor opt-in still draws the tunable ellipse');")
sub("ok(_D.furious.startLives === 1, 'FURIOUS starts with 1 life');",
    "ok(_D.furious.startLives === 3 && _D.insanity.startLives === 1, 'FURIOUS starts with 3 lives; INSANITY is the one-life mode');")
sub("ok(_D.furious.contLives === 1, 'and its one continue returns exactly 1 life, not a full stock');",
    "ok(_D.furious.contLives === 3 && _D.insanity.continues === 0, 'FURIOUS restores 3 lives once; INSANITY has no continue');")
sub("ok(_fzk.length === 45 && _fzMissing.length === 0, 'all 45 Furnace plates are registered and on disk (' + _fzMissing.join(',') + ')');",
    "ok(_fzk.length >= 45 && _fzMissing.length === 0 && vm.runInContext(\"!!BOFX.img.fzt_eye_beam_0 && !!BOFX.img.fzt_fire_laser_0920\", ctxv),\r\n"
    "     'the Furnace plates plus eye-laser expansion are registered and on disk (' + _fzMissing.join(',') + ')');")
assert b.count(b'\n')==b.count(b'\r\n')
p.write_bytes(b)
print('Updated shadow, Insanity/Furious, and expanded Furnace art assertions')
