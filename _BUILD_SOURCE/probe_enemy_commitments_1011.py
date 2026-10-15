"""Native collision, camera, co-op and late-fleet checks for the enemy pass."""
from pathlib import Path
import json, base64, subprocess
from playwright.sync_api import sync_playwright
import imageio_ffmpeg, shoot

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/enemy_behaviour_1011'
checks=[];errors=[]
def check(name,ok,data=None):
 checks.append({'name':name,'pass':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--mute-audio']);p=br.new_page(viewport={'width':1280,'height':1000})
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.add_script_tag(path=str(ROOT/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  def setup(stage=6,diff='normal'):
   p.evaluate('([s,d])=>EA11.setup(s,d)',[stage,diff])
   p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(run.stage).ready;}',polling=50)
   p.evaluate('()=>{stagePlan=[];aiQueue=[];s6Wing=null;FS11.pending=null;FS11.boxes=[];run._fs11StartDelivered=true;enemies=[];powerups=[];}')
  for dodge in [False,True]:
   setup()
   q=p.evaluate('''(dodge)=>{
    spawnEnemy('s6lancer',worldWidth()/2,100,{inPlace:true});window.E=enemies.at(-1);
    let warning=null;for(let i=0;i<300;i++){updatePlay(1/60);const q=E._s6Act;if(q?._eb11?.started&&q.t>.15&&!q.fired){warning={...q._eb11.target};break;}}
    const safe=!player.dead&&eBullets.length===0;player.invuln=0;run.shield=0;
    if(dodge)player.x+=115;
    let hit=false,shots=0;for(let i=0;i<180;i++){updatePlay(1/60);shots=Math.max(shots,eBullets.length);if(player.dead){hit=true;break;}}
    return {safe,hit,shots,warning,player:{x:player.x,y:player.y}};
   }''',dodge)
   check('Dodging the committed lane avoids the native volley' if dodge else 'Remaining in the warned lane is hit by actual enemy projectiles',q['safe'] and q['shots']>0 and q['hit']!=dodge,q)
  setup()
  q=p.evaluate('''()=>{coopOn=true;withSeat(2,()=>{player.reset();player.dead=player.out=false;player.x=worldWidth()/2+55;player.y=230;});
   spawnEnemy('s6lancer',worldWidth()/2,100,{inPlace:true});const e=enemies.at(-1);let lock=null;
   for(let i=0;i<250;i++){updatePlay(1/60);if(e._s6Act?._eb11?.target){lock={...e._s6Act._eb11.target};break;}}
   const p2=seatShip(2);return {lock,p2:{x:p2.x,y:p2.y},p1:{x:player.x,y:player.y}};}''')
  check('A committed volley targets the nearer live co-op pilot',q['lock'] and abs(q['lock']['x']-q['p2']['x'])<1 and abs(q['lock']['y']-q['p2']['y'])<1,q)
  for edge in ['left','right']:
   setup()
   q=p.evaluate('''edge=>{camX=edge==='left'?0:worldWidth()-viewW();player.x=camX+viewW()/2;
    spawnEnemy('s6lancer',edge==='left'?camLeftX()-70:camRightX()+70,100,{inPlace:true});const e=enemies.at(-1);
    for(let i=0;i<240;i++)updatePlay(1/60);const hidden=eBullets.length===0;
    e.x=player.x;e.y=100;for(let i=0;i<240;i++)updatePlay(1/60);
    return {hidden,shots:e._eb11.attacks,finite:Number.isFinite(e.x+e.y)};}''',edge)
   check(edge+' camera departure queues safely and visible re-entry attacks',q['hidden'] and q['shots']>0 and q['finite'],q)
  metrics=[]
  for diff in ['normal','hard','furious']:
   setup(8,diff)
   q=p.evaluate('''()=>{spawnEnemy('s8interceptor',worldWidth()/2,-90);const e=enemies.at(-1);let maxPocket=0;
    for(let i=0;i<1500;i++){player.invuln=40002;updatePlay(1/60);if(e._frRealmAI&&e._frRealmAI.seq<eb11Profile().cycles)maxPocket=Math.max(maxPocket,e.y);if(e.dead)break;}
    return {seq:e._frRealmAI?.seq,dead:e.dead,maxPocket,limit:viewTopY()+viewH()*.39,attacks:e._ea11?.shots||0};}''')
   metrics.append(q)
   check(diff+': late alien holds its pocket, completes its engagement and leaves',q['maxPocket']<=q['limit']+2 and q['dead'] and q['attacks']>0,q)
  check('Realm attack cycles increase Normal to Hard with a larger Furious step',metrics[1]['seq']-metrics[0]['seq']>0 and metrics[2]['seq']-metrics[1]['seq']>metrics[1]['seq']-metrics[0]['seq'],metrics)
  setup(8,'furious')
  p.evaluate('''()=>{spawnEnemy('s8interceptor',worldWidth()/2-65,-90);spawnEnemy('s8spread',camLeftX()-80,105,{_side:1});window.E=enemies[0];}''')
  proc=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-f','image2pipe','-vcodec','mjpeg','-r','20','-i','pipe:0','-an','-c:v','libx264','-crf','20','-pix_fmt','yuv420p',str(OUT/'late-alien-commitments.mp4')],stdin=subprocess.PIPE)
  for frame in range(240):
   p.evaluate('''()=>{for(let i=0;i<3;i++){player.invuln=40002;updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}drawHUD();}''')
   proc.stdin.write(base64.b64decode(p.evaluate('cv.toDataURL("image/jpeg",.88).split(",")[1]')))
   if frame in [40,90,140,210]:(OUT/f'late-alien-{frame}.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
   if frame%10==0:p.wait_for_timeout(2)
  proc.stdin.close();check('Late alien attack recording encodes',proc.wait()==0)
  check('No page or console errors',not errors,errors);br.close()
finally:stop()
(OUT/'commitments.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2))
if errors or any(not q['pass'] for q in checks):raise SystemExit(1)
