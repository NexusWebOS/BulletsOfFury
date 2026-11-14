from pathlib import Path
import sys,json,base64,io,http.server
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;O=W.parents[1]/'outputs/dracodia-overload';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=serve(str(R));errors=[];checks={}
SETUP="""()=>{run.stage=8;curStage=STAGES[7];setState(GS.PLAY);diffKey='furious';spawnBoss('vileexistence');bossActive=true;window.B=boss;v18Enter(B,2,0);B._r30.mode='fight';B.enter=B._noHit=false;B.x=340;B.y=190;for(const i of V18.forms)if(i!==0)j3State(B).hp[i]=0;player.dead=player.out=false;player.invuln=0;player.roll=player.somer=null;player.x=340;player.y=440;DBGT.god=true;for(const k of Object.keys(Input.keys))Input.keys[k]=false;pBullets=[];eBullets=[];RD84.events=[];B._lastPart=B.parts[0];modularHit(B.hp);window.D=dr5State(B);window.Q=D.rd84;}"""
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--mute-audio']);p=boot(br.new_context(viewport={'width':1100,'height':1000}),port,8,errors,'boss');p.evaluate(SETUP)
  checks['native_final_hit']=p.evaluate('B.hp===0&&V18.forms.every(i=>j3State(B).hp[i]===0)&&B._r30.mode==="dr5Death"&&!!Q')
  p.evaluate(STEP,540);print('Recording montage and post-teleport overload',flush=True)
  frames=[];timeline=[];paused=False
  for i in range(350):
   err=p.evaluate(STEP,4)
   if err:raise RuntimeError(err)
   q=p.evaluate('({t:B._r30.t,mode:B._r30.mode,phase:Q.phase,stats:DF110.stats,events:RD84.events,hp:B.hp,state,fx:Q.df110?.blasts?.length||0})');timeline.append(q)
   encoded=p.evaluate("document.querySelector('#screen').toDataURL('image/png').split(',')[1]");im=Image.open(io.BytesIO(base64.b64decode(encoded))).convert('RGB').resize((480,512),Image.Resampling.NEAREST);frames.append(im)
   if q['phase']=='post-teleport-overload':
    age=q['t']-13.2
    for t in [.3,1.1,2.1,3.5,4.8]:
     if abs(age-t)<.035:im.save(W/f'overload-{t}.png')
    if not paused and age>2:
     expr='({t:B._r30.t,age:Q.age,blasts:Q.df110.blasts.map(f=>f.t)})';before=p.evaluate(expr);p.evaluate("setState('paused')");p.evaluate(STEP,90);checks['pause_freezes_overload']=before==p.evaluate(expr);p.evaluate('setState(GS.PLAY)');paused=True
   if q['phase']=='shatter':
    for t in [.3,.6,1.2,2.2]:
     if abs(q['t']-18.4-t)<.035:im.save(W/f'shatter-{t}.png')
   if q['mode']=='dr5Portal' and q['t']>.2:break
  # Continue through the unchanged gate, squad reunion and native reward owner.
  p.evaluate(STEP,1000)
  checks['single_native_victory_reward']=p.evaluate('B._r30.rewarded===true&&run._trueFinaleCleared&&state==="debugmenu"')
  checks['all_pools_remain_exhausted']=p.evaluate('V18.forms.every(i=>j3State(B).hp[i]===0)')
  old=p.evaluate('Q.age');p.evaluate('j3FinalDeath(B)');checks['repeated_final_notification_does_not_restart']=p.evaluate('Q.age')==old
  events=p.evaluate('RD84.events');stats=p.evaluate('DF110.stats');p.evaluate('beginStage(1)');checks['stage_reset_retires_owner']=p.evaluate('!rd84Own(boss)');br.close()
 # Use one palette for the entire preview; production frames stay lossless.
 contact=Image.new('RGB',(480*4,512*4))
 for i in range(16):contact.paste(frames[round(i*(len(frames)-1)/15)],(i%4*480,i//4*512))
 pal=contact.quantize(colors=192,method=Image.Quantize.MEDIANCUT);gif=[im.quantize(palette=pal,dither=Image.Dither.NONE) for im in frames]
 gif[0].save(O/'dracodia-overload.gif',save_all=True,append_images=gif[1:],duration=[70 if i%3 else 60 for i in range(len(gif))],loop=0,optimize=True)
 report={'source':'actual installed native final-hit checkpoint rendered in Edge','errors':errors,'checks':checks,'timeline':timeline,'events':events,'stats':stats,'frames':len(frames)}
 (O/'capture.json').write_text(json.dumps(report,indent=2));print(json.dumps({'frames':len(frames),'errors':errors,'checks':checks,'stats':stats}),flush=True)
finally:stop()
