"""Render the new pilot identities, dialogue and Rebel masters through the real game context."""
import base64,json
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import GAME,serve,TRAP_RAF,SETUP,STEP
OUT=Path('_shots/portraits_rebels_0922');OUT.mkdir(exist_ok=True)
PILOTS=['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri']
POSES=['idle','happy','laugh','anger','sad','crash','victory','talk-closed','talk-small','talk-medium','talk-wide','talk-o']
SHIPS=['voss_iron_vulture','nyx_ghostknife','rook_breachhammer','kaia_signal_wraith','jace_razorjack']
errors=[];results={};port,stop=serve(GAME)
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  context=browser.new_context(storage_state={'cookies':[],'origins':[]},viewport={'width':1280,'height':900})
  page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.goto(f'http://127.0.0.1:{port}/index.html');page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=60000);page.evaluate(TRAP_RAF)
  def ev(s,a=None):return page.evaluate(s,a)
  def step(n):
   while n>0:
    e=ev(STEP,min(n,60));assert not e,e;n-=60;page.wait_for_timeout(25)
  def cap(name): (OUT/(name+'.png')).write_bytes(base64.b64decode(ev('()=>cv.toDataURL().split(",")[1]')))
  keys=['port_cf_'+p+'_'+e for p in PILOTS for e in POSES]+['comm_'+p+'_'+e for p in PILOTS for e in POSES]+['pav_'+p for p in PILOTS]+['cole_body_0922']+['rr_ship_'+s for s in SHIPS]+['rr_portrait_'+p for p in ['voss','nyx','rook','kaia','jace']]
  page.wait_for_function('ks=>ks.map(k=>XART.rdy(k)).every(Boolean)',arg=keys,timeout=60000)
  results['readyAssets']=len(keys)
  results['aliases']=ev('''ps=>{const sig=k=>{const c=document.createElement('canvas');c.width=c.height=64;c.getContext('2d').drawImage(XART.get(k),0,0,64,64);return c.toDataURL();};return ps.map(p=>({pilot:p,legacy:sig('port_'+p+'_idle')===sig('port_cf_'+p+'_idle'),face:sig('face_'+p)===sig('port_cf_'+p+'_idle'),avatar:sig('pav_'+p)===sig('port_cf_'+p+'_idle')}));}''',PILOTS)
  assert all(r['legacy'] and r['face'] and r['avatar'] for r in results['aliases'])
  ev(SETUP,{'state':'PILOT','stage':1,'pilot':'cole'});ev("()=>{coleUnlocked=true;pilotIndex=PILOTS.findIndex(p=>p.key==='cole');}");step(100);cap('cole_pilot_select')
  results['coleBody']=ev("()=>({select:psBodyKey('cole'),cinematic:cutPose('cole',0,true),intro:campaignIntroPortraitKey('cole')})")
  assert set(results['coleBody'].values())=={'cole_body_0922'}
  ev(SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':True});step(30)
  # Actual dlgBox and real ctx.drawImage. Record requested XART keys rather than unreliable .src.
  for p in PILOTS:
   step(1)
   ev('''p=>{const get=XART.get;window.portraitReads=[];XART.get=function(k){portraitReads.push(k);return get.call(this,k);};try{dlgBox({who:p.toUpperCase(),portrait:p,emo:'idle',full:'COPY. ALL SYSTEMS READY. KEEP YOUR EYES ON THE SKY.',shown:'COPY. ALL SYSTEMS READY. KEEP YOUR EYES ON THE SKY.',fade:1});}finally{XART.get=get;}}''',p)
   assert 'comm_'+p+'_idle' in ev('()=>portraitReads')
   cap('dialogue_'+p)
  # All emotions in one native renderer review surface.
  ev('''({ps,poses})=>{ctx.save();ctx.setTransform(2,0,0,2,0,0);ctx.fillStyle='#080c13';ctx.fillRect(0,0,cv.width/2,cv.height/2);const w=cv.width/2,h=cv.height/2,cw=w/12,ch=h/9;ps.forEach((p,row)=>poses.forEach((e,col)=>{const im=XART.get('port_cf_'+p+'_'+e);ctx.drawImage(im,col*cw,row*ch,Math.min(cw,ch)-2,Math.min(cw,ch)-2);}));ctx.restore();}''',{'ps':PILOTS,'poses':POSES});cap('all_expressions')
  # The five new ships are art assets; no existing boss encounter is silently replaced.
  ev('''ss=>{ctx.save();ctx.setTransform(2,0,0,2,0,0);const w=cv.width/2,h=cv.height/2;ctx.fillStyle='#18242d';ctx.fillRect(0,0,w,h);ss.forEach((s,i)=>{const im=XART.get('rr_ship_'+s),cw=w/5;ctx.drawImage(im,i*cw+8,h*.22,cw-16,(cw-16)*416/352);msgText(s.split('_')[0].toUpperCase(),(i+.5)*cw,h*.78,12,'#ffffff',1,1);});ctx.restore();}''',SHIPS);cap('rebel_fleet')
  ev("()=>{run.mode='campaign';run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');campaignIntroPilot=null;campaignIntroStart(()=>setState(GS.CAMPHUB));}")
  page.wait_for_function('()=>campaignIntroReady()',timeout=30000);step(650);cap('cole_campaign_intro')
  results['intro']=ev('()=>({state,t:campaignIntro.t,portrait:campaignIntroPortraitKey(campaignIntro.pilot)})')
  assert results['intro']['portrait']=='cole_body_0922' and results['intro']['t']>10
  assert not errors,errors
  browser.close()
finally:stop()
results['errors']=errors;(OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS',results['readyAssets'],'assets; nine pilot aliases, native dialogue, Cole selection/intro and five ship masters; zero browser errors.')
