"""Real Chromium Frost Cruiser difficulty variant verification."""
from pathlib import Path
import sys,json,base64,hashlib,http.server,subprocess
import imageio_ffmpeg
R=Path(__file__).resolve().parents[2];O=R/'_shots/cryo_variant_0914'
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(R/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=shoot.serve(str(R));checks=[];errors=[];details={}
def check(v,label):checks.append({'pass':bool(v),'label':label});print(('ok 'if v else'FAIL ')+label,flush=True)
with sync_playwright()as p:
 b=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);pg=b.new_page(viewport={'width':1100,'height':1200})
 pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 pg.goto('http://127.0.0.1:%d/index.html'%port,wait_until='load',timeout=120000);pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
 pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB)
 def step(n):
  for i in range(0,n,20):pg.evaluate('n=>__step(n)',min(20,n-i));pg.wait_for_timeout(10)
 def shot(name):
  (O/(name+'.png')).write_bytes(base64.b64decode(pg.evaluate('()=>document.querySelector("#screen").toDataURL().split(",")[1]')))
 def fight(stage,role):
  pg.evaluate('a=>{__auto=function(){};__fight(a[0],a[1],"yuri");stagePlan=[];enemies=[];story=null;playerHit=function(){};Object.keys(Input.keys).forEach(k=>Input.keys[k]=false);}',[stage,role]);step(2)
  for _ in range(240):
   if pg.evaluate('role=>!!(role==="mini"?subBoss:boss)',role):break
   step(4);pg.wait_for_timeout(20)
  assert pg.evaluate('role=>!!(role==="mini"?subBoss:boss)',role), 'fight target did not spawn'
 def movie(name,n,snaps):
  ff=imageio_ffmpeg.get_ffmpeg_exe();path=O/(name+'.mp4');q=subprocess.Popen([ff,'-y','-v','error','-f','image2pipe','-vcodec','mjpeg','-framerate','30','-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',str(path)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
  for f in range(n*30):
   pg.evaluate('()=>__step(2)')
   q.stdin.write(base64.b64decode(pg.evaluate('()=>document.querySelector("#screen").toDataURL("image/jpeg",.90).split(",")[1]')))
   if f in snaps:shot(snaps[f])
   if f%30==0:pg.wait_for_timeout(10)
  q.stdin.close();err=q.stderr.read();assert q.wait()==0,err;subprocess.run([ff,'-v','error','-i',str(path),'-f','null','-'],check=True)


 def spawn(d,stage=3,role='mini'):
  pg.evaluate('d=>{diffKey=d;}',d);fight(stage,role)
  for _ in range(180):
   if pg.evaluate('role=>{const b=role==="mini"?subBoss:boss;return b&&!b.enter&&b.y>65;}',role):break
   step(4)
  pg.wait_for_function('()=>XART.rdy("nsb_frost_cruiser")',timeout=120000)
  pg.evaluate('()=>{eBullets=[];pBullets=[];powerups=[];story=null;}')
 pg.evaluate("""()=>{window.__hullDraws=[];window.__variantKey=null;const plate=frostCruiserVariantPlate;frostCruiserVariantPlate=function(k){const im=plate(k);__variantKey=k;return im;};const draw=ctx.drawImage;ctx.drawImage=function(){if(__variantKey){__hullDraws.push({key:__variantKey,args:Array.from(arguments).slice(1)});__variantKey=null;}return draw.apply(this,arguments);};}""")
 rows=[]
 for d in ['easy','normal','hard','furious']:
  spawn(d);pg.evaluate('()=>{subBoss.x=worldWidth()/2;subBoss.y=150;subBoss._drawY=150;subBoss._sba=null;subBoss._sbaKick=0;subBoss._sbaHitT=0;subBoss._sbaPhaseT=0;subBoss._jc.rot=0;subBoss._jc.charge=0;subBoss._jc.thrust=0;subBoss.fireCd=999;shake=0;drawWorld(0);}')
  shot(d+'_live');rows.append(pg.evaluate('()=>({difficulty:diffKey,kind:subBoss._ship,variant:subBoss._jc.hardVariant,w:subBoss.w,h:subBoss.h,mounts:["L","C","R"].map(k=>({slot:k,...shipBossMount(subBoss,k)})),x:subBoss.x,y:subBoss.y})'))
 details['difficulties']=rows
 check(all(r['kind']=='frostcruiser'for r in rows),'the real stage-3 roster spawns Frost Cruiser, not the alternate Cryo Spear')
 check(all(r['w']==168 and r['h']==168 and not r['variant']for r in rows[:2]),'Easy and Normal retain the original 168px hull')
 check(all(abs(r['w']-226.8)<.001 and abs(r['h']-226.8)<.001 and r['variant']for r in rows[2:]),'Hard and Furious enlarge both hull dimensions by exactly 35 percent')
 check(all(abs((r['mounts'][2]['x']-r['x'])/(rows[1]['mounts'][2]['x']-rows[1]['x'])-1.35)<.001 for r in rows[2:]),'wing weapon origins grow with the hull instead of remaining at the old width')
 pixels=pg.evaluate("""()=>{const k='nsb_frost_cruiser',im=XART.get(k),v=frostCruiserVariantPlate(k),c=document.createElement('canvas');c.width=v.width;c.height=v.height;const g=c.getContext('2d');g.drawImage(im,0,0);const a=g.getImageData(0,0,c.width,c.height).data,b=v.getContext('2d').getImageData(0,0,c.width,c.height).data;let alpha=0,protectedChanged=0,changed=0,blue=0,outline=0,sum=0,total=0;for(let i=0;i<a.length;i+=4){if(a[i+3]!==b[i+3])alpha++;if(!a[i+3])continue;const r=a[i],n=a[i+1],z=a[i+2],L=.2126*r+.7152*n+.0722*z,keep=L<22||(r>n*1.18&&r>z*1.12)||(Math.max(r,n,z)>210&&Math.max(r,n,z)-Math.min(r,n,z)>95),diff=r!==b[i]||n!==b[i+1]||z!==b[i+2];if(keep&&diff)protectedChanged++;if(diff){changed++;if(b[i+2]>b[i+1]&&b[i+2]>b[i])blue++;sum+=.2126*b[i]+.7152*b[i+1]+.0722*b[i+2];total+=L;}if(L<22&&!diff)outline++;}return {key:k,alpha,protectedChanged,changed,blue,outline,luminanceRatio:sum/total};}""");details['palette']=pixels
 check(pixels['alpha']==0 and pixels['protectedChanged']==0 and pixels['outline']>0,'palette preserves every alpha pixel, black outline, warm accent and bright emitter')
 check(pixels['changed']>1000 and pixels['blue']==pixels['changed']and pixels['luminanceRatio']<.85,'armor receives shaded black and royal-dark-blue tones')
 pg.evaluate("""()=>{ctx.save();ctx.setTransform(2,0,0,2,0,0);ctx.fillStyle='#102033';ctx.fillRect(0,0,VW,VH);ctx.drawImage(XART.get('nsb_frost_cruiser'),26,85,168,168);ctx.drawImage(frostCruiserVariantPlate('nsb_frost_cruiser'),220,65,226.8,226.8);msgText('NORMAL',110,315,16,'#ffffff',1,1);msgText('HARD / FURIOUS',335,315,16,'#ffffff',1,1);ctx.restore();}""");shot('palette_comparison')
 spawn('hard');pg.evaluate('()=>{__hullDraws=[];}')
 for hp,n in [(1,'intact'),(.5,'damaged'),(.2,'enraged')]:
  pg.evaluate('q=>{subBoss.hp=subBoss.maxhp*q;subBoss._animKey=null;subBoss.flash=0;}',hp);step(3);shot('hard_'+n)
 check(pg.evaluate('()=>__hullDraws.length>=3&&__hullDraws.every(q=>q.key==="nsb_frost_cruiser"&&Math.abs(q.args[q.args.length-2]-226.8)<.001&&Math.abs(q.args[q.args.length-1]-226.8)<.001)'),'intact, damaged and enraged states keep the enlarged variant in real drawImage calls')
 origins=pg.evaluate("""()=>{subBoss._jc.rot=0;subBoss._sba=null;subBoss._sbaHitT=0;subBoss._sbaKick=0;subBoss._sbaPhaseT=0;const b=subBoss,out=[];for(const slot of ['L','R']){const m=shipBossMount(b,slot),n=eBullets.length;jungleCruiserPodPair(b,slot,false);out.push({slot,match:eBullets.slice(n).every((q,i)=>Math.abs(q.x-m.x-(i?4:-4))<.001&&Math.abs(q.y-m.y-2)<.001),unchanged:eBullets.slice(n).every(q=>q.kind==='emissile'&&q._jcRocket)});}const m=shipBossMount(b,'C');jungleCruiserNoseRound(b);const q=eBullets[eBullets.length-1];out.push({slot:'C',match:q.x===m.x&&q.y===m.y,unchanged:q.kind==='mg'});return out;}""");details['origins']=origins
 check(all(q['match']and q['unchanged']for q in origins),'actual pod missiles and nose rounds leave scaled mounts and retain their ordnance families')
 hits=pg.evaluate('()=>{subBoss._jcGhost=false;return {inner:subBossHit(subBoss.x+110,subBoss.y),outer:subBossHit(subBoss.x+140,subBoss.y)};}');check(hits['inner']and not hits['outer'],'existing hull-hit routing expands with the larger target and rejects points outside it')
 pg.evaluate("()=>{subBoss.hp=subBoss.maxhp;subBoss._jc.enraged=false;subBoss._jc.damaged=false;subBoss._jc.rageQueued=false;subBoss._jc.blasts=[];jungleCruiserSetState(subBoss,'acquire');eBullets=[];pBullets=[];powerups=[];story=null;}")
 movie('Frost_Cruiser_Hard_Variant_0914',7,{28:'hard_attack',130:'hard_pattern'})
 spawn('hard',3,'boss');check(pg.evaluate('()=>boss._ship==="cryospear"&&!(boss._jc&&boss._jc.hardVariant)&&boss.w===SHIPBOSS.cryospear.w'),'stage-3 end boss is not accidentally enlarged or recolored')
 check(pg.evaluate("()=>{const b={_ship:'junglecruiser',x:240,y:100,w:SHIPBOSS.junglecruiser.w,h:SHIPBOSS.junglecruiser.h};jungleCruiserInit(b);return !b._jc.hardVariant&&b.w===SHIPBOSS.junglecruiser.w;}"),'the shared Jungle Cruiser encounter does not inherit the frost-only variant')
 check(not errors and not pg.evaluate('()=>window.__err||null'),'no page, console or game-loop errors')
 details['runtimeSha256']=hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest();(O/'native.json').write_text(json.dumps({'checks':checks,'errors':errors,'details':details,'fixture':'Real debug fights across four difficulties; controlled HP snapshots and capture-only invincibility. Silent seven-second Hard preview.'},indent=2)+'\n');b.close()
stop();assert all(c['pass']for c in checks)
