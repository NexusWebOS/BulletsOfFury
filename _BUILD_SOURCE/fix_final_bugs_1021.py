from pathlib import Path
import hashlib,json,shutil
from PIL import Image
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
S=R/'_ART_SOURCES/final_version_1021';S.mkdir(parents=True,exist_ok=True)
p=R/'assets/combat_polish_0927b.js';b=p.read_bytes();s=b.decode('utf-8')
changes=[
 ('if(m&&m.hp<=0)continue;const core=',"if((m&&m.hp<=0)||(p.id==='core'&&b._bomber.core<=0))continue;const core="),
 ('dead:b.dead||b.enter||!!(m&&m.hp<=0)',"dead:b.dead||b.enter||!!(m?m.hp<=0:b._bomber.core<=0)"),
 ('if(B.core<=0){b.hp=0;b.dead=true;', 'if(b.hp<=0){b.hp=0;b.dead=true;')]
for old,new in changes:
 assert s.count(old)==1,(p,old,s.count(old));s=s.replace(old,new)
(S/'combat_polish_0927b.before.js').write_bytes(b);p.write_bytes(s.encode('utf-8'))
p=R/'assets/game.js';b=p.read_bytes();assert b'\r\n' not in b;s=b.decode('utf-8')
old='''      spaceMode:false,dkT:0,sonicT:0,forge:{},forgeForms:{},forgeElems:{},_forgeBlastSeq:P.blastSeq||(P.blastSeq={}),_chainRev:0,_chainHeat:0,_chainOverheat:0,_kinN:0,
'''
new='''      spaceMode:false,dkT:0,sonicT:0,forge:{},forgeForms:{},forgeElems:{},_forgeBlastSeq:P.blastSeq||(P.blastSeq={}),_chainRev:0,_chainHeat:0,_chainOverheat:0,_kinN:0,
      // A preview owns its alternating barrels and visual clocks; live flight never supplies them.
      _chainSide:P.chainSide||0,_chainSpinT:P.chainSpinT||0,
'''
assert s.count(old)==1;s=s.replace(old,new)
old='''    player=Object.assign({},sv.player,{x:VW/2,y:VH-70,dead:false,invuln:0,_mgMuzT:0,_spaceMuzzle:0});'''
new='''    player=Object.assign({},sv.player,{x:VW/2,y:VH-70,dead:false,out:false,invuln:0,
      roll:0,somer:0,spin:0,_hammerEvap:0,_eradicated:0,_cinematicHide:false,_s7Hidden:false,
      _mgMuzT:P.mgMuzT||0,_chainMuzzle:P.chainMuzzle||0,_spaceMuzzle:0});'''
assert s.count(old)==1;s=s.replace(old,new)
old='''    P.impacts=pImpacts;P.explosions=explosions;P.smoke=smokeTrails;P.bullets=pBullets;P.parts=particles;P.zaps=zaps;P.bursts=efxBursts;P.geysers=geysers;P.voids=voids;'''
new='''    P.chainSide=run._chainSide;P.chainSpinT=run._chainSpinT;
    P.mgMuzT=player._mgMuzT;P.chainMuzzle=player._chainMuzzle;
'''+old
assert s.count(old)==1;s=s.replace(old,new)
old='''    P.cd-=dt;
    if(P.cd<=0){'''
new='''    player._mgMuzT=Math.max(0,(player._mgMuzT||0)-dt);
    player._chainMuzzle=Math.max(0,(player._chainMuzzle||0)-dt);
'''+old
assert s.count(old)==1;s=s.replace(old,new)
(S/'game.forge-before.js').write_bytes(b);p.write_bytes(s.encode('utf-8'))
for name in ['hammer','portal']:
 src=Path(__file__).parent/(name+'-master-1021.png');dest=S/(name+'-master.png');shutil.copy2(src,dest)
 if name=='hammer':
  im=Image.open(src).convert('RGBA');im.resize((256,256),Image.Resampling.NEAREST).save(S/'hammer-animation-source.png')
print('Corrected miniboss full health, dead-core targeting, isolated Forge barrel/muzzle state; preserved source masters.')
