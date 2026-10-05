"""Chromium pixel review of Stage 6-8 authored hit silhouettes."""
from pathlib import Path
import base64, io, json, sys, traceback
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright
import shoot as sh

R = Path(__file__).resolve().parents[1]
O = R / '_shots/flash_palette_1004'
O.mkdir(parents=True, exist_ok=True)
SETUP = (R / '_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
CASES = [
    ('stage6-siege', {'stage': 6, 'kind': 'siegebomber', 'mini': True}, 'B', 'B._bomber.mode="hold";'),
    ('stage6-warhive', {'stage': 6, 'kind': 'warhive'}, 'B', 'B._whv.st="hold";B._whv.cx=B.x;B._whv.cy=B.y;'),
    ('stage6-rebel', {'stage': 6, 'kind': 'rebelsquad'}, 'B._rebels.ships[0]', 'B._rebels.frIntro={done:true};B.enter=false;for(const q of B._rebels.ships){q.mode="fight";q.warp=0;q.x=player.x+(q.i-2)*104;q.y=175;XART.rdy("rr_ship_"+REBEL_SHIPS[q.i]);XART.rdy("rr_roll_"+REBEL_SHIPS[q.i]+"_0");}'),
    ('stage7-warden', {'stage': 7, 'kind': 'sludgeemperor'}, 'B', 's7mInit(B);B._s7mod.mode="fight";B._s7warden.noHit=false;'),
    ('stage8-herald', {'stage': 8, 'kind': 'heralddeath', 'mini': True}, 'B', 'B.enter=false;B._hd1003.mode="fight";'),
    ('stage8-alien', {'stage': 8}, 'E', 'window.E=spawnEnemy("s8leech",player.x,150,{});E._orbit1003.phase="orbit";'),
    ('stage8-dracula', {'stage': 8, 'kind': 'vileexistence'}, 'B', 'j3Encounter(B,2);B._r30.mode="fight";B.enter=false;'),
]

def screen(pg, name, save=True):
    pg.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
    path = O / (name + '.png')
    raw = base64.b64decode(pg.evaluate('()=>cv.toDataURL().split(",")[1]'))
    if save: path.write_bytes(raw)
    return Image.open(io.BytesIO(raw)).convert('RGB')

def flash_pixels(before, after):
    a, b = before.load(), after.load()
    changed = pale = 0
    for y in range(before.height):
        for x in range(before.width):
            p, q = a[x,y], b[x,y]
            if min(q[i]-p[i] for i in range(3)) > 20:
                changed += 1
                if max(q)-min(q) < 55 and min(q) > 130: pale += 1
    return {'brightened': changed, 'white': pale}

report = {'cases': [], 'errors': []}
port, stop = sh.serve(str(R))
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
        pg = browser.new_page(viewport={'width': 1100, 'height': 950})
        pg.on('pageerror', lambda e: report['errors'].append(str(e)))
        pg.on('console', lambda m: report['errors'].append(m.text[:500]) if m.type == 'error' else None)
        pg.goto(f'http://127.0.0.1:{port}/index.html', timeout=120000)
        pg.wait_for_function('()=>window.__bofFrames>4', timeout=120000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate('()=>{s81003Warm();r30Warm();whvWarm();hd1003Warm();for(const a of Object.values(FMC_ART))XART.rdy(a.key);}')
        pg.wait_for_function('()=>Object.values(FMC_ART).every(a=>XART.rdy(a.key))&&Object.keys(REALM30_ART).every(k=>XART.rdy("r30_"+k))', timeout=120000)
        for name, cfg, actor, init in CASES:
            if len(sys.argv)>1 and sys.argv[1] not in name: continue
            pg.evaluate(SETUP, cfg)
            pg.evaluate('()=>{' + init + 'window.__flashActor=' + actor + ';__flashActor.flash=0; if(__flashActor.parts)for(const q of __flashActor.parts)q.flash=0;}')
            if name == 'stage6-rebel':
                pg.wait_for_function('()=>B._rebels.ships.every(q=>XART.rdy("rr_ship_"+REBEL_SHIPS[q.i]))',timeout=120000)
            else: pg.wait_for_timeout(100)
            base = screen(pg, name + '-base')
            pg.evaluate('()=>{__flashActor.flash=.16;if(__flashActor.parts)for(const q of __flashActor.parts)q.flash=.16;}')
            hit = screen(pg, name + '-hit')
            stat = flash_pixels(base, hit)
            ok = stat['white'] > 70
            report['cases'].append({'name':name,'ok':ok,**stat})
            print(('PASS ' if ok else 'FAIL ') + name + ' ' + str(stat), flush=True)
        ordinary = {
            6: ['s6dart','s6mine','s6lancer','s6skimmer','s6thunder','s6probe','s6cyclone','s6buoy','s6turbine'],
            7: ['s7sampler','s7pipe','s7tank','s7skimmer','s7lamprey','s7mine','s7walker','s7canister','s7barge','s7serpent'],
            8: ['s8interceptor','s8needlejet','s8leech','s8scout','s8razor','s8manta','s8spread','s8deathorb','s8parasite','s8crescent','s8hunter','s8skull','s8solar','s8tentacle','s8symbiote','s8bomber','s8carrier','s8gunship'],
        }
        for stage, types in ordinary.items():
            for kind in types:
                name = f'stage{stage}-{kind}'
                if len(sys.argv)>1 and sys.argv[1] not in name: continue
                pg.evaluate(SETUP, {'stage':stage})
                pg.evaluate('(kind)=>{window.E=spawnEnemy(kind,player.x,180,{});if(E){E.x=player.x;E.y=180;E.flash=0;}}',kind)
                if stage==8: pg.wait_for_function('()=>XART.rdy("fr27_realm_fleet")',timeout=120000)
                pg.wait_for_timeout(80)
                base=screen(pg,name+'-base',False)
                pg.evaluate('()=>{if(E)E.flash=.16;}')
                hit=screen(pg,name+'-hit',False)
                stat=flash_pixels(base,hit)
                ok=stat['white']>35
                row={'name':name,'ok':ok,**stat}
                if not ok and stage==8:
                    row['debug']=pg.evaluate('()=>{const H=S8MEGA[E._s8mega],k=H.fixed?"s8nf_"+H.art+"_idle":"s8atk_"+H.art+"_0",im=XART.get(k),t=xartTint(k,"#ffffff",1);return{type:E.type,mega:E._s8mega,key:k,ready:XART.rdy(k),image:{w:im.width,nw:im.naturalWidth,h:im.height,nh:im.naturalHeight},tint:{w:t?.width,h:t?.height},flash:E.flash};}')
                report['cases'].append(row)
                if not ok:
                    base.save(O/(name+'-base.png'));hit.save(O/(name+'-hit.png'))
                print(('PASS ' if ok else 'FAIL ') + name + ' ' + str(row), flush=True)
        for stage, kind in [(6,'s6dart'),(7,'s7sampler'),(8,'s8carrier')]:
            name=f'native-hit-stage{stage}'
            if len(sys.argv)>1 and sys.argv[1] not in name: continue
            pg.evaluate(SETUP, {'stage':stage})
            pg.evaluate('(kind)=>{window.E=spawnEnemy(kind,player.x,180,{});E.x=player.x;E.y=180;}',kind)
            if stage==8: pg.wait_for_function('()=>XART.rdy("fr27_realm_fleet")',timeout=120000)
            pg.wait_for_timeout(100)
            base=screen(pg,name+'-base',False)
            state=pg.evaluate('()=>{const old=E.hp;hitEnemy(E,1);return {old,hp:E.hp,flash:E.flash};}')
            hit=screen(pg,name+'-hit',False)
            stat=flash_pixels(base,hit)
            ok=state['hp']<state['old'] and state['flash']>0 and stat['white']>35
            report['cases'].append({'name':name,'ok':ok,'damage':state,**stat})
            if not ok or stage==8: base.save(O/(name+'-base.png'));hit.save(O/(name+'-hit.png'))
            print(('PASS ' if ok else 'FAIL ')+name+' '+str(state)+' '+str(stat),flush=True)
        browser.close()
except Exception as e:
    report['fatal'] = str(e)
    traceback.print_exc()
finally:
    stop()
    (O/'flash_probe.json').write_text(json.dumps(report,indent=2), encoding='utf-8')
print('errors', report['errors'][:4], flush=True)
sys.exit(bool(report['errors']) or 'fatal' in report or any(not x['ok'] for x in report['cases']))
