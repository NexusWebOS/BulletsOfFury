from pathlib import Path
p=Path(__file__).with_name('night_missile_stats_physical_1116.py');s=p.read_text(encoding='utf8')
needle="  p.goto('http://127.0.0.1:8765/index.html?night-missile-stats=1116');"
# The goto shares a source line with page creation; insert by its actual token.
needle="p.goto('http://127.0.0.1:8765/index.html?night-missile-stats=1116');"
new="p.route('**/assets/online-config.js*',lambda r:r.fulfill(status=200,content_type='application/javascript',body='window.BOF_ONLINE_CONFIG={};'));"+needle
assert needle in s;s=s.replace(needle,new).replace("O/'physical-shipping.json'","O/'physical-offline.json'")
s=s.replace('Tests accounting, not campaign wins.', 'Optional online configuration disabled only in these browser contexts after an external429 interrupted the online-enabled fixture; shipping online code remains unchanged. Tests accounting, not campaign wins.')
(p.parent/'night_missile_stats_offline_1116.py').write_text(s,encoding='utf8',newline='\n')
