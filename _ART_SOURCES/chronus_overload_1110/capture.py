from pathlib import Path
import sys,functools,http.server,threading,json,base64,io,argparse
sys.dont_write_bytecode=True
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
WORK=Path(__file__).resolve().parent
OUT=WORK.parents[1]/'outputs/chronus-overload'
OUT.mkdir(parents=True,exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--candidate',action='store_true');ap.add_argument('--installed',action='store_true');args=ap.parse_args()
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
    def translate_path(self,path):
        path=path.split('?')[0]
        if args.candidate and path.startswith('/assets/game/levels/stage_05/boss/chronus_electric_1110/'):
            return str(WORK/'candidate/frames'/path.rsplit('/',1)[1])
        return super().translate_path(path)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT)))
server.daemon_threads=True
threading.Thread(target=server.serve_forever,daemon=True).start()
errors=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(channel='msedge',headless=True,args=['--mute-audio'])
    page=browser.new_page(viewport={'width':1100,'height':1000},device_scale_factor=1)
    page.set_default_timeout(180000)
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(f'http://127.0.0.1:{server.server_address[1]}/index.html',wait_until='domcontentloaded')
    page.wait_for_function('window.__bofFrames>4&&typeof HF17!=="undefined"')
    page.evaluate(shoot.TRAP_RAF)
    page.add_script_tag(content=(ROOT/'_BUILD_SOURCE/balance_lab_1007.js').read_text(encoding='utf-8'))
    page.evaluate("""()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='campaign';startRun(5);BAL7.setup({stage:5,kind:'chromehammer',pilot:'cole',diff:'normal',seconds:120,fire:false});hf17Warm();h3Warm();furyShipWarm();}""")
    page.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(5).ready&&hf17Warm()&&furyShipReady()&&XART.rdy("h3_earth");}',polling=50)
    if args.candidate:
        code=(WORK/'candidate/hammer_finale_1017.js').read_text(encoding='utf-8')
        patch=code[code.index('const CE110'):code.index('stageLoadBegin=function')]
        patch+=code[code.index('function hf17Phase'):code.index('h3EndingStart=function')]
        patch+=code[code.index('h3EndingTick=function'):code.index('function hf17Cell')]
        patch+=code[code.index('function hf17Actor(e)'):code.index('function hf17Missile(F)')]
        page.add_script_tag(content=patch)
        page.wait_for_function('ce110Warm()',polling=50)
    page.evaluate("""()=>{BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;AP10_X.intro=null;P2M.active=null;FS11.pending=null;FS11.boxes=[];B.x=worldWidth()/2;B.y=VH*.31;B.enter=B.dead=B._noHit=false;B._hammer.state='storm_raise';B._hammer.t=2;player.x=B.x;player.y=VH*.81;player.dead=player.out=false;player.invuln=99999;camX=clamp(player.x-VW/2,0,worldWidth()-VW);eBullets=[];pBullets=[];enemies=[];l5Rocks=[];l5RockT=999;stagePlan=[];B.hp=0;bossDie();if(window.__bofFit)__bofFit();SC12.refresh();}""")
    # Capture the entire buildup so outward illumination and flashing remain visible.
    print('Capture starting',page.evaluate('H3.ending?.hf17?.phase'),flush=True)
    frames=[];timeline=[]
    for i in range(340):
        err=page.evaluate(shoot.STEP,4)
        if err:raise RuntimeError(err)
        if i%5==0:page.wait_for_timeout(3)
        q=page.evaluate('({phase:H3.ending?.hf17?.phase,t:H3.ending?.hf17?.t,impacts:H3.ending?.hf17?.impacts,core:H3.ending?.hf17?.core,events:HF17.events,loopClock:ce110Loop(H3.ending?.hf17?.age||0),age:H3.ending?.hf17?.age,overload:CO110.stats,stats:typeof CE110!=="undefined"?CE110.stats:null})')
        timeline.append(q)
        encoded=page.evaluate("document.querySelector('#screen').toDataURL('image/png').split(',')[1]")
        im=Image.open(io.BytesIO(base64.b64decode(encoded))).convert('RGB')
        frames.append(im.resize((480,512),Image.Resampling.NEAREST))
        if (args.candidate or args.installed) and q['phase']=='burst' and .4<=q['t']<=.47:frames[-1].save(WORK/'after-peak.png')
        if (args.candidate or args.installed) and q['phase']=='burst' and 1.05<=q['t']<=1.12:frames[-1].save(WORK/'after-collapse.png')
        if q['phase']=='engulf' and .9<q['t']<1.0:frames[-1].save(WORK/'electric-charge.png')
        if q['phase']=='burst' and 2.0<q['t']<2.1:frames[-1].save(WORK/'electric-shatter.png')
        if q['phase']=='engulf' and any(abs(q['t']-target)<.035 for target in [0.3,1.1,2.1,3.5,4.8]):frames[-1].save(WORK/('overload-'+str(round(q['t'],1))+'.png'))
        if q['phase']=='after':break
    name='installed' if args.installed else 'after' if args.candidate else 'before'
    browser.close()
    start=next(i for i,q in enumerate(timeline) if q['phase']=='missile')
    clip=frames[start:];contact=Image.new('RGB',(480*4,512*4))
    for i in range(16):contact.paste(clip[round(i*(len(clip)-1)/15)],(i%4*480,i//4*512))
    pal=contact.quantize(colors=192,method=Image.Quantize.MEDIANCUT)
    gif=[im.quantize(palette=pal,dither=Image.Dither.NONE) for im in clip]
    gif[0].save(OUT/'chronus-overload.gif',save_all=True,append_images=gif[1:],duration=[70 if i%3 else 60 for i in range(len(gif))],loop=0,optimize=True)
    (OUT/f'{name}-capture.json').write_text(json.dumps({'source':'native current game rendered in Chromium; final-defeat checkpoint','frames':len(frames),'canvas':frames[0].size,'errors':errors,'timeline':timeline},indent=2))
    for i in [0,30,50,65,80,95]:
        if i<len(frames):frames[i].save(WORK/f'{name}-{i:03}.png')
    print(name,len(frames),frames[0].size,'errors',errors,flush=True)
server.shutdown()
