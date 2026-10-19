"""Compare actual ally projectile pixels with the same player projectile art."""
from pathlib import Path
import ast,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/rebels';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];port,stop=shoot.serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=128
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate(SETUP,dict(stage=6,kind='rebelsquad',diff='normal',pilot='cole'))
  p.wait_for_function('()=>{stageLoadTick();rg4Warm();return stageLoadReady(6)&&bmfReady("game")}',polling=50)
  p.evaluate('''()=>{R=B._rebels;rf28Init(B,R);R.frIntro={done:true};B.enter=B._noHit=false;G=rg4Init(B);G.scene=null;G.gang=true;H3.release=false;H3.ending=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=fb2Talk=fb2Intro=thaw=s6Opening=null;P2M.active=null;window.RPIX19={cases:[],alphas:[]};const draw=ctx.drawImage;ctx.drawImage=function(){if(RPIX19.live)RPIX19.alphas.push(this.globalAlpha);return draw.apply(this,arguments);};
   const target=R.ships[0];eBullets=[];pBullets=[];for(const key of S6_PILOTS){const first=pBullets.length,q={key,x:player.x,y:player.y,slot:0,target,missileCd:0,specialCd:0};s6WingArsenal(q,0);for(const b of pBullets.slice(first))if(!RPIX19.cases.some(c=>c.kind===b.kind&&c._inf===b._inf))RPIX19.cases.push({...b});}
   // This is the native wing-gun payload, copied from an actual wingman's
   // update below rather than replacing its authored projectile renderer.
   s6WingInit();s6WingLaunch(4,true);s6Wing.all=true;s6Wing.beats=3;for(const q of s6Wing.ships){q.phase='fight';q.fcd=-1;q.missileCd=999;q.specialCd=999;q.x=target.x;q.y=target.y+200;q.target=target;}
   s6WingTick(1/60);let mg=pBullets.find(b=>b.ally&&b.kind==='mg'&&!b._inf);
   if(!mg){const old=pBullets;pBullets=[];run.spaceMode=false;run.wlevels||=Array(8).fill(0);run.wvars||=Array(8).fill(null);weaponFormSelect(7,{kind:'primary1003b',id:'mg'});run.weapon=0;run.wlevel=run.wlevels[0]=1;run.wvars[0]=null;run.forge={};run.forgeForms={};run.infusion=null;player.fireCd=0;pShoot();mg=pBullets.find(b=>b.kind==='mg');pBullets=old;}
   if(mg&&!RPIX19.cases.some(c=>c.kind==='mg'&&!c._inf))RPIX19.cases.push({...mg,ally:true});
   window.rpix19Draw=(i,off,ally=true)=>{const b={...RPIX19.cases[i],x:camLeftX()+viewW()/2,y:VH-150,t:.3,ally,_hit:[]};pBullets=[b];eBullets=[];window.RBAL19_OFF=off?1:0;RPIX19.alphas=[];ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,ctx.canvas.width/SS,ctx.canvas.height/SS);RPIX19.live=true;drawBullets();RPIX19.live=false;ctx.restore();const d=ctx.getImageData(0,0,ctx.canvas.width,ctx.canvas.height).data;let energy=0,ink=0;for(let k=0;k<d.length;k+=4){energy+=(d[k]+d[k+1]+d[k+2])*d[k+3]/255;if(d[k+3]>0)ink++;}return{kind:b.kind,inf:b._inf,energy,ink,alphas:RPIX19.alphas};};}''')
  n=p.evaluate('RPIX19.cases.length')
  # Request all real source keys by drawing, then yield for lazy downloads.
  for i in range(n):p.evaluate('i=>rpix19Draw(i,true)',i)
  p.wait_for_function('()=>Object.values(XART.img).every(im=>!im||im.complete!==false)',polling=50)
  for i in range(n):
   p.evaluate('i=>rpix19Draw(i,true)',i);p.wait_for_timeout(20)
   off=p.evaluate('i=>rpix19Draw(i,true)',i);on=p.evaluate('i=>rpix19Draw(i,false)',i);own=p.evaluate('i=>rpix19Draw(i,false,false)',i)
   ratio=on['energy']/max(1,off['energy']);ownRatio=own['energy']/max(1,off['energy']);name=off['kind']+' '+str(off.get('inf'))
   ck(name+' friendly art is dimmer while the player art remains full',off['ink']>0 and .25<ratio<.85 and .90<ownRatio<1.1,dict(ratio=ratio,ownRatio=ownRatio,off=off,on=on))
  br.close()
finally:stop()
ck('No page, console, draw or asset errors',not errors,errors)
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors);(O/'bullet-pixels-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');sys.exit(report['failed']>0)
