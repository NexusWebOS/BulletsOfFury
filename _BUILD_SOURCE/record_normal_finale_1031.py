from pathlib import Path
import sys,http.server,inspect
R=Path(__file__).resolve().parents[1];W=R/'_shots/boss_balance_normal_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import rough_riders_capture_base_1028 as rec
http.server.ThreadingHTTPServer.request_queue_size=256;rec.OUT=W/'video';rec.CONFIG=dict(id='normal-ending-preview-1031',stage=5,role='boss',kind='chromehammer',name='Normal completion / Earth return / Hard-Furious choice / pilot selection',limit=27)
start=rec.CAPTURE.index("  g.fillStyle='rgba(5,12,24,.94)'");end=rec.CAPTURE.index('  analyser.getFloatTimeDomainData',start);rec.CAPTURE=rec.CAPTURE[:start]+rec.CAPTURE[end:]
rec.CAPTURE=rec.CAPTURE.replace('try{aim(elapsed);}',"try{if(elapsed>11&&!window.choseRow){Input.injectTap('s');window.choseRow=true;}if(elapsed>15&&!window.confirmedRow){Input.injectTap('enter');window.confirmedRow=true;}}")
tail=rec.CAPTURE.index(" diffKey='furious';debugUnlocked=true;")
rec.CAPTURE=rec.CAPTURE[:tail]+""" run.pilot='cole';run.stage=5;run.mode='campaign';run.ngplus=false;coopOn=false;diffKey='normal';debugFight=null;nf100Open(true,true);
 return {preview:true,screen:{width:cv.width,height:cv.height},difficulty:diffKey};
}"""
rec.SNAPSHOT="""()=>({seconds:+((performance.now()-captureStart)/1000).toFixed(3),state,stage:run.stage,difficulty:diffKey,hp:null,maxhp:null,mode:NF100.current?.phase,phase:NF100.current?.phase,form:null,bossDefeated:state===GS.PILOT,botErrors:reviewBot.errors,deaths:0,audioPeak:captureStats.peak,nativeFrames:window.__bofFrames,frames:captureStats.frames})"""
src=inspect.getsource(rec.record).replace("page.mouse.click(3, 3)","page.mouse.click(3,3)\n            page.wait_for_function('()=>nf100Warm()',timeout=180000)")
src=src.replace("'difficulty': 'furious'","'difficulty':'normal'").replace("'invulnerable': True","'invulnerable':False").replace("reason='native defeat'","reason='native Normal ending preview; staged entry; actual input selection; no user save writes'")
src=src.replace("mp4 = folder / f'stage{stage}-furious.mp4'","mp4 = folder / 'normal-ending-preview.mp4'")
src=src.replace("'method': 'Native encounter spawn, real RAF, Cole with level-5 Laser and40 missiles, native GOD and input-only aiming; no enemy HP/phase/timer writes.'","'method':'Staged entry to new Normal finale; actual game renderer/audio and real-time flight; input-only choice/fade. Preview does not write completion saves.'")
exec(src,rec.__dict__);print('FINAL',rec.record(5,27),flush=True)
