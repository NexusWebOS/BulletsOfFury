# plan10.py - the v10 take plan (Gasline cut), exec'd into capture10.py's namespace.
# Every take is real play: the game's own playerHit is live (real9.py), the dodge autopilot flies, only GAME OVER is off.
PWSET = ("debugFight = null; coopOn = false; run.mode = 'arcade'; setState(GS.PASSWORD); pwInput = '%s'; submitPassword();"
         " pilotIndex = PILOTS.findIndex(p => p.key === '%s'); startRun(PENDING_STAGE);"
         " try { floaters.length = 0; story = null; } catch (_) {}")


def pwtake(tid, code, pilot, warm, rec, **kw):
    """an encounter reached through its own password (docs/PASSWORD_ENCOUNTERS_1005.md) - intros kept"""
    kw.setdefault('mode', 'boss'); kw.setdefault('fire', True); kw.setdefault('quiet', False)
    take(tid, 'menu', setup=PWSET % (code, pilot), warm=warm, rec=rec, pilot=pilot, **kw)


BURST = (36, 66)

# ---- A: the front end ----------------------------------------------------------------------------------------------
menu('A_title', "setState(GS.TITLE); menuIndex = 0;", 60, 240)
menu('A_pilots', "setState(GS.PILOT); pilotIndex = 0;", 40, 460, events={60 + 48 * k: tap('d') for k in range(1, 9)})
CAMP = ("run.mode = 'campaign'; campaign.bonusUnlocked = 0; campaign.unlockedMax = 8; campaign.rivalScattered = true;"
        " campaign.rivalDefeated = [false,false,false,false,false];"
        " campaign.rank = {1: 'S', 2: 'A', 3: 'B', 4: 'S', 5: 'A', 6: 'B', 7: 'A'}; ")
menu('C_mapfly', CAMP + "pilotIndex = PILOTS.findIndex(p => p.key === 'axel'); cmap2.bar = 0; openStageSelect(1, {});", 60, 600,
     events={120: tap('d'), 190: tap('d'), 260: tap('d'), 330: tap('d'), 400: tap('d'), 470: tap('d'), 540: tap('d')})

# ---- F / G: the stages - each card, then the stage itself mid-flight on its own pilot ------------------------------
FI_PLAN = {1: 'yuri', 2: 'cole', 3: 'axel', 4: 'freezer', 5: 'juggernaut', 6: 'lizzie', 7: 'maverick', 8: 'decker', 9: 'falva'}
for _n, _p in FI_PLAN.items():
    stage('F_card_s%d' % _n, _n, _p, 0, 130, fire=False, mode='none')
take('F_card_s8b', 'menu', setup="XART.rdy('scard_8'); setState(GS.TITLE);", warm=90, rec=130, quiet=True,
     events={90: "run.stage = 8; curStage = STAGES[7]; setState(GS.INTRO);"})
G_PLAN = [(1, 'lizzie', 1500), (2, 'juggernaut', 1500), (3, 'yuri', 1500), (4, 'maverick', 1500), (5, 'axel', 2700),
          (7, 'falva', 1500), (8, 'cole', 1500), (9, 'decker', 1500)]
for _n, _p, _w in G_PLAN:
    stage('G_s%d' % _n, _n, _p, _w, 300, diff='normal', arm=(1, 3, None))

# ---- P: the nine pilots on their specials --------------------------------------------------------------------------
stage('P_axel', 2, 'axel', 1400, 240, events={1410: SPECIAL}, diff='normal')
stage('P_decker', 4, 'decker', 1300, 240, events={1310: SPECIAL}, diff='normal')
fight('P_maverick', 3, 'mini', 'maverick', 330, 300, events=held(340), diff='normal')
stage('P_freezer', 3, 'freezer', 1500, 240, arm=(5, 5, 'fireice'), events={1510: SPECIAL}, diff='normal')
CHARGE_ON = "window.__mode = 'hold'; window.__hx = null; window.__hy = -9999; Input.keys.h = true;"
CHARGE_GO = "Input.keys.h = false; window.__mode = 'boss';"
fight('P_juggernaut', 4, 'boss', 'juggernaut', 390, 300, events={400: SPECIAL, 430: CHARGE_ON, 512: CHARGE_GO, 600: CHARGE_ON, 672: CHARGE_GO}, diff='normal')
fight('P_yuri', 2, 'mini', 'yuri', 330, 240, events={340: SPECIAL}, diff='normal')
fight('P_lizzie', 3, 'boss', 'lizzie', 390, 300, events={400: SPECIAL, **strikes(412, gap=90)}, diff='normal')
fight('P_falva', 4, 'mini', 'falva', 560, 240, events={335: UP, 340: SPECIAL, 350: DOWN, 655: UP}, diff='normal')
stage('P_cole', 1, 'cole', 1500, 300, events={1510: SPECIAL, **strikes(1522)}, diff='normal')

# ---- V: EASY/NORMAL vs HARD vs FURIOUS - where the game really changes ----------------------------------------------
for _d, _p, _w in [('normal', 'yuri', 0), ('hard', 'decker', 1), ('furious', 'freezer', 5)]:
    fight('V_rzb_' + _d, 1, 'mini', _p, 0, 420, until=RZB_IN, arm=(_w, 4, None), diff=_d, burst=BURST)
for _d, _p in [('normal', 'lizzie'), ('hard', 'axel')]:
    fight('V_frost_' + _d, 3, 'mini', _p, 200, 360, arm=(1, 4, None), diff=_d, burst=BURST)
fight('V_sov_furious', 4, 'boss', 'cole', 600, 1500, arm=(0, 5, None), diff='furious', burst=BURST)
fight('V_ovl_furious', 1, 'boss', 'axel', 520, 600, arm=(0, 5, None), diff='furious', burst=BURST,
      events={520: "if (boss && bossActive && boss.hp > boss.maxhp * 0.49) { _dmgBullet = null; boss.hp = boss.maxhp * 0.49; } return 1;"})

# ---- B: the boss montage (20 BOSSES) -------------------------------------------------------------------------------
fight('B_s1b', 1, 'boss', 'juggernaut', 0, 600, arm=(1, 4, None), diff='normal', burst=BURST)
B_PLAN = [('B_s2m', 2, 'mini', 'decker', 60, 330), ('B_s2b', 2, 'boss', 'freezer', 120, 700),
          ('B_s3b', 3, 'boss', 'falva', 240, 330), ('B_s4m', 4, 'mini', 'axel', 60, 330),
          ('B_s4b', 4, 'boss', 'lizzie', 240, 330), ('B_s5m', 5, 'mini', 'yuri', 60, 330),
          ('B_s5b', 5, 'boss', 'maverick', 1600, 600), ('B_s6m', 6, 'mini', 'freezer', 600, 360),
          ('B_s7m', 7, 'mini', 'cole', 60, 330), ('B_s7b', 7, 'boss', 'axel', 760, 600),
          ('B_s9m', 9, 'mini', 'juggernaut', 60, 330), ('B_s9b', 9, 'boss', 'falva', 240, 400)]
for _t, _n, _r, _p, _warm, _rec in B_PLAN:
    fight(_t, _n, _r, _p, _warm, _rec, arm=(1, 4, None), diff='hard' if _r == 'boss' and _n in (7,) else 'normal', burst=BURST)
pwtake('B_s8m', 'MINI8', 'decker', 200, 360, arm=(1, 4, None), burst=BURST)

# ---- M: MISSILE VOLLEY GALORE - Uber manual missiles on Retina locks, max homing racks ------------------------------
MSL = ("run.missileTier = 'uber'; run.bombs = 20; run.missileLevel = 5; "
       "try { for (const k of ['msl_uber','msl_ultra']) XART.rdy(k); } catch (e) {}")
_ev = {}
for k in range(14):
    _ev[400 + k * 18] = LOCK if k % 3 == 0 else LAUNCH
for k in range(14):
    _ev[420 + k * 18] = LAUNCH
fight('M_uber', 4, 'boss', 'decker', 390, 360, pre=MSL, events=_ev, diff='normal', arm=(1, 4, None), burst=BURST)
MSL2 = "run.missileTier = 'ultra'; run.bombs = 35; run.missileLevel = 5;"
_ev2 = {}
for k in range(18):
    _ev2[340 + k * 14] = LAUNCH
fight('M_rack', 2, 'mini', 'maverick', 330, 330, pre=MSL2, events=_ev2, diff='normal', arm=(2, 5, None), burst=BURST)
fight('M_cole', 5, 'boss', 'cole', 1700, 360, events={1710: SPECIAL, **strikes(1722, gap=40, lead=20, n=5)}, diff='normal')

# ---- Z: THE FINALE - the drone, the ghost, Dracodia in the void and his eight stolen forms ---------------------------
pwtake('Z_drone', 'FINAL1', 'falva', 0, 900, burst=BURST)
pwtake('Z_ghost', 'FINAL2', 'decker', 0, 700, burst=BURST)
pwtake('Z_void', 'FINAL3', 'yuri', 0, 1500, fire=False)
FIGHT = "boss && boss._r30 && boss._r30.mode === 'fight'"
MORPH = lambda i: "if (boss && boss._r30) { j3Morph(boss, %d); } return 1;" % i
_zev = {}
for k, i in enumerate([1, 5, 2, 6, 3, 7, 4, 0]):
    _zev[60 + k * 330] = MORPH(i)
pwtake('Z_forms', 'FINAL3', 'juggernaut', 0, 2760, pre_until=FIGHT, events=_zev, burst=BURST)
DEATH = ("if (!boss || !boss._r30) return 'no'; const J = j3State(boss); for (let i = 0; i < J.hp.length; i++) J.hp[i] = 0;"
         " J.active = 0; J.mimic = null; boss._r30.finale1003b = false; boss._r30.mode = 'fight'; boss.enter = false;"
         " boss.hp = J.hp[0] = 1; boss._lastPart = boss.parts[0]; _dmgBullet = null; modularHit(10); return boss._r30.mode;")
pwtake('Z_death', 'FINAL3', 'cole', 0, 1200, pre_until=FIGHT, events={30: DEATH}, burst=BURST)

# ---- S6: stage 6 flown through, both routes - the opening, the allies, the choice, the Harrier, the Rebels ---------
S6_WHEN_COMMON = {
    "subBossActive && subBoss && !subBoss.dead && !window.__sbAt": "window.__sbAt = window.__i;",
    "window.__sbAt && window.__i - window.__sbAt > 720 && subBossActive": KILL + " window.__fire = true;",
}


def _route(key):
    return {
        "s6Wing && s6Wing.choice && !s6Wing.route && !window.__chose": "window.__mode = 'none'; window.__fire = false; window.__chose = window.__i;",
        "window.__chose && window.__i - window.__chose > 50 && !window.__tapped": "Input.injectTap('%s'); window.__tapped = 1;" % ('arrowright' if key == 'left' else 'arrowleft'),
        "window.__tapped === 1 && window.__i - window.__chose > 95": "Input.injectTap('%s'); window.__tapped = 2;" % ('arrowleft' if key == 'left' else 'arrowright'),
        "window.__tapped === 2 && window.__i - window.__chose > 150 && !window.__confirmed": "Input.injectTap('enter'); window.__confirmed = 1;",
        "s6Wing && s6Wing.route && !window.__routed": "window.__routed = window.__i; window.__mode = 'boss'; window.__fire = true;",
    }


WHV_FALL = "if (boss && boss._whv && boss._whv.mode === 'carrier') { whvDeathStart(boss); window.__fell = window.__i; }"
take('S6L', 'stage', stage=6, pilot='maverick', warm=0, rec=24000, mode='weave', fire=True, diff='normal', quiet=False,
     when=dict(S6_WHEN_COMMON, **_route('left'),
               **{"bossActive && boss && !boss._rebels && !window.__bAt": "window.__bAt = window.__i;",
                  "window.__bAt && window.__i - window.__bAt > 900 && !window.__fell": WHV_FALL}),
     windows=[[1600, 2500, '_open'], ['@window.__chose', 420, '_choice'], ['@window.__bAt', 1500, '_harrier']],
     stop="window.__bAt && window.__i - window.__bAt > 1560")
take('S6R', 'stage', stage=6, pilot='lizzie', warm=0, rec=24000, mode='weave', fire=True, diff='normal', quiet=False,
     when=dict(S6_WHEN_COMMON, **_route('right'),
               **{"bossActive && boss && boss._rebels && !window.__bAt": "window.__bAt = window.__i;",
                  "window.__bAt && boss && boss._rebels && boss._rebels.frIntro && boss._rebels.frIntro.done && !window.__rfGo": "window.__rfGo = window.__i;"}),
     windows=[[2500, 3300, '_assault'], ['@s6Wing && s6Wing.beats === 1', 600, '_allies'], ['@window.__chose', 420, '_choice'],
              ['@window.__bAt', 1500, '_rebintro'], ['@window.__rfGo', 1500, '_rebfight']],
     stop="window.__rfGo && window.__i - window.__rfGo > 1560")

# ---- X: STAGE X - the floating city at the centre of the map, its card, the rival duel ----------------------------
X_SETUP = ("run.mode = 'campaign'; pilotIndex = PILOTS.findIndex(p => p.key === 'yuri'); run.pilot = 'yuri';"
           " campaign.unlockedMax = 8; campaign.rivalScattered = true; campaign.rivalDefeated = [false,false,false,false,false];"
           " campaign.rank = {1:'S',2:'A',3:'B',4:'S',5:'A',6:'B',7:'A'}; openStageSelect(7, {}); sselBoot = 0;")
X_DUEL = "boss && boss._rebels && boss._rebels.frIntro && boss._rebels.frIntro.done"
take('X_rival', 'menu', setup=X_SETUP, warm=90, rec=6000, quiet=False, mode='boss', fire=True, diff='normal', pilot='yuri',
     events={120: tap('arrowdown'), 200: tap('arrowright'), 260: tap('enter'), 330: tap('enter'), 380: tap('arrowright'),
             430: tap('enter'), 500: tap('enter')},
     when={"state === GS.PLAY && !window.__played": "window.__played = window.__i; window.__mode = 'boss'; window.__fire = true;"},
     windows=[[0, 760, '_map'], ['@' + X_DUEL, 900, '_duel']])

# The map's deploy keys changed (the walk above lands in SAVE GAME), so the Stage X duel is reached through its own
# password: XREBEL - the Rebels in the floating-city mountain/coast arena, intro card and radio kept.
pwtake('X_rx', 'XREBEL', 'yuri', 0, 6000, windows=[[0, 330, '_card'], ['@' + X_DUEL, 900, '_duel']],
       stop="(" + X_DUEL + ") && window.__i > 0 && false")
