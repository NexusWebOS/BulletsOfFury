"""Decode the final recording and verify the actual review player in Chromium."""
from pathlib import Path
import json,subprocess,re,math,array
from PIL import Image,ImageDraw
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_recall_1025/video'
r=json.loads((O/'review.json').read_text());qa=json.loads((R/'docs/qa/chronos_recall_video_1025.json').read_text());chapters=qa['recording']['chapters'];ff=imageio_ffmpeg.get_ffmpeg_exe();video=O/'chronos-full-fight.mp4'
contact=Image.new('RGB',(1536,350*math.ceil(len(chapters)/3)),'#102030');draw=ImageDraw.Draw(contact)
for i,(label,t) in enumerate(chapters):
 file=O/f'decoded-{i}.png';subprocess.run([ff,'-v','error','-y','-ss',str(t+1),'-i',str(video),'-frames:v','1','-vf','scale=512:320',str(file)],check=True)
 contact.paste(Image.open(file),(i%3*512,i//3*350+30));draw.text((i%3*512+8,i//3*350+8),f'{t:.1f}s {label}',fill='white')
contact.save(O/'decoded-contact.png')
audio=[]
for label,t in [('dialogue',8),('wave',next(t for label,t in chapters if label=='Red lightning wave'))]:
 raw=subprocess.check_output([ff,'-v','error','-ss',str(t),'-i',str(video),'-t','2','-vn','-ac','1','-ar','16000','-f','f32le','-']);v=array.array('f');v.frombytes(raw);audio.append({'part':label,'peak':max(map(abs,v)),'rms':math.sqrt(sum(x*x for x in v)/len(v))})
checks={'defeat':r['defeated'],'opening_dialogue':any(q.get('intro') and q.get('radio') for q in r['timeline']),'all_new_cues_played':all(r['audio']['playing'].get('c33_'+n,0)>0 for n in ['rage','wave','palm','charge','thunder','smash','hammercharge']),'no_game_errors':not r['errors'],'audible_video':all(a['rms']>.005 for a in audio)}
port,stop=serve(str(R));errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':900});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/chronos_frames_1025/index.html');p.evaluate('playAt(0)');p.wait_for_function('fight.currentTime>.2&&!fight.paused',timeout=120000)
  checks['review_plays']=True;t=next(t for label,t in chapters if label=='Red lightning wave');p.evaluate('(t)=>playAt(t)',t);p.wait_for_timeout(700);checks['chapter_seeks']=p.evaluate('(t)=>Math.abs(fight.currentTime-t)<3',t);p.screenshot(path=str(O/'review-player.png'));checks['no_review_errors']=not errors;b.close()
finally:stop()
(O/'delivery.json').write_text(json.dumps({'checks':checks,'audio':audio,'errors':errors},indent=2));print(json.dumps({'checks':checks,'audio':audio,'errors':errors}))
