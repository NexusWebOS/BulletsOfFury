"""Chromium proof for the new cue bank, weapon decals, music, and boss-clear controls."""
from pathlib import Path
import importlib.util
import json

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/qa_0920_audio'
OUT.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('shoot',ROOT/'_BUILD_SOURCE/shoot.py')
sh=importlib.util.module_from_spec(spec);spec.loader.exec_module(sh)

def main():
    port,stop=sh.serve(str(ROOT))
    report={}
    errs=[]
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--autoplay-policy=no-user-gesture-required'])
            page=browser.new_page(viewport={'width':960,'height':1024})
            page.on('pageerror',lambda e:errs.append('page: '+str(e)[:200]))
            page.on('console',lambda e:errs.append('console: '+e.text[:200]) if e.type=='error' else None)
            page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000)
            page.wait_for_function("() => typeof state!=='undefined' && (window.__bofFrames|0)>4",timeout=120000)
            page.evaluate(sh.TRAP_RAF)
            setup=page.evaluate(sh.SETUP,{'state':'PLAY','pilot':'cole','stage':1,'invuln':True})
            assert setup['ok'],setup
            report['audio']=page.evaluate("""() => {
              const names=['cfComboFire','cfComboIce','cfComboLightning','cfComboPrism',
                'cfComboToxic','cfComboKinetic','cfComboChrome','cfComboWater','cfComboDark',
                'cfComboThermoshock','cfFireWave','cfFireBurst','cfFireGeyser',
                'cfShieldDestroy','cfBossRazorback','cfBossOverlord','cfBossWarden',
                'cfEnemyFlame','cfEnemyIce','cfEnemyElectric'];
              return {missing:names.filter(n=>!Snd.pools[n]||!Snd.TAME[n]||!Audio.SFX[n]),
                musicVol:Snd.vol.music,stageMusic:Snd.music.lvl1.src};
            }""")
            assert not report['audio']['missing'],report['audio']
            report['decals']=page.evaluate("""() => ({
              mg:weaponDecalKey('mg','',false),spread:weaponDecalKey('spread','',false),
              missile:weaponDecalKey('missile','',false),laser:weaponDecalKey('beam','',false),
              flame:weaponDecalKey('flame','',false),orb:weaponDecalKey('orb','magmaorb',false),
              mist:weaponDecalKey('lasermist','',false),chain:weaponDecalKey('chaingun','',false),
              lightning:weaponDecalKey('yuriLightningOrb','',false)} )""")
            assert len(set(report['decals'].values()))>=6,report['decals']
            report['onHit']=page.evaluate("""() => {
              const e={x:player.x,y:PLAY.y+95,w:38,h:38,hp:80,maxhp:80,t:0,dead:false};
              enemies.push(e);
              const oldP=pImpacts.length,oldE=efxBursts.length;
              _dmgBullet={kind:'orb',_wvar:'iceorb',_el:'ice',_inf:'ice',dmg:2};
              try{hitEnemy(e,2);}finally{_dmgBullet=null;enemies= enemies.filter(x=>x!==e);}
              return {impact:pImpacts.length-oldP,burst:efxBursts.length-oldE,
                type:pImpacts[pImpacts.length-1]&&pImpacts[pImpacts.length-1].key,
                element:efxBursts[efxBursts.length-1]&&efxBursts[efxBursts.length-1].elem};
            }""")
            assert report['onHit']['impact']>=1 and report['onHit']['element']=='ice',report['onHit']
            page.evaluate("""(keys) => {for(const k of keys) XART.rdy(k);}
            """,list(set(report['decals'].values())))
            page.wait_for_timeout(700)
            page.evaluate("""() => {
              player.x=worldWidth()/2;player.y=PLAY.y+PLAY.h*.72;
              bossDefeated=true;stageEnding=0;bossActive=false;
              for(const [i,k] of Object.entries(['mg','spread','missile','beam','flame','orb','lasermist','chaingun','yuriLightningOrb'])){
                const x=camLeftX()+45+Number(i)%3*60,y=PLAY.y+55+Math.floor(Number(i)/3)*60;
                pImpacts.push({x,y,t:0,dur:.6,size:32,key:weaponDecalKey(k,k==='orb'?'magmaorb':'',false),rot:0});
              }
            }""")
            page.keyboard.down('ArrowLeft')
            before=page.evaluate('player.x')
            step=page.evaluate(sh.STEP,8)
            page.keyboard.up('ArrowLeft')
            after=page.evaluate('player.x')
            report['postBossMove']={'before':before,'after':after,'step':step}
            assert after<before-1,report['postBossMove']
            page.evaluate("""() => {player.invuln=0;player.dead=false;eBullets.length=0;drawWorld(0);}""")
            page.screenshot(path=str(OUT/'decals_after_boss.png'))
            page.evaluate("""() => {
              flyoverT=0;flyoverStartX=player.x;flyoverStartY=player.y;
              setState(GS.FLYOVER);drawFlyover._clearStarted=false;
            }""")
            page.keyboard.down('ArrowRight')
            hb=page.evaluate('player.x')
            page.evaluate(sh.STEP,8)
            hm=page.evaluate('player.x')
            page.keyboard.up('ArrowRight')
            page.evaluate(sh.STEP,95)
            page.keyboard.down('ArrowRight')
            cb=page.evaluate('player.x')
            page.evaluate(sh.STEP,8)
            ca=page.evaluate('player.x')
            page.keyboard.up('ArrowRight')
            report['flyoff']={'hoverBefore':hb,'hoverAfter':hm,'climbBefore':cb,'climbAfter':ca,'state':page.evaluate('state')}
            assert hm>hb+1 and abs(ca-cb)<.1,report['flyoff']
            page.evaluate("""() => {player.invuln=0;player.dead=false;drawFlyover(0);}""")
            page.screenshot(path=str(OUT/'flyoff_climb.png'))
            # Music volume must stay at the user's selected full level through a boss transition.
            report['bossMusic']=page.evaluate("""() => {
              setState(GS.PLAY);Audio.startMusic('boss2');
              return {src:Snd.cur&&Snd.cur.src,volume:Snd.cur&&Snd.cur.volume,
                user:Snd.vol.music,master:Snd.vol.master};
            }""")
            assert 'boss2_bossfight3_loud_0920' in report['bossMusic']['src']
            assert report['bossMusic']['volume']>=.99
            report['playback']=page.evaluate("""async () => {
              const names=['cfComboFire','cfFireWave','cfFireGeyser','cfShieldDestroy',
                'cfBossRazorback','cfEnemyElectric'];
              const out={};
              for(const n of names){
                const p=Snd.pools[n],i=p.i,a=p.list[i];
                const accepted=Snd.play(n);
                await new Promise(r=>setTimeout(r,240));
                out[n]={accepted,ready:a.readyState,time:a.currentTime,paused:a.paused};
              }
              return out;
            }""")
            assert all(v['accepted'] and v['ready']>=2 and v['time']>.01 for v in report['playback'].values()),report['playback']
            browser.close()
    finally:
        stop()
    report['errors']=errs
    (OUT/'browser_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
    assert not errs,errs

if __name__=='__main__':main()
