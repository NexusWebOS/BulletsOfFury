from pathlib import Path
from PIL import Image
import json,math
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/city-atlas';O.mkdir(parents=True,exist_ok=True)
s=(R/'assets/city_rescue_art_1115.js').read_text(encoding='utf8');at=s.index('const CITY16_ART=')+len('const CITY16_ART=');D,_=json.JSONDecoder().raw_decode(s[at:]);pages={p['key']:p for b in D['banks'].values()for p in b['pages']};bad=[];need={};cell_count=0
images={k:Image.open(R/p['path']).convert('RGBA')for k,p in pages.items()}
for n,b in D['banks'].items():
 for i,c in enumerate(b['cells']):
  k,x,y=c;im=images[k];cell_count+=1;right=x+b['w'];bottom=y+b['h'];p=need.setdefault(k,{'right':0,'bottom':0,'cells':0});p['right']=max(p['right'],right);p['bottom']=max(p['bottom'],bottom);p['cells']+=1
  if x<0 or y<0 or right>im.width or bottom>im.height:bad.append({'bank':n,'frame':i,'key':k,'source':[x,y,b['w'],b['h']],'actual':list(im.size),'required':[right,bottom]})
summary=[]
for k,a in need.items():
 im=images[k]
 if a['right']>im.width or a['bottom']>im.height:
  alpha=im.getchannel('A');summary.append({'key':k,'path':pages[k]['path'],'actual':list(im.size),'required':[math.ceil(a['right']/2)*2,math.ceil(a['bottom']/2)*2],'lastRowMaxAlpha':alpha.crop((0,im.height-1,im.width,im.height)).getextrema()[1],'lastColumnMaxAlpha':alpha.crop((im.width-1,0,im.width,im.height)).getextrema()[1],'cells':a['cells']})
report={'banks':len(D['banks']),'pages':len(pages),'cells':cell_count,'badCells':bad,'pagesNeedingPadding':summary,'scope':'Static current shipping CITY16 atlas cells against actual decoded page sizes. Does not alter original pixels or assert missing ink restoration.'};(O/'before.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps({'banks':report['banks'],'cells':cell_count,'badCells':len(bad),'pagesNeedingPadding':summary},indent=2))
