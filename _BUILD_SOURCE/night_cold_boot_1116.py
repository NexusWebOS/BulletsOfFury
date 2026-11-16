from pathlib import Path
from playwright.async_api import async_playwright
from urllib.parse import urlsplit
import asyncio,json,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116/server';O.mkdir(parents=True,exist_ok=True);label=sys.argv[1]if len(sys.argv)>1 else'before'
async def main():
 async with async_playwright()as w:
  b=await w.chromium.launch(args=['--no-sandbox']);rows=[]
  async def one(n):
   errors=[];failed=[];c=await b.new_context();p=await c.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('requestfailed',lambda q:failed.append({'host':urlsplit(q.url).netloc,'path':urlsplit(q.url).path,'failure':q.failure}))
   try:
    await p.goto('http://127.0.0.1:8765/index.html?night-cold='+str(n),timeout=180000);await p.wait_for_function('window.__bofFrames>6&&typeof CQA16!=="undefined"&&typeof NQA16!=="undefined"',timeout=180000);q=await p.evaluate('({state,frames:__bofFrames,cinemaVersion:CQA16.version,paddedPages:NQA16.length})')
   except Exception as e:q={'exception':str(e)}
   row={'context':n,'state':q,'errors':errors.copy(),'failed':failed.copy(),'ok':not errors and not failed and 'exception'not in q};rows.append(row);await c.close();print(json.dumps(row),flush=True)
  await asyncio.gather(*(one(n)for n in range(4)));await b.close()
 (O/(label+'.json')).write_text(json.dumps({'rows':rows,'scope':'Four fresh isolated browser contexts loading the complete current shipping index concurrently on the local game server. No gameplay, scores or account operations.'},indent=2),encoding='utf8')
asyncio.run(main())
