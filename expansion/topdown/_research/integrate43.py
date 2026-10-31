from pathlib import Path
import shutil,hashlib,json,wave
W=Path(__file__).parent;G=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');B=G/'expansion/topdown';stamp='overdrive1018-gosfar43-r1'
def edit(p,old,new):
 s=p.read_text(encoding='utf-8');assert old in s,(p,old[:80]);p.write_text(s.replace(old,new),encoding='utf-8',newline='')
shutil.copy2(W/'gosfar43.js',B/'js/gosfar43.js')
main=B/'js/main.js'
s=main.read_text()
if '!MISSION.exclusiveWhen' not in s:edit(main,'if(MISSION.exclusiveStep){','if(MISSION.exclusiveStep&&(!MISSION.exclusiveWhen||MISSION.exclusiveWhen(G))){')
s=main.read_text()
if 'G.gosfar43=null;' not in s:edit(main,'G.escape29=null;', 'G.gosfar43=null; G.escape29=null;')
level=B/'js/level36.js';s=level.read_text()
if 'if(!TD.Gosfar43)art.draw' not in s:edit(level,"art.draw(ctx,'l36_door_'+door", "if(!TD.Gosfar43)art.draw(ctx,'l36_door_'+door")
s=level.read_text()
if "flash:s.gosfarWall43?" not in s:edit(level,"{s:scale,flash:s.flash>0?1:0}","{s:scale,flash:s.gosfarWall43?Math.min(.52,(s.flash||0)*5):s.flash>0?1:0}")
s=(B/'js/audio_1011.js').read_text()
if "gosfar43:" not in s:edit(B/'js/audio_1011.js',"    lastHope:","    gosfar43: 'expansion/topdown/audio/music43/gosfar-last-hope.wav',\n    lastHope:")
s=(B/'js/audio_1011.js').read_text()
if "TD.Stealth.phase === 'ALERT') this.loop" in s:edit(B/'js/audio_1011.js',"TD.Stealth.phase === 'ALERT') this.loop", "TD.Stealth.phase === 'ALERT' && !G.gosfar43?.power) this.loop")
audio=B/'audio/music43';audio.mkdir(exist_ok=True)
src=Path(r'C:/Users/Mike/Downloads/rise_of_the_last_hope_fast_riff_genesis (2).wav');dst=audio/'gosfar-last-hope.wav';shutil.copy2(src,dst)
with wave.open(str(dst)) as f:meta={'file':dst.relative_to(G).as_posix(),'user_source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'duration':f.getnframes()/f.getframerate(),'channels':f.getnchannels(),'sample_rate':f.getframerate()}
(audio/'source.json').write_text(json.dumps(meta,indent=2))
index=B/'index.html';s=index.read_text()
if 'art/gosfar43/manifest.js' not in s:s=s.replace('<script src="audio/colesfx75/manifest.js',f'<script src="art/gosfar43/manifest.js?v={stamp}"></script>\n<script src="audio/colesfx75/manifest.js')
if "'gosfar43'" not in s:s=s.replace("'audio42', 'frontend_1011'","'audio42', 'gosfar43', 'frontend_1011'")
s=s.replace('overdrive1018-combat42-r5',stamp);index.write_text(s,encoding='utf-8',newline='')
for f in ['build_gosfar43.py','integrate43.py']:shutil.copy2(W/f,B/'_research'/f)
print(meta)
