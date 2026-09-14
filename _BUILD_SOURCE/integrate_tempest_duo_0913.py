"""Integrate pinned, reviewed encounter AI into the existing self-contained game.
The source files and native adapter remain readable beside this build script.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / '_BUILD_SOURCE/tempest_source_0913'
game = ROOT / 'assets/game.js'
g = game.read_bytes().decode('utf-8')
def change(old, new):
    global g
    assert g.count(old) == 1, (old[:110], g.count(old))
    g = g.replace(old, new)
def ai_block():
    sources=[]
    for name in ['engine.js','engine-brother.js','engine-duo.js']:
        text=(SRC/name).read_text(encoding='utf-8').replace('\r\n','\n')
        if name in ['engine.js','engine-duo.js']:
            # Standalone input/collisions/escape are deliberately not shipped.
            # step is the last method in both classes; keep the class closing
            # brace and exports, and preserve the reviewed AI methods verbatim.
            start=text.index('step(dt,input={}){')
            end=text.rindex('\n}\nconst api=')
            text=text[:start]+text[end:]
        sources.append(text)
    return "const TEMPEST_DUO_AI=(function(){\n  const window={},globalThis=window,module=undefined;\n"+'\n'.join(sources)+"\n  return window.JetDuoEngine;\n})();\n"+(SRC/'fighter.js').read_text(encoding='utf-8')+'\n'+(SRC/'adapter.js').read_text(encoding='utf-8')+'\n'
if 'const TEMPEST_DUO_AI=' in g:
    start=g.index('const TEMPEST_DUO_AI=')
    end=g.index('function tempestProjectileDraw(q){',start)
    g=g[:start]+ai_block()+g[end:]
    game.write_bytes(g.replace('\r\n','\n').encode('utf-8'))
    print('Refreshed native adapter; excluded standalone step/input/escape methods.')
    raise SystemExit(0)
change("  for(const _tl of ['hull','hull_damaged','beam','charge','bolt','needle']) BOFX.img['tlv_'+_tl]='assets/game/bosses/tempest/tlv_'+_tl+'.png';",
       "  for(const _tl of ['hull','hull_damaged','beam','charge','bolt','needle']) BOFX.img['tlv_'+_tl]='assets/game/bosses/tempest/tlv_'+_tl+'.png';\n  for(const _tl of ['hull','hull_damaged']) BOFX.img['tlvb_'+_tl]='assets/game/bosses/tempest/tlvb_'+_tl+'.png';")
change("6:{at:0.45, kind:'tempestleviathan', afterScroll:1121}", "6:{at:0.45, kind:'tempestbrothers', afterScroll:1121}")
change("// Mike 0912: the TEMPEST LEVIATHAN jet duel is stage 6's miniboss; the Blacksteel Raptor is ALTBOSS[6]",
       "// Mike 0913: the approved black/gray Tempest brothers share stage 6; Blacksteel remains ALTBOSS[6]")
change("  return (b.dead || T.phase==='falsecrash' || T.phase==='frenzy' || b.hp<=b.maxhp*0.25) ? 'tlv_hull_damaged' : 'tlv_hull';",
       "  const prefix=b._tempestGray?'tlvb_':'tlv_';\n  return prefix+((b.dead || T.phase==='falsecrash' || T.phase==='frenzy' || b.hp<=b.maxhp*0.25) ? 'hull_damaged' : 'hull');")
change("    const end=q.dir<0 ? ((typeof viewTopY==='function')?viewTopY():0)-8 : VH+8, y0=Math.min(end,q.y), len=Math.abs(end-q.y);",
       "    const end=q.dir<0 ? ((typeof viewTopY==='function')?viewTopY():0)+77/((typeof viewZoom==='function')?viewZoom():1) : VH+8, y0=Math.min(end,q.y), len=Math.abs(end-q.y);")
block = "/* Reviewed encounter AI from GitHub main f936f106d85d935aaf518fbac5ab34756bc26724.\n   Private exports keep this single-file runtime compatible with every game page and Node QA. */\n"+ai_block()
change("function tempestProjectileDraw(q){", block + "function tempestProjectileDraw(q){")
change("    case 'tempestleviathan': tempestInit(b); break;", "    case 'tempestbrothers': tempestBrothersInit(b); break;\n    case 'tempestleviathan': tempestInit(b); break;")
change("  if(b._tlv){ tempestUpdate(b,dt); return; }", "  if(b._tempestDuo){ tempestBrothersUpdate(b,dt); return; }\n  if(b._tlv){ tempestUpdate(b,dt); return; }")
change("  if(b._s9rift){ s9VoidHorizonDraw(b); return; }\n  if(typeof drawSubBossBar==='function') drawSubBossBar(b);",
       "  if(b._s9rift){ s9VoidHorizonDraw(b); return; }\n  if(b._tempestDuo){ tempestBrothersDraw(b); drawSubBossBar(b); return; }\n  if(typeof drawSubBossBar==='function') drawSubBossBar(b);")
change("  if(b._tlv && typeof tempestPartAt==='function') return tempestPartAt(b,x,y);", "  if(b._tempestDuo) return tempestBrothersPartAt(b,x,y);\n  if(b._tlv && typeof tempestPartAt==='function') return tempestPartAt(b,x,y);")
change("  if(b._tlv && typeof tempestPartAt==='function') return tempestPartAt(b,x,y)!==null;", "  if(b._tempestDuo) return tempestBrothersPartAt(b,x,y)!==null;\n  if(b._tlv && typeof tempestPartAt==='function') return tempestPartAt(b,x,y)!==null;")
change("  const b=subBoss; if(!b||b.dead) return;\n  if(b._jcGhost) return;", "  const b=subBoss; if(!b||b.dead) return;\n  if(b._tempestDuo){ tempestBrothersHit(b,dmg,hx,hy); return; }\n  if(b._jcGhost) return;")
change("&& (!subBoss._harrier||subBoss._chCollision) && Math.abs(subBoss.x-player.x)", "&& (!subBoss._harrier||subBoss._chCollision) && (!subBoss._tempestDuo||tempestBrothersContact(subBoss,player.x,player.y)) && Math.abs(subBoss.x-player.x)")
change("      tempestleviathan:'tlv_',", "      tempestleviathan:'tlv_', tempestbrothers:'tlv',")
change("tempestleviathan:'TEMPEST LEVIATHAN',", "tempestleviathan:'TEMPEST LEVIATHAN', tempestbrothers:'TEMPEST LEVIATHAN BROTHERS',")
change("tempestleviathan:['tlv_'],", "tempestleviathan:['tlv_'], tempestbrothers:['tlv_','tlvb_'],")
game.write_bytes(g.replace('\r\n','\n').encode('utf-8'))
print('Integrated reviewed trio and native adapter; preserved the stored solo and existing stage slots.')
