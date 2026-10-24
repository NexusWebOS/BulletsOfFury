from pathlib import Path
import json, subprocess, time, imageio_ffmpeg, html

W=Path(__file__).resolve().parent
O=W/'review'; M=O/'media'; M.mkdir(parents=True,exist_ok=True)
ff=imageio_ffmpeg.get_ffmpeg_exe()
specs=[
 ('s02_mini_magmaward','Stage 2 · Inferno Reaver','native-final','Every module has its own share of HP. The core opens after all modules break.'),
 ('s03_mini_frostcruiser','Stage 3 · Frost Cruiser','native-final','Authored turret turns and ordinary-weapon access to the rear missile racks.'),
 ('s03_boss_cryospear','Stage 3 · Rime Wall','native-final','Rear missile racks remain reachable after the front cannons break.'),
 ('s04_mini_olivewarden','Stage 4 · Olive Warden','native-final','Ordinary projectile corridors to the live modules.'),
 ('s04_boss_stormsovereign','Stage 4 · Storm Sovereign','native-approved','Reachable generators and cores; one half-health shield rebuild, with the final cannon phase retained.'),
 ('s05_mini_siegebomber','Stage 5 · Siege Bomber','native-final','The engines and rear guns can be reached with straight-firing weapons.'),
 ('s05_boss_chromehammer','Stage 5 · Chronos','native-release','Live dialogue, shielded charging, red spike-ball feedback, distance combo and missile-reversible hammer.'),
 ('s06_mini_siegefortress17','Stage 6 · Siege Fortress','native-final','The exposed reactor alternates wind/lightning spreads and orb pincers.'),
 ('s07_mini_dualscoopdredger','Stage 7 · Caustic Dredger','native-release','Reactive attack selection, crossing volleys and committed double rushes on Furious.'),
 ('s08_mini_heralddeath','Stage 8 · Herald of Death','native-review','Talon pursuit, crossing swoops, feather lanes and a disarmed head phase.'),
 ('s08_boss_vileexistence','Stage 8 · Dracodia','native-approved','Teleport entrance, protected arm/core budget, rolling core, falling destruction and symbiote rebirth into the final arena.'),
 ('alt3_rimewall','Alternate encounter · Rime Wall','native-approved','Fresh take with artwork loading verified before recording.'),
]

def chapter_rows(r):
 out=[{'t':0,'name':'Start'}]; seen=set()
 book=[('dr5er23entry','Arena teleport'),('dr5er23rebirth','Falling host / symbiote rebirth'),('dr5Monologue','New arena / Dracodia speaks'),('encounter0:','First body'),('form8:','Hammer form'),('form1:','Helicopter form'),('form6:','Neural Archon'),('form2:','Volcano form'),('giant_warn','Distance attack'),('er23_depth_combo','Double slam + side sweeps'),('storm_raise','Shielded hammer charge'),('|spin','Hammer throw windup'),('|chaingun','Chaingun'),('fr_activation','Chromium activation'),('|ball','Spike ball'),('reunion','Reunion')]
 for e in r.get('events',[]):
  if e.get('type')!='phase':continue
  phase=e.get('phase','')
  for token,name in book:
   if token in phase and name not in seen:
    seen.add(name);out.append({'t':e['t'],'name':name});break
 if r.get('config',{}).get('kind')=='vileexistence':
  start=next((q['t']for q in out if q['name']=='Falling host / symbiote rebirth'),None);finish=next((q['t']for q in out if q['name']=='New arena / Dracodia speaks'),None)
  if start is not None and finish is not None:
   factor=(finish-start)/28.5
   for dt,name in [(4,'Pilot reaction'),(10.4,'Rising symbiote'),(14,'Fusion'),(17,'24 accelerating lightning beats'),(25.3,'Whiteout / new arena')]:out.append({'t':round(start+dt*factor,2),'name':name})
  samples=[q for q in r.get('samples',[])if '|fight|encounter0:'in q.get('phase','')and q.get('hp')is not None]
  peak=max([q['hp']for q in samples],default=0);roll=next((q for q in samples if peak>0 and q['hp']<=peak*.3345),None)
  if roll:out.append({'t':roll['t'],'name':'Arms down / exposed rolling core'})
 return sorted(out,key=lambda x:x['t'])

def publish(rows):
 (O/'clips.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
 data=json.dumps(rows).replace('</','<\\/')
 page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOF · Corrected encounters</title>
 <style>*{box-sizing:border-box}body{margin:0;background:#08101a;color:#e8edf6;font:16px system-ui}header,main{max-width:1440px;margin:auto;padding:24px}header{padding-bottom:6px}h1{margin:0 0 10px;font-size:clamp(24px,4vw,38px)}p{line-height:1.55;color:#b9c8db}a{color:#72dce9}main{display:grid;grid-template-columns:280px 1fr;gap:22px}nav{display:flex;flex-direction:column;gap:7px}button{background:#142437;color:#e8edf6;border:1px solid #324c65;border-radius:6px;padding:12px;text-align:left;font:inherit;cursor:pointer}button:hover,button[aria-current=true]{border-color:#64dfed;background:#1b3c4c}video{image-rendering:pixelated;display:block;width:100%;background:#000;max-height:72vh}h2{margin:0 0 10px;font-size:23px}.chips{display:flex;gap:8px;flex-wrap:wrap;font-size:13px;margin-bottom:15px}.chips span{background:#173344;border:1px solid #2c5869;border-radius:5px;padding:5px 9px}.chapters{display:flex;gap:7px;flex-wrap:wrap;margin:15px 0}.chapters button{font-size:13px;padding:8px}.foot{font-size:13px;color:#95a9be}.missing{color:#f7ce75}@media(max-width:800px){main{display:block}nav{flex-direction:row;overflow-x:auto;margin-bottom:20px}nav button{flex:0 0 210px}} </style>
 <header><h1>Bullets of Fury · Corrected encounters</h1><p>October 23–24 review. Real-time native game footage with the actual audio, enemies, attacks and damage system. The review bot ignores player damage and uses ordinary controls; enemy HP and phase completion are unchanged.</p><a href="/index.html">All 30 original encounter recordings</a></header>
 <main><nav id="list" aria-label="Choose encounter"></nav><section><h2 id="title"></h2><div class="chips"><span>LIVE ENGINE</span><span>FURIOUS</span><span>COLE · WEAPON LEVEL 3</span></div><video id="player" controls playsinline preload="metadata"></video><p id="description"></p><div class="chapters" id="chapters"></div><p class="foot" id="facts"></p><a id="download" download>Download MP4</a><p class="foot">H.264 / AAC with seeking enabled. No animation interpolation or simulated video. Contact counts from an invulnerable bot are diagnostic and are not a human balance test.</p></section></main>
 <script>const clips=__DATA__,v=document.querySelector('#player'),list=document.querySelector('#list');let selected;
 function choose(c){selected=c;document.querySelector('#title').textContent=c.title;document.querySelector('#description').textContent=c.description;document.querySelector('#facts').textContent=`${Math.round(c.duration)} seconds · ${c.fps.toFixed(1)} engine frames/sec · ${c.completed?'Native defeat recorded':'Recording in progress'}`;v.src=c.file;v.poster=c.poster;document.querySelector('#download').href=c.file;document.querySelectorAll('nav button').forEach(b=>b.setAttribute('aria-current',String(b.dataset.id===c.id)));const ch=document.querySelector('#chapters');ch.replaceChildren();for(const q of c.chapters){const b=document.createElement('button');b.textContent=`${Math.floor(q.t/60)}:${String(Math.floor(q.t%60)).padStart(2,'0')} ${q.name}`;b.onclick=()=>{v.currentTime=q.t;v.play()};ch.append(b)}history.replaceState(null,'','#'+c.id)}
 for(const c of clips){const b=document.createElement('button');b.textContent=c.title;b.dataset.id=c.id;b.onclick=()=>choose(c);list.append(b)}if(clips.length)choose(clips.find(c=>c.id===location.hash.slice(1))||clips[0]);</script></html>'''.replace('__DATA__',data)
 (O/'index.html').write_text(page,encoding='utf-8')

rows=[]
for slug,title,folder,description in specs:
 source=W/folder/(slug+'.webm'); report=W/folder/(slug+'.json')
 while True:
  r=json.loads(report.read_text()) if report.exists() else {}
  if r.get('completed') and r.get('saved') and r.get('reason')=='native-defeat':break
  print('WAIT',slug,flush=True);time.sleep(15)
 target=M/(slug+'.mp4');stamp=M/(slug+'.source.json')
 identity={'bytes':source.stat().st_size,'mtime':source.stat().st_mtime}
 if not target.exists() or not stamp.exists() or json.loads(stamp.read_text())!=identity:
  temp=target.with_suffix('.partial.mp4')
  q=subprocess.run([ff,'-v','error','-y','-i',str(source),'-map','0:v:0','-map','0:a:0?','-c:v','libx264','-preset','veryfast','-crf','23','-maxrate','2000k','-bufsize','4000k','-threads','2','-pix_fmt','yuv420p','-fps_mode','vfr','-c:a','aac','-b:a','128k','-movflags','+faststart',str(temp)],capture_output=True,text=True)
  if q.returncode:raise RuntimeError(q.stderr[-1500:])
  temp.replace(target);stamp.write_text(json.dumps(identity))
 poster=M/(slug+'.png')
 subprocess.run([ff,'-v','error','-ss',str(min(18,r['elapsed']*.3)),'-i',str(target),'-frames:v','1','-y',str(poster)],capture_output=True)
 errors=r.get('pageErrors',[]);js=[e for e in errors if not e.startswith('Failed to load resource') and not e.startswith('The AudioContext')]
 rows.append({'id':slug,'title':title,'file':'media/'+target.name,'poster':'media/'+poster.name,'duration':r['elapsed'],'fps':r['fps'],'completed':r['completed'],'description':description,'chapters':chapter_rows(r),'pageExceptions':js,'assetErrors':r.get('assetErrors',[]),'source':str(source),'report':str(report)})
 publish(rows);print('READY',slug,flush=True)
print('COMPLETE',len(rows),'native recordings',flush=True)
