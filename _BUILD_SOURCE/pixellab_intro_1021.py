"""Requested intro art through PixelLab; credentials never leave its MCP client."""
from pathlib import Path
import sys,json,re,urllib.request,uuid,concurrent.futures
from PIL import Image
from pixellab_mcp import PixelLab,unpack
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/intro_repair_1021';D.mkdir(exist_ok=True)

def content(v):return '\n'.join(c.get('text','') for c in v.get('content',[]) if c.get('type')=='text')
def upload(client,path,url):
 data=path.read_bytes();boundary='bof'+uuid.uuid4().hex
 body=('--'+boundary+'\r\nContent-Disposition: form-data; name="file"; filename="reference.png"\r\nContent-Type: image/png\r\n\r\n').encode()+data+('\r\n--'+boundary+'--\r\n').encode()
 req=urllib.request.Request(url,data=body,headers={'Content-Type':'multipart/form-data; boundary='+boundary},method='POST')
 with urllib.request.urlopen(req,timeout=60) as response:q=json.loads(response.read())
 return q['ref']
def start(name,tool,args):
 c=PixelLab();v=c.call(tool,args);(D/(name+'-job.json')).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8');c.close()
 print(json.dumps({'bank':name,'result':content(v)[:1600],'error':v.get('isError',False)}),flush=True);return v
if __name__=='__main__':
 c=PixelLab();raw=content(c.call('get_upload_url',{}));url=re.search(r'https://[^\s"<>]+',raw).group(0)
 refs={}
 for name in ['cin_federation_station_1','cin_origin_tower','cin_pilot_lizzie_open','cin_pilot_decker_open','dp20_dracodia_portrait','nbl_logo_0916']:
  im=Image.open(D/'references'/(name+'.png')).convert('RGBA');scale=min(1,512/max(im.size));size=(round(im.width*scale),round(im.height*scale));im=im.resize(size,Image.Resampling.NEAREST);a=Image.new('RGBA',(size[0]+size[0]%2,size[1]+size[1]%2));a.paste(im,(0,0));path=D/'references'/(name+'-input.png');a.save(path);refs[name]=upload(c,path,url)
 (D/'upload-refs.json').write_text(json.dumps(refs,indent=2)+'\n',encoding='utf-8');c.close()
 station=dict(description='FRAME FORMAT: 256 x 256 pixel transparent sprite, fixed canvas pivot128,128 and one proportional scale. Improve the supplied actual Fury communications satellite in detailed Bullets of Fury arcade pixel art. Preserve its recognizable three dishes, central cylindrical relay, white eagle insignia, two rectangular side solar decks, cyan illuminated belt and lower engine. Rich dark chromium panels, sharp bright metallic bevels, tiny antennae and orange warning lamps. Intact healthy satellite before invasion. Three-quarter top-down space view, same silhouette and perspective as reference, full object centered with transparent margin for future alien tendrils. No text or extra objects.',width=256,height=256,no_background=True,reference_images=[{'url':refs['cin_federation_station_1'],'usage':'actual Fury satellite identity, geometry and palette'}],seed=102101)
 dispatch=dict(description='FRAME FORMAT: 512 x 288 pixels, fixed cinematic canvas and camera. Detailed Bullets of Fury arcade pixel-art scene. Lizzie and Decker at their dispatch consoles in the supplied observation tower, concerned and speaking into headsets while city warning lights flicker through the windows. Clearly show both faces in three-quarter side view and hands at controls, waist-up. LEFT Decker has the exact supplied blond swept hair, black rectangular glasses, slim young face, black flight jacket with yellow piping. RIGHT Lizzie has the exact supplied long curly auburn hair, warm tan skin and yellow flight jacket over black shirt. Preserve both identities, no generic military operators. Wide composition, twilight city outside, red alert lamps, cyan screens. Empty bottom quarter clear for separately drawn game dialogue. No letters, captions, logos, weapons, visible aircraft or UI frame.',width=512,height=288,no_background=False,reference_images=[{'url':refs['cin_origin_tower'],'usage':'tower room and window scene composition only; replace the generic operators'},{'url':refs['cin_pilot_decker_open'],'usage':'Decker exact face, blond hair, rectangular glasses and black-yellow outfit'},{'url':refs['cin_pilot_lizzie_open'],'usage':'Lizzie exact face, curly auburn hair and yellow-black outfit'}],seed=102102)
 effect=dict(description='FRAME FORMAT: 256 x 128 transparent pixels, fixed pivot128,64 with wide transparent margins. Bullets of Fury arcade logo reveal EFFECT ONLY: a sharp white-cyan electrical flash with fiery orange sparks and blue plasma streaks sweeping horizontally around a mostly empty center. Use the supplied logo only for its metallic arcade lighting and fiery cyan-orange palette. Do NOT reproduce or invent any text or logo; the actual unchanged game logo is composited separately. Crisp authored pixel-art lightning branches and scattered sparks, silhouette unclipped, transparent background, no rectangle, no blur.',width=256,height=128,no_background=True,reference_images=[{'url':refs['nbl_logo_0916'],'usage':'palette and metallic arcade light only; generate effect only, NO logo or text'}],seed=102103)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for future in [pool.submit(start,n,'create_image_pro',a) for n,a in [('satellite',station),('dispatch-seated',dispatch),('logo-fx',effect)]]:future.result()
