from pathlib import Path
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from urllib.request import Request,urlopen
import subprocess,json,re,hashlib,html
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];O=R/'_shots/city_style_1115';FF=imageio_ffmpeg.get_ffmpeg_exe()
q=json.loads((O/'recording.json').read_text(encoding='utf8'));c=q['clips'][0];assert c['part']=='city'and not q['errors']and q['coreBefore']==q['coreAfter']
checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append({'name':name,'ok':bool(ok),'data':data})
 if not ok:print('FAIL',name,str(data)[:900],flush=True)
def ff(args):
 p=subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*map(str,args)],capture_output=True,text=True);assert p.returncode==0 and not p.stderr,p.stderr
def event(contains):return next(s['at']for s in c['stages']if contains in s['tag'])
chapters=[(0,'City rescued: another win'),(event(':CITY16-02:'),'Back to the riverbank'),(event(':CITY16-03:'),'Is it going to smell bad?'),(event(':CITY16-05:'),'A favorite album'),(event(':CITY16-ALBUM:'),'Bulletalica'),(event(':::chibi-flight:'),'Flight to Stage7'),(event(':::stage7-ready:'),'Stage7 selection'),(event('intro:'),'Stage7 card'),(event(':stage7-approach:A701:'),'Approaching the riverbank'),(event(':stage7-approach:ARRIVAL7-02:'),'The sewer entrance')]
for needle,title in [(':7:run','Fly into the sewer'),(':7:cd','Ready for Stage7')]:
 if any(needle in s['tag']for s in c['stages']):chapters.append((event(needle),title))
chapters=[{'start':t,'title':name}for t,name in sorted(chapters)]
for i in range(1,7):ck('recorded full city dialogue '+str(i),any(':CITY16-'+str(i).zfill(2)+':'in s['tag']for s in c['stages']))
ck('latest Bulletalica image was installed during capture',q['coreBefore']['assets/city_rescue_art_1115.js']==hashlib.sha256((R/'assets/city_rescue_art_1115.js').read_bytes()).hexdigest())
ck('native chibi flight and manual selection reach real7',c['end']['state']=='play'and c['end']['stage']==7 and c['end']['city']['travelSeen']and c['end']['city']['debriefSeen']and c['end']['brief'],c['end'])
speeches=c.get('faceSamples',[])
ck('recorded album request is spoken by Juggernaut',any(v['who']=='JUGGERNAUT'and 'favorite albums'in v['text']for v in speeches),speeches)
faces=[f for v in speeches for f in v.get('faces',[])]
ck('every recorded comic face uses the current cockpit family',len(faces)>6 and all(f.get('family')=='talking-cockpit'and f.get('key')=='cp15_'+f['pilot']and not f.get('loading')for f in faces),faces)
ck('recorded sewer approach uses current Decker cockpit',any('stage7-approach:A701:'in v['tag']and any(f.get('key')=='cp15_decker'for f in v.get('faces',[]))for v in speeches),speeches)
encoded=O/'stagex-to-stage7-encoded.mp4';movie=O/'stagex-to-stage7-full.mp4'
ff(['-i',O/'films/city.webm','-vf','fps=30','-fps_mode','cfr','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-threads','2','-af','aresample=async=1:first_pts=0','-c:a','aac','-b:a','160k',encoded])
p=subprocess.run([FF,'-hide_banner','-i',str(encoded)],capture_output=True,text=True);m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',p.stderr);duration=int(m[1])*3600+int(m[2])*60+float(m[3])
meta=';FFMETADATA1\ntitle=Bullets of Fury - Stage X to Stage7\n'
for i,ch in enumerate(chapters):
 end=chapters[i+1]['start']if i+1<len(chapters)else duration;assert ch['start']<end<=duration+.2
 meta+='[CHAPTER]\nTIMEBASE=1/1000\nSTART='+str(round(ch['start']*1000))+'\nEND='+str(round(end*1000))+'\ntitle='+ch['title']+'\n'
(O/'chapters.ffmeta').write_text(meta,encoding='utf8');ff(['-i',encoded,'-f','ffmetadata','-i',O/'chapters.ffmeta','-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',movie]);ff(['-i',movie,'-f','null','-']);ck('full H264/AAC movie decodes without errors',True)
p=subprocess.run([FF,'-hide_banner','-i',str(movie),'-af','volumedetect','-vn','-f','null','-'],capture_output=True,text=True);audio=[s.strip()for s in p.stderr.splitlines()if'mean_volume:'in s or'max_volume:'in s];ck('recorded native audio is audible',len(audio)==2 and not any('-inf'in s for s in audio),audio)
points=[(event(':CITY16-02:')+2,'Decker and Cole'),(event(':CITY16-ALBUM:')+1,'Bulletalica'),(event(':::chibi-flight:')+1.5,'Map flight'),(event(':stage7-approach:A701:')+1.5,'Riverbank approach'),(event(':stage7-approach:ARRIVAL7-02:')+1,'Sewer briefing'),(event(':7:run')+3,'Entering the sewer')]
contact=Image.new('RGB',(1280,1152),'#102030');draw=ImageDraw.Draw(contact)
for i,(t,label)in enumerate(points):
 path=O/('frame-'+str(i)+'.png');ff(['-ss',t,'-i',movie,'-frames:v','1',path]);im=Image.open(path).convert('RGB');im.thumbnail((640,360),Image.Resampling.NEAREST);x=i%2*640;y=i//2*384;contact.paste(im,(x,y));draw.text((x+10,y+362),label,fill='white')
contact.save(O/'contact.jpg',quality=95)
buttons=''.join('<button data-time="'+str(ch['start'])+'">'+html.escape(ch['title'])+'</button>'for ch in chapters)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOF Stage X to Stage7</title><style>body{max-width:1200px;margin:24px auto;padding:0 20px;background:#0c1723;color:#f1e9d7;font:17px/1.6 system-ui}video,img{width:100%;background:#000}button{padding:9px;margin:4px;background:#253d51;color:#fff;border:1px solid #668ba5;border-radius:4px;cursor:pointer}a{color:#8fe3d0}.scope{color:#a9bfd0;font-size:15px}</style><h1>Stage X → Stage7</h1><p>Juggernaut owns the album joke. All airborne dialogue uses the current matching talking-cockpit family, including Decker at the sewer approach. Full native dialogue, Bulletalica, map flight and Stage7 entrance with game audio.</p><video id="sequence" controls preload="metadata" poster="frame-0.png" src="stagex-to-stage7-full.mp4"></video><p>__BUTTONS__</p><p class="scope">Prepared Cole/Furious city-victory checkpoint, not an unassisted campaign win. The real city Harrier/Nightwing and terminal result owners run before the recording; all dialogue and transitions then play at their native pace.</p><h2>Selected-card overlay</h2><img src="../pursuit_overlay_1115/pursuit-highlights.gif" alt="The approved traced card and interior pulsing in matching color"><p><a href="../../docs/CITY_STYLE_1115.md">Recording and verification</a></p><script>document.querySelectorAll('button').forEach(b=>b.onclick=async()=>{const v=document.getElementById('sequence');v.currentTime=Number(b.dataset.time);try{await v.play()}catch(e){if(e.name!=='AbortError')throw e}});</script></html>'''
(O/'review.html').write_text(page.replace('__BUTTONS__',buttons),encoding='utf8')
url='http://127.0.0.1:8766/_shots/city_style_1115/'
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(30000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto(url+'review.html');p.wait_for_function('document.querySelector("video").readyState>=1')
 info=p.evaluate('()=>{const v=document.querySelector("video");return{w:v.videoWidth,h:v.videoHeight,duration:v.duration}}');ck('browser movie geometry/duration',info['w']==1824 and info['h']==1024 and abs(info['duration']-duration)<.2,info)
 p.evaluate('async()=>{window.qaAC=new AudioContext();await qaAC.resume();window.qaAnal=qaAC.createAnalyser();qaAnal.fftSize=2048;qaAC.createMediaElementSource(document.querySelector("video")).connect(qaAnal);qaAnal.connect(qaAC.destination)}');peak=0
 for ch in chapters:
  p.locator('button').filter(has_text=ch['title']).click();p.wait_for_function('t=>{const v=document.querySelector("video");return Math.abs(v.currentTime-t)<1.5&&!v.paused&&!v.seeking}',arg=ch['start'])
  t=p.evaluate('async()=>await new Promise(r=>document.querySelector("video").requestVideoFrameCallback((_,m)=>r(m.mediaTime)))');ck('browser decoded chapter: '+ch['title'],abs(t-ch['start'])<2,t)
  a=p.evaluate('async()=>{const b=new Float32Array(2048);let peak=0;for(let i=0;i<10;i++){await new Promise(r=>setTimeout(r,25));qaAnal.getFloatTimeDomainData(b);for(const v of b)peak=Math.max(peak,Math.abs(v))}return peak}');peak=max(peak,a)
 ck('browser decoded game audio',peak>.001,peak);p.evaluate('document.querySelector("video").pause()');p.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth)');p.screenshot(path=str(O/'browser-preview.png'),full_page=True);b.close()
with urlopen(Request(url+movie.name,headers={'Range':'bytes=0-255'}))as r:ck('byte-range seeking works',r.status==206 and len(r.read())==256)
ck('recording and review have no page/console/HTTP errors',not errors and not q['errors'],errors)
ck('capture source hashes still match the installed build',all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in q['coreAfter'].items()))
q['movie']={'file':movie.name,'duration':duration,'chapters':chapters,'audio':audio,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'size':[1824,1024],'fps':30};q['checks']=checks;q['browserErrors']=errors;(O/'recording.json').write_text(json.dumps(q,indent=2),encoding='utf8')
print(json.dumps({'movie':q['movie'],'passed':sum(v['ok']for v in checks),'checks':len(checks)},indent=2));assert all(v['ok']for v in checks)
