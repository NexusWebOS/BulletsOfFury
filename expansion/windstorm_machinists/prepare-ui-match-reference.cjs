const fs=require('fs'),path=require('path');
const sharp=require('C:/Users/Mike/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root=__dirname,game=path.resolve(root,'../../output/bof-portable-1006/Two ZIP Launch Test/BulletsOfFury'),source=path.resolve(root,'../../bof-repair-0927');
(async()=>{
 const out=path.join(root,'reference/ui_match_v2');fs.mkdirSync(out,{recursive:true});
 const rects={maverick_box:[2481,842,351,400],freezer_box:[2127,842,352,400],yuri_box:[1041,842,347,405]};
 for(const [name,r]of Object.entries(rects))await sharp(path.join(game,'assets/game/atlas/ui_hud.webp')).extract({left:r[0],top:r[1],width:r[2],height:r[3]}).png().toFile(path.join(out,name+'.png'));
 const atlas=JSON.parse(fs.readFileSync(path.join(source,'assets/game/atlas/bof_player_weapon_special_icons.json')));
 for(const who of ['maverick','freezer','yuri']){const entry=atlas.entries.find(e=>e.key===atlas.aliases['spicon_'+who]);const r=entry.rect;await sharp(path.join(game,'assets/game/atlas/bof_player_weapon_special_icons.webp')).extract({left:r[0],top:r[1],width:r[2],height:r[3]}).png().toFile(path.join(out,who+'_icon.png'));}
 for(const who of ['cole','axel','maverick'])await sharp(path.join(game,'assets/game/pilots_0922/portraits/'+who+'-idle.webp')).png().toFile(path.join(out,who+'_portrait.png'));
 fs.copyFileSync(path.join(source,'assets/game/pilot_avatars/avatar_frame_template_0919.png'),path.join(out,'portrait_frame_template.png'));
 console.log('Extracted current portable-build references; no game assets modified.');
})();
