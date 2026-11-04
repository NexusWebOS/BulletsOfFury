"""Film every distinct projectile through the real game for the projectile gallery.

    python _BUILD_SOURCE/capture_projectile_gallery_1103.py [--tag before|after] [--quick]

Two passes on one page: the PRIME pass runs every case so each projectile's art is requested
(XART loads lazily, and a first-frame capture would otherwise film the procedural fallback), then
the CAPTURE pass reruns the same seeded cases and films the first instance of each signature.
Output: _shots/projectiles_1103/<tag>/strips/*.webp + catalog.json. QA evidence only.
"""
from pathlib import Path
import json, sys, base64, argparse, http.server, time
from playwright.sync_api import sync_playwright
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / '_BUILD_SOURCE')); import shoot
A = argparse.ArgumentParser(); A.add_argument('--tag', default='before'); A.add_argument('--quick', action='store_true')
A.add_argument('--off', default='', help='window flag set before boot, e.g. PG1103_OFF')
args = A.parse_args()
O = R / '_shots/projectiles_1103' / args.tag; (O / 'strips').mkdir(parents=True, exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None

BOSSES = ['damkeeper','infernoreaver','cryospear','stormsovereign','xenoregent','warhive','sludgeemperor','vileexistence','tidalfusion']
MINIS = ['razorback','magmaward','frostcruiser','olivewarden','spacebomber','siegebomber','dualscoopdredger','heralddeath','voidhorizon']
def enemy_cases():
    out = []
    for st in range(1, 10):
        # long enough to reach later attack phases and the stage's later waves
        out.append(dict(stage=st, kind=MINIS[st-1], mini=True, diff='furious', secs=36))
        out.append(dict(stage=st, kind=BOSSES[st-1], diff='furious', secs=50))
        out.append(dict(stage=st, kind=BOSSES[st-1], diff='furious', slice=True, secs=70))
    out.append(dict(stage=6, kind='rebelsquad', diff='furious', secs=20))
    if args.quick: out = out[:4]
    for i, c in enumerate(out):
        c['id'] = f"e{i:02}-s{c['stage']}-{c['kind']}" + ('-mini' if c.get('mini') else '') + ('-stage' if c.get('slice') else '') + ('-ace' if c.get('ace') else '')
        c.update(pilot='yuri', level=3)
    return out
def player_cases(pilots):
    out = []
    for pilot in pilots:
        for w in range(8):
            out.append(dict(pilot=pilot, weapon=w, level=3))
    for lv in (1, 5):
        for w in range(9):
            out.append(dict(pilot='yuri', weapon=w, level=lv))
    for lv in (1, 3, 5): out.append(dict(pilot='yuri', weapon=8, level=lv))
    for lv in (1, 3, 5):
        for sw in range(3): out.append(dict(pilot='yuri', weapon=0, level=lv, stage=5, space=sw, spaceWeapon=sw))
    for ml in (1, 3, 5): out.append(dict(pilot='cole', weapon=0, level=3, missileLevel=ml))
    for pilot in pilots: out.append(dict(pilot=pilot, weapon=0, level=5, charge=True))
    if args.quick: out = out[:6]
    for i, c in enumerate(out):
        c.setdefault('stage', 1); c.update(kind='damkeeper', diff='normal')
        c['id'] = f"p{i:03}-{c['pilot']}-w{c['weapon']}-L{c['level']}" + (f"-space{c['space']}" if 'space' in c else '') + (f"-m{c['missileLevel']}" if 'missileLevel' in c else '') + ('-charge' if c.get('charge') else '')
    return out

report = {'errors': [], 'cases': 0}
catalog = []
port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
        ctxb = br.new_context(viewport={'width': 1100, 'height': 950})
        # no route() interceptor: it makes Python answer every request, and a synchronous request
        # issued from inside a long evaluate() deadlocks (browser waits on Python, Python on browser).
        # The game is served locally and makes no outside requests.
        p = ctxb.new_page(); p.set_default_timeout(180000)
        p.on('pageerror', lambda e: report['errors'].append(str(e)[:300]))
        if args.off: p.add_init_script(f'window.{args.off}=1;')
        p.goto(f'http://127.0.0.1:{port}/index.html', timeout=180000)
        p.wait_for_function('()=>window.__bofFrames>4'); p.evaluate(shoot.TRAP_RAF)
        for f in ['balance_lab_1007.js', 'projectile_lab_1007.js', 'projectile_gallery_1103.js']:
            p.add_script_tag(path=str(R / '_BUILD_SOURCE' / f))
        pilots = p.evaluate('()=>PILOTS.map(p=>p.key)')
        EC, PC = enemy_cases(), player_cases(pilots)
        RC = [dict(id=f'r{st}-s{st}-registry', stage=st, kind=BOSSES[st-1], diff='furious', pilot='yuri', level=3) for st in range(1, 10)]
        if args.quick: RC = RC[:1]

        def pump(n=24, gap=25):
            # The game's image queue advances inside its own loop(), which TRAP_RAF holds. Run the
            # trapped loop for a few real frames with wall time between them so queued art decodes.
            for _ in range(n):
                p.evaluate('()=>{const cb=window.__bofPendingRAF;window.__bofPendingRAF=null;if(cb)cb(performance.now());}')
                p.wait_for_timeout(gap)
        def unfilmed(js, arg=None):
            p.evaluate('()=>{PG3._was=PG3.prime;PG3.prime=true;}'); p.evaluate(js, arg); p.evaluate('()=>{PG3.prime=PG3._was;PG3.live=[];}')
        def run_enemy(c):
            # Changing stage releases the previous stage's art (asset_memory_1007), so in the capture
            # pass each fight is first run unfilmed and pumped, then rerun from the top and filmed.
            if not PRIME[0]:
                p.evaluate('c=>PG3.enemyCase(c)', c)
                unfilmed('n=>{for(let i=0;i<n;i++)PG3.enemySteps(30);}', c['secs'] * 2); pump(60, 45)
            p.evaluate('c=>PG3.enemyCase(c)', c)
            for _ in range(c['secs'] * 2): p.evaluate('()=>PG3.enemySteps(30)')
            p.evaluate('()=>PG3.end()')
        def run_player(c):
            p.evaluate('c=>PG3.playerCase(c)', c)
            # warm-up: the first shots request their art without being filmed, then the page gets
            # wall time to decode it (stepping is synchronous, so a fresh image never lands mid-chunk)
            p.evaluate('ch=>{const was=PG3.prime;PG3.prime=true;PG3.playerSteps(20,ch);PG3.prime=was;}', bool(c.get('charge')))
            pump()
            for _ in range(5): p.evaluate('ch=>PG3.playerSteps(60,ch)', bool(c.get('charge')))
            p.evaluate('()=>PG3.end()')
        def run_registry(c):
            kinds = p.evaluate('c=>PG3.registryCase(c)', c)
            if not PRIME[0]:
                unfilmed('ks=>{for(const k of ks)PG3.registryFire(k,12);}', kinds); pump(60, 45)
            for k in kinds: p.evaluate('k=>PG3.registryFire(k,50)', k)
            p.evaluate('()=>PG3.end()')
        RUN = {'e': lambda c: run_enemy(c), 'p': lambda c: run_player(c), 'r': lambda c: run_registry(c)}
        def safe(fn, c):
            try: fn(c)
            except Exception as e:
                report['errors'].append(c['id'] + ': ' + str(e)[:300]); print('ERR', c['id'], str(e)[:200], flush=True)
                try: p.evaluate('()=>{PG3.live=[];ctx.setTransform(1,0,0,1,0,0);}')
                except Exception: pass

        # PRIME
        PRIME = [True]
        p.evaluate('()=>{PG3.prime=true;}')
        for c in EC + PC + RC: safe(RUN[c['id'][0]], c)
        print('PRIMED', p.evaluate('()=>Object.keys(PG3.caps).length'), flush=True)
        pump(150, 40)
        p.evaluate('()=>{PG3.prime=false;PG3.caps={};PG3.order=[];}'); PRIME[0] = False
        # CAPTURE
        for c in EC + PC + RC:
            safe(RUN[c['id'][0]], c)
            for cap in p.evaluate('()=>PG3.flush()'):
                i = len(catalog); name = f'{i:04}.webp'
                (O / 'strips' / name).write_bytes(base64.b64decode(cap.pop('strip').split(',', 1)[1]))
                cap['file'] = 'strips/' + name; cap.pop('sent', None); catalog.append(cap)
            report['cases'] += 1
            print('CASE', c['id'], len(catalog), flush=True)
            if report['cases'] % 10 == 0:
                (O / 'catalog.json').write_text(json.dumps({'crop': 128, 'ss': 2, 'fps': 30, 'items': catalog, 'report': report}) + '\n')
        br.close()
finally:
    stop()
(O / 'catalog.json').write_text(json.dumps({'crop': 128, 'ss': 2, 'fps': 30, 'items': catalog, 'report': report}) + '\n')
print('DONE', len(catalog), 'errors', len(report['errors']), flush=True)
