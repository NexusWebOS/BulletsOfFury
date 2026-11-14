from pathlib import Path
W=Path(__file__).resolve().parent;OLD=W.parent/'solid_hammer_1111'
for stage in [5,8]:
 s=(OLD/f'verify_stage{stage}.py').read_text().replace('outputs/Solid-metal-hammers','outputs/Three-way-hammer')
 s=s.replace("q?.a.bank==='blue-overhead'","q?.a.bank?.startsWith('blue-overhead')")
 s=s.replace("q['bank']=='blue-overhead'","q['bank'].startswith('blue-overhead')")
 s=s.replace("activation['bank']=='blue-overhead'","activation['bank'].startswith('blue-overhead')")
 s=s.replace("activation['bank']=='ba119_corrupt-overhead_chrome'","activation['bank'].startswith('ba119_corrupt-overhead')and activation['bank'].endswith('_chrome')")
 s=s.replace('  from front_record_loaded import record_loaded',f'  from verify_three_way import run_three_way\n  run_three_way(p,{stage},ck,shot)\n  from front_record_loaded import record_loaded')
 (W/f'verify_stage{stage}.py').write_text(s)
s=(OLD/'front_record_loaded.py').read_text().split(' # Step the real native loop')[0].replace('outputs/Solid-metal-hammers','outputs/Three-way-hammer')
s+=' p.close()\n';(W/'front_record_loaded.py').write_text(s)
s=(OLD/'verify_password.py').read_text().replace('outputs/Solid-metal-hammers','outputs/Three-way-hammer').replace("r.get('bank')=='blue-overhead'","r.get('bank','').startswith('blue-overhead')")
(W/'verify_password.py').write_text(s)
print('Prepared existing native checks plus three-direction, four-form pixel probes.')
