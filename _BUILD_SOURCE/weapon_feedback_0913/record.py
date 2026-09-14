"""Forty seconds of native combat, real input, real effects, frame-logged game audio."""
import base64,json,subprocess,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE/trailer_v7'));import capture3,render_audio
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
OUT=ROOT/'_shots/weapon_feedback_0913/video';OUT.mkdir(parents=True,exist_ok=True)
TAKES=[('cole_sonic',1,'boss','cole',10),('juggernaut_dash',4,'mini','juggernaut',10),('juggernaut_flails',4,'mini','juggernaut',8),('laser_mist',1,'mini','falva',12)]
DRIVE="""([kind,i])=>{const K=Input.keys,T=window.__tgt(),ww=worldWidth();for(const k of ['a','d','w','s','j','h'])K[k]=false;
 let tx=ww/2,ty=PLAY.y+PLAY.h*.80;
 if(kind==='cole_sonic'){tx=T&&Number.isFinite(T.x)?T.x+Math.sin(i/60)*22:ww/2;const c=i%160,n=Math.floor(i/160);K.j=c<(n%2?30:72);}
 if(kind==='juggernaut_dash'){const c=i%240;tx=T&&Number.isFinite(T.x)?T.x:ww/2;if(c<78){K.h=true;K.w=true;}else if(c>103)K.s=player.y<ty-5;}
 if(kind==='juggernaut_flails'){tx=(T&&Number.isFinite(T.x)?T.x:ww/2)+Math.sin(i/60*1.7)*55;ty=T?clamp((T._drawY||T.y)+(T._drawH||T.h||100)*.35+50,PLAY.y+110,PLAY.y+PLAY.h*.66):PLAY.y+PLAY.h*.60;}
 if(kind==='laser_mist'){tx=ww/2+Math.sin(i/60*.85)*96;K.j=true;}
 K.a=player.x>tx+5;K.d=player.x<tx-5;
 if(kind!=='juggernaut_dash'){K.w=player.y>ty+5;K.s=player.y<ty-5;}
}"""
def main():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
        def log_message(self,*a):pass
    srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
    ff=imageio_ffmpeg.get_ffmpeg_exe();reports=json.loads((OUT/'report.json').read_text())['takes'] if '--resume'in sys.argv and (OUT/'report.json').exists() else [];errors=[]
    with sync_playwright()as p:
        b=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
        for name,stage,role,pilot,seconds in TAKES:
            if any(r['name']==name for r in reports):continue
            pg=b.new_page(viewport={'width':1100,'height':1200})
            pg.on('pageerror',lambda e:errors.append('page '+str(e)))
            pg.on('console',lambda m:errors.append('console '+m.text)if m.type=='error'else None)
            pg.goto('http://127.0.0.1:%d/index.html'%srv.server_port,wait_until='load',timeout=120000)
            pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);pg.evaluate(shoot.TRAP_RAF);pg.wait_for_timeout(80)
            pg.evaluate(capture3.LIB);pg.evaluate('()=>window.__auto=function(){}')
            result=pg.evaluate('([s,r,p])=>window.__fight(s,r,p)',[stage,role,pilot]);assert result['ok'],result
            for _ in range(200):
                ready=pg.evaluate('()=>{const T=window.__tgt();return T&&!T.dead&&!T.enter&&T.y>0;}')
                if ready:break
                pg.evaluate('()=>window.__step(6)');pg.wait_for_timeout(5)
            assert ready,'fight did not become playable '+name
            pg.evaluate('(p)=>{warmPlayerAtlases();weaponFeedbackWarm(p===\'cole\'?\'cole\':\'juggernaut\');laserMistWarm();Audio.resume();}',pilot)
            for _ in range(120):
                ready=pg.evaluate('(p)=>XART.rdy("ship_"+p)&&["nsw_dist_3","jchg_3","jwb_ball","jwb_link","jwb_burst","ndr_dambreaker_bottomthruster_2","bof_laser_mist_weapon_atlas"].every(k=>XART.rdy(k))',pilot)
                if ready:break
                pg.wait_for_timeout(60)
            assert ready,'art not ready '+name
            pg.evaluate('''([n,p])=>{playerHit=function(){};player.invuln=0;story=null;dlgBox=function(){};floaters.length=0;
             player.x=worldWidth()/2;player.y=PLAY.y+PLAY.h*.8;
             if(n==='cole_sonic')sonicGrant();if(p==='juggernaut')startSpecial();
             if(n==='laser_mist'){run.weapon=6;run.wlevel=5;player.fireCd=0;laserMistWarm();}
             window.__i=1;window.__auto=function(){};const L=window.__alog;L.snd.length=0;L.syn.length=0;L.warp.length=0;L.restarts.length=0;L.loops={};
            }''',[name,pilot])
            rec0=pg.evaluate('()=>window.__i')
            silent=OUT/(name+'_picture.mp4');movie=OUT/(name+'.mp4')
            enc=subprocess.Popen([ff,'-y','-v','error','-f','image2pipe','-vcodec','mjpeg','-framerate','30','-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(silent)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            timeline=[];peakMist=0;dashes=0
            for frame in range(seconds*30):
                pg.evaluate(DRIVE,[name,frame*2]);pg.evaluate('()=>window.__step(2)')
                raw=pg.evaluate("()=>document.querySelector('#screen').toDataURL('image/jpeg',.92).split(',')[1]")
                enc.stdin.write(base64.b64decode(raw))
                metrics=pg.evaluate('()=>({state:state,dead:player.dead,px:player.x,py:player.y,dash:!!player._chgDash,mist:pBullets.filter(b=>b.kind==="lasermist"&&!b.dead).length,target:window.__tgt()?{name:window.__tgt().kind,hp:window.__tgt().hp}:null,error:window.__err||null})')
                peakMist=max(peakMist,metrics['mist']);dashes+=int(metrics['dash'])
                assert not metrics['dead']and not metrics['error'],metrics
                if frame%60==0:timeline.append({'seconds':frame/30,**metrics});print(name+' %ds '%(frame/30)+json.dumps(metrics),flush=True)
                if frame in [20,42,90,150,220,300]:
                    path=OUT/(name+'_%03d.png'%frame);path.write_bytes(base64.b64decode(pg.evaluate("()=>document.querySelector('#screen').toDataURL().split(',')[1]")))
            enc.stdin.close();err=enc.stderr.read();assert enc.wait()==0,err
            ev=pg.evaluate('()=>window.__audioDump()');ev.update(rec0=rec0,frames=seconds*60)
            (OUT/(name+'_events.json')).write_text(json.dumps(ev),encoding='utf-8')
            res=pg.evaluate(render_audio.RENDER,{'ev':ev,'iife':render_audio.audio_module_source(),'tail':0,'exclude':[]})
            assert not res['errs']and res['rms']>0 and res['peak']<1,res.get('errs')
            wav=OUT/(name+'_sfx.wav');render_audio.write_wav_float(str(wav),base64.b64decode(res['b64']))
            subprocess.run([ff,'-y','-v','error','-i',str(silent),'-i',str(wav),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',str(movie)],check=True)
            report={'name':name,'stage':stage,'role':role,'pilot':pilot,'seconds':seconds,'peakMist':peakMist,'dashFrames':dashes,'audio':{k:res[k]for k in ['peak','rms','counts','errs']},'sounds':sorted(set(e[1]for e in ev['snd'])),'loops':sorted(ev['loops']),'timeline':timeline}
            reports.append(report);(OUT/'report.json').write_text(json.dumps({'takes':reports,'errors':errors},indent=2),encoding='utf-8')
            silent.unlink();wav.unlink();pg.close();print('DONE '+name,flush=True)
        b.close()
    srv.shutdown();assert not errors,errors
    inputs=OUT/'concat.txt';inputs.write_text(''.join("file '%s'\n"%(OUT/(t[0]+'.mp4')).as_posix()for t in TAKES))
    final=OUT/'BulletsOfFury_Weapon_Feedback_0913.mp4'
    subprocess.run([ff,'-y','-v','error','-f','concat','-safe','0','-i',str(inputs),'-c','copy','-movflags','+faststart',str(final)],check=True)
    subprocess.run([ff,'-v','error','-i',str(final),'-f','null','-'],check=True)
    print('VIDEO '+str(final),flush=True)
if __name__=='__main__':main()
