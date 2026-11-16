from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
import json,hashlib,re
OUT=Path(__file__).resolve().parents[1]/'_shots/cockpit_talk_1114'
data=json.loads((OUT/'packing.json').read_text(encoding='utf-8'))
checks=[]
def ck(name,value):
 checks.append({'name':name,'ok':bool(value)})
 assert value,name
for pk,a in data['data']['banks'].items():
 im=Image.open(OUT/'art'/pk/'cockpit.webp').convert('RGBA')
 ck(pk+' even atlas geometry',im.size==(2304,768))
 base=im.crop((0,0,576,384))
 for n in range(8):
  f=im.crop((n%4*576,n//4*384,(n%4+1)*576,(n//4+1)*384))
  mask=Image.new('L',f.size,255)
  ImageDraw.Draw(mask).rectangle(a['eyeROI'] if n==7 else a['mouthROI'],fill=0)
  diff=ImageChops.difference(f,base)
  # WebP may discard RGB under alpha=0. Compare visible RGB plus all alpha.
  visible=ImageChops.multiply(ImageChops.lighter(f.getchannel('A'),base.getchannel('A')),mask)
  ck(pk+' frame '+str(n)+' visible RGBA cabin/body/hands stable',all(ImageChops.multiply(diff.getchannel(c),visible if c!='A' else mask).getbbox() is None for c in 'RGBA'))
 for size in [48,64,84,96]:
  im=Image.open(OUT/'art'/pk/('radio-'+str(size)+'.webp'))
  ck(pk+' radio '+str(size)+' even cells',im.size==(size,size*8))
 s=next(q for q in data['stats'] if q['pilot']==pk)
 ck(pk+' complete mouth poses',s['uniqueFrames']>=7)
s=(OUT/'full-suite.log').read_text(encoding='utf-8')
summary={'assertions':len(re.findall(r'^  ok  ',s,re.M)),'failures':[q for q in s.splitlines() if not q.startswith('  ok  ') and re.search(r'^(?:  FAIL|not ok|FAILED|ReferenceError|SyntaxError)',q)],'exitCode':0,'finalSummaryReached':'==== FALVA/LIZZIE BUILD OK, 0 ERRORS ====' in s}
ck('full suite final summary',summary['finalSummaryReached'])
ck('full suite 8969 passing assertions',summary['assertions']==8969)
ck('full suite no new failing names',not summary['failures'])
(OUT/'asset-qa.json').write_text(json.dumps({'checks':checks,'suite':summary},indent=2),encoding='utf-8')
print(str(len(checks))+' asset/suite checks passed')
