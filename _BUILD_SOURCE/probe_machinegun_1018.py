#!/usr/bin/env python3
"""Real Chromium trigger, launch geometry and authored-pixel proof for the nose MG.

--before records the reported regression without requiring the fix to pass.
Output stays under _shots/machinegun_1018. No product QA hooks or saved games.
"""
from pathlib import Path
import json
import sys

import shoot
from playwright.sync_api import sync_playwright

ROOT = Path(shoot.GAME)
BEFORE = '--before' in sys.argv
OUT = ROOT / '_shots' / 'machinegun_1018' / ('before' if BEFORE else 'after')
PILOTS = ['cole', 'maverick', 'lizzie', 'juggernaut', 'yuri', 'freezer', 'falva', 'decker', 'axel']

SETUP = r"""() => {
 diffKey='normal';run.mode='arcade';startRun(1);beginStage(1);setState(GS.PLAY);player.reset();
 playerHit=function(){};stagePlan=[];enemies=[];powerups=[];special=null;run.shield=0;
 window.MG18={shots:[],keys:[],draws:0};
 const shot=pShoot;pShoot=function(){const old=new Set(pBullets),r=shot.apply(this,arguments);
  MG18.shots.push(pBullets.filter(b=>!old.has(b)).map(b=>({kind:b.kind,x:b.x,y:b.y,vx:b.vx,vy:b.vy,
   dmg:b.dmg,lv:b.lv,inf:b._inf,cal50:!!b._cal50,chaingun:!!b._chaingun,cf:b._cfLaser})));
  return r;};
 const get=XART.get,draw=ctx.drawImage;const keys=new WeakMap();
 XART.get=function(k){const im=get.apply(this,arguments);if(im&&typeof im==='object')keys.set(im,k);return im;};
 ctx.drawImage=function(im){const k=keys.get(im);if(k&&/^(mgcf_|ea11_|d27_|repair30_chaingun)/.test(k)){
   MG18.keys.push(k);MG18.draws++;}return draw.apply(this,arguments);};
 wm26Warm();for(let l=1;l<=5;l++)for(let f=0;f<6;f++)XART.rdy('mgcf_'+l+'_'+f);
 for(const pk of PILOTS.map(p=>p.key))XART.rdy('ship_'+pk);
 for(const a of Object.values(EA11_ART.banks))XART.rdy(a.key);
 for(const a of Object.values(REPAIR30_ART))if(/chaingun/.test(a.key))XART.rdy(a.key);
 return true;
}"""

CONFIG = r"""cfg => {
 for(const k of Object.keys(Input.keys))Input.keys[k]=false;
 run.pilot=cfg.pilot;pilotIndex=PILOTS.findIndex(p=>p.key===cfg.pilot);
 run.weapon=cfg.weapon??0;run.wlevel=cfg.lv;run.wlevels[run.weapon]=cfg.lv;run.wlevels[0]=cfg.lv;
 run.spaceMode=false;run.loadout=[run.weapon];run.forge={};run.forgeForms={};run.infusion=cfg.inf?{elem:cfg.inf,lv:3}:null;
 player.reset();player.x=worldWidth()/2;player.y=PLAY.y+viewH()*.75;player._drawY=player.y;
 player.invuln=0;player.fireCd=0;player._bank=0;special=null;pBullets=[];eBullets=[];
 powerups=[];enemies=[];wm26Releases=[];MG18.shots=[];MG18.keys=[];MG18.draws=0;
 const key=shipGlowKey('ship_'+cfg.pilot);XART.rdy(key);
 return {x:player.x,y:player.y,nose:wm26PlayerNose(),weapon:run.weapon};
}"""

RESULT = r"""() => ({shots:MG18.shots,keys:[...new Set(MG18.keys)],draws:MG18.draws,
 flashes:wm26Releases.filter(f=>f.player).map(f=>({...wm26Point(f),family:f.family,emitter:f.emitter})),
 player:{x:player.x,y:player.y},nose:wm26PlayerNose(),state})"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    port, stop = shoot.serve(str(ROOT))
    errors, report, checks = [], {'cases': []}, []

    def check(name, passed):
        checks.append({'name': name, 'passed': bool(passed)})
        print(('ok   ' if passed else 'FAIL ') + name, flush=True)

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(channel='msedge', args=['--mute-audio'])
            page = browser.new_page(viewport={'width': 1600, 'height': 900})
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('console', lambda m: errors.append(m.text) if m.type == 'error' or 'draw error' in m.text else None)
            page.goto(f'http://127.0.0.1:{port}/index.html', timeout=120000)
            page.wait_for_function('window.__bofFrames>4', timeout=120000)
            page.evaluate(shoot.TRAP_RAF)
            page.wait_for_timeout(35)
            page.evaluate(SETUP)
            page.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&bmfReady("game");}', timeout=120000)
            page.wait_for_function("()=>[1,2,3,4,5].every(l=>[0,1,2,3,4,5].every(f=>XART.rdy('mgcf_'+l+'_'+f)))", timeout=60000)

            def frames(n):
                for i in range(0, n, 12):
                    result = page.evaluate(shoot.STEP, min(12, n-i))
                    if result:
                        errors.append(result)
                    page.wait_for_timeout(5)

            def case(pk, lv, weapon=0, inf=None, capture=False):
                cfg = dict(pilot=pk, lv=lv, weapon=weapon, inf=inf)
                page.evaluate(CONFIG, cfg)
                page.wait_for_function("()=>XART.rdy(shipGlowKey('ship_'+run.pilot))", timeout=60000)
                origin = page.evaluate('wm26PlayerNose()')
                page.keyboard.down('j')
                frames(2)
                page.keyboard.up('j')
                r = page.evaluate(RESULT)
                r.update(cfg)
                r['origin'] = origin
                if capture:
                    page.screenshot(path=str(OUT / f'{pk}_w{weapon}_l{lv}_{inf or "plain"}_launch.png'))
                frames(16)
                r['flight'] = page.evaluate(RESULT)
                if capture:
                    page.screenshot(path=str(OUT / f'{pk}_w{weapon}_l{lv}_{inf or "plain"}_flight.png'))
                report['cases'].append(r)
                return r

            for pk in (['cole'] if BEFORE else PILOTS):
                for lv in range(6):
                    r = case(pk, lv, capture=pk == 'cole' or lv == 5)
                    rounds = [b for s in r['shots'] for b in s if b['kind'] == 'mg' and not b['cal50']]
                    check(f'{pk} L{lv}: {lv+1} regular MG projectiles', len(rounds) == lv+1)
                    if rounds:
                        mean = sum(b['x'] for b in rounds)/len(rounds)
                        check(f'{pk} L{lv}: tight centered nose launch',
                              abs(mean-r['origin']['x']) < .01 and
                              max(b['x'] for b in rounds)-min(b['x'] for b in rounds) <= 20.01 and
                              all(abs(b['y']+6-r['origin']['y']) < .01 for b in rounds))
                    flashes = r['flashes']
                    check(f'{pk} L{lv}: one flash at the actual nose', len(flashes) == 1 and
                          abs(flashes[0]['x']-r['origin']['x']) < .01 and abs(flashes[0]['y']-r['origin']['y']) < .01)
                    check(f'{pk} L{lv}: authored MG round pixels reach the native renderer',
                          any(k.startswith('mgcf_'+str(max(1,lv))+'_') for k in r['flight']['keys']))

            if not BEFORE:
                for lv in range(1, 6):
                    r = case('cole', lv, weapon=7, capture=lv == 5)
                    rounds = [b for s in r['shots'] for b in s if b['cal50'] and b['chaingun']]
                    check(f'Chaingun L{lv}: retains its distinct wing pod pattern',
                          len(rounds) == (1 if lv == 1 else 2) and
                          all(abs(b['x']-r['player']['x']) > 8 for b in rounds))
                for inf in ['fire','kinetic','lightning','water','ice','chrome','toxic','dark','wind']:
                    r = case('cole', 3, inf=inf, capture=inf in ['wind','fire'])
                    rounds = [b for s in r['shots'] for b in s if b['kind']=='mg']
                    check(inf+': infusion preserves four centered MG rounds', len(rounds)==4 and all(b.get('inf')==inf for b in rounds))
                for lv, count in [(6, 3), (7, 4)]:
                    r = case('cole', lv)
                    rounds = [b for s in r['shots'] for b in s if b['kind']=='mg']
                    arcs = [b for s in r['shots'] for b in s if b['kind']=='coletri']
                    check(f'Cole L{lv}: retains authored laser tier and separate homing arches',
                          len(rounds)==count and len(arcs)==count and all(b.get('cf')==lv for b in rounds))

            check('No page, console or draw errors', not errors)
            browser.close()
    finally:
        stop()
    report.update(checks=checks, errors=errors, passed=sum(c['passed'] for c in checks), failed=sum(not c['passed'] for c in checks))
    (OUT / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f"{report['passed']} passed / {report['failed']} failed", flush=True)
    return 0 if BEFORE else int(report['failed'] > 0)


if __name__ == '__main__':
    sys.exit(main())
