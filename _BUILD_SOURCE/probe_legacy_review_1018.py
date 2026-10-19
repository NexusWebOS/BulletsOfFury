"""Native review UI, committed attack geometry and complete visible art banks."""
from pathlib import Path
import json,sys,http.server,base64
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/late_legends_1018/native';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/legacy_legion_1018/index.html?stage=7&scene=ll18brood&difficulty=furious')
  p.wait_for_function('ready&&!busy');w=p.frames[1];w.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(35)
  def frames(n):
   for i in range(0,n,12):w.evaluate(shoot.STEP,min(12,n-i));p.wait_for_timeout(5)
  def choose(mode,stage=None):
   if stage is not None:p.select_option('#stage',str(stage));p.wait_for_function('!busy')
   p.select_option('#scene',mode);p.wait_for_function('!busy')
  def until(expr,limit=1500):
   for i in range(limit//12):
    if w.evaluate(expr):return True
    frames(12)
   return False
  def snap(name):
   w.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}');p.screenshot(path=str(O/(name+'.png')))
  check('Fresh Stage7 loads fighter rounds and toxic bullets before combat',w.evaluate('XART.rdy("fr27_realm_ordnance")&&XART.rdy("cfx_stage7_toxic_projectiles_v2")'))
  check('Fresh Stage7 carrier fighters attack without a prior Stage8 visit',until('enemies.some(e=>e._ll18Escort&&e._frRealmAI?.seq>0)'))
  snap('review-cold-stage7-launch');choose('ll18raptor',8);frames(120)
  row=w.evaluate('({isolated:__legacyReviewStorage,mode:SC12.mode,field:SC12.layout.field,bg:curStage.bg})')
  check('Review uses the full native playfield, side HUD and isolated saves',row['isolated'] and row['mode']=='sides' and row['field']['h']>800,row)
  check('Raptor reaches a genuine ion-lance warning',until('LL18.events.some(e=>e.event==="tell"&&e.attack==="special")'))
  snap('review-raptor-warning')
  warn=w.evaluate('''()=>{const e=enemies.find(e=>e._ll18),A=e._ll18;window.fixedLanes=A.lanes.map(l=>({...l}));return{count:A.lanes.length,origins:A.lanes.every((l,i)=>Math.hypot(l.x-ll18Mount(e,i).x,l.y-ll18Mount(e,i).y)<.01)};}''')
  check('FOV lanes originate on the current physical wing emitters',warn['count']==2 and warn['origins'],warn)
  w.evaluate('player.x=camRightX()-30');check('Raptor releases its warned ion lances',until('LL18.beams.length>0'))
  geo=w.evaluate('''()=>({same:LL18.beams.every((l,i)=>['x','y','ex','ey','width'].every(k=>Math.abs(l[k]-fixedLanes[i][k])<.01)),clear:LL18.beams.every(l=>s81003Distance(player.x,player.y,l)>l.width+5),hp:enemies.find(e=>e._ll18).hp})''')
  check('Released beams use the exact committed FOV and can be evaded',geo['same'] and geo['clear'],geo);snap('review-raptor-live-lances')
  choose('ll18spear');check('Cryo Spear prepares its artillery',until('groundTargetingFx.some(q=>q.owner?._ll18&&!q.impact)'))
  rows=w.evaluate('''()=>groundTargetingFx.filter(q=>q.owner?._ll18).map(q=>({x:q.x,y:q.y,track:q.track,warn:q.warn}))''')
  check('Ice artillery has spaced, fixed Retina targets and a full warning',len(rows)>=2 and all(not q['track'] and q['warn']>=1.2 for q in rows) and all(abs(rows[i]['x']-rows[i-1]['x'])>=69 for i in range(1,len(rows))),rows)
  snap('review-cryo-artillery-warning');check('Actual glacial strike graphics activate',until('groundTargetingFx.some(q=>q.owner?._ll18&&q.impact)'));snap('review-cryo-artillery-impact')
  choose('ll18herald');check('Herald releases its actual native beams',until('LL18.beams.length>0'));snap('review-herald-live-beams')
  check('Herald also releases the safe-sector projectile ring',until('LL18.events.some(e=>e.event==="shot"&&e.type==="ll18herald")'));snap('review-herald-ring')
  choose('ll18brood',7);check('Stage7 carrier launches actual Crescent fighters',until('enemies.some(e=>e._ll18Escort&&e.type==="s8crescent"&&e._frRealmAI?.seq>0)'))
  check('Stage7 retains the authored sewer biome',w.evaluate('curStage.bg==="sewer"'));snap('review-stage7-brood-fighters')
  p.select_option('#bot','on');frames(40);check('Review bot control enables native primary fire',w.evaluate('legacyReviewBot&&Input.keys.j&&pBullets.length>0'))
  p.select_option('#bot','off');check('Turning the bot off releases its input',w.evaluate('!legacyReviewBot&&!Input.keys.j'))
  choose('waves',8);p.select_option('#bot','on');check('Wave review actually dispatches the restored Raptor beat',until('LL18.events.some(e=>e.event==="spawn"&&e.type==="ll18raptor")',2400));snap('review-stage8-mixed-waves')
  # Draw every reused hull-bank cell on the game's own canvas for inspection.
  bank=w.evaluate('''()=>{const keys=['nsb_cryo_spear','nsb_cryo_spear_damaged','nsb_cryo_spear_critical','nsb_rap_intact','nsb_rap_crit','nsb_spawncarrier_intact_v2','nsb_spawncarrier_damaged_v2','nsb_spawncarrier_critical_v2',...Array.from({length:6},(_,i)=>'nhd_idle_'+i)];return keys.map(key=>{const im=XART.get(key);return{key,w:im.width,h:im.height};});}''')
  check('All reused hull frames retain their even source resolutions',all(q['w']%2==0 and q['h']%2==0 for q in bank),bank)
  w.evaluate('''()=>{window.artBefore={w:cv.width,h:cv.height};cv.width=1400;cv.height=900;ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#07121e';ctx.fillRect(0,0,1400,900);ctx.imageSmoothingEnabled=false;ctx.font='12px monospace';ctx.textAlign='center';
   const keys=['nsb_cryo_spear','nsb_cryo_spear_damaged','nsb_cryo_spear_critical','nsb_rap_intact','nsb_rap_crit','nsb_spawncarrier_intact_v2','nsb_spawncarrier_damaged_v2','nsb_spawncarrier_critical_v2',...Array.from({length:6},(_,i)=>'nhd_idle_'+i)];
   keys.forEach((key,i)=>{const im=XART.get(key),x=(i%7)*200+100,y=Math.floor(i/7)*430+195,k=175/Math.max(im.width,im.height);ctx.drawImage(im,x-im.width*k/2,y-im.height*k/2,im.width*k,im.height*k);ctx.fillStyle='white';ctx.fillText(key.replace('nsb_',''),x,y+116);});}''')
  (O/'authored-hull-banks.png').write_bytes(base64.b64decode(w.evaluate("cv.toDataURL().split(',')[1]")))
  check('Review page, console and assets are clean',not errors,errors)
  result=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
  (O/'review-results.json').write_text(json.dumps(result,indent=2));print('SUMMARY '+json.dumps({k:result[k] for k in ['passed','failed']}),flush=True);br.close()
finally:stop()
sys.exit(1 if errors or any(not c['passed'] for c in checks) else 0)
