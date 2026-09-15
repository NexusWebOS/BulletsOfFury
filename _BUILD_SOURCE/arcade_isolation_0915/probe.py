"""Exercise Warden exits and campaign isolation with the real renderer and real confirm input."""
import base64, hashlib, json, sys
from pathlib import Path
R = Path(__file__).resolve().parents[2]
O = R / '_shots/arcade_isolation_0915'
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

    pg.evaluate("""()=>{
      Object.assign(campaign,{unlockedMax:4,rank:{1:'A',2:'B'},bonusUnlocked:1,_l78Pending:1,justUnlocked:4});
      campSession={v:1,stage:4,pilot:'yuri',score:4200};
      localStorage.setItem('bof_campaign_slot0','campaign-slot-sentinel');
      localStorage.setItem('Autosav01.json','autosave-sentinel');
      localStorage.setItem('bof_autosave_latest','Autosav01.json');
      window.__campBefore=JSON.stringify(campaign);window.__sessionBefore=JSON.stringify(campSession);
      window.__campaignIntact=()=>JSON.stringify(campaign)===__campBefore&&JSON.stringify(campSession)===__sessionBefore&&localStorage.getItem('bof_campaign_slot0')==='campaign-slot-sentinel'&&localStorage.getItem('Autosav01.json')==='autosave-sentinel'&&localStorage.getItem('bof_autosave_latest')==='Autosav01.json';
    }""")
    pg.evaluate("()=>{run.mode='arcade';startRun(9);__auto=function(){};}")
    ok(pg.evaluate('()=>__campaignIntact()'), 'Arcade bonus entry preserves campaign unlock, pending arrival, session and saves')
    pg.evaluate("()=>{playPauseSave();campSuspend();setState(GS.TITLE);}")
    ok(pg.evaluate('()=>__campaignIntact()'), 'Arcade pause save and title return cannot overwrite campaign saves')
    pg.evaluate("()=>{debugStartFight(debugFightList().find(f=>f.stage===7&&f.role==='boss'),{pilot:'cole'});debugFight=null;}")
    ok(pg.evaluate('()=>__campaignIntact()'), 'debug fight no longer consumes campaign Stage 8 arrival latch')
    # All four difficulty routes keep the same authored boss identifiers and HP as Campaign.
    for difficulty in ['easy','normal','hard','furious']:
        values = pg.evaluate("""key=>{
          diffKey=key;const rows=[];
          for(const mode of ['campaign','arcade']){
            run.mode=mode;DIFF=difficultyForRun(mode,key);run._threatBuild=0;
            rows.push(STAGES.map((s,i)=>{run.stage=i+1;curStage=s;boss=null;spawnBoss(s.boss);
              return boss?{stage:i+1,kind:boss.kind,ship:boss._ship,name:boss.name,hp:boss.maxhp,hammer:!!boss._hammer,warden:!!boss._s7warden}:null;}));
          }
          return rows;
        }""", difficulty)
        ok(values[0] == values[1], difficulty+' actual boss spawns match between Campaign and Arcade across all nine stages')
    # Drive the genuine damage router, authored death frames and results; do not jump to results.
    for coop in [False, True]:
        pg.evaluate("""co=>{
          coopOn=co;diffKey='normal';run.mode='arcade';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');
          startRun(7);__auto=function(){};debugFight=null;beginStage(7);
          mapScroll=levelScrollRange();stageTimer=135;spawnClock=135;waveIdx=stagePlan.length;
          subBossDone=true;subBossTriggered=true;subBossActive=false;subBoss=null;
          spawnBoss('sludgeemperor');boss.y=boss.ty;s7WardenPhase(boss,'fight');boss._s7FinalNoBar=false;
          bossActive=true;setState(GS.PLAY);player.x=120;player.y=VH*.78;player.invuln=999;
          if(co){player2.x=300;player2.y=VH*.78;player2.invuln=999;}
          run.score=10000;run2.score=20000;run.contUsed=2;run.lives=4;run2.lives=3;run.bombs=17;run2.bombs=11;
          window.__shipStart={x:player.x,y:player.y};window.__warden=boss;
          boss.hp=1;hitBoss(1000);window.__killScore=run.score;
        }""", coop)
        ok(pg.evaluate("()=>s7FinalPhase(boss)==='defeat'&&bossDefeated&&run.score===45000"), ('co-op' if coop else 'solo')+' lethal hit begins Warden defeat and grants kill score once')
        for _ in range(120):
            if pg.evaluate("()=>XART.rdy('cfx_stage7_warden_laststand')"):break
            pg.wait_for_timeout(30)
        step(115)
        ok(pg.evaluate("()=>state===GS.PLAY&&s7FinalPhase(boss)==='escape'&&!boss._s7warden.final.radio&&!s7WardenShipHidden()&&Math.abs(player.x-__shipStart.x)<.01&&Math.abs(player.y-__shipStart.y)<.01&&boss._s7warden.final.portalOpen===0"), ('co-op' if coop else 'solo')+' defeat keeps ship visible and in place without story radio or portal flight')
        if not coop:shot('arcade_warden_defeat')
        for _ in range(30):
            if pg.evaluate('()=>state===GS.STAGECLEAR'):break
            step(10)
        ok(pg.evaluate('()=>state===GS.STAGECLEAR&&run.stage===7&&__warden._s7warden.final.finished&&__warden.dead'), ('co-op' if coop else 'solo')+' complete authored defeat reaches Stage 7 results')
        step(25)
        pg.evaluate("()=>{window.__expectedScore=run.score+drawStageClear._res.bonus;window.__expectedScore2=run2.score+(drawStageClear._res.seats?drawStageClear._res.seats[1].bonus:0);s7WardenFinishCampaign(__warden);s7WardenBeginDefeat(__warden);}")
        ok(pg.evaluate('()=>run.score===__killScore'), 'repeated finish/defeat callbacks cannot pay kill score twice')
        enter();step(150)
        shot('coop_results' if coop else 'solo_results')
        enter()
        ok(pg.evaluate("()=>run.stage===8&&state===GS.INTRO&&run.score===__expectedScore&&run2.score===__expectedScore2&&run.contUsed===2&&run.lives===4&&run2.lives===3&&run.bombs===17&&run2.bombs===11"), ('co-op' if coop else 'solo')+' results award each active seat and preserve stocks before Stage 8')
        ok(pg.evaluate('()=>__campaignIntact()'), ('co-op' if coop else 'solo')+' Warden exit leaves campaign progress and saves unchanged')
    # Campaign still owns the long escape, radio, forced flight, map unlock and saved handoff.
    pg.evaluate("""()=>{
      coopOn=false;run.mode='campaign';diffKey='normal';DIFF=difficultyForRun('campaign','normal');beginStage(7);
      mapScroll=levelScrollRange();spawnBoss('sludgeemperor');boss.y=boss.ty;s7WardenPhase(boss,'fight');
      bossActive=true;setState(GS.PLAY);boss.hp=1;hitBoss(1000);player.invuln=999;
    }""")
    step(100)
    ok(pg.evaluate("()=>s7FinalPhase(boss)==='defeat'&&!!boss._s7warden.final.radio"), 'Campaign retains its defeat dialogue and original hold')
    step(200);shot('campaign_escape')
    ok(pg.evaluate("()=>state===GS.PLAY&&s7FinalPhase(boss)==='escape'&&boss._s7warden.final.portalOpen>0"), 'Campaign retains its portal flight')
    step(200)
    ok(pg.evaluate("()=>state===GS.STAGESEL&&campaign.unlockedMax===8&&campaign._l78Pending===1&&!!campaign.rank[7]&&campSession.stage===7"), 'Campaign still unlocks Stage 8 and suspends at the map')
    pg.evaluate("()=>{campaign.bonusUnlocked=1;run.mode='campaign';beginStage(9);}")
    ok(pg.evaluate('()=>campaign.bonusUnlocked===0'), 'Campaign itself still spends its selected bonus unlock')
    loop_error=pg.evaluate('()=>window.__err||null')
    ok(not errors and not loop_error, 'zero page, console and controlled-loop errors')
    b.close()
stop()
board=Image.new('RGB',(960,570),'#10131c');d=ImageDraw.Draw(board)
for i,path in enumerate(shots):
    im=Image.open(path).convert('RGB');im.thumbnail((240,540));board.paste(im,(i*240,25));d.text((i*240+6,5),path.stem,fill='white')
board.save(O/'contact.png')
result={'runtimeSha256':hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest(),'checks':checks,'errors':errors,'loopError':loop_error,'screenshots':[str(s)for s in shots]}
(O/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
n=sum(c['ok']for c in checks);print('%d passed / %d failed'%(n,len(checks)-n),flush=True)
if n!=len(checks):raise SystemExit(1)
