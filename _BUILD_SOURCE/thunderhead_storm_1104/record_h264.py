"""Native high-quality storm fight using browser-supported H264 capture.
Collect an honest CPU profile of the actual recording, including allies/bot.
"""
from pathlib import Path
import sys
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');source=R/'_BUILD_SOURCE/record_boss_comparison_1102.py';sys.path.insert(0,str(source.parent))
text=source.read_text().replace("demonstrate=35 if stage in [5,8]and role=='boss'else 27","demonstrate=45 if stage==6 and role=='boss'else 35 if stage in [5,8]and role=='boss'else 27")
text=text.replace("paths=['index.html']", "capture=capture.replace('codecs=vp8,opus','codecs=h264,opus')\npaths=['index.html']")
# Profiling changes the recorder only, never the game simulation.
text=text.replace("src=original.replace(","original=original.replace(\"print('START', stage, json.dumps(report['setup']), flush=True)\",\"print('START', stage, json.dumps(report['setup']), flush=True)\\n                cdp=page.context.new_cdp_session(page);cdp.send('Profiler.enable');cdp.send('Profiler.setSamplingInterval',{'interval':2000});cdp.send('Profiler.start')\").replace(\"page.screenshot(path=str(folder / 'final.png'))\",\"(folder/'capture.cpuprofile').write_text(json.dumps(cdp.send('Profiler.stop')['profile']));page.screenshot(path=str(folder / 'final.png'))\")\n src=original.replace(")
sys.argv=[str(source),'--difficulty','furious','--stages','6','--ids','stage6-boss','--track','thunderhead-storm-h264-1104','--capture-codec','vp8']
exec(compile(text,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
