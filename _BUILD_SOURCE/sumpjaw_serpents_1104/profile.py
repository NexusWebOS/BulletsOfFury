from pathlib import Path
import sys
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');s=R/'_BUILD_SOURCE/furious_perf_1104/profile.py'
text=s.read_text().replace("R=Path(__file__).resolve().parents[2]",'R=Path('+repr(str(R))+')').replace("W=R/'_shots/furious_perf_1104'",'W=Path('+repr(str(W/'profile'))+')')
(W/'profile').mkdir(exist_ok=True)
text=text.replace('run.stage=6','run.stage=7').replace('stage:6','stage:7').replace("kind:'razorwake',name:'RAZORWAKE'","kind:'dualscoopdredger',name:'SUMPJAW'").replace("spawnSubBoss('razorwake')","spawnSubBoss('dualscoopdredger')").replace('stageLoadBegin(6)','stageLoadBegin(7)').replace('fb112Ready()&&stageLoadReady(6)','sj98Ready()&&stageLoadReady(7)')
text=text.replace("['fb112Draw','fb112Blit','fb112Cell','fb112Opaque','fb112Shadow','fb112Ready','fb112Tick','updatePlay','drawWorld']","['ss116Blit','ss116Segments','sj98Tick','sj98Draw','updatePlay','drawWorld']")
sys.argv=[str(s),'--label','uncaptured-sumpjaw','--seconds','40'];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
exec(compile(text,str(s),'exec'),{'__file__':str(s),'__name__':'__main__'})
