#!/usr/bin/env python3
"""
probe_bossdrop_0917.py - the combination comes off the boss, and the ladder is Mike's, in real Chromium.

Mike, 0917:
  "you dont unlock all these weapon combination upgrades. Your going to make powerup upgrade's for
   these new weapon types that drop from the boss when they die at each level, and thats how we gain
   new combinations and such."
  "Achievement points are also tied to this ... Collecting items, powerups and special abilities also
   gives you points like 250 each. Somersalting, or barrel rolling before a projectile would've
   impacted you grants you a 'Stylish!' award of 500 points that appears letter by letter and glows
   before fading away letter by letter ... scale our new system to start with each upgrade at about
   1000 ... goes up by 25%."

WHAT IS MEASURED, AND WHY EACH ONE IS THE HONEST QUESTION

  THE DROP     a REAL bossDie() leaves exactly one combination pickup, at the boss's own position -
               driven through the death branch rather than by calling forgeBossDrop, because "the
               boss drops it when it dies" is a claim about that path.
  THE GRANT    collecting it through the real applyPowerup owns the pair, with NO cost on the record
               (a reward that advanced the price ladder would be a punishment), and it survives
               achievementNormalize, which is what "permanent" means here.
  THE GATE     the Forge refuses the pair it was never given ('locked') and takes the one it was;
               the ARMORY refuses a LEVEL on an unearned pair and prints no price beside it.
  PER SLOT     the element list belongs to the slot under the cursor - a combination is ELEMENT x
               WEAPON, so FIRE on the machine gun may not offer what was earned for the laser.
  THE LADDER   1000 / 1250 / 1560 / 1950 / 2440, advanced by a PAID purchase and not by a drop.
  THE POOL     balance = achievement points + converted - spent.
  250 / 500    a pickup pays 250 through applyPowerup; a round that would have hit during a roll pays
               500 once, and ordinary post-hit i-frames pay nothing.

⚠ THE PROFILE IS localStorage AND PERSISTS - cleared at the start and at the end (the awards probe's
lesson), or the second run measures a build where everything is already owned.
⚠ AND THE STYLISH ARM IS READ AS PIXELS, NOT AS A FLAG. "It types in and types out" is a claim about
what is on the canvas; a counter cannot tell a word being erased from a word that never drew.
"""
import os, sys, base64, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, 'docs', 'proofs', 'bossdrop_0917')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 1000, 'height': 1200})
        errs = []
        pg.on('pageerror', lambda e: errs.append('page:' + str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof forgeBossDrop==='function' && typeof stylishCheck==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate("() => { try{ localStorage.removeItem(ACHIEVEMENT_STORE_KEY); }catch(_){} achievementReload(); }")
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.__step=%s; window.playerHit=function(){}; run.mode='arcade'; run.lives=9; }" % sh.STEP)
        def step(n): pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", n)
        def shot(name):
            d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
            if d: open(os.path.join(OUT, name + '.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        step(6)

        # ---- 1. THE LADDER, before anything is bought ----
        L = pg.evaluate("() => [0,1,2,3,4].map(n=>forgeUpgradeCost(n))")
        print('  ladder:', json.dumps(L))
        ok(L[0] == 1000, 'the first upgrade is 1,000 (%s)' % L[0])
        ok(all(abs(L[i + 1] / L[i] - 1.25) < 0.01 for i in range(4)),
           'and every one after it is 25%% more than the last: %s' % L)
        ok(pg.evaluate("() => forgeUpgradesBought()===0 && forgeUpgradeCost()===1000"),
           'nothing bought yet, so the price on the screen is the first rung')

        # ---- 2. THE POOL ----
        pg.evaluate("() => { achievementState=achievementEmpty(); achievementState.unlocked={stage_nodeath_1:{at:1}}; furiousConvertLevel(1, 4200); }")
        P = pg.evaluate("() => ({pts:achievementPoints(), conv:furiousConverted(), spent:furiousSpent(), bal:furiousBalance()})")
        print('  pool:', json.dumps(P))
        ok(P['pts'] == 200 and P['conv'] == 4 and P['bal'] == 204,
           'the balance is the AWARDS plus what the levels converted, less what was spent (%d + %d = %d)' % (P['pts'], P['conv'], P['bal']))

        # ---- 3. THE BOSS DROPS IT, THROUGH THE REAL DEATH ----
        pg.evaluate("() => { achievementState=achievementEmpty(); powerups.length=0; }")
        D = pg.evaluate("""() => {
          spawnBoss((STAGES[0]&&STAGES[0].boss)||'damkeeper');
          if(!boss) return {err:'no boss'};
          const bx=boss.x, by=(boss._drawY!=null?boss._drawY:boss.y);
          boss.hp=0; bossDie();
          const P=powerups.filter(p=>p.kind==='forgecombo');
          return {n:P.length, dx:P[0]?Math.abs(P[0].x-bx):-1, by:by, py:P[0]?P[0].y:-1, vh:VH,
                  inField:P[0]?(P[0].y>0&&P[0].y<VH):false, holds:P[0]?(P[0]._fcHold!=null):false,
                  elem:P[0]?P[0].elem:null, w:P[0]?P[0].fw:null, owned:P[0]?forgeComboOwned(P[0].elem,P[0].fw):null}; }""")
        print('  boss drop:', json.dumps(D))
        ok(D.get('n') == 1, 'a boss death leaves EXACTLY ONE combination powerup (%s)' % D.get('n'))
        ok(D.get('dx', 99) < 1, "on the boss's own column (%s px off)" % D.get('dx'))
        # [!] MEASURED, NOT ASSUMED: the first build spawned this at boss.y = 618.6 on a 512-tall field
        # and the cull killed it on frame one - a guaranteed reward nobody could ever touch.
        ok(D.get('inField') and D.get('holds'),
           'and INSIDE the playfield, with a hover line, so the cook-off cannot take it away (y %s of %s, boss y %s)'
           % (round(D.get('py', -1)), D.get('vh'), round(D.get('by', -1))))
        ok(D.get('elem') and D.get('w') is not None and D.get('owned') is False,
           'naming a pair the player does not own yet: %s on slot %s' % (D.get('elem'), D.get('w')))
        shot('01_boss_drop')

        # ---- 4. THE FORGE REFUSES THE PAIR IT WAS NEVER GIVEN ----
        el, wslot = D.get('elem'), D.get('w')
        pg.evaluate("""([e,w]) => { run.forge={}; run.forgeElems={}; run.forgeCombos=2; run.forgeRespecs=2;
          run.weapon=w; run.infusion=null; forgeDiscover(e); }""", [el, wslot])
        ok(pg.evaluate("([e,w]) => forgeCombine(w,e)==='locked'", [el, wslot]),
           'the Forge refuses that combination BEFORE the drop is collected, even with the element seen in the field')
        ok(pg.evaluate("([e,w]) => forgeElemsFor(w).indexOf(e)<0", [el, wslot]),
           "and it is not in the slot's own element list, so the picker never offers it")

        # ---- 5. COLLECTING IT ----
        G = pg.evaluate("""([e,w]) => {
          const before=run.score|0;
          const P=powerups.filter(p=>p.kind==='forgecombo')[0];
          applyPowerup(P);
          const rec=(achievementState.owned||{})[forgeComboId(e,w)]||null;
          return {owned:forgeComboOwned(e,w), rec:rec, cost:rec?(rec.cost==null?'none':rec.cost):null,
                  spent:furiousSpent(), bought:forgeUpgradesBought(), score:(run.score|0)-before}; }""", [el, wslot])
        print('  grant:', json.dumps(G))
        ok(G['owned'] is True, 'collecting it owns the combination')
        ok(G['cost'] == 'none' and G['spent'] == 0, 'with NO cost on the record, so it is not spending (%s)' % G['cost'])
        ok(G['bought'] == 0 and pg.evaluate("() => forgeUpgradeCost()===1000"),
           'and it does not advance the price ladder - a reward may not raise your prices')
        ok(pg.evaluate("([e,w]) => { const v=achievementNormalize(JSON.parse(JSON.stringify(achievementState))); return !!v.owned[forgeComboId(e,w)] && v.owned[forgeComboId(e,w)].cost==null; }", [el, wslot]),
           'it survives a save/load round trip, still with no cost - which is what PERMANENT means here')

        # ---- 6. NOW THE FORGE TAKES IT, AND ONLY ON THAT SLOT ----
        ok(pg.evaluate("([e,w]) => forgeElemsFor(w).indexOf(e)>=0", [el, wslot]),
           "the element is in that slot's list now")
        other = pg.evaluate("([w]) => FORGE_WEAPONS.filter(x=>x!==w)[0]", [wslot])
        ok(pg.evaluate("([e,w]) => forgeElemsFor(w).indexOf(e)<0", [el, other]),
           'and in NO OTHER slot\'s - a combination is ELEMENT x WEAPON, not an element (slot %s)' % other)
        ok(pg.evaluate("([e,w]) => forgeCombine(w,e)==='locked'", [el, other]),
           'so combining it on another slot is still refused')
        R = pg.evaluate("([e,w]) => { const r=forgeCombine(w,e); return {r:r, f:run.forge[w]||null}; }", [el, wslot])
        ok(R['r'] == 'ok' and R['f'] and R['f']['elem'] == el, 'and on the slot it was earned for it combines (%s)' % json.dumps(R))

        # ---- 7. THE ARMORY ----
        pg.evaluate("() => { achievementState=achievementEmpty(); furiousConvertLevel(1, 9000000); }")
        A0 = pg.evaluate("([e,w]) => { const rows=armoryRows(w); const r=rows.filter(x=>x.elem===e)[0]; return {earned:r.earned, cost:r.cost, buy:forgeLevelBuy(e,w)}; }", [el, wslot])
        ok(A0['earned'] is False and A0['cost'] == 0 and A0['buy'] == 'locked',
           'the ARMORY shows an unearned pair with NO price and refuses to sell its level (%s)' % json.dumps(A0))
        ok(pg.evaluate("([e,w]) => furiousSpent()===0", [el, wslot]),
           'and the refusal took nothing - an undeliverable sale is the one thing a derived balance cannot repair')
        pg.evaluate("([e,w]) => forgeComboGrant(e,w)", [el, wslot])
        B = pg.evaluate("""([e,w]) => {
          const c0=forgeUpgradeCost(), b0=furiousBalance();
          const r1=forgeLevelBuy(e,w), c1=forgeUpgradeCost(), b1=furiousBalance();
          const r2=forgeLevelBuy(e,w), c2=forgeUpgradeCost();
          return {c0,b0,r1,c1,b1,r2,c2,lv:forgeOwnedLevel(e,w),bought:forgeUpgradesBought()}; }""", [el, wslot])
        print('  armory:', json.dumps(B))
        ok(B['r1'] == 'ok' and B['b0'] - B['b1'] == B['c0'], 'once earned, a LEVEL sells at the ladder price and the balance drops by exactly it')
        ok(B['c1'] == 1250 and B['c2'] == 1560, 'and each purchase raises the next price 25%%: %d -> %d -> %d' % (B['c0'], B['c1'], B['c2']))
        ok(B['lv'] == 3 and B['bought'] == 2, 'two levels bought, two rungs climbed')

        # ---- 8. A PICKUP IS 250 ----
        S = pg.evaluate("""() => { const b=run.score|0; applyPowerup({kind:'bomb',x:100,y:100}); const a=run.score|0;
          return {d:a-b, k:PICKUP_SCORE}; }""")
        ok(S['d'] == 250 and S['k'] == 250, 'collecting a pickup is worth 250 points (%s)' % json.dumps(S))
        ok(not pg.evaluate("() => /run\\.score\\+=50/.test(String(updateEffects))") and
           pg.evaluate("() => /PICKUP_SCORE/.test(String(applyPowerup))"),
           'scored inside applyPowerup, which every collection route passes - the old 50 at the touch test is gone')

        # ---- 9. STYLISH ----
        pg.evaluate("""() => { eBullets.length=0; player.dead=false; player.invuln=0; player.roll=null; player.somer=null;
          player._rollCool=0; player._somerCool=0; stylish=null; }""")
        ST = pg.evaluate("""() => {
          const out={};
          /* a round sitting ON the player, with NO manoeuvre: ordinary i-frames must pay nothing */
          player.invuln=60;
          let b={x:player.x,y:player.y,vx:0,vy:0,w:8,h:8,kind:'pellet',dead:false};
          const s0=run.score|0; out.noManoeuvre=stylishCheck(b); out.noManoeuvreScore=(run.score|0)-s0;
          player.invuln=0;
          /* now roll, which sets its own i-frames, and put the same round on the hitbox */
          startRoll(1);
          out.invulnFromRoll=player.invuln>0;
          b={x:player.x,y:player.y,vx:0,vy:0,w:8,h:8,kind:'pellet',dead:false};
          const s1=run.score|0; out.first=stylishCheck(b); out.firstScore=(run.score|0)-s1;
          /* a second round in the same roll: one award per manoeuvre */
          const s2=run.score|0; out.second=stylishCheck({x:player.x,y:player.y,vx:0,vy:0,w:8,h:8,kind:'pellet',dead:false});
          out.secondScore=(run.score|0)-s2;
          out.live=!!stylish;
          return out; }""")
        print('  stylish:', json.dumps(ST))
        ok(ST['noManoeuvre'] is False and ST['noManoeuvreScore'] == 0,
           'ordinary i-frames pay NOTHING - you were lucky, not stylish')
        ok(ST['invulnFromRoll'] is True, 'a barrel roll sets its own i-frames, which is why the round would have hit')
        ok(ST['first'] is True and ST['firstScore'] == 500, 'a round that would have impacted you during the roll pays 500 (%s)' % ST['firstScore'])
        ok(ST['second'] is False and ST['secondScore'] == 0, 'and the SECOND round in the same roll pays nothing - one award per manoeuvre')
        ok(ST['live'] is True, 'the award is on screen')
        # it types in and types out, read as ink
        INK = pg.evaluate("""(D) => {
          const c=document.getElementById('screen'), g=c.getContext('2d');
          const out=[];
          for(const t of D){
            stylish={t:t, x:VW/2, y:VH*0.34, n:0};
            g.clearRect(0,0,c.width,c.height);
            stylishDraw();
            const im=g.getImageData(0,0,c.width,c.height).data; let n=0;
            for(let i=3;i<im.length;i+=4) if(im[i]>24) n++;
            out.push({t:t, px:n});
          }
          stylish=null;
          return out; }""", [0.02, 0.18, 0.40, 0.80, 1.30, 1.45, 1.52])
        print('  stylish ink:', json.dumps(INK))
        rising = [r['px'] for r in INK[:3]]
        falling = [r['px'] for r in INK[4:]]
        ok(rising[0] > 0 and rising[0] < rising[1] < rising[2],
           'it TYPES IN - the lit pixels grow letter by letter (%s)' % rising)
        ok(falling[0] > falling[1] > falling[2] and falling[2] == 0,
           'and it is ERASED the same way, letter by letter, to nothing (%s)' % falling)
        ok(pg.evaluate("() => { stylish={t:0.9,x:VW/2,y:VH*0.34,n:0}; const a=[]; const st=stageText; window.stageText=function(art,txt){ a.push(String(txt)); return st.apply(this,arguments); }; stylishDraw(); window.stageText=st; stylish=null; return a.some(x=>/500/.test(x)); }"),
           'and it says what it paid')
        shot('02_stylish')

        # ---- the profile is left as it was found ----
        pg.evaluate("() => { try{ localStorage.removeItem(ACHIEVEMENT_STORE_KEY); }catch(_){} achievementReload(); }")
        print('  errors:', len(errs))
        for e in errs[:6]: print('   !', e[:200])
        ok(len(errs) == 0, 'no page or console errors (%d)' % len(errs))
        br.close()
    stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
