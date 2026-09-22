"""Verify a forged element follows its exact equipped weapon and level in Chromium."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve, SETUP, TRAP_RAF

ROOT=Path(__file__).resolve().parents[1]
port,stop=serve(str(ROOT))
errors=[]
try:
  with sync_playwright() as pw:
    browser=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
    page=browser.new_page(viewport={'width':1100,'height':1200})
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
    page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=60000)
    page.wait_for_function("() => typeof forgeApply==='function' && (window.__bofFrames|0)>4",timeout=45000)
    page.evaluate(TRAP_RAF)
    assert page.evaluate(SETUP,{'state':'PLAY','stage':2,'pilot':'cole','invuln':True})['ok']
    result=page.evaluate("""() => {
      run.forge={0:{elem:'kinetic',lv:5},1:{elem:'kinetic',lv:1}};
      run.forgeForms={0:{kinetic:run.forge[0]},1:{kinetic:run.forge[1]}};
      run.wlevels=WEAPONS.map(()=>1);run.weapon=0;run.infusion=null;forgeApply();
      const mg={weapon:run.weapon,elem:run.infusion&&run.infusion.elem,lv:run.infusion&&run.infusion.lv};
      applyPowerup({kind:'weapon',wtype:1,wvar:null});
      const spread={weapon:run.weapon,elem:run.infusion&&run.infusion.elem,lv:run.infusion&&run.infusion.lv};
      applyPowerup({kind:'weapon',wtype:4,wvar:'flamethrower'});
      const bare={weapon:run.weapon,elem:run.infusion&&run.infusion.elem,lv:run.infusion&&run.infusion.lv};
      return {mg,spread,bare};
    }""")
    matrix=page.evaluate("""() => {
      const elems=Object.values(BOSS_ELEMENT_BY_STAGE),bad=[];
      run.forge={};run.forgeForms={};run.forgeElems={};
      for(const e of elems)run.forgeElems[e]=1;
      for(const w of FORGE_WEAPONS)for(const e of elems){
        run.forgeCombos=2;
        const made=forgeCombine(w,e);
        run.weapon=w;run.infusion=null;forgeApply();
        const option=weaponFormOptions(w).find(o=>o.kind==='forge'&&o.elem===e);
        if(made!=='ok'||!option||run.infusion?.elem!==e||run.infusion?.lv!==1)
          bad.push({w,e,made,option:!!option,held:run.infusion});
      }
      delete run.forge[4];run.weapon=4;run.infusion=null;infusionGrant('fire');forgeApply();
      return {pairs:FORGE_WEAPONS.length*elems.length,bad,fieldKeeps:run.infusion?.elem==='fire'&&run.infusion?._forgeW==null};
    }""")
    browser.close()
finally:stop()
print(result,matrix,errors)
assert matrix['pairs']==81 and not matrix['bad'] and matrix['fieldKeeps'],matrix
assert result['mg']=={'weapon':0,'elem':'kinetic','lv':5},result
assert result['spread']=={'weapon':1,'elem':'kinetic','lv':1},result
assert result['bare']['weapon']==4 and result['bare']['elem'] is None,result
assert not errors,errors
print('PASS forged forms follow weapon pickups without leaking element or level')
