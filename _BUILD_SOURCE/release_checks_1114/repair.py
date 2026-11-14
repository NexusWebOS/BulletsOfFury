from pathlib import Path
from PIL import Image
import json,hashlib,subprocess
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');changes=[];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def edit(name,fn,why):
 p=R/name;b=p.read_bytes();bak=W/(name.replace('/','__')+'.repair-before');
 if not bak.exists():bak.write_bytes(b)
 s=b.decode();s=fn(s);assert p.read_bytes()==b;p.write_bytes(s.encode());changes.append(dict(file=name,why=why,before=hashlib.sha256(b).hexdigest(),after=sha(p)))
def replace(s,a,b):
 if a in s:return s.replace(a,b)
 assert b in s,(a[:80],'patch no longer matches');return s
def main(s):
 s=replace(s,"var _sv=_vk.filter(function(k){return _seen2[k];});","var _scheduledVolc=['skim','disc','miner','ash','cruc','lance','carrier','lavamaw','pod'];\r\n  var _sv=_scheduledVolc.filter(function(k){return _seen2[k];});")
 s=replace(s,"ok(_sv.length===11, 'all eleven active volcanic roles appeared after retiring the golem ('+_sv.length+'/11: '+_sv.join(',')+')');","ok(_sv.length===9&&!['eye','crawl','golem'].some(k=>_seen2[k]), 'all nine scheduled volcanic roles appear; retired eye/crawler/golem stay out ('+_sv.join(',')+')');")
 s=replace(s,"['ash','skim','cinderwasp','magmaorb','basaltbomber','eye','lance','disc','cruc','carrier','miner','lavamaw','crawl','pod','firejet1002']","['ash','skim','cinderwasp','basaltbomber','lance','disc','cruc','carrier','miner','lavamaw','lavasnake','pod','firejet1002']")
 s=replace(s,'Stage 2 fields its fifteen volcanic and new fire-jet types without rejected aliases','Stage 2 fields its thirteen current volcanic and fire-jet types without rejected aliases')
 old='ok(vm.runInContext("hitSubBoss.toString().indexOf(\'b.flash=0.18\')>0", ctxv), \'and the flash is held long enough for a single hit to register\');'
 new='ok(vm.runInContext("(()=>{const prior=subBoss;try{subBoss={x:240,y:140,w:40,h:40,hp:100,maxhp:100,dead:false,enter:false};hitSubBoss(1,240,140);return subBoss.hp<100&&subBoss.flash>=.18;}finally{subBoss=prior;}})()",ctxv), \'native damage holds the actual hit flash for at least .18 seconds\');'
 s=replace(s,old,new)
 s=replace(s,"ok(_sizes.length>10 && Math.min.apply(null,_sizes)>=11,\r\n     'every helpLabel call asks for 11px or more (' + _sizes.length + ' calls, smallest ' + Math.min.apply(null,_sizes) + ')');","ok(_sizes.length>10 && vm.runInContext('HELP_MIN>=11',ctxv) && /Math\\.max\\(HELP_MIN, size\\)/.test(_hlp) && /Math\\.max\\(HELP_MIN, stageFitH/.test(_hlp),\r\n     'every help label renders at least 11px, including fit-to-width labels');")
 marker="run('assets/game.js', 'game');"
 if "run('assets/stage8_leech_recovery_1114.js'"not in s:s=s.replace(marker,marker+"\r\nrun('assets/stage8_leech_recovery_1114.js', 'stage8_leech_recovery');")
 return s
edit('_BUILD_SOURCE/test_fl.js',main,'Current authored Stage2 roster; actual markHit feedback; effective help font floor; load recovered native leech atlas.')
def mutator(s):
 s=replace(s,"o['dialogue ends with the opening jump warning']=b._hammer.state==='warn'&&!b._noHit;","o['dialogue yields directly to native armor preparation']=b._hammer.state==='hammer'&&!b._noHit&&!b._hammer.openingJump1003;")
 s=replace(s,"o['opening jump lands and returns before chromium activation']=['warn','leap','recover','back','fr_activation','hammer'].every((s,i,a)=>opening.includes(s)&&(i===0||opening.indexOf(s)>opening.indexOf(a[i-1])));","const armorAt=opening.indexOf('fr_activation');o['chromium activates before the first combat attack']=armorAt>=0&&opening.indexOf('hammer',armorAt+1)>armorAt&&!opening.slice(0,armorAt).some(s=>['warn','leap','recover','back'].includes(s));")
 return s
edit('_BUILD_SOURCE/test_mutator_1003.cjs',mutator,'The approved October24 dialogue → armor → combat order superseded the pre-armor opening jump.')
def stage8(s):
 old="o['100 generated frames and four crystal chunks resolve to project files']=Object.values(S81003_ART).reduce((n,a)=>n+a.frames,0)===104;"
 prior="o['96 authored actor/effect frames and four crystal chunks resolve to real sheets']=Object.values(S81003_ART).reduce((n,a)=>n+a.frames,0)===100&&S81003_ART.shards.frames===4&&Object.values(S81003_ART).every(a=>fs.existsSync(path.join(__dirname,'../',a.path)));"
 s=s.replace(prior,old)
 s=replace(s,old,"o['96 authored actor/effect frames and four crystal chunks resolve to real sheets']=Object.values(S81003_ART).reduce((n,a)=>n+a.frames,0)===100&&S81003_ART.shards.frames===4&&${filesPresent};")
 if 'const filesPresent='not in s:s=s.replace(" const rows=JSON.parse", " const filesPresent=Object.values(JSON.parse(vm.runInContext('JSON.stringify(S81003_ART)',ctxv))).every(a=>fs.existsSync(path.join(__dirname,'../',a.path)));\n const rows=JSON.parse",1)
 return s
edit('_BUILD_SOURCE/test_stage8_1003.cjs',stage8,'Actual selected importer metadata has96 actor/effect frames plus4 chunks; verify every source sheet exists.')
edit('_BUILD_SOURCE/test_campaign_focus_1004b.cjs',lambda s:replace(s,"for(const route of ['left','right']){setup(6);s6WingInit();","for(const route of ['left','right']){campaign.stageX1004=null;delete run._gp4StageX;delete run._cf4Return;setup(6);s6WingInit();"),'Each alternate campaign-route fixture must start a fresh pending-route record instead of inheriting the completed previous branch.')
edit('_BUILD_SOURCE/test_campaign_controls_1004h.cjs',lambda s:replace(s.replace("cmap2.focus==='map'&&Input.tap('enter')&&state===GS.STAGESEL","cmap2.focus==='map'&&Input.menuConfirm()&&state===GS.STAGESEL"),"out['Start gives the bar ownership before Stage X can deploy']=cmap2.focus==='bar'&&!Rival24.mapInput()&&state===GS.STAGESEL;","out['Start preserves the focused map deployment confirmation']=cmap2.focus==='map'&&Input.menuConfirm()&&state===GS.STAGESEL;\n Input.clearTaps();Input.injectTap('escape');campaignMenuInputTick();out['Back gives the toolbar ownership and blocks Stage X deployment']=cmap2.focus==='bar'&&!Rival24.mapInput()&&state===GS.STAGESEL;"),'Current Start confirms map focus; Back opens toolbar. Verify both real input ownership paths.')
# Recover exact original pixels; keep archived source data intact. A separate
# generated sheet/cell registration leaves existing atlases and newer art alone.
source=R/'UNUSED_ASSETS/cleanup_2026-10-06/assets/game/stage8_mega_enemies/armored_leech';E=W/'exports';E.mkdir(exist_ok=True);frames=[];inputs={};cells={}
for action in ['attack','roll']:
 for i in range(8):
  p=source/f'{action}_{i+1:02}.png';im=Image.open(p).convert('RGBA');assert im.size==(256,256);inputs[str(p.relative_to(R))]=sha(p);frames.append(im);n=len(frames)-1;cells[f's8{ "atk"if action=="attack"else"roll"}_armored_leech_{i}']=['stage8_leech_recovery_1114',n%4*264+4,n//4*264+4,256,256]
out=Image.new('RGBA',(1056,1056))
for i,f in enumerate(frames):out.paste(f,(i%4*264+4,i//4*264+4))
out.save(E/'stage8_leech_recovery_1114.png');dest=R/'assets/game/levels/stage_08/enemies/atlas';dest.mkdir(exist_ok=True);(dest/'stage8_leech_recovery_1114.png').write_bytes((E/'stage8_leech_recovery_1114.png').read_bytes())
for i,f in enumerate(frames):assert out.crop((i%4*264+4,i//4*264+4,i%4*264+260,i//4*264+260)).tobytes()==f.tobytes()
js="'use strict';\n/* Exact archived native leech reels. Builder: _BUILD_SOURCE/release_checks_1114/repair.py. */\nBOFX.img.nca_stage8_leech_recovery_1114='assets/game/levels/stage_08/enemies/atlas/stage8_leech_recovery_1114.png';\nXART._src.nca_stage8_leech_recovery_1114=BOFX.img.nca_stage8_leech_recovery_1114;\nObject.assign(BOFX.cells,"+json.dumps(cells,separators=(',',':'))+");\n"
(W/'stage8_leech_recovery_1114.js').write_text(js);(R/'assets/stage8_leech_recovery_1114.js').write_text(js)
edit('index.html',lambda s:s if'assets/stage8_leech_recovery_1114.js'in s else s.replace('<script src="assets/game.js?v=tester-repairs-1106d"></script>','<script src="assets/game.js?v=tester-repairs-1106d"></script>\r\n<script src="assets/stage8_leech_recovery_1114.js?v=1"></script>'),'Register all16 recovered leech cells before encounter code can request them.')
assert(R/'_BUILD_SOURCE/test_fl.js').read_bytes().count(b'\n')==(R/'_BUILD_SOURCE/test_fl.js').read_bytes().count(b'\r\n')
for c in changes:
 if c['file'].endswith(('.js','.cjs')):subprocess.run(['node','--check',str(R/c['file'])],check=True)
(W/'repair-report.json').write_text(json.dumps(dict(changes=changes,recoveredFrames=16,pixelExact=True,sourceHashes=inputs),indent=2));print('Repaired current-spec fixtures and recovered16 exact leech frames; native game.js remains unchanged.',flush=True)
