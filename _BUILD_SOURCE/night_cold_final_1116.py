from pathlib import Path
R=Path(__file__).resolve().parents[1];s=(R/'_BUILD_SOURCE/night_cold_boot_1116.py').read_text()
s=s.replace("p.on('pageerror'", "p.on('response',lambda r:errors.append(str(r.status)+' '+urlsplit(r.url).path)if r.status>=400 else None);p.on('pageerror'")
s=s.replace("row={'context':n,", "expected=[q for q in failed if q['failure']=='net::ERR_ABORTED' and Path(q['path']).suffix.lower()in['.mp3','.wav','.ogg','.m4a','.webm'] and (R/q['path'].lstrip('/')).exists()];hard=[q for q in failed if q not in expected]\n   row={'expectedAudioPreloadCancellations':expected,'hardFailed':hard,'context':n,")
s=s.replace("'ok':not errors and not failed", "'ok':not errors and not hard")
(R/'_BUILD_SOURCE/night_cold_final_1116.py').write_text(s,encoding='utf8',newline='\n')
