"""Compile fixed-pivot walking banks and measured connected-host masks.

Source pixels are preserved. No per-frame scaling or rectangular moving limbs.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib, shutil, re
import numpy as np

R=Path(__file__).resolve().parents[1]
SRC=R/'_shots/stage78_review_1025/source'
ARCH=R/'_BUILD_SOURCE/stage78_review_1025'
OUT=R/'assets/game/shared/combat/stage78_review_1025'
OUT.mkdir(parents=True,exist_ok=True);ARCH.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()[:12]
def bounds(im):return list(im.getbbox() or (0,0,0,0))
def eye(im):
    a=np.array(im);y,x=np.indices(a.shape[:2]);r,g,b=a[:,:,:3].astype(float).transpose(2,0,1)
    mask=(r>150)&(r>g*1.7)&(r>b*1.35)&(x>215)&(x<300)&(y>208)&(y<293)&(a[:,:,3]>80)
    yy,xx=np.where(mask)
    if len(xx)<8:raise ValueError('Unmeasured eye')
    return [round(float(xx.mean()),2),round(float(yy.mean()),2),int(xx.max()-xx.min()+1),int(yy.max()-yy.min()+1)]

def main():
    art={'legs':{},'host':{},'sheets':{}}
    native_hips={'frontL':(143,29),'frontR':(81,29),'rearL':(115,27),'rearR':(111,27)}
    source_ids={'frontL':'cf26878d-9f75-49be-89db-499eb5566ad0','frontR':'19b3d58b-1788-4973-afe0-788b6fa36dbc','rearL':'1af53861-9256-4803-80a9-028d035b63d2','rearR':'469adbb9-2875-4ceb-81dd-61394c757fe1'}
    motion_ids={'frontL':'34d47f14-48a2-4581-bac6-e8839c66c48f','frontR':'752ecc8b-4792-421b-9899-44319c6590db','rearL':'d448e591-796c-4edf-8a9f-d68c87bff97a','rearR':'7c9b9c27-731a-45cb-a528-4700a0081506'}
    manifest=[]
    def register(name,im):
        p=OUT/(name+'.webp');im.save(p,lossless=True,method=6)
        art['sheets'][name]={'key':'r25_'+name,'path':p.relative_to(R).as_posix(),'sha12':sha(p),'w':im.width,'h':im.height}
    for name,hip in native_hips.items():
        for fn in (name+'.png',name+'-walk-sheet.png'):
            dest=ARCH/fn
            if not dest.exists():shutil.copyfile(SRC/fn,dest)
        raw=Image.open(ARCH/(name+'-walk-sheet.png')).convert('RGBA');assert raw.size==(1792,224)
        frames=[];sheet=Image.new('RGBA',(4*256,2*256));hits=Image.new('RGBA',sheet.size)
        ref=np.array(raw.crop((0,0,224,224)))
        hx,hy=hip;box=(hx-32,0,hx+32,60);patch=ref[box[1]:box[3],box[0]:box[2]].astype(float)
        for f in range(8):
            cell=raw.crop((f*224,0,(f+1)*224,224));a=np.array(cell).astype(float)
            # Translation only: match the unchanged round hip, then use a shared canvas.
            best=(float('inf'),0,0)
            for dy in range(0,7):
                for dx in range(-6,7):
                    candidate=a[dy:dy+60,box[0]+dx:box[2]+dx]
                    score=float(np.mean((candidate-patch)**2))
                    if score<best[0]:best=(score,dx,dy)
            dx,dy=best[1:];c=Image.new('RGBA',(256,256));c.alpha_composite(cell,(16-dx,16-dy))
            px=np.array(c);mask=px[:,:,3]>80;yy,xx=np.where(mask);foot=mask & (np.indices(mask.shape)[0]>yy.max()-9)
            fy,fx=np.where(foot);toe=[round(float(fx.mean()),2),round(float(fy.mean()),2)]
            solid=px[:,:,3]>200;sy,sx=np.where(solid);nearest=int(np.argmin((sx-toe[0])**2+(sy-toe[1])**2));target=[int(sx[nearest]),int(sy[nearest])]
            frames.append({'key':f'r25_leg_{name}_{f}','white':f'r25_leg_{name}_hit_{f}','w':256,'h':256,'pivot':[hx+16,hy+16],'foot':toe,'target':target,'bounds':bounds(c),'alignment':[dx,dy]})
            sheet.alpha_composite(c,((f%4)*256,(f//4)*256));white=Image.new('RGBA',c.size,'white');white.putalpha(c.getchannel('A'));hits.alpha_composite(white,((f%4)*256,(f//4)*256))
        register('leg_'+name,sheet);register('leg_'+name+'_hit',hits)
        art['legs'][name]={'frames':frames,'count':8,'cols':4,'w':256,'h':256,'pivot':[hx+16,hy+16],'worldScale':.60 if name.startswith('front') else .64}
        manifest +=[{'asset_id':source_ids[name],'sha12':sha(ARCH/(name+'.png')),'label':name+' native identity'},{'asset_id':motion_ids[name],'sha12':sha(ARCH/(name+'-walk-sheet.png')),'label':name+' eight-pose walk source'}]
    bi=json.loads((R/'assets/boss_integrity_art_1024.js').read_text().split('const BI24_ART=',1)[1].split(';',1)[0])
    for name in ('dracodia_wind','dracodia_strike','dracodia_recover'):
        a=bi['banks'][name];raw=Image.open(R/bi['sheets'][name]['path']).convert('RGBA');rows=(a['count']+3)//4
        layers={id:Image.new('RGBA',(2048,rows*512)) for id in ('core','left','right')};frames=[]
        for f in range(a['count']):
            im=raw.crop((f%4*512,f//4*512,f%4*512+512,f//4*512+512));pix=np.array(im);Y,X=np.indices((512,512))
            # Curved anatomy seam: shoulder/forearm outside, face/tendrils retained centrally.
            # Keep crown, face flares and the full-width torso attached. Only
            # the outside arm contour detaches; the old narrow strip cut body pixels.
            border=np.interp(np.arange(512),[0,190,208,245,285,340,511],[0,0,80,166,180,198,198])[:,None]
            left=X<border;right=X>512-border
            for id,select in [('left',left),('right',right),('core',~(left|right))]:
                p=pix.copy();p[:,:,3]=np.where(select,p[:,:,3],0);layers[id].alpha_composite(Image.fromarray(p),((f%4)*512,(f//4)*512))
            arms=a['arms'][f];muzzles={}
            for side in ('left','right'):
                ax,ay=arms[side];raised=name=='dracodia_wind' and f>=5 or name=='dracodia_strike' and f==0
                muzzles[side]=[round(ax*2+(-18 if side=='left' else 18),2),round(ay*2+(48 if raised else 66),2)]
            targets={}
            for side,region in [('left',left),('right',right)]:
                solid=region&(pix[:,:,3]>96)
                for _ in range(3):solid=solid&np.roll(solid,1,0)&np.roll(solid,-1,0)&np.roll(solid,1,1)&np.roll(solid,-1,1)
                yy,xx=np.where(solid)
                if len(xx):
                    ax,ay=arms[side];n=((xx-ax*2)**2+(yy-ay*2)**2).argmin();targets[side]=[int(xx[n]),int(yy[n])]
            frames.append({'eye':eye(im),'muzzles':muzzles,'targets':targets})
        for id,im in layers.items():register(name+'_'+id,im)
        art['host'][name]={'count':a['count'],'cols':4,'w':512,'h':512,'pivot':[256,256],'frames':frames}
    # Reuse actual authored branching blue lightning; never the rejected pinwheel.
    lightning=Image.open(R/'assets/game/levels/stage_05/boss/stage5_archmage_0916/combat_0926/hammer_lightning.png').convert('RGBA')
    bolt=Image.new('RGBA',(4*256,2*448))
    for f in range(8):bolt.alpha_composite(lightning.crop((f%4*384+64,f//4*512+32,f%4*384+320,f//4*512+480)),(f%4*256,f//4*448))
    register('lightning',bolt);art['lightning']={'key':'r25_lightning','w':256,'h':448,'cols':4,'count':8,'pivot':[128,224]}
    # The native laser's root supplies its own moving white/red tongues.
    beam=Image.open(R/'assets/game/shared/combat/encounter_revision_1023/laser_down.webp').convert('RGBA');root=Image.new('RGBA',(8*104,2*80))
    for f in range(16):root.alpha_composite(beam.crop((f%8*104,f//8*624,f%8*104+104,f//8*624+80)),(f%8*104,f//8*80))
    register('eye_root',root);art['eye_root']={'key':'r25_eye_root','w':104,'h':80,'cols':8,'count':16,'pivot':[52,12]}
    flare_source=SRC/'eye-flare-sheet.png'
    if flare_source.exists():
        for fn in ('eye-flare-source.png','eye-flare-sheet.png'):
            if not (ARCH/fn).exists():shutil.copyfile(SRC/fn,ARCH/fn)
        raw=Image.open(ARCH/'eye-flare-sheet.png').convert('RGBA');assert raw.size==(1360,170)
        flare=Image.new('RGBA',(4*256,2*256));widths=[]
        for f in range(8):
            im=raw.crop((f*170,0,f*170+170,170));b=im.getbbox();widths.append(b[2]-b[0]);flare.alpha_composite(im,((f%4)*256+43,(f//4)*256+43))
        register('eye_flare',flare);art['eye_flare']={'key':'r25_eye_flare','w':256,'h':256,'cols':4,'count':8,'pivot':[128,128],'visibleWidth':max(widths)}
        manifest +=[{'asset_id':'97389be6-208b-4b71-b0c7-e7b843d12899','sha12':sha(ARCH/'eye-flare-source.png'),'label':'red eye aperture source'},{'asset_id':'6dd5142b-3d0c-41d9-91e3-4279c140c094','sha12':sha(ARCH/'eye-flare-sheet.png'),'label':'eight-pose red eye laser flare'}]
    (ARCH/'spritecook-assets.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (OUT/'manifest.json').write_text(json.dumps(art,indent=2)+'\n')
    (R/'assets/stage78_review_art_1025.js').write_text('"use strict";\n// Generated by _BUILD_SOURCE/build_stage78_review_1025.py.\nconst R25_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8')
    taxonomy=R/'assets/data/ART_TAXONOMY.json';raw=taxonomy.read_bytes();nl=b'\r\n' if b'\r\n'in raw else b'\n'
    entry={'r25_':{'role':'warden_walking_dracodia_first_host_download','sheet':None,'owner':'_BUILD_SOURCE/build_stage78_review_1025.py','note':'Mike October25: four eight-pose authored modular leg walks, fixed256 cells/common hip pivots/one scale; planted diagonal stance, actual alpha hit regions and opaque toe targets. Complete512 connected first-host plates retain original pixels; measured arm/core masks support explicit exploding breakaway arms. Animated measured-eye flare, native claw projectiles/physical rockets/muzzles, continuous ball/code bombs, living original arena and protected24-beat digital reconstruction. Original branching lightning replaces the rejected pinwheel. Native HP/portal/rewards/copies remain owned by their existing encounter.'}}
    fragment=(json.dumps(entry,indent=2,ensure_ascii=False)[2:-2]+',\n').encode().replace(b'\n',nl)
    if b'  "r25_":' in raw:updated=re.sub(rb'(?m)^  "r25_": \{[\s\S]*?^  \},\r?\n',lambda m:fragment,raw,count=1)
    else:updated=raw.replace(b'{'+nl,b'{'+nl+fragment,1)
    if updated!=raw:taxonomy.write_bytes(updated)
    print(json.dumps({'sheets':len(art['sheets']),'legFrames':32,'hostFrames':sum(a['count']for a in art['host'].values())}))
if __name__=='__main__':main()
