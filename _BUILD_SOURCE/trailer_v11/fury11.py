"""fury11.py - the v11 trailer's pilot: _BUILD_SOURCE/bot/furybot.js, the non-cheating Furious bot (Mike, 1014).

v9/v10 flew real9.py, which held run.lives at 3 and re-applied the take's loadout after every death. v11 does neither:
the game's own playerHit is restored (capture3 stubs it), the bot only presses keys, and a death is a death - lives,
shields, i-frames and weapons are whatever the game says they are. A take's setup still chooses the encounter, pilot
and starting weapon (that is the camera crew choosing the scene), but nothing is topped up once the take is rolling.

LIB_FURY is evaluated after capture3.LIB and capture10's LIB9 and replaces window.__auto:
  'none'    no input (menus, cards)
  'hold'    the charge wind-up takes keep their scripted hold (window.__hy === -9999)
  'gates'   the stage-5 warp run: the bot's own dodging, with the next gate's line as its target
  anything else ('weave', 'boss') - the bot's own target (the boss's hittable column, pickups, the field)
The take's burst fire (window.__burst -> window.__fire) still gates the trigger, so bosses are not held in their
white hit flash; the bot's own Fusion release also stands.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BOT = os.path.abspath(os.path.join(HERE, '..', 'bot', 'furybot.js'))

LIB_RESTORE = r"""() => { if (window.__realHit) playerHit = window.__realHit; return true; }"""

LIB_FURY = r"""() => {
  const MOVE = ['a', 'd', 'w', 's'];
  FB.targetOverride = function(){
    const m = window.__mode;
    if (m === 'gates') {
      let g = null;
      if (typeof s5run !== 'undefined' && s5run && !s5run.done && s5run.gates)
        for (const q of s5run.gates) { if (!q.passed && !q.missed) { g = q; break; } }
      return [g ? g.x : worldWidth() / 2, PLAY.y + PLAY.h * 0.72];
    }
    if (m === 'hold' && window.__hx != null && window.__hy != null && window.__hy !== -9999) return [window.__hx, window.__hy];
    return null;
  };
  window.__auto = function(i){
    const K = Input.keys, m = window.__mode;
    const play = (typeof player !== 'undefined') && state === GS.PLAY;
    if (window.__burst) { const b = window.__burst; window.__fire = (i % (b[0] + b[1])) < b[0]; }
    if (!play || m === 'none') { for (const k of MOVE) K[k] = false; K.j = play && !!window.__fire; return; }
    if (m === 'hold' && window.__hy === -9999) {      // the charge wind-up: the take is steering, not dodging
      K.a = K.d = false; K.w = true; K.s = false; return;
    }
    FB.i = i;
    FB.playSafe();
    if (!window.__fire) K.j = false;                 // the take's burst decides when the trigger may be held
  };
  const _m = window.__metrics;
  window.__metrics = function(){
    const o = _m();
    o.hits = FB.hits; o.deaths = FB.deaths; o.rolls = FB.rolls;
    o.dd = (player.dead || player._spin) ? 1 : 0;
    o.iv = (player.invuln | 0) > 0 ? 1 : 0;
    o.lv = run.lives | 0;
    return o;
  };
  window.__armSpecSet = function(){};                // v11: a death keeps its consequences
  return true;
}"""


def install(page):
    page.evaluate(LIB_RESTORE)
    page.evaluate(open(BOT, encoding='utf-8').read())
    page.evaluate(LIB_FURY)
