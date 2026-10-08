"""Read-only native frame audit; output is QA evidence, never replacement art."""
from pathlib import Path
import json,sys,base64
from playwright.sync_api import sync_playwright
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/projectiles_1007/before';O.mkdir(parents=True,exist_ok=True)
report={'errors':[]};port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);c=br.new_context(viewport={'width':1100,'height':950})
  c.route('**/*',lambda r:r.continue_() if r.request.url.startswith(('http://127.0.0.1:','data:','blob:')) else r.abort())
  p=c.new_page();p.on('pageerror',lambda e:report['errors'].append(str(e)));p.on('console',lambda m:report['errors'].append(m.text[:500]) if m.type=='error' and ('127.0.0.1' in m.text or 'ERR_' not in m.text) else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.add_script_tag(path=str(R/'_BUILD_SOURCE/balance_lab_1007.js'))
  p.evaluate("()=>{BAL7.setup({stage:8,kind:'heralddeath',mini:true,diff:'furious',pilot:'yuri',level:3,seed:1007,seconds:1});player.invuln=99999;}")
  keys=p.evaluate("""()=>{
   const set=new Set(Object.keys(BOFX.cells||{}).concat(Object.keys(XART._src)).filter(k=>/^(nhd_(primary|special)_projectile_|bfx_.+_p_|l23fx_|mgcf_|mfx_(ea|hom|emr|mg)_)/.test(k)));
   for(let st=1;st<=9;st++){run.stage=st;for(const F of Object.values(FIRETYPES))if(F.art)for(let i=0;i<24;i++){try{const key=F.art({t:i/24,kind:'pellet',pal:'red',vx:0,vy:2});if(key)set.add(key);}catch(e){}}}
   for(const k of set)XART.rdy(k);return [...set].filter(k=>XART._src[k]||BOFX.cells?.[k]);
  }""")
  print('KEYS',len(keys),flush=True)
  p.wait_for_function('(ks)=>ks.every(k=>XART.rdy(k))',arg=keys,timeout=120000,polling=100)
  report['frames']=p.evaluate("""ks=>ks.map(key=>{
   const im=XART.get(key),w=im.naturalWidth||im.width,h=im.naturalHeight||im.height,cv=document.createElement('canvas');cv.width=w;cv.height=h;const g=cv.getContext('2d',{willReadFrequently:true});g.drawImage(im,0,0);const d=g.getImageData(0,0,w,h).data;
   let left=w,right=-1,top=h,bottom=-1,n=0,sx=0,sy=0,edge=0,bright=0,bx=0,by=0;
   for(let y=0;y<h;y++)for(let x=0;x<w;x++){const i=(y*w+x)*4;if(d[i+3]<32)continue;n++;sx+=x;sy+=y;left=Math.min(left,x);right=Math.max(right,x);top=Math.min(top,y);bottom=Math.max(bottom,y);if(x===0||y===0||x===w-1||y===h-1)edge++;if(Math.max(d[i],d[i+1],d[i+2])>180&&d[i+3]>200){bright++;bx+=x;by+=y;}}
   return {key,size:[w,h],bounds:n?[left,top,right+1,bottom+1]:null,pixels:n,edge,centroid:n?[sx/n,sy/n]:null,bright:bright?[bx/bright,by/bright]:null,cell:BOFX.cells?.[key],source:XART._src[key],pi:window.BOFPI?.[key]};
  })""",keys)
  # Exact source-cell contact; layout/labels are QA only.
  for kind in ['primary','special']:
   data=p.evaluate("""kind=>{const cv=document.createElement('canvas');cv.width=1200;cv.height=230;const g=cv.getContext('2d');g.fillStyle='#17202b';g.fillRect(0,0,cv.width,cv.height);g.font='15px monospace';g.imageSmoothingEnabled=false;for(let i=0;i<6;i++){const key='nhd_'+kind+'_projectile_'+i,im=XART.get(key);g.fillStyle='#354354';g.fillRect(i*200+4,24,192,192);g.drawImage(im,i*200+4,24,192,192);g.fillStyle='#ffffff';g.fillText(kind+' '+i,i*200+7,18);}return cv.toDataURL().split(',')[1];}""",kind)
   (O/f'herald-{kind}-source.png').write_bytes(base64.b64decode(data))
  # Real Herald combat sequence and actual draw dispatch.
  p.evaluate("""()=>{run.stage=8;window.AUDITKEYS={};const get=XART.get;XART.get=function(k){AUDITKEYS[k]=(AUDITKEYS[k]||0)+1;return get.apply(this,arguments);};}""")
  for f in range(720):
   p.evaluate('()=>{player.invuln=99999;updatePlay(1/60);drawWorld(1/60);}')
   if f in [80,140,200,280,420,580,719]:
    image=p.evaluate('()=>cv.toDataURL().split(",")[1]');(O/f'herald-live-{f}.png').write_bytes(base64.b64decode(image))
  report['heraldDrawKeys']=p.evaluate('()=>AUDITKEYS')
  report['registry']=p.evaluate('()=>({stages:STAGES.map((s,i)=>({stage:i+1,boss:s.boss})),minis:SUBBOSS,firetypes:Object.keys(FIRETYPES),proj:Object.keys(PROJ)})')
  br.close()
finally:stop()
(O/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'frames':len(report.get('frames',[])),'errors':report['errors'],'out':str(O)}),flush=True)
