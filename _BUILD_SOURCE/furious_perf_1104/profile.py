from pathlib import Path
import argparse,collections,json,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2];W=R/'_shots/furious_perf_1104';W.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
ap=argparse.ArgumentParser();ap.add_argument('--label',default='baseline');ap.add_argument('--seconds',type=int,default=18);ap.add_argument('--candidate');ap.add_argument('--baseline',action='store_true');args=ap.parse_args()
baseline=R/'_BUILD_SOURCE/furious_perf_1104/before_controller.js'
if not baseline.exists():baseline.write_bytes((R/'assets/furious_encounters_1102.js').read_bytes())
port,stop=serve(str(R));errors=[]
setup="""()=>{diffKey='furious';DIFF=difficultyForRun('arcade',diffKey);run.stage=6;debugUnlocked=true;debugStartFight({stage:6,role:'mini',kind:'razorwake',name:'RAZORWAKE'},{pilot:'cole',record:false});DBGT.god=true;DBGT.speed=1;player.invuln=0;run.weapon=3;run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);run.bombs=40;if(s6Wing)Object.assign(s6Wing,{route:'left',choice:false,fake:null,fakeDone:true,_fb2Talked:true,beats:2,all:true,line:null});spawnSubBoss('razorwake');debugFight.spawned=true;warnT=0;s6Opening=null;fb2Talk=fb2Intro=null;H3.release=false;story=null;BOFCinematicDirector.cancel();setState(GS.PLAY);window.B=subBoss;}"""
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows'])
  p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)))
  if args.baseline:p.route('**/assets/furious_encounters_1102.js*',lambda r:r.fulfill(path=str(baseline),content_type='application/javascript'))
  p.goto(f'http://127.0.0.1:{port}/index.html?quality=high',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3)
  p.evaluate("()=>{diffKey='furious';DIFF=difficultyForRun('arcade',diffKey);run.stage=6;stageLoadBegin(6);}");p.wait_for_function('()=>{stageLoadTick();return fb112Ready()&&stageLoadReady(6)}',timeout=180000)
  if args.candidate:p.add_script_tag(path=str(W/args.candidate))
  p.evaluate(setup);p.wait_for_timeout(3500)
  p.evaluate("""()=>{window.qaStats={functions:{},cells:0,misses:0,gaps:[],phases:{},running:true,previous:performance.now()};for(const name of ['fb112Draw','fb112Blit','fb112Cell','fb112Opaque','fb112Shadow','fb112Ready','fb112Tick','updatePlay','drawWorld']){const old=window[name];if(typeof old!=='function')continue;const row=qaStats.functions[name]={calls:0,ms:0,max:0};window[name]=function(...args){const a=performance.now();if(name==='fb112Cell'){qaStats.cells++;if(!FB112.cells.has(args[0].key+':'+args[1]))qaStats.misses++;}try{return old.apply(this,args)}finally{const d=performance.now()-a;row.calls++;row.ms+=d;row.max=Math.max(row.max,d)}};}function tick(t){if(!qaStats.running)return;qaStats.gaps.push(t-qaStats.previous);qaStats.previous=t;const q=subBoss?._fb112,key=q?q.phase+':'+q.attack:'none';qaStats.phases[key]=(qaStats.phases[key]||0)+1;requestAnimationFrame(tick)}requestAnimationFrame(tick);}""")
  c=p.context.new_cdp_session(p);c.send('Profiler.enable');c.send('Profiler.setSamplingInterval',{'interval':1000});c.send('Profiler.start');a=p.evaluate('({t:performance.now(),frames:__bofFrames})');p.wait_for_timeout(args.seconds*1000);z=p.evaluate('()=>{qaStats.running=false;return{t:performance.now(),frames:__bofFrames,SS,stats:qaStats,cellBytes:FB112.cellBytes,cache:FB112.cells.size,shadows:FB112.shadows.size,rounds:eBullets.length}}');profile=c.send('Profiler.stop')['profile'];p.screenshot(path=str(W/(args.label+'.png')));b.close()
finally:stop()
nodes={n['id']:n for n in profile['nodes']};counts=collections.Counter()
for sample,delta in zip(profile.get('samples',[]),profile.get('timeDeltas',[])):counts[sample]+=delta
top=[dict(name=nodes[i]['callFrame']['functionName'],file=nodes[i]['callFrame']['url'].split('/')[-1],line=nodes[i]['callFrame']['lineNumber']+1,ms=round(v/1000,2))for i,v in counts.most_common(22)]
gaps=sorted(z['stats']['gaps']);elapsed=z['t']-a['t'];out=dict(label=args.label,fps=(z['frames']-a['frames'])*1000/elapsed,p95=gaps[int((len(gaps)-1)*.95)],p99=gaps[int((len(gaps)-1)*.99)],details=z,top=top,errors=errors)
(W/(args.label+'.json')).write_text(json.dumps(out,indent=2));(W/(args.label+'.cpuprofile')).write_text(json.dumps(profile))
print(json.dumps({k:out[k]for k in ['label','fps','p95','p99','top','errors']},indent=2));print('FUNCTION_TIMES',z['stats']['functions']);print('CELL_CACHE',z['stats']['cells'],z['stats']['misses'],z['cellBytes'])
