"""PixelLab-owned Dracodia additions; credentials and signed URLs stay private."""
from pathlib import Path
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
import argparse,base64,json,re,shutil,urllib.request
from PIL import Image
from pixellab_mcp import PixelLab,unpack
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/dracodia_archive_1018'
S.mkdir(parents=True,exist_ok=True)
def write(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
def ids(obj):
 if isinstance(obj,str):
  match=re.search(r'(?:job_id|\bid)\s*[:=]\s*["\']?([a-f0-9-]{36})',obj)
  return match.group(1) if match else None
 if isinstance(obj,dict):
  for k,v in obj.items():
   if k in ['job_id','id'] and isinstance(v,str) and len(v)==36:return v
  for v in obj.values():
   r=ids(v)
   if r:return r
 if isinstance(obj,list):
  for v in obj:
   r=ids(v)
   if r:return r
 return None
refs={
 'bastion':Path(r'C:/Users/Mdogg/Desktop/Coding Files - AI Game Development/BOF-V0.8/assets/enemies/bosses/bz0_inta.png'),
 'camo':Path(r'C:/Users/Mdogg/Desktop/Coding Files - AI Game Development/BOF-V0.8/assets/enemies/bosses/bz4_inta.png'),
 'halberd':Path(r'C:/Users/Mdogg/AppData/Local/Temp/codex-clipboard-08e44916-3654-4e46-8637-6e0970fce420.png')}
header='RESOLUTION FIRST: one 256x256 RGBA sprite, fixed canvas and center pivot 128,128, even dimensions. Center all physical mass with 24px transparent padding. Bullets of Fury Neo-Geo arcade pixel art, sharp clusters, mechanical volume, dark outlines and bright readable details. No text, labels, UI, scenery or checkerboard. '
prompts={
 'bastion':header+'Regenerate the supplied IRON BASTION old boss as the same recognizable olive angular warship, central armored spine and paired purple missile batteries. Preserve the silhouette, palette, facing and distinctive armor; improve readable gun pods and mechanical shading. Top-down enemy warship, two clearly separated side weapon assemblies attached to the core. Purple ordnance remains purple. Black in reference is empty background. Transparent background.',
 'camo':header+'Regenerate the supplied CAMO COLOSSUS old boss as the same recognizable olive spiked armored warship, central long spindle and paired red munition batteries, organic thorn-like wing edges. Preserve its silhouette, palette, facing and distinctive armor. Top-down enemy warship with two clearly separated side weapon assemblies attached to the core. Red ordnance remains red. Black in reference is empty background. Transparent background.',
 'halberd':header+'Regenerate the supplied BLUE ARCHIVE GUNSHIP, an old wide fortress gunship. Preserve its very broad rectangular blue-gray armor wings, paired small bottom gun barrels and enormous central downward cannon with a bright muzzle, rivets and vents. Straight top-down, enemy guns aimed toward bottom of image. Keep it broad, not a triangular jet. Ignore all checkerboard, blue strip and screenshot margins. Two clearly separated side weapon assemblies attached to core. Transparent background.',
 'bomb':header.replace('256x256','128x128').replace('128,128','64,64').replace('24px','16px')+'A powerful floating corrupted CODE BOMB: compact black chromium sphere/cube hybrid, segmented purple armored shell around a bright radioactive emerald reactor, tiny luminous binary glyph fragments cut into its armor, dangerous symbiote hooks, white hot pixel highlights. One solid volume, readable silhouette. No large halo, no trail. Transparent background.',
 'lightning':header.replace('256x256','128x128').replace('128,128','64,64').replace('24px','16px')+'One curling spiraling lightning projectile: a compact electric crescent with a bright blue-white jagged core, deep cobalt and violet sparks, a sharp curved forked tail. This is a small fast dangerous lightning curl, not a full ring, icon, laser beam, or orb. Keep all art inside a centered 88px footprint. Transparent background.',
 'transfer':header+'A standalone digital materialization VFX, no ship or actor: small emerald binary square fragments fall in vertical data columns around two bright scanning bars. A narrow center pool of white green energy and many scattered rectangular pixel blocks, dark teal shadows, sharp arcade pixel clusters. Empty transparent background, no frame, ground, circle, scenery or readable lettering.',
 'storm':header+'A subtle background void-storm effect plate: dark violet-black turbulent symbiote vapor curling around scattered green circuit sparks and faint floating code shards. Mostly empty transparent center for readable bullets, wispy dim outer turbulence, no frame, walls, tunnel or hard sides. This will be a low-opacity parallax layer behind a space boss, no ships, characters or scenery. Transparent background.'}
def request(client,name,tool,args,count,jobs):
 cached=S/'jobs'/(name+'.json')
 result=json.loads(cached.read_text()) if cached.exists() else client.call(tool,args)
 if result.get('isError') and 'rate limit exceeded' in json.dumps(result).lower():
  write(S/'jobs'/(name+'-rate-limit.json'),result)
  result=client.call(tool,args)
 write(cached,result)
 if result.get('isError'):raise RuntimeError('PixelLab rejected '+name)
 job=ids(unpack(result))
 if not job:raise RuntimeError('No job ID for '+name)
 jobs[name]=dict(id=job,count=count,tool=tool);write(S/'jobs.json',jobs);print('Queued '+name+' ('+str(count)+' frames)',flush=True)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['seeds','poll','animate']);a=ap.parse_args();client=PixelLab();jobs=json.loads((S/'jobs.json').read_text()) if (S/'jobs.json').exists() else {}
 if a.mode=='seeds':
  write(S/'prompts.json',prompts)
  for name,prompt in prompts.items():
   if name in jobs:continue
   args=dict(description=prompt,width=128 if name in ['bomb','lightning'] else 256,height=128 if name in ['bomb','lightning'] else 256,no_background=True)
   if name in refs:
    ref=S/'refs'/(name+'.png');ref.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(refs[name],ref)
    args['reference_images']=[dict(base64=base64.b64encode(ref.read_bytes()).decode(),usage='Exact old boss identity, shape, palette and facing; regenerate its pixels while preserving the design.')]
   request(client,name,'create_image_pro',args,1,jobs)
 elif a.mode=='poll':
  for name,j in jobs.items():
   expected=j['count']+(j['count']>1);dest=S/'returned'/name
   if all((dest/f'frame_{i:03}.png').exists() for i in range(expected)):continue
   result=client.call('get_image',dict(job_id=j['id']));write(S/'jobs'/(name+'-status.json'),result);info=unpack(result)
   summary=json.dumps(info).lower();done='completed' in summary or 'download' in summary
   if result.get('isError') or not done:print(name+': waiting',flush=True);continue
   dest.mkdir(parents=True,exist_ok=True)
   def download(i):
    out=dest/f'frame_{i:03}.png'
    if out.exists():return
    url=f"https://api.pixellab.ai/mcp/images/{j['id']}/download?index={i}"
    with urllib.request.urlopen(url,timeout=55) as response:data=response.read()
    if not data.startswith(b'\x89PNG'):raise RuntimeError('Not PNG: '+name)
    out.write_bytes(data)
   with ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(download,range(expected)))
   print(name+': downloaded',flush=True)
 elif a.mode=='animate':
  motion={
   'bastion_download':('bastion','The intact ship digitally DISASSEMBLES: green scan bars pass over it, individual armor plates fragment into glowing binary blocks and stream upward, leaving scattered tiny green and purple code pixels, then only sparse isolated pixels. Camera and ship center stay completely fixed, no flight, rotation, zoom or extra objects. Body identity remains recognizable until dissolved.'),
   'camo_download':('camo','The intact ship digitally DISASSEMBLES: green scan bars pass over it, individual thorn armor plates and red batteries fragment into luminous binary blocks and stream upward, leaving sparse green and red code pixels. Fixed camera and immutable centered ship, no rotation, flight or zoom. Preserve its physical identity.'),
   'halberd_download':('halberd','The intact broad gunship digitally DISASSEMBLES: green scan bars pass over it, blue metal wing panels fragment into luminous binary blocks and rise upward in orderly data columns, ending in sparse blue and green pixels. Completely fixed camera, size, center and identity. No flight, rotation or zoom.'),
   'transfer_loop':('transfer','Data blocks rain downward in broken streams while bright emerald scan bars sweep top to bottom, data fragments burst outward then converge, white-green pixels flicker at assembly points. A seamless animated digital download field, centered on fixed transparent canvas with no ship, character, floor, frame or camera motion.'),
   'bomb_burst_v2':('bomb','A SINGLE explosive detonation: the casing shatters immediately into many irregular chrome fragments, a dense emerald-white PLASMA CLOUD balloons outward, violet-black curling turbulent smoke, organic green fire tendrils and tiny binary pixel embers. The initial flash is brief, then actual rolling energy volume and scattered fragments expand and fade to empty transparent air. No star shapes, straight pointed rays, geometric icons, circular glyph grids, reset, surviving bomb or camera movement. All fragments stay inside the canvas.'),
   'bomb_charge':('bomb','The same compact code bomb charges and pulsates in a seamless loop: green reactor flickers brighter, purple shell seams surge, small binary code sparks orbit close to the casing. Physical casing stays centered at exactly the same scale and pose, no translation, spin, extra bombs or background.'),
   'bomb_burst':('bomb','This code bomb explodes into a violent emerald white core flash, violet-black energy shockwave, fractured chrome casing fragments and thousands of little binary code sparks, then scattered fading green sparks. An actual compact pixel-art explosion expanding from the fixed center, all fragments stay in frame. Transparent background; no intact bomb remaining at the end, no scene or UI.'),
   'lightning_loop':('lightning','Seamless loop of this single curling lightning bolt crackling and forking rapidly, internal blue-white current travels along its curved tail and violet sparks flicker. Keep the same centered crescent silhouette, size, pivot and facing; no travel, zoom or extra projectiles.'),
   'storm_loop':('storm','Seamless slow swirling void turbulence: dark vapor curls circularly, dim green circuit sparks blink through it and code shards drift within the clouds. Preserve a mostly empty transparent center. No borders, walls, scenery, characters or camera motion.')}
  write(S/'motion-prompts.json',motion)
  for name,(source,prompt) in motion.items():
   if name in jobs:continue
   if not (S/'returned'/source/'frame_000.png').exists():print('Seed not ready: '+source,flush=True);continue
   url=f"https://api.pixellab.ai/mcp/images/{jobs[source]['id']}/download?index=0"
   args=dict(description=prompt,first_frame_url=url,frame_count=32,no_background=True,enhance_prompt=False,
    subject_description='a centered top-down arcade '+('mechanical warship' if source in refs else 'energy effect'),
    initial_pose='intact and centered, at a fixed scale',view='high top-down')
   if name.endswith('_download'):
    # A synthetic empty endpoint contains no private data and guarantees the
    # reverse sequence starts with empty air rather than a half-built hull.
    first=Image.open(S/'returned'/source/'frame_000.png');buf=BytesIO();Image.new('RGBA',first.size).save(buf,format='PNG');args['last_frame_base64']=base64.b64encode(buf.getvalue()).decode()
   request(client,name,'animate_image_pixminimax',args,32,jobs)
if __name__=='__main__':main()
