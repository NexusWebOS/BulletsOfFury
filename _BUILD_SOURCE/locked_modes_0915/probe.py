"""Real Chromium proof for locked Boss Rush / Time Attack mode cards."""
import base64, json, sys, threading, http.server
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'_shots'/'locked_modes_0915'
OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'))
import capture3
from playwright.sync_api import sync_playwright
from PIL import Image

def main():
    checks,errors,shots=[],[],[]
    def ok(value,label):
        checks.append({'pass':bool(value),'label':label})
        print(('ok  ' if value else 'FAIL ')+label,flush=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT),**kwargs)
        def log_message(self,*args): pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    with sync_playwright() as pw:
        browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
        page=browser.new_page(viewport={'width':1100,'height':1200})
        page.on('pageerror',lambda e: errors.append('page '+str(e)))
        page.on('console',lambda m: errors.append('console '+m.text) if m.type=='error' else None)
        page.goto(f'http://127.0.0.1:{server.server_port}/index.html',wait_until='load',timeout=120000)
        page.wait_for_function('() => (window.__bofFrames|0)>4',timeout=120000)
        page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB)
        page.evaluate("""() => {
          window.__modeProbe={locks:0,panels:[],blocked:0};
          const ml=modeLockDraw;modeLockDraw=function(r){const q=ml.apply(this,arguments);if(q)window.__modeProbe.locks++;return q;};
          const mp=modePanelDraw;modePanelDraw=function(it,cx,cy,pw,locked){const q=mp.apply(this,arguments);window.__modeProbe.panels.push({mode:it.mode,locked:!!locked,rect:q});return q;};
          const old=Audio.SFX.blocked;Audio.SFX.blocked=function(){window.__modeProbe.blocked++;if(old)old();};
          try{localStorage.removeItem(BONUS_MODE_UNLOCK_KEY);}catch(e){}bonusModesUnlocked=false;
          setState(GS.MODESEL);modeIndex=3;stateT=1;
        }""")
        def step(n):
            for i in range(0,n,20):
                page.evaluate('n=>window.__step(n)',min(20,n-i));page.wait_for_timeout(20)
        def ready():
            return page.evaluate("() => ['mode_boss_rush_0915','mode_time_attack_0915','mode_lock_nexus_0915'].every(k=>XART.rdy(k))")
        for _ in range(180):
            if ready():break
            page.wait_for_timeout(35)
        ok(ready(),'both generated mode cards and the exact Nexus lock decode')

        def capture(name):
            page.evaluate('() => {window.__modeProbe.locks=0;window.__modeProbe.panels=[];drawModeSelect(0);}')
            png=page.evaluate("() => document.querySelector('#screen').toDataURL('image/png').split(',')[1]")
            path=OUT/f'{name}.png';path.write_bytes(base64.b64decode(png));shots.append(path)
            return page.evaluate("() => JSON.parse(JSON.stringify({state,modeIndex,locks:window.__modeProbe.locks,panels:window.__modeProbe.panels,deny:drawModeSelect._deny||null,blocked:window.__modeProbe.blocked,unlocked:bonusModesUnlocked}))")

        locked_boss=capture('boss_rush_locked')
        page.evaluate("() => {modeIndex=4;}")
        locked_time=capture('time_attack_locked')
        ok(locked_boss['locks']==2 and locked_time['locks']==2,'both final-clear modes carry the visible Nexus chain layer')
        ok(len(locked_boss['panels'])==5 and all(p['rect'] for p in locked_boss['panels']),'all five authored cards draw in one menu frame')
        ys=[p['rect']['y'] for p in locked_boss['panels']]
        bottoms=[p['rect']['y']+p['rect']['h'] for p in locked_boss['panels']]
        ok(all(bottoms[i]<ys[i+1]+22 for i in range(4)) and bottoms[-1]<470,'five-card layout stays clear of adjacent cards and the hint bar')

        page.evaluate("() => {modeIndex=3;stateT=1;Input.injectTap('enter');}")
        step(2)
        denied=page.evaluate("() => ({state,blocked:window.__modeProbe.blocked,text:drawModeSelect._deny&&drawModeSelect._deny.text})")
        ok(denied['state']=='modesel' and denied['blocked']==1 and denied['text']=='CLEAR CAMPAIGN TO UNLOCK','confirming a locked card stays put and plays the denial alert')

        unlocked=page.evaluate("""() => {
          run.mode='campaign';run.stage=CAMPAIGN_STAGES;const earned=bonusModesUnlockFromCampaign();
          return {earned,stored:localStorage.getItem(BONUS_MODE_UNLOCK_KEY),boss:modeItemUnlocked(MODE_ITEMS[3]),time:modeItemUnlocked(MODE_ITEMS[4])};
        }""")
        ok(unlocked=={'earned':True,'stored':'1','boss':True,'time':True},'a final Campaign clear reveals both modes and persists the account gate')
        page.evaluate("() => {modeIndex=3;drawModeSelect._deny=null;}")
        revealed=capture('bonus_modes_revealed')
        ok(revealed['locks']==0 and revealed['unlocked'],'the revealed cards restore full color and remove both chain overlays')
        page.evaluate("() => {stateT=1;Input.injectTap('enter');}");step(2)
        deferred=page.evaluate("() => ({state,blocked:window.__modeProbe.blocked,text:drawModeSelect._deny&&drawModeSelect._deny.text})")
        ok(deferred['state']=='modesel' and deferred['blocked']==2 and deferred['text']=='MODE DEVELOPMENT IN PROGRESS','revealed card cannot enter the unfinished ACH-14 route')

        for path in shots:
            im=Image.open(path).convert('RGB')
            ok(im.size==(960,1024) and im.getbbox() is not None,f'{path.stem} is a non-empty native game frame')
        dims=page.evaluate("() => Object.fromEntries(['mode_boss_rush_0915','mode_time_attack_0915','mode_lock_nexus_0915'].map(k=>{const im=XART.get(k);return [k,[im.naturalWidth,im.naturalHeight]];}))")
        ok(dims['mode_boss_rush_0915']==[2170,725] and dims['mode_time_attack_0915']==[2170,725] and dims['mode_lock_nexus_0915']==[1100,614],'Chromium decodes the two full generated plates and exact 1100x614 Nexus source')
        ok(not errors,'zero Chromium page or console errors')
        browser.close()
    server.shutdown()
    result={'checks':checks,'errors':errors,'shots':[str(p.relative_to(ROOT)) for p in shots]}
    (OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(c['pass'] for c in checks)
    print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)

if __name__=='__main__':main()
