from pathlib import Path
import ast,sys,json,base64
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;W.mkdir(exist_ok=True);(W/'references').mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
from barrage_review_common_1025 import boot
seed=(W/'seed119.js').read_text(encoding='utf8')
INSTRUMENT="""()=>{window.PERF1110={fn:{},frames:[],canvas:0};for(const name of ['drawWorld','updatePlay','hammerBossDraw','cgWithGlow','cgUnder','cgOver','cgRings','cgSwirl','cgDrive','c45Aura','c45AuraMask','c45Body','c45Strikes','cgBolt','c32Pose','c32Hands']){const orig=window[name];if(typeof orig!=='function')continue;window[name]=function(...a){const t=performance.now();try{return orig.apply(this,a)}finally{const d=performance.now()-t,q=PERF1110.fn[name]||(PERF1110.fn[name]={calls:0,total:0,max:0});q.calls++;q.total+=d;q.max=Math.max(q.max,d)}};}const create=document.createElement;document.createElement=function(n,...a){if(n==='canvas')PERF1110.canvas++;return create.call(this,n,...a)};let previous;window.perf1110Live=true;function sample(t){if(!perf1110Live)return;if(previous!=null)PERF1110.frames.push(t-previous);previous=t;requestAnimationFrame(sample)};requestAnimationFrame=__bofRealRAF;requestAnimationFrame(loop);requestAnimationFrame(sample);}"""
def summarize(q):
 fs=sorted(q['frames']);return dict(frames=len(fs),fps=round(1000*len(fs)/sum(fs),2)if fs else 0,p95=round(fs[int(len(fs)*.95)],2)if fs else 0,max=round(max(fs),2)if fs else 0,over50=sum(f>50 for f in fs),canvas=q['canvas'],functions=sorted(q['fn'].items(),key=lambda v:-v[1]['total']))
errors=[];results=[];port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,5,errors,'boss');p.wait_for_function('()=>{stageLoadTick();return ba119Warm(5)&&c29Warm()&&c30Warm()&&c32Warm()}',polling=50,timeout=180000);p.evaluate(seed)
  refs=p.evaluate("""()=>{const out={};for(const [n,a]of [['chronos-rage-start',c29Row('rage',2,'regular')],['chronos-rage-roar',c29Row('rage',9,'red')],['chronos-volley-left',C32_ART.banks.palms[C32_ART.leftFrame]],['chronos-volley-right',C32_ART.banks.palms[C32_ART.rightFrame]]]){const c=document.createElement('canvas');c.width=a.w;c.height=a.h;c.getContext('2d').drawImage(XART.get(a.key),0,0);out[n]=c.toDataURL('image/png').split(',')[1]}return out;}""")
  for n,b in refs.items():(W/'references'/f'{n}.png').write_bytes(base64.b64decode(b))
  p.evaluate(INSTRUMENT)
  for phase in ['charge','volley']:
   p.evaluate("""phase=>{seed119('furious','regular');const h=B._hammer;h._c45Burst=false;h._c45AfterDone=true;h.hb20Pickup=null;h.frArmor.hp=0;h.c29Break=null;h.c27RagePending=true;B.hp=B.maxhp*.1;B.x=worldWidth()/2;B.y=viewTopY()+230;const hold=Input.hold;Input.hold=function(...a){return a.includes('fire')?false:hold.apply(this,a)};if(phase==='charge')hf22BeginBlueRage(B);else{h._hf22Charge=null;h._hf22Red=true;h._c46Done=true;h.c30=null;c30Start(B);}PERF1110.frames=[];PERF1110.fn={};PERF1110.canvas=0;}""",phase)
   p.wait_for_timeout(phase=='charge'and 8500 or 7000);q=p.evaluate('PERF1110');results.append(dict(phase=phase,**summarize(q)));p.screenshot(path=str(W/(phase+'-baseline.png')));print(json.dumps(results[-1]),flush=True)
  p.evaluate('perf1110Live=false');br.close()
finally:stop()
(W/('profile-after.json'if '--after'in sys.argv else'profile-before.json')).write_text(json.dumps(dict(results=results,errors=errors),indent=2));print('Errors',errors,flush=True)
