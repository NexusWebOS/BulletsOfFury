"""Assert the current four-form symbiote plates instead of retired mbv reel swaps."""
from pathlib import Path

p=Path('_BUILD_SOURCE/test_fl.js');b=p.read_bytes();assert b'\r\n' in b
def one(a,z):
 global b
 a,z=a.encode(),z.encode();assert b.count(a)==1,(a[:80],b.count(a));b=b.replace(a,z)
one("vileAnimKey(boss)==='mbv_f1_idle_0'", "vileAnimKey(boss)==='s8symboss_form_0'")
one("'far from firing -> idle reel'", "'form one keeps its authored possessed plate while idle'")
one("if(vm.runInContext(\"vileAnimKey(boss)\", ctxv)!=='mbv_f1_idle_'+f) _cyc=false;",
    "if(vm.runInContext(\"vileAnimKey(boss)\", ctxv)!=='s8symboss_form_0') _cyc=false;")
one("'idle reel cycles all 6 frames at 8fps'", "'the possessed silhouette stays stable through the old reel timestamps'")
one("(vileAnimKey(boss)||'').indexOf('_atk_')>0", "vileAnimKey(boss)==='s8symboss_form_0'")
one("'inside the tell window -> attack-charge reel'", "'the charge tell keeps form one intact for anchored effects'")
one("vileAnimKey(boss)==='mbv_f4_atk_5'||vileAnimKey(boss)==='mbv_f1_atk_5'",
    "vileAnimKey(boss)==='s8symboss_form_0'")
one("'tell reaches its final frame just before the shot'", "'the committed release keeps the same physical hull plate'")
one("vileAnimKey(boss)==='mbv_f4_idle_0'", "vileAnimKey(boss)==='s8symboss_form_3'")
one("'morphing to FURIOUS DEATH repoints the reel to form 4'", "'the final morph selects the authored alien form-four plate'")
one("boss.parts.length===5 && boss.name==='FURIOUS DEATH'", "boss.parts.length===5 && boss.name==='THE VILE EXISTENCE'")
one("'form 4 keeps its 5 modular parts'", "'the final alien form keeps its five independently damaged modules'")
p.write_bytes(b)
