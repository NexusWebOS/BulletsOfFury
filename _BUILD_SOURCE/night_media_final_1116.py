from pathlib import Path
import subprocess,json,re
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116';ff=imageio_ffmpeg.get_ffmpeg_exe();rows=[]
q=json.loads((R/'docs/qa/cinema_overnight_1116.json').read_text())
for item in q['clips']:
 p=O/item['file'];meta=subprocess.run([ff,'-hide_banner','-i',str(p)],capture_output=True,text=True,errors='replace').stderr;m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',meta);duration=sum(float(a)*b for a,b in zip(m.groups(),[3600,60,1]))if m else None
 if not duration:raise RuntimeError('No decoded duration '+str(p))
 sample=subprocess.run([ff,'-hide_banner','-ss',str(duration*.5),'-i',str(p),'-t','2','-map','0:a:0','-af','astats=metadata=0:reset=0','-f','null','-'],capture_output=True,text=True,errors='replace',timeout=45)
 peaks=re.findall(r'Peak level dB: ([-\w.]+)',sample.stderr);peak=float(peaks[-1])if peaks else float('-inf');has_audio='Audio:'in meta;row={'file':item['file'],'duration':duration,'audio':has_audio,'sampleDecodeExit':sample.returncode,'midpointPeakDb':peak if peak!=float('-inf')else None,'ok':sample.returncode==0 and has_audio and peak> -90};rows.append(row);print(json.dumps(row),flush=True)
 (O/'media-final.json').write_text(json.dumps({'rows':rows,'scope':'FFmpeg container metadata and a2-second decoded midpoint native-audio sample from each review film. This verifies encoded audio exists and is non-silent; it does not certify every cue or target-hardware playback.'},indent=2),encoding='utf8')
assert all(q['ok']for q in rows)
