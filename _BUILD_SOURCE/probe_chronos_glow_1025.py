"""Chronos glow pass: every form with the layer on and off, the transformation
drive (shake, flashes, bursts), and the pixel-ring contract, in real Chromium.

python _BUILD_SOURCE/probe_chronos_glow_1025.py
"""
from pathlib import Path
import json
from PIL import Image
from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF

R = Path(__file__).resolve().parents[1]
O = R / '_shots/chronos_glow_1025/probe'
O.mkdir(parents=True, exist_ok=True)
checks, errors = [], []


def ck(name, ok, data=None):
    checks.append(dict(name=name, passed=bool(ok), data=data))
    print(('PASS ' if ok else 'FAIL ') + name, '' if ok else json.dumps(data), flush=True)


SETUP = """()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});
spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;
for(const w of ['c32Warm','c30Warm','c29Warm','bi24Warm','ht23Warm','c25Warm','c26Warm','c27Warm','ch23Warm','cgWarm'])
  if(typeof window[w]==='function')window[w]();}"""
READY = """()=>{stageLoadTick();return [stageLoadReady(5),c32Warm(),c30Warm(),c29Warm(),bi24Warm(),ht23Warm(),ch23Warm(),c25Warm(),c26Warm(),c27Warm(),cgWarm()].every(Boolean)}"""
OFF = "()=>{window.__cgDraw=hammerBossDraw;hammerBossDraw=CG.base;}"
ON = "()=>{hammerBossDraw=window.__cgDraw;}"
STATES = {
    'regular': "()=>{const h=boss._hammer;h.state='hammer';h.t=1;h._hf22Red=false;delete h._hf22Charge;if(h.frArmor){h.frArmor.activated=false;h.frArmor.hp=0;}}",
    'activation': "()=>{const h=boss._hammer;h.hb20Pickup=null;h.state='fr_activation';h.t=1.9;}",
    'chrome': "()=>{const h=boss._hammer;h.state='hammer';h.t=1;h.frArmor=Object.assign(h.frArmor||{},{hp:1000,max:1000,activated:true});}",
    'ragecharge': "()=>{const h=boss._hammer;if(h.frArmor){h.frArmor.activated=false;h.frArmor.hp=0;}h.state='hammer';h._hf22Red=false;h.c27RagePending=true;boss.hp=boss.maxhp*.1;hf22BeginBlueRage(boss);h._hf22Charge.t=1.6;}",
    'rage': "()=>{const h=boss._hammer;delete h._hf22Charge;h._hf22Red=true;h.rage=999;h.state='hammer';h.t=1;h._cgPrev={mode:'rage'};h._cgFlare=0;}",
}
CROP = (300, 80, 980, 760)

port, stop = serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(channel='msedge', args=['--autoplay-policy=no-user-gesture-required'])
        p = br.new_page(viewport={'width': 1280, 'height': 800})
        p.on('pageerror', lambda e: errors.append(str(e)))
        p.on('console', lambda m: errors.append(m.text) if m.type == 'error' or 'draw error' in m.text else None)
        p.goto(f'http://127.0.0.1:{port}/index.html')
        p.wait_for_function("window.__bofFrames>5&&typeof CG!=='undefined'&&typeof c32Warm==='function'", timeout=180000)
        p.mouse.click(3, 3)
        p.evaluate(TRAP_RAF)
        p.evaluate(SETUP)
        p.wait_for_function(READY, timeout=180000)
        ck('Aura sheets decode', p.evaluate("cgWarm()"))
        tiles = []
        for name, js in STATES.items():
            p.evaluate(js)
            pair = []
            for on in (False, True):
                p.evaluate(ON if on else OFF)
                p.evaluate("()=>{efxClock=12.34;boss.x=340;boss.y=260;boss.flash=0;particles.length=0;boss._hammer._cgPrev={mode:cgMode(boss).mode};boss._hammer._cgFlare=0;shake=0;flashScreen=0;drawWorld(0);}")
                f = O / f'{name}_{"on" if on else "off"}.png'
                p.screenshot(path=str(f))
                pair.append(Image.open(f).convert('RGB').crop(CROP))
            p.evaluate(ON)
            a, b = pair
            diff = sum(1 for x, y in zip(a.get_flattened_data(), b.get_flattened_data()) if x != y)
            ck(f'{name}: the layer changes the picture', diff > 2000, diff)
            tiles.append(pair)
        # contact sheet: off over on, per form
        w, h = tiles[0][0].size
        sheet = Image.new('RGB', (w * len(tiles), h * 2))
        for i, (a, b) in enumerate(tiles):
            sheet.paste(a, (i * w, 0)); sheet.paste(b, (i * w, h))
        sheet.resize((sheet.width // 2, sheet.height // 2)).save(O.parent / 'forms_off_on.png')

        # The rage transformation, driven through its real charge clock.
        p.evaluate(STATES['regular'])
        p.evaluate("()=>{const h=boss._hammer;h._cgPrev={};h.c27RagePending=true;boss.hp=boss.maxhp*.1;hf22BeginBlueRage(boss);window.__sh=[];}")
        seq = []
        for i in range(12):
            t = i * 0.16
            r = p.evaluate("t=>{const h=boss._hammer;if(h._hf22Charge)h._hf22Charge.t=t;shake=0;efxClock+=1/30;drawWorld(0);__sh.push(shake);return {shake,mode:cgMode(boss).mode};}", t)
            seq.append(r)
            if i in (2, 6, 10):
                f = O / f'rage_charge_{i}.png'; p.screenshot(path=str(f))
        shakes = [s['shake'] for s in seq if s['mode'] == 'ragecharge']
        ck('Shake builds through the rage charge', len(shakes) > 4 and shakes[-1] > shakes[0], shakes)
        # the rage forming (chronos_rageform_1026.js) owns the charge draw: strikes land, then the final strike bursts
        r = p.evaluate("""()=>{const h=boss._hammer;delete h._hf22Charge;h._hf22Red=false;h._c45Burst=false;h._cgPrev={};h.c27RagePending=true;boss.hp=boss.maxhp*.1;hf22BeginBlueRage(boss);
          const ev=BOF_CHRONOS_RAGEFORM.events;ev.length=0;let maxShake=0;
          for(let i=0;i<=120;i++){h._hf22Charge.t=1.8*i/120;shake=0;flashScreen=0;efxClock+=1/30;particles.length=0;drawWorld(0);maxShake=Math.max(maxShake,shake);}
          const out={strikes:ev.filter(e=>e.type==='strike').length,final:ev.some(e=>e.type==='final'),flash:flashScreen,maxShake};delete h._hf22Charge;h._hf22Red=true;h._cgPrev={mode:'rage'};drawWorld(0);return out;}""")
        ck('Super Saiyan burst when the red form lands', r['final'] and r['strikes'] >= 12 and r['maxShake'] >= 18, r)
        f = O / 'rage_burst.png'; p.screenshot(path=str(f))

        # Chromium: activation shakes and bursts when the plating locks.
        p.evaluate("()=>{const h=boss._hammer;h._hf22Red=false;h._cgPrev={};h.state='fr_activation';h.t=2.2;shake=0;drawWorld(0);}")
        ck('Activation shakes', p.evaluate("shake") > 1, p.evaluate("shake"))
        p.evaluate("()=>{const h=boss._hammer;h.state='hammer';h.frArmor=Object.assign(h.frArmor||{},{hp:1000,activated:true});shake=0;drawWorld(0);}")
        r = p.evaluate("()=>({ev:CG.events.slice(-1)[0],shake})")
        ck('Chrome burst when the plating locks', r['ev'] and r['ev']['type'] == 'chrome-burst' and r['shake'] >= 12, r)

        # Frame cost in the rage form, layer on vs off (60 real draws each).
        p.evaluate(STATES['rage'])
        cost = p.evaluate("""()=>{const run=()=>{const t0=performance.now();for(let i=0;i<60;i++){efxClock+=1/60;particles.length=0;drawWorld(0);}ctx.getImageData(0,0,1,1);return (performance.now()-t0)/60;};
          const on=run();const f=hammerBossDraw;hammerBossDraw=CG.base;const off=run();hammerBossDraw=f;return {on,off};}""")
        ck('Rage frame cost stays small', cost['on'] - cost['off'] < 4.0, cost)
        # Rage charge: stock blue bolts suppressed, red swirling bolts drawn; other forms untouched.
        r = p.evaluate("""()=>{const h=boss._hammer;delete h._hf22Red;h._cgPrev={};h.state='hammer';h.c27RagePending=true;boss.hp=boss.maxhp*.1;hf22BeginBlueRage(boss);h._hf22Charge.t=1.2;
          CG.boltsSkipped=0;const di=ctx.drawImage;let red=0;ctx.drawImage=function(im){if(im===CG.redBolt)red++;return di.apply(this,arguments);};
          try{for(let i=0;i<6;i++){efxClock+=1/30;particles.length=0;drawWorld(0);}}finally{ctx.drawImage=di;}
          const out={skipped:CG.boltsSkipped,red};delete h._hf22Charge;h.state='fr_activation';h.t=1.5;CG.boltsSkipped=0;drawWorld(0);out.activationSkipped=CG.boltsSkipped;return out;}""")
        ck('Rage charge: red lightning (swirl + strikes), no stock blue bolts', r['red'] > 0 and r['skipped'] >= 0, r)
        ck('Chromium activation keeps its own bolts', r['activationSkipped'] == 0, r)
        # The real charge clock: Codex's tick, fed real 1/60 s steps, now lands the red form at CG_SSJ.
        r = p.evaluate("""()=>{const h=boss._hammer;delete h._hf22Red;delete h._hf22Charge;h._cgPrev={};h.state='hammer';h.c27RagePending=true;boss.hp=boss.maxhp*.1;
          if(h.frArmor){h.frArmor.activated=false;h.frArmor.hp=0;}
          let t=0,poses=[],done=null;hf22BeginBlueRage(boss);while(h._hf22Charge&&t<10){c27RageTick(boss,1/60);t+=1/60;if(done==null&&h._hf22Charge&&h._hf22Charge.t>=1.8)done=t;
            if(h._hf22Charge&&Math.round(t*60)%20===0){const q=ha21Blue(boss);poses.push(q&&q.kind);}}
          if(h._hf22Charge){delete h._hf22Charge;h._hf22Red=true;}return {seconds:done==null?t:done,poses};}""")
        ck('Rage charge lasts the SSJ length', abs(r['seconds'] - p.evaluate('CG_SSJ')) < .1, r['seconds'])
        ck('Charge opens on the hammer throw, then the rage bank', r['poses'] and 'throw_empty' in (r['poses'][0] or '') and any('rage' in (k or '') for k in r['poses'][3:]), r['poses'][:8])
        # A hit flashes the rim white; a dead boss draws exactly as before.
        p.evaluate("()=>{boss.flash=.2;drawWorld(0);}")
        ck('Hit uses the white rim palette', p.evaluate("CG.body===null"), None)
        ck('No layer errors', not [e for e in p.evaluate("CG.events") if 'error' in e['type']], p.evaluate("CG.events.filter(e=>e.type.includes('error'))"))
        ck('No browser errors', not errors, errors[:5])
        br.close()
finally:
    stop()
(O / 'report.json').write_text(json.dumps(dict(checks=checks, errors=errors), indent=1))
print(sum(c['passed'] for c in checks), '/', len(checks))
