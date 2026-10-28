from pathlib import Path
import sys,ast,json,base64,hashlib
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/stage2_peak_1021';O.mkdir(exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
port,stop=shoot.serve(str(R));errors=[];checks=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,ok=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 if not ok:raise AssertionError(name)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1366,'height':900});p.set_default_timeout(120000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>3&&typeof ht27Stop==="function"');p.evaluate(shoot.TRAP_RAF)
  for diff in ['easy','normal','hard','furious']:
   p.evaluate(SETUP,{'stage':2,'pilot':'cole','diff':diff,'kind':'infernoreaver'})
   p.wait_for_function('()=>{const c=_levelCfg();_liquidFrames(c.liquid);return XART.rdy(c.master)&&BOFSTAGE2LAVA.ready;}')
   result=p.evaluate('''()=>{const failures=[];let inspected=0;const original=ctx.drawImage;
    for(const fit of [0,1]){VIEW_FIT=fit;const H=Math.round(viewH()),top=Math.round(viewTopY()),W=worldWidth();
     for(const gap of [0,1,200,800,1600])for(const fraction of [0,.125,.25,.375,.5,.625,.75,.875,1]){
      mapScroll=levelScrollRange()-gap;_bossHold=1;drawLevelMaster._l2Join=H*fraction;
      const actual=document.createElement('canvas'),expected=document.createElement('canvas');actual.width=expected.width=W;actual.height=expected.height=H;
      const a=actual.getContext('2d'),e=expected.getContext('2d');a.imageSmoothingEnabled=e.imageSmoothingEnabled=false;a.translate(0,-top);e.translate(0,-top);
      let im=XART.get(_levelCfg().master),calls=[];
      ctx.drawImage=function(image,...args){if((image.naturalWidth||image.width)===680&&(image.naturalHeight||image.height)===4080){a.drawImage(image,...args);calls.push(args);}return original.call(this,image,...args);};
      try{ctx.setTransform(1,0,0,1,0,0);ctx.imageSmoothingEnabled=false;drawLevelMaster(0);}finally{ctx.drawImage=original;}
      // Independent reference: place the WHOLE authored terrain at its published
      // world position; let the canvas viewport do the clipping, never a crop.
      e.drawImage(im,0,-_masterSrcY);
      const A=a.getImageData(0,0,W,H).data,E=e.getImageData(0,0,W,H).data;let mismatch=0;
      for(let i=0;i<A.length;i+=4)if(A[i+3]!==E[i+3]||(A[i+3]&&(A[i]!==E[i]||A[i+1]!==E[i+1]||A[i+2]!==E[i+2])))mismatch++;
      if(mismatch)failures.push({fit,gap,fraction,mismatch,calls});
      if(calls.some(c=>c[5]>top+.01&&c[1]>.01))failures.push({fit,gap,fraction,cutTop:true,calls});
      inspected++;
     }
    }VIEW_FIT=0;return{inspected,failures};}''')
   ck(diff+' full terrain matches uncropped authored reference',result['inspected']==90 and not result['failures'],result)
  for gap in [0,200,800,1600]:
   for dy in [0,160,400,512]:
    q=p.evaluate('''([gap,dy])=>{VIEW_FIT=0;mapScroll=levelScrollRange()-gap;_bossHold=1;drawLevelMaster._l2Join=dy;shake=0;ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);drawWorld(0);return cv.toDataURL().split(',')[1];}''',[gap,dy]);(O/f'after-gap{gap}-dy{dy}.png').write_bytes(base64.b64decode(q))
  # Advance the real transition clock, with the native boss and no artificial
  # join writes, and verify full exit/reset/retry plus the independently flowing bed.
  p.evaluate('''()=>{mapScroll=levelScrollRange()-200;_bossHold=1;drawLevelMaster._l2Join=0;window.savedHP=boss.hp;window.samples=[];for(let n=0;n<180;n++){drawLevelMaster(1/60);samples.push(drawLevelMaster._l2Join);} }''')
  ck('Native join finishes on its original clock',p.evaluate('samples[0]>0&&samples.at(-1)===Math.round(viewH())&&samples.every((v,i)=>!i||v>=samples[i-1])'))
  ck('Transition never changes boss health',p.evaluate('boss.hp===savedHP'))
  ck('Published ground coordinates put the entire mountain below view',p.evaluate('_masterSrcY<=-VH'))
  p.evaluate('()=>{boss=null;bossActive=false;bossDefeated=false;_arenaHold=false;drawLevelMaster(0);}')
  ck('Retry clears the arena join',p.evaluate('drawLevelMaster._l2Join===0'))
  p.evaluate('()=>{efxClock=0;drawLevelMaster(0);window.oldFrame=BOFSTAGE2LAVA.phase;efxClock=0.2;drawLevelMaster(0);}')
  ck('Lava keeps its independent animated frames',p.evaluate('BOFSTAGE2LAVA.phase!==oldFrame'))
  ck('No browser errors',not errors,errors);b.close()
finally:
 stop();(O/'verification.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf-8')
print('COMPLETE',len(checks),'checks',flush=True)
