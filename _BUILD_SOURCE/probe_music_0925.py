#!/usr/bin/env python3
"""Check that live music keys decode and their HTMLAudio clocks advance."""
import json,os,sys
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.insert(0,os.path.join(ROOT,'_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

def main():
    port,stop=sh.serve(sh.GAME)
    rows=[]
    try:
        with sync_playwright() as pw:
            br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
            pg=br.new_page(viewport={'width':1100,'height':1200})
            errs=[]
            pg.on('pageerror',lambda e:errs.append(str(e)))
            pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=60000)
            pg.wait_for_function("() => typeof Snd!=='undefined' && Snd.music && Snd.music.title",timeout=60000)
            pg.wait_for_function("() => (window.__bofFrames|0)>4",timeout=60000)
            pg.wait_for_timeout(2500)
            pg.mouse.click(480,400)
            for key in ('title','stage7mus','boss8','boss8p3','finalCinematic'):
                pg.evaluate('(key) => Snd.startMusic(key)',key)
                pg.wait_for_timeout(1600)
                v=pg.evaluate("(key) => ({mapped:BOFA.music[key],entry:Snd.music[key]&&Snd.music[key].src,"
                              "src:Snd.cur&&Snd.cur.currentSrc,paused:Snd.cur&&Snd.cur.paused,"
                              "ready:Snd.cur&&Snd.cur.readyState,time:Snd.cur&&Snd.cur.currentTime,"
                              "code:Snd.cur&&Snd.cur.error&&Snd.cur.error.code,playing:Snd.musicPlaying()})",key)
                rows.append({'key':key,**v})
            pg.evaluate(sh.SETUP,{'state':'PLAY','stage':8,'pilot':'cole','invuln':True})
            pg.evaluate("() => Snd.startMusic('boss8p3')")
            pg.wait_for_timeout(1600)
            v=pg.evaluate("() => ({src:Snd.cur&&Snd.cur.currentSrc,paused:Snd.cur&&Snd.cur.paused,"
                          "time:Snd.cur&&Snd.cur.currentTime,playing:Snd.musicPlaying()})")
            rows.append({'key':'boss8p3-in-play',**v})
            print(json.dumps({'tracks':rows,'errors':errs[:8]},indent=2))
            br.close()
    finally:stop()

if __name__=='__main__':main()
