from pathlib import Path
import sys,json,base64
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;V=W/'references';V.mkdir(exist_ok=True,parents=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve
from barrage_review_common_1025 import boot
from playwright.sync_api import sync_playwright
errors=[];inventory={};port,stop=serve(str(R))
def save(p,name,expression):
 result=p.evaluate(expression);data=result.pop('png');(V/(name+'.png')).write_bytes(base64.b64decode(data.split(',')[1]));inventory[name]=result
key_export="""key=>{if(!XART.rdy(key))throw new Error('Not ready '+key);const im=XART.get(key),c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.drawImage(im,0,0);return{key,size:[c.width,c.height],png:c.toDataURL('image/png')}}"""
pose_export="""q=>{const a=q.a,bank=RD74_ART.banks[a.bank],c=document.createElement('canvas');c.width=a.w;c.height=a.h;const g=c.getContext('2d');g.imageSmoothingEnabled=false;const im=XART.get(a.key);if(bank)g.drawImage(im,a.frame%bank.cols*bank.cw,Math.floor(a.frame/bank.cols)*bank.ch,bank.cw,bank.ch,0,0,c.width,c.height);else g.drawImage(im,0,0,c.width,c.height);return{bank:a.bank,key:a.key,frame:a.frame,size:[c.width,c.height],pivot:a.pivot,muzzle:a.muzzle,tip:a.tip,png:c.toDataURL('image/png')}}"""
try:
 with sync_playwright()as pw:
  for stage in [5,8]:
   br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,stage,errors,'boss')
   p.wait_for_function('(s)=>{stageLoadTick();if(stageLoadReady(s))updatePlay(0);return stageLoadReady(s)&&!bp119Pending()}',arg=stage,timeout=180000)
   p.wait_for_function('(s)=>{stageLoadTick();return ba119Warm(s)}',arg=stage,timeout=180000)
   p.evaluate("()=>{BOFCinematicDirector.cancel();window.B=boss;DBGT.god=true;player.invuln=1e9;}")
   if stage==5:
    for mat in ['regular','chrome']:
     save(p,'chronos-ready-'+mat,"()=>{const q=ba119Pose('blue-overhead',0,'"+mat+"');return("+pose_export+")(q)}")
    p.wait_for_function("()=>XART.rdy('arch_ship_transform')&&Object.values(CH23_ART.sheets).map(a=>XART.rdy(a.key)).every(Boolean)&&XART.rdy(HB20_PICKUP.box)&&XART.rdy(HB20_PICKUP.icon)",timeout=180000)
    for name,key in [('legacy-ship-sheet','arch_ship_transform'),('approved-icon-box','hb20_chaingun_crate_exclusive'),('approved-gun-icon','hb20_chaingun_icon_exclusive')]:
     save(p,name,'()=>('+key_export+')('+json.dumps(key)+')')
    for bank in ['body','barrel','hands']:
     save(p,'chronos-gun-'+bank,"()=>{const a=ch23Cell('"+bank+"',B,0);return("+key_export+")(a.key)}")
    inventory['chaingun-spec']=p.evaluate("()=>({gunSocket:CH23_ART.gunSocket,muzzle:CH23_ART.muzzle,body:CH23_ART.banks.body[0],barrel:CH23_ART.banks.barrel[0],keys:Object.keys(HT23_ART.banks)})")
    p.evaluate("()=>{hammerState(B,'unfold');B._hammer.t=1;drawWorld(0);SC12.refresh();__bofFit();}");p.screenshot(path=str(V/'legacy-chronos-transformation-native.png'))
   else:
    p.evaluate("()=>{v18Enter(B,2,8);B._r30.mode='fight';B._r30.v18.donorAge=0;B.enter=B._noHit=B.dead=false;window.Q=hb20State(B);}")
    for mat in ['regular','chrome']:
     save(p,'draconus-ready-'+mat,"()=>{Q.chrome="+str(mat=='chrome').lower()+";Q.rage=false;return("+pose_export+")(ba119Corrupt(Q,0))}")
    p.wait_for_function("()=>Object.entries(RD74_ART.banks).filter(([n])=>/^(gun|pickup|empty)_/.test(n)).map(([,a])=>XART.rdy(a.key)).every(Boolean)",timeout=180000)
    for bank in ['gun_chrome','pickup_chrome']:
     for frame in [0,8,16]:
      save(p,'legacy-draconus-'+bank+'-'+str(frame),"()=>{return("+pose_export+")(rd74Sample('"+bank+"',"+str(frame)+"))}")
    inventory['draconus-spec']=p.evaluate("()=>({banks:Object.fromEntries(Object.entries(RD74_ART.banks).filter(([n])=>/^(gun|pickup|empty)_/.test(n))),crate:RD74_ART.effects.crate,parts:Q.parts.map(p=>({id:p.id,hp:p.hp,max:p.max})),modes:Object.keys(boss._r30.v18)})")
    p.evaluate("()=>{hb20Start(B,'gun');Q.action.t=Q.action.tell+1;drawWorld(0);SC12.refresh();__bofFit();}");p.screenshot(path=str(V/'legacy-draconus-gun-native.png'))
   br.close();print('Exported native references for Stage'+str(stage),flush=True)
finally:stop()
(V/'native-reference-inventory.json').write_text(json.dumps(dict(art=inventory,errors=errors),indent=2));assert not errors,errors
print('Saved original live boss, ship, gun and icon-box pixels.',flush=True)
