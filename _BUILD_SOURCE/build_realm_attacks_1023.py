from pathlib import Path
from PIL import Image,ImageFilter
import json,hashlib,shutil,sys
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/realm_attacks_1023';W.mkdir(exist_ok=True);O=W/'shipping';O.mkdir(exist_ok=True)
families={'deathorb':(['s8deathorb','s8bomber'],[[33,91],[93,91]],'1558d1c2-eb9a-4e8b-b4ac-1337e4670edc'),'carrier':(['s8carrier','s8tentacle'],[[33,86],[94,86]],'3d5c0b49-dde8-425c-acb1-a2719c0672a4')}
for family,(types,sockets,job)in families.items():
 reference=Image.open(W/f'fleet-{family}-raw/00.png').convert('RGBA');mask=reference.getchannel('A').filter(ImageFilter.MaxFilter(7));frames=[]
 for f in range(17):
  raw=Image.open(W/f'fleet-{family}-raw/{f:02}.png').convert('RGBA');raw.putalpha(Image.fromarray(__import__('numpy').minimum(__import__('numpy').array(raw.getchannel('A')),__import__('numpy').array(mask))));frames.append(raw)
 for typ in types:
  unit=M[typ]['unit'];dim=round(128*unit);canvas=384;sheet=Image.new('RGBA',(canvas*4,canvas*5))
  for f,raw in enumerate(frames):
   frame=raw.resize((dim,dim),Image.Resampling.NEAREST);sheet.alpha_composite(frame,(f%4*canvas+(canvas-dim)//2,f//4*canvas+(canvas-dim)//2))
  for suffix,im in [('',sheet),('_hit',Image.new('RGBA',sheet.size,'white'))]:
   if suffix:im.putalpha(sheet.getchannel('A'))
   name=typ+suffix+'.webp';im.save(O/name,lossless=True,exact=True);key='at23_'+typ+suffix;A['sheets'][key]={'key':key,'path':'assets/game/levels/stage_08/enemies/realm_attacks_1023/'+name,'sha256':hashlib.sha256((O/name).read_bytes()).hexdigest()}
  A['models'][typ]={'key':'at23_'+typ,'white':'at23_'+typ+'_hit','frames':17,'cell':canvas,'pivot':[192,192],'unit':unit,'nativeSpan':M[typ]['nativeSpan'],'sockets':sockets,'job':job,'family':family}
runtime='''"use strict";
/* Accepted PixelLab charge / recoil / recovery. Generated detached beam tails
   are excluded offline. Native bullets remain the sole damaging ordnance.
   Stored world-space socket offsets are shared by release and its exact FOV. */
const AT23_ART=__ART__,AT23={actor:null,target:null,follow:false,warning:false,events:[],base:{draw:drawS8Mega,tick:s8MegaTick,shot:fr27RealmShot,point:combatHardpoint,warn:combatWarningDraw,load:stageLoadBegin}};
for(const a of Object.values(AT23_ART.sheets))XART._src[a.key]=a.path;
stageLoadBegin=function(n,keys){return AT23.base.load.call(this,n,[...(keys||[]),...(n===8?Object.keys(AT23_ART.sheets):[])]);};
function at23Socket(e,index){const m=AT23_ART.models[e.type],p=m.sockets[index%2];return{x:e.x+(p[0]-64)*m.unit,y:e.y+(p[1]-64)*m.unit};}
function at23Warm(){return diffKey==='easy'?1.25:[1,.85,.72][fr27Difficulty()];}
function at23Own(e){return run.stage===8&&!!AT23_ART.models[e?.type]&&!e._d20&&!e._ll18;}
combatWarningDraw=function(owner,q){if(at23Own(owner)&&owner._frRealmAI&&!AT23.warning)return;return AT23.base.warn.apply(this,arguments);};
combatHardpoint=function(e,ox,oy){if(!at23Own(e))return AT23.base.point.apply(this,arguments);if(ox<-.01)return at23Socket(e,0);if(ox>.01)return at23Socket(e,1);const m=AT23_ART.models[e.type];return{x:e.x,y:e.y+44*m.unit};};
s8MegaTick=function(e,dt){const old=AT23.actor,target=AT23.target,follow=AT23.follow,A=e._frRealmAI,Q=A?.ap10Follow;AT23.actor=at23Own(e)?e:null;AT23.follow=!!Q&&!A?.tell;AT23.target=A?.tell?{x:A.tell.x,y:A.tell.y}:Q?.target||null;if(AT23.actor&&Q){const p=at23Socket(e,1);Q.x=p.x;Q.y=p.y;}
 try{const result=AT23.base.tick.apply(this,arguments),next=e._frRealmAI?.ap10Follow;if(AT23.actor&&next&&!next._at23Port){const p=at23Socket(e,1);next.x=p.x;next.y=p.y;next._at23Port=true;}return result;}finally{AT23.actor=old;AT23.target=target;AT23.follow=follow;}};
fr27RealmShot=function(x,y,angle,speed,row){const e=AT23.actor,m=e&&AT23_ART.models[e.type],T=AT23.target;
 if(!m||!T)return AT23.base.shot.apply(this,arguments);
 if(AT23.follow){const offset=angle-Math.atan2(T.y-y,T.x-x),p=at23Socket(e,1);x=p.x;y=p.y;angle=Math.atan2(T.y-y,T.x-x)+offset;}
 const A=e._frRealmAI,result=AT23.base.shot.call(this,x,y,angle,speed,row),ports=[at23Socket(e,0),at23Socket(e,1)],distance=ports.map(p=>Math.hypot(p.x-x,p.y-y)),port=distance[0]<distance[1]?0:1;e._at23Fired=efxClock;
 AT23.events.push({type:e.type,seq:A.seq,round:A.tell?.fired,follow:AT23.follow,port,x,y,aim:angle,speed,row,target:{...T},socketError:Math.min(...distance),clock:efxClock});if(AT23.events.length>160)AT23.events.shift();return result;
};
drawS8Mega=function(e){const m=AT23_ART.models[e.type];if(!at23Own(e))return AT23.base.draw.apply(this,arguments);
 const a=e._frRealmAI,warm=at23Warm(),target=targetShip(e.x,e.y),liveTell=a?.tell&&a.tell.t<warm&&e.y<=target.y-65&&e.y>=viewTopY()+e.h*.5,follow=a?.ap10Follow,age=efxClock-(e._at23Fired??-999),f=liveTell?Math.min(11,Math.floor(a.tell.t/warm*12)):follow?Math.min(11,8+Math.floor((.35-follow.left)/.35*4)):age<.4?Math.min(16,12+Math.floor(age/.08)):0,key=e.flash>0?m.white:m.key;
 if(!XART.rdy(key))return false;const im=XART.get(key),s=m.cell,size=Math.max(e.w,e.h)*1.28;e._drawW=size*.82;e._drawH=size;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,f%4*s,Math.floor(f/4)*s,s,s,Math.round(e.x-192),Math.round(e.y-192),s,s);
 if(liveTell){const lanes=[],row=fr27RealmRow(e);if(row===1){for(let i=0;i<2;i++){const side=i%2?-1:1,p=at23Socket(e,side>0?1:0);lanes.push({...p,angle:Math.atan2(a.tell.y-p.y,a.tell.x-p.x)+side*.22});}}
  else{const p=at23Socket(e,1),aim=Math.atan2(a.tell.y-p.y,a.tell.x-p.x),step=TAU/9;for(let i=0;i<9;i++){const angle=i*step;if(Math.abs(Math.atan2(Math.sin(angle-aim),Math.cos(angle-aim)))>=step*1.25)lanes.push({...p,angle});}}
  const old=AT23.warning;AT23.warning=true;try{for(const p of lanes){const len=viewH()*1.5;combatWarningDraw(e,{x:p.x,y:p.y,ex:p.x+Math.cos(p.angle)*len,ey:p.y+Math.sin(p.angle)*len,progress:a.tell.t/warm,width:row===1?32:28,fieldOnly:true});}}finally{AT23.warning=old;}}
 if(follow){const old=AT23.warning;AT23.warning=true;try{const a=Math.atan2(follow.target.y-follow.y,follow.target.x-follow.x),len=viewH()*1.5;for(const d of [-.11,.11])combatWarningDraw(e,{x:follow.x,y:follow.y,ex:follow.x+Math.cos(a+d)*len,ey:follow.y+Math.sin(a+d)*len,progress:1-follow.left/.35,width:28,fieldOnly:true});}finally{AT23.warning=old;}}
 return true;
};
window.BOF_REALM_ATTACKS=AT23;
'''.replace('__ART__',json.dumps(A,separators=(',',':')))
(O/'realm_attacks_1023.js').write_text(runtime,encoding='utf-8');(O/'manifest.json').write_text(json.dumps(A,indent=2))
if '--install'in sys.argv:
 T=R/'assets/game/levels/stage_08/enemies/realm_attacks_1023';T.mkdir(parents=True,exist_ok=True)
 for p in O.glob('*.webp'):shutil.copy2(p,T/p.name)
 shutil.copy2(O/'manifest.json',T/'manifest.json');shutil.copy2(O/'realm_attacks_1023.js',R/'assets/realm_attacks_1023.js');p=R/'index.html';s=p.read_bytes();nl=b'\r\n'if b'\r\n'in s else b'\n'
 if b'realm_attacks_1023.js'not in s:s=s.replace(b'</body>',b'<script src="assets/realm_attacks_1023.js?v=at23-2"></script>'+nl+b'</body>')
 s=s.replace(b'realm_attacks_1023.js?v=at23-1',b'realm_attacks_1023.js?v=at23-2');p.write_bytes(s)
print(json.dumps({'types':list(A['models']),'frames':sum(m['frames']for m in A['models'].values()),'canonicalUnits':[m['unit']for m in A['models'].values()]}))
