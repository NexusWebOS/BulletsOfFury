from pathlib import Path
import sys,os,json
from playwright.sync_api import sync_playwright
R=Path(os.environ.get('BOF_REPO',str(Path(__file__).resolve().parents[1])))
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/formation_palettes_1013';O.mkdir(parents=True,exist_ok=True)
os.environ['PLAYWRIGHT_BROWSERS_PATH']='C:/Users/Mike/AppData/Local/ms-playwright'
port,stop=shoot.serve(str(R));checks=[];errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport={'width':1440,'height':1000})
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4',timeout=120000);p.evaluate(shoot.TRAP_RAF)
  for stage in [1,4,6]:
   p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True})
   p.wait_for_function('n=>{stageLoadTick();return stageLoadReady(n)&&[...FBP13.keys].filter(x=>x[1]===n).every(x=>XART.rdy(x[0]))}',arg=stage,timeout=120000)
   stats=p.evaluate('''n=>{
    const results=[];
    for(const [key,stage]of FBP13.keys){if(stage!==n)continue;
     const original=BOF_FORMATION_PALETTES.source(key),im=XART.get(key),a=document.createElement('canvas');a.width=im.width;a.height=im.height;
     const c=a.getContext('2d');c.drawImage(original,0,0);const src=c.getImageData(0,0,a.width,a.height).data;
     c.clearRect(0,0,a.width,a.height);c.drawImage(im,0,0);const dst=c.getImageData(0,0,a.width,a.height).data;
     let alpha=true,changed=0,solid=0;for(let i=0;i<src.length;i+=4){alpha=alpha&&src[i+3]===dst[i+3];if(src[i+3])solid++;if(src[i+3]&&(src[i]!==dst[i]||src[i+1]!==dst[i+1]||src[i+2]!==dst[i+2]))changed++;}
     const builds=FBP13.builds;for(let i=0;i<120;i++)XART.get(key);
     results.push({key,stage,width:im.width,height:im.height,alpha,changed,solid,stable:builds===FBP13.builds&&XART.get(key)===im});
    }
    return {sheets:results,bytes:FBP13.bytes};
   }''',stage)
   for row in stats['sheets']:
    assert row['alpha'] and row['stable'] and row['changed']>100 and row['width']%2==0 and row['height']%2==0,row
   assert stats['bytes']<3*1024*1024,stats
   checks.append(stats)
   p.evaluate('''()=>{story=null;s6Opening=null;s6Wing=null;run._mission29OpeningDone=true;debugFight=null;waveIdx=999;spawnClock=9999;subBossTriggered=true;subBossDone=true;subBossActive=false;bossActive=false;warnT=0;if(wfx)wfx.fseq=null;stageTimer=1;VP12.next=9999;CP12.next=9999;Input.keys={};player.dead=false;player.invuln=1e9+2;EP13.next=9999;enemies=[];eBullets=[];pBullets=[];VP12.groups=[];vp12Spawn('barrel');}''')
   for i in range(4):assert p.evaluate(shoot.STEP,30) is None
   p.screenshot(path=str(O/f'stage{stage}-native.png'))
   p.evaluate('''n=>{let panel=document.createElement('div');panel.id='palette-review';panel.style='position:fixed;inset:0;background:#16212b;z-index:999999;padding:24px;color:white;font:18px monospace';document.body.append(panel);
    const d=AM13_ART['flight_variant_'+n];for(const kind of ['heading','roll']){const m=d[kind],row=document.createElement('div');row.textContent='STAGE '+n+' '+kind.toUpperCase()+' — SOURCE / LIVE PALETTE';panel.append(row);const canvas=document.createElement('canvas');canvas.width=1280;canvas.height=280;row.append(canvas);const c=canvas.getContext('2d');c.imageSmoothingEnabled=false;
     for(let j=0;j<8;j++)for(let k=0;k<2;k++){const im=k?XART.get(m.key):BOF_FORMATION_PALETTES.source(m.key),f=kind==='roll'?j*2:j;c.drawImage(im,f*m.cell,0,m.cell,m.cell,j*160,k*136,128,128);}
    }}''',stage)
   p.screenshot(path=str(O/f'stage{stage}-palette-review.png'));p.evaluate("document.getElementById('palette-review').remove()")
  p.evaluate('()=>{fbp13Clear()}');assert p.evaluate('FBP13.bytes===0&&FBP13.cache.size===0')
  b.close()
finally:stop()
report={'checks':checks,'errors':errors,'scope':'12 authored heading/roll/fallback sheets; native stages1/4/6; exact alpha, even geometry, cache reuse and retirement'}
(O/'verification.json').write_text(json.dumps(report,indent=2));assert not errors,errors
print(json.dumps({'sheets':sum(len(q['sheets']) for q in checks),'errors':errors,'bytes':[q['bytes'] for q in checks]}))
