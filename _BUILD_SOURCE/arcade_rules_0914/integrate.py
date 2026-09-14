from pathlib import Path
import hashlib,sys
R=Path(__file__).resolve().parents[2];O=R/'_shots/arcade_rules_0914';p=R/'assets/game.js';current=p.read_bytes();b=(O/'game.before.js').read_bytes()if(O/'game.before.js').exists()else current
assert hashlib.sha256(b).hexdigest()=='3e8159683cba3b65b344244e50de5ee300e0f7371e2119eb5b30bd9511a14212'
if not(O/'game.before.js').exists():
 (O/'game.before.js').write_bytes(b);(O/'test.before.js').write_bytes((R/'_BUILD_SOURCE/test_fl.js').read_bytes())
s=b.decode('utf-8')
def edit(a,z):
 global s
 assert s.count(a)==1,(a[:100],s.count(a));s=s.replace(a,z)
edit("let DIFF = DIFFS.normal;", """let DIFF = DIFFS.normal;
/* Mike 0914: Arcade credits belong to the entire run. A continue restores the
   selected starting stock. Keep campaign/co-op tuning separate and never mutate DIFFS. */
const ARCADE_STOCK = {easy:{lives:7,continues:7},normal:{lives:5,continues:5},hard:{lives:3,continues:3},furious:{lives:3,continues:1}};
function difficultyForRun(mode,key){
  const base=DIFFS[key]||DIFFS.normal,stock=ARCADE_STOCK[key]||ARCADE_STOCK.normal;
  return mode==='arcade'?Object.assign({},base,{startLives:stock.lives,contLives:stock.lives,continues:stock.continues}):base;
}
function continueCap(){
  return run.stage===9&&run.mode!=='arcade'
    ? (DIFF.continues>=0?Math.min(DIFF.continues, STAGE9_CONTINUES):STAGE9_CONTINUES)
    : DIFF.continues;
}""")
edit("  DIFF=DIFFS[diffKey]||DIFFS.normal;\n",'')
edit("  run.lives=DIFF.startLives; run.bombs=DIFF.startBombs;", "  DIFF=difficultyForRun(run.mode,diffKey);\n  run.lives=DIFF.startLives; run.bombs=DIFF.startBombs;")
edit("  if(s.diff) diffKey=s.diff;", "  if(s.diff) diffKey=s.diff;\n  DIFF=difficultyForRun(run.mode,diffKey);")
edit("  if(run.stage===9&&!bossDefeated&&typeof riftFallbackStart==='function')", "  if(run.stage===9&&run.mode!=='arcade'&&!bossDefeated&&typeof riftFallbackStart==='function')")
edit("function riftFallbackStart(){\n  if(state===GS.RIFTFALLBACK)return;", "function riftFallbackStart(){\n  // Arcade never refunds a spent credit bank through the campaign rift retreat.\n  if(run.mode==='arcade'){triggerGameOver();return;}\n  if(state===GS.RIFTFALLBACK)return;")
a=s.index('    /* CONTINUES ARE CAPPED PER DIFFICULTY',s.index('function drawContinue(dt)'))
z=s.index('    if(_capNow>=0',a)
s=s[:a]+"    // Campaign keeps its rift limit; Arcade spends one shared bank across every stage.\n    const _capNow = continueCap();\n"+s[z:]
edit("      if(run.stage===9){riftFallbackStart();return;}\n      setState(GS.GAMEOVER); return;", "      triggerGameOver(); return;")
# Preserve the authored difficulty buttons; derive their descriptions from actual runtime stocks.
a=s.index('const DIFF_DESC=');z=s.index('\nfunction scrollSpaceBG',a)
s=s[:a]+"""const DIFF_DESC=['SLOWER ENEMIES / MORE DROPS','STANDARD FURY','FASTER / TOUGHER / FEWER DROPS','RELENTLESS / NO MERCY'];
function difficultyDescription(i){
  i=clamp(i,0,DIFF_KEYS.length-1);const d=difficultyForRun(run.mode,DIFF_KEYS[i]);
  return d.startLives+' '+(d.startLives===1?'LIFE':'LIVES')+' \\u00B7 '+
    (d.continues<0?'UNLIMITED CONTINUES':d.continues+' '+(d.continues===1?'CONTINUE':'CONTINUES'))+' \\u00B7 '+DIFF_DESC[i];
}"""+s[z:]
edit('const desc=DIFF_DESC[clamp(menuIndex,0,N-1)];','const desc=difficultyDescription(menuIndex);')
edit("  if(stateT>0.3 && Math.floor(stateT*2)%2){ ctx.textAlign='center';", """  if(run.mode==='arcade'){
    const left=Math.max(0,continueCap()-(run.contUsed||0));
    const label=left+' '+(left===1?'CONTINUE':'CONTINUES')+' REMAINING';
    if(artReady(art))stageText(art,label,VW/2,VH*.84,13,null,null,1,.055);
    else {ctx.textAlign='center';ctx.fillStyle='#eaf2ff';ctx.font='13px "BOFmil", monospace';ctx.fillText(label,VW/2,VH*.84);}
  }
  if(stateT>0.3 && Math.floor(stateT*2)%2){ ctx.textAlign='center';""")
x=s.encode('utf-8');assert b'\r\n'not in x;assert current in[b,x]
if '--dry-run'not in sys.argv:p.write_bytes(x)
(O/'game.expected.js').write_bytes(x)
print(hashlib.sha256(x).hexdigest())
