"""Generate the requested coherent stage 2/6/9 aircraft, using inspected game art."""
from pathlib import Path
import concurrent.futures,json,re,sys
from pixellab_mcp import PixelLab
from pixellab_intro_1021 import upload
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/biome_roster_1022'
def txt(r):return '\n'.join(x.get('text','') for x in r.get('content',[]) if x.get('type')=='text')
identities={
 'magma_small':'Small agile MAGMA INTERCEPTOR jet. Obsidian black basalt armor, glowing orange molten fissures INSIDE the metal armor, deep crimson wing edges, white-hot small thrusters. Sharp compact swept wings, pointed nose, two clearly visible nose cannon ports. This is a lava-powered military aircraft, not a creature or loose flame.',
 'magma_large':'Large heavy MAGMA BOMBER jet. Broad obsidian black armored swept wings, two huge cylindrical molten-orange reactors, crimson armored engine housings, white-hot exhaust at the rear, visibly substantial cannon barrels at the front and two missile launch bays. Heavy lava-powered military aircraft, broad and imposing, coherent with the small magma interceptor.',
 'sky_small':'Small agile SKY DART interceptor. White ceramic and cool light gray alloy hull, TEAL trim and teal engine lights. Sharp narrow swept wings, compact elegant fuselage, two small forward guns, two rear turbine exhausts. Wind-powered aircraft, crisp military mechanical structure. No yellow, red, royal blue or black-ice livery.',
 'sky_medium':'Medium SKY GALE fighter. White ceramic and gray alloy hull, TEAL trim and turbine lights. Distinct broad curved swept wings with two circular turbine intakes in the wing roots, twin nose cannons and two rear teal exhaust ports. Wind-powered aircraft, balanced and aerodynamic, same fleet family as the sky dart. No yellow, red or royal blue.',
 'sky_large':'Large SKY TEMPEST bomber jet. White ceramic, light and dark gray armor panels, TEAL trim and engine lights. Huge broad swept wings, four circular wind turbine engines and a thick central fuselage, two heavy forward cannon barrels and paired missile pods. Same fleet family as smaller sky dart/gale, substantial mechanical aircraft, no yellow, red or royal blue.',
 'water_small':'Small WATER RIPTIDE interceptor jet, manta-like swept wings but clearly a mechanical aircraft. Deep navy armor, azure cobalt panels, aqua cyan glowing channels, pale pearl highlights. Two forward water-pressure cannon ports, twin rear aqua engine nozzles. Sleek narrow nose. Aquatic powered fighter, no purple void effects, no stone, no tank treads.',
 'water_medium':'Medium WATER UNDERTOW fighter jet, clearly mechanical ocean-powered aircraft with broad hydrofoil-shaped wings and a circular aqua pressure turbine in the fuselage. Navy and cobalt blue armor, cyan water channels, pearl white highlights. Two forward cannons, two rear aqua nozzles, distinct readable metal silhouette. No purple void, no ground treads.',
 'water_large':'Large WATER ABYSS gunship jet. Broad heavy mechanical manta-shaped armored wings, two large cylindrical pressure turbines, four forward cannon ports, twin missile launch bays, rear cyan jet nozzles. Navy/cobalt alloy with cyan liquid channels and pearl highlights. Same aquatic fleet identity as riptide and undertow. Aircraft only, no creature, no purple void or ground vehicle.'}
def start(name):
 p=D/(name+'-job.json')
 if p.exists() and not json.loads(p.read_text()).get('isError'):return
 c=PixelLab()
 try:
  raw=txt(c.call('get_upload_url',{}));url=re.search(r'https://[^\s"<>]+',raw).group(0)
  ref=upload(c,D/'references'/(name+'.png'),url)
  args=dict(width=192,height=192,no_background=True,seed=10222000+list(identities).index(name),description='FRAME FORMAT: 192 x192 transparent pixels. Fixed fuselage center pivot96,96, one common proportional scale, reserve at least20 pixels clear transparent margin on all sides. Crisp detailed 16/32-bit arcade pixel art, clean single-pixel outlines, sharp metallic shading. STRICT ORTHOGRAPHIC TOP VIEW looking directly down onto aircraft. Nose points straight DOWN toward bottom edge, rear engines at top. Symmetrical wings, never diagonal or isometric. One complete aircraft centered and uncropped, no background or shadow plate, no text, no external bullets or muzzle flash. '+identities[name],reference_images=[dict(url=ref,usage='Existing Bullets of Fury arcade art style and top-down aircraft proportions. Recreate as the requested themed fleet; preserve clean detailed arcade pixel art, not generic smooth vector or photoreal art.')])
  r=c.call('create_image_pro',args);p.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(dict(name=name,error=r.get('isError',False),receipt=txt(r)[:300])),flush=True)
 finally:c.close()
if __name__=='__main__':
 names=sys.argv[1:] or list(identities)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(start,names))
