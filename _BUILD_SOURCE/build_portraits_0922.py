"""Import Mike's portraits and package generated expression cells without repainting art."""
import json, shutil, zipfile
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/game/pilots_0922'
META=ROOT/'_shots/portraits_rebels_0922/generations.json'
POSES=['idle','happy','laugh','anger','sad','crash','victory','talk-closed','talk-small','talk-medium','talk-wide','talk-o']

def main():
    if META.exists():records=json.loads(META.read_text())
    else:records=[dict(name=a['pilot'],generated=str(ROOT/a['sheet']),path=str(ROOT/a['source']),prompt=a['prompt']) for a in json.loads((OUT/'provenance.json').read_text())['assets']]
    for sub in ['sources','sheets','portraits','comm','bodies']:(OUT/sub).mkdir(parents=True,exist_ok=True)
    archive=Path.home()/'Downloads/NexusII_Cole_Square_16bit_Portraits.zip'
    if archive.exists():
        with zipfile.ZipFile(archive) as z:
            for entry in z.infolist():
                if entry.filename.endswith('.png'):
                    (OUT/'sources'/('cole_'+Path(entry.filename).name)).write_bytes(z.read(entry))
    shipped=[]
    for r in records:
        pilot=r['name'];master=OUT/'sheets'/(pilot+'_expressions.png')
        if Path(r['generated']).resolve()!=master.resolve():shutil.copy2(r['generated'],master)
        source=OUT/'sources'/(pilot+'_reference.png')
        if Path(r['path']).resolve()!=source.resolve():shutil.copy2(r['path'],source)
        im=Image.open(master).convert('RGBA');w,h=im.size
        xs=[round(w*i/4) for i in range(5)]
        ys=[round(h*i/3) for i in range(4)]
        cells=[]
        for i,pose in enumerate(POSES):
            c,row=i%4,i//4;box=(xs[c],ys[row],xs[c+1],ys[row+1])
            cell=im.crop(box).resize((256,256),Image.Resampling.NEAREST)
            supplied={'idle':'02_neutral','happy':'03_smirking','sad':'06_brooding','victory':'07_sunglasses_salute'} if pilot=='cole' else {}
            if pose in supplied:
                cell=Image.open(OUT/'sources'/('cole_'+supplied[pose]+'.png')).convert('RGBA').resize((256,256),Image.Resampling.NEAREST)
            # Stable closed-mouth anchor; generated closed-talking can have parted lips.
            if pose=='talk-closed':cell=Image.open(OUT/'portraits'/(pilot+'-idle.png')).convert('RGBA')
            cell.save(OUT/'portraits'/(pilot+'-'+pose+'.png'))
            # Mike requested dialogue faces looking toward the text on their right.
            cell.transpose(Image.Transpose.FLIP_LEFT_RIGHT).resize((128,128),Image.Resampling.NEAREST).save(OUT/'comm'/('comm_'+pilot+'_'+pose+'.png'))
            cells.append({'pose':pose,'rect':box,'suppliedOverride':supplied.get(pose)})
        # Preserve all supplied Cole expressions as additional selectable authored portraits.
        if pilot=='cole':
            extras={'neutral':'02_neutral','smirking':'03_smirking','brooding':'06_brooding','sunglasses':'01_sunglasses_neutral','shout':'04_sunglasses_shout','smile-shades':'05_sunglasses_smile','salute':'07_sunglasses_salute','thinking':'08_sunglasses_thinking'}
            for pose,base in extras.items():
                cell=Image.open(OUT/'sources'/('cole_'+base+'.png')).convert('RGBA').resize((256,256),Image.Resampling.NEAREST)
                cell.save(OUT/'portraits'/('cole-'+pose+'.png'))
                cell.transpose(Image.Transpose.FLIP_LEFT_RIGHT).resize((128,128),Image.Resampling.NEAREST).save(OUT/'comm'/('comm_cole_'+pose+'.png'))
        shipped.append({'pilot':pilot,'source':source.relative_to(ROOT).as_posix(),'sheet':master.relative_to(ROOT).as_posix(),'cells':cells,'generator':'built-in image_gen','prompt':r['prompt']})
    body_source=OUT/'sources/cole_full_body.png'
    if not body_source.exists():shutil.copy2(Path.home()/'Desktop/b6b4fd57-9c05-4741-9395-5ee67265d92d.png',body_source)
    body=Image.open(body_source).convert('RGBA')
    body.thumbnail((512,1024),Image.Resampling.NEAREST);body.save(OUT/'bodies/cole.png')
    (OUT/'provenance.json').write_text(json.dumps({'date':'2026-09-22','poses':POSES,'assets':shipped},indent=2)+'\n')
    print('Packaged',len(records),'pilot sheets,',len(list((OUT/'portraits').glob('*.png'))),'portraits and Cole body.')

if __name__=='__main__':main()
