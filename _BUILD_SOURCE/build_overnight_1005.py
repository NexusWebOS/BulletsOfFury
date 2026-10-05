"""Import authored RGBA generation; slice equal cells without repainting alpha."""
from pathlib import Path
from PIL import Image
import json, hashlib, shutil
R=Path(__file__).resolve().parents[1]
G=Path(r'C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
S=R/'_ART_SOURCES/overnight_1005'; O=R/'assets/game/overnight_1005'
S.mkdir(parents=True,exist_ok=True); O.mkdir(parents=True,exist_ok=True)
sources={
 'symbiote':('exec-066a063f-6fdb-450c-a28d-e7193a537956.png',4,3,'Twelve black oily symbiote rise, gather, swirl, void, emergence and scatter frames. Steel glints, crimson fissures, detailed arcade pixels; transparent background, no binary download or spherical morph.'),
 'knight':('exec-4c67c833-1f87-40ea-8003-9d6babc3b50a.png',4,2,'Eight whole chrome/crimson alien knight poses, same complete attached horned head in EVERY frame. Neutral, windup, strike, slash, guard, shield bash, casting, jump. Remove swords/shields/lasers/halo/backdrop, preserve arms and hands, genuine RGBA cutouts for independently attached weapons.'),
 'fragments':('exec-f737e6f3-a9fd-4913-b64f-7c199364f40c.png',8,3,'Twenty-four loose oily black symbiote fragments, 8 ordered 360-degree rotational views for each of three hooked/forked tendril shapes. Wide front, three-quarter, edge-on, rear, flipped backside and returning front; transparent background, no ring or backdrop.')}
art={}; manifest={'generator':'built-in image_gen','sources':{},'alpha':'native, unmodified','layout':'equal-cell slicing, no shared atlas edits'}
for name,(file,cols,rows,prompt) in sources.items():
 src=S/(name+'.png')
 if not src.exists(): shutil.copyfile(G/file,src)
 im=Image.open(src).convert('RGBA'); cw=im.width//cols; ch=im.height//rows
 assert im.width%cols==0 and im.height%rows==0
 assert im.getchannel('A').getextrema()[0]==0
 cells=[]
 for f in range(cols*rows):
  path=O/(name+'_'+str(f)+'.png'); im.crop((f%cols*cw,f//cols*ch,(f%cols+1)*cw,(f//cols+1)*ch)).save(path)
  cells.append({'key':'on5_'+name+'_'+str(f),'path':path.relative_to(R).as_posix(),'w':cw,'h':ch})
 art[name]=cells
 manifest['sources'][name]={'path':src.relative_to(R).as_posix(),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'prompt':prompt,'columns':cols,'rows':rows}
(R/'assets/overnight_art_1005.js').write_text('"use strict";\nconst ON5_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(S/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Imported 44 native-alpha cells; knight heads remain part of each whole body.')
