"""Observe the native rewritten entrance and inspect real rendered pixels."""
from barrage_review_common_1025 import ROOT, boot
from shoot import serve, STEP
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
import json
import numpy as np

O = ROOT / '_shots/drone_rework_1026/probe'
O.mkdir(parents=True, exist_ok=True)
checks, errors, trace, shots = [], [], [], []
def ck(name, ok, data=None):
    checks.append({'name': name, 'passed': bool(ok), 'data': data})
    print(('PASS ' if ok else 'FAIL ') + name + ((' ' + json.dumps(data)) if not ok else ''), flush=True)
port, stop = serve(str(ROOT))
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='msedge', args=['--autoplay-policy=no-user-gesture-required'])
        p = boot(browser.new_context(viewport={'width':1280,'height':800}), port, 8, errors, 'boss')
        p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&rd29Ready()&&bi24Warm()}', timeout=180000)
        initial = p.evaluate('({hp:boss.hp,pools:j3State(boss).hp,ship:{x:player.x,y:player.y}})')
        p.evaluate("""()=>{window.rd29Rejected={dragon:0,void:0};const art=dr21Art;dr21Art=function(name){if(rd29Own(boss)&&name==='symbiote')rd29Rejected.dragon++;return art.apply(this,arguments);};const portal=pl11World;pl11World=function(name){if(rd29Own(boss)&&name==='black_void')rd29Rejected.void++;return portal.apply(this,arguments);};}""")
        marks = [.8,2.4,3.42,4.5,6.4,7.8,9.8,11.5,13.7,14.8,15.7,16.7]
        seen = set()
        for i in range(1300):
            p.evaluate(STEP,1)
            q = p.evaluate("""()=>({time:rd29Time(boss),mode:boss._r30.mode,t:boss._r30.t,hp:boss.hp,pools:j3State(boss).hp,protected:boss._noHit,targets:retinaBossTargets(boss).length,ship:{x:player.x,y:player.y},draw:RD29.last,bg:RD29.backgroundLast,x:boss.x,y:boss.y})""")
            trace.append(q)
            for mark in marks:
                if mark not in seen and q['time']>=mark:
                    seen.add(mark);p.evaluate('drawWorld(0)');png=O/('native-'+str(mark)+'.png');p.screenshot(path=str(png));shots.append((mark,png))
                    if mark==11.5:
                        pixels=p.evaluate('''()=>{const out={};for(const name of ['rd28Strands','rd29CodeSkin']){drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data,fn=window[name];window[name]=()=>{};try{drawWorld(0);}finally{window[name]=fn;}const z=ctx.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<z.length;i+=4)if(a[i]!==z[i]||a[i+1]!==z[i+1]||a[i+2]!==z[i+2])n++;out[name]=n;}drawWorld(0);return out;}''')
                        ck('Actual authored code strand pixels surround the drone',pixels['rd28Strands']>1000,pixels)
                        ck('Actual animated code pixels fill the drone silhouette',pixels['rd29CodeSkin']>100,pixels)
                    if mark==13.7:
                        pixels=p.evaluate('''()=>{drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data,get=XART.get,c=document.createElement('canvas');c.width=c.height=256;XART.get=function(k){return k===RD29_ART.key?c:get.apply(this,arguments);};try{drawWorld(0);}finally{XART.get=get;}const z=ctx.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<z.length;i+=4)if(a[i]!==z[i]||a[i+1]!==z[i+1]||a[i+2]!==z[i+2])n++;drawWorld(0);return n;}''')
                        ck('Own-pixel 1015 magenta glow changes visible drone pixels',pixels>100,pixels)
            if q['mode']=='fight':
                break
            if i%12==0:p.wait_for_timeout(1)
        ck('All stages reach native phase1 without phase or timer skips',q['mode']=='fight' and len(seen)==len(marks))
        intro=[q for q in trace if q['mode']!='fight']
        ck('Full native host and five form pools survive the protected introduction',all(q['hp']==initial['hp'] and q['pools']==initial['pools'] for q in intro))
        ck('Introduction remains protected with no premature Retina targets',all(q['protected'] and q['targets']==0 for q in intro))
        ck('Player stays in place instead of entering a void',max(q['ship']['x'] for q in intro)-min(q['ship']['x'] for q in intro)<.1 and max(q['ship']['y'] for q in intro)-min(q['ship']['y'] for q in intro)<.1)
        bg=[q['bg']for q in intro if q.get('bg')]
        ck('Current background warps and walks palette brightness into black',any(q['source']=='current-stage'and q['warp']>30 for q in bg)and min(q['level']for q in bg if q['source']=='current-stage')<.02)
        ck('New arena fades from black to its authored brightness before the gate',min(q['level']for q in bg if q['source']=='new-arena')==0 and max(q['level']for q in bg if q['source']=='new-arena')==1)
        drawn=[q['draw']for q in intro if q.get('draw')]
        ck('Authored amethyst gate animates before the real drone emerges',len({q['gateFrame']for q in drawn if q['gate']})>20 and any(q['gate']and q['drone']for q in drawn))
        ck('Synthetic code surrounds the drone in front and behind',any(q.get('code')and q['code']['front']>10 and q['code']['back']>10 for q in drawn))
        ck('Drone charge walks the 1015 brightness ladder and flashes white',len({q['glow']['level']for q in drawn if q.get('glow')})==6 and any(q['glow']['blink']for q in drawn if q.get('glow')))
        ck('First host is never drawn until full covering whiteout',all(not q['host']or q['white']==16 for q in drawn if q['mode']=='v18conversion'and q['time']<15.1))
        ck('Whiteout clears onto the complete first host before combat',any(q['host']and q['white']==0 for q in drawn))
        rejected=p.evaluate('rd29Rejected');ck('Rejected dragon overlay and black void are never drawn',rejected['dragon']==0 and rejected['void']==0,rejected)
        ck('Native first-host combat restores damage after reveal',not q['protected'] and q['hp']==initial['hp'])
        events=p.evaluate('RD29.events')
        ck('Gate, charge, flash and reveal have native mixer cues',all(any(e['event']==name for e in events)for name in ['amethyst-gate-opens','drone-charge','covering-white-impact','infused-host-reveal']))
        # Native combat damage, not a synthetic palette flash.
        damaged=p.evaluate('''()=>{drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data;boss._lastPart=boss.parts.find(p=>p.id==='left');const hp=boss._lastPart.hp;hitBoss(1);drawWorld(0);const z=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<z.length;i+=4)if(z[i]>240&&z[i+1]>240&&z[i+2]>240&&(a[i]<220||a[i+1]<220||a[i+2]<220))white++;return{white,damaged:boss._lastPart.hp<hp};}''')
        ck('First-host damage visibly flashes actual authored pixels',damaged['damaged']and damaged['white']>50,damaged)
        p.evaluate(STEP,30)
        ck('First-host native hit flash expires normally',p.evaluate('boss.flash<=0&&boss.parts.every(p=>p.flash<=0)'))
        a=np.array(Image.open(O/'native-14.8.png').convert('RGB'))[:,280:1000]
        ck('Peak whiteout covers the pilot and entire playfield pixels',float((a.min(axis=2)>240).mean())>.97,float((a.min(axis=2)>240).mean()))
        a=np.array(Image.open(O/'native-3.42.png').convert('RGB'))[:600,280:1000]
        ck('Arena handoff pixels pass through palette black',float(a.mean())<8,float(a.mean()))
        ck('No page or console errors',not errors,errors)
        browser.close()
finally:
    stop()
(O/'report.json').write_text(json.dumps({'checks':checks,'trace':trace,'errors':errors,'events':events},indent=2),encoding='utf8')
contact=Image.new('RGB',(1280,((len(shots)+2)//3)*285),(5,10,17));draw=ImageDraw.Draw(contact)
for i,(mark,png)in enumerate(shots):
    contact.paste(Image.open(png).convert('RGB').resize((426,266)),(i%3*426,i//3*285));draw.text((i%3*426+3,i//3*285+266),str(mark),fill='white')
contact.save(O/'contact.jpg')
print(json.dumps({'passed':sum(q['passed']for q in checks),'failed':sum(not q['passed']for q in checks)}))
raise SystemExit(0 if all(q['passed']for q in checks)else 1)
