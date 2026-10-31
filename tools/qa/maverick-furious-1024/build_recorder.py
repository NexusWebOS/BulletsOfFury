from pathlib import Path
W=Path(__file__).resolve().parent
B=W/'capture_base.js'
if not B.exists():B=W.parent/'BOF-Furious-Bot-1023/furious_bot.js'
s=B.read_text(encoding='utf-8')
s=s[s.index('window.FURYBOT='):]
a=s.index('playerHit=function(source)');b=s.index('if(window.BOFOnline)',a)
s=s[:a]+s[b:]
a=s.index('FURYBOT.start=');b=s.index(' // A disclosed normal weapon loadout',a)
s=s[:a]+'''FURYBOT.start=async function(c){this.config=c;
 const audio=await this.audio();
 diffKey='furious';run.mode='campaign';pilotIndex=PILOTS.findIndex(p=>p.key==='maverick');
 debugUnlocked=true;DBGT.god=false;DBGT.hud=false;DBGT.speed=1;
 startRun(1);
'''+s[b:]
a=s.index(' // A disclosed normal weapon loadout');b=s.index(' this.geom=',a)
s=s[:a]+''' this.loadout={pilot:run.pilot,diff:diffKey,mode:run.mode,weapon:run.weapon,level:run.wlevel,bombs:run.bombs,grants:[]};
'''+s[b:]
s=s.replace('videoBitsPerSecond:4000000','videoBitsPerSecond:3000000')
a=s.index('FURYBOT.post=');b=s.index('FURYBOT.paint=',a)
s=s[:a]+s[b:]
s+='\n'+(W/'campaign_controller.js').read_text(encoding='utf-8')+'\n'+(W/'audio_capture.js').read_text(encoding='utf-8')
s=s.replace('this.chunks.push(e.data);','')
(W/'campaign_bot.js').write_text(s,encoding='utf-8')
print('Built native campaign recorder')
