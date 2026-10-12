"""Real Chromium menus, input polling, decoded sound, save/award integration.

Native canvas screenshots use the live renderer. Protected gameplay fixtures
isolate controls and award events; these are not unassisted balance results.
All storage changes belong to fresh browser contexts, never Mike's saves.
"""
from pathlib import Path
import json, sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/overdrive_menu_1011';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];observations={}
def check(name,passed):
    checks.append({'name':name,'passed':bool(passed)})
    print(('PASS ' if passed else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch()
  context=browser.new_context(viewport={'width':1400,'height':1100})
  page=context.new_page()
  def monitor(pg):
   pg.on('pageerror',lambda e:errors.append(str(e)))
   pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   pg.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  monitor(page)
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?qa=menu1011')
  page.wait_for_function('window.TDGAME && TDGAME.G.state==="boot"',timeout=60000)
  page.evaluate('TDGAME.freeze()')
  def frames(n):
   while n:
    k=min(45,n);page.evaluate('n=>TDGAME.step(n)',k);page.wait_for_timeout(25);n-=k
  def tap(k,n=20):
   page.keyboard.down(k);frames(1);page.keyboard.up(k);frames(n)
  def snap(name):
   page.evaluate('TDGAME.render()');page.locator('#screen').screenshot(path=str(OUT/(name+'.png')))
  def go(s):
   page.evaluate("s=>{TD.Frontend.returnTo='title';TD.Frontend.go(s);}",s);frames(24)
  frames(24)
  check('startup waits for input with the supplied recording and no stage picker',page.evaluate('!TD.Audio.on && TD.STARTUP_AUDIO.file.endsWith("/overdrive-startup.mp3") && !TD.Frontend.voice && TDGAME.G.state==="boot"'))
  snap('startup')
  tap('Enter');check('Start enters the new Overdrive intro',page.evaluate('TDGAME.G.state==="intro"'))
  page.wait_for_function('TD.Frontend.voiceDone',timeout=15000)
  frames(150);check('recorded intro reaches the original-style title menu',page.evaluate('TDGAME.G.state==="title" && TD.Display.w===640 && TD.Display.h===512'))
  page.wait_for_function('TD.Audio.musicKey==="title" && TD.Audio.music.readyState>=3 && TD.Audio.music.currentTime>0',timeout=15000)
  check('Title uses the decoded original BOF title track',page.evaluate('TD.Audio.music.currentSrc.endsWith("/Title.mp3") && !TD.Audio.music.paused'))
  snap('title')
  tap('Enter');check('New Game goes to five new difficulty plates',page.evaluate('TDGAME.G.state==="difficulty" && Object.keys(TD.DIFFICULTIES).length===5'))
  snap('difficulty')
  tap('Enter');frames(90)
  check('difficulty enters the actual twelve-pilot roster',page.evaluate('TDGAME.G.state==="pilot" && TD.PILOTS.join(",")==="axel,decker,maverick,freezer,juggernaut,yuri,lizzie,falva,cole,hotwire,phoenix,niel"'))
  page.wait_for_function('TD.Audio.musicKey==="select" && TD.Audio.music.readyState>=3 && TD.Audio.music.currentTime>0',timeout=15000)
  check('pilot selection plays the original PilotSelect music',page.evaluate('TD.Audio.music.currentSrc.endsWith("/PilotSelect.mp3")'))
  page.wait_for_function('TD.FRONT_WARM.every(k=>!!ART.get(k))',timeout=30000)
  check('all authored UI, original portraits, ships, emblems and bitmap glyphs decode',page.evaluate('TD.FRONT_WARM.every(k=>ART.get(k)) && BOF.stageFontV4.final.frames[BOF.stageFontV4.final.font.A][3]===21'))
  check('every new UI frame and boss canvas has even registered dimensions',page.evaluate('[...Object.values(TD_UI_ART.assets),...Object.values(TD_WARRIOR_ART.assets)].every(a=>a.size.every(n=>Number.isInteger(n)&&n%2===0))'))
  for pk in ['cole','hotwire','phoenix','niel']:
   page.evaluate('p=>{TD.pilot=p;TD.Frontend.pilotAge=0;}',pk);frames(150);snap('pilot_'+pk)
  tap('Enter');check('pilot confirmation opens the campaign briefing',page.evaluate('TDGAME.G.state==="brief" && TDGAME.G.sel===0 && TDGAME.G.mission===2'))
  frames(60);tap('Enter');check('briefing starts the first authored campaign mission',page.evaluate('TDGAME.G.state==="play" && TD.Achievements.data.unlocked.deploy'))
  tap('Enter');check('Start pauses into Resume, Options and Help',page.evaluate('TDGAME.G.state==="pause" && TD.Display.w===640'))
  snap('pause');tap('ArrowDown');tap('Enter');check('pause opens the restored Options menu',page.evaluate('TDGAME.G.state==="options" && TD.Frontend.returnTo==="pause"'))
  snap('sound')
  baseline=page.evaluate('({...TD.Frontend.settings})')
  tap('ArrowLeft');check('sound controls change actual music gain',page.evaluate('Math.abs(TD.Audio.music.volume-TD.Frontend.settings.music*TD.Frontend.settings.master)<.00001 && TD.Frontend.settings.master===.95'))
  tap('b');check('Options Cancel restores the exact previous sound mix',page.evaluate('(JSON.stringify(TD.Frontend.settings)===JSON.stringify(TD.Frontend.snapshot.settings)) && TDGAME.G.state==="pause"'))
  tap('b');check('B resumes paused gameplay',page.evaluate('TDGAME.G.state==="play"'))
  go('options');tap('ArrowDown');tap('ArrowLeft')
  page.evaluate('TD.Frontend.sel=TD.Frontend.optionsRows().length');tap('Enter')
  check('Apply persists the changed music setting',page.evaluate('JSON.parse(localStorage.bof_od_options).music===.5'))
  go('options');page.evaluate('TD.Frontend.tab=1;TD.Frontend.sel=0');frames(1);snap('keyboard')
  tap('Enter',1);page.keyboard.press('t');frames(20)
  check('keyboard capture rebinds and persists movement',page.evaluate('TD.BIND.up[0]==="t" && !TD.Input.rebind && JSON.parse(localStorage.bof_od_keys).up[0]==="t"'))
  fresh="""TDGAME.G.sel=0;TD.difficulty='normal';TDGAME.start();const G=TDGAME.G,p=G.player;G.units=[];G.props=[];G.structures=[];TD.World.load(800,4000,[]);p.x=250;p.y=2200;p.inv=99999;p.a=p.aim=Math.PI;TD.Input.pointer.active=false;"""
  page.evaluate('()=>{'+fresh+'}');y=page.evaluate('TDGAME.G.player.y');page.keyboard.down('t');frames(35);page.keyboard.up('t');frames(1)
  check('the rebound key actually moves the tank through native input',page.evaluate('TDGAME.G.player.y')<y-65)
  page.evaluate('TD.Input.resetKeys()');check('keyboard reset restores original controls',page.evaluate('TD.BIND.up.includes("w") && !TD.BIND.back.includes("backspace")'))
  go('password');page.evaluate("TD.Frontend.pwSel=39");tap('Enter');frames(2)
  code=page.evaluate('TD.Password.encode(2,"phoenix","hard","hotwire")')
  page.keyboard.press('Backspace');page.keyboard.type(code[2:-1]+'X');page.keyboard.press('Backspace');page.keyboard.type(code[-1]);frames(2)
  check('typing accepts letters and Backspace deletes without navigating Back',page.evaluate('TDGAME.G.state==="password" && TD.Frontend.pw')==code)
  snap('password');tap('Enter')
  check('an Overdrive password restores pilot, difficulty, partner and campaign position',page.evaluate('TDGAME.G.state==="pilot" && TD.pilot==="phoenix" && TD.difficulty==="hard" && TD.companion==="hotwire" && TDGAME.G.sel===2'))
  r=page.evaluate("""()=>{let n=0;for(const s of [0,2,3])for(const p of TD.PILOTS)for(const d of Object.keys(TD.DIFFICULTIES))for(const c of TD.COMPANIONS){const code=TD.Password.encode(s,p,d,c),v=TD.Password.decode(code);if(!v||v.sel!==s||v.pilot!==p||v.difficulty!==d||v.companion!==c)return {ok:false,code};n++;}return{ok:true,n,legacy:TD.Password.decode('BOF-1234'),bad:TD.Password.decode('OD-2222-2222')};}""")
  observations['passwords']=r;check('all 540 campaign passwords round-trip; old and corrupt codes reject',r.get('ok') and r['n']==540 and r['legacy'] is None and r['bad'] is None)
  go('password');page.evaluate('TD.Frontend.pw="BAD";TD.Frontend.pwSel=38');tap('Enter')
  check('invalid passwords stay on the password menu with a chip error cue',page.evaluate('TDGAME.G.state==="password" && TD.Frontend.message.includes("INVALID") && TD.Audio.stats.error>0'))
  # The actual navigator polling path, with test hardware replacing only the
  # physical browser Gamepad source. Rendering and gameplay remain real.
  page.evaluate("window.testPad={id:'OVERDRIVE QA six button',connected:true,buttons:Array.from({length:20},()=>({pressed:false})),axes:[0,0,0,0]};Object.defineProperty(navigator,'getGamepads',{value:()=>[testPad],configurable:true});TD.Input.setPadStyle('six');TDGAME.step(2)")
  page.evaluate('()=>{'+fresh+'}')
  page.evaluate('testPad.buttons[15].pressed=true');frames(35);p0=page.evaluate('({...TDGAME.G.player})')
  page.evaluate('testPad.buttons[15].pressed=false;testPad.buttons[6].pressed=true;testPad.buttons[12].pressed=true;testPad.buttons[2].pressed=true');frames(65)
  r=page.evaluate('({dx:TDGAME.G.player.x,dy:TDGAME.G.player.y,angle:TDGAME.G.player.aim,cruise:TDGAME.G.player.cruising,shots:TDGAME.G.shots.length,award:!!TD.Achievements.data.unlocked.cruise})')
  observations['cruise']={'before':{k:p0[k] for k in ['x','y','aim']},'after':r}
  check('L cruises in the prior direction while D-pad turns the turret and X fires',r['dx']>p0['x']+145 and abs(r['dy']-p0['y'])<1 and r['cruise'] and r['shots']>0 and r['award'])
  page.evaluate('testPad.buttons=Array.from({length:20},()=>({pressed:false}));TDGAME.step(25)')
  check('releasing the cruise shoulder brakes to a stop',page.evaluate('!TDGAME.G.player.cruising && Math.hypot(TDGAME.G.player.vx,TDGAME.G.player.vy)<.1'))
  page.evaluate('()=>{'+fresh+"p.y=2200;G.units=[TD.makeUnit('heavy',p.x,p.y-130,{a:Math.PI})];G.units[0].speed=0;TD.Cam.x=p.x-240;TD.Cam.y=p.y-240;testPad.buttons[7].pressed=true;}")
  frames(30);observations['retina']=page.evaluate('({r:TDGAME.G.player.retina?.locked,state:TD.Input.state,cam:TD.Cam,p:{x:TDGAME.G.player.x,y:TDGAME.G.player.y,aim:TDGAME.G.player.aim},target:TDGAME.G.units.map(u=>({x:u.x,y:u.y,dead:u.dead}))})');check('R shoulder acquires a real Retina target',page.evaluate('TDGAME.G.player.retina?.locked && TD.Input.state.retina'))
  page.evaluate('testPad.buttons[5].pressed=true');frames(2);page.evaluate('testPad.buttons[5].pressed=false');frames(1)
  check('releasing the cannon with R held launches a locked tank missile',page.evaluate('TDGAME.G.shots.some(s=>s.retinaTarget) && TDGAME.G.player.missiles===5 && TD.Achievements.data.unlocked.lock'))
  page.evaluate('testPad.buttons=Array.from({length:20},()=>({pressed:false}));TD.Input.setPadStyle("standard")');frames(2)
  go('options');page.evaluate('TD.Frontend.tab=2;TD.Frontend.sel=0');frames(1);snap('controller_options')
  check('standard controller preset exposes both shoulders, stick aim and boost',page.evaluate('TD.Input.padStyle()==="standard" && TD.Input.padProfile().L===4 && TD.Input.padProfile().R===5 && TD.Input.padProfile().boost===6'))
  page.evaluate('()=>{'+fresh+'testPad.axes=[1,0,0,-1];testPad.buttons[0].pressed=true;testPad.buttons[6].pressed=true;}');frames(35)
  check('standard pad moves, boosts, aims the right stick and fires independently',page.evaluate('TDGAME.G.player.x>400 && TDGAME.G.player.boosting && Math.abs(TD.M.wrap(TDGAME.G.player.aim-Math.PI))<.05 && TDGAME.G.shots.length>0'))
  page.evaluate('testPad.axes=[0,0,0,0];testPad.buttons=Array.from({length:20},()=>({pressed:false}));TD.Input.setPadStyle("six");TD.Input.beginSetup();TD.Frontend.go("padsetup")');frames(20)
  # Learn all 14 inputs, including two physical shoulders. B remains assignable
  # while learning; keyboard B/Escape and the Cancel plate exit this sub-screen.
  for idx in [12,13,14,15,0,1,5,2,3,4,8,9,6,7]:
   page.evaluate('i=>{testPad.buttons[i].pressed=true}',idx);frames(1)
   page.evaluate('i=>{testPad.buttons[i].pressed=false}',idx);frames(2)
  check('six-button learn records all 14 controls with neutral separation',page.evaluate('TD.Input.setup.done && TD.Input.setup.i===14 && TD.Input.padProfile().L===6 && TD.Input.padProfile().R===7'))
  tap('Enter');page.evaluate('TD.Input.setPadStyle("standard");TD.Input.beginSetup();TD.Frontend.go("padsetup")');frames(20)
  for idx in [12,13,14,15,0,1,2,3,8,9,4,5,6]:
   page.evaluate('i=>{testPad.buttons[i].pressed=true}',idx);frames(1)
   page.evaluate('i=>{testPad.buttons[i].pressed=false}',idx);frames(2)
  check('standard learn records 13 controls and persists actual shoulder buttons',page.evaluate('TD.Input.setup.done && TD.Input.setup.i===13 && JSON.parse(localStorage.bof_td_controllers)[testPad.id].R===5'))
  tap('Enter');go('help');frames(1);snap('controller_help');tap('ArrowRight');snap('onfoot_help')
  check('Help includes the actual museum infantry controls',page.evaluate('TD.Frontend.helpTab===2'))
  go('options');page.evaluate("TD.Input.beginSetup();TD.Frontend.setupReturn='options';TD.Frontend.go('padsetup')");frames(20);snap('controller_setup')
  box=page.locator('#screen').bounding_box();page.mouse.click(box['x']+box['width']*.5,box['y']+box['height']*445/512);frames(20)
  check('the generated Cancel plate exits controller learning through native pointer input',page.evaluate('!TD.Input.setup && TDGAME.G.state==="options"'))
  # All difficulty levels exercise actual health reduction and body counts.
  r=page.evaluate("()=>Object.entries(TD.DIFFICULTIES).map(([d,v])=>{TD.difficulty=d;TDGAME.G.sel=0;TDGAME.start();const p=TDGAME.G.player;p.inv=0;TD.hurtPlayer(TDGAME.G,2);return {d,damage:12-p.hp,want:2*v.damage,lives:TDGAME.G.lives+1};})")
  observations['difficulties']=r;check('difficulty changes real damage and total lives to 5/3/2/1/1',all(abs(v['damage']-v['want'])<1e-7 for v in r) and [v['lives'] for v in r]==[5,3,2,1,1])
  page.evaluate('()=>{'+fresh+"TD.Frontend.settings.master=.5;TD.Frontend.settings.sfx=.8;TD.Frontend.settings.engine=.4;TD.Frontend.applyAudio();}");frames(2)
  r=page.evaluate('Array.from(TD.Audio.loops.values()).find(v=>v.key==="gd_tankEngineLoop")?.audio.volume')
  observations['quietEngineVolume']=r;check('engine reduction and its separate slider reach the actual media gain',r is not None and abs(r-.08*.8*.5*.4*.65)<.00001)
  page.evaluate('Object.assign(TD.Frontend.settings,{master:1,engine:1,sfx:.8});TD.Frontend.applyAudio()')
  # Translation-based awards and actual structural destruction.
  page.keyboard.down('d');page.keyboard.down('r');frames(65);page.keyboard.up('d');page.keyboard.up('r');frames(1)
  check('moving boost earns Full Throttle through actual play',page.evaluate('!!TD.Achievements.data.unlocked.boost'))
  page.evaluate("const G=TDGAME.G;G.structures=Array.from({length:6},(_,i)=>TD.makeStructure({kind:'barrier',x:120+i*40,y:2150}));G.structures.forEach(s=>TD.hitStructure(G,s,99));")
  frames(2);check('destroying six real walls earns Concrete Carnage',page.evaluate('TDGAME.G.structuresBroken>=6 && TD.Achievements.data.unlocked.demolition'))
  # A real boss death drives clear, code generation and the new awards.
  page.evaluate("TDGAME.G.sel=0;TD.pilot='hotwire';TD.difficulty='normal';TDGAME.start();TDGAME.G.units=[];TDGAME.G.player.x=400;TDGAME.G.player.y=650;TDGAME.G.player.inv=99999;TD.Achievements.queue=[];")
  frames(160);check('new Warrior enters a 480-square arena at 1:1 zoom',page.evaluate('TDGAME.G.boss && TD.VH===480 && TD.Display.h===480 && TD.Cam.zoom===1'))
  page.evaluate("TDGAME.G.boss.state='recover';TDGAME.G.boss.cooldown=999;TDGAME.G.boss.x=400;TDGAME.G.boss.y=472;TDGAME.G.boss.a=TDGAME.G.boss.upper=0");frames(45)
  page.evaluate('TDGAME.G.player.inv=0');snap('warrior_front');page.evaluate('TDGAME.G.player.inv=99999')
  page.evaluate("TDGAME.G.boss.damage('hull',800)");frames(14);page.evaluate('TDGAME.G.player.inv=0');snap('warrior_damaged');page.evaluate('TDGAME.G.player.inv=99999')
  check('armored hull damage reaches the authored damaged chassis while modules remain mounted',page.evaluate('TDGAME.G.boss.parts.hull>0 && TDGAME.G.boss.parts.hull<TDGAME.G.boss.max.hull*.4 && TDGAME.G.boss.parts.armL>0 && TDGAME.G.boss.parts.armR>0 && TDGAME.G.boss.parts.helmet>0'))
  page.evaluate("TDGAME.G.boss.damage('armL',999)");frames(12);page.evaluate('TDGAME.G.player.inv=0');snap('warrior_arm_break');page.evaluate('TDGAME.G.player.inv=99999')
  page.evaluate("const B=TDGAME.G.boss;B.damage('armR',999);B.damage('helmet',999);B.damage('hull',999)");frames(340)
  check('actual Warrior defeat awards clear, no-death, pilot and a new password',page.evaluate('TDGAME.G.state==="clear" && ["warrior","warriorclean","hotwire"].every(k=>TD.Achievements.data.unlocked[k]) && TD.Password.decode(TDGAME.G.results.password).sel===2'))
  frames(165);page.evaluate('TDGAME.G.player.inv=0');snap('results')
  # Remaining award event hooks are isolated fixtures, preserving their actual
  # finish and museum functions. No claim of an unassisted campaign completion.
  page.evaluate("TD.pilot='phoenix';TDGAME.G.sel=2;TD.difficulty='furious';TDGAME.start();TDGAME.G.results={};TD.Frontend.saveClear(TDGAME.G);TD.pilot='niel';TDGAME.G.sel=3;TDGAME.start();TDGAME.G.results={};TDGAME.G.rescued=TDGAME.G.hostages.length;TDGAME.G.hostagesLost=0;TD.Frontend.saveClear(TDGAME.G);")
  check('rogue squad, pilot, rescue and full campaign awards use mission completion hooks',page.evaluate('["machinists","phoenix","niel","rescue","campaign"].every(k=>TD.Achievements.data.unlocked[k])'))
  page.evaluate("TDGAME.G.sel=0;TDGAME.start();TDGAME.G.results={};TD.Frontend.saveClear(TDGAME.G)")
  check('Furious completion requires all three campaign missions at that difficulty',page.evaluate('TD.Achievements.data.unlocked.furious'))
  for wi in ['vulcan','homing','laser']:
   page.evaluate('id=>{TDGAME.G.sel=0;TDGAME.start();TDGAME.G.player.weapons=[{id,lv:3}];}',wi);frames(1)
  check('ground maximum weapons feed Combined Arms without repeated saves',page.evaluate('BOF_GENERAL_ACHIEVEMENTS.snapshot().weapons[0] && BOF_GENERAL_ACHIEVEMENTS.snapshot().weapons[2] && BOF_GENERAL_ACHIEVEMENTS.snapshot().weapons[3] && BOF_GENERAL_ACHIEVEMENTS.list()[3].unlocked'))
  go('achievements');page.evaluate('TD.Frontend.sel=16');frames(1);snap('achievements_general')
  check('gallery includes sixteen Overdrive and four shared general awards',page.evaluate('TD.Achievements.defs.length===16 && BOF_GENERAL_ACHIEVEMENTS.defs.length===4 && TD.Frontend.rects.length===0'))
  page.evaluate('TD.Frontend.sel=4');frames(1);snap('achievements');tap('ArrowRight');check('earned-only filter works',page.evaluate('TD.Frontend.achFilter===true'))
  # Root-game integration goes through the game's real public APIs and renderer.
  base=context.new_page();monitor(base);base.add_init_script(shoot.TRAP_RAF)
  base.goto(f'http://127.0.0.1:{port}/index.html?qa=general1011',timeout=60000)
  base.wait_for_function('typeof achievementList==="function" && window.BOF_GENERAL_ACHIEVEMENTS',timeout=60000)
  r=base.evaluate("""()=>{const original=achievementList().length-4;for(let i=0;i<10;i++){run.pilot=['cole','axel','decker'][i%3];achievementStageComplete(1,{deaths:0,missiles:0});}for(const w of [0,2,3])achievementWeaponMax(w,5);const before=BOF_GENERAL_ACHIEVEMENTS.snapshot().clears,stats={deaths:0};achievementStageComplete(1,stats);achievementStageComplete(1,stats);return {original,n:achievementList().length,awards:BOF_GENERAL_ACHIEVEMENTS.list().map(d=>d.unlocked),dedup:BOF_GENERAL_ACHIEVEMENTS.snapshot().clears===before+1,points:BOF_GENERAL_ACHIEVEMENTS.points(),profile:Object.keys(achievementProfileSnapshot().unlocked).filter(k=>k.startsWith('general_')).length};}""")
  observations['baseIntegration']=r;check('all four general awards integrate with original completion and weapon APIs',all(r['awards']) and r['n']==r['original']+4 and r['profile']==4 and r['points']==450)
  check('repeat reporting of the same original clear does not double-count',r['dedup'])
  setup=base.evaluate(shoot.SETUP,{'state':'ACHIEVEMENTS'})
  if not setup.get('ok'):raise RuntimeError(setup)
  base.evaluate('awardsOpen();awards.tab=1;awards.fv.type=awardsTabValues("type",awards.rows).findIndex(v=>v.v==="general")')
  for _ in range(10):base.evaluate(shoot.STEP,30);base.wait_for_timeout(60)
  base.evaluate("for(const d of BOF_GENERAL_ACHIEVEMENTS.defs)XART.get(d.plaque)")
  base.wait_for_function('BOF_GENERAL_ACHIEVEMENTS.defs.every(d=>!!XART.get(d.plaque))',timeout=20000)
  base.locator('#screen').screenshot(path=str(OUT/'original_achievements.png'))
  check('original achievement screen includes the new four award rows',base.evaluate('awards.rows.filter(r=>r.id.startsWith("general_")).length===4 && state===GS.ACHIEVEMENTS'))
  check('new general badges decode through original XART keys',base.evaluate('BOF_GENERAL_ACHIEVEMENTS.defs.every(d=>!!XART.get(d.plaque))'))
  base.close()
  page.reload();page.wait_for_function('window.TDGAME && TDGAME.G.state==="boot"',timeout=60000);page.evaluate('TDGAME.freeze()');frames(24)
  check('settings, achievements and campaign Continue survive a real reload',page.evaluate('TD.Frontend.settings.music===.5 && TD.Achievements.data.unlocked.warrior && BOF_GENERAL_ACHIEVEMENTS.points()===450 && TD.Frontend.titleItems().includes("CONTINUE")'))
  page.evaluate("TD.Frontend.returnTo='title';TD.Frontend.go('title')");frames(24);snap('title_continue')
  page.set_viewport_size({'width':520,'height':650});frames(2);snap('title_narrow')
  check('menus fit a narrow browser pane without cropping',page.evaluate('(()=>{const b=document.getElementById("screen").getBoundingClientRect();return b.left>=-.1&&b.right<=innerWidth+.1&&b.top>=-.1&&b.bottom<=innerHeight+.1;})()'))
  check('no browser, asset, decode or playback errors',not errors and page.evaluate('!TD.Audio.failures.length'))
  browser.close()
finally:stop()
(OUT/'verification.json').write_text(json.dumps({'checks':checks,'errors':errors,'observations':observations},indent=2),encoding='utf-8')
print(f'{sum(c["passed"] for c in checks)}/{len(checks)} checks passed',flush=True)
sys.exit(0 if all(c['passed'] for c in checks) and not errors else 1)
