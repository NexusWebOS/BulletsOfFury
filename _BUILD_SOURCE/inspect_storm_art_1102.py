"""Explicit art-only pose/damage fixtures; never used in fight films.
Warning coverage is checked against the measured opaque roll silhouette.
"""
from pathlib import Path
import sys,json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/furious_encounters_1102';frames=[];report={}
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(4,4);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('''()=>{EA11.setup(6,'furious');stagePlan=[];debugUnlocked=true;DBGT.god=true;spawnSubBoss('siegefortress17');window.B=subBoss;}''');p.wait_for_function('()=>{stageLoadTick();return fb112Ready()}',timeout=180000)
 for state in [0,3]:
  for pose in range(8):
   raw=p.evaluate('''a=>{const q=B._fb112;B.x=VW/2;B.y=245;B.t=8;B.enter=false;q.t=.2;q.phase='attack';q.attack='pass';q.heading=Math.PI/2;q.pose=q.M.clips.roll[a.pose];q.parts.forEach((p,i)=>p.hp=a.state&(1<<i)?0:p.maxhp);ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);fb112Draw(B);return cv.toDataURL().split(',')[1];}''',dict(state=state,pose=pose));f=O/f'roll-native-{state}-{pose}.png';f.write_bytes(base64.b64decode(raw));frames.append((f,state,pose))
 report=p.evaluate('''()=>{const Bk=FB112_ART.banks.razor_roll,im=XART.get(Bk.key),c=document.createElement('canvas');c.width=c.height=Bk.cell;const g=c.getContext('2d',{willReadFrequently:true});let same=true,max=0;const a=Math.atan2(45,790),dir=fb112Dir(a,Bk.dirs),k=B._fb112.scale*512/384;for(let pose=0;pose<8;pose++){let base;for(let state=0;state<4;state++){const n=(state*8+pose)*Bk.dirs+dir;g.clearRect(0,0,Bk.cell,Bk.cell);g.drawImage(im,n%Bk.cols*Bk.cell,Math.floor(n/Bk.cols)*Bk.cell,Bk.cell,Bk.cell,0,0,Bk.cell,Bk.cell);const data=g.getImageData(0,0,Bk.cell,Bk.cell).data;if(!state)base=data;else for(let i=3;i<data.length;i+=4)if(data[i]!==base[i])same=false;if(!state)for(let y=0;y<Bk.cell;y++)for(let x=0;x<Bk.cell;x++)if(data[(y*Bk.cell+x)*4+3]>24){const dx=(x-Bk.cell/2)*k,dy=(y-Bk.cell/2)*k;max=Math.max(max,Math.abs(-dx*Math.sin(a)+dy*Math.cos(a)));}}}return{rollStatesPreserveExactAlpha:same,passHalfSpan:max,warningHalfWidth:B._fb112.M.world*1.08/2,verts:FB112_ART.models.razor.shear};}''');b.close()
sheet=Image.new('RGB',(1280,1368),'#06121d');draw=ImageDraw.Draw(sheet)
for i,(f,state,pose)in enumerate(frames):
 im=Image.open(f).convert('RGBA');im.thumbnail((320,320));x=i%4*320;y=i//4*342;sheet.paste(im,(x,y+20),im);draw.text((x+5,y+3),('Intact'if state==0 else'Gun wrecks')+' / roll '+str(pose),fill='white')
sheet.save(O/'roll-native-contact.jpg',quality=94);(O/'art-pixel-checks.json').write_text(json.dumps(report,indent=2));print(report)
