from pathlib import Path
import sys,json,time,base64,subprocess,shutil,hashlib
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Release-checks-1114';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
setup=(W.parent/'stage5_bomber_assault_1114/setup.js').read_text();audio=(W.parent/'draconus_rotor_stages_1111/record-audio-init.js').read_text();capture=(W.parent/'restore_boss_1112/capture.js').read_text().replace("(window.reviewLabel||'Recovered animations')+' / NATIVE ANIMATION CHECKPOINT / INVULNERABLE REVIEW'","'ROTATING / FLASHING / BEEPING TARGET LOCK — FURIOUS — INVULNERABLE REVIEW'")
checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS 'if ok else'FAIL ')+name,str(data)[:700]if not ok else'',flush=True);(O/'targeting-checks.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2))
port,stop=serve(str(R));raw=O/'retina-raw.mp4';movie=O/'bomber-retina-rotation-flash-beeps.mp4';assert not raw.exists()and not movie.exists()
hashes={n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in ['assets/game.js','assets/difficulty_helpers_1114.js','assets/difficulty_rules_1101.js','assets/stage5_bomber_assault_1114.js','assets/stage5_bomber_assault_art_1114.js','index.html']}
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling']);c=br.new_context(viewport={'width':1280,'height':800});c.add_init_script(audio);c.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});");p=boot(c,port,5,errors,'mini');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&s5b14Warm()}',timeout=180000)
  p.evaluate("""()=>{window.cueSpy=[];window.opticSpy=[];const play=Snd.play,blit=s5b14Blit;Snd.play=function(k,...a){if(k==='retinaLockBeep')cueSpy.push({phase:subBoss?._s5b14?.phase,t:subBoss?._s5b14?.t,locked:subBoss?._s5b14?.locked});return play.call(this,k,...a)};s5b14Blit=function(n,f,x,y,...a){if(n==='retina_tracking_1114')opticSpy.push({f,x,y});return blit.call(this,n,f,x,y,...a)};}""")
  p.evaluate(setup,'furious');p.evaluate("()=>{powerups=[];s5b14Mode(B,'lock');cueSpy=[];opticSpy=[]}")
  q=p.evaluate("""()=>{const rows=[],locks=playerLocks.length;for(let i=0;i<48;i++){updatePlay(1/60);if(i%3===0){s5b14Optic(B);rows.push({t:M.t,f:opticSpy.at(-1)?.f,target:{...M.target}})}}return{rows,beeps:cueSpy.slice(),locksBefore:locks,locksAfter:playerLocks.length}}""")
  frames=[q['f']for q in q['rows']];ck('Tracking continuously cycles baked headings and bright/dim authored frames',len(set((f%32)//2 for f in frames))>=8 and{f%2 for f in frames}=={0,1},q['rows'])
  beeps=q['beeps'];gaps=[b['t']-a['t']for a,b in zip(beeps,beeps[1:])];ck('Repeated owner-timed beeps accelerate while tracking, without changing player Retina ownership',len(beeps)>=5 and all(not b['locked']and b['phase']=='lock'for b in beeps)and gaps[-1]<=gaps[0]and q['locksBefore']==q['locksAfter'],dict(beeps=beeps,gaps=gaps))
  p.evaluate('()=>{for(let i=0;i<5;i++)updatePlay(1/60);drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(O/'retina-committed.png'));q=p.evaluate("""()=>{const n=cueSpy.length,target={...M.target},x=player.x;player.x+=70;for(let i=0;i<14;i++)updatePlay(1/60);return{locked:M.locked,silent:cueSpy.length===n,stable:JSON.stringify(target)===JSON.stringify(M.target),phase:M.phase}}""");ck('Just before firing, the red lock commits and the tracking beeps stop',q['locked']and q['silent']and q['stable']and q['phase']=='lock',q)
  p.evaluate(setup,'normal');q=p.evaluate("""()=>{s5b14Mode(B,'lock');for(let i=0;i<12;i++)updatePlay(1/60);for(const id of ['laserL','laserR']){const m=siegeBomberParts(B).find(q=>q.id===id);siegeBomberHit(B,99999,m.x,m.y,id);}const n=cueSpy.length;for(let i=0;i<90;i++)updatePlay(1/60);return{quiet:n===cueSpy.length,guns:s5b14Guns(B).length,target:M.target}}""");ck('Destroyed cannons cancel their targeting beeps and optic',q['quiet']and q['guns']==0 and q['target']is None,q)
  p.evaluate(setup,'normal');p.evaluate("s5b14Mode(B,'lock');setState(GS.PAUSED)");before=p.evaluate('({n:cueSpy.length,t:M.t})');p.evaluate(STEP,30);after=p.evaluate('({n:cueSpy.length,t:M.t})');ck('Pause freezes both the animated lock and beep scheduler',before==after,dict(before=before,after=after))
  p.evaluate(setup,'furious');p.evaluate('()=>{powerups=[];cueSpy=[];opticSpy=[];Audio.stopMusic();window.reviewLabel="ROTATING TARGET LOCK";}')
  # Real-clock native combat and real shared mixer, no manual phase progression.
  with raw.open('wb')as f:
   p.expose_function('saveReviewChunk',lambda b:f.write(base64.b64decode(b)));p.evaluate(capture,5);start=time.monotonic();saved=set();timeline=[];complete=False
   while time.monotonic()-start<45:
    p.wait_for_timeout(80);wall=time.monotonic()-start
    q=p.evaluate('()=>({phase:M.phase,t:M.t,locked:M.locked,beeps:cueSpy.length,commits:S5B14.events.filter(q=>q.event==="optic-commit").length,cool:S5B14.events.filter(q=>q.event==="cannons-cooling").length,hp:B.hp,max:B.maxhp})');q['wall']=wall;timeline.append(q)
    name='tracking'if q['phase']=='lock'and not q['locked']and q['t']>.25 else'locked'if q['phase']=='lock'and q['locked']else'burst'if q['phase']=='burst'else'cooling'if q['phase']=='cool'else None
    if name and name not in saved:p.screenshot(path=str(O/('retina-native-'+name+'.png')));saved.add(name)
    if wall>=12 and q['commits']>=3 and q['cool']>=1:complete=True;break
   stats=p.evaluate("async()=>{await new Promise(r=>{reviewRec.onstop=r;reviewRec.stop()});await reviewPending;reviewLive=false;return{...reviewStats,beeps:cueSpy.slice(),events:S5B14.events}}")
  ck('Real-clock native fight repeatedly beeps, commits, fires, cools and reacquires',complete and stats['cues'].get('retinaLockBeep',0)>=10 and all(not b['locked']for b in stats['beeps'])and stats['peak']>.001 and not stats['tapErrors']and all(q['hp']==q['max']for q in timeline),dict(beeps=stats['cues'].get('retinaLockBeep'),peak=stats['peak'],saved=sorted(saved)))
  ck('Native page/update/draw has no errors',not errors,errors);br.close()
finally:stop()
ff=imageio_ffmpeg.get_ffmpeg_exe();subprocess.run([ff,'-v','error','-i',str(raw),'-map','0:v:0','-map','0:a:0','-c:v','copy','-c:a','aac','-b:a','128k','-movflags','+faststart',str(movie)],capture_output=True,check=True);subprocess.run([ff,'-v','error','-threads','2','-i',str(movie),'-f','null','-'],capture_output=True,check=True)
probe=shutil.which('ffprobe');media=json.loads(subprocess.check_output([probe,'-v','error','-show_streams','-show_format','-of','json',str(movie)]));assert all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in hashes.items())
(O/'retina-recording.json').write_text(json.dumps(dict(stats=stats,timeline=timeline,media=media,errors=errors,hashes=hashes,movieSha256=hashlib.sha256(movie.read_bytes()).hexdigest()),indent=2));assert raw.resolve().parent==O.resolve();raw.unlink();assert all(q['passed']for q in checks)and not errors
print('Completed native rotation/flash/beep preview and focused targeting checks.',flush=True)
