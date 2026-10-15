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
# The ground pack's west run is a mirrored east sequence, not loose west files.
# Materialize that contract so runtime keys are valid in all four directions.
from PIL import ImageOps
for pilot,p in pilots.items():
    for i in range(4):
        east=frames['fp_'+pilot+'_run_east_'+str(i)];im=Image.open(ROOT/east['file']).convert('RGBA')
        name=pilot+'_run_west_'+str(i)+'.png';ImageOps.mirror(im).save(OUT/name)
        frames['fp_'+pilot+'_run_west_'+str(i)]={'file':'expansion/topdown/art/campaign_1008/'+name,
            'anchor':[im.width-east['anchor'][0],east['anchor'][1]],'mirrored_source':east['file'],'pilot':pilot,'palette':p['color']}
# Every gameplay action uses the same pilot paint as idle/run; shared blue
# source sheets are retained unchanged. Keep each authored canvas and root pivot.
import hashlib
action_checks=[]
for pilot,p in pilots.items():
    body=p['body']
    requests=[('wm_'+body+'_prone_fire_'+d,'prone_fire_'+d) for d in ['north','east','south','west']]
    requests += [('of_'+body+'_'+a,a) for a in ['roll_to_stand','roll_to_prone','grenade_throw','death']]
    for source_seq,action in requests:
        source=sequences[source_seq];ids=[]
        for i,key in enumerate(source['frames']):
            meta=frames[key];original=Image.open(ROOT/meta['file']).convert('RGBA')
            rendered=paint(original.copy(),p);name=pilot+'_'+action+'_'+str(i)+'.png';rendered.save(OUT/name)
            ident='fa_'+pilot+'_'+action+'_'+str(i);ids.append(ident)
            frames[ident]={'file':'expansion/topdown/art/campaign_1008/'+name,'anchor':meta['anchor'],
                'source':meta['file'],'pilot':pilot,'palette':p['color'],'size':list(original.size)}
            action_checks.append({'frame':ident,'alpha_unchanged':original.getchannel('A').tobytes()==rendered.getchannel('A').tobytes(),
                'source_sha256':hashlib.sha256((ROOT/meta['file']).read_bytes()).hexdigest()})
        sequences['fa_'+pilot+'_'+action]=dict(source,frames=ids)
# Calibrated muzzle points use the same frame, scale, anchor and rotation as drawing.
for key,meta in frames.items():
    if key.startswith('fp_') or key.startswith('fa_') and '_prone_fire_' in key:
        im=Image.open(ROOT/meta['file']).convert('RGBA');box=im.getbbox();ax,ay=meta['anchor']
        if '_aim_' in key: direction=['north','east','south','west'][int(key.rsplit('_',1)[1])]
        else: direction=key.split('_')[-2]
        meta['muzzle']={'north':[ax,box[1]+1],'east':[box[2]-2,ay],'south':[ax,box[3]-2],'west':[box[0]+1,ay]}[direction]
(OUT/'action_palette_verification.json').write_text(json.dumps({'checks':action_checks,'all_alpha_unchanged':all(q['alpha_unchanged'] for q in action_checks)},indent=1)+'\n',encoding='utf-8')
data={'frames':frames,'sequences':sequences,'pilots':pilots,'tanks':packs['windstorm_machinists']['tanks']}
(OUT/'manifest.json').write_text(json.dumps(data,indent=1)+'\n')
(OUT/'manifest.js').write_text('window.TD_CAMPAIGN_ART='+json.dumps(data,separators=(',',':'))+';\n')
print(len(frames),'registered authored frames;',len(sequences),'sequences')
