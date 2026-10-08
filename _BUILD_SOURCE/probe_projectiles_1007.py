"""Real Chromium render/animation pass. Protected observations, not balance clears."""
from pathlib import Path
import json,sys,base64,time,http.server,argparse
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
P=argparse.ArgumentParser();P.add_argument('--catalog-only',action='store_true');args=P.parse_args()
O=R/'_shots/projectiles_1007/after';O.mkdir(parents=True,exist_ok=True)
report={'errors':[],'encounters':[],'catalog':{},'checks':{}}
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=shoot.serve(str(R))
def screenshot(p,name):
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);c=br.new_context(viewport={'width':1100,'height':950})
  c.route('**/*',lambda r:r.continue_() if r.request.url.startswith(('http://127.0.0.1:','data:','blob:')) else r.abort())
  p=c.new_page();p.set_default_timeout(120000);p.on('pageerror',lambda e:report['errors'].append(str(e)))
  p.on('console',lambda m:report['errors'].append(m.text[:400]) if m.type=='error' and ('127.0.0.1' in m.text or 'ERR_' not in m.text) else None)
  def boot():
   p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
   p.add_script_tag(path=str(R/'_BUILD_SOURCE/balance_lab_1007.js'));p.add_script_tag(path=str(R/'_BUILD_SOURCE/projectile_lab_1007.js'))
  boot()
  p.evaluate("()=>AP7.begin({id:'catalog',stage:8,kind:'heralddeath',mini:true,diff:'normal',pilot:'yuri',level:3})")
  # Prime actual draw routes, yield to decoding, then sample loaded frames.
  p.evaluate('()=>AP7.catalog()');p.wait_for_timeout(1500);p.evaluate('()=>AP7.catalog()');p.wait_for_timeout(1000)
  for diff in ['easy','normal','hard','furious']:
   p.evaluate("d=>{diffKey=d;DIFF=difficultyForRun('arcade',d);AP7.geometry=[];}",diff)
   report['catalog'][diff]={'rows':p.evaluate('()=>AP7.catalog()'),'geometry':p.evaluate('()=>AP7.geometry')}
   print('CATALOG',diff,len(report['catalog'][diff]['rows']),flush=True)
  # Stable-pose sheets get moving light, without growth-column jumps. Render
  # unrotated to distinguish source alignment from intended physical rotation.
  report['stableSheets']=p.evaluate("""()=>{
   const rows=[];for(const kind of Object.keys(CFX_STAGE_PROJECTILE)){
    const b={kind,x:VW/2,y:VH/2,vx:0,vy:-3,t:0,_visualAge:0,szMul:1,_noArsenal:true};
    const saved=CFX_STAGE_PROJECTILE[kind][3];CFX_STAGE_PROJECTILE[kind][3]='up';
    const frames=[];for(let f=0;f<24;f++){b._visualAge=b.t=f/24;frames.push(AP7.frame(b));}
    CFX_STAGE_PROJECTILE[kind][3]=saved;rows.push({kind,frames});
   }return rows;
  }""")
  # Slow wall time cannot advance a projectile's flame/shard/energy animation.
  p.evaluate("()=>{window.pauseB={kind:'shard',_fire:true,lv:3,x:240,y:260,w:8,h:14,ang:-2.4,t:0,_visualAge:.23};AP7.frame(pauseB,false);}")
  p.wait_for_timeout(300)
  first=p.evaluate('()=>AP7.frame(pauseB,false)');p.wait_for_timeout(230);second=p.evaluate('()=>AP7.frame(pauseB,false)')
  report['checks']['fireShardFrozenAcrossWallTime']=first==second and first['n']>0
  report['checks']['negativePhasesValid']=p.evaluate("()=>[-100,-13,-1,0,1,13].every(phase=>{const f=projectileVisualFrame({t:0},1000/70,8,phase);return f>=0&&f<8;})")
  # A comparison contact sheet from the active CFX draw, no replacement artwork.
  data=p.evaluate("""()=>{
   const c=document.createElement('canvas');c.width=1200;c.height=700;const g=c.getContext('2d');g.fillStyle='#101b29';g.fillRect(0,0,c.width,c.height);g.font='17px monospace';g.imageSmoothingEnabled=false;
   const kinds=['s8pair','s8blade','s8rift','s8missile','s7sludge','s7bio'];
   for(let row=0;row<kinds.length;row++){for(let f=0;f<8;f++){
    const b={kind:kinds[row],x:240,y:256,vx:0,vy:-3,t:f/8,_visualAge:f/8,w:16,h:16,_noArsenal:true};AP7.frame(b);
    g.drawImage(cv,(240-50)*SS,(256-50)*SS,100*SS,100*SS,200+f*123,row*115,100,100);
   }g.fillStyle='#c2d9ed';g.fillText(kinds[row],12,row*115+47);}return c.toDataURL().split(',')[1];
  }""");(O/'projectile-motion.png').write_bytes(base64.b64decode(data))
  if not args.catalog_only:
   bosses=['damkeeper','infernoreaver','cryospear','stormsovereign','xenoregent','warhive','sludgeemperor','vileexistence','tidalfusion']
   minis=['razorback','magmaward','frostcruiser','olivewarden','spacebomber','siegebomber','dualscoopdredger','heralddeath','voidhorizon']
   cases=[]
   for diff in ['easy','normal','hard','furious']:
    for st in range(1,10):
     cases.extend([dict(stage=st,kind=bosses[st-1],diff=diff),dict(stage=st,kind=minis[st-1],diff=diff,mini=True)])
    cases.extend([dict(stage=6,kind='rebelsquad',diff=diff),dict(stage=6,kind='warhive',diff=diff,ace=True)])
    for form in ['host','ghost','home']+list(range(9)):
     cases.append(dict(stage=8,kind='vileexistence',diff=diff,form=form))
    for st in range(1,10):cases.append(dict(stage=st,kind=bosses[st-1],diff=diff,slice=True))
   for i,case in enumerate(cases):
    # Fresh page per case avoids asset/state pollution between encounters.
    boot();case.update(id=f"{i:03}-{case['diff']}-s{case['stage']}-{case['kind']}"+('-mini' if case.get('mini') else '')+('-ace' if case.get('ace') else '')+(f"-form{case['form']}" if 'form' in case else '')+('-stage' if case.get('slice') else ''),pilot='yuri',level=3)
    try:
     p.evaluate('(c)=>AP7.begin(c)',case);p.wait_for_timeout(130)
     seconds=36 if case.get('slice') else 24
     for j in range(seconds*2):
      result=p.evaluate('()=>AP7.step(30)')
      if j%12==0:p.wait_for_timeout(25)
     result['case']=case;report['encounters'].append(result)
     if case['diff']=='normal' and not case.get('slice'):
      screenshot(p,case['id']);result['screenshot']=case['id']+'.png'
     print('CASE',i+1,len(cases),case['id'],result['frames'],sum(result['shots'].values()),len(result['geometry']),flush=True)
    except Exception as e:report['errors'].append(case['id']+': '+str(e));print('ERROR',report['errors'][-1],flush=True)
    (O/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
  br.close()
finally:stop()
(O/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('DONE',json.dumps({'encounters':len(report['encounters']),'errors':report['errors'],'checks':report['checks']}),flush=True)
