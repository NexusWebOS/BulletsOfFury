"""Own the music-only manifest update and byte-preserving October 3 organization.
Rerunnable; source recordings and historical documentation remain preserved.
"""
from pathlib import Path
import hashlib, json, re

R = Path(__file__).resolve().parents[1]
M = R / 'assets/game/music'
NAMES = {
 'stage1_rumble_in_the_jungle.mp3':'Level1.mp3',
 'stage2_its_hot_in_here.mp3':'Level2.mp3',
 'stage3_ice_still_cant_see.mp3':'Level3.mp3',
 'stage4_crouching_missiles.mp3':'Level4.mp3',
 'lvl3-alt.mp3':'Level5.mp3',
 'stage6_city_in_the_sky.mp3':'Level6.mp3',
 'stage7_over_the_horizon_0925.mp3':'Level7.mp3',
 'stage8_furious_death.mp3':'Level8.mp3',
 'stage9_lord_of_the_shadows.mp3':'Level9.mp3',
 'stagex_gasline_1003.mp3':'LevelX.mp3',
 'miniboss_fireboss.mp3':'Level1mb.mp3',
 'miniboss2_magma_ward.mp3':'Level2mb.mp3',
 'miniboss3_frost_cruiser.mp3':'Level3mb.mp3',
 'unused9 - stage5b-alt.mp3':'Level4mb.mp3',
 'boss5_deadly_night.mp3':'Level5mb.mp3',
 'unused7 - stage6.mp3':'Level6mb.mp3',
 'unused13 - stage7b.mp3':'Level7mb.mp3',
 'unused4 - stage1b.mp3':'Level9mb.mp3',
 'boss1_helicopterboss.mp3':'Level1b.mp3',
 'boss2_bossfight3_loud_0920.mp3':'Level2b.mp3',
 'boss3_pandemonium.mp3':'Level3b.mp3',
 'boss4_cowboyfromhell_loud_0920.mp3':'Level4b.mp3',
 'boss5_hammerman_cometh_0926.mp3':'Level5b.mp3',
 'boss6_battle_in_the_sky.mp3':'Level6b.mp3',
 'boss7_reaperman_0927.mp3':'Level7b.mp3',
 'final_boss_phase1_0925.mp3':'Level8b.mp3',
 'unused3 - stage8b-p3.mp3':'Level8b2.mp3',
 'final_boss_phase3_the_final_confrontation_0925.mp3':'Level8b3.mp3',
 'stage9_boss_captain_timekeeper.mp3':'Level9b.mp3',
 'stage9_bonus_warp_run.mp3':'Opening.mp3',
 'stage9_rival_dog_showdown.mp3':'Rival.mp3',
 'stage5_egypt.mp3':'Unused_Egypt.mp3',
 'campaign_map.mp3':'CampaignMap.mp3',
 'cinematic_final_level_0925.mp3':'FinalCinematic.mp3',
 'cinematics_rapbeat.mp3':'Cinematics.mp3',
 'password_and_stage_clear.mp3':'Password_StageClear.mp3',
 'pilot_select.mp3':'PilotSelect.mp3',
 'title_main_menu.mp3':'Title.mp3',
 'hammer_time_mike_0927.mp3':'HammerTime.mp3',
 'hama_instrumental_0928.mp3':'HAMA_Instrumental.mp3',
 'ratchetman_0925.mp3':'Unused_Ratchetman.mp3',
 'unknownbosstheme_0925.mp3':'Unused_UnknownBossTheme.mp3',
 'unused1 - stage7.mp3':'Unused1.mp3',
 'unused2 - stage8b-p1.mp3':'Unused2.mp3',
 'unused8 - stage5b.mp3':'Unused8.mp3',
 'unused10 - stage4b-oldmix.mp3':'Unused10.mp3',
 'unused11 - stage2b-oldmix.mp3':'Unused11.mp3',
 'unused12 - stage1b-old.mp3':'Unused12.mp3',
}
MOVED = {
 'assets/game/shared/audio/hama_vocals_1001/hama_mike_robot_mix_1001_v3.mp3':'assets/game/shared/audio/music/HAMA.mp3',
 'assets/game/shared/audio/hama_vocals_1001/hama_mike_robot_mix_1001_v2.mp3':'assets/game/music/HAMA_Previous_v2.mp3',
 'assets/game/shared/audio/hama_vocals_1001/hama_mike_robot_mix_1001.mp3':'assets/game/music/HAMA_Previous_v1.mp3',
}
ASSIGN = {'mini4':'Level4mb.mp3','mini6':'Level6mb.mp3','mini7':'Level7mb.mp3',
          'mini9':'Level9mb.mp3','boss8p2':'Level8b2.mp3'}
REMOVE = ['unused13','unused3old','unused_x','unused3','unused5']

def organize():
    replacements = {'assets/game/music/'+old:'assets/game/music/'+new for old,new in NAMES.items()}
    replacements.update(MOVED)
    entries=[]
    for old,new in replacements.items():
        src,dst=R/old,R/new
        assert dst.resolve().is_relative_to(M.resolve())
        if src.exists():
            assert not dst.exists(), new
            digest=hashlib.sha256(src.read_bytes()).hexdigest()
            src.rename(dst)
            assert hashlib.sha256(dst.read_bytes()).hexdigest()==digest
        else:
            assert dst.is_file(), new
            digest=hashlib.sha256(dst.read_bytes()).hexdigest()
        entries.append({'file':new,'formerPath':old,'sha256':digest})
    # Update runtime modules and executable build/probe references while retaining bytes/newlines.
    for folder in ['assets','_BUILD_SOURCE']:
        for p in (R/folder).rglob('*'):
            if p.suffix not in ['.js','.py','.cjs','.json'] or p==Path(__file__) or '_shots' in p.parts:continue
            if p.name=='manifest.js':continue # regenerated below through this owning workflow
            data=p.read_bytes();updated=data
            for old,new in replacements.items():updated=updated.replace(old.encode(),new.encode())
            # Some builders construct music paths from basename strings.
            if folder=='_BUILD_SOURCE':
                for old,new in NAMES.items():updated=updated.replace(old.encode(),new.encode())
            if updated!=data:p.write_bytes(updated)
    p=R/'assets/game.js';data=p.read_bytes()
    for key in REMOVE:
        data=re.sub(rb"  BOFA\.music\."+key.encode()+rb"='[^']*';\n",b'',data)
    marker=b"  BOFA.music.mini5='assets/game/levels/stage_05/audio/music/Level5mb.mp3';"
    if b'BOFA.music.mini4=' not in data:
        extra='\n'.join("  BOFA.music.%s='assets/game/music/%s';"%(k,v) for k,v in ASSIGN.items())
        data=data.replace(marker,marker+b'\n'+extra.encode())
    p.write_bytes(data)
    # BOFA's non-music namespaces are copied unchanged via the existing music-owner parse contract.
    p=R/'assets/manifest.js';src=p.read_text(encoding='utf-8');start=src.index('window.BOFA=')+len('window.BOFA=')
    obj,used=json.JSONDecoder().raw_decode(src[start:]);routes=obj['music']
    for k,v in list(routes.items()):routes[k]=replacements.get(v,v)
    for k in REMOVE:routes.pop(k,None)
    game=(R/'assets/game.js').read_text(encoding='utf-8')
    for k,v in re.findall(r"BOFA\.music\.([\w]+)='([^']+)'",game):routes[k]=v
    routes.update({k:'assets/game/music/'+v for k,v in ASSIGN.items()})
    routes.update({'boss5':'assets/game/levels/stage_05/audio/music/Level5b.mp3','mini2':'assets/game/levels/stage_02/audio/music/Level2mb.mp3',
                  'mini3':'assets/game/levels/stage_03/audio/music/Level3mb.mp3','stagex':'assets/game/levels/stage_x/audio/music/LevelX.mp3',
                  'hammerTime':'assets/game/shared/audio/music/HammerTime.mp3','hama':'assets/game/shared/audio/music/HAMA.mp3',
                  'realm8':'assets/game/levels/stage_08/audio/music/Level8.mp3'})
    assert all((R/v).is_file() for v in routes.values())
    encoded=json.dumps(obj,separators=(',',':'),ensure_ascii=True)
    updated=src[:start]+encoded+src[start+used:]
    # Two legacy image aliases also point to MP3s; retain aliases with their renamed paths.
    for old,new in replacements.items():updated=updated.replace(old,new)
    p.write_text(updated,encoding='utf-8',newline='\n')
    (M/'catalog.json').write_text(json.dumps({'tracks':entries,'routes':routes,
      'notes':{'Level8mb':'Herald shares Level8b; no separate song assigned.',
               'Level8b2':'Hive Helicopter, the second finale form.',
               'Level8b3':'Finale forms 3 through 8 share this score.',
               'Unused_Egypt':'Former Stage 8 field alias; current Stage 8 uses Level8.',
               'HAMA_Previous':'Preserved superseded vocal mixes.'}},indent=2)+'\n',encoding='utf-8')
    print('Organized',len(entries),'music files;',len(routes),'registered routes.')

if __name__=='__main__':organize()
