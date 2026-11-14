from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import sys,json,base64,io,subprocess,http.server,hashlib,threading
W=Path(__file__).resolve().parent;ARCHIVED=W.parent.name=='_BUILD_SOURCE';R=W.parent.parent if ARCHIVED else Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=R/'_shots/helicopter_effects_1111'if ARCHIVED else W.parents[1]/'outputs/dracodia-helicopter';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
class LimitedServer(http.server.ThreadingHTTPServer):
 request_queue_size=128
 slots=threading.BoundedSemaphore(16)
 def process_request(self,request,address):
  self.slots.acquire()
  try:super().process_request(request,address)
  except BaseException:self.slots.release();raise
 def process_request_thread(self,request,address):
  try:super().process_request_thread(request,address)
  finally:self.slots.release()
http.server.ThreadingHTTPServer=LimitedServer
BOOT="""()=>{debugUnlocked=true;diffKey='furious';debugStartFight(debugFightFor(8,'boss'),{pilot:'cole'});spawnBoss('vileexistence');debugFight.spawned=true;warnT=0;DBGT.god=false;DBGT.speed=1;player.invuln=1e9;player.x=worldWidth()/2;player.y=VH-65;BOFCinematicDirector.cancel();setState(GS.PLAY);for(const k of Object.keys(Input.keys))Input.keys[k]=false;stagePlan=[];enemies=[];powerups=[];window.B=boss;}"""
SETUP="""()=>{window.checkpoint=(kind='guns',diff='furious')=>{v18Clear(B);spawnBoss('vileexistence');B=boss;const J=j3State(B);for(const i of V18.forms)if(i!==1)J.hp[i]=0;v18Enter(B,2,1);B._r30.mode='fight';B.enter=B._noHit=false;B.x=340;B.y=174;B._r30.cd=100;B._r30.v18.arenaPhase=2;player.dead=player.out=false;player.x=340;player.y=VH-65;player.invuln=1e9;player.roll=player.somer=null;run.armor=run.shield=0;DBGT.god=false;for(const k of Object.keys(Input.keys))Input.keys[k]=false;pBullets=[];eBullets=[];playerLocks=[];stagePlan=[];enemies=[];powerups=[];camX=(worldWidth()-VW)/2;HC79.events=[];H125.events=[];diffKey=diff;window.P=hc79Start(B,kind);window.Q=hc79State(B);return B.hp;};}"""
def step(p,n=1):
 e=p.evaluate(STEP,n);assert e is None,e
def shot(p):return Image.open(io.BytesIO(base64.b64decode(p.evaluate("document.querySelector('#screen').toDataURL('image/png').split(',')[1]")))).convert('RGB').resize((480,512),Image.Resampling.NEAREST)
def record(p,name,seconds):
 e=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','480x512','-framerate','15','-i','pipe:0','-an','-c:v','ffv1','-level','3',str(W/(name+'.mkv'))],stdin=subprocess.PIPE);rows=[]
 try:
  for i in range(round(seconds*15)):
   step(p,4);rows.append(p.evaluate("({kind:Q.action?.kind,t:Q.action?.t,hp:B.hp,fx:H125.fx.length,missiles:eBullets.filter(q=>q._hc79Type==='missile').length})"));im=shot(p);e.stdin.write(im.tobytes())
   if i in [24,29,35,45,60]:im.save(O/(name+'-'+str(i)+'.png'))
 finally:e.stdin.close();assert e.wait(timeout=60)==0
 print('Recorded '+name,flush=True);return {'rows':rows,'events':p.evaluate('H125.events'),'native':p.evaluate('HC79.events')}
def main():
 errors=[];checks={};details={};port,stop=serve(str(R))
 def check(n,q):checks[n]=bool(q);print(json.dumps({n:q}),flush=True)
 try:
  with sync_playwright()as pw:
   br=pw.chromium.launch(channel='msedge',headless=True,args=['--mute-audio','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':1000});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400])if m.type=='error'or'draw error'in m.text else None);p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('window.__bofFrames>5&&typeof H125!=="undefined"');p.evaluate(TRAP_RAF);p.evaluate(BOOT);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()}');p.evaluate(SETUP);print('Helicopter native effects ready',flush=True)
   p.evaluate("checkpoint('guns')");details['guns']=record(p,'guns',4.1);check('both_gun_pods_fire_new_tracers',len([e for e in details['guns']['events']if e['event']=='gun-fire'])>=24)
   p.evaluate("checkpoint('missiles')");details['missiles']=record(p,'missiles',4.4);check('furious_keeps_eight_physical_missiles',len([e for e in details['missiles']['events']if e['event']=='rocket-fire'])==8)
   p.evaluate("()=>{checkpoint('missiles');Input.keys.j=true;}");details['intercepts']=record(p,'intercepts',5);check('ordinary_player_fire_triggers_new_missile_explosions',any(e.get('reason')=='missile-impact'for e in details['intercepts']['events']))
   p.evaluate("()=>{checkpoint('missiles');B._lastPart=B.parts.find(q=>q.id==='left');modularHit(B._lastPart.hp);}");details['pod-break']=record(p,'pod-break',2.8)
   check('broken_pod_uses_new_staggered_explosions',len([e for e in details['pod-break']['events']if e.get('reason')in ['pod-break','pod-secondary']])==3)
   check('broken_pod_cancels_queued_launches',p.evaluate("!HC79.events.some(e=>e.event==='missile-launch'&&e.part==='left')&&HC79.events.filter(e=>e.event==='missile-launch'&&e.part==='right').length===4"))
   check('destroyed_pod_removed_from_live_rig',p.evaluate("!v18Rig(B).some(v=>v.p.id==='left')&&!hc79Alive(B,'left')"))
   for diff,n in [('normal',4),('hard',6)]:
    p.evaluate('(d)=>checkpoint("missiles",d)',diff);step(p,130);check(diff+'_missile_count_preserved',p.evaluate("HC79.events.filter(e=>e.event==='missile-launch').length")==n)
   # Reach the original committed safe corridor with normal movement and no GOD.
   p.evaluate("()=>{checkpoint('guns');player.invuln=0;}")
   for i in range(220):
    p.evaluate('()=>{Input.keys.a=player.x>P.safeX+2;Input.keys.d=player.x<P.safeX-2;}');step(p,1)
   check('new_tracers_keep_reachable_native_safe_gap',p.evaluate('!player.dead&&player.invuln===0&&Math.abs(player.x-P.safeX)<7'))
   check('ordinary_gunfire_remains_noninterceptible',p.evaluate("eBullets.filter(q=>q._hc79Type==='gun').every(q=>!enemyOrdnanceCanIntercept(q)&&q._weaponProof)"))
   p.evaluate("checkpoint('missiles')");step(p,85);check('missiles_remain_shootable_and_lock_owned',p.evaluate("eBullets.some(q=>q._hc79Type==='missile')&&eBullets.filter(q=>q._hc79Type==='missile').every(q=>enemyOrdnanceCanIntercept(q)&&q._lockId&&q._shootable)"))
   before=p.evaluate('JSON.stringify([P.t,Q.rotor,B.x,B.y,efxClock])');p.evaluate("setState('paused')");step(p,90);check('pause_freezes_effect_and_weapon_clocks',before==p.evaluate('JSON.stringify([P.t,Q.rotor,B.x,B.y,efxClock])'));p.evaluate('setState(GS.PLAY)')
   p.evaluate("()=>{const q=eBullets.find(q=>q._hc79Type==='missile');window.hitMissile=q;for(const k of Object.keys(Input.keys))Input.keys[k]=false;pBullets.push({kind:'mg',x:q.x,y:q.y,w:10,h:20,vx:0,vy:0,dmg:1,t:0,life:1,_ph:0});}");step(p,2)
   check('real_interception_spawns_exactly_one_burst_per_missile',p.evaluate("hitMissile.dead&&hitMissile._h125Burst&&H125.events.filter(e=>e.reason==='missile-impact'&&Math.abs(e.x-hitMissile.x)<.1&&Math.abs(e.y-hitMissile.y)<.1).length===1"))
   step(p,52);check('missile_explosion_finishes_without_lingering',p.evaluate('H125.fx.every(q=>efxClock-q.born<.8)'))
   p.evaluate('v18Clear(B)');check('clear_removes_watchers_and_explosions',p.evaluate('H125.watch.size===0&&H125.fx.length===0'))
   p.evaluate("checkpoint('guns')");step(p,75);p.evaluate("()=>{B._lastPart=B.parts.find(q=>q.id==='right');modularHit(1);}");
   for i in range(3):
    step(p,1)
    if p.evaluate('Math.floor(efxClock*30)%2===0'):break
   shot(p).save(O/'actual-pod-hit.png');check('native_pod_hit_flash_retained',p.evaluate("B.parts.find(q=>q.id==='right').flash>0"));step(p,12);shot(p).save(O/'actual-pod-hit-expired.png');check('native_hit_flash_expires',p.evaluate('B.flash<=0&&B.parts.every(p=>p.flash<=0)'))
   # Read source blits in one real frame to verify the emitter still uses the
   # current recoiling pod socket, including integer placement.
   p.evaluate("()=>{checkpoint('guns');window.h125Blits=[];window.oldDraw=ctx.drawImage;ctx.drawImage=function(im,...a){const key=Object.keys(H125_ART.pages).find(k=>XART.get(k)===im);if(key)h125Blits.push({key,a});return oldDraw.call(this,im,...a);};}");step(p,80)
   details['emitters']=p.evaluate("()=>{const rows=H125_ART.banks.muzzle;return ['left','right'].map(id=>{const flash=Q._h125Flashes[id],age=efxClock-flash.t,f=Math.min(7,Math.floor(age/.16*8)),d=hc79Dir(Q.turn[id]+Math.PI/2),a=rows[f*64+d],m=hc79Socket(B,id);return{part:id,expected:[Math.round(m.x+a.offset[0]),Math.round(m.y+a.offset[1])],matched:h125Blits.some(v=>v.key===a.key&&v.a[0]===a.rect[0]&&v.a[1]===a.rect[1]&&v.a[4]===Math.round(m.x+a.offset[0])&&v.a[5]===Math.round(m.y+a.offset[1]))};});}");p.evaluate('ctx.drawImage=oldDraw');check('new_muzzle_pixels_follow_current_recoil_sockets',all(q['matched']for q in details['emitters']))
   p.evaluate("()=>{checkpoint('missiles');H125.reduced=true;}");step(p,130);check('reduced_flashing_keeps_native_eight_launches',p.evaluate("HC79.events.filter(e=>e.event==='missile-launch').length===8"));p.evaluate('H125.reduced=false')
   p.evaluate("()=>{checkpoint('sonic');}");step(p,200);check('sonic_attack_still_uses_native_owner',p.evaluate("HC79.events.some(q=>q.event==='red-sonic')&&eBullets.filter(q=>q._hc79Type==='sonic').every(q=>!enemyOrdnanceCanIntercept(q))"))
   p.evaluate("checkpoint('dash')");step(p,128);check('native_warned_charge_still_exits_screen',p.evaluate('B.y>VH&&B._noHit'));step(p,145);check('native_charge_returns_to_hover',p.evaluate('B.y>160&&B.y<190&&!B._noHit'))
   details['audio']=p.evaluate("""async()=>{const a=Snd._audioCtx();await a.resume();const out=[];for(const key of ['overlordGun','overlordRocket','expSmall','expBig']){let path=BOFA.sfx[key];if(Array.isArray(path))path=path[0];const d=await a.decodeAudioData(await(await fetch(path)).arrayBuffer());let peak=0;for(const x of d.getChannelData(0))peak=Math.max(peak,Math.abs(x));out.push({key,peak,duration:d.duration});}return out;}""");check('gun_rocket_and_blast_cues_decode',all(q['peak']>.001 for q in details['audio']))
   check('all_new_pages_preloaded',p.evaluate('h125Keys().every(k=>XART.rdy(k))'));details['draws']=p.evaluate('H125.draws');check('all_requested_effect_banks_rendered',all(n in details['draws']for n in ['muzzle','launch','tracer','missile','burst72','burst112','burst160']))
   check('effect_concurrency_is_bounded',p.evaluate('H125.fx.length<=24&&H125.watch.size<=16'));check('no_native_browser_errors',not errors);br.close()
 finally:stop()
 before=json.loads((W/'before.json').read_text());check('original_body_ai_and_other_forms_unchanged',all(hashlib.sha256((R/'assets'/n).read_bytes()).hexdigest()==h for n,h in before.items()if n!='index.html'))
 (O/'verification.json').write_text(json.dumps({'checks':checks,'details':details,'errors':errors},indent=2));assert all(checks.values()),[n for n,q in checks.items()if not q]
if __name__=='__main__':main()
