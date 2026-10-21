from pathlib import Path
from PIL import Image
import json,shutil,re
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;S=R/'_ART_SOURCES/menu_heart_1021';O=R/'_shots/menu_heart_1021'
for name in ['prepare_menu_heart_1021.py','collect_heart_1021.py','build_menu_heart_1021.py','probe_menu_heart_1021.py','review_menu_heart_1021.py','check_menu_review_1021.py','finish_menu_heart_1021.py']:
 if (W/name).resolve()!=(R/'_BUILD_SOURCE'/name).resolve():shutil.copy2(W/name,R/'_BUILD_SOURCE'/name)
prompts={
 'menu_family':{'generator':'built-in image_gen','common':'Bullets of Fury military digital NeoGeo/Sega32X pixel art. Straight-on gunmetal/chrome bevels, small amber/red lights, clipped corners. One full-width empty header and uninterrupted opaque charcoal body. No avatars, portrait slots, words, icons, or baked buttons. Transparent exterior. Preserve proportions and reusable safe text apertures.', 'variants':{'xl':'Substantial landscape large menu window intended720x480.','l':'Separate16:9 landscape medium menu frame intended720x400; reference XL for material consistency.','m':'Newly authored short2.6:1 notification/question window intended720x276; reference L.','s':'Compact4:1 notification intended640x160; reference M.'}},
 'boss_preview_concepts':[
  {'name':'Fury Threat Console','prompt':'Original wide enemy inspection console. Gunmetal, silver, red status lights. Large central B.O.B turntable, skinny identity sidebar left, three stat bands right, part carousel and bottom targeting strip. No pilot avatar. Reference actual grey/orange B.O.B and facts, not original card layout.'},
  {'name':'Holoscan','prompt':'Deep navy technical terminal, restrained cyan/silver chassis. Huge blue holographic B.O.B exploded into body, cannon and pod, leader lines, right part selector, broad title. Bottom readouts240HP/ICE, WEAK:FIRE x1.5, MISSILES:CORE. Original composition, no pilot avatar.'},
  {'name':'Field Manual95','prompt':'Two-page cream technical instruction folio in olive military case. Chunky black bitmap headings, orange callouts, grey/orange friendly training robot with bright blue core. Left page large B.O.B and stats, right cutaway/module diagram. WHY HAVEN’T I RETIRED YET? Mid1990s printed strategy guide texture. Robot training UI, no combat scene.'},
  {'name':'Arcade Data Cartridge','prompt':'Huge black Sega-era cartridge inspection UI, knurled charcoal shell, silver label, amber/cobalt tabs and exposed contact pins. Actual B.O.B to right with wireframe and module chips. Large left stats and quote. Original composition, no pilot avatar.'},
  {'name':'Hangar Service Lift','prompt':'Friendly sci-fi robot maintenance game screen. NeoGeo pixel art, huge grey/orange B.O.B on service turntable, mechanical gantry holding detached utility pods, amber workshop lights and teal monitors. Broad bottom silver stats shelf, fine module callouts and thumbnail strip. No human avatars.'}],
 'heart_master':{'generator':'built-in image_gen','reference':'actual blue Hammer idle256','prompt':'Re-author original Hammer identity as CHROME HEART: athletic armored robot, angular spiked helmet, dark segmented chassis, glowing heart reactor, plated boots, huge long-handled solid heart-shaped chrome hammer. Vibrant hot-pink/rose chromium armor and polished pearl silver highlights. Front-facing entire full body, hammer diagonal down left. NeoGeo/Sega32X production pixel art, transparent background, generous animation margins, one sprite not sheet.'},
 'animation':{'generator':'PixelLab PixMiniMax','seed':'heart_seed.png, fixed256','jobs':'pixellab-jobs.json','constraints':'Fixed camera, full body, stable proportions/armor/palette and shared chest pivot. Idle8, dance24, overhead slam20, hammer spin16, shield channel16, heart projectile12, shield rim16. Only generated frames1..N exported; raw inputframe0 preserved as seed.'},
 'shield_repair':{'tool':'PixelLab pixelart_workbench','receipt':'shield-alpha-repair.json','instruction':'Remove exactly12 observed dark opaque purple backdrop colors from every shield frame; preserve bright authored rim/lightning. Common16px transparent outer padding; retain original visible scale.'}}
(S/'prompts.json').write_text(json.dumps(prompts,indent=2,ensure_ascii=False),encoding='utf-8')
counts={};runtime=R/'assets/game/levels/secret/chrome_heart_1021'
for n in ['idle','dance','slam','spin','channel','heart','shield-clean']:
 files=sorted((S/n).glob('*.png'));counts[n]={'frames':len(files),'even':all(Image.open(p).width%2==0 and Image.open(p).height%2==0 for p in files)}
counts['runtime_bytes']=sum(p.stat().st_size for p in runtime.glob('*.webp'));counts['ui_bytes']=sum(p.stat().st_size for p in (R/'assets/game/shared/ui/menu_windows_1021').glob('*.webp'));counts['pixellab_remaining_usd']=2.59
log=(O/'full-suite.log').read_text(encoding='utf-8');counts['full_suite']={'assertions':sum('  ok ' in l for l in log.splitlines()),'zero_errors':'BUILD OK, 0 ERRORS' in log,'exit':0}
for n in ['verification','cross-browser']:
 p=O/f'{n}.json'
 if p.exists():
  d=json.loads(p.read_text());counts[n]={'checks':len(d['checks']),'passed':sum(c['ok'] for c in d['checks']),'errors':d['errors']}
(S/'final-verification.json').write_text(json.dumps(counts,indent=2),encoding='utf-8')
doc='''# Menu windows and Chrome Heart — October21

The tutorial menu now uses a neutral deployment prompt in a dedicated generated menu frame. No pilot name or portrait is used to ask about training. Instructor Cole remains the instructor during the actual tutorial.

## Four reusable menu windows

Separate generated S/M/L/XL art in `assets/game/shared/ui/menu_windows_1021/`. Source crops retain even720px-wide canvases and proportional scaling. The runtime preserves corners with nine-slice rendering, maps header/body apertures through the same transform, wraps text and fits its height, then centers the actual bitmap glyphs. No portrait column is present. Intended game layouts: S384x132, M456x196, L456x286, XL456x366. The L tutorial menu keeps choices, recommendation, and controls separate from the paragraph.

## Five preview choices

Open http://127.0.0.1:8794/_shots/menu_heart_1021/review.html . The five directions are Fury Threat Console, Holoscan, Field Manual95, Arcade Data Cartridge, and Hangar Service Lift. These are review concepts, not live replacements. Robot details and baked mockup text are illustrative; the chosen implementation must use BOF’s real B.O.B. parts/turntables and live440-total/240-core stats with fitted text. The original Overdrive-derived card remains pending Mike’s choice.

## BARBIE / Chrome Heart

A real final-stage victory with Falva or Lizzie, including an eligible co-op seat, saves the account unlock `bof_chrome_heart_v1`. Both campaign and arcade final victories qualify on every difficulty. Starting a level, clearing a different stage, a debug/bossmode fight or winning as another solo pilot does not unlock it. Entering BARBIE before the unlock explains the requirement; afterward the native difficulty and pilot selection lead directly to the optional fight. This does not unlock the password merely by typing it.

Chrome Heart is a newly authored pink/pearl chromium Hammer actor with a heart reactor and solid chrome heart hammer.112 PixelLab animation/effect frames ship as seven compact atlases. The attack book is dance volleys, a targeted overhead slam with impact Retina, an absorbing breakable heart shield, a moving hammer waltz with ring bursts and a wider heart bouquet. All four difficulty settings tune HP, telegraph duration, shot count, speed and recovery. Aimed heart fans use actual-ray FOVs, with committed vectors and safe reaction time. The shield absorbs without deflection; hits flash the body and shield through native hit owners. The core has a Retina target. Measured chest/hammer offsets match projectile and slam origins.

The secret arena clears normal stage scheduling, retains native ship controls, weapons, dodge invulnerability, mixer cues and the Hammer death/explosion/fly-off sequence. Restart stays in the secret encounter. Its final fly-off leads to a dedicated result window without normal Stage5 Forge/unlock/progression menus. Normal Hammer encounters retain their established art and combat.

## Music

Aqua’s “Barbie Girl” instrumental cover is offered in the Tency/Karaoke Version licensing catalog: https://www.tencymusic.com/music-licensing/aqua/barbie-girl.html (ISRC FR3Z80700459,3:17,130BPM). It is a re-recording, not Aqua’s master. Purchase/licensing is required; no paid file or preview was ripped or bundled. The game currently uses its existing Hammer track. After supplying a locally licensed instrumental, set its relative asset path in `assets/chrome_heart_music_1021.js` (`CH21_MUSIC`). It then uses `Snd.music`, retaining the existing master/music sliders, mute, pause and warp handling.

## Verification

See `_ART_SOURCES/menu_heart_1021/final-verification.json` for exact current counts and `_shots/menu_heart_1021/verification.json`, `cross-browser.json` and `full-suite.log` for details. Native Edge contracts cover four difficulty attack books, real damage flashes, shield absorption, actual routed audio decode/playback, restart, death/fly-off/result routing, unlock/save/reload and the ordinary Hammer. Chrome/Firefox/Edge checks cover actual keyboard menu input, all five animation selections and desktop/mobile review layout. The review reel is native game rendering, not a Python mock. Automated fixtures are not a human survival-rate measurement.

Source art, prompt set, PixelLab job IDs and shield repair receipt are in `_ART_SOURCES/menu_heart_1021/`. Generated menu sources and concepts used built-in image_gen; animated banks and shield transparency repair used PixelLab. No source raw artwork is needed at game boot. No GitHub publish was performed in this pass.
'''
(R/'docs/MENU_HEART_1021.md').write_text(doc,encoding='utf-8')
p=O/'review.html';h=p.read_text(encoding='utf-8')
if 'alt="Native Chrome Heart attack reel"' not in h:h=h.replace('<h1>Live game verification</h1>','<h1>Live game verification</h1><p><a href="heart-actions.gif"><img src="heart-actions.gif" alt="Native Chrome Heart attack reel" style="max-height:680px"></a></p>')
if 'Art prompts and provenance' not in h:h=h.replace('<p><a href="/index.html" target="_blank">','<p><a href="/docs/MENU_HEART_1021.md">Pass notes</a> · <a href="/_ART_SOURCES/menu_heart_1021/prompts.json">Art prompts and provenance</a> · <a href="cross-browser.json">Chrome / Firefox / Edge checks</a></p><p><a href="/index.html" target="_blank">')
p.write_text(h,encoding='utf-8')
for name,marker,addition in [
 ('AGENTS.md','## Menu windows and Chrome Heart (October21)', '\n## Menu windows and Chrome Heart (October21)\n\n- Menu confirmation/training prompts use the avatar-free S/M/L/XL `MW21` family, its measured text apertures and proportional corner-preserving renderer. Cinematic pilot dialogue stays separate. Never stretch a cinematic portrait plate into a tall menu window.\n- Five boss-preview concepts in `_shots/menu_heart_1021/review.html` await Mike’s choice; do not install an unchosen concept or copy Overdrive’s card again. Bind the chosen design to actual BOF models and live stats.\n- BARBIE is a protected account unlock after a real Falva/Lizzie final win (including co-op), never a debug victory. Chrome Heart stays scoped to its secret arena, with native dodge/death/audio ownership, absorbing shields, real hit flashes and its own post-fight result. See `docs/MENU_HEART_1021.md`.\n'),
 ('HANDOFF_CODEX.md','## October21 — menu windows / Chrome Heart', '\n## October21 — menu windows / Chrome Heart\n\nSee `docs/MENU_HEART_1021.md` and `_ART_SOURCES/menu_heart_1021/final-verification.json`. Avatar-free S/M/L/XL menu windows and a neutral tutorial prompt are live. Five boss dossier concepts await Mike’s choice at `_shots/menu_heart_1021/review.html`; original card is not silently replaced. BARBIE unlocks from an actual Falva/Lizzie final win and starts the separate pink Chromium/heart-Hammer fight.112 generated animation/FX poses; native flash/audio/death/restart/result routing verified. Aqua instrumental licensing source located; no unlicensed audio bundled. Native Hammer music remains until a licensed local track is supplied. No GitHub publish requested or performed.\n')]:
 p=R/name;b=p.read_bytes()
 if marker.encode() not in b:p.write_bytes(b+addition.replace('\n','\r\n' if b'\r\n' in b else '\n').encode('utf-8'))
print(json.dumps(counts,indent=2))
