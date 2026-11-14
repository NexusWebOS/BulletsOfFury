from pathlib import Path
import json,hashlib
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;C=W/'candidate';C.mkdir(exist_ok=True);O=W.parents[1]/'outputs/snake-assault';p=R/'assets/sumpjaw_tandem_1105.js';live=p.read_bytes();bk=C/'before.js';before=bk.read_bytes()if bk.exists()else live;assert live==before or live==(C/p.name).read_bytes(),'Concurrent snake edits'
if not bk.exists():bk.write_bytes(before)
s=before.decode();art=json.loads((O/'art.json').read_text());init="const SA123={art:"+json.dumps(art,separators=(',',':'))+",speeds:[430,560,700,880],modes:new Set(['side-warn','side-run','dig-approach','burrow','underground','emerge','arch','arch-land','arch-exit']),draws:{},warningDraws:0};\nfor(const[k,a]of Object.entries(SA123.art))XART._src['sa123_'+k]=a.path;\n"
s=s.replace('sj98Ready=function(){',init+'sj98Ready=function(){if(!Object.keys(SA123.art).map(k=>XART.rdy(\'sa123_\'+k)).every(Boolean))return false;',1)
s=s.replace("a._sj120?!a.dead&&a.phase!=='entry'", "a._sj120?!a.dead&&!a.underground&&a.phase!=='entry'",1)
s=s.replace('function sj120Shoot(b,a){','function sj120Shoot(b,a,angle=Math.PI/2,speed=5.2){',1)
s=s.replace("if(a.dead||a.stun>0)return;const m=sj98Socket(a,'heart');", "if(a.dead||a.underground||a.stun>0)return;const m=sj98Socket(a,'heart');",1)
s=s.replace("Math.abs(player.x-m.x)<52&&player.y>=m.y-15&&player.y<m.y+86", "Math.abs(-(player.x-m.x)*Math.sin(angle)+(player.y-m.y)*Math.cos(angle))<52&&((player.x-m.x)*Math.cos(angle)+(player.y-m.y)*Math.sin(angle))>=-15&&((player.x-m.x)*Math.cos(angle)+(player.y-m.y)*Math.sin(angle))<86",1)
s=s.replace("eShootT(m.x,m.y,Math.PI/2,5.2,'s7acid'", "eShootT(m.x,m.y,angle,speed,'s7acid'",1)
s=s.replace("angle:Math.PI/2,speed:5.2", "angle,speed,heading:a.heading",1)
s=s.replace("!['hop','split','row-fire'].includes(a.phase)", "a.underground||!['hop','split','row-fire','side-run','arch','arch-land'].includes(a.phase)",1)
s=s.replace("if(((player.x-m.x)/32)**2+((player.y-m.y)/18)**2<1)", "if((['side-run','arch','arch-land'].includes(a.phase)?s81003Distance123(player.x,player.y,a.prevMouth||m,m)<26:((player.x-m.x)/32)**2+((player.y-m.y)/18)**2<1))",1)
# Use the project's existing swept-point helper without changing legacy contacts.
s=s.replace('s81003Distance123(player.x,player.y,a.prevMouth||m,m)', 's81003Distance123(player.x,player.y,a.prevMouth||m,m)')
idx=s.index('// Continuous locomotion');helper=(W/'pattern.js').read_text();helper+="\nfunction s81003Distance123(x,y,p,q){const dx=q.x-p.x,dy=q.y-p.y,u=clamp(((x-p.x)*dx+(y-p.y)*dy)/Math.max(.0001,dx*dx+dy*dy),0,1);return Math.hypot(x-p.x-u*dx,y-p.y-u*dy);}\n";s=s[:idx]+helper+'\n'+s[idx:]
s=s.replace("a.jaw=0;a.mouthLevel=0;a.phase=C.mode;a.t=C.t;", "a.prevMouth=sj98Socket(a,'heart');a.jaw=0;a.mouthLevel=0;a.phase=C.mode;a.t=C.t;",1)
s=s.replace("if(C.mode==='entry'){a.phase='entry';", "if(sj123Motion(b,a,dt)){}else if(C.mode==='entry'){a.phase='entry';",1)
s=s.replace("if(C.mode==='entry'){C.hop=0;", "if(sj123Next(b))return;\n if(C.mode==='entry'){C.hop=0;",1)
s=s.replace("else if(C.mode==='north'){if(live===2)sj120StartCross(b);else sj120Return(b);}", "else if(C.mode==='north')sj123Side(b,0);",1)
s=s.replace("C.t+=dt*(ng27On()?1.15:1);", "C.t+=dt*(ng27On()?1.15:1);sj123Tick(b,dt);",1)
s=s.replace("if(lost){sj120Log", "if(lost){sj123Cancel(b);sj120Log",1)
s=s.replace("if(SJ120.owner){for(const q", "if(SJ120.owner){sj123Cancel(SJ120.owner);for(const q",1)
start=s.index('function sj122Segments');end=s.index('function sj120Warnings',start)
s=s[:start]+'''function sj122Segments(a){a.segments=SJ122.stations.map(d=>{let p,n,type=d<42?0:d<90?1:d<132?2:d<170?3:d<205?4:5,hidden=a.underground&&a.phase==='underground';if(a.feed!=null){const D=d-a.feed;if(D<0){const neck=sj120Neck(a),u=clamp(-D/110,0,1);p={x:lerp(neck.x,a.x,u),y:lerp(neck.y,a.gy+64,u),h:0};n=0;hidden=-D>100;}else{p=sr110SnakePoint(a,D);n=((Math.round(a.heading/TAU*32)%32)+32)%32;}}else{p=sr110SnakePoint(a,d);const lead=sr110SnakePoint(a,Math.max(0,d-3)),tail=sr110SnakePoint(a,d+3),angle=Math.atan2(-(lead.x-tail.x),lead.y-tail.y);n=((Math.round(angle/TAU*32)%32)+32)%32;if(a.emergeTravel!=null&&a.emergeTravel<d+35)hidden=true;}return{...p,n,type,d,hidden};});}
function sj120Segments(a,shadow){if(!a.segments)sj122Segments(a);for(let i=a.segments.length-1;i>=0;i--){const p=a.segments[i];if(p.hidden)continue;sr110Blit('rib'+p.type+'-'+(shadow?'shadow':a.flash>0?'hit':'body'),p.n,p.x,p.y+(shadow?12:-p.h));}}
''' +s[end:]
s=s.replace("sj120Warnings(b);\n", "sj120Warnings(b);sj123Warnings(b);\n",1)
s=s.replace("ss116Blit('head_shadow',ss116Frame(a)%32,a.x,a.gy+12);", "if(!a.underground&&!a.buryDepth)ss116Blit('head_shadow',ss116Frame(a)%32,a.x,a.gy+12);",1)
s=s.replace("for(const a of [...G.actors].sort", "sj123Holes(b,false);\n for(const a of [...G.actors].sort",1)
s=s.replace(";ss116Blit(white?'hit':'body'+sj98State(a)", ";if(!sj123Head(b,a,white))ss116Blit(white?'hit':'body'+sj98State(a)",1)
s=s.replace("if(!white&&!a.dead&&a.mouthLevel>0)", "if(!white&&!a.dead&&!a.underground&&!a.buryDepth&&a.mouthLevel>0)",1)
s=s.replace("if(!a.dead&&a.flashFx>0)", "if(!a.dead&&!a.underground&&!a.buryDepth&&a.flashFx>0)",1)
s=s.replace("for(const f of G.fragments)sj98Blit", "sj123Holes(b,true);\n for(const f of G.fragments)sj98Blit",1)
(C/p.name).write_text(s,encoding='utf-8',newline='\n');m={'expected_source_hash':hashlib.sha256(live).hexdigest(),'art':art,'source':'existing Sumpjaw identity/direction/hit art; new generated sewer-burrow sheet; existing native arrow silhouette','changes':['Four warned alternating side runs at430/560/700/880px per second','Head follows actual travel heading and fires rapid forward toxic orbs','Complete source-pixel burrow with sequential body entry','Two committed emergence points and staggered arches over the player','Existing native HP/gills/solo/death and earlier jumps retained'],'sprite_frames':448,'notes':'Explicit user request supersedes older no-arrow warning preference for these side runs only.'};(O/'manifest.json').write_text(json.dumps(m,indent=2));print('Prepared accelerating slither/burrow/paired-arch director')
