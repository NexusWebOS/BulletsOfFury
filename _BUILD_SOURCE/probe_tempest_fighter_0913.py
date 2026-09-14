"""Real game QA and a sound-synced recording of Mike's revised fighter-jet passes."""
import base64,http.server,json,subprocess,sys,threading
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE/trailer_v7'));import capture3,render_audio
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import imageio_ffmpeg
RETURNS='--return-pass'in sys.argv
OUT=ROOT/('_shots/tempest_return_0913'if RETURNS else'_shots/tempest_fighter_0913')
STATE="""()=>{const b=subBoss;if(!b)return {none:true,done:subBossDone};return {hp:b.hp,max:b.maxhp,striker:b._tempestDuo.striker?b._tempestDuo.striker._tempestGray?'gray':'black':null,ships:b._tempestDuo.ships.map(p=>({gray:p._tempestGray,x:p.x,y:p.y,angle:p._jet.angle,active:p._jet.active,state:p._jet.state,cue:p._jet.cue,passes:p._jet.passes,greens:p._jet.greens,thrusts:p._jet.thrusts,phase:p._ai.phase,vuln:p._tlv.vuln,outside:tempestJetOutside(p),bounds:tempestJetBounds(p)}))};}"""
HOOK="""()=>{
window.__fighter={playerMoves:0,diagonal:[0,0],turns:[0,0],cues:[{},{}],samples:[],overlap:0,ports:0,exits:[0,0],returns:[0,0],afterExit:[false,false],noseMismatch:0,earlyTurn:0,teleports:0,turnMoved:0};
const W=window.__fighter,ou=tempestBrothersUpdate;
tempestBrothersUpdate=function(b,dt){const px=player.x,py=player.y,D=b._tempestDuo,before=D.ships.map(p=>[p._ai.boss.x,p._ai.boss.y,p._jet.angle,p._jet.state]);ou(b,dt);
if(player.x!==px||player.y!==py)W.playerMoves++;
if(D.ships.filter(p=>p._jet.active).length>1)W.overlap++;
D.ships.forEach((p,i)=>{const dx=(p._ai.boss.x-before[i][0])*TLV_KX,dy=(p._ai.boss.y-before[i][1])*TLV_KY,d=Math.hypot(dx,dy),old=before[i][3],J=p._jet;
if(Math.abs(dx)>1e-6&&Math.abs(dy)>1e-6)W.diagonal[i]++;if(Math.abs(J.angle-before[i][2])>0.01)W.turns[i]++;if(J.cue)W.cues[i][J.cue]=(W.cues[i][J.cue]||0)+1;
if((old==='thrust'||old==='return')&&d>1e-6&&J.active){if((dx*Math.sin(J.angle)-dy*Math.cos(J.angle))/d<.999999)W.noseMismatch++;if(d>(old==='return'?560:Math.hypot(J.vx,J.vy))*dt+1e-6)W.teleports++;}
if(old==='thrust'&&J.state==='offscreen-turn'){W.exits[i]++;W.afterExit[i]=true;if(!tempestJetOutside(p,90))W.earlyTurn++;}
if(old==='offscreen-turn'&&d>1e-6)W.turnMoved++;
if(W.afterExit[i]&&old==='return'&&!tempestJetOutside(p)){W.returns[i]++;W.afterExit[i]=false;}
});
};
playerHit=function(){};
}"""
DRIVE="""(i)=>{const t=i/60,K=Input.keys,tx=worldWidth()/2+Math.sin(t*.95)*125,ty=PLAY.y+PLAY.h*.77+Math.sin(t*1.5)*22;K.a=player.x>tx+5;K.d=player.x<tx-5;K.w=player.y>ty+5;K.s=player.y<ty-5;K.j=true;}"""
if RETURNS:DRIVE=DRIVE.replace('K.j=true','K.j=false')
def main():
    OUT.mkdir(parents=True,exist_ok=True);checks=[];errors=[];shots=[]
    def ok(c,label):checks.append({'pass':bool(c),'label':label});print(('ok  'if c else'FAIL ')+label,flush=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
        def log_message(self,*a):pass
    srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
    with sync_playwright()as pw:
        br=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
        pg=br.new_page(viewport={'width':1100,'height':1200})
        pg.on('pageerror',lambda e:errors.append('page '+str(e)))
        pg.on('console',lambda m:errors.append('console '+m.text)if m.type=='error'else None)
        pg.goto('http://127.0.0.1:%d/index.html'%srv.server_port,wait_until='load',timeout=120000)
        pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);pg.evaluate(shoot.TRAP_RAF);pg.wait_for_timeout(80)
        def step(n=2):
            r=pg.evaluate(shoot.STEP,n)
            if r:errors.append('step '+str(r))
            pg.wait_for_timeout(5)
        def st():return pg.evaluate(STATE)
        def shot(name):
            raw=pg.evaluate("()=>document.getElementById('screen').toDataURL('image/png').split(',')[1]");path=OUT/(name+'.png');path.write_bytes(base64.b64decode(raw));shots.append(path);print('capture '+name,flush=True)
        def start():
            pg.evaluate("()=>{ASSETS.ready=true;story=null;BOSSMODE.start(6,'mini','cole',false);playerHit=function(){};}")
            for _ in range(200):
                if pg.evaluate('()=>!!subBoss'):break
                step(6)
            keys=['tlv_hull','tlvb_hull','tlv_hull_damaged','tlvb_hull_damaged','tlv_beam','tlv_charge']+['ndr_dambreaker_bottomthruster_'+str(i)for i in range(4)]
            for _ in range(70):
                if all(pg.evaluate('(ks)=>ks.map(k=>XART.rdy(k))',keys)):break
                step(2);pg.wait_for_timeout(60)
            pg.evaluate("()=>{player.invuln=0;player.dead=false;Input.keys.j=false;}");pg.evaluate(HOOK)
        start();ok(pg.evaluate("()=>subBoss.kind==='tempestbrothers'&&subBoss._tempestDuo.ships.every(p=>p._jet.angle===Math.PI)"),'warning route starts both authored hulls nose south')
        for _ in range(200):
            if all(p['phase']=='chase'for p in st()['ships']):break
            step(2)
        shot('01_south_facing')
        seen=set()
        for _ in range(1100 if RETURNS else 850):
            step(2);state=st()
            view=pg.evaluate('()=>({left:camLeftX(),right:camRightX(),top:viewTopY()+77/viewZoom(),bottom:VH})')if RETURNS else None
            for p in state['ships']:
                if p['cue']and(p['gray'],p['cue'])not in seen:
                    seen.add((p['gray'],p['cue']));shot(('gray'if p['gray']else'black')+'_'+p['cue'])
                if p['active']and p['state']=='thrust'and(p['gray'],'thrust')not in seen:
                    seen.add((p['gray'],'thrust'));shot(('gray'if p['gray']else'black')+'_thrust')
                if RETURNS and p['state']=='offscreen-turn'and(p['gray'],'exit')not in seen:
                    seen.add((p['gray'],'exit'));shot(('gray'if p['gray']else'black')+'_fully_offscreen')
                if RETURNS and p['state']=='return'and p['bounds']['top']>view['top']and p['bounds']['bottom']<view['bottom']and p['bounds']['left']>view['left']and p['bounds']['right']<view['right']and(p['gray'],'return')not in seen:
                    seen.add((p['gray'],'return'));shot(('gray'if p['gray']else'black')+'_returning')
            if len(seen)==(10 if RETURNS else 6):break
        proof=pg.evaluate('()=>window.__fighter');print('proof '+json.dumps(proof),flush=True)
        ok(all((g,c)in seen for g in [False,True]for c in ['red','green','thrust']),'each brother visibly aims red, commits green and thrusts')
        ok(all(n>0 for n in proof['diagonal'])and all(n>0 for n in proof['turns']),'both jets bank and slide through real two-axis motion')
        ok(proof['overlap']==0 and proof['playerMoves']==0,'fighter passes are coordinated and never move the pilot')
        if RETURNS:
            ok(all(n>0 for n in proof['exits'])and all(n>0 for n in proof['returns']),'each brother completely exits and physically re-enters the camera')
            ok(proof['noseMismatch']==0,'the authored nose follows outbound thrust and inbound flight')
            ok(proof['earlyTurn']==0 and proof['turnMoved']==0 and proof['teleports']==0,'turns happen fully offscreen and reentry has no position jumps')
        port=None
        for _ in range(120):
            port=pg.evaluate("()=>{const b=subBoss,p=b._tempestDuo.ships.find(p=>{if(!p._tlv.vuln||p._ai.rig[0].hp<=100)return false;const q=tempestPortXY(p,0);return tempestBrothersPartAt(b,q.x,q.y)===(p._tempestGray?'G0':'B0');});if(!p)return null;const before=p._ai.rig[0].hp,q=tempestPortXY(p,0);hitSubBoss(b.maxhp*.006,q.x,q.y);return {before:before,after:p._ai.rig[0].hp,key:tempestJetPartAt(p,q.x,q.y)};}")
            if port:break
            step(2)
        print('port hit '+json.dumps(port),flush=True)
        ok(port and port['after']<port['before']and port['key']=='ap0','a real damage call reaches the front port on the rotated hull')
        # Screen-space gauge pixels, including a 45-degree bank and angled lasers.
        band="""(off)=>{const b=subBoss,p=b._tempestDuo.ships[0];p._jet.angle=Math.PI/4;p._jet.baseAngle=Math.PI;p._ai.boss.x=450;p._ai.boss.y=900;p._ai.vulnerable=true;p._ai.beams=[{id:0,dir:-1,active:true,charge:1}];tempestBrothersSync(b);if(off)p._tlv.beams=[];const c=document.getElementById('screen');ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,c.width,c.height);ctx.setTransform(SS,0,0,SS,0,0);ctx.save();const z=viewZoom();if(z!==1){ctx.scale(z,z);ctx.translate(0,VH*(1-z)/z);}if(worldWidth()>viewW())ctx.translate(-camX,0);_inWorldXform=true;drawSubBoss();_inWorldXform=false;ctx.restore();return Array.from(ctx.getImageData(0,0,c.width,c.height*77/VH).data);}"""
        ok(pg.evaluate(band,False)==pg.evaluate(band,True),'banked laser pixels remain outside the MINI BOSS gauge band')
        pg.evaluate(capture3.LIB);start()
        pg.evaluate("()=>{story=null;dlgBox=function(){};floaters.length=0;window.__i=1;window.__auto=function(){};const L=window.__alog;L.snd.length=0;L.syn.length=0;L.warp.length=0;L.restarts.length=0;L.loops={};}")
        rec0=pg.evaluate('()=>window.__i');ff=imageio_ffmpeg.get_ffmpeg_exe();silent=OUT/'fighter_picture.mp4';movie=OUT/('BulletsOfFury_Tempest_ExitAndReturn.mp4'if RETURNS else'BulletsOfFury_Tempest_FighterPasses.mp4')
        cmd=[ff,'-y','-loglevel','error','-f','image2pipe','-vcodec','mjpeg','-framerate','30','-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(silent)]
        timeline=[]
        with subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)as enc:
            for frame in range(30*30):
                pg.evaluate(DRIVE,frame*2);pg.evaluate('()=>window.__step(2)')
                raw=pg.evaluate("()=>document.getElementById('screen').toDataURL('image/jpeg',.92).split(',')[1]");enc.stdin.write(base64.b64decode(raw))
                if frame%90==0:
                    ss=st();timeline.append({'seconds':frame/30,'state':ss});print('video %ds %s'%(frame/30,json.dumps(ss)),flush=True)
            enc.stdin.close();err=enc.stderr.read();ret=enc.wait();assert ret==0,err
        ev=pg.evaluate('()=>window.__audioDump()');ev.update(rec0=rec0,frames=30*60);(OUT/'audio_events.json').write_text(json.dumps(ev),encoding='utf-8')
        res=pg.evaluate(render_audio.RENDER,{'ev':ev,'iife':render_audio.audio_module_source(),'tail':0,'exclude':[]});render_audio.write_wav_float(str(OUT/'fighter_sfx.wav'),base64.b64decode(res['b64']))
        names={e[1]for e in ev['snd']};ok(all(k in names for k in ['tlvJetCharge','tlvJetReady','tlvJetTurn','tlvJetThrust','tlvJetBrake'])and 'tlvJetEngine'in ev['loops'],'recorded game audio includes turns, charge, green cue, ignition, engine and brakes')
        ok(not res['errs']and res['rms']>0,'game sound replay renders without errors or silence')
        subprocess.run([ff,'-y','-loglevel','error','-i',str(silent),'-i',str(OUT/'fighter_sfx.wav'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-af','alimiter=limit=0.9:level=false','-shortest','-movflags','+faststart',str(movie)],check=True)
        proof=pg.evaluate('()=>window.__fighter');ok(proof['overlap']==0 and proof['playerMoves']==0,'recorded real-input demonstration keeps coordinated passes and pilot ownership')
        if RETURNS:ok(all(n>0 for n in proof['exits'])and all(n>0 for n in proof['returns'])and proof['noseMismatch']==0 and proof['teleports']==0,'recorded gameplay includes both complete exits and aligned physical returns')
        ok(not errors,'zero console errors and page errors');br.close()
    srv.shutdown()
    contact=Image.new('RGB',(320*4,370*((len(shots)+3)//4)),'#111821')
    for i,path in enumerate(shots):
        im=Image.open(path).convert('RGB');im.thumbnail((320,342));contact.paste(im,(i%4*320,i//4*370));ImageDraw.Draw(contact).text((i%4*320+8,i//4*370+348),path.stem,fill='white')
    contact.save(OUT/'_contact.png');(OUT/'video_timeline.json').write_text(json.dumps(timeline,indent=2),encoding='utf-8')
    (OUT/'results.json').write_text(json.dumps({'checks':checks,'errors':errors,'motion':proof,'audio':{'counts':res['counts'],'rms':res['rms'],'errors':res['errs']}},indent=2),encoding='utf-8')
    print('VIDEO '+str(movie),flush=True);print('%d ok / %d fail'%(sum(c['pass']for c in checks),sum(not c['pass']for c in checks)),flush=True)
    return int(any(not c['pass']for c in checks))
if __name__=='__main__':sys.exit(main())
