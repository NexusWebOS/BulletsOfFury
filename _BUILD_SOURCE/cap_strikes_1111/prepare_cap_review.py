from pathlib import Path
import textwrap

W=Path(__file__).resolve().parent
capture=(W/'capture_hammers.py').read_text()
start=capture.index('   p.evaluate("()=>{const hold=Input.hold;')
end=capture.index('\n  br.close()',start)
body=textwrap.dedent(capture[start:end])
body=body.replace('behind-head overheads / forward gaze','square end-cap strikes')
body=body.replace("'ba119_corrupt-empty_regular'", "'ba119_corrupt-empty_regular'")
prefix=capture[:capture.index('errors=[];records=[];contracts=[];')]
prefix=prefix.replace("O=Path(__file__).resolve().parent.parent/'outputs'", "O=Path(__file__).resolve().parent.parent/'outputs/End-cap-strikes'")
prefix+='\nff=imageio_ffmpeg.get_ffmpeg_exe()\n'
function='def record_loaded(p,stage,errors):\n unit="chronos" if stage==5 else "dracodia"\n records=[];contracts=[]\n'+textwrap.indent(body,' ')+'\n'
(W/'record_loaded.py').write_text(prefix+function)
for stage in ['5','8']:
 source=(W/('verify_stage'+stage+'.py')).read_text()
 source=source.replace("O=W.parent/'outputs'/('verification-stage'+sys.argv[1])", "O=W.parent/'outputs/End-cap-strikes'/('verification-stage'+sys.argv[1])")
 marker="  ck('No browser or renderer exceptions'"
 source=source.replace(marker,"  from record_loaded import record_loaded\n  record_loaded(p,"+stage+",errors)\n"+marker)
 (W/('verify_caps_stage'+stage+'.py')).write_text(source)
print('Prepared one isolated loaded session per boss for native checks and recording.')
