from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'assets/game.js';s=p.read_text(encoding='utf-8')
def replace(a,b,count=1):
    global s
    if s.count(a)!=count:raise ValueError((a[:90],s.count(a),count))
    s=s.replace(a,b)
replace('stageTimer+=dt*timeScale','stageTimer+=dt')
replace('stageTimer-=dt*timeScale','stageTimer-=dt')
replace('if(boss && !_tslow) updateBoss(dt);','if(boss && (!_tslow || boss.enter || (boss._ovIntro&&!boss._ovIntro.done))) updateBoss(dt);')
replace("if(!bossWarned && stageTimer>=curStage.length && enemies.length<=7", "if(!bossWarned && stageTimer>=curStage.length && (run.stage!==1||typeof damAssaultReady1002!=='function'||damAssaultReady1002()) && enemies.length<=7")
replace("p.kind!=='mcrate'&&p.kind!=='hqspacebox')) continue;", "p.kind!=='mcrate'&&p.kind!=='hqspacebox'&&!/^missileupbox_(super|ultra|uber)$/.test(p.kind))) continue;")
# Direct beams and projectiles share the same impact/audio dispatch for destructible ordnance.
replace("if(b.dead) continue;\n    }\n    if(b.kind==='omegawarhead')", "if(b.dead){if(typeof ordnanceBreak1002==='function')ordnanceBreak1002(b);continue;}\n    }\n    if(b.kind==='omegawarhead')")
replace('const allW=WEAPONS.map((_,i)=>i),elements=Object.keys(INFUSIONS),visible=1;', 'const allW=WEAPONS.map((_,i)=>i),elements=forgeDiscovered(),visible=1;')
replace("{type:'golem',fx:.50}","{type:'firejet1002',fx:.50}")
replace("function hammerStormFloorY(){return PLAY.y+PLAY.h-76;}","function hammerStormFloorY(){return PLAY.y+PLAY.h-6;}")
replace('height:VH*.75,started:false','height:PLAY.h,started:false')
replace("if(h.state==='whirlwind'||h.state==='whirl_turn'){", "if(h.state==='whirlwind'){")
temp=R/'_shots/game_feedback_1002.tmp'
temp.write_text(s,encoding='utf-8',newline='\n')
temp.replace(p)
idx=R/'index.html';h=idx.read_text(encoding='utf-8');needle='<script src="assets/feedback_1001b.js"></script>'
if needle not in h:raise ValueError('index anchor')
h=h.replace(needle,needle+'\n<script src="assets/feedback_art_1002.js"></script>\n<script src="assets/feedback_1002.js"></script>')
idx.write_text(h,encoding='utf-8',newline='\r\n')
print('Applied October 2 core fixes (LF)')
