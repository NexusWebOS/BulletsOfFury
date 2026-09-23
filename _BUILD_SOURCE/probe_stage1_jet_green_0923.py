"""Check the Stage 1 jet paint swap on actual Chromium game canvases."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64, json, sys, http.server

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
from shoot import GAME, SETUP, TRAP_RAF, serve

OUT=ROOT/'_shots/stage1_jet_palette_0923';OUT.mkdir(exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=serve(GAME);errors=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  page=browser.new_page(viewport={'width':1500,'height':1000})
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
  page.wait_for_function('()=>window.__bofFrames>4');page.evaluate(TRAP_RAF)
  page.evaluate(SETUP,{'state':'PLAY','stage':1,'pilot':'axel','invuln':True})
  page.evaluate("""()=>{
    diffKey='furious';DIFF=DIFFS.furious;story=null;stagePlan=[];waveIdx=0;
    enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;subBoss=null;bossActive=false;subBossActive=false;
    player.x=450;player.y=750;player.invuln=9999;
    const types=['s1jetdelta','s1jetbomber','s1jetdelta_b','s1jetbomber_b'];
    window.paletteJets=types.map((type,i)=>spawnEnemy(type,315+i*75,i&1?350:215,{route:'straight'}));
    for(const e of paletteJets){e._s1DelayFrames=0;e._stagger=0;furyFleetPreload(e);}
  }""")
  page.wait_for_function("()=>[0,1,2,3].every(v=>XART.rdy('furyjet_'+v+'_bank_0'))")
  for _ in range(12):page.evaluate('()=>drawWorld(0)');page.wait_for_timeout(40)
  png=base64.b64decode(page.evaluate("document.getElementById('screen').toDataURL('image/png').split(',')[1]"))
  (OUT/'four_jets.png').write_bytes(png)
  result=page.evaluate("""()=>{
    const r=[];
    for(let v=0;v<4;v++){
      const key='furyjet_'+v+'_bank_0',original=XART.get(key),swapped=furyJetGreenFrame(key,v,original);
      const src=document.createElement('canvas'),sc=src.getContext('2d',{willReadFrequently:true});
      src.width=original.width;src.height=original.height;sc.drawImage(original,0,0);
      const a=sc.getImageData(0,0,src.width,src.height).data;
      const b=swapped.getContext('2d').getImageData(0,0,src.width,src.height).data;
      let changed=0,alphaChanged=0,greenDominant=0,originalRed=0,remainingRed=0;
      for(let i=0;i<a.length;i+=4){
        if(a[i+3]!==b[i+3])alphaChanged++;
        if(a[i]>a[i+1]*1.4&&a[i]>a[i+2]*1.3&&a[i]>80)originalRed++;
        if(b[i+3]&&b[i]>b[i+1]*1.4&&b[i]>b[i+2]*1.3&&b[i]>80)remainingRed++;
        if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]){
          changed++;if(b[i+1]>b[i]*2&&b[i+1]>b[i+2]*2)greenDominant++;
        }
      }
      r.push({v,changed,alphaChanged,greenDominant,originalRed,remainingRed});
    }
    return {frames:r,cacheCount:Object.keys(_furyJetGreenFrames).length,
      jetArts:paletteJets.map(e=>({type:e.type,variant:furyJetVariant(e)}))};
  }""")
  assert all(f['changed']>50 and f['greenDominant']==f['changed'] and not f['alphaChanged'] for f in result['frames']),result
  assert result['cacheCount']>=4,result
  assert not errors,errors
  result['errors']=errors
  (OUT/'results.json').write_text(json.dumps(result,indent=2))
  print('PASS: four Stage 1 jet variants recolor red accents green, keep alpha and render in Chromium; no page or console errors.')
  browser.close()
finally:stop()
