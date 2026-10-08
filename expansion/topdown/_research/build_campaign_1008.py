"""Register existing authored packs and normalize the campaign's loose plates.

No base atlas changes. Source grids, pivots, sequences and pilot paint rules stay
owned by the original manifests. Runtime keys use pack prefixes to avoid collisions.
"""
from pathlib import Path
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'expansion/topdown/art/campaign_1008'
OUT.mkdir(exist_ok=True)
packs = {}
frames = {}
sequences = {}
for pack, prefix in [('ground','gr'),('onfoot','of'),('windstorm_machinists','wm')]:
    data = json.loads((ROOT / 'expansion' / pack / 'manifest.json').read_text())
    packs[pack] = data
    for key, meta in data['frames'].items():
        frames[prefix+'_'+key] = {'file': 'expansion/'+pack+'/'+(meta.get('file') or meta['path']),
                               'anchor': meta.get('pivot',[48,48])}
    for key, meta in data['sequences'].items():
        sequences[prefix+'_'+key] = dict(meta, frames=[prefix+'_'+k for k in meta['frames']])
miami = OUT / 'miami_open_source.png'
Image.open(miami if miami.exists() else ROOT/'expansion/onfoot/stage/miami_infiltration.png').resize((800,1200),Image.Resampling.NEAREST).save(OUT/'miami_ground.png')
frames['miami_ground'] = {'file':'expansion/topdown/art/campaign_1008/miami_ground.png','anchor':[400,600]}
rebel = OUT / 'rebel_ground_source.png'
if rebel.exists():
    Image.open(rebel).resize((800,2400),Image.Resampling.NEAREST).save(OUT/'rebel_ground.png')
    frames['rebel_ground'] = {'file':'expansion/topdown/art/campaign_1008/rebel_ground.png','anchor':[400,1200]}
# Preserve the approved ground paint contract; recolor only authored cobalt armor.
def paint(im, p):
    rgb = [int(p['color'][i:i+2],16) for i in (1,3,5)]
    target = sum(c*w for c,w in zip(rgb,[.2126,.7152,.0722]))
    def px(q):
        r,g,b,a=q
        if a and b>r+23 and b>g*1.08 and g>b*.14:
            lum=(.2126*r+.7152*g+.0722*b)*p.get('lum',1)
            return tuple(min(255,round(c*lum/target)) for c in rgb)+(a,)
        return q
    im.putdata([px(q) for q in im.get_flattened_data()])
    return im
pilots=dict(packs['ground']['pilots'])
pilots['niel']=dict(packs['windstorm_machinists']['pilots']['niel'],family='assault')
for pilot,p in pilots.items():
    for part in ['hull','turret','damaged_hull','wreck']:
        if pilot != 'niel': continue
        name='niel_'+part+'.png'
        paint(Image.open(ROOT/'expansion/ground/tanks'/('assault_'+part+'.png')).convert('RGBA'),p).save(OUT/name)
        frames['pt_niel_'+part]={'file':'expansion/topdown/art/campaign_1008/'+name,'anchor':[96,124]}
    body=p['body']
    # Sprite silhouettes, highlights and alpha are copied unchanged; armor alone follows paint mask.
    for key,meta in packs['ground']['frames'].items():
        if not key.startswith(body+'_') or not any(q in key for q in ['_aim_','_run_']): continue
        name=pilot+'_'+key[len(body)+1:]+'.png'
        paint(Image.open(ROOT/'expansion/ground'/meta['path']).convert('RGBA'),p).save(OUT/name)
        frames['fp_'+pilot+'_'+key[len(body)+1:]]={'file':'expansion/topdown/art/campaign_1008/'+name,'anchor':meta['pivot']}
data={'frames':frames,'sequences':sequences,'pilots':pilots,'tanks':packs['windstorm_machinists']['tanks']}
(OUT/'manifest.json').write_text(json.dumps(data,indent=1)+'\n')
(OUT/'manifest.js').write_text('window.TD_CAMPAIGN_ART='+json.dumps(data,separators=(',',':'))+';\n')
print(len(frames),'registered authored frames;',len(sequences),'sequences')
