"""Stage 5 authored attack frames, chrome lanes, lockable modules, and spell commitment."""
import sys,json,base64,http.server
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path('_shots/hammer_authored_0926');out.mkdir(exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[];report={}
def save(pg,name):
 data=pg.evaluate("()=>ctx.canvas.toDataURL('image/png')")
 (out/(name+'.png')).write_bytes(base64.b64decode(data.split(',',1)[1]))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
  pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':True})
  pg.evaluate("""() => {
    diffKey='furious';DIFF=DIFFS.furious;story=null;stagePlan=[];enemies=[];pBullets=[];eBullets=[];
    spawnBoss('chromehammer');boss.x=(camLeftX()+camRightX())/2;boss.y=VH*.34;boss.enter=false;
    boss._noHit=false;boss._hammer.balance0922=true;player.invuln=1e9;
    for(const k of ['arch_whirlwind_0926','arch_orbital_sweep_0926','arch_chromium_beam_0926'])XART.rdy(k);
  }""")
  pg.wait_for_function("()=>['arch_whirlwind_0926','arch_orbital_sweep_0926','arch_chromium_beam_0926'].every(k=>XART.rdy(k))")
  report['beamCollision']=pg.evaluate("""() => {
    const oldHit=playerHit,b=boss,h=b._hammer,px=player.x,py=player.y,results=[];
    try{
      for(const test of [{name:'above',x:b.x,y:b.y-65},{name:'core',x:b.x,y:b.y+100},{name:'leftEscape',x:camLeftX()+12,y:b.y+100},{name:'rightEscape',x:camRightX()-12,y:b.y+100}]){
        let hits=0;playerHit=()=>{hits++};hammerState(b,'mega_beam');h.t=1;h.hitCd=0;h.shotCd=99;player.x=test.x;player.y=test.y;
        hammerBossTick(b,1/60);results.push({name:test.name,hits});
      }
    }finally{playerHit=oldHit;player.x=px;player.y=py;}
    return results;
  }""")
  report['spell']=pg.evaluate("""() => {
    const b=boss,h=b._hammer;hammerSpellStart(b);
    for(let i=0;i<110;i++){player.x=camRightX()-20;hammerBossTick(b,1/60);}
    const before=h.spellTargets.map(q=>q.x),locked=h.spellTargets.every(q=>q.locked);
    player.x=camLeftX()+20;for(let i=0;i<20;i++)hammerBossTick(b,1/60);
    return {before,after:h.spellTargets.map(q=>q.x),locked,gaps:before.slice(1).map((x,i)=>x-before[i])};
  }""")
  pg.evaluate("""() => {
    ctx.canvas.width=1200;ctx.canvas.height=760;ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#172838';ctx.fillRect(0,0,1200,760);
    for(let f=0;f<8;f++){boss.x=150+(f%4)*300;boss.y=210+Math.floor(f/4)*370;hammerOrbitalPose(boss,f,.85);}
  }""");save(pg,'orbital_frames')
  report['difficulties']=[]
  for difficulty in ['normal','hard','furious']:
   pg.evaluate("""d => {
     diffKey=d;DIFF=DIFFS[d];ctx.canvas.width=VW*SS;ctx.canvas.height=VH*SS;
     boss.x=(camLeftX()+camRightX())/2;boss.y=VH*.34;hammerState(boss,'mega_beam');boss._hammer.t=1.8;
     player.x=camLeftX()+28;player.y=VH*.76;shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);
   }""",difficulty)
   pg.wait_for_timeout(60)
   pg.evaluate("()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60)}");save(pg,'beam_'+difficulty)
   report['difficulties'].append(pg.evaluate("()=>({difficulty:diffKey,width:hammerEradWidth(),duration:hammerEradDuration(),escapeLane:(VW-hammerEradWidth())/2})"))
  pg.evaluate("""() => {
    hammerSpellStart(boss);boss._hammer.pillars=boss._hammer.spellTargets.map(q=>({x:q.x,t:0}));
    hammerState(boss,'spell_blast');boss._hammer.t=.5;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);
  }""");save(pg,'spell_pillars')
  br.close()
finally:stop()
report['errors']=errors;(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
assert not errors
assert [x['hits'] for x in report['beamCollision']]==[0,1,0,0]
assert report['spell']['locked'] and report['spell']['before']==report['spell']['after']
assert all(abs(gap-72)<.001 for gap in report['spell']['gaps'])
assert all(d['escapeLane']>=70 for d in report['difficulties'])

