from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R));rows=[]
def check(n,v):rows.append({'name':n,'pass':v});assert v,n;print('PASS',n,flush=True)
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page();p.goto(f'http://127.0.0.1:{port}/index.html?quality=high');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(150,150);p.keyboard.press('Enter')
  check('audio unlocks with an actual user gesture',p.evaluate("async()=>{await Snd._audioCtx().resume();return Snd._audioCtx().state==='running';}"))
  p.evaluate(shoot.TRAP_RAF)
  check('map entry clears a stale tutorial hover',p.evaluate("()=>{run.mode='campaign';campaign.unlockedMax=1;const r=cmap2BtnRects()[0];Input.mouse.x=r.x+r.w/2;Input.mouse.y=r.y+r.h/2;Input.mouse.moved=true;openStageSelect(1,{});stateT=2;cmap2BarInput(1,1);return cmap2.focus==='map'&&!campPause;}"))
  check('Space confirms on the map',p.evaluate("()=>{Input.clearTaps();Input.injectTap(' ');const consumed=campaignMenuInputTick();return !consumed&&Input.tap('enter')&&cmap2.focus==='map';}"))
  check('controller Start confirms on the map',p.evaluate("()=>{Input.clearTaps();Input.injectTap('pad_b9');return !campaignMenuInputTick()&&Input.tap('enter');}"))
  p.evaluate("()=>{Snd.prepare(['machineGun','expSmall']);Audio.stopMusic();}");p.wait_for_function("['machineGun','expSmall'].every(BOF_AUDIO_LATENCY_1106.ready)",timeout=20000,polling=50)
  check('portal reflection uses the shared decoded sample',p.evaluate("()=>{Snd._last={};Snd.setWarpMix(.8);Snd.play('expSmall');return [...AL116.active].some(v=>v.echo)&&AL116.active.size<=AL116.maxVoices;}"))
  check('leaving the portal cancels its reflection',p.evaluate("()=>{Snd.setWarpMix(0);return [...AL116.active].every(v=>!v.echo);}"))
  p.evaluate("async()=>{Snd.stopCue('machineGun');await Snd._audioCtx().suspend();Snd._last={};AL116.events=[];Snd.play('machineGun');Snd.stopCue('machineGun');}");p.wait_for_timeout(150)
  check('stopped pending cues never arrive late',p.evaluate("!AL116.events.some(v=>v.name==='machineGun')&&AL116.stats.cancelled>0"))
  check('Ice Breath keeps its native damage',p.evaluate("()=>{run.pilot='freezer';run.stage=2;run.weapon=4;run.wvars=[];run.wvars[4]='icebreath';return flameIsIce()&&flameDmg(5)===11;}"))
  check('Fire uses the revised damage curve',p.evaluate("()=>{run.pilot='axel';run.wvars[4]='flamethrower';return !flameIsIce()&&flameDmg(5)===24;}"))
  (W/'edge-results.json').write_text(json.dumps(rows,indent=2),encoding='utf8');b.close()
finally:stop()
