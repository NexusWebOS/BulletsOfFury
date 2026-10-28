from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import sys,json,base64
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_ART_SOURCES/biome_fleet_1022' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent/'BOF-BiomeFleet-1022';D=W/'references';D.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
keys={'magma_small':'overhaul_stage2_fire_jet_02','magma_large':'nvl_carrier_0','sky_small':'p2_stealth_blue_idle','sky_medium':'n6v2_steel_intact_c','sky_large':'n6v1_steel_intact_c','water_small':'overhaul_stage9_water_jet_01','water_manta':'ns9e_vmanta_idle','water_large':'ns9x_dreadv','water_drone':'overhaul_stage9_water_drone_01'}
port,stop=shoot.serve(str(R));records=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(120000)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4')
  p.evaluate('window.__biomeWarm=()=>{let ok=true;for(const k of '+json.dumps(list(keys.values()))+')if(!XART.rdy(k))ok=false;return ok;}')
  p.wait_for_function('__biomeWarm()',polling=50)
  for name,key in keys.items():
   out=p.evaluate('''k=>{let im=XART.get(k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return {w:c.width,h:c.height,png:c.toDataURL('image/png').split(',')[1]};}''',key)
   (D/(name+'.png')).write_bytes(base64.b64decode(out.pop('png')));records.append({'id':name,'key':key,**out})
  runtime=p.evaluate('''()=>({volcanic:VOLC,skyFleet:L6_FLEET,skyStorm:S6STORM,skyJets:L6JETS,waterVoid:S9VOID,waterNative:S9_UNITS,stages:STAGES.map((x,i)=>({stage:i+1,name:x.name})),airFamilies:[...AF21.aliases].filter(([k,v])=>v.M.stages.some(s=>[2,6,9].includes(s))).map(([alias,v])=>({alias,model:v.id,stages:v.M.stages,source:v.M.sourceKeys?.[alias],span:v.M.span}))})'''.replace('S6STORM','typeof S6STORM!=="undefined"?S6STORM:{}'))
  (W/'native-roster.json').write_text(json.dumps(runtime,indent=2),encoding='utf-8')
  b.close()
finally:stop()
(D/'manifest.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
sheet=Image.new('RGB',(960,960),'#0b111b');g=ImageDraw.Draw(sheet)
for i,row in enumerate(records):
 im=Image.open(D/(row['id']+'.png')).convert('RGBA');im.thumbnail((280,270),Image.Resampling.NEAREST);x=i%3*320+(320-im.width)//2;y=i//3*320;sheet.paste(im,(x,y),im);g.text((i%3*320+8,y+286),row['id'],fill='white')
sheet.save(W/'native-roster-contact.png');print('Exported9 native identities and runtime roster specs.')
