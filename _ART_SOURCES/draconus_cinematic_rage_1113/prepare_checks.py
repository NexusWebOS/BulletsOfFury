from pathlib import Path
W=Path(__file__).resolve().parent;old=W.parent/'draconus_front_rage_1113'
s=(old/'verify.py').read_text().replace("outputs/Draconus-frontal-and-rage","outputs/Draconus-new-rage")
s=s.replace('Q.action=null;Q.rf1110=null;', 'Q.action=null;Q.rf1110=null;Q.rf1110Rings=null;')
s=s.replace("O=W.parents[1]/'outputs/Draconus-new-rage';sys.path", "O=W.parents[1]/'outputs/Draconus-new-rage';O.mkdir(exist_ok=True);sys.path")
extra='''
  # Exercise the real armor transition before inspecting its actual center hit.
  q=p.evaluate("""()=>{seed13('regular');hb20Start(B,'armor');const A=Q.action;for(let i=0;i<600&&Q.action===A;i++)v19NativeTick(B,1/60);Q._td1111Next=0;hb20Start(B,'skystrike');const rows=[];for(const u of [.55,.65,.75,.85,.95,1,1.10]){Q.action.t=Q.action.tell+u;ba119Root(B,Q.action);const a=hb20Pose(B).a;rows.push({u,source:a.sourceCell,frame:a.frame,tip:a.tip,head:a.headCenter,grip:a.grip,bank:a.bank});}return{chrome:Q.chrome,rows};}""")
  contacts=[r for r in q['rows']if r['u']>=1]
  ck('Actual armor activation leads to a centered rigid cap strike below both hands',q['chrome']and all(abs(r['tip'][0]-256)<12 and r['head'][1]>r['grip'][1]+30 for r in contacts),q)
  down=[r for r in q['rows']if .55<=r['u']<=1]
  ck('Chromium hammer visibly descends on the centerline over a broad vertical arc',max(r['tip'][0]for r in down)-min(r['tip'][0]for r in down)<16 and down[-1]['tip'][1]-down[0]['tip'][1]>150,down)
  for u,label in [(.55,'lift'),(.75,'descending'),(1,'ground-contact')]:
   p.evaluate('u=>{Q.action.t=Q.action.tell+u;ba119Root(B,Q.action);}',u);shot(p,'chrome-new-center-'+label)
  # Native action/phase owners, with actual two-handed artwork and sockets.
  p.evaluate("seed13('chrome');hb20Start(B,'rage');")
  for t,label in [(1.32,'stop'),(1.70,'recoup'),(3.5,'charge'),(5.9,'red-release')]:
   q=p.evaluate('t=>{Q.action.t=t;Q.speech=null;const a=hb20Pose(B).a;return{bank:a.bank,frame:a.frame};}',t);shot(p,'new-rage-'+label)
  q=p.evaluate("""()=>{const out=[];for(const scale of [1,.42])for(const phase of ['kame_charge','kame_thrust','kame_fire','kame_recover','gather','thrust','beam']){const R={phase,t:phase.includes('thrust')?.22:phase.includes('charge')?1.8:.35,scale};const a=rf1110CastPose('drac',R).a,at=rf1110DracHands(B,R),release=rf1110DracHands(B,R,true);out.push({phase,scale,frame:a.frame,bank:a.bank,socketError:Math.hypot(at.x-(B.x+a.ball[0]-a.pivot[0]),at.y-(B.y+a.ball[1]-a.pivot[1])),release});}return out;}""")
  ck('Both depth variants gather, thrust both hands, sustain and recover with registered ball sockets',all(r['bank'].startswith('cast_')and r['socketError']<.001 for r in q)and all(3<=r['frame']<=6 for r in q if r['phase']=='kame_charge')and all(7<=r['frame']<=12 for r in q if r['phase']in ['kame_thrust','thrust'])and all(r['frame']in[12,13]for r in q if r['phase']in ['beam','kame_fire']),q)
  p.evaluate("seed13('chrome');hb20Start(B,'rage');rf1110DracStart(B);Q.speech=null;Q.rf1110.scale=1;Q.rf1110.phase='kame_charge';Q.rf1110.t=1.8;B.x=worldWidth()/2;B.y=viewTopY()+190;B.flash=0;");shot(p,'new-two-hand-gather-foreground')
  for phase,t,label in [('kame_thrust',.20,'thrust'),('kame_fire',.35,'wave')]:
   p.evaluate('([phase,t])=>{Q.rf1110.phase=phase;Q.rf1110.t=t;}',[phase,t]);shot(p,'new-two-hand-'+label+'-foreground')
  ck('New actor draw routes have no native renderer errors',not errors,errors)
'''
s=s.replace("ck('No native page/update/draw errors',not errors,errors);br.close()", "ck('No native page/update/draw errors',not errors,errors)"+extra+"\n  br.close()")
s=s.replace("R/'assets/draconus_front_rage_1113.js'","R/'assets/draconus_cinematic_rage_1113.js'")
(W/'verify.py').write_text(s)
checks=(old/'checks.py').read_text().replace('frontal-rage-syntax','cinematic-rage-syntax').replace('assets/draconus_front_rage_1113.js','assets/draconus_cinematic_rage_1113.js')
(W/'checks.py').write_text(checks)
print('Prepared native combat regression, real armor/center trajectory, and two-hand socket checks.')
