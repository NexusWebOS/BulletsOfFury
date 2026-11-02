"""Verify the published project-path hub, native video playback and review routes."""
from pathlib import Path
import argparse,json,re,sys,subprocess,threading,urllib.parse
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/github_upload_1102'
ap=argparse.ArgumentParser();ap.add_argument('--base',default='https://nexuswebos.github.io/BulletsOfFury');ap.add_argument('--local-preview',action='store_true');args=ap.parse_args();base=args.base.rstrip('/');checks=[];errors=[];bad=[];ignored=[];server=None
if args.local_preview:
 S=R/'docs/previews/review_update_1102'
 class Handler(SimpleHTTPRequestHandler):
  def __init__(self,*a,**kw):super().__init__(*a,directory=str(S),**kw)
  def log_message(self,*a):pass
  def do_GET(self):
   name=urllib.parse.unquote(urllib.parse.urlsplit(self.path).path).removeprefix('/BulletsOfFury/');name=name or'index.html'
   if '..'in Path(name).parts:self.send_error(400);return
   self.path='/'+name
   if (S/name).is_file()or(S/name).is_dir():return super().do_GET()
   q=subprocess.run(['git','show','origin/gh-pages:'+name],cwd=R,capture_output=True)
   if q.returncode:self.send_error(404);return
   self.send_response(200);self.send_header('Content-Type',self.guess_type(name));self.send_header('Content-Length',str(len(q.stdout)));self.end_headers()
   try:self.wfile.write(q.stdout)
   except(ConnectionAbortedError,ConnectionResetError,BrokenPipeError):pass
 server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();base='http://127.0.0.1:'+str(server.server_port)+'/BulletsOfFury'
def clean(s):return re.sub(r'https?://[^\s]+',lambda m:m[0].split('?')[0],str(s))
def ck(name,data,ok):checks.append(dict(name=name,data=data,passed=bool(ok)));print('PASS'if ok else'FAIL',name,flush=True)
def console(message):
 if message.type!='error':return
 row=dict(text=clean(message.text),url=clean(message.location.get('url','')))
 (ignored if urllib.parse.urlsplit(row['url']).path=='/favicon.ico'else errors).append(row)
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1500,'height':1000});p.on('pageerror',lambda e:errors.append(clean(e)));p.on('console',console);p.on('response',lambda r:bad.append(dict(status=r.status,url=clean(r.url)))if r.status>=400 and not r.url.endswith('favicon.ico')else None)
 if args.local_preview:
  media={a['url']:'http://127.0.0.1:8805'+a['routes'][0]for a in json.loads((O/'plan.json').read_text())['media']}
  p.route('https://github.com/NexusWebOS/BulletsOfFury/releases/download/**',lambda route:route.fulfill(status=307,headers={'location':media.get(route.request.url,route.request.url.replace('https://github.com/NexusWebOS/BulletsOfFury/releases/download/','http://127.0.0.1:8805/_releases/'))}))
 def goto(path):return p.goto(base+'/'+path,wait_until='domcontentloaded',timeout=90000)
 goto('?revision=publication-1102');p.get_by_role('link',name='57 boss comparisons',exact=True).wait_for();ck('Public hub has current November2 feature links',None,p.get_by_role('link',name='Download playable build',exact=True).count()==1);p.screenshot(path=str(O/'public-hub.png'),full_page=True)
 goto('current/boss-comparison-1102.html');p.wait_for_function('typeof data!=="undefined"&&data.completed===57',timeout=90000);p.wait_for_function('videos.length===3&&videos.every(v=>v.readyState>=2)',timeout=180000);p.locator('#all').click();p.wait_for_timeout(1600);q=p.evaluate('videos.map(v=>({diff:v.dataset.diff,time:v.currentTime,width:v.videoWidth,muted:v.muted}))');ck('Three public release videos decode and play',q,len(q)==3 and all(v['time']>.5 and v['width']==1280 for v in q));p.locator('#pause').click();p.locator('#scrub').fill('12');p.locator('#scrub').dispatch_event('input');p.wait_for_function('videos.every(v=>Math.abs(v.currentTime-12)<.3)',timeout=90000);ck('Public release movies support synchronized seek',None,True);p.get_by_role('button',name='Listen to Hard',exact=True).click();ck('Only selected difficulty has audio enabled',None,p.evaluate('videos.filter(v=>!v.muted).length===1&&videos.find(v=>!v.muted).dataset.diff==="hard"'));p.locator('#pause').click();p.wait_for_function('[...document.querySelectorAll(".concepts img")].every(i=>i.complete&&i.naturalWidth>500)');ck('Four concept boards load from Pages',None,p.locator('.concepts img').count()==4);p.screenshot(path=str(O/'public-comparison.png'),full_page=True)
 p.locator('#stage').select_option('8');p.locator('#role').select_option('boss');p.wait_for_function('videos.length===3&&videos.every(v=>v.readyState>=1)',timeout=180000);p.locator('#transform').click();p.locator('#pause').click();p.wait_for_function('videos.every(v=>!v.seeking&&v.readyState>=2&&Math.abs(v.currentTime-v._row.chapters.find(c=>c.label==="Final transformation").seconds)<3)',timeout=180000);ck('Dracodia final transformation chapters seek on every difficulty',p.evaluate('videos.map(v=>({diff:v.dataset.diff,time:v.currentTime}))'),True);p.locator('#pause').click();p.screenshot(path=str(O/'public-transformations.png'),full_page=True)
 p.set_viewport_size({'width':390,'height':844});p.locator('#stage').select_option('1');p.locator('#role').select_option('mini');p.wait_for_timeout(250);ck('Comparison layout fits mobile',None,p.evaluate('document.documentElement.scrollWidth<=innerWidth'));p.screenshot(path=str(O/'public-mobile.png'),full_page=True);p.set_viewport_size({'width':1500,'height':1000})
 goto('current/all-waves-1101.html');p.wait_for_function('typeof library!=="undefined"&&library.levels.length===10',timeout=90000);ck('Ten regular-wave films expose all313 chapters',p.evaluate('library.levels.reduce((n,l)=>n+l.waves.length,0)'),p.evaluate('library.levels.reduce((n,l)=>n+l.waves.length,0)===313'));p.wait_for_function('video.readyState>=2',timeout=90000);p.locator('#full').click();p.wait_for_timeout(1200);ck('Regular-wave film plays from the public release',None,p.evaluate('video.currentTime>.3&&video.videoWidth===1280'));p.evaluate('video.pause()')
 goto('enemy-showcase-1031.html#enemy=stage9-cbreak');p.wait_for_function('typeof data!=="undefined"&&data.ready===154',timeout=90000);p.wait_for_function('document.querySelector("video").readyState>=2',timeout=90000);ck('Current154-enemy guide loads Current Breaker',p.locator('#title').inner_text(),p.evaluate('document.querySelector("video").videoWidth===1280'));p.screenshot(path=str(O/'public-enemies.png'),full_page=True)
 goto('game/index.html');links=p.locator('a[href$=".zip"]').evaluate_all('(a)=>a.map(e=>e.href)');ck('Playable build links all three verified packages',links,len(links)==3 and all('bof-complete-update-2026-11-02/'in x for x in links))
 for path,name in [('storyboard-1102.html','Dialogue storyboard'),('cast-cinematics-1102.html','Cast library'),('field-manual/guide.html','Existing full field manual')]:
  res=goto(path);p.wait_for_timeout(500);ck(name+' remains available',None,res.status==200 and p.locator('body').inner_text().strip()!='')
 ck('No public page, console or missing-resource errors',dict(errors=errors,responses=bad,ignoredRootFavicons=ignored),not errors and not bad);b.close()
if server:server.shutdown()
(O/('staged-site-playback.json'if args.local_preview else'public-playback.json')).write_text(json.dumps(checks,indent=2),encoding='utf-8');print('SUMMARY',sum(c['passed']for c in checks),'/',len(checks));sys.exit(0 if all(c['passed']for c in checks)else 1)
