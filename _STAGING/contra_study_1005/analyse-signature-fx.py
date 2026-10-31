from pathlib import Path
from PIL import Image
import hashlib, json, shutil
root=Path(__file__).resolve().parent
source=Path(r'C:\Users\Mike\.codex\generated_images\01a10ef4-27c3-71d2-97c8-0d9fa5c0bb2f\exec-c1424c24-040e-43f3-aa9c-1844ef0e339f.png')
dest=root/'art'/'boss_signature_fx.png'
shutil.copyfile(source,dest)
im=Image.open(dest)
w,h=im.size
assert im.mode=='RGBA' and w%4==0 and h%3==0
cw,ch=w//4,h//3
frames=[]
for i in range(12):
    x,y=(i%4)*cw,(i//4)*ch
    alpha=im.getchannel('A').crop((x,y,x+cw,y+ch))
    bounds=alpha.point(lambda a:255 if a>=16 else 0).getbbox()
    assert bounds
    padding=min(bounds[0],bounds[1],cw-bounds[2],ch-bounds[3])
    frames.append({'index':i,'sourceRect':[x,y,cw,ch],'alphaBoundsAt16':bounds,'padding':padding})
manifest={'id':'bof_boss_signature_1006','status':'sandbox_candidate_native_art_review_required','file':dest.name,'mode':im.mode,'nativeSize':[w,h],'grid':[4,3],'cellSize':[cw,ch],'playback':'Four equal frame slots across clip duration; one-shot with alpha fade','loop':False,'collision':'cosmetic_only','alphaExtrema':im.getchannel('A').getextrema(),'frames':frames,'clips':{'joint':{'frames':[0,1,2,3],'durationSeconds':.65,'pivot':[cw*.5,ch*.58]},'contact':{'frames':[4,5,6,7],'durationSeconds':.65,'pivot':[cw*.5,ch*.72]},'breach':{'frames':[8,9,10,11],'durationSeconds':1,'pivot':[cw*.5,ch*.5]}},'minimumSignificantAlphaPadding':min(f['padding'] for f in frames),'requested48PixelPaddingMet':all(f['padding']>=48 for f in frames),'sourceOriginal':str(source),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'processing':'Exact copy. Read-only alpha/cell analysis; no raster edits.','generator':'OpenAI imagegen, original effects, no Contra pixels supplied','notes':'Four-frame motion is a candidate. Joint endpoint drift, pixel density, timing and native BOF blending require art review. Collision is supplied separately.'}
(root/'art'/'boss_signature_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:manifest[k] for k in ['nativeSize','cellSize','alphaExtrema','minimumSignificantAlphaPadding','requested48PixelPaddingMet']}))
print(json.dumps(frames))
