"""Export current native boss art as identity references; never substitutes a renderer."""
import base64, json
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve, GAME

OUT=Path(GAME)/'_shots/stage78_review_1025/source'
OUT.mkdir(parents=True,exist_ok=True)
port,stop=serve(GAME)
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required'])
        page=browser.new_page(viewport={'width':1280,'height':800})
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000)
        page.wait_for_function('window.__bofFrames>5',timeout=180000)
        page.evaluate('s7mWarm();bi24Warm();')
        page.wait_for_function("XART.rdy('s7m_warden')&&XART.rdy('s7m_body')&&bi24Warm()",timeout=180000)
        data=page.evaluate('''()=>{
          const out={};
          const save=(name,c)=>out[name]=c.toDataURL('image/png').split(',')[1];
          for(const [name,i]of Object.entries({frontL:1,frontR:2,rearL:3,rearR:4})){
            const im=s7mCell('warden',i,true),c=document.createElement('canvas');
            c.width=c.height=256;const g=c.getContext('2d');g.imageSmoothingEnabled=false;
            const k=Math.min(204/im.width,224/im.height);g.drawImage(im,128-im.width*k/2,16,im.width*k,im.height*k);
            save(name,c);
          }
          for(const name of ['dracodia_wind','dracodia_strike','dracodia_recover']){
            const a=BI24_ART.banks[name];
            for(let f=0;f<a.count;f++){
              const c=document.createElement('canvas');c.width=c.height=512;
              c.getContext('2d').drawImage(XART.get(a.key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,0,0,512,512);
              save(name+'-'+String(f).padStart(2,'0'),c);
            }
          }
          return out;
        }''')
        for name,b in data.items():(OUT/(name+'.png')).write_bytes(base64.b64decode(b))
        (OUT/'export.json').write_text(json.dumps({'files':list(data),'errors':errors},indent=2))
        print(json.dumps({'exported':len(data),'errors':errors,'out':str(OUT)}))
        browser.close()
finally:stop()
