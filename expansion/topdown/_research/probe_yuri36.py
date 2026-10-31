from pathlib import Path
from playwright.sync_api import sync_playwright
import base64,json,sys
R=Path(__file__).resolve().parents[3] if Path(__file__).parent.name=='_research' else Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=R/'_shots/yuri36';O.mkdir(exist_ok=True)
checks=[];errors=[];data={}
def check(n,v):checks.append({'name':n,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+n,flush=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8781/expansion/topdown/index.html?fullscreen=0',wait_until='domcontentloaded');p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=120000);ev=p.evaluate;ev('TDGAME.freeze()')
 if not ev('!!TD.Yuri36'):p.add_script_tag(url='http://127.0.0.1:8781/expansion/topdown/js/yuri36.js')
 ev('ART.warm(Object.keys(TD_YURI32_ART.assets).concat(Object.keys(TD_ESCAPE29_ART.assets),Object.keys(TD_BASTION19_ART.assets)))');p.wait_for_function('Object.keys(TD_YURI32_ART.assets).every(k=>ART.get(k))',timeout=120000)
 def frames(n):
  for i in range(n):ev('TDGAME.step(1)');p.wait_for_timeout(1)
 def fresh():
  ev('TD.Input.pointer.active=false;TD.pilot="yuri";TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===3);TDGAME.start();TD.game.fortress.pending=[];TD.game.units=[];TD.game.msgs=[];TD.Achievements.queue=[];');frames(1)
 fresh()
 data['crawl']=ev('''()=>{const p={...TD.game.player,aim:-Math.PI/2,lowSide36:'east',stance:'prone',prone:true,stanceTransition:null,roll:0,jump:0,action:null,cover:null,moving:true};return Array.from({length:40},(_,i)=>{const z=TD.footPose({...p,gaitPhase:i/40}),m=TD_ASSAULT_ART.assets[z.key];return{...z,h:(m.bounds[3]-m.bounds[1])*z.scale};})}''')
 check('crawl never replays upright lowering frames',all(int(z['key'].split('_')[-1])>=11 for z in data['crawl']))
 check('grounded crawl retains one scale and stays 36–40 pixels high',len(set(z['scale']for z in data['crawl']))==1 and max(z['h']for z in data['crawl'])<=40)
 data['transition']=ev('''()=>{const p={...TD.game.player,aim:-Math.PI/2,stance:'prone',prone:true,cover:null,roll:0,jump:0,action:null,moving:false};return ['prone','stand'].map(to=>Array.from({length:12},(_,i)=>TD.footPose({...p,stanceTransition:{to,t:i/12*.46}}).key));}''')
 check('side prone entry and exit use the same twelve drawings reversed',data['transition'][0]==list(reversed(data['transition'][1])))
 data['coverBanks']=ev('''()=>{const base={...TD.game.player,aim:-Math.PI/2,stance:'crouch',prone:false,stanceTransition:null,roll:0,jump:0,action:null,blindfire:false,moving:false,x:445,y:2100},r={x0:380,x1:430,y0:2070,y1:2130};return ['od_column36','od_barrier'].map(kind=>Array.from({length:20},(_,i)=>TD.footPose({...base,cover:{kind,dead:false,rect:r},peek:i/19*.24,peekExposed:i===19})));}''')
 check('column uses all nineteen authored standing back-cover frames',len(set(z['key']for z in data['coverBanks'][0]))==19)
 check('low-wall lateral peek stops at the extended gun, before withdrawal',len(set(z['key']for z in data['coverBanks'][1]))==13 and data['coverBanks'][1][-1]['index']==12)
 data['return']=ev('''()=>{const base={...TD.game.player,aim:-Math.PI/2,stance:'crouch',prone:false,stanceTransition:null,roll:0,jump:0,action:null,blindfire:false,moving:false,x:445,y:2100,cover:{kind:'od_barrier',dead:false,rect:{x0:380,x1:430,y0:2070,y1:2130}},coverReturn36:true};return Array.from({length:36},(_,i)=>TD.footPose({...base,peek:(1-i/35)*.24,peekExposed:false}).index);}''')
 check('crouched return plays the authored withdrawal then tucks into cover',all(i in data['return']for i in [13,14,15,16,4,3,2,1,0])and data['return'][-1]==0)
 check('cover banks keep one fixed body scale',all(z['scale']==1 for bank in data['coverBanks']for z in bank))
 data['north']=ev('''()=>{const p={...TD.game.player,aim:Math.PI,stance:'crouch',prone:false,stanceTransition:null,roll:0,jump:0,action:null,blindfire:false,moving:false,x:400,y:2150,cover:{kind:'od_barrier',rect:{x0:300,x1:500,y0:2110,y1:2130}}};return[0,.12,.239,.24].map(peek=>TD.footPose({...p,peek,peekExposed:peek===.24,firing:peek===.24?.13:0}));}''')
 check('full exposure keeps the same north peek endpoint',data['north'][-1]['key']==data['north'][-2]['key'])
 check('cover muzzle is exactly the selected authored barrel pixel',ev('''()=>{const p={...TD.game.player,aim:-Math.PI/2,stance:'crouch',prone:false,stanceTransition:null,roll:0,jump:0,action:null,blindfire:false,moving:false,x:445,y:2100,cover:{kind:'od_column36',rect:{x0:380,x1:430,y0:2070,y1:2130}},peek:.24,peekExposed:true};const z=TD.footPose(p),m=TD_ASSAULT_ART.assets[z.key],q=TD.footVisualSocket(p);return q.x===p.x+(m.muzzle[0]-m.anchor[0])*z.scale&&q.y===p.y+(m.muzzle[1]-m.anchor[1])*z.scale;}'''))
 check('north cover side step uses all eight authored gait frames',ev('''()=>{const p={...TD.game.player,aim:Math.PI,stance:'crouch',prone:false,stanceTransition:null,roll:0,jump:0,action:null,blindfire:false,moving:true,vx:1,x:400,y:2150,cover:{kind:'od_barrier',rect:{x0:300,x1:500,y0:2110,y1:2130}},peek:0,peekExposed:false};return new Set(Array.from({length:8},(_,i)=>TD.footPose({...p,gaitPhase:i/8}).key)).size===8;}'''))
 # Native key path: hold cover and fire from a real static structure. Only the
 # fixture placement is explicit; footTick owns exposure and projectile birth.
 fresh();ev('''TD.game.player.x=400;TD.game.player.y=2250;TD.game.player.aim=-Math.PI/2;TD.game.player.manualAim=999;TD.game.player.inv=0;window.y36fixture={kind:'od_column36',assault:true,cover:true,dead:false,x:355,y:2250,type:{hw:28,hh:26},rect:{x0:327,x1:383,y0:2224,y1:2276},hp:Infinity,max:Infinity};TD.game.structures=[y36fixture];''')
 p.keyboard.down('c');frames(2);p.keyboard.down('z')
 data['timing']=[]
 for i in range(31):
  frames(1);data['timing'].append(ev('({peek:TD.game.player.peek,key:TD.footPose(TD.game.player).key,shots:TD.game.shots.length,exposed:TD.game.player.peekExposed})'))
 p.keyboard.up('z');frames(31);p.keyboard.up('c')
 check('keyboard cover fire does not expose before the complete pop-out',not any(v['exposed']for v in data['timing'][:25]))
 check('keyboard cover fire reaches exposure after the full pop-out',any(v['exposed']for v in data['timing'][26:]))
 check('release returns to the protected first frame',ev('TD.game.player.peek===0&&!TD.game.player.peekExposed'))
 # Render the exact game draw path at original pixel scale for frame review.
 sheet=ev('''()=>{const c=document.createElement('canvas');c.width=1200;c.height=840;const x=c.getContext('2d');x.imageSmoothingEnabled=false;x.fillStyle='#141c24';x.fillRect(0,0,c.width,c.height);for(let row=0;row<4;row++)for(let i=0;i<6;i++){const px=100+i*200,py=180+row*210,s={...TD.game.player,x:px,y:py,aim:-Math.PI/2,stance:row===3?'prone':'crouch',prone:row===3,stanceTransition:null,roll:0,jump:0,jumpZ:0,action:null,blindfire:false,moving:row===3,gaitPhase:i/6,peek:row===3?0:i/5*.24,peekExposed:i===5,inv:0};s.cover=row===3?null:{kind:row===0?'od_column36':'od_barrier',rect:{x0:px-80,x1:px-15,y0:py-25,y1:py+25}};if(row===2){s.aim=Math.PI;s.cover.rect={x0:px-60,x1:px+60,y0:py-40,y1:py-18};}TD.drawFoot(x,s,{});const z=TD.footPose(s);x.fillStyle='#b1c9d3';x.font='11px monospace';x.fillText(z.key,5+i*200,18+row*210);x.fillRect(i*200,py,200,1);}return c.toDataURL('image/png').split(',')[1]}''');(O/'native_motion_review.png').write_bytes(base64.b64decode(sheet))
 check('browser reports no page or console errors',not errors);b.close()
 report={'checks':checks,'errors':errors,'measurements':data};(O/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps({'passed':sum(c['passed']for c in checks),'total':len(checks),'errors':errors}),flush=True)
sys.exit(0 if all(c['passed']for c in checks)and not errors else 1)
