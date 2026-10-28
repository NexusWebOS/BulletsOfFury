from pathlib import Path
from PIL import Image
import json,math,hashlib,shutil,sys
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/animation_feedback_1023';W.mkdir(exist_ok=True);O=W/'shipping';O.mkdir(exist_ok=True);backup=W/'before';backup.mkdir(exist_ok=True)
D=json.loads((R/'assets/data/AIR_MOTION_1013.json').read_text())['entries'];models={};sheets={}
sizes={'s8leech':(64,88),'s8manta':(94,76),'s8hunter':(78,82),'s8deathorb':(96,96),'s8carrier':(126,112),'s8tentacle':(104,98),'s8bomber':(116,104),'s8solar':(122,118),'s8gunship':(118,114),'s8needlejet':(66,94),'s8scout':(86,72)}
for typ,(w,h)in sizes.items():
 entry=next((m for m in D.values()if typ in m['aliases']),None)
 if not entry:continue
 src=Image.open(R/entry['heading']['path']).convert('RGBA');native=max(round(w*1.3),round(h*1.3))*1.28;unit=native/entry['heading']['span'];dim=round(128*unit);canvas=384;sheet=Image.new('RGBA',(canvas*4,canvas*2))
 for f in range(8):
  frame=src.crop((f*128,0,(f+1)*128,128)).resize((dim,dim),Image.Resampling.NEAREST);sheet.alpha_composite(frame,(f%4*canvas+(canvas-dim)//2,f//4*canvas+(canvas-dim)//2))
 for suffix,im in [('',sheet),('_hit',Image.new('RGBA',sheet.size,'white'))]:
  if suffix:im.putalpha(sheet.getchannel('A'))
  name=typ+suffix+'.webp';im.save(O/name,lossless=True,exact=True);key='aq23_'+typ+suffix;sheets[key]={'key':key,'path':'assets/game/levels/stage_08/enemies/animation_feedback_1023/'+name,'w':im.width,'h':im.height,'sha256':hashlib.sha256((O/name).read_bytes()).hexdigest()}
 models[typ]={'key':'aq23_'+typ,'white':'aq23_'+typ+'_hit','cell':canvas,'pivot':[canvas//2,canvas//2],'frames':8,'unit':unit,'source':entry['heading']['path'],'nativeSpan':native}
A={'version':1,'owner':'_BUILD_SOURCE/install_animation_feedback_1023.py','models':models,'sheets':sheets};(O/'manifest.json').write_text(json.dumps(A,indent=2));(O/'animation_feedback_art_1023.js').write_text('"use strict";\nconst AQ23_ART='+json.dumps(A,separators=(',',':'))+';\n',encoding='utf-8')
runtime='''"use strict";
/* Native fleet controllers keep warnings, hitboxes, shields, attacks and deaths.
   Shared retired atlas aliases cannot be sampled as their former 4x4 layout.
   Correct type-specific authored cells and white variants are prebaked at
   native units; this renderer uses integer blits and no runtime recoloring. */
const AQ23_FIX={base:{realm:drawS8Mega,load:stageLoadBegin},draws:0};
for(const s of Object.values(AQ23_ART.sheets))XART._src[s.key]=s.path;
stageLoadBegin=function(n,keys){return AQ23_FIX.base.load.call(this,n,[...(keys||[]),...(n===8?Object.keys(AQ23_ART.sheets):[])]);};
drawS8Mega=function(e){const m=AQ23_ART.models[e.type];if(!m)return AQ23_FIX.base.realm.apply(this,arguments);
 const A=e._frRealmAI,size=Math.max(e.w,e.h)*1.28;e._drawW=size*.82;e._drawH=size;
 const turn=Math.abs(e._frBank||0)>10?(e._frBank<0?1:7):0,key=e.flash>0?m.white:m.key;
 if(!XART.rdy(key))return false;const im=XART.get(key),s=m.cell;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,turn%4*s,Math.floor(turn/4)*s,s,s,Math.round(e.x-m.pivot[0]),Math.round(e.y-m.pivot[1]),s,s);AQ23_FIX.draws++;
 if(A?.tell)combatWarningDraw(e,{x:e.x,y:e.y+e.h*.35,ex:A.tell.x,ey:A.tell.y,progress:A.tell.t/.8,width:fr27RealmRow(e)===0?85:fr27RealmRow(e)===2?30:100,alpha:.32});
 return true;
};
window.BOF_ANIMATION_FEEDBACK=AQ23_FIX;
'''
(O/'animation_feedback_1023.js').write_text(runtime,encoding='utf-8')
changes={}
p=R/'assets/air_motion_1013.js';s=p.read_text(encoding='utf-8');old='air13Blit(p,e.x,e.y,size*p.d.referenceRatio,1,e.flash>0?hitFlashColor(e):null);';new='air13Blit(p,e.x,e.y,size*(Number.isFinite(p.d.referenceRatio)?p.d.referenceRatio:1),1,e.flash>0?hitFlashColor(e):null);';assert old in s or new in s;changes[p]=s if new in s else s.replace(old,new)
p=R/'assets/encounters_0930.js';s=p.read_text(encoding='utf-8');old='function enc30Cell(name,f,x,y,w,h,tint){';new='''function enc30Cell(name,f,x,y,w,h,tint){
 // The refitted hull is a complete 128-cell, not this retired 120x144 atlas.
 // Route its normal and flash layers through the same authored pose owner.
 if(name==='jet'&&typeof AF21!=='undefined'&&AF21.currentEnemy&&AF21.requestPose){
  const e=AF21.currentEnemy,p=AF21.requestPose,d=AIR13.aliases.get(e.type),span=Math.max(e.w||32,e.h||32)*(d?.nativeRatios?.[e.type]||1);
  return af21Draw(p,x,y,span,1,tint||(e.flash>0?hitFlashColor(e):null));
 }''';assert old in s or new in s;changes[p]=s if new in s else s.replace(old,new)
if '--install' in sys.argv:
 for p,s in changes.items():
  b=backup/p.name
  if not b.exists():shutil.copy2(p,b)
  p.write_text(s,encoding='utf-8',newline='\n')
 target=R/'assets/game/levels/stage_08/enemies/animation_feedback_1023';target.mkdir(parents=True,exist_ok=True)
 for p in O.glob('*.webp'):shutil.copy2(p,target/p.name)
 shutil.copy2(O/'manifest.json',target/'manifest.json')
 for n in ['animation_feedback_art_1023.js','animation_feedback_1023.js']:shutil.copy2(O/n,R/'assets'/n)
 p=R/'index.html';data=p.read_bytes();b=backup/'index.html'
 if not b.exists():shutil.copy2(p,b)
 if b'animation_feedback_1023.js'not in data:
  nl=b'\r\n'if b'\r\n'in data else b'\n';data=data.replace(b'</body>',b'<script src="assets/animation_feedback_art_1023.js?v=aq23-1"></script>'+nl+b'<script src="assets/animation_feedback_1023.js?v=aq23-1"></script>'+nl+b'</body>')
 data=data.replace(b'assets/air_motion_1013.js?v=combat-revision-1017',b'assets/air_motion_1013.js?v=animation-audit-1023').replace(b'assets/encounters_0930.js"',b'assets/encounters_0930.js?v=animation-audit-1023"');p.write_bytes(data)
 print(json.dumps({'installed':True,'fixedFleetTypes':len(models),'geometryFixes':2}))
else:print(json.dumps({'prepared':True,'fleetTypes':list(models),'geometryFixes':2}))
