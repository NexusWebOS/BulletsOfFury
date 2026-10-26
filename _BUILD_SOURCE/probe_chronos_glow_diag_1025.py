"""Diagnostic: what Chronos actually draws in each form (before the glow pass).

Renders the live fight in real Chromium in each state and records every image
hammerBossDraw puts on the canvas (key, size, destination), so the aura layer
can attach to the body plates and nothing else.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from shoot import serve, TRAP_RAF

R = Path(__file__).resolve().parents[1]
O = R / '_shots/chronos_glow_1025/diag'
O.mkdir(parents=True, exist_ok=True)
errors = []

SETUP = """()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});
spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;
for(const w of ['c32Warm','c30Warm','c29Warm','bi24Warm','ht23Warm','c25Warm','c26Warm','c27Warm','ch23Warm'])
  if(typeof window[w]==='function')window[w]();}"""
READY = """()=>{stageLoadTick();return [stageLoadReady(5),c32Warm(),c30Warm(),c29Warm(),bi24Warm(),ht23Warm(),ch23Warm(),c25Warm(),c26Warm(),c27Warm()].every(Boolean)}"""

TRACE = """()=>{
 if(window.__gd)return;window.__gd={on:false,log:[]};
 const get=XART.get;XART.get=function(k){const im=get.apply(this,arguments);if(im&&typeof k==='string')try{im.__k=k}catch(e){}return im;};
 const di=ctx.drawImage;ctx.drawImage=function(im){if(__gd.on){const a=[...arguments];
   const m=ctx.getTransform();__gd.log.push({k:im.__k||('canvas'+(im.width||0)+'x'+(im.height||0)),n:a.length,
   w:a.length>=9?a[7]:a[3],h:a.length>=9?a[8]:a[4],op:ctx.globalCompositeOperation,al:+ctx.globalAlpha.toFixed(2),sx:+m.a.toFixed(2)});}
   return di.apply(this,arguments);};
 const hd=hammerBossDraw;window.hammerBossDraw=hammerBossDraw=function(){__gd.on=true;try{return hd.apply(this,arguments)}finally{__gd.on=false}};
}"""

STATES = {
    'regular_idle': "()=>{const h=boss._hammer;h.state='hammer';h.t=1;h._hf22Red=false;delete h._hf22Charge;const A=fr27Armor(boss);if(A){A.activated=false;A.hp=0;}}",
    'chrome_activation_1.2': "()=>{const h=boss._hammer;h.hb20Pickup=null;h.state='fr_activation';h.t=1.2;}",
    'chrome_activation_2.4': "()=>{const h=boss._hammer;h.state='fr_activation';h.t=2.4;}",
    'chrome_idle': "()=>{const h=boss._hammer;h.state='hammer';h.t=1;boss._hammer.frArmor=Object.assign(boss._hammer.frArmor||{},{hp:1000,max:1000,activated:true});}",
    'rage_charge_0.4': "()=>{const h=boss._hammer;const A=fr27Armor(boss);if(A){A.activated=false;A.hp=0;}h.state='hammer';h._hf22Red=false;h.c27RagePending=true;boss.hp=boss.maxhp*.1;hf22BeginBlueRage(boss);h._hf22Charge.t=.4;}",
    'rage_charge_1.5': "()=>{const h=boss._hammer;if(h._hf22Charge)h._hf22Charge.t=1.5;}",
    'rage_idle': "()=>{const h=boss._hammer;delete h._hf22Charge;h._hf22Red=true;h.rage=999;h.state='hammer';h.t=1;}",
}

port, stop = serve(str(R))
report = {}
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(channel='msedge', args=['--autoplay-policy=no-user-gesture-required'])
        p = br.new_page(viewport={'width': 1280, 'height': 800})
        p.on('pageerror', lambda e: errors.append(str(e)))
        p.on('console', lambda m: errors.append(m.text) if m.type == 'error' or 'draw error' in m.text else None)
        p.goto(f'http://127.0.0.1:{port}/index.html')
        p.wait_for_function("window.__bofFrames>5&&typeof c32Warm==='function'", timeout=180000)
        p.mouse.click(3, 3)
        p.evaluate(TRAP_RAF)
        p.evaluate(SETUP)
        p.wait_for_function(READY, timeout=180000)
        p.evaluate(TRACE)
        p.evaluate("()=>{boss.x=340;boss.y=260;boss.flash=0;}")
        for name, js in STATES.items():
            p.evaluate(js)
            p.evaluate("()=>{boss.x=340;boss.y=260;boss.flash=0;__gd.log=[];drawWorld(0);}")
            report[name] = p.evaluate("()=>__gd.log")
            p.screenshot(path=str(O / (name + '.png')))
        br.close()
finally:
    stop()
(O / 'report.json').write_text(json.dumps(dict(report=report, errors=errors), indent=1))
for k, v in report.items():
    print(k, [(e['k'], e['w'], e['h'], e['op']) for e in v][:8])
print('errors', errors[:5])
