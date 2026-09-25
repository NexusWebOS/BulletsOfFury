"""Differentiate Hard/Furious Furnace cannon pressure without shortening its tell."""
from pathlib import Path

path = Path('assets/game.js')
data = path.read_bytes()
assert b'\r\n' not in data
old = b"""function furnaceCannon(b,t,period,lockPose){
  const F=b._fz; if(F.pools.right<=0) return;
  const cycle=t%period, beat=Math.floor(t/period), m0=furnaceMount(b,'right');"""
new = b"""function furnaceCannon(b,t,period,lockPose){
  const F=b._fz; if(F.pools.right<=0) return;
  /* Hard and Furious close the recovery between charged shots. The visible 1.05s
     aiming/charge tell stays intact on every difficulty before each release. */
  period*=diffKey==='insanity'?.75:diffKey==='furious'?.82:diffKey==='hard'?.92:1;
  const cycle=t%period, beat=Math.floor(t/period), m0=furnaceMount(b,'right');"""
assert data.count(old) == 1
path.write_bytes(data.replace(old, new))
