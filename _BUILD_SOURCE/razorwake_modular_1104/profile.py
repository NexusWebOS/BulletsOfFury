from pathlib import Path
import sys
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');s=R/'_BUILD_SOURCE/furious_perf_1104/profile.py';(W/'profile').mkdir(exist_ok=True)
text=s.read_text().replace("R=Path(__file__).resolve().parents[2]",'R=Path('+repr(str(R))+')').replace("W=R/'_shots/furious_perf_1104'",'W=Path('+repr(str(W/'profile'))+')')
text=text.replace("['fb112Draw','fb112Blit','fb112Cell','fb112Opaque','fb112Shadow','fb112Ready','fb112Tick','updatePlay','drawWorld']","['rw117Blit','rw117Wings','rw117Mask','rw117Fields','rw117Weather','fb112Draw','fb112Tick','updatePlay','drawWorld']")
sys.argv=[str(s),'--label','modular-wind-cached','--seconds','40'];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
exec(compile(text,str(s),'exec'),{'__file__':str(s),'__name__':'__main__'})
