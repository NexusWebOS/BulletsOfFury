"""Announce Freezer's Stage 2 Ice Breath alongside Fire Orb and Thermoshock."""
from pathlib import Path

p=Path('assets/game.js');b=p.read_bytes();assert b'\r\n' not in b
old=b"freezer:[['FIRE ORB','micon_fireorb_3'],['THERMOSHOCK BALL','micon_thermoshock_3']]"
new=b"freezer:[['FIRE ORB','micon_fireorb_3'],['ICE BREATH','micon_icebreath_3'],['THERMOSHOCK BALL','micon_thermoshock_3']]"
assert b.count(old)==1;p.write_bytes(b.replace(old,new))
