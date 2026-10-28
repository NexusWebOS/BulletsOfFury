from pathlib import Path
import json, html, subprocess, re, imageio_ffmpeg, os
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parent;O=Path(os.environ.get('BOF_CAPTURE_DIR',str(W/'review')));jobs=json.loads((W/'jobs.json').read_text());ff=imageio_ffmpeg.get_ffmpeg_exe()
names={'s05_boss_chromehammer':'CHRONOS','s06_boss_warhive':'WARHIVE HARRIER','s08_boss_vileexistence':'DRACODIA — COMPLETE ENCOUNTER','s06_mini_siegefortress17':'SIEGE FORTRESS','s08_mini_heralddeath':'HERALD OF DEATH','s09_boss_tidalfusion':'WARP SENTINELS'}
cards=[];coverage=[];thumbs=[]
for j in jobs:
 slug=j['id'];p=O/(slug+'.json');q=json.loads(p.read_text())if p.exists()else{};done=q.get('completed')and q.get('reason')=='native-defeat'and not any(e.get('type')=='diagnostic-engine-update'for e in q.get('events',[]));raw=O/(slug+'.webm');video=O/(slug+'-seek.webm');name=names.get(slug,j['name'])
 if done and raw.exists()and(not video.exists()or video.stat().st_mtime<raw.stat().st_mtime):
  r=subprocess.run([ff,'-v','error','-y','-i',str(raw),'-map','0','-c','copy',str(video)],capture_output=True,text=True)
  if r.returncode:print('REMUX ERROR',slug,r.stderr[-600:])
 shots=sorted(O.glob(slug+'-*.png'));shots=[p for p in shots if re.search(r'-\d{4}\.png$',p.name)]
 spawn=next((e['t']for e in q.get('events',[])if e.get('type')=='native-spawn'),0)
 defeat=next((e['t']for e in q.get('events',[])if e.get('type')=='native-defeat'),q.get('elapsed',40))
 mid=(spawn+defeat)/2
 shot=min(shots,key=lambda p:abs(int(re.search(r'-(\d{4})\.png$',p.name)[1])-mid))if shots else None
 if done and video.exists():
  shot=O/(slug+'-frame.png')
  if not shot.exists()or shot.stat().st_mtime<video.stat().st_mtime:subprocess.run([ff,'-v','error','-y','-ss',str(max(.3,min(mid,q.get('elapsed',10)-2))),'-i',str(video),'-frames:v','1',str(shot)],capture_output=True)
  if not shot.exists():shot=None
 thumb=O/(slug+'-thumb.jpg')
 if shot:
  im=Image.open(shot).convert('RGB');im.thumbnail((640,360));im.save(thumb,quality=90)
  if done:thumbs.append((name,im.copy()))
 e={'id':slug,'name':name,'stage':'X'if j.get('stageX')else j['stage'],'role':j['role'],'complete':bool(done),'seconds':q.get('elapsed'),'reason':q.get('reason'),'nativeFPS':q.get('fps'),'pageErrors':q.get('pageErrors',[]),'assetErrors':q.get('assetErrors',[]),'protectedContacts':q.get('stats',{}).get('protectedContacts'),'file':video.name if done else None}
 coverage.append(e)
 status='RECORDED THROUGH NATIVE DEFEAT'if done else 'CAPTURE PENDING'
 if q and not done:status='RETRY / '+str(q.get('reason','INCOMPLETE')).upper()
 duration=f"{int(q.get('elapsed',0))//60}:{int(q.get('elapsed',0))%60:02}"
 controls=f'<video controls preload="none" poster="{thumb.name if thumb.exists()else ""}" src="{video.name}"></video>'if done else f'<img src="{thumb.name}" alt="Live capture preview">'if thumb.exists()else '<div class="empty">Waiting for full encounter</div>'
 details=f'<a href="{slug}.json">Run report</a> · <a download href="{video.name}">Download video</a>'if done else ''
 cards.append(f'<article data-done="{int(bool(done))}" data-group="{j["role"]}"><div class="tag">STAGE {e["stage"]} / {j["role"].upper()} / FURIOUS</div><h2>{html.escape(name)}</h2>{controls}<p class="status">{status} {"· "+duration if done else ""}</p><p>{details}</p></article>')
done=sum(c['complete']for c in coverage)
(O/'coverage.json').write_text(json.dumps({'complete':done,'total':len(jobs),'encounters':coverage},indent=2),encoding='utf-8')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOF · Furious fight recordings</title><style>
*{box-sizing:border-box}body{margin:0;background:#070b12;color:#edf3fa;font:16px system-ui,sans-serif}header,main{max-width:1500px;margin:auto;padding:28px}header{border-bottom:1px solid #394759}h1{font-size:34px;margin:6px 0 12px}p{line-height:1.6;color:#b9c8d8}a{color:#7cdcff}button{background:#172537;color:#e9f5ff;border:1px solid #4c6680;padding:10px 18px;margin:4px;cursor:pointer}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,520px),1fr));gap:24px}article{background:#101925;padding:18px;border:1px solid #334659}h2{font-size:22px;margin:8px 0 18px}.tag{color:#80d6e9;font-size:13px;letter-spacing:1px}video,article img{width:100%;aspect-ratio:16/9;background:black;object-fit:contain}.status{font-weight:700;color:#f7cf7b;font-size:13px}.empty{height:180px;display:grid;place-items:center;background:#080f18;color:#8296a9}.count{font-size:22px;color:#9be39c}nav{margin-top:18px}footer{padding:30px;color:#a0b1c3}small{color:#94a5b7}
</style><header><div class="tag">BULLETS OF FURY / LIVE ENGINE REVIEW</div><h1>Furious: every boss and miniboss</h1><div class="count">COUNT</div><p>Real running game footage with native graphics, music, sound, warnings, combat and death sequences. Cole is controlled by an invulnerable test bot with delayed reactions, normal movement, firing, Retina missiles, rolls and somersaults. Enemy health and attack rules are unchanged. No forced damage or phase jumps.</p><p>Each encounter starts through the native isolated fight launcher or its native route. Disclosed starting loadout: primary level 3, space weapons level 3 where applicable, speed 2 and auto-missiles level 1. Pickups and subsequent weapon changes are native. The bot is a playtest driver, not a balance benchmark.</p><nav><button onclick="filter('all')">All encounters</button><button onclick="filter('complete')">Completed videos</button><button onclick="filter('boss')">Main / route bosses</button><button onclick="filter('mini')">Minibosses</button><button onclick="location.reload()">Refresh progress</button></nav></header><main><div class="grid">CARDS</div><footer>Saved locally · October 23, 2026 · <a href="coverage.json">Coverage report</a><br><small>Original capture files and per-run input/phase logs are retained. Some native optional online-service requests may fail when the local score service is unavailable; these are listed in the reports separately from missing game assets.</small></footer></main><script>function filter(v){document.querySelectorAll('article').forEach(a=>a.hidden=!(v==='all'||v==='complete'&&a.dataset.done==='1'||v===a.dataset.group));}document.querySelectorAll('video').forEach(v=>v.addEventListener('play',()=>document.querySelectorAll('video').forEach(o=>{if(o!==v)o.pause()})));</script></html>'''
page=page.replace('Starting loadout:', 'Starting loadout:').replace('primary level 3, space weapons level 3 where applicable, speed 2 and auto-missiles level 1.','primary level 3 (basic level 1 for the three small arsenal elites), space weapons level 3 where applicable, speed 2 and auto-missiles level 1.')
(O/'index.html').write_text(page.replace('COUNT',f'{done} / {len(jobs)} complete').replace('CARDS','\n'.join(cards)),encoding='utf-8')
if thumbs:
 cols=3;cw,ch=426,274;sheet=Image.new('RGB',(cols*cw,((len(thumbs)+cols-1)//cols)*ch),'#080e17');d=ImageDraw.Draw(sheet)
 for i,(name,im)in enumerate(thumbs):
  x=(i%cols)*cw;y=(i//cols)*ch;im.thumbnail((420,236));sheet.paste(im,(x,y));d.text((x+6,y+242),name[:49],fill='#daefff')
 sheet.save(O/'contact-sheet.jpg',quality=91)
print(f'{done}/{len(jobs)} complete; gallery refreshed',flush=True)
