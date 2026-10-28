from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>5');p.evaluate(shoot.TRAP_RAF)
  result=p.evaluate('''()=>{
   diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer',name:'CHRONOS'},{pilot:'cole'});warnT=0;spawnBoss('chromehammer');const b=boss,h=b._hammer;
   BOFCinematicDirector.cancel();HT23.speech.length=0;HT23.events.length=0;h.openingJump1003=true;h.state='warn';const refused=fr27BeginArmor(b);
   const declined={result:refused,queued:HT23.speech.length,events:HT23.events.length,state:h.state};h.openingJump1003=false;const accepted=fr27BeginArmor(b);
   const real={result:!!accepted,queued:HT23.speech.length,events:HT23.events.length,state:h.state,text:HT23.speech[0]?.text};
   // These are isolated regression fixtures, never used by the recording bot.
   h.chainDestroyed=true;h.chainHP=0;h.mode='chaingun';h.arsenalStep=0;const hp=b.hp;hammerChainStart(b);const rest={state:h.state,hp:b.hp,broken:h.chainDestroyed,gunHP:h.chainHP};
   h.state='chaingun';h.t=100;h.chainDir=0;b._noHit=false;h.frArmor.hp=0;h.frArmor.checkpoints=[.75,.50,.35];b.hp=b.maxhp*.07;
   const checkpointHP=b.hp;hammerBossTick(b,1/60);const checkpoint={state:h.state,hp:b.hp,expectedHP:checkpointHP,broken:h.chainDestroyed};
   return{declined,real,rest,checkpoint,checks:{declinedDoesNotSpeak:refused===null&&declined.queued===0&&declined.events===0,realSpeaksOnce:!!accepted&&real.state==='fr_activation'&&real.queued===1&&real.text==='Chromium Armor, Activated!',brokenGunRests:rest.state==='chain_cool'&&rest.hp===hp&&rest.broken&&rest.gunHP===0,furiousCheckpointPreserved:checkpoint.state==='fr_twirl'&&checkpoint.hp===checkpointHP}};
  }''')
  result['pageErrors']=errors;result['pass']=all(result['checks'].values())and not errors;(W/'native-regression.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));b.close()
finally:stop()
