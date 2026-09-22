"""Browser audit of a boss kill through guaranteed element, debrief, and Forge controls."""
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve, SETUP, STEP, TRAP_RAF

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/forge_reward_flow_0920'; OUT.mkdir(parents=True,exist_ok=True)
port,stop=serve(str(ROOT)); errors=[]
try:
  with sync_playwright() as pw:
    browser=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
    page=browser.new_page(viewport={'width':1100,'height':1200})
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
    page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=60000)
    page.wait_for_function("() => typeof forgeStart==='function' && (window.__bofFrames|0)>4",timeout=45000)
    page.evaluate(TRAP_RAF);page.wait_for_timeout(50)
    assert page.evaluate(SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':True})['ok']
    page.evaluate("""() => {
      run.mode='arcade'; run.forge={};run.forgeForms={};run.forgeElems={};
      run.infusion=null;run.lives=9;achievementState.owned={};
      enemies.length=0;eBullets.length=0;powerups.length=0;
      stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;spawnClock=9999;
      spawnBoss(curStage.boss);boss.enter=false;
      if(boss._ovIntro)boss._ovIntro.done=true;
      boss.hp=1;hitBoss(2);
    }""")
    reward=page.evaluate("""() => ({dead:boss&&boss.dead,pickups:powerups.filter(p=>p.kind==='forgecombo').map(p=>p.elem),elements:Object.keys(run.forgeElems)})""")
    assert reward['dead'] and reward['pickups']==['kinetic'] and not reward['elements'],reward
    for _ in range(20):
      err=page.evaluate(STEP,30);assert err is None,err
      page.wait_for_timeout(20)
      if page.evaluate("() => state==='stageclear'"):break
    clear=page.evaluate("""() => ({state,elements:Object.keys(run.forgeElems),rewards:run._stageElements,pickups:powerups.filter(p=>p.kind==='forgecombo'&&!p.dead).length})""")
    assert clear['state']=='stageclear' and clear['elements']==['kinetic'] and clear['rewards']==['kinetic'] and clear['pickups']==0,clear
    def tap(key):
      page.evaluate('(k)=>BOSSMODE.hold(k,true)',key)
      assert page.evaluate(STEP,1) is None
      page.evaluate('(k)=>BOSSMODE.hold(k,false)',key)
      assert page.evaluate(STEP,8) is None
    for _ in range(16):
      if page.evaluate("() => state==='forge'"):break
      tap('enter')
      assert page.evaluate(STEP,35) is None
      page.wait_for_timeout(20)
    forge=page.evaluate("""() => ({state,combos:run.forgeCombos,respecs:run.forgeRespecs,all:FORGE_WEAPONS.every(w=>forgeElemsFor(w).join(',')==='kinetic'),sel:forge&&forge.sel,row:forge&&forge.row})""")
    assert forge['state']=='forge' and forge['combos']==2 and forge['respecs']==2 and forge['all'],forge
    page.evaluate("""() => {window.__forgeAudio={blip:0,powerup:0,blocked:0};for(const k of Object.keys(window.__forgeAudio)){const f=Audio.SFX[k];if(f)Audio.SFX[k]=function(){window.__forgeAudio[k]++;return f.apply(this,arguments);};}}""")
    for _ in range(5):
      assert page.evaluate(STEP,30) is None
      page.wait_for_timeout(20)
    png=page.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
    (OUT/'forge_after_real_boss_reward.png').write_bytes(base64.b64decode(png.split(',',1)[1]))
    tap('j');pick=page.evaluate("""() => ({state,row:forge&&forge.row,elem:forgeDiscovered()[forge.esel]})""")
    assert pick['row']==1 and pick['elem']=='kinetic',pick
    tap('j');made=page.evaluate("""() => ({state,combos:run.forgeCombos,form:run.forge&&run.forge[0],saved:run.forgeForms&&run.forgeForms[0]&&run.forgeForms[0].kinetic,held:run.infusion&&run.infusion.elem})""")
    assert made['state']=='forging' and made['combos']==1 and made['form']['elem']=='kinetic' and made['saved']['elem']=='kinetic' and made['held']=='kinetic',made
    for _ in range(8):
      assert page.evaluate(STEP,50) is None
      page.wait_for_timeout(20)
    assert page.evaluate("() => state==='forged'")
    tap('escape')
    assert page.evaluate("() => state==='forge'")
    tap('d'); assert page.evaluate("() => forge.sel") == 1
    tap('j'); assert page.evaluate("() => forge.row") == 1
    tap('j'); second=page.evaluate("""() => ({state,combos:run.forgeCombos,form:run.forge&&run.forge[1]})""")
    assert second['state']=='forging' and second['combos']==0 and second['form']['elem']=='kinetic',second
    for _ in range(8):
      assert page.evaluate(STEP,50) is None
      page.wait_for_timeout(20)
    assert page.evaluate("() => state==='forged'")
    tap('escape'); assert page.evaluate("() => state==='forge'")
    tap('j')
    refused=page.evaluate("""() => ({row:forge.row,combos:run.forgeCombos,msg:forge.msg})""")
    assert refused['row']==0 and refused['combos']==0 and 'NO COMBINES' in refused['msg'],refused
    tap('h')
    respec=page.evaluate("""() => ({active:!!(run.forge&&run.forge[1]),stored:!!(run.forgeForms&&run.forgeForms[1]&&run.forgeForms[1].kinetic),left:run.forgeRespecs})""")
    assert not respec['active'] and respec['stored'] and respec['left']==1,respec
    tap('enter')
    assert page.evaluate("() => state==='loadout'")
    assert page.evaluate(STEP,45) is None
    tap('d'); assert page.evaluate("() => loadoutScr.sel") == 1
    tap('w'); choices=page.evaluate("""() => ({row:loadoutScr.row,names:weaponFormOptions(1).map(o=>o.name)})""")
    assert choices['row']==2 and 'SHOCK FAN' in choices['names'],choices
    tap('d');tap('j')
    selected=page.evaluate("""() => ({row:loadoutScr.row,active:run.forge[1]&&run.forge[1].elem,forms:run.forgeForms[1],audio:window.__forgeAudio})""")
    assert selected['row']==0 and selected['active']=='kinetic' and selected['audio']['blip']>0 and selected['audio']['powerup']>0 and selected['audio']['blocked']>0,selected
    tap('enter')
    for _ in range(50):
      err=page.evaluate(STEP,30);assert err is None,err
      page.wait_for_timeout(20)
      if page.evaluate("() => run.stage===2 && state==='play'"):break
    launched=page.evaluate("""() => ({state,stage:run.stage,elements:Object.keys(run.forgeElems),mg:run.forge[0]&&run.forge[0].elem,spread:run.forge[1]&&run.forge[1].elem})""")
    assert launched['state']=='play' and launched['stage']==2 and launched['mg']=='kinetic' and launched['spread']=='kinetic',launched
    page.evaluate("() => {run.shield=0;player.invuln=0;playerHit();}")
    death=page.evaluate("""() => ({dead:player.dead,weapon:run.weapon,infusion:run.infusion&&run.infusion.elem,mg:run.forge[0]&&run.forge[0].elem,spread:run.forge[1]&&run.forge[1].elem,forms:!!(run.forgeForms[1]&&run.forgeForms[1].kinetic)})""")
    assert death['dead'] and death['weapon']==0 and death['infusion']=='kinetic' and death['mg']=='kinetic' and death['spread']=='kinetic' and death['forms'],death
    browser.close()
finally:stop()

print({'reward':reward,'clear':clear,'forge':forge,'picked':pick,'combined':made,'second':second,'refused':refused,'respec':respec,'choices':choices,'selected':selected,'launched':launched,'death':death,'errors':errors[:5]})
assert not errors,errors
print('PASS boss reward, two UI combines, cap, re-spec, loadout, audio and Stage-2 death persistence')
