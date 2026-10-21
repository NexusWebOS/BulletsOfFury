"""Native intro pixels, film beats, input, cues and actual map handoff."""
from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/intro_repair_1021';http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=shoot.serve(str(R));checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio','--autoplay-policy=no-user-gesture-required'])
  p=b.new_page(viewport=dict(width=1920,height=1080));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&ASSETS.ready&&typeof IP21!=="undefined"')
  p.evaluate(shoot.TRAP_RAF)
  p.evaluate('()=>{run.pilot="yuri";run.mode="campaign";campaignIntroStart();campaignIntroWarm();UI20.warm();Audio.init();}')
  p.wait_for_function('()=>campaignIntroKeys().every(k=>XART.rdy(k))&&bmfReady("dialogue")')
  p.evaluate('''()=>{window.ip21Tags=new WeakMap();window.ip21Draws=[];const get=XART.get,draw=ctx.drawImage,blit=ASSETS.blit;
   XART.get=function(k){const im=get.apply(this,arguments);if(im)ip21Tags.set(im,k);return im;};
   ctx.drawImage=function(im){ip21Draws.push({key:ip21Tags.get(im)||null,args:Array.from(arguments).slice(1)});return draw.apply(this,arguments);};
   window.ip21BulletDraws=0;ASSETS.blit=function(k){if(/bullet/i.test(k))ip21BulletDraws++;return blit.apply(this,arguments);};
   window.ip21GunCues=0;const mg=Audio.SFX.machineGun;Audio.SFX.machineGun=function(){ip21GunCues++;return mg.apply(this,arguments);};
   window.ip21Seek=t=>{campaignIntro.t=t;ip21Draws=[];ctx.setTransform(SS,0,0,SS,0,0);drawCampaignIntro(0);return{last:IP21.last,caption:IP21.caption,logo:IP21.logo,jet:IP21.jet,narration:IP21.narration,draws:ip21Draws,viewport:{w:cutsceneViewWidth(),h:VH}};};}''')
  # Every accepted source frame must blit through the real game context.
  for bank in p.evaluate('Object.keys(IP21_ART.banks)'):
   row=p.evaluate('''bank=>{const a=IP21_ART.banks[bank];ip21Draws=[];for(let i=0;i<a.frames;i++)ip21Blit(bank,i,240,240,a.w,a.h);
    const seen=ip21Draws.filter(d=>d.key===a.key);return{frames:a.frames,calls:seen.length,rects:seen.map(d=>d.args.slice(0,4)),w:a.w,h:a.h,columns:a.columns};}''',bank)
   ck(bank+' every fixed-canvas pose draws natively',row['calls']==row['frames'] and row['w']%2==0 and row['h']%2==0 and all(r==[i%row['columns']*row['w'],i//row['columns']*row['h'],row['w'],row['h']] for i,r in enumerate(row['rects'])),row)
   p.wait_for_timeout(20)
  for width,height in [(1920,1080),(1366,768),(390,844)]:
   p.set_viewport_size(dict(width=width,height=height));p.evaluate('_setCinematicViewport(true)');p.wait_for_timeout(100)
   for selector in ['federation','dispatch','turn','run','pilot','comic']:
    row=p.evaluate('''selector=>{const b=IP21.beats.find(b=>selector==='federation'?b.federation:selector==='pilot'?b.pilotCam==='axel':selector==='comic'?b.comic:b.dispatch===selector);return ip21Seek(selector==="run"||selector==="turn"?b.at+1.7:b.to-.6);}''',selector)
    d=row['caption'];v=row['viewport']
    if selector=='run':ck(str(width)+' running action stays unobstructed',d is None and row['last']['bank']=='run',row['last'])
    else:ck(str(width)+' '+selector+' caption fits completely',d['x']>=0 and d['y']>=0 and d['x']+d['w']<=v['w']+1 and d['y']+d['h']<=v['h']-35 and d['layout']['height']<=d['body']['h']+1,dict(bounds=[d[k] for k in ['x','y','w','h']],font=d['layout']['H'],body=d['body']))
    p.screenshot(path=str(O/(selector+'-'+str(width)+'.png')))
   row=p.evaluate('ip21Seek(IP21.finaleAt+1.0)')
   ck(str(width)+' actual Yuri hull and growing native thrusters',row['jet']['pilot']=='yuri' and row['jet']['key'].startswith('ship_yuri') and row['jet']['plume'] and row['jet']['power']>.9,row['jet'])
   p.screenshot(path=str(O/('logo-boost-'+str(width)+'.png')))
   row=p.evaluate('ip21Seek(IP21.finaleAt+.1)')
   ck(str(width)+' unchanged BOF logo is drawn with PixelLab effects',any(d['key']=='nbl_logo_0916' for d in row['draws']) and any(d['key']=='ip21_logo' for d in row['draws']),row['logo'])
   p.screenshot(path=str(O/('logo-flash-'+str(width)+'.png')))
   row=p.evaluate('ip21Seek(IP21.finaleAt+11.5)')
   ck(str(width)+' full mission and good-luck narration fit',row['narration']['budget']==len(row['narration']['text']) and row['narration']['tail']==len(row['narration']['last']) and row['narration']['layout']['height']<=row['narration']['body']['h']+1,row['narration'])
   p.screenshot(path=str(O/('mission-'+str(width)+'.png')))
  p.set_viewport_size(dict(width=1920,height=1080));p.evaluate('_setCinematicViewport(true)')
  for pilot in p.evaluate('PILOTS.map(p=>p.key)'):
   row=p.evaluate('''pilot=>{run.pilot=pilot;campaignIntroStart();const b=IP21.beats.find(b=>b.pilotCam===pilot);const a=ip21Seek(b.at+2);const im=a.draws.find(d=>d.key==='cin_pilot_'+pilot+'_helmet');return{last:a.last,im,narration:ip21Seek(IP21.finaleAt+11.5).narration};}''',pilot)
   ck(pilot+' uses its actual full-screen cockpit and own mission name',row['last']['fullScreen'] and row['last']['background']=='#000' and row['im'] is not None and pilot.upper() in row['narration']['text'].upper(),row)
  ck('Finale has no bullet rendering or machine-gun cue',p.evaluate('ip21BulletDraws===0&&ip21GunCues===0'),p.evaluate('({bullets:ip21BulletDraws,gunCues:ip21GunCues})'))
  # Cross the actual sound thresholds naturally rather than making seeks play cues.
  p.evaluate('()=>{run.pilot="yuri";campaignIntroStart();campaignIntro.t=IP21.finaleAt-.9;IP21.events=[];}')
  for i in range(40):
   p.evaluate('drawCampaignIntro(.05)')
   if i%8==0:p.wait_for_timeout(20)
  p.wait_for_timeout(250)
  cues=p.evaluate('''()=>({events:IP21.events,pools:Object.fromEntries(['hammerImpact','jetDash'].map(k=>[k,(Snd.pools[k]?.slots||[]).filter(Boolean).map(q=>({ready:q.el.readyState,time:q.el.currentTime,error:q.el.error?.code||null}))]))})''')
  ck('Logo impact and boost cues trigger once through the shared mixer',all(sum(e['id']==key and e['played'] for e in cues['events'])==1 for key in ['logo','boost']),cues)
  ck('Actual impact and engine audio decode and advance',all(any(q['ready']>=2 and q['time']>0 and not q['error'] for q in cues['pools'][key]) for key in ['hammerImpact','jetDash']),cues['pools'])
  # A reveals/advances; Start keeps the authored skip and completion owner.
  p.evaluate('()=>{window.ip21Done=0;campaignIntroStart(()=>ip21Done++);campaignIntro.t=1;stateT=1;Input.clearTaps();}')
  p.keyboard.press('j');p.evaluate('drawCampaignIntro(.016)');first=p.evaluate('campaignIntro?.t')
  p.keyboard.press('j');p.evaluate('drawCampaignIntro(.016)');second=p.evaluate('campaignIntro?.t')
  ck('Native A input reveals then advances one beat',first is not None and second is not None and second>first and p.evaluate('ip21Done===0'),[first,second])
  p.keyboard.press('Enter');p.evaluate('drawCampaignIntro(.016)')
  ck('Native Start skips through the original callback once',p.evaluate('ip21Done===1&&campaignIntro===null'))
  p.evaluate('()=>{window.ip21Done=0;window.ip21Film={frames:0,beats:[],banks:{},cues:[]};campaignIntroStart(()=>{ip21Done++;openStageSelect(1,{boot:true});});Input.clearTaps();stateT=1;IP21.events=[];}')
  for batch in range(200):
   running=p.evaluate('''()=>{for(let i=0;i<60&&campaignIntro;i++){
    ip21Draws=[];stateT+=1/30;drawCampaignIntro(1/30);ip21Film.frames++;
    const b=campaignIntro&&IP21.beats.find(b=>campaignIntro.t>=b.at&&campaignIntro.t<b.to);
    const id=b?b.dispatch||b.pilotCam||b.bg||(b.federation?'satellite':b.pilotLine||'flight'):'finale';
    if(ip21Film.beats.at(-1)!==id)ip21Film.beats.push(id);
    for(const d of ip21Draws){if(!d.key?.startsWith('ip21_'))continue;
     const bank=d.key.slice(5),a=IP21_ART.banks[bank],index=d.args[1]/a.h*a.columns+d.args[0]/a.w;
     const frames=ip21Film.banks[bank]||(ip21Film.banks[bank]=[]);if(!frames.includes(index))frames.push(index);}
   }return !!campaignIntro;}''')
   p.wait_for_timeout(10)
   if not running:break
  film=p.evaluate('({...ip21Film,cues:IP21.events})')
  ck('Entire opening advances naturally through dispatch, turn, run and finale',not running and all(s in film['beats'] for s in ['satellite','dispatch','turn','run','axel','cole','resolve','finale']),film)
  ck('Natural timeline displays every corruption and character animation frame',all(len(film['banks'].get(k,[]))==n for k,n in [('corruption',33),('dispatch',17),('turn',25),('run',33)]),film['banks'])
  ck('Natural final fade enters the actual campaign map once',p.evaluate('ip21Done===1&&campaignIntro===null&&state===GS.STAGESEL'),p.evaluate('({state,done:ip21Done})'))
  for i in range(12):
   p.evaluate(shoot.STEP,12);p.wait_for_timeout(20)
  p.screenshot(path=str(O/'map-handoff.png'))
  # Review controls must play the same native owner, not a separate mock film.
  p.goto(f'http://127.0.0.1:{port}/docs/previews/intro_repair_1021/index.html?scene=turn')
  p.wait_for_function('!document.querySelector("#replay").disabled')
  review=p.frame_locator('#game')
  game=p.frames[1]
  game.wait_for_function('window.BOF_INTRO_REPAIR&&campaignIntro?.t>=IP21.beats.find(b=>b.dispatch==="turn").at')
  p.select_option('#pilot','lizzie');p.select_option('#scene','launch');p.click('#replay')
  ck('Review replay and pilot selector use the actual opening',game.evaluate('campaignIntro?.pilot==="lizzie"&&campaignIntro?.t>=IP21.beats.find(b=>b.pilotLine==="resolve").at'))
  ck('No page, console, draw or asset errors',not errors,errors);b.close()
finally:stop()
q=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'native-report.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in q.items() if k!='checks'}));sys.exit(bool(q['failed']))
