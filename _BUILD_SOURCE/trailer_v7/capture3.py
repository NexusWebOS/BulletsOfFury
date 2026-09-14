"""capture3.py - the v3 trailer library: frame-perfect 60 fps takes WITH the game's own sound log.

    python capture3.py --list                          # the take plan, and takes per pilot
    python capture3.py S1_cole C_flame A_mapfly        # a subset
    python capture3.py --all --workers 4 --missing     # everything not yet recorded

Mike, on v2: "The trailer was supposed to be all one trailer, and have the sounds in there. Be more
thorough with showcasing instead of doing it 3x with the same pilot throughout different spots in the
trailer."

Everything capture.py learned still holds (fresh page per take, synthetic clock, real input map, the
debug fight route, playerHit stubbed rather than invuln pinned, dlgBox stubbed on action takes). Two
things are new:

1. THE SOUND LOG. v2 recorded pictures only - the page ran with --mute-audio and nothing listened, so
   the cut had the song and forty generic explosion accents and none of the game. Every take now logs,
   stamped with the frame counter on the synthetic clock:
     snd    each Snd.play() that actually PLAYED (it returns false when the TAME retrigger gate refuses,
            and that gate reads performance.now(), which is pinned to the same clock - so the log holds
            exactly what a player hears, gated the way a player hears it)
     loops  every held bed's level per frame (Snd.loops[n].lvl * want) - the flamethrower, the laser,
            every charge - plus the frames a bed restarts from zero
     syn    each call to a SYNTH-only Audio.SFX cue (the keys BOFA.sfx does not replace), with its args;
            nested calls are not logged twice
     warp   warpAmbienceStart/Level/Stop, the procedural warp bed
   render_audio.py turns that log into takes/<id>/sfx.wav, frame-aligned to s00000.jpg.
2. A LIBRARY BUILT SO NO SHOT HAS TO REPEAT. v2 had 58 takes under 158 clips, so B_lizzie was on screen
   nine times and B_maverick seven. v3 has every special from two angles (S1, S2), every weapon on its
   own pilot (C, C2), every miniboss and boss fought by two different pilots (D, D2, E, E2), the six
   stages on six new pilots, the new campaign map and the stage-5 warp drive. --list prints takes per
   pilot; the plan keeps every pilot within one take of the others.
"""
import os, sys, json, time, base64, shutil, argparse, subprocess, functools, threading, http.server

ROOT = r'C:\Users\Mdogg\Desktop\BOF-CODE\BulletsOfFury'
HERE = os.path.dirname(os.path.abspath(__file__))
TAKES_DIR = os.path.join(HERE, 'takes3')
MIN_FREE_GB = 4.0

LIB = r"""() => {
  window.requestAnimationFrame = function(cb){ window.__pend = cb; return 0; };
  window.__now = performance.now();
  performance.now = function(){ return window.__now; };
  try { storyPlay = function(){ return false; }; } catch (e) {}
  try { story = null; } catch (e) {}
  window.__realHit = playerHit;
  playerHit = function(){};
  window.__mode = 'none'; window.__fire = false; window.__i = 0; window.__hx = null; window.__hy = null;
  window.__tgt = function(){
    if (typeof subBoss !== 'undefined' && subBoss && !subBoss.dead) return subBoss;
    if (typeof boss !== 'undefined' && boss && !boss.dead) return boss;
    return null;
  };

  /* ---- THE SOUND LOG ---- */
  window.__alog = {snd: [], syn: [], warp: [], loops: {}, restarts: []};
  (function(){
    const L = window.__alog;
    if (typeof Snd !== 'undefined' && Snd) {
      const _play = Snd.play;
      Snd.play = function(name, vol){
        const ok = _play.call(this, name, vol);
        if (ok) L.snd.push([window.__i, name, (vol == null ? 1 : vol)]);
        return ok;
      };
      const _on = Snd.loopOn;
      Snd.loopOn = function(name, vol){
        const pre = Snd.loops[name];
        if (!pre || !pre.on) L.restarts.push([window.__i, name]);
        return _on.call(this, name, vol);
      };
    }
    let depth = 0;
    const bofa = (window.BOFA && BOFA.sfx) || {};
    const SKIP = {expSmall: 1, expBig: 1, expBoss: 1, expIce: 1};
    const wrap = function(obj, k, bucket){
      const fn = obj[k];
      obj[k] = function(){
        if (depth === 0) bucket.push([window.__i, k, Array.prototype.slice.call(arguments)]);
        depth++;
        try { return fn.apply(this, arguments); } finally { depth--; }
      };
    };
    if (typeof Audio !== 'undefined' && Audio && Audio.SFX) {
      for (const k of Object.keys(Audio.SFX)) {
        if ((k in bofa) || SKIP[k] || typeof Audio.SFX[k] !== 'function') continue;
        wrap(Audio.SFX, k, L.syn);
      }
      for (const k of ['warpAmbienceStart', 'warpAmbienceLevel', 'warpAmbienceStop'])
        if (typeof Audio[k] === 'function') wrap(Audio, k, L.warp);
    }
  })();
  window.__loopSample = function(){
    if (typeof Snd === 'undefined' || !Snd || !Snd.loops) return;
    for (const n in Snd.loops) {
      const Lp = Snd.loops[n];
      if (Lp.lvl > 0) (window.__alog.loops[n] = window.__alog.loops[n] || []).push([window.__i, +(Lp.lvl * Lp.want).toFixed(4)]);
    }
  };
  window.__audioDump = function(){
    const L = window.__alog, names = {};
    for (const e of L.snd) names[e[1]] = 1;
    for (const n in L.loops) names[n] = 1;
    const files = {};
    for (const n in names) files[n] = (window.BOFA && BOFA.sfx && typeof BOFA.sfx[n] === 'string') ? BOFA.sfx[n] : null;
    return {snd: L.snd, syn: L.syn, warp: L.warp, loops: L.loops, restarts: L.restarts, files: files,
            tame: (typeof Snd !== 'undefined' && Snd) ? Snd.TAME : {}, vol: (typeof Snd !== 'undefined' && Snd) ? Snd.vol : {},
            voice: (typeof Snd !== 'undefined' && Snd) ? Snd.VOICE_SET : {}};
  };

  const MOVE = ['a', 'd', 'w', 's'];
  window.__auto = function(i){
    const K = Input.keys, m = window.__mode;
    const play = (typeof player !== 'undefined') && state === GS.PLAY;
    if (!play || m === 'none') { for (const k of MOVE) K[k] = false; K.j = play && !!window.__fire; return; }
    player.dead = false;
    if (player.invuln > 0) player.invuln = 0;
    const t = i / 60, ww = worldWidth();
    let tx = player.x, ty = player.y;
    if (m === 'weave') {
      tx = ww / 2 + Math.sin(t * 0.9) * Math.min(150, ww * 0.24);
      ty = PLAY.y + PLAY.h * 0.76 + Math.sin(t * 1.7) * 28;
    } else if (m === 'boss') {
      const T = window.__tgt();
      tx = (T && isFinite(T.x)) ? T.x + Math.sin(t * 1.1) * 46 : ww / 2 + Math.sin(t * 0.8) * 90;
      ty = PLAY.y + PLAY.h * 0.80 + Math.sin(t * 1.5) * 16;
    } else if (m === 'hold') {
      tx = (window.__hx == null) ? player.x : window.__hx;
      ty = (window.__hy == null) ? player.y : window.__hy;
    } else if (m === 'gates') {
      /* the warp run: hold the next gate's line; the pass test, the drive and the jump are the game's */
      let g = null;
      if (typeof s5run !== 'undefined' && s5run && !s5run.done && s5run.gates)
        for (const q of s5run.gates) { if (!q.passed && !q.missed) { g = q; break; } }
      tx = g ? g.x : ww / 2;
      ty = PLAY.y + PLAY.h * 0.72;
    }
    const dx = tx - player.x, dy = ty - player.y, dz = (m === 'gates') ? 3 : 5;
    K.a = dx < -dz; K.d = dx > dz; K.w = dy < -dz; K.s = dy > dz;
    K.j = !!window.__fire;
  };
  window.__step = function(n){
    for (let k = 0; k < n; k++) {
      window.__i++;
      try { window.__auto(window.__i); } catch (e) { window.__err = 'auto ' + String(e).slice(0, 140); }
      window.__now += 1000 / 60;
      try { loop(window.__now); } catch (e) { window.__err = 'loop ' + String(e).slice(0, 140); }
      try { window.__loopSample(); } catch (e) {}
    }
  };
  window.__metrics = function(){
    const T = window.__tgt();
    const cam = (typeof camX !== 'undefined') ? camX : 0;
    return {e: enemies.length, eb: eBullets.length, pb: pBullets.length, pa: particles.length, ex: explosions.length,
            sb: !!subBossActive, bo: !!bossActive, bd: !!bossDefeated,
            th: T ? Math.round(T.hp || 0) : null, tn: T ? (T.name || T.kind || null) : null,
            tsx: (T && isFinite(T.x)) ? Math.round((T.x - cam) * 2) : null, ty: (T && isFinite(T.y)) ? Math.round(T.y) : null,
            sp: (special && special.t > 0) ? special.pilot : null,
            ch: (special && special.charge) ? +special.charge.toFixed(2) : 0,
            st: state, px: Math.round(player.x), py: Math.round(player.y), cx: Math.round(cam),
            ro: !!player.roll, so: !!player.somer, dd: !!player.dead,
            fi: !!Input.keys.j, sh: +(shake || 0).toFixed(2), fl: +(flashScreen || 0).toFixed(2),
            gi: (typeof s5run !== 'undefined' && s5run) ? s5run.idx : null,
            wp: (typeof s9warp !== 'undefined' && s9warp) ? s9warp.ph : null,
            fz: (typeof boss !== 'undefined' && boss && boss._fz) ? boss._fz.phase : null,
            gm: (typeof gravityMode !== 'undefined' && gravityMode) ? gravityMode.phase : null,
            tl: (typeof subBoss !== 'undefined' && subBoss && subBoss._tlv) ? [subBoss._tlv.phase || null, subBoss._tlv.state || null] : null,
            lb: (typeof boss !== 'undefined' && boss && boss._l23Beam) ? [boss._l23Beam.family, +(boss._l23Beam.t / Math.max(0.001, boss._l23Beam.warm)).toFixed(2), !!boss._l23Beam.released] : null,
            err: window.__err || null};
  };
  window.__fight = function(stage, role, pilot){
    const e = debugFightFor(stage, role);
    if (!e) return {ok: false, why: 'no debug fight for ' + stage + '/' + role};
    const ok = debugStartFight(e, {pilot: pilot});
    try { floaters.length = 0; story = null; } catch (_) {}
    return {ok: ok, name: e.name, kind: e.kind, pilot: _pilotKey(), state: state};
  };
  window.__run = function(stage, pilot){
    const i = PILOTS.findIndex(p => p.key === pilot); if (i >= 0) pilotIndex = i;
    try { debugRecStop(); } catch (_) {}
    debugFight = null; run.mode = 'arcade'; diffKey = diffKey || 'normal';
    try { _coleScene = 0; } catch (_) {}
    run._l78Entry = 0; run._s5ResumeArm = 0; coopOn = false; PENDING_STAGE = 1;
    startRun(stage);
    try { floaters.length = 0; story = null; } catch (_) {}
    return {ok: true, state: state, pilot: _pilotKey(), stage: run.stage};
  };
  window.__arm = function(w, lv, wvar){
    for (let k = 0; k < lv; k++) applyPowerup({kind: 'weapon', wtype: w, wvar: wvar || null, x: player.x, y: player.y});
    try { floaters.length = 0; } catch (_) {}
    return {weapon: run.weapon, wlevel: run.wlevel, missiles: run.missileLevel, wvar: (run.wvars || {})[w] || null};
  };
  window.__kill = function(){
    if (typeof subBoss !== 'undefined' && subBoss && !subBoss.dead) {
      try { subBoss.hp = Math.min(subBoss.hp, 1); hitSubBoss(999999, subBoss.x, subBoss.y); }
      catch (e) { window.__err = 'kill sub ' + String(e).slice(0, 100); }
      if (subBoss && !subBoss.dead) { subBoss.hp = 0; subBoss.dead = true; subBoss.dying = 0; return 'sub-forced'; }
      return 'sub';
    }
    if (typeof boss !== 'undefined' && boss && bossActive && !boss.dead) { boss.hp = 0; bossDie(); return 'boss'; }
    return null;
  };
  window.__grabN = function(n, hud, q){
    const s = document.querySelector('#screen'), h = document.querySelector('#hud');
    const out = {s: [], h: [], m: []};
    for (let k = 0; k < n; k++) {
      window.__step(1);
      out.s.push(s.toDataURL('image/jpeg', q));
      if (hud) out.h.push(h.toDataURL('image/png'));
      out.m.push(window.__metrics());
    }
    return out;
  };
  return true;
}"""

TAKES = {}


def take(tid, kind, **kw):
    d = dict(kind=kind, warm=0, rec=300, hud=False, mode='none', fire=False, events={}, arm=None, pre=None,
             until=None, quiet=True)
    d.update(kw)
    TAKES[tid] = d


def menu(tid, setup, warm, rec, events=None):
    take(tid, 'menu', setup=setup, warm=warm, rec=rec, events=events or {}, quiet=False)


def fight(tid, stage_n, role, pilot, warm, rec, events=None, **kw):
    kw.setdefault('mode', 'boss')
    kw.setdefault('fire', True)
    take(tid, 'fight', stage=stage_n, role=role, pilot=pilot, warm=warm, rec=rec, events=events or {}, **kw)


def stage(tid, stage_n, pilot, warm, rec, events=None, **kw):
    kw.setdefault('mode', 'weave')
    kw.setdefault('fire', True)
    take(tid, 'stage', stage=stage_n, pilot=pilot, warm=warm, rec=rec, events=events or {}, **kw)


TAP = "Input.injectTap('enter');"
SPECIAL = "startSpecial();"
LOCK = "Input.injectTap('c');"          # retina key -> cycleLock(): the seeker flies to a target
LAUNCH = "Input.injectTap('k');"        # missile key -> retinaFire() / lizzieFire() / useBomb()
KILL = "window.__kill(); window.__fire = false;"
# THE RAZORBACK DRIVES IN AT ~0.7 px/frame and is not fully on screen until ~540 frames into its fight - measured on
# the first D_s1: y 33 at the scripted kill, and 300 frames of the pilot firing at empty jungle before it. Every
# other miniboss is in by ~170. So stage 1's miniboss takes wait for the tank instead of trusting a warm.
RZB_EDGE = "subBossActive && subBoss && subBoss.y >= 20"
RZB_IN = "subBossActive && subBoss && subBoss.y >= 90"
UP, DOWN = "window.__fire = false;", "window.__fire = true;"


def strikes(at, gap=78, lead=28, n=3):
    """lock, then launch `lead` frames later once the seeker has landed - n times"""
    ev = {}
    for k in range(n):
        ev[at + k * gap] = LOCK
        ev[at + k * gap + lead] = LAUNCH
    return ev


def held(at, n=3, hold=130, gap=10):
    """charge pilots: a FRESH press after the special starts, released and re-pressed n times"""
    ev = {at - 5: UP, at: SPECIAL, at + gap: DOWN}
    t = at + gap
    for k in range(n):
        t += hold
        ev[t] = UP
        if k < n - 1:
            ev[t + gap] = DOWN
    return ev


def tap(k):
    return "Input.injectTap('%s');" % k


# ---- A: the front end, the campaign map v2 and its button bar ---------------------------------------
menu('A_boot', "setState(GS.BOOT); drawBoot._started = true; drawBoot._ct = 0; drawBoot._chimed = true;", 0, 390)
menu('A_walk', "setState(GS.TITLE); menuIndex = 0;", 0, 1500,
     events={150: TAP, 250: tap('w'), 330: TAP, 480: TAP, 630: TAP, 780: TAP})
menu('A_title', "setState(GS.TITLE); menuIndex = 0;", 60, 300)
menu('A_camphub', "campHubIndex = 0; campPick = null; setState(GS.CAMPHUB);", 45, 150)
CAMP = ("run.mode = 'campaign'; campaign.bonusUnlocked = 0; campaign.unlockedMax = 8; "
        "campaign.rank = {1: 'S', 2: 'A', 3: 'B', 4: 'S', 5: 'A', 6: 'B', 7: 'A'}; ")
menu('A_mapboot', CAMP + "pilotIndex = PILOTS.findIndex(p => p.key === 'yuri'); openStageSelect(1, {boot: true});", 0, 720)
menu('A_mapfly', CAMP + "pilotIndex = PILOTS.findIndex(p => p.key === 'lizzie'); cmap2.bar = 0; openStageSelect(1, {});", 60, 1140,
     events={120: tap('d'), 195: tap('d'), 270: tap('d'), 345: tap('a'), 420: tap('a'), 495: tap('a'), 570: tap('a'),
             660: tap('w'), 720: tap('d'), 770: tap('d'), 830: tap('j'), 930: tap('k'), 975: tap('a'), 1025: tap('j'),
             1110: tap('k'), 1160: tap('s')})
menu('A_pilots', "setState(GS.PILOT); pilotIndex = 0;", 40, 700,
     events={60 + 72 * k: tap('d') for k in range(1, 9)})

# ---- S1 / S2: every special, from two angles, against a live target ----------------------------------
fight('S1_axel', 2, 'mini', 'axel', 330, 420, events={340: SPECIAL})
fight('S1_decker', 3, 'boss', 'decker', 390, 420, events={400: SPECIAL})
fight('S1_maverick', 2, 'boss', 'maverick', 390, 480, events=held(400))
fight('S1_freezer', 5, 'mini', 'freezer', 330, 480, arm=(5, 5, 'fireice'), events={340: SPECIAL})
fight('S1_juggernaut', 3, 'mini', 'juggernaut', 330, 420, events={340: SPECIAL})
stage('S1_yuri', 4, 'yuri', 480, 420, until="state === GS.PLAY", events={490: SPECIAL})
fight('S1_lizzie', 4, 'boss', 'lizzie', 390, 480, events={400: SPECIAL, **strikes(412, gap=90)})
fight('S1_falva', 2, 'mini', 'falva', 560, 420, events={335: UP, 340: SPECIAL, 350: DOWN, 655: UP})   # v4: no stage-6 bosses (Mike)
fight('S1_cole', 1, 'boss', 'cole', 390, 480, events={400: SPECIAL, **strikes(412)})

fight('S2_axel', 1, 'boss', 'axel', 390, 420, events={400: SPECIAL})
fight('S2_decker', 1, 'mini', 'decker', 330, 420, events={340: SPECIAL})   # kept as recorded: the tank is in view from ~f110 of 420
fight('S2_maverick', 4, 'mini', 'maverick', 330, 480, events=held(340))
fight('S2_freezer', 3, 'boss', 'freezer', 390, 480, arm=(5, 5, 'fireice'), events={400: SPECIAL})
fight('S2_juggernaut', 5, 'boss', 'juggernaut', 390, 420, events={400: SPECIAL})
fight('S2_yuri', 3, 'mini', 'yuri', 330, 420, events={340: SPECIAL})
fight('S2_lizzie', 1, 'mini', 'lizzie', 330, 480, events={340: SPECIAL, **strikes(352, gap=90)})   # kept as recorded: the bombs read with the tank at the top edge
fight('S2_falva', 2, 'boss', 'falva', 560, 420, events={395: UP, 400: SPECIAL, 410: DOWN, 715: UP})
fight('S2_cole', 5, 'mini', 'cole', 330, 480, events={340: SPECIAL, **strikes(352)})
# JUGGERNAUT'S CHARGE DASH, for the v4 abilities showcase. chargeTick winds up while CHARGE and UP are both HELD and
# rams on release, and only while his special is live. 'hold' mode steering at __hy far above the ship is what holds
# UP every frame (MOVE keys belong to the autopilot); h is not a MOVE key, so an event can hold it.
CHARGE_ON = "window.__mode = 'hold'; window.__hx = null; window.__hy = -9999; Input.keys.h = true;"
CHARGE_GO = "Input.keys.h = false; window.__mode = 'boss';"
fight('J_charge', 4, 'boss', 'juggernaut', 390, 540, events={400: SPECIAL, 430: CHARGE_ON, 512: CHARGE_GO,
                                                            600: CHARGE_ON, 682: CHARGE_GO, 770: CHARGE_ON, 850: CHARGE_GO})

# ---- C / C2: the arsenal at max level, every weapon on its own pilot ----------------------------------
# weapon-exclusive pilots stay on their own weapons: ice breath / thermoshock are Freezer's, the incendiary
# shotgun Decker's, the heavy MG mount Lizzie's, the sonic boom Cole's.
fight('C_mg', 4, 'boss', 'falva', 390, 300, arm=(0, 5, None))
fight('C_spread', 1, 'mini', 'juggernaut', 330, 300, arm=(1, 5, None))   # kept as recorded: the tank is in view from ~f80 of 300
# v6: stage 5 swapped the ground loadout for the space weapons, so this take showed LASER CANNON + VOLLEY MISSILES. On a
# ground stage: the homing missiles, plus Decker's own retina lock + missile strikes (c then k, with bombs to spend).
fight('C_missiles', 4, 'boss', 'decker', 390, 360, arm=(2, 5, None),
      events={0: "window.__arm(3, 5, null); run.bombs = 12;", **strikes(400, gap=80, lead=30, n=4)})
fight('C_laser', 4, 'mini', 'lizzie', 330, 300, arm=(3, 5, None))
fight('C_flame', 3, 'mini', 'axel', 330, 300, arm=(4, 5, 'flamethrower'))
fight('C_icebreath', 2, 'boss', 'freezer', 390, 300, arm=(4, 5, 'icebreath'))
fight('C_fireorb', 2, 'mini', 'cole', 330, 300, arm=(5, 5, 'fireorb'))
fight('C_iceorb', 3, 'boss', 'yuri', 390, 300, arm=(5, 5, 'iceorb'))
# v6: every stage-2 frame fell inside the Furnace Tyrant's assembly and hit nothing - ice takes the thermoshock at 2x
fight('C_thermo', 3, 'mini', 'freezer', 330, 300, arm=(5, 5, 'fireice'), hud=True)
# v6 (Mike: "Laser mist is actually laser cannon"): slot 6 on stage 5 IS the space LASER CANNON. The real LASER MIST is
# the ground slot-6 weapon, so it is filmed on a ground stage and the cannon gets its own take in space.
fight('C_lasermist', 3, 'mini', 'maverick', 330, 300, arm=(6, 5, None), hud=True)
fight('C_lasercannon', 5, 'mini', 'axel', 330, 300, arm=(6, 5, None), hud=True)   # v7: not maverick twice in a row after LASER MIST
# SHADOW ORB - the space primary 1, a CHARGE weapon (release under 0.42s cancels, full at 1.55s): three 100-frame holds
fight('C_shadoworb', 5, 'mini', 'juggernaut', 330, 420, arm=(1, 4, None), fire=False, hud=True,
      events={340: DOWN, 440: UP, 470: DOWN, 570: UP, 600: DOWN, 700: UP})
# RETINAS + MISSILES: the Razorback's Razor Rack - ten launches queued on ONE retina - forced twice, the second broken by a roll
RACK = ("const R = subBoss && subBoss._rzb; if (!R || R.state === 'arrival') return 'arriving';"
        " R.idx = 2; R.attack = 'missiles'; R.at = 0; R.beat = -1; R.trans = 0; return 'rack';")
fight('L_rack', 1, 'mini', 'yuri', 60, 480, until=RZB_IN, arm=(0, 4, None),
      events={60: RACK, 330: RACK, 430: "startRoll(1);"})
# THE FURNACE TYRANT forming, attacking and through every phase - on the REAL damage path (hitBoss with the impact point
# set, which routes shield -> furnaceHit -> part pools -> boss hp; furnaceHit alone never moves the boss). Frames count
# from the fight start: spawn ~143, the assembly descends/chains/latches/surges to ~695 (ARMS).
FZT = r"""window.__fzt = function(part, frac){
  const b = boss, F = b && b._fz, H = b && b._mwBarrier;
  if (!F || b.dead) return 'no rig';
  if (F.phase === 'intro' || F.trans > 0) return 'wait ' + F.phase;
  _dmgBullet = null;
  if (part === 'shield') { if (!H || !H.active) return 'down'; _lastHitX = b.x; _lastHitY = b.y; hitBoss(H.hp); return 'shield broke'; }
  if (H && H.active) return 'shield up';
  const q = furnaceBoxes(b).find(c => c.key === part); if (!q) return 'no ' + part;
  _lastHitX = q.x; _lastHitY = q.y;
  hitBoss(Math.max(1, Math.ceil(F.pools[part] * (frac == null ? 1 : frac))));
  return part + ' ' + F.pools[part] + ' ' + F.phase;
};"""
_Z = lambda a: "return window.__fzt(%s);" % a
FZ = {0: UP, 700: DOWN, 1100: _Z("'shield'"), 1160: _Z("'left',0.6"), 1250: _Z("'right',0.6"),
      1500: _Z("'left'"), 1620: _Z("'right'"),
      2030: _Z("'shield'"), 2100: _Z("'body',0.55"), 2760: _Z("'body'"),
      3250: _Z("'head',0.6"), 3620: _Z("'head'")}
# four pilots, not one - the Furnace sequence is four bars and lizzie alone would top the balance by eight seconds
# THE TEMPEST LEVIATHAN (Mike, on v6: "Showcase the new level 6 mini boss dual ship fight a little bit") - the one stage-6
# unit allowed in the trailer. Real damage path: a round at the hull through hitSubBoss, which the rig clamps at its gate,
# so each call lands the jet exactly on its next phase: chase -> overtake (it crosses the player) -> pursuit rams -> hell.
TLV = r"""window.__tlvGate = function(frac){
  const b = subBoss, T = b && b._tlv;
  if (!T || b.dead) return 'no rig';
  _dmgBullet = null;
  const need = b.hp - b.maxhp * frac;
  if (need <= 0) return 'already ' + (b.hp / b.maxhp).toFixed(2);
  hitSubBoss(Math.ceil(need) + 1, b.x, b.y);
  return T.phase + ' ' + (b.hp / b.maxhp).toFixed(2);
};"""
fight('T_tempest', 6, 'mini', 'cole', 330, 900, pre=TLV, hud=True,
      events={600: "return window.__tlvGate(0.74);", 1000: "return window.__tlvGate(0.49);"})
for _tid, _p, _warm, _rec in [('E3_s2_form', 'yuri', 120, 600), ('E3_s2_arms', 'maverick', 690, 1000),
                              ('E3_s2_core', 'axel', 1720, 1060), ('E3_s2_head', 'lizzie', 2850, 900)]:
    fight(_tid, 2, 'boss', _p, _warm, _rec, pre=FZT, events=FZ, hud=True)
fight('C_shotgun', 2, 'boss', 'decker', 390, 300, events={380: "dkGrant();"})
fight('C_turret', 3, 'mini', 'lizzie', 330, 300, events={320: "lzMountGrant();"})
# v5: FULL charges on a dark stage (Mike: "Make coles sonic boom an actual charged one"). Each hold is 82 frames
# against SONIC_MAX's 69, and all four releases land inside the recording.
# v6: off the space stage (Mike: "Coles sonic boom should not be in space") - the stage-4 desert boss, where a green wave reads
fight('C_sonic', 4, 'boss', 'cole', 390, 360,
      events={380: "sonicGrant();", 386: UP, 392: DOWN, 474: UP, 484: DOWN, 566: UP, 576: DOWN, 658: UP, 668: DOWN, 740: UP})
fight('C2_mg', 3, 'boss', 'maverick', 390, 300, arm=(0, 5, None))
fight('C2_spread', 5, 'boss', 'yuri', 390, 300, arm=(1, 5, None))
fight('C2_missiles', 4, 'mini', 'axel', 330, 300, arm=(2, 5, None), events={0: "window.__arm(3, 5, null);"})

# ---- D / D2: every miniboss, by two different pilots - warning, entrance, attacks, the kill -----------
for n, p, w in zip(range(1, 7), ['axel', 'yuri', 'falva', 'cole', 'decker', 'lizzie'], [1, 3, 1, 5, 4, 3]):
    fight('D_s%d' % n, n, 'mini', p, 0, 660, arm=(w, 4, None), events={450: KILL}, until=RZB_EDGE if n == 1 else None)
for n, p, w in zip(range(1, 7), ['maverick', 'juggernaut', 'cole', 'freezer', 'falva', 'yuri'], [0, 5, 3, 1, 3, 4]):
    fight('D2_s%d' % n, n, 'mini', p, 120, 540, arm=(w, 4, None), events={120 + 420: KILL}, until=RZB_IN if n == 1 else None)

# ---- E / E2: every boss, by two different pilots - warning, entrance, patterns, the death set-piece ----
for n, p, w in zip(range(1, 7), ['lizzie', 'axel', 'maverick', 'juggernaut', 'yuri', 'falva'], [3, 1, 5, 4, 3, 0]):
    fight('E_s%d' % n, n, 'boss', p, 0, 900, arm=(w, 4, None), hud=True, events={450: KILL})
for n, p, w in zip(range(1, 7), ['freezer', 'decker', 'cole', 'axel', 'maverick', 'juggernaut'], [4, 1, 0, 5, 1, 3]):
    fight('E2_s%d' % n, n, 'boss', p, 240, 720, arm=(w, 4, None), events={240 + 480: KILL})

# ---- F: the six stages on six new pilots (stage cards + launch, then gameplay with rolls and a somersault)
# warm frames come from survey.py's flights; 900 recorded frames leave the edit room to find the busy part
# whichever pilot's weapon ends the miniboss sooner or later than the survey pilot's did.
F_PLAN = {1: ('falva', 0, 1260), 2: ('juggernaut', 3, 4020), 3: ('decker', 4, 3540),
          4: ('lizzie', 5, 2040), 5: ('axel', 1, 720), 6: ('maverick', 0, 600)}   # v4: at 6000 the Doomsday Carrier filled every frame
for n, (p, w, warm) in F_PLAN.items():
    stage('F_s%d' % n, n, p, warm, 900, until="state === GS.PLAY", arm=(w, 4, None), hud=True,
          events={warm + 100: "startRoll(1);", warm + 300: "startRoll(-1);", warm + 520: "startSomersault();"})
FI_PLAN = {1: 'yuri', 2: 'cole', 3: 'axel', 4: 'freezer', 5: 'juggernaut', 6: 'lizzie', 7: 'maverick', 8: 'decker'}   # v6: all eight cards (Mike)
for n, p in FI_PLAN.items():
    stage('F_intro_s%d' % n, n, p, 0, 480, fire=False)

# ---- X: the stage-5 SPACESHIP TRANSFORMATION, live (Mike, on v6: "Show the spaceship transformation scene and make it
# properly fixed and working in-game") - drift, charge, scatter, snap, pixel glow, the white, the reveal, 3-2-1, GO. The
# 0913a probe put charge at ~496, snap ~792, reveal ~917 and GO ~1200 frames from the stage start.
stage('X_launch5', 5, 'falva', 600, 720, fire=False, mode='none')   # v7 balance: yuri ran 18.9s, falva 12.8s

# ---- W: the stage-5 warp drive - all eight gates, the jump, the white --------------------------------
stage('W_warp', 5, 'freezer', 90, 1560, until="state === GS.PLAY", mode='gates',
      pre="s5RunInit(); try { if (typeof powerups !== 'undefined') powerups.length = 0; } catch (e) {}")

# ---- G: the death spin-out (Mike's header rule), the real playerHit restored ---------------------------
DIE = ("window.__mode = 'none'; window.__fire = false; run.shield = 0; if (special) endSpecial(); "
       "player.invuln = 0; playerHit = window.__realHit; playerHit();")
stage('G_death', 4, 'decker', 300, 420, until="state === GS.PLAY", events={390: DIE})
fight('G_death2', 2, 'boss', 'falva', 390, 420, events={400: DIE})


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve():
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(_Quiet, directory=ROOT))
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd.server_address[1], httpd.shutdown


def run_take(browser, port, tid, spec, quality):
    free = shutil.disk_usage(HERE).free / 1e9
    if free < MIN_FREE_GB:
        raise RuntimeError('only %.1f GB free - refusing to record' % free)
    d = os.path.join(TAKES_DIR, tid)
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
    errs, notes = [], []
    t0 = time.time()
    page = browser.new_page(viewport={'width': 1280, 'height': 960})
    page.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:180]))
    page.on('console', lambda m: errs.append(m.text[:180]) if m.type == 'error' else None)
    page.goto('http://127.0.0.1:%d/index.html?quality=high' % port)
    page.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=90000)
    page.evaluate(LIB)
    page.evaluate("() => { ASSETS.ready = true; }")
    if spec.get('quiet'):
        page.evaluate("() => { dlgBox = function(){}; }")

    def js(body):
        return page.evaluate("() => { try { %s } catch (e) { return 'ERR ' + String(e).slice(0, 200); } }" % body)

    if spec['kind'] == 'menu':
        notes.append('setup -> %s' % js(spec['setup'] + ' return state;'))
    elif spec['kind'] == 'fight':
        notes.append('setup ' + json.dumps(page.evaluate("([s, r, p]) => window.__fight(s, r, p)", [spec['stage'], spec['role'], spec['pilot']])))
    else:
        notes.append('setup ' + json.dumps(page.evaluate("([s, p]) => window.__run(s, p)", [spec['stage'], spec['pilot']])))
    if spec.get('until'):
        n = 0
        while n < 3600 and js('return !!(%s);' % spec['until']) is not True:
            page.evaluate("(n) => window.__step(n)", 20)
            n += 20
            page.wait_for_timeout(50)
        notes.append('until after %d frames (state %s)' % (n, js('return state;')))
    if spec.get('pre'):
        notes.append('pre -> %s' % js(spec['pre'] + ' return null;'))
    if spec.get('arm'):
        w, lv, wv = spec['arm']
        notes.append('arm ' + json.dumps(page.evaluate("([w, l, v]) => window.__arm(w, l, v)", [w, lv, wv])))
    page.evaluate("([m, f]) => { window.__mode = m; window.__fire = f; }", [spec['mode'], spec['fire']])

    events = {int(k): v for k, v in spec['events'].items()}
    total = spec['warm'] + spec['rec']
    f, idx, metrics = 0, 0, []
    rec0 = None

    def next_event(after):
        later = [k for k in events if k > after]
        return min(later) if later else 10 ** 9

    while f < total:
        if f in events:
            r = js(events[f] + ' return null;')
            notes.append('@%d %s -> %s' % (f, events[f][:48], r))
        if f < spec['warm']:
            n = min(20, spec['warm'] - f, next_event(f) - f)
            page.evaluate("(n) => window.__step(n)", n)
            f += n
            page.wait_for_timeout(60)
        else:
            if rec0 is None:
                rec0 = page.evaluate("() => window.__i + 1")      # the frame counter of s00000.jpg
            n = min(6, total - f, next_event(f) - f)
            out = page.evaluate("([n, h, q]) => window.__grabN(n, h, q)", [n, spec['hud'], quality])
            for k in range(n):
                with open(os.path.join(d, 's%05d.jpg' % idx), 'wb') as fh:
                    fh.write(base64.b64decode(out['s'][k].split(',', 1)[1]))
                if spec['hud']:
                    with open(os.path.join(d, 'h%05d.png' % idx), 'wb') as fh:
                        fh.write(base64.b64decode(out['h'][k].split(',', 1)[1]))
                metrics.append(out['m'][k])
                idx += 1
            f += n
            if idx % 60 == 0:
                page.wait_for_timeout(30)
    audio = page.evaluate("() => window.__audioDump()")
    audio['rec0'] = rec0
    audio['frames'] = idx
    page.close()
    dt = time.time() - t0
    json.dump(metrics, open(os.path.join(d, 'metrics.json'), 'w'))
    json.dump(audio, open(os.path.join(d, 'audio_events.json'), 'w'))
    peak = {k: max((m.get(k) or 0) for m in metrics) for k in ('e', 'eb', 'pb', 'pa', 'ex')} if metrics else {}
    mb = sum(os.path.getsize(os.path.join(d, x)) for x in os.listdir(d)) / 1e6
    in_rec = lambda i: rec0 is not None and i >= rec0
    meta = dict(id=tid, spec=spec, frames=idx, seconds=round(dt, 1), mb=round(mb, 1), notes=notes, rec0=rec0,
                page_errors=errs[:10], step_errors=sorted({m['err'] for m in metrics if m.get('err')})[:6],
                peak=peak, targets=sorted({m['tn'] for m in metrics if m.get('tn')}),
                specials=sorted({m['sp'] for m in metrics if m.get('sp')}),
                states=sorted({m['st'] for m in metrics}),
                sound=dict(snd=sum(1 for e in audio['snd'] if in_rec(e[0])), syn=sum(1 for e in audio['syn'] if in_rec(e[0])),
                           loops=sorted(audio['loops']), warp=len(audio['warp'])),
                event_idx={str(k - spec['warm']): v for k, v in sorted(events.items())})
    json.dump(meta, open(os.path.join(d, 'meta.json'), 'w'), indent=1)
    contact(d, idx, tid)
    return meta


def contact(d, n, tid):
    from PIL import Image, ImageDraw
    if n == 0:
        return
    picks = [int(i * (n - 1) / 15) for i in range(16)]
    T = 200
    th = int(T * 1024 / 960)
    S = Image.new('RGB', (T * 8, (th + 16) * 2), (14, 14, 18))
    dr = ImageDraw.Draw(S)
    for j, i in enumerate(picks):
        im = Image.open(os.path.join(d, 's%05d.jpg' % i)).convert('RGB').resize((T, th), Image.LANCZOS)
        x, y = (j % 8) * T, (j // 8) * (th + 16)
        S.paste(im, (x, y + 16))
        dr.text((x + 3, y + 2), '%s f%d' % (tid, i), fill=(255, 220, 140))
    S.save(os.path.join(d, 'contact.jpg'), quality=88)


def worker(ids, quality):
    from playwright.sync_api import sync_playwright
    port, stop = serve()
    args = ['--autoplay-policy=no-user-gesture-required', '--disable-background-timer-throttling',
            '--disable-renderer-backgrounding', '--mute-audio']
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=args)
        for tid in ids:
            try:
                m = run_take(browser, port, tid, TAKES[tid], quality)
                print('%-14s %4d fr %6.1fs %6.1fMB peak %s tgt %s sp %s sound %s err %d/%d | %s' % (
                    tid, m['frames'], m['seconds'], m['mb'], m['peak'], m['targets'], m['specials'], m['sound'],
                    len(m['page_errors']), len(m['step_errors']), ' | '.join(m['notes'])[:300]), flush=True)
            except Exception as e:
                print('%-14s FAILED: %s' % (tid, str(e)[:300]), flush=True)
                try:
                    browser.close()
                except Exception:
                    pass
                browser = pw.chromium.launch(args=args)
        browser.close()
    stop()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ids', nargs='*')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--missing', action='store_true', help='skip takes that already have a meta.json')
    ap.add_argument('--workers', type=int, default=1)
    ap.add_argument('--quality', type=float, default=0.90)
    a = ap.parse_args()
    if a.list:
        tot, per = 0, {}
        for tid, s in TAKES.items():
            tot += s['rec']
            if s.get('pilot'):
                per.setdefault(s['pilot'], []).append(tid)
            print('%-14s %-6s warm %4d rec %4d  %s' % (tid, s['kind'], s['warm'], s['rec'],
                  {k: v for k, v in s.items() if k in ('stage', 'role', 'pilot', 'arm')}))
        print('%d takes, %d recorded frames (%.1f min of footage, ~%.1f GB)' % (len(TAKES), tot, tot / 3600.0, tot * 0.35 / 1000))
        for p in sorted(per):
            print('  %-11s %2d  %s' % (p, len(per[p]), ' '.join(per[p])))
        return
    ids = list(TAKES) if a.all else a.ids
    bad = [i for i in ids if i not in TAKES]
    if bad:
        sys.exit('unknown takes: %s' % bad)
    if a.missing:
        ids = [i for i in ids if not os.path.exists(os.path.join(TAKES_DIR, i, 'meta.json'))]
    os.makedirs(TAKES_DIR, exist_ok=True)
    if a.workers <= 1 or len(ids) <= 1:
        worker(ids, a.quality)
        return
    order = sorted(ids, key=lambda i: -(TAKES[i]['rec'] + TAKES[i]['warm'] * 0.15))
    shards = [order[k::a.workers] for k in range(a.workers)]
    procs = [subprocess.Popen([sys.executable, os.path.abspath(__file__)] + s + ['--quality', str(a.quality)],
                              cwd=HERE, env=dict(os.environ, PYTHONIOENCODING='utf-8')) for s in shards if s]
    for p in procs:
        p.wait()


if __name__ == '__main__':
    main()
