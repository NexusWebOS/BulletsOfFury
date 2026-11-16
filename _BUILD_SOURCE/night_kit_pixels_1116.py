from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,base64
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/kit';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':900});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8765/index.html?kd18final');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>BOFOnline.submitScore=()=>{}');p.wait_for_function("()=>{kd18Warm();return ['cd27_neutral_460',...PILOTS.map(p=>'pav_'+p.key)].every(k=>XART.rdy(k));}")
 for pk in p.evaluate('PILOTS.map(p=>p.key)'):
  q=p.evaluate("""pk=>{setState(GS.LAUNCH);ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=1;ctx.fillStyle='#183b61';ctx.fillRect(0,0,VW,VH);
   let expected=null,rect=null;const prior=ui20Portrait;
   ui20Portrait=function(g,key,r){rect=r;expected=document.createElement('canvas');expected.width=cv.width;expected.height=cv.height;const e=expected.getContext('2d');e.drawImage(cv,0,0);e.setTransform(ctx.getTransform());e.imageSmoothingEnabled=false;e.globalAlpha=ctx.globalAlpha;
    const im=XART.get('pav_'+pk),k=Math.min(r.w/im.width,r.h/im.height),w=im.width*k,h=im.height*k;e.beginPath();e.rect(r.x,r.y,r.w,r.h);e.clip();e.drawImage(im,r.x+(r.w-w)/2,r.y+(r.h-h)/2,w,h);return prior.apply(this,arguments);};
   try{dlgBox({who:pk.toUpperCase(),full:'We are ready for launch.',shown:'We are ready for launch.',forceShown:true,y:12,screenSpace:false});}finally{ui20Portrait=prior;}
   const a=KD18.radio,ex=expected.getContext('2d').getImageData(0,0,cv.width,cv.height).data,ac=ctx.getImageData(0,0,cv.width,cv.height).data;let total=0,bad=0;
   for(let y=Math.ceil(rect.y*SS);y<Math.floor((rect.y+rect.h)*SS);y++)for(let x=Math.ceil(rect.x*SS);x<Math.floor((rect.x+rect.w)*SS);x++){const i=(y*cv.width+x)*4;total++;if(ex[i]!==ac[i]||ex[i+1]!==ac[i+1]||ex[i+2]!==ac[i+2]||ex[i+3]!==ac[i+3])bad++;}return {avatar:a.avatar,total,bad,frame:a.frame};}""",pk)
  checks.append({'name':pk+' native portrait pixels match selection avatar','ok':q['bad']==0 and q['total']>10000,'data':q})
 for st in ['OPENING','CUTSCENE','VICTORY']:
  for width in [480,912]:
   q=p.evaluate("""([st,W])=>{setState(GS[st]);cv.width=W*SS;cv.height=512*SS;ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#16324a';ctx.fillRect(0,0,W,512);const full='The prototype kit is ready. We are tracing the signal back to its source.';inv20Text('COLE',full,W,512,full.length);return {r:KD18.radio,ui:UI20.dialogue,tw:dlgBox._tw};}""",[st,width])
   a=q['r']['frame'];checks.append({'name':st+' '+str(width)+' shared proportional frame is centered and bounded','ok':abs(a['w']/a['h']-460/84)<.001 and a['x']>=0 and a['x']+a['w']<=width and a['y']+a['h']<=512 and q['ui']['w']==a['w'],'data':a})
   (O/(st.lower()+'-'+str(width)+'-caption.png')).write_bytes(base64.b64decode(p.evaluate("cv.toDataURL('image/png')").split(',')[1]))
 checks.append({'name':'no final viewport browser errors','ok':not errors,'data':errors});b.close()
(O/'final-native-qa.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf8');print(sum(x['ok']for x in checks),'/',len(checks),'final native checks');assert all(x['ok']for x in checks)
