"""Restore original complete two-handed attacks; normalize only, no weapon assembly."""
from pathlib import Path
from PIL import Image
import json,math,ast
R=Path(__file__).resolve().parents[1];O=R/'assets/game/shared/combat/chronos_motion_1025';P=O/'manifest.json';art=json.loads(P.read_text());WORLD=art['worldScale']
s=(R/'assets/hammer_correction_art_1022.js').read_text();original=json.loads(s[s.index('{'):s.rindex('}')+1])
for n in ast.parse((R/'_BUILD_SOURCE/build_chronos_final_1025.py').read_text()).body:
 if isinstance(n,ast.FunctionDef) and n.name=='export':exec(compile(ast.Module(body=[n],type_ignores=[]),'export','exec'))
# One scale per source bank, shared chest pivot, even 448 canvas.
for mat in ['regular','chrome']:
 suffix='_armor' if mat=='chrome' else ''
 for bank,source,start,end in [('windup','blue_slam',0,9),('strike','blue_slam',9,13),('retract','blue_slam',13,16),('takeoff','blue_slam',0,9),('land','blue_slam',9,0),('left','blue_counter_left',0,15),('right','blue_counter_right',0,15)]:
  rows=[]
  for i in range(17):
   f=round(start+(end-start)*i/16);a=original['banks'][source+suffix][f];x,y,w,h=a['cell'];im=Image.open(R/original['sheets'][a['sheet']]['path']).convert('RGBA').crop((x,y,x+w,y+h));k=300/w;offset=[round(art['pixelPivot'][j]-a['pivot'][j]*k) for j in range(2)];body=Image.new('RGBA',(448,448));body.alpha_composite(im.resize((300,300),Image.Resampling.NEAREST),tuple(offset));tip=[(a['tip'][j]*k+offset[j])*WORLD for j in range(2)];bounds=body.getbbox();meta=dict(tip=tip,grip=[v*WORLD for v in art['pixelPivot']],headBounds=[tip[0]-28,tip[1]-35,tip[0]+28,tip[1]+35],bounds=[v*WORLD for v in bounds],angle=0,empty=False,wholeAuthored=True,gripHands=2,sourceKey=a['key'],sourceFrame=f);rows.append((body,meta))
  export(bank+'_'+mat,rows)
art['originalTwoHandAttacks']={'source':'H22_ART','banks':['blue_slam','blue_counter_left','blue_counter_right'],'materials':['regular','chrome'],'hands':2,'toolComposites':0}
P.write_text(json.dumps(art,indent=2)+'\n');(R/'assets/chronos_motion_art_1025.js').write_text('"use strict";\nconst C27_ART='+json.dumps(art,separators=(',',':'))+';\n',newline='\n')
print('Restored 238 whole two-handed frames across 14 banks')

import runpy
runpy.run_path(str(R/'_BUILD_SOURCE/clean_chronos_chromium_1025.py'))
