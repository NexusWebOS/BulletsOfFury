"""Align retired boss and prologue checks with shipped encounter directors."""
from pathlib import Path

path = Path('_BUILD_SOURCE/test_fl.js')
text = path.read_bytes().decode('utf-8').replace('\r\n', '\n')

def swap(old, new):
    global text
    assert text.count(old) == 1, (old[:120], text.count(old))
    text = text.replace(old, new)

swap("  ok(_route246.indexOf(\"cinbg_hq_aerial\")>0 && _route246.indexOf(\"cinbg_hq_beach\")<0 &&\n     _route246.indexOf(\"cinbg_hq_gate\")<0 && _motion246.indexOf(\"cinDrawShip(p,1\")>0,\n     'moving arrival shots use the aerial HQ view and top-down ships only');",
     "  ok(_route246.indexOf(\"return cinCover('cinbg_hq_aerial'\")>0 && _motion246.indexOf(\"cinDrawShip(p,1\")>0,\n     'moving arrival shots use the aerial HQ view and top-down ships only');")
swap("  ok(/if\\(when==='pre' && stage===1\\)/.test(_s246) && _s246.indexOf('return hqPlayPilot(pk, briefing)')>0,\n     'stage 1 plays the opening first and the briefing after it');",
     "  ok(_s246.indexOf(\"if(when==='post' && stage===1 && run.mode==='campaign')return campaignBridgeStart(onDone)\")>0 &&\n     _s246.indexOf('campaignIntroStart(function(){ openStageSelect(fromStage,{boot:true}); })')>0,\n     'the history prologue precedes Stage 1 and its HQ debrief follows completion');")
start = text.index("  var _mini264=JSON.parse(")
end = text.index("  var _boss264=JSON.parse(", start)
text = text[:start] + ("  var _s3Thermo264=fs.readFileSync(ROOT+'/assets/stage3_thermo.js','utf8');\n"
     "  ok(vm.runInContext(\"SUBBOSS[1].kind==='razorback' && SUBBOSS[3].kind==='frostcruiser'\",ctxv) &&\n"
     "     /s3ThermoStrikeTick\\('mini',b,dt\\)/.test(fs.readFileSync(ROOT+'/assets/game.js','utf8')) &&\n"
     "     _s3Thermo264.indexOf(\"spawnSubBoss__inner('thermocloud')\")>0,\n"
     "     'the retired Jungle Cruiser attack is replaced by Razorback and Stage-3 Furious Thermocloud handoff');\n"
     "  ok(_s3Thermo264.indexOf(\"spawnBoss('therno')\")>0 &&\n"
     "     _s3Thermo264.indexOf(\"['ice','fire','thermal']\")>0 &&\n"
     "     _s3Thermo264.indexOf(\"s3ThermoRadial\")>0,\n"
     "     'Therno alternates ice, fire and thermoshock attacks after the nuclear boss strike');\n\n") + text[end:]
start = text.index("  ok(_tiers267.r[0].length")
end = text.index("  ok(_tiers267.c[0]", start)
text = text[:start] + ("  ok(vm.runInContext(\"SUBBOSS[3].kind==='frostcruiser'\",ctxv) &&\n"
     "     /s3FrostOrbBegin\\(b\\)/.test(fs.readFileSync(ROOT+'/assets/game.js','utf8')) &&\n"
     "     /function s3FrostOrbTick/.test(fs.readFileSync(ROOT+'/assets/stage3_thermo.js','utf8')),\n"
     "     'the active Frost Cruiser charges its authored ice orb before shard release');\n") + text[end:]
start = text.index("  ok(_tiers268.o[0].length")
end = text.index("}\n\n// ===== 269.", start)
text = text[:start] + ("  ok(vm.runInContext(\"SUBBOSS[4].kind==='olivewarden' && !!subBoss._s4war && subBoss._s4war.mini\",ctxv) &&\n"
     "     /function stage4WarfareMiniTick/.test(fs.readFileSync(ROOT+'/assets/game.js','utf8')) &&\n"
     "     vm.runInContext(\"SHIPBOSS.olivewarden.pats.join(',')==='s4warburst,s4wargate,s4wardrones'\",ctxv),\n"
     "     'Olive Warden uses the current modular burst, gate and drone director');\n") + text[end:]
swap("  ok(_src.indexOf('_sx=IX+2+(_ek?')>0 || _src.indexOf('_sx = IX+2+(_ek ?')>0,\n     'the subtitle only indents when the emblem actually resolved');",
     "  ok(_src.indexOf('const emblemReady=!!(emblem&&XART.rdy(emblem))')>0 &&\n     _src.indexOf('width-(emblemReady?28:0)')>0,\n     'the subtitle reserves badge width only after the emblem decodes');")
swap("     'a boss visibly anticipates first and releases its unchanged attack only on the authored beat');",
     "     'a boss visibly anticipates first and releases its unchanged attack only on the authored beat '+JSON.stringify(_boss245));")
swap("     'crossing a real boss phase cancels the old tell and performs a readable power-up reset');",
     "     'crossing a real boss phase cancels the old tell and performs a readable power-up reset '+JSON.stringify(_phase245));")
swap("     'the river corvette fires a five-beat port/starboard broadside from alternating physical cannons');",
     "     'the river corvette fires a five-beat port/starboard broadside from alternating physical cannons '+JSON.stringify(_nav245));")

path.write_bytes(text.replace('\n', '\r\n').encode('utf-8'))
assert path.read_bytes().count(b'\r\n') == path.read_bytes().count(b'\n')
