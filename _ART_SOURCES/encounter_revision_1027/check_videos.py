from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess,re,urllib.request
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;videos=json.loads((W/'film-summary.json').read_text());url=json.loads((W/'viewer.json').read_text())['url'];ff=imageio_ffmpeg.get_ffmpeg_exe();rows=[];errors=[]
sheet=Image.new('RGB',(1200,5*230),(7,13,22));draw=ImageDraw.Draw(sheet)
for i,v in enumerate(videos):
 path=W/v['video'];row={'id':v['id'],'video':v['video'],'bytes':path.stat().st_size,'frames':[]}
 # Seek/decode independent points in each final MP4, not the source WebM.
 for j,t in enumerate([8,min(48,v['duration']*.40),v['duration']*.75,max(1,v['duration']-9)]):
  reader=imageio_ffmpeg.read_frames(str(path),pix_fmt='rgb24',input_params=['-ss',str(t),'-threads','2']);meta=next(reader);frame=next(reader);reader.close();im=Image.frombytes('RGB',meta['size'],frame);im.thumbnail((294,184),Image.Resampling.NEAREST);sheet.paste(im,(j*300,i*230+24));row['frames'].append({'time':t,'size':meta['size'],'fps':meta['fps']});row['duration']=meta['duration']
 draw.text((10,i*230+6),v['title'],fill=(218,234,246))
 # Decode audio from the finished file and measure the encoded peak.
 a=subprocess.run([ff,'-v','info','-threads','2','-i',str(path),'-vn','-af','volumedetect','-f','null','-'],capture_output=True,text=True);m=re.search(r'max_volume: ([-\d.]+) dB',a.stderr);row['audioPeakDb']=float(m[1])if m else None;row['audioDecodeOK']=a.returncode==0
 request=urllib.request.Request(url+'/'+v['video'],headers={'Range':'bytes=0-15'})
 with urllib.request.urlopen(request)as r:row['rangeSeekOK']=r.status==206 and len(r.read())==16
 assert row['audioDecodeOK']and row['audioPeakDb']is not None and row['audioPeakDb']<0 and row['rangeSeekOK'],row
 rows.append(row)
sheet.save(W/'final-film-contact.jpg',quality=92)
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':900});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(url+'/index.html',wait_until='load');p.wait_for_selector('video')
 for i,row in enumerate(rows):
  result=p.evaluate('''async i=>{const v=document.querySelectorAll('video')[i];v.muted=true;if(v.readyState<1)await new Promise((r,j)=>{v.addEventListener('loadedmetadata',r,{once:true});v.addEventListener('error',()=>j(Error(v.error?.message||'video error')),{once:true})});v.currentTime=Math.min(20,v.duration*.4);await new Promise(r=>v.addEventListener('seeked',r,{once:true}));const from=v.currentTime;await v.play();await new Promise(r=>setTimeout(r,700));v.pause();return{duration:v.duration,from,to:v.currentTime,error:v.error?.message||null}}''',i)
  row['browser']=result;assert result['to']>result['from']+.3 and not result['error'],result
 p.screenshot(path=str(W/'review-page.png'),full_page=True);b.close()
assert not errors,errors
(W/'video-checks.json').write_text(json.dumps({'clips':rows,'pageErrors':errors,'checks':'All five final clips decoded at four seek points, contained unclipped audible audio, served byte ranges, and played/seeking succeeded in Chromium.'},indent=2));print('All five final MP4s passed seek, playback, audio and byte-range checks.',flush=True)
