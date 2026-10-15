"""Export inspected production crops; no painting, recoloring or per-frame fitting.

Generated masters are preserved. One scale per bank, even output frames, explicit
source rectangles and physical mounting pivots. These loose banks own their JS.
"""
from pathlib import Path
from PIL import Image
import json,hashlib
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'expansion/topdown/art/menu_1011'

def save_doc(out,name,doc):
 (out/'manifest.json').write_text(json.dumps(doc,indent=2),encoding='utf-8',newline='\n')
 (out/'manifest.js').write_text('(function(root){root.'+name+'='+json.dumps(doc,separators=(',',':'))+';})(window);\n',encoding='utf-8',newline='\n')

def main():
 assets={};sources={}
 def bank(file,keys,rects,size,scale=1):
  src=OUT/'source'/file;im=Image.open(src).convert('RGBA');sources[file]={'size':list(im.size),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'uniformScale':scale}
  if scale!=1:im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
  for key,rect in zip(keys,rects):
   x,y,w,h=rect;assert w==size[0] and h==size[1] and w%2==h%2==0
   frame=im.crop((x,y,x+w,y+h));frame.save(OUT/(key+'.png'))
   assets[key]={'file':'expansion/topdown/art/menu_1011/'+key+'.png','size':size,'anchor':[w//2,h//2],'source':file,'sourceCrop':rect,'uniformScale':scale}
 # The generated revision intentionally reordered several labels. Register
 # the artwork we inspected, rather than assuming the prompt's requested order.
 keys=['new_game','continue','options','password','achievements','help','resume','armory','credits','exit_game','apply','cancel']
 bank('buttons_final.png',['od_btn_'+k for k in keys],[[i%2*768,64+i//2*152,768,152] for i in range(12)],[768,152])
 bank('missing_buttons_1011.png',['od_btn_'+k for k in ['return_to_main_menu','fullscreen','windowed','locked']],[[0,204,768,192],[768,204,768,192],[0,620,768,192],[768,620,768,192]],[768,192])
 keys=['easy','normal','hard','furious','insanity','sound','controls','passwords']
 bank('difficulty.png',['od_diff_'+k for k in keys],[[i%2*768,64+i//2*224,768,224] for i in range(8)],[768,224])
 # Mike's correction: restore the original Insanity plate, and give Furious
 # its own chaotic melting skull. Keep the old generated master as provenance.
 # Separate authored sources share a 768x224 export canvas and center pivot.
 revisions=[
  ('furious','furious_melting_1011.png',[8,45,2078,588],'melting_1011'),
  ('insanity','insanity_original_0916.png',[0,0,199,58],'original_1011'),
 ]
 for label,file,rect,suffix in revisions:
  src=OUT/'source'/file;im=Image.open(src).convert('RGBA');x,y,w,h=rect
  assert x>=0 and y>=0 and x+w<=im.width and y+h<=im.height
  crop=im.crop((x,y,x+w,y+h))
  # Add transparent right/bottom padding to measured odd source dimensions.
  padded=Image.new('RGBA',(w+w%2,h+h%2));padded.paste(crop,(0,0))
  scale=min(736/padded.width,208/padded.height)
  scaled=padded.resize((round(padded.width*scale),round(padded.height*scale)),Image.Resampling.NEAREST)
  frame=Image.new('RGBA',(768,224));offset=((768-scaled.width)//2,(224-scaled.height)//2);frame.paste(scaled,offset)
  filename='od_diff_'+label+'_'+suffix+'.png';frame.save(OUT/filename)
  sources[file]={'size':list(im.size),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'uniformScale':scale,'role':'original BOF plate' if label=='insanity' else 'built-in image_gen melting-skull edit'}
  assets['od_diff_'+label]={'file':'expansion/topdown/art/menu_1011/'+filename,'size':[768,224],'anchor':[384,112],'source':file,'sourceCrop':rect,'sourcePadding':list(padded.size),'paddingOffset':list(offset),'uniformScale':scale}
 bank('controllers.png',['od_controller_six','od_controller_modern'],[[0,64,768,640],[768,64,768,640]],[768,640])
 im=Image.open(OUT/'source/achievements.png')
 assert im.width==im.height
 bank('achievements.png',['od_ach_'+str(i) for i in range(16)],[[i%4*256,i//4*256,256,256] for i in range(16)],[256,256],1024/im.width)
 general=OUT/'source/general.png'
 if general.exists():
  im=Image.open(general);assert im.width==im.height
  bank('general.png',['od_general_'+str(i) for i in range(4)],[[i%2*256,i//2*256,256,256] for i in range(4)],[256,256],512/im.width)
 save_doc(OUT,'TD_UI_ART',{'assets':assets,'sources':sources,'frameFormat':'even fixed canvases; one proportional scale and center pivot per bank'})
 # A different bank owns the new original HK-inspired Warrior. The old bank
 # remains intact. Each module is cropped around its measured physical mount.
 out=ROOT/'expansion/topdown/art/warrior_mk2_1011';src=out/'source/warrior_final.png';im=Image.open(src).convert('RGBA');assert im.size==(1536,1024)
 # key, source rectangle, physical source mount, fixed output size/pivot
 crops=[
  ('warrior_hull',[32,72,554,440],[309,206],[640,512],[320,180]),
  ('warrior_helmet',[590,64,456,432],[829,480],[512,512],[256,432]),
  ('warrior_arm_l',[24,570,468,390],[446,721],[512,512],[450,176]),
  ('warrior_arm_r',[1056,104,470,378],[1106,220],[512,512],[62,176]),
  ('warrior_damaged',[490,544,556,432],[780,683],[640,512],[320,180]),
  ('warrior_wreck',[1046,548,482,442],[1290,718],[640,512],[320,180]),
 ]
 wa={}
 for key,rect,mount,size,pivot in crops:
  x,y,w,h=rect;frame=Image.new('RGBA',size);offset=(pivot[0]-(mount[0]-x),pivot[1]-(mount[1]-y));frame.paste(im.crop((x,y,x+w,y+h)),offset);frame.save(out/(key+'.png'))
  bounds=frame.getchannel('A').point(lambda a:255 if a>=80 else 0).getbbox()
  wa[key]={'file':'expansion/topdown/art/warrior_mk2_1011/'+key+'.png','size':size,'anchor':pivot,'bounds':list(bounds),'sourceCrop':rect,'sourceMount':mount,'paddingOffset':list(offset)}
 rig={
  'hull':{'key':'warrior_hull','x':0,'y':0,'hx':0,'hy':0,'r':112,'scale':.52,'baseAngle':0},
  'helmet':{'key':'warrior_helmet','x':0,'y':0,'hx':0,'hy':-108,'r':52,'scale':.4,'mx':0,'my':-98},
  'armL':{'key':'warrior_arm_l','x':-84,'y':-82,'hx':-187,'hy':-27,'r':43,'scale':.33,'mx':-185,'my':-13},
  'armR':{'key':'warrior_arm_r','x':84,'y':-82,'hx':185,'hy':-24,'r':43,'scale':.33,'mx':186,'my':-11}}
 save_doc(out,'TD_WARRIOR_ART',{'tool':'built-in image_gen','master':'source/warrior_final.png','sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'frameFormat':'chassis 640x512; torso/arms 512x512; physical pivots stable per module bank','spawnYOffset':-28,'assets':wa,'rig':rig})
 print(f'{len(assets)} menu frames and 6 Warrior modules exported with even canvases')
if __name__=='__main__':main()
