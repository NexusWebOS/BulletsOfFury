from pathlib import Path
p=Path(__file__).with_name('night_weather_final_probe_1116.py');s=p.read_text(encoding='utf8')
needle=" p.evaluate('()=>{drawWorld(0);SC12.refresh()}');"
probe=""" q['fallbacks']=p.evaluate('''()=>{const rows=[];for(const mode of['rotation','reflection','shadow','filter','copy']){function render(fn){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalCompositeOperation='source-over';ctx.filter='none';ctx.shadowBlur=0;ctx.fillStyle='#1a3447';ctx.fillRect(0,0,cv.width,cv.height);ctx.setTransform(SS,0,0,SS,0,0);if(mode==='rotation')ctx.rotate(.12);if(mode==='reflection')ctx.scale(-1,1);if(mode==='shadow'){ctx.shadowBlur=5;ctx.shadowColor='#22ff33';}if(mode==='filter')ctx.filter='blur(2px)';if(mode==='copy')ctx.globalCompositeOperation='copy';const a=NW16.skipped;fn();const skip=NW16.skipped-a;ctx.restore();return{data:ctx.getImageData(0,0,cv.width,cv.height).data,skip};}const a=render(NW16.base.weather),b=render(th114Weather);let different=0;for(let i=0;i<a.data.length;i++)if(a.data[i]!==b.data[i])different++;rows.push({mode,different,skipped:b.skip});}return rows;}''')
 assert all(r['different']==0 and r['skipped']==0 for r in q['fallbacks'])
"""
assert needle in s;s=s.replace(needle,probe+needle)
(p.parent/'night_weather_fallback_probe_1116.py').write_text(s,encoding='utf8',newline='\n')
