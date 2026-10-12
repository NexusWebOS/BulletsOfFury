"""Native Overdrive entrance/card/control/zoom QA; protected framing fixtures."""
from pathlib import Path
import json, sys
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
from shoot import serve
OUT=ROOT/'_shots/overdrive_intro_1011';OUT.mkdir(parents=True,exist_ok=True)
checks,errors,observations=[],[],{}

def check(name,value):
    checks.append({'name':name,'passed':bool(value)})
    print(('PASS ' if value else 'FAIL ')+name,flush=True)

def frames(n):
    while n>0:
        batch=min(24,n);page.evaluate('(n)=>TDGAME.step(n)',batch)
        page.wait_for_timeout(1);n-=batch

def tap(key):
    page.keyboard.down(key);frames(1);page.keyboard.up(key);frames(9)

def until(phase,limit=1200):
    for _ in range(limit//12):
        if page.evaluate('(p)=>TDGAME.G.bossIntro.phase===p',phase):return True
        frames(12)
    return False

def snap(name):
    page.evaluate('TDGAME.G.player.inv=0;TDGAME.render()')
    page.screenshot(path=str(OUT/(name+'.png')))
    page.evaluate('TDGAME.G.player.inv=99999')

def pixels():
    return page.evaluate('''()=>{const c=document.getElementById('screen').getContext('2d'),draw=c.drawImage,art=ART.draw,fill=c.fillText,keys=[],words=[];let key;
      ART.draw=function(ctx,k,...args){const old=key;key=k;try{return art.call(this,ctx,k,...args);}finally{key=old;}};
      c.drawImage=function(...args){if(key)keys.push(key);return draw.apply(this,args);};
      c.fillText=function(...args){words.push(args[0]);return fill.apply(this,args);};
      try{TDGAME.render();return {keys,words};}finally{c.drawImage=draw;ART.draw=art;c.fillText=fill;}}''')

port,stop=serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport={'width':1920,'height':1080})
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1011-boss-intro')
  page.wait_for_function('window.TDGAME&&TDGAME.G.state==="boot"',timeout=60000)
  page.evaluate('TDGAME.freeze()');page.keyboard.press('Enter')
  page.evaluate('TDGAME.start();TDGAME.G.units=[];TDGAME.G.props=[];TDGAME.G.player.y=830;TDGAME.G.player.inv=99999;TD.Cam.follow(400,806,1);TDGAME.render()')
  before=page.locator('#screen').bounding_box();snap('stage_close_1920')
  check('ordinary gameplay uses the requested close 640x480 field at 1:1 zoom',page.evaluate('TD.VW===640&&TD.VH===480&&TD.Cam.zoom===1'))
  check('fullscreen-sized canvas fills the available height proportionally',abs(before['height']-1076)<1 and abs(before['width']/before['height']-4/3)<.002)
  page.wait_for_function('TD.BossIntro.warm.every(k=>!!ART.get(k))')
  check('all 17 generated frames decode with their even registered sizes',page.evaluate('TD.BossIntro.warm.length===17&&TD.BossIntro.warm.every(k=>JSON.stringify(ART.size(k))===JSON.stringify(TD_BOSS_INTRO_ART.assets[k].size)&&ART.size(k).every(n=>n%2===0))'))
  check('all turntable views share one scale and grounded pivot',page.evaluate('new Set(TD_BOSS_INTRO_ART.turntable.map(k=>TD_BOSS_INTRO_ART.assets[k].scale)).size===1&&TD_BOSS_INTRO_ART.turntable.every(k=>TD_BOSS_INTRO_ART.assets[k].anchor.join(",")==="256,454")'))
  page.keyboard.down('w');frames(70)
  check('real driving triggers a boss entering from above the map',page.evaluate('TD.BossIntro.active(TDGAME.G)&&TDGAME.G.boss.y<0&&TDGAME.G.bossIntro.phase==="arrival"'))
  origin=page.evaluate('({x:TDGAME.G.player.x,y:TDGAME.G.player.y,hp:TDGAME.G.player.hp,time:TDGAME.G.time})')
  page.keyboard.down('j');page.keyboard.down('h');frames(40)
  early=page.evaluate('({y:TDGAME.G.boss.y,zoom:TD.Cam.zoom,cameraY:TD.Cam.y})');snap('arrival_early')
  check('entrance captures the arriving boss with a zoom above normal',early['zoom']>1.3)
  check('movement, fire, cannon charge and incoming damage are gated during the entrance',page.evaluate('(p)=>{const G=TDGAME.G;return G.player.x===p.x&&G.player.y===p.y&&G.player.hp===p.hp&&!G.shots.length&&!G.eshots.length&&G.player.charge===0}',origin))
  for key in ['w','j','h']:page.keyboard.up(key)
  tap('Enter');pause=page.evaluate('({phase:TDGAME.G.bossIntro.phase,t:TDGAME.G.bossIntro.t,y:TDGAME.G.boss.y,zoom:TD.Cam.zoom})');frames(60)
  check('Start pauses the entrance without moving its boss or camera clock',page.evaluate('(p)=>TDGAME.G.state==="pause"&&TDGAME.G.bossIntro.t===p.t&&TDGAME.G.boss.y===p.y&&TD.Cam.zoom===p.zoom',pause))
  tap('ArrowDown');tap('Enter');frames(20);snap('options_during_entrance')
  check('the original Options panel remains available during a paused entrance',page.evaluate('TDGAME.G.state==="options"&&TD.Display.w===480&&TD.Display.h===512&&TD.OriginalOptions.rows().filter(r=>r.t==="vol").length===4'))
  tap('b');tap('Enter');frames(115)
  late=page.evaluate('({y:TDGAME.G.boss.y,zoom:TD.Cam.zoom,cameraY:TD.Cam.y})');snap('arrival_follow')
  check('the camera follows south while pulling out as the tank gets closer',late['y']>early['y']+100 and late['cameraY']>early['cameraY'] and late['zoom']<early['zoom'])
  check('entry does not resize the screen or change its 640x480 field',page.evaluate('TD.VW===640&&TD.VH===480') and abs(page.locator('#screen').bounding_box()['width']-before['width'])<.1)
  check('the boss settles and opens its generated dossier',until('card'))
  frames(145)
  profile=page.evaluate('TDGAME.G.bossIntro.profile');observations['profile']=profile
  check('dossier reports actual 510 HP and the helmet-dependent 82% hull guard',profile['total']==510 and profile['armor']==82 and [p['hp'] for p in profile['targets']]==[85,85,120,220])
  words=pixels()
  check('the game context actually draws the generated card and yaw view', 'od_warrior_card' in words['keys'] and any(k.startswith('od_warrior_view_') for k in words['keys']))
  check('the card renders all four target labels with HP and attack descriptions',all(any(w.startswith(p['name']+' / ') and w.endswith(' HP') for w in words['words']) for p in profile['targets']) and all(a in words['words'] for a in profile['attacks']))
  check('the exact warning is drawn on the card', '"Stings like a butterfly,' in words['words'] and 'Tramples you like a giant ass tank that it is!"' in words['words'])
  check('all four health fills finish before the card can leave',page.evaluate('TDGAME.G.bossIntro.filled===4'))
  seen=set()
  for i in range(16):
    frames(12);seen.add(page.evaluate('TDGAME.G.bossIntro.frame'))
  check('natural showcase rotation actually draws every one of its 16 yaw views',len(seen)==16)
  page.evaluate('TDGAME.G.bossIntro.yaw=0');snap('card_front')
  page.evaluate('TDGAME.G.bossIntro.yaw=Math.PI');snap('card_back')
  check('a full 360-degree scan enables Continue',page.evaluate('TDGAME.G.bossIntro.turns>=1'))
  tap('ArrowDown');check('D-pad-style keyboard navigation selects the next target and opens inspection',page.evaluate('TDGAME.G.bossIntro.selected===1&&TDGAME.G.bossIntro.inspect'))
  beforeYaw=page.evaluate('TDGAME.G.bossIntro.yaw');page.keyboard.down('ArrowRight');frames(18);page.keyboard.up('ArrowRight')
  check('manual rotation remains available while inspecting a part',page.evaluate('(y)=>TDGAME.G.bossIntro.yaw>y+.5',beforeYaw))
  r=page.locator('#screen').bounding_box();page.mouse.click(r['x']+475*r['width']/640,r['y']+238*r['height']/480);frames(1)
  check('actual pointer selection inspects the head with its correct HP',page.evaluate('TDGAME.G.bossIntro.selected===2&&TDGAME.G.bossIntro.profile.targets[2].hp===120&&TDGAME.G.bossIntro.inspect'))
  snap('card_head_inspection')
  check('inspection draws the original BOF boss Retina on the rotating model', 'nbret_cole' in pixels()['keys'])
  page.evaluate("window.testPad={id:'Overdrive intro six-button fixture',connected:true,buttons:Array.from({length:16},()=>({pressed:false,value:0})),axes:[]};Object.defineProperty(navigator,'getGamepads',{value:()=>[testPad],configurable:true});window.pad=(...ids)=>testPad.buttons.forEach((b,i)=>{b.pressed=ids.includes(i);b.value=+b.pressed});pad(13)")
  frames(1);page.evaluate('pad()');frames(1)
  check('controller D-pad selects the body instead of moving the tank',page.evaluate('(p)=>TDGAME.G.bossIntro.selected===3&&TDGAME.G.player.x===p.x&&TDGAME.G.player.y===p.y',origin))
  page.evaluate('pad(1)');frames(1);page.evaluate('pad()');frames(2)
  check('controller B returns to the rotating overview without firing a shell',page.evaluate('!TDGAME.G.bossIntro.inspect&&!TDGAME.G.shots.length'))
  page.evaluate("Object.defineProperty(navigator,'getGamepads',{value:()=>[],configurable:true})")
  page.keyboard.press('Alt+Enter');page.wait_for_function('!!document.fullscreenElement')
  check('native fullscreen can change during the card without becoming Start',page.evaluate('TDGAME.G.bossIntro.phase==="card"&&TD.Display.w===640&&TD.Display.h===480'))
  page.keyboard.press('Alt+Enter');page.wait_for_function('!document.fullscreenElement')
  check('combat HP and the stage scoring clock remain unchanged throughout inspection',page.evaluate('(p)=>TDGAME.G.player.hp===p.hp&&TDGAME.G.time===p.time&&TDGAME.G.boss.hpFrac()===1&&!TDGAME.G.eshots.length',origin))
  page.keyboard.down('j');frames(19);snap('card_slide_out')
  check('Continue slides the card away while combat remains gated',page.evaluate('TDGAME.G.bossIntro.phase==="slide"&&!TDGAME.G.shots.length'))
  check('slide-out enters the camera restoration phase',until('restore'))
  z=page.evaluate('TD.Cam.zoom');frames(30)
  check('restoration gradually returns the camera towards normal zoom',page.evaluate('(z)=>TD.Cam.zoom<z&&TD.Cam.zoom>1',z))
  check('restoration finishes with normal combat and exactly 1:1 zoom',until('combat'))
  frames(12)
  check('a held inspection/fire button cannot discharge on return to combat',page.evaluate('TDGAME.G.introFireLatch&&!TDGAME.G.shots.length&&TDGAME.G.player.charge===0'))
  page.keyboard.up('j');frames(2);page.keyboard.down('j');frames(10);page.keyboard.up('j')
  check('releasing and pressing Fire again restores real weapon control',page.evaluate('!TDGAME.G.introFireLatch&&TDGAME.G.shots.length>0'))
  page.wait_for_function('TD.Audio.musicKey==="warrior"&&TD.Audio.music&&!TD.Audio.music.paused&&TD.Audio.music.readyState>=3',timeout=15000)
  check('supplied Warrior music begins after the introduction',page.evaluate('TD.Audio.music.currentSrc.endsWith("/expansion/topdown/audio/BOF-O-BOSS1.mp3")&&TD.Audio.music.loop'))
  check('arcade warning, scan beeps, confirmation fill and launch cues play',page.evaluate('["warn","intro","blip","lockon","forgeComplete","loadoutLaunch","alert"].every(k=>TD.Audio.stats[TD.Audio.resolve(k)]>0)'))
  observations['history']=page.evaluate('TDGAME.G.bossIntro.history');observations['camera']={'early':early,'late':late,'normal':page.evaluate('({x:TD.Cam.x,y:TD.Cam.y,zoom:TD.Cam.zoom})')}
  snap('combat_close')
  armor=page.evaluate('''()=>{const B=TDGAME.G.boss, before=B.parts.hull;B.damage('hull',100);
    const guarded=B.parts.hull;B.damage('helmet',999);B.damage('hull',100);
    return {guardedLoss:before-guarded,exposedLoss:guarded-B.parts.hull};}''')
  observations['armorDamage']=armor
  check('the card armor percentage matches actual guarded hull damage',abs(armor['guardedLoss']-18)<.001)
  check('breaking the displayed head target removes that hull protection',abs(armor['exposedLoss']-100)<.001)
  for width,height in [(1612,878),(1469,796),(520,650)]:
    page.set_viewport_size({'width':width,'height':height})
    # Native resize delivery is asynchronous; poll it before frozen-frame QA.
    page.wait_for_function('''()=>{const r=document.getElementById('screen').getBoundingClientRect();
      return Math.abs(r.width-640*Math.min(innerWidth/640,(innerHeight-4)/480))<.1;}''',timeout=5000)
    frames(1)
    r=page.locator('#screen').bounding_box()
    observations.setdefault('resize',{})[f'{width}x{height}']=r
    check(f'{width}x{height}: closer playfield fits proportionally without clipping the canvas',r['x']>=-.1 and r['y']>=-.1 and r['x']+r['width']<=width+.1 and r['y']+r['height']<=height+.1 and abs(r['width']/r['height']-4/3)<.002 and page.evaluate('TD.VW===640&&TD.VH===480'))
  page.evaluate('TDGAME.G.sel=0;TDGAME.start()')
  check('restart clears the old dossier and restores the close stage view',page.evaluate('TDGAME.G.bossIntro===null&&!TDGAME.G.boss&&TD.VW===640&&TD.VH===480&&TD.Cam.zoom===1'))
  check('no page, console, missing-file, decode or playback errors',not errors and page.evaluate('TD.Audio.failures.length===0'))
  browser.close()
finally:stop()
report={'checks':checks,'errors':errors,'observations':observations,'scope':__doc__}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'{sum(c["passed"] for c in checks)}/{len(checks)} checks passed',flush=True)
sys.exit(0 if all(c['passed'] for c in checks) and not errors else 1)
