"""Stages1-9 native miniboss/boss comparison on Normal,Hard,Furious.
Normal6-9 are review-only encounters: the campaign still ends at5. Uses actual
native entrances/health/parts/attack books/transformations/defeats and input-only
level5 Cole aiming, with labelled invulnerability. No enemy HP/phase/timer writes
after encounter spawn. The unrelated Stage6 opening radio is excluded.
"""
from pathlib import Path
import sys,json,inspect,hashlib,re,time,subprocess,argparse,http.server
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import rough_riders_capture_base_1028 as rec
from capture_mix_1102 import postmix
P=argparse.ArgumentParser();P.add_argument('--difficulty',required=True,choices=['normal','hard','furious']);P.add_argument('--stages',default='all');P.add_argument('--roles',default='all');P.add_argument('--ids',default='all');P.add_argument('--redo',action='store_true');P.add_argument('--capture-codec',choices=['vp9','vp8'],default='vp9');P.add_argument('--track');P.add_argument('--playfield',action='store_true');args=P.parse_args()
if args.track and not re.fullmatch('[a-z0-9_-]+',args.track):P.error('Track name must be a simple recording label')
O=R/'_shots/boss_comparison_1102'/(args.track or args.difficulty);O.mkdir(parents=True,exist_ok=True)
statefile=O/'batch.json';state=json.loads(statefile.read_text())if statefile.exists()else dict(difficulty=args.difficulty,method=__doc__,jobs={})
minis=['razorback','magmaward','frostcruiser','olivewarden','spacebomber','siegefortress17','dualscoopdredger','heralddeath','voidhorizon']
bosses=['damkeeper','infernoreaver','cryospear','stormsovereign','chromehammer','warhive','sludgeemperor','vileexistence','tidalfusion']
jobs=[]
for stage in range(1,10):
 for role,kind in [('mini',minis[stage-1]),('boss',bosses[stage-1])]:
  jobs.append(dict(id=f'stage{stage}-{role}',stage=stage,role=role,kind=kind,name=f'Stage {stage} '+('miniboss'if role=='mini'else'boss'),demonstrate=35 if stage in [5,8]and role=='boss'else 27,limit=2100 if stage==8 and role=='boss'else 720))
 if stage==6:jobs.append(dict(id='stage6-rough-riders',stage=6,role='boss',kind='rebelsquad',name='Stage6 / Rough Riders alternate route',demonstrate=230,limit=900))
selected=set(range(1,10))if args.stages=='all'else{int(s)for s in args.stages.split(',')};roles={'mini','boss'}if args.roles=='all'else set(args.roles.split(','));jobs=[j for j in jobs if j['stage']in selected and j['role']in roles]
if args.ids!='all':jobs=[j for j in jobs if j['id']in args.ids.split(',')]
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=O
original=inspect.getsource(rec.record);snapshot=rec.SNAPSHOT;capture=postmix(rec.CAPTURE).replace('videoBitsPerSecond:4500000','videoBitsPerSecond:3200000')
if args.capture_codec=='vp8':capture=capture.replace('codecs=vp9,opus','codecs=vp8,opus').replace('videoBitsPerSecond:3200000','videoBitsPerSecond:6000000')
capture=capture.replace("  g.fillStyle=getComputedStyle(document.body).backgroundColor;", "  const frame=Math.floor(elapsed*30);if(frame===window.captureCompositeFrame){requestAnimationFrame(render);return;}window.captureCompositeFrame=frame;g.fillStyle=getComputedStyle(document.body).backgroundColor;")
if args.playfield:
 capture=capture.replace('const stream=canvas.captureStream(30)', 'const stream=cv.captureStream(30)').replace('window.reviewCapture=canvas;', 'window.reviewCapture=cv;').replace('  const frame=Math.floor(elapsed*30);', '  if(cfg.playfield){analyser.getFloatTimeDomainData(samples);for(const v of samples)stats.peak=Math.max(stats.peak,Math.abs(v));stats.frames++;requestAnimationFrame(render);return;}const frame=Math.floor(elapsed*30);')
paths=['index.html']+[s.split('?')[0]for s in re.findall(r'<script src="([^"]+)"',(R/'index.html').read_text(encoding='utf-8'))if(R/s.split('?')[0]).is_file()]
def hashes():return{p:hashlib.sha256((R/p).read_bytes()).hexdigest()for p in paths}
for job in jobs:
 if state['jobs'].get(job['id'],{}).get('passed')and not args.redo:continue
 previous=state['jobs'].get(job['id'])
 # Higher Normal stages are isolated test entries, not campaign unlocks.
 rec.CAPTURE=capture.replace("diffKey='furious';debugUnlocked=true;",f"diffKey='{args.difficulty}';DIFF=difficultyForRun('arcade',diffKey);debugUnlocked=true;")
 rec.CAPTURE=rec.CAPTURE.replace("const b=cfg.role==='mini'?subBoss:boss;", "const b=cfg.role==='mini'?subBoss:boss;if(elapsed>(cfg.demonstrate??25)&&b?._rebels?.ships.some(q=>q.key==='nyx'&&!q.dead&&q._ny46Hidden)&&elapsed-(A.lastRetinaTap??-999)>2.2&&retina.phase!=='locking'&&retina.phase!=='locked'){Input.injectTap('l');A.lastRetinaTap=elapsed;}")
 rec.CAPTURE=rec.CAPTURE.replace("if(!entry)throw Error", "if(cfg.nativeKind){const live=debugFightFor(cfg.stage,cfg.role);if(live){entry.kind=cfg.kind=live.kind;entry.name=live.name;}}if(!entry)throw Error")
 rec.CAPTURE=rec.CAPTURE.replace("debugStartFight(entry,{pilot:'cole',record:false});", "const gate=nf100Ends;try{if(cfg.reviewNormal)nf100Ends=()=>false;debugStartFight(entry,{pilot:'cole',record:false});}finally{nf100Ends=gate;}")
 rec.CAPTURE=rec.CAPTURE.replace("if(cfg.role==='mini')spawnSubBoss(cfg.kind);", "if(cfg.stage===6&&s6Wing){if(cfg.role==='boss')s6WingLaunch(8,true);Object.assign(s6Wing,{route:cfg.kind==='rebelsquad'?'right':'left',choice:false,fake:null,fakeDone:true,_fb2Talked:true,beats:2,all:true,line:null});}if(cfg.role==='mini')spawnSubBoss(cfg.kind);")
 rec.CAPTURE=rec.CAPTURE.replace('debugFight.spawned=true;warnT=0;','debugFight.spawned=true;warnT=0;if(cfg.stage===6){s6Opening=null;fb2Talk=fb2Intro=null;H3.release=false;story=null;}run.spaceLevels=[5,5,5];run.spaceWeapon=1;')
 rec.CAPTURE=rec.CAPTURE.replace("cfg.name+' / FURIOUS / GOD BOT / NATIVE HP & PHASES / '+elapsed.toFixed(1)+'s'", "cfg.name+' / '+cfg.difficulty.toUpperCase()+' / INVULNERABLE INPUT PILOT / NATIVE HP & PHASES'+(cfg.reviewNormal?' / REVIEW ONLY':'')+' / '+elapsed.toFixed(1)+'s'")
 rec.CONFIG={**job,'playfield':args.playfield,'difficulty':args.difficulty,'reviewNormal':args.difficulty=='normal'and job['stage']>=6,'nativeKind':job['id']!='stage6-rough-riders'}
 rec.SNAPSHOT=snapshot.replace('target:reviewBot.targetInfo,',"storm:b?._fb112?{model:b._fb112.model,phase:b._fb112.phase,attack:b._fb112.attack,open:b._fb112.open,core:b._fb112.core.hp,parts:b._fb112.parts.map(p=>({id:p.id,hp:p.hp})),events:FB112.events.slice(-12)}:null,sumpjaw:b?._sj98?{actors:b._sj98.actors.map(a=>({hp:a.hp,max:a.maxhp,phase:a.phase})),events:SJ98.events.slice(-8)}:null,hammer:b?._hammer?{state:b._hammer.state,gun:b._hammer.chainHP,red:!!b._hammer._hf22Red}:null,target:reviewBot.targetInfo,")
 src=original.replace("'s=>{run.stage=s;stageLoadBegin(s);}'",repr("s=>{diffKey='"+args.difficulty+"';DIFF=difficultyForRun('arcade',diffKey);run.stage=s;stageLoadBegin(s);}"))
 src=src.replace("'n=>{beginStage(n);BOFCinematicDirector.cancel();story=null;}'",repr("n=>{const gate=nf100Ends;try{if(diffKey==='normal'&&n>=6)nf100Ends=()=>false;beginStage(n);}finally{nf100Ends=gate;}BOFCinematicDirector.cancel();story=null;}"))
 # Longer Warden tail includes the current escape-to-portal handoff.
 if job['stage']==7 and job['role']=='boss':src=src.replace("q['seconds'] - completed_at > 7", "q['seconds'] - completed_at > 42")
 # Source-stable movies use a compact lossless-input/CRF22 export; keep all raw
 # evidence. No user/trailer scratch is removed by this runner.
 src=src.replace("'-crf', '20'","'-crf', '22'").replace("'videoBitsPerSecond:4500000'","'videoBitsPerSecond:3200000'")
 src=src.replace("'libx264',", "'libx264', '-threads', '2',")
 exec(src,rec.__dict__)
 state['active']=job;statefile.write_text(json.dumps(state,indent=2));before=hashes();print('JOB_START',args.difficulty,job['id'],flush=True)
 try:
  folder=rec.record(job['stage'],job['limit']);report=json.loads((folder/'report.json').read_text());report['difficulty']=args.difficulty;report['method']=__doc__;report['reviewOnlyNormal']=rec.CONFIG['reviewNormal'];report['sourceHashes']=before;report['sourceStable']=before==hashes();(folder/'report.json').write_text(json.dumps(report,indent=2))
  movie=folder/f'stage{job["stage"]}-furious.mp4';d=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-nostats','-i',str(movie),'-af','volumedetect','-f','null','-'],capture_output=True,text=True);(folder/'decode.log').write_text(d.stderr);m=re.search(r'max_volume: ([\-\d.inf]+) dB',d.stderr);peak=float(m[1])if m else-999;last=report['timeline'][-1]
  failures=[q for q in report['failedRequests']if q['failure']!='net::ERR_ABORTED'];checks=dict(complete=report['completed'],decoded=d.returncode==0,audible=-60<peak<0,sourceStable=report['sourceStable'],nativeHealth=report['setup']['difficulty']==args.difficulty,noErrors=not report['pageErrors']and not report['consoleErrors']and not report['assetErrors']and not failures and not report['audio']['tapErrors']and not last['botErrors'])
  first=report['timeline'][0];result=dict(**job,view='playfield'if args.playfield else'cabinet',path=str(movie.relative_to(R)),folder=str(folder.relative_to(R)),seconds=last['seconds'],nativeFps=(last['nativeFrames']-first['nativeFrames'])/max(.1,last['seconds']-first['seconds']),peakDb=peak,checks=checks,passed=all(checks.values()),reviewOnlyNormal=rec.CONFIG['reviewNormal'],actualKind=report['setup']['entry']['kind'])
 except Exception as e:result=dict(**job,passed=False,error=str(e))
 if previous:state.setdefault('previousTakes',[]).append(previous)
 state['jobs'][job['id']]=result;statefile.write_text(json.dumps(state,indent=2));print('JOB_DONE',args.difficulty,job['id'],json.dumps({k:v for k,v in result.items()if k in ['passed','seconds','peakDb','checks','error']}),flush=True)
 if not result['passed']:print('STOP: investigate this take before continuing this track',flush=True);break
state['active']=None;statefile.write_text(json.dumps(state,indent=2));print('TRACK_FINISHED',args.difficulty,flush=True)
