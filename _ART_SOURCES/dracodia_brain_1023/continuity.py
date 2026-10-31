from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(name,ok,data):checks.append({'name':name,'passed':bool(ok),'data':data});print(('PASS 'if ok else'FAIL ')+name+' '+json.dumps(data),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for f in ['balance_lab_1007.js','animation_audit_1023/hammer_review_lab_1023.js']:p.add_script_tag(path=str(R/'_BUILD_SOURCE'/f))
  ev=p.evaluate;ev('BAL7.setup({stage:8,kind:"vileexistence",pilot:"cole",diff:"normal",fire:false,seconds:60})');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&nb23Warm();}')
  row=ev('''()=>{HR23.clean();v18Budget(B);v18Enter(B,2,0);v18Fight(B);j3State(B).attacks=D20.book.length;j3Morph(B,6);const seen=[];for(let i=0;i<205;i++){r30Tick(B,1/60);if(!seen.includes(B._r30.mode))seen.push(B._r30.mode);}drawWorld(0);return{seen,form:B._r30.v18.form,mode:B._r30.mode,model:v18Model(B)};}''');ck('Native main-to-brain morph reaches the new form and resumes combat',row['model']=='brain'and row['mode']=='fight'and'v18formOut'in row['seen']and'v18formIn'in row['seen'],row)
  row=ev('''()=>{v18Clear(B);v18Fight(B);modularHit(37);const hp=B.hp;j3State(B).attacks=3;B._r30.cd=0;r30Tick(B,1/60);const pending=B._r30.v18.to;for(let i=0;i<205;i++)r30Tick(B,1/60);return{pending,model:v18Model(B),mode:B._r30.mode,saved:j3State(B).hp[6],expected:hp};}''');ck('After its3 attacks the brain naturally morphs home with damage saved',row['pending']==0 and row['model']=='colossus'and row['mode']=='fight'and row['saved']==row['expected'],row)
  ev('BAL7.setup({stage:6,kind:"warhive",pilot:"cole",diff:"normal",fire:false,seconds:60})');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6);}')
  row=ev('''()=>{HR23.clean();updateBoss(1/60);drawWorld(0);return{stage:run.stage,kind:B.kind,native:!!B._whv,brain:nb23Own(B),formNames:V18.forms.map(k=>V18.names[k])};}''');ck('Standalone Stage6 Harrier remains its original aircraft encounter',row['stage']==6 and row['kind']=='warhive'and row['native']and not row['brain'],row)
  br.close()
finally:stop()
ck('No continuity page errors',not errors,errors);out={'checks':checks,'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks),'errors':errors};(W/'review/continuity.json').write_text(json.dumps(out,indent=2));sys.exit(bool(out['failed']))
