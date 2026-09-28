"""Native warning coverage for the upgraded encounter directors."""
import ast,base64,http.server,json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(sh.GAME)
OUT=Path(sh.GAME)/'_shots/repair_0927';OUT.mkdir(parents=True,exist_ok=True)
tree=ast.parse((Path(sh.GAME)/'_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(str(ROOT));errors=[];report={'encounters':[],'sewer':[]}
def shot(p,name):
 p.evaluate('()=>{const inv=player.invuln;player.invuln=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);player.invuln=inv;}')
 (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1200});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate("()=>{l23FovWarm();for(const k of Object.keys(MR27_ART))XART.rdy('mr27_'+k);s7mWarm();}")
  p.wait_for_function("()=>['bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall','bmfx_alert_red_danger'].every(k=>XART.rdy(k))&&Object.keys(MR27_ART).every(k=>XART.rdy('mr27_'+k))")
  for stage,kind,mini in [(2,'magmaward',True),(3,'frostcruiser',True),(3,'cryospear',False),(4,'olivewarden',True),(4,'stormsovereign',False)]:
   p.evaluate(SETUP,{'stage':stage,'kind':kind,'mini':mini,'diff':'furious'})
   p.evaluate("()=>{story=null;B.enter=false;B._noHit=false;B.x=worldWidth()/2;B.y=180;B._drawY=B.y;er26Init(B);if(B._s4war?.shield){B._s4war.shield.active=false;B._s4war.shield.rearming=false;}}")
   report['encounters'].extend(p.evaluate("""()=>{const result=[];for(const mode of er26Book(B)){polishReset();groundTargetingFx=[];eBullets=[];B._l23Beam=null;er26Set(B,mode);const R=B._er26;R.t=R.warm*.60;er26Tick(B,.001);result.push({kind:B.kind,mode,earlyShots:eBullets.length,fields:R.warnings.length,beam:!!B._l23Beam,ground:groundTargetingFx.length,lanes:polishLanes.length});}return result;}"""))
   if kind in ['cryospear','stormsovereign']:
    p.evaluate("()=>{B._l23Beam=null;polishReset();er26Set(B,'bastion-gates');B._er26.t=B._er26.warm*.60;er26Tick(B,.001);}");shot(p,'boss-fov-'+kind)
    if kind=='cryospear':
     report['gate']=p.evaluate("""()=>{const R=B._er26,angles=R.warnings.map(w=>w.angle),gap=R.gateGap;eBullets=[];R.t=R.warm;er26Tick(B,.01);const first=eBullets.slice();R.shot=0;er26Tick(B,.01);return{warned:angles.length,first:first.length,match:first.every(q=>angles.some(a=>Math.abs(a-q.ang)<1e-8)),committed:R.gateGap===gap,second:eBullets.length-first.length};}""")
  for kind,mini in [('dualscoopdredger',True),('sludgeemperor',False)]:
   p.evaluate(SETUP,{'stage':7,'kind':kind,'mini':mini,'diff':'furious'})
   p.evaluate("()=>{story=null;B.enter=false;s7mInit(B);B.x=worldWidth()/2;B.y=180;}")
   modes=['tank-cross','tank-orbits','tank-charge'] if mini else ['chain','aim','laser','orbs','bounce','swipeL','swipeX']
   for mode in modes:
    report['sewer'].append(p.evaluate("""mode=>{eBullets=[];s7mSet(B,mode);const M=B._s7mod;M.t=mode==='bounce'?.55:M.warn*.60;s7mTick(B,.001);let fields=0,alerts=0;const draw=combatWarningDraw;combatWarningDraw=(o,q)=>{if(q.fieldOnly)fields++;if(q.alertOnly)alerts++;draw(o,q);};try{s7mWarnings(false);s7mWarnings(true);}finally{combatWarningDraw=draw;}return{mode,fields,alerts,earlyShots:eBullets.length};}""",mode))
   shot(p,'sewer-fov-'+kind)
  report['counter']=p.evaluate("""()=>{const M=B._s7mod;for(const q of M.parts)if(/front|rear/.test(q.id))q.hp=0;M.shield=100;M.counter=0;s7mSet(B,'recover');eBullets=[];s7mHit(B,1,B.x,B.y,'core');const queued=!!M.counterTell,instant=eBullets.length;s7mTick(B,.4);const before=eBullets.length;s7mTick(B,.66);return{queued,instant,before,released:eBullets.length};}""")
  report['errors']=errors;br.close()
finally:stop()
(OUT/'boss-warnings-probe.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
assert not errors,errors
assert all(q['earlyShots']==0 and (q['fields'] or q['beam'] or q['ground'] or q['lanes']) for q in report['encounters'])
assert all(q['earlyShots']==0 and q['fields'] and q['alerts'] for q in report['sewer'])
assert report['counter']['queued'] and report['counter']['instant']==report['counter']['before']==0 and report['counter']['released']>0
assert report['gate']['match'] and report['gate']['committed'] and report['gate']['first']==report['gate']['second']==report['gate']['warned']
