from pathlib import Path
from PIL import Image,ImageDraw
import json,math
W=Path(__file__).parent/'BOF-Cinema-Rebuild';D=W/'consistency_1021'
# Exact authored garment selections, excluding neighbouring pilots.
parts={
 'hq_regroup':[('freezer','purple',[(334,138),(349,132),(363,138),(373,155),(374,181),(367,204),(330,204),(325,179),(327,154)])],
 'forge_upgrade':[('cole','green',[(58,170),(77,170),(97,174),(119,190),(131,220),(120,246),(119,282),(126,310),(116,383),(61,383),(58,343),(52,305),(58,271),(53,250),(40,226),(39,197)])],
 'hq_alarm':[('cole','green',[(199,177),(214,174),(228,177),(242,184),(260,181),(267,184),(258,191),(241,194),(231,206),(231,227),(220,242),(225,271),(215,294),(211,307),(204,306),(208,280),(204,254),(198,252),(192,275),(187,295),(177,295),(180,284),(182,256),(185,230),(178,217),(182,190)]),
  ('maverick','olive',[(409,176),(422,171),(432,177),(441,183),(443,191),(435,195),(430,196),(430,212),(414,213),(405,199),(396,199),(397,188),(404,185)])],
 'hq_river':[('cole','green',[(105,192),(131,188),(154,194),(169,202),(178,216),(187,227),(202,234),(199,254),(180,255),(174,246),(171,278),(165,305),(169,336),(160,383),(99,383),(94,354),(98,319),(99,290),(91,266),(76,244),(77,219),(91,202)]),
  ('freezer','purple',[(201,193),(211,191),(220,196),(225,208),(224,224),(199,224),(195,211)])],
 'launch_generator':[('cole','green',[(148,70),(162,66),(176,71),(183,83),(181,99),(183,110),(178,127),(175,149),(177,180),(166,185),(164,162),(160,132),(153,132),(151,156),(149,185),(139,189),(139,173),(142,143),(140,119),(133,107),(132,91),(139,77)])],
 'power_cell':[('cole','green',[(511,217),(528,215),(542,223),(553,235),(558,259),(554,285),(549,298),(554,321),(551,347),(555,376),(542,378),(536,364),(535,341),(526,313),(518,316),(512,345),(512,369),(502,381),(492,379),(495,370),(499,339),(502,305),(505,284),(500,263),(483,256),(469,242),(468,233),(477,228),(491,239),(506,242)])]
}
def color(rgb,kind):
 r,g,b=rgb;lum=.2126*r+.7152*g+.0722*b
 if lum<19 or lum>126 or b>g*1.75+6:return None
 if kind=='purple' and r>g*1.28+4:return None
 if kind!='purple' and lum>80 and r>g*1.35+4:return None
 # Keep near-white steel highlights, warm skin/fur, black outlines and bright UI.
 if lum>102 and max(rgb)-min(rgb)<20:return None
 if kind=='purple':
  c=lum*.65+8;rr=lum+.45*c;bb=lum+1.56*c
 elif kind=='green':
  c=lum*.65+8;rr=lum-.60*c;bb=lum-.40*c
 else:
  c=lum*.45+8;rr=lum+.05*c;bb=lum-.75*c
 gg=(lum-.2126*rr-.0722*bb)/.7152
 out=tuple(round(max(0,min(255,v))) for v in (rr,gg,bb))
 return out if out!=rgb else None
out={}
for shot,items in parts.items():
 im=Image.open(D/(shot+'-before.png')).convert('RGB');changes=[];stats=[]
 for name,kind,points in items:
  mask=Image.new('1',im.size);ImageDraw.Draw(mask).polygon(points,fill=1)
  colors={}
  for old in set(im.getdata()):
   new=color(old,kind)
   if new:colors['#%02x%02x%02x'%old]='#%02x%02x%02x'%new
  key=name+'_'+kind
  changes.extend([{'operation':'select_mask','layer':'image','frames':[1],'name':key,'selector':{'kind':'polygon','points':points},'reason':'Observed '+name+' garment in '+shot+'; preserve surrounding pilots, skin, hair and geometry.'},
   {'operation':'map_colors','layer':'image','frames':[1],'mask':key,'region':[0,0,687,383],'colors':colors,'reason':'Match '+name+' canonical '+kind+' jacket ramp; retain original luminance, alpha, outlines and motion.'}])
  stats.append({'pilot':name,'color':kind,'ramp_entries':len(colors)})
 if shot=='launch_generator':
  # Foreground catwalk rails cross in front of the actor, so keep those source pixels.
  props=[[(126,117),(207,129),(207,133),(126,121)],[(131,139),(194,149),(194,153),(131,143)],[(164,125),(168,125),(168,194),(164,194)],[(136,122),(139,122),(139,158),(136,158)]]
  for j,points in enumerate(props):
   key='rail_'+str(j)
   changes.extend([{'operation':'select_mask','layer':'image','frames':[1],'name':key,'selector':{'kind':'polygon','points':points},'reason':'Foreground metal rail must retain its original material.'},
    {'operation':'copy_region','layer':'image','frames':[1],'source_layer':'image','source_frame':1,'region':[120,110,215,200],'at':[120,110],'mask':key,'reason':'Restore exact original foreground catwalk rail pixels after the garment swap.'}])
 out[shot]={'changes':changes,'stats':stats}
(D/'palette-decisions.json').write_text(json.dumps(out),encoding='utf-8')
print(json.dumps(out))
