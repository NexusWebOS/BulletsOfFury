from pathlib import Path
import json,hashlib
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;C=W/'candidate';C.mkdir(exist_ok=True);O=W.parents[1]/'outputs/snake-arrow';O.mkdir(parents=True,exist_ok=True)
old="for(let i=0;i<7;i++){const x=lerp(camLeftX()+30,camRightX()-30,i/6),u=clamp((x-a.from.x)/(a.to.x-a.from.x),0,1),p=sj123SidePoint(a,u),angle=Math.atan2(p.dy,p.dx),n=((Math.round(angle/TAU*32)%32)+32)%32;sj123Blit('arrows',(col*2+pulse)*32+n,p.x,p.y);}SA123.warningDraws++;"
new="const x=a.to.x>a.from.x?camLeftX()+34:camRightX()-34,u=clamp((x-a.from.x)/(a.to.x-a.from.x),0,1),p=sj123SidePoint(a,u),angle=Math.atan2(p.dy,p.dx),n=((Math.round(angle/TAU*32)%32)+32)%32;sj123Blit('arrows',(col*2+pulse)*32+n,p.x,p.y);SA123.warningDraws++;"
targets=[('runtime',R/'assets/sumpjaw_tandem_1105.js'),('pattern',R/'_BUILD_SOURCE/snake_assault_1110/pattern.js')];records=[]
for name,p in targets:
 b=p.read_bytes();s=b.decode();assert s.count(old)==1,'Warning source changed: '+name;(C/(name+'.before')).write_bytes(b);(C/(name+'.js')).write_text(s.replace(old,new,1),encoding='utf-8',newline='\n');records.append({'name':name,'path':str(p),'before_sha256':hashlib.sha256(b).hexdigest()})
(O/'manifest.json').write_text(json.dumps({'targets':records,'change':'One existing authored direction-arrow indicator per living snake at its viewport entry edge; colors and timing retained. No attack, movement, health or projectile changes.'},indent=2));print('Prepared one entry arrow per snake')
