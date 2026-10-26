from pathlib import Path
import json,re,sys
from pixellab_mcp import PixelLab
from pixellab_intro_1021 import upload
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/stage59_1024';D.mkdir(exist_ok=True)
def txt(r):return '\n'.join(x.get('text','') for x in r.get('content',[]) if x.get('type')=='text')
c=PixelLab()
try:
 raw=txt(c.call('get_upload_url',{}));url=re.search(r'https://[^\s"<>]+',raw).group(0)
 ref=upload(c,D/'references/black-3.png',url)
 plan={'warp':('create_image_pro',dict(width=256,height=256,no_background=False,seed=10224001,description='FRAME FORMAT:256x256 pixels, one common scale and fixed vanishing point128,128. Full-frame opaque cinematic WATER WARP SPEED tunnel for a premium 16/32-bit arcade space shooter. Flying at extreme speed down the center of a deep navy and cobalt water vortex through a portal. Intense cyan white foam streaks rush from a small bright distant central vanishing point toward every outer edge; spiral liquid walls form concentric curling wave ribs, tiny bubbles and refracted aquamarine light. Strong depth and spectacular watery hyperspace speed, crisp authored pixel-art texture with rich metallic-arcade shading, no ship, characters, text, black border, horizon or stars. Entire square filled by the rushing underwater warp tunnel, all four edges carry streaming watery light.'))}
 header='FRAME FORMAT:256x256 transparent pixels, fixed central cyan EYE pivot128,128 throughout, common proportional scale and full-wing transparent margins. Exact supplied BLACK/dark charcoal mechanical flying eye, same black crescent wings, long pointed spine, cyan circular central eye, crisp authored pixels and dark metal highlights. One whole identical aircraft, no new parts, no additional effects or projectiles. '
 for name,motion,count in [('drift','Subtle controlled banking left then right while flying; wings pitch in depth around the unmoving central eye, the visible armor stays exactly the same. Begin/end with supplied front pose, no translation or zoom.',8),('spin','A complete fluid 360-degree clockwise spin around the fixed central eye in the image plane. The whole black crescent-wing aircraft turns through every orientation and returns to its exact supplied upright pose. Preserve the exact silhouette, no morphing, no vanishing, no extra objects.',16),('charge','The central cyan EYE brightens and charges a tightly contained white-cyan light INSIDE its lens while mechanical eyelid panels open slightly, wings brace outward subtly. Hold a visibly charged eye then relax. No laser ray baked into the sprite, no external aura or circles.',8)]:
  plan['black_'+name]=('animate_image_pixminimax',dict(first_frame_url=ref,last_frame_url=ref,frame_count=count,no_background=True,seed=10224010+count+len(name),description=header+motion,subject_description='the supplied black crescent-wing mechanical aircraft with a cyan central eye',initial_pose='upright complete black winged aircraft, central eye fixed at128,128',view='high top-down',direction='south'))
 names=sys.argv[1:] or list(plan)
 for n in names:
  p=D/(n+'-job.json')
  if p.exists() and not json.loads(p.read_text()).get('isError'):continue
  tool,args=plan[n];r=c.call(tool,args);p.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(dict(bank=n,error=r.get('isError',False),receipt=txt(r)[:180])),flush=True)
finally:c.close()
