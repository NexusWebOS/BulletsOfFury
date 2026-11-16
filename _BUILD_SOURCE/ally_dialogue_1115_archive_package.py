from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.request import Request,urlopen
import imageio_ffmpeg,json,subprocess,re,hashlib,html
R=Path(__file__).resolve().parents[1];O=R/'_shots/ally_dialogue_1115';A=O/'archive';FF=imageio_ffmpeg.get_ffmpeg_exe();q=json.loads((A/'recording.json').read_text(encoding='utf8'));checks=[];errors=[]
def ck(n,v,data=None):checks.append({'name':n,'ok':bool(v),'data':data})
def ff(args):
 p=subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*map(str,args)],capture_output=True,text=True);assert p.returncode==0 and not p.stderr,p.stderr
def duration(path):
 p=subprocess.run([FF,'-hide_banner','-i',str(path)],capture_output=True,text=True);m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',p.stderr);assert m,p.stderr;return int(m[1])*3600+int(m[2])*60+float(m[3])
def tc(t):return str(int(t)//60)+':'+str(int(t)%60).zfill(2)
ck('six rehearsals completed without page errors',len(q['clips'])==6 and all(c['completed']and c['peak']>.001 for c in q['clips'])and not q['errors']);ck('shipping unchanged',q['before']==q['after'])
files=[];chapters=[];lines=[];time=0
for c in q['clips']:
 plan=c['plan'];key=plan['key'];p=A/(key+'.mp4');files.append(p);print('ENCODING '+key,flush=True)
 ff(['-i',A/'films'/(key+'.webm'),'-vf','fps=30','-fps_mode','cfr','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-threads','2','-af','aresample=async=1:first_pts=0','-ar','48000','-c:a','aac','-b:a','160k',p]);d=duration(p);start=time;time+=d;chapters.append({'key':key,'title':plan['title'],'start':start,'duration':d,'pilot':plan['pilot']})
 ck('exact retained script '+key,[r['text']for r in c['rows']]==[r['text']for r in plan['original']])
 ck('all dialogue rendered in order '+key,[r['id']for r in c['rows']]==[s['tag']for s in c['stages']if s['tag']!='end'])
 faces=[f for r in c['receipts']for f in r['faces']];ck('current row-B cockpit artwork '+key,bool(faces)and all(f.get('artFamily')=='castB-1115'and not f.get('loading')for f in faces))
 for row in c['rows']:
  at=start+next(s['at']for s in c['stages']if s['tag']==row['id']);lines.append({'pilot':plan['pilot'],'chapter':key,'shot':row['id'],'speaker':row['who'],'text':row['text'],'start':at})
concat=A/'clips.ffconcat';concat.write_text('ffconcat version 1.0\n'+''.join("file '"+p.name+"'\n"for p in files),encoding='utf8');meta=';FFMETADATA1\ntitle=BOF - Archived duo dialogue rehearsal - not campaign routing\n'
for i,c in enumerate(chapters):meta+='[CHAPTER]\nTIMEBASE=1/1000\nSTART='+str(round(c['start']*1000))+'\nEND='+str(round((chapters[i+1]['start']if i+1<len(chapters)else time)*1000))+'\ntitle=ARCHIVE REHEARSAL - '+c['title'].replace('&','and')+'\n'
(A/'chapters.ffmeta').write_text(meta,encoding='utf8');movie=O/'archived-duo-rehearsal.mp4';ff(['-safe','0','-f','concat','-i',concat,'-f','ffmetadata','-i',A/'chapters.ffmeta','-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',movie]);ff(['-i',movie,'-f','null','-']);ck('complete archive H264/AAC decode',True)
text='# Archived duo openings — native dialogue rehearsals\n\nThese are exact retained PILOT_OPENINGS words and casts staged for review with the current talking cockpits and native text/audio clocks. The old flight action is not recreated. They do not currently play through the Fury crawl/jungle intro and this review does not reconnect them.\n\n'
for c in chapters:
 text+='## '+tc(c['start'])+' — '+c['title']+'\n\n'
 for r in [r for r in lines if r['chapter']==c['key']]:text+='['+tc(r['start'])+'] '+r['speaker']+': '+r['text']+'\n\n'
(A/'transcript.md').write_text(text,encoding='utf8');(A/'transcript.json').write_text(json.dumps({'chapters':chapters,'lines':lines},indent=2),encoding='utf8')
buttons=''.join('<button class="archive-chapter" data-archive-time="'+str(c['start'])+'">'+tc(c['start'])+' '+html.escape(c['title'])+'</button>'for c in chapters)
section='<h2 id="archive-rehearsal">Archived duo openings — dialogue rehearsals</h2><p>These are the six pilot-specific duo scripts retained from the earlier openings. Their exact words are rehearsed here with current talking-cockpit art and native letter audio. The older flight actions are not recreated, and the current campaign intro is unchanged.</p><video id="archive-sequence" controls preload="metadata" poster="archive/archive-falva-01.png" src="archived-duo-rehearsal.mp4"></video><div>'+buttons+'</div><p><a href="archive/transcript.md">Timecoded archive rehearsal transcript</a></p><h2>Retained opening scripts</h2>'
page=(O/'review.html').read_text(encoding='utf8');assert '<h2>Inactive legacy duo openings</h2>'in page;page=page.replace('<h2>Inactive legacy duo openings</h2>',section,1)
rehearsal=section.rsplit('<h2>Retained opening scripts</h2>',1)[0];page=page.replace(section,'<h2>Retained opening scripts</h2>',1);page=page.replace('<h2>Notes for the dialogue wrap</h2>',rehearsal+'<h2>Notes for the dialogue wrap</h2>',1)
page=page.replace('</body>','') if '</body>'in page else page
page=page.replace('</html>','<script>document.querySelectorAll("[data-archive-time]").forEach(b=>b.onclick=async()=>{document.getElementById("sequence").pause();const v=document.getElementById("archive-sequence");v.currentTime=Number(b.dataset.archiveTime);try{await v.play()}catch(e){if(e.name!=="AbortError")throw e}});document.getElementById("sequence").addEventListener("play",()=>document.getElementById("archive-sequence").pause());document.getElementById("archive-sequence").addEventListener("play",()=>document.getElementById("sequence").pause());</script></html>');(O/'review.html').write_text(page,encoding='utf8')
url='http://127.0.0.1:8766/_shots/ally_dialogue_1115/'
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1320,'height':1000});p.set_default_timeout(30000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto(url+'review.html');p.wait_for_function('document.getElementById("archive-sequence").readyState>=1');qv=p.evaluate('()=>{const v=document.getElementById("archive-sequence");return{w:v.videoWidth,h:v.videoHeight,d:v.duration}}');ck('archive dimensions and duration',qv['w']==1824 and qv['h']==1024 and abs(qv['d']-time)<1,qv)
 p.evaluate('async()=>{window.arcAC=new AudioContext();await arcAC.resume();window.arcAnal=arcAC.createAnalyser();arcAC.createMediaElementSource(document.getElementById("archive-sequence")).connect(arcAnal);arcAnal.connect(arcAC.destination)}');peak=0
 for i,c in enumerate(chapters):
  p.locator('button.archive-chapter').nth(i).click();p.wait_for_function('t=>{const v=document.getElementById("archive-sequence");return !v.paused&&!v.seeking&&Math.abs(v.currentTime-t)<1.5}',arg=c['start']);t=p.evaluate('async()=>await new Promise(r=>document.getElementById("archive-sequence").requestVideoFrameCallback((_,m)=>r(m.mediaTime)))');ck('archive chapter decodes '+c['key'],abs(t-c['start'])<1.6,t)
  v=p.evaluate('async()=>{const a=new Float32Array(arcAnal.fftSize);let peak=0;for(let i=0;i<8;i++){await new Promise(r=>setTimeout(r,25));arcAnal.getFloatTimeDomainData(a);for(const v of a)peak=Math.max(peak,Math.abs(v))}return peak}');peak=max(peak,v)
 ck('native archive audio decodes in browser',peak>.001,peak)
 p.locator('button.chapter').nth(0).click();p.wait_for_function('()=>!document.getElementById("sequence").paused&&document.getElementById("archive-sequence").paused');ck('two reels prevent overlapping audio',True)
 p.evaluate('document.querySelectorAll("video").forEach(v=>v.pause());scrollTo(0,0)');p.screenshot(path=str(O/'browser-review-final.png'));ck('combined review page has no errors',not errors,errors);b.close()
with urlopen(Request(url+movie.name,headers={'Range':'bytes=0-255'}))as r:ck('archive range seeking206',r.status==206 and len(r.read())==256)
ck('source hashes remain unchanged',all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in q['before'].items()))
result={'checks':checks,'errors':errors,'movie':{'file':movie.name,'duration':duration(movie),'chapters':chapters,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest()},'lines':len(lines),'scope':q['scope']};(A/'qa.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps({'duration':result['movie']['duration'],'lines':len(lines),'chapters':len(chapters),'passed':sum(c['ok']for c in checks),'checks':len(checks)},indent=2));assert all(c['ok']for c in checks)
