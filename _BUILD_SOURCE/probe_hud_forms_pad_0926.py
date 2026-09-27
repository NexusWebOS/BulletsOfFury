import sys,json,base64,http.server
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
from pathlib import Path
sys.path.insert(0,str(Path('_BUILD_SOURCE').resolve()))
import shoot as sh
from playwright.sync_api import sync_playwright

out=Path('_shots/hud_forms_pad_0926');out.mkdir(exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[];report={}
def shot(pg,name):
    data=pg.evaluate("() => ctx.canvas.toDataURL('image/png').split(',')[1]")
    (out/(name+'.png')).write_bytes(base64.b64decode(data))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
  pg.wait_for_function('() => window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF)
  # Save a non-XInput A assignment; reload rather than calling the binding loader directly.
  pg.evaluate("() => {keybind.fire=['j','pad_b2'];keybind.charge=['h','pad_b4'];saveKeybind();}")
  pg.reload(wait_until='load');pg.wait_for_function('() => window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF)
  report['persisted']=pg.evaluate("() => ({fire:keybind.fire,charge:keybind.charge})")
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':6,'pilot':'cole','invuln':True})
  report['padFire']=pg.evaluate("""() => {
    s6Opening=null;stagePlan=[];enemies=[];run.weapon=0;run.wlevel=1;run.spaceMode=false;
    pBullets=[];player.fireCd=0;
    const pad={id:'8BitDo M30 synthetic raw-button probe',index:2,connected:true,mapping:'',axes:[0,0],buttons:Array.from({length:16},()=>({pressed:false,value:0}))};
    navigator.getGamepads=()=>[null,null,pad];pad.buttons[2]={pressed:true,value:1};Input.pollGamepad();
    for(let i=0;i<30;i++)updatePlay(1/60);
    const n=pBullets.length;pad.buttons[2]={pressed:false,value:0};Input.pollGamepad();
    return {shots:n,released:!Input.down('pad_b2')};
  }""")
  report['forms']=pg.evaluate("""() => {
    achievementState.owned={};run.weapon=3;run.forge={};run.forgeForms={};run.forgeElems={fire:1};run.forgeCombos=2;
    const available=weaponBaseForms(3).find(o=>o.id==='firewhip');
    const first=weaponFormSelect(3,available),remaining=run.forgeCombos;
    const second=weaponFormSelect(3,available);pBullets=[];pShoot();
    return {available:!!available,first,second,remaining,after:run.forgeCombos,kind:pBullets[0]?.kind,forms:weaponFormOptions(3)};
  }""")
  pg.evaluate("() => {special={pilot:'cole',t:12,dur:15,strikes:3};for(const k of ['hud_equip_frame_0924','hud_radar_bezel_0924','lock_frame_0922','retm_0'])XART.rdy(k);}")
  pg.wait_for_function("() => ['hud_equip_frame_0924','hud_radar_bezel_0924','lock_frame_0922','retm_0'].every(k=>XART.rdy(k))")
  for i in range(4):pg.evaluate(sh.STEP,5);pg.wait_for_timeout(50)
  report['hud']=pg.evaluate('() => bottomHudLayout()');shot(pg,'hud')
  # Use the game's actual preview/fire/render paths for every weapon/element pair.
  pg.evaluate("() => {setState(GS.LOADOUT);window.__beforeForms=JSON.stringify(run.forgeForms);window.__beforeVars=JSON.stringify(run.wvars);}")
  report['previews']=[]
  for elem in [None,'fire','ice','lightning','prism','toxic','kinetic','chrome','water','dark']:
   pg.evaluate('(elem) => {window.__previews=WEAPONS.map((_,w)=>forgePreviewNew(w,elem,5));}',elem)
   for i in range(6):
    pg.evaluate("() => {for(const p of __previews)for(let i=0;i<15;i++)forgePreviewTick(p,200,260,1/60);for(const p of __previews)forgePreviewDraw(p,0,0,220,300);}")
    pg.wait_for_timeout(35)
   report['previews']+=pg.evaluate("() => __previews.map(p=>({w:p.w,elem:p.elem,lv:p.lv,error:p.err,shots:p.fired,kinds:[...new Set(p.bullets.map(b=>b.kind))],tags:[...new Set(p.bullets.map(b=>b._inf))],positions:p.w===8?p.bullets.map(b=>({x:b.x,y:b.y,life:b.life,kind:b.kind})):[]}))")
   pg.evaluate("""() => {
    const c=ctx.canvas;c.width=960;c.height=1050;ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.fillStyle='#162033';ctx.fillRect(0,0,960,1050);
    for(const p of __previews){const x=(p.w%3)*320,y=Math.floor(p.w/3)*350;forgePreviewDraw(p,x+5,y+24,310,320);ctx.font='16px monospace';ctx.fillStyle='#fff';ctx.fillText(WEAPONS[p.w]+' / '+(p.elem||'base'),x+8,y+18);}
   }""")
   shot(pg,'preview_'+str(elem))
  report['isolated']=pg.evaluate("() => __beforeForms===JSON.stringify(run.forgeForms)&&__beforeVars===JSON.stringify(run.wvars)")
  br.close()
finally:stop()
report['errors']=errors
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='previews'},indent=2))
print('Preview errors:',[p for p in report['previews'] if p['error'] or not p['shots']])
assert not errors and report['isolated']
assert report['padFire']['shots']>0 and report['padFire']['released']
assert report['forms']['kind']=='firewhip' and report['forms']['remaining']==report['forms']['after']==1
assert all(not p['error'] and p['shots']>0 and p['lv']==1 for p in report['previews'])
