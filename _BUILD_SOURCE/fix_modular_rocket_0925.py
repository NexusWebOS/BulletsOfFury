from pathlib import Path

p = Path(__file__).resolve().parents[1] / "assets/game.js"
b = p.read_bytes()
for before, after in (
    (b"w==='mg'?'mg':w==='missile'?'s4missile':", b"w==='mg'?'mg':w==='missile'?'s4rocket':"),
    (b"fire(p,a+side*.10,2.15,'s4missile'", b"fire(p,a+side*.10,2.15,'s4rocket'"),
):
    assert b.count(before) == 1, (before, b.count(before))
    b = b.replace(before, after, 1)
assert b"\r\n" not in b
p.write_bytes(b)
