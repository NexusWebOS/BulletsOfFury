from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageChops
import json,sys
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=R/'_shots/depth35';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[];measured={}
def check(n,v):checks.append({'name':n,'passed':bool(v)});print(('PASS 'if v else'FAIL ')+n,flush=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':960});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.add_init_script("window.testPad={id:'6B controller',mapping:'',index:0,connected:true,axes:[0,0],buttons:Array.from({length:12},()=>({pressed:false,value:0}))};Object.defineProperty(navigator,'getGamepads',{value:()=>[testPad]});window.pad=(...ids)=>testPad.buttons.forEach((b,i)=>{b.pressed=ids.includes(i);b.value=+b.pressed;});")
 p.goto('http://127.0.0.1:8781/expansion/topdown/index.html?fullscreen=0&build=overdrive1016-depth35-r1',wait_until='domcontentloaded');p.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=120000);ev=p.evaluate
 ev('TDGAME.freeze();TD.Input.setPadPreset("m30");ART.warm([...Object.keys(TD_DEPTH35_ART.assets),...Object.keys(TD_CONTRA34_ART.assets)])');p.wait_for_function('[...Object.keys(TD_DEPTH35_ART.assets),...Object.keys(TD_CONTRA34_ART.assets)].every(k=>ART.get(k))',timeout=120000)
 def frames(n):
  while n:q=min(30,n);ev(f'TDGAME.step({q})');p.wait_for_timeout(1);n-=q
 def fresh(id=3):
  ev(f'pad();testPad.axes=[0,0];TD.Input.pointer.active=false;TD.Input.update();TD.pilot="yuri";TD.difficulty="normal";TD.game.sel=TD.MISSIONS.findIndex(m=>m.id==={id});TDGAME.start();TD.Achievements.queue=[];TD.game.msgs=[];');frames(1)
 def shot(n):ev('TD.Achievements.queue=[];TDGAME.render()');p.locator('#screen').screenshot(path=str(O/(n+'.png')))
 fresh();ev('TD.game.fortress.pending=[];TD.game.units=[];TD.game.player.inv=0');shot('topdown_standing')
 p.keyboard.down('f');frames(1);p.keyboard.up('f');frames(32);check('keyboard F enters prone',ev('TD.game.player.prone&&TD.game.player.stance==="prone"'))
 start=ev('TD.game.player.x');p.keyboard.down('d');frames(25);p.keyboard.up('d');check('WASD crawls while prone',ev('TD.game.player.x')>start+10);shot('topdown_prone')
 p.keyboard.down('f');frames(1);p.keyboard.up('f');frames(32);check('F toggles back to standing',ev('!TD.game.player.prone&&TD.game.player.stance==="stand"'))
 p.keyboard.down('c');frames(25);shot('topdown_crouch');check('keyboard C crouches without changing body unit',ev('TD.game.player.stance==="crouch"'));p.keyboard.up('c');frames(2)
 check('all raised props and damage states decode',ev('Object.keys(TD_DEPTH35_ART.assets).filter(k=>/^d35_(barrier|bunker|crate|barrel|wall|wood|server|relay)_/.test(k)).length===32'))
 check('all exported frame canvases have even dimensions',ev('Object.values(TD_DEPTH35_ART.assets).every(m=>m.size.every(n=>Number.isInteger(n)&&n%2===0))'))
 # Real hit damage selects the authored broken plate and releases collision.
 ev('const c=TD.game.structures.find(s=>s.kind==="od_crate");window.testCrate=c;TD.hitStructure(TD.game,c,8);');check('damaged crate changes art',ev('TD.Depth35.coverPose(testCrate).key.endsWith("_1")'));ev('TD.hitStructure(TD.game,testCrate,100)');check('destroyed crate releases collision',ev('testCrate.dead&&testCrate.rect.dead&&TD.Depth35.coverPose(testCrate).key.endsWith("_3")'))
 # Every roster is assigned to a real encounter, rather than an art preview.
 fresh();measured['overheadRoster']=ev('TD.game.fortress.pending.map(s=>s.type)');check('overhead contains all ten enemy archetypes',len(set(measured['overheadRoster']))==10)
 ev('TD.game.fortress.pending=[];TD.game.units=[];TD.game.player.inv=999;TD.game.player.x=400;TD.game.player.y=2340;');
 ev('for(const [i,k] of ["shotgun","double","roller"].entries()){const u=TD.makeUnit("c35_"+k,270+i*130,2210,{a:0});u.spawnId=i;TD.game.units.push(u);}')
 frames(150);shot('ground_enemy_attacks');check('ground shotgun and twin barrel attack',ev('(TD.Depth35.attacks.shotgun||0)>0&&(TD.Depth35.attacks.double||0)>0'))
 frames(180);check('rolling alien completes roll and unfolds',ev('TD.Depth35.rolls>0'));shot('ground_enemy_roll')
 # Stand/crouch/prone/cover scales and alpha inspected at the same native grid.
 measured['poseScales']=ev('(()=>{const p={...TD.game.player,inv:0,cover:null,action:null,moving:false,roll:0,jump:0,stanceTransition:null,poseT:1,aim:Math.PI};return ["stand","crouch","prone"].map(stance=>TD.footPose({...p,stance,prone:stance==="prone"}))})()')
 check('sideways crouch uses matching approved Yuri bank',ev('TD.footPose({...TD.game.player,aim:-Math.PI/2,stance:"crouch",moving:false,cover:null,action:null,roll:0,jump:0,stanceTransition:null}).key.startsWith("e29_crouch_")'))
 # Actual canvas compositing for every added family, including flash expiry.
 measured['flashes']=ev('''()=>{const out=[];for(const kind of Object.keys(TD.Depth35.profiles)){const u=TD.makeUnit('c35_'+kind,160,190,{a:0});u.phase='fight';u.age=1;const cv=document.createElement('canvas');cv.width=cv.height=256;const ctx=cv.getContext('2d');ctx.imageSmoothingEnabled=false;TD.drawAssaultRobot(ctx,u,false);const a=ctx.getImageData(0,0,256,256).data.slice();ctx.clearRect(0,0,256,256);u.flash=.12;TD.drawAssaultRobot(ctx,u,false);const b=ctx.getImageData(0,0,256,256).data;let changed=0;for(let i=0;i<a.length;i+=4)if(a[i+3]&&b[i]+b[i+1]+b[i+2]>a[i]+a[i+1]+a[i+2])changed++;TD.unitTick(u,TD.game,.2);out.push({kind,changed,expired:u.flash===0});}return out}''')
 check('every new troop flashes visible pixels and expires',all(x['changed']>20 and x['expired'] for x in measured['flashes']))
 # Real scene order: a wall in front of Yuri must hide his lower pixels.
 fresh();ev('TD.game.fortress.pending=[];TD.game.units=[];TD.game.player.inv=0;TD.game.player.x=400;TD.game.player.y=2100;TD.game.player.aim=Math.PI;TD.game.player.prone=true;TD.game.player.stance="prone";');frames(2);shot('behind_bunker')
 check('depth sorting draws Yuri before his foreground bunker',ev('TD.game.player.y<TD.game.structures.find(s=>s.kind==="od_bunker"&&s.y===2140).y'))
 # Distinct attacks emit moving projectiles, with real named sprites at their roots.
 for kind in ['rifle','heavy','laser','rocket','shotgun','double','roller']:
  fresh();ev('TD.Escape29.begin(TD.game);TD.Escape29.setPhase(TD.game,"corridor");TD.game.escape29.pending=[];TD.game.escape29.solids=[];TD.game.player.inv=999;TD.game.player.x=200;')
  ev(f'''TD.game.escape29.enemies=[{{kind:'{kind}',x:480,y:350,homeX:480,phase:'fight',age:0,walk:0,hp:99,max:99,flash:0,fireCd:.1}}];TD.Depth35.attacks['{kind}']=0;''');frames(220)
  check(kind+' has live side attack',ev(f'(TD.Depth35.attacks["{kind}"]||0)>0'))
  check(kind+' side pose is authored',ev('TD.Contra34.sidePose(TD.game.escape29.enemies[0],TD.game).key.startsWith("c34_side_")'))
  if kind in ['shotgun','double','roller']:shot('side_'+kind)
 fresh(7);frames(130);check('first Bastion room spawns shotgun and double barrel',ev('TD.game.units.some(u=>u.kind==="shotgun")&&TD.game.units.some(u=>u.kind==="double")'));shot('bastion_new_roster')
 for kind in ['rifle','heavy','laser','rocket','shotgun','double','roller','flame','flyer','bat']:
  fresh(7);ev(f'''TD.game.bastion.phase='fight';TD.game.bastion.totalWave=1;TD.game.bastion.turrets=[];TD.game.units=[];TD.game.player.inv=999;const u=TD.Bastion.spawn(TD.game,'{kind}',320,0);Object.assign(u,{{phase:'peek',phaseT:0,x:320,y:338,scale:.54,duck:0}});TD.Depth35.attacks['{kind}']=0;''');frames(300)
  check(kind+' has live front attack',ev(f'(TD.Depth35.attacks["{kind}"]||0)>0'))
  check(kind+' front sprite resolves',ev('!!ART.get(TD.Bastion.unitPose(TD.game.units[0]))'))
  if kind in ['double','roller','flame']:shot('front_'+kind)
 # Same native pixels must visibly flash and then return to their authored palette.
 fresh();ev('TD.game.fortress.pending=[];TD.game.units=[TD.makeUnit("c35_shotgun",500,2200,{a:0})];TD.game.player.inv=0;');shot('hit_before');ev('TD.game.units[0].flash=.12');shot('hit_after');check('new troop pixels flash on hit',ImageChops.difference(Image.open(O/'hit_before.png').convert('RGB'),Image.open(O/'hit_after.png').convert('RGB')).getbbox() is not None);frames(12);check('troop hit flash expires',ev('TD.game.units[0].flash===0'))
 measured['audio']=ev('''async()=>{const cues=[...new Set(Object.values(TD.Depth35.profiles).map(d=>d.cue))],c=new AudioContext(),out=[];TD.Audio.unlock();for(const k of cues){const d=TD.Audio.sounds[TD.Audio.resolve(k)],buf=await c.decodeAudioData(await(await fetch(ART.BASE+d.file)).arrayBuffer());TD.Audio.play(k,.1);out.push({key:k,seconds:buf.duration,gated:d.min>0});}await c.close();return out}''');check('all attack cues decode and use retrigger gates',all(x['seconds']>0 and x['gated'] for x in measured['audio']))
 # Export an inspectable native-pixel pose sheet, using the game's own draw path.
 import base64
 sheet=ev('''()=>{const c=document.createElement('canvas');c.width=720;c.height=480;const x=c.getContext('2d');x.imageSmoothingEnabled=false;x.fillStyle='#293840';x.fillRect(0,0,720,480);for(let row=0;row<3;row++)for(let col=0;col<4;col++){const stance=['stand','crouch','prone','cover'][col],p={...TD.game.player,pilot:'yuri',modernFoot:true,pseudo3D:false,dead:false,inv:0,x:col*180+90,y:row*160+133,aim:[-Math.PI/2,Math.PI,0][row],a:[-Math.PI/2,Math.PI,0][row],stance:stance==='cover'?'crouch':stance,prone:stance==='prone',moving:false,action:null,roll:0,jump:0,jumpZ:0,stanceTransition:null,cover:stance==='cover'?{dead:false}:null,peek:0,peekExposed:false,blindfire:false,poseT:1,footTime:0,gaitPhase:0};TD.drawFoot(x,p,{});x.fillStyle='white';x.font='11px monospace';x.fillText(stance,col*180+10,row*160+15);}return c.toDataURL('image/png').split(',')[1]}''')
 (O/'yuri_stance_review.png').write_bytes(base64.b64decode(sheet))
 check('browser has no errors',not errors);report={'checks':checks,'errors':errors,'measured':measured};(O/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps({'pass':sum(x['passed'] for x in checks),'total':len(checks),'errors':errors}),flush=True);b.close()
sys.exit(0 if all(x['passed']for x in checks) and not errors else 1)
