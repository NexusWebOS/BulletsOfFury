"""Actual campaign camera, authored marker pixels and level navigation."""
from pathlib import Path
import argparse,json,sys
from playwright.sync_api import sync_playwright
import shoot
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_shots/campaign_close_1017';OUT.mkdir(parents=True,exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('--before',action='store_true');parser.add_argument('--review-only',action='store_true');args=parser.parse_args()
checks=[];rows=[];errors=[];tag='review' if args.review_only else 'before' if args.before else 'after'
def check(name,ok,data=None):
 checks.append({'name':name,'passed':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport={'width':1920,'height':1080});p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof CF9!=="undefined"');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{window.cm17Pixels={};let owner=null,key=null;const get=XART.get,draw=ctx.drawImage;
   XART.get=function(k){key=k;return get.apply(this,arguments);};ctx.drawImage=function(im,...a){if(owner&&a.length>=4){const [x,y,w,h]=a.slice(-4),m=ctx.getTransform();cm17Pixels[owner]={key:owner==='ship'?'ship_'+_pilotKey():key,height:Math.hypot(m.c*h,m.d*h)/SS,size:Math.max(Math.hypot(m.a*w,m.b*w),Math.hypot(m.c*h,m.d*h))/SS,smoothing:ctx.imageSmoothingEnabled};}return draw.call(this,im,...a);};
   const flag=map4fFlagDraw,ship=sselShipDraw;map4fFlagDraw=function(st){owner='flag'+st;try{return flag.apply(this,arguments);}finally{owner=null;}};sselShipDraw=function(){owner='ship';try{return ship.apply(this,arguments);}finally{owner=null;}};}''')
  def tick(n):
   for i in range(0,n,12):
    err=p.evaluate(shoot.STEP,min(12,n-i))
    if err:errors.append(err)
    p.wait_for_timeout(8)
  def init(stage,fresh=False):
   p.evaluate('''([stage,fresh])=>{ht27Stop();BOFCinematicDirector.cancel();Rival24.reset();debugFight=null;coopOn=false;run.mode='campaign';run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');campaign.unlockedMax=stage===9?8:8;campaign.bonusUnlocked=stage===9;campaign.rank=fresh?{}:{1:'S'};campaign.rivalScattered=false;campaign.stageX1004=null;CF4.focus=false;CF4.flight=4;campPause=null;_selFlash=null;s9MapCine=null;riftReturn=null;openStageSelect(stage,{});sselBoot=0;sselUnlockCine=null;Input.clearTaps();Input.mouse.active=false;Input.mouse.moved=false;map4eWarm();}''',[stage,fresh])
   p.wait_for_function('MAP4E.keys.every(k=>XART.rdy("map4e_region_"+k))&&XART.rdy("ship_cole")&&MAP4F_FLAG_STATES.every(v=>XART.rdy("map4f_flag"+sselCursor+"_"+v))')
  def measure(name):
   row=p.evaluate('''()=>{const f=sselFlagXY(sselCursor),sh=sselShip;return {stage:sselCursor,z:cmap2.cam.z,flag:cmap2ToScreen(f.x,f.y),ship:sh&&cmap2ToScreen(sh.x,sh.y),left:-campaignViewOffset(),right:VW+campaignViewOffset(),top:CM2_BAND_TOP,bottom:CM2_BAND_BOT,detail:typeof cf9FlagHeight==='function'?cf9FlagHeight(sselCursor):28,shipSize:typeof cf9ShipSize==='function'?cf9ShipSize():40,pixels:{flag:cm17Pixels['flag'+sselCursor],ship:cm17Pixels.ship}};}''');row['name']=name;rows.append(row);p.screenshot(path=str(OUT/(tag+'-'+name+'.png')));return row
  if not args.review_only:
   init(1,True);tick(30);measure('approach-stage1');tick(210);measure('selected-stage1')
   for stage in [1,2,3,4,5,6,7,8,9]:
    init(stage);tick(240);r=measure('selected-stage'+str(stage))
    if not args.before:
     check('Stage'+str(stage)+' holds the closer camera',r['z']>=1,r)
     check('Stage'+str(stage)+' has a larger readable flag and ship',r['detail']>=55 and r['shipSize']>=51,r)
     check('Stage'+str(stage)+' keeps both markers inside the map band',r['left']<r['ship']['x']<r['right'] and r['top']+r['detail']<r['flag']['y']<r['bottom']-r['shipSize']/2,r)
     check('Stage'+str(stage)+' actually draws the authored flag at56px without smoothing',abs(r['pixels']['flag']['height']-56)<.01 and not r['pixels']['flag']['smoothing'] and r['pixels']['flag']['key'].startswith('map4f_flag'),r['pixels']['flag'])
     check('Stage'+str(stage)+' actually draws the pilot hull at52px without smoothing',abs(r['pixels']['ship']['size']-52)<.01 and not r['pixels']['ship']['smoothing'],r['pixels']['ship'])
   if not args.before:
    for source,direction,target in [(1,'right',2),(4,'down',5),(7,'up',8)]:
     init(source);tick(60);p.evaluate('(direction)=>Input.injectTap(keybind[direction][0])',direction);trace=[]
     for i in range(90):
      tick(1);trace.append(p.evaluate('()=>({z:cmap2.cam.z,s:cmap2ToScreen(sselShip.x,sselShip.y),left:-campaignViewOffset(),right:VW+campaignViewOffset()})'))
     measure('travel-'+str(source)+'-'+str(target));check('Real '+direction+' input selects Stage'+str(target),p.evaluate('(n)=>sselCursor===n',target))
     check(str(source)+' to'+str(target)+' stays close and keeps the ship in view',all(r['z']>=1 and r['left']+26<r['s']['x']<r['right']-26 and 72<r['s']['y']<286 for r in trace),{'trace':trace[::15],'minY':min(r['s']['y'] for r in trace),'maxY':max(r['s']['y'] for r in trace)})
    p.evaluate('cmap2.focus="bar"');tick(240);r=measure('overview');check('The top-menu overview remains available',r['z']<.3,r)
    init(6);p.evaluate('''()=>{campaign.rivalScattered=true;campaign.rivalDefeated=[false,false,false,false,false];}''');tick(360);r=measure('stage6-with-rebels');check('Selected Stage6 stays close after the rebel flight',r['z']>=1 and p.evaluate('Rival24.mapAvailable'),r)
    p.evaluate('''()=>{Input.injectTap(keybind.up[0]);}''');tick(240);r=measure('stagex-framing');check('Stage X keeps its dedicated encounter camera and controls',p.evaluate('Rival24.mapFocused||map4hXFocused()') and r['z']<.5,r)
    init(2);p.evaluate('''()=>{campaign.unlockedMax=1;campaign.rank={1:'A'};openStageSelect(2,{unlock:2});sselBoot=0;}''');tick(420);r=measure('post-clear');check('The unlock cinematic finishes close to the newly available level',p.evaluate('!sselUnlockCine&&sselCursor===2&&campaign.unlockedMax>=2') and r['z']>=1,r)
    p.set_viewport_size({'width':1000,'height':900});init(4);tick(240);r=measure('compact-stage4');check('Compact viewport keeps enlarged markers clear of the briefing',r['flag']['y']+r['shipSize']/2<r['bottom'],r)
  else:
   p.goto(f'http://127.0.0.1:{port}/docs/previews/campaign_close_1017/index.html');p.wait_for_function('ready&&game.contentWindow.__campaignCloseReviewStorage&&game.contentWindow.eval("sselCursor===4&&cmap2.cam.z>1")')
   check('Review loads the live close camera with separate save storage',True)
   p.select_option('#level','8');p.wait_for_function('game.contentWindow.eval("sselCursor===8&&cmap2.cam.z>1")');p.wait_for_timeout(900);p.screenshot(path=str(OUT/'review-stage8.png'))
   check('Review can select another actual campaign level',True)
   slot=p.evaluate('game.contentWindow.eval("campSlotKey(0)")');p.evaluate('(key)=>localStorage.setItem(key,"real-campaign-sentinel")',slot)
   saved=p.evaluate('game.contentWindow.eval("campWriteSlot(0)")');check('Review save writes leave real campaign slots intact',saved and p.evaluate('(key)=>localStorage.getItem(key)',slot)=='real-campaign-sentinel')
   p.evaluate('game.contentWindow.eval("localStorage.clear()")');check('Review storage clear leaves real campaign slots intact',p.evaluate('(key)=>localStorage.getItem(key)',slot)=='real-campaign-sentinel')
   p.click('#approach');p.wait_for_function('game.contentWindow.eval("sselCursor===1&&!!sselShip")');p.wait_for_timeout(550);p.screenshot(path=str(OUT/'review-approach.png'));check('HQ approach replays using the native ship and camera',p.evaluate('game.contentWindow.eval("cmap2.cam.z>1&&sselShip.cf9")'))
   p.click('#overview');p.wait_for_function('game.contentWindow.eval("cmap2.focus===\'bar\'&&cmap2.cam.z<.3")');check('Review overview button reaches the live map menu',True)
  check('No native page or console errors',not errors,errors);b.close()
finally:stop()
report={'checks':checks,'rows':rows,'errors':errors,'passed':sum(q['passed'] for q in checks),'failed':sum(not q['passed'] for q in checks)}
(OUT/(tag+'-verification.json')).write_text(json.dumps(report,indent=2)+'\n');print('SUMMARY',report['passed'],'passed',report['failed'],'failed');sys.exit(bool(report['failed']))
