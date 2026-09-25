"""Put the new ice-drone art on Stage 3's authored shard-mine AI."""
from pathlib import Path

p=Path('assets/game.js')
b=p.read_bytes()
assert b'\r\n' not in b
old=b"    /* Large centre circle / miniboss gate: deliberately clear for its warning and entrance. */"
new=(b"    /* The newly authored ice drone uses the native shard-mine's three-slot radial\n"
     b"       escape gate. Keep it isolated from the numbered interceptor files. */\n"
     b"    add(20.4,()=>encounterRipple([{type:'s3mine',fx:.50}],.36));\n\n"
     +old)
assert b.count(old)==1
b=b.replace(old,new)
old=b"    add(40.0,()=> encounterRipple([\n      {type:'sharddart',fx:.18,ai:{kind:'diag',slowY:VH*.20}},"
new=(b"    /* A second drone owns the far-bank approach; Furious fields a separated partner. */\n"
     b"    add(36.5,()=>encounterRipple(diffKey==='furious'?\n"
     b"      [{type:'s3mine',fx:.28},{type:'s3mine',fx:.72}]:\n"
     b"      [{type:'s3mine',fx:.68}],.42));\n"
     +old)
assert b.count(old)==1
b=b.replace(old,new)
p.write_bytes(b)
