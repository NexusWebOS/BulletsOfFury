"""Warm current authored Stage 3 and Stage 8 boss art before their first cinematic frame."""
from pathlib import Path

path = Path('assets/game.js')
source = path.read_bytes()
assert b'\r\n' not in source
old = b"  if(n===7){add('s7sluice_vent');add('s7sluice_warning');}\n"
new = old + (b"  // The Furious Stage-3 replacements and four current VILE forms live outside\n"
             b"  // the older ship-boss art namespaces. Decode them during stage entry.\n"
             b"  if(n===3)addPrefix('s3thermo_');\n"
             b"  if(n===8)addPrefix('vile24_');\n")
assert source.count(old) == 1
path.write_bytes(source.replace(old, new))
