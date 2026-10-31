from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/dracodia_return_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;errors=[];checks=[];states=[];port,stop=serve(str(R))
def check(name,value):
 checks.append({'name':name,'passed':bool(value)});print(('PASS 'if value else'FAIL ')+name,flush=True)
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  for form in [8,1,6,2]:
   for last in [False,True]:
    setup=p.evaluate('''([form,last])=>{
     spawnBoss('vileexistence');window.B=boss;const J=j3State(B);v18Enter(B,2,0);
     J.hp[0]-=200;B.hp=J.hp[0];J.modules[0].find(p=>p.id==='left').hp=0;J.modules[0].find(p=>p.id==='left').destroyed=true;
     if(last)for(const i of V18.forms)if(i!==0&&i!==form)J.hp[i]=0;
     v18Enter(B,2,form);B._r30.mode='fight';B.enter=B._noHit=false;B.hp=0;
     window.before={hp:J.hp.slice(),main:J.hp[0],mainParts:J.modules[0].map(p=>({id:p.id,hp:p.hp,destroyed:p.destroyed}))};
     RD76.events=[];r30Break(B);return{mode:B._r30.mode,max:J.max[0],...before};}''',[form,last])
    label=f'form{form} '+('last life'if last else'earlier return')
    check(label+' uses native copied-life defeat',setup['mode']=='v19copyDeath')
    p.evaluate(STEP,175)
    start=p.evaluate('({mode:B._r30.mode,t:rd76State(B)?.t,last:rd76State(B)?.last,form:B._r30.v18.form,targets:retinaBossTargets(B).length,protected:B._noHit,locked:dr5Locked()})')
    check(label+' enters protected download',start['mode']=='v18returnDownload'and start['protected']and start['targets']==0 and start['last']==last)
    p.evaluate(STEP,95)
    build=p.evaluate('({mode:B._r30.mode,t:rd76State(B)?.t,form:B._r30.v18.form,arena:B._r30.v18.arenaCurrent,phase:B._r30.v18.arenaPhase,hp:B.hp,parts:B.parts.map(p=>({id:p.id,hp:p.hp,max:p.maxhp,destroyed:p.destroyed})),draws:RD76.draws})')
    check(label+' returns to main arena with original HP',build['form']==0 and build['arena']=='void'and build['phase']==2 and build['hp']==setup['main'])
    left=next(q for q in build['parts']if q['id']=='left')
    check(label+' applies limb exception',left['destroyed']==last and left['hp']==(0 if last else left['max']))
    if form==8:
     p.screenshot(path=str(W/('last-life-download.png'if last else'healthy-download.png')))
    p.evaluate(STEP,180)
    end=p.evaluate('({mode:B._r30.mode,form:B._r30.v18.form,hp:B.hp,pools:j3State(B).hp.slice(),parts:B.parts.map(p=>({id:p.id,hp:p.hp,destroyed:p.destroyed})),transition:rd76State(B)||rd30State(B).transition,events:RD76.events,protected:B._noHit,enter:B.enter,targets:retinaBossTargets(B).length})')
    check(label+' completes and restores native combat',end['mode']=='fight'and end['form']==0 and not end['transition']and not end['enter'])
    expected=setup['hp'][:];expected[form]=0
    check(label+' never heals or resurrects life pools',end['pools']==expected and end['hp']==setup['main'])
    check(label+' commits exactly once',sum(e['event']=='arena-restored'for e in end['events'])==1 and sum(e['event']=='return-complete'for e in end['events'])==1)
    check(label+' preserves final-life vulnerability',end['targets']>0 if last else end['targets']==0)
    states.append({'form':form,'last':last,'start':start,'build':build,'end':end})
  # Defeating the real last pool must use the original ending, with no new repair.
  p.evaluate('''()=>{spawnBoss('vileexistence');window.B=boss;const J=j3State(B);for(const i of V18.forms)if(i!==0)J.hp[i]=0;v18Enter(B,2,0);B._r30.mode='fight';B.enter=B._noHit=false;B.hp=0;RD76.events=[];r30Break(B);}''')
  p.evaluate(STEP,200);end=p.evaluate('({mode:B._r30.mode,hp:B.hp,pools:j3State(B).hp.slice(),events:RD76.events})')
  check('True final life proceeds to original final destruction',end['mode']=='dr5Death'and end['hp']==0 and not end['events'])
  check('Authored download frames were drawn',p.evaluate('RD76.draws')>0)
  check('No native/browser drawing errors',not errors)
  br.close()
finally:stop();(W/'checks.json').write_text(json.dumps({'method':'Native death-boundary checkpoints; damaged home-limb fixture, real copied-death tick, download, arena, rendering and ending. No claim of full encounter balance.', 'checks':checks,'states':states,'errors':errors},indent=2))
assert all(c['passed']for c in checks),[c['name']for c in checks if not c['passed']]
