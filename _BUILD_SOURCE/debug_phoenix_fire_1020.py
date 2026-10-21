from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'_BUILD_SOURCE/film_dracodia_phoenix_1020.py').read_text()
s=s.replace("for phase,attack in [('arms','cannon'),('arms','sweep'),('arms','spin900'),('core','ring'),('core','coreLaser'),('core','rotor'),('core','rollerball'),('head','eyeSweep')]:","for phase,attack in []:")
s=s.replace("movie('live-attack-reel',whole)","# no movie in diagnosis")
s=s.replace("for phase in ['arms','core']:","for phase in ['arms']:")
s=s.replace("run.spaceMode=false;run.wlevels", "window.PDBG=[];const _at=r30At,_hit=modularHit;r30At=function(b,x,y){const out=_at.apply(this,arguments);if(b===B&&out)PDBG.push({event:'contact',id:out.id,x,y});return out;};modularHit=function(dmg){const hp=B.hp,id=B._lastPart?.id;const out=_hit.apply(this,arguments);PDBG.push({event:'damage',id,dmg,loss:hp-B.hp,phase:F.phase});return out;};run.spaceMode=false;run.wlevels")
s=s.replace("frame().save(O/('ordinary-fire-'+phase+'.png'))","frame().save(O/('ordinary-fire-'+phase+'.png'));print(json.dumps(p.evaluate('({events:PDBG.slice(-40),parts:v18Rig(B).map(v=>({id:v.p.id,key:v.key,x:v.x,y:v.y,ax:v.ax,ay:v.ay,rot:v.rot})),player:{x:player.x,y:player.y},f:F.phase})')),flush=True)")
s=s.replace("for cue in ['enemyBossCannon','furnaceFlameIgnite','furnaceLaserCharge','furnaceLaserBurst','shieldBreakCombat']:","for cue in []:")
exec(compile(s,str(R/'_BUILD_SOURCE/film_dracodia_phoenix_1020.py'),'exec'),{'__file__':str(R/'_BUILD_SOURCE/debug_phoenix_fire_1020.py'),'__name__':'__main__'})
