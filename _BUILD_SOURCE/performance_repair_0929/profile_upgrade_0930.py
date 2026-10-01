"""Check live simulation after warmup without individual draw-call instrumentation."""
from pathlib import Path
import ast,http.server
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
p=Path(__file__).with_name('profile_late_stages.py');s=p.read_text(encoding='utf-8');node=next(n for n in ast.parse(s).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='INSTRUMENT' for t in n.targets))
lines=s.splitlines(keepends=True)
thin=r'''INSTRUMENT=r"""()=>{
 window.__profiles={};window.__images={};window.__samples=[];window.__deltas=[];window.__prev=0;
 const own=loop;loop=function(t){const p=performance.now();if(window.__prev)window.__deltas.push(t-window.__prev);window.__prev=t;try{return own(t);}finally{window.__samples.push(performance.now()-p);}};
 window.playerHit=function(){};
}"""
'''
s=''.join(lines[:node.lineno-1])+thin+''.join(lines[node.end_lineno:])
s=s.replace('for stage in [1,6,7,8]:','for stage in [5,6,7,8]:')
s=s.replace('pg.wait_for_timeout(6000)', '''pg.wait_for_timeout(8000)
   pg.evaluate('()=>{window.__samples=[];window.__deltas=[];window.__prev=0;}')
   pg.wait_for_timeout(6000)''')
exec(compile(s,str(p),'exec'))
