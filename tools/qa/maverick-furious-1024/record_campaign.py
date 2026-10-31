from pathlib import Path
import asyncio,functools,http.server,threading,json,time,base64,traceback,os
from playwright.async_api import async_playwright
W=Path(__file__).resolve().parent
R=Path(os.environ['BOF_GAME_ROOT']).resolve()
O=W/'review';O.mkdir(exist_ok=True)
SLUG='maverick-furious-full-campaign'
http.server.ThreadingHTTPServer.request_queue_size=128
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_POST(self):
  if self.path!='/__capture/'+SLUG:self.send_error(400);return
  d=self.rfile.read(int(self.headers['Content-Length']));p=O/(SLUG+'.webm');offset=int(self.headers['X-Capture-Offset']);size=p.stat().st_size if p.exists()else 0
  if size==offset:
   with p.open('ab')as f:f.write(d)
  else:
   with p.open('rb')as f:f.seek(offset);same=f.read(len(d))==d
   if not same:self.send_error(409);return
  self.send_response(200);self.end_headers();self.wfile.write(b'ok')
async def main():
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(R)));server.daemon_threads=True
 threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_address[1]}'
 (W/'host.json').write_text(json.dumps({'url':url,'pid':os.getpid()}));print('SERVER',url,flush=True)
 errors=[];console=[];assets=[];failed=[]
 async with async_playwright()as pw:
  browser=await pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows'],headless=True)
  context=await browser.new_context(viewport={'width':1280,'height':720},accept_downloads=True)
  p=await context.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:console.append(m.text)if m.type=='error'else None)
  p.on('response',lambda r:assets.append({'status':r.status,'url':r.url})if r.status>=400 else None)
  p.on('requestfailed',lambda r:failed.append({'url':r.url,'failure':r.failure}))
  try:
   await p.goto(url,wait_until='load',timeout=180000);await p.wait_for_function('window.__bofFrames>5&&typeof RB23!=="undefined"',timeout=120000)
   await p.keyboard.press('Shift',delay=90)
   await p.add_script_tag(content=(W/'campaign_bot.js').read_text(encoding='utf-8'))
   setup=await p.evaluate('(c)=>FURYBOT.start(c)',{'id':SLUG,'limit':14400,'role':'campaign'})
   print('SETUP',json.dumps(setup),flush=True)
   lastPrint=0;nextShot=5;previous='';stateAt=time.time();nextMenu=0;mapPrepared=False;want9=False
   while True:
    await asyncio.sleep(1)
    control=W/'control.js'
    if control.exists():
     code=control.read_text(encoding='utf-8');control.rename(W/f'control-applied-{int(time.time())}.js');print('CONTROL',await p.evaluate(code),flush=True)
    s=await p.evaluate('''()=>({t:FURYBOT.age(),state,stateT,stage:run.stage,pilot:run.pilot,diff:diffKey,hp:FURYBOT.health(),phase:FURYBOT.phase(),sim:stageTimer,god:DBGT.god,lives:run.lives,bombs:run.bombs,weapon:run.weapon,level:run.wlevel,score:run.score,done:FURYBOT.finished,saved:FURYBOT.saved,error:FURYBOT.error,frames:FURYBOT.frames,player:{x:player.x,y:player.y,dead:player.dead},scene:BOFCinematicDirector.current?.id,story:story?{i:story.i,t:story.t}:null,fb2:typeof fb2Talk!=="undefined"&&fb2Talk?{i:fb2Talk.i,t:fb2Talk.t}:null,route:s6Wing?.route,choice:s6Wing?.choice,stageX:campaign.stageX1004,xrun:run._gp4StageX,unlocked:campaign.unlockedMax,bonus:campaign.bonusUnlocked,rank:campaign.rank,ssel:typeof sselCursor!=="undefined"?sselCursor:null,forge:typeof forge!=="undefined"&&forge?{row:forge.row,sel:forge.sel}:null,ending:drawVictory._t,trueFinale:run._trueFinaleCleared,cinema:typeof campaignIntro!=="undefined"&&campaignIntro?{t:campaignIntro.t}:null})''')
    stateKey=str(s['state'])+'|'+str(s['stage'])+'|'+str(s.get('xrun'))
    changed=stateKey!=previous
    if changed:previous=stateKey;stateAt=time.time();mapPrepared=False
    (O/'live.json').write_text(json.dumps(s,indent=2),encoding='utf-8')
    with (O/'host-telemetry.jsonl').open('a',encoding='utf-8')as f:f.write(json.dumps(s)+'\n')
    if changed or s['t']-lastPrint>29:print('PROGRESS',json.dumps(s),flush=True);lastPrint=s['t']
    if s['t']>nextShot or changed:
     await p.screenshot(path=str(O/f'screen-{int(s["t"]):05}.png'))
     raw=await p.evaluate('()=>FURYBOT.capture.toDataURL("image/png").split(",")[1]');(O/f'capture-{int(s["t"]):05}.png').write_bytes(base64.b64decode(raw));nextShot=s['t']+35
    if s['done']:
     if s.get('saved'):break
     continue
    elapsed=time.time()-stateAt
    if time.time()<nextMenu:continue
    st=s['state']
    if st=='stagesel' and elapsed>8:
     if s.get('stageX') and not s['stageX'].get('done'):
      # This is exactly the earned map action, after the unchosen route escapes.
      await p.evaluate('()=>{FURYBOT.events.push({t:FURYBOT.age(),type:"menu-select",action:"Earned Stage X Harrier pursuit"});cf4LaunchX();}')
     else:
      # Select only already earned stages. No unlock or campaign progress writes.
      await p.evaluate('()=>{if(campaign.bonusUnlocked&&!campaign.rank[9])sselCursor=9;else sselCursor=clamp(campaign.unlockedMax||1,1,8);if(cmap2)cmap2.focus="map";}')
      await p.keyboard.press('j',delay=90)
     nextMenu=time.time()+5
    elif st in ['forge','loadout','supplies'] and elapsed>5:
     await p.keyboard.press('p');await p.keyboard.press('Enter');nextMenu=time.time()+3
    elif st in ['stageclear','unlocks','powers','forged','yuriup'] and elapsed>7:
     await p.keyboard.press('Enter');nextMenu=time.time()+3
    elif st=='continue' and elapsed>4:
     await p.keyboard.press('Enter');nextMenu=time.time()+3
    elif st=='play' and s.get('choice') and not s.get('route'):
     await p.keyboard.press('d');nextMenu=time.time()+1
    elif st=='play' and s.get('story') and not s.get('scene') and elapsed>6:
     await p.keyboard.press('j');nextMenu=time.time()+5
    elif st not in ['play','victory','stagesel','intro','launch','outbound','flyover','warpentry','hq','cinematic','campaignintro','cutscene','opening'] and elapsed>18:
     await p.keyboard.press('Enter');nextMenu=time.time()+5
   report=await p.evaluate('()=>FURYBOT.report()');report.update(pageErrors=errors,consoleErrors=console,assetErrors=assets,failedRequests=failed)
   (O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('DONE',report['reason'],report['elapsed'],flush=True)
  except Exception as e:
   print('ERROR',repr(e),flush=True);traceback.print_exc()
   try:
    await p.evaluate('()=>FURYBOT.stop("host-error")');await asyncio.sleep(4)
    report=await p.evaluate('()=>FURYBOT.report()');report.update(hostError=str(e),pageErrors=errors,consoleErrors=console,assetErrors=assets,failedRequests=failed)
    (O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
   except:pass
  finally:await context.close();await browser.close();server.shutdown()
if __name__=='__main__':asyncio.run(main())
