from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'_BUILD_SOURCE/record_furious_789_1025.py').read_text(encoding='utf8')
s=s.replace("OUT = ROOT / '_shots' / 'furious_789_1025'","OUT = ROOT / '_shots/cinema_overnight_1116/native-boss'")
start=s.index(' const gain=audio.createGain();')
end=s.index(" const canvas=document.createElement('canvas');",start)
s=s[:start]+''' aq112Bus().output.connect(analyser);analyser.connect(mix);
 const stats=window.captureStats={peak:0,tapped:1,playing:{},tapErrors:[],frames:0};
 BOFOnline.submitScore=()=>{};
'''+s[end:]
s=s.replace("'twins:F?'", "'twins:F?'")
s=s.replace('twins:F?', "dracodia:J?{pools:{...J.hp},locked:typeof rd30Locked==='function'&&rd30Locked(b),attacks:J.attacks,book:S.v18?.seq,unlocked:J.rd30?.unlocked}:null,twins:F?")
s=s.replace("'method': 'Native boss-mode entry, real RAF, input-only aiming; no enemy HP/phase writes.'", "'method': 'Native boss-mode entry, real RAF, input-only aiming and native GOD. Current shared mixer audio. No enemy HP/phase/timer writes. This is a protected bot stress run, not human balance or a campaign win.'")
(R/'_BUILD_SOURCE/night_full_boss_1116.py').write_text(s,encoding='utf8',newline='\n')
print('Prepared current-mixer native-input stress recording')
