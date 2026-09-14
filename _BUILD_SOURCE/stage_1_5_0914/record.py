"""Native encounter preview, streamed frames and actual accepted game sound routes."""
import base64,json,subprocess,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE/trailer_v7'));import capture3,render_audio
import audio_export as render_audio
from probe import PREP
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
OUT=ROOT/'_shots/stage_1_5_0914/video';OUT.mkdir(parents=True,exist_ok=True)
TAKES=[('s1_burning_fodder',1,None,5),('s1_razorback',1,'mini',6),('s1_overlord',1,'boss',6),
 ('s2_flight_pixels',2,None,4),('s3_drone_visibility',3,None,4),('s3_cannon_lasers',3,'boss',6),
 ('s4_warmachine',4,'mini',9),('s4_helpers_and_dive',4,'boss',12),('s5_sky_and_spaceship',5,'launch',14),('s5_regent_and_volley',5,'boss',10)]
DRIVE=r'''([name,i])=>{const K=Input.keys;for(const k of ['a','d','w','s','j','h'])K[k]=false;
 const T=window.__tgt(),mid=(camLeftX()+camRightX())*.5;
 if(name==='s1_burning_fodder'&&i%120===0){for(const dx of [-80,80]){const e=spawnEnemy('s1jetdelta',worldWidth()/2+dx,-35,{});if(e){e.ghost=false;e.hp=e.maxhp*.40;}}}
 if(name==='s2_flight_pixels'&&i%80===0){for(const [type,dx]of [['ash',-85],['skim',0],['lance',85]])spawnEnemy(type,worldWidth()/2+dx,80,{});}
 if(name==='s3_drone_visibility'&&i%100===0){for(const dx of [-80,80]){const e=spawnEnemy('cryoeye',worldWidth()/2+dx,100,{vy:0});e.ghost=false;e._dr.aim=Math.PI/2;droneFire(e);}}
 if(name==='s1_razorback'&&i===180){const R=T._rzb;R.state='turret';R.attack='sonic';R.at=.18;R.trans=0;R.beat=-1;}
 if(name==='s1_overlord'){if(i===120)ovRocketSide(T,-1);if(i===200)ovGreenVolley(T);if(i===260)ovRotorTempest(T);}
 if(name==='s4_helpers_and_dive'){
   const H=T._s4war.shield,live=H.nodes.filter(n=>!n.dead);
   if(live.length){const side=live.some(n=>n.side<0)?-1:1,n=live.find(n=>n.side===side),tx=n.x;
     K.a=player.x>tx+4;K.d=player.x<tx-4;K.j=Math.abs(player.x-tx)<14;
   }else{K.a=player.x>worldWidth()/2+6;K.d=player.x<worldWidth()/2-6;if(!T._s4war.ram&&!window.__diveStarted){window.__diveStarted=stage4RamStart(T);}}
   return;
 }
 if(name==='s5_regent_and_volley'){const tx=mid+Math.sin(i/60*.9)*100;K.a=player.x>tx+4;K.d=player.x<tx-4;K.j=true;
   if(i===240){run.spaceWeapon=1;spaceShadowRelease(SPACE_SHADOW_FULL_CHARGE);}
   if(i===360)run.spaceWeapon=0;
 }
}'''
def main():
 class Quiet(http.server.SimpleHTTPRequestHandler):
  def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
  def log_message(self,*a):pass
 srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
 ff=imageio_ffmpeg.get_ffmpeg_exe();reports=json.loads((OUT/'report.json').read_text())['takes']if '--resume'in sys.argv and (OUT/'report.json').exists()else[];errors=[]
 with sync_playwright()as p:
  browser=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
  for name,stage,role,seconds in TAKES:
   if any(r['name']==name for r in reports):continue
   pg=browser.new_page(viewport={'width':1100,'height':1200});pg.on('pageerror',lambda e:errors.append('page '+str(e)));pg.on('console',lambda m:errors.append('console '+m.text)if m.type=='error'else None)
   pg.goto('http://127.0.0.1:%d/index.html'%srv.server_port,wait_until='load',timeout=120000);pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB);pg.evaluate('()=>window.__auto=function(){}')
   if '--audio-diagnose'in sys.argv:
    diagnose='s5_regent_and_volley'if '--regent'in sys.argv else's5_sky_and_spaceship'if '--sky'in sys.argv else's4_helpers_and_dive'
    ev=json.loads((OUT/(diagnose+'_events.json')).read_text());names=set(q[1]for q in ev['snd']+ev['syn'])|set(ev['loops']);stems={}
    res=pg.evaluate(render_audio.RENDER,{'ev':ev,'iife':render_audio.audio_module_source(),'tail':0,'exclude':[]})
    import numpy as np
    a=np.frombuffer(base64.b64decode(res['b64']),dtype='<f4');at=int(np.argmax(np.abs(a)))/96000;print('FULL PEAK '+str(res['peak'])+' AT '+str(at)+'s',flush=True);print('NEARBY '+str([q for q in ev['snd']+ev['syn']if abs((q[0]-ev['rec0'])/60-at)<.8]),flush=True)
    if '--candidates'in sys.argv:
     import copy
     candidates=[(.24,.40,.50,.60,1),(.24,.40,.50,.60,.60),(.22,.36,.46,.56,.55)]
     for c,h,l,v,enemy in candidates:
      q=copy.deepcopy(ev);q['tame']['spaceLaserCannon']['g']=c;q['tame']['spaceVolleyHit']['g']=h;q['tame']['spaceLaserHit']['g']=l
      for e in q['snd']:
       if e[1]=='spaceVolleyLaunch':e[2]*=v/.92
       if enemy!=1 and e[1]in ['bossWeaponCharge','bossfireXenoregent','enemyPulseLaserAlien','shieldHitLight']:e[2]*=enemy
      rr=pg.evaluate(render_audio.RENDER,{'ev':q,'iife':render_audio.audio_module_source(),'tail':0,'exclude':[]});print('CANDIDATE '+str((c,h,l,v,enemy))+' peak '+str(rr['peak']),flush=True)
     return
    for key in sorted(names):
     res=pg.evaluate(render_audio.RENDER,{'ev':ev,'iife':render_audio.audio_module_source(),'tail':0,'exclude':sorted(names-{key})});stems[key]={k:res[k]for k in ['peak','rms','counts','errs']};print(key+' '+str(res['peak']),flush=True)
    (OUT/(diagnose+'_audio-stems.json')).write_text(json.dumps(stems,indent=2));return
   if role=='launch':
    pg.evaluate('()=>{window.__run(5,"yuri");window.__auto=function(){};}')
    for _ in range(400):
     if pg.evaluate('()=>drawLaunch._phase==="settle"'):break
     pg.evaluate('()=>window.__step(6)');pg.wait_for_timeout(8)
    assert pg.evaluate('()=>drawLaunch._phase==="settle"'),'launch did not settle'
   elif role:
    r=pg.evaluate('a=>window.__fight(a[0],a[1],"yuri")',[stage,role]);assert r['ok'],r
    for _ in range(150):
     if pg.evaluate('()=>{const T=window.__tgt();return T&&!T.enter&&T.y>0&&(!T._rzb||T._rzb.state!=="arrival");}'):break
     pg.evaluate('()=>window.__step(6)');pg.wait_for_timeout(8)
   else:pg.evaluate(PREP,stage)
   pg.evaluate('''()=>{Audio.resume();stageRevisionWarm('razorback');stageRevisionWarm('damkeeper');stageRevisionWarm('olivewarden');warmPlayerAtlases();
     for(const k of ['nxp_upward_7','nsd_chim_7','cfx_stage2_volcanic_projectiles','bpfx_proj_laser_0','mgcf_1_5','bpfx_proj_missile_0','bmfx_fov_green_tall','bmfx_fov_red_tall'])XART.rdy(k);
     if(run.stage===5){for(let lv=1;lv<=5;lv++)for(const k of ['volley_sprite_','shadow_core_','laser_sprite_'])spaceAtlasCanvas(k+lv,'yuri');spaceAtlasCanvas('ship_base','yuri');}
   }''');pg.wait_for_timeout(900)
   pg.evaluate('''([n,r])=>{playerHit=function(){};player.invuln=0;story=null;dlgBox=function(){};floaters=[];Object.keys(Input.keys).forEach(k=>Input.keys[k]=false);window.__auto=function(){};
    if(r!=='launch'){stagePlan=[];enemies=[];player.x=worldWidth()/2;player.y=430;pBullets=[];eBullets=[];}
    if(n==='s3_cannon_lasers'){boss._l23Beam=null;boss._sba=null;stage3BossAttack(boss,'s3wallcannons',0,0,1);}
    if(n==='s4_helpers_and_dive'){boss.hp=boss.maxhp*.5;boss._s4war.shieldThresholdIndex=2;boss._s4war.shield.nodes.forEach(n=>n.hp=1);stage4CoreTurretSpawnMissing(boss,.5);stage4ShieldTick(boss,1);run.pilot='axel';run.weapon=3;run.wlevel=5;window.__diveStarted=false;}
    if(n==='s5_regent_and_volley'){run.spaceWeapon=0;run.spaceLevels=[3,3,3];}
    window.__i=1;const L=window.__alog;L.snd.length=0;L.syn.length=0;L.warp.length=0;L.restarts.length=0;L.loops={};
   }''',[name,role]);rec0=pg.evaluate('()=>window.__i')
   silent=OUT/(name+'_picture.mp4');movie=OUT/(name+'.mp4')
   enc=subprocess.Popen([ff,'-y','-v','error','-f','image2pipe','-vcodec','mjpeg','-framerate','30','-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(silent)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
   timeline=[]
   for frame in range(seconds*30):
    pg.evaluate(DRIVE,[name,frame*2]);pg.evaluate('()=>window.__step(2)')
    enc.stdin.write(base64.b64decode(pg.evaluate("()=>document.querySelector('#screen').toDataURL('image/jpeg',.90).split(',')[1]")))
    if frame%60==0:
     q=pg.evaluate('()=>({state:state,dead:player.dead,error:window.__err||null,target:window.__tgt()&&window.__tgt().name,mode:boss&&boss._s4war&&boss._s4war.mode,launch:drawLaunch._phase,missiles:pBullets.filter(q=>q.kind==="spaceVolley").length})');assert not q['dead']and not q['error'],q;timeline.append({'seconds':frame/30,**q});print(name+' '+str(frame/30)+'s '+json.dumps(q),flush=True)
    if frame in [30,90,150,210,270,330]:
     (OUT/(name+'_%03d.png'%frame)).write_bytes(base64.b64decode(pg.evaluate("()=>document.querySelector('#screen').toDataURL().split(',')[1]")))
    if frame%30==0:pg.wait_for_timeout(5)
   enc.stdin.close();err=enc.stderr.read();assert enc.wait()==0,err
   ev=pg.evaluate('()=>window.__audioDump()');ev.update(rec0=rec0,frames=seconds*60);(OUT/(name+'_events.json')).write_text(json.dumps(ev),encoding='utf-8')
   res=pg.evaluate(render_audio.RENDER,{'ev':ev,'iife':render_audio.audio_module_source(),'tail':0,'exclude':[]});assert not res['errs'],res['errs'];assert res['peak']<1,res['peak']
   wav=OUT/(name+'_sfx.wav');render_audio.write_wav_float(str(wav),base64.b64decode(res['b64']))
   subprocess.run([ff,'-y','-v','error','-i',str(silent),'-i',str(wav),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',str(movie)],check=True)
   reports.append({'name':name,'stage':stage,'role':role,'seconds':seconds,'timeline':timeline,'audio':{k:res[k]for k in ['peak','rms','counts','errs']},'sounds':sorted(set(e[1]for e in ev['snd'])),'loops':sorted(ev['loops'])});(OUT/'report.json').write_text(json.dumps({'takes':reports,'errors':errors},indent=2),encoding='utf-8')
   silent.unlink();wav.unlink();pg.close();print('DONE '+name,flush=True)
  browser.close()
 srv.shutdown();assert not errors,errors
 inputs=OUT/'concat.txt';inputs.write_text(''.join("file '%s'\n"%(OUT/(t[0]+'.mp4')).as_posix()for t in TAKES))
 final=OUT/'BulletsOfFury_Stages_1_to_5_0914.mp4';subprocess.run([ff,'-y','-v','error','-f','concat','-safe','0','-i',str(inputs),'-c','copy','-movflags','+faststart',str(final)],check=True)
 subprocess.run([ff,'-v','error','-i',str(final),'-f','null','-'],check=True);print('VIDEO '+str(final),flush=True)
if __name__=='__main__':main()
