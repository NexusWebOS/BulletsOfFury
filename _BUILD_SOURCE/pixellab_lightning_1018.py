"""Retrieve only the PixelLab-generated lightning jobs; never uploads local art."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse, json, urllib.request, urllib.error
from pixellab_mcp import PixelLab

R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/lightning_depth_1018'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['poll','download'])
    parser.add_argument('--name',action='append')
    args=parser.parse_args()
    jobs=json.loads((S/'jobs.json').read_text(encoding='utf-8'))
    names=args.name or list(jobs)
    if args.mode=='poll':
        client=PixelLab()
        try:
            for name in names:
                j=jobs[name]
                if not j.get('id'):continue
                result=client.call('get_image',{'job_id':j['id'],'index':0})
                p=S/'status'/(name+'.json');p.parent.mkdir(parents=True,exist_ok=True)
                p.write_text(json.dumps(result,indent=2),encoding='utf-8')
                s='\n'.join(c.get('text','') for c in result.get('content',[]) if c.get('type')=='text')
                print(name+': '+s.splitlines()[0][:160],flush=True)
        finally:client.close()
        return
    for name in names:
        j=jobs[name]
        if not j.get('id'):continue
        count=j.get('count',0)+1 if j.get('count') else 1
        dest=S/'returned'/name;dest.mkdir(parents=True,exist_ok=True)
        def download(i):
            path=dest/f'frame_{i:03}.png'
            if path.exists():return
            url=f"https://api.pixellab.ai/mcp/images/{j['id']}/download?index={i}"
            with urllib.request.urlopen(url,timeout=55) as response:data=response.read()
            if not data.startswith(b'\x89PNG'):raise ValueError('Not a PNG: '+name)
            path.write_bytes(data)
        try:download(0)
        except urllib.error.HTTPError as exc:
            if exc.code==423:
                print(name+': waiting for PixelLab',flush=True);continue
            raise
        with ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(download,range(1,count)))
        print(f'{name}: {count} PNGs saved',flush=True)

if __name__=='__main__':main()
