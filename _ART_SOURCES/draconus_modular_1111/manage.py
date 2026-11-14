from pathlib import Path
import subprocess,sys
W=Path(__file__).resolve().parent
scripts={'--export':'export.py','--build':'build.py','--install':'install.py','--verify':'verify.py','--preflight':'preflight.py','--sources':'prepare_sources.py','--finish':'finish.py','--diagnose':'status.py','--retry-7':'retry_stage7.py',**{'--record-'+str(n):'record.py'for n in range(5,9)}}
scripts['--dump']='dump_record.py'
scripts['--retry-8']='retry_stage8.py'
scripts['--repair-stage8']='repair_stage8.py'
scripts['--verify-repair']='verify_stage8_repair.py'
scripts['--retry-8-repaired']='retry_stage8_after_repair.py'
scripts['--inspect-record']='inspect_record.py'
scripts['--tidy-incomplete']='tidy_incomplete.py'
if len(sys.argv)!=2 or sys.argv[1]not in scripts:raise SystemExit('Choose a task export, build, install, verification, recording, or finalization step.')
job=scripts[sys.argv[1]];args=[sys.executable,str(W/job)]
if sys.argv[1].startswith('--record-'):args.append(sys.argv[1][-1])
subprocess.run(args,check=True)
