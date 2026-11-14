from pathlib import Path
from PIL import Image
import json,hashlib,shutil,math,statistics
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;O=W.parents[1]/'outputs/snake-assault';v=json.loads((O/'verification.json').read_text());art=json.loads((O/'art.json').read_text());assert all(v['checks'].values())and not v['errors'];assert (R/'assets/sumpjaw_tandem_1105.js').read_bytes()==(W/'candidate/sumpjaw_tandem_1105.js').read_bytes()
rows=v['rows'];target=v['data']['target'];arches=[]
for i in range(2):
 r=min((r for r in rows if r['mode']=='arch'),key=lambda r:abs((r['ct']-i*.18)/1.35-.5));a=r['actors'][i];dist=math.hypot(a['x']-target['x'],a['gy']-target['y']);assert dist<24 and a['h']>100;arches.append({'actor':i,'ground_distance_from_committed_player':dist,'height':a['h']})
speeds=[]
for n in range(4):
 samples=[r for r in rows if r['mode']=='side-run'and r['pass']==n];vel=[abs((b['actors'][0]['x']-a['actors'][0]['x'])/(b['t']-a['t']))for a,b in zip(samples,samples[1:])if b['t']>a['t']];actual=statistics.median(vel);assert abs(actual-[430,560,700,880][n])<1;speeds.append(actual)
for n,a in art.items():
 p=W/'candidate/frames'/(n+'.png');im=Image.open(p);w,h=a['cell'];assert w%2==0 and h%2==0 and im.width==w*a['cols']and im.height==h*math.ceil(a['frames']/a['cols']);assert p.read_bytes()==(R/a['path']).read_bytes();assert(O/'editable'/(n+'.aseprite')).exists()
compat=json.loads((W/'sumpjaw_tandem_1105-probe/report.json').read_text());assert all(c['passed']for c in compat['checks']);shutil.copy2(W/'compat.log',O/'compatibility.log');shutil.copy2(W/'suite.log',O/'full-suite.log');shutil.copy2(R/'assets/sumpjaw_tandem_1105.js',O/'sumpjaw_tandem_1105.js')
summary={
 'native_checks':len(v['checks']),'compatibility_checks':len(compat['checks']),
 'actual_side_speeds':speeds,'arches_over_player':arches,
 'new_authored_banks':len(art),'new_frames':sum(a['frames']for a in art.values()),
 'gif_frames':v['frames'],'gif_game_size':[480,512],
 'gif_duration_seconds':sum(60 if i%3==0 else 70 for i in range(v['frames']))/1000,
 'errors':v['errors'],
 'full_suite':{'exit_code':1,'existing_blocker':'difficultyHealthBaseline15 is not defined at assets/combat_polish_0927b.js:151'},
 'runtime_sha256':hashlib.sha256((O/'sumpjaw_tandem_1105.js').read_bytes()).hexdigest()
};(O/'verification-summary.json').write_text(json.dumps(summary,indent=2))
(O/'README.md').write_text('Sumpjaw side-rush / burrow / paired arches\n\nBoth snakes perform four alternating offscreen-to-offscreen side runs at430,560,700 and880px/s. Each has1.05s of source-authored green/yellow/red directional arrows. The heads use the actual path tangent and fire rapid toxic balls forward from their measured mouths. New side rounds outrun the snake and keep the existing unshootable/capped/lifetime rules.\n\nThey slither to separate burrow points; the heads descend through authored source-pixel poses while each body section feeds into its pit. Both become fully underground. Two marked emergence points commit to the pilot current position. The snakes rise from their pits and perform staggered high arches over that committed point, land, then leave north and return to the existing book. Moving the pilot after commitment does not move the targets.\n\nNative pools, gill gates, independent7000HP halves, hit flashes, pause, survivor and once-only defeat/reward remain. The earlier continuously moving jumps are retained. Player shooting/interception rules stay native.\n\nGIF: both-snakes-full-sequence.gif — full native480x512 view,15fps, first warning through the two landings; MP4 also included. QA starts directly at the new chapter and protects the stationary pilot; all later phases/attacks use native update/draw owners.\n\nNew pit art was made with the built-in image generator and saved as generated-burrow-master.png; prompt is in generation-prompt.txt. Existing serpent identity, damage/hit frames and warning-arrow silhouette are retained.448 authored frames in18 fixed even-size banks; editable Aseprite sources in editable/. Runtime uses fixed blits and positions only.\n\nSee verification-summary.json for observed speed/overflight results. The full test suite still exits1 at its recorded missing difficultyHealthBaseline15 dependency; it is not a full-suite pass.\n',encoding='utf-8');print(json.dumps(summary))
