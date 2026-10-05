"""Real Chromium: entry routes, eight visible forms, attacks, modules and finale reward.
Controlled fixtures, not a human campaign win or balance certification.
"""
from pathlib import Path
import json,sys,base64,http.server
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'_shots/finale_1003b';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
errors=[];report={'checks':[],'forms':[],'scope':'Real Chromium controlled encounters; human balance playtest still needed.'}
def ck(v,name):
 report['checks'].append({'ok':bool(v),'name':name});print(('OK ' if v else 'FAIL ')+name,flush=True)
def frames(p,n):
 for i in range(0,n,20):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);}}',min(20,n-i));p.wait_for_timeout(8)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
  p=browser.new_page(viewport={'width':1100,'height':950});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  # Intercept before rotation5 captures its bound native drawImage. The cached
  # rotation path bypasses a later ctx.drawImage wrapper; .src is not evidence.
  p.add_init_script('(()=>{const draw=CanvasRenderingContext2D.prototype.drawImage;CanvasRenderingContext2D.prototype.drawImage=function(){if(window.finalArtCalls&&window.finalArtKey&&typeof ctx!=="undefined"&&this===ctx)window.finalArtCalls.push(window.finalArtKey);return draw.apply(this,arguments);};})()')
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50);p.mouse.click(500,500)
  p.evaluate('()=>{r30Warm();mm1003Warm();er26Warm();window.nativeFinaleHit=playerHit;window.finaleSounds={};const sound=r30Sound;r30Sound=function(k){finaleSounds[k]=(finaleSounds[k]||0)+1;return sound.apply(this,arguments);};}')
  p.wait_for_function('()=>Object.values(FINALE1003B_ART).every(a=>XART.rdy(a.key))&&Object.values(S81003_ART).every(a=>XART.rdy(a.key))&&Object.keys(REALM30_ART).every(k=>XART.rdy("r30_"+k))',timeout=120000,polling=70)
  ck(p.evaluate('()=>Object.values(FINALE1003B_ART).every(a=>{const im=XART.get(a.key);return im.width===a.size[0]&&im.height===a.size[1];})'),'five generated transformation reels decode through XART')
  # Actual password entry path startRun, fresh profile unlock off, every pilot.
  for pilot in p.evaluate('()=>PILOTS.map(p=>p.key)'):
   q=p.evaluate('(pilot)=>{pilotIndex=PILOTS.findIndex(p=>p.key===pilot);chaingunUnlocked=false;diffKey="furious";startRun(7);BOFCinematicDirector.cancel();story=null;special=null;setState(GS.PLAY);player.invuln=0;player.dead=false;player.out=false;player.roll=null;player.somer=null;player._hammerEvap=false;player._eradicated=false;pBullets=[];pShoot();return {weapon:run.weapon,rounds:pBullets.filter(q=>q._chaingun).length,visible:chaingunMountsVisible(),load:run.loadout};}',pilot)
   ck(q['weapon']==7 and q['rounds']>0 and q['visible'],pilot+' password boot equips, fires and displays anchored chainguns')
  p.evaluate(SETUP,{'stage':7,'pilot':'yuri','diff':'furious'});p.evaluate('()=>{player.invuln=0;run.weapon=7;run.wlevel=3;run.wlevels[7]=3;window.mountCalls=[];const cell=repair30Cell,draw=ctx.drawImage;window.mountKey=null;repair30Cell=function(k){mountKey=k;try{return cell.apply(this,arguments);}finally{mountKey=null;}};ctx.drawImage=function(){if(mountKey)mountCalls.push(mountKey);return draw.apply(this,arguments);};drawWorld(0);ctx.drawImage=draw;repair30Cell=cell;}')
  p.wait_for_function('()=>XART.rdy("repair30_chaingun_mount_yuri_left")&&XART.rdy("repair30_chaingun_mount_yuri_right")&&XART.rdy("repair30_chaingun_barrel_top")',timeout=120000)
  shot(p,'yuri-chainguns');ck(p.evaluate('()=>mountCalls.includes("chaingun_mount_yuri_left")&&mountCalls.includes("chaingun_mount_yuri_right")'),'game context draws both Yuri authored wing mounts')
  p.evaluate('()=>{enemies=[];for(const wave of buildStagePlan(7))wave.fn();}');ck(p.evaluate('()=>!enemies.some(e=>["s7mine","s7canister"].includes(e.type))&&enemies.some(e=>e._mutatorSlot1003==="s7mine")&&enemies.some(e=>e._mutatorSlot1003==="s7canister")'),'sewer wave callbacks replace toxic pods')
  p.evaluate(SETUP,{'stage':7});p.evaluate('()=>{spawnEnemy("s7canister",player.x-78,145,{});spawnEnemy("s7mine",player.x+78,155,{});}');frames(p,55);shot(p,'sewer-pod-replacements')
  # UI route deliberately switches back and the save preserves the preference.
  p.evaluate('()=>{loadoutStart(()=>{});loadoutScr.row=2;loadoutScr.sel=run.loadout.indexOf(7);loadoutScr.vsel=1;loadoutScr.t=1;}');p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawLoadout(0);}');(O/'machine-gun-loadout.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  ck(p.evaluate('()=>{const r=loadoutScr.formRects[0];Input.mouse.x=r.x+r.w/2;Input.mouse.y=r.y+r.h/2;Input.mouse.down=true;loadoutScr.md=false;drawLoadout(1/60);Input.mouse.down=false;const selected=run._primary1003b==="mg";const s=campSnapshot();run._primary1003b="chain";campApply(s);beginStage(8);return selected&&run.weapon===0&&!chaingunReplacesMG()&&run.loadout.includes(0);}'),'loadout mouse handler equips machine gun and preserves it through save and next stage')
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'});p.evaluate('()=>{B.enter=true;B._r30.t=1.1;}');shot(p,'eight-bars-filling');p.evaluate('()=>B._r30.t=4.8');shot(p,'eight-bars-full')
  ck(p.evaluate('()=>f1003bBarFractions(B).every(f=>f===1)&&B._r30.pools.length===8'),'Furious intro fills eight separate colored health lives')
  # Native blit evidence: record the logical XART key at the game context boundary.
  p.evaluate('()=>{window.finalArtCalls=[];window.finalArtKey=null;const blit=r30Blit,cell=f1003bCell,sprite=s81003Cell,draw=ctx.drawImage;r30Blit=function(k){finalArtKey=REALM30_ART[k]?"r30_"+k:k;try{return blit.apply(this,arguments);}finally{finalArtKey=null;}};f1003bCell=function(k){finalArtKey="finale1003b_"+k;try{return cell.apply(this,arguments);}finally{finalArtKey=null;}};s81003Cell=function(k){finalArtKey="s81003_"+k;try{return sprite.apply(this,arguments);}finally{finalArtKey=null;}};ctx.drawImage=function(){if(finalArtKey)finalArtCalls.push(finalArtKey);return draw.apply(this,arguments);};window.finalRestoreDraw=()=>{r30Blit=blit;f1003bCell=cell;s81003Cell=sprite;ctx.drawImage=draw;};playerHit=function(){};}')
  for form in range(8):
   p.evaluate('(n)=>{r30Clear(B);r30Form(B,n);B._r30.mode="fight";B.enter=false;B._r30.cd=99;player.invuln=0;powerups=[];}',form);shot(p,f'form-{form+1}-idle')
   p.evaluate('()=>{window.formHP=B.hp;const v=r30Parts(B)[0];pBullets.push({kind:"mg",_chaingun:true,x:v.x,y:v.y,vx:0,vy:0,w:6,h:12,dmg:10,t:0});}');frames(p,1)
   ck(p.evaluate('()=>B.hp<formHP'),'real player shots damage form '+str(form+1))
   book=p.evaluate('()=>f1003bDef(B).book');stats={'form':form,'id':p.evaluate('()=>f1003bDef(B).id'),'attacks':[]}
   for index,attack in enumerate(book):
    p.evaluate('(i)=>{r30Clear(B);B._r30.seq=i;B._r30.attack=null;r30Attack(B);window.attackObject=B._r30.attack;window.peakShots=0;window.peakBeams=0;window.peakGround=0;}',index)
    captured=False
    for batch in range(180):
     frames(p,5)
     q=p.evaluate('()=>{peakShots=Math.max(peakShots,eBullets.filter(q=>q._finale1003b&&!q.dead).length);peakBeams=Math.max(peakBeams,S81003.beams.length);peakGround=Math.max(peakGround,groundTargetingFx.filter(q=>q.owner===B&&!q.dead).length);const P=B._r30.attack;return {same:P===attackObject,t:P?.t||0,tell:P?.tell||0,phase:P?.k1003?.phase};}')
     if not captured and (q.get('phase')=='followTell' if attack=='knight' else q['t']>q['tell']*.65 and q['t']<q['tell']):shot(p,f'form-{form+1}-{attack}-tell');captured=True
     if not q['same']:break
    q=p.evaluate('()=>({shots:peakShots,beams:peakBeams,ground:peakGround,done:B._r30.attack!==attackObject,recovery:B._r30.cd,finite:Number.isFinite(B.x+B.y),phaseHistory:B._r30.history.filter(q=>q.event==="knight1003").map(q=>q.phase)})')
    stats['attacks'].append({'type':attack,**q});ck(q['done'] and q['recovery']>0 and q['finite'],f'form {form+1} {attack} completes warning, attack and recovery')
    if attack not in ['talons','ram','stomp','knight']:ck(q['shots']>0 or q['beams']>0 or q['ground']>0,f'form {form+1} {attack} produces real hazards')
   report['forms'].append(stats)
  report['artCalls']=p.evaluate('()=>[...new Set(finalArtCalls)]');p.evaluate('()=>finalRestoreDraw()');ck(p.evaluate('()=>[...Object.keys(FINALE1003B_ART).map(k=>"finale1003b_"+k),"r30_possessed_body","r30_chopper_body","s81003_knight"].every(k=>finalArtCalls.includes(k))'),'all eight identities render authored art through game drawImage')
  # Actual player projectile hits module then a normal core; neither uses test-only collision.
  p.evaluate('()=>{r30Clear(B);r30Form(B,0);B._r30.mode="fight";B.enter=false;B._r30.cd=99;const v=r30Parts(B)[1];window.oldArm=v.p.hp;window.arm=v.p;window.oldBoss=B.hp;pBullets.push({kind:"mg",_chaingun:true,x:v.x,y:v.y,vx:0,vy:0,w:6,h:12,dmg:25,t:0});}');frames(p,1)
  report['armCollision']=p.evaluate('()=>({hp:arm.hp,before:oldArm,boss:B.hp,beforeBoss:oldBoss,part:B._lastPart?.id,bullets:pBullets.length,x:B.x,y:B.y})');ck(p.evaluate('()=>arm.hp<oldArm&&B.hp<oldBoss'),'native chaingun collision damages an independent host arm')
  p.evaluate('()=>{B._lastPart=arm;modularHit(arm.hp+1);}');shot(p,'host-arm-broken');ck(p.evaluate('()=>arm.destroyed&&r30Parts(B).length===2'),'destroyed host arm leaves the core and opposite arm intact')
  # Full progression, no reward until eighth life + existing escape/reunion.
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'});p.evaluate('()=>{playerHit=function(){};B._r30.mode="fight";B.enter=false;window.finalStartScore=run.score;window.formSequence=[];}')
  for form in range(8):
   ck(p.evaluate('(f)=>B._r30.form===f&&r30Live(B)&&B.parts.every(p=>p.hp>0&&!p.destroyed)',form),'full progression enters intact form '+str(form+1))
   p.evaluate('()=>{formSequence.push(B._r30.form);B._lastPart=B.parts[0];modularHit(B.hp+1);}');frames(p,180 if form<7 else 950)
   if form<7:ck(p.evaluate('()=>run.score===finalStartScore&&!bossDefeated'),'no premature reward after life '+str(form+1))
  ck(p.evaluate('()=>B._r30.rewarded&&B._r30.mode==="done"&&run._trueFinaleCleared&&run._realmReturned&&state===GS.STAGECLEAR&&formSequence.length===8'),'eighth life alone releases portal, reunion and final stage clear')
  report['sounds']=p.evaluate('()=>finaleSounds');report['errors']=errors;ck(not errors,'no page or console errors')
  (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'checks':len(report['checks']),'failed':[q['name'] for q in report['checks'] if not q['ok']],'errors':errors}),flush=True);browser.close()
finally:stop()
if errors or any(not q['ok'] for q in report['checks']):raise SystemExit(1)
