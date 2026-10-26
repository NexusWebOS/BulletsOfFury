"""Native ColeForge V7 UI and authoring QA. Reuses shoot.py's real HTTP server.

python _BUILD_SOURCE/probe_coleforge_ui_1011.py
All temporary captures/downloads stay in ignored _shots/. No game state fixtures.
"""
from pathlib import Path
import json, struct, sys, wave
from PIL import Image
from playwright.sync_api import sync_playwright
import shoot

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/coleforge_v7_1011'; OUT.mkdir(parents=True,exist_ok=True)
REPORT=ROOT/'_SFXGenerator_upload/docs/QA_UI_V7_1011.json'
checks=[];page_errors=[];console_errors=[];failed_requests=[]
def check(value,name,details=None):
    result={'name':name,'passed':bool(value)}
    if details is not None:result['details']=details
    checks.append(result);print(('ok   ' if value else 'FAIL ')+name,flush=True)

def no_overflow(page,label):
    data=page.evaluate('''() => ({viewport:innerWidth,width:document.documentElement.scrollWidth,
      visible:[...document.querySelectorAll('main')].filter(m=>!m.hidden).map(m=>m.id)})''')
    check(data['width']<=data['viewport'],label+' fits viewport',data)

def capture(page,name,full=False):page.screenshot(path=str(OUT/name),full_page=full)

def download(page,button,name):
    with page.expect_download() as event:page.locator(button).click()
    d=event.value;path=OUT/name;d.save_as(path);check(path.stat().st_size>32,'actual '+name+' download');return path

def run():
    port,close=shoot.serve(str(ROOT))
    try:
      with sync_playwright() as pw:
        browser=pw.chromium.launch()
        context=browser.new_context(viewport={'width':1600,'height':1000},accept_downloads=True)
        page=context.new_page()
        page.on('pageerror',lambda e:page_errors.append(str(e)))
        page.on('console',lambda e:console_errors.append(e.text) if e.type=='error' else None)
        page.on('requestfailed',lambda r:failed_requests.append({'url':r.url,'failure':r.failure}))
        page.goto(f'http://127.0.0.1:{port}/_SFXGenerator_upload/index.html',wait_until='networkidle')
        page.wait_for_function('!!window.ColeForgeUI')
        page.evaluate('document.fonts.ready')
        check(page.evaluate('document.fonts.check(\'16px "ColeForge Circuit"\')'),'custom WOFF2 loads in native Chromium')
        check(page.locator('.brand-copy h1').inner_text()=='COLEFORGE V7.0','visible V7.0 brand')
        check(page.locator('.boot-hit').is_visible(),'generated V7 boot has visible entry control')
        capture(page,'boot_desktop.png')
        original=page.evaluate('JSON.stringify(ColeSoundForge.getCurrentPatch())')
        page.keyboard.press('Tab');check(page.locator('.boot-hit').evaluate('(e)=>e===document.activeElement'),'boot traps keyboard focus')
        page.keyboard.press('Enter');page.wait_for_timeout(300)
        check(page.locator('#boot-screen').get_attribute('aria-hidden')=='true','keyboard enters studio')
        check(page.evaluate('JSON.stringify(ColeSoundForge.getCurrentPatch())')==original,'boot key does not edit hidden synth')
        check(page.locator('#chip-workspace').is_visible() and page.locator('main:visible').count()==1,'Genesis opens as sole default workspace')
        no_overflow(page,'desktop Genesis')
        check(page.locator('#studio-status').inner_text()=='CHIP READY','status belongs to selected mode')
        page.locator('#chip-cats .preset-main').filter(has_text='BRAWLER POWER HOOK').click()
        page.locator('#chip-stop').click()
        check(page.locator('#chip-name').inner_text()=='BRAWLER POWER HOOK','signature preset loads design')
        check(page.locator('#chip-count').inner_text()=='042','all 42 authored presets available')
        check(page.locator('.chip-op').count()==4 and page.locator('.chip-op[open]').count()==1,'four operators have collapsible controls')
        page.locator('.chip-op').nth(1).locator('summary').click()
        check(page.locator('.chip-op[open]').count()==2,'operator disclosure opens with native button action')
        before=page.evaluate('ColeForgeChip.state.design.fm[0].hz')
        first=page.locator('#chip-editor .chip-field input[type=range]').first
        first.fill(str(before+20));first.dispatch_event('input');page.wait_for_timeout(120)
        check(page.evaluate('ColeForgeChip.state.design.fm[0].hz')==before+20,'pitch control changes the actual design')
        check(float(first.evaluate('(e)=>parseFloat(e.style.getPropertyValue("--range-fill"))'))>0,'slider fill follows actual control value')
        page.locator('.studio-strip h2').click()
        page.keyboard.press('Space')
        check(page.evaluate('!!ColeForgeChip.state.src'),'Space plays active chip source')
        check(page.evaluate('ColeForgeChip.state.ctx.state')=='running','WebAudio context runs')
        check(page.evaluate('JSON.stringify(ColeSoundForge.getCurrentPatch())')==original,'chip playback leaves hidden synth intact')
        page.keyboard.press('Escape');check(page.evaluate('ColeForgeChip.state.src===null'),'Escape stops audition')
        capture(page,'chip_desktop.png')
        pixel=page.evaluate('''() => {const c=document.getElementById('chip-scope'),g=c.getContext('2d');const p=g.getImageData(0,0,c.width,c.height).data;let signal=0,amber=0;for(let i=0;i<p.length;i+=4){if(p[i+1]>120&&p[i+2]>120&&p[i]<p[i+1])signal++;if(p[i]>150&&p[i+1]>100&&p[i+2]<130)amber++;}return {signal,amber};}''')
        check(pixel['signal']>1000 and pixel['amber']>500,'native monitor contains real waveform and pitch pixels',pixel)
        for tab in ['NOISE','PSG','GLOBAL']:
            page.locator('#chip-tabs button').filter(has_text=tab).click()
            check(page.locator('#chip-editor').locator('input').count()>0,tab+' editor opens')
        page.locator('#chip-tabs button').filter(has_text='FM1').click()
        page.locator('#chip-search').fill('laser')
        check(0<page.locator('#chip-cats .preset-main').count()<42,'preset search filters library')
        page.locator('#chip-search').fill('')
        wavpath=download(page,'#chip-wav','ui_export.wav')
        with wave.open(str(wavpath)) as w:
            check(w.getnchannels()==2 and w.getsampwidth()==2 and w.getnframes()>500,'WAV is real stereo PCM audio')
        vgmpath=download(page,'#chip-vgm','ui_export.vgm')
        check(vgmpath.read_bytes()[:4]==b'Vgm ','VGM has valid register-log header')
        recipepath=download(page,'#chip-json','ui_export.recipe.json')
        recipe=json.loads(recipepath.read_text());check(bool(recipe.get('design') and recipe.get('fm')),'recipe preserves design and tracks')
        page.locator('#chip-file').set_input_files(str(vgmpath))
        page.wait_for_function('ColeForgeChip.state.mode==="recipe"')
        check(page.locator('#chip-morph-panel').is_visible(),'VGM imports into editable recipe with morph controls')
        trans=page.locator('#chip-morph input').first;trans.fill('5');trans.dispatch_event('input');page.wait_for_timeout(120)
        check(page.evaluate('ColeForgeChip.state.morph.transpose')==5,'imported recipe transpose works')
        capture(page,'chip_imported_recipe.png')
        page.locator('#chip-todesign').click();check(page.evaluate('ColeForgeChip.state.morph.transpose')==0,'original recipe restores')
        page.locator('#chip-file').set_input_files(str(recipepath));page.wait_for_function('ColeForgeChip.state.mode==="design"')
        check(page.evaluate('ColeForgeChip.state.design.name')==recipe['design']['name'],'JSON design re-imports intact')
        page.locator('#chip-play').click();page.locator('#mode-synth').click()
        check(page.evaluate('ColeForgeChip.state.src===null'),'switching modes stops chip audio')
        check(page.locator('main:visible').count()==1 and page.locator('#synth-workspace').is_visible(),'synth mode shows one workspace')
        no_overflow(page,'desktop synth');capture(page,'synth_desktop.png')
        page.locator('#play').click();page.locator('#stop').click()
        check(page.locator('#play').is_visible(),'generated synth transport remains interactive')
        page.locator('#mode-sample').click()
        page.wait_for_function('document.querySelectorAll(".sample-main").length>0')
        check(page.locator('main:visible').count()==1 and page.locator('#sample-workspace').is_visible(),'sample mode shows one workspace')
        no_overflow(page,'desktop sample');capture(page,'sample_desktop.png')
        check(page.locator('.sample-pad').count()==16,'sixteen playable sample pads remain')
        page.locator('#sample-play').click();page.locator('#sample-stop').click()
        page.locator('#mode-targets').click();page.wait_for_function('document.querySelector("#tg-count").textContent!=="0 shown"')
        check(page.locator('main:visible').count()==1 and page.locator('#targets-workspace').is_visible(),'targets mode shows one workspace')
        no_overflow(page,'desktop targets');capture(page,'targets_desktop.png')
        page.locator('#mode-chip').click();page.locator('#open-kit').click()
        check(page.locator('#v7-kit').evaluate('(d)=>d.open'),'design-kit modal opens')
        check(page.locator('.cursor-specimen img').count()==8,'all eight cursor designs preview')
        check('pointer.png' in page.locator('#open-kit').evaluate('(e)=>getComputedStyle(e).cursor'),'app applies the generated pointer cursor')
        normal=page.locator('.kit-buttons .btn').first
        check('pointer.png' in normal.evaluate('(e)=>getComputedStyle(e).cursor'),'generated buttons use the custom cursor')
        hover=normal.evaluate('(e)=>getComputedStyle(e).borderImageSource')
        normal.hover();page.wait_for_timeout(60)
        hover_source=normal.evaluate('(e)=>getComputedStyle(e).borderImageSource')
        check('hover.png' in hover_source,'generated button hover state renders',hover_source)
        page.mouse.down();page.wait_for_timeout(40)
        pressed_source=normal.evaluate('(e)=>getComputedStyle(e).borderImageSource')
        check('pressed.png' in pressed_source,'generated button pressed state renders',pressed_source)
        page.mouse.up()
        check('disabled.png' in page.locator('.kit-buttons .btn:disabled').first.evaluate('(e)=>getComputedStyle(e).borderImageSource'),'generated button disabled state renders')
        capture(page,'kit_desktop.png')
        fontpath=download(page,'a[href$="coleforge-circuit.ttf"]','coleforge-circuit.ttf')
        check(fontpath.read_bytes()[:4]==b'\x00\x01\x00\x00','downloaded custom font is a real TrueType file')
        kitpath=download(page,'a[href$="coleforge-v7-design-kit.zip"]','coleforge-v7-design-kit.zip')
        import zipfile
        with zipfile.ZipFile(kitpath) as archive:
            check(len([n for n in archive.namelist() if n.startswith('buttons/')])==16 and len([n for n in archive.namelist() if n.endswith('.cur')])==8,'downloaded kit contains full button and cursor banks')
        page.keyboard.press('Escape');check(not page.locator('#v7-kit').evaluate('(d)=>d.open'),'Escape closes design kit')
        for width,height,label in [(1366,768,'compact'),(1024,768,'tablet'),(390,844,'mobile')]:
            page.set_viewport_size({'width':width,'height':height});page.evaluate('scrollTo(0,0)')
            no_overflow(page,label+' Genesis');capture(page,'chip_'+label+'.png',label=='mobile')
            if label=='mobile':
                bounds=page.evaluate('''()=>{const a=document.querySelector('.brand-block').getBoundingClientRect(),b=document.querySelector('.mode-switch').getBoundingClientRect();return {brandBottom:a.bottom,navTop:b.top};}''')
                check(bounds['navTop']>=bounds['brandBottom'],'mobile navigation clears the full brand',bounds)
            page.locator('#open-kit').click();no_overflow(page,label+' design kit');capture(page,'kit_'+label+'.png')
            page.keyboard.press('Escape')
            for mode in ['synth','sample','targets']:
                page.locator('#mode-'+mode).click();page.evaluate('scrollTo(0,0)');no_overflow(page,label+' '+mode)
                if label=='mobile':capture(page,mode+'_mobile.png',True)
            page.locator('#mode-chip').click()
        manifest=json.loads((ROOT/'_SFXGenerator_upload/assets/v7/manifest.json').read_text())
        for asset in manifest['buttons']+manifest['cursors']:
            image=Image.open(ROOT/'_SFXGenerator_upload/assets/v7'/asset['file'])
            check(image.width%2==image.height%2==0,'even exported canvas '+asset['file'])
            check(image.mode=='RGBA' and image.getchannel('A').getextrema()[0]==0,'actual transparent padding '+asset['file'])
            if 'hotspot' in asset:
                cur=(ROOT/'_SFXGenerator_upload/assets/v7'/asset['windowsFile']).read_bytes()
                check(struct.unpack('<HHH',cur[:6])==(0,2,1),'valid Windows CUR '+asset['name'])
        native_assets=page.evaluate('''async assets => {const results=[];for(const asset of assets){const r=await fetch('assets/v7/'+asset.file);results.push({file:asset.file,status:r.status});}return results;}''',manifest['buttons']+manifest['cursors'])
        check(all(r['status']==200 for r in native_assets),'all exported button/cursor URLs serve in Chromium')
        check(not page_errors,'zero native page errors',page_errors)
        check(not console_errors,'zero native console errors',console_errors)
        check(not failed_requests,'zero failed asset requests',failed_requests)
        page.set_viewport_size({'width':1600,'height':1000})
        page.goto(f'http://127.0.0.1:{port}/_SFXGenerator_upload/index.html?studio=1',wait_until='networkidle')
        check(page.locator('#boot-screen').get_attribute('aria-hidden')=='true' and page.locator('#chip-workspace').is_visible(),'direct studio link opens the finished workspace')
        browser.close()
    finally:close()

try:run()
except Exception as error:
    check(False,'probe completed',str(error))
    raise
finally:
    result={'date':'2026-10-11','browser':'Chromium','workflow':'shoot.serve / actual ColeForge application','passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'pageErrors':page_errors,'consoleErrors':console_errors,'failedRequests':failed_requests,'checks':checks,'captures':'_shots/coleforge_v7_1011/'}
    REPORT.parent.mkdir(exist_ok=True);REPORT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f"\nCOLEFORGE V7 UI: {result['passed']} passed / {result['failed']} failed",flush=True)
sys.exit(1 if any(not c['passed'] for c in checks) else 0)
