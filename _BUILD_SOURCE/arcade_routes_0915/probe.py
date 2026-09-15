"""Exercise Arcade route boundaries with the real renderer and real confirm input."""
import base64, hashlib, json, sys
from pathlib import Path
R = Path(__file__).resolve().parents[2]
O = R / '_shots/arcade_routes_0915'
O.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(R / '_BUILD_SOURCE'))
import shoot
sys.path.insert(0, str(R / '_BUILD_SOURCE/trailer_v7'))
import capture3
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
checks, errors, shots = [], [], []
def ok(value, name):
    checks.append({'name': name, 'ok': bool(value)})
    print(('ok  ' if value else 'FAIL ') + name, flush=True)
port, stop = shoot.serve(str(R))
with sync_playwright() as p:
    b = p.chromium.launch(args=['--no-sandbox', '--mute-audio', '--autoplay-policy=no-user-gesture-required'])
    pg = b.new_page(viewport={'width': 1100, 'height': 1000})
    pg.on('pageerror', lambda e: errors.append('page ' + str(e)))
    pg.on('console', lambda m: errors.append('console ' + m.text) if m.type == 'error' else None)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
    pg.wait_for_function('()=>(window.__bofFrames|0)>4', timeout=120000)
    pg.evaluate(shoot.TRAP_RAF)
    pg.evaluate(capture3.LIB)
    pg.evaluate("()=>{__auto=function(){};debugFight=null;_coleScene=0;coopOn=false;diffKey='normal';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');}")
    def step(n):
        for i in range(0, n, 20):
            pg.evaluate('n=>__step(n)', min(20, n-i))
            pg.wait_for_timeout(12)
    def enter():
        pg.keyboard.down('Enter'); step(1)
        pg.keyboard.up('Enter'); step(1)
    def shot(name):
        path = O / (name + '.png')
        path.write_bytes(base64.b64decode(pg.evaluate("()=>document.querySelector('#screen').toDataURL().split(',')[1]")))
        shots.append(path)
    def clear():
        pg.evaluate("()=>{setState(GS.STAGECLEAR);drawStageClear._init=false;}")
        step(20); enter(); step(2); enter()
    pg.evaluate("()=>{run.mode='arcade';run._s5Resume={t:999};run._s5ResumeArm=1;run._l78Entry=1;startRun(1);__auto=function(){};}")
    ok(pg.evaluate("()=>state===GS.INTRO&&!run._s5Resume&&!run._s5ResumeArm&&!run._l78Entry"), 'fresh Arcade starts at Stage 1 card and clears old detour state')
    for stage in range(1, 8):
        pg.evaluate("n=>{run.mode='arcade';beginStage(n);run.contUsed=2;run.lives=4;run.bombs=17;}", stage)
        clear()
        ok(pg.evaluate("n=>run.stage===n+1&&state===GS.INTRO&&run.mode==='arcade'&&run.contUsed===2&&run.lives===4&&run.bombs===17", stage), 'Stage %d results confirm reaches next card with stocks intact' % stage)
        if stage in (1, 4, 7):
            for _ in range(100):
                if pg.evaluate('()=>XART.rdy("scard_"+run.stage)'): break
                pg.wait_for_timeout(30)
            step(55); shot('after_stage_%d' % stage)
    pg.evaluate("()=>{run.mode='arcade';campaign._l78Pending=1;run._l78Entry=1;beginStage(8);}")
    ok(pg.evaluate("()=>state===GS.INTRO&&!run._l78Entry&&campaign._l78Pending===1"), 'Arcade ignores and preserves pending campaign rift entrance')
    pg.evaluate("()=>{proceedIntro();}")
    ok(pg.evaluate('()=>state===GS.LAUNCH'), 'Arcade Stage 8 card proceeds to ordinary launch')
    pg.evaluate("()=>{run.mode='campaign';beginStage(8);}")
    ok(pg.evaluate('()=>state===GS.WARPENTRY&&run._l78Entry===1&&campaign._l78Pending===0'), 'Campaign still consumes its own Stage 8 rift entrance')
    pg.evaluate("()=>{run.mode='arcade';beginStage(5);stageTimer=123;scroll=456;spawnClock=7;waveIdx=3;run.contUsed=2;run.bombs=17;s9WarpStart();s9warp.ph='white';s9warp.t=S9W_WHITE;s9WarpTick(0);}")
    ok(pg.evaluate("()=>run.stage===9&&state===GS.INTRO&&run._s5Resume.t===123&&run._s5Resume.scroll===456&&run.spaceMode&&run.gravityShipReady"), 'earned secret gate enters Stage 9 directly with ship ready and Stage 5 saved')
    clear()
    ok(pg.evaluate("()=>run.stage===5&&state===GS.INTRO&&stageTimer===123&&scroll===456&&spawnClock===7&&waveIdx===3&&!run._s5Resume&&run._s9taken===1&&run.contUsed===2&&run.bombs===17"), 'bonus results restore exact Stage 5 clock/scroll/wave without refunding resources')
    # Password Stage 9 has no previous level to resume and follows the existing Stage 6 fallback.
    pg.evaluate("()=>{startRun(9);__auto=function(){};}")
    clear()
    ok(pg.evaluate("()=>run.stage===6&&state===GS.INTRO&&run.mode==='arcade'"), 'password bonus clear proceeds to Stage 6 without campaign map')
    pg.evaluate("()=>{run.mode='campaign';beginStage(5);s9WarpStart();s9warp.ph='white';s9warp.t=S9W_WHITE;s9WarpTick(0);}")
    ok(pg.evaluate("()=>state===GS.STAGESEL"), 'Campaign secret gate retains its map route')
    pg.evaluate("()=>{run.mode='arcade';beginStage(1);storyPlay(1,'boss');}")
    ok(pg.evaluate('()=>story===null'), 'Arcade clears old radio and suppresses scripted boss dialogue')
    pg.evaluate("()=>{run.mode='arcade';beginStage(8);run.score=12345;}")
    clear()
    ok(pg.evaluate('()=>state===GS.VICTORY&&drawVictory._ready'), 'final Arcade results reach score ending without cinematic loading gate')
    step(240); shot('arcade_final_score')
    step(90); enter()
    ok(pg.evaluate('()=>state===GS.TITLE'), 'real confirm returns from Arcade final card to title')
    # The ordinary Stage 5 launch remains the authored transformation, not a direct PLAY jump.
    pg.evaluate("()=>{run.mode='arcade';startRun(5);__auto=function(){};proceedIntro();}")
    ok(pg.evaluate('()=>state===GS.LAUNCH&&run.spaceMode&&run.gravityShipReady===false'), 'fresh Stage 5 retains its authored transformation launch')
    loop_error = pg.evaluate('()=>window.__err||null')
    ok(not errors and not loop_error, 'zero page, console and controlled-loop errors')
    b.close()
stop()
board = Image.new('RGB', (960, 570), '#10131c')
d = ImageDraw.Draw(board)
for i, path in enumerate(shots):
    im = Image.open(path).convert('RGB'); im.thumbnail((240, 540))
    board.paste(im, (i*240, 25)); d.text((i*240+6, 5), path.stem, fill='white')
board.save(O / 'contact.png')
result = {'runtimeSha256': hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest(), 'checks': checks, 'errors': errors, 'loopError': loop_error, 'screenshots': [str(s) for s in shots]}
(O/'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
n = sum(c['ok'] for c in checks)
print('%d passed / %d failed' % (n, len(checks)-n), flush=True)
if n != len(checks): raise SystemExit(1)
