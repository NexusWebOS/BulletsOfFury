"""Real Chromium: lightning first, chest-origin armor reveal, completed and interrupted healing."""
import sys,json,base64,http.server
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path('_shots/hammer_core_wave_0926');out.mkdir(exist_ok=True)
errors=[];report={};port,stop=sh.serve(sh.GAME)
fixture="""d=>{
 diffKey=d;DIFF=DIFFS[d];story=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];powerups=[];explosions=[];particles=[];smokeTrails=[];l5Rocks=[];l5RockT=9999;
 spawnBoss('chromehammer');boss.x=340;boss.y=256;boss.enter=false;boss._noHit=false;boss.hp=boss.maxhp*.35;boss._hammer.balance0922=true;
 player.x=340;player.y=410;player.invuln=1e9;player.dead=false;camX=100;boss._hammer.chainDestroyed=true;hammerStormStart(boss);
}"""
def shot(pg,name):
 pg.evaluate('()=>{powerups=[];shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60)}')
 data=pg.evaluate("()=>ctx.canvas.toDataURL('image/png')");(out/(name+'.png')).write_bytes(base64.b64decode(data.split(',',1)[1]))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':True});pg.evaluate(fixture,'normal')
  pg.wait_for_function("()=>['arch_storm_charge_0926','arch_hammer_lightning_0926','arch_stun_0920','arch_stun_static_0926','bmbar_fill_solid'].every(k=>XART.rdy(k))")
  report['order']=[]
  for d in ['normal','hard','furious']:
   pg.evaluate(fixture,d)
   report['order'].append(pg.evaluate("""()=>{
    const h=boss._hammer,samples=[];for(let i=0;i<230;i++){hammerBossTick(boss,1/60);if([73,78,93,108,138,168,219].includes(i))samples.push({t:h.t,lightning:h.lightningCue,charged:h.charged,body:h.empowerLevel});}
    return{difficulty:diffKey,samples};
   }"""))
  pg.evaluate(fixture,'normal')
  report['pixels']=pg.evaluate("""()=>{
   const h=boss._hammer,key='arch_storm_charge_0926';boss.x=240;boss.y=270;boss.flash=0;h.t=3.4;h.chromiumT=1.6;h.charged=true;
   const r=HAMMER_CHARGE_REEL[5],base=hammerEnergySheet(key,HAMMER_CHARGE_REEL,1),frames=[];
   ctx.save();ctx.setTransform(1,0,0,1,0,0);
   for(const level of [-1,0,.12,.34,1]){h.empowered=level>=0;h.empowerLevel=Math.max(0,level);ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);hammerChromiumPoseDraw(boss,key,r,.64,base);frames.push(ctx.getImageData(0,0,ctx.canvas.width,ctx.canvas.height).data);}
   const areas=[{name:'core',x:230,y:260,w:20,h:20},{name:'leftArm',x:185,y:223,w:24,h:24},{name:'rightArm',x:271,y:223,w:24,h:24},{name:'leftBoot',x:177,y:364,w:30,h:24},{name:'rightBoot',x:273,y:364,w:30,h:24}],result=[];
   for(let f=1;f<frames.length;f++){const regions={};for(const a of areas){let changed=0,opaque=0;for(let y=a.y;y<a.y+a.h;y++)for(let x=a.x;x<a.x+a.w;x++){
     const i=(y*ctx.canvas.width+x)*4;if(frames[0][i+3]>128){opaque++;if([0,1,2].some(c=>Math.abs(frames[f][i+c]-frames[0][i+c])>12))changed++;}}
     regions[a.name]={changed,opaque};}result.push({level:[0,.12,.34,1][f-1],regions});}
   ctx.restore();return result;
  }""")
  pg.evaluate(fixture,'normal')
  for name,t in [('lightning',1.40),('core_ignites',1.84),('spreading',2.25),('empowered',3.65)]:
   pg.evaluate('t=>{while(boss._hammer.t<t)updatePlay(1/60)}',t);shot(pg,name)
  # The same chest-origin mask is used when the interrupted weapon reforms.
  pg.evaluate("()=>{const h=boss._hammer;hammerRecoveryBreak(boss);for(let i=0;i<278;i++)updatePlay(1/60)}");shot(pg,'rebuild_core')
  report['rebuild']=pg.evaluate('()=>({state:boss._hammer.state,level:boss._hammer.empowerLevel,status:boss._hammer.recovery.status})')
  pg.evaluate(fixture,'normal')
  data=pg.evaluate("""async()=>{
   const stream=ctx.canvas.captureStream(30),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8',videoBitsPerSecond:3000000}),chunks=[];
   rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};const done=new Promise(resolve=>rec.onstop=()=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
   const start=performance.now();rec.start();await new Promise(resolve=>{const timer=setInterval(()=>{const now=performance.now();powerups=[];loop(now);if(now-start>=9000){clearInterval(timer);resolve();}},1000/60);});
   rec.stop();const result=await done;stream.getTracks().forEach(t=>t.stop());return result;
  }""")
  (out/'core_wave.webm').write_bytes(base64.b64decode(data.split(',',1)[1]));br.close()
finally:stop()
report['errors']=errors;(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
assert not errors,errors
for d in report['order']:
 s=d['samples'];assert not s[0]['lightning'] and s[1]['charged'] and s[1]['body']==0 and s[2]['body']==0 and 0<s[3]['body']<s[4]['body']<s[5]['body']<s[6]['body']==1,d
zero,early,mid,full=[r['regions'] for r in report['pixels']]
assert all(a['changed']==0 for a in zero.values()),zero
assert early['core']['changed']>40 and all(early[n]['changed']==0 for n in ['leftArm','rightArm','leftBoot','rightBoot']),early
assert all(mid[n]['changed']>40 for n in ['core','leftArm','rightArm']) and all(mid[n]['changed']==0 for n in ['leftBoot','rightBoot']),mid
assert all(a['changed']>40 for a in full.values()),full
assert report['rebuild']['state']=='storm_rebuild' and 0<report['rebuild']['level']<1 and report['rebuild']['status']=='cancelled',report['rebuild']
