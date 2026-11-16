from pathlib import Path
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from urllib.request import urlopen,Request
import imageio_ffmpeg,json,subprocess,re,hashlib,html,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/ally_dialogue_1115';FF=imageio_ffmpeg.get_ffmpeg_exe();q=json.loads((O/'recording.json').read_text(encoding='utf8'));inv=json.loads((O/'dialogue-inventory.json').read_text(encoding='utf8'));checks=[];errors=[]
def ck(n,v,data=None):
 checks.append({'name':n,'ok':bool(v),'data':data})
 if not v:print('FAIL',n,str(data)[:750],flush=True)
def ff(args):
 p=subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*map(str,args)],capture_output=True,text=True);assert p.returncode==0 and not p.stderr,p.stderr
def duration(path):
 p=subprocess.run([FF,'-hide_banner','-i',str(path)],capture_output=True,text=True);m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',p.stderr);assert m,p.stderr;return int(m[1])*3600+int(m[2])*60+float(m[3])
ck('all nine excerpts completed with native audio and no game errors',len(q['clips'])==9 and not q['errors']and all(c['completed']and c['peak']>.001 and not c['errors']for c in q['clips']))
ck('shipping source unchanged during recording',q['before']==q['after'])
chapters=[];transcript=[];time=0;files=[]
for c in q['clips']:
 plan=c['plan'];name=plan['key'];target=O/(name+'.mp4');files.append(target)
 print('ENCODING '+name,flush=True)
 ff(['-i',O/'films'/(name+'.webm'),'-vf','fps=30','-fps_mode','cfr','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-threads','2','-af','aresample=async=1:first_pts=0','-ar','48000','-c:a','aac','-b:a','160k',target])
 d=duration(target);start=time;chapters.append({'key':name,'title':plan['title'],'start':start,'duration':d,'file':target.name,'scene':plan['scene'],'pilot':plan['pilot']});time+=d
 ids=[r['id']for r in c['rows']];captured=[s['tag']for s in c['stages']if s['tag']!='end'];ck('native ordered dialogue '+name,ids==captured,{'expected':ids,'captured':captured})
 ck('recorded text exactly matches current rows '+name,all(r['text']==next(v['text']for v in c['receipts']if v['tag']==r['id'])for r in c['rows']))
 for row in c['rows']:
  at=start+next(s['at']for s in c['stages']if s['tag']==row['id']);transcript.append({'chapter':name,'title':plan['title'],'scene':plan['scene'],'shot':row['id'],'start':at,'speaker':row['who'],'text':row['text'],'duration':row['duration'],'people':row['people']})
 ck('clip geometry and native clock '+name,abs(d-c['seconds'])<.6,{'movie':d,'capture':c['seconds']})
 (O/'chapters.json').write_text(json.dumps(chapters,indent=2),encoding='utf8')
concat=O/'clips.ffconcat';concat.write_text('ffconcat version 1.0\n'+''.join("file '"+p.name+"'\n"for p in files),encoding='utf8')
meta=';FFMETADATA1\ntitle=Bullets of Fury - Ally and sibling dialogue review\n'
for i,ch in enumerate(chapters):
 meta+='[CHAPTER]\nTIMEBASE=1/1000\nSTART='+str(round(ch['start']*1000))+'\nEND='+str(round((chapters[i+1]['start']if i+1<len(chapters)else time)*1000))+'\ntitle='+ch['title'].replace('&','and')+'\n'
(O/'chapters.ffmeta').write_text(meta,encoding='utf8');movie=O/'allies-and-siblings-full.mp4';ff(['-safe','0','-f','concat','-i',concat,'-f','ffmetadata','-i',O/'chapters.ffmeta','-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',movie]);ff(['-i',movie,'-f','null','-']);ck('full chaptered H264/AAC reel decodes',True)
p=subprocess.run([FF,'-hide_banner','-i',str(movie),'-af','volumedetect','-vn','-f','null','-'],capture_output=True,text=True);audio=[s.strip()for s in p.stderr.splitlines()if 'mean_volume:'in s or 'max_volume:'in s];ck('combined native audio remains audible',len(audio)==2 and not any('-inf'in s for s in audio),audio)
archived=[{'pilot':p,'cast':v['cast'],'destination':v['destination'],'lines':[b for b in v['beats']if b.get('text')]}for p,v in inv['legacy'].items()if len(v['cast'])>1]
ck('six distinct retained duo opening scripts found',len(archived)==6,[r['pilot']for r in archived])
original=json.loads(re.search(r'const C16_STORY=(.*?);\n',(R/'assets/comic_story_1111.js').read_text(encoding='utf8')).group(1));oldSisters=[b for b in original['scenes']['post-4']if b['id']in ['POST4-08','POST4-09']]
def tc(t):return str(int(t)//60)+':'+str(int(t)%60).zfill(2)
text='# Ally and sibling dialogue review\n\nCurrent native scene excerpts, with original dialogue clocks and audio. The excerpts are shared story beats; they do not establish selected-ally exclusivity. No story, art, unlock or save changes.\n\n'
for ch in chapters:
 text+='## '+tc(ch['start'])+' — '+ch['title']+'\n\nSource: '+ch['scene']+', lead '+ch['pilot']+'.\n\n'
 for row in [r for r in transcript if r['chapter']==ch['key']]:text+='['+tc(row['start'])+'] '+row['shot']+' — '+row['speaker']+': '+(row['text']or'[Silent authored insert]')+'\n\n'
text+='## Inactive legacy duo openings — transcript only\n\nThe current Fury crawl and selected-pilot jungle comic supersede these scripts. They are retained source data and are not reactivated by this review.\n\n'
for a in archived:
 text+='### '+a['pilot'].title()+' lead — '+', '.join(v.title()for v in a['cast'])+'\n\n'
 for row in a['lines']:text+=row['who'].upper()+': '+row['text']+'\n\n'
text+='### Superseded sisters’ Stage 4 banter\n\n'
for row in oldSisters:text+=row['who']+': '+row['text']+'\n\n'
(O/'transcript.md').write_text(text,encoding='utf8');(O/'transcript.json').write_text(json.dumps({'current':transcript,'inactiveOpenings':archived,'supersededSisters':oldSisters},indent=2),encoding='utf8')
contact=Image.new('RGB',(1200,729),'#0c1821');g=ImageDraw.Draw(contact)
for i,c in enumerate(q['clips']):
 shot=next((s for s in c['shots']if len(s['text'])>0),c['shots'][0]);im=Image.open(O/shot['file']).convert('RGB');im.thumbnail((400,225),Image.Resampling.NEAREST);x=i%3*400;y=i//3*243;contact.paste(im,(x,y));g.text((x+7,y+225),c['plan']['title'].replace('—','-'),fill='white')
contact.save(O/'contact.jpg',quality=94)
buttons=''.join('<button class="chapter" data-time="'+str(c['start'])+'">'+tc(c['start'])+' '+html.escape(c['title'])+'</button>'for c in chapters)
rows=''.join('<details open><summary>'+html.escape(c['title'])+'</summary><p class="scope">'+html.escape(c['scene'])+' · '+html.escape(c['pilot'])+' lead</p>'+''.join('<p><button class="line" data-time="'+str(r['start'])+'">'+tc(r['start'])+'</button> <code>'+html.escape(r['shot'])+'</code> <b>'+html.escape(r['speaker'])+':</b> '+html.escape(r['text']or'[Silent authored insert]')+'</p>'for r in transcript if r['chapter']==c['key'])+'</details>'for c in chapters)
archive=''.join('<details><summary>'+html.escape(a['pilot'].title()+' lead / '+', '.join(p.title()for p in a['cast']))+'</summary>'+''.join('<p><b>'+html.escape(r['who'].upper())+':</b> '+html.escape(r['text'])+'</p>'for r in a['lines'])+'</details>'for a in archived)
body='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOF — Allies and siblings dialogue review</title><style>body{max-width:1200px;margin:24px auto;padding:0 18px;background:#0a1721;color:#ecedf0;font:17px/1.55 system-ui,sans-serif}video,img{width:100%;height:auto;background:#000}button{padding:8px 11px;margin:4px 5px 4px 0;background:#213c4d;color:#eaf6fa;border:1px solid #6a96a9;cursor:pointer}button.line{font:inherit;padding:1px 7px}code{color:#aac9d5}a{color:#8de0e0}summary{cursor:pointer;font-weight:bold}details{margin:16px 0;padding:12px;border:1px solid #395366}.scope{color:#afc4d2;font-size:15px}h2{margin-top:32px}li{margin:9px 0}</style><h1>Allies &amp; siblings — existing dialogue</h1><p>Nine native cinematic excerpts with game audio. Pick a chapter, or click any transcript timestamp to jump directly to a line.</p><video id="sequence" controls preload="metadata" poster="roundtable-03.png" src="allies-and-siblings-full.mp4"></video><div>__BUTTONS__</div><p class="scope">Recorded directly from the current game’s scene builders and renderer at their normal clocks. Focused excerpts, not full campaign transitions or completed playthroughs. No shipping story, art, unlock or save changes.</p><h2>Notes for the dialogue wrap</h2><ul><li><b>Exclusivity:</b> these current pair scenes are shared campaign beats. The older pilot-specific duo openings are retained below as inactive scripts; the new opening crawl/jungle comic supersedes them.</li><li><b>Artwork:</b> the front/cockpit portraits use their current families. Juggernaut’s guitar insert still contains the older black-vest illustration beside his current orange-vest portrait. Workshop plates are retained as they currently appear; this review does not certify every baked illustration against the new likeness references.</li><li><b>Read time:</b> several ending lines have short native holds. Each line’s timing is preserved here so you can judge the actual pacing.</li><li><b>Speaker ownership:</b> Juggernaut owns the favorite-album request and Cole answers. The current Bulletalica reveal is included.</li></ul><p><a href="transcript.md">Full timecoded transcript</a> · <a href="transcript.json">Structured dialogue inventory</a></p><h2>Current transcript</h2>__ROWS__<h2>Inactive legacy duo openings</h2><p class="scope">Source archive only. These do not currently play through the new opening. Wording is preserved, including older squad references.</p>__ARCHIVE__<details><summary>Superseded Stage 4 sisters’ bomber exchange</summary>__BOMBER__</details><h2>Native contact sheet</h2><img src="contact.jpg" alt="Nine current native dialogue scenes"><script>document.querySelectorAll('[data-time]').forEach(b=>b.onclick=async()=>{const v=document.getElementById('sequence');v.currentTime=Number(b.dataset.time);try{await v.play()}catch(e){if(e.name!=='AbortError')throw e}});</script></html>'''
(O/'review.html').write_text(body.replace('__BUTTONS__',buttons).replace('__ROWS__',rows).replace('__ARCHIVE__',archive).replace('__BOMBER__',''.join('<p><b>'+html.escape(r['who'])+':</b> '+html.escape(r['text'])+'</p>'for r in oldSisters)),encoding='utf8')
print('VERIFYING BROWSER',flush=True)
url='http://127.0.0.1:8766/_shots/ally_dialogue_1115/'
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1320,'height':1000});p.set_default_timeout(30000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto(url+'review.html');p.wait_for_function('document.querySelector("video").readyState>=1');info=p.evaluate('()=>{const v=document.querySelector("video");return {w:v.videoWidth,h:v.videoHeight,duration:v.duration}}');ck('browser movie geometry/duration',info['w']==1824 and info['h']==1024 and abs(info['duration']-time)<1,info)
 p.evaluate('async()=>{window.qaAC=new AudioContext();await qaAC.resume();window.qaAnal=qaAC.createAnalyser();qaAnal.fftSize=2048;qaAC.createMediaElementSource(document.querySelector("video")).connect(qaAnal);qaAnal.connect(qaAC.destination)}');peak=0
 for i,ch in enumerate(chapters):
  p.locator('button.chapter').nth(i).click();p.wait_for_function('t=>{const v=document.querySelector("video");return Math.abs(v.currentTime-t)<1.4&&!v.paused&&!v.seeking}',arg=ch['start']);t=p.evaluate('async()=>await new Promise(r=>document.querySelector("video").requestVideoFrameCallback((_,m)=>r(m.mediaTime)))');ck('decoded chapter '+ch['key'],abs(t-ch['start'])<1.6,t)
  a=p.evaluate('async()=>{const b=new Float32Array(2048);let peak=0;for(let i=0;i<8;i++){await new Promise(r=>setTimeout(r,25));qaAnal.getFloatTimeDomainData(b);for(const v of b)peak=Math.max(peak,Math.abs(v))}return peak}');peak=max(peak,a)
 ck('decoded game audio in browser',peak>.001,peak)
 lastLine=p.locator('button.line').nth(4);wanted=float(lastLine.get_attribute('data-time'));lastLine.click();p.wait_for_function('t=>Math.abs(document.querySelector("video").currentTime-t)<1.5&&!document.querySelector("video").seeking',arg=wanted);ck('transcript timestamp seeks video',True)
 p.evaluate('document.querySelector("video").pause()');p.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth)');p.evaluate('scrollTo(0,0)');p.screenshot(path=str(O/'browser-review.png'));ck('all review assets load without errors',not errors,errors);ck('review page has no horizontal overflow',p.evaluate('document.documentElement.scrollWidth<=innerWidth'));b.close()
with urlopen(Request(url+movie.name,headers={'Range':'bytes=0-255'}))as r:ck('HTTP range seeking206',r.status==206 and len(r.read())==256)
ck('shipping hashes still match after packaging',all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in q['before'].items()))
result={'checks':checks,'errors':errors,'movie':{'file':movie.name,'duration':duration(movie),'size':[1824,1024],'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'chapters':chapters,'audio':audio},'rows':len(transcript),'scope':q['scope'],'knownFindings':['Shared story beats, not selected-ally gated unlocks.','Six retained duo opening scripts are inactive under the current Fury opening.','Juggernaut guitar insert includes older black-vest illustration beside current orange portrait.','Ending read holds remain short and are preserved for review.'],'sourceBefore':q['before'],'sourceAfter':q['after']}
(O/'qa.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps({'duration':result['movie']['duration'],'rows':len(transcript),'chapters':len(chapters),'passed':sum(c['ok']for c in checks),'checks':len(checks)},indent=2));assert all(c['ok']for c in checks)
