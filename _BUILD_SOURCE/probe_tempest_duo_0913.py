"""Native Stage 6 duo QA plus a compact in-game video with frame-aligned game sound.
Uses the existing real-game capture and OfflineAudioContext sound workflows.
The demonstration pilot is invincible; health gates are accelerated through
hitSubBoss so the recording can show coordination, both reactors and the survivor.
"""
import argparse,base64,http.server,importlib.util,json,os,subprocess,sys,threading,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE/trailer_v7'))
import capture3,render_audio
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import imageio_ffmpeg
STATE="""() => {const b=subBoss;if(!b)return {none:true,done:subBossDone};const D=b._tempestDuo;return {kind:b.kind,hp:b.hp,max:b.maxhp,dead:b.dead,alone:D.ai.alone,holds:D.ai.holds,pincers:D.ai.pincers,ships:D.ships.map(p=>({gray:p._tempestGray,x:p.x,y:p.y,phase:p._ai.phase,state:p._ai.state,hp:p._ai.hp,gone:p._ai.gone,vuln:p._tlv.vuln,beams:p._tlv.beams.filter(q=>q.active).length,warn:!!p._ai.entryWarn,rig:p._ai.rig.map(r=>r.hp)}))};}"""
HOOK="""() => {
window.__duoProof={blackX:0,blackY:0,blackDiagonal:0,grayDiagonal:0,playerMoves:0,keys:{},hits:0,rams:0,conflicts:0,needles:0,unbound:0,survivorFrames:0};
const W=window.__duoProof,og=XART.get.bind(XART);XART.get=function(k){if(/^tlv/.test(k))W.keys[k]=(W.keys[k]||0)+1;return og(k);};
const ou=tempestBrothersUpdate;tempestBrothersUpdate=function(b,dt){const D=b._tempestDuo,p=player,px=p.x,py=p.y,xy=D.ships.map(p=>[p.x,p.y]),prev=D.ai.black.state;ou(b,dt);
if(p.x!==px||p.y!==py)W.playerMoves++;
D.ships.forEach((p,i)=>{const dx=Math.abs(p.x-xy[i][0])>1e-6,dy=Math.abs(p.y-xy[i][1])>1e-6;if(i===0){if(dx)W.blackX++;if(dy)W.blackY++;if(dx&&dy)W.blackDiagonal++;}else if(dx&&dy)W.grayDiagonal++;});
if(prev!=='ram-warn'&&D.ai.black.state==='ram-warn'){W.rams++;if(D.ai.grayCrossing()&&!D.ai.alone)W.conflicts++;}
if(D.ai.alone&&!b.dead)W.survivorFrames++;
};
const seen=new WeakSet();window.__qaNeedles=()=>{for(const q of eBullets)if(q.kind==='tlvNeedle'&&!seen.has(q)){seen.add(q);W.needles++;if(!q._lockId||q.hp!==1||!q._shootable)W.unbound++;}};
playerHit=function(){W.hits++;};
}"""
DRIVE="""(i) => {
const t=i/60,K=Input.keys;let tx=worldWidth()/2+Math.sin(t*1.1)*130,ty=PLAY.y+PLAY.h*.78+Math.sin(t*1.6)*22;
K.a=player.x>tx+5;K.d=player.x<tx-5;K.w=player.y>ty+5;K.s=player.y<ty-5;K.j=true;
const b=subBoss;if(!b||!b._tempestDuo)return;
const D=b._tempestDuo;
const gate=(p,at,phase)=>{if(t>=at&&p._ai.phase===phase&&p._tlv.vuln)hitSubBoss(b.maxhp*4,p.x,p.y);};
gate(D.ships[0],10,'chase');gate(D.ships[0],23,'pursuit');gate(D.ships[0],30,'hell');gate(D.ships[0],35,'frenzy');
gate(D.ships[1],40,'chase');gate(D.ships[1],44,'pursuit');gate(D.ships[1],48,'hell');gate(D.ships[1],52,'frenzy');
}"""
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='_shots/tempest_duo_0913');ap.add_argument('--video',action='store_true');a=ap.parse_args()
    out=ROOT/a.out;out.mkdir(parents=True,exist_ok=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*args,**kw):super().__init__(*args,directory=str(ROOT),**kw)
        def log_message(self,*args):pass
    srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
    errors=[];checks=[];caps=[]
    def ok(c,label):checks.append({'pass':bool(c),'label':label});print(('ok  'if c else'FAIL ')+label,flush=True)
    with sync_playwright() as pw:
        br=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
        pg=br.new_page(viewport={'width':1100,'height':1200})
        pg.on('pageerror',lambda e:errors.append('pageerror '+str(e)))
        pg.on('console',lambda m:errors.append('console '+m.text)if m.type=='error'else None)
        pg.goto('http://127.0.0.1:%d/index.html'%srv.server_port,wait_until='load',timeout=120000)
        pg.wait_for_function("()=>(window.__bofFrames|0)>4",timeout=120000)
        pg.evaluate(shoot.TRAP_RAF);pg.wait_for_timeout(70)
        pg.evaluate("()=>{ASSETS.ready=true;story=null;playerHit=function(){};}")
        def step(n=2,wait=8):
            r=pg.evaluate(shoot.STEP,n)
            if r:errors.append('step '+str(r))
            if wait:pg.wait_for_timeout(wait)
            if pg.evaluate('()=>!!window.__qaNeedles'):pg.evaluate('()=>window.__qaNeedles()')
        def st():return pg.evaluate(STATE)
        def shot(name,label):
            raw=pg.evaluate("()=>document.getElementById('screen').toDataURL('image/png')")
            path=out/(name+'.png');path.write_bytes(base64.b64decode(raw.split(',')[1]));caps.append((label,path));print('capture '+name,flush=True)
        def start():
            pg.evaluate("()=>{story=null;ASSETS.ready=true;BOSSMODE.start(6,'mini','cole',false);playerHit=function(){};}")
            for _ in range(200):
                if pg.evaluate('()=>!!subBoss'):break
                step(6)
            pg.evaluate(HOOK)
            keys=['tlv_hull','tlv_hull_damaged','tlvb_hull','tlvb_hull_damaged','tlv_beam','tlv_charge','tlv_needle','tlv_bolt']+['nxp_barrage_'+str(i)for i in range(8)]
            for _ in range(50):
                if all(pg.evaluate('(ks)=>ks.map(k=>XART.rdy(k))',keys)):break
                step(2,70)
            pg.evaluate("()=>{player.invuln=0;player.dead=false;Input.keys.j=false;}")
        start();ok(st()['kind']=='tempestbrothers','Boss Mode warning spawns the native Stage 6 duo')
        for _ in range(100):
            if all(s['phase']=='chase' for s in st()['ships']):break
            step(2)
        ok(all(s['phase']=='chase'for s in st()['ships']),'both authored ships arrive and open their independent chase')
        step(30);shot('01_both_brothers','Both brothers in the real game')
        for _ in range(240):step(2)
        proof=pg.evaluate('()=>window.__duoProof')
        ok(proof['grayDiagonal']>0,'gray crosses diagonally while black stays on one axis')
        ok(proof['blackDiagonal']==0,'black movement remains axis-aligned')
        ok('tlvb_hull'in proof['keys'] and 'tlv_hull'in proof['keys'],'the real renderer draws both authored hull keys')
        # Explicit pincer: keep the approved AI planning and movement, only choose its starting state.
        pg.evaluate("()=>{const D=subBoss._tempestDuo;D.ai.black.enter('chase');D.ai.black.change('laser-track');D.ai.black.boss.y=230;D.ai.black.boss.x=450;D.ai.black.st=.6;D.ai.gray.change('regroup');D.ai.gray.planRun();D.ai.gray.boss={...D.ai.gray.start,a:0};D.ai.gray.change('warn');tempestBrothersSync(subBoss);}")
        step(44);shot('02_pincer','Gray pincer beneath black rear lasers')
        ok(st()['pincers']>0,'approved pincer planning runs in the native game')
        pg.evaluate("()=>{const b=subBoss,p=b._tempestDuo.ships[0];p._ai.vulnerable=true;tempestBrothersSync(b);hitSubBoss(b.maxhp*4,p.x,p.y);}")
        for _ in range(180):
            if st()['ships'][0]['phase']=='pursuit':break
            step(2)
        ok(st()['ships'][0]['phase']=='pursuit','native hit advances black alone to pursuit')
        for _ in range(480):
            if st()['ships'][0]['state']=='ram-warn':break
            step(2)
        print('ram state '+json.dumps(st()),flush=True)
        shot('03_ram_warning','Black ram; gray yields offscreen')
        ok(st()['holds']>0,'gray waits offscreen during the black ram sequence')
        step(36);shot('04_side_ram','Black crosses the screen on its warned row')
        # Gauge pixel equality with simultaneous forward laser lanes at camera zoom.
        pg.evaluate("()=>{const b=subBoss,D=b._tempestDuo;D.ai.black.enter('pursuit');D.ai.black.boss.x=450;D.ai.black.boss.y=930;D.ai.black.vulnerable=true;D.ai.black.lasers(-1,.7,.5,1.2);tempestBrothersSync(b);shake=0;}")
        pg.evaluate('()=>drawScene(0)');shot('05_forward_lasers','Forward lasers stop below MINI BOSS gauge')
        # Isolate the production miniboss renderer from the rain's independent
        # animation. Preserve the exact world camera/zoom and screenBar path.
        band="""(off)=>{const c=document.getElementById('screen');ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,c.width,c.height);ctx.setTransform(SS,0,0,SS,0,0);const z=viewZoom();ctx.save();if(z!==1){ctx.scale(z,z);ctx.translate(0,VH*(1-z)/z);}if(worldWidth()>viewW())ctx.translate(-camX,0);_inWorldXform=true;if(off)for(const p of subBoss._tempestDuo.ships)p._tlv.beams=[];drawSubBoss();_inWorldXform=false;ctx.restore();return Array.from(ctx.getImageData(0,0,c.width,Math.round(c.height*77/VH)).data);}"""
        pix=pg.evaluate(band,False)
        pix2=pg.evaluate(band,True)
        ok(pix==pix2,'gauge-band pixels are identical with the forward lasers on and off')
        # All source gates through native damage, with no writes to player by the AI.
        pg.evaluate("()=>{const b=subBoss,p=b._tempestDuo.ships[0];p._ai.vulnerable=true;tempestBrothersSync(b);hitSubBoss(b.maxhp*4,p.x,p.y);}")
        step(120)
        for _ in range(240):step(2)
        proof=pg.evaluate('()=>window.__duoProof')
        ok(proof['needles']>0 and proof['unbound']==0,'hell needles use the real unit retina and one-HP shootable rounds')
        shot('06_hell_needles','Hell needles with the game retina lock')
        pg.evaluate("()=>{const b=subBoss,p=b._tempestDuo.ships[0];p._ai.vulnerable=true;tempestBrothersSync(b);hitSubBoss(b.maxhp*4,p.x,p.y);}")
        step(100)
        pg.evaluate("()=>{const b=subBoss,p=b._tempestDuo.ships[0];p._ai.vulnerable=true;tempestBrothersSync(b);hitSubBoss(b.maxhp*4,p.x,p.y);}")
        step(220);shot('07_gray_survivor','Gray fights on after black reactor failure')
        ok(st()['alone'] and st()['ships'][0]['gone'] and not st()['dead'],'black reactor leaves gray fighting on alone')
        proof=pg.evaluate('()=>window.__duoProof')
        ok(proof['playerMoves']==0 and proof['conflicts']==0,'AI never moves the player or starts a ram during gray crossing')
        if a.video:
            print('Starting 58-second real-renderer demonstration',flush=True)
            pg.evaluate(capture3.LIB);start()
            pg.evaluate("()=>{story=null;dlgBox=function(){};floaters.length=0;window.__i=1;window.__mode='none';window.__fire=false;window.__auto=function(){};const L=window.__alog;L.snd.length=0;L.syn.length=0;L.warp.length=0;L.restarts.length=0;L.loops={};}")
            # Capture starts on a fresh sound log supplied by LIB before warmup; rec0 trims warmup.
            rec0=pg.evaluate('()=>window.__i')
            ff=imageio_ffmpeg.get_ffmpeg_exe();silent=out/'duo_picture.mp4'
            cmd=[ff,'-y','-loglevel','error','-f','image2pipe','-vcodec','mjpeg','-framerate','30','-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(silent)]
            with subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)as enc:
                timeline=[]
                for frame in range(58*30):
                    i=frame*2
                    pg.evaluate(DRIVE,i)
                    pg.evaluate('()=>window.__step(2)')
                    pg.evaluate('()=>window.__qaNeedles()')
                    raw=pg.evaluate("()=>document.getElementById('screen').toDataURL('image/jpeg',.92).split(',')[1]")
                    enc.stdin.write(base64.b64decode(raw))
                    if frame%150==0:
                        ss=st();timeline.append({'seconds':frame/30,'state':ss});print('video %.0fs %s'%(frame/30,json.dumps(ss)),flush=True)
                enc.stdin.close();err=enc.stderr.read();ret=enc.wait();assert ret==0,err
            ev=pg.evaluate('()=>window.__audioDump()');ev.update(rec0=rec0,frames=58*60)
            (out/'audio_events.json').write_text(json.dumps(ev),encoding='utf-8')
            res=pg.evaluate(render_audio.RENDER,{'ev':ev,'iife':render_audio.audio_module_source(),'tail':0,'exclude':[]})
            raw=base64.b64decode(res['b64']);render_audio.write_wav_float(str(out/'duo_sfx.wav'),raw)
            print('audio',res.get('counts'),res.get('errors'),flush=True)
            audio_errors=res.get('errors',res.get('errs',[]));ok(not audio_errors,'frame-aligned game sound renders without errors')
            ok(res['counts']['snd']>0 and res['rms']>0,'recording contains the game shot, laser and explosion sounds')
            movie=out/'BulletsOfFury_Stage6_TempestBrothers.mp4'
            subprocess.run([ff,'-y','-loglevel','error','-i',str(silent),'-i',str(out/'duo_sfx.wav'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-af','alimiter=limit=0.9:level=false','-shortest','-movflags','+faststart',str(movie)],check=True)
            (out/'video_timeline.json').write_text(json.dumps(timeline,indent=2),encoding='utf-8')
            ok(st().get('done',False),'recorded demonstration finishes both reactors and releases the native slot')
            print('VIDEO '+str(movie),flush=True)
        ok(not errors,'zero page errors and console errors')
        br.close()
    srv.shutdown()
    thumbs=[]
    for label,path in caps:
        im=Image.open(path).convert('RGB');im.thumbnail((320,342));tile=Image.new('RGB',(340,374),'#131822');tile.paste(im,((340-im.width)//2,0));ImageDraw.Draw(tile).text((8,346),label[:49],fill='white');thumbs.append(tile)
    contact=Image.new('RGB',(340*4,374*2),'#080b11')
    for i,im in enumerate(thumbs):contact.paste(im,((i%4)*340,(i//4)*374))
    contact.save(out/'_contact.png')
    (out/'results.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf-8')
    print('%d ok / %d fail'%(sum(c['pass']for c in checks),sum(not c['pass']for c in checks)),flush=True)
    return int(any(not c['pass']for c in checks))
if __name__=='__main__':sys.exit(main())
