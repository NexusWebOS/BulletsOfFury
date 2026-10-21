from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parents[1];O=R/'_shots/dracodia_phoenix_1020';S=R/'_ART_SOURCES/dracodia_phoenix_1020'
for name,folder,indices in [('pixellab-wing-charge','wing-charge',range(9)),('pixellab-muzzle','plume-motion',range(1,17)),('pixellab-beam','beam-motion-clean',range(1,17)),('pixellab-head-charge','head-charge',range(1,17))]:
 frames=[Image.open(S/folder/f'{i:02}.png').convert('RGBA') for i in indices];frames[0].save(O/(name+'.webp'),save_all=True,append_images=frames[1:],duration=85,loop=0,lossless=True)
base=(R/'_BUILD_SOURCE/build_dracodia_volcano_review_1019.py').read_text()
base=base.replace("_shots/dracodia_volcano_1019","_shots/dracodia_phoenix_1020").replace('Break the Volcano','Corrupted Fire Phoenix').replace('BREAK THE VOLCANO','CORRUPTED FIRE PHOENIX')
base=base.replace("Dracodia's volcano body now fights as an articulated machine.","A completely new, forward-facing PixelLab phoenix replaces Dracodia's angled volcano robot.")
base=base.replace('moving mechanical joints, attack-driven recoil and charging','jointed fire wings, molten feather volleys, charging furnace weapons')
base=base.replace('Two shoulder armor sections','Two wing-root armor sections').replace('two weapon arms','two furnace cannons').replace('Two exhaust chimneys','Two blade-feather wings').replace('two leg assemblies','two talon / fire-tail assemblies')
base=base.replace('Seventeen original sprite pieces, one reused mechanical bearing and sixteen PixelLab vent-flame frames. Fixed pivots and the original palette.','Seventeen lossless parts from the new PixelLab master, nine coordinated wing/charge poses, sixteen muzzle effects, sixteen molten beam frames and a new phoenix skull. Fixed physical pivots.')
base=base.replace('<img loading="lazy" src="vent-flame-sheet.png" alt="All sixteen PixelLab vent flame frames">','')
base=base.replace('Aiming shoulder, charging barrel, mechanical recoil, bracing legs and a flash at the real muzzle.','Twin furnace cannons charge, aim and recoil; PixelLab molten feathers launch from the visible muzzles.')
base=base.replace('A rotating shoulder and forearm carry the warning and sustained flame from the same nozzle.','Jointed phoenix cannons sweep the arena with an animated PixelLab infernal beam and fiery muzzle bloom.')
base=base.replace('The assembled machine turns with its weapon arms, exhaust and firing points attached.','The phoenix turns through its inherited 900-degree inferno attack with every firing socket attached.')
base=base.replace('Vents and legs fold inward while both surviving chimneys emit rotating fire. Each vent can be destroyed.','Wings and talons tuck inward while both surviving feather roots cast rotating fire. Each wing can be destroyed.')
base=base.replace('Knees, feet and chimneys fold into a compact machine before the committed rolling passes.','Wings, talons and tail tuck inward for the inherited committed rolling passes.')
base=base.replace('A planted shoulder, hinged forearm, visible windup and committed swing.','A furnace cannon draws back, warns and commits to a sweeping strike.')
base=base.replace('CHR'+'OMIUM CANNON','FURNACE FEATHER CANNON').replace('EXHAUST ROTOR','PHOENIX FIRE ROTOR').replace('ARMORED ROLL','FIREBIRD ROLL')
base=base.replace('Native volcano cannon attack','Native phoenix cannon attack').replace('All authored volcano components','All authored phoenix components')
exec(compile(base,str(R/'_BUILD_SOURCE/build_dracodia_volcano_review_1019.py'),'exec'),{'__file__':str(R/'_BUILD_SOURCE/review_phoenix_1020.py'),'__name__':'__main__'})
p=O/'review.html';s=p.read_text(encoding='utf-8');extra='<details><summary>PixelLab attack animation sources</summary><p>Every source below was generated in PixelLab. The live fight applies these to independent moving modules and physical firing points.</p>'
for label,file in [('Coordinated wingbeat / furnace charge','pixellab-wing-charge.webp'),('Phoenix muzzle bloom','pixellab-muzzle.webp'),('Molten infernal beam','pixellab-beam.webp'),('Detached skull charging','pixellab-head-charge.webp')]:extra+='<h2>'+label+'</h2><img loading="lazy" style="width:auto;max-width:100%" src="'+file+'" alt="'+label+'">'
extra+='</details><details><summary>Native module destruction</summary><p>Actual damaged components leave the rig, cancel their weapons and persist through form changes.</p><img loading="lazy" src="module-breaks.webp" alt="Native module destruction"></details>'
s=s.replace('<p><a href="../dracodia_download_1019/review.html">',extra+'<p><a href="../dracodia_download_1019/review.html">');p.write_text(s,encoding='utf-8');print('Phoenix review assembled',flush=True)
