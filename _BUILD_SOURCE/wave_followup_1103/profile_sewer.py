from pathlib import Path
import json, sys, time, hashlib, subprocess, collections
from playwright.sync_api import sync_playwright

W = Path(__file__).parent
W.mkdir(exist_ok=True)
R = Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
OBS = Path(r'C:/Users/Mike/Documents/New project/BOF-Wave-Observe-1102')
sys.path.insert(0, str(R/'_BUILD_SOURCE'))
from shoot import TRAP_RAF

tag = sys.argv[1] if len(sys.argv)>1 else 'baseline'
errors = []
with sync_playwright() as pw:
    browser = pw.chromium.launch(channel='msedge', headless=True, args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding'])
    page = browser.new_page(viewport={'width':1280,'height':800})
    if tag.startswith('paged'):
        page.route('**/assets/game/shared/combat/sewer_pages_1103/*',lambda route:route.fulfill(path=str(W/'pages'/route.request.url.rsplit('/',1)[-1]),content_type='image/png'))
    page.on('pageerror', lambda e:errors.append(str(e)))
    page.goto('http://127.0.0.1:65041/game/index.html?quality=default',wait_until='load',timeout=180000)
    page.wait_for_function('window.__bofFrames>5&&!!window.BOF_LAYERED_STAGES',timeout=180000)
    page.wait_for_load_state('networkidle',timeout=60000)
    page.mouse.click(3,3)
    page.evaluate(TRAP_RAF)
    page.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
    page.add_script_tag(path=str(OBS/'reference_wave_maps.js'))
    page.add_script_tag(path=str(OBS/'wave_observe_1102.js'))
    if tag.startswith('paged'):
        page.add_script_tag(path=str(W/'sewer_pages_art_1103.js'))
        page.add_script_tag(path=str(W/'sewer_pages_1103.js'))
    page.evaluate('WO16.start(7)')
    page.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)}',timeout=180000)
    if tag.startswith('candidate'):
        page.add_script_tag(path=str(W/'candidate_cells.js'))
    cdp=page.context.new_cdp_session(page)
    cdp.send('Profiler.enable')
    cdp.send('Profiler.setSamplingInterval',{'interval':1000})
    cdp.send('Profiler.start')
    page.evaluate('''()=>{
      window.sewerPerf={frames:[],update:[],draw:[],running:true}; let prev=performance.now(),debt=0;
      function frame(now){if(!sewerPerf.running)return;const gap=now-prev;prev=now;debt+=Math.min(.05,gap/1000);let n=0;const a=performance.now();
        stageLoadTick();while(debt>=1/60&&n<3){WO16.input(1/60);stateT+=1/60;updatePlay(1/60);debt-=1/60;n++;}
        const b=performance.now();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;drawWorld(n/60);
        sewerPerf.frames.push(gap);sewerPerf.update.push(b-a);sewerPerf.draw.push(performance.now()-b);
        window.__bofRealRAF(frame);
      }window.__bofRealRAF(frame);
    }''')
    page.wait_for_timeout(15000)
    data=page.evaluate('()=>{sewerPerf.running=false;return {perf:sewerPerf,state:WO16.snapshot(),SS,VW,VH,cache:typeof S7CELL!=="undefined"?{hits:S7CELL.hits,misses:S7CELL.misses,bytes:S7CELL.bytes}:null}}')
    prof=cdp.send('Profiler.stop')['profile']
    (W/(tag+'.cpuprofile')).write_text(json.dumps(prof),encoding='utf8')
    page.screenshot(path=str(W/(tag+'.png')))
    browser.close()

nodes={n['id']:n for n in prof['nodes']};weights=collections.Counter()
for sample,delta in zip(prof.get('samples',[]),prof.get('timeDeltas',[])):weights[sample]+=delta
parents={child:n['id'] for n in prof['nodes'] for child in n.get('children',[])}
inclusive=collections.Counter()
for node,delta in weights.items():
    while node in nodes:
        inclusive[node]+=delta
        node=parents.get(node)
def top(counter):
    return [{'function':nodes[i]['callFrame']['functionName'],'url':nodes[i]['callFrame']['url'],'line':nodes[i]['callFrame']['lineNumber']+1,'ms':round(t/1000,2)} for i,t in counter.most_common(30)]
def stats(values):
    v=sorted(values);return {'mean':sum(v)/len(v),'p95':v[int((len(v)-1)*.95)],'max':v[-1]}
report={**data,'errors':errors,'self':top(weights),'inclusive':top(inclusive),'stats':{k:stats(data['perf'][k])for k in ['frames','update','draw']}}
(W/(tag+'.json')).write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps({k:report[k]for k in ['SS','VW','VH','stats','errors','self']},indent=2),flush=True)
