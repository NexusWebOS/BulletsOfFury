from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':960,'height':768});p.goto(f'http://127.0.0.1:{port}/index.html?quality=high');p.wait_for_function('window.__bofFrames>5',timeout=180000)
  p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate("EA11.setup(5,'furious')")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)}',timeout=180000,polling=20)
  p.evaluate('()=>{for(const m of Object.values(S511_ART.models))XART.rdy(m.bank.key);for(const b of Object.values(S511_ART.banks))XART.rdy(b.key);}')
  p.wait_for_function('()=>[...Object.values(S511_ART.models).map(m=>m.bank),...Object.values(S511_ART.banks)].every(b=>XART.rdy(b.key))',timeout=60000,polling=20)
  result=p.evaluate('''()=>{let checks=0,bad=[];PXG.active=null;ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;
   for(const M of [S511_ART.models.frigate.bank,S511_ART.models.rammer.bank,S511_ART.models.leech.bank,S511_ART.banks.thruster,S511_ART.banks.laser]){
    const registered=M.key.startsWith('r46_'),original=registered?SP116.base.r46:SP116.base.v31,current=registered?r46Blit:v31Blit;
    const frames=registered?[0,16,56]:[0,Math.min(3,M.frames-1)];
    for(const frame of frames)for(const a of [.4,3.14])for(const color of [null,'#ffffff','#ff3b30','#83d9ff','#000000']){
     const args=[M,frame,a,150.25,155.75,143.5,color,.77];ctx.clearRect(0,0,320,320);original(...args);const before=ctx.getImageData(0,0,320,320).data;
     ctx.clearRect(0,0,320,320);current(...args);const after=ctx.getImageData(0,0,320,320).data;let mismatch=0,maxDiff=0,alphaDiff=0;
     for(let i=0;i<before.length;i++)if(before[i]!==after[i]){mismatch++;maxDiff=Math.max(maxDiff,Math.abs(before[i]-after[i]));if(i%4===3)alphaDiff++;}
     checks++;if(maxDiff>2||alphaDiff)bad.push({key:M.key,frame,a,color,mismatch,maxDiff,alphaDiff});
    }
   }return {checks,bad,edgeRGBTolerance:2,alphaTolerance:0,pages:Object.keys(SP116_ART.pages).length,draws:SP116.draws,misses:SP116.misses,fallbacks:SP116.fallbacks,bytes:SP116.bytes};}''')
  (W/'page-runtime-verification.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result),flush=True);assert not result['bad'];assert result['misses']==result['fallbacks']==0;b.close()
finally:stop()
