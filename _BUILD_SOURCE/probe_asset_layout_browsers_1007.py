"""Production menus, portraits, all current password fights; no archived art fetches."""
import sys,json,ast,base64,argparse
from pathlib import Path
from playwright.sync_api import sync_playwright
args=argparse.ArgumentParser();args.add_argument('--engine',default='chromium');args=args.parse_args()
R=Path(__file__).resolve().parents[1];O=R/'_shots/asset_layout_1007'/args.engine;O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];archive_requests=[];captures=[]
def ck(ok,name):checks.append({'ok':bool(ok),'name':name});print(('OK ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=getattr(pw,args.engine).launch(**({'args':['--no-sandbox','--mute-audio']} if args.engine=='chromium' else {}));p=br.new_page(viewport={'width':1100,'height':1000})
  p.add_init_script('navigator.getGamepads=()=>[]')
  p.route('**/*',lambda route:route.continue_() if route.request.url.startswith(('http://127.0.0.1:','data:','blob:')) else route.abort())
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:500]) if (m.type=='error' and 'ERR_FAILED' not in m.text and 'Failed to load resource: net::' not in m.text) or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.on('request',lambda r:archive_requests.append(r.url) if '/UNUSED_ASSETS/' in r.url else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(shoot.TRAP_RAF)
  p.evaluate('()=>{for(const P of PILOTS)for(const em of PP5.poses){XART.rdy("pp5_raw_"+P.key+"_"+em);XART.rdy("port_"+P.key+"_"+em);XART.rdy("comm_"+P.key+"_"+em);}for(const em of CP5.poses){XART.rdy("cp5_raw_"+em);XART.rdy("comm_cole_"+em);}}')
  p.wait_for_function('()=>PILOTS.every(P=>PP5.poses.every(em=>XART.rdy("port_"+P.key+"_"+em)&&XART.rdy("comm_"+P.key+"_"+em)))',timeout=120000)
  q=p.evaluate('()=>PILOTS.map(P=>({pilot:P.key,count:PP5.poses.filter(em=>{const a=XART.get("port_"+P.key+"_"+em),b=XART.get("comm_"+P.key+"_"+em);return (a.width||a.naturalWidth)>1&&(b.width||b.naturalWidth)>1}).length}))')
  for row in q:ck(row['count']==12,row['pilot']+' all 12 portrait and comm poses draw through current renderer')
  ck(p.evaluate('()=>!Object.entries(BOFX.cells).some(([k,c])=>c[0]==="ui_dialogue"&&/^(port_|face_)/.test(k))'),'72 obsolete portrait cells absent from production atlas')
  ck(p.evaluate('()=>!Object.keys(BOFA.music).some(k=>k.startsWith("unused"))'),'unused music aliases removed from playable registry')
  def cap(name):
   (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));captures.append(name)
  for state_name in ['TITLE','DIFF','PILOT','HELP','PASSWORD','OPTIONS','CAMPAIGN']:
   exists=p.evaluate('n=>GS[n]!=null',state_name)
   if not exists:continue
   p.evaluate('n=>setState(GS[n])',state_name);p.wait_for_timeout(180);p.evaluate(shoot.STEP,3);cap('menu-'+state_name.lower());ck(True,state_name+' renders')
  # Drive the actual loading loop to completion for every mission. Short encounter draws
  # alone cannot catch obsolete texture roots left in a broad stage preload prefix.
  for stage in (range(1,10) if args.engine=='chromium' else [1,4,8,1]):
   q=p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True})
   ck(q['ok'],'Stage '+str(stage)+' starts')
   for _ in range(600):
    p.evaluate('()=>stageLoadTick()');p.wait_for_timeout(100)
    if p.evaluate('()=>stageLoadInfo(run.stage).ready'):break
   info=p.evaluate('()=>stageLoadInfo(run.stage)')
   ck(info['ready'] and info['failed']==0,'Stage '+str(stage)+' preload completes with zero failed textures')
   p.evaluate(shoot.STEP,60);p.wait_for_timeout(200)
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   cap('stage-'+str(stage))
  # Current ordinary, alternate, phase and donor routes, including every current miniboss.
  codes=p.evaluate('()=>Object.keys(ON5_CODES)')
  if args.engine!='chromium':codes=codes[:2]+codes[-12:]
  for code in codes:
   p.evaluate('code=>{const E=ON5_CODES[code];diffKey="furious";DIFF=DIFFS.furious;run.mode="arcade";run.pilot="yuri";beginStage(E.stage);setState(GS.PLAY);player.reset();player.invuln=1e9;on5LaunchEncounter({...E,code});const b=E.role==="boss"?boss:subBoss;if(b){b.enter=false;b.x=worldWidth()/2;b.y=b.ty||170;b._drawY=b.y;}player.x=worldWidth()/2;player.y=VH-80;camX=player.x-VW/2;}',code)
   p.wait_for_timeout(350)
   for _ in range(4):p.evaluate('(n)=>{for(let i=0;i<n;i++)updatePlay(1/60);}',15);p.wait_for_timeout(40)
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}');cap('fight-'+code.lower());ck(True,code+' actual encounter renders')
  p.wait_for_timeout(2000);ck(not archive_requests,'Production menus and fights never fetch archived artwork');ck(not errors,'Zero native page, console or missing-asset errors');br.close()
finally:stop()
report={'checks':checks,'errors':errors,'archive_requests':archive_requests,'captures':captures,'scope':'Protected short native art fixtures, not full campaign clears.'};(O/'verification.json').write_text(json.dumps(report,indent=2));bad=[c['name'] for c in checks if not c['ok']];print(json.dumps({'checks':len(checks),'failed':bad,'errors':errors,'archive_requests':archive_requests}));assert not bad and not errors
