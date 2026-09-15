"""Real Chromium proof for authored Hard/Furious elite plan injection."""
import base64, json, sys, threading, http.server
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'_shots'/'difficulty_elite_aces_0915'
OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'))
import capture3
from playwright.sync_api import sync_playwright
from PIL import Image

PRIMARY={1:'razorback',2:'emberwing',3:'glacierlance',4:'furytalon',5:'voidreaver',6:'tempest',7:'ironserpent',8:'nighthammer',9:'solarwarden'}

def main():
    checks,errors,shots=[],[],[]
    def ok(value,label):
        checks.append({'pass':bool(value),'label':label});print(('ok  ' if value else 'FAIL ')+label,flush=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
        def log_message(self,*args):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    with sync_playwright() as pw:
        browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
        page=browser.new_page(viewport={'width':1100,'height':1200})
        page.on('pageerror',lambda e:errors.append('page '+str(e)))
        page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
        page.goto(f'http://127.0.0.1:{server.server_port}/index.html',wait_until='load',timeout=120000)
        page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
        page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB)
        page.evaluate("""()=>{__auto=function(){};window.__eliteGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__eliteGets.push(k);return g(k);};}""")
        plan_audit=page.evaluate("""()=>{const out={};for(let s=1;s<=9;s++){out[s]={};for(const k of ['normal','hard','furious']){run.stage=s;curStage=STAGES[s-1];diffKey=k;DIFF=DIFFS[k];const p=buildStagePlan(s),w=p.filter(q=>q.fn&&q.fn._difficultyElite);out[s][k]={count:w.length,times:w.map(q=>q.t),sorted:p.every((q,i)=>!i||p[i-1].t<=q.t)};}}return out;}""")
        ok(all(plan_audit[str(s)]['normal']['count']==0 and plan_audit[str(s)]['hard']['count']==1 and plan_audit[str(s)]['furious']['count']==2 for s in range(1,10)),'all nine live plans inject zero/one/two aces on Normal/Hard/Furious')
        ok(all(all(plan_audit[str(s)][k]['sorted'] for k in ('normal','hard','furious')) for s in range(1,10)),'difficulty injection preserves chronological scheduling in every live plan')
        stage_details={}
        for stage,name in PRIMARY.items():
            setup=page.evaluate("""arg=>{
              beginStage(arg.stage);__auto=function(){};run.stage=arg.stage;curStage=STAGES[arg.stage-1];diffKey='hard';DIFF=DIFFS.hard;
              state=GS.PLAY;stateT=1;story=null;dlgBox=function(){};warnT=0;warnKind=null;stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];
              boss=null;bossActive=false;subBoss=null;subBossActive=false;player.x=worldWidth()/2;player.y=650;player.invuln=1e9;player.dead=false;
              const plan=buildStagePlan(arg.stage),wave=plan.find(q=>q.fn&&q.fn._difficultyElite);wave.fn();const e=enemies.find(q=>q._difficultyElite);
              e.x=worldWidth()/2;e.y=170;e.vx=e.vy=0;e._fcd=999;for(let i=0;i<32;i++){e.t=(e.t||0)+1/60;enemyShieldTick(e,1/60);}
              window.__eliteGets=[];return {art:e.art,variant:e._eliteAuthoredVariant,tag:e._difficultyElite,eligible:e._continueEligible,shield:e._esh&&{family:e._esh.family,phase:e._esh.phase,energy:e._esh.energy},waveTime:wave.t};
            }""",{'stage':stage})
            for _ in range(240):
                ready=page.evaluate("name=>XART.rdy('xelite_'+name+'_idle')",name)
                if ready:break
                page.wait_for_timeout(25)
            page.evaluate("()=>{warnT=0;warnKind=null;window.__eliteGets=[];drawWorld(0);}")
            gets=page.evaluate("()=>window.__eliteGets.slice()")
            png=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]")
            path=OUT/f'elite_stage_{stage:02d}_{name}.png';path.write_bytes(base64.b64decode(png));shots.append(path)
            setup['gets']=gets;stage_details[str(stage)]=setup
            ok(ready and setup['art']=='xelite_'+name and setup['variant']==name,f'Stage {stage} draws its authored {name} ace plate')
            ok(setup['tag']=='hard' and setup['eligible'] and setup['shield'] and setup['shield']['phase']=='active',f'Stage {stage} ace is shielded, tagged and reward-eligible')
            ok(any(k=='xelite_'+name+'_idle' for k in gets),f'Stage {stage} live renderer requests the exact authored hull')
            image=Image.open(path).convert('RGB');ok(image.size==(960,1024) and image.getbbox() is not None,f'Stage {stage} elite frame is non-empty native gameplay')
        behavior=page.evaluate("""()=>{run.stage=6;curStage=STAGES[5];diffKey='furious';DIFF=DIFFS.furious;enemies=[];eBullets=[];pBullets=[];player.x=430;player.y=650;const e=spawnDifficultyElite(6,0);e.x=150;e.y=VH*ELITEX.tempest.band;e._fcd=0;const x0=e.x;pBullets=[{x:e.x-8,y:e.y+45,vy:-8,dead:false}];elitexTick(e,1/30);return {roll:e._rollT!=null,moved:e.x!==x0,shots:eBullets.length,want:ELITEX.tempest.vol,shield:!!e._esh,kind:e._eliteAuthoredVariant};}""")
        ok(behavior['roll'] and behavior['moved'],'the live ace dodges incoming fire while strafing toward the player')
        ok(behavior['shots']==behavior['want'],'the live Furious ace releases its complete aimed volley')
        ok(behavior['shield'] and behavior['kind']=='tempest','the behavior proof retains authored identity and shield state')
        ok(not errors,'zero Chromium page or console errors')
        browser.close()
    server.shutdown()
    result={'checks':checks,'errors':errors,'plans':plan_audit,'stages':stage_details,'behavior':behavior,'shots':[str(p.relative_to(ROOT)) for p in shots]}
    (OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)

if __name__=='__main__':main()
