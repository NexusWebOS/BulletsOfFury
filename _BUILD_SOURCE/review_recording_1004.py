"""Read-only frame review of Mike's complete 61-minute playthrough.

Writes compact timestamped contact sheets, never alters the source recording.
Use --start/--end/--step for close inspection of an incident.
"""
import argparse, json
from pathlib import Path
import av
from PIL import Image, ImageDraw

p=argparse.ArgumentParser()
p.add_argument('--start',type=float,default=0)
p.add_argument('--end',type=float,default=None)
p.add_argument('--source',default=r'C:\Users\Mdogg\Videos\2026-10-04 00-46-51.mp4')
p.add_argument('--out',default='_shots/gameplay_audit_1004')
p.add_argument('--step',type=float,default=2)
p.add_argument('--cols',type=int,default=4)
p.add_argument('--rows',type=int,default=6)
p.add_argument('--width',type=int,default=384)
p.add_argument('--name',default='timeline')
a=p.parse_args()
out=Path(a.out)/a.name
out.mkdir(parents=True,exist_ok=True)
source=Path(a.source)
c=av.open(str(source)); stream=c.streams.video[0]
stream.thread_type='AUTO'
next_t=a.start; frames=[]; pages=[]; page_index=0
cellh=round(a.width*720/1280)+24
canvas=None
if a.start: c.seek(int(a.start/float(stream.time_base)),stream=stream,backward=True)
for frame in c.decode(stream):
    t=float(frame.time)
    if t+0.02<next_t: continue
    if a.end is not None and t>a.end: break
    if canvas is None: canvas=Image.new('RGB',(a.width*a.cols,cellh*a.rows),'#141923')
    n=len(frames)%(a.cols*a.rows); x=(n%a.cols)*a.width; y=(n//a.cols)*cellh
    im=frame.to_image(); im.thumbnail((a.width,cellh-24))
    canvas.paste(im,(x,y+24))
    stamp=f'{int(t)//3600:02}:{(int(t)//60)%60:02}:{int(t)%60:02}.{int(t*10)%10}'
    ImageDraw.Draw(canvas).text((x+6,y+5),stamp,fill='white')
    frames.append({'seconds':round(t,3),'timestamp':stamp,'page':page_index,'cell':n})
    next_t+=a.step
    if n==a.cols*a.rows-1:
        path=out/f'{page_index:03}.jpg'; canvas.save(path,quality=86)
        pages.append(str(path)); page_index+=1; canvas=None
        print(path,flush=True)
if canvas:
    path=out/f'{page_index:03}.jpg'; canvas.save(path,quality=86); pages.append(str(path))
(out/'index.json').write_text(json.dumps({'source':str(source),'duration':c.duration/1e6,'interval':a.step,'frames':frames,'pages':pages},indent=2))
print(f'{len(frames)} frames, {len(pages)} sheets; complete through {frames[-1]["timestamp"]}',flush=True)
