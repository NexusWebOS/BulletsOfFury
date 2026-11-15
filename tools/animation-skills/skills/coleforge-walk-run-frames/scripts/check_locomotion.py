"""Check complete-character cycle export contracts; does not judge animation quality."""
from pathlib import Path
from PIL import Image
import argparse,hashlib,json

def inspect(path):
    p=Path(path);m=json.loads(p.read_text(encoding='utf-8'))
    atlas=Image.open(p.parent/m['atlas']['image']).convert('RGBA')
    w,h=m['frame_size'];ox,oy=m['origin'];rects=m['atlas']['rects']
    frames=[];heights=[];hashes=[]
    assert len(rects)==len(m['animation']['frames'])
    durations=m['animation'].get('duration_ms')
    assert durations and len(durations)==len(rects) and all(isinstance(v,int) and v>0 for v in durations)
    for i,r in enumerate(rects):
        assert r['w']==w and r['h']==h
        assert 0<=r['x']<=atlas.width-w and 0<=r['y']<=atlas.height-h
        f=atlas.crop((r['x'],r['y'],r['x']+w,r['y']+h));a=f.getchannel('A');b=f.getbbox()
        assert b and set(a.tobytes())=={0,255},(p,i,'empty or soft alpha')
        assert b[0]>2 and b[1]>2 and b[2]<w-2 and b[3]<h-2,(p,i,'cell edge/clipping')
        assert b[3]<=oy,(p,i,'below floor')
        heights.append(b[3]-b[1]);hashes.append(hashlib.sha256(f.tobytes()).hexdigest())
    return m,{'frames':len(rects),'cell':[w,h],'origin':[ox,oy],'duration_ms':sum(durations),
              'drawn_heights':heights,'unique_drawings':len(set(hashes))}

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--walk',required=True);a.add_argument('--run',required=True)
    a.add_argument('--indexed-dir');a.add_argument('--palette-idle');a.add_argument('--out')
    args=a.parse_args();wm,w=inspect(args.walk);rm,r=inspect(args.run)
    assert wm['frame_size']==rm['frame_size'] and wm['origin']==rm['origin']
    assert wm['body_unit']==rm['body_unit'] and wm['body_unit']>0
    assert max(w['drawn_heights'])-min(w['drawn_heights'])<=max(5,wm['body_unit']*.05),'Walk silhouette varies; review anatomy, hair and flame bounds'
    report={'body_unit':wm['body_unit'],'walk':w,'run':r,'visual_review_required':True}
    if args.indexed_dir or args.palette_idle:
        assert args.indexed_dir and args.palette_idle,'Supply both indexed directory and palette idle'
        idle=Image.open(args.palette_idle);assert idle.mode=='P'
        paths=sorted(Path(args.indexed_dir).glob('m1105-*.png'));assert paths,'No native movement PNGs found'
        for p in paths:
            im=Image.open(p);assert im.mode=='P' and im.getpalette()==idle.getpalette(),(p,'model palette mismatch')
            assert im.info.get('transparency')==0
            assert set(im.convert('RGBA').getchannel('A').tobytes())=={0,255}
        report['indexed_palette_frames_checked']=len(paths)
    text=json.dumps(report,indent=2)+'\n'
    if args.out:Path(args.out).write_text(text,encoding='utf-8')
    print(text)

if __name__=='__main__':main()
