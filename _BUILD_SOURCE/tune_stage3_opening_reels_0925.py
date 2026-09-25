"""Shorten Stage 3's first laser reels while preserving each full warning."""
from pathlib import Path

path = Path('assets/game.js')
data = path.read_bytes()
assert b'\r\n' not in data

edits = [
    (
        b"""    /* Five locked laser lanes walk across the arena while the wings add two compact shard beats.
       The boss itself slides slowly in the opposite direction, so every warning remains readable. */
    S.cannonSeq={t:0,i:0,next:0,count:5,finishCharge:false,
      slots:(step&1)?['L','C','R','C','L']:['R','C','L','C','R'],warm:.24,active:.34,retract:.14,width:26};""",
        b"""    /* Three locked lanes teach both wings and the core. Each keeps the full three-second FOV
       warning; a five-beam reel kept the next attack hidden for nearly twenty seconds. */
    S.cannonSeq={t:0,i:0,next:0,count:3,finishCharge:false,
      slots:(step&1)?['L','C','R']:['R','C','L'],warm:.24,active:.34,retract:.14,width:26};""",
    ),
    (
        b"""    /* Seven individually timed siege lanes traverse with the Wall. The opening teaches the
       left/right rhythm, then raised batteries and core join before the giant reactor orb. */
    S.cannonSeq={t:0,i:0,next:0,count:7,finishCharge:true,
      slots:(step&1)?['L','R','TL','TR','L','R','C']:['R','L','TR','TL','R','L','C'],warm:.30,active:.50,retract:.18,width:46};
    /* Seven full beam cycles plus the reactor release need a clean recovery beat.  Keeping the
       director locked out for the whole 8.35s prevents the next phase from being queued while
       the final cannon is still retracting. */
    stage3BossBeginSlide(b,7.35);b.fireCd=8.35*cdMul;""",
        b"""    /* One beam from each wing, then the core. The engine gives each lane the full three-second
       FOV warning, so seven sequential lanes delayed the orb and every later pattern too long. */
    S.cannonSeq={t:0,i:0,next:0,count:3,finishCharge:true,
      slots:(step&1)?['L','R','C']:['R','L','C'],warm:.30,active:.50,retract:.18,width:46};
    /* The busy-action gate below owns the exact reel lifetime, including the final orb charge. */
    stage3BossBeginSlide(b,4.35);b.fireCd=5.35*cdMul;""",
    ),
]
for old, new in edits:
    assert data.count(old) == 1, old[:80]
    data = data.replace(old, new)
path.write_bytes(data)
