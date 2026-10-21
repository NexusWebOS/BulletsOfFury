from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import ast,base64,json,sys
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/ui_production_1020';O=R/'_shots/ui_production_1020';O.mkdir(exist_ok=True);checks=[];errors=[]
def ck(n,v,data=None):checks.append(dict(name=n,passed=bool(v),data=data));print(('PASS ' if v else 'FAIL ')+n,flush=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
def snap(p,name):p.screenshot(path=str(O/(name+'.png')))
import sys,atexit
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import shoot
port,stop=shoot.serve(str(R));atexit.register(stop)
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport=dict(width=1920,height=1080));p.set_default_timeout(120000);p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''));p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
 p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(SETUP,dict(stage=1,pilot='cole'));p.wait_for_function('()=>{SC12.refresh();return UI20.draws>0}');p.evaluate('()=>{window.requestAnimationFrame=()=>0;}');p.wait_for_timeout(100)
 for pilot in json.loads((W/'references/pilots.json').read_text()):
  pk=pilot['key'];p.evaluate('pk=>{run.pilot=pk;special=null;run.sonicT=run.dkT=0;lzMount=null;run.score=123456;run.lives=3;run.bombs=24;run.shield=5;run.speedLevel=3;player.dead=false;player._rollCool=player._somerCool=0;commPortrait(pk,"idle");XART.rdy("ship_"+pk);SC12.invalidate();}',pk)
  p.wait_for_function('()=>XART.rdy(commPortrait(run.pilot,"idle"))&&XART.rdy("ship_"+run.pilot)');p.evaluate('()=>{window.__bofFit();SC12.refresh();ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
  p.evaluate('()=>{dlgBox({who:run.pilot.toUpperCase(),full:"We got him! Dracodia is down. Tell everyone it is finally over!",shown:"We got him! Dracodia is down. Tell everyone it is finally over!",forceShown:true,pw:460,ph:130,x:10,y:360});}');snap(p,'pilot-'+pk)
  ck(pk+' HUD and dialogue use roster color, actual portrait and ship',p.evaluate('()=>UI20.last[0].color===UI20.color(run.pilot)&&UI20.last[0].portrait===commPortrait(run.pilot,"idle")&&UI20.last[0].ship==="ship_"+run.pilot&&UI20.dialogue.color===UI20.color(run.pilot)'))
  ck(pk+' colored name glyphs actually reach the canvas',p.evaluate('''()=>{const d=UI20.dialogue,bw=Math.min(d.h*1.13,d.w*.27),x=d.x+bw+Math.min(12,d.w*.025),rgb=[1,3,5].map(i=>parseInt(d.color.slice(i,i+2),16)),a=ctx.getImageData(Math.floor(x*SS),Math.floor((d.y+d.h*.1)*SS),Math.ceil(110*SS),Math.ceil(d.h*.2*SS)).data;let n=0;for(let i=0;i<a.length;i+=4)if(a[i+3]>220&&rgb.every((v,k)=>Math.abs(a[i+k]-v)<5))n++;return n>2;}'''))
 p.evaluate('()=>{run.pilot="cole";sonicGrant();startSpecial();special.strikes=7;run.bombs=7;SC12.invalidate();SC12.refresh();}')
 ck('Cole Sonic Boom and seven nuclear warheads are independently visible',p.evaluate('()=>UI20.last[0].primary==="SONIC BOOM"&&UI20.last[0].primaryFrac>0&&UI20.last[0].secondaryValue==="X 7"'))
 p.evaluate('()=>{run.pilot="decker";run.dkT=9;startSpecial();SC12.refresh();}')
 ck('Decker cloak and shotgun timers coexist',p.evaluate('()=>UI20.last[0].primary==="CLOAKING SYSTEM"&&UI20.last[0].secondaryValue==="9S"'))
 p.evaluate('()=>{run.pilot="lizzie";startSpecial();lzMount={docked:true,life:12};SC12.refresh();}')
 ck('Lizzie atom bombs and turret timer coexist',p.evaluate('()=>UI20.last[0].primary==="ATOM BOMB"&&UI20.last[0].secondaryValue==="12S"'))
 p.evaluate('()=>{lzMount=null;special=null;run.pilot="cole";run.sonicT=0;player._rollCool=BR_COOL/2;player._somerCool=SS_COOL/4;run.lives=0;run.bombs=0;run.shield=0;player.dead=true;SC12.invalidate();SC12.refresh();}')
 ck('Depleted cooldowns, lives, missiles and armor reflect actual state',p.evaluate('()=>{const v=UI20.last[0];return v.roll===.5&&v.somer===.75&&v.lives===0&&v.missiles===0&&v.shield===0&&v.primaryDetail==="SHIP LOST";}'))
 p.evaluate('()=>{player.dead=false;run.lives=3;run.bombs=24;run.shield=5;player._rollCool=player._somerCool=0;run.score=987654321;SC12.invalidate();SC12.refresh();}');snap(p,'large-score')
 p.evaluate('()=>{coopOn=true;run2.pilot="yuri";run2.score=654321;run2.lives=2;run2.bombs=8;player2.dead=false;window.__bofFit();SC12.invalidate();SC12.refresh();}')
 ck('Co-op retains two independent pilot readouts and colors',p.evaluate('()=>UI20.last.length===2&&UI20.last[0].pilot==="cole"&&UI20.last[1].pilot==="yuri"&&UI20.last[1].score===654321'));snap(p,'coop')
 for size in [(390,844),(1366,768),(2560,1440)]:
  p.set_viewport_size(dict(width=size[0],height=size[1]));p.evaluate('()=>{window.__bofFit();SC12.invalidate();SC12.refresh();}')
  ck(str(size)+' playfield and HUD remain inside viewport',p.evaluate('()=>[cv,...(SC12.mode==="sides"?SC12.panels:[SC12.compact])].every(c=>{const r=c.getBoundingClientRect();return r.left>=-1&&r.top>=-1&&r.right<=innerWidth+1&&r.bottom<=innerHeight+1;})'));snap(p,'layout-'+str(size[0]))
 p.set_viewport_size(dict(width=1280,height=720));p.evaluate('()=>{coopOn=false;run.pilot="cole";BOFCinematicDirector.cancel();run.mode="campaign";drawVictory._ready=true;drawVictory._trueEnding=true;drawVictory._t=29;drawVictory._sfx={};setState(GS.VICTORY);victoryEndingWarm();}')
 p.wait_for_function('()=>{victoryEndingWarm();return victoryEndingKeys().every(k=>XART.rdy(k));}')
 for time in [29,60,114]:
  p.evaluate('t=>{drawVictory._t=t;ctx.setTransform(SS,0,0,SS,0,0);drawVictory(0);}',time);snap(p,'ending-'+str(time))
 ck('Ending dialogue retains colored speaker and actual portrait',p.evaluate('()=>!!INV20.caption&&INV20.caption.x>=0&&INV20.caption.y+INV20.caption.h<=VH'))
 p.evaluate('()=>{for(const k of ["cole_body_0922","ui20_cole-neutral","inv20_cole","inv20_cole_horror","ui20_cole-talk"])XART.rdy(k);}')
 p.wait_for_function('()=>["cole_body_0922","ui20_cole-neutral","inv20_cole","inv20_cole_horror","ui20_cole-talk"].every(k=>XART.rdy(k))')
 ck('Cole body aliases resolve to corrected full-body master',p.evaluate('()=>XART.get("cole_body_0922")===XART.get("ui20_cole-neutral")&&XART.get("cole_body_0922").width===512'))
 ck('Cole ending report and horror retain fixed original runtime canvas',p.evaluate('()=>["inv20_cole","inv20_cole_horror"].every(k=>{const c=XART.get(k);return c.width===256&&c.height===384;})'))
 p.evaluate('()=>{BOFCinematicDirector.cancel();BOFCinematicDirector.start(4,()=>window.ui20Callback=true);BOFCinematicDirector.tick(.01);BOFCinematicDirector.draw();BOFCinematicDirector.finish();}');ck('Post-stage director still completes its original callback',p.evaluate('ui20Callback===true'))
 p.goto(f'http://127.0.0.1:{port}/docs/previews/ui_production_1020/index.html');p.wait_for_function('manifest&&dialogue.complete&&dialogue.naturalWidth>0')
 for s in 'abc':
  p.locator('[data-style="'+s+'"]').click()
  for pk in [q['key'] for q in json.loads((W/'references/pilots.json').read_text())]:
   p.select_option('#pilot',pk);p.wait_for_function('dialogue.complete&&dialogue.naturalWidth>0&&left.complete&&right.complete');ck('Template '+s+'/'+pk+' named dialogue and rails load',p.evaluate('dialogue.naturalWidth>0&&left.naturalWidth>0&&right.naturalWidth>0'))
 p.locator('[data-style="b"]').click();p.select_option('#pilot','falva');snap(p,'library-b-falva');p.set_viewport_size(dict(width=390,height=844));snap(p,'library-narrow');ck('Template library fits narrow window',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
 ck('No native browser or missing-asset errors',not errors,errors);b.close()
for f in [*(W/'templates').glob('*/*-*.webp'),*(R/'assets/game/pilots/cole/body_frames/front_identity_1020').glob('*.webp')]:
 im=Image.open(f);ck('Even frame '+f.name,im.width%2==0 and im.height%2==0)
for f in (R/'assets/game/pilots/cole/body_frames/front_identity_1020').glob('cole*.webp'):
 im=Image.open(f);r=im.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox();ck('Cole pose '+f.stem+' retains clear frame margins',r and r[0]>2 and r[1]>2 and r[2]<im.width-2 and r[3]<im.height-2,r)
result=dict(passed=sum(c['passed'] for c in checks),total=len(checks),errors=errors,checks=checks);(O/'report.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='checks'}));sys.exit(not all(c['passed'] for c in checks))
