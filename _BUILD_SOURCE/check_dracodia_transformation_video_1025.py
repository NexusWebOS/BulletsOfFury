"""Verify playback and seeking of the recorded native transformation."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,argparse

ap=argparse.ArgumentParser();ap.add_argument('--depth',action='store_true');ap.add_argument('--climax',action='store_true');ap.add_argument('--strikes',action='store_true');ap.add_argument('--polish',action='store_true');ap.add_argument('--dna',action='store_true');ap.add_argument('--palette',action='store_true');args=ap.parse_args();args.dna=args.dna or args.palette;args.polish=args.polish or args.dna;args.strikes=args.strikes or args.polish;args.climax=args.climax or args.strikes
R=Path(__file__).resolve().parents[1];info=json.loads((R/('_shots/dracodia_palette_1026/video/latest.json'if args.palette else'_shots/dracodia_dna_1026/video/latest.json'if args.dna else'_shots/dracodia_polish_1026/video/latest.json'if args.polish else'_shots/dracodia_strikes_1026/video/latest.json'if args.strikes else'_shots/dracodia_climax_1026/video/latest.json'if args.climax else'_shots/dracodia_depth_1026/video/latest.json'if args.depth else'_shots/dracodia_transformation_1025/latest.json')).read_text());folder=Path(info['folder']);q=json.loads(Path(info['report']).read_text());checks={};errors=[]
url='http://127.0.0.1:53746/'+q['video']
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto(url,wait_until='domcontentloaded');p.wait_for_function('document.querySelector("video")?.readyState>=2')
 checks['decodes1280x800']=p.evaluate('()=>{const v=document.querySelector("video");return v.videoWidth===1280&&v.videoHeight===800;}')
 for key in ['lightning','storm','reveal']+(['left-arm-break','closing-roar']if args.polish else[])+(['dna-forms-skeleton']if args.dna else[]):
  t=q['chapters'][key];p.evaluate('(t)=>{const v=document.querySelector("video");v.pause();v.currentTime=t;}',t)
  p.wait_for_function('(t)=>{const v=document.querySelector("video");return !v.seeking&&Math.abs(v.currentTime-t)<.12;}',arg=t)
  p.evaluate('async()=>{const v=document.querySelector("video");v.muted=false;await v.play();}')
  p.wait_for_function('(t)=>document.querySelector("video").currentTime>t+.2',arg=t)
  checks[key+'PlaysWithAudio']=p.evaluate('()=>{const v=document.querySelector("video");v.pause();return !v.error&&!v.muted&&v.getVideoPlaybackQuality().totalVideoFrames>2;}')
  if key in ['storm','left-arm-break','closing-roar']:p.screenshot(path=str(folder/('playback-lightning.png'if key=='storm'else'playback-'+key+'.png')))
 response=p.request.get(url,headers={'Range':'bytes=1000-1999'});checks['byteRangeSeeking']=response.status==206 and len(response.body())==1000
 checks['noBrowserErrors']=not errors;b.close()
(folder/'playback.json').write_text(json.dumps({'url':url,'checks':checks,'errors':errors},indent=2),encoding='utf8')
print(json.dumps({'url':url,'checks':checks,'errors':errors}),flush=True)
raise SystemExit(0 if all(checks.values())else 1)
