#!/usr/bin/env python3
"""
probe_l6fleet_0912d.py - THE LEVEL-6 FLEET ACTUALLY FLIES.

    python3 _BUILD_SOURCE/probe_l6fleet_0912d.py --out /tmp/l6

Mike (0912): "Ive noticed we have an l6 fleet folder of enemies that should be used on level 6
immediately. make sure these enemies spawn."

Renders all 27 plates (9 hulls x intact/damaged/critical) BEFORE trusting them, then starts a real
stage 6 and asserts each of the nine types spawns, takes its own stats off L6_FLEET, draws its own
art, and walks its damage states as HP drops.
"""
import os, sys, argparse, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

HULLS = ['n6v0_steel','n6v1_steel','n6v2_steel',
         'n6v0_royal','n6v1_royal','n6v2_royal',
         'n6v0_blackice','n6v1_blackice','n6v2_blackice']
TYPES = ['l6v_s0','l6v_s1','l6v_s2','l6v_r0','l6v_r1','l6v_r2','l6v_b0','l6v_b1','l6v_b2']

SHEET = r"""
(spec) => {
  const [rows, cell] = spec;
  const pad=4, lw=120;
  const c=document.createElement('canvas');
  c.width = lw + 3*(cell+pad) + pad;
  c.height = rows.length*(cell+pad) + pad + 16;
  const x=c.getContext('2d');
  x.fillStyle='#11141a'; x.fillRect(0,0,c.width,c.height);
  x.font='10px monospace'; x.textBaseline='middle'; x.imageSmoothingEnabled=false;
  x.fillStyle='#9fb4c8';
  ['INTACT','DAMAGED','CRITICAL'].forEach((h,i)=>x.fillText(h, lw+i*(cell+pad)+4, 9));
  rows.forEach((base,ri)=>{
    const cy=pad+16+ri*(cell+pad);
    x.fillStyle='#ffc21a'; x.fillText(base, 3, cy+cell/2);
    ['intact','dama','crit'].forEach((st,ki)=>{
      const key=base+'_'+st+'_c', cx=lw+ki*(cell+pad);
      const ok=(typeof XART!=='undefined') && XART.rdy(key);
      x.fillStyle = ok ? '#05070a' : '#3a1414'; x.fillRect(cx,cy,cell,cell);
      if(ok){
        const im=XART.get(key);
        const s=Math.min(cell/im.naturalWidth, cell/im.naturalHeight)*0.94;
        x.drawImage(im, cx+(cell-im.naturalWidth*s)/2, cy+(cell-im.naturalHeight*s)/2,
                    im.naturalWidth*s, im.naturalHeight*s);
      } else { x.fillStyle='#ff8a7a'; x.fillText('MISSING', cx+4, cy+cell/2); }
    });
  });
  return c.toDataURL('image/png');
}
"""

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/l6'); a=ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs=[]; fails=[]; n_ok=[0]
    def ok(c,m):
        if c: n_ok[0]+=1; print('  ok  ',m)
        else: fails.append(m); print('  FAIL',m)
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg=b.new_page(viewport={'width':1100,'height':1000})
        pg.on('pageerror', lambda e: errs.append('pageerror: '+str(e)[:200]))
        pg.goto(f'http://127.0.0.1:{port}/index.html?bossmode=1', wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOSSMODE && window.BOSSMODE.ready", timeout=90000)

        # ---- the art, rendered rather than trusted. rdy() is false on its first call. ----
        keys=[h+'_'+s+'_c' for h in HULLS for s in ('intact','dama','crit')]
        pg.evaluate("(ks)=>ks.forEach(k=>{try{XART.rdy(k);}catch(e){}})", keys)
        pg.wait_for_timeout(4000)
        pg.evaluate("(ks)=>ks.forEach(k=>{try{XART.rdy(k);}catch(e){}})", keys)
        pg.wait_for_timeout(2500)
        miss=pg.evaluate("(ks)=>ks.filter(k=>!XART.rdy(k))", keys)
        ok(not miss, 'all 27 fleet plates decode (9 hulls x 3 damage states) - missing: %s' % (miss or 'none'))
        d=pg.evaluate(SHEET, [HULLS, 104])
        open(os.path.join(a.out,'01_fleet.png'),'wb').write(base64.b64decode(d.split(',',1)[1]))

        # ---- the roster is real, not a reskin ----
        tbl=pg.evaluate("() => { const o={}; for(const k in L6_FLEET) o[k]=L6_FLEET[k]; return o; }")
        ok(len(tbl)==9, 'L6_FLEET carries nine roster entries (%d)' % len(tbl))
        ok(len(set((t['hp'],t['score'],t['vy']) for t in tbl.values()))==9,
           'and each has its OWN stats - no two share hp/score/speed')

        # ---- stage 6 actually fields them ----
        plan=pg.evaluate("""() => {
            run.stage=6; curStage=STAGES[5];
            const P=buildStagePlan(6);
            const seen={};
            for(const ev of P){ const src=String(ev.fn||ev.f||ev.go||'');
                (src.match(/l6v_[a-z0-9]+/g)||[]).forEach(k=>seen[k]=(seen[k]||0)+1); }
            return {events:P.length, seen:seen};
        }""")
        got=sorted(plan['seen'].keys())
        ok(len(got)==9, 'stage 6 schedules all nine fleet types (%d of 9): %s' % (len(got), got))
        ok(plan['events']>20, "and they join the storm hulls rather than replacing them (%d events)" % plan['events'])

        # ---- each one really spawns, with its own art and stats ----
        res=pg.evaluate("""(types) => {
            const out={};
            for(const t of types){
                enemies.length=0;
                spawnEnemy(t, 240, 120, {});
                const e=enemies[0];
                out[t]= e ? {name:e.name, vk:e._vk, hp:e.hp, w:e.w, h:e.h, shoots:!!e.shoots} : null;
            }
            enemies.length=0;
            return out;
        }""", TYPES)
        bad=[t for t in TYPES if not res.get(t) or not res[t]['vk'].startswith('n6v')]
        ok(not bad, 'every one of the nine spawns and carries its own n6v art key - bad: %s' % (bad or 'none'))
        ok(len(set(r['name'] for r in res.values()))==9,
           'nine distinct roster names: %s' % ', '.join(sorted(r['name'] for r in res.values())[:3]) + ' ...')

        # ---- and the damage states are reachable ----
        st=pg.evaluate("""() => {
            enemies.length=0; spawnEnemy('l6v_b1',240,200,{});
            const e=enemies[0], seen=[];
            for(const frac of [1.0, 0.5, 0.15]){
                e.hp = Math.max(1, Math.round(e.maxhp*frac));
                seen.push(e._vk + '_' + _vaultState(e));
            }
            enemies.length=0; return seen;
        }""")
        ok(len(set(st))>=2, 'HP drives the damage plate: %s' % st)

        # ---- a real stage-6 run puts them on screen ----
        pg.evaluate("""async () => {
            run.mode='arcade'; startRun(6); setState(GS.PLAY);
            for(let i=0;i<40;i++) await new Promise(r=>requestAnimationFrame(r));
        }""")
        live=pg.evaluate("""async () => {
            const seen={};
            /* ⚠ THE WAVE PUMP GATES ON AN ON-SCREEN CAP, so a probe that never shoots deadlocks the
               stage. Measured: waveIdx froze at 9 with exactly 10 live enemies while stageTimer ran
               on to 201s of a 56s stage - the dispatcher was holding the queue because the deck was
               full, which is the density guard working exactly as designed. A player clears the
               lane; this clears it for them, which is the only way to see the whole plan run. */
            for(let i=0;i<60*400; i++){
                updatePlay(1/60);
                for(const e of enemies){
                    if(e && /^n6v/.test(e._vk||'')) seen[e.name]=1;
                }
                if((i % 24)===0){ for(const e of enemies){ if(!e._tur && !e._bunker && !e._mini) e.dead=true; } }
                if(Object.keys(seen).length>=9) break;
            }
            return {seen:Object.keys(seen), t:Math.round(stageTimer), idx:waveIdx,
                    plan:(typeof stagePlan!=='undefined'&&stagePlan)?stagePlan.length:-1};
        }""")
        ok(len(live['seen'])>=9,
           'a real stage-6 run fields all nine (%d, by wave %d of %d at t=%ss): %s'
           % (len(live['seen']), live['idx'], live['plan'], live['t'], sorted(live['seen'])))
        b.close()
    stop()
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails: print('  FAIL', f)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:8]: print('   ', e)
    sys.exit(1 if fails or errs else 0)

if __name__=='__main__':
    main()
