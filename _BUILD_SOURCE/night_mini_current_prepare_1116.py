from pathlib import Path
R=Path(__file__).resolve().parents[1];s=(R/'_BUILD_SOURCE/night_diagnostic_1116.py').read_text(encoding='utf8')
s=s.replace("'_shots/cinema_overnight_1116/native-diagnostic'","'_shots/cinema_overnight_1116/native-mini-current'")
s=s.replace("debugFightFor(cfg.stage,'boss')","debugFightFor(cfg.stage,'mini')").replace('const b=bossActive&&boss&&!boss.dead?boss:null;','const b=subBossActive&&subBoss&&!subBoss.dead?subBoss:null;')
s=s.replace('let list=b?retinaBossTargets(b).filter',"let list=b?_lockTargets().filter(t=>t===b||t._retinaOwner===b).filter")
s=s.replace('const b=boss,S=b?._r30','const b=subBoss,S=b?._r30').replace('dead:!!b?.dead,bossDefeated,active:bossActive,','dead:!!b?.dead,bossDefeated:subBossDone,active:subBossActive,')
s=s.replace(' / FURIOUS / COLE / INVULNERABLE INPUT BOT',' / FURIOUS MINIBOSS / COLE / INVULNERABLE INPUT BOT').replace("report = {'stage': stage, 'difficulty': 'furious', 'pilot': 'cole',","report = {'stage': stage, 'role':'mini', 'difficulty': 'furious', 'pilot': 'cole',")
(R/'_BUILD_SOURCE/night_mini_current_1116.py').write_text(s,encoding='utf8',newline='\n');print('Prepared current-origin whole Dredger fixture without enemy HP or phase writes')
