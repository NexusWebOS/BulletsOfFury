from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,ast,json,base64,math
R=Path(__file__).resolve().parents[1];S=Path(__file__).parent;O=R/'_shots/retina_colors_1020';O.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
EXPECTED=dict(yuri='#e02020',axel='#2f6fff',cole='#39ff5a',decker='#ffe11a',juggernaut='#ff8a1a',lizzie='#ffc21a',falva='#ff4fa3',freezer='#9a4fe0',maverick='#1f7a3a')
checks=[];errors=[];cases=[]
def ck(n,v,data=None):checks.append(dict(name=n,passed=bool(v),data=data));print(('PASS ' if v else 'FAIL ')+n,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport=dict(width=1366,height=768));p.set_default_timeout(120000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof ht27Stop==="function"');p.evaluate(shoot.TRAP_RAF);p.evaluate(SETUP,dict(stage=1,pilot='cole'))
  p.wait_for_function('()=>[...Array.from({length:4},(_,i)=>["retm_"+i,"retmb_"+i]).flat(),...PILOTS.map(p=>"nbret_"+p.key)].map(k=>XART.rdy(k)).every(Boolean)')
  p.evaluate('''()=>{window.rc20Stats=(x,y)=>{const D=ctx.getImageData(Math.round((x-45)*SS),Math.round((y-45)*SS),Math.round(90*SS),Math.round(90*SS)).data;let hx=0,hy=0,n=0;for(let i=0;i<D.length;i+=4){const r=D[i]/255,g=D[i+1]/255,b=D[i+2]/255,mx=Math.max(r,g,b),mn=Math.min(r,g,b),d=mx-mn;if(mx<.12||d/Math.max(mx,.001)<.25)continue;let h=mx===r?60*((g-b)/d%6):mx===g?60*((b-r)/d+2):60*((r-g)/d+4),weight=d;hx+=Math.cos(h*Math.PI/180)*weight;hy+=Math.sin(h*Math.PI/180)*weight;n++;}return {hue:(Math.atan2(hy,hx)*180/Math.PI+360)%360,n};};window.rc20Mark=(x,y,big,phase,frame)=>{const target={x,y,w:big?96:38,h:big?96:38,dead:false,hp:200};return {target,x,y,phase,lockT:5,scale:1,spin:0,animT:frame*(phase==='seek'?.09:.13)+.001,seekT:.2};};window.rc20Paint=c=>{coopOn=false;run.pilot=c.pilot;diffKey=c.diff;DIFF=DIFFS[diffKey];ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#000000';ctx.fillRect(0,0,VW,VH);if(c.mode==='regular'){retina=rc20Mark(240,256,c.big,c.phase,c.frame);drawRetina();return [rc20Stats(240,256)];}player._retinaScan={marks:[rc20Mark(150,256,c.big,c.phase,c.frame),rc20Mark(330,256,c.big,c.phase,c.frame)]};drawRetinaScans();return [rc20Stats(150,256),rc20Stats(330,256)];};}''')
  def hue(hex):
   import colorsys
   return colorsys.rgb_to_hsv(*[int(hex[i:i+2],16)/255 for i in [1,3,5]])[0]*360
  for pk,color in EXPECTED.items():
   ck(pk+' uses its approved Retina color, independently of dialogue',p.evaluate('pk=>retinaColor(pk)===RETINA_TINTS[pk]',pk) and p.evaluate('pk=>retinaColor(pk)',pk)==color)
   for diff in ['easy','normal','hard','furious']:
    batch=[]
    for mode in ['regular','multi']:
     for big in [False,True]:
      for phase in ['seek','locked']:
       for frame in range(4):
        c=dict(pilot=pk,diff=diff,mode=mode,big=big,phase=phase,frame=frame);pixels=p.evaluate('c=>rc20Paint(c)',c);ok=all(q['n']>80 and abs((q['hue']-hue(color)+180)%360-180)<10 for q in pixels);row=dict(**c,pixels=pixels,passed=ok);cases.append(row);batch.append(row)
    ck(pk+' '+diff+' native regular/multi, ordinary/boss, seek/lock, all frames have correct pixels',all(q['passed'] for q in batch),[q for q in batch if not q['passed']])
   p.evaluate('''pk=>{run.pilot=pk;coopOn=false;ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#000000';ctx.fillRect(0,0,VW,VH);ui20Text(ctx,pk+' RETINA',240,30,20,430,'center',retinaColor(pk));for(const [row,big]of [[0,false],[1,true]]){ui20Text(ctx,big?'BOSS / MINI':'ORDINARY TARGET',240,85+row*180,13,430);for(const [col,phase]of [[0,'seek'],[1,'locked']]){const x=150+col*180,y=150+row*180;retina=rc20Mark(x,y,big,phase,1);drawRetina();ui20Text(ctx,phase,x,y+58,12,150);}}ui20Text(ctx,'REGULAR AND MULTI USE THE SAME PALETTE',240,470,11,450);}''',pk)
   (O/(pk+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
  ck('Decker orange dialogue remains separate from yellow targeting',p.evaluate('dialogueNameColor("DECKER")==="#ff9b30"&&retinaColor("decker")==="#ffe11a"'))
  ck('Rebel scanners retain their own approved colors',p.evaluate('()=>["nyx","kaia","jace","rook","voss"].every(k=>retinaColor(k)===P2_COLORS[k])'))
  p.evaluate('''()=>{coopOn=true;run.pilot='axel';run2.pilot='decker';player2.dead=false;player._retinaScan={marks:[rc20Mark(150,256,true,'locked',1)]};player2._retinaScan={marks:[rc20Mark(330,256,true,'locked',1)]};ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#000000';ctx.fillRect(0,0,VW,VH);const old=retina;drawRetinaScans();window.rc20Coop={left:rc20Stats(150,256),right:rc20Stats(330,256),restored:retina===old&&_seat===1&&run.pilot==='axel'};}''')
  row=p.evaluate('rc20Coop');ck('Co-op Multi-Retina keeps Axel blue and Decker yellow without leaking seat state',row['restored'] and abs(row['left']['hue']-hue(EXPECTED['axel']))<10 and abs(row['right']['hue']-hue(EXPECTED['decker']))<10,row)
  (O/'coop.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
  for diff in ['easy','normal','hard','furious']:
   p.evaluate('''diff=>{coopOn=false;run.pilot='decker';diffKey=diff;DIFF=DIFFS[diff];bossActive=subBossActive=false;boss=subBoss=null;special=null;pBullets=[];player.dead=false;run.bombs=4;retina={target:null};enemies=[{x:170,y:180,w:38,h:38,dead:false,hp:500},{x:310,y:180,w:96,h:96,dead:false,hp:500}];player._retinaScan=null;retinaScanAdd(enemies[0]);retinaScanAdd(enemies[1]);retinaScanTick(.46);window.rc20Locked=player._retinaScan.marks.every(m=>m.phase==='locked');retinaScanFire();retinaScanTick(.001);retinaScanTick(.051);window.rc20Mechanics={locked:rc20Locked,missiles:pBullets.filter(q=>q.kind==='gmiss').length,ammo:run.bombs,targets:pBullets.map(q=>enemies.indexOf(q.tgt)),hp:enemies.map(q=>q.hp)};}''',diff)
   row=p.evaluate('rc20Mechanics');ck(diff+' real Multi-Retina still acquires two targets and spends one missile each',row['locked'] and row['missiles']==2 and row['ammo']==2 and row['targets']==[0,1] and row['hp']==[500,500],row)
  ck('No native page, console, draw or missing-asset errors',not errors,errors);b.close()
finally:stop()
result=dict(passed=sum(c['passed'] for c in checks),total=len(checks),errors=errors,checks=checks,cases=cases);(O/'report.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ['checks','cases']}));raise SystemExit(not all(c['passed'] for c in checks))
