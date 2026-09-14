"""Final feedback refinements discovered by native combat audio recording."""
import json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def refine(s):
    def rep(a,b,n=1):
        nonlocal s
        assert s.count(a)>=n,a[:80];s=s.replace(a,b,n)
    rep("            hitBoss(_bd);\n            explode(b.x,b.y,b.kind==='fire'?9:6,b.kind==='fire'?'red':'blue');", "            hitBoss(_bd);\n            if(b.kind==='sonic')sonicImpact(b.x,b.y,b._p);\n            else explode(b.x,b.y,b.kind==='fire'?9:6,b.kind==='fire'?'red':'blue');")
    rep("if(_sd>0){hitSubBoss(_sd, b.x, b.y);explode(b.x,b.y,6,'red');}", "if(_sd>0){hitSubBoss(_sd, b.x, b.y);if(b.kind==='sonic')sonicImpact(b.x,b.y,b._p);else explode(b.x,b.y,6,'red');}")
    rep('const WB_DRAW=17;         // ⚠ drawn a little under the hit radius: six 37px balls read as a wall', 'const WB_DRAW=17;         // 0913: readable steel silhouettes match the unchanged 17px contact radius')
    rep("// 0912z: the ram-boost sample, not Cole's boom", '// 0913: Juggernaut owns the launch cue')
    rep('    if(Math.abs(subBoss.x-b.x)<(sw+b.w)/2&&Math.abs(sy-b.y)<(sh+b.h)/2&&laserMistLedgerHit(b,subBoss)){',
        '    const inBox=Math.abs(subBoss.x-b.x)<(sw+b.w)/2&&Math.abs(sy-b.y)<(sh+b.h)/2;\n    const solid=inBox&&typeof subBossSolidAt===\'function\'?subBossSolidAt(b.x,b.y):null;\n    if(inBox&&solid!==false&&laserMistLedgerHit(b,subBoss)){')
    rep('function sonicFrontGeometry(b){',"function juggernautRamImpact(x,y){\n  weaponFeedbackBurst('ram',x,y,74,.24);\n  weaponFeedbackSound('juggernautRamImpact',.85);\n}\nfunction sonicFrontGeometry(b){")
    rep("hitEnemy(e,999); explode(e.x,e.y,26,'red'); shake=Math.max(shake,7); Audio.SFX.expSmall();", "hitEnemy(e,999); juggernautRamImpact(e.x,e.y); shake=Math.max(shake,7);")
    rep("player._ramT=0.2; explode(player.x,player.y-10,20,'red'); shake=Math.max(shake,6);", "player._ramT=0.2; juggernautRamImpact(player.x,player.y-10); shake=Math.max(shake,6);",2)
    rep("    juggernautRamStop:'", "    juggernautRamImpact:'assets/game/sounds/juggernaut_wreck_hit_0913.wav',\n    juggernautRamStop:'")
    rep('    juggernautRamStop:{', '    juggernautRamImpact:{g:.70,lp:5200,min:.18},\n    juggernautRamStop:{')
    rep("'juggernautRamStop','juggernautChains'", "'juggernautRamStop','juggernautRamImpact','juggernautChains'")
    return s
if __name__=='__main__':
    p=ROOT/'assets/game.js';s=p.read_text(encoding='utf-8')
    if 'function juggernautRamImpact('not in s:p.write_bytes(refine(s).encode('utf-8'))
    (HERE/'runtime-sha256.txt').write_text(hashlib.sha256(p.read_bytes()).hexdigest())
    print('Ram contact now owns one authored impact cue; duplicate generic blasts removed')
