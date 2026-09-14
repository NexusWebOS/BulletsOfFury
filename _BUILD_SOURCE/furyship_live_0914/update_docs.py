from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];D=R/'docs';p=D/'REQUEST_CHECKLIST_0914.json';data=json.loads(p.read_text(encoding='utf-8'))
updates={
 'SPACE-12':('partial','New ship integrated: six parts with 30 views, eight roll poses and twelve somersault poses; approved frame 13 is the level-flight hull. Remaining: generated silhouette/wingspan drift, exact part fit and smoother intermediate component turns.'),
 'SPACE-13':('complete','Assembly energy, sky-space curtain, travelling seam effect, speed streaks and anchored thrusters integrated. Reusable authored effect helper uses simulation time; native transformation and evasion video verified.'),
 'SPACE-14':('complete','All nine pilot palettes integrated across ship and components; new flight, Stage 9 and space death rendering verified. SPCBOY selects the preserved original ship and campaign snapshots save/restore that selection.')}
for x in data['items']:
 if x['id']in updates:
  x['status'],x['request']=updates[x['id']];x['evidence']='FURYSHIP_LIVE_0914.md';x['dependency']=''
data['latestBatch']={'description':'Installed the Furyship replacement, component assembly, both rolls and 12-frame somersault, transition/speed effects, all nine palettes and the SPCBOY legacy option. Native Chromium 26/0; full suite 3,849/61 (exit 1, all failures match baseline); 26-second in-game video with sound. Frame consistency remains open under SPACE-12.','evidence':'FURYSHIP_LIVE_0914.md','completed':['SPACE-13','SPACE-14']}
p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
note='''

## Codex update — September 14: Furyship installed in the game

Read docs/FURYSHIP_LIVE_0914.md and docs/qa/furyship_live_0914.json. The approved frame-13 hull, six-part assembly, 12 somersault poses, both eight-frame rolls, transition/speed effects and all nine palettes now run in the game. SPCBOY selects the preserved original fighter; campaign snapshots save/restore the selection. New cannon anchors and space death/Stage 9 rendering verified. Sources _BUILD_SOURCE/furyship_live_0914; no atlas repack or shipping-manifest changes in this batch.

Native Chromium 26/0, no page/console/loop errors. Full suite 3,849 passed / 61 failed, exit 1, final summary reached; failure names exactly match docs/qa/supply_audit_0914.json. Section309 10/0; two older replacement-sensitive assertions updated with separate legacy checks. Runtime SHA256 3fc67f9238c635ee3367f574a2a57bd2a1094ffadcf52aae1b7e76de59a02e45. LF/CRLF preserved.

Video: _shots/furyship_live_0914/video/BulletsOfFury_Furyship_0914.mp4 (26 seconds, actual game sound events, export gain prevents clipping, full decode passed). Capture skips completed HQ dialogue/entrance and uses fixture-only invincibility; this is not a full balance run. SPACE-13/14 complete; SPACE-12 partial for wingspan/silhouette drift and smoother component turns/fit. Tally 135: 51 complete / 11 partial / 73 pending, 84 unfinished. Preserve docs/WORK_ORDER_0914.md; the larger encounter requests are still open. No commits/pushes/deletion/background automation.
'''
for p in [R/'CLAUDE.md',R/'HANDOFF_CODEX.md']:
 b=p.read_bytes()
 if '## Codex update — September 14: Furyship installed in the game'.encode('utf-8')not in b:
  newline='\r\n'if b'\r\n'in b else'\n';p.write_bytes(b+note.replace('\n',newline).encode('utf-8'))
for name in ['FURYSHIP_ASSETS_0914.md','FURYSHIP_SOMERSAULT_0914.md']:
 p=D/name;s=p.read_text(encoding='utf-8')
 follow='\n\n## Later integration update\n\nThe candidate-only status above records the earlier asset pass. The ship and effects are now installed; see [FURYSHIP_LIVE_0914.md](FURYSHIP_LIVE_0914.md) for native verification, the in-game video and remaining animation refinement.\n'
 if '## Later integration update'not in s:p.write_text(s+follow,encoding='utf-8')
