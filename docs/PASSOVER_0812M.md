0812m: the lava reavers fly, and the ship bosses charge, cross and ram

THE LAVA REAVERS FLY, THEY DO NOT BOB
Mike: "you have those lava boats. they need to appear and act like jets or remove them."
They were spawned on `sine` - a slow wobble straight down the middle, which on a volcano stage
reads as a boat drifting on lava. Kept rather than removed, because the art is the stage's own
authored elite; the movement was what was wrong. They enter from the sides now on the jet routes
the stage-1 deltas use, which gives them the bank, the missile dodge and the lane-hold in jetTick
for free. Measured: the unit keeps its own art and 57x68 footprint and simply changes tick.

SHIP BOSSES MANOEUVRE INSTEAD OF DRIFTING
Mike: "I wanna see our jet mini bosses and bosses charge at us, and then do in-game off screen on
screen x pattern strikes where we have to avoid them, then they try to do a vertical south,
vertical north, vertical south aggresively like they are trying to ram into us. Try to not just
think Shmup, but Mega Man and other amazin arcade classics too."

What was there: b.x = worldWidth()/2 + sin(drift*0.9)*96. One sine, forever, for every ship boss
and miniboss in the game.

THE ARCADE PART IS THE TELL, NOT THE SPEED. A Mega Man boss is readable: it stops, it announces,
THEN it commits, and the window to react opens during the announcement. So every manoeuvre is
preceded by a 0.5s TELL - the hull halts, flashes and drags backwards - and only then moves fast.
Without that a 430px/s dive is not an attack, it is a collision.

  HOLD     the old drift, shortened as its health falls
  TELL     halt + flash + recoil, so the commitment is legible
  CHARGE   dives at where you ARE, overshoots past the bottom, climbs back
  XSTRIKE  leaves the field and re-enters corner-to-corner, twice, drawing an X across it
  RAM      south, north, south - three passes, each re-aimed at your column as it starts

The fight escalates because the POOL is phase-weighted, measured over 70s per unit:
  phase 0   hold 22s  charge 8s  ram 14s              no crossing yet
  phase 1   hold 14s  charge 3s  XSTRIKE 22s  ram 10s  off-screen time triples to 6.1s
  phase 2   hold  8s                                   holds collapse, aggression dominates

Off-screen legs are deliberate and bounded: a 7-second watchdog forces RECOVER, because the
failure mode here is not "too hard", it is a fight that stalls with the boss parked out of view.
And nothing runs while `enter` is set, or a boss would dive while still flying in.

FOUR ARCADE ATTACKS: chargebeam, beamfan, mslfan, mslhome
The charge beam locks your column ONCE at the start of a 0.62s wind-up and never tracks after -
a beam that follows you is unavoidable, and unavoidable is not difficulty. It draws a brightening
column down the locked lane so the wind-up means something. The spread laser is deliberately dense
because a "laser" of sparse rounds reads as a machine gun. Seven of the nine ship units field at
least one of the four.

A PHASE IS ONE PATTERN, WHICH NEARLY RUINED THE CHARGE BEAM. shipBossPhase maps an HP band to a
single entry in pats[], so once the Void Bat entered its chargebeam band that was its ONLY attack:
measured 55.7 seconds of telegraph in 70, a permanent red column down the screen. It arms every
third volley now and fires an ordinary aimed pair in between - 18.4s of 70, an event again.

Also fixed while measuring: a probe that pinned bosses at full HP reported the X-strike and the
charge beam as missing. Both are phase-gated; a unit at 100% health only ever shows phase 0.

Suite 2,585 / 231 / 5 - the same five long-standing failures.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
