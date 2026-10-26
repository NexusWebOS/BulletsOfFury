from pathlib import Path
import json,urllib.request
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/storyroom_1024';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
def ck(n,ok,data=None):checks.append(dict(name=n,passed=bool(ok),data=data));print(('PASS 'if ok else'FAIL ')+n,flush=True)
url='http://127.0.0.1:8795'
original=json.load(urllib.request.urlopen(url+'/api/storyboard'))['project']
def restore():
 req=urllib.request.Request(url+'/api/storyboard/save',data=json.dumps(original).encode(),headers={'Content-Type':'application/json','Origin':url},method='POST');urllib.request.urlopen(req).read()
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);context=br.new_context(viewport={'width':1600,'height':1000});p=context.new_page();p.set_default_timeout(180000)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400]+' '+str(m.location))if m.type=='error'else None)
  p.goto(url+'/tools/storyboard/');p.wait_for_function("document.querySelectorAll('.scene').length>20")
  row=p.evaluate('({scenes:catalog.length,pilots:api.pilots.length,shots:cards().length})');ck('Native scene catalog and nine pilot versions load',row['scenes']>=24 and row['pilots']==9 and row['shots']>10,row)
  p.locator('[data-scene="post-3"]').click();p.wait_for_timeout(1500);p.screenshot(path=str(O/'storyboard-initial.png'));print(p.evaluate("()=>{const c=document.querySelector('.card'),b=c.querySelector('.card-body');return {card:c.getBoundingClientRect().height,body:b.getBoundingClientRect().height,template:getComputedStyle(document.getElementById('board')).gridTemplateRows,line:c.querySelector('.line').getBoundingClientRect().height}}"),flush=True)
  ck('Storyboard cards visibly contain their dialogue',p.evaluate("()=>{const c=document.querySelector('.card'),line=c.querySelector('.line');return line.getBoundingClientRect().bottom<c.getBoundingClientRect().bottom}"));old=p.locator('#dialogue').input_value();p.locator('#dialogue').fill('Storyroom QA: the ice relay is silent.');p.locator('#speaker').click()
  ck('Dialogue edits update their storyboard card',p.locator('.card.selected .line').inner_text()=='Storyroom QA: the ice relay is silent.')
  p.locator('#moveDown').click();ck('Move shot changes actual source order',p.evaluate('cards()[1].source===0&&cards()[1].fields.text.startsWith("Storyroom QA")'))
  p.locator('#undo').click();ck('Undo restores the earlier order',p.evaluate('cards()[0].source===0&&cards()[0].fields.text.startsWith("Storyroom QA")'))
  p.locator('#redo').click();ck('Redo restores the edited order',p.evaluate('cards()[1].source===0'));p.locator('.card[data-i="1"]').drag_to(p.locator('.card[data-i="2"]'));ck('Native drag and drop reorders storyboard cards',p.evaluate('cards()[2].source===0'));p.locator('#undo').click()
  p.locator('#pilot').select_option('cole');ck('Other pilot version remains untouched',not p.locator('#dialogue').input_value().startswith('Storyroom QA'))
  p.locator('#pilot').select_option('yuri');p.locator('.card[data-i="1"]').click();p.locator('#playScene').click()
  frame=p.frame_locator('#game');p.wait_for_function("document.getElementById('game').contentWindow.BOFCinematicDirector.current?.id==='storyboard-preview'")
  row=p.evaluate("()=>{const w=document.getElementById('game').contentWindow;return w.BOFCinematicDirector.current.beats.map(b=>b.text)}")
  ck('Native cinematic rehearsal uses edited order and dialogue',row[1].startswith('Storyroom QA'),row[:3])
  p.locator('#pause').click();p.screenshot(path=str(O/'storyboard-editing.png'))
  p.locator('#stop').click()
  with p.expect_download()as pending:p.locator('#export').click()
  downloaded=pending.value;downloaded.save_as(str(O/'exported-project.json'));ck('Export produces the editable project',json.load(open(O/'exported-project.json'))['version']==1)
  p.locator('#importFile').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':b'{"version":99}'})
  p.wait_for_function("document.getElementById('toast').textContent.includes('version 1')");ck('Invalid imports do not replace the draft',p.evaluate('project.overrides["post-3"].yuri[1].fields.text.startsWith("Storyroom QA")'))
  imported=p.evaluate('project');imported['overrides']['post-3']['yuri'][0]['notes']='Imported director note'
  p.locator('#importFile').set_input_files({'name':'valid.json','mimeType':'application/json','buffer':json.dumps(imported).encode()});p.locator('#acceptConfirm').click()
  ck('JSON imports preserve editable shot notes',p.evaluate('project.overrides["post-3"].yuri[0].notes==="Imported director note"'))
  p.wait_for_timeout(450);draft=p.context.new_page();draft.goto(url+'/tools/storyboard/');draft.wait_for_function('typeof api!=="undefined"&&!!api&&catalog.length>20')
  ck('Local draft recovers after reopening the editor',draft.evaluate('!!project.overrides["post-3"]&&dirty'));draft.close()
  p.locator('#apply').click();p.wait_for_function("document.getElementById('saveState').textContent==='Game version is up to date'")
  disk=json.load(urllib.request.urlopen(url+'/api/storyboard'))['project'];ck('Apply persists real runtime data',disk['overrides']['post-3']['yuri'][1]['fields']['text'].startswith('Storyroom QA'))
  game=br.new_page();game.on('pageerror',lambda e:errors.append(str(e)));game.goto(url+'/index.html?storyroom-qa=1');game.wait_for_function('!!window.BOF_STORYBOARD')
  row=game.evaluate("()=>{run.pilot='yuri';window.callback24=0;BOFCinematicDirector.cancel();BOFCinematicDirector.play('post-3',BOFCinematicDirector.script(3,'yuri'),()=>callback24++);const texts=BOFCinematicDirector.current.beats.map(b=>b.text);BOFCinematicDirector.finish();BOFCinematicDirector.finish();return{texts,callback:callback24}}")
  ck('Fresh game loads saved edits and preserves callback once',row['texts'][1].startswith('Storyroom QA') and row['callback']==1,row['texts'][:3])
  row=game.evaluate("()=>{const d={version:1,overrides:{},triggers:{'post-2':'post-4'},order:[]};BOF_STORYBOARD.setData(d);BOFCinematicDirector.play('post-2',BOFCinematicDirector.script(2,'yuri'),()=>{});const actual=BOFCinematicDirector.current.beats[0].text,expected=BOFCinematicDirector.script(4,'yuri')[0].text;BOFCinematicDirector.cancel();return{actual,expected}}")
  ck('Scene game-event reassignment selects correct native sequence',row['actual']==row['expected'],row)
  p.set_viewport_size({'width':1100,'height':850});p.screenshot(path=str(O/'storyboard-1100.png'));ck('Editor fits 1100px without horizontal overflow',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  p.set_viewport_size({'width':480,'height':900});p.screenshot(path=str(O/'storyboard-480.png'));ck('Narrow editor remains accessible',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  ck('No page/console errors',not errors,errors);br.close()
finally:restore()
out=dict(passed=sum(c['passed']for c in checks),failed=sum(not c['passed']for c in checks),checks=checks,errors=errors);(O/'report.json').write_text(json.dumps(out,indent=2)+'\n');print('SUMMARY',out['passed'],out['failed']);raise SystemExit(bool(out['failed']))
