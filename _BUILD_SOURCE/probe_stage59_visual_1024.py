from pathlib import Path
import json,base64
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage59_1024/visual';O.mkdir(exist_ok=True);checks=[];errors=[]
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS 'if ok else'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:300])if m.type=='error'else None);p.goto(f'http://127.0.0.1:{port}/index.html?debug=1');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{window.paint59=()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0)};window.setup59=(stage,kind)=>{diffKey='furious';debugStartFight({stage,role:'mini',kind,name:kind},{pilot:'maverick'});spawnSubBoss__inner(kind);window.B=subBoss;debugFight.spawned=true;B.enter=B._noHit=false;B.y=B._drawY=B.ty||150;BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=s6Opening=null;AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;stagePlan=[];waveIdx=999;warnT=0;player.dead=false;DBGT.god=true;player.x=worldWidth()/2;player.y=VH-55;enemies=[];pBullets=[];eBullets=[];l5Rocks=[];l5RockT=9999;setState(GS.PLAY);};}''')
  p.evaluate("setup59(5,'spacebomber')")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&s5924Keys().every(k=>XART.rdy(k))}')
  p.evaluate('''()=>{B=subBoss;debugFight.spawned=true;B.enter=B._noHit=false;B.y=B._drawY=138;B._bomber.mode='hc-recover';const R=B._bomber.parts.find(p=>p.id==='laserR');B._bomber.core=0;for(const p of B._bomber.parts)if(p!==R)p.hp=0;B.hp=R.hp;retinaScanClear();retinaScanAdd(retinaBossTargets(B)[0]);for(let i=0;i<32;i++)retinaScanTick(1/60);for(let i=0;i<4;i++){retinaTinted('retA',i,_pilotKey());retinaTinted('retB',i,_pilotKey());}XART.rdy('nbret_'+_pilotKey());paint59();}''')
  p.wait_for_timeout(200)
  row=p.evaluate('''()=>{const seen=[],ret=drawRetina,d=ctx.drawImage;let inRetina=false;drawRetina=function(){inRetina=true;try{return ret.apply(this,arguments)}finally{inRetina=false}};ctx.drawImage=function(im,...a){if(inRetina)seen.push({key:'native-retina-renderer',a});return d.call(this,im,...a)};try{paint59()}finally{ctx.drawImage=d;drawRetina=ret}return{marks:retinaScanState().marks.map(m=>({phase:m.phase,id:m.target._retinaId,x:m.x,y:m.y})),seen};}''')
  ck('Actual authored Retina pixels draw over the last live turret',len(row['marks'])==1 and row['marks'][0]['phase']=='locked' and len(row['seen'])>0,row);p.screenshot(path=str(O/'stage5-last-retina.png'))
  p.evaluate("setup59(9,'voidhorizon')")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(9)&&s5924Keys().every(k=>XART.rdy(k))}')
  p.evaluate('B=subBoss;B.enter=B._noHit=false;B._s9rift.core.x=B.x=worldWidth()/2;B._s9rift.core.y=B.y=160;')
  for mode in ['aimed','orbit','sweep','spin']:
   p.evaluate('''mode=>{const F=B._s9rift;B.enter=false;F.core.x=B.x=worldWidth()/2;F.core.y=B.y=160;F.s5924={mode:'entry',t:0,age:2,cycle:0};s5924Set(B,mode);F.s5924.t=mode==='spin'?F.s5924.warm+.55:F.s5924.warm*.7;paint59();}''',mode);p.screenshot(path=str(O/('horizon-'+mode+'.png')))
  row=p.evaluate('''()=>{const F=B._s9rift,Q=F.s5924;Q.mode='aimed';Q.t=Q.warm*.7;const get=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,cv.width,cv.height);ctx.restore();s9VoidHorizonDraw(B);const d=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<d.length;i+=4)if(d[i]>230&&d[i+1]>230&&d[i+2]>230)white++;return white};const before=get();s9VoidHorizonHit(B,1,B.x,B.y);const hit=get();for(let i=0;i<10;i++)s9VoidHorizonTick(B,1/60);const after=get();return{before,hit,after,timer:F.core.flash}}''')
  ck('Black hull shows actual white hit pixels and natural expiry',row['hit']>row['before']+500 and row['timer']==0 and row['after']<row['hit']*.6,row)
  # Use each real shield owner and capture its actual native draw dimensions.
  p.evaluate('''()=>{subBoss=null;subBossActive=false;enemies=[];for(const[i,type]of ['s9interceptor','s9ring','s9gunship','s9prism','s9beacon'].entries())spawnEnemy(type,camLeftX()+70+i*85,140+(i%2)*130,{});}''')
  p.wait_for_function('()=>Object.values(BF22_ART.sheets).filter(s=>/water/.test(s.key)).map(s=>XART.rdy(s.key)).every(Boolean)')
  row=p.evaluate('''()=>{const records=[],old=fv21Frame;fv21Frame=function(n,t,x,y,size,a,...r){if(n.startsWith('shield'))records.push({name:n,size,alpha:a});return old.apply(this,arguments)};try{for(const e of enemies){enemyShieldEquip(e,'bubble_void');e._esh.phase='active';e._esh.animT=1;drawEnemy(e);drawEnemyShieldLayer(e,true);}}finally{fv21Frame=old}return{records,units:enemies.map(e=>({type:e.type,span:e._bf22Rendered?.scale*bf22Model(e).M.span,w:e._drawW,h:e._drawH}))}}''')
  ck('Stage9 shields are bounded and hull metadata matches rendered fleet',len(row['records'])>0 and all(x['size']<=144 and x['alpha']<=.38 for x in row['records']) and all(abs(x['span']-x['w'])<.01 for x in row['units']),row)
  p.evaluate('paint59()');p.screenshot(path=str(O/'stage9-shields.png'))
  row=p.evaluate('''()=>{pBullets=[];for(let i=0;i<12;i++){const q={x:240+i%3*5,y:200,t:0};pBullets.push(q);spaceImpact(q,'laser',5,200);}return{visible:pBullets.filter(q=>!q._quietVisual).length,max:Math.max(...pBullets.map(q=>q.w)),lifetimes:pBullets.map(q=>q.life)}}''')
  ck('Repeated native space hits keep one compact spark per area',row['visible']==1 and row['max']<=20 and all(t<=.14 for t in row['lifetimes']),row)
  ck('No page/console errors',not errors,errors);br.close()
finally:stop()
out=dict(passed=sum(q['passed']for q in checks),failed=sum(not q['passed']for q in checks),checks=checks,errors=errors);(O/'report.json').write_text(json.dumps(out,indent=2)+'\n');print('SUMMARY',out['passed'],out['failed']);raise SystemExit(bool(out['failed']))
