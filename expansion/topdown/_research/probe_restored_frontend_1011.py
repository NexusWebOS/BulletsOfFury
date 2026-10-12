"""Native QA for the original-menu, sequential-voice and completion-gate correction.

Uses actual browser media time and real keyboard/pointer events. Controller
tests use the game's own polling with named test hardware. Completion hooks
use protected fixtures, not an unassisted campaign clear. Saves are isolated.
"""
from pathlib import Path
import hashlib,json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/overdrive_restored_1011';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];observations={}
def check(name,value):
 checks.append({'name':name,'passed':bool(value)});print(('PASS ' if value else 'FAIL ')+name,flush=True)
recipe=json.loads((ROOT/'expansion/topdown/audio/startup_reverb_1011.json').read_text())
check('Overdrive loudness matches the original call within 0.1 LUFS',abs(float(recipe['referenceLoudness']['input_i'])-float(recipe['processedLoudness']['input_i']))<.1)
check('original BOF title call remains byte-identical to the measured reference',hashlib.sha256((ROOT/recipe['reference']).read_bytes()).hexdigest()==recipe['referenceSha256'])
check('Mike\'s dry Overdrive WAV is preserved exactly',hashlib.sha256((ROOT/'expansion/topdown/audio/source/overdrive.wav').read_bytes()).hexdigest()==recipe['sourceSha256'])
prov=json.loads((ROOT/'expansion/topdown/_research/original_options_provenance_1011.json').read_text())
check('thirteen original renderer helpers are copied verbatim; Options adapts row/input data',sum(v['copiedVerbatim'] for v in prov['functions'].values())==13 and not prov['functions']['drawOptions']['copiedVerbatim'])
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();context=browser.new_context(viewport={'width':1400,'height':1100})
  page=context.new_page()
  def monitor(p):
   p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  monitor(page)
  page.add_init_script("if(!localStorage.getItem('bof_od_options'))localStorage.setItem('bof_od_options',JSON.stringify({master:.5,voice:.6,music:.4,sfx:.5,engine:1}));")
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1011-restored')
  page.wait_for_function('window.TDGAME && TDGAME.G.state==="boot"',timeout=60000);page.evaluate('TDGAME.freeze()')
  page.wait_for_function('TD.FRONT_WARM.every(k=>!!ART.get(k))',timeout=30000)
  def frames(n):
   while n:
    k=min(n,45);page.evaluate('n=>TDGAME.step(n)',k);page.wait_for_timeout(25);n-=k
  def tap(k,n=24):
   page.keyboard.down(k);frames(1);page.keyboard.up(k);frames(n)
  def go(s):
   page.evaluate("s=>{TD.Frontend.returnTo='title';TD.Frontend.go(s)}",s);frames(24)
  def snap(name):
   page.evaluate('TDGAME.render()');page.locator('#screen').screenshot(path=str(OUT/(name+'.png')))
  def click(x,y):
   r=page.locator('#screen').bounding_box();v=page.evaluate('TD.Display')
   page.mouse.move(r['x']+x*r['width']/v['w'],r['y']+y*r['height']/v['h']);page.mouse.down();frames(1);page.mouse.up();frames(20)
  def select(who,act):
   page.evaluate("([who,act])=>{const rows=TD.OriginalOptions.rows().filter(r=>r.t!=='head');TD.OriginalOptions.select(rows.findIndex(r=>r.who===who&&r.act===act));}",[who,act]);frames(1)
  def pad_button(i):
   page.evaluate('i=>testPad.buttons[i].pressed=true',i);frames(1);page.evaluate('i=>testPad.buttons[i].pressed=false',i);frames(20)
  frames(24);tap('Enter')
  page.wait_for_function('TD.Frontend.voice?.readyState>=3 && TD.Frontend.voice.currentTime>0',timeout=15000)
  page.evaluate('window.bofCall=TD.Frontend.voice;window.pendingCall=TD.Frontend.voiceClips[1]')
  check('the first call is the actual original announce.mp3',page.evaluate('TD.Frontend.voicePhase==="bof" && bofCall.currentSrc.endsWith("/announce.mp3") && !bofCall.paused && pendingCall.paused'))
  check('saved Voice and Master gains apply to the original call',page.evaluate('Math.abs(bofCall.volume-.3)<1e-6 && bofCall.playbackRate===1'))
  snap('bof_call');frames(220)
  check('title music waits while the original call plays',page.evaluate('TDGAME.G.state==="intro" && !TD.Audio.music'))
  page.wait_for_function('TD.Frontend.voicePhase==="overdrive" && TD.Frontend.voice.currentTime>0',timeout=15000)
  check('enhanced Overdrive starts after the BOF call ends',page.evaluate('bofCall.ended && bofCall.paused && TD.Frontend.voice===pendingCall && !pendingCall.paused && pendingCall.currentSrc.endsWith("/overdrive-reverb_1011.mp3")'))
  check('Overdrive retains natural pitch, saved gain and its added echo tail',page.evaluate('pendingCall.playbackRate===1 && Math.abs(pendingCall.volume-.3)<1e-6 && pendingCall.duration>3.7'))
  observations['audio']=page.evaluate('({leadSeconds:bofCall.duration,overdriveSeconds:pendingCall.duration,voiceGain:pendingCall.volume})')
  page.wait_for_function('TD.Frontend.voice.currentTime>.6',timeout=10000);frames(30);snap('overdrive_call')
  page.wait_for_function('TD.Frontend.voiceDone',timeout=15000);frames(24)
  page.wait_for_function('TD.Audio.music?.currentTime>0',timeout=15000)
  check('title begins only after the final echo ends',page.evaluate('TDGAME.G.state==="title" && pendingCall.ended && TD.Audio.musicKey==="title" && TD.Frontend.voice===null'))
  page.evaluate('TD.Frontend.boot()');frames(24);tap('Enter');page.wait_for_function('TD.Frontend.voice?.currentTime>0');page.evaluate('window.skippedClips=TD.Frontend.voiceClips.slice()');tap('b')
  check('B skips and stops both current and queued calls',page.evaluate('TDGAME.G.state==="title" && skippedClips.every(v=>v.paused) && !TD.Frontend.voiceClips.length'))

  go('difficulty');page.evaluate('TD.Frontend.sel=4');frames(1);snap('insanity_locked');tap('Enter')
  check('fresh Insanity is visibly locked and cannot be confirmed',page.evaluate('!TD.Frontend.insanityUnlocked() && TDGAME.G.state==="difficulty" && TD.Frontend.message.includes("UNLOCK INSANITY")'))
  go('password');page.evaluate("TD.Frontend.pw=TD.Password.encode(0,'cole','insanity','hotwire');TD.Frontend.submit()")
  check('an Insanity password cannot bypass the completion gate',page.evaluate('TDGAME.G.state==="password" && TD.Frontend.message.includes("UNLOCK INSANITY")'))
  page.evaluate("TD.difficulty='insanity';TDGAME.G.sel=0;TDGAME.start()")
  check('direct campaign launch also enforces the Insanity gate',page.evaluate('TD.difficulty==="furious"'))

  go('pilot');page.evaluate("TD.pilot='cole'");frames(90);snap('pilot_grid')
  grid=page.evaluate('TD.pilotRects');observations['pilotGrid']=grid
  check('the pilot screen contains exactly two horizontal rows of six',len(grid)==12 and len({r[1] for r in grid})==2 and all(sum(v[1]==y for v in grid)==6 for y in {r[1] for r in grid}))
  check('every avatar and ship remains inside the pilot viewport',all(r[0]>=0 and r[0]+r[2]<=640 and r[1]+r[3]<456 for r in grid))
  tap('ArrowDown');check('vertical pilot navigation moves exactly six slots',page.evaluate("TD.PILOTS.indexOf(TD.pilot)===2")) # Cole index 8 -> index 2.
  tap('ArrowUp');check('up returns to the corresponding slot in the other row',page.evaluate("TD.pilot==='cole'"))
  click(23+3*100+72,398+22);check('clicking a lower-row ship selects its matching pilot',page.evaluate("TD.pilot==='hotwire'"))

  go('options');page.wait_for_function('document.fonts.check("11px BOFmil")');snap('original_options')
  check('Options uses the original 480x512 panel viewport',page.evaluate('TD.Display.w===480 && TD.Display.h===512'))
  check('original four volume rows replace the custom tabs',page.evaluate('TD.OriginalOptions.rows().filter(r=>r.t==="vol").map(r=>r.k).join(",")==="master,music,sfx,voice" && TD.OriginalOptions.rows()[0].label==="VOLUME"'))
  tap('ArrowLeft');check('original segmented Master slider changes real media gain by 10%',page.evaluate('Math.abs(TD.Frontend.settings.master-.4)<1e-6 && Math.abs(TD.Audio.music.volume-.16)<1e-6'))
  click(340,96);check('the original volume strip supports actual pointer adjustment',page.evaluate('Math.abs(TD.Frontend.settings.master-.8)<1e-6'))
  click(125,455);check('original Cancel restores all four volumes and returns to title',page.evaluate('TDGAME.G.state==="title" && TD.Frontend.settings.master===.5 && TD.Frontend.settings.voice===.6'))
  go('options');tap('ArrowDown');tap('ArrowDown');tap('ArrowDown');tap('ArrowRight');click(350,455)
  check('original Apply persists Voice volume and returns to title',page.evaluate('TDGAME.G.state==="title" && TD.Frontend.settings.voice===.7 && JSON.parse(localStorage.bof_od_options).voice===.7'))
  go('options');select(1,'left');tap('Enter');check('the original key cap arms keyboard capture',page.evaluate('TD.OriginalOptions.snapshot().capture==="left" && TD.OriginalOptions.snapshot().who===1'))
  tap('y');check('keyboard capture updates the actual movement binding',page.evaluate('TD.BIND.left[0]==="y" && !TD.OriginalOptions.snapshot().capture'))
  tap('b');check('Cancel restores the actual prior keyboard binding',page.evaluate('TD.BIND.left[0]==="a" && TDGAME.G.state==="title"'))
  go('options');select(1,'left');tap('Enter');tap('Backspace');check('Backspace is reserved for text and leaves binding capture alone',page.evaluate('TDGAME.G.state==="options" && TD.OriginalOptions.snapshot().capture==="left"'));tap('Escape');check('Escape cancels capture without closing Options',page.evaluate('TDGAME.G.state==="options" && !TD.OriginalOptions.snapshot().capture && TD.BIND.left[0]==="a"'))
  page.mouse.wheel(0,600);page.wait_for_timeout(60);frames(3);check('wheel scrolling moves the original options panel',page.evaluate('TD.OriginalOptions.snapshot().scroll>0'))

  page.evaluate("window.testPad={id:'Overdrive restored-menu QA',index:0,connected:true,mapping:'standard',axes:[0,0,0,0],buttons:Array.from({length:20},()=>({pressed:false}))};Object.defineProperty(navigator,'getGamepads',{configurable:true,value:()=>[testPad]});")
  frames(1);select(2,'L');snap('original_controller');tap('Enter');pad_button(10)
  check('the original controller key cap captures a real polled shoulder assignment',page.evaluate('TD.Input.padProfile().L===10 && !TD.OriginalOptions.snapshot().capture'))
  select(2,'R');tap('Enter');pad_button(11)
  check('Retina can be assigned independently to the other shoulder',page.evaluate('TD.Input.padProfile().R===11 && TD.Input.padProfile().L===10'))
  click(125,455);check('Cancel restores the previous L/R physical assignments',page.evaluate('TD.Input.padProfile().L===6 && TD.Input.padProfile().R===7 && TDGAME.G.state==="title"'))
  go('options');select(2,'L');tap('Enter');pad_button(10);select(2,'R');tap('Enter');pad_button(11);click(350,455)
  check('Apply persists controller assignments through the original menu',page.evaluate('JSON.parse(localStorage.bof_td_controllers)[testPad.id].L===10 && JSON.parse(localStorage.bof_td_controllers)[testPad.id].R===11'))
  # Actual gameplay proves the menu adapter writes bindings that the tank uses.
  page.evaluate("TDGAME.G.sel=0;TD.difficulty='normal';TDGAME.start();TDGAME.G.units=[];TDGAME.G.structures=[];TDGAME.G.props=[];TD.World.load(800,4000,[]);TDGAME.G.player.inv=99999;TDGAME.G.player.y=2200;TD.Input.pointer.active=false;")
  page.keyboard.down('d');frames(12);page.keyboard.up('d');page.evaluate('testPad.buttons[10].pressed=true');frames(12)
  check('the newly bound L button activates live cruise/free aim',page.evaluate('TDGAME.G.player.cruising && TDGAME.G.player.moving'))
  page.evaluate('testPad.buttons[11].pressed=true');frames(12)
  check('the newly bound R button activates live Retina',page.evaluate('TD.Input.down("retina") && TDGAME.G.player.retina'))
  page.evaluate('testPad.buttons.forEach(b=>b.pressed=false)');frames(1);tap('Enter');snap('pause_buttons')
  check('pause draws the generated Return to Main Menu plate',page.evaluate('TDGAME.G.state==="pause" && ART.get("od_btn_return_to_main_menu") && TD.Frontend.rects.length===4'))
  go('options');select(2,'learn');tap('Enter');check('the original controller menu opens full physical-button learning',page.evaluate('TDGAME.G.state==="padsetup" && TD.Input.setup.steps.includes("L") && TD.Input.setup.steps.includes("R")'))
  tap('b');check('returning from learning preserves the Options transaction',page.evaluate('TDGAME.G.state==="options" && TD.OriginalOptions.snapshot().rows.some(r=>r.act==="learn")'))
  index=page.evaluate('TD.OriginalOptions.rows().filter(r=>r.t!=="head").findIndex(r=>r.t==="reset")');page.evaluate('i=>TD.OriginalOptions.select(i)',index);frames(1);tap('Enter');check('original Reset Controls restores keyboard and physical pad defaults',page.evaluate('TD.BIND.left[0]==="a" && TD.Input.padProfile().L===6 && TD.Input.padProfile().R===7'))
  click(350,455)

  for sel in [0,2,3]:
   page.evaluate("sel=>{TDGAME.G.sel=sel;TD.difficulty='normal';TDGAME.start();TDGAME.G.results={};TD.Frontend.saveClear(TDGAME.G);}",sel)
   if sel!=3:check('clearing mission '+str(sel)+' alone does not unlock Insanity',page.evaluate('!TD.Frontend.insanityUnlocked()'))
  check('completing the campaign unlocks Insanity and saves that unlock',page.evaluate('TD.Frontend.insanityUnlocked() && JSON.parse(localStorage.bof_od_unlocks).insanity===true'))
  page.reload();page.wait_for_function('window.TDGAME && TDGAME.G.state==="boot"',timeout=60000);page.evaluate('TDGAME.freeze()');frames(24)
  check('campaign unlock and applied Voice volume survive a real reload',page.evaluate('TD.Frontend.insanityUnlocked() && TD.Frontend.settings.voice===.7'))
  go('difficulty');page.evaluate('TD.Frontend.sel=4');frames(1);snap('insanity_unlocked');tap('Enter')
  check('completed-game Insanity can now enter the pilot screen',page.evaluate('TDGAME.G.state==="pilot" && TD.difficulty==="insanity"'))
  page.set_viewport_size({'width':520,'height':650});frames(150);snap('pilot_narrow');check('the two-row pilot grid fits a narrow browser pane',page.evaluate('(()=>{const r=document.getElementById("screen").getBoundingClientRect();return r.left>=-.1&&r.right<=innerWidth+.1&&r.bottom<=innerHeight+.1;})()'))
  go('options');snap('options_narrow');check('the original Options menu fits a narrow browser pane',page.evaluate('(()=>{const r=document.getElementById("screen").getBoundingClientRect();return r.left>=-.1&&r.right<=innerWidth+.1&&r.bottom<=innerHeight+.1;})()'))
  go('help');frames(2);snap('help_fullscreen')
  check('new button cells use even registered dimensions',page.evaluate('["return_to_main_menu","fullscreen","windowed","locked"].every(k=>TD_UI_ART.assets["od_btn_"+k].size.every(n=>n%2===0))'))

  fs=context.new_page();monitor(fs);fs.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=1')
  fs.wait_for_function('window.TDGAME && TDGAME.G.state==="boot"',timeout=60000);fs.evaluate('TDGAME.freeze();TDGAME.step(24)')
  fs.keyboard.down('Enter');fs.evaluate('TDGAME.step(1)');fs.keyboard.up('Enter');fs.evaluate('TDGAME.step(24)')
  fs.wait_for_function('!!document.fullscreenElement',timeout=15000)
  check('the default fullscreen launch enters native fullscreen on Start',fs.evaluate('TD.Fullscreen.auto && !!document.fullscreenElement && document.getElementById("fs-btn").getAttribute("aria-pressed")==="true"'))
  fs.locator('#fs-btn').click();fs.wait_for_function('!document.fullscreenElement',timeout=15000)
  check('the generated Windowed button exits native fullscreen',fs.evaluate('!TD.Fullscreen.isOn() && document.getElementById("fs-btn").getAttribute("aria-label")==="Enter fullscreen"'))
  fs.keyboard.down('Alt');fs.keyboard.down('Enter');fs.evaluate('TDGAME.step(1)');fs.keyboard.up('Enter');fs.keyboard.up('Alt');fs.evaluate('TDGAME.step(24)');fs.wait_for_function('!!document.fullscreenElement',timeout=15000)
  check('Alt+Enter also enters fullscreen',fs.evaluate('TD.Fullscreen.isOn()'))
  check('the fullscreen chord does not act as Start or skip the intro',fs.evaluate('TDGAME.G.state==="intro" && !!TD.Frontend.voice'))
  fs.keyboard.press('Escape');fs.wait_for_function('!document.fullscreenElement',timeout=15000)
  check('Escape exits native fullscreen without trapping the player',fs.evaluate('!TD.Fullscreen.isOn()'))
  fs.close()
  check('no page, console, asset, decode or playback errors',not errors and page.evaluate('!TD.Audio.failures.length'))
  browser.close()
finally:stop()
report={'date':'2026-10-11','entry':'expansion/topdown/index.html','build':'overdrive1011-restored','checks':checks,'browserErrors':errors,'observations':observations,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'scope':__doc__}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'{report["passed"]}/{len(checks)} checks passed',flush=True)
sys.exit(0 if not report['failed'] and not errors else 1)
