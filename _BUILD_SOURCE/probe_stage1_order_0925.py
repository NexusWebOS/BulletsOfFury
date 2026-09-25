#!/usr/bin/env python3
"""Observe the full Stage-1 wave order in real Chromium, including sand tanks."""
import json,os,sys
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.insert(0,os.path.join(ROOT,'_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

def main():
    port,stop=sh.serve(sh.GAME)
    try:
        with sync_playwright() as pw:
            br=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
            pg=br.new_page(viewport={'width':1100,'height':1200})
            errors=[]
            pg.on('pageerror',lambda e:errors.append(str(e)))
            pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=60000)
            pg.wait_for_function("() => typeof ASSETS!=='undefined' && (window.__bofFrames|0)>4",timeout=60000)
            pg.evaluate(sh.TRAP_RAF)
            pg.evaluate(sh.SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':True})
            pg.evaluate("""() => {
                diffKey='normal';DIFF=difficultyForRun(run.mode,'normal');
                player.invuln=1e9;run.lives=9;window.__waveSpawns=[];
                const old=spawnEnemy;
                spawnEnemy=function(...args){const e=old(...args);
                    if(e)window.__waveSpawns.push({type:e.type,t:stageTimer,scroll:mapScroll});
                    return e;};
              }""")
            for i in range(105):
                err=pg.evaluate(sh.STEP,60)
                if err:raise RuntimeError(f'loop {i}: {err}')
                if i%3==0:pg.wait_for_timeout(25)
                pg.evaluate("() => {if(subBoss&&subBossActive){subBoss.dead=true;subBossActive=false;subBossDone=true;}}")
                if i%15==0:
                    z=pg.evaluate("() => ({t:stageTimer,scroll:mapScroll,waveIdx,state})")
                    print(i,z,flush=True)
            out=pg.evaluate("() => ({spawns:window.__waveSpawns,stageTimer,mapScroll,waveIdx,state})")
            os.makedirs(os.path.join(ROOT,'_shots'),exist_ok=True)
            with open(os.path.join(ROOT,'_shots','stage1_order_0925.json'),'w') as f:
                json.dump({'result':out,'errors':errors},f,indent=2)
            for typ in ('s1tankheavy','s1tankapc','modturret'):
                x=[e for e in out['spawns'] if e['type']==typ]
                print(typ,len(x),x[:4],flush=True)
            print('errors',errors[:5],flush=True)
            br.close()
    finally:stop()

if __name__=='__main__':main()
