from pathlib import Path
from PIL import Image
import hashlib,json
R=Path(__file__).resolve().parents[1];path='assets/game/levels/stage_06/boss/thunderhead_reactor_1105/page_155.png';im=Image.open(R/path).convert('RGBA');blank=[92,0,2,2];assert im.crop((92,0,94,2)).getchannel('A').getextrema()==(0,0)
record={'bank':'beam_coupling_tail','frame':5,'key':'tc119_page_155','path':path,'sha256':hashlib.sha256((R/path).read_bytes()).hexdigest(),'before':[556,0,2,2],'after':blank,'proof':'Existing end frame is entirely beyond the source page and draws no pixels. The replacement rectangle is wholly transparent; destination offsets, original page and every visible frame remain unchanged.'}
p=R/'_ART_SOURCES/cinema_overnight_1116/empty-frame.json';p.write_text(json.dumps(record,indent=2)+'\n',encoding='utf8',newline='\n')
p=R/'assets/night_city_atlas_1116.js';s=p.read_text(encoding='utf8');marker='// Keep the authored empty end frame inside its actual atlas page.'
if marker not in s:s+='\n'+marker+'\nconst NQA16_EMPTY='+json.dumps(record,separators=(',',':'))+';\n{const c=TC119_ART.banks.beam_coupling_tail.cells[5];if(c[0]===NQA16_EMPTY.key&&c[1]===556&&c[2]===0&&c[3]===2&&c[4]===2){c[1]=92;c[2]=0;}}\n';p.write_text(s,encoding='utf8',newline='\n')
p=R/'index.html';s=p.read_text(encoding='utf8').replace('assets/night_city_atlas_1116.js?v=1','assets/night_city_atlas_1116.js?v=2');p.write_text(s,encoding='utf8',newline='\n');print('Registered the verified transparent end frame without changing any image pixels')
