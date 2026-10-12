"""Native full homecoming animation recording; no fabricated/tweened sprites."""
from pathlib import Path
import sys,json,base64,subprocess,os
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/os.environ.get('BOF_HL10_OUT','_shots/hq_landing_1010');OUT.mkdir(parents=True,exist_ok=True)
END=float(os.environ.get('BOF_HL10_END','26.25'))
BEGIN=float(os.environ.get('BOF_HL10_BEGIN','0'))
PILOT=os.environ.get('BOF_HL10_PILOT','cole')
errors=[];port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1280,height=900));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:1000]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  # Capture the game's actual WebAudio master bus alongside its native canvas.
  # No replacement sound synthesis and no mutation of the shipping audio code.
  p.add_init_script('''(()=>{const Base=window.AudioContext||window.webkitAudioContext;if(!Base)return;
   window.__bofRecordAudio=[];const connect=AudioNode.prototype.connect;
   class RecordingContext extends Base{constructor(...args){super(...args);
    this.__bofMovie=this.createMediaStreamDestination();window.__bofRecordAudio.push(this);
    if(window.__bofMovieMix)window.__bofMovieMix.createMediaStreamSource(this.__bofMovie.stream).connect(window.__bofMovieMix.__bofMovie);}}
   window.AudioContext=RecordingContext;if(window.webkitAudioContext)window.webkitAudioContext=RecordingContext;
   AudioNode.prototype.connect=function(target,...args){const out=connect.call(this,target,...args);
    if(target===this.context.destination&&this.context.__bofMovie)connect.call(this,this.context.__bofMovie,...args);
    return out;};
   window.__bofMovieMix=new RecordingContext();
   const play=HTMLMediaElement.prototype.play;
   HTMLMediaElement.prototype.play=function(...args){
    if(this.tagName==='AUDIO'&&!this.__bofMovieSource){try{
     this.__bofMovieSource=window.__bofMovieMix.createMediaElementSource(this);
     this.__bofMovieSource.connect(window.__bofMovieMix.destination);
    }catch(e){this.__bofMovieSource='existing game DSP source';}}
    return play.apply(this,args);
   };})();''')
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("pk=>{Object.defineProperty(navigator,'getGamepads',{configurable:true,value:()=>[]});BOFCinematicDirector.cancel();run.mode='campaign';run.pilot=pk;story=null;fb2Talk=null;s6Opening=null;drawVictory._t=0;drawVictory._ready=false;drawVictory._hl10=null;drawVictory._trueEnding=true;setState(GS.VICTORY);victoryEndingWarm();hl10Warm();Audio.init();Audio.stopMusic();Audio.resume();}",PILOT)
  p.wait_for_function('victoryEndingReady()&&hl10Warm()',polling=50)
  p.evaluate('()=>{for(const a of window.__bofRecordAudio||[])a.resume();}')
  p.wait_for_function('window.__bofRecordAudio?.length>0&&window.__bofRecordAudio.every(a=>a.state==="running")',polling=50)
  data=p.evaluate("""async({begin,end})=>{
   drawVictory._ready=true;drawVictory._t=begin;HL10.events=[];
   const stream=cv.captureStream(30);for(const track of window.__bofMovieMix.__bofMovie.stream.getAudioTracks())stream.addTrack(track);
   const audioTracks=stream.getAudioTracks().length,rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp9',videoBitsPerSecond:2800000}),chunks=[],samples=[],start=performance.now();let lastPhase='';
   rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};const done=new Promise(r=>rec.onstop=()=>{const f=new FileReader();f.onload=()=>r(f.result.split(',')[1]);f.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});rec.start(500);
   await new Promise(resolve=>{const timer=setInterval(()=>{loop(performance.now());const s=HL10.last,phase=drawVictory._t>=VICTORY_WARNING_AT?'command':HL10.transition?.phase==='survivor'?'survivor-'+SV10.last?.phase:s?.phase;
    if(phase&&phase!==lastPhase){lastPhase=phase;samples.push({time:drawVictory._t,phase,ship:s?.ship,actor:s?.actor,camera:s?.camera,png:cv.toDataURL()});}
    if(drawVictory._t>=end||(performance.now()-start)>(end-begin+8)*1000){clearInterval(timer);resolve();}
   },1000/60);});rec.stop();const movie=await done;stream.getTracks().forEach(t=>t.stop());return{movie,samples,seconds:(performance.now()-start)/1000,startingTime:begin,endingTime:drawVictory._t,events:HL10.events,survivorEvents:SV10.events,audioTracks};
  }""",dict(begin=BEGIN,end=END))
  (OUT/'homecoming.webm').write_bytes(base64.b64decode(data.pop('movie')))
  for sample in data['samples']:(OUT/('record-'+sample['phase']+'.png')).write_bytes(base64.b64decode(sample.pop('png').split(',')[1]))
  data['errors']=errors;data['note']='Actual engine canvas/clock and original WebAudio master-bus sound cues; background music disabled for review.'
  (OUT/'recording-report.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');br.close()
finally:stop()
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-i',str(OUT/'homecoming.webm'),'-vf','pad=ceil(iw/2)*2:ceil(ih/2)*2','-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',str(OUT/'homecoming.mp4')],check=True)
print(json.dumps(dict(seconds=data['seconds'],endingTime=data['endingTime'],phases=[s['phase'] for s in data['samples']],errors=errors)),flush=True)
sys.exit(1 if errors or data['endingTime']<END or data['audioTracks']<1 else 0)
