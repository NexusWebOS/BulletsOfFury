"""Native Chromium proof for MODE-07 Continue Up reward boundaries."""
import base64, json, sys, threading, http.server
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'_shots'/'continue_up_rewards_0915'
OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
from playwright.sync_api import sync_playwright
from PIL import Image

def main():
    checks,errors,shots=[],[],[]
    def ok(value,label):
        checks.append({'pass':bool(value),'label':label})
        print(('ok  ' if value else 'FAIL ')+label,flush=True)
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
        page.evaluate(shoot.TRAP_RAF)
        entered=page.evaluate("()=>{run.mode='arcade';diffKey='hard';beginStage(4);return run.stage===4&&curStage===STAGES[3];}")
        ok(entered,'native beginStage opens Stage 4 in Chromium')
        page.evaluate("""()=>{
          __auto=function(){};story=null;dlgBox=function(){};warnT=0;warnKind=null;stagePlan=[];waveIdx=0;
          enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;
          bossDefeated=false;stageEnding=0;stageTimer=1;state=GS.PLAY;stateT=1;run.mode='arcade';run.stage=4;
          diffKey='hard';DIFF=difficultyForRun(run.mode,diffKey);run.contUsed=3;run.contBonus=0;
          stageStats.deaths=0;stageStats.pickupsSeen=0;stageStats.pickups=0;stageStats2.deaths=0;
          player.x=worldWidth()/2;player.y=420;player.invuln=1e9;player.dead=false;player.out=false;
          window.__cuBlits=[];window.__cuDrawImages=0;window.__cuLifeSfx=0;window.__cuStageLabels=[];
          const ob=ASSETS.blit.bind(ASSETS);ASSETS.blit=function(k){window.__cuBlits.push(k);return ob.apply(null,arguments);};
          const od=ctx.drawImage.bind(ctx);ctx.drawImage=function(){window.__cuDrawImages++;return od.apply(null,arguments);};
          const ol=Audio.SFX.life;Audio.SFX.life=function(){window.__cuLifeSfx++;return ol&&ol.apply(this,arguments);};
          const ost=stageText;stageText=function(a,s){window.__cuStageLabels.push(String(s));return ost.apply(this,arguments);};
        }""")
        page.wait_for_function("()=>ASSETS.ready&&ASSETS.has('pu_life')",timeout=120000)
        ok(page.evaluate("()=>ASSETS.has('pu_life')"),'authored Life Up base plate is decoded for the temporary composed pickup')

        elite=page.evaluate("""()=>{
          stagePlan=buildStagePlan(4);const wave=stagePlan.find(q=>q.fn&&q.fn._difficultyElite);wave.fn();
          const e=enemies.find(q=>q._difficultyElite);e.x=worldWidth()/2;e.y=190;e.hp=0;killEnemy(e);
          drawWorld(0);const p=powerups.find(q=>q.kind==='continueup');
          return {drop:!!p,source:p&&p._continueSource,count:powerups.filter(q=>q.kind==='continueup').length,
            blits:window.__cuBlits.slice(),drawImages:window.__cuDrawImages,eligible:e._continueEligible,variant:e._eliteAuthoredVariant};
        }""")
        ok(elite['drop'] and elite['source']=='elite' and elite['count']==1,'a real Hard authored ace death drops exactly one Continue Up')
        ok(elite['eligible'] and bool(elite['variant']),'the reward came from the authored difficulty-elite boundary')
        ok('pu_life' in elite['blits'] and elite['drawImages']>0,'the game canvas draws the authored base plate for the visible pickup')
        page.evaluate("()=>{explosions=[];particles=[];enemies=[];window.__cuBlits=[];drawWorld(0);}")

        def capture(name):
            raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]")
            path=OUT/f'{name}.png';path.write_bytes(base64.b64decode(raw));shots.append(path);return path
        capture('continue_up_01_elite_drop')

        collected=page.evaluate("""()=>{
          const p=powerups.find(q=>q.kind==='continueup');p.x=player.x;p.y=player.y;p.vy=0;
          stagePlan=[];waveIdx=0;updatePlay(1/60);if(_arcBan)_arcBan.t=1;drawWorld(0);
          return {bonus:run.contBonus,cap:continueCap(),left:continueCap()-run.contUsed,present:powerups.some(q=>q.kind==='continueup'),
            banner:_arcBan&&_arcBan.text,lifeSfx:window.__cuLifeSfx};
        }""")
        ok(collected['bonus']==1 and collected['cap']==4 and collected['left']==1,'real pickup collision extends the Hard Arcade bank from three to four')
        ok(not collected['present'] and collected['banner']=='CONTINUE UP - 1 READY','collection consumes the pickup and announces the remaining reserve')
        ok(collected['lifeSfx']==1,'collection reaches the existing authored Life Up sound route once')
        capture('continue_up_02_collected_banner')

        deathless=page.evaluate("""()=>{
          powerups=[];stageStats.deaths=0;stageStats2.deaths=0;const encounter={};continueRewardMark(encounter);
          const clean=continueRewardResolve(encounter,240,150,'miniboss');const one=powerups.length;
          const duplicate=continueRewardResolve(encounter,240,150,'miniboss');
          const failed={};continueRewardMark(failed);stageStats.deaths=1;const blocked=continueRewardResolve(failed,240,150,'boss');
          return {clean,one,duplicate,blocked,sources:powerups.map(p=>p._continueSource)};
        }""")
        ok(deathless['clean'] and deathless['one']==1 and not deathless['duplicate'],'a deathless encounter resolves once at its marked boundary')
        ok(not deathless['blocked'] and deathless['sources']==['miniboss'],'a life lost inside the marked encounter blocks the reward')

        hooks=page.evaluate("""()=>{
          powerups=[];explosions=[];particles=[];stageStats.deaths=0;stageStats2.deaths=0;
          run.stage=4;curStage=STAGES[3];spawnSubBoss('subcore');const miniMarked=subBoss._continueDeathMark===0;
          subBoss.dead=true;subBoss.dying=1.89;updateSubBoss(.02);
          const mini=powerups.filter(p=>p.kind==='continueup'&&p._continueSource==='miniboss').length;
          powerups=[];explosions=[];particles=[];run.stage=2;curStage=STAGES[1];spawnBoss('magmacolossus');const bossMarked=boss._continueDeathMark===0;
          boss.hp=0;bossDie();const final=powerups.filter(p=>p.kind==='continueup'&&p._continueSource==='boss').length;
          return {miniMarked,mini,bossMarked,final};
        }""")
        ok(hooks['miniMarked'] and hooks['mini']==1,'the real miniboss spawn and death-completion hooks award one clean-section pickup')
        ok(hooks['bossMarked'] and hooks['final']==1,'the real boss spawn and death hooks award one clean-section pickup')

        prompt=page.evaluate("""()=>{
          powerups=[];explosions=[];particles=[];floaters=[];_arcBan=null;run.contUsed=3;run.contBonus=1;run.lives=0;state=GS.CONTINUE;stateT=.5;drawContinue._vo=true;
          window.__cuStageLabels=[];drawContinue(0);return {cap:continueCap(),labels:window.__cuStageLabels.slice()};
        }""")
        ok(prompt['cap']==4 and '1 CONTINUE REMAINING' in prompt['labels'],'finite Continue screen displays the earned reserve before it is spent')
        capture('continue_up_03_augmented_continue_prompt')

        spent=page.evaluate("""()=>{
          const ot=Input.tap;Input.tap=k=>k==='enter';Input.mouse.down=false;state=GS.CONTINUE;stateT=.5;drawContinue._vo=true;drawContinue(0);Input.tap=ot;
          return {state,used:run.contUsed,lives:run.lives,cap:continueCap()};
        }""")
        ok(spent['state']==page.evaluate('()=>GS.PLAY') and spent['used']==4 and spent['lives']==3 and spent['cap']==4,'the augmented fourth credit restores the configured Hard stock')
        for path in shots:
            image=Image.open(path).convert('RGB')
            ok(image.size==(960,1024) and image.getbbox() is not None,f'{path.stem} is a non-empty native frame')
        ok(not errors,'zero Chromium page or console errors')
        browser.close()
    server.shutdown()
    result={'checks':checks,'errors':errors,'elite':elite,'collected':collected,'deathless':deathless,'prompt':prompt,'spent':spent,
            'shots':[str(p.relative_to(ROOT)) for p in shots]}
    (OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)

if __name__=='__main__':main()
