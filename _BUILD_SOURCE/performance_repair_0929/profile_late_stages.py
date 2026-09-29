"""Profile the actual engine in Chromium. No render substitutes or fake canvas."""
import sys,json,time,base64
from pathlib import Path
GAME=next(p for p in Path(__file__).resolve().parents if (p/'assets/game.js').is_file())
sys.path.insert(0,str(GAME/'_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

INSTRUMENT=r'''() => {
 window.__profiles={};window.__samples=[];window.__deltas=[];window.__prev=0;window.__owner='';window.__images={};
 const map=new WeakMap(),get=XART.get.bind(XART);XART.get=function(k){const im=get(k);if(im&&typeof im==='object')map.set(im,k);return im;};
 const di=ctx.drawImage;ctx.drawImage=function(im){const t=performance.now();try{return di.apply(this,arguments);}finally{const ms=performance.now()-t,k=(map.get(im)||im?.src?.split('/').pop()||'canvas')+'|'+window.__owner+'|blur:'+ctx.shadowBlur+'|filter:'+ctx.filter;const p=window.__images[k]||(window.__images[k]={ms:0,calls:0,max:0,width:im?.width,height:im?.height});p.ms+=ms;p.calls++;p.max=Math.max(p.max,ms);}};
 window.__wrap=function(name,fn){return function(){const t=performance.now(),owner=window.__owner;window.__owner=name;try{return fn.apply(this,arguments);}finally{window.__owner=owner;const d=performance.now()-t,p=window.__profiles[name]||(window.__profiles[name]={ms:0,calls:0,max:0});p.ms+=d;p.calls++;p.max=Math.max(p.max,d);}};};
 for(const name of ['drawEnemy','drawEnemyShieldBack','drawEnemyShieldFront','drawEnemyDamage','drawLaserTell','drawNavalFlashes','wm26DrawEnemy','sceneDrawWorld','wfxDraw','drawEffects','drawScanlines','drawHUDOverlay','drawSpecialHUD','drawPowerups','polishCombatDraw','s6WingDraw','drawRollCharge','drawEquipCorner','drawIncomingLockHud','drawWorld','drawBG','updatePlay','drawBullets','efxDraw','drawAnimTerrain','bg6Draw','bg6CloudsDraw','bg6RainDraw','xartTint','fr28SewerMaster','fr27LoopTerrain','drawS7Toxic','furyFleetDraw','drawS8Mega','s7mDraw','s7mWarnings','combatWarningDraw','l23FovDraw','drawIncomingWarnings','drawPlayer','drawZaps','drawCampaignRadar','drawWeather']){
  try{if(eval('typeof '+name)==='function')eval(name+'=window.__wrap("'+name+'",'+name+')');}catch(e){}
 }
 const own=loop;loop=function(t){const p=performance.now();if(window.__prev)window.__deltas.push(t-window.__prev);window.__prev=t;
  try{return own(t);}finally{window.__samples.push(performance.now()-p);}};
 window.playerHit=function(){};
}'''
SETUP=r'''cfg => {
 ht27Stop();debugFight=null;coopOn=false;run.mode='arcade';diffKey='furious';DIFF=DIFFS.furious;
 pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.pilot='cole';run.weapon=0;run.wlevels=WEAPONS.map(()=>1);run.wlevels[0]=6;run.wlevel=6;
 beginStage(cfg.stage);setState(GS.PLAY);story=null;player.dead=false;player.invuln=0;
 s6Opening=null;run._mission29OpeningDone=true;stageTimer=cfg.stage===6?28:cfg.stage===8?15:20;
 if(cfg.stage===6){s6WingInit();s6WingTick(.01);}
 if(cfg.stage===7){mapScroll=1400;drawBG(0);const e=stage7SluiceEvents()[0];e.row=_masterSrcY+VH*.65;e.side=-1;e.tier=0;e.live=true;e.done=false;e.t=stage7SluiceWarn()+.1;}
 const keys=keybindFor(1).fire||[];window.__perfDown=Input.down;Input.down=function(k){return keys.includes(k)||window.__perfDown.call(this,k);};
 window.__profiles={};window.__samples=[];window.__deltas=[];window.__prev=0;
}'''

def main():
 label=sys.argv[1] if len(sys.argv)>1 else 'before'
 out=GAME/'_shots/performance_0929';out.mkdir(parents=True,exist_ok=True)
 port,stop=sh.serve(str(GAME));result={'label':label,'scenes':[],'errors':[]}
 with sync_playwright() as p:
  br=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
  pg=br.new_page(viewport={'width':1440,'height':1000})
  pg.on('pageerror',lambda e:result['errors'].append(str(e)))
  pg.on('console',lambda m:result['errors'].append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000)
  pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
  pg.evaluate(sh.TRAP_RAF);pg.evaluate(INSTRUMENT)
  for stage in [1,6,7,8]:
   pg.evaluate(SETUP,{'stage':stage})
   # Step the real loop briefly while lazy families decode, then measure browser rAF.
   pg.evaluate(sh.STEP,120);pg.wait_for_timeout(1200)
   pg.evaluate('''()=>{window.__profiles={};window.__samples=[];window.__deltas=[];window.__images={};window.__prev=0;requestAnimationFrame=window.__bofRealRAF;requestAnimationFrame(loop);}''')
   pg.wait_for_timeout(6000)
   pg.evaluate(sh.TRAP_RAF)
   data=pg.evaluate('''()=>{const s=window.__samples.slice(5).sort((a,b)=>a-b),d=window.__deltas.slice(5).sort((a,b)=>a-b),q=(a,p)=>a[Math.min(a.length-1,Math.floor(a.length*p))]||0;
    return {stage:run.stage,state,frames:s.length,frameMean:s.reduce((a,b)=>a+b,0)/Math.max(1,s.length),frameP95:q(s,.95),frameMax:q(s,1),intervalP50:q(d,.5),intervalP95:q(d,.95),fps:1000/(d.reduce((a,b)=>a+b,0)/Math.max(1,d.length)),functions:window.__profiles,images:window.__images,
     enemies:enemies.length,pBullets:pBullets.length,eBullets:eBullets.length,particles:particles.length,fx:efxBursts.length,explosions:explosions.length,phase:s6Opening?.phase,cachedTints:Object.keys(_mfxtc).length};}''')
   result['scenes'].append(data);print(json.dumps(data),flush=True)
   img=pg.evaluate('()=>document.getElementById("screen").toDataURL("image/png")')
   (out/f'{label}_stage{stage}.png').write_bytes(base64.b64decode(img.split(',',1)[1]))
   # Remove the previous shoot override before the next scenario.
   pg.evaluate('()=>{Input.down=window.__perfDown;}')
  (out/f'{label}.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
  br.close()
 stop();return bool(result['errors'])

if __name__=='__main__':sys.exit(main())
