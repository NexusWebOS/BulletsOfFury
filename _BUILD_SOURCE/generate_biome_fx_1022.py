from pathlib import Path
import concurrent.futures,json,sys
from pixellab_mcp import PixelLab
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/biome_roster_1022'
themes={'magma':'Molten lava energy: brilliant ivory white-hot center, saturated orange and deep red flame lobes with tiny dark basalt sparks. Crisp arcade pixels.','sky':'Wind pressure energy: brilliant pearl white center, pale gray wind edges and TEAL curling air ribbons, no lightning bolts. Crisp arcade pixels.','water':'Water pressure energy: brilliant pearl white foam core, cyan aqua and cobalt blue liquid edges and tiny discrete droplets. Crisp arcade pixels.'}
forms={'muzzle':'A single circular energy MUZZLE FLASH viewed directly face-on, concentric expanding rings around an empty tiny center. Centered exactly96,96. Round compact symmetrical burst, effects only, no barrel, aircraft, weapon or symbols.', 'shot':'One compact elongated pointed ENERGY PROJECTILE facing DOWN, narrow tip at bottom, short clean tapering wake above. Center96,96. No circles around it, no huge trail, no ship or gun. Unambiguous bright projectile silhouette.', 'charge':'A single circular weapon CHARGE glow, viewed face-on with bright center and two thin curling concentric energy bands INSIDE a compact circle. Center96,96, restrained symmetrical charge; no aircraft, weapon or symbols.'}
def start(item):
 theme,kind=item;name=theme+'_'+kind;p=D/(name+'-job.json')
 if p.exists() and not json.loads(p.read_text()).get('isError'):return
 c=PixelLab()
 try:
  r=c.call('create_image_pro',dict(width=192,height=192,no_background=True,seed=10222100+list(themes).index(theme)*10+list(forms).index(kind),description='FRAME FORMAT:192 x192 transparent pixels, fixed physical pivot96,96, generous32pixel transparent margin, one common scale, crisp 16/32-bit arcade pixel-art special effect with distinct outlined pixels, absolutely no scenery or background plate. '+themes[theme]+' '+forms[kind]));p.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(dict(name=name,error=r.get('isError',False))),flush=True)
 finally:c.close()
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(start,[(t,k) for t in themes for k in forms]))
