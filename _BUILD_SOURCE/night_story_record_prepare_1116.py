from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'_BUILD_SOURCE/record_stage3_talking_1114.py').read_text(encoding='utf8')
s=s.replace("OUT=ROOT/'_shots/stage3_talking_1114'","OUT=ROOT/'_shots/cinema_overnight_1116/stage3-current';OUT.mkdir(parents=True,exist_ok=True)")
s=s.replace("p.set_default_timeout(240000)","p.set_default_timeout(480000)")
s=s.replace("run.pilot='cole';", "BOFOnline.submitScore=()=>{};run.pilot='cole';")
s=s.replace("part==='arrival'?state===GS.PLAY", "part==='arrival'?state===GS.PLAY")
# Allow current complete-text reading holds to finish without the old170s film cap.
s=s.replace("report={'pilot'", "RECORD=RECORD.replace('(now-start)>170000','(now-start)>360000')\nreport={'pilot'")
(R/'_BUILD_SOURCE/night_story_record_1116.py').write_text(s,encoding='utf8',newline='\n')
