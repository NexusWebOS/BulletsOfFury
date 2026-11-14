from pathlib import Path
import sys,json,base64,io,argparse
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;O=W.parents[1]/'outputs/stage67-repair';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
ap=argparse.ArgumentParser();ap.add_argument('--after',action='store_true');args=ap.parse_args();name='after' if args.after else 'before';port,stop=serve(str(R));errors=[];report={}
def snap(p,n):
 s=p.evaluate("document.querySelector('#screen').toDataURL('image/png').split(',')[1]");im=Image.open(io.BytesIO(base64.b64decode(s))).convert('RGB').resize((480,512),Image.Resampling.NEAREST);im.save(W/(name+'-'+n+'.png'));return im
def boot(br,n,kind):
 p=br.new_page(viewport={'width':1100,'height':1000});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:300]) if m.type=='error' or 'draw error' in m.text else None);p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate("([n,k])=>{EA11.setup(n,'furious');stagePlan=[];waveIdx=0;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;debugUnlocked=true;DBGT.god=true;player.invuln=9999;if(n===6)spawnBoss(k);else spawnSubBoss(k);window.B=n===6?boss:subBoss;}",[n,kind]);p.wait_for_function('(n)=>{stageLoadTick();return stageLoadReady(n)&&(n===6?fb112Ready():sj98Ready())}',arg=n);return p
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--mute-audio']);p=boot(br,6,'thunderhead');p.evaluate(STEP,190)
  p.evaluate("()=>{B._fb112.phase='warn';B._fb112.attack='storm-cyclone';B._fb112.dur=99;B._fb112.t=2;B._tc119.flow=null;B._tc119.di=0;}");p.evaluate(STEP,30);snap(p,'thunderhead')
  report['thunder']=p.evaluate('({hp:B.hp,maxhp:B.maxhp,parts:B._fb112.parts.map(q=>({id:q.id,hp:q.hp,mount:fb112PartPoint(B,q),bore:fb112Bore(B,q)})),beams:tm115State(B).beams.map(q=>({x:q.x,y:q.y,part:q.part.id})),hud:typeof SR110!=="undefined"?SR110.hud:null})')
  p.close();p=boot(br,7,'dualscoopdredger');p.evaluate(STEP,100);frames=[];rows=[]
  for i in range(150):
   p.evaluate(STEP,4);frames.append(snap(p,'sumpjaw-current'))
   rows.append(p.evaluate('({mode:B._sj120.mode,t:B._sj120.t,hp:B.hp,actors:B._sj98.actors.map(a=>({x:a.x,y:a.y,heading:a.heading,trail:a.trail.length,height:a.height})),hud:typeof SR110!=="undefined"?SR110.hud:null})'))
   if i in [20,70,130]:frames[-1].save(W/(name+'-sumpjaw-'+str(i)+'.png'))
  report['sumpjaw']=rows;p.close();br.close()
  pal=frames[60].quantize(colors=192);gif=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in frames];gif[0].save(O/(name+'-sumpjaw.gif'),save_all=True,append_images=gif[1:],duration=70,loop=0,optimize=True)
finally:stop()
report['errors']=errors;(O/(name+'-capture.json')).write_text(json.dumps(report,indent=2));print(json.dumps({'name':name,'errors':errors,'thunder':report['thunder']}))
