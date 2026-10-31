"""Native geometry/cover/Gosfer chain QA. Isolated fixtures, not a campaign clear."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json, sys, base64

R = Path(__file__).resolve().parents[3] if Path(__file__).parent.name=='_research' else Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
O = R/'_shots/layout36'
O.mkdir(parents=True, exist_ok=True)
checks, errors, measured = [], [], {}
def check(name, value):
    checks.append({'name': name, 'passed': bool(value)})
    print(('PASS ' if value else 'FAIL ')+name, flush=True)

with sync_playwright() as pw:
    browser = pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    page = browser.new_page(viewport={'width':1280,'height':960})
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('console', lambda m: errors.append(m.text) if m.type=='error' else None)
    page.goto('http://127.0.0.1:8781/expansion/topdown/index.html?fullscreen=0&build=overdrive1016-base36-r1', wait_until='domcontentloaded')
    page.wait_for_function('window.TDGAME && TD.game.state==="boot"', timeout=120000)
    ev=page.evaluate
    ev('TDGAME.freeze(); TD.Input.pointer.active=false; TD.pilot="yuri"; TD.difficulty="normal"; TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===3); TDGAME.start(); TD.Achievements.queue=[]; TD.game.msgs=[];')
    def frames(n):
        while n:
            q=min(30,n); ev(f'TDGAME.step({q})'); page.wait_for_timeout(1); n-=q
    def shot(name):
        ev('TD.Achievements.queue=[];TDGAME.render()')
        page.locator('#screen').screenshot(path=str(O/(name+'.png')))
    ev('ART.warm(Object.keys(window.TD_LEVEL36_ART?.assets||{}));ART.warm(Object.keys(TD_ASSAULT_ART.assets));')
    page.wait_for_function('Object.keys(window.TD_LEVEL36_ART?.assets||{}).every(k=>!!ART.get(k))',timeout=120000)
    check('new level module loaded',ev('!!TD.Level36'))
    check('new scenery assets decoded',ev('Object.keys(window.TD_LEVEL36_ART?.assets||{}).length>0&&Object.keys(TD_LEVEL36_ART.assets).every(k=>!!ART.get(k))'))
    page.wait_for_timeout(1500)
    measured['layout']=ev('''()=>({world:[TD.World.w,TD.World.h],start:{x:TD.game.player.x,y:TD.game.player.y},structures:TD.game.structures.map(s=>({kind:s.kind,x:s.x,y:s.y,hw:s.type.hw,hh:s.type.hh,drop:s.drop,gate:!!s.gate36,column:!!s.column36})),map:TD.MISSIONS.find(m=>m.id===3).map})''')
    full_map=ev('''()=>{const m=TD.MISSIONS.find(m=>m.id===3),G=TD.game,c=document.createElement('canvas');c.width=800;c.height=2800;const ctx=c.getContext('2d'),save={x:TD.Cam.x,y:TD.Cam.y,zoom:TD.Cam.zoom};ctx.imageSmoothingEnabled=false;const g=ART.get(m.map.key);ctx.drawImage(g.im,g.sx,g.sy,g.sw,g.sh,0,0,g.sw,g.sh);for(let y=0;y<2800;y+=320){TD.Cam.y=y;ctx.save();ctx.beginPath();ctx.rect(0,y,800,320);ctx.clip();m.drawFloor(ctx,G);ctx.restore();}TD.Depth35.drawActors(ctx,G);Object.assign(TD.Cam,save);return c.toDataURL('image/png').split(',')[1]}''')
    (O/'full_map.png').write_bytes(base64.b64decode(full_map))
    shot('start')
    kinds=measured['layout']['structures']
    columns=[s for s in kinds if 'column' in s['kind'] or 'beam' in s['kind'] or s['column']]
    relays=[s for s in kinds if s['kind']=='od_relay']
    check('exactly four beam columns',len(columns)==4)
    check('exactly three electric units',len(relays)==3)
    check('three weapon chests in route',len([s for s in kinds if s.get('drop')])>=3)
    check('map expanded to fit supplied vertical plan',measured['layout']['world'][1]>=2700)
    measured['reachability']=ev('''()=>{const W=TD.World,N=TD.Nav,p=TD.game.player;N.build();const f=N.field(p.x,p.y,0),at=(x,y)=>f.D[Math.floor(y/N.C)*N.cols+Math.floor(x/N.C)];return {relays:TD.game.structures.filter(s=>s.kind==='od_relay').map(s=>({x:s.x,y:s.y,reachable:Array.from({length:16},(_,i)=>{const a=i*Math.PI/8,x=s.x+Math.cos(a)*80,y=s.y+Math.sin(a)*80;return !W.solidAt(x,y)&&at(x,y)>=0}).some(Boolean)})),arena:at(400,430)};}''')
    check('all relays reachable before gate opens',all(x['reachable'] for x in measured['reachability']['relays']))
    check('arena cannot be reached through active gate',measured['reachability']['arena']<0)
    # Safe isolated combat fixtures still fire ordinary keyboard bullets.
    ev('TD.game.fortress.pending=[];TD.game.units=[];window.relays36=TD.game.structures.filter(s=>s.kind==="od_relay");')
    ev('Object.assign(TD.game.player,{x:580,y:625,aim:Math.PI,a:Math.PI});TD.Cam.follow(580,625,1);')
    page.keyboard.down('w');frames(60);page.keyboard.up('w');frames(1)
    check('active electric wall physically stops northward movement',ev('TD.game.player.y>=604'))
    shot('gate_locked')
    ev('window.col36=TD.game.structures.find(s=>s.kind==="od_column36");Object.assign(TD.game.player,{x:col36.rect.x1+11,y:col36.y,aim:-Math.PI/2,a:-Math.PI/2,manualAim:999});TD.Cam.follow(TD.game.player.x,TD.game.player.y,1);')
    page.keyboard.down('c');frames(32)
    check('beam column supports back-contact cover',ev('TD.game.player.cover===col36'))
    shot('column_cover')
    page.keyboard.up('c');frames(1)
    for i in range(len(relays)):
        ev(f'''(()=>{{const s=relays36[{i}],p=TD.game.player;Object.assign(p,{{x:s.x,y:s.y+110,aim:Math.PI,a:Math.PI,manualAim:999,cover:null,prone:false,stance:'stand',stanceTransition:null,action:null,inv:0}});TD.Cam.follow(p.x,p.y,1);TD.game.shots=[];TD.game.eshots=[];}})()''')
        key=ev('TD.BIND.A[0]')
        page.keyboard.down(key);frames(240);page.keyboard.up(key);frames(1)
        check('ordinary projectiles destroy electric unit '+str(i+1),ev(f'relays36[{i}].dead'))
        shot('relay_'+str(i+1))
    measured['relayCount']=ev('TD.game.fortress.relays')
    check('all electric units recorded once',measured['relayCount']==3)
    measured['arenaReachable']=ev('''()=>{const N=TD.Nav;N.build();const p=TD.game.player,f=N.field(p.x,p.y,100);return f.D[Math.floor(430/N.C)*N.cols+Math.floor(400/N.C)]>=0;}''')
    check('gate removal opens route to arena',measured['arenaReachable'])
    # Existing Gosfer chain must retain its shield and next-scene entry.
    ev('TD.game.player.x=400;TD.game.player.y=530;TD.game.units=[];TD.game.eshots=[];TD.game.shots=[];')
    frames(1)
    check('Gosfer starts after entering unlocked arena',ev('!!TD.game.boss'))
    if ev('!!TD.game.boss'):
        frames(180);shot('arena')
        check('three linked arena barriers retained',ev('TD.game.boss.barriers.length===3&&TD.game.boss.barriers.every(s=>s.gosferBarrier)'))
        ev('window.b36=TD.game.boss;window.hp36=b36.hp;b36.hit(b36.x,b36.y,40,99);')
        check('shield absorbs player attacks',ev('b36.shield&&b36.hp===hp36'))
        ev('for(const s of b36.barriers){TD.coverDamageSource={owner:b36};TD.hitStructure(TD.game,s,999);TD.coverDamageSource=null;}')
        frames(1);check('boss-owned barrier destruction starts dialogue',ev('b36.state==="dialogue"&&!b36.shield'))
        frames(660);shot('dialogue_transform');frames(240)
        check('dialogue and transformation finish into phase two',ev('b36.phase===2&&!TD.game.player.scripted'))
        ev('b36.state="recover";b36.hit(b36.x,b36.y,40,b36.hp+1);')
        check('defeat opens north elevator',ev('b36.dead&&TD.game.fortress.exitReady29&&TD.game.fortress.doorOpen'))
        ev('TD.game.player.x=400;TD.game.player.y=150;TD.game.player.dead=false;');frames(1)
        check('north door starts elevator escape',ev('!!TD.game.escape29'))
    check('no browser errors',not errors)
    report={'checks':checks,'errors':errors,'measured':measured,'scope':'Geometry BFS, real-input relay destruction and isolated Gosfer/transition fixtures. Not a full combat playthrough.'}
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'pass':sum(x['passed']for x in checks),'total':len(checks),'errors':errors}),flush=True)
    browser.close()
sys.exit(0 if all(c['passed']for c in checks) and not errors else 1)
