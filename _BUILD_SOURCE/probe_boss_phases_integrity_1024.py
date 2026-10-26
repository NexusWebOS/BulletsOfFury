from pathlib import Path
import json,base64,subprocess,imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/boss_integrity_1024';port,stop=serve(str(R));checks=[];errors=[];records=[]
def ck(n,v,d=None):checks.append({'name':n,'passed':bool(v),'data':d});print(('PASS 'if v else'FAIL ')+n,flush=True)
with sync_playwright()as pw:
 br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(2,2);p.evaluate("()=>{diffKey='furious';debugStartFight({stage:8,role:'boss',kind:'vileexistence',name:'Dracodia'},{pilot:'cole'});}");p.wait_for_function('boss?._r30?.v18',timeout=180000);p.evaluate('v18Warm()');p.wait_for_function('v18Warm()',timeout=180000);p.evaluate(TRAP_RAF);p.wait_for_timeout(30)
 for n,form,name in [(1,0,'ghost'),(2,0,'dracodia-final'),(2,8,'corrupt-hammer'),(2,2,'phoenix-swoop')]:
  p.evaluate("([n,form])=>{v18Budget(boss);j3State(boss).ph21=null;v18Enter(boss,n,form);v18Fight(boss);boss.enter=false;boss._noHit=false;dr5State(boss).introSeen=true;dr5State(boss).introWanted=false;BOFCinematicDirector.cancel();}",[n,form]);p.evaluate(STEP,3)
  if name=='phoenix-swoop':
   r=p.evaluate("""()=>{const b=boss,at=ph21Muzzle(b,'cannonL'),part=r30At(b,at.x,at.y-3);for(const id of ['cannonL','cannonR']){b._lastPart=ph21Part(b,id);modularHit(b._lastPart.hp+1);}const Q=ph21State(b);return{stage:Q.stage,pods:b.parts.filter(p=>p.id.startsWith('cannon')).map(p=>({id:p.id,dead:p.destroyed})),muzzle:at,hit:part?.id,debris:D27_MODULE_DEBRIS.length};}""");ck('Phoenix native cannons exhaust into swoop without body tiles',r['stage']=='swoon'and all(q['dead']for q in r['pods'])and r['debris']==0,r);ck('Phoenix displayed barrel overlaps its native damage target',r['hit']=='cannonL',r)
  if name in ['ghost','dracodia-final']:
   r=p.evaluate("""()=>{drawWorld(0);const before=ctx.getImageData(0,0,cv.width,cv.height).data;for(const p of boss.parts)markHit(p,.12);drawWorld(0);const after=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<after.length;i+=4)if(after[i]>240&&after[i+1]>240&&after[i+2]>240&&before[i]+before[i+1]+before[i+2]<650)white++;return{draws:BI24.draws[v18Model(boss)+'_connected_plate'],white,rig:v18Rig(boss).map(v=>({rot:v.rot,anchor:v.anchor}))};}""");ck(name+' native plate stays connected and visibly flashes',(r.get('draws')or 0)>0 and r['white']>80 and all(v['rot']==0 for v in r['rig']),r)
  ff=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-f','image2pipe','-vcodec','png','-r','10','-i','pipe:0','-vf','scale=960:600:force_original_aspect_ratio=decrease,pad=960:600:(ow-iw)/2:(oh-ih)/2','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(O/(name+'-after.mp4'))],stdin=subprocess.PIPE);last=''
  for f in range(300):
   p.evaluate('()=>{player.invuln=999;player.x=worldWidth()/2+Math.sin(efxClock)*90;}');p.evaluate(STEP,6)
   if f%10==0:
    r=p.evaluate("()=>({mode:boss._r30.mode,form:boss._r30.v18.form,attack:boss._r30.v18.attack?.type,action:hb20Own(boss)?hb20State(boss)?.action?.type:ph21Own(boss)?ph21State(boss)?.action?.mode:null,pose:hb20Own(boss)?hb20Pose(boss)?.kind:null,scale:ph21Own(boss)?ph21State(boss)?.scale:1})");k=json.dumps(r)
    if k!=last:last=k;r.update({'clip':name,'seconds':f/10});records.append(r);(O/(name+f'-{f}.png')).write_bytes(base64.b64decode(p.evaluate("cv.toDataURL().split(',')[1]")))
   ff.stdin.write(base64.b64decode(p.evaluate("cv.toDataURL().split(',')[1]")))
   if f%100==0:p.wait_for_timeout(10)
  ff.stdin.close();ff.wait();print('RECORDED',name,flush=True)
 ck('No page or console errors',not errors,errors);br.close()
stop();(O/'phase-checks.json').write_text(json.dumps({'checks':checks,'records':records,'errors':errors},indent=2),encoding='utf8');raise SystemExit(0 if all(c['passed']for c in checks)else 1)
