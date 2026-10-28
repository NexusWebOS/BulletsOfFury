from pathlib import Path
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import sys,json,base64,io,time,argparse,numpy as np
R=Path(__file__).resolve().parents[2];W=R/'_shots/animation_audit_1023';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
ap=argparse.ArgumentParser();ap.add_argument('--diffs',nargs='+',default=['normal','hard','furious','easy']);ap.add_argument('--stages',nargs='+',type=int,default=list(range(1,10)));ap.add_argument('--limit',type=int,default=0);ap.add_argument('--output',default='enemy-native');args=ap.parse_args()
O=W/args.output;O.mkdir(exist_ok=True);(O/'frames').mkdir(exist_ok=True);(O/'issues').mkdir(exist_ok=True)
report_path=O/'report.json';report=json.loads(report_path.read_text())if report_path.exists()else{'cases':[],'errors':[],'cancelledMedia':[],'started':time.time()};done={r['id']for r in report['cases']};catalog=json.loads((W/'roster/catalog.json').read_text());port,stop=shoot.serve(str(R))
def im(s):return Image.open(io.BytesIO(base64.b64decode(s))).convert('RGBA')
def metrics(a,b):
 a=np.array(a);b=np.array(b);mask=(a[:,:,:3].max(2)>12)&(a[:,:,3]>30);body=int(mask.sum());dif=np.abs(a[:,:,:3].astype(int)-b[:,:,:3].astype(int));bright=(b[:,:,:3].astype(float)@np.array([.2126,.7152,.0722]))-(a[:,:,:3].astype(float)@np.array([.2126,.7152,.0722]));changed=int((mask&(dif.max(2)>35)&(bright>15)).sum());white=int((mask&(a[:,:,:3].sum(2,dtype=int)<690)&(b[:,:,:3].min(2)>232)).sum());return{'bodyPixels':body,'brightenedPixels':changed,'newWhitePixels':white,'visible':changed>=max(6,body*.008)or white>=max(6,body*.005)}
def save_report():report_path.write_text(json.dumps(report,indent=2))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1100,height=950));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:report['errors'].append({'case':report.get('current'), 'error':str(e)}));p.on('console',lambda m:(report['cancelledMedia']if 'ERR_ABORTED'in m.text else report['errors']).append({'case':report.get('current'),'error':m.text[:600]})if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.add_script_tag(path=str(Path(__file__).parent/'animation_enemy_lab_1023.js'))
  for diff in args.diffs:
   for stage in args.stages:
    specs=next(s['specs']for s in catalog['stages']if s['stage']==stage)
    p.evaluate('([s,d])=>EA11.setup(s,d)',[stage,diff]);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage);}')
    for index,spec in enumerate(specs):
     case_id=f'{diff}-s{stage}-{index:03}-{spec["type"]}'
     if case_id in done:continue
     if args.limit and len(report['cases'])>=args.limit:break
     report['current']=case_id;row={'id':case_id,'difficulty':diff,'stage':stage,'index':index,'spec':spec,'status':'pending','flash':None,'samples':[],'issues':[]};started=time.monotonic()
     try:
      ok=p.evaluate('s=>{const r=AQ23.begin(s);bossWarned=false;return r;}',spec)
      if not ok:row['status']='not_spawned';row['issues'].append('Replay did not create an actor; inspect authored spawn gating.')
      else:
       hit_done=False;last_sample=-100
       for batch in range(24):
        met=p.evaluate('()=>AQ23.step(40)');row['metrics']=met
        if met['visible'] and met['alive']:
         if not hit_done:
          p.wait_for_timeout(80);data=p.evaluate('()=>AQ23.draw(E)');normal=im(data['image']);pixels=int((np.array(normal)[:,:,:3].max(2)>12).sum())
          if pixels>6:
           native=p.evaluate('()=>AQ23.hit(E)');control=im(native['control']['image']);first=metrics(normal,im(native['native']['image']));marked=metrics(control,im(native['marked']['image']));p.wait_for_timeout(100);decoded=p.evaluate('()=>AQ23.draw(E)');decoded_metrics=metrics(control,im(decoded['image']));native2=None;guarded=p.evaluate('()=>!!E.enter||!!E._noHit')
           if not first['visible'] and decoded_metrics['visible']:
            again=p.evaluate('()=>AQ23.hit(E)');native2=metrics(im(again['control']['image']),im(again['native']['image']))
           row['flash']={'timerAfterNativeHit':native['timer'],'hpBefore':native['hpBefore'],'hpAfter':native['hpAfter'],'noHit':native['noHit'],'hitError':native['hitError'],'firstNative':first,'markedControl':marked,'decodedMarked':decoded_metrics,'secondNative':native2,'drawKeys':native['native']['keys']}
           hit_done=True;normal.save(O/'frames'/(case_id+'.webp'),lossless=True)
           actual=first['visible']or bool(native2 and native2['visible'])
           row['guardedEntryAtHit']=guarded
           if not actual and not native['noHit'] and not guarded:row['issues'].append('Native damage did not produce visible hull brightness change.')
           if not actual and not guarded and not marked['visible'] and not decoded_metrics['visible']:row['issues'].append('Controlled owner flash did not produce visible hull brightness change.')
           if not first['visible'] and native2 and native2['visible']:row['issues'].append('First-hit flash needed a later asset decode; investigate preload.')
           if row['issues']:
            contact=Image.new('RGBA',(normal.width*3,normal.height));contact.alpha_composite(control,(0,0));contact.alpha_composite(im(native['native']['image']),(normal.width,0));contact.alpha_composite(im(decoded['image']),(normal.width*2,0));contact.save(O/'issues'/(case_id+'.png'))
         if batch-last_sample>=4:
          data=p.evaluate('()=>AQ23.draw(E)');row['samples'].append({'batch':batch,'keys':data['keys'],'pixels':int((np.array(im(data['image']))[:,:,:3].max(2)>12).sum())});last_sample=batch
        if not met['alive']:break
        if batch%4==0:p.wait_for_timeout(3)
       row['status']='observed'if row['flash']else'not_visible_or_no_hull';row['flashExpired']=p.evaluate('()=>!E||E.flash<=0||E.dead||E._dyingT!=null');row['metrics']=p.evaluate('()=>AQ23.step(0)')
       if not row['flashExpired']:row['issues'].append('Owner flash remained after native update playback.')
       if row['metrics']['geometry']:row['issues'].append('Native renderer requested invalid image geometry.')
       if not row['metrics']['finite']:row['issues'].append('Nonfinite actor/projectile position.')
       if not row['flash']:row['issues'].append('No visible hull reached the inspection viewport; diagnostic placement required.')
     except Exception as e:row['status']='exception';row['issues'].append(str(e))
     row['wallSeconds']=round(time.monotonic()-started,2);report['cases'].append(row);done.add(case_id);save_report()
     if index%5==0 or row['issues']:print(json.dumps({'case':case_id,'status':row['status'],'issues':row['issues'],'done':len(report['cases'])}),flush=True)
    print(json.dumps({'completedStage':stage,'difficulty':diff,'total':len(report['cases'])}),flush=True)
  br.close()
finally:stop();save_report()
print(json.dumps({'cases':len(report['cases']),'issues':sum(bool(r['issues'])for r in report['cases']),'errors':len(report['errors'])}))
