from pathlib import Path
import hashlib,json,shutil,subprocess
W=Path(__file__).resolve().parent
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
S=R/'_shots/boss_comparison_1102/furious-new-1104'
batch=json.loads((S/'batch.json').read_text());fast=R/'_shots/boss_comparison_1102/furious-fast-1104/batch.json'
if fast.exists():batch['jobs'].update(json.loads(fast.read_text()).get('jobs',{}))
storm=R/'_shots/boss_comparison_1102/thunderhead-storm-native-final-1104/batch.json'
if storm.exists():batch['jobs'].update(json.loads(storm.read_text()).get('jobs',{}))
modular=R/'_shots/boss_comparison_1102/thunderhead-modular-mp4-1104/batch.json'
if modular.exists():batch['jobs'].update(json.loads(modular.read_text()).get('jobs',{}))
sump=R/'_shots/boss_comparison_1102/sumpjaw-serpents-final-1104/batch.json'
if sump.exists():batch['jobs'].update(json.loads(sump.read_text()).get('jobs',{}))
razor=R/'_shots/boss_comparison_1102/razorwake-tempest-final-ready-1105/batch.json'
if razor.exists():batch['jobs'].update(json.loads(razor.read_text()).get('jobs',{}))
reactor=R/'_shots/boss_comparison_1102/thunderhead-reactor-final-1105/batch.json'
if reactor.exists():batch['jobs'].update(json.loads(reactor.read_text()).get('jobs',{}))
tandem=R/'_shots/boss_comparison_1102/sumpjaw-tandem-final-1105/batch.json'
if tandem.exists():batch['jobs'].update(json.loads(tandem.read_text()).get('jobs',{}))
(W/'posters').mkdir(exist_ok=True)
defs=[('razorwake','stage6-mini','Razorwake','Stage 6 Â· Furious miniboss','Intact modular wings, detachable rotary guns and tapered twin thrusters. Two rolling forward gun runs, center/right/left straight burst lanes and sixteen accelerating north/south passes. Teal aura, wing flaps, lightning and a growing wind Helix orb. Shoot it into nine wind balls, or risk its exclusive vortex crash. About 15% more HP than the native Hard miniboss.'),('thunderhead','stage6-boss','Thunderhead','Stage 6 Â· Furious boss','Connected cyclone cannon beams with animated throat flashes. Four rotating gun batteries target three distinct allies, reserving one for the player in 75% of cycles. Wind rises and rotates inside the chamber. Thunderhead flies into the background, charges, recoils and launches a growing cyclone, then returns. Destroyed modules explode, break away and shatter; all six weapons still gate the core.'),('sumpjaw','stage7-mini','Sumpjaw pair','Stage 7 Â· Furious miniboss','Coordinated serpents repeatedly leap left/right over the pilot while firing large toxic orbs downward. They form a separated firing row, strafe together with rapid dual-mouth bursts, split, jump north and cross over/under each other before returning. The mouths charge internally without a green body aura. One shared bar: 7,000 HP per snake, 14,000 total; break each pair of gills to expose its heart. No small spread pellets.')]
clips=[];routes={};reports=[]
for id,jobid,name,slot,description in defs:
 job=batch['jobs'][jobid];assert job['passed'];folder=R/job['folder'];report=json.loads((folder/'report.json').read_text());file=R/job['path'];assert file.is_file()
 poster=folder/'frame-0008.png';shutil.copyfile(poster,W/'posters'/f'{id}.png')
 chapters=[{'label':'Entrance','time':0}];seen=set()
 labels={'guns':'Twin guns'if id=='razorwake'else'Gun batteries','rotary':'Straight rotary wind-slug streams','wind-cyclone':'Charged core cyclones','wing-storm':'Wing-flap tornado sweep','pass':'Rolling flyby','shear':'Wind shear','vortex':'Tornado','gates':'Tornado gates','rail':'Electric fronts','eye':'Hurricane reactor','storm-cyclone':'Core cyclone salvo','storm-tornado':'Twin tornadoes','storm-thunder':'Targeted thunderstorm','storm-tempest':'Giant core lightning storm'}
 for t in report['timeline']:
  tempest=t.get('tempest')
  if id=='razorwake'and tempest:
   state=tempest.get('state');label={'roll-exit':'Rolling forward gun runs','burst-move':'Center / right / left burst lanes','dive-warn':'Charged south dive','throttle-run':'Accelerating up/down throttle runs','orb-charge':'Storm Helix charge and lightning','orb-flight':'Expanding storm orb'}.get(state)
   if label and state not in seen:chapters.append({'label':label,'time':max(0,t['seconds']-.4)});seen.add(state)
   for e in tempest.get('events',[]):
    if e['event']=='orb-break'and'orb-break'not in seen:chapters.append({'label':'Break orb into nine wind balls','time':max(0,t['seconds']-.5)});seen.add('orb-break')
  reactor=t.get('reactor')
  if id=='thunderhead'and reactor:
   state=reactor.get('flow');label={'turn-north':'Turn north and leave the foreground','far-charge':'Distant chamber charge and lightning','recoil':'Cyclone launch and kickback','foreground-return':'Return to the foreground'}.get(state)
   if label and state not in seen:chapters.append({'label':label,'time':max(0,t['seconds']-.35)});seen.add(state)
   for e in reactor.get('events',[]):
    key=e['event'];label={'target-assignment':'Coordinated ally / player targeting','module-breakaway':'Complete module breaks away and explodes'}.get(key)
    if label and key not in seen:chapters.append({'label':label,'time':max(0,t['seconds']-.5)});seen.add(key)
  storm=t.get('storm')
  if storm:
   if id=='razorwake':
    for event in storm.get('events',[]):
     key=event.get('event');label=None
     if key=='razor-charge' and storm.get('attack')=='wing-storm':key='wing-charge';label='Warning and accelerating wing flaps'
     elif key=='razor-gun-detach':label='Complete gun detaches; wing remains intact'
     if label and key not in seen:chapters.append({'label':label,'time':max(0,t['seconds']-.5)});seen.add(key)
   if id=='thunderhead':
    for event in storm.get('events',[]):
     key=event.get('event')
     label={'modular-core-charge':'Reactor and full-body charge','modular-wind-beam':'Giant wind cannon beams'}.get(key)
     if label and key not in seen:chapters.append({'label':label,'time':max(0,t['seconds']-.5)});seen.add(key)
   attack=storm.get('attack')
   if storm.get('phase')=='attack'and attack in labels and attack not in seen:chapters.append({'label':labels[attack],'time':max(0,t['seconds']-1)});seen.add(attack)
   if storm.get('open')and'core'not in seen:chapters.append({'label':'Core exposed','time':max(0,t['seconds']-1)});seen.add('core')
  tandem=t.get('tandem')
  if id=='sumpjaw'and tandem:
   state=tandem.get('mode');label={'hop':'Repeated airborne left/right jumps','row-form':'Pair into a firing row','row-charge':'Inner-mouth toxic charge','row-fire':'Strafing dual large-orb bursts','split':'Split apart and hop north','cross':'Over / under crossing return','return':'Return to the fight'}.get(state)
   if label and state not in seen:chapters.append({'label':label,'time':max(0,t['seconds']-.25)});seen.add(state)
   for event in tandem.get('events',[]):
    if event['event']=='snake-defeat'and'single-survivor'not in seen:chapters.append({'label':'One snake / half of the shared bar remains','time':max(0,t['seconds']-.5)});seen.add('single-survivor')
  sump=t.get('sumpjaw')
  if sump:
   for e in sump.get('events',[]):
    key=None;label=None
    if e['event']=='release':
     key=e.get('kind');label={'breach':'Breach attack','lob':'Toxic mortar lobs','bite':'Bite lunge','leap':'Airborne pounce over the pilot','orb':'Giant toxic orb volley','acid':'Rapid acid spit volley','coil':'Coiling serpent attack','leap':'Airborne pounce over the pilot','orb':'Giant toxic orb volley','acid':'Rapid acid spit volley','coil':'Coiling serpent attack'}.get(key)
    elif e['event']=='actor-defeat':key='first-defeat';label='First Sumpjaw defeated'
    elif e['event']=='part-break'and e.get('part')in['gillL','gillR']:key='gill-break';label='Gill rupture'
    if label and key not in seen:chapters.append({'label':label,'time':max(0,t['seconds']-2)});seen.add(key)
 chapters.append({'label':'Defeat & aftermath','time':max(0,report['defeatSeconds']-4)})
 chapters.sort(key=lambda c:c['time'])
 sha=hashlib.sha256(file.read_bytes()).hexdigest();routes[f'/media/{id}.mp4']=str(file)
 clips.append(dict(id=id,name=name,slot=slot,description=description,url=f'/media/{id}.mp4',poster=f'/posters/{id}.png',duration=job['seconds'],nativeFps=round(job['nativeFps'],1),width=960 if job.get('view')=='playfield'else 1280,height=1024 if job.get('view')=='playfield'else 800,peakDb=job['peakDb'],chapters=chapters,sha256=sha,bytes=file.stat().st_size))
 if id=='razorwake':
  deathBatch=R/'_shots/boss_comparison_1102/razorwake-vortex-final-1105/batch.json'
  if deathBatch.exists():
   dj=json.loads(deathBatch.read_text())['jobs'].get('stage6-mini',{});df=R/dj.get('folder','')/'vortex-death.mp4'
   if dj.get('passed')and df.is_file():
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(df)],text=True));routes['/media/razorwake-vortex-death.mp4']=str(df);clips[-1]['death']={'url':'/media/razorwake-vortex-death.mp4','seconds':dur,'sha256':hashlib.sha256(df.read_bytes()).hexdigest(),'bytes':df.stat().st_size,'method':'Natural first orb; GOD switched off on release; native capture, airborne throw, burning fall and crash.'}
 reports.append(dict(id=id,name=name,seconds=job['seconds'],checks=job['checks'],nativeFps=job['nativeFps'],peakDb=job['peakDb'],sourceStable=report['sourceStable'],god=report['audio'].get('god'),deaths=report['audio'].get('deaths'),sha256=sha))
(W/'routes.json').write_text(json.dumps(routes,indent=2));(W/'manifest.json').write_text(json.dumps(clips,indent=2))
(W/'report.json').write_text(json.dumps(dict(baseSourceCommit='7dff42bca92856552d357db3fcab89d64941d27f',localRevision='sumpjaw-tandem-final-1105',method='Fresh real-RAF Furious encounters; native GOD and input-only Cole bot; native health, modules, attack clocks, audio and defeat. Thunderhead uses 70 seconds player hold-fire, direct high-quality native-canvas H264 capture and the connected beam throats, coordinated batteries, animated chamber and background cyclone launch. Sumpjaw uses 60 seconds and Razorwake 60 seconds of player hold-fire. Razorwake demonstrates rolling forward gun runs, three burst lanes, accelerating throttle passes, a lightning charge and the wind Helix orb; its native solo guard keeps NPC allies out. Other native ally owners remain active. No enemy HP/phase/timer writes after spawn.',films=reports,limits='Capture performance is included in reported engine FPS. These are isolated encounter recordings, not a human-dodgeability or complete campaign test.'),indent=2))
(W/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOF Â· New Furious bosses</title>
<style>*{box-sizing:border-box}body{margin:0;background:#07111c;color:#e7f4fa;font:17px/1.5 system-ui,sans-serif}main{max-width:1320px;margin:auto;padding:28px}h1{font-size:clamp(28px,4vw,44px);line-height:1.1;margin:8px 0 16px}h2{margin:0}p{color:#b6cddc}.tag{color:#71e6ed;font-size:13px;font-weight:800;letter-spacing:2px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:24px 0}.card{border:1px solid #365069;background:#101e2d;color:inherit;padding:0;text-align:left;font:inherit;cursor:pointer}.card[aria-pressed=true]{border:3px solid #70e8ed}.card img{display:block;width:100%;aspect-ratio:1.6;object-fit:contain;background:#02070c}.card .info{display:block;padding:12px}.card strong,.card small{display:block}.card small{color:#b2cadb}video{display:block;width:100%;max-height:78vh;background:#000;margin:15px 0}button:focus-visible,a:focus-visible{outline:3px solid #ffdf82;outline-offset:4px}.chapters{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0 22px}.chapters button{font:inherit;background:#142b3c;color:#d9f5ff;border:1px solid #507082;padding:9px 13px;cursor:pointer}a{color:#82e6f1}details{border-top:1px solid #365069;margin-top:26px;padding:18px 0}summary{cursor:pointer}.note{color:#f1d58d}#status{font-size:14px;color:#9ebacc}@media(max-width:700px){main{padding:18px}.cards{grid-template-columns:1fr}.card{display:flex;align-items:center}.card img{width:38%}video{max-height:none}.card .info{flex:1}}</style>
<main><div class="tag">BULLETS OF FURY / NOVEMBER 5</div><h1>The new Furious encounters</h1><p>The latest complete recordings for these revised encounters, captured in the actual game engine. Cole is controlled by an <strong>invulnerable input bot</strong>. Native health, attack patterns, module destruction and game audio remain active. Thunderhead demonstrates attacks for 70 seconds; Sumpjaw for 60 seconds and Razorwake for 60 seconds before the pilot fires. Razorwake is a solo encounter with no NPC allies. Thunderhead uses the native game canvas, including its boss health bar; cabinet side panels are outside this recording.</p><nav class="cards" aria-label="Choose a fight" id="cards"></nav><section aria-label="Selected video"><div class="tag" id="slot"></div><h2 id="title"></h2><p id="description"></p><video id="movie" controls playsinline preload="metadata"></video><div id="status" aria-live="polite"></div><div class="chapters" id="chapters" aria-label="Attack shortcuts"></div><p><a id="download" download>Download this video</a> Â· <a href="/report.json">Recording checks and notes</a></p></section><section id="vortex-demo" hidden><h2>Razorwake Â· exclusive vortex crash</h2><p>First natural storm orb. GOD is switched off when it releases; the pilot holds fire. Native capture, airborne throw, burning fall and crash, with game audio.</p><video id="vortex-video" controls playsinline preload="metadata"></video></section><details><summary>Recording performance and verification</summary><p>All three encounters completed through native defeat; full video/audio decoding, source stability and browser-error checks passed. No enemy HP, phase or attack-timer values were changed after spawn.</p><p class="note">All three fights now have fresh recordings of their revised encounters; actual engine FPS is shown above. The regenerated kit, actual hit pixels, cannon warning lanes, beam cancellation and native defeat have been checked in the game. Capture is 30 FPS; the displayed averages measure the actual engine. This is an encounter showcase, not a full campaign or human dodgeability test.</p></details></main>
<script>let clips=[],active=null;const video=document.querySelector('#movie');function stamp(s){return Math.floor(s/60)+':'+String(Math.floor(s%60)).padStart(2,'0')}function select(id,seek=0){const c=clips.find(c=>c.id===id)||clips[0];active=c;const demo=document.querySelector('#vortex-demo'),death=document.querySelector('#vortex-video');death.pause();demo.hidden=!c.death;if(c.death)death.src=c.death.url;else{death.removeAttribute('src');death.load()}video.pause();video.src=c.url;video.poster=c.poster;document.querySelector('#slot').textContent=c.slot;document.querySelector('#title').textContent=c.name;document.querySelector('#description').textContent=c.description;document.querySelector('#download').href=c.url;document.querySelector('#status').textContent=stamp(c.duration)+' Â· FURIOUS Â· COLE / GOD BOT Â· '+c.nativeFps+' captured engine FPS';document.querySelectorAll('.card').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.id===c.id)));const list=document.querySelector('#chapters');list.replaceChildren();for(const ch of c.chapters){const b=document.createElement('button');b.textContent=stamp(ch.time)+' '+ch.label;b.onclick=()=>{video.currentTime=ch.time;video.play().catch(()=>{})};list.append(b)}if(seek)video.addEventListener('loadedmetadata',()=>video.currentTime=seek,{once:true});history.replaceState(null,'','#'+c.id)}fetch('/manifest.json').then(r=>r.json()).then(data=>{clips=data;const cards=document.querySelector('#cards');for(const c of clips){const b=document.createElement('button');b.className='card';b.dataset.id=c.id;b.setAttribute('aria-pressed','false');const img=document.createElement('img');img.src=c.poster;img.alt=c.name+' in the actual game';const box=document.createElement('span');box.className='info';const title=document.createElement('strong');title.textContent=c.name;const sub=document.createElement('small');sub.textContent=c.slot+' Â· '+stamp(c.duration);box.append(title,sub);b.append(img,box);b.onclick=()=>select(c.id);cards.append(b)}select(location.hash.slice(1)||clips[0].id)});</script></html>''',encoding='utf8')
print('Prepared',len(clips),'verified videos and chapter shortcuts.')
