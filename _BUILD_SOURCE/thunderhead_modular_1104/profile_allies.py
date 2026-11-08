from pathlib import Path
import sys
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');s=R/'_BUILD_SOURCE/furious_perf_1104/profile.py'
text=s.read_text().replace("R=Path(__file__).resolve().parents[2]",'R=Path('+repr(str(R))+')').replace("W=R/'_shots/furious_perf_1104'",'W=Path('+repr(str(W/'profile'))+')').replace("role:'mini',kind:'razorwake',name:'RAZORWAKE'","role:'boss',kind:'thunderhead',name:'THUNDERHEAD'").replace("spawnSubBoss('razorwake')","spawnBoss('thunderhead')").replace('window.B=subBoss','window.B=boss').replace('const q=subBoss?._fb112','const q=boss?._fb112').replace("'fb112Draw','fb112Blit'","'tm115Bank','tm115Aura','tm115Mask','th114Blit','th114Weather','th114RoundDraw','fb112Draw','fb112Blit'")
text=text.replace("if(s6Wing)Object.assign(s6Wing,{","s6WingLaunch(8,true);if(s6Wing)Object.assign(s6Wing,{")
sys.argv=[str(s),'--label',sys.argv[1]if len(sys.argv)>1 else'modular-allies','--seconds','55'];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
exec(compile(text,str(s),'exec'),{'__file__':str(s),'__name__':'__main__'})
